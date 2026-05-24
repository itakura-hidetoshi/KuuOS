#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyCandidateAdmission:
    gate_version: str
    gate_status: str
    admission_decision: str
    admission_reason: str
    admitted_candidate_action: str | None
    candidate_adjustment_class: str | None
    candidate_priority: str | None
    gate_blockers: list[str]
    required_constraints_seen: list[str]
    missing_constraints: list[str]
    candidate_only: bool
    nonfinal_marker: bool
    source_candidate_adapter_path: str | None
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


def _has_authority_grant(payload: Mapping[str, Any]) -> list[str]:
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


def compile_qi_policy_candidate_admission(
    *,
    candidate_adapter: Mapping[str, Any] | None = None,
    source_candidate_adapter_path: Path | None = None,
) -> KuuOSQiPolicyCandidateAdmission:
    adapter = candidate_adapter or {}
    policy_constraints = _lst(adapter, "policy_candidate_constraints")
    active_constraints = _lst(adapter, "active_inference_constraints")
    all_constraints = set(policy_constraints + active_constraints)
    required = {
        "candidate_only",
        "nonfinal_marker",
        "no_policy_mutation",
        "no_belief_update",
        "no_precision_commit",
    }
    seen = sorted(required.intersection(all_constraints))
    missing = sorted(required.difference(all_constraints))
    blockers: list[str] = []

    candidate_only = bool(adapter.get("candidate_only"))
    nonfinal_marker = bool(adapter.get("nonfinal_marker"))
    authority_grants = _has_authority_grant(adapter)

    if not adapter:
        blockers.append("candidate_adapter_missing")
    if not candidate_only:
        blockers.append("candidate_only_missing_or_false")
    if not nonfinal_marker:
        blockers.append("nonfinal_marker_missing_or_false")
    if missing:
        blockers.append("required_constraints_missing")
    for flag in authority_grants:
        blockers.append(f"authority_grant_detected:{flag}")

    if blockers:
        decision = "QI_POLICY_CANDIDATE_NOT_ADMITTED"
        reason = blockers[0]
        action = None
    else:
        decision = "QI_POLICY_CANDIDATE_ADMITTED"
        reason = "candidate_only_nonfinal_constraints_satisfied"
        action = _s(adapter, "recommended_candidate_action")

    return KuuOSQiPolicyCandidateAdmission(
        gate_version="kuuos_runtime_daemon_qi_policy_candidate_admission_gate_v0_1",
        gate_status="QI_POLICY_CANDIDATE_ADMISSION_EVALUATED",
        admission_decision=decision,
        admission_reason=reason,
        admitted_candidate_action=action,
        candidate_adjustment_class=_s(adapter, "candidate_adjustment_class"),
        candidate_priority=_s(adapter, "candidate_priority"),
        gate_blockers=blockers,
        required_constraints_seen=seen,
        missing_constraints=missing,
        candidate_only=candidate_only,
        nonfinal_marker=nonfinal_marker,
        source_candidate_adapter_path=str(source_candidate_adapter_path) if source_candidate_adapter_path else None,
    )


def read_and_compile_qi_policy_candidate_admission(dispatch_dir: Path) -> KuuOSQiPolicyCandidateAdmission:
    dispatch_dir = Path(dispatch_dir)
    adapter_path = dispatch_dir / "qi_policy_feedback_candidate_adapter_v0_1.json"
    return compile_qi_policy_candidate_admission(
        candidate_adapter=_read_json(adapter_path),
        source_candidate_adapter_path=adapter_path if adapter_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS Qi policy candidate admission gate v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    admission = read_and_compile_qi_policy_candidate_admission(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_candidate_admission_gate_v0_1.json", admission.to_dict())
    print(json.dumps(admission.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
