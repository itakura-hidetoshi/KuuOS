#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyFlowCandidateShadowAdmission:
    gate_version: str
    gate_status: str
    shadow_admission_decision: str
    shadow_admission_reason: str
    admitted_shadow_candidate_action: str | None
    admitted_shadow_candidate_class: str | None
    admitted_shadow_candidate_priority: str | None
    admitted_shadow_score: float
    admitted_shadow_grade: str | None
    gate_blockers: list[str]
    warning_terms: list[str]
    positive_terms: list[str]
    boundary_markers: dict[str, bool]
    source_shadow_evaluator_path: str | None
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


def _lst(payload: Mapping[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    return [str(item) for item in value] if isinstance(value, list) else []


def _f(payload: Mapping[str, Any], key: str) -> float:
    try:
        return float(payload.get(key, 0.0))
    except (TypeError, ValueError):
        return 0.0


def _authority_grants(payload: Mapping[str, Any]) -> list[str]:
    flags = [
        "grants_execution_authority",
        "grants_truth_authority",
        "grants_final_commitment_authority",
        "grants_memory_overwrite_authority",
        "grants_clinical_authority",
        "grants_theorem_authority",
        "grants_completed_identity_authority",
    ]
    return [flag for flag in flags if bool(payload.get(flag))]


def compile_qi_policy_flow_candidate_shadow_admission(
    *,
    shadow_evaluation: Mapping[str, Any] | None = None,
    source_shadow_evaluator_path: Path | None = None,
    minimum_shadow_score: float = 0.5,
) -> KuuOSQiPolicyFlowCandidateShadowAdmission:
    shadow = shadow_evaluation or {}
    score = _f(shadow, "candidate_shadow_score")
    blockers = _lst(shadow, "blocker_terms")
    warnings = _lst(shadow, "warning_terms")
    positives = _lst(shadow, "positive_terms")
    boundary_raw = shadow.get("boundary_markers")
    boundaries = {str(k): bool(v) for k, v in boundary_raw.items()} if isinstance(boundary_raw, dict) else {}

    gate_blockers: list[str] = []
    if not shadow:
        gate_blockers.append("shadow_evaluation_missing")
    if shadow.get("shadow_decision") != "QI_POLICY_FLOW_CANDIDATE_SHADOW_EVALUATED":
        gate_blockers.append("shadow_evaluation_not_evaluated")
    if blockers:
        gate_blockers.append("shadow_evaluator_blockers_present")
    if score < minimum_shadow_score:
        gate_blockers.append("shadow_score_below_minimum")
    for marker in ["append_only", "candidate_only", "nonfinal_marker", "no_policy_mutation", "no_belief_update", "no_precision_commit"]:
        if not boundaries.get(marker):
            gate_blockers.append(f"boundary_missing:{marker}")
    for flag in _authority_grants(shadow):
        gate_blockers.append(f"authority_grant_detected:{flag}")
    if not bool(shadow.get("shadow_only")):
        gate_blockers.append("shadow_only_missing_or_false")
    if not bool(shadow.get("read_only")):
        gate_blockers.append("read_only_missing_or_false")
    if not bool(shadow.get("candidate_only")):
        gate_blockers.append("candidate_only_missing_or_false")
    if not bool(shadow.get("nonfinal_marker")):
        gate_blockers.append("nonfinal_marker_missing_or_false")

    if gate_blockers:
        decision = "QI_POLICY_FLOW_SHADOW_CANDIDATE_NOT_ADMITTED"
        reason = gate_blockers[0]
        action = None
        candidate_class = None
        priority = None
        grade = None
        admitted_score = 0.0
    else:
        decision = "QI_POLICY_FLOW_SHADOW_CANDIDATE_ADMITTED"
        reason = "shadow_score_and_boundaries_satisfied"
        action = _s(shadow, "candidate_action")
        candidate_class = _s(shadow, "candidate_class")
        priority = _s(shadow, "candidate_priority")
        grade = _s(shadow, "candidate_shadow_grade")
        admitted_score = score

    return KuuOSQiPolicyFlowCandidateShadowAdmission(
        gate_version="kuuos_runtime_daemon_qi_policy_flow_candidate_shadow_admission_gate_v0_1",
        gate_status="QI_POLICY_FLOW_SHADOW_ADMISSION_EVALUATED",
        shadow_admission_decision=decision,
        shadow_admission_reason=reason,
        admitted_shadow_candidate_action=action,
        admitted_shadow_candidate_class=candidate_class,
        admitted_shadow_candidate_priority=priority,
        admitted_shadow_score=round(admitted_score, 4),
        admitted_shadow_grade=grade,
        gate_blockers=gate_blockers,
        warning_terms=warnings,
        positive_terms=positives,
        boundary_markers=boundaries,
        source_shadow_evaluator_path=str(source_shadow_evaluator_path) if source_shadow_evaluator_path else None,
        final_raw_state_path=_s(shadow, "final_raw_state_path"),
        final_state_bundle_path=_s(shadow, "final_state_bundle_path"),
        shadow_only=True,
        read_only=True,
        candidate_only=True,
        nonfinal_marker=True,
    )


def read_and_compile_qi_policy_flow_candidate_shadow_admission(dispatch_dir: Path) -> KuuOSQiPolicyFlowCandidateShadowAdmission:
    dispatch_dir = Path(dispatch_dir)
    shadow_path = dispatch_dir / "qi_policy_flow_candidate_shadow_evaluator_v0_1.json"
    return compile_qi_policy_flow_candidate_shadow_admission(
        shadow_evaluation=_read_json(shadow_path),
        source_shadow_evaluator_path=shadow_path if shadow_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS Qi policy flow candidate shadow admission v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_policy_flow_candidate_shadow_admission(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_flow_candidate_shadow_admission_gate_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
