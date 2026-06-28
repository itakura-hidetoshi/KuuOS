#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_leibniz_candidate_validation_v0_71 import validate_leibniz_candidate
from runtime.kuuos_memory_family_evaluation_v0_73 import (
    BLOCKED,
    SELECTED,
    SOURCE_RETAINED,
    evaluate_memory_family,
)
from runtime.kuuos_memory_family_v0_73 import MemoryFamily, MemoryFamilyMember
from runtime.kuuos_memory_policy_v0_73 import MemoryEvaluationPolicy
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import (
    FiniteMemoryKernel,
    MemoryKernelDeformation,
    MemoryKernelTerm,
)
from scripts.check_kuuos_noncommutative_leibniz_v071 import (
    fixture as leibniz_fixture,
    square_matrix,
)
from scripts.check_kuuos_nonmarkov_memory_v072 import history_fixture


def build_family(source_kernel: FiniteMemoryKernel) -> tuple[
    MemoryFamily,
    tuple[MemoryFamilyMember, MemoryFamilyMember],
]:
    balanced_deformation = MemoryKernelDeformation(
        source_kernel.digest,
        (
            MemoryKernelTerm(
                "dt",
                1,
                square_matrix(10, {(6, 6): -0.05, (7, 7): -0.10}),
            ),
            MemoryKernelTerm(
                "dt",
                3,
                square_matrix(10, {(6, 6): 0.02, (7, 7): -0.02}),
            ),
        ),
    )
    balanced_a = MemoryFamilyMember("balanced-a", balanced_deformation)
    balanced_b = MemoryFamilyMember("balanced-b", balanced_deformation)

    high_score = MemoryFamilyMember(
        "high-score",
        MemoryKernelDeformation(
            source_kernel.digest,
            (
                MemoryKernelTerm(
                    "dt",
                    3,
                    square_matrix(10, {(6, 6): 0.50, (7, 7): -0.50}),
                ),
            ),
        ),
    )
    invalid_channel = MemoryFamilyMember(
        "invalid-channel",
        MemoryKernelDeformation(
            source_kernel.digest,
            (
                MemoryKernelTerm(
                    "dt",
                    2,
                    square_matrix(10, {(8, 6): 1.0}),
                ),
            ),
        ),
    )
    family = MemoryFamily(
        "memory-family-v073",
        source_kernel.digest,
        (balanced_b, high_score, invalid_channel, balanced_a),
    )
    return family, (balanced_a, balanced_b)


def main() -> int:
    leibniz_inputs = leibniz_fixture()
    calculus, module, _, _, gauge, algebra_samples, sections, _ = leibniz_inputs
    base_connection, base_receipt = validate_leibniz_candidate(*leibniz_inputs)
    assert base_receipt.status == "LEIBNIZ_CONNECTION_CANDIDATE_READY"

    source_capsule_digest = canonical_digest({"memory_capsule": "read-only-v073"})
    history = history_fixture(source_capsule_digest)
    history_digest_before = history.digest
    source_kernel = FiniteMemoryKernel(
        module.digest,
        history.digest,
        calculus.direction_labels,
        module.module_rank,
        (
            MemoryKernelTerm(
                "dt",
                1,
                square_matrix(10, {(6, 6): 0.10, (7, 7): 0.20}),
            ),
        ),
    )
    source_kernel_digest_before = source_kernel.digest
    family, balanced_members = build_family(source_kernel)

    selected, record = evaluate_memory_family(
        family,
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        gauge,
        algebra_samples,
        sections,
        10,
        MemoryEvaluationPolicy(require_nonincrease=True),
    )
    expected_member = min(balanced_members, key=lambda member: member.digest)
    assert record.status == SELECTED
    assert record.selected_member_id == expected_member.member_id
    assert record.selected_member_digest == expected_member.digest
    assert record.selected_kernel_digest == selected.memory_kernel.digest
    assert record.selected_connection_digest == selected.digest
    assert record.selected_score < record.source_score
    assert record.evaluated_count == 4
    assert record.accepted_count == 2
    assert record.source_history_unchanged
    assert record.source_kernel_unchanged
    assert record.candidate_only
    assert record.writes_enabled is False
    assert record.live_application_enabled is False
    assert record.permission_expansion_enabled is False
    assert record.record_digest
    assert history.digest == history_digest_before
    assert source_kernel.digest == source_kernel_digest_before

    assessments = {item.member_id: item for item in record.assessments}
    assert assessments["balanced-a"].accepted
    assert assessments["balanced-b"].accepted
    assert assessments["balanced-a"].gauge_score_invariant
    assert assessments["high-score"].accepted is False
    assert "memory_score_increased" in assessments["high-score"].issues
    assert assessments["invalid-channel"].accepted is False
    assert "memory_kernel_not_memory_supported" in assessments["invalid-channel"].issues
    assert "memory_kernel_semantic_projector_noncommuting" in assessments["invalid-channel"].issues

    strict_selected, strict_record = evaluate_memory_family(
        family,
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        gauge,
        algebra_samples,
        sections,
        10,
        MemoryEvaluationPolicy(
            require_nonincrease=True,
            require_strict_decrease=True,
        ),
    )
    assert strict_record.status == SELECTED
    assert strict_record.selected_member_id == expected_member.member_id
    assert strict_selected.digest == selected.digest

    rejected_family = MemoryFamily(
        "rejected-family-v073",
        source_kernel.digest,
        tuple(
            member
            for member in family.members
            if member.member_id in {"high-score", "invalid-channel"}
        ),
    )
    retained, retained_record = evaluate_memory_family(
        rejected_family,
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        gauge,
        algebra_samples,
        sections,
        10,
        MemoryEvaluationPolicy(require_nonincrease=True),
    )
    assert retained_record.status == SOURCE_RETAINED
    assert retained.memory_kernel.digest == source_kernel.digest
    assert retained_record.selected_member_id == ""
    assert "memory_family_has_no_accepted_member" in retained_record.issues

    wrong_source = canonical_digest({"wrong": source_kernel.digest})
    wrong_member = MemoryFamilyMember(
        "wrong-source",
        MemoryKernelDeformation(wrong_source, ()),
    )
    wrong_family = MemoryFamily("wrong-family-v073", wrong_source, (wrong_member,))
    blocked, blocked_record = evaluate_memory_family(
        wrong_family,
        module,
        calculus,
        base_connection,
        history,
        source_kernel,
        gauge,
        algebra_samples,
        sections,
        10,
        MemoryEvaluationPolicy(),
    )
    assert blocked_record.status == BLOCKED
    assert blocked.memory_kernel.digest == source_kernel.digest
    assert "memory_family_source_binding_mismatch" in blocked_record.issues

    print(json.dumps({
        "status": "KUUOS_MEMORY_EVALUATION_V0_73_VALIDATED",
        "family_digest": family.digest,
        "selected_member_id": record.selected_member_id,
        "selected_kernel_digest": record.selected_kernel_digest,
        "source_score": record.source_score,
        "selected_score": record.selected_score,
        "checks": [
            "finite-family-source-binding",
            "v0.72-admissibility-reuse",
            "gauge-invariant-memory-score",
            "deterministic-selection",
            "strict-decrease-policy",
            "source-retained-fallback",
            "fail-closed-binding-mismatch",
            "read-only-source-preservation",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
