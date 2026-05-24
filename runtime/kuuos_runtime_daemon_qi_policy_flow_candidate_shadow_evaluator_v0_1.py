#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyFlowCandidateShadowEvaluation:
    evaluator_version: str
    evaluator_status: str
    shadow_decision: str
    shadow_reason: str
    candidate_shadow_score: float
    candidate_shadow_grade: str
    candidate_action: str | None
    candidate_class: str | None
    candidate_priority: str | None
    positive_terms: list[str]
    warning_terms: list[str]
    blocker_terms: list[str]
    boundary_markers: dict[str, bool]
    source_intake_view_path: str | None
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    shadow_only: bool
    read_only: bool
    candidate_only: bool
    nonfinal_marker: bool
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


def _lst(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list) else []


def _weights(value: Any) -> dict[str, float]:
    if not isinstance(value, dict):
        return {}
    out: dict[str, float] = {}
    for key, raw in value.items():
        try:
            out[str(key)] = float(raw)
        except (TypeError, ValueError):
            out[str(key)] = 0.0
    return out


def _grade(score: float) -> str:
    if score >= 0.75:
        return "strong_shadow_candidate"
    if score >= 0.5:
        return "moderate_shadow_candidate"
    if score > 0.0:
        return "weak_shadow_candidate"
    return "blocked_shadow_candidate"


def compile_qi_policy_flow_candidate_shadow_evaluation(
    *,
    intake_view: Mapping[str, Any] | None = None,
    source_intake_view_path: Path | None = None,
) -> KuuOSQiPolicyFlowCandidateShadowEvaluation:
    view = intake_view or {}
    candidate_view = view.get("policy_flow_candidate_view")
    candidate_view = candidate_view if isinstance(candidate_view, dict) else {}
    boundaries_raw = view.get("boundary_markers") or candidate_view.get("boundary_markers")
    boundaries_raw = boundaries_raw if isinstance(boundaries_raw, dict) else {}
    boundaries = {str(k): bool(v) for k, v in boundaries_raw.items()}

    available = bool(view.get("policy_flow_view_available")) and view.get("view_decision") == "QI_POLICY_FLOW_CANDIDATE_VIEW_READY"
    action = _s(view, "candidate_action") or _s(candidate_view, "candidate_action")
    candidate_class = _s(view, "candidate_class") or _s(candidate_view, "candidate_class")
    priority = _s(view, "candidate_priority") or _s(candidate_view, "candidate_priority")
    weights = _weights(view.get("candidate_weight_hints") or candidate_view.get("candidate_weight_hints"))
    policy_constraints = _lst(view.get("policy_constraints") or candidate_view.get("policy_constraints"))
    active_constraints = _lst(view.get("active_inference_constraints") or candidate_view.get("active_inference_constraints"))

    required_boundaries = [
        "append_only",
        "candidate_only",
        "nonfinal_marker",
        "no_policy_mutation",
        "no_belief_update",
        "no_precision_commit",
    ]
    missing = [name for name in required_boundaries if not boundaries.get(name)]
    positives: list[str] = []
    warnings: list[str] = []
    blockers: list[str] = []

    if not available:
        blockers.append("intake_view_not_ready")
    if missing:
        blockers.append("required_boundary_missing")
        warnings.extend([f"missing:{name}" for name in missing])
    if not action:
        blockers.append("candidate_action_missing")
    if "no_policy_mutation" in policy_constraints:
        positives.append("policy_mutation_blocked")
    if "no_belief_update" in active_constraints:
        positives.append("belief_update_blocked")
    if "no_precision_commit" in active_constraints:
        positives.append("precision_commit_blocked")
    if weights.get("safety_barrier", 0.0) > 0:
        positives.append("safety_barrier_visible")
    if weights.get("epistemic_value", 0.0) > 0:
        positives.append("epistemic_value_visible")
    if weights.get("trace_load_penalty", 0.0) > 0:
        warnings.append("trace_load_penalty_visible")
    if weights.get("action_precision", 0.0) > 0:
        warnings.append("positive_action_precision_requires_later_review")

    if blockers:
        score = 0.0
        decision = "QI_POLICY_FLOW_CANDIDATE_SHADOW_BLOCKED"
        reason = blockers[0]
    else:
        base = 0.4
        boundary_bonus = 0.3
        positive_bonus = min(0.2, len(positives) * 0.05)
        priority_bonus = 0.1 if priority in {"high", "critical"} else 0.05 if priority == "medium" else 0.0
        warning_penalty = min(0.2, len(warnings) * 0.05)
        score = max(0.0, min(1.0, base + boundary_bonus + positive_bonus + priority_bonus - warning_penalty))
        decision = "QI_POLICY_FLOW_CANDIDATE_SHADOW_EVALUATED"
        reason = "candidate_shadow_evaluated_nonexecuting"

    return KuuOSQiPolicyFlowCandidateShadowEvaluation(
        evaluator_version="kuuos_runtime_daemon_qi_policy_flow_candidate_shadow_evaluator_v0_1",
        evaluator_status="QI_POLICY_FLOW_CANDIDATE_SHADOW_EVALUATION_COMPILED",
        shadow_decision=decision,
        shadow_reason=reason,
        candidate_shadow_score=round(score, 4),
        candidate_shadow_grade=_grade(score),
        candidate_action=action if not blockers else None,
        candidate_class=candidate_class if not blockers else None,
        candidate_priority=priority if not blockers else None,
        positive_terms=positives,
        warning_terms=warnings,
        blocker_terms=blockers,
        boundary_markers=boundaries,
        source_intake_view_path=str(source_intake_view_path) if source_intake_view_path else None,
        final_raw_state_path=_s(view, "final_raw_state_path"),
        final_state_bundle_path=_s(view, "final_state_bundle_path"),
        shadow_only=True,
        read_only=True,
        candidate_only=True,
        nonfinal_marker=True,
    )


def read_and_compile_qi_policy_flow_candidate_shadow_evaluation(dispatch_dir: Path) -> KuuOSQiPolicyFlowCandidateShadowEvaluation:
    dispatch_dir = Path(dispatch_dir)
    view_path = dispatch_dir / "qi_policy_flow_candidate_intake_view_v0_1.json"
    return compile_qi_policy_flow_candidate_shadow_evaluation(
        intake_view=_read_json(view_path),
        source_intake_view_path=view_path if view_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi policy flow candidate shadow evaluation v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_policy_flow_candidate_shadow_evaluation(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_flow_candidate_shadow_evaluator_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
