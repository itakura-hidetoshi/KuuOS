from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_memory_overwrite_receipt_v0_50"
SOURCE_VERSION = "kuuos_planos_memory_overwrite_authorization_grant_v0_49"

MEMORY_OVERWRITE_RECEIPT_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_memory_overwrite_authorization_grant_preserved": True,
    "selected_candidate_bound_to_memory_overwrite_grant": True,
    "external_commit_preserved": True,
    "external_commit_closeout_preserved": True,
    "memory_overwrite_authorization_grant_preserved": True,
    "memory_overwrite_receipt_only": True,
    "memory_overwrite_authorization_requested": True,
    "memory_overwrite_authorization_granted": True,
    "memory_overwrite_granted": True,
    "truth_authority_granted": False,
    "blocker_release_granted": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "grant_owned_by_plan_os",
    "source_memory_overwrite_authorization_request_preserved",
    "selected_candidate_bound_to_memory_overwrite_request",
    "external_commit_preserved",
    "external_commit_closeout_preserved",
    "memory_overwrite_authorization_grant_only",
    "memory_overwrite_authorization_requested",
    "memory_overwrite_authorization_granted",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "memory_overwrite_granted",
    "truth_authority_granted",
    "blocker_release_granted",
)


@dataclass(frozen=True)
class MemoryOverwriteReceiptRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_memory_overwrite_authorization_grant_digest: str
    source_memory_overwrite_authorization_request_digest: str
    memory_overwrite_receipt_digest: str
    receipt_scope: str
    memory_overwrite_authorization_requested: bool = True
    memory_overwrite_authorization_granted: bool = True
    memory_overwrite_granted: bool = True
    truth_authority_ready: bool = False
    blocker_release_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MemoryOverwriteReceipt:
    version: str
    source_version: str
    status: str
    source_memory_overwrite_authorization_grant_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    memory_overwrite_receipt: dict[str, Any] | None
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


def _source_grant_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("memory_overwrite_authorization_grant"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_memory_overwrite_authorization_grant_version_invalid")
    if receipt.get("status") != "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_GRANT_READY":
        blockers.append("source_memory_overwrite_authorization_grant_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_memory_overwrite_authorization_grant_digest_missing")
    record = _source_grant_record(receipt)
    if not record:
        blockers.append("source_memory_overwrite_authorization_grant_record_missing")
    if record:
        if _truthy(record.get("memory_overwrite_authorization_granted")) is not True:
            blockers.append("source_record_memory_overwrite_authorization_granted_missing")
        for field in ("memory_overwrite_ready", "truth_authority_ready", "blocker_release_ready"):
            if _truthy(record.get(field)):
                blockers.append(f"source_record_{field}_promoted")
    return blockers


def build_memory_overwrite_receipt(
    *,
    memory_overwrite_grant: Mapping[str, Any],
) -> MemoryOverwriteReceipt:
    source = _m(memory_overwrite_grant)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_grant_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_memory_overwrite_grant_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_memory_overwrite_grant_mismatch")

    receipt_record = None
    if selected_id and selected_digest and not blockers:
        receipt_obj = MemoryOverwriteReceiptRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_memory_overwrite_authorization_grant_digest=str(source.get("receipt_digest", "")),
            source_memory_overwrite_authorization_request_digest=str(record.get("source_memory_overwrite_authorization_request_digest", "")),
            memory_overwrite_receipt_digest=sha({
                "source_memory_overwrite_authorization_grant_digest": source.get("receipt_digest"),
                "selected_candidate_id": selected_id,
                "selected_candidate_digest": selected_digest,
                "scope": "memory_overwrite_receipt_only",
            }),
            receipt_scope="memory_overwrite_receipt_only",
        )
        receipt_record = receipt_obj.to_dict()

    status = "PLANOS_MEMORY_OVERWRITE_RECEIPT_READY" if not blockers else "PLANOS_MEMORY_OVERWRITE_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_memory_overwrite_authorization_grant_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "memory_overwrite_receipt": receipt_record,
        "blockers": blockers,
        "boundary": dict(MEMORY_OVERWRITE_RECEIPT_BOUNDARY),
    }
    return MemoryOverwriteReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_memory_overwrite_receipt_v0_50.py MEMORY_OVERWRITE_GRANT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_memory_overwrite_receipt(memory_overwrite_grant=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
