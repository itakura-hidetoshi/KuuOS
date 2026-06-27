#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_connection_deformation_v0_70 import (
    ConnectionDeformation,
    deformation_issues,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_module_connection_v0_70 import ModuleConnection, curvature_observable
from runtime.kuuos_module_rollback_v0_70 import rollback_connection
from runtime.kuuos_state_module_v0_70 import KuuStateModule

VERSION = "kuuos_module_candidate_validation_v0_70"
READY = "MODULE_CONNECTION_CANDIDATE_READY"
BLOCKED = "MODULE_CONNECTION_CANDIDATE_BLOCKED"
TOLERANCE = 1.0e-9


@dataclass(frozen=True)
class ModuleSelfOrganizationReceipt:
    status: str
    source_module_digest: str
    source_connection_digest: str
    candidate_connection_digest: str
    deformation_digest: str
    source_curvature_observable: float
    candidate_curvature_observable: float
    curvature_nonincreasing: bool
    semantic_projectors_commute: bool
    protected_part_zero: bool
    authority_filtration_preserved: bool
    gauge_observables_preserved: bool
    rollback_exact: bool
    source_unchanged: bool
    candidate_only: bool
    live_effect_allowed: bool
    authority_widening_allowed: bool
    blockers: tuple[str, ...]
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return payload


def self_organization_receipt_digest(receipt: ModuleSelfOrganizationReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


def validate_module_candidate(
    module: KuuStateModule,
    source: ModuleConnection,
    deformation: ConnectionDeformation,
    gauge: SignedPermutation,
) -> tuple[ModuleConnection, ModuleSelfOrganizationReceipt]:
    source_digest_before = source.digest
    issues = list(deformation_issues(module, source, deformation))
    if not module.is_admissible_gauge(gauge):
        issues.append("module_gauge_not_admissible")

    candidate = deformation.candidate_connection(source)
    source_curvature = curvature_observable(source)
    candidate_curvature = curvature_observable(candidate)
    curvature_nonincreasing = candidate_curvature <= source_curvature + TOLERANCE
    if not curvature_nonincreasing:
        issues.append("candidate_curvature_increased")

    gauge_observables_preserved = False
    if module.is_admissible_gauge(gauge):
        source_gauge_curvature = curvature_observable(source.gauge_transform(gauge))
        candidate_gauge_curvature = curvature_observable(candidate.gauge_transform(gauge))
        gauge_observables_preserved = (
            abs(source_gauge_curvature - source_curvature) <= TOLERANCE
            and abs(candidate_gauge_curvature - candidate_curvature) <= TOLERANCE
        )
    if not gauge_observables_preserved:
        issues.append("gauge_curvature_observable_not_preserved")

    _, rollback = rollback_connection(source, candidate, deformation)
    rollback_exact = rollback.algebraic_exact and rollback.structural_exact and rollback.digest_exact
    if not rollback_exact:
        issues.append("module_connection_rollback_not_exact")

    source_unchanged = source.digest == source_digest_before
    if not source_unchanged:
        issues.append("source_connection_changed")

    semantic_ok = "deformation_semantic_projector_noncommuting" not in issues
    protected_ok = "deformation_protected_part_nonzero" not in issues
    filtration_ok = "deformation_authority_filtration_not_preserved" not in issues
    issues = list(dict.fromkeys(issues))
    status = READY if not issues else BLOCKED

    receipt = ModuleSelfOrganizationReceipt(
        status,
        module.digest,
        source.digest,
        candidate.digest,
        deformation.digest,
        source_curvature,
        candidate_curvature,
        curvature_nonincreasing,
        semantic_ok,
        protected_ok,
        filtration_ok,
        gauge_observables_preserved,
        rollback_exact,
        source_unchanged,
        deformation.candidate_only,
        False,
        False,
        tuple(issues),
        "",
    )
    return candidate, replace(
        receipt,
        receipt_digest=self_organization_receipt_digest(receipt),
    )
