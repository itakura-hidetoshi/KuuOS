#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_development_mcp_capability_routing_v7_24 import (
    BLOCKED,
    PARTIAL,
    READY,
    route_development_mcp_task,
)

REGISTRY = ROOT / "manifests" / "kuuos_development_mcp_capability_registry_v7_16.json"


def registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def env(*, writes: bool = False, unavailable: list[str] | None = None) -> dict:
    return {
        "unavailable_server_ids": unavailable or [],
        "sentry_project_configured": False,
        "github_write_authority_ready": writes,
        "workspace_write_authority_ready": writes,
        "browser_effect_authority_ready": writes,
        "mcp_orchestration_authority_ready": writes,
        "vercel_write_authority_ready": writes,
        "supabase_write_authority_ready": writes,
        "neon_write_authority_ready": writes,
    }


def ids(result) -> list[str]:
    return [route["server_id"] for route in result.routes]


def by_id(result) -> dict[str, dict]:
    return {route["server_id"]: route for route in result.routes}


def test_lean_ci_repair_uses_minimal_repository_semantic_route() -> None:
    result = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "lean-red",
            "task_kind": "lean_ci_repair",
            "target_path": "formal/KUOS/Test.lean",
            "request_write": False,
        },
        environment=env(),
    )
    assert result.status == READY, result.to_dict()
    assert ids(result) == [
        "github_official",
        "filesystem_reference",
        "lean_lsp",
        "git_reference",
    ]
    assert "playwright" not in ids(result)
    assert "docker_mcp_gateway" not in ids(result)
    routes = by_id(result)
    assert routes["github_official"]["fact_authority"] == "remote_repository_and_ci_state"
    assert routes["filesystem_reference"]["fact_authority"] == "current_working_bytes"
    assert routes["lean_lsp"]["fact_authority"] == "lean_semantic_state_for_bound_bytes"


def test_external_docs_are_added_only_when_requested() -> None:
    plain = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "lean-no-docs",
            "task_kind": "lean_ci_repair",
            "target_path": "formal/KUOS/Test.lean",
        },
        environment=env(),
    )
    assert "context7" not in ids(plain)

    with_docs = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "lean-with-docs",
            "task_kind": "lean_ci_repair",
            "target_path": "formal/KUOS/Test.lean",
            "needs_external_docs": True,
        },
        environment=env(),
    )
    assert "context7" in ids(with_docs)
    assert by_id(with_docs)["context7"]["role"] == "corroborating"


def test_mcp_spec_prefers_official_docs() -> None:
    result = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "mcp-spec",
            "task_kind": "mcp_spec_research",
        },
        environment=env(),
    )
    assert result.status == READY
    assert ids(result) == ["mcp_docs", "context7", "mcp_fetch"]
    routes = by_id(result)
    assert routes["mcp_docs"]["role"] == "primary"
    assert routes["mcp_docs"]["fact_authority"] == "current_mcp_specification"
    assert routes["context7"]["role"] == "corroborating"
    assert routes["mcp_fetch"]["role"] == "fallback"


def test_browser_functional_and_diagnostic_roles_do_not_collapse() -> None:
    functional = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "browser-functional",
            "task_kind": "browser_functional_validation",
            "needs_browser_diagnostics": True,
        },
        environment=env(),
    )
    assert ids(functional) == ["playwright", "chrome_devtools"]
    assert by_id(functional)["playwright"]["role"] == "primary"
    assert by_id(functional)["chrome_devtools"]["role"] == "corroborating"

    debug = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "browser-debug",
            "task_kind": "browser_debugging",
        },
        environment=env(),
    )
    assert ids(debug) == ["chrome_devtools", "playwright"]
    assert by_id(debug)["chrome_devtools"]["role"] == "primary"


def test_write_request_without_authority_is_partial_not_rejected() -> None:
    result = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "lean-write",
            "task_kind": "lean_ci_repair",
            "target_path": "formal/KUOS/Test.lean",
            "request_write": True,
        },
        environment=env(writes=False),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.authority_required_count >= 3
    routes = by_id(result)
    assert routes["filesystem_reference"]["activation_state"] == "authority_required"
    assert routes["lean_lsp"]["activation_state"] == "authority_required"
    assert routes["git_reference"]["activation_state"] == "authority_required"
    assert routes["github_official"]["activation_state"] == "ready"


def test_unavailable_required_server_blocks_only_requested_route() -> None:
    result = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "lean-missing-lsp",
            "task_kind": "lean_ci_repair",
            "target_path": "formal/KUOS/Test.lean",
        },
        environment=env(unavailable=["lean_lsp"]),
    )
    assert result.status == BLOCKED
    assert result.unavailable_required_count == 1
    assert by_id(result)["lean_lsp"]["activation_state"] == "unavailable"


def test_provider_specific_routes_do_not_broaden() -> None:
    vercel = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "vercel",
            "task_kind": "deployment_debugging",
            "provider": "vercel",
        },
        environment=env(),
    )
    assert ids(vercel) == ["vercel_existing", "github_official"]
    assert "supabase_existing" not in ids(vercel)

    supabase = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "supabase",
            "task_kind": "database_debugging",
            "provider": "supabase",
            "needs_external_docs": True,
        },
        environment=env(),
    )
    assert ids(supabase) == ["supabase_existing", "context7"]
    assert "neon_existing" not in ids(supabase)


def test_maximal_profile_is_never_implicitly_selected() -> None:
    result = route_development_mcp_task(
        registry=registry(),
        request={
            "task_id": "local",
            "task_kind": "local_worktree_review",
            "target_path": "README.md",
        },
        environment=env(),
    )
    assert result.status == READY
    assert len(result.routes) == 2
    assert ids(result) == ["git_reference", "filesystem_reference"]


def main() -> int:
    test_lean_ci_repair_uses_minimal_repository_semantic_route()
    test_external_docs_are_added_only_when_requested()
    test_mcp_spec_prefers_official_docs()
    test_browser_functional_and_diagnostic_roles_do_not_collapse()
    test_write_request_without_authority_is_partial_not_rejected()
    test_unavailable_required_server_blocks_only_requested_route()
    test_provider_specific_routes_do_not_broaden()
    test_maximal_profile_is_never_implicitly_selected()
    print("PASS: KuuOS Development MCP Capability Routing v7.24")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
