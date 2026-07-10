from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_truth_authority_receipt_v0_54"
SOURCE_VERSION = "kuuos_planos_truth_authority_authorization_grant_v0_53"

TRUTH_AUTHORITY_RECEIPT_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_truth_authority_authorization_grant_preserved": True,
    "selected_candidate_bound_to_truth_authority_grant": True,
    "memory_overwrite_preserved": True,
    "memory_overwrite_closeout_preserved": True,
    "cycle_closed_preserved": True,
    "truth_authority_authorization_grant_preserved": True,
    "truth_authority_receipt_only": True,
    "truth_authority_authorization_requested": True,
    "truth_authority_authorization_granted": True,
    "truth_authority_granted": True,
    "blocker_release_granted": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "grant_owned_by_plan_os",
    "source_truth_authority_authorization_request_preserved",
    "selected_candidate_bound_to_truth_authority_request",
    "memory_overwrite_preserved",
    "memory_overwrite_closeout_preserved",
    "cycle_closed_preserved",
    "truth_authority_authorization_grant_only",
    "truth_authority_authorization_requested",
    "truth_authority_authorization_granted",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "truth_authority_granted",
    "blocker_release_granted",
)


@dataclass(frozen=True)
class TruthAuthorityReceiptRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_truth_authority_authorization_grant_digest: str
    source_truth_authority_authorization_request_digest: str
    source_memory_overwrite_closeout_receipt_digest: str
    truth_authority_receipt_digest: str
    receipt_scope: str = "truth_authority_receipt_only"
    memory_overwrite_preserved: bool = True
    memory_overwrite_closeout_preserved: bool = True
    cycle_closed_preserved: bool = True
    truth_authority_authorization_requested: bool = True
    truth_authority_authorization_granted: bool = True
    truth_authority_granted: bool = True
    blocker_release_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TruthAuthorityReceipt:
    version: str
    source_version: str
    status: str
    source_truth_authority_authorization_grant_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    truth_authority_receipt: dict[str, Any] | None
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
    return _m(receipt.get("truth_authority_authorization_grant"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_truth_authority_authorization_grant_version_invalid")
    if receipt.get("status") != "PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_GRANT_READY":
        blockers.append("source_truth_authority_authorization_grant_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_truth_authority_authorization_grant_digest_missing")
    record = _source_grant_record(receipt)
    if not record:
        blockers.append("source_truth_authority_authorization_grant_record_missing")
    if record:
        for field in (
            "memory_overwrite_preserved",
            "memory_overwrite_closeout_preserved",
            "cycle_closed_preserved",
            "truth_authority_authorization_requested",
            "truth_authority_authorization_granted",
        ):
            if _truthy(record.get(field)) is not True:
                blockers.append(f"source_record_{field}_missing")
        if _truthy(record.get("truth_authority_ready")):
            blockers.append("source_record_truth_authority_ready_promoted")
        if _truthy(record.get("blocker_release_ready")):
            blockers.append("source_record_blocker_release_ready_promoted")
    return blockers


def build_truth_authority_receipt(
    *,
    truth_authority_grant: Mapping[str, Any],
) -> TruthAuthorityReceipt:
    source = _m(truth_authority_grant)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_grant_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_truth_authority_grant_mismatch")
        if str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_truth_authority_grant_mismatch")

    receipt_record = None
    if selected_id and selected_digest and not blockers:
        receipt_obj = TruthAuthorityReceiptRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_truth_authority_authorization_grant_digest=str(source.get("receipt_digest", "")),
            source_truth_authority_authorization_request_digest=str(
                record.get("source_truth_authority_authorization_request_digest", "")
            ),
            source_memory_overwrite_closeout_receipt_digest=str(
                record.get("source_memory_overwrite_closeout_receipt_digest", "")
            ),
            truth_authority_receipt_digest=sha({
                "source_truth_authority_authorization_grant_digest": source.get("receipt_digest"),
                "source_truth_authority_authorization_request_digest": record.get(
                    "source_truth_authority_authorization_request_digest"
                ),
                "source_memory_overwrite_closeout_receipt_digest": record.get(
                    "source_memory_overwrite_closeout_receipt_digest"
                ),
                "selected_candidate_id": selected_id,
                "selected_candidate_digest": selected_digest,
                "scope": "truth_authority_receipt_only",
            }),
        )
        receipt_record = receipt_obj.to_dict()

    status = "PLANOS_TRUTH_AUTHORITY_RECEIPT_READY" if not blockers else "PLANOS_TRUTH_AUTHORITY_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_truth_authority_authorization_grant_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "truth_authority_receipt": receipt_record,
        "blockers": blockers,
        "boundary": dict(TRUTH_AUTHORITY_RECEIPT_BOUNDARY),
    }
    return TruthAuthorityReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_truth_authority_receipt_v0_54.py TRUTH_AUTHORITY_GRANT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_truth_authority_receipt(truth_authority_grant=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
