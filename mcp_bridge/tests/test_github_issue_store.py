from __future__ import annotations

import json

import pytest

from kuuos_mcp_bridge.github_issue_store import (
    GitHubIssueStateStore,
    parse_canonical_issue_state,
)


def test_parse_canonical_issue_state_normalizes_frontier() -> None:
    payload = {
        "schema_version": 1,
        "version": 7,
        "project": "KuuOS",
        "repository": "itakura-hidetoshi/KuuOS",
        "canonical_branch": "main",
        "canonical_sha": "abc123",
        "frontier": "continue the bridge",
        "next_actions": ["deploy"],
    }
    body = "before\n```json\n" + json.dumps(payload) + "\n```\nafter"
    state = parse_canonical_issue_state(body)

    assert state["version"] == 7
    assert state["canonical_sha"] == "abc123"
    assert state["mathematical_frontier"] == "continue the bridge"
    assert state["next_actions"] == ["deploy"]
    assert state["updated_by"] == "github-issue"


def test_parse_canonical_issue_state_requires_json_fence() -> None:
    with pytest.raises(ValueError):
        parse_canonical_issue_state("no canonical state here")


def test_github_issue_store_is_read_only() -> None:
    store = GitHubIssueStateStore()
    with pytest.raises(RuntimeError, match="read-only"):
        store.update({"canonical_sha": "nope"}, expected_version=0, actor="chat")
