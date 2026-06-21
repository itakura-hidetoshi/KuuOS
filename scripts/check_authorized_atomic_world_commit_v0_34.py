from __future__ import annotations

from pathlib import Path
import json
import tempfile

from runtime.kuuos_authorized_atomic_world_commit_entry_v0_34 import (
    ZERO_DIGEST,
    build_authorized_world_commit_request,
    commit_world_fragment_atomic,
    initialize_world_store,
    make_initial_world_store,
    make_world_commit_authorization_receipt,
    validate_atomic_world_commit_receipt,
    validate_world_store,
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
from runtime.kuuos_verifyos_world_adoption_entry_v0_33 import (
    build_verifyos_request,
    build_world_disposition_candidate,
    make_verification_protocol_receipt,
    make_verification_receipt,
)


def build_adopt_candidate(*, suffix: str, prior_fragment: str):
    state = make_initial_state(
        agency_id=f"v034-check-{suffix}",
        root_lineage_digest="a" * 64,
        created_at_ms=100,
    )
    item_id = f"world-item-{suffix}"
    packet = make_world_evidence_packet(
        packet_id=f"v034-packet-{suffix}",
        source_state_digest=state["body_digest"],
        world_fragment_digest=prior_fragment,
        observed_at_ms=110,
        unresolved_items=[{
            "item_id": item_id,
            "question": "Should this WORLD fragment be updated?",
            "severity": 3,
            "uncertainty": 4,
            "evidence_refs": ["evidence:prior"],
            "counterevidence_refs": ["counterevidence:prior"],
        }],
        observation_channels=[{
            "channel_id": "structured-observer",
            "modality": "structured-observation",
            "supports_items": [item_id],
            "cost_class": "LOW",
            "risk_class": "LOW",
            "latency_class": "SHORT",
        }],
    )
    report = build_mission_observation_report(state, packet, generated_at_ms=120)
    observation_id = report["body"]["observation_portfolio"][0]["observation_candidate_id"]
    observe_authorization = make_observation_authorization_receipt(
        authorization_id=f"observe-auth-{suffix}",
        source_report_envelope=report,
        observation_candidate_id=observation_id,
        tool_id="tool.structured-observer.v1",
        scope_digest="c" * 64,
        host_license_digest="d" * 64,
        issued_by="external-observation-governance",
        issued_at_ms=130,
        not_before_ms=140,
        expires_at_ms=250,
    )
    observe_request = build_authorized_observe_request(
        report,
        observe_authorization,
        requested_at_ms=150,
    )
    evidence = make_observation_evidence_receipt(
        observe_request,
        evidence_id=f"evidence-{suffix}",
        collected_at_ms=160,
        raw_artifact_digest="1" * 64,
        value_digest="2" * 64,
        collector_identity="collector-primary",
        independent_source_identity="independent-source",
        uncertainty_digest="3" * 64,
        calibration_digest="4" * 64,
        context_digest="5" * 64,
        tamper_evidence_digest="6" * 64,
        provenance_chain_digest="7" * 64,
        relation="SUPPORTS",
    )
    feedback = build_world_feedback_candidate(report, evidence, generated_at_ms=170)
    protocol = make_verification_protocol_receipt(
        protocol_id=f"verify-protocol-{suffix}",
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
        issued_at_ms=180,
        not_before_ms=190,
        expires_at_ms=300,
    )
    verify_request = build_verifyos_request(
        feedback,
        evidence,
        protocol,
        requested_at_ms=200,
    )
    verification = make_verification_receipt(
        verify_request,
        verification_id=f"verification-{suffix}",
        completed_at_ms=210,
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
        generated_at_ms=220,
    )
    assert disposition["body"]["route"] == "ADOPT_CANDIDATE"
    return disposition


def authorize_and_request(
    disposition,
    *,
    authorization_id: str,
    expected_generation: int,
    expected_prior_commit_digest: str,
    fencing_token: int,
    lease_epoch: int,
):
    authorization = make_world_commit_authorization_receipt(
        authorization_id=authorization_id,
        source_disposition_envelope=disposition,
        world_store_id="world-store-main",
        expected_generation=expected_generation,
        expected_prior_commit_digest=expected_prior_commit_digest,
        fencing_token=fencing_token,
        lease_epoch=lease_epoch,
        scope_digest="1" * 64,
        host_license_digest="2" * 64,
        issued_by="external-world-governance",
        issued_at_ms=230,
        not_before_ms=240,
        expires_at_ms=400,
    )
    request = build_authorized_world_commit_request(
        disposition,
        authorization,
        requested_at_ms=250,
    )
    return authorization, request


def main() -> int:
    first = build_adopt_candidate(suffix="one", prior_fragment="b" * 64)
    first_authorization, first_request = authorize_and_request(
        first,
        authorization_id="world-commit-auth-one",
        expected_generation=0,
        expected_prior_commit_digest=ZERO_DIGEST,
        fencing_token=1,
        lease_epoch=1,
    )
    with tempfile.TemporaryDirectory() as tmp:
        store_path = Path(tmp) / "world-store.json"
        initial_store = make_initial_world_store(
            world_store_id="world-store-main",
            root_lineage_digest=first["body"]["root_lineage_digest"],
            current_world_fragment_digest=first["body"]["prior_world_fragment_digest"],
            created_at_ms=225,
        )
        initialize_world_store(store_path=store_path, store_envelope=initial_store)
        first_result = commit_world_fragment_atomic(
            store_path=store_path,
            source_disposition_envelope=first,
            authorization_envelope=first_authorization,
            request_envelope=first_request,
            committed_at_ms=260,
        )
        replay = commit_world_fragment_atomic(
            store_path=store_path,
            source_disposition_envelope=first,
            authorization_envelope=first_authorization,
            request_envelope=first_request,
            committed_at_ms=999,
        )
        first_receipt = validate_atomic_world_commit_receipt(first_result.receipt)
        first_store = validate_world_store(first_result.store)
        assert first_result.status == "COMMITTED"
        assert replay.status == "REPLAYED"
        assert replay.receipt["body_digest"] == first_result.receipt["body_digest"]
        assert first_store["generation"] == 1
        assert first_store["current_world_fragment_digest"] == first["body"]["candidate_world_fragment_digest"]
        assert first_receipt["constitutional_root_rewritten"] is False
        assert first_receipt["memory_history_overwritten"] is False
        assert first_receipt["automatic_rollback_performed"] is False
        assert first_receipt["open_horizon_preserved"] is True
        assert first_receipt["global_generation_limit"] is None

        second = build_adopt_candidate(
            suffix="two",
            prior_fragment=first_store["current_world_fragment_digest"],
        )
        second_authorization, second_request = authorize_and_request(
            second,
            authorization_id="world-commit-auth-two",
            expected_generation=1,
            expected_prior_commit_digest=first_result.receipt["body_digest"],
            fencing_token=2,
            lease_epoch=1,
        )
        second_result = commit_world_fragment_atomic(
            store_path=store_path,
            source_disposition_envelope=second,
            authorization_envelope=second_authorization,
            request_envelope=second_request,
            committed_at_ms=261,
        )
        second_store = validate_world_store(second_result.store)
        assert second_result.status == "COMMITTED"
        assert second_store["generation"] == 2
        assert len(second_store["commits"]) == 2
        assert second_result.receipt["body"]["previous_commit_digest"] == first_result.receipt["body_digest"]
        assert second_result.receipt["body"]["previous_world_fragment_digest"] == first_store["current_world_fragment_digest"]

        print(json.dumps({
            "status": "AUTHORIZED_ATOMIC_WORLD_COMMIT_V0_34_OK",
            "first_commit_receipt_digest": first_result.receipt["body_digest"],
            "second_commit_receipt_digest": second_result.receipt["body_digest"],
            "world_store_digest": second_result.store["body_digest"],
            "generation": second_store["generation"],
            "history_entries": len(second_store["commits"]),
            "open_horizon_preserved": second_store["open_horizon_preserved"],
            "global_generation_limit": second_store["global_generation_limit"],
            "constitutional_root_immutable": second_store["constitutional_root_immutable"],
        }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
