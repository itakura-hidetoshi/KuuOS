from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_actos_invocation_receipt_v0_39"
SOURCE_VERSION = "kuuos_planos_activation_authorization_grant_v0_38"

ACTOS_INVOCATION_RECEIPT_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_activation_authorization_grant_preserved": True,
    "selected_candidate_bound_to_activation_grant": True,
    "materialization_execution_preserved": True,
    "activation_authorization_preserved": True,
    "actos_invocation_receipt_only": True,
    "materialization_authorization_granted": True,
    "materialization_executed": True,
    "activation_authorization_granted": True,
    "actos_invoked": True,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class ActOSInvocationReceiptRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_activation_grant_digest: str
    source_activation_request_digest: str
    actos_invocation_digest: str
    receipt_scope: str
    materialization_authorization_granted: bool = True
    materialization_executed: bool = True
    activation_authorization_granted: bool = True
    actos_invoked: bool = True
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ActOSInvocationReceipt:
    version: str
    source_version: str
    status: str
    source_activation_grant_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    actos_invocation_receipt: dict[str, Any] | None
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


def _source_activation_grant_record(grant: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(grant.get("activation_authorization_grant"))


def _source_blockers(grant: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if grant.get("version") != SOURCE_VERSION:
        blockers.append("source_activation_authorization_grant_version_invalid")
    if grant.get("status") != "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_READY":
        blockers.append("source_activation_authorization_grant_not_ready")
    boundary = _m(grant.get("boundary"))
    for required in (
        "grant_owned_by_plan_os",
        "source_activation_authorization_request_preserved",
        "selected_candidate_bound_to_activation_request",
        "materialization_execution_preserved",
        "activation_authorization_grant_only",
        "materialization_authorization_granted",
        "materialization_executed",
        "activation_authorization_granted",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
        "actos_invoked",
        "execution_granted",
        "truth_authority_granted",
        "memory_overwrite_granted",
        "blocker_release_granted",
        "external_commit_granted",
    ):
        if boundary.get(closed) is not False:
            blockers.append(f"source_boundary_{closed}_promoted")
    if not grant.get("receipt_digest"):
        blockers.append("source_activation_grant_digest_missing")
    record = _source_activation_grant_record(grant)
    if not record:
        blockers.append("source_activation_grant_record_missing")
    for required in (
        "materialization_authorization_granted",
        "materialization_executed",
        "activation_authorization_granted",
    ):
        if record and _truthy(record.get(required)) is not True:
            blockers.append(f"source_record_{required}_missing")
    for closed in (
        "actos_invoked",
        "execution_ready",
    ):
        if record and _truthy(record.get(closed)):
            blockers.append(f"source_record_{closed}_promoted")
    return blockers


def build_actos_invocation_receipt(
    *,
    activation_grant: Mapping[str, Any],
) -> ActOSInvocationReceipt:
    source = _m(activation_grant)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_activation_grant_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_activation_grant_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_activation_grant_mismatch")

    invocation_receipt = None
    if selected_id and selected_digest and not blockers:
        receipt_obj = ActOSInvocationReceiptRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_activation_grant_digest=str(source.get("receipt_digest", "")),
            source_activation_request_digest=str(record.get("source_activation_request_digest", "")),
            actos_invocation_digest=_digest(
                {
                    "source_activation_grant_digest": source.get("receipt_digest"),
                    "source_activation_request_digest": record.get("source_activation_request_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "scope": "actos_invocation_receipt_only",
                }
            ),
            receipt_scope="actos_invocation_receipt_only",
            materialization_authorization_granted=True,
            materialization_executed=True,
            activation_authorization_granted=True,
            actos_invoked=True,
            execution_ready=False,
        )
        invocation_receipt = receipt_obj.to_dict()

    status = "PLANOS_ACTOS_INVOCATION_RECEIPT_READY" if not blockers else "PLANOS_ACTOS_INVOCATION_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_activation_grant_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "actos_invocation_receipt": invocation_receipt,
        "blockers": list(blockers),
        "boundary": dict(ACTOS_INVOCATION_RECEIPT_BOUNDARY),
    }
    return ActOSInvocationReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_actos_invocation_receipt_v0_39.py ACTIVATION_GRANT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_actos_invocation_receipt(activation_grant=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
