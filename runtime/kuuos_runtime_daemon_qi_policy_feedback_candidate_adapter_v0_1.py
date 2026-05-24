#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyFeedbackCandidateAdapterResult:
    adapter_version: str
    adapter_status: str
    policy_feedback_class: str | None
    policy_flow_candidate_signal: str | None
    active_inference_candidate_signal: str | None
    candidate_adjustment_class: str
    candidate_weight_hints: dict[str, float]
    policy_candidate_constraints: list[str]
    active_inference_constraints: list[str]
    recommended_candidate_action: str
    candidate_priority: str
    candidate_only: bool
    nonfinal_marker: bool
    source_policy_feedback_surface_path: str | None
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


def _weights(**kwargs: float) -> dict[str, float]:
    base = {
        "safety_barrier": 0.0,
        "epistemic_value": 0.0,
        "trace_load_penalty": 0.0,
        "reentry_rollout_value": 0.0,
        "precondition_repair": 0.0,
        "action_precision": 0.0,
        "planning_horizon": 0.0,
    }
    base.update(kwargs)
    return base


def compile_qi_policy_feedback_candidate_adapter(
    *,
    policy_feedback_surface: Mapping[str, Any] | None = None,
    source_policy_feedback_surface_path: Path | None = None,
) -> KuuOSQiPolicyFeedbackCandidateAdapterResult:
    surface = policy_feedback_surface or {}
    policy_class = _s(surface, "policy_feedback_class")
    policy_signal = _s(surface, "policy_flow_candidate_signal")
    active_signal = _s(surface, "active_inference_candidate_signal")

    candidate_class = "CANDIDATE_ADJUSTMENT_NO_ACTION"
    weights = _weights()
    policy_constraints: list[str] = ["candidate_only", "nonfinal_marker", "no_policy_mutation"]
    active_constraints: list[str] = ["no_belief_update", "no_precision_commit"]
    action = "keep_current_candidate"
    priority = "low"

    if policy_class == "POLICY_FEEDBACK_SAFETY_HOLD":
        candidate_class = "CANDIDATE_ADJUSTMENT_SAFETY_HOLD"
        weights = _weights(safety_barrier=1.0, action_precision=-0.8, planning_horizon=-0.6)
        policy_constraints.extend(["prefer_hold_candidate", "block_reentry_escalation", "require_review_before_action"])
        active_constraints.extend(["increase_uncertainty", "reduce_action_precision"])
        action = "prefer_safe_hold_candidate"
        priority = "critical"
    elif policy_class == "POLICY_FEEDBACK_INFORMATION_GAIN":
        candidate_class = "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN"
        weights = _weights(epistemic_value=0.9, action_precision=-0.3, planning_horizon=-0.4)
        policy_constraints.extend(["prefer_observation_candidate", "defer_reentry_until_observed"])
        active_constraints.extend(["increase_epistemic_value", "preserve_uncertainty_visibility"])
        action = "prefer_observation_candidate"
        priority = "high"
    elif policy_class == "POLICY_FEEDBACK_TRACE_LOAD":
        candidate_class = "CANDIDATE_ADJUSTMENT_TRACE_LOAD_REDUCTION"
        weights = _weights(trace_load_penalty=0.85, planning_horizon=-0.5)
        policy_constraints.extend(["prefer_trace_load_reduction", "do_not_extend_rollout_until_compacted"])
        active_constraints.extend(["limit_policy_rollout", "preserve_compaction_debt_visibility"])
        action = "prefer_trace_load_reduction_candidate"
        priority = "medium"
    elif policy_class == "POLICY_FEEDBACK_REENTRY_ROLLOUT":
        candidate_class = "CANDIDATE_ADJUSTMENT_REENTRY_ROLLOUT"
        weights = _weights(reentry_rollout_value=0.75, planning_horizon=0.35, action_precision=-0.1)
        policy_constraints.extend(["use_reentry_as_candidate_rollout_only", "do_not_commit_reentry_as_truth"])
        active_constraints.extend(["candidate_efe_update_only", "do_not_raise_precision_without_observation"])
        action = "incorporate_candidate_reentry_rollout"
        priority = "high"
    elif policy_class == "POLICY_FEEDBACK_REENTRY_PRECONDITION_GAP":
        candidate_class = "CANDIDATE_ADJUSTMENT_PRECONDITION_REPAIR"
        weights = _weights(precondition_repair=0.9, reentry_rollout_value=-0.5, planning_horizon=-0.4)
        policy_constraints.extend(["repair_reentry_preconditions", "do_not_retry_reentry_without_inputs"])
        active_constraints.extend(["hold_reentry_precision", "preserve_precondition_gap"])
        action = "prefer_precondition_repair_candidate"
        priority = "medium"

    return KuuOSQiPolicyFeedbackCandidateAdapterResult(
        adapter_version="kuuos_runtime_daemon_qi_policy_feedback_candidate_adapter_v0_1",
        adapter_status="QI_POLICY_FEEDBACK_CANDIDATE_ADAPTED",
        policy_feedback_class=policy_class,
        policy_flow_candidate_signal=policy_signal,
        active_inference_candidate_signal=active_signal,
        candidate_adjustment_class=candidate_class,
        candidate_weight_hints=weights,
        policy_candidate_constraints=policy_constraints,
        active_inference_constraints=active_constraints,
        recommended_candidate_action=action,
        candidate_priority=priority,
        candidate_only=True,
        nonfinal_marker=True,
        source_policy_feedback_surface_path=str(source_policy_feedback_surface_path) if source_policy_feedback_surface_path else None,
        final_raw_state_path=_s(surface, "final_raw_state_path"),
        final_state_bundle_path=_s(surface, "final_state_bundle_path"),
    )


def read_and_compile_qi_policy_feedback_candidate_adapter(dispatch_dir: Path) -> KuuOSQiPolicyFeedbackCandidateAdapterResult:
    dispatch_dir = Path(dispatch_dir)
    surface_path = dispatch_dir / "qi_policy_feedback_surface_v0_1.json"
    return compile_qi_policy_feedback_candidate_adapter(
        policy_feedback_surface=_read_json(surface_path),
        source_policy_feedback_surface_path=surface_path if surface_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi policy feedback candidate adapter v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_policy_feedback_candidate_adapter(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_feedback_candidate_adapter_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
