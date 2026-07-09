from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_selected_candidate_synthesis_request_v0_30"
SOURCE_VERSION = "kuuos_planos_decisionos_selection_receipt_intake_v0_29"

NON_AUTHORITY_BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_selection_receipt_intake_preserved": True,
    "selected_candidate_bound_to_intake": True,
    "synthesis_request_only": True,
    "materialization_granted": False,
    "activation_authorization_granted": False,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class SelectedCandidateSynthesisRequest:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_intake_digest: str
    synthesis_request_digest: str
    synthesis_scope: str
    materialization_granted: bool = False
    activation_authorization_granted: bool = False
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelectedCandidateSynthesisRequestReceipt:
    version: str
    source_version: str
    status: str
    source_selection_receipt_intake_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    synthesis_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass"}
    return bool(value)


def _digest(value: Any) -> str:
    return sha(value)


def _source_blockers(intake: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if intake.get("version") != SOURCE_VERSION:
        blockers.append("source_selection_receipt_intake_version_invalid")
    if intake.get("status") != "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_READY":
        blockers.append("source_selection_receipt_intake_not_ready")
    boundary = _m(intake.get("boundary"))
    for required in (
        "intake_owned_by_plan_os",
        "selection_receipt_owned_by_decision_os",
        "selection_receipt_intake_only",
        "selected_candidate_bound_to_request",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
        "selected_candidate_committed_here",
        "plan_synthesis_granted",
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
        blockers.append("source_selection_receipt_intake_digest_missing")
    record = _m(intake.get("intake_record"))
    if not record:
        blockers.append("source_intake_record_missing")
    for closed in (
        "selected_candidate_committed_here",
        "plan_synthesis_ready",
        "activation_authorization_granted",
        "execution_ready",
    ):
        if _truthy(record.get(closed)):
            blockers.append(f"source_record_{closed}_promoted")
    return blockers


def build_selected_candidate_synthesis_request_receipt(
    *,
    selection_receipt_intake: Mapping[str, Any],
) -> SelectedCandidateSynthesisRequestReceipt:
    intake = _m(selection_receipt_intake)
    blockers = _source_blockers(intake)
    selected_id = str(intake.get("selected_candidate_id", ""))
    selected_digest = str(intake.get("selected_candidate_digest", ""))
    record = _m(intake.get("intake_record"))
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_record_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_record_mismatch")

    request = None
    if selected_id and selected_digest and not blockers:
        request_obj = SelectedCandidateSynthesisRequest(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_intake_digest=str(intake.get("receipt_digest", "")),
            synthesis_request_digest=_digest(
                {
                    "source_intake_digest": intake.get("receipt_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "scope": "selected_candidate_plan_synthesis_request_only",
                }
            ),
            synthesis_scope="selected_candidate_plan_synthesis_request_only",
            materialization_granted=False,
            activation_authorization_granted=False,
            execution_ready=False,
        )
        request = request_obj.to_dict()

    status = "PLANOS_SELECTED_CANDIDATE_SYNTHESIS_REQUEST_READY" if not blockers else "PLANOS_SELECTED_CANDIDATE_SYNTHESIS_REQUEST_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_selection_receipt_intake_digest": str(intake.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "synthesis_request": request,
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return SelectedCandidateSynthesisRequestReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_selected_candidate_synthesis_request_v0_30.py SELECTION_RECEIPT_INTAKE.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_selected_candidate_synthesis_request_receipt(selection_receipt_intake=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
