#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyFlowCandidateInboxPacket:
    inbox_version: str
    inbox_status: str
    inbox_decision: str
    inbox_reason: str
    queued_candidate_available: bool
    queued_candidate_action: str | None
    queued_candidate_class: str | None
    queued_candidate_priority: str | None
    queued_candidate_weight_hints: dict[str, float]
    queued_policy_constraints: list[str]
    queued_active_inference_constraints: list[str]
    inbox_packet: dict[str, Any]
    source_receiver_path: str | None
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    append_only: bool
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


def compile_qi_policy_flow_candidate_inbox(
    *,
    receiver_result: Mapping[str, Any] | None = None,
    source_receiver_path: Path | None = None,
) -> KuuOSQiPolicyFlowCandidateInboxPacket:
    receiver = receiver_result or {}
    intake = receiver.get("normalized_policy_flow_intake")
    intake = intake if isinstance(intake, dict) else {}

    available = bool(receiver.get("policy_flow_candidate_available") or intake.get("policy_flow_candidate_available"))
    candidate_only = bool(receiver.get("candidate_only", intake.get("candidate_only", False)))
    nonfinal = bool(receiver.get("nonfinal_marker", intake.get("nonfinal_marker", False)))

    action = _s(receiver, "policy_flow_candidate_action") or _s(intake, "candidate_action")
    candidate_class = _s(receiver, "candidate_adjustment_class") or _s(intake, "candidate_adjustment_class")
    priority = _s(receiver, "candidate_priority") or _s(intake, "candidate_priority")
    weights = _weights(receiver.get("candidate_weight_hints") or intake.get("candidate_weight_hints"))
    policy_constraints = _lst(receiver.get("policy_candidate_constraints") or intake.get("policy_candidate_constraints"))
    active_constraints = _lst(receiver.get("active_inference_constraints") or intake.get("active_inference_constraints"))

    if available and candidate_only and nonfinal:
        decision = "QI_POLICY_FLOW_CANDIDATE_QUEUED"
        reason = "receiver_candidate_available_candidate_only_nonfinal"
        packet = {
            "queue_status": "queued_candidate_only",
            "candidate_action": action,
            "candidate_adjustment_class": candidate_class,
            "candidate_priority": priority,
            "candidate_weight_hints": weights,
            "policy_candidate_constraints": policy_constraints,
            "active_inference_constraints": active_constraints,
            "candidate_only": True,
            "nonfinal_marker": True,
            "append_only": True,
            "source": "qi_policy_flow_candidate_inbox_v0_1",
        }
    else:
        decision = "QI_POLICY_FLOW_CANDIDATE_NOT_QUEUED"
        reason = _s(receiver, "intake_reason") or _s(intake, "intake_reason") or "candidate_unavailable_or_boundary_missing"
        packet = {
            "queue_status": "blocked_candidate_only",
            "blocked": True,
            "block_reason": reason,
            "candidate_only": True,
            "nonfinal_marker": True,
            "append_only": True,
            "source": "qi_policy_flow_candidate_inbox_v0_1",
        }

    return KuuOSQiPolicyFlowCandidateInboxPacket(
        inbox_version="kuuos_runtime_daemon_qi_policy_flow_candidate_inbox_v0_1",
        inbox_status="QI_POLICY_FLOW_CANDIDATE_INBOX_COMPILED",
        inbox_decision=decision,
        inbox_reason=reason,
        queued_candidate_available=decision == "QI_POLICY_FLOW_CANDIDATE_QUEUED",
        queued_candidate_action=action if decision == "QI_POLICY_FLOW_CANDIDATE_QUEUED" else None,
        queued_candidate_class=candidate_class if decision == "QI_POLICY_FLOW_CANDIDATE_QUEUED" else None,
        queued_candidate_priority=priority if decision == "QI_POLICY_FLOW_CANDIDATE_QUEUED" else None,
        queued_candidate_weight_hints=weights if decision == "QI_POLICY_FLOW_CANDIDATE_QUEUED" else {},
        queued_policy_constraints=policy_constraints if decision == "QI_POLICY_FLOW_CANDIDATE_QUEUED" else [],
        queued_active_inference_constraints=active_constraints if decision == "QI_POLICY_FLOW_CANDIDATE_QUEUED" else [],
        inbox_packet=packet,
        source_receiver_path=str(source_receiver_path) if source_receiver_path else None,
        final_raw_state_path=_s(receiver, "final_raw_state_path"),
        final_state_bundle_path=_s(receiver, "final_state_bundle_path"),
        append_only=True,
        candidate_only=True,
        nonfinal_marker=True,
    )


def read_and_compile_qi_policy_flow_candidate_inbox(dispatch_dir: Path) -> KuuOSQiPolicyFlowCandidateInboxPacket:
    dispatch_dir = Path(dispatch_dir)
    receiver_path = dispatch_dir / "qi_policy_flow_handoff_receiver_v0_1.json"
    return compile_qi_policy_flow_candidate_inbox(
        receiver_result=_read_json(receiver_path),
        source_receiver_path=receiver_path if receiver_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi policy flow candidate inbox v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    packet = read_and_compile_qi_policy_flow_candidate_inbox(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_flow_candidate_inbox_v0_1.json", packet.to_dict())
    print(json.dumps(packet.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
