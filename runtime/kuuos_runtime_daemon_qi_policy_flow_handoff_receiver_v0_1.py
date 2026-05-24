#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyFlowHandoffReceiverResult:
    receiver_version: str
    receiver_status: str
    intake_decision: str
    intake_reason: str
    policy_flow_candidate_available: bool
    policy_flow_candidate_action: str | None
    candidate_adjustment_class: str | None
    candidate_priority: str | None
    candidate_weight_hints: dict[str, float]
    policy_candidate_constraints: list[str]
    active_inference_constraints: list[str]
    normalized_policy_flow_intake: dict[str, Any]
    source_handoff_path: str | None
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


def compile_qi_policy_flow_handoff_receiver(
    *,
    admitted_policy_candidate_handoff: Mapping[str, Any] | None = None,
    source_handoff_path: Path | None = None,
) -> KuuOSQiPolicyFlowHandoffReceiverResult:
    handoff = admitted_policy_candidate_handoff or {}
    payload = handoff.get("policy_flow_handoff_payload")
    payload = payload if isinstance(payload, dict) else {}

    handoff_ready = handoff.get("handoff_decision") == "QI_POLICY_CANDIDATE_HANDOFF_READY"
    payload_blocked = bool(payload.get("blocked"))
    candidate_only = bool(handoff.get("candidate_only", payload.get("candidate_only", False)))
    nonfinal_marker = bool(handoff.get("nonfinal_marker", payload.get("nonfinal_marker", False)))

    if handoff_ready and payload and not payload_blocked and candidate_only and nonfinal_marker:
        decision = "QI_POLICY_FLOW_CANDIDATE_INTAKE_READY"
        reason = "handoff_ready_candidate_only_nonfinal"
        available = True
        action = _s(payload, "recommended_candidate_action") or _s(handoff, "admitted_candidate_action")
    else:
        decision = "QI_POLICY_FLOW_CANDIDATE_INTAKE_BLOCKED"
        reason = _s(payload, "block_reason") or _s(handoff, "handoff_reason") or "handoff_not_ready"
        available = False
        action = None

    candidate_adjustment_class = _s(payload, "candidate_adjustment_class") or _s(handoff, "candidate_adjustment_class")
    candidate_priority = _s(payload, "candidate_priority") or _s(handoff, "candidate_priority")
    weights = _weights(payload.get("candidate_weight_hints") or handoff.get("candidate_weight_hints"))
    policy_constraints = _lst(payload.get("policy_candidate_constraints") or handoff.get("policy_candidate_constraints"))
    active_constraints = _lst(payload.get("active_inference_constraints") or handoff.get("active_inference_constraints"))

    normalized = {
        "policy_flow_candidate_available": available,
        "candidate_action": action,
        "candidate_adjustment_class": candidate_adjustment_class,
        "candidate_priority": candidate_priority,
        "candidate_weight_hints": weights,
        "policy_candidate_constraints": policy_constraints,
        "active_inference_constraints": active_constraints,
        "candidate_only": True,
        "nonfinal_marker": True,
        "source": "qi_policy_flow_handoff_receiver_v0_1",
        "intake_decision": decision,
        "intake_reason": reason,
    }

    return KuuOSQiPolicyFlowHandoffReceiverResult(
        receiver_version="kuuos_runtime_daemon_qi_policy_flow_handoff_receiver_v0_1",
        receiver_status="QI_POLICY_FLOW_HANDOFF_RECEIVED",
        intake_decision=decision,
        intake_reason=reason,
        policy_flow_candidate_available=available,
        policy_flow_candidate_action=action,
        candidate_adjustment_class=candidate_adjustment_class,
        candidate_priority=candidate_priority,
        candidate_weight_hints=weights,
        policy_candidate_constraints=policy_constraints,
        active_inference_constraints=active_constraints,
        normalized_policy_flow_intake=normalized,
        source_handoff_path=str(source_handoff_path) if source_handoff_path else None,
        final_raw_state_path=_s(handoff, "final_raw_state_path"),
        final_state_bundle_path=_s(handoff, "final_state_bundle_path"),
        candidate_only=True,
        nonfinal_marker=True,
    )


def read_and_compile_qi_policy_flow_handoff_receiver(dispatch_dir: Path) -> KuuOSQiPolicyFlowHandoffReceiverResult:
    dispatch_dir = Path(dispatch_dir)
    handoff_path = dispatch_dir / "qi_admitted_policy_candidate_handoff_v0_1.json"
    return compile_qi_policy_flow_handoff_receiver(
        admitted_policy_candidate_handoff=_read_json(handoff_path),
        source_handoff_path=handoff_path if handoff_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi policy flow handoff receiver v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_policy_flow_handoff_receiver(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_flow_handoff_receiver_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
