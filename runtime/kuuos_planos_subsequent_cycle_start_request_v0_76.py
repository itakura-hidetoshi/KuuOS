from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_start_request_v0_76"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_admission_grant_v0_75"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_START_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_subsequent_cycle_admission_grant_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "admission_scope_preserved": True,
    "admission_constraints_digest_preserved": True,
    "subsequent_cycle_start_request_only": True,
    "subsequent_cycle_admission_requested": True,
    "subsequent_cycle_admission_granted": True,
    "subsequent_cycle_start_requested": True,
    "subsequent_cycle_started": False,
}


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


@dataclass(frozen=True)
class SubsequentCycleStartRequestRecord:
    source_admission_grant_receipt_digest: str
    source_admission_grant_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    start_scope: str
    start_constraints_digest: str
    start_request_digest: str
    subsequent_cycle_admission_requested: bool = True
    subsequent_cycle_admission_granted: bool = True
    subsequent_cycle_start_requested: bool = True
    subsequent_cycle_started: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleStartRequestReceipt:
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
    subsequent_cycle_start_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_subsequent_cycle_start_request(
    source_admission_grant: Mapping[str, Any],
    *,
    start_scope: str = "selected_candidate_subsequent_cycle_start_only",
    start_constraints: Mapping[str, Any] | None = None,
) -> SubsequentCycleStartRequestReceipt:
    blockers: list[str] = []
    if source_admission_grant.get("version") != SOURCE_VERSION:
        blockers.append("source_admission_grant_version_invalid")
    if source_admission_grant.get("status") != "PLANOS_SUBSEQUENT_CYCLE_ADMISSION_GRANT_READY":
        blockers.append("source_admission_grant_not_ready")
    if not source_admission_grant.get("receipt_digest"):
        blockers.append("source_admission_grant_receipt_digest_missing")

    boundary = _m(source_admission_grant.get("boundary"))
    for field in ("subsequent_cycle_admission_requested", "subsequent_cycle_admission_granted"):
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    if boundary.get("subsequent_cycle_started") is not False:
        blockers.append("source_boundary_subsequent_cycle_started_promoted")

    record = _m(source_admission_grant.get("subsequent_cycle_admission_grant"))
    if not record:
        blockers.append("source_admission_grant_record_missing")
    elif not record.get("admission_grant_digest"):
        blockers.append("source_admission_grant_digest_missing")

    preserved_fields = (
        "selected_candidate_id",
        "selected_candidate_digest",
        "candidate_set_digest",
        "evaluation_set_digest",
        "review_set_digest",
        "admission_scope",
        "admission_constraints_digest",
    )
    for field in preserved_fields:
        if not source_admission_grant.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_admission_grant.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    constraints = dict(start_constraints or {
        "admission_grant_must_be_preserved": True,
        "selected_candidate_identity_must_be_preserved": True,
        "start_receipt_required_before_cycle_start": True,
        "candidate_substitution_forbidden": True,
        "cycle_start_forbidden_at_request_layer": True,
    })
    if not start_scope:
        blockers.append("start_scope_missing")
    if not constraints:
        blockers.append("start_constraints_missing")
    constraints_digest = sha(constraints) if constraints else ""

    request_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_START_REQUEST_BLOCKED"
    if not blockers:
        payload = {
            "source_admission_grant_receipt_digest": str(source_admission_grant["receipt_digest"]),
            "source_admission_grant_digest": str(record["admission_grant_digest"]),
            "selected_candidate_id": str(source_admission_grant["selected_candidate_id"]),
            "selected_candidate_digest": str(source_admission_grant["selected_candidate_digest"]),
            "candidate_set_digest": str(source_admission_grant["candidate_set_digest"]),
            "evaluation_set_digest": str(source_admission_grant["evaluation_set_digest"]),
            "review_set_digest": str(source_admission_grant["review_set_digest"]),
            "admission_scope": str(source_admission_grant["admission_scope"]),
            "admission_constraints_digest": str(source_admission_grant["admission_constraints_digest"]),
            "start_scope": start_scope,
            "start_constraints_digest": constraints_digest,
        }
        request_record = SubsequentCycleStartRequestRecord(
            **payload,
            start_request_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": str(source_admission_grant.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source_admission_grant.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source_admission_grant.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_admission_grant.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_admission_grant.get("review_set_digest", "")),
        "admission_scope": str(source_admission_grant.get("admission_scope", "")),
        "admission_constraints_digest": str(source_admission_grant.get("admission_constraints_digest", "")),
        "start_scope": start_scope,
        "start_constraints_digest": constraints_digest,
        "subsequent_cycle_start_request": request_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleStartRequestReceipt(**outer, receipt_digest=sha(outer))
