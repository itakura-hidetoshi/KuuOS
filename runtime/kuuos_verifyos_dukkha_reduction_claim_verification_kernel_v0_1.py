#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
DIMENSIONS = (
    "misfit",
    "update_lag",
    "attachment_rigidity",
    "relational_curvature",
    "structural_constraint",
    "uncertainty_burden",
)
AVOIDABLE_DIMENSIONS = frozenset(set(DIMENSIONS) - {"structural_constraint"})
INTERVAL_FIELDS = {"lower", "upper"}
ASSESSMENT_FLAGS = (
    "observation_integrity_preserved",
    "adverse_evidence_retained",
    "precision_collapse_not_used",
    "model_family_narrowing_not_used",
    "uncertainty_disclosed",
    "structural_suffering_acknowledged",
    "agency_preserved",
    "dissent_preserved",
    "minority_preserved",
    "future_burden_assessed",
    "causal_model_not_truth",
    "single_scalar_utility_forbidden",
)
ASSESSMENT_FIELDS = {
    "source_verifyos_v05_certificate_digest",
    "source_plan_receipt_digest",
    "source_concrete_plan_digest",
    "reference_plan_digest",
    "assessment_horizon",
    "dimension_records",
    "loop_gain_before_interval",
    "loop_gain_after_interval",
    "revision_capacity_before_interval",
    "revision_capacity_after_interval",
    "protected_impact_records",
    "causal_assumption_digests",
    "evidence_lineage_digests",
    *ASSESSMENT_FLAGS,
    "dukkha_assessment_digest",
}
DIMENSION_FIELDS = {
    "dimension",
    "before_interval",
    "after_interval",
    "delta_interval",
    "avoidable",
    "evidence_digests",
    "dimension_record_digest",
}
IMPACT_FIELDS = {
    "subject_id",
    "subject_kind",
    "delta_intervals",
    "evidence_digests",
    "impact_record_digest",
}


@dataclass
class VerifyOSDukkhaReductionClaimVerificationResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def compute_dukkha_assessment_digest(assessment: Mapping[str, Any]) -> str:
    unsigned = dict(assessment)
    unsigned.pop("dukkha_assessment_digest", None)
    return canonical_digest(unsigned)


def compute_verifyos_dukkha_reduction_verification_bundle_digest(
    **fields: Any,
) -> str:
    return canonical_digest(fields)


def _string_list(value: Any, *, allow_empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _interval(
    value: Any,
    *,
    minimum: int,
    maximum: int,
) -> tuple[bool, dict[str, int]]:
    if not isinstance(value, Mapping) or set(value) != INTERVAL_FIELDS:
        return False, {}
    lower = value.get("lower")
    upper = value.get("upper")
    if (
        not isinstance(lower, int)
        or isinstance(lower, bool)
        or not isinstance(upper, int)
        or isinstance(upper, bool)
        or lower < minimum
        or upper > maximum
        or lower > upper
    ):
        return False, {}
    return True, {"lower": lower, "upper": upper}


def _expected_delta(before: Mapping[str, int], after: Mapping[str, int]) -> dict:
    return {
        "lower": after["lower"] - before["upper"],
        "upper": after["upper"] - before["lower"],
    }


def _verify_source(
    source: dict,
    expected_digest: str,
    blockers: list[str],
) -> tuple[str, list[str], list[str]]:
    if not source:
        blockers.append("source_verifyos_certificate_missing")
        return "", [], []
    expected_headers = {
        "kernel": "VerifyOS Bounded Plan Middle-Way Verification Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.5",
        "status": "VERIFYOS_BOUNDED_PLAN_MIDDLE_WAY_VERIFIED",
        "conditional_validity_status": "valid",
        "verification_disposition": (
            "bounded_plan_verified_for_materialization_intake"
        ),
    }
    for field, expected in expected_headers.items():
        if source.get(field) != expected:
            blockers.append(f"source_{field}_invalid")
    digest_field = (
        "verifyos_bounded_plan_middle_way_verification_certificate_digest"
    )
    digest = source.get(digest_field)
    if not isinstance(digest, str) or not digest:
        blockers.append("source_verifyos_certificate_digest_missing")
        digest = ""
    else:
        unsigned = dict(source)
        unsigned.pop(digest_field, None)
        if digest != canonical_digest(unsigned):
            blockers.append("source_verifyos_certificate_digest_mismatch")
        if digest != expected_digest:
            blockers.append("source_verifyos_certificate_expected_binding_mismatch")
    required_true = (
        "world_conditions_current",
        "bounded_plan_verified_for_materialization_intake",
        "materialization_intake_admitted",
        "structural_verification_passed",
        "source_receipt_digest_verified",
        "finite_plan_verified",
        "checkpoint_order_verified",
        "stop_conditions_verified",
        "forbidden_effects_absent",
        "selected_candidate_preserved",
        "plan_intent_preserved",
        "alternative_candidates_preserved",
        "dissent_evidence_preserved",
        "minority_evidence_preserved",
        "source_lineage_preserved",
        "source_responsibility_preserved",
        "plan_remains_conditionally_binding",
        "plan_not_reified",
        "plan_not_erased",
        "selection_remains_decisionos_owned",
        "persistent_world_state_unchanged",
        "world_model_prediction_not_truth",
        "world_mutation_not_granted",
        "history_read_only",
        "qi_grants_no_authority",
        "future_only",
    )
    required_false = (
        "plan_revision_required",
        "selection_authority_granted_to_verifyos",
        "plan_revision_authority_granted_to_verifyos",
        "plan_activated",
        "materialization_performed",
        "execution_authority_granted",
        "execution_permission",
        "active_now",
    )
    for field in required_true:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in required_false:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    lineage_ok, lineage = _string_list(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _string_list(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, lineage, responsibility


def _verify_dimensions(
    raw_records: Any,
    blockers: list[str],
) -> dict[str, dict[str, dict[str, int]]]:
    normalized: dict[str, dict[str, dict[str, int]]] = {}
    if not isinstance(raw_records, list) or len(raw_records) != len(DIMENSIONS):
        blockers.append("dimension_records_invalid")
        return normalized
    names = [
        record.get("dimension") if isinstance(record, Mapping) else None
        for record in raw_records
    ]
    if tuple(names) != DIMENSIONS:
        blockers.append("dimension_records_not_canonical")
    for index, raw in enumerate(raw_records):
        if not isinstance(raw, Mapping) or set(raw) != DIMENSION_FIELDS:
            blockers.append(f"dimension_record_schema_invalid_{index}")
            continue
        record = dict(raw)
        name = record.get("dimension")
        if name not in DIMENSIONS:
            blockers.append(f"dimension_invalid_{index}")
            continue
        if record.get("avoidable") is not (name in AVOIDABLE_DIMENSIONS):
            blockers.append(f"dimension_avoidable_flag_invalid_{name}")
        before_ok, before = _interval(
            record.get("before_interval"), minimum=0, maximum=10000
        )
        after_ok, after = _interval(
            record.get("after_interval"), minimum=0, maximum=10000
        )
        delta_ok, delta = _interval(
            record.get("delta_interval"), minimum=-10000, maximum=10000
        )
        if not before_ok:
            blockers.append(f"dimension_before_interval_invalid_{name}")
        if not after_ok:
            blockers.append(f"dimension_after_interval_invalid_{name}")
        if not delta_ok:
            blockers.append(f"dimension_delta_interval_invalid_{name}")
        if before_ok and after_ok and delta_ok and delta != _expected_delta(before, after):
            blockers.append(f"dimension_delta_interval_mismatch_{name}")
        evidence_ok, _ = _string_list(record.get("evidence_digests"))
        if not evidence_ok:
            blockers.append(f"dimension_evidence_invalid_{name}")
        supplied_digest = record.get("dimension_record_digest")
        unsigned = dict(record)
        unsigned.pop("dimension_record_digest", None)
        if supplied_digest != canonical_digest(unsigned):
            blockers.append(f"dimension_record_digest_mismatch_{name}")
        normalized[name] = {"before": before, "after": after, "delta": delta}
    return normalized


def _verify_impacts(raw_records: Any, blockers: list[str]) -> list[dict]:
    normalized: list[dict] = []
    if not isinstance(raw_records, list) or len(raw_records) < 2:
        blockers.append("protected_impact_records_invalid")
        return normalized
    keys: list[tuple[str, str]] = []
    for index, raw in enumerate(raw_records):
        if not isinstance(raw, Mapping) or set(raw) != IMPACT_FIELDS:
            blockers.append(f"impact_record_schema_invalid_{index}")
            continue
        record = dict(raw)
        subject_id = record.get("subject_id")
        subject_kind = record.get("subject_kind")
        if not isinstance(subject_id, str) or not subject_id:
            blockers.append(f"impact_subject_id_invalid_{index}")
        if subject_kind not in {"protected_group", "future_subject"}:
            blockers.append(f"impact_subject_kind_invalid_{index}")
        keys.append((str(subject_kind), str(subject_id)))
        raw_deltas = record.get("delta_intervals")
        deltas: dict[str, dict[str, int]] = {}
        if not isinstance(raw_deltas, Mapping) or set(raw_deltas) != set(DIMENSIONS):
            blockers.append(f"impact_delta_schema_invalid_{index}")
        else:
            for dimension in DIMENSIONS:
                valid, interval = _interval(
                    raw_deltas.get(dimension), minimum=-10000, maximum=10000
                )
                if not valid:
                    blockers.append(
                        f"impact_delta_interval_invalid_{index}_{dimension}"
                    )
                deltas[dimension] = interval
        evidence_ok, _ = _string_list(record.get("evidence_digests"))
        if not evidence_ok:
            blockers.append(f"impact_evidence_invalid_{index}")
        supplied_digest = record.get("impact_record_digest")
        unsigned = dict(record)
        unsigned.pop("impact_record_digest", None)
        if supplied_digest != canonical_digest(unsigned):
            blockers.append(f"impact_record_digest_mismatch_{index}")
        normalized.append(
            {"subject_id": subject_id, "subject_kind": subject_kind, "deltas": deltas}
        )
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        blockers.append("impact_records_not_canonical")
    if not any(kind == "protected_group" for kind, _ in keys):
        blockers.append("protected_group_impact_missing")
    if not any(kind == "future_subject" for kind, _ in keys):
        blockers.append("future_subject_impact_missing")
    return normalized


def build_verifyos_dukkha_reduction_claim_verification_certificate(
    *,
    source_verifyos_certificate: Mapping[str, Any],
    expected_source_verifyos_certificate_digest: str,
    dukkha_assessment: Mapping[str, Any],
    expected_dukkha_assessment_digest: str,
    verification_policy_digest: str,
    verification_owner_responsibility_digest: str,
    verification_request_id: str,
    verification_bundle_digest: str,
) -> VerifyOSDukkhaReductionClaimVerificationResult:
    blockers: list[str] = []
    source = dict(source_verifyos_certificate) if isinstance(source_verifyos_certificate, Mapping) else {}
    assessment = dict(dukkha_assessment) if isinstance(dukkha_assessment, Mapping) else {}
    for name, value in {
        "expected_source_verifyos_certificate_digest": expected_source_verifyos_certificate_digest,
        "expected_dukkha_assessment_digest": expected_dukkha_assessment_digest,
        "verification_policy_digest": verification_policy_digest,
        "verification_owner_responsibility_digest": verification_owner_responsibility_digest,
        "verification_request_id": verification_request_id,
        "verification_bundle_digest": verification_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    source_digest, source_lineage, source_responsibility = _verify_source(
        source, expected_source_verifyos_certificate_digest, blockers
    )
    if not assessment:
        blockers.append("dukkha_assessment_missing")
    elif set(assessment) != ASSESSMENT_FIELDS:
        blockers.append("dukkha_assessment_schema_invalid")
    assessment_digest = assessment.get("dukkha_assessment_digest", "")
    if not assessment_digest:
        blockers.append("dukkha_assessment_digest_missing")
    else:
        if assessment_digest != compute_dukkha_assessment_digest(assessment):
            blockers.append("dukkha_assessment_digest_mismatch")
        if assessment_digest != expected_dukkha_assessment_digest:
            blockers.append("dukkha_assessment_expected_binding_mismatch")
    if assessment.get("source_verifyos_v05_certificate_digest") != source_digest:
        blockers.append("assessment_source_verifyos_binding_mismatch")
    if source:
        if assessment.get("source_plan_receipt_digest") != source.get("source_plan_receipt_digest"):
            blockers.append("assessment_source_plan_receipt_binding_mismatch")
        if assessment.get("source_concrete_plan_digest") != source.get("source_concrete_plan_digest"):
            blockers.append("assessment_source_concrete_plan_binding_mismatch")
    reference_plan_digest = assessment.get("reference_plan_digest")
    if not isinstance(reference_plan_digest, str) or not reference_plan_digest:
        blockers.append("reference_plan_digest_missing")
    horizon = assessment.get("assessment_horizon")
    if not isinstance(horizon, int) or isinstance(horizon, bool) or not 1 <= horizon <= 64:
        blockers.append("assessment_horizon_invalid")
    dimensions = _verify_dimensions(assessment.get("dimension_records"), blockers)
    loop_before_ok, loop_before = _interval(
        assessment.get("loop_gain_before_interval"), minimum=0, maximum=20000
    )
    loop_after_ok, loop_after = _interval(
        assessment.get("loop_gain_after_interval"), minimum=0, maximum=20000
    )
    revision_before_ok, revision_before = _interval(
        assessment.get("revision_capacity_before_interval"), minimum=0, maximum=10000
    )
    revision_after_ok, revision_after = _interval(
        assessment.get("revision_capacity_after_interval"), minimum=0, maximum=10000
    )
    for name, valid in (
        ("loop_gain_before_interval", loop_before_ok),
        ("loop_gain_after_interval", loop_after_ok),
        ("revision_capacity_before_interval", revision_before_ok),
        ("revision_capacity_after_interval", revision_after_ok),
    ):
        if not valid:
            blockers.append(f"{name}_invalid")
    impacts = _verify_impacts(assessment.get("protected_impact_records"), blockers)
    for field in ("causal_assumption_digests", "evidence_lineage_digests"):
        valid, _ = _string_list(assessment.get(field))
        if not valid:
            blockers.append(f"{field}_invalid")
    flags_true = all(assessment.get(field) is True for field in ASSESSMENT_FLAGS)
    if not blockers:
        expected_bundle = compute_verifyos_dukkha_reduction_verification_bundle_digest(
            source_verifyos_certificate_digest=source_digest,
            expected_source_verifyos_certificate_digest=expected_source_verifyos_certificate_digest,
            dukkha_assessment_digest=assessment_digest,
            expected_dukkha_assessment_digest=expected_dukkha_assessment_digest,
            reference_plan_digest=reference_plan_digest,
            verification_policy_digest=verification_policy_digest,
            verification_owner_responsibility_digest=verification_owner_responsibility_digest,
            verification_request_id=verification_request_id,
        )
        if verification_bundle_digest != expected_bundle:
            blockers.append("verification_bundle_digest_mismatch")
    if blockers:
        return VerifyOSDukkhaReductionClaimVerificationResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )
    avoidable_deltas = [dimensions[name]["delta"] for name in DIMENSIONS if name in AVOIDABLE_DIMENSIONS]
    dimension_definite_worsening = any(item["lower"] > 0 for item in avoidable_deltas)
    dimension_nonworsening = all(item["upper"] <= 0 for item in avoidable_deltas)
    strict_improvement = any(item["upper"] < 0 for item in avoidable_deltas)
    impact_intervals = [
        interval
        for impact in impacts
        for interval in impact["deltas"].values()
    ]
    impact_definite_worsening = any(item["lower"] > 0 for item in impact_intervals)
    impact_nonworsening = all(item["upper"] <= 0 for item in impact_intervals)
    loop_definite_worsening = (
        loop_after["lower"] >= loop_before["upper"]
        or loop_after["lower"] >= 10000
    )
    loop_reduced = (
        loop_after["upper"] < loop_before["lower"]
        and loop_after["upper"] < 10000
    )
    revision_definite_loss = revision_after["upper"] < revision_before["lower"]
    revision_preserved = revision_after["lower"] >= revision_before["upper"]
    contradicted = (
        not flags_true
        or dimension_definite_worsening
        or impact_definite_worsening
        or loop_definite_worsening
        or revision_definite_loss
    )
    supported = (
        not contradicted
        and dimension_nonworsening
        and strict_improvement
        and impact_nonworsening
        and loop_reduced
        and revision_preserved
    )
    claim_status = "supported" if supported else "contradicted" if contradicted else "indeterminate"
    disposition = {
        "supported": "dukkha_reduction_supported_for_materialization_intake",
        "indeterminate": "additional_evidence_required",
        "contradicted": "return_to_planos_revision",
    }[claim_status]
    admitted = claim_status == "supported"
    record = {
        "source_verifyos_certificate_digest": source_digest,
        "dukkha_assessment_digest": assessment_digest,
        "reference_plan_digest": reference_plan_digest,
        "dukkha_reduction_claim_status": claim_status,
        "verification_disposition": disposition,
        "materialization_intake_admitted": admitted,
        "avoidable_dukkha_robust_nonworsening": dimension_nonworsening,
        "persistent_loop_gain_robustly_reduced": loop_reduced,
        "revision_capacity_robustly_preserved": revision_preserved,
        "protected_impacts_robustly_nonworsening": impact_nonworsening,
    }
    record_digest = canonical_digest(record)
    resulting_lineage = sorted(
        set(source_lineage)
        | {source_digest, assessment_digest, record_digest, verification_bundle_digest}
    )
    resulting_responsibility = sorted(
        set(source_responsibility) | {verification_owner_responsibility_digest}
    )
    protected_ok = all(
        item["upper"] <= 0
        for impact in impacts
        if impact["subject_kind"] == "protected_group"
        for item in impact["deltas"].values()
    )
    future_ok = all(
        item["upper"] <= 0
        for impact in impacts
        if impact["subject_kind"] == "future_subject"
        for item in impact["deltas"].values()
    )
    certificate = {
        "kernel": "VerifyOS Dukkha Reduction Claim Verification Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.6",
        "status": "VERIFYOS_DUKKHA_REDUCTION_CLAIM_VERIFIED",
        "source_verifyos_v05_certificate_digest": source_digest,
        "source_plan_receipt_digest": source["source_plan_receipt_digest"],
        "source_concrete_plan_digest": source["source_concrete_plan_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "reference_plan_digest": reference_plan_digest,
        "dukkha_assessment_digest": assessment_digest,
        "assessment_horizon": horizon,
        "verification_policy_digest": verification_policy_digest,
        "verification_owner_responsibility_digest": verification_owner_responsibility_digest,
        "verification_request_id": verification_request_id,
        "verification_bundle_digest": verification_bundle_digest,
        "verification_record": record,
        "verification_record_digest": record_digest,
        "dukkha_reduction_claim_status": claim_status,
        "verification_disposition": disposition,
        "materialization_intake_admitted": admitted,
        "additional_evidence_required": claim_status == "indeterminate",
        "plan_revision_required": claim_status == "contradicted",
        "dukkha_vector_preserved": True,
        "single_scalar_utility_forbidden": True,
        **{field: assessment[field] for field in ASSESSMENT_FLAGS},
        "avoidable_dukkha_nonworsening_supported": dimension_nonworsening,
        "at_least_one_avoidable_dimension_improved": strict_improvement,
        "attachment_rigidity_not_increased": dimensions["attachment_rigidity"]["delta"]["upper"] <= 0,
        "relational_curvature_not_hidden": dimensions["relational_curvature"]["delta"]["upper"] <= 0,
        "persistent_loop_gain_reduced": loop_reduced,
        "model_revision_capacity_preserved": revision_preserved,
        "protected_group_suffering_not_externalized": protected_ok,
        "future_suffering_not_externalized": future_ok,
        "source_plan_preserved": True,
        "source_lineage_preserved": True,
        "source_responsibility_preserved": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_verifyos": False,
        "plan_revision_authority_granted_to_verifyos": False,
        "dukkha_minimization_authority_granted_to_verifyos": False,
        "plan_activated": False,
        "materialization_performed": False,
        "execution_authority_granted": False,
        "execution_permission": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    certificate["verifyos_dukkha_reduction_claim_verification_certificate_digest"] = canonical_digest(certificate)
    return VerifyOSDukkhaReductionClaimVerificationResult(STATUS_READY, [], certificate)
