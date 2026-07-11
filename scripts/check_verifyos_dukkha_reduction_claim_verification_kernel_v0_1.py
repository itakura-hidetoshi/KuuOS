#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_reduction_claim_verification_kernel_v0_1 import (
    DIMENSIONS,
    STATUS_READY,
    build_verifyos_dukkha_reduction_claim_verification_certificate,
    canonical_digest,
    compute_dukkha_assessment_digest,
    compute_verifyos_dukkha_reduction_verification_bundle_digest,
)
from scripts.check_verifyos_bounded_plan_middle_way_verification_kernel_v0_1 import (
    _build as build_verifyos_v05_certificate,
)


def _source_certificate() -> dict:
    result = build_verifyos_v05_certificate()
    assert result.status == STATUS_READY, result.blockers
    assert result.certificate is not None
    return deepcopy(result.certificate)


def _dimension_record(
    dimension: str,
    before: tuple[int, int],
    after: tuple[int, int],
    *,
    avoidable: bool,
) -> dict:
    record = {
        "dimension": dimension,
        "before_interval": {"lower": before[0], "upper": before[1]},
        "after_interval": {"lower": after[0], "upper": after[1]},
        "delta_interval": {
            "lower": after[0] - before[1],
            "upper": after[1] - before[0],
        },
        "avoidable": avoidable,
        "evidence_digests": [f"evidence-{dimension}-01"],
    }
    record["dimension_record_digest"] = canonical_digest(record)
    return record


def _impact_record(subject_id: str, subject_kind: str) -> dict:
    record = {
        "subject_id": subject_id,
        "subject_kind": subject_kind,
        "delta_intervals": {
            dimension: {"lower": -800, "upper": 0}
            for dimension in DIMENSIONS
        },
        "evidence_digests": [f"impact-evidence-{subject_id}"],
    }
    record["impact_record_digest"] = canonical_digest(record)
    return record


def _assessment(source: dict) -> dict:
    assessment = {
        "source_verifyos_v05_certificate_digest": source[
            "verifyos_bounded_plan_middle_way_verification_certificate_digest"
        ],
        "source_plan_receipt_digest": source["source_plan_receipt_digest"],
        "source_concrete_plan_digest": source["source_concrete_plan_digest"],
        "reference_plan_digest": "reference-plan-hold-v01",
        "assessment_horizon": 8,
        "dimension_records": [
            _dimension_record("misfit", (7000, 8000), (5000, 6000), avoidable=True),
            _dimension_record("update_lag", (6000, 7000), (4000, 5000), avoidable=True),
            _dimension_record(
                "attachment_rigidity", (8000, 9000), (5000, 6000), avoidable=True
            ),
            _dimension_record(
                "relational_curvature", (7000, 8000), (5500, 6500), avoidable=True
            ),
            _dimension_record(
                "structural_constraint", (4000, 5000), (4000, 5000), avoidable=False
            ),
            _dimension_record(
                "uncertainty_burden", (6000, 7000), (4500, 5500), avoidable=True
            ),
        ],
        "loop_gain_before_interval": {"lower": 12000, "upper": 13000},
        "loop_gain_after_interval": {"lower": 7000, "upper": 8000},
        "revision_capacity_before_interval": {"lower": 4000, "upper": 5000},
        "revision_capacity_after_interval": {"lower": 7000, "upper": 8000},
        "protected_impact_records": [
            _impact_record("future-horizon-01", "future_subject"),
            _impact_record("minority-group-01", "protected_group"),
        ],
        "causal_assumption_digests": ["causal-assumption-01"],
        "evidence_lineage_digests": [
            "dukkha-evidence-01",
            "dukkha-evidence-02",
        ],
        "observation_integrity_preserved": True,
        "adverse_evidence_retained": True,
        "precision_collapse_not_used": True,
        "model_family_narrowing_not_used": True,
        "uncertainty_disclosed": True,
        "structural_suffering_acknowledged": True,
        "agency_preserved": True,
        "dissent_preserved": True,
        "minority_preserved": True,
        "future_burden_assessed": True,
        "causal_model_not_truth": True,
        "single_scalar_utility_forbidden": True,
    }
    assessment["dukkha_assessment_digest"] = compute_dukkha_assessment_digest(
        assessment
    )
    return assessment


def _redigest_dimension(record: dict) -> dict:
    value = deepcopy(record)
    value.pop("dimension_record_digest", None)
    value["dimension_record_digest"] = canonical_digest(value)
    return value


def _redigest_impact(record: dict) -> dict:
    value = deepcopy(record)
    value.pop("impact_record_digest", None)
    value["impact_record_digest"] = canonical_digest(value)
    return value


def _redigest_assessment(assessment: dict) -> dict:
    value = deepcopy(assessment)
    value["dukkha_assessment_digest"] = compute_dukkha_assessment_digest(value)
    return value


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(
        "verifyos_bounded_plan_middle_way_verification_certificate_digest",
        None,
    )
    value[
        "verifyos_bounded_plan_middle_way_verification_certificate_digest"
    ] = canonical_digest(value)
    return value


def _build(**overrides):
    source_override = overrides.pop("source_verifyos_certificate", None)
    source = deepcopy(_source_certificate() if source_override is None else source_override)
    assessment_override = overrides.pop("dukkha_assessment", None)
    assessment = deepcopy(
        (_assessment(source) if source else {})
        if assessment_override is None
        else assessment_override
    )
    source_digest = source.get(
        "verifyos_bounded_plan_middle_way_verification_certificate_digest",
        "source-v05-missing",
    )
    assessment_digest = assessment.get(
        "dukkha_assessment_digest", "dukkha-assessment-missing"
    )
    expected_source_digest = overrides.pop(
        "expected_source_verifyos_certificate_digest", source_digest
    )
    expected_assessment_digest = overrides.pop(
        "expected_dukkha_assessment_digest", assessment_digest
    )
    policy = overrides.pop(
        "verification_policy_digest", "verifyos-dukkha-policy-v06"
    )
    owner = overrides.pop(
        "verification_owner_responsibility_digest", "verifyos-dukkha-owner-v06"
    )
    request_id = overrides.pop(
        "verification_request_id", "verify-dukkha-v06-001"
    )
    reference_plan_digest = assessment.get(
        "reference_plan_digest", "reference-plan-missing"
    )
    bundle = overrides.pop(
        "verification_bundle_digest",
        compute_verifyos_dukkha_reduction_verification_bundle_digest(
            source_verifyos_certificate_digest=source_digest,
            expected_source_verifyos_certificate_digest=expected_source_digest,
            dukkha_assessment_digest=assessment_digest,
            expected_dukkha_assessment_digest=expected_assessment_digest,
            reference_plan_digest=reference_plan_digest,
            verification_policy_digest=policy,
            verification_owner_responsibility_digest=owner,
            verification_request_id=request_id,
        ),
    )
    args = {
        "source_verifyos_certificate": source,
        "expected_source_verifyos_certificate_digest": expected_source_digest,
        "dukkha_assessment": assessment,
        "expected_dukkha_assessment_digest": expected_assessment_digest,
        "verification_policy_digest": policy,
        "verification_owner_responsibility_digest": owner,
        "verification_request_id": request_id,
        "verification_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_verifyos_dukkha_reduction_claim_verification_certificate(**args)


def main() -> int:
    supported = _build()
    assert supported.status == STATUS_READY, supported.blockers
    assert supported.certificate is not None
    certificate = supported.certificate
    assert certificate["verifyos_version"] == "v0.6"
    assert certificate["dukkha_reduction_claim_status"] == "supported"
    assert certificate["verification_disposition"] == (
        "dukkha_reduction_supported_for_materialization_intake"
    )
    assert certificate["materialization_intake_admitted"] is True
    assert certificate["dukkha_vector_preserved"] is True
    assert certificate["single_scalar_utility_forbidden"] is True
    assert certificate["persistent_loop_gain_reduced"] is True
    assert certificate["model_revision_capacity_preserved"] is True
    assert certificate["protected_group_suffering_not_externalized"] is True
    assert certificate["future_suffering_not_externalized"] is True
    assert certificate["dukkha_minimization_authority_granted_to_verifyos"] is False
    assert certificate["execution_permission"] is False

    indeterminate_assessment = _assessment(_source_certificate())
    record = deepcopy(indeterminate_assessment["dimension_records"][0])
    record["after_interval"] = {"lower": 5500, "upper": 8500}
    record["delta_interval"] = {"lower": -2500, "upper": 1500}
    indeterminate_assessment["dimension_records"][0] = _redigest_dimension(record)
    indeterminate_assessment = _redigest_assessment(indeterminate_assessment)
    indeterminate = _build(dukkha_assessment=indeterminate_assessment)
    assert indeterminate.status == STATUS_READY, indeterminate.blockers
    assert indeterminate.certificate is not None
    assert indeterminate.certificate["dukkha_reduction_claim_status"] == (
        "indeterminate"
    )
    assert indeterminate.certificate["additional_evidence_required"] is True
    assert indeterminate.certificate["materialization_intake_admitted"] is False

    contradicted_assessment = _assessment(_source_certificate())
    impact = deepcopy(contradicted_assessment["protected_impact_records"][1])
    impact["delta_intervals"]["relational_curvature"] = {
        "lower": 100,
        "upper": 500,
    }
    contradicted_assessment["protected_impact_records"][1] = _redigest_impact(
        impact
    )
    contradicted_assessment = _redigest_assessment(contradicted_assessment)
    contradicted = _build(dukkha_assessment=contradicted_assessment)
    assert contradicted.status == STATUS_READY, contradicted.blockers
    assert contradicted.certificate is not None
    assert contradicted.certificate["dukkha_reduction_claim_status"] == (
        "contradicted"
    )
    assert contradicted.certificate["plan_revision_required"] is True
    assert contradicted.certificate["materialization_intake_admitted"] is False

    integrity_failed = _assessment(_source_certificate())
    integrity_failed["observation_integrity_preserved"] = False
    integrity_failed = _redigest_assessment(integrity_failed)
    integrity_result = _build(dukkha_assessment=integrity_failed)
    assert integrity_result.status == STATUS_READY, integrity_result.blockers
    assert integrity_result.certificate is not None
    assert integrity_result.certificate["dukkha_reduction_claim_status"] == (
        "contradicted"
    )

    promoted_source = _source_certificate()
    promoted_source["execution_permission"] = True
    promoted_source = _redigest_source(promoted_source)

    malformed_dimension = _assessment(_source_certificate())
    malformed_dimension["dimension_records"][0]["delta_interval"] = {
        "lower": 0,
        "upper": 0,
    }
    malformed_dimension["dimension_records"][0] = _redigest_dimension(
        malformed_dimension["dimension_records"][0]
    )
    malformed_dimension = _redigest_assessment(malformed_dimension)

    missing_future = _assessment(_source_certificate())
    missing_future["protected_impact_records"] = [
        missing_future["protected_impact_records"][1]
    ]
    missing_future = _redigest_assessment(missing_future)

    blocked = [
        _build(source_verifyos_certificate={}),
        _build(expected_source_verifyos_certificate_digest="wrong"),
        _build(expected_dukkha_assessment_digest="wrong"),
        _build(verification_bundle_digest="wrong"),
        _build(source_verifyos_certificate=promoted_source),
        _build(dukkha_assessment=malformed_dimension),
        _build(dukkha_assessment=missing_future),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.certificate is None

    print("PASS: VerifyOS Dukkha Reduction Claim Verification Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
