#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiPolicyFlowCandidateIntakeView:
    view_version: str
    view_status: str
    view_decision: str
    view_reason: str
    policy_flow_view_available: bool
    candidate_action: str | None
    candidate_class: str | None
    candidate_priority: str | None
    candidate_weight_hints: dict[str, float]
    policy_constraints: list[str]
    active_inference_constraints: list[str]
    boundary_markers: dict[str, bool]
    policy_flow_candidate_view: dict[str, Any]
    source_inbox_path: str | None
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


def compile_qi_policy_flow_candidate_intake_view(
    *,
    inbox_packet: Mapping[str, Any] | None = None,
    source_inbox_path: Path | None = None,
) -> KuuOSQiPolicyFlowCandidateIntakeView:
    inbox = inbox_packet or {}
    packet = inbox.get("inbox_packet")
    packet = packet if isinstance(packet, dict) else {}

    queued = bool(inbox.get("queued_candidate_available")) and inbox.get("inbox_decision") == "QI_POLICY_FLOW_CANDIDATE_QUEUED"
    append_only = bool(inbox.get("append_only", packet.get("append_only", False)))
    candidate_only = bool(inbox.get("candidate_only", packet.get("candidate_only", False)))
    nonfinal = bool(inbox.get("nonfinal_marker", packet.get("nonfinal_marker", False)))

    action = _s(inbox, "queued_candidate_action") or _s(packet, "candidate_action")
    candidate_class = _s(inbox, "queued_candidate_class") or _s(packet, "candidate_adjustment_class")
    priority = _s(inbox, "queued_candidate_priority") or _s(packet, "candidate_priority")
    weights = _weights(inbox.get("queued_candidate_weight_hints") or packet.get("candidate_weight_hints"))
    policy_constraints = _lst(inbox.get("queued_policy_constraints") or packet.get("policy_candidate_constraints"))
    active_constraints = _lst(inbox.get("queued_active_inference_constraints") or packet.get("active_inference_constraints"))

    boundaries = {
        "append_only": append_only,
        "candidate_only": candidate_only,
        "nonfinal_marker": nonfinal,
        "no_policy_mutation": "no_policy_mutation" in policy_constraints,
        "no_belief_update": "no_belief_update" in active_constraints,
        "no_precision_commit": "no_precision_commit" in active_constraints,
    }

    if queued and all(boundaries.values()):
        decision = "QI_POLICY_FLOW_CANDIDATE_VIEW_READY"
        reason = "queued_candidate_with_required_boundaries"
        available = True
        view = {
            "view_status": "ready_candidate_only",
            "candidate_action": action,
            "candidate_class": candidate_class,
            "candidate_priority": priority,
            "candidate_weight_hints": weights,
            "policy_constraints": policy_constraints,
            "active_inference_constraints": active_constraints,
            "boundary_markers": boundaries,
            "candidate_only": True,
            "nonfinal_marker": True,
            "append_only": True,
            "source": "qi_policy_flow_candidate_intake_view_v0_1",
        }
    else:
        decision = "QI_POLICY_FLOW_CANDIDATE_VIEW_BLOCKED"
        reason = _s(inbox, "inbox_reason") or _s(packet, "block_reason") or "queued_candidate_or_boundary_missing"
        available = False
        view = {
            "view_status": "blocked_candidate_only",
            "blocked": True,
            "block_reason": reason,
            "boundary_markers": boundaries,
            "candidate_only": True,
            "nonfinal_marker": True,
            "append_only": True,
            "source": "qi_policy_flow_candidate_intake_view_v0_1",
        }

    return KuuOSQiPolicyFlowCandidateIntakeView(
        view_version="kuuos_runtime_daemon_qi_policy_flow_candidate_intake_view_v0_1",
        view_status="QI_POLICY_FLOW_CANDIDATE_INTAKE_VIEW_COMPILED",
        view_decision=decision,
        view_reason=reason,
        policy_flow_view_available=available,
        candidate_action=action if available else None,
        candidate_class=candidate_class if available else None,
        candidate_priority=priority if available else None,
        candidate_weight_hints=weights if available else {},
        policy_constraints=policy_constraints if available else [],
        active_inference_constraints=active_constraints if available else [],
        boundary_markers=boundaries,
        policy_flow_candidate_view=view,
        source_inbox_path=str(source_inbox_path) if source_inbox_path else None,
        final_raw_state_path=_s(inbox, "final_raw_state_path"),
        final_state_bundle_path=_s(inbox, "final_state_bundle_path"),
        append_only=True,
        candidate_only=True,
        nonfinal_marker=True,
    )


def read_and_compile_qi_policy_flow_candidate_intake_view(dispatch_dir: Path) -> KuuOSQiPolicyFlowCandidateIntakeView:
    dispatch_dir = Path(dispatch_dir)
    inbox_path = dispatch_dir / "qi_policy_flow_candidate_inbox_v0_1.json"
    return compile_qi_policy_flow_candidate_intake_view(
        inbox_packet=_read_json(inbox_path),
        source_inbox_path=inbox_path if inbox_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi policy flow candidate intake view v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    view = read_and_compile_qi_policy_flow_candidate_intake_view(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_policy_flow_candidate_intake_view_v0_1.json", view.to_dict())
    print(json.dumps(view.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
