#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_self_organizing_improvement_loop_v0_78"

ADOPTED = "SELF_ORGANIZATION_ADOPTED"
ROLLED_BACK = "SELF_ORGANIZATION_ROLLED_BACK"
NO_CHANGE = "SELF_ORGANIZATION_NO_CHANGE"


@dataclass(frozen=True)
class StructureState:
    revision: int
    coordinates: tuple[tuple[str, float], ...]
    protected_coordinates: tuple[str, ...]
    lineage: tuple[str, ...] = ()
    version: str = VERSION

    def __post_init__(self) -> None:
        if self.revision < 0:
            raise ValueError("structure_revision_invalid")
        names = tuple(name for name, _ in self.coordinates)
        if not names or len(set(names)) != len(names):
            raise ValueError("structure_coordinates_invalid")
        if tuple(sorted(names)) != names:
            raise ValueError("structure_coordinates_not_canonical")
        if any(name not in names for name in self.protected_coordinates):
            raise ValueError("protected_coordinate_missing")
        if len(set(self.protected_coordinates)) != len(self.protected_coordinates):
            raise ValueError("protected_coordinate_duplicate")

    @property
    def values(self) -> dict[str, float]:
        return {name: float(value) for name, value in self.coordinates}

    def to_dict(self) -> dict[str, Any]:
        return {
            "revision": self.revision,
            "coordinates": [[name, value] for name, value in self.coordinates],
            "protected_coordinates": list(self.protected_coordinates),
            "lineage": list(self.lineage),
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class ObservationContext:
    context_id: str
    targets: tuple[tuple[str, float], ...]
    weights: tuple[tuple[str, float], ...]

    def __post_init__(self) -> None:
        if not self.context_id:
            raise ValueError("observation_context_id_missing")
        target_names = tuple(name for name, _ in self.targets)
        weight_names = tuple(name for name, _ in self.weights)
        if tuple(sorted(target_names)) != target_names:
            raise ValueError("observation_targets_not_canonical")
        if target_names != weight_names:
            raise ValueError("observation_target_weight_domain_mismatch")
        if any(weight < 0.0 for _, weight in self.weights):
            raise ValueError("observation_weight_negative")

    @property
    def target_map(self) -> dict[str, float]:
        return {name: float(value) for name, value in self.targets}

    @property
    def weight_map(self) -> dict[str, float]:
        return {name: float(value) for name, value in self.weights}

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class ObservationSnapshot:
    context_id: str
    context_digest: str
    state_digest: str
    state_revision: int
    values: tuple[tuple[str, float], ...]
    score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class StructuralDiagnosis:
    observation_digest: str
    pressures: tuple[tuple[str, float], ...]
    mutable_pressures: tuple[tuple[str, float], ...]
    protected_pressure_detected: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class FiniteStructureCandidate:
    candidate_id: str
    source_state_digest: str
    changes: tuple[tuple[str, float], ...]
    rationale_digest: str

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id_missing")
        names = tuple(name for name, _ in self.changes)
        if tuple(sorted(names)) != names or len(set(names)) != len(names):
            raise ValueError("candidate_changes_not_canonical")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class ShadowAssessment:
    candidate_digest: str
    candidate_state_digest: str
    aggregate_source_score: float
    aggregate_candidate_score: float
    worst_score_delta: float
    nonworsening_in_all_contexts: bool
    strict_improvement_observed: bool
    protected_coordinates_preserved: bool
    admissible: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class SelfOrganizationPolicy:
    max_candidates: int = 8
    max_changed_coordinates: int = 2
    step_fractions: tuple[float, ...] = (0.25, 0.5, 1.0)
    tolerance: float = 1.0e-9
    require_shadow_nonworsening: bool = True
    require_strict_shadow_improvement: bool = True
    require_reobservation_nonworsening: bool = True

    def __post_init__(self) -> None:
        if self.max_candidates <= 0:
            raise ValueError("max_candidates_invalid")
        if self.max_changed_coordinates <= 0:
            raise ValueError("max_changed_coordinates_invalid")
        if not self.step_fractions:
            raise ValueError("step_fractions_empty")
        if any(step <= 0.0 or step > 1.0 for step in self.step_fractions):
            raise ValueError("step_fraction_invalid")
        if self.tolerance < 0.0:
            raise ValueError("tolerance_invalid")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class SelfOrganizationCycleReceipt:
    cycle_id: str
    status: str
    source_state_digest: str
    source_revision: int
    initial_observation_digest: str
    diagnosis_digest: str
    candidate_digests: tuple[str, ...]
    shadow_assessment_digests: tuple[str, ...]
    selected_candidate_digest: str
    provisional_state_digest: str
    final_state_digest: str
    final_revision: int
    reobservation_digest: str
    rollback_performed: bool
    source_restored_on_failure: bool
    finite_candidate_generation: bool
    external_approval_required: bool
    authority_widening_performed: bool
    host_state_write_performed: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidate_digests"] = list(self.candidate_digests)
        payload["shadow_assessment_digests"] = list(self.shadow_assessment_digests)
        return payload


def cycle_receipt_digest(receipt: SelfOrganizationCycleReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
