from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_truth_authority_authorization_request_v0_52"
SOURCE_VERSION = "kuuos_planos_memory_overwrite_closeout_receipt_v0_51"

TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_memory_overwrite_closeout_preserved": True,
    "selected_candidate_bound_to_memory_overwrite_closeout": True,
    "memory_overwrite_preserved": True,
    "memory_overwrite_closeout_preserved": True,
    "cycle_closed_preserved": True,
    "truth_authority_authorization_request_only": True,
    "truth_authority_authorization_requested": True,
    "truth_authority_authorization_granted": False,
    "truth_authority_granted": False,
    "blocker_release_granted": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "closeout_owned_by_plan_os",
    "source_memory_overwrite_receipt_preserved",
    "selected_candidate_bound_to_memory_overwrite_receipt",
    "memory_overwrite_preserved",
    "memory_overwrite_closeout_receipt_only",
    "cycle_closed",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "truth_authority_granted",
    "blocker_release_granted",
)


@dataclass(frozen=True)
class TruthAuthorityAuthorizationRequestRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_memory_overwrite_closeout_receipt_digest: str
    source_memory_overwrite_receipt_digest: str
    truth_authority_authorization_request_digest: str
    request_scope: str = "truth_authority_authorization_request_only"
    memory_overwrite_preserved: bool = True
    memory_overwrite_closeout_preserved: bool = True
    cycle_closed_preserved: bool = True
    truth_authority_authorization_requested: bool = True
    truth_authority_authorization_granted: bool = False
    truth_authority_ready: bool = False
    blocker_release_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TruthAuthorityAuthorizationRequestReceipt:
    version: str
    source_version: str
    status: str
    source_memory_overwrite_closeout_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    truth_authority_authorization_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass", "required"}
    return bool(value)


def _source_closeout_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("memory_overwrite_closeout_receipt"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_memory_overwrite_closeout_version_invalid")
    if receipt.get("status") != "PLANOS_MEMORY_OVERWRITE_CLOSEOUT_RECEIPT_READY":
        blockers.append("source_memory_overwrite_closeout_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_memory_overwrite_closeout_digest_missing")
    record = _source_closeout_record(receipt)
    if not record:
        blockers.append("source_memory_overwrite_closeout_record_missing")
    if record:
        if _truthy(record.get("memory_overwrite_preserved")) is not True:
            blockers.append("source_record_memory_overwrite_preserved_missing")
        if _truthy(record.get("cycle_closed")) is not True:
            blockers.append("source_record_cycle_closed_missing")
        for field in ("truth_authority_ready", "blocker_release_ready"):
            if _truthy(record.get(field)):
                blockers.append(f"source_record_{field}_promoted")
    return blockers


def build_truth_authority_authorization_request(
    *,
    memory_overwrite_closeout: Mapping[str, Any],
) -> TruthAuthorityAuthorizationRequestReceipt:
    source = _m(memory_overwrite_closeout)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_closeout_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_memory_overwrite_closeout_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_memory_overwrite_closeout_mismatch")

    request = None
    if selected_id and selected_digest and not blockers:
        request_obj = TruthAuthorityAuthorizationRequestRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_memory_overwrite_closeout_receipt_digest=str(source.get("receipt_digest", "")),
            source_memory_overwrite_receipt_digest=str(record.get("source_memory_overwrite_receipt_digest", "")),
            truth_authority_authorization_request_digest=sha({
                "source_memory_overwrite_closeout_receipt_digest": source.get("receipt_digest"),
                "source_memory_overwrite_receipt_digest": record.get("source_memory_overwrite_receipt_digest"),
                "selected_candidate_id": selected_id,
                "selected_candidate_digest": selected_digest,
                "scope": "truth_authority_authorization_request_only",
            }),
        )
        request = request_obj.to_dict()

    status = "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_READY" if not blockers else "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_memory_overwrite_closeout_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "truth_authority_authorization_request": request,
        "blockers": blockers,
        "boundary": dict(TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_BOUNDARY),
    }
    return TruthAuthorityAuthorizationRequestReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_truth_authority_authorization_request_v0_52.py MEMORY_OVERWRITE_CLOSEOUT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_truth_authority_authorization_request(memory_overwrite_closeout=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
