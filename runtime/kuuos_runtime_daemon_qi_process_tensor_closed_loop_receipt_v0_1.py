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
class KuuOSQiProcessTensorClosedLoopReceipt:
    receipt_version: str
    receipt_status: str
    daemon_status: str
    stop_reason: str
    ticks_run: int
    qi_process_tensor_actuator_path: str | None
    qi_process_tensor_tick_scheduler_path: str | None
    next_tick_advisory: str
    scheduled_next_sleep_seconds_hint: float
    scheduled_next_max_ticks_hint: int
    scheduled_next_max_steps_per_tick_hint: int
    scheduled_compact_before_next_tick: bool
    scheduled_reobserve_before_next_tick: bool
    scheduled_hold_until_observation: bool
    closed_loop_next_state: str
    observation_required: bool
    compact_required: bool
    receipt_reason: str
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


def compile_qi_process_tensor_closed_loop_receipt(
    daemon_result: Mapping[str, Any],
    scheduler_result: Mapping[str, Any],
) -> KuuOSQiProcessTensorClosedLoopReceipt:
    daemon_status = str(daemon_result.get("daemon_status") or "DAEMON_STATUS_UNKNOWN_APPEND_ONLY")
    stop_reason = str(daemon_result.get("stop_reason") or "UNKNOWN_RESULT_HELD")
    ticks_run = max(0, _as_int(daemon_result.get("ticks_run"), 0))
    actuator_path = daemon_result.get("qi_process_tensor_actuator_path")
    scheduler_path = daemon_result.get("qi_process_tensor_tick_scheduler_path")

    advisory = str(scheduler_result.get("next_tick_advisory") or "CONTINUE_WITH_PROCESS_TENSOR_MONITOR")
    next_sleep = max(0.0, _as_float(scheduler_result.get("next_sleep_seconds_hint"), 0.0))
    next_ticks = max(1, _as_int(scheduler_result.get("next_max_ticks_hint"), 1))
    next_steps = max(1, _as_int(scheduler_result.get("next_max_steps_per_tick_hint"), 1))
    compact = _as_bool(scheduler_result.get("compact_before_next_tick"))
    reobserve = _as_bool(scheduler_result.get("reobserve_before_next_tick"))
    hold = _as_bool(scheduler_result.get("hold_until_observation"))

    if hold:
        receipt_status = "QI_PROCESS_TENSOR_CLOSED_LOOP_HOLD"
        next_state = "HOLD_UNTIL_OBSERVATION"
        observation_required = True
        reason = "scheduler_holds_next_tick_until_observation"
    elif reobserve:
        receipt_status = "QI_PROCESS_TENSOR_CLOSED_LOOP_REOBSERVE"
        next_state = "REOBSERVE_BEFORE_NEXT_TICK"
        observation_required = True
        reason = "scheduler_requires_reobserve_before_next_tick"
    elif compact:
        receipt_status = "QI_PROCESS_TENSOR_CLOSED_LOOP_COMPACT"
        next_state = "COMPACT_BEFORE_NEXT_TICK"
        observation_required = False
        reason = "scheduler_requires_trace_compaction_before_next_tick"
    else:
        receipt_status = "QI_PROCESS_TENSOR_CLOSED_LOOP_CONTINUE"
        next_state = "CONTINUE_NEXT_TICK"
        observation_required = False
        reason = "scheduler_allows_bounded_nonexecuting_next_tick"

    return KuuOSQiProcessTensorClosedLoopReceipt(
        receipt_version="kuuos_runtime_daemon_qi_process_tensor_closed_loop_receipt_v0_1",
        receipt_status=receipt_status,
        daemon_status=daemon_status,
        stop_reason=stop_reason,
        ticks_run=ticks_run,
        qi_process_tensor_actuator_path=str(actuator_path) if actuator_path else None,
        qi_process_tensor_tick_scheduler_path=str(scheduler_path) if scheduler_path else None,
        next_tick_advisory=advisory,
        scheduled_next_sleep_seconds_hint=round(next_sleep, 6),
        scheduled_next_max_ticks_hint=next_ticks,
        scheduled_next_max_steps_per_tick_hint=next_steps,
        scheduled_compact_before_next_tick=compact,
        scheduled_reobserve_before_next_tick=reobserve,
        scheduled_hold_until_observation=hold,
        closed_loop_next_state=next_state,
        observation_required=observation_required,
        compact_required=compact,
        receipt_reason=reason,
        allowed_projection=[
            "qi_process_tensor_closed_loop_receipt",
            "nonexecuting_runtime_receipt",
            "next_tick_schedule_trace",
            "observation_compaction_hold_hints",
        ],
    )


def read_and_compile_qi_process_tensor_closed_loop_receipt(daemon_dir: Path) -> KuuOSQiProcessTensorClosedLoopReceipt:
    daemon_result = _read_json(daemon_dir / "daemon_result_v0_1.json") or {}
    scheduler_result = _read_json(daemon_dir / "daemon_qi_process_tensor_tick_scheduler_v0_1.json") or {}
    return compile_qi_process_tensor_closed_loop_receipt(daemon_result, scheduler_result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor closed-loop receipt v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_process_tensor_closed_loop_receipt(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_closed_loop_receipt_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
