#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_actos_dukkha_preserving_atomic_external_host_effect_intake_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_DIGEST_FIELD,
    canonical_digest,
    compute_external_host_effect_application_receipt_digest,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
RECEIPT_DIGEST_FIELD = "observeos_dukkha_preserving_external_host_effect_observation_intake_receipt_digest"
EVIDENCE_DIGEST_FIELD = "independent_observation_evidence_packet_digest"
STATE_BEFORE = "host_effect_recorded_unobserved"
STATE_AFTER = "host_effect_observed_unverified"
OBSERVATION_OUTCOME = "independent_host_effect_observation_recorded"
INTAKE_OUTCOME = "host_effect_observed_pending_verification"

SOURCE_TRUE = (
    "external_host_effect_application_receipt_supplied", "canonical_host_effect_receipt_bound",
    "committed_effect_envelope_consumed", "committed_effect_envelope_marked_applied",
    "committed_effect_envelope_replay_closed", "host_effect_application_receipt_replay_closed",
    "host_effect_intake_nonce_consumed", "host_effect_intake_nonce_replay_closed",
    "source_effect_commit_replay_closed", "world_conditions_current",
    "host_effect_application_duration_current", "host_effect_intake_delay_current",
    "exactly_one_external_host_effect_recorded", "external_host_effect_receipt_issued",
    "external_host_effect_performed", "host_driver_tool_invocation_performed",
    "host_driver_external_side_effect_performed", "tool_invocation_performed",
    "external_side_effect_performed", "persistent_host_state_changed",
    "persistent_world_model_state_unchanged", "observation_intake_admitted",
    "observation_receipt_required", "verification_intake_required", "verification_debt_open",
    "compensation_route_ready", "effect_scope_preserved", "effect_ceiling_preserved",
    "checkpoint_guards_preserved", "stop_conditions_preserved", "evidence_lineage_preserved",
    "alternative_candidates_preserved", "dissent_preserved", "minority_preserved",
    "dukkha_reduction_support_preserved", "protected_group_nonexternalization_preserved",
    "future_nonexternalization_preserved", "revision_capacity_preserved",
    "persistent_loop_reduction_preserved", "single_scalar_utility_not_introduced",
    "selection_remains_decisionos_owned", "bounded_host_effect_authority_consumed",
    "world_model_prediction_not_truth", "history_read_only", "qi_grants_no_authority", "future_only",
)
SOURCE_FALSE = (
    "committed_effect_envelope_double_applied", "kernel_tool_invocation_performed",
    "kernel_external_side_effect_performed", "world_fact_confirmed", "causal_attribution_confirmed",
    "observation_performed", "independent_world_evidence_present", "verification_intake_admitted",
    "verification_completed", "compensation_performed", "automatic_truth_promotion",
    "automatic_plan_completion", "automatic_rollback", "selection_authority_granted_to_actos",
    "plan_revision_authority_granted_to_actos", "dukkha_minimization_authority_granted_to_actos",
    "general_execution_authority_granted", "execution_permission", "world_mutation_authority_granted",
    "active_now",
)
EVIDENCE_FIELDS = {
    "source_host_effect_receipt_digest", "external_host_effect_record_digest",
    "observation_handoff_envelope_digest", "frontier_materialization_candidate_id",
    "frontier_adapter_id", "frontier_binding_digest", "requested_effect_tags", "host_target_digest",
    "collector_id", "evidence_source_id", "collection_started_epoch", "collection_completed_epoch",
    "maximum_collection_duration", "raw_artifact_digest", "observed_value_digest",
    "uncertainty_digest", "calibration_digest", "observation_context_digest",
    "tamper_evidence_digest", "provenance_chain_digests", "collector_independent_from_host_driver",
    "evidence_source_independent_from_host_receipt", "exactly_one_observation",
    "observation_outcome", EVIDENCE_DIGEST_FIELD,
}
CONTEXT_FIELDS = {
    "source_host_effect_receipt_digest", EVIDENCE_DIGEST_FIELD, "current_world_binding_digest",
    "current_world_model_state_digest", "current_world_model_revision", "current_world_lineage_digest",
    "source_host_effect_receipt_observed_epoch", "observation_intake_epoch",
    "maximum_observation_intake_delay", "observation_intake_session_id",
    "observation_intake_nonce_digest", "prior_observation_intake_session_ids",
    "prior_observation_evidence_packet_digests", "prior_observation_intake_nonce_digests",
    "prior_observed_source_host_effect_receipt_digests", "requested_observation_operation_digest",
    "exact_observation_cycle_digest", "observation_intake_context_digest",
}

@dataclass
class ObserveOSDukkhaPreservingExternalHostEffectObservationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def compute_independent_observation_evidence_packet_digest(packet: Mapping[str, Any]) -> str:
    return _digest_without(packet, EVIDENCE_DIGEST_FIELD)


def compute_observation_intake_context_digest(context: Mapping[str, Any]) -> str:
    return _digest_without(context, "observation_intake_context_digest")


def compute_requested_observation_operation_digest(source: Mapping[str, Any], evidence: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_host_effect_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "external_host_effect_record_digest": source.get("external_host_effect_record_digest"),
        "observation_handoff_envelope_digest": source.get("observation_handoff_envelope_digest"),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "state_before": STATE_BEFORE, "state_after": STATE_AFTER,
    })


def compute_exact_observation_cycle_digest(source: Mapping[str, Any], evidence: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_host_effect_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        "observation_intake_session_id": context.get("observation_intake_session_id"),
        "observation_intake_nonce_digest": context.get("observation_intake_nonce_digest"),
        "observation_intake_epoch": context.get("observation_intake_epoch"),
        "current_world_model_revision": context.get("current_world_model_revision"),
        "requested_observation_operation_digest": context.get("requested_observation_operation_digest"),
    })


def compute_external_host_effect_observation_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(x, str) or not x for x in value):
        return False, []
    return value == sorted(value) and len(value) == len(set(value)), list(value)


def _exact(actual: Mapping[str, Any], expected: Mapping[str, Any], prefix: str, blockers: list[str]) -> None:
    for field, value in expected.items():
        if actual.get(field) != value:
            blockers.append(f"{prefix}_{field}_mismatch")


def _verify_source(source: dict, expected_digest: str, blockers: list[str]):
    if not source:
        blockers.append("source_host_effect_receipt_missing")
        return "", {}, {}, [], []
    _exact(source, {
        "kernel": "ActOS Dukkha-Preserving Atomic External Host-Effect Intake Kernel",
        "kernel_version": "v0.1", "actos_version": "v0.11",
        "status": "ACTOS_DUKKHA_PRESERVING_ATOMIC_EXTERNAL_HOST_EFFECT_RECORDED",
        "host_effect_state_after": STATE_BEFORE,
    }, "source", blockers)
    digest = source.get(SOURCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_host_effect_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_DIGEST_FIELD):
        blockers.append("source_host_effect_receipt_digest_mismatch")
    if digest != expected_digest:
        blockers.append("source_host_effect_expected_binding_mismatch")
    for field in SOURCE_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    host = _map(source.get("external_host_effect_application_receipt"))
    record = _map(source.get("external_host_effect_record"))
    consumption = _map(source.get("committed_effect_consumption_record"))
    handoff = _map(source.get("observation_handoff_envelope"))
    for name, item, field, digest_fn in (
        ("host_application", host, "external_host_effect_application_receipt_digest", compute_external_host_effect_application_receipt_digest),
        ("external_host_effect_record", record, "external_host_effect_record_digest", canonical_digest),
        ("committed_effect_consumption_record", consumption, "committed_effect_consumption_record_digest", canonical_digest),
        ("observation_handoff_envelope", handoff, "observation_handoff_envelope_digest", canonical_digest),
    ):
        if not item:
            blockers.append(f"source_{name}_invalid")
        elif source.get(field) != digest_fn(item):
            blockers.append(f"source_{name}_digest_mismatch")
    _exact(record, {
        "source_effect_commit_receipt_digest": source.get("source_effect_commit_receipt_digest"),
        "effect_commit_record_digest": source.get("source_effect_commit_record_digest"),
        "committed_effect_envelope_digest": source.get("source_committed_effect_envelope_digest"),
        "external_host_effect_application_receipt_digest": source.get("external_host_effect_application_receipt_digest"),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "state_before": "effect_committed_host_not_applied",
        "state_after": STATE_BEFORE,
        "intake_outcome": "bounded_external_host_effect_recorded_pending_observation",
    }, "source_external_host_effect_record", blockers)
    if consumption.get("committed_effect_consumed") is not True:
        blockers.append("source_committed_effect_not_consumed")
    if consumption.get("double_application_performed") is not False:
        blockers.append("source_committed_effect_double_application_promoted")
    _exact(handoff, {
        "source_effect_commit_receipt_digest": source.get("source_effect_commit_receipt_digest"),
        "committed_effect_envelope_digest": source.get("source_committed_effect_envelope_digest"),
        "external_host_effect_application_receipt_digest": source.get("external_host_effect_application_receipt_digest"),
        "external_host_effect_record_digest": source.get("external_host_effect_record_digest"),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "host_effect_state": "applied_unobserved", "observation_state": "not_observed",
        "verification_state": "verification_debt_open", "observation_intake_admitted": True,
        "observation_receipt_required": True, "verification_intake_required": True,
        "verification_intake_admitted": False, "compensation_route_ready": True,
    }, "source_observation_handoff", blockers)
    requested_ok, requested = _strings(handoff.get("requested_effect_tags"), True)
    if not requested_ok:
        blockers.append("source_requested_effect_tags_invalid")
    if host.get("requested_effect_tags") != requested:
        blockers.append("source_requested_effect_tags_host_binding_mismatch")
    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(source.get("resulting_responsibility_lineage_digests"))
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, host, handoff, lineage, responsibility


def _verify_evidence(evidence: dict, expected_digest: str, source: dict, host: dict, handoff: dict, blockers: list[str]):
    if not evidence:
        blockers.append("independent_observation_evidence_packet_missing")
        return "", False, []
    if set(evidence) != EVIDENCE_FIELDS:
        blockers.append("independent_observation_evidence_packet_schema_invalid")
    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("independent_observation_evidence_packet_digest_missing")
    elif digest != compute_independent_observation_evidence_packet_digest(evidence):
        blockers.append("independent_observation_evidence_packet_digest_mismatch")
    if digest != expected_digest:
        blockers.append("independent_observation_evidence_expected_binding_mismatch")
    _exact(evidence, {
        "source_host_effect_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "external_host_effect_record_digest": source.get("external_host_effect_record_digest"),
        "observation_handoff_envelope_digest": source.get("observation_handoff_envelope_digest"),
        "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "requested_effect_tags": handoff.get("requested_effect_tags"),
        "host_target_digest": host.get("host_target_digest"),
        "collector_independent_from_host_driver": True,
        "evidence_source_independent_from_host_receipt": True,
        "exactly_one_observation": True, "observation_outcome": OBSERVATION_OUTCOME,
    }, "independent_observation_evidence", blockers)
    for field in ("collector_id", "evidence_source_id", "raw_artifact_digest", "observed_value_digest",
                  "uncertainty_digest", "calibration_digest", "observation_context_digest", "tamper_evidence_digest"):
        if not isinstance(evidence.get(field), str) or not evidence.get(field):
            blockers.append(f"independent_observation_evidence_{field}_invalid")
    if evidence.get("collector_id") == host.get("host_driver_id"):
        blockers.append("observation_collector_not_independent_from_host_driver")
    if evidence.get("evidence_source_id") in {host.get("host_driver_id"), source.get("external_host_effect_application_receipt_digest")}:
        blockers.append("host_receipt_used_as_independent_observation_evidence")
    start, end, maximum = (evidence.get("collection_started_epoch"), evidence.get("collection_completed_epoch"), evidence.get("maximum_collection_duration"))
    duration_current = all(isinstance(x, int) and not isinstance(x, bool) for x in (start, end, maximum)) and 1 <= maximum <= 64 and 0 <= end - start <= maximum
    if not duration_current:
        blockers.append("independent_observation_collection_duration_invalid")
    provenance_ok, provenance = _strings(evidence.get("provenance_chain_digests"))
    if not provenance_ok:
        blockers.append("independent_observation_provenance_chain_invalid")
    return digest, duration_current, provenance


def _verify_context(context: dict, expected_digest: str, source: dict, evidence: dict, blockers: list[str]):
    if not context:
        blockers.append("observation_intake_context_missing")
        return "", (False,) * 6
    if set(context) != CONTEXT_FIELDS:
        blockers.append("observation_intake_context_schema_invalid")
    digest = context.get("observation_intake_context_digest", "")
    if not digest:
        blockers.append("observation_intake_context_digest_missing")
    elif digest != compute_observation_intake_context_digest(context):
        blockers.append("observation_intake_context_digest_mismatch")
    if digest != expected_digest:
        blockers.append("observation_intake_context_expected_binding_mismatch")
    _exact(context, {
        "source_host_effect_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
    }, "observation_intake_context", blockers)
    world_current = all(context.get(k) == v for k, v in {
        "current_world_binding_digest": source.get("source_world_binding_digest"),
        "current_world_model_state_digest": source.get("source_world_model_state_digest"),
        "current_world_model_revision": source.get("source_world_model_revision"),
        "current_world_lineage_digest": source.get("source_world_lineage_digest"),
    }.items())
    if context.get("requested_observation_operation_digest") != compute_requested_observation_operation_digest(source, evidence):
        blockers.append("observation_intake_context_operation_digest_mismatch")
    if context.get("exact_observation_cycle_digest") != compute_exact_observation_cycle_digest(source, evidence, context):
        blockers.append("observation_intake_context_cycle_digest_mismatch")
    observed, epoch, maximum = (context.get("source_host_effect_receipt_observed_epoch"), context.get("observation_intake_epoch"), context.get("maximum_observation_intake_delay"))
    delay_current = all(isinstance(x, int) and not isinstance(x, bool) for x in (observed, epoch, maximum)) and 1 <= maximum <= 64 and 0 <= epoch - observed <= maximum
    collections = []
    for field in ("prior_observation_intake_session_ids", "prior_observation_evidence_packet_digests", "prior_observation_intake_nonce_digests", "prior_observed_source_host_effect_receipt_digests"):
        ok, values = _strings(context.get(field), True)
        if not ok:
            blockers.append(f"observation_intake_context_{field}_invalid")
        collections.append(values)
    sessions, evidence_seen, nonces, sources = collections
    return digest, (
        world_current, delay_current,
        context.get("observation_intake_session_id") not in sessions,
        evidence.get(EVIDENCE_DIGEST_FIELD) not in evidence_seen,
        context.get("observation_intake_nonce_digest") not in nonces,
        source.get(SOURCE_DIGEST_FIELD) not in sources,
    )


def build_observeos_dukkha_preserving_external_host_effect_observation_intake(*,
    source_host_effect_receipt: Mapping[str, Any], expected_source_host_effect_receipt_digest: str,
    independent_observation_evidence_packet: Mapping[str, Any], expected_independent_observation_evidence_packet_digest: str,
    observation_intake_context: Mapping[str, Any], expected_observation_intake_context_digest: str,
    observation_intake_policy_digest: str, observeos_observation_responsibility_digest: str,
    observation_intake_request_id: str, external_host_effect_observation_bundle_digest: str,
) -> ObserveOSDukkhaPreservingExternalHostEffectObservationResult:
    blockers: list[str] = []
    source, evidence, context = _map(source_host_effect_receipt), _map(independent_observation_evidence_packet), _map(observation_intake_context)
    for name, value in {
        "expected_source_host_effect_receipt_digest": expected_source_host_effect_receipt_digest,
        "expected_independent_observation_evidence_packet_digest": expected_independent_observation_evidence_packet_digest,
        "expected_observation_intake_context_digest": expected_observation_intake_context_digest,
        "observation_intake_policy_digest": observation_intake_policy_digest,
        "observeos_observation_responsibility_digest": observeos_observation_responsibility_digest,
        "observation_intake_request_id": observation_intake_request_id,
        "external_host_effect_observation_bundle_digest": external_host_effect_observation_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    source_digest, host, handoff, lineage, responsibility = _verify_source(source, expected_source_host_effect_receipt_digest, blockers)
    evidence_digest, duration_current, provenance = _verify_evidence(evidence, expected_independent_observation_evidence_packet_digest, source, host, handoff, blockers)
    context_digest, checks = _verify_context(context, expected_observation_intake_context_digest, source, evidence, blockers)
    labels = ("observation_world_refresh_required", "observation_intake_expired", "observation_intake_session_replay_rejected",
              "observation_evidence_packet_replay_rejected", "observation_intake_nonce_replay_rejected", "source_host_effect_receipt_replay_rejected")
    if not duration_current:
        blockers.append("independent_observation_collection_not_current")
    for ok, label in zip(checks, labels):
        if not ok:
            blockers.append(label)
    if not blockers:
        expected_bundle = compute_external_host_effect_observation_bundle_digest(
            source_host_effect_receipt_digest=source_digest,
            expected_source_host_effect_receipt_digest=expected_source_host_effect_receipt_digest,
            external_host_effect_record_digest=source.get("external_host_effect_record_digest"),
            observation_handoff_envelope_digest=source.get("observation_handoff_envelope_digest"),
            independent_observation_evidence_packet_digest=evidence_digest,
            expected_independent_observation_evidence_packet_digest=expected_independent_observation_evidence_packet_digest,
            observation_intake_context_digest=context_digest,
            expected_observation_intake_context_digest=expected_observation_intake_context_digest,
            requested_observation_operation_digest=context.get("requested_observation_operation_digest"),
            exact_observation_cycle_digest=context.get("exact_observation_cycle_digest"),
            observation_intake_policy_digest=observation_intake_policy_digest,
            observeos_observation_responsibility_digest=observeos_observation_responsibility_digest,
            observation_intake_request_id=observation_intake_request_id,
        )
        if external_host_effect_observation_bundle_digest != expected_bundle:
            blockers.append("external_host_effect_observation_bundle_digest_mismatch")
    if blockers:
        return ObserveOSDukkhaPreservingExternalHostEffectObservationResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    observation_record = {
        "source_host_effect_receipt_digest": source_digest,
        "external_host_effect_record_digest": source["external_host_effect_record_digest"],
        "observation_handoff_envelope_digest": source["observation_handoff_envelope_digest"],
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "collector_id": evidence["collector_id"], "evidence_source_id": evidence["evidence_source_id"],
        "observation_intake_session_id": context["observation_intake_session_id"],
        "observation_intake_nonce_digest": context["observation_intake_nonce_digest"],
        "observation_intake_epoch": context["observation_intake_epoch"],
        "state_before": STATE_BEFORE, "state_after": STATE_AFTER, "intake_outcome": INTAKE_OUTCOME,
    }
    observation_record_digest = canonical_digest(observation_record)
    debt_record = {
        "source_host_effect_receipt_digest": source_digest, EVIDENCE_DIGEST_FIELD: evidence_digest,
        "observation_record_digest": observation_record_digest, "observation_debt_consumed": True,
        "source_host_effect_receipt_marked_observed": True, "double_observation_performed": False,
    }
    debt_digest = canonical_digest(debt_record)
    verification_handoff = {
        "source_host_effect_receipt_digest": source_digest,
        "external_host_effect_record_digest": source["external_host_effect_record_digest"],
        EVIDENCE_DIGEST_FIELD: evidence_digest, "observation_record_digest": observation_record_digest,
        "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "requested_effect_tags": list(handoff["requested_effect_tags"]),
        "observed_value_digest": evidence["observed_value_digest"], "uncertainty_digest": evidence["uncertainty_digest"],
        "calibration_digest": evidence["calibration_digest"], "provenance_chain_digests": list(provenance),
        "host_effect_state": "observed_unverified", "observation_state": "observed",
        "verification_state": "verification_debt_open", "verification_intake_admitted": True,
        "verification_receipt_required": True, "world_fact_confirmed": False,
        "causal_attribution_confirmed": False, "compensation_route_ready": True,
    }
    verification_handoff_digest = canonical_digest(verification_handoff)
    resulting_lineage = sorted(set(lineage) | set(provenance) | {source_digest, source["external_host_effect_record_digest"],
        source["observation_handoff_envelope_digest"], evidence_digest, context_digest,
        context["requested_observation_operation_digest"], context["exact_observation_cycle_digest"],
        observation_record_digest, debt_digest, verification_handoff_digest, external_host_effect_observation_bundle_digest})
    resulting_responsibility = sorted(set(responsibility) | {evidence["collector_id"], evidence["evidence_source_id"], observeos_observation_responsibility_digest})
    receipt = {
        "kernel": "ObserveOS Dukkha-Preserving External Host-Effect Observation Intake Kernel",
        "kernel_version": "v0.1", "observeos_version": "v0.5",
        "status": "OBSERVEOS_DUKKHA_PRESERVING_EXTERNAL_HOST_EFFECT_OBSERVED",
        "source_host_effect_receipt_digest": source_digest,
        "source_effect_commit_receipt_digest": source["source_effect_commit_receipt_digest"],
        "source_external_host_effect_application_receipt_digest": source["external_host_effect_application_receipt_digest"],
        "source_external_host_effect_record_digest": source["external_host_effect_record_digest"],
        "source_observation_handoff_envelope_digest": source["observation_handoff_envelope_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"],
        "invoked_frontier_candidate_id": source["invoked_frontier_candidate_id"],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "independent_observation_evidence_packet": evidence, EVIDENCE_DIGEST_FIELD: evidence_digest,
        "observation_intake_context_digest": context_digest, "observation_intake_policy_digest": observation_intake_policy_digest,
        "observeos_observation_responsibility_digest": observeos_observation_responsibility_digest,
        "observation_intake_request_id": observation_intake_request_id,
        "external_host_effect_observation_bundle_digest": external_host_effect_observation_bundle_digest,
        "observation_state_before": STATE_BEFORE, "observation_state_after": STATE_AFTER,
        "observation_record": observation_record, "observation_record_digest": observation_record_digest,
        "observation_debt_consumption_record": debt_record, "observation_debt_consumption_record_digest": debt_digest,
        "verification_handoff_envelope": verification_handoff, "verification_handoff_envelope_digest": verification_handoff_digest,
    }
    receipt.update({
        "source_host_effect_receipt_supplied": True, "source_host_effect_receipt_fully_revalidated": True,
        "independent_observation_evidence_bound": True, "collector_identity_bound": True,
        "evidence_source_identity_bound": True, "collection_epoch_freshness_confirmed": True,
        "raw_artifact_digest_bound": True, "observed_value_digest_bound": True,
        "uncertainty_digest_bound": True, "calibration_digest_bound": True, "context_digest_bound": True,
        "tamper_evidence_digest_bound": True, "provenance_chain_preserved": True,
        "host_effect_observation_identity_exact": True, "exactly_one_observation_receipt_issued": True,
        "observation_performed": True, "independent_world_evidence_present": True,
        "observation_debt_consumed": True, "observation_debt_replay_closed": True,
        "observation_double_consumed": False, "observation_evidence_packet_replay_closed": True,
        "observation_intake_nonce_consumed": True, "observation_intake_nonce_replay_closed": True,
        "source_host_effect_receipt_replay_closed": True,
        "observation_intake_session_replay_fresh_before_intake": True,
        "observation_evidence_replay_fresh_before_intake": True,
        "observation_intake_nonce_replay_fresh_before_intake": True,
        "source_host_effect_receipt_replay_fresh_before_observation": True,
        "world_conditions_current": True, "observation_collection_duration_current": True,
        "observation_intake_delay_current": True, "collector_independent_from_host_driver": True,
        "evidence_source_independent_from_host_receipt": True, "host_receipt_used_as_independent_evidence": False,
        "host_operation_reexecuted": False, "tool_invocation_performed": False,
        "external_side_effect_performed": False, "persistent_host_state_changed_by_observation": False,
        "persistent_world_model_state_unchanged": True, "world_fact_confirmed": False,
        "causal_attribution_confirmed": False, "verification_intake_required": True,
        "verification_intake_admitted": True, "verification_receipt_required": True,
        "verification_completed": False, "verification_debt_open": True,
        "compensation_route_ready": True, "compensation_performed": False,
        "automatic_truth_promotion": False, "automatic_plan_completion": False,
        "automatic_rollback": False, "automatic_compensation": False,
        "effect_scope_preserved": True, "effect_ceiling_preserved": True,
        "checkpoint_guards_preserved": True, "stop_conditions_preserved": True,
        "evidence_lineage_preserved": True, "responsibility_lineage_preserved": True,
        "alternative_candidates_preserved": True, "dissent_preserved": True, "minority_preserved": True,
        "dukkha_reduction_support_preserved": True, "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True, "revision_capacity_preserved": True,
        "persistent_loop_reduction_preserved": True, "single_scalar_utility_not_introduced": True,
        "selection_remains_decisionos_owned": True, "selection_authority_granted_to_observeos": False,
        "plan_revision_authority_granted_to_observeos": False,
        "dukkha_minimization_authority_granted_to_observeos": False,
        "general_execution_authority_granted": False, "execution_permission": False,
        "world_mutation_authority_granted": False, "world_model_prediction_not_truth": True,
        "history_read_only": True, "qi_grants_no_authority": True, "future_only": True, "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    })
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return ObserveOSDukkhaPreservingExternalHostEffectObservationResult(STATUS_READY, [], receipt)
