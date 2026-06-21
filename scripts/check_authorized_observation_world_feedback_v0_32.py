from __future__ import annotations

import json

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
        agency_id="v032-check",
        root_lineage_digest="a" * 64,
        created_at_ms=1_000,
    )
    packet = make_world_evidence_packet(
        packet_id="v032-check-packet",
        source_state_digest=state["body_digest"],
        world_fragment_digest="b" * 64,
        observed_at_ms=1_010,
        unresolved_items=[
            {
                "item_id": "anomaly-1",
                "question": "Which WORLD interpretation explains the anomaly?",
                "severity": 3,
                "uncertainty": 4,
                "evidence_refs": ["observation:old-support"],
                "counterevidence_refs": ["observation:old-counter"],
            }
        ],
        observation_channels=[
            {
                "channel_id": "structured-observer",
                "modality": "structured-observation",
                "supports_items": ["anomaly-1"],
                "cost_class": "LOW",
                "risk_class": "LOW",
                "latency_class": "SHORT",
            }
        ],
    )
    report = build_mission_observation_report(state, packet, generated_at_ms=1_020)
    observation_id = report["body"]["observation_portfolio"][0]["observation_candidate_id"]
    authorization = make_observation_authorization_receipt(
        authorization_id="v032-auth-1",
        source_report_envelope=report,
        observation_candidate_id=observation_id,
        tool_id="tool.structured-observer.v1",
        scope_digest="c" * 64,
        host_license_digest="d" * 64,
        issued_by="external-governance",
        issued_at_ms=1_030,
        not_before_ms=1_040,
        expires_at_ms=1_100,
    )
    request = build_authorized_observe_request(
        report,
        authorization,
        requested_at_ms=1_050,
    )
    evidence = make_observation_evidence_receipt(
        request,
        evidence_id="v032-evidence-1",
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
        relation="CONTRADICTS",
    )
    feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=1_070)
    body = feedback["body"]
    assert request["body"]["single_use"] is True
    assert request["body"]["authorization_window_bound"] is True
    assert evidence["body"]["authorization_window_observed"] is True
    assert evidence["body"]["verification_required"] is True
    assert body["route"] == "WORLD_UPDATE_CANDIDATE"
    assert body["candidate_state"] == "CONTRADICTED_UPDATE_CANDIDATE"
    assert body["automatic_truth_promotion"] is False
    assert body["automatic_root_rewrite"] is False
    print(json.dumps({
        "status": "AUTHORIZED_OBSERVATION_WORLD_FEEDBACK_V0_32_OK",
        "authorization_digest": authorization["body_digest"],
        "request_digest": request["body_digest"],
        "evidence_digest": evidence["body_digest"],
        "feedback_digest": feedback["body_digest"],
        "route": body["route"],
        "candidate_state": body["candidate_state"],
        "verification_required": body["verification_required"],
        "candidate_not_truth": body["automatic_truth_promotion"] is False,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
