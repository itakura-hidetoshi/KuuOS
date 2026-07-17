#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import (
    DISPOSITION_SUPPORTED as SRC_SUPPORTED,
    PACKET_DIGEST_FIELD as SRC_PACKET_DIGEST,
    POLICY_DIGEST_FIELD as SRC_POLICY_DIGEST,
    RECEIPT_DIGEST_FIELD as SRC_RECEIPT_DIGEST,
    STATUS_BLOCKED, STATUS_READY, SUPPORTED_STATE as SRC_STATE,
    canonical_digest, digest_without, mapping, nat, pos, strings,
)

RECEIPT_DIGEST_FIELD = "verifyos_sequential_epistemic_observation_verification_handoff_receipt_digest"
REQUEST_DIGEST_FIELD = "independent_verification_request_digest"
REVIEW_DIGEST_FIELD = "independent_verification_handoff_review_digest"
CONTEXT_DIGEST_FIELD = "independent_verification_handoff_context_digest"
STATE_AFTER = SRC_STATE + "_independent_verification_handoff_prepared"

D_SUPPORTED = "independent_verification_handoff_supported"
D_SOURCE = "source_observability_receipt_repair_required"
D_CORRESPONDENCE = "observability_correspondence_repair_required"
D_WORLD = "world_refresh_required"
D_CONTEXT = "verification_handoff_context_refresh_required"
D_REVIEW = "verification_handoff_review_refresh_required"
D_INDEPENDENCE = "verifier_independence_repair_required"
D_SNAPSHOT = "evidence_snapshot_repair_required"
D_PROTOCOL = "verification_protocol_repair_required"
D_ACCEPTANCE = "acceptance_criteria_repair_required"
D_REPRODUCTION = "reproduction_plan_repair_required"
D_WINDOW = "verification_request_window_repair_required"
D_REPLAY = "replay_conflict_rejected"
D_MUTATION = "current_state_mutation_rejected"
D_AUTHORITY = "authority_escalation_rejected"

REQUEST_FIELDS = {
    "source_observability_receipt_digest", "source_observation_receipt_digest",
    "source_observability_packet_digest", "source_observability_policy_digest",
    "trace_id", "span_id", "provenance_bundle_digest",
    "sequential_uncertainty_digest", "conformal_calibration_digest",
    "distribution_shift_evidence_digest", "verification_protocol_digest",
    "acceptance_criteria_digest", "reproduction_plan_digest",
    "environment_snapshot_digest", "evidence_snapshot_digests",
    "independent_evidence_source_ids", "verification_scope", "verifier_id",
    "collector_id", "source_evidence_source_id",
    "minimum_independent_evidence_sources", "minimum_reproduction_attempts",
    "planned_reproduction_attempts", "request_prepared_epoch",
    "request_expires_epoch", "maximum_request_lifetime",
    "verifier_independence_declared", "blinded_review_required",
    "observation_recollection_requested", "current_state_mutation_requested",
    "authority_escalation_requested", "verification_completion_claimed",
    REQUEST_DIGEST_FIELD,
}
REVIEW_FIELDS = {
    "source_observability_receipt_digest", REQUEST_DIGEST_FIELD, "reviewer_id",
    "review_method_digest", "review_evidence_digest", "review_started_epoch",
    "review_completed_epoch", "maximum_review_duration",
    "source_observability_correspondence_confirmed",
    "observability_supported_confirmed", "trace_context_bound",
    "provenance_bound", "sample_accounting_bound",
    "sequential_uncertainty_bound", "conformal_calibration_bound",
    "distribution_shift_absent", "verifier_independence_adequate",
    "evidence_snapshot_adequate", "verification_protocol_adequate",
    "acceptance_criteria_adequate", "reproduction_plan_adequate",
    "request_window_valid", "no_observation_recollection",
    "no_current_state_mutation", "no_authority_escalation",
    "no_verification_completion_claim", REVIEW_DIGEST_FIELD,
}
CONTEXT_FIELDS = {
    "source_observability_receipt_digest", REQUEST_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD, "source_world_revision", "current_world_revision",
    "source_observation_completed_epoch", "handoff_intake_epoch",
    "maximum_handoff_intake_delay", "handoff_session_id",
    "handoff_nonce_digest", "prior_handoff_session_ids",
    "prior_handoff_nonce_digests", "prior_verification_request_digests",
    "prior_handoff_review_digests",
    "prior_source_observability_receipt_digests",
    "requested_verification_handoff_operation_digest",
    "exact_verification_handoff_cycle_digest", CONTEXT_DIGEST_FIELD,
}

@dataclass(frozen=True)
class Result:
    status: str
    blockers: list[str]
    receipt: dict[str, Any] | None

def request_digest(v: Mapping[str, Any]) -> str:
    return digest_without(v, REQUEST_DIGEST_FIELD)

def review_digest(v: Mapping[str, Any]) -> str:
    return digest_without(v, REVIEW_DIGEST_FIELD)

def context_digest(v: Mapping[str, Any]) -> str:
    return digest_without(v, CONTEXT_DIGEST_FIELD)

def operation_digest(source: Mapping[str, Any], request: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source": source.get(SRC_RECEIPT_DIGEST),
        "request": request.get(REQUEST_DIGEST_FIELD),
        "review": review.get(REVIEW_DIGEST_FIELD),
        "revision": source.get("resulting_world_revision"),
        "before": SRC_STATE, "after": STATE_AFTER,
    })

def cycle_digest(source: Mapping[str, Any], request: Mapping[str, Any], review: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source": source.get(SRC_RECEIPT_DIGEST),
        "request": request.get(REQUEST_DIGEST_FIELD),
        "review": review.get(REVIEW_DIGEST_FIELD),
        "session": context.get("handoff_session_id"),
        "nonce": context.get("handoff_nonce_digest"),
        "epoch": context.get("handoff_intake_epoch"),
        "revision": context.get("current_world_revision"),
        "operation": context.get("requested_verification_handoff_operation_digest"),
    })

def bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)

def _duration(v: Mapping[str, Any], start: str, end: str, maximum: str) -> bool:
    a, b, m = v.get(start), v.get(end), v.get(maximum)
    return all(nat(x) for x in (a, b, m)) and a <= b and b - a <= m

def _exact(v: Mapping[str, Any], expected: Mapping[str, Any], prefix: str, blockers: list[str]) -> None:
    blockers.extend(f"{prefix}_{k}_mismatch" for k, x in expected.items() if v.get(k) != x)

def build_verifyos_sequential_epistemic_observation_verification_handoff(
    *, source_observability_receipt: Mapping[str, Any],
    expected_source_observability_receipt_digest: str,
    independent_verification_request: Mapping[str, Any],
    expected_independent_verification_request_digest: str,
    verification_handoff_review: Mapping[str, Any],
    expected_verification_handoff_review_digest: str,
    verification_handoff_context: Mapping[str, Any],
    expected_verification_handoff_context_digest: str,
    verification_handoff_policy_digest: str,
    verifyos_responsibility_digest: str,
    verification_handoff_id: str,
    verification_handoff_bundle_digest: str,
) -> Result:
    s, q, r, c = map(mapping, (
        source_observability_receipt, independent_verification_request,
        verification_handoff_review, verification_handoff_context,
    ))
    blockers: list[str] = []
    if not all((s, q, r, c)):
        return Result(STATUS_BLOCKED, ["verification_handoff_input_missing"], None)

    sd = s.get(SRC_RECEIPT_DIGEST, "")
    qd = q.get(REQUEST_DIGEST_FIELD, "")
    rd = r.get(REVIEW_DIGEST_FIELD, "")
    cd = c.get(CONTEXT_DIGEST_FIELD, "")
    checks = (
        (sd == digest_without(s, SRC_RECEIPT_DIGEST), "source_receipt_digest_mismatch"),
        (sd == expected_source_observability_receipt_digest, "source_expected_binding_mismatch"),
        (set(q) == REQUEST_FIELDS, "request_schema_invalid"),
        (qd == request_digest(q), "independent_verification_request_digest_mismatch"),
        (qd == expected_independent_verification_request_digest, "request_expected_binding_mismatch"),
        (set(r) == REVIEW_FIELDS, "review_schema_invalid"),
        (rd == review_digest(r), "review_digest_mismatch"),
        (rd == expected_verification_handoff_review_digest, "review_expected_binding_mismatch"),
        (set(c) == CONTEXT_FIELDS, "context_schema_invalid"),
        (cd == context_digest(c), "context_digest_mismatch"),
        (cd == expected_verification_handoff_context_digest, "context_expected_binding_mismatch"),
    )
    blockers.extend(name for ok, name in checks if not ok)
    _exact(s, {
        "kernel": "ObserveOS Sequential Epistemic Observability Envelope Kernel",
        "kernel_version": "v0.1", "observeos_version": "v0.7",
        "status": "OBSERVEOS_SEQUENTIAL_EPISTEMIC_OBSERVABILITY_ROUTED",
        "verification_completed": False, "verification_debt_open": True,
        "persistent_world_state_changed_by_observability": False,
        "world_model_revision_incremented_by_observability": False,
        "current_plan_revised_by_observability": False,
        "current_policy_activated_by_observability": False,
        "learning_delta_activated_by_observability": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "generalized_truth_claimed": False, "causal_verification_claimed": False,
        "verification_authority_granted_to_observeos": False,
        "world_mutation_authority_granted": False,
        "policy_activation_authority_granted": False,
        "execution_authority_granted": False,
        "history_read_only": True, "future_only": True, "active_now": False,
    }, "source", blockers)
    _exact(q, {
        "source_observability_receipt_digest": sd,
        "source_observation_receipt_digest": s.get("source_observation_receipt_digest"),
        "source_observability_packet_digest": s.get(SRC_PACKET_DIGEST),
        "source_observability_policy_digest": s.get(SRC_POLICY_DIGEST),
        "trace_id": s.get("trace_id"), "span_id": s.get("span_id"),
        "collector_id": s.get("collector_id"),
        "source_evidence_source_id": s.get("evidence_source_id"),
    }, "request", blockers)
    _exact(r, {"source_observability_receipt_digest": sd, REQUEST_DIGEST_FIELD: qd}, "review", blockers)
    _exact(c, {
        "source_observability_receipt_digest": sd, REQUEST_DIGEST_FIELD: qd,
        REVIEW_DIGEST_FIELD: rd, "source_world_revision": s.get("resulting_world_revision"),
    }, "context", blockers)

    if s.get("source_world_revision") != s.get("resulting_world_revision"):
        blockers.append("source_world_revision_mismatch")
    for field in ("source_lineage_digests", "resulting_lineage_digests",
                  "source_responsibility_lineage_digests", "resulting_responsibility_lineage_digests"):
        if not strings(s.get(field))[0]: blockers.append(f"{field}_invalid")
    for field in ("evidence_snapshot_digests", "independent_evidence_source_ids", "verification_scope"):
        if not strings(q.get(field))[0]: blockers.append(f"{field}_invalid")
    for field in ("prior_handoff_session_ids", "prior_handoff_nonce_digests",
                  "prior_verification_request_digests", "prior_handoff_review_digests",
                  "prior_source_observability_receipt_digests"):
        if not strings(c.get(field), True)[0]: blockers.append(f"{field}_invalid")
    if c.get("requested_verification_handoff_operation_digest") != operation_digest(s, q, r):
        blockers.append("operation_digest_mismatch")
    if c.get("exact_verification_handoff_cycle_digest") != cycle_digest(s, q, r, c):
        blockers.append("cycle_digest_mismatch")
    if any(not isinstance(x, str) or not x for x in (
        verification_handoff_policy_digest, verifyos_responsibility_digest, verification_handoff_id
    )): blockers.append("handoff_metadata_invalid")

    source_supported = all((
        s.get("observability_disposition") == SRC_SUPPORTED,
        s.get("observability_state_after") == SRC_STATE,
        s.get("sequential_epistemic_observability_envelope_recorded") is True,
        s.get("trace_context_valid") is True,
        s.get("signal_coverage_complete") is True,
        s.get("provenance_bound") is True,
        s.get("sample_accounting_confirmed") is True,
        s.get("missingness_within_policy") is True,
        s.get("distribution_shift_detected") is False,
        s.get("sequential_uncertainty_bound") is True,
        s.get("conformal_calibration_bound") is True,
        s.get("observation_window_valid") is True,
        s.get("replay_closed") is True,
    ))
    q_window = _duration(q, "request_prepared_epoch", "request_expires_epoch", "maximum_request_lifetime")
    r_current = _duration(r, "review_started_epoch", "review_completed_epoch", "maximum_review_duration")
    c_current = all(nat(c.get(x)) for x in (
        "source_observation_completed_epoch", "handoff_intake_epoch", "maximum_handoff_intake_delay"
    )) and c["source_observation_completed_epoch"] <= c["handoff_intake_epoch"] and (
        c["handoff_intake_epoch"] - c["source_observation_completed_epoch"] <= c["maximum_handoff_intake_delay"]
    )
    min_sources = q.get("minimum_independent_evidence_sources")
    min_attempts = q.get("minimum_reproduction_attempts")
    attempts = q.get("planned_reproduction_attempts")
    independence = all((
        q.get("verifier_independence_declared") is True,
        isinstance(q.get("verifier_id"), str), bool(q.get("verifier_id")),
        q.get("verifier_id") not in {q.get("collector_id"), q.get("source_evidence_source_id")},
        r.get("reviewer_id") not in {q.get("verifier_id"), q.get("collector_id")},
        pos(min_sources), len(q.get("independent_evidence_source_ids", [])) >= min_sources if pos(min_sources) else False,
    ))
    reproduction = pos(min_attempts) and nat(attempts) and attempts >= min_attempts
    replay = any((
        c.get("handoff_session_id") in c.get("prior_handoff_session_ids", []),
        c.get("handoff_nonce_digest") in c.get("prior_handoff_nonce_digests", []),
        qd in c.get("prior_verification_request_digests", []),
        rd in c.get("prior_handoff_review_digests", []),
        sd in c.get("prior_source_observability_receipt_digests", []),
    ))
    world_current = c.get("current_world_revision") == s.get("resulting_world_revision")
    computed_bundle = bundle_digest(
        source_observability_receipt_digest=sd,
        independent_verification_request_digest=qd,
        verification_handoff_review_digest=rd,
        verification_handoff_context_digest=cd,
        requested_verification_handoff_operation_digest=c.get("requested_verification_handoff_operation_digest"),
        exact_verification_handoff_cycle_digest=c.get("exact_verification_handoff_cycle_digest"),
        verification_handoff_policy_digest=verification_handoff_policy_digest,
        verifyos_responsibility_digest=verifyos_responsibility_digest,
        verification_handoff_id=verification_handoff_id,
    )
    if computed_bundle != verification_handoff_bundle_digest:
        blockers.append("verification_handoff_bundle_digest_mismatch")
    if blockers:
        return Result(STATUS_BLOCKED, sorted(set(blockers)), None)

    if replay: disposition = D_REPLAY
    elif not source_supported: disposition = D_SOURCE
    elif not r.get("source_observability_correspondence_confirmed") or not r.get("observability_supported_confirmed"): disposition = D_CORRESPONDENCE
    elif not world_current: disposition = D_WORLD
    elif not c_current: disposition = D_CONTEXT
    elif not r_current: disposition = D_REVIEW
    elif not q_window or not r.get("request_window_valid"): disposition = D_WINDOW
    elif not independence or not r.get("verifier_independence_adequate"): disposition = D_INDEPENDENCE
    elif not q.get("evidence_snapshot_digests") or not r.get("evidence_snapshot_adequate"): disposition = D_SNAPSHOT
    elif not r.get("verification_protocol_adequate"): disposition = D_PROTOCOL
    elif not r.get("acceptance_criteria_adequate"): disposition = D_ACCEPTANCE
    elif not reproduction or not r.get("reproduction_plan_adequate"): disposition = D_REPRODUCTION
    elif any((q.get("observation_recollection_requested"), q.get("current_state_mutation_requested"),
              not r.get("no_observation_recollection"), not r.get("no_current_state_mutation"))): disposition = D_MUTATION
    elif any((q.get("authority_escalation_requested"), q.get("verification_completion_claimed"),
              not r.get("no_authority_escalation"), not r.get("no_verification_completion_claim"))): disposition = D_AUTHORITY
    else: disposition = D_SUPPORTED

    supported = disposition == D_SUPPORTED
    lineage = sorted(set(s["resulting_lineage_digests"]) | {sd, qd, rd, cd, verification_handoff_bundle_digest})
    responsibility = sorted(set(s["resulting_responsibility_lineage_digests"]) | {verifyos_responsibility_digest})
    receipt = {
        "kernel": "VerifyOS Sequential Epistemic Observation Verification Handoff Kernel",
        "kernel_version": "v0.1", "verifyos_version": "v0.13",
        "status": "VERIFYOS_SEQUENTIAL_EPISTEMIC_VERIFICATION_HANDOFF_ROUTED",
        "source_observability_receipt_digest": sd, REQUEST_DIGEST_FIELD: qd,
        REVIEW_DIGEST_FIELD: rd, CONTEXT_DIGEST_FIELD: cd,
        "verification_handoff_policy_digest": verification_handoff_policy_digest,
        "verifyos_responsibility_digest": verifyos_responsibility_digest,
        "verification_handoff_id": verification_handoff_id,
        "verification_handoff_bundle_digest": verification_handoff_bundle_digest,
        "verification_handoff_disposition": disposition,
        "verification_handoff_state_before": SRC_STATE,
        "verification_handoff_state_after": STATE_AFTER if supported else SRC_STATE,
        "source_observability_envelope_recorded": s["sequential_epistemic_observability_envelope_recorded"],
        "verifier_independence_confirmed": supported,
        "evidence_snapshot_bound": supported, "verification_protocol_bound": supported,
        "acceptance_criteria_bound": supported, "reproduction_plan_bound": supported,
        "verification_request_recorded": supported,
        "independent_verification_handoff_prepared": supported,
        "verification_completed": False, "verification_debt_open": True,
        "observation_recollected_by_handoff": False,
        "persistent_world_state_changed_by_handoff": False,
        "world_model_revision_incremented_by_handoff": False,
        "current_plan_revised_by_handoff": False,
        "current_policy_activated_by_handoff": False,
        "learning_delta_activated_by_handoff": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "generalized_truth_claimed": False, "causal_verification_claimed": False,
        "selection_authority_granted_to_verifyos": False,
        "world_mutation_authority_granted": False,
        "policy_activation_authority_granted": False,
        "execution_authority_granted": False,
        "history_read_only": True, "future_only": True, "active_now": False,
        "source_world_revision": s["resulting_world_revision"],
        "resulting_world_revision": s["resulting_world_revision"],
        "source_lineage_digests": s["resulting_lineage_digests"],
        "resulting_lineage_digests": lineage,
        "source_responsibility_lineage_digests": s["resulting_responsibility_lineage_digests"],
        "resulting_responsibility_lineage_digests": responsibility,
        "verifier_id": q["verifier_id"], "reviewer_id": r["reviewer_id"],
        "verification_scope": q["verification_scope"],
        "evidence_snapshot_digests": q["evidence_snapshot_digests"],
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return Result(STATUS_READY, [], receipt)

VerifyOSSequentialEpistemicVerificationHandoffResult = Result
compute_independent_verification_request_digest = request_digest
compute_independent_verification_handoff_review_digest = review_digest
compute_independent_verification_handoff_context_digest = context_digest
compute_requested_verification_handoff_operation_digest = operation_digest
compute_exact_verification_handoff_cycle_digest = cycle_digest
compute_verification_handoff_bundle_digest = bundle_digest
DISPOSITION_SUPPORTED = D_SUPPORTED
DISPOSITION_SOURCE_REPAIR = D_SOURCE
DISPOSITION_CORRESPONDENCE_REPAIR = D_CORRESPONDENCE
DISPOSITION_WORLD_REFRESH = D_WORLD
DISPOSITION_CONTEXT_REFRESH = D_CONTEXT
DISPOSITION_REVIEW_REFRESH = D_REVIEW
DISPOSITION_INDEPENDENCE_REPAIR = D_INDEPENDENCE
DISPOSITION_EVIDENCE_SNAPSHOT_REPAIR = D_SNAPSHOT
DISPOSITION_PROTOCOL_REPAIR = D_PROTOCOL
DISPOSITION_ACCEPTANCE_REPAIR = D_ACCEPTANCE
DISPOSITION_REPRODUCTION_REPAIR = D_REPRODUCTION
DISPOSITION_WINDOW_REPAIR = D_WINDOW
DISPOSITION_REPLAY_REJECTED = D_REPLAY
DISPOSITION_CURRENT_STATE_MUTATION_REJECTED = D_MUTATION
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = D_AUTHORITY
