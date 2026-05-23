#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status
except ModuleNotFoundError:
    from kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status


@dataclass(frozen=True)
class KuuOSQiProcessTensorRecoverabilityProjection:
    projection_version: str
    projection_status: str
    recoverability_status: str
    dominant_recovery_path: str
    recommended_recovery_action: str
    recoverability_score: float
    observation_debt: float
    transition_gap: float
    memory_gap: float
    nonmarkov_inertia: float
    compaction_debt: float
    boundary_blocker_weight: float
    reentry_blocker_weight: float
    recovery_blockers: list[str]
    recovery_unsafe: bool
    local_recovery_allowed: bool
    recovery_reason: str
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


def _b(value: Any) -> bool:
    return bool(value)


def _i(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _lst(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list) else []


def _summary_from_status(daemon_dir: Path) -> dict[str, Any]:
    status = read_runtime_daemon_status(daemon_dir)
    summary = status.latest_qi_process_tensor_summary
    return dict(summary) if isinstance(summary, Mapping) else {}


def _score(*values: float) -> float:
    debt = sum(values) / max(1, len(values))
    return round(max(0.0, min(1.0, 1.0 - debt)), 6)


def compile_qi_process_tensor_recoverability_projection(
    *,
    process_tensor_summary: Mapping[str, Any] | None = None,
    reentry_plan: Mapping[str, Any] | None = None,
    license_gate: Mapping[str, Any] | None = None,
    invocation_boundary: Mapping[str, Any] | None = None,
    executor_receipt: Mapping[str, Any] | None = None,
) -> KuuOSQiProcessTensorRecoverabilityProjection:
    s = process_tensor_summary or {}
    rp = reentry_plan or {}
    lg = license_gate or {}
    ib = invocation_boundary or {}
    er = executor_receipt or {}

    process_visible = _b(s.get("process_tensor_visible"))
    transition_visible = _b(s.get("transition_continuity_visible"))
    memory_visible = _b(s.get("memory_continuity_visible"))
    nonmarkov_visible = _b(s.get("nonmarkov_memory_visible"))
    history_len = _i(s.get("process_history_length"), 0)
    missing = _lst(s.get("missing_process_requirements"))

    observation_debt = 0.0 if process_visible else 1.0
    if history_len == 1:
        observation_debt = max(observation_debt, 0.5)
    transition_gap = 0.0 if transition_visible else 1.0
    memory_gap = 0.0 if memory_visible else 1.0
    nonmarkov_inertia = 0.0 if nonmarkov_visible else 0.5

    plan_status = str(rp.get("plan_status") or "")
    license_decision = str(lg.get("license_decision") or "")
    boundary_decision = str(ib.get("invocation_decision") or "")
    token = _b(ib.get("single_tick_invocation_token")) or _b(er.get("single_tick_invocation_token"))
    tick_invoked = _b(er.get("tick_invoked"))
    executor_status = str(er.get("executor_status") or "")

    compaction_debt = 1.0 if plan_status == "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST" or _b(rp.get("compact_before_reentry")) else 0.0
    boundary_blocker_weight = 1.0 if boundary_decision == "NO_SINGLE_TICK_INVOCATION_TOKEN" else 0.0
    reentry_blocker_weight = 1.0 if plan_status == "QI_PROCESS_TENSOR_REENTRY_HELD" else 0.0
    if license_decision == "NO_BOUNDED_TICK_LICENSE":
        reentry_blocker_weight = max(reentry_blocker_weight, 0.75)

    blockers = []
    for ok, name in [
        (observation_debt >= 1.0, "observation_debt"),
        (transition_gap >= 1.0, "transition_gap"),
        (memory_gap >= 1.0, "memory_gap"),
        (compaction_debt >= 1.0, "compaction_debt"),
        (boundary_blocker_weight >= 1.0, "boundary_blocker"),
        (reentry_blocker_weight >= 1.0, "reentry_blocker"),
    ]:
        if ok:
            blockers.append(name)
    blockers.extend(missing)

    unsafe = (license_decision == "NO_BOUNDED_TICK_LICENSE" and token) or (tick_invoked and not token)
    score = _score(observation_debt, transition_gap, memory_gap, nonmarkov_inertia, compaction_debt, boundary_blocker_weight, reentry_blocker_weight)

    if unsafe:
        status, path, action, allowed, reason, receipt = (
            "UNSAFE_RECOVERY",
            "blocked",
            "hold",
            False,
            "recovery_boundary_inconsistent",
            None,
        )
    elif tick_invoked and executor_status == "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED":
        status, path, action, allowed, reason, receipt = (
            "RECOVERED_BY_MANUAL_RUNNER",
            "manual_runner_completed",
            "no_action",
            False,
            "bounded_tick_already_invoked",
            "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json",
        )
    elif observation_debt >= 1.0:
        status, path, action, allowed, reason, receipt = (
            "RECOVERABLE_BY_OBSERVATION",
            "observation",
            "observe",
            True,
            "process_tensor_support_missing",
            None,
        )
    elif transition_gap >= 1.0:
        status, path, action, allowed, reason, receipt = (
            "RECOVERABLE_BY_REOBSERVATION",
            "reobservation",
            "reobserve",
            True,
            "transition_continuity_missing",
            None,
        )
    elif memory_gap >= 1.0:
        status, path, action, allowed, reason, receipt = (
            "RECOVERABLE_BY_OBSERVATION",
            "memory_support_observation",
            "observe",
            True,
            "memory_continuity_missing",
            None,
        )
    elif compaction_debt >= 1.0:
        status, path, action, allowed, reason, receipt = (
            "RECOVERABLE_BY_COMPACTION",
            "trace_compaction",
            "compact_trace",
            True,
            "compaction_required",
            "daemon_qi_process_tensor_reentry_plan_v0_1.json",
        )
    elif token and license_decision == "BOUNDED_TICK_LICENSE_GRANTED":
        status, path, action, allowed, reason, receipt = (
            "RECOVERABLE_BY_MANUAL_RUNNER",
            "manual_runner",
            "invoke_manual_runner",
            True,
            "single_tick_token_ready",
            "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json",
        )
    elif reentry_blocker_weight > 0.0 or boundary_blocker_weight > 0.0:
        status, path, action, allowed, reason, receipt = (
            "LOCAL_RECOVERY_BLOCKED",
            "blocked_boundary",
            "hold",
            False,
            "boundary_or_reentry_blocks_local_recovery",
            "daemon_qi_process_tensor_reentry_license_gate_v0_1.json",
        )
    elif nonmarkov_inertia >= 0.5:
        status, path, action, allowed, reason, receipt = (
            "FRAGILE_RECOVERY",
            "nonmarkov_memory_reconstruction",
            "reobserve",
            True,
            "nonmarkov_memory_missing",
            None,
        )
    else:
        status, path, action, allowed, reason, receipt = (
            "RECOVERY_UNRESOLVED",
            "unresolved",
            "reobserve",
            False,
            "recoverability_unresolved",
            None,
        )

    return KuuOSQiProcessTensorRecoverabilityProjection(
        projection_version="kuuos_runtime_daemon_qi_process_tensor_recoverability_projection_v0_1",
        projection_status="QI_PROCESS_TENSOR_RECOVERABILITY_PROJECTED",
        recoverability_status=status,
        dominant_recovery_path=path,
        recommended_recovery_action=action,
        recoverability_score=score,
        observation_debt=round(observation_debt, 6),
        transition_gap=round(transition_gap, 6),
        memory_gap=round(memory_gap, 6),
        nonmarkov_inertia=round(nonmarkov_inertia, 6),
        compaction_debt=round(compaction_debt, 6),
        boundary_blocker_weight=round(boundary_blocker_weight, 6),
        reentry_blocker_weight=round(reentry_blocker_weight, 6),
        recovery_blockers=sorted(set(blockers)),
        recovery_unsafe=unsafe,
        local_recovery_allowed=allowed,
        recovery_reason=reason,
        recommended_next_receipt=receipt,
        runtime_hot_path_tier="T0_hot_path_projection",
        validation_tier="T3_runtime_full_check",
    )


def read_and_compile_qi_process_tensor_recoverability_projection(daemon_dir: Path) -> KuuOSQiProcessTensorRecoverabilityProjection:
    daemon_dir = Path(daemon_dir)
    return compile_qi_process_tensor_recoverability_projection(
        process_tensor_summary=_summary_from_status(daemon_dir),
        reentry_plan=_read_json(daemon_dir / "daemon_qi_process_tensor_reentry_plan_v0_1.json") or {},
        license_gate=_read_json(daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json") or {},
        invocation_boundary=_read_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json") or {},
        executor_receipt=_read_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json") or {},
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor recoverability projection v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    projection = read_and_compile_qi_process_tensor_recoverability_projection(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_recoverability_projection_v0_1.json", projection.to_dict())
    print(json.dumps(projection.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
