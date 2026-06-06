#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


REQUIRED_GITHUB_ACTIONS_WORKFLOWS = [
    "All Governance Validation",
    "Core Governance Validation",
    "Emptiness Superposition Non-Collapse Validation",
    "Emptiness Two Truths Runtime Audit Validation",
    "KuuOS Runtime Full Check",
    "Qi Process Tensor Review Checks",
]

QI_WORKFLOWS = {"Qi Process Tensor Review Checks"}
RUNTIME_WORKFLOWS = {"KuuOS Runtime Full Check"}
GOVERNANCE_WORKFLOWS = {
    "All Governance Validation",
    "Core Governance Validation",
    "Emptiness Superposition Non-Collapse Validation",
    "Emptiness Two Truths Runtime Audit Validation",
}


@dataclass(frozen=True)
class QiGitHubActionsCapabilityPlannerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_class: str
    batch_length: int
    batch_packet_path: str
    receipt_path: str
    audit_path: str
    write_performed: bool
    blockers: list[str]
    warnings: list[str]

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


def _runs(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, Mapping):
            out.append(dict(item))
    return out


def _required(packet: Mapping[str, Any]) -> list[str]:
    raw = packet.get("required_workflows")
    if isinstance(raw, list) and raw:
        return [str(x) for x in raw]
    return list(REQUIRED_GITHUB_ACTIONS_WORKFLOWS)


def _latest_by_name(runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for run in runs:
        name = str(run.get("name", ""))
        if not name:
            continue
        latest.setdefault(name, run)
    return latest


def _is_success(run: Mapping[str, Any]) -> bool:
    return run.get("status") == "completed" and run.get("conclusion") == "success"


def _is_pending(run: Mapping[str, Any]) -> bool:
    return str(run.get("status", "")).lower() in {"queued", "requested", "waiting", "pending", "in_progress"}


def _is_failure(run: Mapping[str, Any]) -> bool:
    if run.get("status") != "completed":
        return False
    return str(run.get("conclusion", "")).lower() not in {"", "none", "success", "neutral", "skipped"}


def _classify(required: list[str], latest: Mapping[str, Mapping[str, Any]]) -> tuple[str, list[str], list[str], list[str]]:
    missing = [name for name in required if name not in latest]
    pending = [name for name in required if name in latest and _is_pending(latest[name])]
    failed = [name for name in required if name in latest and _is_failure(latest[name])]
    if missing:
        return "github_actions_missing_required_blocked", missing, pending, failed
    if pending:
        return "github_actions_pending_observe_batch", missing, pending, failed
    if not failed and all(_is_success(latest[name]) for name in required):
        return "github_actions_all_green_batch", missing, pending, failed
    failed_set = set(failed)
    if failed_set <= QI_WORKFLOWS:
        return "github_actions_qi_repair_batch", missing, pending, failed
    if failed_set <= RUNTIME_WORKFLOWS:
        return "github_actions_runtime_repair_batch", missing, pending, failed
    if failed_set <= GOVERNANCE_WORKFLOWS:
        return "github_actions_governance_repair_batch", missing, pending, failed
    return "github_actions_mixed_repair_batch", missing, pending, failed


def _recipe(name: str, **kwargs: Any) -> dict[str, Any]:
    out = {
        "capability_recipe": name,
        "capability_recipe_allowed": True,
        "github_actions_planner_source": "qi_github_actions_capability_planner_v5_5",
    }
    out.update(kwargs)
    return out


def _batch_for(plan_class: str) -> list[dict[str, Any]]:
    if plan_class == "github_actions_all_green_batch":
        return [_recipe("compile_recipe_and_batch"), _recipe("safe_compile_full_surface")]
    if plan_class == "github_actions_pending_observe_batch":
        return [_recipe("compile_recipe_and_batch")]
    if plan_class == "github_actions_qi_repair_batch":
        return [_recipe("route_observe_then_compile"), _recipe("compile_recipe_and_batch")]
    if plan_class == "github_actions_runtime_repair_batch":
        return [_recipe("compile_then_execute_recipe"), _recipe("compile_recipe_and_batch")]
    if plan_class == "github_actions_governance_repair_batch":
        return [_recipe("safe_compile_full_surface")]
    if plan_class == "github_actions_mixed_repair_batch":
        return [_recipe("compile_recipe_and_batch"), _recipe("safe_compile_full_surface"), _recipe("compile_batch_then_execute_batch")]
    return []


def _batch_packet(plan_class: str, batch: list[dict[str, Any]], source: Mapping[str, Any], missing: list[str], pending: list[str], failed: list[str]) -> dict[str, Any]:
    return {
        "version": "qi_executable_capability_recipe_batch_packet_from_github_actions_v5_5",
        "batch_allowed": True,
        "github_actions_plan_class": plan_class,
        "batch": batch,
        "max_capability_recipe_batch": max(len(batch), 1),
        "compiled_from": "qi_github_actions_capability_planner_v5_5",
        "source_digest": _sha(dict(source)),
        "observed_missing_workflows": missing,
        "observed_pending_workflows": pending,
        "observed_failed_workflows": failed,
        "boundary": {
            "observed_status_only": True,
            "does_not_dispatch_workflows": True,
            "does_not_rerun_workflows": True,
            "does_not_merge_prs": True,
            "requires_v5_3_capability_recipe_batch_executor": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_capability_planner(*, runtime_context: Mapping[str, Any], github_actions_planner_license: Mapping[str, Any]) -> QiGitHubActionsCapabilityPlannerResult:
    ctx = _m(runtime_context)
    lic = _m(github_actions_planner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    status_packet_path = root / "qi_github_actions_status_packet.json"
    batch_packet_path = root / "qi_executable_capability_recipe_batch_packet.json"
    receipt_path = root / "qi_github_actions_capability_planner_receipt.json"
    audit_path = root / "qi_github_actions_capability_planner_audit.jsonl"

    if ctx.get("qi_github_actions_capability_planner_enabled") is not True:
        blockers.append("qi_github_actions_capability_planner_enabled_not_true")
    if ctx.get("apply_github_actions_capability_planner") is not True:
        blockers.append("apply_github_actions_capability_planner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_LICENSE_READY":
        blockers.append("github_actions_capability_planner_license_not_ready")
    for name in ["github_actions_status_packet_read_allowed", "capability_recipe_batch_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(status_packet_path)
    if not packet:
        blockers.append("github_actions_status_packet_missing_or_invalid")
    if packet and packet.get("github_actions_status_allowed") is not True:
        blockers.append("github_actions_status_packet_allowed_not_true")
    runs = _runs(packet)
    if packet and not runs:
        blockers.append("workflow_runs_empty_or_invalid")
    required = _required(packet)
    latest = _latest_by_name(runs)
    plan_class, missing, pending, failed = _classify(required, latest)
    if plan_class == "github_actions_missing_required_blocked":
        blockers.append("required_workflows_missing")
    batch = _batch_for(plan_class)
    if not batch and not blockers:
        blockers.append("github_actions_plan_batch_empty")
    payload: dict[str, Any] = {}
    write_performed = False
    if not blockers:
        payload = _batch_packet(plan_class, batch, packet, missing, pending, failed)
        _write_json(batch_packet_path, payload)
        write_performed = True
    status = "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_READY" if not blockers else "QI_GITHUB_ACTIONS_CAPABILITY_PLANNER_BLOCKED"
    packet_id = "qi-github-actions-capability-planner-" + _sha({"packet": packet, "plan": plan_class, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_capability_planner_v5_5",
        "status": status,
        "packet_id": packet_id,
        "plan_class": plan_class,
        "batch_length": len(batch),
        "write_performed": write_performed,
        "required_workflows": required,
        "missing_workflows": missing,
        "pending_workflows": pending,
        "failed_workflows": failed,
        "batch_packet_digest": _sha(payload),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsCapabilityPlannerResult(
        "kuuos_runtime_daemon_qi_github_actions_capability_planner_v5_5",
        status,
        packet_id,
        str(root),
        plan_class,
        len(batch),
        str(batch_packet_path),
        str(receipt_path),
        str(audit_path),
        write_performed,
        blockers,
        warnings,
    )
