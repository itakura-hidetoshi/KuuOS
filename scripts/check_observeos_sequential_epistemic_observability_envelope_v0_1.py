#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import runtime.kuuos_observeos_sequential_epistemic_observability_envelope_v0_1 as m

def seal(value: dict, field: str) -> dict:
    out = deepcopy(value); out.pop(field, None); out[field] = m.canonical_digest(out); return out

def source() -> dict:
    return seal({
        "maintenance_monitoring_observation_recorded": True,
        "maintenance_monitoring_observation_scope_exactly_bounded": True,
        "verification_completed": False, "verification_debt_open": True,
        "persistent_world_state_changed_by_observation": False,
        "world_model_revision_incremented_by_observation": False,
        "current_plan_revised_by_observation": False,
        "current_policy_activated_by_observation": False,
        "learning_delta_activated_by_observation": False,
        "tool_invocation_performed": False, "external_side_effect_performed": False,
        "history_read_only": True, "future_only": True, "active_now": False,
        "resulting_world_revision": 41, "resulting_lineage_digests": ["lineage-source"],
        "resulting_responsibility_lineage_digests": ["responsibility-source"],
    }, m.SOURCE_RECEIPT_DIGEST_FIELD)

def policy() -> dict:
    return seal({
        "required_signals": ["logs", "metrics", "traces"], "minimum_observed_samples": 80,
        "maximum_missing_fraction_ppm": 100_000, "maximum_observation_duration": 3_600,
        "maximum_conformal_coverage_gap_ppm": 20_000, "require_w3c_trace_context": True,
        "require_prov_o_bundle": True, "require_anytime_valid_uncertainty": True,
        "require_conformal_calibration": True,
    }, m.POLICY_DIGEST_FIELD)

def packet(source_digest: str) -> dict:
    provenance = seal({"profile": "W3C-PROV-O", "entity_digests": ["entity-1"],
        "activity_digests": ["activity-1"], "agent_digests": ["agent-1"],
        "relation_digests": ["wasGeneratedBy:entity-1:activity-1"]}, m.PROVENANCE_DIGEST_FIELD)
    sequential = seal({"method": "confidence_sequence", "alpha_ppm": 50_000,
        "lower_bound_ppm": 420_000, "upper_bound_ppm": 580_000,
        "e_process_log_digest": "e-process-log", "stopping_rule_predeclared": True}, m.SEQUENTIAL_DIGEST_FIELD)
    conformal = seal({"method": "split_conformal", "target_coverage_ppm": 900_000,
        "empirical_coverage_ppm": 895_000, "calibration_sample_count": 200,
        "exchangeability_scope_digest": "exchangeability-scope"}, m.CONFORMAL_DIGEST_FIELD)
    drift = seal({"detector": "ADWIN", "window_size": 256, "delta_ppm": 1_000,
        "change_detected": False, "detector_state_digest": "adwin-state"}, m.DRIFT_DIGEST_FIELD)
    return seal({
        "source_observation_receipt_digest": source_digest,
        "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01",
        "tracestate": "kuuos=observeos-v0.7", "trace_id": "0af7651916cd43dd8448eb211c80319c",
        "span_id": "b7ad6b7169203331", "trace_flags": "01",
        "signals": ["baggage", "logs", "metrics", "traces"],
        "resource_attributes_digest": "resource-attributes",
        "semantic_conventions_schema_url": "https://opentelemetry.io/schemas/1.38.0",
        "provenance_bundle": provenance, "sequential_uncertainty": sequential,
        "conformal_calibration": conformal, "distribution_shift_evidence": drift,
        "sampling_policy_digest": "sampling-policy", "missingness_policy_digest": "missingness-policy",
        "raw_artifact_digests": ["artifact-1", "artifact-2"], "total_samples": 100,
        "observed_samples": 95, "missing_samples": 5, "observation_started_epoch": 1_000,
        "observation_completed_epoch": 1_600, "collector_id": "collector-independent-1",
        "evidence_source_id": "source-independent-1", "session_id": "session-1",
        "nonce_digest": "nonce-1", "prior_session_ids": [], "prior_nonce_digests": [],
        "prior_packet_digests": [], "telemetry_collection_performed_by_kernel": False,
        "persistent_world_state_changed": False, "world_model_revision_incremented": False,
        "current_plan_revised": False, "current_policy_activated": False,
        "learning_delta_activated": False, "tool_invocation_performed": False,
        "external_side_effect_performed": False, "generalized_truth_claimed": False,
        "causal_verification_claimed": False, "authority_escalation_claimed": False,
    }, m.PACKET_DIGEST_FIELD)

def route(src: dict, pkt: dict, pol: dict) -> dict:
    result = m.build_observeos_sequential_epistemic_observability_envelope(
        source_observation_receipt=src,
        expected_source_observation_receipt_digest=src[m.SOURCE_RECEIPT_DIGEST_FIELD],
        observability_packet=pkt, observability_policy=pol)
    assert result.status == m.STATUS_READY and result.receipt is not None, result
    receipt = result.receipt
    assert receipt[m.RECEIPT_DIGEST_FIELD] == m.canonical_digest({k:v for k,v in receipt.items() if k != m.RECEIPT_DIGEST_FIELD})
    return receipt

def reseal(pkt: dict) -> dict: return seal(pkt, m.PACKET_DIGEST_FIELD)

def main() -> None:
    src, pol = source(), policy(); base = packet(src[m.SOURCE_RECEIPT_DIGEST_FIELD])
    ok = route(src, base, pol)
    assert ok["observability_disposition"] == m.DISPOSITION_SUPPORTED
    assert ok["sequential_epistemic_observability_envelope_recorded"] is True
    assert ok["verification_completed"] is False and ok["verification_debt_open"] is True
    assert ok["source_world_revision"] == ok["resulting_world_revision"]
    assert set(ok["source_lineage_digests"]) <= set(ok["resulting_lineage_digests"])
    assert ok["persistent_world_state_changed_by_observability"] is False
    assert ok["execution_authority_granted"] is False

    def mutate(field: str, value):
        x = deepcopy(base); x[field] = value; return reseal(x)
    cases: list[tuple[str, dict, dict]] = []
    bad_src = deepcopy(src); bad_src["maintenance_monitoring_observation_recorded"] = False
    bad_src = seal(bad_src, m.SOURCE_RECEIPT_DIGEST_FIELD)
    bound = deepcopy(base); bound["source_observation_receipt_digest"] = bad_src[m.SOURCE_RECEIPT_DIGEST_FIELD]
    cases.append((m.DISPOSITION_SOURCE_REPAIR, bad_src, reseal(bound)))
    cases += [
        (m.DISPOSITION_TRACE_REPAIR, src, mutate("traceparent", "00-" + "0"*32 + "-" + "1"*16 + "-01")),
        (m.DISPOSITION_SIGNAL_REPAIR, src, mutate("signals", ["logs", "traces"])),
    ]
    x=deepcopy(base); v=deepcopy(x["provenance_bundle"]); v["profile"]="bad"; x["provenance_bundle"]=seal(v,m.PROVENANCE_DIGEST_FIELD); cases.append((m.DISPOSITION_PROVENANCE_REPAIR,src,reseal(x)))
    cases.append((m.DISPOSITION_SAMPLE_ACCOUNTING_REPAIR,src,mutate("missing_samples",6)))
    x=deepcopy(base); x["observed_samples"],x["missing_samples"]=80,20; cases.append((m.DISPOSITION_MISSINGNESS_REVIEW,src,reseal(x)))
    x=deepcopy(base); v=deepcopy(x["distribution_shift_evidence"]); v["change_detected"]=True; x["distribution_shift_evidence"]=seal(v,m.DRIFT_DIGEST_FIELD); cases.append((m.DISPOSITION_DISTRIBUTION_SHIFT_REVIEW,src,reseal(x)))
    x=deepcopy(base); v=deepcopy(x["sequential_uncertainty"]); v["stopping_rule_predeclared"]=False; x["sequential_uncertainty"]=seal(v,m.SEQUENTIAL_DIGEST_FIELD); cases.append((m.DISPOSITION_SEQUENTIAL_UNCERTAINTY_REPAIR,src,reseal(x)))
    x=deepcopy(base); v=deepcopy(x["conformal_calibration"]); v["empirical_coverage_ppm"]=850_000; x["conformal_calibration"]=seal(v,m.CONFORMAL_DIGEST_FIELD); cases.append((m.DISPOSITION_CONFORMAL_REPAIR,src,reseal(x)))
    cases += [
        (m.DISPOSITION_WINDOW_REPAIR,src,mutate("observation_completed_epoch",5_000)),
        (m.DISPOSITION_REPLAY_REJECTED,src,mutate("prior_session_ids",["session-1"])),
        (m.DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,src,mutate("current_plan_revised",True)),
        (m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,src,mutate("authority_escalation_claimed",True)),
    ]
    for expected, case_src, case_pkt in cases:
        assert route(case_src, case_pkt, pol)["observability_disposition"] == expected
    print("ObserveOS v0.7 sequential epistemic observability checks: PASS (14 routes)")

if __name__ == "__main__": main()
