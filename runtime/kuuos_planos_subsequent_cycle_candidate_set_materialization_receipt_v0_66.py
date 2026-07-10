from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65"
MAX_CANDIDATES = 16

SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_candidate_generation_start_receipt_preserved": True,
    "selected_candidate_provenance_bound_to_generation_start": True,
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
    "next_cycle_admission_grant_preserved": True,
    "next_cycle_start_receipt_preserved": True,
    "next_cycle_closeout_receipt_preserved": True,
    "subsequent_cycle_replan_request_preserved": True,
    "candidate_generation_start_receipt_preserved": True,
    "next_cycle_cycle_closed": True,
    "subsequent_cycle_replan_requested": True,
    "subsequent_cycle_candidate_generation_started": True,
    "subsequent_cycle_candidate_set_materialization_receipt_only": True,
    "subsequent_cycle_candidate_set_materialized": True,
    "subsequent_cycle_candidate_set_nonempty": True,
    "subsequent_cycle_candidate_ids_unique": True,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "receipt_owned_by_plan_os",
    "source_subsequent_cycle_replan_request_preserved",
    "selected_candidate_bound_to_replan_request",
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
    "next_cycle_admission_request_preserved",
    "next_cycle_admission_grant_preserved",
    "next_cycle_start_receipt_preserved",
    "next_cycle_closeout_receipt_preserved",
    "subsequent_cycle_replan_request_preserved",
    "next_cycle_admission_requested",
    "next_cycle_admission_granted",
    "next_cycle_started",
    "next_cycle_cycle_closed",
    "subsequent_cycle_replan_requested",
    "subsequent_cycle_candidate_generation_start_receipt_only",
    "subsequent_cycle_candidate_generation_started",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "subsequent_cycle_candidate_set_materialized",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)


@dataclass(frozen=True)
class MaterializedCandidate:
    candidate_id: str
    parent_candidate_id: str
    parent_candidate_digest: str
    objective: str
    constraint_digest: str
    ordinal: int
    candidate_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCandidateSetMaterializationRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_candidate_generation_start_receipt_digest: str
    source_subsequent_cycle_replan_request_digest: str
    source_next_cycle_closeout_receipt_digest: str
    source_blocker_release_authorization_request_digest: str
    source_truth_authority_closeout_receipt_digest: str
    source_memory_overwrite_closeout_receipt_digest: str
    candidate_count: int
    candidate_set_digest: str
    materialization_digest: str
    materialization_scope: str = "subsequent_cycle_candidate_set_materialization_receipt_only"
    memory_overwrite_preserved: bool = True
    truth_authority_preserved: bool = True
    blocker_release_preserved: bool = True
    next_cycle_cycle_closed: bool = True
    subsequent_cycle_replan_requested: bool = True
    subsequent_cycle_candidate_generation_started: bool = True
    subsequent_cycle_candidate_set_materialized: bool = True
    subsequent_cycle_candidate_selected: bool = False
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCandidateSetMaterializationReceipt:
    version: str
    source_version: str
    status: str
    source_candidate_generation_start_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set: list[dict[str, Any]]
    candidate_set_digest: str
    candidate_count: int
    subsequent_cycle_candidate_set_materialization_receipt: dict[str, Any] | None
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


def _source_start_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("subsequent_cycle_candidate_generation_start_receipt"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_candidate_generation_start_receipt_version_invalid")
    if receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_READY":
        blockers.append("source_candidate_generation_start_receipt_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_candidate_generation_start_receipt_digest_missing")
    record = _source_start_record(receipt)
    if not record:
        blockers.append("source_candidate_generation_start_receipt_record_missing")
    if record:
        for field in (
            "memory_overwrite_preserved",
            "truth_authority_preserved",
            "blocker_release_preserved",
            "next_cycle_cycle_closed",
            "subsequent_cycle_replan_requested",
            "subsequent_cycle_candidate_generation_started",
        ):
            if _truthy(record.get(field)) is not True:
                blockers.append(f"source_record_{field}_missing")
        for field in (
            "subsequent_cycle_candidate_set_materialized",
            "subsequent_cycle_candidate_selected",
            "subsequent_cycle_admission_requested",
        ):
            if _truthy(record.get(field)):
                blockers.append(f"source_record_{field}_promoted")
    return blockers


def _materialize_candidates(
    *,
    candidate_specs: Sequence[Mapping[str, Any]],
    parent_candidate_id: str,
    parent_candidate_digest: str,
) -> tuple[list[MaterializedCandidate], list[str]]:
    blockers: list[str] = []
    if not candidate_specs:
        blockers.append("candidate_specs_empty")
        return [], blockers
    if len(candidate_specs) > MAX_CANDIDATES:
        blockers.append("candidate_specs_exceed_bounded_limit")

    materialized: list[MaterializedCandidate] = []
    ids: list[str] = []
    for ordinal, raw_spec in enumerate(candidate_specs):
        spec = _m(raw_spec)
        candidate_id = str(spec.get("candidate_id", "")).strip()
        objective = str(spec.get("objective", "")).strip()
        constraint_digest = str(spec.get("constraint_digest", "")).strip()
        if not candidate_id:
            blockers.append(f"candidate_{ordinal}_id_missing")
        if not objective:
            blockers.append(f"candidate_{ordinal}_objective_missing")
        if not constraint_digest:
            blockers.append(f"candidate_{ordinal}_constraint_digest_missing")
        if candidate_id:
            ids.append(candidate_id)
        if candidate_id and objective and constraint_digest:
            candidate_digest = sha({
                "candidate_id": candidate_id,
                "parent_candidate_id": parent_candidate_id,
                "parent_candidate_digest": parent_candidate_digest,
                "objective": objective,
                "constraint_digest": constraint_digest,
                "ordinal": ordinal,
            })
            materialized.append(
                MaterializedCandidate(
                    candidate_id=candidate_id,
                    parent_candidate_id=parent_candidate_id,
                    parent_candidate_digest=parent_candidate_digest,
                    objective=objective,
                    constraint_digest=constraint_digest,
                    ordinal=ordinal,
                    candidate_digest=candidate_digest,
                )
            )
    if len(ids) != len(set(ids)):
        blockers.append("candidate_ids_not_unique")
    return materialized, blockers


def build_subsequent_cycle_candidate_set_materialization_receipt(
    *,
    candidate_generation_start_receipt: Mapping[str, Any],
    candidate_specs: Sequence[Mapping[str, Any]],
) -> SubsequentCycleCandidateSetMaterializationReceipt:
    source = _m(candidate_generation_start_receipt)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    source_record = _source_start_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if source_record:
        if selected_id and str(source_record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_generation_start_mismatch")
        if selected_digest and str(source_record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_generation_start_mismatch")

    candidates, candidate_blockers = _materialize_candidates(
        candidate_specs=candidate_specs,
        parent_candidate_id=selected_id,
        parent_candidate_digest=selected_digest,
    )
    blockers.extend(candidate_blockers)
    candidate_set = [candidate.to_dict() for candidate in candidates]
    candidate_set_digest = sha(candidate_set) if candidate_set else ""

    materialization_record = None
    if selected_id and selected_digest and candidate_set and not blockers:
        record_obj = SubsequentCycleCandidateSetMaterializationRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_candidate_generation_start_receipt_digest=str(source.get("receipt_digest", "")),
            source_subsequent_cycle_replan_request_digest=str(source_record.get("source_subsequent_cycle_replan_request_digest", "")),
            source_next_cycle_closeout_receipt_digest=str(source_record.get("source_next_cycle_closeout_receipt_digest", "")),
            source_blocker_release_authorization_request_digest=str(source_record.get("source_blocker_release_authorization_request_digest", "")),
            source_truth_authority_closeout_receipt_digest=str(source_record.get("source_truth_authority_closeout_receipt_digest", "")),
            source_memory_overwrite_closeout_receipt_digest=str(source_record.get("source_memory_overwrite_closeout_receipt_digest", "")),
            candidate_count=len(candidate_set),
            candidate_set_digest=candidate_set_digest,
            materialization_digest=sha({
                "source_candidate_generation_start_receipt_digest": source.get("receipt_digest"),
                "source_subsequent_cycle_replan_request_digest": source_record.get("source_subsequent_cycle_replan_request_digest"),
                "selected_candidate_id": selected_id,
                "selected_candidate_digest": selected_digest,
                "candidate_set_digest": candidate_set_digest,
                "candidate_count": len(candidate_set),
                "scope": "subsequent_cycle_candidate_set_materialization_receipt_only",
            }),
        )
        materialization_record = record_obj.to_dict()

    status = (
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_RECEIPT_READY"
        if not blockers
        else "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_RECEIPT_BLOCKED"
    )
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_candidate_generation_start_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "candidate_set": candidate_set,
        "candidate_set_digest": candidate_set_digest,
        "candidate_count": len(candidate_set),
        "subsequent_cycle_candidate_set_materialization_receipt": materialization_record,
        "blockers": blockers,
        "boundary": dict(SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_BOUNDARY),
    }
    return SubsequentCycleCandidateSetMaterializationReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66.py "
            "CANDIDATE_GENERATION_START_RECEIPT.json CANDIDATE_SPECS.json",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        source = json.load(handle)
    with open(argv[2], "r", encoding="utf-8") as handle:
        candidate_specs = json.load(handle)
    if not isinstance(candidate_specs, list):
        print("candidate specs must be a JSON array", file=sys.stderr)
        return 2
    receipt = build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=source,
        candidate_specs=candidate_specs,
    )
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
