#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

POLICIES = [
    "CONTINUE_HARMONIZED",
    "CONTINUE_WITH_COMPACT_MONITOR",
    "CONTINUE_AFTER_COMPACT",
    "SLOW_DOWN_AND_REOBSERVE",
    "BRANCH_EXPLORE_LIGHTLY",
    "HOLD_WITH_RECOVERY",
    "QUARANTINE_WITH_RETURN_PATH",
]

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
class KuuOSDaemonActiveInferenceResult:
    kernel_version: str
    kernel_status: str
    selected_policy: str
    selected_expected_free_energy: float
    variational_free_energy_proxy: float
    posterior_belief_state: dict[str, float]
    posterior_precision: float
    policy_free_energy_table: dict[str, dict[str, float]]
    policy_selection_reason: str
    hard_constraint_active: str | None
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
    path = daemon_dir / "daemon_tick_log_v0_1.json"
    if not path.is_file():
        return 0
    value = json.loads(path.read_text(encoding="utf-8"))
    return len(value) if isinstance(value, list) else 0


def infer_daemon_belief_state(inputs: Mapping[str, Any]) -> dict[str, float]:
    yinyang = inputs.get("yinyang_polarity_state")
    phase = inputs.get("four_image_phase")
    qi_mode = inputs.get("qi_policy_mode")
    qique = inputs.get("qique_regime")
    emptiness = inputs.get("emptiness_action")
    wa = inputs.get("wa_posture")
    tick_density = int(inputs.get("tick_density", 0) or 0)
    missing = int(inputs.get("missing_source_count", 0) or 0)

    boundary = 0.0
    if yinyang == "BOUNDARY_YIN_REQUIRED" or qi_mode == "QUARANTINE_REVIEW":
        boundary = 1.0
    elif qi_mode == "HOLD_FOR_DAEMON_REPAIR" or emptiness == "HOLD_OR_QUARANTINE_NONFINAL":
        boundary = 0.85

    uncertainty = _clamp(0.1 * missing)
    if qi_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"}:
        uncertainty = _clamp(uncertainty + 0.35)
    if yinyang in {"FALSE_YANG", "YIN_REOBSERVE_REQUIRED"}:
        uncertainty = _clamp(uncertainty + 0.25)
    if qique == "OBSERVATION_GAP":
        uncertainty = _clamp(uncertainty + 0.25)

    density = _clamp(tick_density / 10.0)
    if phase == "GREATER_YANG":
        density = _clamp(density + 0.35)
    if qique in {"OVERDIFFUSION", "LOCALIZED_MEMORY_CHANNEL"}:
        density = _clamp(density + 0.25)

    recovery = 0.0
    if wa in {"HOLD_WITH_RECOVERY", "QUARANTINE_WITH_RETURN_PATH"}:
        recovery = 0.85
    elif phase == "GREATER_YIN" or yinyang in {"YIN_STAGNATION", "SWITCHING_UNSTABLE"}:
        recovery = 0.65
    elif qi_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"}:
        recovery = 0.45

    action = 0.0
    if wa in {"CONTINUE_HARMONIZED", "CONTINUE_WITH_COMPACT_MONITOR", "CONTINUE_AFTER_COMPACT"}:
        action = 0.75
    if phase == "LESSER_YANG" or qi_mode == "CONTINUE_WITH_QI_MEMORY_MONITOR":
        action = max(action, 0.55)
    if wa == "BRANCH_EXPLORE_LIGHTLY":
        action = 0.6

    nihilism = 0.0
    if wa in {"HOLD_WITH_RECOVERY", "QUARANTINE_WITH_RETURN_PATH"}:
        nihilism = 0.35
    if qi_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"}:
        nihilism = _clamp(nihilism + 0.2)
    if phase == "GREATER_YIN":
        nihilism = _clamp(nihilism + 0.25)

    return {
        "boundary_pressure": boundary,
        "uncertainty": uncertainty,
        "density_pressure": density,
        "recovery_need": recovery,
        "action_drive": action,
        "nihilism_risk": nihilism,
    }


def posterior_precision(belief: Mapping[str, float]) -> float:
    penalty = 0.55 * belief["uncertainty"] + 0.25 * belief["boundary_pressure"] + 0.15 * belief["density_pressure"] + 0.05 * belief["nihilism_risk"]
    return _clamp(1.0 - penalty)


def variational_free_energy_proxy(belief: Mapping[str, float]) -> float:
    prediction_error = belief["uncertainty"] + belief["boundary_pressure"] + 0.5 * belief["density_pressure"]
    complexity = 0.25 * belief["recovery_need"] + 0.2 * belief["nihilism_risk"]
    return round(_clamp((prediction_error + complexity) / 2.2), 6)


def _policy_components(policy: str, belief: Mapping[str, float]) -> dict[str, float]:
    b = belief["boundary_pressure"]
    u = belief["uncertainty"]
    d = belief["density_pressure"]
    r = belief["recovery_need"]
    n = belief["nihilism_risk"]
    a = belief["action_drive"]

    if policy == "QUARANTINE_WITH_RETURN_PATH":
        risk = 0.1 * (1.0 - b) + 0.05 * u
        ambiguity = 0.35 * u
        epistemic_value = 0.25 * u + 0.15 * b
        control_cost = 0.55
        preference_misalignment = 0.05 if b >= 0.85 else 0.65
    elif policy == "HOLD_WITH_RECOVERY":
        risk = 0.25 * b + 0.15 * d
        ambiguity = 0.35 * u
        epistemic_value = 0.2 * u + 0.25 * r
        control_cost = 0.45
        preference_misalignment = 0.1 if r >= 0.6 else 0.45
    elif policy == "SLOW_DOWN_AND_REOBSERVE":
        risk = 0.2 * b + 0.1 * d
        ambiguity = 0.15 * u
        epistemic_value = 0.45 * u
        control_cost = 0.35
        preference_misalignment = 0.1 if u >= 0.45 else 0.35
    elif policy == "CONTINUE_AFTER_COMPACT":
        risk = 0.35 * b + 0.15 * d
        ambiguity = 0.3 * u
        epistemic_value = 0.15 * d
        control_cost = 0.3
        preference_misalignment = 0.08 if d >= 0.55 else 0.25
    elif policy == "CONTINUE_WITH_COMPACT_MONITOR":
        risk = 0.4 * b + 0.25 * d
        ambiguity = 0.35 * u
        epistemic_value = 0.15 * (u + d)
        control_cost = 0.25
        preference_misalignment = 0.12 if d < 0.65 and b < 0.5 else 0.35
    elif policy == "BRANCH_EXPLORE_LIGHTLY":
        risk = 0.55 * b + 0.25 * u + 0.2 * d
        ambiguity = 0.35 * u
        epistemic_value = 0.25 * (1.0 - a) + 0.2 * r
        control_cost = 0.4
        preference_misalignment = 0.08 if r >= 0.55 and b < 0.5 else 0.32
    else:  # CONTINUE_HARMONIZED
        risk = 0.65 * b + 0.35 * u + 0.3 * d
        ambiguity = 0.45 * u
        epistemic_value = 0.05 * a
        control_cost = 0.1
        preference_misalignment = 0.06 if a >= 0.6 and b < 0.3 and u < 0.4 and d < 0.65 else 0.55

    expected_free_energy = risk + ambiguity + control_cost + preference_misalignment - epistemic_value
    return {
        "expected_free_energy": round(max(0.0, expected_free_energy), 6),
        "risk": round(risk, 6),
        "ambiguity": round(ambiguity, 6),
        "epistemic_value": round(epistemic_value, 6),
        "control_cost": round(control_cost, 6),
        "preference_misalignment": round(preference_misalignment, 6),
    }


def select_policy_by_expected_free_energy(belief: Mapping[str, float]) -> tuple[str, dict[str, dict[str, float]], str, str | None]:
    if belief["boundary_pressure"] >= 0.85:
        table = {policy: _policy_components(policy, belief) for policy in POLICIES}
        return "QUARANTINE_WITH_RETURN_PATH", table, "hard_boundary_constraint", "boundary_pressure"
    table = {policy: _policy_components(policy, belief) for policy in POLICIES}
    selected = min(POLICIES, key=lambda policy: table[policy]["expected_free_energy"])
    return selected, table, "min_expected_free_energy", None


def run_active_inference_kernel(inputs: Mapping[str, Any]) -> KuuOSDaemonActiveInferenceResult:
    belief = infer_daemon_belief_state(inputs)
    precision = posterior_precision(belief)
    vfe = variational_free_energy_proxy(belief)
    selected, table, reason, hard = select_policy_by_expected_free_energy(belief)
    return KuuOSDaemonActiveInferenceResult(
        kernel_version="kuuos_runtime_daemon_active_inference_kernel_v0_1",
        kernel_status="ACTIVE_INFERENCE_POLICY_SELECTED",
        selected_policy=selected,
        selected_expected_free_energy=table[selected]["expected_free_energy"],
        variational_free_energy_proxy=vfe,
        posterior_belief_state={k: round(float(v), 6) for k, v in belief.items()},
        posterior_precision=round(precision, 6),
        policy_free_energy_table=table,
        policy_selection_reason=reason,
        hard_constraint_active=hard,
        source_summary={k: inputs.get(k) for k in [
            "yinyang_polarity_state",
            "four_image_phase",
            "qi_policy_mode",
            "qique_regime",
            "emptiness_action",
            "wa_posture",
            "tick_density",
            "missing_source_count",
        ]},
        allowed_projection=["daemon_active_inference_kernel_result", "selected_policy_advisory"],
    )


def read_and_run_daemon_active_inference_kernel(daemon_dir: Path) -> KuuOSDaemonActiveInferenceResult:
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
    return run_active_inference_kernel(inputs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS daemon Active Inference kernel v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_run_daemon_active_inference_kernel(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_active_inference_kernel_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
