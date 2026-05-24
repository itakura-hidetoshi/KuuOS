#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyFeedbackSurface:
    surface_version: str
    surface_status: str
    feedback_signal: str | None
    policy_adjustment_hint: str | None
    active_inference_hint: str | None
    policy_feedback_class: str
    policy_flow_candidate_signal: str
    active_inference_candidate_signal: str
    efe_weight_hint: str
    precision_adjustment_hint: str
    planning_horizon_hint: str
    safety_barrier_hint: str
    observation_value_hint: str
    compaction_load_hint: str
    reentry_rollout_hint: str
    feedback_priority: str | None
    candidate_only: bool
    nonfinal_marker: bool
    source_feedback_path: str | None
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
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


def _s(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    return str(value) if value is not None else None


def compile_qi_policy_feedback_surface(
    *,
    recovery_feedback: Mapping[str, Any] | None = None,
    source_feedback_path: Path | None = None,
) -> KuuOSQiPolicyFeedbackSurface:
    feedback = recovery_feedback or {}
    signal = _s(feedback, "feedback_signal")
    policy_hint = _s(feedback, "policy_adjustment_hint")
    active_hint = _s(feedback, "active_inference_hint")
    priority = _s(feedback, "feedback_priority")

    policy_class = "POLICY_FEEDBACK_NO_ACTION"
    policy_signal = "keep_current_policy_candidate"
    active_signal = "maintain_current_active_inference_settings"
    efe_weight = "unchanged"
    precision = "unchanged"
    horizon = "unchanged"
    safety = "unchanged"
    observation = "unchanged"
    compaction = "unchanged"
    reentry = "unchanged"

    if signal == "QI_FEEDBACK_HOLD_REQUIRED":
        policy_class = "POLICY_FEEDBACK_SAFETY_HOLD"
        policy_signal = "prefer_safe_hold_policy_candidate"
        active_signal = "increase_uncertainty_reduce_action_precision"
        efe_weight = "increase_risk_and_safety_terms"
        precision = "decrease_action_precision"
        horizon = "shorten_planning_horizon"
        safety = "raise_safety_barrier"
    elif signal == "QI_FEEDBACK_OBSERVATION_REQUIRED":
        policy_class = "POLICY_FEEDBACK_INFORMATION_GAIN"
        policy_signal = "prefer_observation_policy_candidate"
        active_signal = "increase_epistemic_value_weight"
        efe_weight = "increase_epistemic_value"
        precision = "maintain_or_lower_action_precision"
        horizon = "defer_long_horizon_reentry"
        observation = "observation_required"
    elif signal == "QI_FEEDBACK_COMPACTION_REQUIRED":
        policy_class = "POLICY_FEEDBACK_TRACE_LOAD"
        policy_signal = "prefer_trace_load_reduction_candidate"
        active_signal = "limit_policy_rollout_until_trace_load_reduced"
        efe_weight = "increase_trace_load_penalty"
        precision = "unchanged"
        horizon = "shorten_until_compaction"
        compaction = "compaction_required"
    elif signal == "QI_FEEDBACK_REENTRY_PERFORMED":
        policy_class = "POLICY_FEEDBACK_REENTRY_ROLLOUT"
        policy_signal = "incorporate_candidate_reentry_rollout"
        active_signal = "update_candidate_efe_landscape_noncommittally"
        efe_weight = "candidate_rollout_feedback_available"
        precision = "do_not_raise_precision_without_observation"
        horizon = "allow_bounded_candidate_extension"
        reentry = "bounded_reentry_feedback_available"
    elif signal == "QI_FEEDBACK_REENTRY_BLOCKED":
        policy_class = "POLICY_FEEDBACK_REENTRY_PRECONDITION_GAP"
        policy_signal = "prefer_precondition_repair_over_reentry"
        active_signal = "hold_reentry_until_required_inputs_exist"
        efe_weight = "increase_precondition_gap_penalty"
        precision = "lower_reentry_precision"
        horizon = "keep_short_horizon"
        reentry = "reentry_blocked"

    return KuuOSQiPolicyFeedbackSurface(
        surface_version="kuuos_runtime_daemon_qi_policy_feedback_surface_v0_1",
        surface_status="QI_POLICY_FEEDBACK_SURFACE_COMPILED",
        feedback_signal=signal,
        policy_adjustment_hint=policy_hint,
        active_inference_hint=active_hint,
        policy_feedback_class=policy_class,
        policy_flow_candidate_signal=policy_signal,
        active_inference_candidate_signal=active_signal,
        efe_weight_hint=efe_weight,
        precision_adjustment_hint=precision,
        planning_horizon_hint=horizon,
        safety_barrier_hint=safety,
        observation_value_hint=observation,
        compaction_load_hint=compaction,
        reentry_rollout_hint=reentry,
        feedback_priority=priority,
        candidate_only=True,
        nonfinal_marker=True,
        source_feedback_path=str(source_feedback_path) if source_feedback_path else None,
        final_raw_state_path=_s(feedback, "final_raw_state_path"),
        final_state_bundle_path=_s(feedback, "final_state_bundle_path"),
    )


def read_and_compile_qi_policy_feedback_surface(dispatch_dir: Path) -> KuuOSQiPolicyFeedbackSurface:
    dispatch_dir = Path(dispatch_dir)
    feedback_path = dispatch_dir / "qi_recovery_feedback_v0_1.json"
    return compile_qi_policy_feedback_surface(
        recovery_feedback=_read_json(feedback_path),
        source_feedback_path=feedback_path if feedback_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi policy feedback surface v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    surface = read_and_compile_qi_policy_feedback_surface(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_feedback_surface_v0_1.json", surface.to_dict())
    print(json.dumps(surface.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
