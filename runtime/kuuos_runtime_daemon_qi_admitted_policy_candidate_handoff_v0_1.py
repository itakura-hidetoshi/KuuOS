#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiAdmittedPolicyCandidateHandoff:
    handoff_version: str
    handoff_status: str
    handoff_decision: str
    handoff_reason: str
    admitted_candidate_action: str | None
    candidate_adjustment_class: str | None
    candidate_priority: str | None
    candidate_weight_hints: dict[str, float]
    policy_candidate_constraints: list[str]
    active_inference_constraints: list[str]
    policy_flow_handoff_payload: dict[str, Any]
    source_candidate_adapter_path: str | None
    source_admission_gate_path: str | None
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
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


def _weights(payload: Mapping[str, Any]) -> dict[str, float]:
    raw = payload.get("candidate_weight_hints")
    if not isinstance(raw, dict):
        return {}
    out: dict[str, float] = {}
    for key, value in raw.items():
        try:
            out[str(key)] = float(value)
        except (TypeError, ValueError):
            out[str(key)] = 0.0
    return out


def compile_qi_admitted_policy_candidate_handoff(
    *,
    candidate_adapter: Mapping[str, Any] | None = None,
    admission_gate: Mapping[str, Any] | None = None,
    source_candidate_adapter_path: Path | None = None,
    source_admission_gate_path: Path | None = None,
) -> KuuOSQiAdmittedPolicyCandidateHandoff:
    adapter = candidate_adapter or {}
    admission = admission_gate or {}
    admitted = admission.get("admission_decision") == "QI_POLICY_CANDIDATE_ADMITTED"
    adapter_present = bool(adapter)

    if admitted and adapter_present:
        decision = "QI_POLICY_CANDIDATE_HANDOFF_READY"
        reason = "admission_gate_admitted_candidate"
        action = _s(admission, "admitted_candidate_action") or _s(adapter, "recommended_candidate_action")
        payload = {
            "candidate_adjustment_class": _s(adapter, "candidate_adjustment_class"),
            "recommended_candidate_action": action,
            "candidate_priority": _s(adapter, "candidate_priority"),
            "candidate_weight_hints": _weights(adapter),
            "policy_candidate_constraints": _lst(adapter, "policy_candidate_constraints"),
            "active_inference_constraints": _lst(adapter, "active_inference_constraints"),
            "candidate_only": True,
            "nonfinal_marker": True,
            "source": "qi_admitted_policy_candidate_handoff_v0_1",
        }
    else:
        decision = "QI_POLICY_CANDIDATE_HANDOFF_BLOCKED"
        reason = _s(admission, "admission_reason") or "candidate_not_admitted_or_missing"
        action = None
        payload = {
            "candidate_only": True,
            "nonfinal_marker": True,
            "blocked": True,
            "block_reason": reason,
            "source": "qi_admitted_policy_candidate_handoff_v0_1",
        }

    return KuuOSQiAdmittedPolicyCandidateHandoff(
        handoff_version="kuuos_runtime_daemon_qi_admitted_policy_candidate_handoff_v0_1",
        handoff_status="QI_ADMITTED_POLICY_CANDIDATE_HANDOFF_COMPILED",
        handoff_decision=decision,
        handoff_reason=reason,
        admitted_candidate_action=action,
        candidate_adjustment_class=_s(adapter, "candidate_adjustment_class"),
        candidate_priority=_s(adapter, "candidate_priority"),
        candidate_weight_hints=_weights(adapter),
        policy_candidate_constraints=_lst(adapter, "policy_candidate_constraints"),
        active_inference_constraints=_lst(adapter, "active_inference_constraints"),
        policy_flow_handoff_payload=payload,
        source_candidate_adapter_path=str(source_candidate_adapter_path) if source_candidate_adapter_path else None,
        source_admission_gate_path=str(source_admission_gate_path) if source_admission_gate_path else None,
        final_raw_state_path=_s(adapter, "final_raw_state_path"),
        final_state_bundle_path=_s(adapter, "final_state_bundle_path"),
        candidate_only=True,
        nonfinal_marker=True,
    )


def read_and_compile_qi_admitted_policy_candidate_handoff(dispatch_dir: Path) -> KuuOSQiAdmittedPolicyCandidateHandoff:
    dispatch_dir = Path(dispatch_dir)
    adapter_path = dispatch_dir / "qi_policy_feedback_candidate_adapter_v0_1.json"
    admission_path = dispatch_dir / "qi_policy_candidate_admission_gate_v0_1.json"
    return compile_qi_admitted_policy_candidate_handoff(
        candidate_adapter=_read_json(adapter_path),
        admission_gate=_read_json(admission_path),
        source_candidate_adapter_path=adapter_path if adapter_path.is_file() else None,
        source_admission_gate_path=admission_path if admission_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi admitted policy candidate handoff v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    handoff = read_and_compile_qi_admitted_policy_candidate_handoff(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_admitted_policy_candidate_handoff_v0_1.json", handoff.to_dict())
    print(json.dumps(handoff.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
