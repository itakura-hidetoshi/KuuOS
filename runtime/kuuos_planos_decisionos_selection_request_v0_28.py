from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_decisionos_selection_request_v0_28"
SOURCE_VERSION = "kuuos_planos_decision_review_intake_v0_27"

NON_AUTHORITY_BOUNDARY = {
    "request_owned_by_plan_os": True,
    "selection_owned_by_decision_os": True,
    "selection_request_only": True,
    "review_intake_preserved": True,
    "probe_candidates_marked_not_selected": True,
    "barrier_candidates_excluded": True,
    "candidate_selection_authority_granted": False,
    "selected_candidate_committed": False,
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
class SelectionRequestItem:
    candidate_id: str
    candidate_digest: str
    review_reason_digest: str
    selection_request_digest: str
    probe_required: bool
    retained_by_planos: bool
    request_role: str
    selectable_by_this_layer: bool = False
    selected_candidate_committed: bool = False
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecisionOSSelectionRequestReceipt:
    version: str
    source_version: str
    status: str
    source_review_intake_digest: str
    selection_request_item_count: int
    requested_candidate_ids: list[str]
    probe_candidate_ids: list[str]
    excluded_barrier_candidate_ids: list[str]
    selection_request_items: list[dict[str, Any]]
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


def _boundary_blockers(intake: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if intake.get("version") != SOURCE_VERSION:
        blockers.append("source_review_intake_version_invalid")
    if intake.get("status") != "PLANOS_DECISION_REVIEW_INTAKE_READY":
        blockers.append("source_review_intake_not_ready")
    boundary = _m(intake.get("boundary"))
    for required in (
        "intake_owned_by_plan_os",
        "review_owned_by_decision_os",
        "decision_review_input_only",
        "silent_substitution_forbidden",
        "barrier_candidate_review_blocked_here",
        "probe_candidate_review_flag_required",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
        "candidate_selection_authority_granted",
        "decision_made",
        "decision_receipt_issued",
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
    if not intake.get("receipt_digest"):
        blockers.append("source_review_intake_digest_missing")
    return blockers


def build_decisionos_selection_request_receipt(
    *,
    review_intake_receipt: Mapping[str, Any],
) -> DecisionOSSelectionRequestReceipt:
    intake = _m(review_intake_receipt)
    blockers = _boundary_blockers(intake)
    review_items = _seq(intake.get("decision_review_items"))
    if not review_items:
        blockers.append("decision_review_items_empty")

    declared_review_ids = [str(x) for x in intake.get("review_candidate_ids", []) if isinstance(x, str)]
    probe_ids = set(str(x) for x in intake.get("probe_candidate_ids", []) if isinstance(x, str))
    excluded_barrier_ids = set(str(x) for x in intake.get("excluded_barrier_candidate_ids", []) if isinstance(x, str))

    items: list[SelectionRequestItem] = []
    actual_request_ids: list[str] = []
    seen: set[str] = set()
    for review in review_items:
        cid = str(review.get("candidate_id", ""))
        if not cid:
            blockers.append("candidate_id_missing")
            continue
        if cid in seen:
            blockers.append(f"candidate_id_duplicate:{cid}")
        seen.add(cid)
        if cid in excluded_barrier_ids:
            blockers.append(f"excluded_barrier_candidate_in_request:{cid}")
            continue
        cdigest = str(review.get("candidate_digest", ""))
        rdigest = str(review.get("review_reason_digest", ""))
        if not cdigest:
            blockers.append(f"candidate_digest_missing:{cid}")
        if not rdigest:
            blockers.append(f"review_reason_digest_missing:{cid}")
        if _truthy(review.get("selectable_here")):
            blockers.append(f"source_review_selectable_here_forbidden:{cid}")
        if _truthy(review.get("execution_ready")):
            blockers.append(f"source_review_execution_ready_forbidden:{cid}")
        actual_request_ids.append(cid)
        probe = _truthy(review.get("probe_required")) or cid in probe_ids
        items.append(
            SelectionRequestItem(
                candidate_id=cid,
                candidate_digest=cdigest,
                review_reason_digest=rdigest,
                selection_request_digest=_digest(
                    {
                        "source_review_intake_digest": intake.get("receipt_digest"),
                        "candidate_id": cid,
                        "candidate_digest": cdigest,
                        "review_reason_digest": rdigest,
                        "probe_required": probe,
                    }
                ),
                probe_required=probe,
                retained_by_planos=_truthy(review.get("retained_by_planos")),
                request_role="decisionos_selection_review_requested",
                selectable_by_this_layer=False,
                selected_candidate_committed=False,
                execution_ready=False,
            )
        )

    if declared_review_ids != actual_request_ids:
        blockers.append("selection_request_ids_do_not_match_review_intake")

    status = "PLANOS_DECISIONOS_SELECTION_REQUEST_READY" if not blockers else "PLANOS_DECISIONOS_SELECTION_REQUEST_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_review_intake_digest": str(intake.get("receipt_digest", "")),
        "selection_request_item_count": len(items),
        "requested_candidate_ids": actual_request_ids,
        "probe_candidate_ids": sorted(probe_ids),
        "excluded_barrier_candidate_ids": sorted(excluded_barrier_ids),
        "selection_request_items": [item.to_dict() for item in items],
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return DecisionOSSelectionRequestReceipt(
        receipt_digest=_digest(partial),
        **partial,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_decisionos_selection_request_v0_28.py REVIEW_INTAKE_RECEIPT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_decisionos_selection_request_receipt(review_intake_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
