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
class KuuOSQiProcessTensorReentryLicenseGate:
    gate_version: str
    gate_status: str
    license_decision: str
    source_plan_status: str
    source_next_invocation_mode: str
    may_invoke_next_tick: bool
    bounded_tick_license: bool
    denied_reason: str | None
    required_preconditions: list[str]
    licensed_sleep_seconds: float
    licensed_max_ticks: int
    licensed_max_steps_per_tick: int
    runtime_hot_path_tier: str
    validation_tier: str
    gate_reason: str
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


def compile_qi_process_tensor_reentry_license_gate(
    reentry_plan: Mapping[str, Any],
) -> KuuOSQiProcessTensorReentryLicenseGate:
    plan_status = str(reentry_plan.get("plan_status") or "QI_PROCESS_TENSOR_REENTRY_UNKNOWN")
    invocation_mode = str(reentry_plan.get("next_invocation_mode") or "UNKNOWN_REENTRY_MODE")
    sleep_seconds = max(0.0, _as_float(reentry_plan.get("recommended_sleep_seconds"), 0.0))
    max_ticks = max(1, _as_int(reentry_plan.get("recommended_max_ticks"), 1))
    max_steps = max(1, _as_int(reentry_plan.get("recommended_max_steps_per_tick"), 1))
    compact = _as_bool(reentry_plan.get("compact_before_reentry"))
    reobserve = _as_bool(reentry_plan.get("reobserve_before_reentry"))
    hold = _as_bool(reentry_plan.get("hold_until_observation"))

    required: list[str] = []
    if hold or plan_status == "QI_PROCESS_TENSOR_REENTRY_HELD":
        required.append("observation_or_quarantine_exit_required")
        return KuuOSQiProcessTensorReentryLicenseGate(
            gate_version="kuuos_runtime_daemon_qi_process_tensor_reentry_license_gate_v0_1",
            gate_status="QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_HOLD",
            license_decision="NO_BOUNDED_TICK_LICENSE",
            source_plan_status=plan_status,
            source_next_invocation_mode=invocation_mode,
            may_invoke_next_tick=False,
            bounded_tick_license=False,
            denied_reason="reentry_plan_is_held",
            required_preconditions=required,
            licensed_sleep_seconds=0.0,
            licensed_max_ticks=0,
            licensed_max_steps_per_tick=0,
            runtime_hot_path_tier="T0_hot_path_guard",
            validation_tier="T3_runtime_full_check",
            gate_reason="hold_state_blocks_next_tick_invocation",
            allowed_projection=["qi_process_tensor_reentry_license_gate", "bounded_tick_license_denial", "hold_boundary"],
        )

    if reobserve or plan_status == "QI_PROCESS_TENSOR_REENTRY_REOBSERVE_FIRST":
        required.append("fresh_observation_required_before_reentry")
        return KuuOSQiProcessTensorReentryLicenseGate(
            gate_version="kuuos_runtime_daemon_qi_process_tensor_reentry_license_gate_v0_1",
            gate_status="QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_REOBSERVE",
            license_decision="NO_BOUNDED_TICK_LICENSE",
            source_plan_status=plan_status,
            source_next_invocation_mode=invocation_mode,
            may_invoke_next_tick=False,
            bounded_tick_license=False,
            denied_reason="reobserve_required_before_reentry",
            required_preconditions=required,
            licensed_sleep_seconds=0.0,
            licensed_max_ticks=0,
            licensed_max_steps_per_tick=0,
            runtime_hot_path_tier="T0_hot_path_guard",
            validation_tier="T3_runtime_full_check",
            gate_reason="reobserve_requirement_blocks_next_tick_invocation",
            allowed_projection=["qi_process_tensor_reentry_license_gate", "bounded_tick_license_denial", "reobserve_boundary"],
        )

    if compact or plan_status == "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST":
        required.append("trace_compaction_required_before_reentry")
        return KuuOSQiProcessTensorReentryLicenseGate(
            gate_version="kuuos_runtime_daemon_qi_process_tensor_reentry_license_gate_v0_1",
            gate_status="QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_COMPACT",
            license_decision="NO_BOUNDED_TICK_LICENSE",
            source_plan_status=plan_status,
            source_next_invocation_mode=invocation_mode,
            may_invoke_next_tick=False,
            bounded_tick_license=False,
            denied_reason="compaction_required_before_reentry",
            required_preconditions=required,
            licensed_sleep_seconds=0.0,
            licensed_max_ticks=0,
            licensed_max_steps_per_tick=0,
            runtime_hot_path_tier="T0_hot_path_guard",
            validation_tier="T3_runtime_full_check",
            gate_reason="compaction_requirement_blocks_next_tick_invocation",
            allowed_projection=["qi_process_tensor_reentry_license_gate", "bounded_tick_license_denial", "compact_boundary"],
        )

    if plan_status == "QI_PROCESS_TENSOR_REENTRY_READY" and invocation_mode == "BOUNDED_REENTRY_READY":
        return KuuOSQiProcessTensorReentryLicenseGate(
            gate_version="kuuos_runtime_daemon_qi_process_tensor_reentry_license_gate_v0_1",
            gate_status="QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
            license_decision="BOUNDED_TICK_LICENSE_GRANTED",
            source_plan_status=plan_status,
            source_next_invocation_mode=invocation_mode,
            may_invoke_next_tick=True,
            bounded_tick_license=True,
            denied_reason=None,
            required_preconditions=[],
            licensed_sleep_seconds=round(sleep_seconds, 6),
            licensed_max_ticks=max_ticks,
            licensed_max_steps_per_tick=max_steps,
            runtime_hot_path_tier="T0_hot_path_guard",
            validation_tier="T3_runtime_full_check",
            gate_reason="bounded_reentry_plan_passed_lightweight_license_gate",
            allowed_projection=["qi_process_tensor_reentry_license_gate", "bounded_tick_license", "executor_precondition_token"],
        )

    required.append("recognized_ready_plan_required")
    return KuuOSQiProcessTensorReentryLicenseGate(
        gate_version="kuuos_runtime_daemon_qi_process_tensor_reentry_license_gate_v0_1",
        gate_status="QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_UNKNOWN",
        license_decision="NO_BOUNDED_TICK_LICENSE",
        source_plan_status=plan_status,
        source_next_invocation_mode=invocation_mode,
        may_invoke_next_tick=False,
        bounded_tick_license=False,
        denied_reason="unrecognized_or_incomplete_reentry_plan",
        required_preconditions=required,
        licensed_sleep_seconds=0.0,
        licensed_max_ticks=0,
        licensed_max_steps_per_tick=0,
        runtime_hot_path_tier="T0_hot_path_guard",
        validation_tier="T3_runtime_full_check",
        gate_reason="unknown_reentry_plan_blocks_next_tick_invocation",
        allowed_projection=["qi_process_tensor_reentry_license_gate", "bounded_tick_license_denial", "unknown_boundary"],
    )


def read_and_compile_qi_process_tensor_reentry_license_gate(daemon_dir: Path) -> KuuOSQiProcessTensorReentryLicenseGate:
    reentry_plan = _read_json(daemon_dir / "daemon_qi_process_tensor_reentry_plan_v0_1.json") or {}
    return compile_qi_process_tensor_reentry_license_gate(reentry_plan)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor reentry license gate v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_process_tensor_reentry_license_gate(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
