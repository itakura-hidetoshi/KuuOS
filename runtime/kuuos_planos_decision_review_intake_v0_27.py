from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_decision_review_intake_v0_27"
SOURCE_VERSION = "kuuos_planos_weighted_decision_evidence_handoff_v0_26"

NON_AUTHORITY_BOUNDARY = {
    "intake_owned_by_plan_os": True,
    "review_owned_by_decision_os": True,
    "decision_review_input_only": True,
    "silent_substitution_forbidden": True,
    "barrier_candidate_review_blocked_here": True,
    "probe_candidate_review_flag_required": True,
    "candidate_selection_authority_granted": False,
    "decision_made": False,
    "decision_receipt_issued": False,
    "activation_authorization_granted": False,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class DecisionReviewItem:
    candidate_id: str
    candidate_digest: str
    advisory_score_digest: str
    recommended_replan_route: str
    probe_required: bool
    retained_by_planos: bool
    review_reason_digest: str
    decisionos_review_required: bool = True
    selectable_here: bool = False
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecisionReviewIntakeReceipt:
    version: str
    source_version: str
    status: str
    source_handoff_receipt_digest: str
    review_item_count: int
    review_candidate_ids: list[str]
    probe_candidate_ids: list[str]
    excluded_barrier_candidate_ids: list[str]
    decision_review_items: list[dict[str, Any]]
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
    for required in (
        "handoff_owned_by_plan_os",
        "selection_owned_by_decision_os",
        "candidate_weights_advisory_only",
        "decision_evidence_only",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
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
        if boundary.get(closed) is not False:
            blockers.append(f"source_boundary_{closed}_promoted")
    if not handoff.get("receipt_digest"):
        blockers.append("source_handoff_receipt_digest_missing")
    return blockers


def build_decision_review_intake_receipt(
    *,
    handoff_receipt: Mapping[str, Any],
) -> DecisionReviewIntakeReceipt:
    handoff = _m(handoff_receipt)
    blockers = _boundary_blockers(handoff)
    evidence_items = _seq(handoff.get("decision_evidence_items"))
    if not evidence_items:
        blockers.append("decision_evidence_items_empty")

    declared_review_ids = [str(x) for x in handoff.get("review_candidate_ids", []) if isinstance(x, str)]
    declared_probe_ids = set(str(x) for x in handoff.get("probe_candidate_ids", []) if isinstance(x, str))
    declared_barrier_ids = set(str(x) for x in handoff.get("barrier_candidate_ids", []) if isinstance(x, str))

    items: list[DecisionReviewItem] = []
    excluded_barrier_ids: list[str] = []
    actual_review_ids: list[str] = []
    seen_ids: set[str] = set()

    for evidence in evidence_items:
        cid = str(evidence.get("candidate_id", ""))
        if not cid:
            blockers.append("candidate_id_missing")
            continue
        if cid in seen_ids:
            blockers.append(f"candidate_id_duplicate:{cid}")
        seen_ids.add(cid)
        cdigest = str(evidence.get("candidate_digest", ""))
        if not cdigest:
            blockers.append(f"candidate_digest_missing:{cid}")
        if _truthy(evidence.get("execution_ready")):
            blockers.append(f"candidate_execution_ready_forbidden:{cid}")
        if _truthy(evidence.get("selection_authority_granted")):
            blockers.append(f"candidate_selection_authority_forbidden:{cid}")

        barrier = _truthy(evidence.get("barrier_required")) or cid in declared_barrier_ids
        probe = _truthy(evidence.get("probe_required")) or cid in declared_probe_ids
        eligible = _truthy(evidence.get("eligible_for_decisionos_review"))
        if barrier:
            excluded_barrier_ids.append(cid)
            continue
        if eligible:
            actual_review_ids.append(cid)
            items.append(
                DecisionReviewItem(
                    candidate_id=cid,
                    candidate_digest=cdigest,
                    advisory_score_digest=str(evidence.get("advisory_score_digest", "")),
                    recommended_replan_route=str(evidence.get("recommended_replan_route", "")),
                    probe_required=probe,
                    retained_by_planos=_truthy(evidence.get("retained_by_planos")),
                    review_reason_digest=_digest(
                        {
                            "candidate_id": cid,
                            "candidate_digest": cdigest,
                            "advisory_score_digest": evidence.get("advisory_score_digest"),
                            "recommended_replan_route": evidence.get("recommended_replan_route"),
                            "probe_required": probe,
                            "retained_by_planos": evidence.get("retained_by_planos"),
                        }
                    ),
                )
            )

    if declared_review_ids != actual_review_ids:
        blockers.append("review_candidate_ids_silent_substitution_detected")
    if set(declared_review_ids).intersection(excluded_barrier_ids):
        blockers.append("barrier_candidate_in_review_ids")

    status = "PLANOS_DECISION_REVIEW_INTAKE_READY" if not blockers else "PLANOS_DECISION_REVIEW_INTAKE_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_handoff_receipt_digest": str(handoff.get("receipt_digest", "")),
        "review_item_count": len(items),
        "review_candidate_ids": actual_review_ids,
        "probe_candidate_ids": sorted(declared_probe_ids),
        "excluded_barrier_candidate_ids": sorted(set(excluded_barrier_ids)),
        "decision_review_items": [item.to_dict() for item in items],
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return DecisionReviewIntakeReceipt(
        receipt_digest=_digest(partial),
        **partial,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_decision_review_intake_v0_27.py HANDOFF_RECEIPT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_decision_review_intake_receipt(handoff_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
