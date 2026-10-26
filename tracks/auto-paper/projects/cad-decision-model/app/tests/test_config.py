from pathlib import Path

from cad_api.config import PACKAGE_ROOT, Settings


def test_server_resources_are_explicitly_configurable(monkeypatch, tmp_path):
    # Keep this test independent of local credentials and .env files.
    monkeypatch.setattr('cad_api.config.load_dotenv', lambda *_args, **_kwargs: None)
    monkeypatch.delenv('CAD_MODEL_BACKENDS_FILE', raising=False)
    monkeypatch.setenv('CAD_MODEL_PROVIDER', 'decision_http')
    monkeypatch.setenv('CAD_MODEL_ENDPOINT', 'http://localhost:9000/decide')
    monkeypatch.delenv('CAD_RESOURCES_DIR', raising=False)
    assert Settings.from_env().resources_dir == (PACKAGE_ROOT / 'resources').resolve()
    resources = tmp_path / 'legends'
    monkeypatch.setenv('CAD_RESOURCES_DIR', str(resources))
    assert Settings.from_env().resources_dir == resources.resolve()


def test_graph_revision_is_default_but_previous_versions_remain_selectable(monkeypatch):
    monkeypatch.setattr('cad_api.config.load_dotenv', lambda *_args, **_kwargs: None)
    monkeypatch.delenv('CAD_MODEL_BACKENDS_FILE', raising=False)
    monkeypatch.delenv('CAD_ALGORITHM_REVISION', raising=False)
    monkeypatch.setenv('CAD_MODEL_PROVIDER', 'decision_http')
    monkeypatch.setenv('CAD_MODEL_ENDPOINT', 'http://localhost:9000/decide')
    assert Settings.from_env().algorithm_revision == 'geometry-local-route-v15-semantics'
    for revision in ('geometry-local-route-v12', 'geometry-local-route-v13-connections', 'geometry-local-route-v14-graph'):
        monkeypatch.setenv('CAD_ALGORITHM_REVISION', revision)
        assert Settings.from_env().algorithm_revision == revision
