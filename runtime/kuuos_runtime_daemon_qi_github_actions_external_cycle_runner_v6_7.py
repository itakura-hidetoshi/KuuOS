#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_external_wait_resolver_v6_3 import build_qi_github_actions_external_wait_resolver
from runtime.kuuos_runtime_daemon_qi_github_actions_external_call_dispatcher_v6_5 import build_qi_github_actions_external_call_dispatcher
from runtime.kuuos_runtime_daemon_qi_github_actions_dispatch_result_collector_v6_6 import build_qi_github_actions_dispatch_result_collector
from runtime.kuuos_runtime_daemon_qi_github_actions_external_call_result_adapter_v6_4 import build_qi_github_actions_external_call_result_adapter


@dataclass(frozen=True)
class QiGitHubActionsExternalCycleRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    cycle_stage: str
    stop_reason: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    stage_records: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _record(name: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage": name,
        "status": str(result.get("status", "unknown")),
        "digest": _sha(dict(result)),
        "blockers": list(result.get("blockers", [])) if isinstance(result.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def _resolver_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_wait_resolver_enabled": True, "apply_github_actions_external_wait_resolver": True, "runtime_root": str(root)}


def _resolver_license(stage: str) -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_LICENSE_READY", "wait_state_read_allowed": True, "external_call_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, f"allow_{stage}_stage": True}


def _dispatcher_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_call_dispatcher_enabled": True, "apply_github_actions_external_call_dispatcher": True, "runtime_root": str(root)}


def _dispatcher_license(targets: list[str]) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_LICENSE_READY", "external_call_packet_read_allowed": True, "dispatch_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    for target in targets:
        value[f"allow_{target}_dispatch"] = True
    return value


def _collector_context(root: pathlib.Path, target: str) -> dict[str, Any]:
    return {"qi_github_actions_dispatch_result_collector_enabled": True, "apply_github_actions_dispatch_result_collector": True, "runtime_root": str(root), "dispatch_target": target}


def _collector_license(target: str) -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_LICENSE_READY", "dispatch_packet_read_allowed": True, "dispatch_result_read_allowed": True, "raw_result_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, f"allow_{target}_collect": True}


def _adapter_context(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_external_call_result_adapter_enabled": True, "apply_github_actions_external_call_result_adapter": True, "runtime_root": str(root)}


def _adapter_license(stage: str) -> dict[str, Any]:
    return {"license_status": "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_LICENSE_READY", "external_call_packet_read_allowed": True, "raw_result_packet_read_allowed": True, "adapted_result_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True, f"allow_{stage}_stage": True}


def _dispatch_targets() -> list[str]:
    return [
        "commit_workflow_runs",
        "workflow_run_jobs",
        "workflow_job_steps",
        "workflow_job_logs",
        "workflow_run_artifacts",
        "rerun_failed_workflow_run_jobs",
        "rerun_workflow_job",
        "merge_pull_request",
    ]


def _target_from_dispatch(root: pathlib.Path) -> str:
    receipt = _read_json(root / "qi_github_actions_external_call_dispatcher_receipt.json")
    return str(receipt.get("dispatch_target", "unknown")) if receipt else "unknown"


def _wait_stage(root: pathlib.Path) -> str:
    call = _read_json(root / "qi_github_actions_external_call_packet.json")
    return str(call.get("wait_stage", "await_status_observation")) if call else "await_status_observation"


def build_qi_github_actions_external_cycle_runner(*, runtime_context: Mapping[str, Any], external_cycle_runner_license: Mapping[str, Any]) -> QiGitHubActionsExternalCycleRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(external_cycle_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_external_cycle_runner_receipt.json"
    audit_path = root / "qi_github_actions_external_cycle_runner_audit.jsonl"

    if ctx.get("qi_github_actions_external_cycle_runner_enabled") is not True:
        blockers.append("qi_github_actions_external_cycle_runner_enabled_not_true")
    if ctx.get("apply_github_actions_external_cycle_runner") is not True:
        blockers.append("apply_github_actions_external_cycle_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_EXTERNAL_CYCLE_RUNNER_LICENSE_READY":
        blockers.append("github_actions_external_cycle_runner_license_not_ready")
    for name in ["resolver_run_allowed", "dispatcher_run_allowed", "collector_run_allowed", "adapter_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    cycle_stage = "unknown"
    if not blockers:
        if _read_json(root / "qi_github_actions_external_call_raw_result_packet.json"):
            cycle_stage = "adapt_raw_result"
            stage = _wait_stage(root)
            res = build_qi_github_actions_external_call_result_adapter(
                runtime_context=_adapter_context(root),
                result_adapter_license=_adapter_license(stage),
            ).to_dict()
            records.append(_record("v6_4_adapter", res))
            stop_reason = "adapted_result_ready" if res.get("status") == "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_READY" else "adapter_blocked"
            if stop_reason == "adapter_blocked":
                blockers.append("adapter_not_ready")
        elif _read_json(root / "qi_github_actions_dispatch_commit_workflow_runs_result.json") or _read_json(root / "qi_github_actions_dispatch_workflow_run_jobs_result.json") or _read_json(root / "qi_github_actions_dispatch_workflow_job_steps_result.json") or _read_json(root / "qi_github_actions_dispatch_workflow_job_logs_result.json") or _read_json(root / "qi_github_actions_dispatch_workflow_run_artifacts_result.json") or _read_json(root / "qi_github_actions_dispatch_rerun_failed_workflow_run_jobs_result.json") or _read_json(root / "qi_github_actions_dispatch_rerun_workflow_job_result.json") or _read_json(root / "qi_github_actions_dispatch_merge_pull_request_result.json"):
            cycle_stage = "collect_dispatch_result"
            target = str(ctx.get("dispatch_target") or _target_from_dispatch(root))
            if target == "unknown":
                # Let collector infer if no dispatcher receipt exists.
                target = "commit_workflow_runs"
            res = build_qi_github_actions_dispatch_result_collector(
                runtime_context=_collector_context(root, target),
                dispatch_result_collector_license=_collector_license(target),
            ).to_dict()
            records.append(_record("v6_6_collector", res))
            if res.get("status") != "QI_GITHUB_ACTIONS_DISPATCH_RESULT_COLLECTOR_READY":
                blockers.append("collector_not_ready")
                stop_reason = "collector_blocked"
            else:
                stage = _wait_stage(root)
                res2 = build_qi_github_actions_external_call_result_adapter(
                    runtime_context=_adapter_context(root),
                    result_adapter_license=_adapter_license(stage),
                ).to_dict()
                records.append(_record("v6_4_adapter", res2))
                stop_reason = "adapted_result_ready" if res2.get("status") == "QI_GITHUB_ACTIONS_EXTERNAL_CALL_RESULT_ADAPTER_READY" else "adapter_blocked"
                if stop_reason == "adapter_blocked":
                    blockers.append("adapter_not_ready")
        elif _read_json(root / "qi_github_actions_external_call_packet.json"):
            cycle_stage = "dispatch_external_call"
            res = build_qi_github_actions_external_call_dispatcher(
                runtime_context=_dispatcher_context(root),
                external_call_dispatcher_license=_dispatcher_license(_dispatch_targets()),
            ).to_dict()
            records.append(_record("v6_5_dispatcher", res))
            stop_reason = "await_dispatch_result" if res.get("status") == "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_READY" else "dispatcher_blocked"
            if stop_reason == "dispatcher_blocked":
                blockers.append("dispatcher_not_ready")
        else:
            cycle_stage = "resolve_wait"
            # allow both wait stages; resolver chooses from current packets.
            res = build_qi_github_actions_external_wait_resolver(
                runtime_context=_resolver_context(root),
                external_wait_resolver_license={
                    "license_status": "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_LICENSE_READY",
                    "wait_state_read_allowed": True,
                    "external_call_packet_write_allowed": True,
                    "receipt_write_allowed": True,
                    "audit_append_allowed": True,
                    "allow_await_connector_operation_stage": True,
                    "allow_await_status_observation_stage": True,
                },
            ).to_dict()
            records.append(_record("v6_3_resolver", res))
            if res.get("status") != "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_READY":
                blockers.append("resolver_not_ready")
                stop_reason = "resolver_blocked"
            else:
                res2 = build_qi_github_actions_external_call_dispatcher(
                    runtime_context=_dispatcher_context(root),
                    external_call_dispatcher_license=_dispatcher_license(_dispatch_targets()),
                ).to_dict()
                records.append(_record("v6_5_dispatcher", res2))
                stop_reason = "await_dispatch_result" if res2.get("status") == "QI_GITHUB_ACTIONS_EXTERNAL_CALL_DISPATCHER_READY" else "dispatcher_blocked"
                if stop_reason == "dispatcher_blocked":
                    blockers.append("dispatcher_not_ready")

    status = "QI_GITHUB_ACTIONS_EXTERNAL_CYCLE_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_EXTERNAL_CYCLE_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-external-cycle-" + _sha({"stage": cycle_stage, "records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_external_cycle_runner_v6_7",
        "status": status,
        "packet_id": packet_id,
        "cycle_stage": cycle_stage,
        "stop_reason": stop_reason,
        "stage_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsExternalCycleRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_external_cycle_runner_v6_7",
        status,
        packet_id,
        str(root),
        cycle_stage,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
