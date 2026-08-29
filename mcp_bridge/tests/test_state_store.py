from __future__ import annotations

import json
from pathlib import Path

import pytest

from kuuos_mcp_bridge.state_store import (
    InvalidStatePatch,
    JsonStateStore,
    StateConflictError,
)


def test_default_state_is_version_zero(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path / "state.json")
    state = store.read()
    assert state["version"] == 0
    assert state["project"] == "KuuOS"


def test_update_is_persisted_and_versioned(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    store = JsonStateStore(path)
    state = store.update(
        {"canonical_sha": "abc123", "next_actions": ["continue"]},
        expected_version=0,
        actor="chat",
    )
    assert state["version"] == 1
    assert state["canonical_sha"] == "abc123"
    assert state["updated_by"] == "chat"
    assert JsonStateStore(path).read()["version"] == 1
    json.loads(path.read_text(encoding="utf-8"))


def test_stale_writer_cannot_overwrite(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path / "state.json")
    store.update({"canonical_sha": "first"}, expected_version=0, actor="chat")
    with pytest.raises(StateConflictError):
        store.update({"canonical_sha": "stale"}, expected_version=0, actor="work")
    assert store.read()["canonical_sha"] == "first"


def test_protected_fields_cannot_be_patched(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path / "state.json")
    with pytest.raises(InvalidStatePatch):
        store.update({"version": 99}, expected_version=0, actor="chat")
