#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_ci_observation_mcp_routing_v7_25 import (
    BLOCKED,
    PARTIAL,
    READY,
    route_ci_observation,
)

REGISTRY_PATH = (
    ROOT / "manifests" / "kuuos_development_mcp_capability_registry_v7_16.json"
)


def registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def env(*, writes: bool = False) -> dict:
    return {
        "unavailable_server_ids": [],
        "github_write_authority_ready": writes,
        "workspace_write_authority_ready": writes,
        "browser_effect_authority_ready": writes,
        "mcp_orchestration_authority_ready": writes,
        "vercel_write_authority_ready": writes,
        "supabase_write_authority_ready": writes,
        "neon_write_authority_ready": writes,
        "sentry_project_configured": False,
    }


def receipt(excerpt: str, *, conclusion: str = "failure") -> dict:
    return {
        "version": "kuuos_runtime_daemon_qi_github_actions_bounded_live_log_observer_v7_0",
        "status": "QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_TERMINAL",
        "packet_id": "fixture",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "expected_head_sha": "a" * 40,
        "run_id": 123,
        "selected_job_id": 456,
        "poll_count": 2,
        "terminal_observed": True,
        "run_status": "completed",
        "run_conclusion": conclusion,
        "latest_log_digest": "b" * 64,
        "final_log_digest": "c" * 64,
        "latest_delta_excerpt": excerpt,
        "raw_logs_persisted": False,
        "records": [],
        "blockers": [],
        "warnings": [],
        "epoch": 0,
    }


def route_ids(result) -> list[str]:
    return [x["server_id"] for x in result.routing_result["routes"]]


def test_lean_failure_selects_full_repair_route() -> None:
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=receipt(
            "formal/KUOS/Example.lean:176:3: error: simp made no progress"
        ),
        observation_context={
            "workflow_name": "Strict Lean",
            "job_name": "Validate formal modules",
        },
        environment=env(),
    )
    assert result.status == READY, result.to_dict()
    assert result.classification == "lean_ci_repair"
    assert result.target_path == "formal/KUOS/Example.lean"
    assert result.full_target_file_audit_required is True
    assert result.ci_error_line_is_locator_not_scope is True
    assert route_ids(result) == [
        "github_official",
        "filesystem_reference",
        "lean_lsp",
        "git_reference",
    ]


def test_lean_mcp_failure_adds_official_mcp_docs() -> None:
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=receipt(
            "formal/KUOS/MCPBridge.lean:42:9: error: type mismatch\n"
            "MCP-Protocol-Version / tools/list contract changed"
        ),
        observation_context={},
        environment=env(),
    )
    assert result.classification == "lean_ci_repair"
    assert result.mcp_signal is True
    assert "mcp_docs" in route_ids(result)
    assert route_ids(result)[:4] == [
        "github_official",
        "filesystem_reference",
        "lean_lsp",
        "git_reference",
    ]


def test_browser_failure_routes_to_debugging_planes() -> None:
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=receipt(
            "Playwright browser_navigate failed with console error NET::ERR_FAILED"
        ),
        observation_context={"workflow_name": "Browser validation"},
        environment=env(),
    )
    assert result.status == READY
    assert result.classification == "browser_debugging"
    assert route_ids(result) == ["chrome_devtools", "playwright"]


def test_mcp_only_failure_routes_to_official_spec() -> None:
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=receipt(
            "JSONRPC invalid params during tools/call after protocolVersion negotiation"
        ),
        observation_context={},
        environment=env(),
    )
    assert result.status == READY
    assert result.classification == "mcp_spec_research"
    assert route_ids(result) == ["mcp_docs", "context7", "mcp_fetch"]


def test_ambiguous_failure_stays_partial() -> None:
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=receipt("Process exited with code 1"),
        observation_context={},
        environment=env(),
    )
    assert result.status == PARTIAL
    assert result.classification == "remote_repository_observation"
    assert route_ids(result) == ["github_official"]
    assert "ci_failure_not_specific_enough_for_repair_route" in result.warnings


def test_success_requires_no_repair_route() -> None:
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=receipt("all checks passed", conclusion="success"),
        observation_context={},
        environment=env(),
    )
    assert result.status == READY
    assert result.classification == "remote_repository_observation"
    assert result.full_target_file_audit_required is False


def test_write_request_without_authority_remains_partial_candidate() -> None:
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=receipt(
            "formal/KUOS/Example.lean:10:1: error: unsolved goals"
        ),
        observation_context={"request_write": True},
        environment=env(writes=False),
    )
    assert result.status == PARTIAL
    assert result.routing_result["authority_required_count"] >= 3
    assert result.blockers == []


def test_invalid_live_log_boundaries_block() -> None:
    bad = receipt("formal/KUOS/Example.lean:1:1: error: type mismatch")
    bad["repository_full_name"] = "other/repo"
    result = route_ci_observation(
        registry=registry(),
        live_log_receipt=bad,
        observation_context={},
        environment=env(),
    )
    assert result.status == BLOCKED
    assert "live_log_repository_invalid" in result.blockers


def main() -> int:
    test_lean_failure_selects_full_repair_route()
    test_lean_mcp_failure_adds_official_mcp_docs()
    test_browser_failure_routes_to_debugging_planes()
    test_mcp_only_failure_routes_to_official_spec()
    test_ambiguous_failure_stays_partial()
    test_success_requires_no_repair_route()
    test_write_request_without_authority_remains_partial_candidate()
    test_invalid_live_log_boundaries_block()
    print("PASS: KuuOS CI Observation MCP Routing v7.25")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
