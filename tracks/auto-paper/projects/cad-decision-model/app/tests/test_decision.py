import asyncio
import base64
import json
import logging
from dataclasses import dataclass
from types import SimpleNamespace

import httpx
import pytest
from typesafe_sdk import Choice, Image, Noul, TypeSafeAPIError, TypeSafeError

import cad_api.decision as decision
from cad_api.decision import create_decision_client


PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl6JfcAAAAASUVORK5CYII=")


def backend(**overrides):
    return {
        "id": "replacement",
        "provider": "decision_http",
        "endpoint": "https://decision.example.test/custom/predict",
        "model": "decision-v2",
        "api_key_env": None,
        **overrides,
    }


def run(coro):
    return asyncio.run(coro)


def invoke(handler, questions=None, *, config=None, state="drawing", extra_headers=None):
    async def operation():
        async with create_decision_client(config or backend(), transport=httpx.MockTransport(handler)) as client:
            return await client.system_one(
                state,
                questions or {"link": Noul(instructions="Are the endpoints connected?")},
                model="historical-jev-default",
                extra_headers=extra_headers,
            )
    return run(operation())


def test_images_in_state_instructions_and_criteria_stay_separate_and_ordered(monkeypatch, tmp_path):
    monkeypatch.setenv("DECISION_TEST_KEY", "credential-private-123")
    path = tmp_path / "crop.png"
    path.write_bytes(PNG)
    image = Image(path)
    seen = []

    def handler(request):
        assert str(request.url) == "https://decision.example.test/custom/predict"
        assert request.headers["authorization"] == "Bearer credential-private-123"
        assert request.headers["TypeSafe-Danger-Zone-Images"] == "true"
        body = json.loads(request.content)
        seen.append(body)
        assert body["model"] == "decision-v2"
        expected_image = {"type": "image", "mime_type": "image/png", "data": base64.b64encode(PNG).decode()}
        assert body["state"] == {"box_1": expected_image, "box_2": expected_image}
        assert body["questions"]["A"]["instructions"][1] == expected_image
        assert body["questions"]["A"]["criteria"]["1"]["example"] == expected_image
        assert list(body["questions"]["A"]["criteria"]) == ["1", "2"]
        assert list(body["questions"]["B"]["criteria"]) == ["2", "1"]
        return httpx.Response(200, json={"model": "decision-v2-served", "answers": {"A": {"2": 0.3, "1": 0.7}, "B": {"1": 0.6, "2": 0.4}, "K3": 0.8}, "usage": {"input_tokens": 42}})

    result = invoke(
        handler,
        {
            "A": Choice(instructions=["Choose", image], criteria={"1": {"example": image}, "2": None}),
            "B": Choice(instructions="Swapped choice", criteria={"2": image, "1": None}),
            "K3": Noul(instructions="Connected?", criteria={"true": [image], "false": "broken"}),
        },
        config=backend(api_key_env="DECISION_TEST_KEY"),
        state={"box_1": image, "box_2": image},
        extra_headers={"TypeSafe-Danger-Zone-Images": "true", "Authorization": "Bearer attacker", "X-Secret": "never-send"},
    )
    assert len(seen) == 1
    assert result.model == "decision-v2-served"
    assert list(result.choices["A"].probabilities) == ["1", "2"]
    assert list(result.choices["B"].probabilities) == ["2", "1"]
    assert result.nouls["K3"].noul == 0.8
    assert result.usage.input_tokens == 42


@pytest.mark.parametrize("answers", [
    {},
    {"pick": {"a": 1}},
    {"pick": {"a": 0.8, "b": 0.2, "extra": 0}},
    {"pick": {"a": 0.6, "b": 0.2}},
    {"pick": {"a": -0.1, "b": 1.1}},
    {"pick": {"a": True, "b": 0}},
    {"pick": {"a": "0.8", "b": 0.2}},
    {"pick": {"a": 0.8, "b": 0.2}, "unrequested": 0.2},
])
def test_incomplete_or_invalid_categorical_answers_do_not_succeed(answers):
    with pytest.raises(TypeSafeError):
        invoke(lambda request: httpx.Response(200, json={"model": "m", "answers": answers, "usage": {"input_tokens": 0}}), {"pick": Choice(criteria={"a": None, "b": None})})


@pytest.mark.parametrize("raw", ["NaN", "Infinity", "-Infinity", "-0.1", "1.1", "true", '"0.8"'])
def test_invalid_noul_probability_does_not_succeed(raw):
    body = '{"model":"m","answers":{"link":' + raw + '},"usage":{"input_tokens":1}}'
    with pytest.raises(TypeSafeError):
        invoke(lambda request: httpx.Response(200, text=body))


@pytest.mark.parametrize("usage", [{}, {"input_tokens": -1}, {"input_tokens": True}, {"input_tokens": 1.5}, {"input_tokens": None}, None])
def test_invalid_usage_does_not_succeed(usage):
    with pytest.raises(TypeSafeError):
        invoke(lambda request: httpx.Response(200, json={"model": "m", "answers": {"link": 0.8}, "usage": usage}))


def test_distribution_tolerance_is_validated_without_renormalizing():
    result = invoke(lambda request: httpx.Response(200, json={"model": "m", "answers": {"pick": {"a": 0.7, "b": 0.28}}, "usage": {"input_tokens": 0}}), {"pick": Choice(criteria={"a": None, "b": None})})
    assert result.choices["pick"].probabilities == {"a": 0.7, "b": 0.28}


@pytest.mark.parametrize("status", [301, 307, 400, 401, 402, 403, 429, 500])
def test_http_errors_preserve_status_and_redact_sensitive_metadata(status, monkeypatch):
    monkeypatch.setenv("DECISION_TEST_KEY", "super-private-key")
    with pytest.raises(TypeSafeAPIError) as caught:
        invoke(lambda request: httpx.Response(status, json={"error": "super-private-key secret upstream drawing"}, headers={"x-typesafe-request-id": "private-record-id", "location": "https://secret.example.test/?token=private"}), config=backend(api_key_env="DECISION_TEST_KEY"))
    error = caught.value
    assert error.status == status
    for text in (str(error), repr(error), repr(error.args), repr(error.body), repr(error.headers)):
        assert "super-private-key" not in text
        assert "private-record-id" not in text
        assert "secret.example.test" not in text
        assert "secret upstream drawing" not in text
    assert error.request_id is None
    assert error.__cause__ is None
    assert error.__suppress_context__


def test_max_tokens_error_remains_detectable_by_frozen_extractor():
    with pytest.raises(TypeSafeAPIError) as caught:
        invoke(lambda request: httpx.Response(400, json={"error": {"code": "max_tokens_exceeded", "message": "private drawing content"}}))
    assert caught.value.status == 400
    assert "max_tokens" in str(caught.value)
    assert "private drawing content" not in repr(caught.value.args)


@pytest.mark.parametrize("exception_type", [httpx.ReadTimeout, httpx.ConnectError])
def test_transport_error_hides_credentials_urls_and_error_chain(exception_type):
    def handler(request):
        raise exception_type("private-key on https://secret.host/path?token=private", request=request)
    with pytest.raises(TypeSafeError) as caught:
        invoke(handler)
    assert not isinstance(caught.value, TypeSafeAPIError)
    assert "private" not in str(caught.value)
    assert "secret.host" not in repr(caught.value)
    assert caught.value.__cause__ is None
    assert caught.value.__suppress_context__


@pytest.mark.parametrize("endpoint", ["file:///secrets", "https://user:password@example.test/predict", "https://example.test/?token=secret", "https://example.test/#secret"])
def test_endpoint_cannot_embed_credentials(endpoint):
    with pytest.raises(TypeSafeError):
        create_decision_client(backend(endpoint=endpoint))


def test_missing_credential_fails_before_any_request(monkeypatch):
    monkeypatch.delenv("MISSING_DECISION_TEST_KEY", raising=False)
    with pytest.raises(TypeSafeError, match="credential is not configured"):
        create_decision_client(backend(api_key_env="MISSING_DECISION_TEST_KEY"))


@dataclass
class BackendConfig:
    id: str = "native"
    provider: str = "typesafe"
    endpoint: str = "https://custom.typesafe.test"
    model: str = "native-model-v3"
    api_key_env: str = "NATIVE_DECISION_TEST_KEY"
    timeout_seconds: float = 23
    concurrency: int = 2


def test_native_sdk_receives_configured_model_root_and_original_images(monkeypatch):
    monkeypatch.setenv("NATIVE_DECISION_TEST_KEY", "native-private-key")
    captured = {}

    class Native:
        def __init__(self, **kwargs):
            captured["init"] = kwargs
        async def system_one(self, **kwargs):
            captured["call"] = kwargs
            return SimpleNamespace(model="native-served", choices={"pick": SimpleNamespace(probabilities={"x": 0.9, "y": 0.1})}, nouls={"link": SimpleNamespace(noul=0.7)}, usage=SimpleNamespace(input_tokens=12))
        async def aclose(self):
            captured["closed"] = True

    monkeypatch.setattr(decision, "_NativeTypeSafeClient", Native)
    image = Image(PNG)
    questions = {"pick": Choice(criteria={"x": image, "y": None}), "link": Noul(instructions="Connected?")}
    async def operation():
        async with create_decision_client(BackendConfig()) as client:
            return await client.system_one(state={"crop": image}, questions=questions, model="obsolete-jev")
    result = run(operation())
    assert captured["init"]["base_url"] == "https://custom.typesafe.test"
    assert captured["init"]["api_key"] == "native-private-key"
    assert captured["init"]["timeout"] == 23
    assert captured["init"]["retry"].max_retries == 0
    assert captured["call"]["model"] == "native-model-v3"
    assert captured["call"]["state"]["crop"] is image
    assert captured["call"]["questions"] is questions
    assert captured["closed"]
    assert result.nouls["link"].noul == 0.7


@pytest.mark.parametrize("failure", [
    TypeSafeAPIError(401, {"error": "native-private-key"}, {"x-typesafe-request-id": "private-native-id"}),
    TypeSafeAPIError(400, {"error": "max_tokens_exceeded native-private-key"}, {}),
    TypeSafeError("native-private-key https://private.example.test"),
])
def test_native_sdk_error_redaction_preserves_fatal_and_token_limit_behavior(monkeypatch, failure):
    monkeypatch.setenv("NATIVE_DECISION_TEST_KEY", "native-private-key")
    class Native:
        def __init__(self, **kwargs):
            pass
        async def system_one(self, **kwargs):
            raise failure
        async def aclose(self):
            pass
    monkeypatch.setattr(decision, "_NativeTypeSafeClient", Native)
    async def operation():
        async with create_decision_client(BackendConfig()) as client:
            return await client.system_one("drawing", {"link": Noul(instructions="Connected?")})
    with pytest.raises(TypeSafeError) as caught:
        run(operation())
    assert "native-private-key" not in str(caught.value)
    assert "private-native-id" not in repr(caught.value.args)
    if isinstance(failure, TypeSafeAPIError):
        assert caught.value.status == failure.status
        if failure.status == 400:
            assert "max_tokens" in str(caught.value)


def test_native_sdk_missing_answers_are_not_accepted(monkeypatch):
    monkeypatch.setenv("NATIVE_DECISION_TEST_KEY", "native-private-key")
    class Native:
        def __init__(self, **kwargs):
            pass
        async def system_one(self, **kwargs):
            return SimpleNamespace(model="m", choices={}, nouls={}, usage=SimpleNamespace(input_tokens=0))
        async def aclose(self):
            pass
    monkeypatch.setattr(decision, "_NativeTypeSafeClient", Native)
    async def operation():
        async with create_decision_client(BackendConfig()) as client:
            return await client.system_one("drawing", {"link": Noul(instructions="Connected?")})
    with pytest.raises(TypeSafeError):
        run(operation())


def test_official_sdk_transport_and_body_logs_are_safe(monkeypatch, caplog):
    import httpx2

    monkeypatch.setenv("NATIVE_DECISION_TEST_KEY", "native-private-key")
    def handler(request):
        assert str(request.url) == "https://custom.typesafe.test/v1/systemone"
        assert request.headers["authorization"] == "Bearer native-private-key"
        body = json.loads(request.content)
        assert body["model"] == "native-model-v3"
        assert list(body["questions"]["pick"]["criteria"]) == ["y", "x"]
        return httpx2.Response(200, json={"model": "native-model-v3", "answers": {"pick": {"type": "choice", "choice": "x", "confidence": 0.6, "probabilities": {"x": 0.8, "y": 0.2}}}, "usage": {"input_tokens": 5, "output_tokens": 0}}, headers={"x-typesafe-request-id": "private-record-id"})

    async def operation():
        async with create_decision_client(BackendConfig(), transport=httpx2.MockTransport(handler)) as client:
            return await client.system_one("private drawing content", {"pick": Choice(criteria={"y": None, "x": None})}, model="obsolete-jev")
    with caplog.at_level(logging.DEBUG, logger="typesafe_sdk"):
        result = run(operation())
    assert result.choices["pick"].probabilities == {"y": 0.2, "x": 0.8}
    assert "private drawing content" not in caplog.text
    assert "private-record-id" not in caplog.text
    assert "native-private-key" not in caplog.text
