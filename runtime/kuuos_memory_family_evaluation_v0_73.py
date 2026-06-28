#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import SignedPermutation
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    LeibnizModuleConnection,
)
from runtime.kuuos_memory_assessment_v0_73 import MemoryAssessment
from runtime.kuuos_memory_family_v0_73 import MemoryFamily, MemoryFamilyMember
from runtime.kuuos_memory_history_v0_72 import ReadOnlyMemoryHistory
from runtime.kuuos_memory_policy_v0_73 import MemoryEvaluationPolicy
from runtime.kuuos_memory_score_v0_73 import (
    changed_term_count,
    memory_return_score,
    score_is_gauge_invariant,
)
from runtime.kuuos_memory_selection_v0_73 import (
    MemorySelectionRecord,
    selection_record_digest,
)
from runtime.kuuos_module_connection_v0_70 import Matrix
from runtime.kuuos_noncommutative_differential_calculus_v0_71 import (
    InnerDifferentialCalculus,
)
from runtime.kuuos_nonmarkov_candidate_validation_v0_72 import (
    READY,
    validate_nonmarkov_candidate,
)
from runtime.kuuos_nonmarkov_memory_connection_v0_72 import NonMarkovMemoryConnection
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import FiniteMemoryKernel
from runtime.kuuos_state_module_v0_70 import KuuStateModule

SELECTED = "MEMORY_FAMILY_MEMBER_SELECTED"
SOURCE_RETAINED = "MEMORY_FAMILY_SOURCE_RETAINED"
BLOCKED = "MEMORY_FAMILY_EVALUATION_BLOCKED"


def assess_memory_member(
    member: MemoryFamilyMember,
    module: KuuStateModule,
    calculus: InnerDifferentialCalculus,
    base_connection: LeibnizModuleConnection,
    history: ReadOnlyMemoryHistory,
    source_kernel: FiniteMemoryKernel,
    gauge: SignedPermutation,
    algebra_samples: tuple[Matrix, ...],
    current_sections: tuple[FreeLeftModuleSection, ...],
    current_epoch: int,
    policy: MemoryEvaluationPolicy,
) -> tuple[NonMarkovMemoryConnection, MemoryAssessment]:
    connection, validation = validate_nonmarkov_candidate(
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        member.deformation,
        gauge,
        algebra_samples,
        current_sections,
        current_epoch,
    )
    source_score = memory_return_score(source_kernel, history.frames, current_epoch)
    evaluated_score = memory_return_score(
        connection.memory_kernel,
        history.frames,
        current_epoch,
    )
    nonincreasing = evaluated_score <= source_score + policy.tolerance
    strict_decrease = evaluated_score < source_score - policy.tolerance
    gauge_invariant = (
        score_is_gauge_invariant(source_kernel, history, current_epoch, gauge, policy.tolerance)
        and score_is_gauge_invariant(
            connection.memory_kernel,
            history,
            current_epoch,
            gauge,
            policy.tolerance,
        )
    )
    issues = list(validation.blockers)
    if policy.require_nonincrease and not nonincreasing:
        issues.append("memory_score_increased")
    if policy.require_strict_decrease and not strict_decrease:
        issues.append("memory_score_not_strictly_decreased")
    if not gauge_invariant:
        issues.append("memory_score_not_gauge_invariant")
    issues = list(dict.fromkeys(issues))
    accepted = validation.status == READY and not issues
    assessment = MemoryAssessment(
        member.member_id,
        member.digest,
        member.deformation.digest,
        connection.digest,
        source_score,
        evaluated_score,
        nonincreasing,
        strict_decrease,
        changed_term_count(source_kernel, connection.memory_kernel),
        gauge_invariant,
        accepted,
        tuple(issues),
    )
    return connection, assessment


def evaluate_memory_family(
    family: MemoryFamily,
    module: KuuStateModule,
    calculus: InnerDifferentialCalculus,
    base_connection: LeibnizModuleConnection,
    history: ReadOnlyMemoryHistory,
    source_kernel: FiniteMemoryKernel,
    gauge: SignedPermutation,
    algebra_samples: tuple[Matrix, ...],
    current_sections: tuple[FreeLeftModuleSection, ...],
    current_epoch: int,
    policy: MemoryEvaluationPolicy,
) -> tuple[NonMarkovMemoryConnection, MemorySelectionRecord]:
    source_connection = NonMarkovMemoryConnection(base_connection, source_kernel)
    source_score = memory_return_score(source_kernel, history.frames, current_epoch)
    history_digest_before = history.digest
    kernel_digest_before = source_kernel.digest
    issues: list[str] = []
    if family.source_kernel_digest != source_kernel.digest:
        issues.append("memory_family_source_binding_mismatch")

    evaluated: list[tuple[MemoryFamilyMember, NonMarkovMemoryConnection, MemoryAssessment]] = []
    if not issues:
        for member in family.members:
            connection, assessment = assess_memory_member(
                member,
                module,
                calculus,
                base_connection,
                history,
                source_kernel,
                gauge,
                algebra_samples,
                current_sections,
                current_epoch,
                policy,
            )
            evaluated.append((member, connection, assessment))

    accepted = [item for item in evaluated if item[2].accepted]
    if accepted:
        selected_member, selected_connection, selected_assessment = min(
            accepted,
            key=lambda item: (
                item[2].evaluated_score,
                item[2].changed_term_count,
                item[0].digest,
            ),
        )
        status = SELECTED
        selected_member_id = selected_member.member_id
        selected_member_digest = selected_member.digest
        selected_deformation_digest = selected_member.deformation.digest
    else:
        selected_connection = source_connection
        selected_assessment = None
        status = BLOCKED if issues else SOURCE_RETAINED
        selected_member_id = ""
        selected_member_digest = ""
        selected_deformation_digest = ""
        if not issues:
            issues.append("memory_family_has_no_accepted_member")

    source_history_unchanged = history.digest == history_digest_before
    source_kernel_unchanged = source_kernel.digest == kernel_digest_before
    if not source_history_unchanged:
        issues.append("source_memory_history_changed")
    if not source_kernel_unchanged:
        issues.append("source_memory_kernel_changed")

    record = MemorySelectionRecord(
        status,
        history.digest,
        source_kernel.digest,
        family.digest,
        selected_member_id,
        selected_member_digest,
        selected_deformation_digest,
        selected_connection.memory_kernel.digest,
        selected_connection.digest,
        source_score,
        selected_assessment.evaluated_score if selected_assessment else source_score,
        len(evaluated),
        len(accepted),
        source_history_unchanged,
        source_kernel_unchanged,
        True,
        False,
        False,
        False,
        tuple(item[2] for item in evaluated),
        tuple(dict.fromkeys(issues)),
        "",
    )
    return selected_connection, replace(record, record_digest=selection_record_digest(record))
