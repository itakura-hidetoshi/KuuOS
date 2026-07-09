from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_literature_grounded_selective_foresight_gate_v0_40"
SOURCE_VERSION = "kuuos_planos_actos_invocation_receipt_v0_39"

REQUIRED_LITERATURE_SIGNALS = (
    "dynamic_planning_compute_accounted",
    "selective_foresight_required",
    "uncertainty_calibration_required",
    "memory_mismatch_review_required",
    "counterfactual_coverage_required",
    "cost_safety_robustness_evaluation_required",
)

SELECTIVE_FORESIGHT_GATE_BOUNDARY = {
    "gate_owned_by_plan_os": True,
    "source_actos_invocation_receipt_preserved": True,
    "selected_candidate_bound_to_invocation_receipt": True,
    "materialization_execution_preserved": True,
    "activation_authorization_preserved": True,
    "actos_invocation_preserved": True,
    "literature_grounding_preserved": True,
    "selective_foresight_gate_only": True,
    "dynamic_planning_compute_accounted": True,
    "selective_foresight_required": True,
    "uncertainty_calibration_required": True,
    "memory_mismatch_review_required": True,
    "counterfactual_coverage_required": True,
    "cost_safety_robustness_evaluation_required": True,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class LiteratureGroundedSelectiveForesightGateRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_actos_invocation_receipt_digest: str
    source_activation_grant_digest: str
    literature_basis_digest: str
    selective_foresight_gate_digest: str
    gate_scope: str
    dynamic_planning_compute_accounted: bool = True
    selective_foresight_required: bool = True
    uncertainty_calibration_required: bool = True
    memory_mismatch_review_required: bool = True
    counterfactual_coverage_required: bool = True
    cost_safety_robustness_evaluation_required: bool = True
    execution_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LiteratureGroundedSelectiveForesightGateReceipt:
    version: str
    source_version: str
    status: str
    source_actos_invocation_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    literature_basis_digest: str
    selective_foresight_gate: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _seq(value: Any) -> Sequence[Any]:
    return value if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)) else ()


def _truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass", "required"}
    return bool(value)


def _digest(value: Any) -> str:
    return sha(value)


def _source_invocation_receipt_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("actos_invocation_receipt"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_actos_invocation_receipt_version_invalid")
    if receipt.get("status") != "PLANOS_ACTOS_INVOCATION_RECEIPT_READY":
        blockers.append("source_actos_invocation_receipt_not_ready")
    boundary = _m(receipt.get("boundary"))
    for required in (
        "receipt_owned_by_plan_os",
        "source_activation_authorization_grant_preserved",
        "selected_candidate_bound_to_activation_grant",
        "materialization_execution_preserved",
        "activation_authorization_preserved",
        "actos_invocation_receipt_only",
        "materialization_authorization_granted",
        "materialization_executed",
        "activation_authorization_granted",
        "actos_invoked",
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
        blockers.append("source_actos_invocation_receipt_digest_missing")
    record = _source_invocation_receipt_record(receipt)
    if not record:
        blockers.append("source_actos_invocation_receipt_record_missing")
    for required in (
        "materialization_authorization_granted",
        "materialization_executed",
        "activation_authorization_granted",
        "actos_invoked",
    ):
        if record and _truthy(record.get(required)) is not True:
            blockers.append(f"source_record_{required}_missing")
    if record and _truthy(record.get("execution_ready")):
        blockers.append("source_record_execution_ready_promoted")
    return blockers


def _literature_blockers(evidence: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    sources = _seq(evidence.get("primary_sources"))
    if len(sources) < 4:
        blockers.append("literature_primary_sources_insufficient")
    for signal in REQUIRED_LITERATURE_SIGNALS:
        if _truthy(evidence.get(signal)) is not True:
            blockers.append(f"literature_signal_{signal}_missing")
    if _truthy(evidence.get("execution_granted")):
        blockers.append("literature_evidence_execution_promoted")
    return blockers


def build_literature_grounded_selective_foresight_gate(
    *,
    actos_invocation_receipt: Mapping[str, Any],
    literature_evidence: Mapping[str, Any],
) -> LiteratureGroundedSelectiveForesightGateReceipt:
    source = _m(actos_invocation_receipt)
    evidence = _m(literature_evidence)
    blockers = _source_blockers(source) + _literature_blockers(evidence)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_invocation_receipt_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_invocation_receipt_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_invocation_receipt_mismatch")

    literature_basis_digest = _digest(
        {
            "primary_sources": list(_seq(evidence.get("primary_sources"))),
            "signals": {signal: bool(_truthy(evidence.get(signal))) for signal in REQUIRED_LITERATURE_SIGNALS},
        }
    )

    gate = None
    if selected_id and selected_digest and not blockers:
        gate_obj = LiteratureGroundedSelectiveForesightGateRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_actos_invocation_receipt_digest=str(source.get("receipt_digest", "")),
            source_activation_grant_digest=str(record.get("source_activation_grant_digest", "")),
            literature_basis_digest=literature_basis_digest,
            selective_foresight_gate_digest=_digest(
                {
                    "source_actos_invocation_receipt_digest": source.get("receipt_digest"),
                    "source_activation_grant_digest": record.get("source_activation_grant_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "literature_basis_digest": literature_basis_digest,
                    "scope": "literature_grounded_selective_foresight_gate_only",
                }
            ),
            gate_scope="literature_grounded_selective_foresight_gate_only",
        )
        gate = gate_obj.to_dict()

    status = "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_READY" if not blockers else "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_actos_invocation_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "literature_basis_digest": literature_basis_digest,
        "selective_foresight_gate": gate,
        "blockers": list(blockers),
        "boundary": dict(SELECTIVE_FORESIGHT_GATE_BOUNDARY),
    }
    return LiteratureGroundedSelectiveForesightGateReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: kuuos_planos_literature_grounded_selective_foresight_gate_v0_40.py ACTOS_INVOCATION_RECEIPT.json LITERATURE_EVIDENCE.json",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        source = json.load(handle)
    with open(argv[2], "r", encoding="utf-8") as handle:
        evidence = json.load(handle)
    receipt = build_literature_grounded_selective_foresight_gate(
        actos_invocation_receipt=source,
        literature_evidence=evidence,
    )
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
