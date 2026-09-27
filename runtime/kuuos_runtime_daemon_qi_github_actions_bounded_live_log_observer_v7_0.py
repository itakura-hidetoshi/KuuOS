#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_write_verification_v0_3 import _normalize_tool_payload
from runtime.kuuos_github_mcp_server_bridge_v0_1 import (
    MCPTransport,
    OfficialGitHubMCPStdioClient,
    _append_jsonl,
    _is_write_tool,
    _mapping,
    _safe_root,
    _sha256,
    _stdio_command,
    _tool_map,
    _write_json,
)

VERSION = "kuuos_runtime_daemon_qi_github_actions_bounded_live_log_observer_v7_0"
PLAN_VERSION = "qi_github_actions_bounded_live_log_observer_plan_v7_0"
AUTHORITY_READY = "QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_AUTHORITY_READY"
TERMINAL = "QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_TERMINAL"
BOUNDED = "QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_BOUNDED"
BLOCKED = "QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_BLOCKED"
REQUIRED_TOOLS = ("actions_get", "actions_list", "get_job_logs")
TERMINAL_RUN_STATUSES = {"completed"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
PINNED_IMAGE = re.compile(r"^ghcr\.io/github/github-mcp-server@sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class QiGitHubActionsBoundedLiveLogObserverResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    repository_full_name: str
    expected_head_sha: str
    run_id: int
    selected_job_id: int
    poll_count: int
    terminal_observed: bool
    run_status: str
    run_conclusion: str
    latest_log_digest: str
    final_log_digest: str
    latest_delta_excerpt: str
    receipt_path: str
    audit_path: str
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _f(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _tool_error(response: Mapping[str, Any]) -> bool:
    if response.get("error"):
        return True
    result = _mapping(response.get("result"))
    return result.get("isError") is True


def _call(
    transport: MCPTransport,
    *,
    tool: str,
    arguments: Mapping[str, Any],
) -> tuple[Any, list[str]]:
    blockers: list[str] = []
    observed: Any = {}
    try:
        response = transport.call_tool(tool, arguments)
        if _tool_error(response):
            blockers.append(f"{tool}_returned_error")
        else:
            observed = _normalize_tool_payload(response)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"{tool}_exception:{type(exc).__name__}")
    return observed, blockers


def _extract_mapping(payload: Any) -> Mapping[str, Any]:
    if isinstance(payload, Mapping):
        for key in ("workflow_run", "run", "job"):
            nested = payload.get(key)
            if isinstance(nested, Mapping):
                return nested
        return payload
    return {}


def _extract_jobs(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [dict(x) for x in payload if isinstance(x, Mapping)]
    root = _mapping(payload)
    for key in ("jobs", "workflow_jobs"):
        value = root.get(key)
        if isinstance(value, list):
            return [dict(x) for x in value if isinstance(x, Mapping)]
        if isinstance(value, Mapping):
            nested = value.get("jobs")
            if isinstance(nested, list):
                return [dict(x) for x in nested if isinstance(x, Mapping)]
    return []


def _job_id(job: Mapping[str, Any]) -> int:
    return _i(job.get("id"), 0)


def _select_job(jobs: list[dict[str, Any]], preferred: int) -> dict[str, Any]:
    if preferred > 0:
        for job in jobs:
            if _job_id(job) == preferred:
                return job
    for status in ("in_progress", "queued", "waiting", "pending"):
        candidates = [job for job in jobs if str(job.get("status", "")) == status]
        if candidates:
            return sorted(candidates, key=_job_id)[-1]
    failed = [
        job
        for job in jobs
        if str(job.get("conclusion", "")) in {"failure", "cancelled", "timed_out", "action_required"}
    ]
    if failed:
        return sorted(failed, key=_job_id)[-1]
    return sorted(jobs, key=_job_id)[-1] if jobs else {}


def _extract_log_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, list):
        parts = [_extract_log_text(x) for x in payload]
        return "\n".join(x for x in parts if x)
    root = _mapping(payload)
    for key in ("content", "logs", "log", "text", "job_logs"):
        value = root.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, (list, Mapping)):
            text = _extract_log_text(value)
            if text:
                return text
    return json.dumps(payload, ensure_ascii=False, sort_keys=True) if payload not in ({}, None) else ""


def _delta(previous: str, current: str) -> tuple[str, bool]:
    if not previous:
        return current, False
    if current.startswith(previous):
        return current[len(previous) :], False
    if previous == current:
        return "", False
    return current, True


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    repo = str(plan.get("repository_full_name", ""))
    if repo.count("/") != 1:
        blockers.append("repository_full_name_invalid")
    if SHA40.fullmatch(str(plan.get("expected_head_sha", ""))) is None:
        blockers.append("expected_head_sha_invalid")
    if _i(plan.get("run_id"), 0) <= 0:
        blockers.append("run_id_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    tail_lines = _i(plan.get("tail_lines"), 500)
    if tail_lines < 1 or tail_lines > 5000:
        blockers.append("tail_lines_out_of_bounds")
    poll_attempts = _i(plan.get("poll_attempts"), 6)
    if poll_attempts < 1 or poll_attempts > 30:
        blockers.append("poll_attempts_out_of_bounds")
    poll_interval = _f(plan.get("poll_interval_seconds"), 5.0)
    if poll_interval < 0 or poll_interval > 60:
        blockers.append("poll_interval_seconds_out_of_bounds")
    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    if PINNED_IMAGE.fullmatch(str(server.get("image", ""))) is None:
        blockers.append("official_server_image_not_immutable")
    if set(str(x) for x in server.get("toolsets", []) if isinstance(x, str)) != {"actions"}:
        blockers.append("actions_toolset_required")
    if set(str(x) for x in server.get("tools", []) if isinstance(x, str)) != set(REQUIRED_TOOLS):
        blockers.append("bounded_live_log_tool_allowlist_invalid")


def _record(
    *,
    phase: str,
    run_status: str,
    run_conclusion: str,
    job_id: int,
    job_status: str,
    job_conclusion: str,
    log_text: str,
    delta_text: str,
    window_rebased: bool,
) -> dict[str, Any]:
    record = {
        "phase": phase,
        "run_status": run_status,
        "run_conclusion": run_conclusion,
        "job_id": job_id,
        "job_status": job_status,
        "job_conclusion": job_conclusion,
        "log_digest": _sha256({"text": log_text}),
        "log_line_count": len(log_text.splitlines()),
        "delta_digest": _sha256({"text": delta_text}),
        "delta_line_count": len(delta_text.splitlines()),
        "window_rebased": window_rebased,
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha256(record)
    return record


def build_qi_github_actions_bounded_live_log_observer(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
) -> QiGitHubActionsBoundedLiveLogObserverResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "qi_github_actions_bounded_live_log_plan_v7_0.json"
    receipt_path = root / "qi_github_actions_bounded_live_log_receipt_v7_0.json"
    audit_path = root / "qi_github_actions_bounded_live_log_audit_v7_0.jsonl"

    if ctx.get("qi_github_actions_bounded_live_log_observer_enabled") is not True:
        blockers.append("bounded_live_log_observer_enabled_not_true")
    if ctx.get("apply_github_actions_bounded_live_log_observer") is not True:
        blockers.append("apply_bounded_live_log_observer_not_true")
    if ctx.get("execute_external_observations") is not True:
        blockers.append("execute_external_observations_not_true")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("bounded_live_log_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "external_read_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    if not plan:
        blockers.append("bounded_live_log_plan_missing_or_invalid")
    else:
        _validate_plan(plan, blockers)

    repo_full_name = str(plan.get("repository_full_name", ""))
    expected_head_sha = str(plan.get("expected_head_sha", ""))
    run_id = _i(plan.get("run_id"), 0)
    preferred_job_id = _i(plan.get("job_id"), 0)
    tail_lines = _i(plan.get("tail_lines"), 500)
    poll_attempts = _i(plan.get("poll_attempts"), 6)
    poll_interval = _f(plan.get("poll_interval_seconds"), 5.0)
    terminal_full_log = plan.get("terminal_full_log") is True
    excerpt_chars = max(0, min(_i(plan.get("persist_delta_excerpt_chars"), 2000), 12000))
    mode = str(plan.get("mode", ctx.get("mode", "mock")))

    if mode not in {"mock", "stdio"}:
        blockers.append("mode_invalid")
    if str(ctx.get("repository_full_name", repo_full_name)) != repo_full_name:
        blockers.append("runtime_repository_scope_mismatch")
    if str(ctx.get("expected_head_sha", expected_head_sha)) != expected_head_sha:
        blockers.append("runtime_expected_head_sha_mismatch")

    owner, repo = (repo_full_name.split("/", 1) + [""])[:2]
    server = dict(_mapping(plan.get("server")))
    active_transport = transport
    owns_transport = False

    if not blockers and active_transport is None:
        if mode == "mock":
            blockers.append("mock_transport_required")
        else:
            token_env = str(server.get("token_env", "GITHUB_PERSONAL_ACCESS_TOKEN"))
            if not os.environ.get(token_env):
                blockers.append("github_personal_access_token_missing")
            else:
                try:
                    command, generated_env = _stdio_command(server, plan)
                    active_transport = OfficialGitHubMCPStdioClient(command, generated_env)
                    owns_transport = True
                except Exception as exc:  # noqa: BLE001
                    blockers.append(f"stdio_transport_build_failed:{type(exc).__name__}")

    if not blockers and active_transport is not None:
        try:
            discovered = _tool_map(active_transport.list_tools())
            for name in REQUIRED_TOOLS:
                if name not in discovered:
                    blockers.append(f"required_tool_not_discovered:{name}")
                elif _is_write_tool(name, discovered[name]):
                    blockers.append(f"read_only_tool_classification_failed:{name}")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    previous_log = ""
    latest_log_digest = ""
    latest_delta_excerpt = ""
    final_log_digest = ""
    selected_job_id = preferred_job_id
    run_status = ""
    run_conclusion = ""
    terminal_observed = False
    poll_count = 0

    if not blockers and active_transport is not None:
        for attempt in range(1, poll_attempts + 1):
            poll_count = attempt
            run_payload, local = _call(
                active_transport,
                tool="actions_get",
                arguments={
                    "method": "get_workflow_run",
                    "owner": owner,
                    "repo": repo,
                    "resource_id": str(run_id),
                },
            )
            if local:
                blockers.extend(local)
                break
            run = _extract_mapping(run_payload)
            observed_head_sha = str(run.get("head_sha", ""))
            run_status = str(run.get("status", ""))
            run_conclusion = str(run.get("conclusion", "") or "")
            if observed_head_sha != expected_head_sha:
                blockers.append("observed_run_head_sha_mismatch")
                break

            jobs_payload, local = _call(
                active_transport,
                tool="actions_list",
                arguments={
                    "method": "list_workflow_jobs",
                    "owner": owner,
                    "repo": repo,
                    "resource_id": str(run_id),
                    "page": 1,
                    "per_page": 100,
                },
            )
            if local:
                blockers.extend(local)
                break
            selected = _select_job(_extract_jobs(jobs_payload), preferred_job_id)
            selected_job_id = _job_id(selected)
            job_status = str(selected.get("status", ""))
            job_conclusion = str(selected.get("conclusion", "") or "")
            if selected_job_id <= 0:
                warnings.append(f"poll_{attempt}_no_job_observed")
                if run_status in TERMINAL_RUN_STATUSES:
                    terminal_observed = True
                    break
                if attempt < poll_attempts and poll_interval > 0:
                    time.sleep(poll_interval)
                continue

            log_payload, local = _call(
                active_transport,
                tool="get_job_logs",
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "job_id": selected_job_id,
                    "return_content": True,
                    "tail_lines": tail_lines,
                },
            )
            if local:
                warnings.extend(local)
                log_text = ""
            else:
                log_text = _extract_log_text(log_payload)
            delta_text, window_rebased = _delta(previous_log, log_text)
            latest_log_digest = _sha256({"text": log_text})
            latest_delta_excerpt = delta_text[-excerpt_chars:] if excerpt_chars else ""
            records.append(
                _record(
                    phase=f"poll_{attempt}",
                    run_status=run_status,
                    run_conclusion=run_conclusion,
                    job_id=selected_job_id,
                    job_status=job_status,
                    job_conclusion=job_conclusion,
                    log_text=log_text,
                    delta_text=delta_text,
                    window_rebased=window_rebased,
                )
            )
            previous_log = log_text

            if run_status in TERMINAL_RUN_STATUSES:
                terminal_observed = True
                if terminal_full_log:
                    final_payload, local = _call(
                        active_transport,
                        tool="get_job_logs",
                        arguments={
                            "owner": owner,
                            "repo": repo,
                            "job_id": selected_job_id,
                            "return_content": True,
                        },
                    )
                    if local:
                        warnings.extend(local)
                    else:
                        final_text = _extract_log_text(final_payload)
                        final_log_digest = _sha256({"text": final_text})
                break

            if attempt < poll_attempts and poll_interval > 0:
                time.sleep(poll_interval)

    if owns_transport and active_transport is not None:
        active_transport.close()

    if blockers:
        status = BLOCKED
    elif terminal_observed:
        status = TERMINAL
    else:
        status = BOUNDED

    packet_id = "qi-github-actions-bounded-live-log-" + _sha256(
        {
            "plan": plan,
            "records": records,
            "blockers": sorted(set(blockers)),
            "warnings": warnings,
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "repository_full_name": repo_full_name,
        "expected_head_sha": expected_head_sha,
        "run_id": run_id,
        "selected_job_id": selected_job_id,
        "poll_count": poll_count,
        "terminal_observed": terminal_observed,
        "run_status": run_status,
        "run_conclusion": run_conclusion,
        "latest_log_digest": latest_log_digest,
        "final_log_digest": final_log_digest,
        "latest_delta_excerpt": latest_delta_excerpt,
        "raw_logs_persisted": False,
        "records": records,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(
            audit_path,
            {
                "version": VERSION,
                "status": status,
                "packet_id": packet_id,
                "records_digest": _sha256(records),
                "blockers": sorted(set(blockers)),
                "warnings": warnings,
                "epoch": int(time.time()),
            },
        )

    return QiGitHubActionsBoundedLiveLogObserverResult(
        VERSION,
        status,
        packet_id,
        str(root),
        repo_full_name,
        expected_head_sha,
        run_id,
        selected_job_id,
        poll_count,
        terminal_observed,
        run_status,
        run_conclusion,
        latest_log_digest,
        final_log_digest,
        latest_delta_excerpt,
        str(receipt_path),
        str(audit_path),
        records,
        sorted(set(blockers)),
        warnings,
    )
