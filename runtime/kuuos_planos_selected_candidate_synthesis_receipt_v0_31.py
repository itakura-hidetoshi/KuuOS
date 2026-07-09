from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_selected_candidate_synthesis_receipt_v0_31"
SOURCE_VERSION = "kuuos_planos_selected_candidate_synthesis_request_v0_30"

NON_AUTHORITY_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_synthesis_request_preserved": True,
    "selected_candidate_bound_to_request": True,
    "synthesis_receipt_only": True,
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
class SelectedCandidateSynthesisReceiptRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_request_digest: str
    synthesis_request_digest: str
    synthesis_receipt_digest: str
    synthesis_receipt_scope: str
    materialization_granted: bool = False
    activation_authorization_granted: bool = False
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelectedCandidateSynthesisReceipt:
    version: str
    source_version: str
    status: str
    source_synthesis_request_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    synthesis_receipt_record: dict[str, Any] | None
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


def _source_blockers(request_receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if request_receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_synthesis_request_version_invalid")
    if request_receipt.get("status") != "PLANOS_SELECTED_CANDIDATE_SYNTHESIS_REQUEST_READY":
        blockers.append("source_synthesis_request_not_ready")
    boundary = _m(request_receipt.get("boundary"))
    for required in (
        "request_owned_by_plan_os",
        "source_selection_receipt_intake_preserved",
        "selected_candidate_bound_to_intake",
        "synthesis_request_only",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
        "materialization_granted",
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
    if not request_receipt.get("receipt_digest"):
        blockers.append("source_synthesis_request_receipt_digest_missing")
    request = _m(request_receipt.get("synthesis_request"))
    if not request:
        blockers.append("source_synthesis_request_missing")
    for closed in (
        "materialization_granted",
        "activation_authorization_granted",
        "execution_ready",
    ):
        if _truthy(request.get(closed)):
            blockers.append(f"source_request_{closed}_promoted")
    return blockers


def build_selected_candidate_synthesis_receipt(
    *,
    synthesis_request_receipt: Mapping[str, Any],
) -> SelectedCandidateSynthesisReceipt:
    source = _m(synthesis_request_receipt)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    request = _m(source.get("synthesis_request"))
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if request:
        if selected_id and str(request.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_request_mismatch")
        if selected_digest and str(request.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_request_mismatch")

    record = None
    if selected_id and selected_digest and request and not blockers:
        record_obj = SelectedCandidateSynthesisReceiptRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_request_digest=str(source.get("receipt_digest", "")),
            synthesis_request_digest=str(request.get("synthesis_request_digest", "")),
            synthesis_receipt_digest=_digest(
                {
                    "source_request_digest": source.get("receipt_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "scope": "selected_candidate_plan_synthesis_receipt_only",
                }
            ),
            synthesis_receipt_scope="selected_candidate_plan_synthesis_receipt_only",
            materialization_granted=False,
            activation_authorization_granted=False,
            execution_ready=False,
        )
        record = record_obj.to_dict()

    status = "PLANOS_SELECTED_CANDIDATE_SYNTHESIS_RECEIPT_READY" if not blockers else "PLANOS_SELECTED_CANDIDATE_SYNTHESIS_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_synthesis_request_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "synthesis_receipt_record": record,
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return SelectedCandidateSynthesisReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_selected_candidate_synthesis_receipt_v0_31.py SYNTHESIS_REQUEST_RECEIPT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_selected_candidate_synthesis_receipt(synthesis_request_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
