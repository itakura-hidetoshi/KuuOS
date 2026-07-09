from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_weighted_decision_evidence_handoff_v0_26"
SOURCE_VERSION = "kuuos_planos_path_integral_candidate_weighting_v0_25"

NON_AUTHORITY_BOUNDARY = {
    "handoff_owned_by_plan_os": True,
    "selection_owned_by_decision_os": True,
    "candidate_weights_advisory_only": True,
    "decision_evidence_only": True,
    "selected_candidate_committed": False,
    "decision_made": False,
    "activation_authorization_granted": False,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class DecisionEvidenceItem:
    candidate_id: str
    candidate_digest: str
    advisory_score_digest: str
    recommended_replan_route: str
    probe_required: bool
    barrier_required: bool
    retained_by_planos: bool
    eligible_for_decisionos_review: bool
    execution_ready: bool = False
    selection_authority_granted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WeightedDecisionEvidenceHandoffReceipt:
    version: str
    source_version: str
    status: str
    source_weighting_receipt_digest: str
    evidence_item_count: int
    review_candidate_ids: list[str]
    probe_candidate_ids: list[str]
    barrier_candidate_ids: list[str]
    blocked_candidate_ids: list[str]
    decision_evidence_items: list[dict[str, Any]]
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


def _boundary_blockers(weighting: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if weighting.get("version") != SOURCE_VERSION:
        blockers.append("source_weighting_version_invalid")
    if weighting.get("status") != "PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_READY":
        blockers.append("source_weighting_not_ready")
    boundary = _m(weighting.get("boundary"))
    for field in (
        "candidate_weighting_advisory_only",
        "selection_authority_granted",
        "activation_authorization_granted",
        "actos_invoked",
        "execution_granted",
        "truth_authority_granted",
        "memory_overwrite_granted",
        "blocker_release_granted",
        "external_commit_granted",
    ):
        if field == "candidate_weighting_advisory_only":
            if boundary.get(field) is not True:
                blockers.append(f"source_boundary_{field}_missing")
        elif boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not weighting.get("receipt_digest"):
        blockers.append("source_weighting_receipt_digest_missing")
    return blockers


def build_weighted_decision_evidence_handoff_receipt(
    *,
    weighting_receipt: Mapping[str, Any],
) -> WeightedDecisionEvidenceHandoffReceipt:
    weighting = _m(weighting_receipt)
    blockers = _boundary_blockers(weighting)
    receipts = _seq(weighting.get("candidate_weight_receipts"))
    if not receipts:
        blockers.append("candidate_weight_receipts_empty")

    retained = set(str(x) for x in weighting.get("retained_candidate_ids", []) if isinstance(x, str))
    probe_ids = set(str(x) for x in weighting.get("probe_candidate_ids", []) if isinstance(x, str))
    barrier_ids = set(str(x) for x in weighting.get("barrier_candidate_ids", []) if isinstance(x, str))

    items: list[DecisionEvidenceItem] = []
    blocked_candidate_ids: list[str] = []
    for receipt in receipts:
        cid = str(receipt.get("candidate_id", ""))
        cdigest = str(receipt.get("candidate_digest", ""))
        route = str(receipt.get("recommended_replan_route", ""))
        if not cid:
            blockers.append("candidate_id_missing")
            continue
        if not cdigest:
            blockers.append(f"candidate_digest_missing:{cid}")
            blocked_candidate_ids.append(cid)
        probe_required = _truthy(receipt.get("probe_required")) or cid in probe_ids
        barrier_required = _truthy(receipt.get("barrier_required")) or cid in barrier_ids
        execution_ready = _truthy(receipt.get("execution_ready"))
        selection_authority = _truthy(receipt.get("selection_authority_granted"))
        if execution_ready:
            blockers.append(f"candidate_execution_ready_forbidden:{cid}")
            blocked_candidate_ids.append(cid)
        if selection_authority:
            blockers.append(f"candidate_selection_authority_forbidden:{cid}")
            blocked_candidate_ids.append(cid)
        eligible = bool(cdigest) and not barrier_required and not execution_ready and not selection_authority
        if barrier_required:
            blocked_candidate_ids.append(cid)
        items.append(
            DecisionEvidenceItem(
                candidate_id=cid,
                candidate_digest=cdigest,
                advisory_score_digest=_digest(
                    {
                        "candidate_id": cid,
                        "advisory_score": receipt.get("advisory_score"),
                        "reentry_mode": receipt.get("reentry_mode"),
                        "path_weight_delta": receipt.get("path_weight_delta"),
                        "process_tensor_bonus": receipt.get("process_tensor_bonus"),
                        "blocker_penalty": receipt.get("blocker_penalty"),
                    }
                ),
                recommended_replan_route=route,
                probe_required=probe_required,
                barrier_required=barrier_required,
                retained_by_planos=cid in retained,
                eligible_for_decisionos_review=eligible,
                execution_ready=False,
                selection_authority_granted=False,
            )
        )

    review_ids = [item.candidate_id for item in items if item.eligible_for_decisionos_review]
    status = "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_READY" if not blockers else "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_weighting_receipt_digest": str(weighting.get("receipt_digest", "")),
        "evidence_item_count": len(items),
        "review_candidate_ids": review_ids,
        "probe_candidate_ids": sorted(probe_ids),
        "barrier_candidate_ids": sorted(barrier_ids),
        "blocked_candidate_ids": sorted(set(blocked_candidate_ids)),
        "decision_evidence_items": [item.to_dict() for item in items],
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return WeightedDecisionEvidenceHandoffReceipt(
        receipt_digest=_digest(partial),
        **partial,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_weighted_decision_evidence_handoff_v0_26.py WEIGHTING_RECEIPT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_weighted_decision_evidence_handoff_receipt(weighting_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
