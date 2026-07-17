#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy

from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import (
    DISPOSITION_SUPPORTED as SRC_SUPPORTED,
    PACKET_DIGEST_FIELD as SRC_PACKET_DIGEST,
    POLICY_DIGEST_FIELD as SRC_POLICY_DIGEST,
    RECEIPT_DIGEST_FIELD as SRC_RECEIPT_DIGEST,
    STATUS_BLOCKED, STATUS_READY, SUPPORTED_STATE as SRC_STATE, canonical_digest,
)
from runtime.kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1 import (
    CONTEXT_DIGEST_FIELD, RECEIPT_DIGEST_FIELD, REQUEST_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD, DISPOSITION_SUPPORTED, DISPOSITION_SOURCE_REPAIR,
    DISPOSITION_CORRESPONDENCE_REPAIR, DISPOSITION_WORLD_REFRESH,
    DISPOSITION_CONTEXT_REFRESH, DISPOSITION_REVIEW_REFRESH,
    DISPOSITION_INDEPENDENCE_REPAIR, DISPOSITION_EVIDENCE_SNAPSHOT_REPAIR,
    DISPOSITION_PROTOCOL_REPAIR, DISPOSITION_ACCEPTANCE_REPAIR,
    DISPOSITION_REPRODUCTION_REPAIR, DISPOSITION_WINDOW_REPAIR,
    DISPOSITION_REPLAY_REJECTED, DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
    DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
    build_verifyos_sequential_epistemic_observation_verification_handoff,
    compute_independent_verification_request_digest as request_digest,
    compute_independent_verification_handoff_review_digest as review_digest,
    compute_independent_verification_handoff_context_digest as context_digest,
    compute_requested_verification_handoff_operation_digest as operation_digest,
    compute_exact_verification_handoff_cycle_digest as cycle_digest,
    compute_verification_handoff_bundle_digest as bundle_digest,
)

POLICY = "verifyos-v0-13-policy"
RESPONSIBILITY = "verifyos-v0-13-responsibility"
HANDOFF_ID = "verify-handoff-001"

def source() -> dict:
    x = {
        "kernel": "ObserveOS Sequential Epistemic Observability Envelope Kernel",
        "kernel_version": "v0.1", "observeos_version": "v0.7",
        "status": "OBSERVEOS_SEQUENTIAL_EPISTEMIC_OBSERVABILITY_ROUTED",
        "source_observation_receipt_digest": "source-observation-receipt",
        SRC_PACKET_DIGEST: "observability-packet",
        SRC_POLICY_DIGEST: "observability-policy",
        "observability_disposition": SRC_SUPPORTED,
        "observability_state_before": "bounded-observation-recorded",
        "observability_state_after": SRC_STATE,
        "trace_context_valid": True, "signal_coverage_complete": True,
        "provenance_bound": True, "sample_accounting_confirmed": True,
        "missing_fraction_ppm": 1000, "missingness_within_policy": True,
        "distribution_shift_detected": False,
        "sequential_uncertainty_bound": True,
        "conformal_calibration_bound": True,
        "conformal_coverage_gap_ppm": 500,
        "observation_window_valid": True, "replay_closed": True,
        "sequential_epistemic_observability_envelope_recorded": True,
        "verification_completed": False, "verification_debt_open": True,
        "persistent_world_state_changed_by_observability": False,
        "world_model_revision_incremented_by_observability": False,
        "current_plan_revised_by_observability": False,
        "current_policy_activated_by_observability": False,
        "learning_delta_activated_by_observability": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "generalized_truth_claimed": False, "causal_verification_claimed": False,
        "selection_authority_granted_to_observeos": False,
        "verification_authority_granted_to_observeos": False,
        "world_mutation_authority_granted": False,
        "policy_activation_authority_granted": False,
        "execution_authority_granted": False,
        "history_read_only": True, "future_only": True, "active_now": False,
        "source_world_revision": 17, "resulting_world_revision": 17,
        "source_lineage_digests": ["lineage-a"],
        "resulting_lineage_digests": ["lineage-a", "observability-packet"],
        "source_responsibility_lineage_digests": ["responsibility-a"],
        "resulting_responsibility_lineage_digests": ["responsibility-a", "responsibility-observeos"],
        "total_samples": 100, "observed_samples": 99, "missing_samples": 1,
        "collector_id": "collector-a", "evidence_source_id": "source-a",
        "session_id": "observe-session-a", "nonce_digest": "observe-nonce-a",
        "trace_id": "0123456789abcdef0123456789abcdef",
        "span_id": "0123456789abcdef",
        "provenance_bundle_digest": "prov-a",
        "sequential_uncertainty_digest": "cs-a",
        "conformal_calibration_digest": "conformal-a",
        "distribution_shift_evidence_digest": "adwin-a",
    }
    x[SRC_RECEIPT_DIGEST] = canonical_digest(x)
    return x

def request(s: dict) -> dict:
    x = {
        "source_observability_receipt_digest": s[SRC_RECEIPT_DIGEST],
        "source_observation_receipt_digest": s["source_observation_receipt_digest"],
        "source_observability_packet_digest": s[SRC_PACKET_DIGEST],
        "source_observability_policy_digest": s[SRC_POLICY_DIGEST],
        "trace_id": s["trace_id"], "span_id": s["span_id"],
        "provenance_bundle_digest": s["provenance_bundle_digest"],
        "sequential_uncertainty_digest": s["sequential_uncertainty_digest"],
        "conformal_calibration_digest": s["conformal_calibration_digest"],
        "distribution_shift_evidence_digest": s["distribution_shift_evidence_digest"],
        "verification_protocol_digest": "protocol-a",
        "acceptance_criteria_digest": "criteria-a",
        "reproduction_plan_digest": "reproduction-a",
        "environment_snapshot_digest": "environment-a",
        "evidence_snapshot_digests": ["evidence-a", "evidence-b"],
        "independent_evidence_source_ids": ["independent-source-a"],
        "verification_scope": ["calibration", "correspondence", "distribution-shift", "reproduction", "uncertainty"],
        "verifier_id": "verifier-a", "collector_id": s["collector_id"],
        "source_evidence_source_id": s["evidence_source_id"],
        "minimum_independent_evidence_sources": 1,
        "minimum_reproduction_attempts": 1, "planned_reproduction_attempts": 2,
        "request_prepared_epoch": 120, "request_expires_epoch": 180,
        "maximum_request_lifetime": 120,
        "verifier_independence_declared": True, "blinded_review_required": True,
        "observation_recollection_requested": False,
        "current_state_mutation_requested": False,
        "authority_escalation_requested": False,
        "verification_completion_claimed": False,
    }
    x[REQUEST_DIGEST_FIELD] = request_digest(x)
    return x

def review(s: dict, q: dict) -> dict:
    x = {
        "source_observability_receipt_digest": s[SRC_RECEIPT_DIGEST],
        REQUEST_DIGEST_FIELD: q[REQUEST_DIGEST_FIELD],
        "reviewer_id": "reviewer-a", "review_method_digest": "review-method-a",
        "review_evidence_digest": "review-evidence-a",
        "review_started_epoch": 121, "review_completed_epoch": 123,
        "maximum_review_duration": 10,
        "source_observability_correspondence_confirmed": True,
        "observability_supported_confirmed": True,
        "trace_context_bound": True, "provenance_bound": True,
        "sample_accounting_bound": True, "sequential_uncertainty_bound": True,
        "conformal_calibration_bound": True, "distribution_shift_absent": True,
        "verifier_independence_adequate": True,
        "evidence_snapshot_adequate": True,
        "verification_protocol_adequate": True,
        "acceptance_criteria_adequate": True,
        "reproduction_plan_adequate": True, "request_window_valid": True,
        "no_observation_recollection": True, "no_current_state_mutation": True,
        "no_authority_escalation": True, "no_verification_completion_claim": True,
    }
    x[REVIEW_DIGEST_FIELD] = review_digest(x)
    return x

def context(s: dict, q: dict, r: dict) -> dict:
    x = {
        "source_observability_receipt_digest": s[SRC_RECEIPT_DIGEST],
        REQUEST_DIGEST_FIELD: q[REQUEST_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: r[REVIEW_DIGEST_FIELD],
        "source_world_revision": s["resulting_world_revision"],
        "current_world_revision": s["resulting_world_revision"],
        "source_observation_completed_epoch": 110, "handoff_intake_epoch": 124,
        "maximum_handoff_intake_delay": 20,
        "handoff_session_id": "handoff-session-a",
        "handoff_nonce_digest": "handoff-nonce-a",
        "prior_handoff_session_ids": [], "prior_handoff_nonce_digests": [],
        "prior_verification_request_digests": [], "prior_handoff_review_digests": [],
        "prior_source_observability_receipt_digests": [],
    }
    x["requested_verification_handoff_operation_digest"] = operation_digest(s, q, r)
    x["exact_verification_handoff_cycle_digest"] = cycle_digest(s, q, r, x)
    x[CONTEXT_DIGEST_FIELD] = context_digest(x)
    return x

def fixture() -> dict:
    s = source(); q = request(s); r = review(s, q); c = context(s, q, r)
    return {"source": s, "request": q, "review": r, "context": c}

def rebind(f: dict) -> None:
    s, q, r, c = f["source"], f["request"], f["review"], f["context"]
    s.pop(SRC_RECEIPT_DIGEST, None); s[SRC_RECEIPT_DIGEST] = canonical_digest(s)
    q.update({
        "source_observability_receipt_digest": s[SRC_RECEIPT_DIGEST],
        "source_observation_receipt_digest": s["source_observation_receipt_digest"],
        "source_observability_packet_digest": s[SRC_PACKET_DIGEST],
        "source_observability_policy_digest": s[SRC_POLICY_DIGEST],
        "trace_id": s["trace_id"], "span_id": s["span_id"],
        "collector_id": s["collector_id"], "source_evidence_source_id": s["evidence_source_id"],
    })
    q.pop(REQUEST_DIGEST_FIELD, None); q[REQUEST_DIGEST_FIELD] = request_digest(q)
    r["source_observability_receipt_digest"] = s[SRC_RECEIPT_DIGEST]
    r[REQUEST_DIGEST_FIELD] = q[REQUEST_DIGEST_FIELD]
    r.pop(REVIEW_DIGEST_FIELD, None); r[REVIEW_DIGEST_FIELD] = review_digest(r)
    c["source_observability_receipt_digest"] = s[SRC_RECEIPT_DIGEST]
    c[REQUEST_DIGEST_FIELD] = q[REQUEST_DIGEST_FIELD]
    c[REVIEW_DIGEST_FIELD] = r[REVIEW_DIGEST_FIELD]
    c["source_world_revision"] = s["resulting_world_revision"]
    c["requested_verification_handoff_operation_digest"] = operation_digest(s, q, r)
    c["exact_verification_handoff_cycle_digest"] = cycle_digest(s, q, r, c)
    c.pop(CONTEXT_DIGEST_FIELD, None); c[CONTEXT_DIGEST_FIELD] = context_digest(c)

def run(f: dict):
    rebind(f)
    s, q, r, c = f["source"], f["request"], f["review"], f["context"]
    b = bundle_digest(
        source_observability_receipt_digest=s[SRC_RECEIPT_DIGEST],
        independent_verification_request_digest=q[REQUEST_DIGEST_FIELD],
        verification_handoff_review_digest=r[REVIEW_DIGEST_FIELD],
        verification_handoff_context_digest=c[CONTEXT_DIGEST_FIELD],
        requested_verification_handoff_operation_digest=c["requested_verification_handoff_operation_digest"],
        exact_verification_handoff_cycle_digest=c["exact_verification_handoff_cycle_digest"],
        verification_handoff_policy_digest=POLICY,
        verifyos_responsibility_digest=RESPONSIBILITY,
        verification_handoff_id=HANDOFF_ID,
    )
    return build_verifyos_sequential_epistemic_observation_verification_handoff(
        source_observability_receipt=s,
        expected_source_observability_receipt_digest=s[SRC_RECEIPT_DIGEST],
        independent_verification_request=q,
        expected_independent_verification_request_digest=q[REQUEST_DIGEST_FIELD],
        verification_handoff_review=r,
        expected_verification_handoff_review_digest=r[REVIEW_DIGEST_FIELD],
        verification_handoff_context=c,
        expected_verification_handoff_context_digest=c[CONTEXT_DIGEST_FIELD],
        verification_handoff_policy_digest=POLICY,
        verifyos_responsibility_digest=RESPONSIBILITY,
        verification_handoff_id=HANDOFF_ID,
        verification_handoff_bundle_digest=b,
    )

def assert_route(name: str, mutate, expected: str) -> None:
    f = fixture(); mutate(f); result = run(f)
    assert result.status == STATUS_READY, (name, result.blockers)
    receipt = result.receipt; assert receipt is not None
    assert receipt["verification_handoff_disposition"] == expected
    assert receipt["verification_completed"] is False
    assert receipt["verification_debt_open"] is True
    assert receipt["persistent_world_state_changed_by_handoff"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["world_mutation_authority_granted"] is False
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest({
        k: v for k, v in receipt.items() if k != RECEIPT_DIGEST_FIELD
    })

def main() -> int:
    routes = (
        ("supported", lambda f: None, DISPOSITION_SUPPORTED),
        ("source", lambda f: (f["source"].__setitem__("observability_disposition", "trace_context_repair_required"), f["source"].__setitem__("sequential_epistemic_observability_envelope_recorded", False), f["source"].__setitem__("observability_state_after", "bounded-observation-recorded")), DISPOSITION_SOURCE_REPAIR),
        ("correspondence", lambda f: f["review"].__setitem__("source_observability_correspondence_confirmed", False), DISPOSITION_CORRESPONDENCE_REPAIR),
        ("world", lambda f: f["context"].__setitem__("current_world_revision", 18), DISPOSITION_WORLD_REFRESH),
        ("context", lambda f: f["context"].__setitem__("handoff_intake_epoch", 200), DISPOSITION_CONTEXT_REFRESH),
        ("review", lambda f: f["review"].__setitem__("review_completed_epoch", 200), DISPOSITION_REVIEW_REFRESH),
        ("independence", lambda f: f["review"].__setitem__("verifier_independence_adequate", False), DISPOSITION_INDEPENDENCE_REPAIR),
        ("snapshot", lambda f: f["review"].__setitem__("evidence_snapshot_adequate", False), DISPOSITION_EVIDENCE_SNAPSHOT_REPAIR),
        ("protocol", lambda f: f["review"].__setitem__("verification_protocol_adequate", False), DISPOSITION_PROTOCOL_REPAIR),
        ("acceptance", lambda f: f["review"].__setitem__("acceptance_criteria_adequate", False), DISPOSITION_ACCEPTANCE_REPAIR),
        ("reproduction", lambda f: f["review"].__setitem__("reproduction_plan_adequate", False), DISPOSITION_REPRODUCTION_REPAIR),
        ("window", lambda f: f["review"].__setitem__("request_window_valid", False), DISPOSITION_WINDOW_REPAIR),
        ("replay", lambda f: f["context"]["prior_handoff_session_ids"].append(f["context"]["handoff_session_id"]), DISPOSITION_REPLAY_REJECTED),
        ("mutation", lambda f: f["request"].__setitem__("current_state_mutation_requested", True), DISPOSITION_CURRENT_STATE_MUTATION_REJECTED),
        ("authority", lambda f: f["request"].__setitem__("authority_escalation_requested", True), DISPOSITION_AUTHORITY_ESCALATION_REJECTED),
    )
    for name, mutate, expected in routes: assert_route(name, mutate, expected)
    f = fixture(); rebind(f); f["request"][REQUEST_DIGEST_FIELD] = "broken"
    result = build_verifyos_sequential_epistemic_observation_verification_handoff(
        source_observability_receipt=f["source"],
        expected_source_observability_receipt_digest=f["source"][SRC_RECEIPT_DIGEST],
        independent_verification_request=f["request"],
        expected_independent_verification_request_digest="broken",
        verification_handoff_review=f["review"],
        expected_verification_handoff_review_digest=f["review"][REVIEW_DIGEST_FIELD],
        verification_handoff_context=f["context"],
        expected_verification_handoff_context_digest=f["context"][CONTEXT_DIGEST_FIELD],
        verification_handoff_policy_digest=POLICY,
        verifyos_responsibility_digest=RESPONSIBILITY,
        verification_handoff_id=HANDOFF_ID,
        verification_handoff_bundle_digest="broken",
    )
    assert result.status == STATUS_BLOCKED
    assert "independent_verification_request_digest_mismatch" in result.blockers
    print(f"VerifyOS v0.13 sequential epistemic verification handoff checks passed ({len(routes)} routes)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
