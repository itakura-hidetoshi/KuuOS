#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_observeos_dukkha_preserving_external_host_effect_observation_intake_v0_1 import (
    EVIDENCE_DIGEST_FIELD,
    OBSERVATION_OUTCOME,
    RECEIPT_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD,
    STATE_AFTER,
    STATUS_BLOCKED,
    STATUS_READY,
    build_observeos_dukkha_preserving_external_host_effect_observation_intake,
    canonical_digest,
    compute_exact_observation_cycle_digest,
    compute_external_host_effect_observation_bundle_digest,
    compute_independent_observation_evidence_packet_digest,
    compute_observation_intake_context_digest,
    compute_requested_observation_operation_digest,
)
from scripts.check_actos_dukkha_preserving_atomic_external_host_effect_intake_v0_1 import (
    _build as build_actos_v011_host_effect,
)


def _source_receipt() -> dict:
    result = build_actos_v011_host_effect()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _evidence(source: dict) -> dict:
    host_application = source["external_host_effect_application_receipt"]
    handoff = source["observation_handoff_envelope"]
    packet = {
        "source_host_effect_receipt_digest": source[SOURCE_DIGEST_FIELD],
        "external_host_effect_record_digest": source[
            "external_host_effect_record_digest"
        ],
        "observation_handoff_envelope_digest": source[
            "observation_handoff_envelope_digest"
        ],
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "requested_effect_tags": list(handoff["requested_effect_tags"]),
        "host_target_digest": host_application["host_target_digest"],
        "collector_id": "observeos-independent-collector-v005",
        "evidence_source_id": "observeos-independent-sensor-v005",
        "collection_started_epoch": 113,
        "collection_completed_epoch": 114,
        "maximum_collection_duration": 4,
        "raw_artifact_digest": "observeos-raw-artifact-v005",
        "observed_value_digest": "observeos-observed-value-v005",
        "uncertainty_digest": "observeos-uncertainty-v005",
        "calibration_digest": "observeos-calibration-v005",
        "observation_context_digest": "observeos-context-v005",
        "tamper_evidence_digest": "observeos-tamper-evidence-v005",
        "provenance_chain_digests": [
            "observeos-provenance-collector-v005",
            "observeos-provenance-sensor-v005",
        ],
        "collector_independent_from_host_driver": True,
        "evidence_source_independent_from_host_receipt": True,
        "exactly_one_observation": True,
        "observation_outcome": OBSERVATION_OUTCOME,
    }
    packet[EVIDENCE_DIGEST_FIELD] = (
        compute_independent_observation_evidence_packet_digest(packet)
    )
    return packet


def _redigest_evidence(source: dict, evidence: dict) -> dict:
    value = deepcopy(evidence)
    handoff = source["observation_handoff_envelope"]
    host_application = source["external_host_effect_application_receipt"]
    value["source_host_effect_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value["external_host_effect_record_digest"] = source[
        "external_host_effect_record_digest"
    ]
    value["observation_handoff_envelope_digest"] = source[
        "observation_handoff_envelope_digest"
    ]
    value["frontier_materialization_candidate_id"] = source[
        "invoked_frontier_candidate_id"
    ]
    value["frontier_adapter_id"] = source["invoked_frontier_adapter_id"]
    value["frontier_binding_digest"] = source["invoked_frontier_binding_digest"]
    value["requested_effect_tags"] = list(handoff["requested_effect_tags"])
    value.setdefault("host_target_digest", host_application["host_target_digest"])
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_independent_observation_evidence_packet_digest(value)
    )
    return value


def _context(source: dict, evidence: dict) -> dict:
    context = {
        "source_host_effect_receipt_digest": source[SOURCE_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: evidence[EVIDENCE_DIGEST_FIELD],
        "current_world_binding_digest": source["source_world_binding_digest"],
        "current_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "current_world_model_revision": source["source_world_model_revision"],
        "current_world_lineage_digest": source["source_world_lineage_digest"],
        "source_host_effect_receipt_observed_epoch": 114,
        "observation_intake_epoch": 115,
        "maximum_observation_intake_delay": 4,
        "observation_intake_session_id": "observeos-observation-intake-v005-001",
        "observation_intake_nonce_digest": "observeos-observation-nonce-v005-001",
        "prior_observation_intake_session_ids": [],
        "prior_observation_evidence_packet_digests": [],
        "prior_observation_intake_nonce_digests": [],
        "prior_observed_source_host_effect_receipt_digests": [],
        "requested_observation_operation_digest": (
            compute_requested_observation_operation_digest(source, evidence)
        ),
        "exact_observation_cycle_digest": "",
    }
    context["exact_observation_cycle_digest"] = compute_exact_observation_cycle_digest(
        source, evidence, context
    )
    context["observation_intake_context_digest"] = (
        compute_observation_intake_context_digest(context)
    )
    return context


def _redigest_context(source: dict, evidence: dict, context: dict) -> dict:
    value = deepcopy(context)
    value["source_host_effect_receipt_digest"] = source[SOURCE_DIGEST_FIELD]
    value[EVIDENCE_DIGEST_FIELD] = evidence[EVIDENCE_DIGEST_FIELD]
    value["requested_observation_operation_digest"] = (
        compute_requested_observation_operation_digest(source, evidence)
    )
    value["exact_observation_cycle_digest"] = compute_exact_observation_cycle_digest(
        source, evidence, value
    )
    value["observation_intake_context_digest"] = (
        compute_observation_intake_context_digest(value)
    )
    return value


def _build(**overrides):
    source_override = overrides.pop("source_host_effect_receipt", None)
    source = deepcopy(_source_receipt() if source_override is None else source_override)

    evidence_override = overrides.pop("independent_observation_evidence_packet", None)
    evidence = deepcopy(
        _evidence(source)
        if evidence_override is None and source
        else (evidence_override or {})
    )

    context_override = overrides.pop("observation_intake_context", None)
    context = deepcopy(
        _context(source, evidence)
        if context_override is None and source and evidence
        else (context_override or {})
    )

    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v011-missing")
    evidence_digest = evidence.get(EVIDENCE_DIGEST_FIELD, "evidence-v005-missing")
    context_digest = context.get(
        "observation_intake_context_digest", "context-v005-missing"
    )
    expected_source = overrides.pop(
        "expected_source_host_effect_receipt_digest", source_digest
    )
    expected_evidence = overrides.pop(
        "expected_independent_observation_evidence_packet_digest", evidence_digest
    )
    expected_context = overrides.pop(
        "expected_observation_intake_context_digest", context_digest
    )
    policy = overrides.pop(
        "observation_intake_policy_digest",
        "observeos-dukkha-preserving-observation-policy-v005",
    )
    owner = overrides.pop(
        "observeos_observation_responsibility_digest",
        "observeos-observation-owner-v005",
    )
    request_id = overrides.pop(
        "observation_intake_request_id",
        "observeos-external-host-effect-observation-v005-001",
    )
    bundle = overrides.pop(
        "external_host_effect_observation_bundle_digest",
        compute_external_host_effect_observation_bundle_digest(
            source_host_effect_receipt_digest=source_digest,
            expected_source_host_effect_receipt_digest=expected_source,
            external_host_effect_record_digest=source.get(
                "external_host_effect_record_digest", "host-record-missing"
            ),
            observation_handoff_envelope_digest=source.get(
                "observation_handoff_envelope_digest", "handoff-missing"
            ),
            independent_observation_evidence_packet_digest=evidence_digest,
            expected_independent_observation_evidence_packet_digest=(
                expected_evidence
            ),
            observation_intake_context_digest=context_digest,
            expected_observation_intake_context_digest=expected_context,
            requested_observation_operation_digest=context.get(
                "requested_observation_operation_digest", "operation-missing"
            ),
            exact_observation_cycle_digest=context.get(
                "exact_observation_cycle_digest", "cycle-missing"
            ),
            observation_intake_policy_digest=policy,
            observeos_observation_responsibility_digest=owner,
            observation_intake_request_id=request_id,
        ),
    )
    args = {
        "source_host_effect_receipt": source,
        "expected_source_host_effect_receipt_digest": expected_source,
        "independent_observation_evidence_packet": evidence,
        "expected_independent_observation_evidence_packet_digest": expected_evidence,
        "observation_intake_context": context,
        "expected_observation_intake_context_digest": expected_context,
        "observation_intake_policy_digest": policy,
        "observeos_observation_responsibility_digest": owner,
        "observation_intake_request_id": request_id,
        "external_host_effect_observation_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_observeos_dukkha_preserving_external_host_effect_observation_intake(
        **args
    )


def _assert_blocked(result, blocker: str) -> None:
    assert result.status == STATUS_BLOCKED
    assert result.receipt is None
    assert blocker in result.blockers, result.blockers


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["observation_state_after"] == STATE_AFTER
    assert receipt["observation_performed"] is True
    assert receipt["independent_world_evidence_present"] is True
    assert receipt["host_operation_reexecuted"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["persistent_world_model_state_unchanged"] is True
    assert receipt["world_fact_confirmed"] is False
    assert receipt["causal_attribution_confirmed"] is False
    assert receipt["verification_intake_admitted"] is True
    assert receipt["verification_completed"] is False
    assert receipt["verification_debt_open"] is True
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {k: v for k, v in receipt.items() if k != RECEIPT_DIGEST_FIELD}
    )

    _assert_blocked(
        _build(source_host_effect_receipt={}),
        "source_host_effect_receipt_missing",
    )
    _assert_blocked(
        _build(independent_observation_evidence_packet={}),
        "independent_observation_evidence_packet_missing",
    )
    _assert_blocked(
        _build(observation_intake_context={}),
        "observation_intake_context_missing",
    )
    _assert_blocked(
        _build(expected_source_host_effect_receipt_digest="wrong-source"),
        "source_host_effect_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(expected_independent_observation_evidence_packet_digest="wrong-evidence"),
        "independent_observation_evidence_expected_binding_mismatch",
    )
    _assert_blocked(
        _build(expected_observation_intake_context_digest="wrong-context"),
        "observation_intake_context_expected_binding_mismatch",
    )

    source = _source_receipt()
    source["world_fact_confirmed"] = True
    source = _redigest_source(source)
    _assert_blocked(
        _build(source_host_effect_receipt=source),
        "source_boundary_world_fact_confirmed_promoted",
    )

    source = _source_receipt()
    evidence = _evidence(source)
    evidence["collector_id"] = source["external_host_effect_application_receipt"][
        "host_driver_id"
    ]
    evidence = _redigest_evidence(source, evidence)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
        ),
        "observation_collector_not_independent_from_host_driver",
    )

    evidence = _evidence(source)
    evidence["host_target_digest"] = "wrong-target"
    evidence = _redigest_evidence(source, evidence)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
        ),
        "independent_observation_evidence_host_target_digest_mismatch",
    )

    evidence = _evidence(source)
    evidence["collection_completed_epoch"] = 130
    evidence = _redigest_evidence(source, evidence)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
        ),
        "independent_observation_collection_duration_invalid",
    )

    evidence = _evidence(source)
    context = _context(source, evidence)
    context["current_world_model_revision"] += 1
    context = _redigest_context(source, evidence, context)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
            observation_intake_context=context,
        ),
        "observation_world_refresh_required",
    )

    context = _context(source, evidence)
    context["prior_observation_intake_session_ids"] = [
        context["observation_intake_session_id"]
    ]
    context = _redigest_context(source, evidence, context)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
            observation_intake_context=context,
        ),
        "observation_intake_session_replay_rejected",
    )

    context = _context(source, evidence)
    context["prior_observation_evidence_packet_digests"] = [
        evidence[EVIDENCE_DIGEST_FIELD]
    ]
    context = _redigest_context(source, evidence, context)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
            observation_intake_context=context,
        ),
        "observation_evidence_packet_replay_rejected",
    )

    context = _context(source, evidence)
    context["prior_observation_intake_nonce_digests"] = [
        context["observation_intake_nonce_digest"]
    ]
    context = _redigest_context(source, evidence, context)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
            observation_intake_context=context,
        ),
        "observation_intake_nonce_replay_rejected",
    )

    context = _context(source, evidence)
    context["prior_observed_source_host_effect_receipt_digests"] = [
        source[SOURCE_DIGEST_FIELD]
    ]
    context = _redigest_context(source, evidence, context)
    _assert_blocked(
        _build(
            source_host_effect_receipt=source,
            independent_observation_evidence_packet=evidence,
            observation_intake_context=context,
        ),
        "source_host_effect_receipt_replay_rejected",
    )

    _assert_blocked(
        _build(external_host_effect_observation_bundle_digest="wrong-bundle"),
        "external_host_effect_observation_bundle_digest_mismatch",
    )

    print("ObserveOS dukkha-preserving external host-effect observation intake v0.1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
