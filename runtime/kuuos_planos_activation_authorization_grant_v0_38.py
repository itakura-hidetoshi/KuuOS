from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_activation_authorization_grant_v0_38"
SOURCE_VERSION = "kuuos_planos_activation_authorization_request_v0_37"

ACTIVATION_AUTHORIZATION_GRANT_BOUNDARY = {
    "grant_owned_by_plan_os": True,
    "source_activation_authorization_request_preserved": True,
    "selected_candidate_bound_to_activation_request": True,
    "materialization_execution_preserved": True,
    "activation_authorization_grant_only": True,
    "materialization_authorization_granted": True,
    "materialization_executed": True,
    "activation_authorization_granted": True,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class ActivationAuthorizationGrantRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_activation_request_digest: str
    source_execution_receipt_digest: str
    activation_authorization_grant_digest: str
    grant_scope: str
    materialization_authorization_granted: bool = True
    materialization_executed: bool = True
    activation_authorization_granted: bool = True
    actos_invoked: bool = False
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ActivationAuthorizationGrantReceipt:
    version: str
    source_version: str
    status: str
    source_activation_request_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    activation_authorization_grant: dict[str, Any] | None
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


def _source_activation_request_record(request: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(request.get("activation_authorization_request"))


def _source_blockers(request: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if request.get("version") != SOURCE_VERSION:
        blockers.append("source_activation_authorization_request_version_invalid")
    if request.get("status") != "PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_READY":
        blockers.append("source_activation_authorization_request_not_ready")
    boundary = _m(request.get("boundary"))
    for required in (
        "request_owned_by_plan_os",
        "source_materialization_execution_receipt_preserved",
        "selected_candidate_bound_to_execution_receipt",
        "materialization_execution_preserved",
        "activation_authorization_request_only",
        "materialization_authorization_granted",
        "materialization_executed",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
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
    if not request.get("receipt_digest"):
        blockers.append("source_activation_request_digest_missing")
    record = _source_activation_request_record(request)
    if not record:
        blockers.append("source_activation_request_record_missing")
    for required in (
        "materialization_authorization_granted",
        "materialization_executed",
    ):
        if record and _truthy(record.get(required)) is not True:
            blockers.append(f"source_record_{required}_missing")
    for closed in (
        "activation_authorization_granted",
        "actos_invoked",
        "execution_ready",
    ):
        if record and _truthy(record.get(closed)):
            blockers.append(f"source_record_{closed}_promoted")
    return blockers


def build_activation_authorization_grant(
    *,
    activation_request: Mapping[str, Any],
) -> ActivationAuthorizationGrantReceipt:
    source = _m(activation_request)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_activation_request_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_activation_request_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_activation_request_mismatch")

    grant = None
    if selected_id and selected_digest and not blockers:
        grant_obj = ActivationAuthorizationGrantRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_activation_request_digest=str(source.get("receipt_digest", "")),
            source_execution_receipt_digest=str(record.get("source_execution_receipt_digest", "")),
            activation_authorization_grant_digest=_digest(
                {
                    "source_activation_request_digest": source.get("receipt_digest"),
                    "source_execution_receipt_digest": record.get("source_execution_receipt_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "scope": "activation_authorization_grant_only",
                }
            ),
            grant_scope="activation_authorization_grant_only",
            materialization_authorization_granted=True,
            materialization_executed=True,
            activation_authorization_granted=True,
            actos_invoked=False,
            execution_ready=False,
        )
        grant = grant_obj.to_dict()

    status = "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_READY" if not blockers else "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_activation_request_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "activation_authorization_grant": grant,
        "blockers": list(blockers),
        "boundary": dict(ACTIVATION_AUTHORIZATION_GRANT_BOUNDARY),
    }
    return ActivationAuthorizationGrantReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_activation_authorization_grant_v0_38.py ACTIVATION_REQUEST.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_activation_authorization_grant(activation_request=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
