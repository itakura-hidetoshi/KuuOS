#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from runtime.kuuos_observeos_dukkha_preserving_external_host_effect_observation_intake_v0_1 import (
    EVIDENCE_DIGEST_FIELD, RECEIPT_DIGEST_FIELD as SOURCE_DIGEST_FIELD,
    canonical_digest, compute_independent_observation_evidence_packet_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
RECEIPT_DIGEST_FIELD = "verifyos_dukkha_preserving_observed_host_effect_verification_intake_receipt_digest"
REVIEW_DIGEST_FIELD = "effect_verification_review_certificate_digest"
STATE_BEFORE, STATE_AFTER_VERIFIED = "host_effect_observed_unverified", "host_effect_verified_world_not_updated"
DISPOSITION_SUPPORTED = "effect_verification_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "verification_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "verification_review_refresh_required"
DISPOSITION_ADDITIONAL_OBSERVATION = "additional_observation_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_EFFECT_CONTRACT_REPAIR = "effect_contract_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_DUKKHA_CONTRADICTED = "dukkha_preservation_contradicted"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

SOURCE_TRUE = (
    "source_host_effect_receipt_supplied", "source_host_effect_receipt_fully_revalidated",
    "independent_observation_evidence_bound", "collector_identity_bound", "evidence_source_identity_bound",
    "collection_epoch_freshness_confirmed", "raw_artifact_digest_bound", "observed_value_digest_bound",
    "uncertainty_digest_bound", "calibration_digest_bound", "context_digest_bound", "tamper_evidence_digest_bound",
    "provenance_chain_preserved", "host_effect_observation_identity_exact", "exactly_one_observation_receipt_issued",
    "observation_performed", "independent_world_evidence_present", "observation_debt_consumed",
    "observation_debt_replay_closed", "observation_evidence_packet_replay_closed", "observation_intake_nonce_consumed",
    "observation_intake_nonce_replay_closed", "source_host_effect_receipt_replay_closed", "world_conditions_current",
    "observation_collection_duration_current", "observation_intake_delay_current", "collector_independent_from_host_driver",
    "evidence_source_independent_from_host_receipt", "persistent_world_model_state_unchanged",
    "verification_intake_required", "verification_intake_admitted", "verification_receipt_required", "verification_debt_open",
    "compensation_route_ready", "effect_scope_preserved", "effect_ceiling_preserved", "checkpoint_guards_preserved",
    "stop_conditions_preserved", "evidence_lineage_preserved", "responsibility_lineage_preserved",
    "alternative_candidates_preserved", "dissent_preserved", "minority_preserved", "dukkha_reduction_support_preserved",
    "protected_group_nonexternalization_preserved", "future_nonexternalization_preserved", "revision_capacity_preserved",
    "persistent_loop_reduction_preserved", "single_scalar_utility_not_introduced", "selection_remains_decisionos_owned",
    "world_model_prediction_not_truth", "history_read_only", "qi_grants_no_authority", "future_only",
)
SOURCE_FALSE = (
    "observation_double_consumed", "host_receipt_used_as_independent_evidence", "host_operation_reexecuted",
    "tool_invocation_performed", "external_side_effect_performed", "persistent_host_state_changed_by_observation",
    "world_fact_confirmed", "causal_attribution_confirmed", "verification_completed", "compensation_performed",
    "automatic_truth_promotion", "automatic_plan_completion", "automatic_rollback", "automatic_compensation",
    "selection_authority_granted_to_observeos", "plan_revision_authority_granted_to_observeos",
    "dukkha_minimization_authority_granted_to_observeos", "general_execution_authority_granted",
    "execution_permission", "world_mutation_authority_granted", "active_now",
)
REVIEW_FIELDS = {
    "source_observation_receipt_digest", "observation_record_digest", "verification_handoff_envelope_digest",
    EVIDENCE_DIGEST_FIELD, "frontier_materialization_candidate_id", "frontier_adapter_id", "frontier_binding_digest",
    "requested_effect_tags", "observed_value_digest", "uncertainty_digest", "calibration_digest",
    "provenance_chain_digests", "expected_effect_contract_digest", "verification_method_digest",
    "verification_evidence_digest", "dukkha_impact_assessment_digest", "protected_group_impact_assessment_digest",
    "future_subject_impact_assessment_digest", "verifier_id", "verification_started_epoch",
    "verification_completed_epoch", "maximum_verification_duration", "effect_identity_match", "evidence_sufficient",
    "uncertainty_acceptable", "calibration_sufficient", "provenance_complete", "effect_scope_conformant",
    "effect_ceiling_not_exceeded", "checkpoint_guards_satisfied", "stop_conditions_satisfied",
    "dukkha_preservation_supported", "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported", "world_fact_claimed", "causal_attribution_claimed", REVIEW_DIGEST_FIELD,
}
CONTEXT_FIELDS = {
    "source_observation_receipt_digest", REVIEW_DIGEST_FIELD, "current_world_binding_digest",
    "current_world_model_state_digest", "current_world_model_revision", "current_world_lineage_digest",
    "source_observation_receipt_observed_epoch", "verification_intake_epoch", "maximum_verification_intake_delay",
    "verification_intake_session_id", "verification_intake_nonce_digest", "prior_verification_intake_session_ids",
    "prior_verification_review_certificate_digests", "prior_verification_intake_nonce_digests",
    "prior_verified_source_observation_receipt_digests", "requested_verification_operation_digest",
    "exact_verification_cycle_digest", "verification_intake_context_digest",
}

@dataclass
class VerifyOSDukkhaPreservingObservedHostEffectVerificationResult:
    status: str
    blockers: list[str]
    receipt: dict | None

def _map(v: Any) -> dict: return dict(v) if isinstance(v, Mapping) else {}
def _digest_without(v: Mapping[str, Any], field: str) -> str:
    x = dict(v); x.pop(field, None); return canonical_digest(x)
def compute_effect_verification_review_certificate_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, REVIEW_DIGEST_FIELD)
def compute_verification_intake_context_digest(v: Mapping[str, Any]) -> str:
    return _digest_without(v, "verification_intake_context_digest")
def compute_observed_host_effect_verification_bundle_digest(**fields: Any) -> str: return canonical_digest(fields)
def _strings(v: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(v, list) and (allow_empty or bool(v)) and all(isinstance(x, str) and x for x in v)
    return (ok and v == sorted(v) and len(v) == len(set(v))), list(v) if isinstance(v, list) else []
def _exact(actual: Mapping[str, Any], expected: Mapping[str, Any], prefix: str, blockers: list[str]) -> None:
    blockers.extend(f"{prefix}_{k}_mismatch" for k, v in expected.items() if actual.get(k) != v)

def compute_requested_verification_operation_digest(source: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_observation_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "observation_record_digest": source.get("observation_record_digest"),
        "verification_handoff_envelope_digest": source.get("verification_handoff_envelope_digest"),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "state_before": STATE_BEFORE, "supported_state_after": STATE_AFTER_VERIFIED,
    })
def compute_exact_verification_cycle_digest(source: Mapping[str, Any], review: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_observation_receipt_digest": source.get(SOURCE_DIGEST_FIELD), REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "verification_intake_session_id": context.get("verification_intake_session_id"),
        "verification_intake_nonce_digest": context.get("verification_intake_nonce_digest"),
        "verification_intake_epoch": context.get("verification_intake_epoch"),
        "current_world_model_revision": context.get("current_world_model_revision"),
        "requested_verification_operation_digest": context.get("requested_verification_operation_digest"),
    })

def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_observation_receipt_missing"); return "", {}, {}, [], []
    _exact(source, {
        "kernel": "ObserveOS Dukkha-Preserving External Host-Effect Observation Intake Kernel",
        "kernel_version": "v0.1", "observeos_version": "v0.5",
        "status": "OBSERVEOS_DUKKHA_PRESERVING_EXTERNAL_HOST_EFFECT_OBSERVED",
        "observation_state_after": STATE_BEFORE,
    }, "source", blockers)
    digest = source.get(SOURCE_DIGEST_FIELD, "")
    if not digest: blockers.append("source_observation_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_DIGEST_FIELD): blockers.append("source_observation_receipt_digest_mismatch")
    if digest != expected: blockers.append("source_observation_expected_binding_mismatch")
    for f in SOURCE_TRUE:
        if source.get(f) is not True: blockers.append(f"source_boundary_{f}_missing")
    for f in SOURCE_FALSE:
        if source.get(f) is not False: blockers.append(f"source_boundary_{f}_promoted")
    evidence, record = _map(source.get("independent_observation_evidence_packet")), _map(source.get("observation_record"))
    debt, handoff = _map(source.get("observation_debt_consumption_record")), _map(source.get("verification_handoff_envelope"))
    if not evidence: blockers.append("source_independent_observation_evidence_invalid")
    elif source.get(EVIDENCE_DIGEST_FIELD) != compute_independent_observation_evidence_packet_digest(evidence):
        blockers.append("source_independent_observation_evidence_digest_mismatch")
    for name, item, field in (
        ("observation_record", record, "observation_record_digest"),
        ("observation_debt_consumption_record", debt, "observation_debt_consumption_record_digest"),
        ("verification_handoff_envelope", handoff, "verification_handoff_envelope_digest"),
    ):
        if not item: blockers.append(f"source_{name}_invalid")
        elif source.get(field) != canonical_digest(item): blockers.append(f"source_{name}_digest_mismatch")
    _exact(record, {
        "source_host_effect_receipt_digest": source.get("source_host_effect_receipt_digest"),
        "external_host_effect_record_digest": source.get("source_external_host_effect_record_digest"),
        "observation_handoff_envelope_digest": source.get("source_observation_handoff_envelope_digest"),
        EVIDENCE_DIGEST_FIELD: source.get(EVIDENCE_DIGEST_FIELD),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "state_before": "host_effect_recorded_unobserved", "state_after": STATE_BEFORE,
        "intake_outcome": "host_effect_observed_pending_verification",
    }, "source_observation_record", blockers)
    if debt.get("observation_debt_consumed") is not True: blockers.append("source_observation_debt_not_consumed")
    if debt.get("source_host_effect_receipt_marked_observed") is not True: blockers.append("source_host_effect_receipt_not_marked_observed")
    if debt.get("double_observation_performed") is not False: blockers.append("source_observation_double_consumption_promoted")
    _exact(handoff, {
        "source_host_effect_receipt_digest": source.get("source_host_effect_receipt_digest"),
        "external_host_effect_record_digest": source.get("source_external_host_effect_record_digest"),
        EVIDENCE_DIGEST_FIELD: source.get(EVIDENCE_DIGEST_FIELD), "observation_record_digest": source.get("observation_record_digest"),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "host_effect_state": "observed_unverified", "observation_state": "observed",
        "verification_state": "verification_debt_open", "verification_intake_admitted": True,
        "verification_receipt_required": True, "world_fact_confirmed": False,
        "causal_attribution_confirmed": False, "compensation_route_ready": True,
    }, "source_verification_handoff", blockers)
    req_ok, requested = _strings(handoff.get("requested_effect_tags"), True)
    prov_ok, provenance = _strings(handoff.get("provenance_chain_digests"))
    ev_prov_ok, ev_prov = _strings(evidence.get("provenance_chain_digests"))
    if not req_ok: blockers.append("source_requested_effect_tags_invalid")
    if not prov_ok: blockers.append("source_verification_provenance_invalid")
    if not ev_prov_ok: blockers.append("source_evidence_provenance_invalid")
    elif ev_prov != provenance: blockers.append("source_verification_provenance_binding_mismatch")
    _exact(handoff, {
        "observed_value_digest": evidence.get("observed_value_digest"),
        "uncertainty_digest": evidence.get("uncertainty_digest"),
        "calibration_digest": evidence.get("calibration_digest"), "requested_effect_tags": requested,
    }, "source_verification_handoff", blockers)
    lin_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    rsp_ok, responsibility = _strings(source.get("resulting_responsibility_lineage_digests"))
    if not lin_ok: blockers.append("source_resulting_lineage_invalid")
    if not rsp_ok: blockers.append("source_resulting_responsibility_invalid")
    return digest, evidence, handoff, lineage, responsibility

def _verify_review(review: dict, expected: str, source: dict, evidence: dict, handoff: dict, blockers: list[str]):
    if not review:
        blockers.append("effect_verification_review_certificate_missing"); return "", False
    if set(review) != REVIEW_FIELDS: blockers.append("effect_verification_review_certificate_schema_invalid")
    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest: blockers.append("effect_verification_review_certificate_digest_missing")
    elif digest != compute_effect_verification_review_certificate_digest(review): blockers.append("effect_verification_review_certificate_digest_mismatch")
    if digest != expected: blockers.append("effect_verification_review_expected_binding_mismatch")
    _exact(review, {
        "source_observation_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "observation_record_digest": source.get("observation_record_digest"),
        "verification_handoff_envelope_digest": source.get("verification_handoff_envelope_digest"),
        EVIDENCE_DIGEST_FIELD: source.get(EVIDENCE_DIGEST_FIELD),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "requested_effect_tags": handoff.get("requested_effect_tags"), "observed_value_digest": handoff.get("observed_value_digest"),
        "uncertainty_digest": handoff.get("uncertainty_digest"), "calibration_digest": handoff.get("calibration_digest"),
        "provenance_chain_digests": handoff.get("provenance_chain_digests"), "world_fact_claimed": False,
        "causal_attribution_claimed": False,
    }, "effect_verification_review", blockers)
    for f in ("expected_effect_contract_digest", "verification_method_digest", "verification_evidence_digest",
              "dukkha_impact_assessment_digest", "protected_group_impact_assessment_digest",
              "future_subject_impact_assessment_digest", "verifier_id"):
        if not isinstance(review.get(f), str) or not review.get(f): blockers.append(f"effect_verification_review_{f}_invalid")
    bools = ("effect_identity_match", "evidence_sufficient", "uncertainty_acceptable", "calibration_sufficient",
             "provenance_complete", "effect_scope_conformant", "effect_ceiling_not_exceeded",
             "checkpoint_guards_satisfied", "stop_conditions_satisfied", "dukkha_preservation_supported",
             "protected_group_nonexternalization_supported", "future_nonexternalization_supported",
             "world_fact_claimed", "causal_attribution_claimed")
    for f in bools:
        if not isinstance(review.get(f), bool): blockers.append(f"effect_verification_review_{f}_invalid")
    start, end, maximum = review.get("verification_started_epoch"), review.get("verification_completed_epoch"), review.get("maximum_verification_duration")
    types_ok = all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in (start, end, maximum))
    if not types_ok: blockers.append("effect_verification_review_epoch_schema_invalid")
    return digest, types_ok and 1 <= maximum <= 64 and 0 <= end - start <= maximum

def _verify_context(context: dict, expected: str, source: dict, review: dict, blockers: list[str]):
    if not context:
        blockers.append("verification_intake_context_missing"); return "", (False,) * 6
    if set(context) != CONTEXT_FIELDS: blockers.append("verification_intake_context_schema_invalid")
    digest = context.get("verification_intake_context_digest", "")
    if not digest: blockers.append("verification_intake_context_digest_missing")
    elif digest != compute_verification_intake_context_digest(context): blockers.append("verification_intake_context_digest_mismatch")
    if digest != expected: blockers.append("verification_intake_context_expected_binding_mismatch")
    _exact(context, {"source_observation_receipt_digest": source.get(SOURCE_DIGEST_FIELD), REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD)}, "verification_intake_context", blockers)
    for f in ("current_world_binding_digest", "current_world_model_state_digest", "current_world_lineage_digest",
              "verification_intake_session_id", "verification_intake_nonce_digest",
              "requested_verification_operation_digest", "exact_verification_cycle_digest"):
        if not isinstance(context.get(f), str) or not context.get(f): blockers.append(f"verification_intake_context_{f}_invalid")
    for f in ("current_world_model_revision", "source_observation_receipt_observed_epoch",
              "verification_intake_epoch", "maximum_verification_intake_delay"):
        v = context.get(f)
        if not isinstance(v, int) or isinstance(v, bool) or v < 0: blockers.append(f"verification_intake_context_{f}_invalid")
    world = all(context.get(k) == v for k, v in {
        "current_world_binding_digest": source.get("source_world_binding_digest"),
        "current_world_model_state_digest": source.get("source_world_model_state_digest"),
        "current_world_model_revision": source.get("source_world_model_revision"),
        "current_world_lineage_digest": source.get("source_world_lineage_digest"),
    }.items())
    if context.get("requested_verification_operation_digest") != compute_requested_verification_operation_digest(source, review): blockers.append("verification_intake_context_operation_digest_mismatch")
    if context.get("exact_verification_cycle_digest") != compute_exact_verification_cycle_digest(source, review, context): blockers.append("verification_intake_context_cycle_digest_mismatch")
    observed, epoch, maximum = context.get("source_observation_receipt_observed_epoch"), context.get("verification_intake_epoch"), context.get("maximum_verification_intake_delay")
    delay = all(isinstance(x, int) and not isinstance(x, bool) for x in (observed, epoch, maximum)) and 1 <= maximum <= 64 and 0 <= epoch - observed <= maximum
    lists = []
    for f in ("prior_verification_intake_session_ids", "prior_verification_review_certificate_digests",
              "prior_verification_intake_nonce_digests", "prior_verified_source_observation_receipt_digests"):
        ok, values = _strings(context.get(f), True)
        if not ok: blockers.append(f"verification_intake_context_{f}_invalid")
        lists.append(values)
    sessions, reviews, nonces, sources = lists
    return digest, (world, delay, context.get("verification_intake_session_id") not in sessions,
                    review.get(REVIEW_DIGEST_FIELD) not in reviews, context.get("verification_intake_nonce_digest") not in nonces,
                    source.get(SOURCE_DIGEST_FIELD) not in sources)

def _route(review: Mapping[str, Any], duration: bool, checks: tuple[bool, ...]) -> str:
    world, delay, session, review_fresh, nonce, source = checks
    if not all((session, review_fresh, nonce, source)): return DISPOSITION_REPLAY_REJECTED
    if not world: return DISPOSITION_WORLD_REFRESH
    if not delay: return DISPOSITION_CONTEXT_REFRESH
    if not duration: return DISPOSITION_REVIEW_REFRESH
    if not review.get("evidence_sufficient") or not review.get("uncertainty_acceptable"): return DISPOSITION_ADDITIONAL_OBSERVATION
    if not review.get("calibration_sufficient"): return DISPOSITION_CALIBRATION_REPAIR
    if not review.get("provenance_complete"): return DISPOSITION_PROVENANCE_REPAIR
    if not all(review.get(f) for f in ("effect_identity_match", "effect_scope_conformant", "effect_ceiling_not_exceeded", "checkpoint_guards_satisfied", "stop_conditions_satisfied")): return DISPOSITION_EFFECT_CONTRACT_REPAIR
    if not review.get("protected_group_nonexternalization_supported") or not review.get("future_nonexternalization_supported"): return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if not review.get("dukkha_preservation_supported"): return DISPOSITION_DUKKHA_CONTRADICTED
    return DISPOSITION_SUPPORTED

def build_verifyos_dukkha_preserving_observed_host_effect_verification_intake(*,
    source_observation_receipt: Mapping[str, Any], expected_source_observation_receipt_digest: str,
    effect_verification_review_certificate: Mapping[str, Any], expected_effect_verification_review_certificate_digest: str,
    verification_intake_context: Mapping[str, Any], expected_verification_intake_context_digest: str,
    verification_intake_policy_digest: str, verifyos_verification_responsibility_digest: str,
    verification_intake_request_id: str, observed_host_effect_verification_bundle_digest: str,
) -> VerifyOSDukkhaPreservingObservedHostEffectVerificationResult:
    blockers: list[str] = []
    source, review, context = _map(source_observation_receipt), _map(effect_verification_review_certificate), _map(verification_intake_context)
    for name, value in {
        "expected_source_observation_receipt_digest": expected_source_observation_receipt_digest,
        "expected_effect_verification_review_certificate_digest": expected_effect_verification_review_certificate_digest,
        "expected_verification_intake_context_digest": expected_verification_intake_context_digest,
        "verification_intake_policy_digest": verification_intake_policy_digest,
        "verifyos_verification_responsibility_digest": verifyos_verification_responsibility_digest,
        "verification_intake_request_id": verification_intake_request_id,
        "observed_host_effect_verification_bundle_digest": observed_host_effect_verification_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value: blockers.append(f"{name}_missing")
    source_digest, evidence, handoff, lineage, responsibility = _verify_source(source, expected_source_observation_receipt_digest, blockers)
    review_digest, duration = _verify_review(review, expected_effect_verification_review_certificate_digest, source, evidence, handoff, blockers)
    context_digest, checks = _verify_context(context, expected_verification_intake_context_digest, source, review, blockers)
    if not blockers:
        bundle = compute_observed_host_effect_verification_bundle_digest(
            source_observation_receipt_digest=source_digest, expected_source_observation_receipt_digest=expected_source_observation_receipt_digest,
            observation_record_digest=source.get("observation_record_digest"), verification_handoff_envelope_digest=source.get("verification_handoff_envelope_digest"),
            effect_verification_review_certificate_digest=review_digest,
            expected_effect_verification_review_certificate_digest=expected_effect_verification_review_certificate_digest,
            verification_intake_context_digest=context_digest, expected_verification_intake_context_digest=expected_verification_intake_context_digest,
            requested_verification_operation_digest=context.get("requested_verification_operation_digest"),
            exact_verification_cycle_digest=context.get("exact_verification_cycle_digest"), verification_intake_policy_digest=verification_intake_policy_digest,
            verifyos_verification_responsibility_digest=verifyos_verification_responsibility_digest,
            verification_intake_request_id=verification_intake_request_id,
        )
        if bundle != observed_host_effect_verification_bundle_digest: blockers.append("observed_host_effect_verification_bundle_digest_mismatch")
    if blockers: return VerifyOSDukkhaPreservingObservedHostEffectVerificationResult(STATUS_BLOCKED, sorted(set(blockers)), None)
    disposition = _route(review, duration, checks); supported = disposition == DISPOSITION_SUPPORTED
    state_after = STATE_AFTER_VERIFIED if supported else STATE_BEFORE
    record = {
        "source_observation_receipt_digest": source_digest, "observation_record_digest": source["observation_record_digest"],
        "verification_handoff_envelope_digest": source["verification_handoff_envelope_digest"], REVIEW_DIGEST_FIELD: review_digest,
        "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"], "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"], "verifier_id": review["verifier_id"],
        "verification_intake_session_id": context["verification_intake_session_id"], "verification_intake_nonce_digest": context["verification_intake_nonce_digest"],
        "verification_intake_epoch": context["verification_intake_epoch"], "verification_disposition": disposition,
        "state_before": STATE_BEFORE, "state_after": state_after,
        "verification_outcome": "bounded_host_effect_verification_supported_world_not_updated" if supported else "observed_host_effect_verification_routed_without_world_update",
    }
    record_digest = canonical_digest(record)
    debt = {"source_observation_receipt_digest": source_digest, REVIEW_DIGEST_FIELD: review_digest,
            "verification_record_digest": record_digest, "verification_debt_consumed": supported,
            "source_observation_receipt_marked_verified": supported, "double_verification_performed": False}
    debt_digest = canonical_digest(debt)
    world = {
        "source_observation_receipt_digest": source_digest, "verification_record_digest": record_digest, REVIEW_DIGEST_FIELD: review_digest,
        "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"], "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"], "requested_effect_tags": list(handoff["requested_effect_tags"]),
        "observed_value_digest": handoff["observed_value_digest"], "uncertainty_digest": handoff["uncertainty_digest"],
        "calibration_digest": handoff["calibration_digest"], "provenance_chain_digests": list(handoff["provenance_chain_digests"]),
        "verification_disposition": disposition, "effect_conformance_verified": supported, "dukkha_preservation_verified": supported,
        "protected_group_nonexternalization_verified": supported, "future_nonexternalization_verified": supported,
        "world_fact_state": "not_promoted", "causal_attribution_state": "not_confirmed",
        "world_disposition_intake_admitted": supported, "world_disposition_receipt_required": supported, "compensation_route_ready": True,
    }
    world_digest = canonical_digest(world)
    resulting_lineage = sorted(set(lineage) | {source_digest, source["observation_record_digest"], source["verification_handoff_envelope_digest"],
        review_digest, context_digest, context["requested_verification_operation_digest"], context["exact_verification_cycle_digest"],
        record_digest, debt_digest, world_digest, observed_host_effect_verification_bundle_digest})
    resulting_responsibility = sorted(set(responsibility) | {review["verifier_id"], verifyos_verification_responsibility_digest})
    world_current, delay_current, session_fresh, review_fresh, nonce_fresh, source_fresh = checks
    receipt = {
        "kernel": "VerifyOS Dukkha-Preserving Observed Host-Effect Verification Intake Kernel", "kernel_version": "v0.1", "verifyos_version": "v0.7",
        "status": "VERIFYOS_DUKKHA_PRESERVING_OBSERVED_HOST_EFFECT_VERIFICATION_ROUTED",
        "source_observation_receipt_digest": source_digest, "source_host_effect_receipt_digest": source["source_host_effect_receipt_digest"],
        "source_external_host_effect_record_digest": source["source_external_host_effect_record_digest"],
        "source_independent_observation_evidence_packet_digest": source[EVIDENCE_DIGEST_FIELD],
        "source_observation_record_digest": source["observation_record_digest"],
        "source_verification_handoff_envelope_digest": source["verification_handoff_envelope_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"], "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"], "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"], "invoked_frontier_candidate_id": source["invoked_frontier_candidate_id"],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"], "invoked_frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "effect_verification_review_certificate": review, REVIEW_DIGEST_FIELD: review_digest,
        "verification_intake_context_digest": context_digest, "verification_intake_policy_digest": verification_intake_policy_digest,
        "verifyos_verification_responsibility_digest": verifyos_verification_responsibility_digest,
        "verification_intake_request_id": verification_intake_request_id,
        "observed_host_effect_verification_bundle_digest": observed_host_effect_verification_bundle_digest,
        "verification_disposition": disposition, "verification_state_before": STATE_BEFORE, "verification_state_after": state_after,
        "verification_record": record, "verification_record_digest": record_digest,
        "verification_debt_consumption_record": debt, "verification_debt_consumption_record_digest": debt_digest,
        "world_disposition_handoff_envelope": world, "world_disposition_handoff_envelope_digest": world_digest,
    }
    receipt.update({
        "source_observation_receipt_supplied": True, "source_observation_receipt_fully_revalidated": True,
        "effect_verification_review_certificate_bound": True, "verifier_identity_bound": True, "verification_method_bound": True,
        "verification_evidence_bound": True, "expected_effect_contract_bound": True, "observed_value_digest_bound": True,
        "uncertainty_digest_bound": True, "calibration_digest_bound": True, "provenance_chain_bound": True,
        "dukkha_impact_assessment_bound": True, "protected_group_impact_assessment_bound": True,
        "future_subject_impact_assessment_bound": True, "exactly_one_verification_receipt_issued": True,
        "verification_review_performed": True, "verification_completed": supported, "effect_conformance_verified": supported,
        "dukkha_preservation_verified": supported, "protected_group_nonexternalization_verified": supported,
        "future_nonexternalization_verified": supported, "verification_debt_consumed": supported,
        "verification_debt_replay_closed": supported, "verification_double_consumed": False,
        "verification_review_certificate_replay_closed": True, "verification_intake_nonce_consumed": True,
        "verification_intake_nonce_replay_closed": True, "source_observation_receipt_replay_closed": supported,
        "verification_intake_session_replay_fresh_before_intake": session_fresh,
        "verification_review_replay_fresh_before_intake": review_fresh,
        "verification_intake_nonce_replay_fresh_before_intake": nonce_fresh,
        "source_observation_receipt_replay_fresh_before_verification": source_fresh,
        "world_conditions_current": world_current, "verification_review_duration_current": duration,
        "verification_intake_delay_current": delay_current, "verification_debt_open": not supported,
        "world_disposition_intake_admitted": supported, "world_disposition_receipt_required": supported,
        "world_disposition_completed": False, "persistent_world_model_state_unchanged": True,
        "world_fact_confirmed": False, "causal_attribution_confirmed": False, "dukkha_reduction_realized_confirmed": False,
        "host_operation_reexecuted": False, "observation_reperformed": False, "tool_invocation_performed": False,
        "external_side_effect_performed": False, "persistent_host_state_changed_by_verification": False,
        "compensation_route_ready": True, "compensation_performed": False, "automatic_truth_promotion": False,
        "automatic_plan_completion": False, "automatic_rollback": False, "automatic_compensation": False,
        "effect_scope_preserved": True, "effect_ceiling_preserved": True, "checkpoint_guards_preserved": True,
        "stop_conditions_preserved": True, "evidence_lineage_preserved": True, "responsibility_lineage_preserved": True,
        "alternative_candidates_preserved": True, "dissent_preserved": True, "minority_preserved": True,
        "dukkha_reduction_support_preserved": True, "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True, "revision_capacity_preserved": True,
        "persistent_loop_reduction_preserved": True, "single_scalar_utility_not_introduced": True,
        "selection_remains_decisionos_owned": True, "selection_authority_granted_to_verifyos": False,
        "plan_revision_authority_granted_to_verifyos": False, "dukkha_minimization_authority_granted_to_verifyos": False,
        "general_execution_authority_granted": False, "execution_permission": False,
        "world_mutation_authority_granted": False, "world_model_prediction_not_truth": True,
        "history_read_only": True, "qi_grants_no_authority": True, "future_only": True, "active_now": False,
        "resulting_lineage_digests": resulting_lineage, "resulting_responsibility_lineage_digests": resulting_responsibility,
    })
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return VerifyOSDukkhaPreservingObservedHostEffectVerificationResult(STATUS_READY, [], receipt)
