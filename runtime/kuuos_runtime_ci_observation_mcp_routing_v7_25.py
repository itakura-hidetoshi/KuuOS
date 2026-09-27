#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

from runtime.kuuos_runtime_development_mcp_capability_routing_v7_24 import (
    BLOCKED as ROUTING_BLOCKED,
    PARTIAL as ROUTING_PARTIAL,
    route_development_mcp_task,
)

VERSION = "kuuos_runtime_ci_observation_mcp_routing_v7_25"
LIVE_LOG_VERSION = (
    "kuuos_runtime_daemon_qi_github_actions_bounded_live_log_observer_v7_0"
)

READY = "KUUOS_CI_OBSERVATION_MCP_ROUTING_READY"
PARTIAL = "KUUOS_CI_OBSERVATION_MCP_ROUTING_PARTIAL"
BLOCKED = "KUUOS_CI_OBSERVATION_MCP_ROUTING_BLOCKED"

FAILURE_CONCLUSIONS = {
    "failure",
    "cancelled",
    "timed_out",
    "action_required",
    "startup_failure",
}

SHA40 = re.compile(r"^[0-9a-f]{40}$")
LEAN_FILE = re.compile(
    r"(?P<path>(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.lean)"
    r"(?::\d+(?::\d+)?)?"
)

LEAN_SIGNAL_PATTERNS = (
    "unsolved goals",
    "unknown identifier",
    "application type mismatch",
    "type mismatch",
    "declaration uses 'sorry'",
    "simp made no progress",
    "maximum recursion depth",
    "maximum heartbeats",
    "failed to synthesize",
    "invalid field",
    "invalid argument",
    "lean error",
    "lake env lean",
)

MCP_SIGNAL_PATTERNS = (
    "mcp-protocol-version",
    "protocolversion",
    "tools/list",
    "tools/call",
    "notifications/initialized",
    "jsonrpc",
    "method not found",
    "invalid params",
    "model context protocol",
    "mcp session",
)

BROWSER_SIGNAL_PATTERNS = (
    "playwright",
    "chrome-devtools",
    "chrome devtools",
    "browser_navigate",
    "navigate_page",
    "page.goto",
    "console error",
    "net::err_",
    "accessibility snapshot",
)


@dataclass(frozen=True)
class CIObservationMCPRoutingResult:
    version: str
    status: str
    packet_id: str
    repository_full_name: str
    expected_head_sha: str
    run_id: int
    run_conclusion: str
    classification: str
    target_path: str
    lean_signal: bool
    mcp_signal: bool
    browser_signal: bool
    full_target_file_audit_required: bool
    ci_error_line_is_locator_not_scope: bool
    routing_request: dict[str, Any]
    routing_result: dict[str, Any]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _signal(text: str, patterns: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in patterns)


def _lean_paths(text: str) -> list[str]:
    result: list[str] = []
    for match in LEAN_FILE.finditer(text):
        path = match.group("path")
        if path not in result:
            result.append(path)
    return result


def _validate_receipt(receipt: Mapping[str, Any], blockers: list[str]) -> None:
    if receipt.get("version") != LIVE_LOG_VERSION:
        blockers.append("live_log_receipt_version_invalid")
    if receipt.get("repository_full_name") != "itakura-hidetoshi/KuuOS":
        blockers.append("live_log_repository_invalid")
    if SHA40.fullmatch(str(receipt.get("expected_head_sha", ""))) is None:
        blockers.append("live_log_expected_head_sha_invalid")
    run_id = receipt.get("run_id")
    if isinstance(run_id, bool) or not isinstance(run_id, int) or run_id <= 0:
        blockers.append("live_log_run_id_invalid")
    if receipt.get("raw_logs_persisted") is not False:
        blockers.append("raw_logs_persistence_boundary_invalid")
    excerpt = receipt.get("latest_delta_excerpt")
    if not isinstance(excerpt, str):
        blockers.append("latest_delta_excerpt_not_string")
    elif len(excerpt) > 12000:
        blockers.append("latest_delta_excerpt_too_large")


def route_ci_observation(
    *,
    registry: Mapping[str, Any],
    live_log_receipt: Mapping[str, Any],
    observation_context: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> CIObservationMCPRoutingResult:
    receipt = _m(live_log_receipt)
    context = _m(observation_context)
    blockers: list[str] = []
    warnings: list[str] = []

    _validate_receipt(receipt, blockers)

    repository_full_name = str(receipt.get("repository_full_name", ""))
    expected_head_sha = str(receipt.get("expected_head_sha", ""))
    run_id = int(receipt.get("run_id", 0) or 0)
    run_conclusion = str(receipt.get("run_conclusion", "") or "").lower()
    excerpt = str(receipt.get("latest_delta_excerpt", ""))

    workflow_name = str(context.get("workflow_name", ""))
    job_name = str(context.get("job_name", ""))
    target_hint = str(context.get("target_path_hint", "")).strip()
    combined = "\n".join((workflow_name, job_name, excerpt))

    paths = _lean_paths(combined)
    target_path = ""
    if target_hint.endswith(".lean"):
        target_path = target_hint
    elif paths:
        target_path = paths[0]

    lean_signal = bool(paths) or _signal(combined, LEAN_SIGNAL_PATTERNS)
    mcp_signal = _signal(combined, MCP_SIGNAL_PATTERNS)
    browser_signal = _signal(combined, BROWSER_SIGNAL_PATTERNS)

    failure = run_conclusion in FAILURE_CONCLUSIONS

    classification = "remote_repository_observation"
    needs_mcp_spec = False
    needs_external_docs = context.get("consult_external_docs") is True
    needs_browser_diagnostics = False

    if failure:
        if lean_signal:
            classification = "lean_ci_repair"
            needs_mcp_spec = mcp_signal
        elif browser_signal:
            classification = "browser_debugging"
            needs_browser_diagnostics = True
        elif mcp_signal:
            classification = "mcp_spec_research"
        else:
            warnings.append("ci_failure_not_specific_enough_for_repair_route")
    elif run_conclusion:
        warnings.append("ci_run_not_failure_no_repair_route_required")
    else:
        warnings.append("ci_run_conclusion_missing_or_nonterminal")

    routing_request: dict[str, Any] = {
        "task_id": f"ci-observation-{run_id}",
        "task_kind": classification,
        "request_write": context.get("request_write") is True,
    }
    if target_path:
        routing_request["target_path"] = target_path
    if needs_external_docs:
        routing_request["needs_external_docs"] = True
    if needs_mcp_spec:
        routing_request["needs_mcp_spec"] = True
    if needs_browser_diagnostics:
        routing_request["needs_browser_diagnostics"] = True

    routing_result: dict[str, Any] = {}
    if not blockers:
        routed = route_development_mcp_task(
            registry=registry,
            request=routing_request,
            environment=environment,
        )
        routing_result = routed.to_dict()
        if routed.status == ROUTING_BLOCKED:
            blockers.extend("routing:" + item for item in routed.blockers)
            if routed.unavailable_required_count:
                blockers.append("routing_required_mcp_unavailable")
        elif routed.status == ROUTING_PARTIAL:
            warnings.append("routing_requires_additional_authority_or_evidence")

    if blockers:
        status = BLOCKED
    elif routing_result.get("status") == ROUTING_PARTIAL:
        status = PARTIAL
    elif failure and classification == "remote_repository_observation":
        status = PARTIAL
    else:
        status = READY

    full_file_audit = classification == "lean_ci_repair"
    line_is_locator = classification == "lean_ci_repair"

    packet_id = "kuuos-ci-observation-mcp-routing-" + _sha(
        {
            "repository_full_name": repository_full_name,
            "expected_head_sha": expected_head_sha,
            "run_id": run_id,
            "run_conclusion": run_conclusion,
            "excerpt_digest": _sha(excerpt),
            "workflow_name": workflow_name,
            "job_name": job_name,
            "routing_request": routing_request,
            "routing_result": routing_result,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    return CIObservationMCPRoutingResult(
        VERSION,
        status,
        packet_id,
        repository_full_name,
        expected_head_sha,
        run_id,
        run_conclusion,
        classification,
        target_path,
        lean_signal,
        mcp_signal,
        browser_signal,
        full_file_audit,
        line_is_locator,
        routing_request,
        routing_result,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
