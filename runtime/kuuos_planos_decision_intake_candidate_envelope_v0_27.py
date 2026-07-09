from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_decision_intake_candidate_envelope_v0_27"
SOURCE_VERSION = "kuuos_planos_weighted_decision_evidence_handoff_v0_26"

NON_AUTHORITY_BOUNDARY = {
    "envelope_owned_by_plan_os": True,
    "decisionos_intake_candidate_only": True,
    "source_evidence_preserved": True,
    "review_candidates_only": True,
    "decision_made": False,
    "selected_candidate_committed": False,
    "activation_authorization_granted": False,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class DecisionIntakeCandidateEnvelopeItem:
    candidate_id: str
    candidate_digest: str
    evidence_digest: str
    recommended_replan_route: str
    intake_role: str
    requires_probe: bool
    blocked_by_barrier: bool
    decisionos_review_open: bool
    decision_made: bool = False
    selected_candidate_committed: bool = False
    execution_granted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecisionIntakeCandidateEnvelopeReceipt:
    version: str
    source_version: str
    status: str
    source_handoff_receipt_digest: str
    envelope_item_count: int
    review_candidate_ids: list[str]
    probe_candidate_ids: list[str]
    barrier_candidate_ids: list[str]
    blocked_candidate_ids: list[str]
    envelope_items: list[dict[str, Any]]
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _seq(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [item for item in value if isinstance(item, Mapping)]
    return []


def _truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass"}
    return bool(value)


def _digest(value: Any) -> str:
    return sha(value)


def _boundary_blockers(handoff: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if handoff.get("version") != SOURCE_VERSION:
        blockers.append("source_handoff_version_invalid")
    if handoff.get("status") != "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_READY":
        blockers.append("source_handoff_not_ready")
    boundary = _m(handoff.get("boundary"))
    required_true = (
        "decision_evidence_only",
        "selection_owned_by_decision_os",
        "candidate_weights_advisory_only",
    )
    for field in required_true:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in (
        "selected_candidate_committed",
        "decision_made",
        "activation_authorization_granted",
        "actos_invoked",
        "execution_granted",
        "truth_authority_granted",
        "memory_overwrite_granted",
        "blocker_release_granted",
        "external_commit_granted",
    ):
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not handoff.get("receipt_digest"):
        blockers.append("source_handoff_receipt_digest_missing")
    return blockers


def build_decision_intake_candidate_envelope_receipt(
    *,
    handoff_receipt: Mapping[str, Any],
) -> DecisionIntakeCandidateEnvelopeReceipt:
    handoff = _m(handoff_receipt)
    blockers = _boundary_blockers(handoff)
    evidence_items = _seq(handoff.get("decision_evidence_items"))
    if not evidence_items:
        blockers.append("decision_evidence_items_empty")

    review_ids = set(str(x) for x in handoff.get("review_candidate_ids", []) if isinstance(x, str))
    probe_ids = set(str(x) for x in handoff.get("probe_candidate_ids", []) if isinstance(x, str))
    barrier_ids = set(str(x) for x in handoff.get("barrier_candidate_ids", []) if isinstance(x, str))
    source_blocked_ids = set(str(x) for x in handoff.get("blocked_candidate_ids", []) if isinstance(x, str))

    items: list[DecisionIntakeCandidateEnvelopeItem] = []
    blocked_candidate_ids: list[str] = list(source_blocked_ids)
    for evidence in evidence_items:
        cid = str(evidence.get("candidate_id", ""))
        cdigest = str(evidence.get("candidate_digest", ""))
        route = str(evidence.get("recommended_replan_route", ""))
        if not cid:
            blockers.append("candidate_id_missing")
            continue
        if not cdigest:
            blockers.append(f"candidate_digest_missing:{cid}")
            blocked_candidate_ids.append(cid)
        if _truthy(evidence.get("execution_ready")):
            blockers.append(f"candidate_execution_ready_forbidden:{cid}")
            blocked_candidate_ids.append(cid)
        if _truthy(evidence.get("selection_authority_granted")):
            blockers.append(f"candidate_selection_authority_forbidden:{cid}")
            blocked_candidate_ids.append(cid)
        barrier = _truthy(evidence.get("barrier_required")) or cid in barrier_ids
        probe = _truthy(evidence.get("probe_required")) or cid in probe_ids
        review_open = cid in review_ids and not barrier and bool(cdigest)
        if barrier:
            blocked_candidate_ids.append(cid)
        items.append(
            DecisionIntakeCandidateEnvelopeItem(
                candidate_id=cid,
                candidate_digest=cdigest,
                evidence_digest=_digest({"source": handoff.get("receipt_digest"), "candidate_id": cid, "candidate_digest": cdigest}),
                recommended_replan_route=route,
                intake_role="decisionos_review_candidate" if review_open else "held_for_replan_or_probe",
                requires_probe=probe,
                blocked_by_barrier=barrier,
                decisionos_review_open=review_open,
                decision_made=False,
                selected_candidate_committed=False,
                execution_granted=False,
            )
        )

    opened = [item.candidate_id for item in items if item.decisionos_review_open]
    status = "PLANOS_DECISION_INTAKE_CANDIDATE_ENVELOPE_READY" if not blockers else "PLANOS_DECISION_INTAKE_CANDIDATE_ENVELOPE_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_handoff_receipt_digest": str(handoff.get("receipt_digest", "")),
        "envelope_item_count": len(items),
        "review_candidate_ids": opened,
        "probe_candidate_ids": sorted(probe_ids),
        "barrier_candidate_ids": sorted(barrier_ids),
        "blocked_candidate_ids": sorted(set(blocked_candidate_ids)),
        "envelope_items": [item.to_dict() for item in items],
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return DecisionIntakeCandidateEnvelopeReceipt(
        receipt_digest=_digest(partial),
        **partial,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_decision_intake_candidate_envelope_v0_27.py HANDOFF_RECEIPT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_decision_intake_candidate_envelope_receipt(handoff_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
