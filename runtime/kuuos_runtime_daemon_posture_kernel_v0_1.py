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
class KuuOSDaemonPostureKernelResult:
    kernel_version: str
    kernel_status: str
    final_runtime_posture: str
    posture_reason: str
    posture_confidence: float
    uncertainty_score: float
    precision_score: float
    density_pressure: float
    boundary_pressure: float
    recovery_need: float
    nihilism_risk: float
    action_drive: float
    source_summary: dict[str, Any]
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


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _tick_density(daemon_dir: Path) -> int:
    tick_log_path = daemon_dir / "daemon_tick_log_v0_1.json"
    if not tick_log_path.is_file():
        return 0
    value = json.loads(tick_log_path.read_text(encoding="utf-8"))
    return len(value) if isinstance(value, list) else 0


def compile_daemon_posture_kernel(inputs: Mapping[str, Any]) -> KuuOSDaemonPostureKernelResult:
    yinyang_state = inputs.get("yinyang_polarity_state")
    four_phase = inputs.get("four_image_phase")
    qi_mode = inputs.get("qi_policy_mode")
    qique_regime = inputs.get("qique_regime")
    emptiness_action = inputs.get("emptiness_action")
    wa_posture = inputs.get("wa_posture")
    tick_density = int(inputs.get("tick_density", 0) or 0)
    missing_count = int(inputs.get("missing_source_count", 0) or 0)

    boundary_pressure = 0.0
    if yinyang_state == "BOUNDARY_YIN_REQUIRED" or qi_mode == "QUARANTINE_REVIEW":
        boundary_pressure = 1.0
    elif qi_mode == "HOLD_FOR_DAEMON_REPAIR":
        boundary_pressure = 0.9
    elif emptiness_action == "HOLD_OR_QUARANTINE_NONFINAL":
        boundary_pressure = 0.85

    density_pressure = _clamp(tick_density / 10.0)
    if qique_regime in {"OVERDIFFUSION", "LOCALIZED_MEMORY_CHANNEL"}:
        density_pressure = _clamp(density_pressure + 0.25)
    if four_phase == "GREATER_YANG":
        density_pressure = _clamp(density_pressure + 0.35)

    recovery_need = 0.0
    if wa_posture in {"HOLD_WITH_RECOVERY", "QUARANTINE_WITH_RETURN_PATH"}:
        recovery_need = 0.85
    elif four_phase == "GREATER_YIN" or yinyang_state in {"YIN_STAGNATION", "SWITCHING_UNSTABLE"}:
        recovery_need = 0.65
    elif qi_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"}:
        recovery_need = 0.45

    action_drive = 0.0
    if wa_posture in {"CONTINUE_HARMONIZED", "CONTINUE_WITH_COMPACT_MONITOR", "CONTINUE_AFTER_COMPACT"}:
        action_drive = 0.75
    elif wa_posture == "BRANCH_EXPLORE_LIGHTLY" or four_phase == "LESSER_YANG":
        action_drive = 0.55
    elif qi_mode == "CONTINUE_WITH_QI_MEMORY_MONITOR":
        action_drive = 0.5

    nihilism_risk = 0.0
    if wa_posture in {"HOLD_WITH_RECOVERY", "QUARANTINE_WITH_RETURN_PATH"}:
        nihilism_risk = 0.35
    if qi_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"}:
        nihilism_risk = _clamp(nihilism_risk + 0.2)
    if four_phase == "GREATER_YIN":
        nihilism_risk = _clamp(nihilism_risk + 0.25)

    uncertainty = _clamp(0.1 * missing_count)
    if qi_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"}:
        uncertainty = _clamp(uncertainty + 0.35)
    if yinyang_state in {"FALSE_YANG", "YIN_REOBSERVE_REQUIRED"}:
        uncertainty = _clamp(uncertainty + 0.25)
    if qique_regime == "OBSERVATION_GAP":
        uncertainty = _clamp(uncertainty + 0.25)

    precision = _clamp(1.0 - uncertainty - (0.2 if boundary_pressure >= 0.85 else 0.0))

    if boundary_pressure >= 0.85:
        posture = "QUARANTINE_WITH_RETURN_PATH"
        reason = "boundary_pressure_dominates"
        status = "POSTURE_KERNEL_BOUNDARY_HOLD"
    elif recovery_need >= 0.8:
        posture = "HOLD_WITH_RECOVERY"
        reason = "recovery_need_dominates"
        status = "POSTURE_KERNEL_RECOVERY_HOLD"
    elif uncertainty >= 0.6:
        posture = "SLOW_DOWN_AND_REOBSERVE"
        reason = "uncertainty_requires_reobservation"
        status = "POSTURE_KERNEL_REOBSERVE"
    elif density_pressure >= 0.65:
        posture = "CONTINUE_AFTER_COMPACT"
        reason = "density_requires_compact_continue"
        status = "POSTURE_KERNEL_COMPACT_CONTINUE"
    elif wa_posture == "BRANCH_EXPLORE_LIGHTLY" or yinyang_state == "YIN_STAGNATION":
        posture = "BRANCH_EXPLORE_LIGHTLY"
        reason = "stagnation_needs_light_branching"
        status = "POSTURE_KERNEL_LIGHT_BRANCH"
    elif wa_posture in {"CONTINUE_WITH_COMPACT_MONITOR", "CONTINUE_AFTER_COMPACT"}:
        posture = str(wa_posture)
        reason = "wa_posture_preserved_compact"
        status = "POSTURE_KERNEL_WA_COMPACT"
    else:
        posture = "CONTINUE_HARMONIZED"
        reason = "bounded_high_precision_continue"
        status = "POSTURE_KERNEL_HARMONIZED"

    confidence = _clamp((precision + (1.0 - density_pressure * 0.5) + (1.0 - nihilism_risk * 0.5)) / 3.0)

    return KuuOSDaemonPostureKernelResult(
        kernel_version="kuuos_runtime_daemon_posture_kernel_v0_1",
        kernel_status=status,
        final_runtime_posture=posture,
        posture_reason=reason,
        posture_confidence=confidence,
        uncertainty_score=uncertainty,
        precision_score=precision,
        density_pressure=density_pressure,
        boundary_pressure=boundary_pressure,
        recovery_need=recovery_need,
        nihilism_risk=nihilism_risk,
        action_drive=action_drive,
        source_summary={
            "yinyang_polarity_state": yinyang_state,
            "four_image_phase": four_phase,
            "qi_policy_mode": qi_mode,
            "qique_regime": qique_regime,
            "emptiness_action": emptiness_action,
            "wa_posture": wa_posture,
            "tick_density": tick_density,
            "missing_source_count": missing_count,
        },
        allowed_projection=["daemon_posture_kernel_result", "final_runtime_posture_advisory"],
    )


def read_and_compile_daemon_posture_kernel(daemon_dir: Path) -> KuuOSDaemonPostureKernelResult:
    yy = _read_json(daemon_dir / "daemon_yinyang_polarity_result_v0_1.json")
    four = _read_json(daemon_dir / "daemon_four_image_phase_result_v0_1.json")
    policy = _read_json(daemon_dir / "daemon_qi_policy_result_v0_1.json")
    qique = policy.get("daemon_qique_gauge") if isinstance(policy, dict) and isinstance(policy.get("daemon_qique_gauge"), dict) else None
    emptiness = _read_json(daemon_dir / "daemon_emptiness_gate_result_v0_1.json")
    wa = _read_json(daemon_dir / "daemon_wa_function_result_v0_1.json")
    sources = [yy, four, policy, emptiness, wa]
    inputs = {
        "yinyang_polarity_state": yy.get("yinyang_polarity_state") if yy else None,
        "four_image_phase": four.get("four_image_phase") if four else None,
        "qi_policy_mode": policy.get("recommended_tick_mode") if policy else None,
        "qique_regime": qique.get("qique_regime") if qique else None,
        "emptiness_action": emptiness.get("recommended_emptiness_action") if emptiness else None,
        "wa_posture": wa.get("recommended_runtime_posture") if wa else None,
        "tick_density": _tick_density(daemon_dir),
        "missing_source_count": sum(1 for source in sources if source is None),
    }
    return compile_daemon_posture_kernel(inputs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS daemon posture kernel v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_daemon_posture_kernel(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_posture_kernel_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
