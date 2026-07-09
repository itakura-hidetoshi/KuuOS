from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_decisionos_selection_receipt_intake_v0_29"
SOURCE_VERSION = "kuuos_planos_decisionos_selection_request_v0_28"
DECISIONOS_SELECTION_VERSION = "kuuos_decisionos_admissible_candidate_selection_v0_4"

NON_AUTHORITY_BOUNDARY = {
    "intake_owned_by_plan_os": True,
    "selection_receipt_owned_by_decision_os": True,
    "selection_receipt_intake_only": True,
    "selected_candidate_bound_to_request": True,
    "selected_candidate_committed_here": False,
    "plan_synthesis_granted": False,
    "activation_authorization_granted": False,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class SelectionReceiptIntakeRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    decisionos_receipt_digest: str
    source_request_digest: str
    admissible_request_match_digest: str
    selected_candidate_committed_here: bool = False
    plan_synthesis_ready: bool = False
    activation_authorization_granted: bool = False
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecisionOSSelectionReceiptIntakeReceipt:
    version: str
    source_version: str
    decisionos_selection_version: str
    status: str
    source_selection_request_digest: str
    decisionos_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    intake_record: dict[str, Any] | None
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


def _request_blockers(selection_request: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if selection_request.get("version") != SOURCE_VERSION:
        blockers.append("source_selection_request_version_invalid")
    if selection_request.get("status") != "PLANOS_DECISIONOS_SELECTION_REQUEST_READY":
        blockers.append("source_selection_request_not_ready")
    boundary = _m(selection_request.get("boundary"))
    for required in (
        "request_owned_by_plan_os",
        "selection_owned_by_decision_os",
        "selection_request_only",
        "review_intake_preserved",
        "probe_candidates_marked_not_selected",
        "barrier_candidates_excluded",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
        "candidate_selection_authority_granted",
        "selected_candidate_committed",
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
    if not selection_request.get("receipt_digest"):
        blockers.append("source_selection_request_digest_missing")
    return blockers


def _decisionos_blockers(decisionos_selection_receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    version = decisionos_selection_receipt.get("version")
    if version not in (DECISIONOS_SELECTION_VERSION, None, ""):
        blockers.append("decisionos_selection_version_unexpected")
    if decisionos_selection_receipt.get("status") not in ("DECISIONOS_ADMISSIBLE_CANDIDATE_SELECTED", "DECISIONOS_SELECTION_READY", "ready", "READY"):
        blockers.append("decisionos_selection_not_ready")
    for closed in (
        "activation_authorization_granted",
        "actos_invoked",
        "execution_granted",
        "truth_authority_granted",
        "memory_overwrite_granted",
        "blocker_release_granted",
        "external_commit_granted",
    ):
        if _truthy(decisionos_selection_receipt.get(closed)):
            blockers.append(f"decisionos_receipt_{closed}_promoted")
    if not decisionos_selection_receipt.get("receipt_digest"):
        blockers.append("decisionos_receipt_digest_missing")
    return blockers


def build_decisionos_selection_receipt_intake(
    *,
    selection_request_receipt: Mapping[str, Any],
    decisionos_selection_receipt: Mapping[str, Any],
) -> DecisionOSSelectionReceiptIntakeReceipt:
    request = _m(selection_request_receipt)
    decision = _m(decisionos_selection_receipt)
    blockers = _request_blockers(request) + _decisionos_blockers(decision)

    requested_ids = [str(x) for x in request.get("requested_candidate_ids", []) if isinstance(x, str)]
    items = _seq(request.get("selection_request_items"))
    item_by_id = {str(item.get("candidate_id", "")): item for item in items if item.get("candidate_id")}

    selected_id = str(decision.get("selected_candidate_id", ""))
    selected_digest = str(decision.get("selected_candidate_digest", ""))
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if selected_id and selected_id not in requested_ids:
        blockers.append("selected_candidate_not_in_requested_ids")
    selected_item = _m(item_by_id.get(selected_id))
    if selected_id and not selected_item:
        blockers.append("selected_candidate_request_item_missing")
    if selected_item:
        request_digest = str(selected_item.get("candidate_digest", ""))
        if selected_digest and request_digest and selected_digest != request_digest:
            blockers.append("selected_candidate_digest_mismatch")
        if _truthy(selected_item.get("selectable_by_this_layer")):
            blockers.append("source_item_selectable_by_planos_forbidden")
        if _truthy(selected_item.get("selected_candidate_committed")):
            blockers.append("source_item_selected_commit_forbidden")
        if _truthy(selected_item.get("execution_ready")):
            blockers.append("source_item_execution_ready_forbidden")
        if not selected_digest:
            selected_digest = request_digest

    record = None
    if selected_id and selected_digest and not blockers:
        record_obj = SelectionReceiptIntakeRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            decisionos_receipt_digest=str(decision.get("receipt_digest", "")),
            source_request_digest=str(request.get("receipt_digest", "")),
            admissible_request_match_digest=_digest(
                {
                    "source_request_digest": request.get("receipt_digest"),
                    "decisionos_receipt_digest": decision.get("receipt_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                }
            ),
            selected_candidate_committed_here=False,
            plan_synthesis_ready=False,
            activation_authorization_granted=False,
            execution_ready=False,
        )
        record = record_obj.to_dict()

    status = "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_READY" if not blockers else "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "decisionos_selection_version": DECISIONOS_SELECTION_VERSION,
        "status": status,
        "source_selection_request_digest": str(request.get("receipt_digest", "")),
        "decisionos_receipt_digest": str(decision.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "intake_record": record,
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return DecisionOSSelectionReceiptIntakeReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: kuuos_planos_decisionos_selection_receipt_intake_v0_29.py SELECTION_REQUEST.json DECISIONOS_SELECTION.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        request = json.load(handle)
    with open(argv[2], "r", encoding="utf-8") as handle:
        decision = json.load(handle)
    receipt = build_decisionos_selection_receipt_intake(selection_request_receipt=request, decisionos_selection_receipt=decision)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
