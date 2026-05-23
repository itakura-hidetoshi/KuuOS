#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

@dataclass(frozen=True)
class KuuOSQiProcessTensorTickScheduler:
    scheduler_version: str
    scheduler_status: str
    next_tick_advisory: str
    next_sleep_seconds_hint: float
    next_max_ticks_hint: int
    next_max_steps_per_tick_hint: int
    compact_before_next_tick: bool
    reobserve_before_next_tick: bool
    hold_until_observation: bool
    scheduler_reason: str
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


def _clamp_int(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(x)))


def _clamp_float(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(x)))


def compile_qi_process_tensor_tick_scheduler(
    actuator_result: Mapping[str, Any],
    *,
    base_sleep_seconds: float = 0.0,
    base_max_ticks: int = 3,
    base_max_steps_per_tick: int = 1,
) -> KuuOSQiProcessTensorTickScheduler:
    advisory = str(actuator_result.get("next_tick_advisory") or "CONTINUE_WITH_PROCESS_TENSOR_MONITOR")
    sleep_scale = float(actuator_result.get("sleep_scale_hint", 1.0) or 1.0)
    max_steps_hint = int(actuator_result.get("max_steps_hint", base_max_steps_per_tick) or base_max_steps_per_tick)
    compact_hint = bool(actuator_result.get("compact_trace_hint", False))
    reobserve_hint = bool(actuator_result.get("reobserve_hint", False))
    hold_hint = bool(actuator_result.get("hold_transition_hint", False))

    base_sleep = max(0.0, float(base_sleep_seconds))
    if base_sleep == 0.0:
        base_sleep = 1.0
    next_sleep = _clamp_float(base_sleep * sleep_scale, 0.0, 3600.0)
    next_ticks = _clamp_int(base_max_ticks, 1, 100)
    next_steps = _clamp_int(max_steps_hint, 1, 25)

    if advisory == "HOLD_AND_REOBSERVE_PROCESS_TENSOR" or hold_hint:
        status = "QI_PROCESS_TENSOR_TICK_SCHEDULER_HOLD"
        next_ticks = 1
        next_steps = 1
        next_sleep = _clamp_float(max(next_sleep, 2.0), 0.0, 3600.0)
        compact = compact_hint
        reobserve = True
        hold_until_observation = True
        reason = "hold_transition_requires_single_tick_reobserve"
    elif advisory == "REOBSERVE_QI_PROCESS_TENSOR" or reobserve_hint:
        status = "QI_PROCESS_TENSOR_TICK_SCHEDULER_REOBSERVE"
        next_ticks = _clamp_int(min(next_ticks, 2), 1, 100)
        next_steps = 1
        compact = compact_hint
        reobserve = True
        hold_until_observation = False
        reason = "observation_gap_requests_short_reobserve_schedule"
    elif advisory == "COMPACT_TRACE_THEN_CONTINUE" or compact_hint:
        status = "QI_PROCESS_TENSOR_TICK_SCHEDULER_COMPACT"
        next_ticks = _clamp_int(next_ticks, 1, 5)
        next_steps = _clamp_int(next_steps, 1, 2)
        compact = True
        reobserve = False
        hold_until_observation = False
        reason = "nonmarkov_or_density_pressure_requests_compact_schedule"
    else:
        status = "QI_PROCESS_TENSOR_TICK_SCHEDULER_CONTINUE"
        next_ticks = _clamp_int(next_ticks, 1, 10)
        next_steps = _clamp_int(max(next_steps, 1), 1, 3)
        compact = False
        reobserve = False
        hold_until_observation = False
        reason = "process_tensor_continuity_supports_bounded_next_tick"

    return KuuOSQiProcessTensorTickScheduler(
        scheduler_version="kuuos_runtime_daemon_qi_process_tensor_tick_scheduler_v0_1",
        scheduler_status=status,
        next_tick_advisory=advisory,
        next_sleep_seconds_hint=round(next_sleep, 6),
        next_max_ticks_hint=next_ticks,
        next_max_steps_per_tick_hint=next_steps,
        compact_before_next_tick=compact,
        reobserve_before_next_tick=reobserve,
        hold_until_observation=hold_until_observation,
        scheduler_reason=reason,
        allowed_projection=["qi_process_tensor_tick_scheduler", "nonexecuting_schedule_hints", "bounded_next_tick_advisory"],
    )


def read_and_compile_qi_process_tensor_tick_scheduler(daemon_dir: Path) -> KuuOSQiProcessTensorTickScheduler:
    actuator = _read_json(daemon_dir / "daemon_qi_process_tensor_actuator_v0_1.json") or {}
    return compile_qi_process_tensor_tick_scheduler(actuator)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor tick scheduler v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--base-sleep-seconds", type=float, default=0.0)
    parser.add_argument("--base-max-ticks", type=int, default=3)
    parser.add_argument("--base-max-steps-per-tick", type=int, default=1)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    actuator = _read_json(args.daemon_dir / "daemon_qi_process_tensor_actuator_v0_1.json") or {}
    result = compile_qi_process_tensor_tick_scheduler(
        actuator,
        base_sleep_seconds=args.base_sleep_seconds,
        base_max_ticks=args.base_max_ticks,
        base_max_steps_per_tick=args.base_max_steps_per_tick,
    )
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_tick_scheduler_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
