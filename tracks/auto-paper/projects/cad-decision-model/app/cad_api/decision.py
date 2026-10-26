"""Interchangeable decision endpoints with the extractor's SDK-shaped interface.

``typesafe`` uses the pinned official SDK and its API-root ``base_url``.
``decision_http`` posts the normalized contract to the configured *full* URL.
Images remain separate assets, including images nested in option descriptions.
The configured model is authoritative; the extractor's historical default is
ignored. Errors expose neither backend response bodies nor credentials.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import math
import os
from collections.abc import Mapping
from dataclasses import dataclass
from types import TracebackType
from typing import Any
from urllib.parse import urlsplit

import httpx
from typesafe_sdk import (
    AsyncTypeSafeClient as _NativeTypeSafeClient,
    Image,
    RetryPolicy,
    TypeSafeAPIError,
    TypeSafeError,
)


class _NoSDKWireLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # SDK debug records contain complete request/response bodies, and INFO
        # records contain upstream request IDs. The server exposes safe status
        # and stage counts instead, even when its own debug logging is enabled.
        return record.levelno >= logging.WARNING


logging.getLogger("typesafe_sdk").addFilter(_NoSDKWireLogs())


@dataclass(frozen=True)
class DecisionChoice:
    probabilities: dict[str, float]


@dataclass(frozen=True)
class DecisionNoul:
    noul: float


@dataclass(frozen=True)
class DecisionUsage:
    input_tokens: int | None


@dataclass(frozen=True)
class DecisionResponse:
    model: str
    choices: dict[str, DecisionChoice]
    nouls: dict[str, DecisionNoul]
    usage: DecisionUsage


def _setting(backend: Any, name: str, default: Any = None) -> Any:
    if isinstance(backend, Mapping):
        return backend.get(name, default)
    return getattr(backend, name, default)


def _config(backend: Any) -> tuple[str, str, str, str | None, float, int]:
    provider = _setting(backend, "provider")
    endpoint = _setting(backend, "endpoint")
    model = _setting(backend, "model")
    if provider not in {"typesafe", "decision_http"}:
        raise TypeSafeError("Unsupported decision backend provider.")
    if not isinstance(endpoint, str) or not endpoint.strip() or any(character.isspace() for character in endpoint):
        raise TypeSafeError("A decision backend endpoint is required.")
    try:
        parsed = urlsplit(endpoint)
        valid = (
            parsed.scheme in {"http", "https"}
            and parsed.hostname
            and parsed.username is None
            and parsed.password is None
            and not parsed.query
            and not parsed.fragment
        )
        _ = parsed.port
    except ValueError:
        valid = False
    if not valid:
        raise TypeSafeError("Decision endpoint must be an HTTP(S) URL without embedded credentials, query or fragment.")
    if not isinstance(model, str) or not model.strip():
        raise TypeSafeError("A decision backend model is required.")
    timeout = _setting(backend, "timeout_seconds", 90)
    concurrency = _setting(backend, "concurrency", 8)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise TypeSafeError("Decision timeout must be a positive finite number.")
    if isinstance(concurrency, bool) or not isinstance(concurrency, int) or concurrency < 1:
        raise TypeSafeError("Decision concurrency must be a positive integer.")
    key_env = _setting(backend, "api_key_env")
    key = None
    if key_env is not None:
        if not isinstance(key_env, str) or not key_env:
            raise TypeSafeError("Invalid decision credential environment setting.")
        key = os.environ.get(key_env, "").strip()
        if not key:
            raise TypeSafeError("Decision backend credential is not configured.")
        if not key.isascii() or any(character.isspace() or ord(character) < 32 or ord(character) == 127 for character in key):
            raise TypeSafeError("Decision backend credential has an invalid format.")
    if provider == "typesafe" and key is None:
        raise TypeSafeError("TypeSafe backend requires an explicit credential environment setting.")
    return provider, endpoint, model, key, float(timeout), concurrency


def _questions(questions: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    if not isinstance(questions, Mapping) or not questions:
        raise TypeSafeError("Decision request must include questions.")
    result = {}
    for name, question in questions.items():
        if not isinstance(name, str) or not name:
            raise TypeSafeError("Decision question names must be nonempty strings.")
        if isinstance(question, Mapping):
            kind, instructions, criteria = (question.get(field) for field in ("type", "instructions", "criteria"))
        else:
            kind = getattr(question, "type", None)
            instructions = getattr(question, "instructions", None)
            criteria = getattr(question, "criteria", None)
        if kind not in {"choice", "noul"}:
            raise TypeSafeError("Decision request supports choice and noul questions only.")
        if kind == "choice" and (
            not isinstance(criteria, Mapping)
            or not criteria
            or any(not isinstance(label, str) or not label for label in criteria)
        ):
            raise TypeSafeError("Decision choice must include named alternatives.")
        if kind == "noul" and criteria is not None and not isinstance(criteria, Mapping):
            raise TypeSafeError("Decision noul criteria must be a mapping.")
        result[name] = {"type": kind, "instructions": instructions, "criteria": criteria}
    return result


async def _serialize(value: Any) -> Any:
    """Walk the content without Pydantic replacing SDK images with references."""
    if isinstance(value, Image):
        try:
            # The SDK is pinned to 0.7.5. This resolves bytes and MIME exactly as
            # its native multipart transport does, including lazily read paths.
            resolved = await value._resolve_async()
            return {
                "type": "image",
                "mime_type": resolved.content_type,
                "data": base64.b64encode(resolved.data).decode("ascii"),
            }
        except Exception:
            raise TypeSafeError("Decision request contains an unreadable image.") from None
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise TypeSafeError("Decision request contains a nonfinite number.")
        return value
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise TypeSafeError("Decision content mapping keys must be strings.")
        return {key: await _serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [await _serialize(item) for item in value]
    raise TypeSafeError("Decision request contains unsupported content.")


def _probability(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise TypeSafeError("Decision backend returned an invalid probability.")
    return float(value)


def _response(model: Any, answers: Any, usage: Any, questions: Mapping[str, Any], *, allow_unknown_usage: bool = False) -> DecisionResponse:
    if not isinstance(model, str) or not model.strip():
        raise TypeSafeError("Decision backend returned an invalid model identifier.")
    if not isinstance(answers, Mapping) or set(answers) != set(questions):
        raise TypeSafeError("Decision backend must return exactly one answer for every question.")
    choices, nouls = {}, {}
    for name, question in questions.items():
        answer = answers[name]
        if question["type"] == "choice":
            criteria = question["criteria"]
            if not isinstance(answer, Mapping) or set(answer) != set(criteria):
                raise TypeSafeError("Decision choice answer must match its requested alternatives.")
            probabilities = {label: _probability(answer[label]) for label in criteria}
            if not math.isclose(math.fsum(probabilities.values()), 1, rel_tol=0, abs_tol=0.02000000001):
                raise TypeSafeError("Decision choice probabilities must sum to one within 0.02.")
            choices[name] = DecisionChoice(probabilities)
        else:
            nouls[name] = DecisionNoul(_probability(answer))
    if not isinstance(usage, Mapping) or "input_tokens" not in usage:
        raise TypeSafeError("Decision backend must report input_tokens usage.")
    tokens = usage["input_tokens"]
    if tokens is None and not allow_unknown_usage:
        raise TypeSafeError("Decision backend must report input_tokens usage.")
    if tokens is not None and (isinstance(tokens, bool) or not isinstance(tokens, int) or tokens < 0):
        raise TypeSafeError("Decision backend returned invalid token usage.")
    return DecisionResponse(model, choices, nouls, DecisionUsage(tokens))


def _api_error(status: int, *, token_limit: bool = False) -> TypeSafeAPIError:
    message = "max_tokens_exceeded" if status == 400 and token_limit else "Decision backend request failed."
    # Empty metadata intentionally strips arbitrary upstream body, URL and
    # request-id strings, which are otherwise logged by the frozen extractor.
    return TypeSafeAPIError(status, {"error": message}, {}, message=message)


def _has_token_limit(body: Any) -> bool:
    if isinstance(body, str):
        return "max_tokens" in body.lower()
    if isinstance(body, Mapping):
        return any(_has_token_limit(value) for value in body.values())
    if isinstance(body, (list, tuple)):
        return any(_has_token_limit(value) for value in body)
    return False


def _headers(extra_headers: Mapping[str, str] | None) -> dict[str, str]:
    # The extractor supplies this feature flag. An arbitrary caller cannot
    # override host/auth or make credentials appear in an HTTP debug log.
    return {
        "TypeSafe-Danger-Zone-Images": "true"
    } if extra_headers and any(key.lower() == "typesafe-danger-zone-images" and value == "true" for key, value in extra_headers.items()) else {}


class DecisionClient:
    """SDK-shaped client for a configured interchangeable model backend."""

    def __init__(self, backend: Any, *, transport: Any = None) -> None:
        provider, endpoint, model, key, timeout, concurrency = _config(backend)
        self.model = model
        self._provider, self._endpoint = provider, endpoint
        self._sem = asyncio.Semaphore(concurrency)
        if provider == "typesafe":
            try:
                self._client = _NativeTypeSafeClient(
                    api_key=key,
                    base_url=endpoint,
                    model=model,
                    timeout=timeout,
                    retry=RetryPolicy(max_retries=0),
                    compression=False,
                    transport=transport,
                )
            except Exception:
                raise TypeSafeError("Decision backend client could not be initialized.") from None
        else:
            headers = {"Authorization": f"Bearer {key}"} if key is not None else {}
            self._client = httpx.AsyncClient(
                timeout=timeout,
                headers=headers,
                transport=transport,
                follow_redirects=False,
                trust_env=False,
            )

    async def system_one(
        self,
        state: Any,
        questions: Mapping[str, Any],
        *,
        model: str | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> DecisionResponse:
        normalized = _questions(questions)
        async with self._sem:
            if self._provider == "typesafe":
                try:
                    result = await self._client.system_one(
                        state=state,
                        questions=questions,
                        model=self.model,
                        extra_headers=_headers(extra_headers),
                    )
                    answers = {name: item.probabilities for name, item in result.choices.items()}
                    answers.update({name: item.noul for name, item in result.nouls.items()})
                    return _response(result.model, answers, {"input_tokens": result.usage.input_tokens}, normalized, allow_unknown_usage=True)
                except TypeSafeAPIError as error:
                    raise _api_error(error.status, token_limit=_has_token_limit(error.body) or "max_tokens" in str(error).lower()) from None
                except Exception:
                    raise TypeSafeError("Decision backend transport or response validation failed.") from None
            payload = {"model": self.model, "state": await _serialize(state), "questions": await _serialize(normalized)}
            try:
                response = await self._client.post(self._endpoint, json=payload, headers=_headers(extra_headers))
            except httpx.TimeoutException:
                raise TypeSafeError("Decision backend request timed out.") from None
            except Exception:
                raise TypeSafeError("Decision backend transport failed.") from None
            if response.is_error or response.is_redirect:
                token_limit = response.status_code == 400 and "max_tokens" in response.text.lower()
                raise _api_error(response.status_code, token_limit=token_limit) from None
            try:
                body = response.json()
            except ValueError:
                raise TypeSafeError("Decision backend returned invalid JSON.") from None
            if not isinstance(body, Mapping):
                raise TypeSafeError("Decision backend returned an invalid response.")
            return _response(body.get("model"), body.get("answers"), body.get("usage"), normalized)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def close(self) -> None:
        await self.aclose()

    async def __aenter__(self) -> DecisionClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()


def create_decision_client(backend: Any, *, transport: Any = None) -> DecisionClient:
    """Create an adapter from a Backend dataclass or equivalent mapping."""
    return DecisionClient(backend, transport=transport)
