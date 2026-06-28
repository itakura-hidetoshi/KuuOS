#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_connection_deformation_v0_70 import ConnectionDeformation
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    LeibnizModuleConnection,
    curvature_representation_exact,
    difference_is_left_module_linear,
    gauge_covariant_on,
    satisfies_leibniz,
)
from runtime.kuuos_module_candidate_validation_v0_70 import (
    READY as MODULE_READY,
    validate_module_candidate,
)
from runtime.kuuos_module_connection_v0_70 import Matrix
from runtime.kuuos_noncommutative_differential_calculus_v0_71 import (
    InnerDifferentialCalculus,
)
from runtime.kuuos_state_module_v0_70 import KuuStateModule

VERSION = "kuuos_leibniz_candidate_validation_v0_71"
READY = "LEIBNIZ_CONNECTION_CANDIDATE_READY"
BLOCKED = "LEIBNIZ_CONNECTION_CANDIDATE_BLOCKED"


@dataclass(frozen=True)
class LeibnizSelfOrganizationReceipt:
    status: str
    calculus_digest: str
    source_module_digest: str
    source_connection_digest: str
    candidate_connection_digest: str
    deformation_digest: str
    algebra_noncommutative: bool
    differential_leibniz_exact: bool
    differential_directions_commute: bool
    source_connection_leibniz_exact: bool
    candidate_connection_leibniz_exact: bool
    connection_difference_module_linear: bool
    curvature_module_linear: bool
    gauge_covariant: bool
    semantic_projectors_commute: bool
    protected_part_zero: bool
    authority_filtration_preserved: bool
    curvature_nonincreasing: bool
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


def leibniz_receipt_digest(receipt: LeibnizSelfOrganizationReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


def validate_leibniz_candidate(
    module: KuuStateModule,
    calculus: InnerDifferentialCalculus,
    source: LeibnizModuleConnection,
    deformation: ConnectionDeformation,
    gauge: SignedPermutation,
    algebra_samples: tuple[Matrix, ...],
    module_sections: tuple[FreeLeftModuleSection, ...],
    noncommutative_witness: tuple[Matrix, Matrix],
) -> tuple[LeibnizModuleConnection, LeibnizSelfOrganizationReceipt]:
    issues: list[str] = []
    source_digest_before = source.digest
    try:
        source.require_compatible(calculus, module)
    except ValueError as error:
        issues.append(str(error))

    candidate_module, module_receipt = validate_module_candidate(
        module,
        source.module_connection,
        deformation,
        gauge,
    )
    candidate = LeibnizModuleConnection(calculus.digest, candidate_module)

    algebra_noncommutative = calculus.is_noncommutative_witness(
        noncommutative_witness[0],
        noncommutative_witness[1],
    )
    if not algebra_noncommutative:
        issues.append("context_algebra_noncommutative_witness_missing")

    differential_leibniz_exact = all(
        calculus.satisfies_leibniz(direction, left, right)
        for direction in range(len(calculus.direction_labels))
        for left in algebra_samples
        for right in algebra_samples
    )
    if not differential_leibniz_exact:
        issues.append("differential_calculus_leibniz_failed")

    differential_directions_commute = all(
        calculus.directions_commute_on(element)
        for element in algebra_samples
    )
    if not differential_directions_commute:
        issues.append("differential_directions_do_not_commute")

    source_connection_leibniz_exact = all(
        satisfies_leibniz(source, calculus, direction, algebra_element, section)
        for direction in range(len(calculus.direction_labels))
        for algebra_element in algebra_samples
        for section in module_sections
    )
    if not source_connection_leibniz_exact:
        issues.append("source_connection_leibniz_failed")

    candidate_connection_leibniz_exact = all(
        satisfies_leibniz(candidate, calculus, direction, algebra_element, section)
        for direction in range(len(calculus.direction_labels))
        for algebra_element in algebra_samples
        for section in module_sections
    )
    if not candidate_connection_leibniz_exact:
        issues.append("candidate_connection_leibniz_failed")

    connection_difference_module_linear = all(
        difference_is_left_module_linear(
            source,
            candidate,
            calculus,
            direction,
            algebra_element,
            section,
        )
        for direction in range(len(calculus.direction_labels))
        for algebra_element in algebra_samples
        for section in module_sections
    )
    if not connection_difference_module_linear:
        issues.append("connection_difference_not_module_linear")

    direction_pairs = tuple(
        (left, right)
        for left in range(len(calculus.direction_labels))
        for right in range(left + 1, len(calculus.direction_labels))
    )
    curvature_module_linear = all(
        curvature_representation_exact(connection, calculus, left, right, section)
        for connection in (source, candidate)
        for left, right in direction_pairs
        for section in module_sections
    )
    if not curvature_module_linear:
        issues.append("connection_curvature_not_module_linear")

    gauge_covariant = module.is_admissible_gauge(gauge) and all(
        gauge_covariant_on(connection, calculus, direction, section, gauge)
        for connection in (source, candidate)
        for direction in range(len(calculus.direction_labels))
        for section in module_sections
    )
    if not gauge_covariant:
        issues.append("leibniz_connection_not_gauge_covariant")

    if module_receipt.status != MODULE_READY:
        issues.extend(module_receipt.blockers)

    source_unchanged = source.digest == source_digest_before
    if not source_unchanged:
        issues.append("source_leibniz_connection_changed")

    issues = list(dict.fromkeys(issues))
    status = READY if not issues else BLOCKED
    receipt = LeibnizSelfOrganizationReceipt(
        status,
        calculus.digest,
        module.digest,
        source.digest,
        candidate.digest,
        deformation.digest,
        algebra_noncommutative,
        differential_leibniz_exact,
        differential_directions_commute,
        source_connection_leibniz_exact,
        candidate_connection_leibniz_exact,
        connection_difference_module_linear,
        curvature_module_linear,
        gauge_covariant,
        module_receipt.semantic_projectors_commute,
        module_receipt.protected_part_zero,
        module_receipt.authority_filtration_preserved,
        module_receipt.curvature_nonincreasing,
        module_receipt.rollback_exact,
        source_unchanged,
        deformation.candidate_only,
        False,
        False,
        tuple(issues),
        "",
    )
    return candidate, replace(receipt, receipt_digest=leibniz_receipt_digest(receipt))
