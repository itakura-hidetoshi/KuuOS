"""Fail-closed PostgreSQL schema-mode policy, independent of live databases."""
from __future__ import annotations

import pytest

from kuuos_mcp_bridge.db_schema_mode import schema_is_preprovisioned, verify_preprovisioned_schema


def test_default_mode_retains_additive_migration(monkeypatch):
    monkeypatch.delenv("KUUOS_MCP_SCHEMA_MODE", raising=False)
    assert schema_is_preprovisioned() is False


def test_explicit_preprovisioned_mode(monkeypatch):
    monkeypatch.setenv("KUUOS_MCP_SCHEMA_MODE", "preprovisioned")
    assert schema_is_preprovisioned() is True


@pytest.mark.parametrize("value", ["", "true", "PREPROVISIONED", "*", "managed"])
def test_unknown_mode_fails_closed(monkeypatch, value):
    monkeypatch.setenv("KUUOS_MCP_SCHEMA_MODE", value)
    with pytest.raises(RuntimeError, match="must be"):
        schema_is_preprovisioned()


def test_unrecognized_table_name_rejected_without_database():
    with pytest.raises(RuntimeError, match="table_unrecognized"):
        verify_preprovisioned_schema(
            None, table="other_application", columns={"x": ("text", True)}
        )
