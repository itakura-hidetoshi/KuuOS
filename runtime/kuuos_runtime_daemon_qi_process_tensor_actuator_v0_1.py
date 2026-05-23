#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

@dataclass(frozen=True)
class KuuOSQiProcessTensorActuator:
    actuator_version: str
    actuator_status: str
    next_tick_advisory: str
    sleep_scale_hint: float
    max_steps_hint: int
    compact_trace_hint: bool
    reobserve_hint: bool
    hold_transition_hint: bool
    process_tensor_drive: dict[str, float]
    actuator_reason: str
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


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


def compile_qi_process_tensor_actuator(
    feature_bundle: Mapping[str, Any],
    policy_governor: Mapping[str, Any] | None = None,
) -> KuuOSQiProcessTensorActuator:
    inputs = feature_bundle.get("active_inference_inputs", {}) if isinstance(feature_bundle, Mapping) else {}
    primary = feature_bundle.get("primary_qi_process_tensor", {}) if isinstance(feature_bundle, Mapping) else {}
    constraints = feature_bundle.get("hard_constraints", {}) if isinstance(feature_bundle, Mapping) else {}
    governor = policy_governor if isinstance(policy_governor, Mapping) else {}

    visible = bool(inputs.get("process_tensor_visible", False))
    history_len = int(inputs.get("process_history_length", 0) or 0)
    transition_support = int(inputs.get("transition_support_count", 0) or 0)
    memory_support = int(inputs.get("memory_support_count", 0) or 0)
    nonmarkov_support = int(inputs.get("nonmarkov_support_count", 0) or 0)
    missing_requirements = primary.get("missing_process_requirements", []) if isinstance(primary, Mapping) else []
    if not isinstance(missing_requirements, list):
        missing_requirements = []

    continuity = _clamp((transition_support + memory_support) / max(history_len, 1))
    nonmarkov_inertia = _clamp(nonmarkov_support / max(history_len, 1))
    missingness_pressure = _clamp(len(missing_requirements) / 5.0)
    density_pressure = _clamp(float(inputs.get("tick_density", 0) or 0) / 10.0)
    observation_gap = 1.0 if (not visible or constraints.get("observation_hard_constraint")) else missingness_pressure
    governor_damping = _clamp(float(governor.get("oscillation_damping", 1.0) or 1.0))
    ramp_fraction = _clamp(float(governor.get("ramp_fraction", 1.0) or 1.0))
    transition_mode = str(governor.get("transition_mode") or "STABLE_NO_RAMP")

    compact_trace = density_pressure >= 0.55 or nonmarkov_inertia >= 0.45
    reobserve = observation_gap >= 0.5 or missingness_pressure >= 0.4
    hold_transition = transition_mode == "HOLD_TRANSITION_REOBSERVE" or governor_damping < 0.35

    if hold_transition:
        next_tick = "HOLD_AND_REOBSERVE_PROCESS_TENSOR"
        sleep_scale = 1.75
        max_steps = 1
        status = "QI_PROCESS_TENSOR_ACTUATOR_HOLD"
        reason = "policy_flow_governor_blocks_unstable_transition"
    elif reobserve:
        next_tick = "REOBSERVE_QI_PROCESS_TENSOR"
        sleep_scale = 1.35
        max_steps = 1
        status = "QI_PROCESS_TENSOR_ACTUATOR_REOBSERVE"
        reason = "process_tensor_observation_gap_or_missing_requirements"
    elif compact_trace:
        next_tick = "COMPACT_TRACE_THEN_CONTINUE"
        sleep_scale = 1.15
        max_steps = 1 if nonmarkov_inertia >= 0.6 else 2
        status = "QI_PROCESS_TENSOR_ACTUATOR_COMPACT"
        reason = "nonmarkov_or_density_pressure_requests_trace_compaction"
    else:
        next_tick = "CONTINUE_WITH_PROCESS_TENSOR_MONITOR"
        sleep_scale = max(0.75, 1.0 - 0.25 * ramp_fraction)
        max_steps = 2
        status = "QI_PROCESS_TENSOR_ACTUATOR_CONTINUE"
        reason = "process_tensor_continuity_supports_bounded_continue"

    drive = {
        "continuity": round(continuity, 6),
        "nonmarkov_inertia": round(nonmarkov_inertia, 6),
        "missingness_pressure": round(missingness_pressure, 6),
        "density_pressure": round(density_pressure, 6),
        "observation_gap": round(observation_gap, 6),
        "governor_damping": round(governor_damping, 6),
        "ramp_fraction": round(ramp_fraction, 6),
    }

    return KuuOSQiProcessTensorActuator(
        actuator_version="kuuos_runtime_daemon_qi_process_tensor_actuator_v0_1",
        actuator_status=status,
        next_tick_advisory=next_tick,
        sleep_scale_hint=round(sleep_scale, 6),
        max_steps_hint=max_steps,
        compact_trace_hint=compact_trace,
        reobserve_hint=reobserve,
        hold_transition_hint=hold_transition,
        process_tensor_drive=drive,
        actuator_reason=reason,
        allowed_projection=["qi_process_tensor_actuator", "nonexecuting_runtime_hints", "next_tick_advisory"],
    )


def read_and_compile_qi_process_tensor_actuator(daemon_dir: Path) -> KuuOSQiProcessTensorActuator:
    feature_bundle = _read_json(daemon_dir / "daemon_active_inference_feature_bundle_v0_1.json") or {}
    governor = _read_json(daemon_dir / "daemon_policy_flow_governor_v0_1.json") or {}
    return compile_qi_process_tensor_actuator(feature_bundle, governor)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor actuator v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_process_tensor_actuator(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_actuator_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
