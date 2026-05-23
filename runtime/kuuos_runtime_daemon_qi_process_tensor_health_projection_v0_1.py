#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status
    from runtime.kuuos_runtime_daemon_qi_process_tensor_recoverability_projection_v0_1 import (
        compile_qi_process_tensor_recoverability_projection,
    )
except ModuleNotFoundError:
    from kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status
    from kuuos_runtime_daemon_qi_process_tensor_recoverability_projection_v0_1 import (
        compile_qi_process_tensor_recoverability_projection,
    )


@dataclass(frozen=True)
class KuuOSQiProcessTensorHealthProjection:
    projection_version: str
    projection_status: str
    qi_process_tensor_phase: str
    daemon_health_status: str
    next_operator_action: str
    qi_process_tensor_visible: bool
    transition_continuity_visible: bool
    memory_continuity_visible: bool
    nonmarkov_memory_visible: bool
    process_history_length: int
    missing_process_requirements: list[str]
    reentry_plan_status: str | None
    reentry_next_invocation_mode: str | None
    reentry_license_decision: str | None
    invocation_boundary_decision: str | None
    single_tick_invocation_token: bool
    executor_status: str | None
    tick_invoked: bool
    recoverability_status: str
    dominant_recovery_path: str
    recommended_recovery_action: str
    recoverability_score: float
    recovery_unsafe: bool
    local_recovery_allowed: bool
    recovery_reason: str
    recovery_blockers: list[str]
    health_reason: str
    recommended_next_receipt: str | None
    runtime_hot_path_tier: str
    validation_tier: str
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _as_bool(value: Any) -> bool:
    return bool(value)


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _summary_from_status(daemon_dir: Path) -> dict[str, Any]:
    status = read_runtime_daemon_status(daemon_dir)
    summary = status.latest_qi_process_tensor_summary
    return dict(summary) if isinstance(summary, Mapping) else {}


def compile_qi_process_tensor_health_projection(
    *,
    daemon_result: Mapping[str, Any] | None = None,
    process_tensor_summary: Mapping[str, Any] | None = None,
    reentry_plan: Mapping[str, Any] | None = None,
    license_gate: Mapping[str, Any] | None = None,
    invocation_boundary: Mapping[str, Any] | None = None,
    executor_receipt: Mapping[str, Any] | None = None,
) -> KuuOSQiProcessTensorHealthProjection:
    daemon_result = daemon_result or {}
    summary = process_tensor_summary or {}
    reentry_plan = reentry_plan or {}
    license_gate = license_gate or {}
    invocation_boundary = invocation_boundary or {}
    executor_receipt = executor_receipt or {}

    recoverability = compile_qi_process_tensor_recoverability_projection(
        process_tensor_summary=summary,
        reentry_plan=reentry_plan,
        license_gate=license_gate,
        invocation_boundary=invocation_boundary,
        executor_receipt=executor_receipt,
    )

    process_visible = _as_bool(summary.get("process_tensor_visible"))
    transition_visible = _as_bool(summary.get("transition_continuity_visible"))
    memory_visible = _as_bool(summary.get("memory_continuity_visible"))
    nonmarkov_visible = _as_bool(summary.get("nonmarkov_memory_visible"))
    history_len = _as_int(summary.get("process_history_length"), 0)
    missing = _as_list(summary.get("missing_process_requirements"))

    plan_status = reentry_plan.get("plan_status") or daemon_result.get("reentry_plan_status")
    next_mode = reentry_plan.get("next_invocation_mode") or daemon_result.get("reentry_next_invocation_mode")
    license_decision = license_gate.get("license_decision") or daemon_result.get("reentry_license_decision")
    boundary_decision = invocation_boundary.get("invocation_decision") or daemon_result.get("invocation_boundary_decision")
    token = _as_bool(
        invocation_boundary.get("single_tick_invocation_token")
        or daemon_result.get("single_tick_invocation_token")
        or executor_receipt.get("single_tick_invocation_token")
    )
    executor_status = executor_receipt.get("executor_status") or None
    tick_invoked = _as_bool(executor_receipt.get("tick_invoked"))

    if recoverability.recovery_unsafe:
        phase = "QI_PROCESS_TENSOR_RECOVERY_UNSAFE"
        health = "RECOVERY_UNSAFE"
        action = "hold"
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt
    elif not process_visible:
        phase = "QI_PROCESS_TENSOR_FORMATION_INCOMPLETE"
        health = "WAITING_FOR_PROCESS_TENSOR_SUPPORT"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt
    elif not transition_visible:
        phase = "QI_TRANSITION_CONTINUITY_INCOMPLETE"
        health = "REOBSERVE_REQUIRED"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt
    elif not memory_visible:
        phase = "QI_MEMORY_CONTINUITY_INCOMPLETE"
        health = "WAITING_FOR_MEMORY_SUPPORT"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt
    elif plan_status == "QI_PROCESS_TENSOR_REENTRY_HELD":
        phase = "QI_REENTRY_HELD"
        health = "HOLD_UNTIL_OBSERVATION"
        action = "hold"
        reason = "reentry_plan_is_held"
        next_receipt = "daemon_qi_process_tensor_reentry_plan_v0_1.json"
    elif plan_status == "QI_PROCESS_TENSOR_REENTRY_REOBSERVE_FIRST":
        phase = "QI_REENTRY_REOBSERVE_FIRST"
        health = "REOBSERVE_REQUIRED"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt or "daemon_qi_process_tensor_reentry_plan_v0_1.json"
    elif plan_status == "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST":
        phase = "QI_REENTRY_COMPACT_FIRST"
        health = "NEEDS_COMPACTION"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt or "daemon_qi_process_tensor_reentry_plan_v0_1.json"
    elif executor_status == "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED" and tick_invoked:
        phase = "QI_BOUNDED_TICK_COMPLETED"
        health = "EXECUTOR_INVOKED"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt
    elif token and license_decision == "BOUNDED_TICK_LICENSE_GRANTED":
        phase = "QI_SINGLE_TICK_TOKEN_READY"
        health = "HEALTHY_REENTRY_READY"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt
    elif license_decision == "NO_BOUNDED_TICK_LICENSE":
        phase = "QI_REENTRY_LICENSE_DENIED"
        health = "EXECUTOR_DENIED"
        action = "hold"
        reason = str(license_gate.get("denied_reason") or daemon_result.get("reentry_license_denied_reason") or recoverability.recovery_reason)
        next_receipt = recoverability.recommended_next_receipt or "daemon_qi_process_tensor_reentry_license_gate_v0_1.json"
    elif recoverability.recoverability_status == "LOCAL_RECOVERY_BLOCKED":
        phase = "QI_LOCAL_RECOVERY_BLOCKED"
        health = "LOCAL_RECOVERY_BLOCKED"
        action = "hold"
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt
    else:
        phase = "QI_PROCESS_TENSOR_REENTRY_UNRESOLVED"
        health = "REOBSERVE_REQUIRED"
        action = recoverability.recommended_recovery_action
        reason = recoverability.recovery_reason
        next_receipt = recoverability.recommended_next_receipt

    return KuuOSQiProcessTensorHealthProjection(
        projection_version="kuuos_runtime_daemon_qi_process_tensor_health_projection_v0_1",
        projection_status="QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY",
        qi_process_tensor_phase=phase,
        daemon_health_status=health,
        next_operator_action=action,
        qi_process_tensor_visible=process_visible,
        transition_continuity_visible=transition_visible,
        memory_continuity_visible=memory_visible,
        nonmarkov_memory_visible=nonmarkov_visible,
        process_history_length=history_len,
        missing_process_requirements=missing,
        reentry_plan_status=str(plan_status) if plan_status is not None else None,
        reentry_next_invocation_mode=str(next_mode) if next_mode is not None else None,
        reentry_license_decision=str(license_decision) if license_decision is not None else None,
        invocation_boundary_decision=str(boundary_decision) if boundary_decision is not None else None,
        single_tick_invocation_token=token,
        executor_status=str(executor_status) if executor_status is not None else None,
        tick_invoked=tick_invoked,
        recoverability_status=recoverability.recoverability_status,
        dominant_recovery_path=recoverability.dominant_recovery_path,
        recommended_recovery_action=recoverability.recommended_recovery_action,
        recoverability_score=recoverability.recoverability_score,
        recovery_unsafe=recoverability.recovery_unsafe,
        local_recovery_allowed=recoverability.local_recovery_allowed,
        recovery_reason=recoverability.recovery_reason,
        recovery_blockers=recoverability.recovery_blockers,
        health_reason=reason,
        recommended_next_receipt=next_receipt,
        runtime_hot_path_tier="T0_hot_path_projection",
        validation_tier="T3_runtime_full_check",
    )


def read_and_compile_qi_process_tensor_health_projection(daemon_dir: Path) -> KuuOSQiProcessTensorHealthProjection:
    daemon_dir = Path(daemon_dir)
    daemon_result = _read_json(daemon_dir / "daemon_result_v0_1.json") or {}
    process_summary = _summary_from_status(daemon_dir)
    reentry_plan = _read_json(daemon_dir / "daemon_qi_process_tensor_reentry_plan_v0_1.json") or {}
    license_gate = _read_json(daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json") or {}
    invocation_boundary = _read_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json") or {}
    executor_receipt = _read_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json") or {}
    return compile_qi_process_tensor_health_projection(
        daemon_result=daemon_result,
        process_tensor_summary=process_summary,
        reentry_plan=reentry_plan,
        license_gate=license_gate,
        invocation_boundary=invocation_boundary,
        executor_receipt=executor_receipt,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor health projection v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    projection = read_and_compile_qi_process_tensor_health_projection(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json", projection.to_dict())
    print(json.dumps(projection.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
