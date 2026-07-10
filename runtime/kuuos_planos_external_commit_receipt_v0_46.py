from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_external_commit_receipt_v0_46"
SOURCE_VERSION = "kuuos_planos_external_commit_authorization_grant_v0_45"

EXTERNAL_COMMIT_RECEIPT_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_external_commit_authorization_grant_preserved": True,
    "selected_candidate_bound_to_external_commit_grant": True,
    "materialization_execution_preserved": True,
    "activation_authorization_preserved": True,
    "actos_invocation_preserved": True,
    "literature_grounding_preserved": True,
    "dynamic_planning_compute_accounted": True,
    "selective_foresight_preserved": True,
    "uncertainty_calibration_preserved": True,
    "memory_mismatch_review_preserved": True,
    "counterfactual_coverage_preserved": True,
    "cost_safety_robustness_evaluation_preserved": True,
    "execution_authorization_grant_preserved": True,
    "execution_receipt_preserved": True,
    "execution_authorization_requested": True,
    "execution_authorization_granted": True,
    "execution_granted": True,
    "external_commit_authorization_request_preserved": True,
    "external_commit_authorization_grant_preserved": True,
    "external_commit_receipt_only": True,
    "external_commit_authorization_requested": True,
    "external_commit_authorization_granted": True,
    "external_commit_granted": True,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "grant_owned_by_plan_os",
    "source_external_commit_authorization_request_preserved",
    "selected_candidate_bound_to_external_commit_request",
    "materialization_execution_preserved",
    "activation_authorization_preserved",
    "actos_invocation_preserved",
    "literature_grounding_preserved",
    "dynamic_planning_compute_accounted",
    "selective_foresight_preserved",
    "uncertainty_calibration_preserved",
    "memory_mismatch_review_preserved",
    "counterfactual_coverage_preserved",
    "cost_safety_robustness_evaluation_preserved",
    "execution_authorization_grant_preserved",
    "execution_receipt_preserved",
    "execution_authorization_requested",
    "execution_authorization_granted",
    "execution_granted",
    "external_commit_authorization_request_preserved",
    "external_commit_authorization_grant_only",
    "external_commit_authorization_requested",
    "external_commit_authorization_granted",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "external_commit_granted",
    "truth_authority_granted",
    "memory_overwrite_granted",
    "blocker_release_granted",
)


@dataclass(frozen=True)
class ExternalCommitReceiptRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_external_commit_authorization_grant_digest: str
    source_external_commit_authorization_request_digest: str
    external_commit_receipt_digest: str
    receipt_scope: str
    execution_authorization_requested: bool = True
    execution_authorization_granted: bool = True
    execution_granted: bool = True
    external_commit_authorization_requested: bool = True
    external_commit_authorization_granted: bool = True
    external_commit_granted: bool = True
    memory_overwrite_ready: bool = False
    truth_authority_ready: bool = False
    blocker_release_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExternalCommitReceipt:
    version: str
    source_version: str
    status: str
    source_external_commit_authorization_grant_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    external_commit_receipt: dict[str, Any] | None
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


def _source_grant_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("external_commit_authorization_grant"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_external_commit_authorization_grant_version_invalid")
    if receipt.get("status") != "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_READY":
        blockers.append("source_external_commit_authorization_grant_not_ready")
    boundary = _m(receipt.get("boundary"))
    for required in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(required) is not True:
            blockers.append(f"source_boundary_{required}_missing")
    for closed in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(closed) is not False:
            blockers.append(f"source_boundary_{closed}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_external_commit_authorization_grant_digest_missing")
    record = _source_grant_record(receipt)
    if not record:
        blockers.append("source_external_commit_authorization_grant_record_missing")
    if record:
        for required in (
            "execution_authorization_requested",
            "execution_authorization_granted",
            "execution_granted",
            "external_commit_authorization_requested",
            "external_commit_authorization_granted",
        ):
            if _truthy(record.get(required)) is not True:
                blockers.append(f"source_record_{required}_missing")
        for closed in (
            "external_commit_ready",
            "memory_overwrite_ready",
            "truth_authority_ready",
            "blocker_release_ready",
        ):
            if _truthy(record.get(closed)):
                blockers.append(f"source_record_{closed}_promoted")
    return blockers


def build_external_commit_receipt(
    *,
    external_commit_grant: Mapping[str, Any],
) -> ExternalCommitReceipt:
    source = _m(external_commit_grant)
    blockers = _source_blockers(source)
    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    record = _source_grant_record(source)
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")
    if record:
        if selected_id and str(record.get("selected_candidate_id", "")) != selected_id:
            blockers.append("selected_candidate_id_external_commit_grant_mismatch")
        if selected_digest and str(record.get("selected_candidate_digest", "")) != selected_digest:
            blockers.append("selected_candidate_digest_external_commit_grant_mismatch")

    receipt_record = None
    if selected_id and selected_digest and not blockers:
        receipt_obj = ExternalCommitReceiptRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_external_commit_authorization_grant_digest=str(source.get("receipt_digest", "")),
            source_external_commit_authorization_request_digest=str(record.get("source_external_commit_authorization_request_digest", "")),
            external_commit_receipt_digest=_digest(
                {
                    "source_external_commit_authorization_grant_digest": source.get("receipt_digest"),
                    "source_external_commit_authorization_request_digest": record.get("source_external_commit_authorization_request_digest"),
                    "selected_candidate_id": selected_id,
                    "selected_candidate_digest": selected_digest,
                    "scope": "external_commit_receipt_only",
                }
            ),
            receipt_scope="external_commit_receipt_only",
        )
        receipt_record = receipt_obj.to_dict()

    status = "PLANOS_EXTERNAL_COMMIT_RECEIPT_READY" if not blockers else "PLANOS_EXTERNAL_COMMIT_RECEIPT_BLOCKED"
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_external_commit_authorization_grant_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "external_commit_receipt": receipt_record,
        "blockers": list(blockers),
        "boundary": dict(EXTERNAL_COMMIT_RECEIPT_BOUNDARY),
    }
    return ExternalCommitReceipt(receipt_digest=_digest(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_external_commit_receipt_v0_46.py EXTERNAL_COMMIT_GRANT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_external_commit_receipt(external_commit_grant=payload)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
