from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_execution_authorization_grant_v0_79"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_execution_request_v0_78"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_AUTHORIZATION_GRANT_READY"

BOUNDARY = {
    "grant_owned_by_plan_os": True,
    "source_subsequent_cycle_execution_request_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "admission_evidence_preserved": True,
    "start_evidence_preserved": True,
    "execution_scope_preserved": True,
    "execution_constraints_digest_preserved": True,
    "subsequent_cycle_execution_requested": True,
    "subsequent_cycle_execution_authority_granted": True,
    "subsequent_cycle_execution_started": False,
}

@dataclass(frozen=True)
class ExecutionAuthorizationGrantRecord:
    source_execution_request_receipt_digest: str
    source_execution_request_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    start_scope: str
    start_constraints_digest: str
    execution_scope: str
    execution_constraints_digest: str
    grant_rationale_digest: str
    execution_authorization_grant_digest: str
    subsequent_cycle_execution_requested: bool = True
    subsequent_cycle_execution_authority_granted: bool = True
    subsequent_cycle_execution_started: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class ExecutionAuthorizationGrantReceipt:
    version: str
    source_version: str
    status: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    start_scope: str
    start_constraints_digest: str
    execution_scope: str
    execution_constraints_digest: str
    subsequent_cycle_execution_authorization_grant: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}

def build_subsequent_cycle_execution_authorization_grant(
    source_execution_request: Mapping[str, Any],
    *,
    grant_rationale: Mapping[str, Any] | None = None,
) -> ExecutionAuthorizationGrantReceipt:
    blockers: list[str] = []
    if source_execution_request.get("version") != SOURCE_VERSION:
        blockers.append("source_execution_request_version_invalid")
    if source_execution_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_REQUEST_READY":
        blockers.append("source_execution_request_not_ready")
    if not source_execution_request.get("receipt_digest"):
        blockers.append("source_execution_request_receipt_digest_missing")

    boundary = _m(source_execution_request.get("boundary"))
    if boundary.get("subsequent_cycle_execution_requested") is not True:
        blockers.append("source_boundary_execution_requested_missing")
    if boundary.get("subsequent_cycle_execution_authority_granted") is not False:
        blockers.append("source_boundary_execution_authority_promoted")
    if boundary.get("subsequent_cycle_execution_started") is not False:
        blockers.append("source_boundary_execution_started_promoted")

    record = _m(source_execution_request.get("subsequent_cycle_execution_request"))
    if not record or not record.get("execution_request_digest"):
        blockers.append("source_execution_request_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest", "candidate_set_digest",
        "evaluation_set_digest", "review_set_digest", "admission_scope",
        "admission_constraints_digest", "start_scope", "start_constraints_digest",
        "execution_scope", "execution_constraints_digest",
    )
    for field in fields:
        if not source_execution_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_execution_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    rationale = dict(grant_rationale or {
        "execution_request_preserved": True,
        "execution_scope_respected": True,
        "execution_constraints_respected": True,
        "execution_start_remains_separate": True,
    })
    if not rationale:
        blockers.append("grant_rationale_missing")

    grant_record = None
    status = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_AUTHORIZATION_GRANT_BLOCKED"
    if not blockers:
        payload = {
            "source_execution_request_receipt_digest": str(source_execution_request["receipt_digest"]),
            "source_execution_request_digest": str(record["execution_request_digest"]),
            **{field: str(source_execution_request[field]) for field in fields},
            "grant_rationale_digest": sha(rationale),
        }
        grant_record = ExecutionAuthorizationGrantRecord(
            **payload,
            execution_authorization_grant_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source_execution_request.get(field, "")) for field in fields},
        "subsequent_cycle_execution_authorization_grant": grant_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return ExecutionAuthorizationGrantReceipt(**outer, receipt_digest=sha(outer))
