from __future__ import annotations

import base64
from types import SimpleNamespace

import pytest

from kuuos_mcp_bridge import event_bootstrap
from kuuos_mcp_bridge.event_subscriptions import MemorySubscriptionStore
from kuuos_mcp_bridge.github_event_contract import CI_EVENT, MGAP_REPO


def fake_state_backend():
    x = object.__new__(event_bootstrap.PostgresStateStore)
    x.database_url = "postgresql://isolated-fixture"
    return x


def configure_allowed(monkeypatch):
    monkeypatch.setenv("KUUOS_MCP_EVENTS_ALLOWED_SUBJECTS", "owner-1")
    monkeypatch.setenv("KUUOS_MCP_EVENTS_ALLOWED_REPOS", MGAP_REPO)
    monkeypatch.setenv(
        "KUUOS_MCP_EVENTS_ENCRYPTION_KEY",
        base64.b64encode(b"m" * 32).decode("ascii"),
    )


def test_requires_oauth_and_durable_backend(monkeypatch):
    configure_allowed(monkeypatch)
    with pytest.raises(RuntimeError, match="OAuth"):
        event_bootstrap.configure_mcp_events(None, None, fake_state_backend())
    with pytest.raises(RuntimeError, match="PostgreSQL"):
        event_bootstrap.configure_mcp_events(None, object(), object())


def test_rejects_missing_owner_and_repository_allowlists(monkeypatch):
    with pytest.raises(RuntimeError, match="subject"):
        event_bootstrap.configure_mcp_events(None, object(), fake_state_backend())
    monkeypatch.setenv("KUUOS_MCP_EVENTS_ALLOWED_SUBJECTS", "owner-1")
    with pytest.raises(RuntimeError, match="repository allowlist"):
        event_bootstrap.configure_mcp_events(None, object(), fake_state_backend())


def test_rejects_wildcards_and_unknown_repository(monkeypatch):
    configure_allowed(monkeypatch)
    monkeypatch.setenv("KUUOS_MCP_EVENTS_ALLOWED_SUBJECTS", "*")
    with pytest.raises(RuntimeError, match="invalid or wildcard"):
        event_bootstrap.configure_mcp_events(None, object(), fake_state_backend())
    monkeypatch.setenv("KUUOS_MCP_EVENTS_ALLOWED_SUBJECTS", "owner-1")
    monkeypatch.setenv("KUUOS_MCP_EVENTS_ALLOWED_REPOS", "someone/foreign")
    with pytest.raises(RuntimeError, match="repository allowlist"):
        event_bootstrap.configure_mcp_events(None, object(), fake_state_backend())


def test_missing_encryption_key_prevents_subscription_activation(monkeypatch):
    configure_allowed(monkeypatch)
    monkeypatch.delenv("KUUOS_MCP_EVENTS_ENCRYPTION_KEY")
    with pytest.raises(RuntimeError, match="encryption key missing"):
        event_bootstrap.configure_mcp_events(None, object(), fake_state_backend())


def test_validated_config_passes_typed_manager_to_handler_installer(monkeypatch):
    configure_allowed(monkeypatch)
    installed = []
    monkeypatch.setattr(
        event_bootstrap, "PostgresSubscriptionStore",
        lambda *args: MemorySubscriptionStore(),
    )
    monkeypatch.setattr(
        event_bootstrap, "install_mcp_event_methods",
        lambda mcp, manager: installed.append((mcp, manager)),
    )
    dummy = object()
    manager = event_bootstrap.configure_mcp_events(dummy, object(), fake_state_backend())
    assert installed == [(dummy, manager)]
    assert manager.authorize("owner-1", CI_EVENT, {"repository": MGAP_REPO})
    assert not manager.authorize("intruder", CI_EVENT, {"repository": MGAP_REPO})
    assert not manager.authorize("owner-1", CI_EVENT, {"repository": "example/other"})


def test_rejects_unverified_sdk_version_before_activating_events(monkeypatch):
    configure_allowed(monkeypatch)
    monkeypatch.setattr(
        event_bootstrap, "installed_package_version", lambda name: "2.99.0"
    )
    with pytest.raises(RuntimeError, match="version-bound adapter requires mcp==2.3.0"):
        event_bootstrap.configure_mcp_events(None, object(), fake_state_backend())

def test_sdk_distribution_matches_packaged_events_pin():
    """The installed SDK and deploy manifests must be version-aligned."""
    from importlib.metadata import version
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    sdk = event_bootstrap.MCP_EVENTS_SDK_PIN
    assert sdk == "2.3.0"
    assert version("mcp") == sdk
    assert f'"mcp=={sdk}"' in (root / "pyproject.toml").read_text()
    assert f"mcp=={sdk}" in (root / "requirements.txt").read_text().splitlines()


def test_runtime_pyproject_provisions_postgres_driver_without_extra():
    """Vercel builds from pyproject.toml; PostgreSQL is not optional there."""
    import tomllib
    from pathlib import Path
    from importlib.metadata import version

    root = Path(__file__).resolve().parents[1]
    document = tomllib.loads((root / "pyproject.toml").read_text())
    dependencies = document["project"]["dependencies"]
    declared = "psycopg[binary]>=3.2,<4"
    assert declared in dependencies
    assert declared in (root / "requirements.txt").read_text().splitlines()
    assert version("psycopg").startswith("3.")
