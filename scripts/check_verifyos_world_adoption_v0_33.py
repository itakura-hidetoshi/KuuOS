from __future__ import annotations

import json

from runtime.kuuos_verifyos_world_adoption_entry_v0_33 import (
    build_verifyos_request,
    build_world_disposition_candidate,
    make_verification_protocol_receipt,
    make_verification_receipt,
)
from runtime.kuuos_authorized_observation_world_feedback_entry_v0_32 import (
    build_authorized_observe_request,
    build_world_feedback_candidate,
    make_observation_authorization_receipt,
    make_observation_evidence_receipt,
)
from runtime.kuuos_endogenous_mission_observation_v0_31 import (
    build_mission_observation_report,
    make_world_evidence_packet,
)
from runtime.kuuos_open_ended_background_agency_v0_30 import make_initial_state


def main() -> int:
    state = make_initial_state(
        agency_id="v033-check",
        root_lineage_digest="a" * 64,
        created_at_ms=1_000,
    )
    packet = make_world_evidence_packet(
        packet_id="v033-check-packet",
        source_state_digest=state["body_digest"],
        world_fragment_digest="b" * 64,
        observed_at_ms=1_010,
        unresolved_items=[
            {
                "item_id": "world-question-1",
                "question": "Does the proposed WORLD fragment survive independent challenge?",
                "severity": 3,
                "uncertainty": 4,
                "evidence_refs": ["observation:prior-support"],
                "counterevidence_refs": ["observation:prior-counter"],
            }
        ],
        observation_channels=[
            {
                "channel_id": "structured-observer",
                "modality": "structured-observation",
                "supports_items": ["world-question-1"],
                "cost_class": "LOW",
                "risk_class": "LOW",
                "latency_class": "SHORT",
            }
        ],
    )
    report = build_mission_observation_report(state, packet, generated_at_ms=1_020)
    observation_id = report["body"]["observation_portfolio"][0]["observation_candidate_id"]
    observation_authorization = make_observation_authorization_receipt(
        authorization_id="v033-observation-auth",
        source_report_envelope=report,
        observation_candidate_id=observation_id,
        tool_id="tool.structured-observer.v1",
        scope_digest="c" * 64,
        host_license_digest="d" * 64,
        issued_by="external-observation-governance",
        issued_at_ms=1_030,
        not_before_ms=1_040,
        expires_at_ms=1_100,
    )
    observe_request = build_authorized_observe_request(
        report,
        observation_authorization,
        requested_at_ms=1_050,
    )
    evidence = make_observation_evidence_receipt(
        observe_request,
        evidence_id="v033-evidence",
        collected_at_ms=1_060,
        raw_artifact_digest="1" * 64,
        value_digest="2" * 64,
        collector_identity="collector-a",
        independent_source_identity="source-a",
        uncertainty_digest="3" * 64,
        calibration_digest="4" * 64,
        context_digest="5" * 64,
        tamper_evidence_digest="6" * 64,
        provenance_chain_digest="7" * 64,
        relation="SUPPORTS",
    )
    feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=1_070)
    protocol = make_verification_protocol_receipt(
        protocol_id="v033-protocol",
        source_feedback_envelope=feedback,
        evidence_receipt_envelope=evidence,
        criterion_digest="8" * 64,
        evaluation_method_digest="9" * 64,
        success_condition_digest="a" * 64,
        failure_condition_digest="b" * 64,
        falsification_condition_digest="c" * 64,
        evidence_requirements_digest="d" * 64,
        assessor_policy_digest="e" * 64,
        host_license_digest="f" * 64,
        issued_by="external-verification-governance",
        issued_at_ms=1_080,
        not_before_ms=1_090,
        expires_at_ms=1_200,
    )
    verify_request = build_verifyos_request(
        feedback,
        evidence,
        protocol,
        requested_at_ms=1_100,
    )
    verification = make_verification_receipt(
        verify_request,
        verification_id="v033-verification",
        completed_at_ms=1_110,
        assessor_identity="assessor-primary",
        independent_assessor_identity="assessor-independent",
        assessment_artifact_digest="1" * 64,
        assessor_receipt_digest="2" * 64,
        challenge_record_digest="3" * 64,
        corroboration_record_digest="4" * 64,
        verdict="PASSED",
        source_matched=True,
        source_divergent=False,
        corroboration_admissible=True,
        criterion_satisfied=True,
        falsifier_triggered=False,
        assessor_independent=True,
        provenance_intact=True,
        method_reproducible=True,
        unresolved_conflict=False,
        reobservation_required=False,
    )
    disposition = build_world_disposition_candidate(
        feedback,
        verification,
        generated_at_ms=1_120,
    )
    body = disposition["body"]
    assert verification["body"]["verification_not_truth"] is True
    assert verification["body"]["verification_not_world_adoption"] is True
    assert verification["body"]["learning_future_only"] is True
    assert body["route"] == "ADOPT_CANDIDATE"
    assert body["disposition_is_candidate"] is True
    assert body["candidate_world_fragment_digest"] == body["proposed_world_fragment_digest"]
    assert body["governance_review_required"] is True
    assert body["world_commit_required_separately"] is True
    assert body["automatic_world_adoption"] is False
    assert body["automatic_world_commit"] is False
    assert body["automatic_root_rewrite"] is False
    print(json.dumps({
        "status": "VERIFYOS_WORLD_ADOPTION_V0_33_OK",
        "feedback_digest": feedback["body_digest"],
        "protocol_digest": protocol["body_digest"],
        "verify_request_digest": verify_request["body_digest"],
        "verification_receipt_digest": verification["body_digest"],
        "world_disposition_digest": disposition["body_digest"],
        "route": body["route"],
        "candidate_only": body["disposition_is_candidate"],
        "verification_not_truth": verification["body"]["verification_not_truth"],
        "world_commit_separate": body["world_commit_required_separately"],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
