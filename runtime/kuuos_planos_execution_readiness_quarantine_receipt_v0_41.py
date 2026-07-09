from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_execution_readiness_quarantine_receipt_v0_41"
SOURCE_VERSION = "kuuos_planos_literature_grounded_selective_foresight_gate_v0_40"

EXECUTION_READINESS_QUARANTINE_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_selective_foresight_gate_preserved": True,
    "selected_candidate_bound_to_selective_foresight_gate": True,
    "materialization_execution_preserved": True,
    "activation_authorization_preserved": True,
    "actos_invocation_preserved": True,
    "literature_grounding_preserved": True,
    "selective_foresight_gate_preserved": True,
    "execution_readiness_quarantine_only": True,
    "dynamic_planning_compute_accounted": True,
    "uncertainty_calibration_required": True,
    "memory_mismatch_review_required": True,
    "counterfactual_coverage_required": True,
    "cost_safety_robustness_evaluation_required": True,
    "execution_ready": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class ExecutionReadinessQuarantineRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_selective_foresight_gate_digest: str
    literature_basis_digest: str
    quarantine_receipt_digest: str
    quarantine_scope: str
    execution_ready: bool = False
    execution_granted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionReadinessQuarantineReceipt:
    version: str
    source_version: str
    status: str
    source_selective_foresight_gate_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    literature_basis_digest: str
    execution_readiness_quarantine: dict[str, Any] | None
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


def _digest(value: Any) -> str:
    return sha(value)


def _source_gate_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("selective_foresight_gate"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_selective_foresight_gate_version_invalid")
    if receipt.get("status") != "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_READY":
        blockers.append("source_selective_foresight_gate_not_ready")
    boundary = _m(receipt.get("boundary"))
    for required in (
        "gate_owned_by_plan_os",
        "source_actos_invocation_receipt_preserved",
        "selected_candidate_bound_to_invocation_receipt",
        "materialization_execution_preserved",
        "activation_authorization_preserved",
        "actos_invocation_preserved",
        "literature_grounding_preserved",
        "selective_foresight_gate_only",
        "dynamic_planning_compute_accounted",
        "uncertainty_calibration_required",
        "memory_mismatch_review_required",
        "counterfactual_coverage_required",
        "cost_safety_robustness_evaluation_required",
    ):
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in (
        "execution_granted",
        "truth_authority_granted",
        "memory_overwrite_granted",
        "blocker_release_granted",
        "external_commit_granted",
    ):
        if boundary.get(closed) is not False:
            blockers.append(f"source_boundary_{closed}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_selective_foresight_gate_digest_missing")
    record = _source_gate_record(receipt)
    if not record:
        blockers.append("source_selective_foresight_gate_record_missing")
    if record and _truthy(record.get("execution_ready")):
        blockers.append("source_record_execution_ready_promoted")
    return blockers


def build_execution_readiness_quarantine_receipt(
    *,
    selective_foresight_gate: Mapping[str, Any],
) -> ExecutionReadinessQuarantineReceipt:
    source = _m(selective_foresight_gate)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_gate_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_selective_foresight_gate_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_selective_foresight_gate_mismatch")

    literature_basis_digest = str(source.get("literature_basis_digest", ""))
    if not literature_basis_digest:
        blockers.append("literature_basis_digest_missing")

    quarantine = None
    if selected_id and selected_digest and literature_basis_digest and not blockers:
        quarantine_obj = ExecutionReadinessQuarantineRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_selective_foresight_gate_digest=str(source.get("receipt_digest", "")),
            literature_basis_digest=literature_basis_digest,
            quarantine_receipt_digest=_digest(
                {
                    "source_selective_foresight_gate_digest": source.get("receipt_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "literature_basis_digest": literature_basis_digest,
                    "scope": "execution_readiness_quarantine_only",
                }
            ),
            quarantine_scope="execution_readiness_quarantine_only",
        )
        quarantine = quarantine_obj.to_dict()

    status = "PLANOS_EXECUTION_READINESS_QUARANTINE_RECEIPT_READY" if not blockers else "PLANOS_EXECUTION_READINESS_QUARANTINE_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_selective_foresight_gate_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "literature_basis_digest": literature_basis_digest,
        "execution_readiness_quarantine": quarantine,
        "blockers": list(blockers),
        "boundary": dict(EXECUTION_READINESS_QUARANTINE_BOUNDARY),
    }
    return ExecutionReadinessQuarantineReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "usage: kuuos_planos_execution_readiness_quarantine_receipt_v0_41.py SELECTIVE_FORESIGHT_GATE.json",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        source = json.load(handle)
    receipt = build_execution_readiness_quarantine_receipt(selective_foresight_gate=source)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
