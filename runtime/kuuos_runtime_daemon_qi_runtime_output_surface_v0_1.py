#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any


@dataclass(frozen=True)
class KuuOSQiRuntimeOutputSurface:
    surface_version: str
    surface_status: str
    daemon_dir: str
    daemon_result_path: str
    daemon_status: str | None
    daemon_stop_reason: str | None
    daemon_ticks_run: int | None
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    recoverability_projection_path: str | None
    health_projection_path: str | None
    observation_debt_schedule_path: str | None
    trace_compaction_plan_path: str | None
    recoverability_status: str | None
    dominant_recovery_path: str | None
    recommended_recovery_action: str | None
    recoverability_score: float | None
    recovery_unsafe: bool | None
    local_recovery_allowed: bool | None
    qi_process_tensor_phase: str | None
    daemon_health_status: str | None
    next_operator_action: str | None
    health_reason: str | None
    observation_debt_status: str | None
    recommended_observation_action: str | None
    observation_priority: str | None
    observation_urgency_score: float | None
    compaction_plan_status: str | None
    recommended_compaction_action: str | None
    compaction_priority: str | None
    compaction_urgency_score: float | None
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _str_or_none(value: Any) -> str | None:
    return str(value) if value is not None else None


def compile_qi_runtime_output_surface(daemon_dir: Path) -> KuuOSQiRuntimeOutputSurface:
    daemon_dir = Path(daemon_dir)
    daemon_result_path = daemon_dir / "daemon_result_v0_1.json"
    recoverability_path = daemon_dir / "daemon_qi_process_tensor_recoverability_projection_v0_1.json"
    health_path = daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json"
    observation_path = daemon_dir / "daemon_qi_process_tensor_observation_debt_schedule_v0_1.json"
    compaction_path = daemon_dir / "daemon_qi_process_tensor_trace_compaction_plan_v0_1.json"

    daemon = _read_json(daemon_result_path)
    recoverability = _read_json(recoverability_path)
    health = _read_json(health_path)
    observation = _read_json(observation_path)
    compaction = _read_json(compaction_path)

    return KuuOSQiRuntimeOutputSurface(
        surface_version="kuuos_runtime_daemon_qi_runtime_output_surface_v0_1",
        surface_status="QI_RUNTIME_OUTPUT_SURFACE_COMPILED",
        daemon_dir=str(daemon_dir),
        daemon_result_path=str(daemon_result_path),
        daemon_status=_str_or_none(daemon.get("daemon_status")),
        daemon_stop_reason=_str_or_none(daemon.get("stop_reason")),
        daemon_ticks_run=_int_or_none(daemon.get("ticks_run")),
        final_raw_state_path=_str_or_none(daemon.get("final_raw_state_path")),
        final_state_bundle_path=_str_or_none(daemon.get("final_state_bundle_path")),
        recoverability_projection_path=str(recoverability_path) if recoverability_path.is_file() else None,
        health_projection_path=str(health_path) if health_path.is_file() else None,
        observation_debt_schedule_path=str(observation_path) if observation_path.is_file() else None,
        trace_compaction_plan_path=str(compaction_path) if compaction_path.is_file() else None,
        recoverability_status=_str_or_none(recoverability.get("recoverability_status") or daemon.get("recoverability_status")),
        dominant_recovery_path=_str_or_none(recoverability.get("dominant_recovery_path") or daemon.get("dominant_recovery_path")),
        recommended_recovery_action=_str_or_none(recoverability.get("recommended_recovery_action") or daemon.get("recommended_recovery_action")),
        recoverability_score=_float_or_none(recoverability.get("recoverability_score") or daemon.get("recoverability_score")),
        recovery_unsafe=bool(recoverability.get("recovery_unsafe") or daemon.get("recovery_unsafe")),
        local_recovery_allowed=bool(recoverability.get("local_recovery_allowed") or daemon.get("local_recovery_allowed")),
        qi_process_tensor_phase=_str_or_none(health.get("qi_process_tensor_phase") or daemon.get("qi_process_tensor_phase")),
        daemon_health_status=_str_or_none(health.get("daemon_health_status") or daemon.get("daemon_health_status")),
        next_operator_action=_str_or_none(health.get("next_operator_action") or daemon.get("next_operator_action")),
        health_reason=_str_or_none(health.get("health_reason") or daemon.get("health_reason")),
        observation_debt_status=_str_or_none(observation.get("observation_debt_status")),
        recommended_observation_action=_str_or_none(observation.get("recommended_observation_action")),
        observation_priority=_str_or_none(observation.get("observation_priority")),
        observation_urgency_score=_float_or_none(observation.get("observation_urgency_score")),
        compaction_plan_status=_str_or_none(compaction.get("compaction_plan_status")),
        recommended_compaction_action=_str_or_none(compaction.get("recommended_compaction_action")),
        compaction_priority=_str_or_none(compaction.get("compaction_priority")),
        compaction_urgency_score=_float_or_none(compaction.get("compaction_urgency_score")),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi runtime output surface v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    surface = compile_qi_runtime_output_surface(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_runtime_output_surface_v0_1.json", surface.to_dict())
    print(json.dumps(surface.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
