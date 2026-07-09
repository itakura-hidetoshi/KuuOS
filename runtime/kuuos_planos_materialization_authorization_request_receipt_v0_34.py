from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_materialization_authorization_request_receipt_v0_34"
SOURCE_VERSION = "kuuos_planos_materialization_authorization_request_v0_33"

NON_AUTHORITY_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_materialization_authorization_request_preserved": True,
    "selected_candidate_bound_to_authorization_request": True,
    "materialization_authorization_request_receipt_only": True,
    "materialization_authorization_granted": False,
    "materialization_executed": False,
    "activation_authorization_granted": False,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class MaterializationAuthorizationRequestReceiptRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_request_digest: str
    source_authorization_request_digest: str
    request_receipt_digest: str
    receipt_scope: str
    materialization_authorization_granted: bool = False
    materialization_executed: bool = False
    activation_authorization_granted: bool = False
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MaterializationAuthorizationRequestReceipt:
    version: str
    source_version: str
    status: str
    source_request_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    materialization_authorization_request_receipt: dict[str, Any] | None
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


def _source_request_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("materialization_authorization_request"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_materialization_authorization_request_version_invalid")
    if receipt.get("status") != "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_READY":
        blockers.append("source_materialization_authorization_request_not_ready")
    boundary = _m(receipt.get("boundary"))
    for required in (
        "request_owned_by_plan_os",
        "source_materialization_preflight_preserved",
        "selected_candidate_bound_to_preflight",
        "materialization_authorization_request_only",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
        "materialization_authorization_granted",
        "materialization_executed",
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
    if not receipt.get("receipt_digest"):
        blockers.append("source_request_digest_missing")
    record = _source_request_record(receipt)
    if not record:
        blockers.append("source_authorization_request_record_missing")
    for closed in (
        "materialization_authorization_granted",
        "materialization_executed",
        "activation_authorization_granted",
        "execution_ready",
    ):
        if _truthy(record.get(closed)):
            blockers.append(f"source_record_{closed}_promoted")
    return blockers


def build_materialization_authorization_request_receipt(
    *,
    authorization_request_receipt: Mapping[str, Any],
) -> MaterializationAuthorizationRequestReceipt:
    source = _m(authorization_request_receipt)
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
            blockers.append("selected_candidate_id_authorization_request_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_authorization_request_mismatch")

    request_receipt = None
    if selected_id and selected_digest and not blockers:
        request_receipt_obj = MaterializationAuthorizationRequestReceiptRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_request_digest=str(source.get("receipt_digest", "")),
            source_authorization_request_digest=str(record.get("authorization_request_digest", "")),
            request_receipt_digest=_digest(
                {
                    "source_request_digest": source.get("receipt_digest"),
                    "source_authorization_request_digest": record.get("authorization_request_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "scope": "materialization_authorization_request_receipt_only",
                }
            ),
            receipt_scope="materialization_authorization_request_receipt_only",
            materialization_authorization_granted=False,
            materialization_executed=False,
            activation_authorization_granted=False,
            execution_ready=False,
        )
        request_receipt = request_receipt_obj.to_dict()

    status = "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_READY" if not blockers else "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_request_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "materialization_authorization_request_receipt": request_receipt,
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return MaterializationAuthorizationRequestReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_materialization_authorization_request_receipt_v0_34.py AUTHORIZATION_REQUEST.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_materialization_authorization_request_receipt(authorization_request_receipt=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
