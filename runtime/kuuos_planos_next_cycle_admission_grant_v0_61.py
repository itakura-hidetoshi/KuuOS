from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_next_cycle_admission_grant_v0_61"
SOURCE_VERSION = "kuuos_planos_next_cycle_admission_request_v0_60"

NEXT_CYCLE_ADMISSION_GRANT_BOUNDARY = {
    "grant_owned_by_plan_os": True,
    "source_next_cycle_admission_request_preserved": True,
    "selected_candidate_bound_to_next_cycle_admission_request": True,
    "memory_overwrite_preserved": True,
    "memory_overwrite_closeout_preserved": True,
    "cycle_closed_preserved": True,
    "truth_authority_authorization_grant_preserved": True,
    "truth_authority_preserved": True,
    "truth_authority_cycle_closed_preserved": True,
    "blocker_release_authorization_request_preserved": True,
    "blocker_release_authorization_grant_preserved": True,
    "blocker_release_preserved": True,
    "blocker_release_cycle_closed_preserved": True,
    "next_cycle_admission_request_preserved": True,
    "next_cycle_admission_grant_only": True,
    "next_cycle_admission_requested": True,
    "next_cycle_admission_granted": True,
    "next_cycle_started": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "request_owned_by_plan_os",
    "source_blocker_release_closeout_preserved",
    "selected_candidate_bound_to_blocker_release_closeout",
    "memory_overwrite_preserved",
    "memory_overwrite_closeout_preserved",
    "cycle_closed_preserved",
    "truth_authority_authorization_grant_preserved",
    "truth_authority_preserved",
    "truth_authority_cycle_closed_preserved",
    "blocker_release_authorization_request_preserved",
    "blocker_release_authorization_grant_preserved",
    "blocker_release_preserved",
    "blocker_release_cycle_closed_preserved",
    "next_cycle_admission_request_only",
    "next_cycle_admission_requested",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "next_cycle_admission_granted",
    "next_cycle_started",
)


@dataclass(frozen=True)
class NextCycleAdmissionGrantRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_next_cycle_admission_request_digest: str
    source_blocker_release_closeout_receipt_digest: str
    source_blocker_release_receipt_digest: str
    source_blocker_release_authorization_grant_digest: str
    source_truth_authority_closeout_receipt_digest: str
    source_memory_overwrite_closeout_receipt_digest: str
    next_cycle_admission_grant_digest: str
    grant_scope: str = "next_cycle_admission_grant_only"
    memory_overwrite_preserved: bool = True
    memory_overwrite_closeout_preserved: bool = True
    cycle_closed_preserved: bool = True
    truth_authority_preserved: bool = True
    truth_authority_cycle_closed_preserved: bool = True
    blocker_release_preserved: bool = True
    blocker_release_cycle_closed_preserved: bool = True
    next_cycle_admission_requested: bool = True
    next_cycle_admission_granted: bool = True
    next_cycle_started: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NextCycleAdmissionGrantReceipt:
    version: str
    source_version: str
    status: str
    source_next_cycle_admission_request_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    next_cycle_admission_grant: dict[str, Any] | None
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


def _source_request_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("next_cycle_admission_request"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_next_cycle_admission_request_version_invalid")
    if receipt.get("status") != "PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_READY":
        blockers.append("source_next_cycle_admission_request_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_next_cycle_admission_request_digest_missing")
    record = _source_request_record(receipt)
    if not record:
        blockers.append("source_next_cycle_admission_request_record_missing")
    if record:
        for field in (
            "memory_overwrite_preserved",
            "memory_overwrite_closeout_preserved",
            "cycle_closed_preserved",
            "truth_authority_preserved",
            "truth_authority_cycle_closed_preserved",
            "blocker_release_preserved",
            "blocker_release_cycle_closed_preserved",
            "next_cycle_admission_requested",
        ):
            if _truthy(record.get(field)) is not True:
                blockers.append(f"source_record_{field}_missing")
        if _truthy(record.get("next_cycle_admission_granted")):
            blockers.append("source_record_next_cycle_admission_granted_promoted")
        if _truthy(record.get("next_cycle_started")):
            blockers.append("source_record_next_cycle_started_promoted")
    return blockers


def build_next_cycle_admission_grant(
    *,
    next_cycle_admission_request: Mapping[str, Any],
) -> NextCycleAdmissionGrantReceipt:
    source = _m(next_cycle_admission_request)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_request_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_next_cycle_admission_request_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_next_cycle_admission_request_mismatch")

    grant = None
    if selected_id and selected_digest and not blockers:
        grant_obj = NextCycleAdmissionGrantRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_next_cycle_admission_request_digest=str(source.get("receipt_digest", "")),
            source_blocker_release_closeout_receipt_digest=str(
                record.get("source_blocker_release_closeout_receipt_digest", "")
            ),
            source_blocker_release_receipt_digest=str(record.get("source_blocker_release_receipt_digest", "")),
            source_blocker_release_authorization_grant_digest=str(
                record.get("source_blocker_release_authorization_grant_digest", "")
            ),
            source_truth_authority_closeout_receipt_digest=str(
                record.get("source_truth_authority_closeout_receipt_digest", "")
            ),
            source_memory_overwrite_closeout_receipt_digest=str(
                record.get("source_memory_overwrite_closeout_receipt_digest", "")
            ),
            next_cycle_admission_grant_digest=sha({
                "source_next_cycle_admission_request_digest": source.get("receipt_digest"),
                "source_blocker_release_closeout_receipt_digest": record.get(
                    "source_blocker_release_closeout_receipt_digest"
                ),
                "source_blocker_release_receipt_digest": record.get("source_blocker_release_receipt_digest"),
                "source_blocker_release_authorization_grant_digest": record.get(
                    "source_blocker_release_authorization_grant_digest"
                ),
                "source_truth_authority_closeout_receipt_digest": record.get(
                    "source_truth_authority_closeout_receipt_digest"
                ),
                "source_memory_overwrite_closeout_receipt_digest": record.get(
                    "source_memory_overwrite_closeout_receipt_digest"
                ),
                "selected_candidate_id": selected_id,
                "selected_candidate_digest": selected_digest,
                "scope": "next_cycle_admission_grant_only",
            }),
        )
        grant = grant_obj.to_dict()

    status = (
        "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_READY"
        if not blockers
        else "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_BLOCKED"
    )
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_next_cycle_admission_request_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "next_cycle_admission_grant": grant,
        "blockers": blockers,
        "boundary": dict(NEXT_CYCLE_ADMISSION_GRANT_BOUNDARY),
    }
    return NextCycleAdmissionGrantReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "usage: kuuos_planos_next_cycle_admission_grant_v0_61.py NEXT_CYCLE_ADMISSION_REQUEST.json",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_next_cycle_admission_grant(next_cycle_admission_request=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
