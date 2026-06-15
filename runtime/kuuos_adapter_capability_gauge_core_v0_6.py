#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    normalize_sources,
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_adapter_capability_bundle_validation_v0_6 import (
    validate_bundle,
    validate_root,
)
from runtime.kuuos_adapter_capability_gauge_execution_v0_6 import (
    run_federation_child,
    validate_child_evidence_and_effect,
)
from runtime.kuuos_adapter_capability_gauge_model_v0_6 import (
    build_selection,
    calibrate,
    empty_bundle,
)
from runtime.kuuos_adapter_capability_gauge_records_v0_6 import (
    build_receipt,
    build_state_and_record,
    paths,
    pending_record,
    replay_result,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    BLOCKED,
    CALIBRATION_VERSION,
    READY,
    SELECTION_VERSION,
    STATE_VERSION,
    VERSION,
    AdapterCapabilityGaugeResult,
    append_jsonl,
    as_list,
    calibration_digest,
    clamp,
    contains_graph_keys,
    integer,
    mapping,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    valid_digest,
    write_json,
)
from runtime.kuuos_adapter_capability_plan_validation_v0_6 import (
    validate_license,
    validate_plan,
)


def _selected_entry(
    registry: Mapping[str, Any], selection: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    selected_id = str(selection.get("selected_federation_adapter_id", ""))
    for raw in as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        if entry.get("federation_adapter_id") == selected_id:
            return entry, dict(mapping(entry.get("adapter_profile")))
    return {}, {}


def _recovery_calibration(
    *,
    run_id: str,
    bundle: Mapping[str, Any],
    selection: Mapping[str, Any],
    effect: Mapping[str, Any],
    evidence_digest: str,
    learning_rate: float,
) -> dict[str, Any]:
    adapter_id = str(selection.get("selected_federation_adapter_id", ""))
    context_key = str(selection.get("context_key", ""))
    trace = next(
        (
            mapping(item)
            for item in reversed(as_list(bundle.get("holonomy_trace")))
            if mapping(item).get("federated_evidence_digest") == evidence_digest
            and mapping(item).get("federation_adapter_id") == adapter_id
            and mapping(item).get("context_key") == context_key
        ),
        {},
    )
    section = next(
        (
            mapping(item)
            for item in as_list(bundle.get("sections"))
            if mapping(item).get("federation_adapter_id") == adapter_id
            and mapping(item).get("context_key") == context_key
        ),
        {},
    )
    packet = {
        "version": CALIBRATION_VERSION,
        "capability_run_id": run_id,
        "federation_adapter_id": adapter_id,
        "adapter_profile_digest": selection.get(
            "selected_adapter_profile_digest", ""
        ),
        "context_key": context_key,
        "effect_receipt_digest": effect.get("effect_receipt_digest", ""),
        "federated_evidence_digest": evidence_digest,
        "outcome": effect.get("outcome", ""),
        "prior_connection": trace.get("prior_connection", 0.0),
        "observed_utility": trace.get("observed_utility", 0.0),
        "effective_learning_rate": round(
            clamp(learning_rate) * clamp(effect.get("confidence")), 6
        ),
        "capability_curvature": trace.get("capability_curvature", 0.0),
        "updated_connection": trace.get(
            "updated_connection", section.get("connection_coefficient", 0.0)
        ),
        "observation_count": section.get("observation_count", 0),
        "capability_section_digest": section.get(
            "capability_section_digest", ""
        ),
        "capability_bundle_digest": bundle.get("capability_bundle_digest", ""),
        "recovered_from_capability_holonomy": True,
    }
    packet["calibration_digest"] = calibration_digest(packet)
    return packet


def build_adapter_capability_gauge(
    *,
    runtime_context: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    capability_plan: Mapping[str, Any],
    capability_license: Mapping[str, Any],
) -> AdapterCapabilityGaugeResult:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(capability_plan)
    license_packet = mapping(capability_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    artifact_paths = paths(root)
    previous_state = read_json(artifact_paths["state"])
    current_bundle = read_json(artifact_paths["bundle"])
    if not current_bundle:
        current_bundle = empty_bundle(str(plan.get("agent_id", "")))
    ledger = read_jsonl(artifact_paths["ledger"])
    run_id = str(plan.get("capability_run_id", ""))
    source_batch = batch_digest(sources)

    if any(row.get("_invalid") for row in ledger):
        blockers.append("capability_ledger_invalid")
    committed = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "committed"
            and row.get("capability_run_id") == run_id
        ),
        None,
    )
    if committed is not None:
        if committed.get("capability_plan_digest") == plan.get(
            "capability_plan_digest"
        ):
            return replay_result(committed, root, artifact_paths)
        blockers.append("capability_run_id_reused_with_different_plan")
    pending = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "pending"
            and row.get("capability_run_id") == run_id
        ),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_capability_run")

    if context.get("adapter_capability_gauge_enabled") is not True:
        blockers.append("adapter_capability_gauge_enabled_not_true")
    if context.get("execute_one_capability_cycle") is not True:
        blockers.append("execute_one_capability_cycle_not_true")
    validate_root(root_packet, blockers)
    validate_adapter_registry(registry, blockers)
    validate_bundle(current_bundle, str(plan.get("agent_id", "")), blockers)
    if previous_state and (
        previous_state.get("version") != STATE_VERSION
        or not valid_digest(previous_state, "capability_state_digest")
    ):
        blockers.append("previous_capability_state_invalid")

    bound_state: Mapping[str, Any] = previous_state
    bound_bundle: Mapping[str, Any] = current_bundle
    if pending is not None:
        bound_state = {
            "capability_state_digest": pending.get(
                "previous_capability_state_digest", ""
            )
        }
        bound_bundle = {
            "capability_bundle_digest": pending.get(
                "previous_capability_bundle_digest", ""
            )
        }
    validate_plan(
        plan,
        source_batch_digest=source_batch,
        root_packet=root_packet,
        registry=registry,
        previous_state=bound_state,
        previous_bundle=bound_bundle,
        blockers=blockers,
    )
    validate_license(
        license_packet,
        plan=plan,
        source_batch_digest=source_batch,
        root_packet=root_packet,
        registry=registry,
        previous_bundle=bound_bundle,
        blockers=blockers,
    )
    validate_source_packets(
        sources,
        max_sources=integer(plan.get("max_sources_per_cycle"), 0),
        max_signals_per_source=integer(plan.get("max_signals_per_source"), 0),
        max_total_signals=integer(plan.get("max_total_signals"), 0),
        blockers=blockers,
    )
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")

    cycle_index = (
        integer(pending.get("cycle_index"), 0)
        if pending is not None
        else integer(previous_state.get("cycle_index"), 0) + 1
    )
    packet_id = "kuuos-capability-gauge-" + sha(
        {"run": run_id, "source_batch": source_batch, "cycle": cycle_index}
    )[:18]
    normalized_wake = normalize_sources(sources) if not blockers else {}
    selection: dict[str, Any] = {}
    selected_entry: dict[str, Any] = {}
    selected_profile: dict[str, Any] = {}

    if not blockers and pending is not None:
        candidate = read_json(artifact_paths["selection"])
        if (
            candidate.get("version") == SELECTION_VERSION
            and valid_digest(candidate, "selection_digest")
            and candidate.get("capability_run_id") == run_id
            and candidate.get("source_batch_digest") == source_batch
            and candidate.get("selection_digest") == pending.get("selection_digest")
        ):
            selection = candidate
            selected_entry, selected_profile = _selected_entry(registry, selection)
        else:
            blockers.append("pending_capability_selection_invalid")
    elif not blockers:
        selection, selected_entry, selected_profile = build_selection(
            capability_run_id=run_id,
            bundle=current_bundle,
            registry=registry,
            source_packets=sources,
            wake=normalized_wake,
            exploration_weight=clamp(plan.get("exploration_weight")),
            max_exploration_bonus=clamp(plan.get("max_exploration_bonus")),
            curvature_penalty=clamp(plan.get("curvature_penalty")),
            blockers=blockers,
        )
        if not blockers:
            write_json(artifact_paths["selection"], selection)
            append_jsonl(
                artifact_paths["ledger"],
                pending_record(
                    packet_id=packet_id,
                    run_id=run_id,
                    plan=plan,
                    source_batch_digest=source_batch,
                    previous_state_digest=previous_state.get(
                        "capability_state_digest", ""
                    ),
                    previous_bundle_digest=current_bundle.get(
                        "capability_bundle_digest", ""
                    ),
                    selection=selection,
                    cycle_index=cycle_index,
                ),
            )

    child_result: dict[str, Any] = {}
    evidence: dict[str, Any] = {}
    effect: dict[str, Any] = {}
    calibration: dict[str, Any] = {}
    updated_bundle = current_bundle
    if not blockers:
        child_result = run_federation_child(
            root=root,
            runtime_context=context,
            capability_plan=plan,
            source_packets=sources,
            root_principles_packet=root_packet,
            registry=registry,
            selection=selection,
            selected_entry=selected_entry,
            selected_profile=selected_profile,
            previous_federation_state=read_json(artifact_paths["federation_state"]),
            blockers=blockers,
        )
    if not blockers:
        evidence, effect = validate_child_evidence_and_effect(
            root=root,
            child_result=child_result,
            require_effect=plan.get("require_effect_observation") is not False,
            blockers=blockers,
        )
    if not blockers:
        updated_bundle, calibration_or_section, calibration_replayed = calibrate(
            capability_run_id=run_id,
            bundle=current_bundle,
            selection=selection,
            selected_profile=selected_profile,
            effect=effect,
            federated_evidence_digest=str(evidence.get("evidence_digest", "")),
            learning_rate=clamp(plan.get("learning_rate")),
        )
        if calibration_replayed:
            existing = read_json(artifact_paths["calibration"])
            if (
                existing.get("version") == CALIBRATION_VERSION
                and valid_digest(existing, "calibration_digest")
                and existing.get("capability_run_id") == run_id
                and existing.get("federated_evidence_digest")
                == evidence.get("evidence_digest")
            ):
                calibration = existing
            else:
                calibration = _recovery_calibration(
                    run_id=run_id,
                    bundle=updated_bundle,
                    selection=selection,
                    effect=effect,
                    evidence_digest=str(evidence.get("evidence_digest", "")),
                    learning_rate=clamp(plan.get("learning_rate")),
                )
            warnings.append("capability_calibration_recovered_without_duplicate_update")
        else:
            calibration = dict(calibration_or_section)
        write_json(artifact_paths["calibration"], calibration)
        write_json(artifact_paths["bundle"], updated_bundle)

    status = READY if not blockers else BLOCKED
    if status == READY:
        state_base = previous_state
        if pending is not None and previous_state.get("capability_run_id") == run_id:
            state_base = {
                "capability_state_digest": pending.get(
                    "previous_capability_state_digest", ""
                ),
                "total_calibrations": max(
                    0, integer(previous_state.get("total_calibrations"), 1) - 1
                ),
            }
        state, record = build_state_and_record(
            previous_state=state_base,
            packet_id=packet_id,
            run_id=run_id,
            plan=plan,
            cycle_index=cycle_index,
            selection=selection,
            calibration=calibration,
            bundle=updated_bundle,
            child_result=child_result,
        )
        write_json(artifact_paths["state"], state)
        append_jsonl(artifact_paths["ledger"], record)

    receipt = build_receipt(
        status=status,
        packet_id=packet_id,
        run_id=run_id,
        cycle_index=cycle_index,
        selection=selection,
        calibration=calibration,
        child_result=child_result,
        blockers=blockers,
        warnings=warnings,
    )
    if license_packet.get("receipt_write_allowed") is True:
        write_json(artifact_paths["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(
            artifact_paths["audit"],
            {**receipt, "audit_record_digest": sha(receipt)},
        )

    return AdapterCapabilityGaugeResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        capability_run_id=run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        context_key=str(selection.get("context_key", "")),
        selected_federation_adapter_id=str(
            selection.get("selected_federation_adapter_id", "")
        ),
        selected_adapter_profile_digest=str(
            selection.get("selected_adapter_profile_digest", "")
        ),
        selection_score=float(selection.get("selected_score", 0.0)),
        prior_connection=float(calibration.get("prior_connection", 0.0)),
        observed_utility=float(calibration.get("observed_utility", 0.0)),
        updated_connection=float(calibration.get("updated_connection", 0.0)),
        capability_curvature=float(calibration.get("capability_curvature", 0.0)),
        observation_count=integer(calibration.get("observation_count"), 0),
        child_federation_status=str(child_result.get("status", "")),
        child_federation_run_id=str(child_result.get("federation_run_id", "")),
        child_evidence_digest=str(child_result.get("evidence_digest", "")),
        effect_receipt_digest=str(child_result.get("effect_receipt_digest", "")),
        next_wake_digest=str(child_result.get("next_wake_digest", "")),
        idempotent_replay=False,
        recovered_pending_run=recovered_pending,
        state_path=str(artifact_paths["state"]),
        bundle_path=str(artifact_paths["bundle"]),
        selection_path=str(artifact_paths["selection"]),
        calibration_path=str(artifact_paths["calibration"]),
        receipt_path=str(artifact_paths["receipt"]),
        ledger_path=str(artifact_paths["ledger"]),
        audit_path=str(artifact_paths["audit"]),
        blockers=blockers,
        warnings=warnings,
    )
