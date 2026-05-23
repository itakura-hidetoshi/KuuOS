#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

@dataclass(frozen=True)
class KuuOSQiProcessTensorReentryPlan:
    plan_version: str
    plan_status: str
    source_receipt_status: str
    source_closed_loop_next_state: str
    next_invocation_mode: str
    recommended_sleep_seconds: float
    recommended_max_ticks: int
    recommended_max_steps_per_tick: int
    compact_before_reentry: bool
    reobserve_before_reentry: bool
    hold_until_observation: bool
    runtime_hot_path_tier: str
    validation_tier: str
    reentry_reason: str
    allowed_projection: list[str]
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


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int = 1) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def compile_qi_process_tensor_reentry_plan(
    closed_loop_receipt: Mapping[str, Any],
    daemon_result: Mapping[str, Any] | None = None,
) -> KuuOSQiProcessTensorReentryPlan:
    daemon_result = daemon_result or {}
    receipt_status = str(closed_loop_receipt.get("receipt_status") or "QI_PROCESS_TENSOR_CLOSED_LOOP_UNKNOWN")
    next_state = str(closed_loop_receipt.get("closed_loop_next_state") or "UNKNOWN_NEXT_STATE")

    sleep_seconds = max(0.0, _as_float(closed_loop_receipt.get("scheduled_next_sleep_seconds_hint"), 0.0))
    max_ticks = max(1, _as_int(closed_loop_receipt.get("scheduled_next_max_ticks_hint"), 1))
    max_steps = max(1, _as_int(closed_loop_receipt.get("scheduled_next_max_steps_per_tick_hint"), 1))
    compact = _as_bool(closed_loop_receipt.get("scheduled_compact_before_next_tick")) or _as_bool(closed_loop_receipt.get("compact_required"))
    reobserve = _as_bool(closed_loop_receipt.get("scheduled_reobserve_before_next_tick")) or _as_bool(closed_loop_receipt.get("observation_required"))
    hold = _as_bool(closed_loop_receipt.get("scheduled_hold_until_observation"))

    if next_state == "HOLD_UNTIL_OBSERVATION" or hold:
        plan_status = "QI_PROCESS_TENSOR_REENTRY_HELD"
        mode = "NO_REENTRY_UNTIL_OBSERVATION"
        reobserve = True
        hold = True
        reason = "closed_loop_receipt_requires_hold_until_observation"
    elif next_state == "REOBSERVE_BEFORE_NEXT_TICK" or reobserve:
        plan_status = "QI_PROCESS_TENSOR_REENTRY_REOBSERVE_FIRST"
        mode = "REOBSERVE_THEN_BOUNDED_REENTRY"
        reobserve = True
        reason = "closed_loop_receipt_requires_reobserve_before_reentry"
    elif next_state == "COMPACT_BEFORE_NEXT_TICK" or compact:
        plan_status = "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST"
        mode = "COMPACT_THEN_BOUNDED_REENTRY"
        compact = True
        reason = "closed_loop_receipt_requires_compaction_before_reentry"
    else:
        plan_status = "QI_PROCESS_TENSOR_REENTRY_READY"
        mode = "BOUNDED_REENTRY_READY"
        reason = "closed_loop_receipt_allows_bounded_nonexecuting_reentry_plan"

    if daemon_result.get("daemon_status") == "DAEMON_QUARANTINE_RETAINED_APPEND_ONLY":
        plan_status = "QI_PROCESS_TENSOR_REENTRY_HELD"
        mode = "NO_REENTRY_DURING_QUARANTINE"
        hold = True
        reobserve = True
        reason = "daemon_quarantine_retained_blocks_reentry"

    return KuuOSQiProcessTensorReentryPlan(
        plan_version="kuuos_runtime_daemon_qi_process_tensor_reentry_plan_v0_1",
        plan_status=plan_status,
        source_receipt_status=receipt_status,
        source_closed_loop_next_state=next_state,
        next_invocation_mode=mode,
        recommended_sleep_seconds=round(sleep_seconds, 6),
        recommended_max_ticks=max_ticks,
        recommended_max_steps_per_tick=max_steps,
        compact_before_reentry=compact,
        reobserve_before_reentry=reobserve,
        hold_until_observation=hold,
        runtime_hot_path_tier="T0_hot_path_guard",
        validation_tier="T3_runtime_full_check",
        reentry_reason=reason,
        allowed_projection=[
            "qi_process_tensor_reentry_plan",
            "nonexecuting_next_tick_plan",
            "bounded_reentry_hints",
            "hot_path_t0_receipt_projection",
        ],
    )


def read_and_compile_qi_process_tensor_reentry_plan(daemon_dir: Path) -> KuuOSQiProcessTensorReentryPlan:
    receipt = _read_json(daemon_dir / "daemon_qi_process_tensor_closed_loop_receipt_v0_1.json") or {}
    daemon_result = _read_json(daemon_dir / "daemon_result_v0_1.json") or {}
    return compile_qi_process_tensor_reentry_plan(receipt, daemon_result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor reentry plan v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_process_tensor_reentry_plan(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_reentry_plan_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
