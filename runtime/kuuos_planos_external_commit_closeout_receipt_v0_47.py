from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_external_commit_closeout_receipt_v0_47"
SOURCE_VERSION = "kuuos_planos_external_commit_receipt_v0_46"

EXTERNAL_COMMIT_CLOSEOUT_BOUNDARY = {
    "closeout_owned_by_plan_os": True,
    "source_external_commit_receipt_preserved": True,
    "selected_candidate_bound_to_external_commit_receipt": True,
    "external_commit_preserved": True,
    "external_commit_closeout_receipt_only": True,
    "cycle_closed": True,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "receipt_owned_by_plan_os",
    "source_external_commit_authorization_grant_preserved",
    "selected_candidate_bound_to_external_commit_grant",
    "materialization_execution_preserved",
    "execution_authorization_grant_preserved",
    "execution_receipt_preserved",
    "external_commit_authorization_request_preserved",
    "external_commit_authorization_grant_preserved",
    "external_commit_receipt_only",
    "external_commit_authorization_requested",
    "external_commit_authorization_granted",
    "external_commit_granted",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "truth_authority_granted",
    "memory_overwrite_granted",
    "blocker_release_granted",
)


@dataclass(frozen=True)
class ExternalCommitCloseoutRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_external_commit_receipt_digest: str
    external_commit_closeout_digest: str
    closeout_scope: str = "external_commit_closeout_receipt_only"
    external_commit_preserved: bool = True
    cycle_closed: bool = True
    memory_overwrite_ready: bool = False
    truth_authority_ready: bool = False
    blocker_release_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExternalCommitCloseoutReceipt:
    version: str
    source_version: str
    status: str
    source_external_commit_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    external_commit_closeout_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _source_blockers(source: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if source.get("version") != SOURCE_VERSION:
        blockers.append("source_external_commit_receipt_version_invalid")
    if source.get("status") != "PLANOS_EXTERNAL_COMMIT_RECEIPT_READY":
        blockers.append("source_external_commit_receipt_not_ready")
    boundary = _m(source.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not source.get("receipt_digest"):
        blockers.append("source_external_commit_receipt_digest_missing")
    record = _m(source.get("external_commit_receipt"))
    if not record:
        blockers.append("source_external_commit_receipt_record_missing")
    elif record.get("external_commit_granted") is not True:
        blockers.append("source_external_commit_not_recorded")
    return blockers


def build_external_commit_closeout_receipt(
    *, external_commit_receipt: Mapping[str, Any]
) -> ExternalCommitCloseoutReceipt:
    source = _m(external_commit_receipt)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    source_record = _m(source.get("external_commit_receipt"))
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
        closeout = ExternalCommitCloseoutRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_external_commit_receipt_digest=str(source.get("receipt_digest", "")),
            external_commit_closeout_digest=sha({
                "source_external_commit_receipt_digest": source.get("receipt_digest"),
                "selected_candidate_id": selected_id,
                "selected_candidate_digest": selected_digest,
                "scope": "external_commit_closeout_receipt_only",
            }),
        )
        record = closeout.to_dict()

    status = "PLANOS_EXTERNAL_COMMIT_CLOSEOUT_RECEIPT_READY" if not blockers else "PLANOS_EXTERNAL_COMMIT_CLOSEOUT_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_external_commit_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "external_commit_closeout_receipt": record,
        "blockers": blockers,
        "boundary": dict(EXTERNAL_COMMIT_CLOSEOUT_BOUNDARY),
    }
    return ExternalCommitCloseoutReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_external_commit_closeout_receipt_v0_47.py EXTERNAL_COMMIT_RECEIPT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_external_commit_closeout_receipt(external_commit_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
