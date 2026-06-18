from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    READY as HOST_READY,
    RECEIPT_VERSION as HOST_RECEIPT_VERSION,
    receipt_digest as host_receipt_digest,
)
from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_observe_os_types_v0_1 import (
    APPLY_RESULT_VERSION,
    COMPARISON_RECEIPT_VERSION,
    COMPARISON_VERDICTS,
    EVENT_VERSION,
    NON_AUTHORITY_FLAGS,
    OBSERVE_PHASE_RECEIPT_VERSION,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    SOURCE_KINDS,
    STATE_VERSION,
    apply_result_digest,
    comparison_receipt_digest,
    copy_boundary,
    copy_non_authority,
    event_digest,
    next_phase,
    observe_phase_receipt_digest,
    require_bool,
    require_int,
    require_string,
    state_digest,
    unit_number,
    unique_strings,
)


def _digest_with_optional_supplied(
    packet: dict[str, Any], field: str, supplied: Any
) -> dict[str, Any]:
    packet[field] = ""
    expected = sha({key: value for key, value in packet.items() if key != field})
    packet[field] = expected
    if supplied not in (None, "", expected):
        raise ValueError(f"{field}_invalid")
    return packet


def _normalize_scope(
    state: Mapping[str, Any], raw: Mapping[str, Any]
) -> dict[str, Any]:
    target = require_string(raw.get("observation_target_digest"), "observation_target_digest")
    if target != state.get("expected_observation_digest"):
        raise ValueError("observation_target_substitution_forbidden")
    start = require_int(raw.get("window_start_ms"), "window_start_ms")
    end = require_int(raw.get("window_end_ms"), "window_end_ms")
    if end <= start:
        raise ValueError("observation_window_invalid")
    if start < int(state.get("source_act_updated_at_ms", 0)):
        raise ValueError("observation_window_precedes_effect_record")
    minimum = require_int(raw.get("minimum_evidence_items"), "minimum_evidence_items")
    if minimum < 1:
        raise ValueError("minimum_evidence_items_positive_required")
    scope = {
        "observation_target_digest": target,
        "observation_protocol_digest": require_string(
            raw.get("observation_protocol_digest"), "observation_protocol_digest"
        ),
        "window_start_ms": start,
        "window_end_ms": end,
        "channels": unique_strings(raw.get("channels"), "channels"),
        "minimum_evidence_items": minimum,
        "independence_required": require_bool(
            raw.get("independence_required"), "independence_required"
        ),
        "observer_context_digest": require_string(
            raw.get("observer_context_digest"), "observer_context_digest"
        ),
        "baseline_digest": require_string(raw.get("baseline_digest"), "baseline_digest"),
        "observation_scope_digest": "",
    }
    return _digest_with_optional_supplied(
        scope, "observation_scope_digest", raw.get("observation_scope_digest")
    )


def _normalize_evidence_item(
    scope: Mapping[str, Any], raw: Mapping[str, Any]
) -> dict[str, Any]:
    channel = require_string(raw.get("channel_id"), "channel_id")
    if channel not in set(scope.get("channels", [])):
        raise ValueError("evidence_channel_not_declared")
    collected = require_int(raw.get("collected_at_ms"), "collected_at_ms")
    if collected < int(scope["window_start_ms"]) or collected > int(
        scope["window_end_ms"]
    ):
        raise ValueError("evidence_outside_observation_window")
    source_kind = require_string(raw.get("source_kind"), "source_kind")
    if source_kind not in SOURCE_KINDS:
        raise ValueError("evidence_source_kind_invalid")
    item = {
        "evidence_id": require_string(raw.get("evidence_id"), "evidence_id"),
        "channel_id": channel,
        "source_kind": source_kind,
        "collector_id": require_string(raw.get("collector_id"), "collector_id"),
        "independent_source_id": require_string(
            raw.get("independent_source_id"), "independent_source_id"
        ),
        "collected_at_ms": collected,
        "raw_artifact_digest": require_string(
            raw.get("raw_artifact_digest"), "raw_artifact_digest"
        ),
        "value_digest": require_string(raw.get("value_digest"), "value_digest"),
        "uncertainty_digest": require_string(
            raw.get("uncertainty_digest"), "uncertainty_digest"
        ),
        "calibration_digest": require_string(
            raw.get("calibration_digest"), "calibration_digest"
        ),
        "context_digest": require_string(raw.get("context_digest"), "context_digest"),
        "tamper_evidence_digest": require_string(
            raw.get("tamper_evidence_digest"), "tamper_evidence_digest"
        ),
        "provenance_hop_digests": unique_strings(
            raw.get("provenance_hop_digests"), "provenance_hop_digests"
        ),
        "evidence_digest": "",
    }
    return _digest_with_optional_supplied(
        item, "evidence_digest", raw.get("evidence_digest")
    )


def _normalize_quality_report(raw: Mapping[str, Any]) -> dict[str, Any]:
    report = {
        "coverage": unit_number(raw.get("coverage"), "coverage"),
        "freshness": unit_number(raw.get("freshness"), "freshness"),
        "provenance": unit_number(raw.get("provenance"), "provenance"),
        "calibration": unit_number(raw.get("calibration"), "calibration"),
        "completeness": unit_number(raw.get("completeness"), "completeness"),
        "conflict": unit_number(raw.get("conflict"), "conflict"),
        "assessment_method_digest": require_string(
            raw.get("assessment_method_digest"), "assessment_method_digest"
        ),
        "quality_report_digest": "",
    }
    admissible = bool(
        report["coverage"] >= 0.7
        and report["freshness"] >= 0.5
        and report["provenance"] >= 0.7
        and report["calibration"] >= 0.5
        and report["completeness"] >= 0.7
        and report["conflict"] <= 0.5
    )
    report["admissible_for_directional_comparison"] = admissible
    return _digest_with_optional_supplied(
        report, "quality_report_digest", raw.get("quality_report_digest")
    )


def build_initial_observe_state(
    *, observe_id: str, act_state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    errors = validate_act_state(act_state)
    if errors:
        raise ValueError("invalid_source_act_state:" + ";".join(errors))
    if act_state.get("current_phase") != "commit":
        raise ValueError("source_act_not_committed")
    if act_state.get("route") != "EFFECT_RECORDED":
        raise ValueError("source_act_effect_not_recorded")
    if act_state.get("effect_recorded") is not True:
        raise ValueError("source_act_effect_flag_missing")
    if act_state.get("observation_required") is not True:
        raise ValueError("source_act_observation_debt_missing")
    if act_state.get("verification_required") is not True:
        raise ValueError("source_act_verification_debt_missing")
    receipt = act_state.get("host_receipt")
    if not isinstance(receipt, Mapping):
        raise ValueError("source_host_receipt_missing")
    if receipt.get("version") != HOST_RECEIPT_VERSION:
        raise ValueError("source_host_receipt_version_invalid")
    if receipt.get("status") != HOST_READY:
        raise ValueError("source_host_receipt_not_ready")
    if receipt.get("host_receipt_digest") != host_receipt_digest(receipt):
        raise ValueError("source_host_receipt_digest_invalid")
    if receipt.get("host_receipt_digest") != act_state.get("host_receipt_digest"):
        raise ValueError("source_host_receipt_binding_mismatch")

    state = {
        "version": STATE_VERSION,
        "observe_id": require_string(observe_id, "observe_id"),
        "lineage_id": require_string(act_state.get("lineage_id"), "lineage_id"),
        "source_act_id": require_string(act_state.get("act_id"), "source_act_id"),
        "source_act_state_digest": require_string(
            act_state.get("act_state_digest"), "source_act_state_digest"
        ),
        "source_act_version": require_int(act_state.get("act_version"), "source_act_version"),
        "source_act_updated_at_ms": require_int(
            act_state.get("updated_at_ms"), "source_act_updated_at_ms"
        ),
        "host_receipt_digest": require_string(
            act_state.get("host_receipt_digest"), "host_receipt_digest"
        ),
        "host_invocation_digest": require_string(
            act_state.get("host_invocation_digest"), "host_invocation_digest"
        ),
        "selected_step_id": require_string(
            act_state.get("selected_step_id"), "selected_step_id"
        ),
        "selected_step_digest": require_string(
            act_state.get("selected_step_digest"), "selected_step_digest"
        ),
        "operation_id": require_string(act_state.get("operation_id"), "operation_id"),
        "expected_observation_digest": require_string(
            act_state.get("expected_observation_digest"), "expected_observation_digest"
        ),
        "verification_criterion_digest": require_string(
            act_state.get("verification_criterion_digest"),
            "verification_criterion_digest",
        ),
        "mission_contract_digest": require_string(
            act_state.get("mission_contract_digest"), "mission_contract_digest"
        ),
        "current_phase": "bind",
        "route": "PENDING",
        "event_index": 0,
        "observe_version": 0,
        "committed_records": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "predecessor_observe_state_digest": "",
        "observe_state_digest": "",
        "observation_scope": {},
        "observation_scope_digest": "",
        "evidence_items": [],
        "evidence_packet_digest": "",
        "provenance_summary": {},
        "quality_report": {},
        "quality_report_digest": "",
        "comparison_receipt": {},
        "comparison_receipt_digest": "",
        "observation_recorded": False,
        "observation_debt_discharged": False,
        "reobservation_required": False,
        "verification_required": True,
        "automatic_truth_promotion": False,
        "automatic_belief_update": False,
        "automatic_plan_completion": False,
        "automatic_causal_attribution": False,
        "processed_event_digests": [],
        "event_history": [],
        "record_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["observe_state_digest"] = state_digest(state)
    return state


def validate_observe_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("observe_state_version_invalid")
        for field in (
            "observe_id",
            "lineage_id",
            "source_act_id",
            "source_act_state_digest",
            "host_receipt_digest",
            "host_invocation_digest",
            "selected_step_id",
            "selected_step_digest",
            "operation_id",
            "expected_observation_digest",
            "verification_criterion_digest",
            "mission_contract_digest",
        ):
            require_string(state.get(field), field)
        for field in (
            "source_act_version",
            "source_act_updated_at_ms",
            "event_index",
            "observe_version",
            "committed_records",
            "updated_at_ms",
        ):
            require_int(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("observe_state_phase_invalid")
        if state.get("route") not in ROUTES:
            errors.append("observe_state_route_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("observe_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("observe_state_boundary_invalid")
        if state.get("observe_state_digest") != state_digest(state):
            errors.append("observe_state_digest_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("observe_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("observe_event_history_count_mismatch")
        if state.get("verification_required") is not True:
            errors.append("observe_verification_debt_lost")
        if state.get("automatic_truth_promotion") is not False:
            errors.append("observe_truth_promotion_forbidden")
        if state.get("automatic_belief_update") is not False:
            errors.append("observe_automatic_belief_update_forbidden")
        if state.get("automatic_plan_completion") is not False:
            errors.append("observe_plan_completion_forbidden")
        if state.get("automatic_causal_attribution") is not False:
            errors.append("observe_causal_attribution_forbidden")
        if state.get("observation_recorded") is True:
            route = state.get("route")
            if route == "PENDING":
                errors.append("observe_recorded_route_pending")
            discharged = state.get("observation_debt_discharged") is True
            reobserve = state.get("reobservation_required") is True
            if route in {"OBSERVATION_MATCHED", "OBSERVATION_DIVERGENT"}:
                if not discharged or reobserve:
                    errors.append("observe_directional_debt_semantics_invalid")
            if route in {"OBSERVATION_INCONCLUSIVE", "OBSERVATION_CONFLICTED"}:
                if discharged or not reobserve:
                    errors.append("observe_open_debt_semantics_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_observe_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "observe_id": require_string(state.get("observe_id"), "observe_id"),
        "lineage_id": require_string(state.get("lineage_id"), "lineage_id"),
        "expected_observe_state_digest": require_string(
            state.get("observe_state_digest"), "expected_observe_state_digest"
        ),
        "source_phase": require_string(state.get("current_phase"), "source_phase"),
        "target_phase": require_string(target_phase, "target_phase"),
        "event_index": require_int(state.get("event_index"), "event_index") + 1,
        "artifact_digest": require_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "observe_event_digest": "",
    }
    event["observe_event_digest"] = event_digest(event)
    return event


def build_comparison_receipt(
    *,
    state: Mapping[str, Any],
    comparison_id: str,
    verdict: str,
    comparison_method_digest: str,
    rationale_digest: str,
    compared_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_phase") != "assess":
        raise ValueError("comparison_requires_assessed_state")
    normalized_verdict = require_string(verdict, "verdict")
    if normalized_verdict not in COMPARISON_VERDICTS:
        raise ValueError("comparison_verdict_invalid")
    packet = {
        "version": COMPARISON_RECEIPT_VERSION,
        "comparison_id": require_string(comparison_id, "comparison_id"),
        "observe_id": state["observe_id"],
        "source_act_state_digest": state["source_act_state_digest"],
        "host_receipt_digest": state["host_receipt_digest"],
        "host_invocation_digest": state["host_invocation_digest"],
        "expected_observation_digest": state["expected_observation_digest"],
        "observation_scope_digest": state["observation_scope_digest"],
        "evidence_packet_digest": state["evidence_packet_digest"],
        "quality_report_digest": state["quality_report_digest"],
        "comparison_method_digest": require_string(
            comparison_method_digest, "comparison_method_digest"
        ),
        "rationale_digest": require_string(rationale_digest, "rationale_digest"),
        "verdict": normalized_verdict,
        "compared_at_ms": require_int(compared_at_ms, "compared_at_ms"),
        "comparison_is_verification": False,
        "truth_authority_granted": False,
        "causal_attribution_granted": False,
        "comparison_receipt_digest": "",
    }
    packet["comparison_receipt_digest"] = comparison_receipt_digest(packet)
    return packet


def build_observe_phase_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_state_digest: str,
    observe_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_observe_state(state)
    if errors:
        raise ValueError("invalid_observe_state:" + ";".join(errors))
    if state.get("current_phase") != "commit" or state.get("route") == "PENDING":
        raise ValueError("observe_phase_receipt_requires_committed_observation")
    packet = {
        "version": OBSERVE_PHASE_RECEIPT_VERSION,
        "observe_id": state["observe_id"],
        "observe_state_digest": state["observe_state_digest"],
        "source_act_state_digest": state["source_act_state_digest"],
        "host_receipt_digest": state["host_receipt_digest"],
        "host_invocation_digest": state["host_invocation_digest"],
        "evidence_packet_digest": state["evidence_packet_digest"],
        "quality_report_digest": state["quality_report_digest"],
        "comparison_receipt_digest": state["comparison_receipt_digest"],
        "route": state["route"],
        "observation_debt_discharged": state["observation_debt_discharged"],
        "reobservation_required": state["reobservation_required"],
        "verification_required": True,
        "mission_cycle_phase": "observe",
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "observe_phase_event_digest": require_string(
            observe_phase_event_digest, "observe_phase_event_digest"
        ),
        "observation_not_verification": True,
        "source_effect_identity_preserved": True,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "observe_phase_receipt_digest": "",
    }
    packet["observe_phase_receipt_digest"] = observe_phase_receipt_digest(packet)
    return packet


def _validate_event_base(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("observe_event_version_invalid")
    if event.get("observe_id") != state.get("observe_id"):
        errors.append("observe_event_id_mismatch")
    if event.get("lineage_id") != state.get("lineage_id"):
        errors.append("observe_event_lineage_mismatch")
    if event.get("observe_event_digest") != event_digest(event):
        errors.append("observe_event_digest_invalid")
    if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("observe_event_authority_escalation")
    source = str(event.get("source_phase", ""))
    if source != state.get("current_phase"):
        errors.append("observe_event_source_phase_stale")
    if event.get("target_phase") != next_phase(source):
        errors.append("observe_event_phase_order_invalid")
    if event.get("event_index") != int(state.get("event_index", -1)) + 1:
        errors.append("observe_event_index_invalid")
    if event.get("expected_observe_state_digest") != state.get(
        "observe_state_digest"
    ):
        errors.append("observe_event_state_digest_stale")
    if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        errors.append("observe_event_time_regression")
    return errors


def _apply_payload(
    state: dict[str, Any], phase: str, payload: Mapping[str, Any]
) -> None:
    if phase == "scope":
        scope = _normalize_scope(state, payload)
        state["observation_scope"] = scope
        state["observation_scope_digest"] = scope["observation_scope_digest"]
        return

    if phase == "collect":
        raw_items = payload.get("evidence_items")
        if not isinstance(raw_items, list):
            raise ValueError("evidence_items_list_required")
        scope = state["observation_scope"]
        items = [
            _normalize_evidence_item(scope, item)
            for item in raw_items
            if isinstance(item, Mapping)
        ]
        if len(items) != len(raw_items):
            raise ValueError("evidence_item_object_required")
        ids = [item["evidence_id"] for item in items]
        if len(ids) != len(set(ids)):
            raise ValueError("evidence_id_duplicate")
        if len(items) < int(scope["minimum_evidence_items"]):
            raise ValueError("minimum_evidence_items_not_met")
        if scope["independence_required"]:
            independent = {item["independent_source_id"] for item in items}
            minimum_sources = min(2, int(scope["minimum_evidence_items"]))
            if len(independent) < minimum_sources:
                raise ValueError("independent_evidence_sources_insufficient")
        state["evidence_items"] = items
        state["evidence_packet_digest"] = sha(
            {
                "source_act_state_digest": state["source_act_state_digest"],
                "host_receipt_digest": state["host_receipt_digest"],
                "host_invocation_digest": state["host_invocation_digest"],
                "selected_step_digest": state["selected_step_digest"],
                "operation_id": state["operation_id"],
                "observation_scope_digest": state["observation_scope_digest"],
                "evidence_items": items,
            }
        )
        return

    if phase == "trace":
        required_true = (
            "evidence_chain_complete",
            "source_identity_preserved",
            "raw_artifacts_immutable",
            "no_unbound_evidence",
        )
        for field in required_true:
            if payload.get(field) is not True:
                raise ValueError(f"trace_{field}_required")
        provenance_receipt = require_string(
            payload.get("provenance_receipt_digest"),
            "provenance_receipt_digest",
        )
        collectors = sorted({item["collector_id"] for item in state["evidence_items"]})
        sources = sorted(
            {item["independent_source_id"] for item in state["evidence_items"]}
        )
        state["provenance_summary"] = {
            "provenance_receipt_digest": provenance_receipt,
            "evidence_chain_complete": True,
            "source_identity_preserved": True,
            "raw_artifacts_immutable": True,
            "no_unbound_evidence": True,
            "collector_ids": collectors,
            "independent_source_ids": sources,
            "evidence_count": len(state["evidence_items"]),
            "provenance_summary_digest": sha(
                {
                    "provenance_receipt_digest": provenance_receipt,
                    "collector_ids": collectors,
                    "independent_source_ids": sources,
                    "evidence_packet_digest": state["evidence_packet_digest"],
                }
            ),
        }
        return

    if phase == "assess":
        raw_report = payload.get("quality_report")
        if not isinstance(raw_report, Mapping):
            raise ValueError("quality_report_required")
        report = _normalize_quality_report(raw_report)
        state["quality_report"] = report
        state["quality_report_digest"] = report["quality_report_digest"]
        return

    if phase == "compare":
        receipt = payload.get("comparison_receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("comparison_receipt_required")
        if receipt.get("version") != COMPARISON_RECEIPT_VERSION:
            raise ValueError("comparison_receipt_version_invalid")
        if receipt.get("comparison_receipt_digest") != comparison_receipt_digest(
            receipt
        ):
            raise ValueError("comparison_receipt_digest_invalid")
        bindings = {
            "observe_id": state["observe_id"],
            "source_act_state_digest": state["source_act_state_digest"],
            "host_receipt_digest": state["host_receipt_digest"],
            "host_invocation_digest": state["host_invocation_digest"],
            "expected_observation_digest": state["expected_observation_digest"],
            "observation_scope_digest": state["observation_scope_digest"],
            "evidence_packet_digest": state["evidence_packet_digest"],
            "quality_report_digest": state["quality_report_digest"],
        }
        for field, expected in bindings.items():
            if receipt.get(field) != expected:
                raise ValueError(f"comparison_receipt_{field}_mismatch")
        if receipt.get("comparison_is_verification") is not False:
            raise ValueError("comparison_must_not_claim_verification")
        if receipt.get("truth_authority_granted") is not False:
            raise ValueError("comparison_truth_authority_forbidden")
        if receipt.get("causal_attribution_granted") is not False:
            raise ValueError("comparison_causal_attribution_forbidden")
        verdict = str(receipt.get("verdict", ""))
        if verdict not in COMPARISON_VERDICTS:
            raise ValueError("comparison_verdict_invalid")
        admissible = bool(
            state["quality_report"].get(
                "admissible_for_directional_comparison", False
            )
        )
        if not admissible and verdict in {"MATCHED", "DIVERGENT"}:
            raise ValueError("low_quality_directional_comparison_forbidden")
        route_map = {
            "MATCHED": "OBSERVATION_MATCHED",
            "DIVERGENT": "OBSERVATION_DIVERGENT",
            "INCONCLUSIVE": "OBSERVATION_INCONCLUSIVE",
            "CONFLICTED": "OBSERVATION_CONFLICTED",
        }
        state["comparison_receipt"] = deepcopy(dict(receipt))
        state["comparison_receipt_digest"] = receipt["comparison_receipt_digest"]
        state["route"] = route_map[verdict]
        state["observation_recorded"] = True
        directional = verdict in {"MATCHED", "DIVERGENT"}
        state["observation_debt_discharged"] = directional
        state["reobservation_required"] = not directional
        state["verification_required"] = True
        return

    if phase == "commit":
        required = {
            "observation_not_verification": True,
            "verification_debt_preserved": True,
            "source_effect_identity_preserved": True,
            "memory_overwrite": False,
            "automatic_truth_promotion": False,
            "automatic_belief_update": False,
            "automatic_plan_completion": False,
            "automatic_causal_attribution": False,
        }
        for field, expected in required.items():
            if payload.get(field) != expected:
                raise ValueError(f"observe_commit_{field}_invalid")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("observe_commit_authority_escalation")
        if state["route"] == "PENDING" or not state["observation_recorded"]:
            raise ValueError("observe_comparison_not_recorded")
        return

    raise ValueError("observe_target_phase_unsupported")


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    event_id: str,
    predecessor: str,
    errors: list[str],
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "observe_event_digest": event_id,
        "predecessor_observe_state_digest": predecessor,
        "result_observe_state_digest": state["observe_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "observe_apply_result_digest": "",
    }
    packet["observe_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_observe_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_observe_state(state)
    if state_errors:
        raise ValueError("invalid_observe_state:" + ";".join(state_errors))
    event_id = str(event.get("observe_event_digest", ""))
    predecessor = str(state["observe_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = _validate_event_base(state, event)
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    next_state = deepcopy(dict(state))
    phase = str(event["target_phase"])
    try:
        _apply_payload(next_state, phase, dict(event.get("payload", {})))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_observe_state_digest"] = predecessor
    next_state["current_phase"] = phase
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": phase,
            "artifact_digest": event["artifact_digest"],
            "observe_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if phase == "commit":
        next_state["observe_version"] += 1
        next_state["committed_records"] += 1
        next_state["record_summaries"] = list(next_state["record_summaries"]) + [
            {
                "observe_version": next_state["observe_version"],
                "route": next_state["route"],
                "source_act_state_digest": next_state["source_act_state_digest"],
                "host_receipt_digest": next_state["host_receipt_digest"],
                "evidence_packet_digest": next_state["evidence_packet_digest"],
                "comparison_receipt_digest": next_state[
                    "comparison_receipt_digest"
                ],
                "observation_debt_discharged": next_state[
                    "observation_debt_discharged"
                ],
                "reobservation_required": next_state["reobservation_required"],
                "verification_required": True,
            }
        ]
    next_state["observe_state_digest"] = ""
    next_state["observe_state_digest"] = state_digest(next_state)
    next_errors = validate_observe_state(next_state)
    if next_errors:
        raise ValueError("next_observe_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )
