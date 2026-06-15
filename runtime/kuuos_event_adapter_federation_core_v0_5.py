#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_renewable_gauge_supervisor_core_v0_4 import (
    BLOCKED as SUPERVISOR_BLOCKED,
    READY as SUPERVISOR_READY,
    REPLAYED as SUPERVISOR_REPLAYED,
    build_renewable_gauge_supervisor,
)
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    normalize_sources,
    select_adapter,
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_event_adapter_federation_records_v0_5 import (
    build_evidence,
    build_receipt,
    build_state_and_record,
    paths,
    pending_record,
    replay_result,
    source_event_keys,
)
from runtime.kuuos_event_adapter_federation_supervisor_bridge_v0_5 import (
    build_supervisor_packets,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    BLOCKED,
    READY,
    STATE_VERSION,
    VERSION,
    EventAdapterFederationResult,
    append_jsonl,
    as_list,
    batch_digest,
    contains_graph_keys,
    integer,
    mapping,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    valid_digest,
    without,
    write_json,
)
from runtime.kuuos_event_adapter_federation_validation_v0_5 import (
    validate_license,
    validate_plan,
    validate_root,
)


def build_event_adapter_federation(
    *,
    runtime_context: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    federation_plan: Mapping[str, Any],
    federation_license: Mapping[str, Any],
) -> EventAdapterFederationResult:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(federation_plan)
    license_packet = mapping(federation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    artifact_paths = paths(root)
    previous_state = read_json(artifact_paths["state"])
    ledger = read_jsonl(artifact_paths["ledger"])
    run_id = str(plan.get("federation_run_id", ""))
    source_batch = batch_digest(sources)
    event_keys = source_event_keys(sources)

    if any(row.get("_invalid") for row in ledger):
        blockers.append("federation_ledger_invalid")
    committed = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "committed" and row.get("federation_run_id") == run_id
        ),
        None,
    )
    if committed is not None:
        if committed.get("federation_plan_digest") == plan.get("federation_plan_digest"):
            return replay_result(committed, root, artifact_paths)
        blockers.append("federation_run_id_reused_with_different_plan")

    if context.get("event_adapter_federation_enabled") is not True:
        blockers.append("event_adapter_federation_enabled_not_true")
    if context.get("execute_one_federated_cycle") is not True:
        blockers.append("execute_one_federated_cycle_not_true")
    validate_root(root_packet, blockers)
    validate_adapter_registry(registry, blockers)
    if previous_state and (
        previous_state.get("version") != STATE_VERSION
        or not valid_digest(previous_state, "federation_state_digest")
    ):
        blockers.append("previous_federation_state_invalid")
    max_sources, max_signals_per_source, max_total_signals = validate_plan(
        plan,
        source_batch=source_batch,
        root_packet=root_packet,
        registry=registry,
        previous_state=previous_state,
        blockers=blockers,
    )
    validate_source_packets(
        sources,
        max_sources=max_sources,
        max_signals_per_source=max_signals_per_source,
        max_total_signals=max_total_signals,
        blockers=blockers,
    )
    validate_license(
        license_packet,
        plan=plan,
        source_batch=source_batch,
        root_packet=root_packet,
        registry=registry,
        blockers=blockers,
    )
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")

    consumed_keys = {
        key
        for row in ledger
        if row.get("phase") == "committed"
        for key in as_list(row.get("source_event_keys"))
    }
    if consumed_keys.intersection(event_keys):
        blockers.append("source_event_already_consumed")
    claimed_keys = {
        key
        for row in ledger
        if row.get("phase") == "pending" and row.get("federation_run_id") != run_id
        for key in as_list(row.get("source_event_keys"))
    }
    if claimed_keys.intersection(event_keys):
        blockers.append("source_event_claimed_by_pending_run")
    pending = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "pending" and row.get("federation_run_id") == run_id
        ),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_federation_run")

    normalized_wake: dict[str, Any] = {}
    selected_entry: dict[str, Any] = {}
    selected_profile: dict[str, Any] = {}
    supervisor_result: dict[str, Any] = {}
    evidence: dict[str, Any] = {}
    cycle_index = integer(previous_state.get("cycle_index"), 0) + 1
    packet_id = "kuuos-federation-" + sha(
        {"run": run_id, "source_batch": source_batch, "cycle": cycle_index}
    )[:18]

    if not blockers:
        normalized_wake = normalize_sources(sources)
        selected_entry, selected_profile = select_adapter(
            registry, sources, normalized_wake, blockers
        )
    if not blockers and pending is None:
        append_jsonl(
            artifact_paths["ledger"],
            pending_record(
                packet_id=packet_id,
                run_id=run_id,
                plan=plan,
                source_batch=source_batch,
                event_keys=event_keys,
                normalized_wake=normalized_wake,
                selected_entry=selected_entry,
                cycle_index=cycle_index,
            ),
        )

    if not blockers:
        write_json(artifact_paths["normalized_wake"], normalized_wake)
        supervisor_plan, supervisor_license = build_supervisor_packets(
            federation_plan=plan,
            normalized_wake=normalized_wake,
            root_principles_packet=root_packet,
            adapter_profile=selected_profile,
            previous_supervisor_state=read_json(artifact_paths["supervisor_state"]),
        )
        raw_result = build_renewable_gauge_supervisor(
            runtime_context={
                "runtime_root": str(root),
                "renewable_gauge_supervisor_enabled": True,
                "execute_one_supervisor_cycle": True,
                "allowed_domain_actions": as_list(context.get("allowed_domain_actions")),
            },
            wake_event=normalized_wake,
            root_principles_packet=root_packet,
            supervisor_plan=supervisor_plan,
            supervisor_license=supervisor_license,
            adapter_profile=selected_profile,
        )
        supervisor_result = raw_result.to_dict()
        if raw_result.status == SUPERVISOR_BLOCKED:
            blockers.extend([f"supervisor_{item}" for item in raw_result.blockers])
        elif raw_result.status not in {SUPERVISOR_READY, SUPERVISOR_REPLAYED}:
            blockers.append("supervisor_status_unknown")

    if not blockers:
        evidence = build_evidence(
            run_id=run_id,
            source_batch=source_batch,
            normalized_wake=normalized_wake,
            selected_entry=selected_entry,
            selected_profile=selected_profile,
            supervisor_result=supervisor_result,
            supervisor_receipt=read_json(artifact_paths["supervisor_receipt"]),
            gauge_state=read_json(artifact_paths["gauge_state"]),
            next_wake=read_json(artifact_paths["next_wake"]),
        )
        write_json(artifact_paths["evidence"], evidence)

    status = READY if not blockers else BLOCKED
    if status == READY:
        state, record = build_state_and_record(
            previous_state=previous_state,
            run_id=run_id,
            packet_id=packet_id,
            cycle_index=cycle_index,
            source_count=len(sources),
            event_keys=event_keys,
            source_batch=source_batch,
            normalized_wake=normalized_wake,
            selected_entry=selected_entry,
            selected_profile=selected_profile,
            supervisor_result=supervisor_result,
            supervisor_state=read_json(artifact_paths["supervisor_state"]),
            gauge_state=read_json(artifact_paths["gauge_state"]),
            evidence=evidence,
        )
        write_json(artifact_paths["state"], state)
        record["federation_plan_digest"] = plan.get("federation_plan_digest")
        record["record_digest"] = sha(without(record, "record_digest"))
        append_jsonl(artifact_paths["ledger"], record)

    receipt = build_receipt(
        status=status,
        packet_id=packet_id,
        run_id=run_id,
        cycle_index=cycle_index,
        source_count=len(sources),
        source_batch=source_batch,
        normalized_wake=normalized_wake,
        selected_entry=selected_entry,
        selected_profile=selected_profile,
        supervisor_result=supervisor_result,
        evidence=evidence,
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

    return EventAdapterFederationResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        federation_run_id=run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        source_count=len(sources),
        normalized_signal_count=len(as_list(normalized_wake.get("signals"))),
        source_batch_digest=source_batch,
        normalized_wake_digest=str(normalized_wake.get("wake_event_digest", "")),
        selected_federation_adapter_id=str(
            selected_entry.get("federation_adapter_id", "")
        ),
        selected_adapter_profile_digest=str(
            selected_profile.get("adapter_profile_digest", "")
        ),
        supervisor_status=str(supervisor_result.get("status", "")),
        supervisor_cycle_index=integer(supervisor_result.get("cycle_index"), 0),
        telos_renewal_applied=bool(
            supervisor_result.get("telos_renewal_applied")
        ),
        intervention_applied=bool(supervisor_result.get("intervention_applied")),
        effect_receipt_digest=str(
            supervisor_result.get("effect_receipt_digest", "")
        ),
        evidence_digest=str(evidence.get("evidence_digest", "")),
        next_wake_digest=str(evidence.get("next_wake_digest", "")),
        idempotent_replay=False,
        recovered_pending_run=recovered_pending,
        state_path=str(artifact_paths["state"]),
        normalized_wake_path=str(artifact_paths["normalized_wake"]),
        evidence_path=str(artifact_paths["evidence"]),
        receipt_path=str(artifact_paths["receipt"]),
        ledger_path=str(artifact_paths["ledger"]),
        audit_path=str(artifact_paths["audit"]),
        blockers=blockers,
        warnings=warnings,
    )
