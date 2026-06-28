#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_self_repair_v0_79"

APPLIED = "REPOSITORY_REPAIR_APPLIED"
ROLLED_BACK = "REPOSITORY_REPAIR_ROLLED_BACK"
NO_CHANGE = "REPOSITORY_REPAIR_NO_CHANGE"
MAX_CYCLES = "REPOSITORY_REPAIR_MAX_CYCLES"


@dataclass(frozen=True)
class RepositorySnapshot:
    root_label: str
    all_paths: tuple[str, ...]
    text_files: tuple[tuple[str, str], ...]
    version: str = VERSION

    @property
    def texts(self) -> dict[str, str]:
        return dict(self.text_files)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_label": self.root_label,
            "all_paths": list(self.all_paths),
            "text_files": [[path, text] for path, text in self.text_files],
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryContract:
    manifest_path: str
    manifest_digest: str
    referenced_paths: tuple[str, ...]
    validator: str
    strict_formal_root: str
    aggregate_lean_modules: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryObservation:
    snapshot_digest: str
    contract_digests: tuple[str, ...]
    malformed_contracts: tuple[str, ...]
    missing_referenced_paths: tuple[str, ...]
    missing_runtime_validator_registrations: tuple[str, ...]
    missing_lake_roots: tuple[str, ...]
    missing_aggregate_imports: tuple[str, ...]
    direct_pr_trigger_workflows: tuple[str, ...]
    weighted_defect_score: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryPatch:
    path: str
    before_digest: str
    after_text: str
    repair_kind: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryRepairCandidate:
    candidate_id: str
    source_snapshot_digest: str
    source_observation_digest: str
    patches: tuple[RepositoryPatch, ...]
    protected_paths_preserved: bool

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["patches"] = [patch.to_dict() for patch in self.patches]
        return payload

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryShadowAssessment:
    candidate_digest: str
    shadow_snapshot_digest: str
    shadow_observation_digest: str
    source_score: int
    candidate_score: int
    nonworsening: bool
    strict_improvement: bool
    protected_paths_preserved: bool
    admissible: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class RepositoryRepairCycleReceipt:
    cycle_id: str
    status: str
    source_snapshot_digest: str
    source_observation_digest: str
    candidate_digests: tuple[str, ...]
    assessment_digests: tuple[str, ...]
    selected_candidate_digest: str
    final_snapshot_digest: str
    final_observation_digest: str
    rollback_performed: bool
    exact_source_restored: bool
    external_approval_required: bool
    arbitrary_code_generation_used: bool
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repair_cycle_receipt_digest(receipt: RepositoryRepairCycleReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryRepairSupervisorReceipt:
    supervisor_id: str
    status: str
    initial_snapshot_digest: str
    final_snapshot_digest: str
    initial_score: int
    final_score: int
    cycle_receipt_digests: tuple[str, ...]
    cycle_count: int
    max_cycles: int
    external_approval_required: bool
    unbounded_execution_allowed: bool
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def supervisor_receipt_digest(receipt: RepositoryRepairSupervisorReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
