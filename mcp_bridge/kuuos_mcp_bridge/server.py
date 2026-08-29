from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mcp.server import MCPServer

from .state_store import JsonStateStore, StateConflictError


STATE_PATH = Path(os.environ.get("KUUOS_MCP_STATE_PATH", "./var/kuuos-mcp-state.json"))
store = JsonStateStore(STATE_PATH)
mcp = MCPServer(
    "KuuOS Chat-Work State Bridge",
    instructions=(
        "Use this server as the canonical continuation-state bridge shared by "
        "Chat and Work. Read before writing. Every write must pass the version "
        "returned by the preceding read as expected_version. On conflict, read "
        "again and reconcile rather than overwriting blindly."
    ),
)


@mcp.tool()
def get_project_state() -> dict[str, Any]:
    """Read the canonical shared project state, including its CAS version."""
    return store.read()


@mcp.tool()
def update_project_state(
    expected_version: int,
    actor: str,
    patch_json: str,
) -> dict[str, Any]:
    """CAS-update canonical state from a JSON object patch.

    Read get_project_state first and pass its version as expected_version.
    actor should identify the writing surface, for example `chat` or `work`.
    """
    patch = json.loads(patch_json)
    if not isinstance(patch, dict):
        raise ValueError("patch_json must decode to a JSON object")
    try:
        return store.update(patch, expected_version=expected_version, actor=actor)
    except StateConflictError as exc:
        return {
            "ok": False,
            "conflict": True,
            "message": str(exc),
            "current": store.read(),
        }


@mcp.tool()
def record_continuation(
    expected_version: int,
    actor: str,
    canonical_sha: str | None = None,
    mathematical_frontier: str | None = None,
    next_actions_json: str | None = None,
    active_pr_json: str | None = None,
    ci_json: str | None = None,
) -> dict[str, Any]:
    """Write the common continuation fields used to hand work across surfaces."""
    patch: dict[str, Any] = {}
    if canonical_sha is not None:
        patch["canonical_sha"] = canonical_sha
    if mathematical_frontier is not None:
        patch["mathematical_frontier"] = mathematical_frontier
    if next_actions_json is not None:
        next_actions = json.loads(next_actions_json)
        if not isinstance(next_actions, list) or not all(
            isinstance(item, str) for item in next_actions
        ):
            raise ValueError("next_actions_json must decode to a list of strings")
        patch["next_actions"] = next_actions
    if active_pr_json is not None:
        patch["active_pr"] = json.loads(active_pr_json)
    if ci_json is not None:
        patch["ci"] = json.loads(ci_json)
    try:
        return store.update(patch, expected_version=expected_version, actor=actor)
    except StateConflictError as exc:
        return {
            "ok": False,
            "conflict": True,
            "message": str(exc),
            "current": store.read(),
        }


@mcp.tool()
def list_next_actions() -> dict[str, Any]:
    """Return the current state version and ordered next actions."""
    state = store.read()
    return {"version": state["version"], "next_actions": state.get("next_actions", [])}


@mcp.resource("kuuos://state/project", mime_type="application/json")
def canonical_project_state() -> str:
    """Canonical Chat/Work continuation state as JSON."""
    return json.dumps(store.read(), ensure_ascii=False, indent=2, sort_keys=True)


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
