from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_truth_authority_closeout_receipt_v0_55"
SOURCE_VERSION = "kuuos_planos_truth_authority_receipt_v0_54"

TRUTH_AUTHORITY_CLOSEOUT_BOUNDARY = {
    "closeout_owned_by_plan_os": True,
    "source_truth_authority_receipt_preserved": True,
    "selected_candidate_bound_to_truth_authority_receipt": True,
    "memory_overwrite_preserved": True,
    "memory_overwrite_closeout_preserved": True,
    "cycle_closed_preserved": True,
    "truth_authority_authorization_grant_preserved": True,
    "truth_authority_preserved": True,
    "truth_authority_closeout_receipt_only": True,
    "truth_authority_cycle_closed": True,
    "blocker_release_granted": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "receipt_owned_by_plan_os",
    "source_truth_authority_authorization_grant_preserved",
    "selected_candidate_bound_to_truth_authority_grant",
    "memory_overwrite_preserved",
    "memory_overwrite_closeout_preserved",
    "cycle_closed_preserved",
    "truth_authority_authorization_grant_preserved",
    "truth_authority_receipt_only",
    "truth_authority_authorization_requested",
    "truth_authority_authorization_granted",
    "truth_authority_granted",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "blocker_release_granted",
)


@dataclass(frozen=True)
class TruthAuthorityCloseoutRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_truth_authority_receipt_digest: str
    source_truth_authority_authorization_grant_digest: str
    source_memory_overwrite_closeout_receipt_digest: str
    truth_authority_closeout_digest: str
    closeout_scope: str = "truth_authority_closeout_receipt_only"
    memory_overwrite_preserved: bool = True
    memory_overwrite_closeout_preserved: bool = True
    cycle_closed_preserved: bool = True
    truth_authority_authorization_grant_preserved: bool = True
    truth_authority_preserved: bool = True
    truth_authority_cycle_closed: bool = True
    blocker_release_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TruthAuthorityCloseoutReceipt:
    version: str
    source_version: str
    status: str
    source_truth_authority_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    truth_authority_closeout_receipt: dict[str, Any] | None
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


def _source_record(source: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(source.get("truth_authority_receipt"))


def _source_blockers(source: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if source.get("version") != SOURCE_VERSION:
        blockers.append("source_truth_authority_receipt_version_invalid")
    if source.get("status") != "PLANOS_TRUTH_AUTHORITY_RECEIPT_READY":
        blockers.append("source_truth_authority_receipt_not_ready")
    boundary = _m(source.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not source.get("receipt_digest"):
        blockers.append("source_truth_authority_receipt_digest_missing")
    record = _source_record(source)
    if not record:
        blockers.append("source_truth_authority_receipt_record_missing")
    if record:
        for field in (
            "memory_overwrite_preserved",
            "memory_overwrite_closeout_preserved",
            "cycle_closed_preserved",
            "truth_authority_authorization_granted",
            "truth_authority_granted",
        ):
            if _truthy(record.get(field)) is not True:
                blockers.append(f"source_record_{field}_missing")
        if _truthy(record.get("blocker_release_ready")):
            blockers.append("source_record_blocker_release_ready_promoted")
    return blockers


def build_truth_authority_closeout_receipt(
    *,
    truth_authority_receipt: Mapping[str, Any],
) -> TruthAuthorityCloseoutReceipt:
    source = _m(truth_authority_receipt)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    source_record = _source_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if source_record:
        if str(source_record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_source_receipt_mismatch")
        if str(source_record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_source_receipt_mismatch")

    record = None
    if selected_id and selected_digest and not blockers:
        closeout = TruthAuthorityCloseoutRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_truth_authority_receipt_digest=str(source.get("receipt_digest", "")),
            source_truth_authority_authorization_grant_digest=str(
                source_record.get("source_truth_authority_authorization_grant_digest", "")
            ),
            source_memory_overwrite_closeout_receipt_digest=str(
                source_record.get("source_memory_overwrite_closeout_receipt_digest", "")
            ),
            truth_authority_closeout_digest=sha({
                "source_truth_authority_receipt_digest": source.get("receipt_digest"),
                "source_truth_authority_authorization_grant_digest": source_record.get(
                    "source_truth_authority_authorization_grant_digest"
                ),
                "source_memory_overwrite_closeout_receipt_digest": source_record.get(
                    "source_memory_overwrite_closeout_receipt_digest"
                ),
                "selected_candidate_id": selected_id,
                "selected_candidate_digest": selected_digest,
                "scope": "truth_authority_closeout_receipt_only",
            }),
        )
        record = closeout.to_dict()

    status = (
        "PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_READY"
        if not blockers
        else "PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_BLOCKED"
    )
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_truth_authority_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "truth_authority_closeout_receipt": record,
        "blockers": blockers,
        "boundary": dict(TRUTH_AUTHORITY_CLOSEOUT_BOUNDARY),
    }
    return TruthAuthorityCloseoutReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "usage: kuuos_planos_truth_authority_closeout_receipt_v0_55.py TRUTH_AUTHORITY_RECEIPT.json",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_truth_authority_closeout_receipt(truth_authority_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
