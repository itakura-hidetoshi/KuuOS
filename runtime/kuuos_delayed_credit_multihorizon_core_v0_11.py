#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_adapter_capability_gauge_model_v0_6 import context_signature
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import empty_bundle as empty_experiment_bundle
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import normalize_sources
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_experiment_outcome_policy_model_v0_9 import empty_bundle as empty_policy_bundle
from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    EFFECT_VERSION,
    effect_digest,
)
from runtime.kuuos_policy_regret_cadence_cycle_v0_10 import build_policy_regret_cadence
from runtime.kuuos_policy_regret_cadence_model_v0_10 import empty_bundle as empty_regret_bundle
from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
    OUTCOME_VERSION as REGRET_OUTCOME_VERSION,
    READY as REGRET_READY,
    REPLAYED as REGRET_REPLAYED,
    outcome_digest as regret_outcome_digest,
)
from runtime.kuuos_delayed_credit_multihorizon_bridge_v0_11 import (
    build_child_regret_license,
    build_child_regret_plan,
)
from runtime.kuuos_delayed_credit_multihorizon_ledger_v0_11 import (
    build_state_and_record,
    pending_record,
)
from runtime.kuuos_delayed_credit_multihorizon_model_v0_11 import (
    build_horizon_decision,
    commit_horizon_outcome,
    empty_bundle,
    section_for,
)
from runtime.kuuos_delayed_credit_multihorizon_paths_v0_11 import paths, replay_result
from runtime.kuuos_delayed_credit_multihorizon_receipt_v0_11 import build_receipt
from runtime.kuuos_delayed_credit_multihorizon_recovery_v0_11 import (
    load_recovery_packets,
    validate_pending,
)
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
    BLOCKED,
    READY,
    VERSION,
    DelayedCreditMultiHorizonResult,
    append_jsonl,
    as_list,
    contains_graph_keys,
    integer,
    mapping,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    write_json,
)
from runtime.kuuos_delayed_credit_multihorizon_validation_v0_11 import validate_inputs


def build_delayed_credit_multihorizon(
    *,
    runtime_context: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    horizon_plan: Mapping[str, Any],
    horizon_license: Mapping[str, Any],
) -> DelayedCreditMultiHorizonResult:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(horizon_plan)
    license_packet = mapping(horizon_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    p = paths(root)

    capability_state = read_json(p["capability_state"])
    capability_bundle = read_json(p["capability_bundle"])
    source_portfolio_bundle = read_json(p["source_portfolio_bundle"])
    experiment_state = read_json(p["experiment_state"])
    experiment_bundle = read_json(p["experiment_bundle"])
    if not experiment_bundle and source_portfolio_bundle:
        experiment_bundle = empty_experiment_bundle(str(plan.get("agent_id", "")), source_portfolio_bundle)
        write_json(p["experiment_bundle"], experiment_bundle)
    policy_state = read_json(p["policy_state"])
    policy_bundle = read_json(p["policy_bundle"])
    if not policy_bundle:
        policy_bundle = empty_policy_bundle(str(plan.get("agent_id", "")))
        write_json(p["policy_bundle"], policy_bundle)
    regret_state = read_json(p["regret_state"])
    regret_bundle = read_json(p["regret_bundle"])
    if not regret_bundle:
        regret_bundle = empty_regret_bundle(str(plan.get("agent_id", "")))
        write_json(p["regret_bundle"], regret_bundle)
    gauge_state = read_json(p["gauge_state"])
    gauge_bundle = read_json(p["gauge_bundle"])
    horizon_state = read_json(p["state"])
    horizon_bundle = read_json(p["bundle"])
    if not horizon_bundle:
        horizon_bundle = empty_bundle(str(plan.get("agent_id", "")))

    ledger = read_jsonl(p["ledger"])
    run_id = str(plan.get("horizon_run_id", ""))
    source_batch = batch_digest(sources)
    if any(row.get("_invalid") for row in ledger):
        blockers.append("horizon_ledger_invalid")
    committed = next(
        (row for row in reversed(ledger)
         if row.get("phase") == "committed" and row.get("horizon_run_id") == run_id),
        None,
    )
    if committed is not None:
        if committed.get("horizon_plan_digest") == plan.get("horizon_plan_digest"):
            return replay_result(committed, root, p)
        blockers.append("horizon_run_id_reused_with_different_plan")
    pending = next(
        (row for row in reversed(ledger)
         if row.get("phase") == "pending" and row.get("horizon_run_id") == run_id),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_horizon_run")

    if context.get("delayed_credit_multihorizon_enabled") is not True:
        blockers.append("delayed_credit_multihorizon_enabled_not_true")
    if context.get("execute_one_horizon_cycle") is not True:
        blockers.append("execute_one_horizon_cycle_not_true")
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")
    for name, packet in (
        ("capability_bundle", capability_bundle),
        ("source_portfolio_bundle", source_portfolio_bundle),
        ("experiment_bundle", experiment_bundle),
        ("policy_bundle", policy_bundle),
        ("regret_bundle", regret_bundle),
    ):
        if not packet:
            blockers.append(f"source_{name}_missing")

    upstream = {
        "capability_state": capability_state,
        "capability_bundle": capability_bundle,
        "source_portfolio_bundle": source_portfolio_bundle,
        "experiment_state": experiment_state,
        "experiment_bundle": experiment_bundle,
        "policy_state": policy_state,
        "policy_bundle": policy_bundle,
    }
    if not blockers and pending is None:
        validate_inputs(
            root_packet=root_packet,
            registry=registry,
            sources=sources,
            upstream=upstream,
            gauge_state=gauge_state,
            gauge_bundle=gauge_bundle,
            regret_state=regret_state,
            regret_bundle=regret_bundle,
            horizon_state=horizon_state,
            horizon_bundle=horizon_bundle,
            plan=plan,
            license_packet=license_packet,
            source_batch_digest=source_batch,
            blockers=blockers,
        )
    elif not blockers:
        validate_pending(
            root_packet=root_packet,
            registry=registry,
            sources=sources,
            plan=plan,
            license_packet=license_packet,
            pending=pending,
            source_batch=source_batch,
            blockers=blockers,
        )

    normalized = normalize_sources(sources) if not blockers else {}
    context_key, _ = context_signature(sources, normalized) if not blockers else ("", {})
    cycle_index = (
        integer(pending.get("cycle_index"), 0)
        if pending is not None
        else integer(horizon_state.get("cycle_index"), 0) + 1
    )
    packet_id = "kuuos-multihorizon-" + sha(
        {"run": run_id, "source_batch": source_batch, "cycle": cycle_index}
    )[:18]
    decision: dict[str, Any] = {}
    child_plan: dict[str, Any] = {}
    child_license: dict[str, Any] = {}

    if not blockers and pending is not None:
        decision, child_plan, child_license = load_recovery_packets(
            run_id=run_id, pending=pending, paths=p, blockers=blockers
        )
    elif not blockers:
        decision = build_horizon_decision(
            horizon_run_id=run_id,
            cycle_index=cycle_index,
            context_key=context_key,
            horizon_bundle=horizon_bundle,
            regret_bundle=regret_bundle,
            plan=plan,
        )
        child_plan = build_child_regret_plan(
            horizon_plan=plan,
            horizon_decision=decision,
            source_packets=sources,
            root_packet=root_packet,
            adapter_registry=registry,
            previous_capability_state=capability_state,
            previous_capability_bundle=capability_bundle,
            source_portfolio_bundle=source_portfolio_bundle,
            previous_experiment_state=experiment_state,
            previous_experiment_bundle=experiment_bundle,
            previous_policy_state=policy_state,
            previous_policy_bundle=policy_bundle,
            previous_regret_state=regret_state,
            previous_regret_bundle=regret_bundle,
        )
        child_license = build_child_regret_license(
            child_plan=child_plan,
            source_packets=sources,
            root_packet=root_packet,
            adapter_registry=registry,
            previous_capability_bundle=capability_bundle,
            source_portfolio_bundle=source_portfolio_bundle,
            previous_experiment_bundle=experiment_bundle,
            previous_policy_bundle=policy_bundle,
            previous_regret_bundle=regret_bundle,
        )
        write_json(p["decision"], decision)
        write_json(p["child_plan"], child_plan)
        write_json(p["child_license"], child_license)
        append_jsonl(
            p["ledger"],
            pending_record(
                packet_id=packet_id,
                run_id=run_id,
                plan=plan,
                source_batch_digest=source_batch,
                previous_regret_state_digest=regret_state.get("regret_state_digest", ""),
                previous_regret_bundle_digest=regret_bundle.get("regret_bundle_digest", ""),
                previous_horizon_state_digest=horizon_state.get("horizon_state_digest", ""),
                previous_horizon_bundle_digest=horizon_bundle.get("horizon_bundle_digest", ""),
                decision=decision,
                child_plan=child_plan,
                cycle_index=cycle_index,
            ),
        )

    child_result: dict[str, Any] = {}
    if not blockers:
        child = build_policy_regret_cadence(
            runtime_context={
                "runtime_root": str(root),
                "policy_regret_cadence_enabled": True,
                "execute_one_regret_cycle": True,
                "allowed_domain_actions": as_list(context.get("allowed_domain_actions")),
            },
            source_packets=sources,
            root_principles_packet=root_packet,
            adapter_registry=registry,
            regret_plan=child_plan,
            regret_license=child_license,
        )
        child_result = child.to_dict()
        if child.status not in {REGRET_READY, REGRET_REPLAYED}:
            blockers.extend([f"regret_{item}" for item in child.blockers])

    child_regret_bundle: dict[str, Any] = {}
    child_regret_outcome: dict[str, Any] = {}
    effect: dict[str, Any] = {}
    current_gauge_bundle: dict[str, Any] = {}
    outcome: dict[str, Any] = {}
    updated_horizon_bundle = horizon_bundle
    if not blockers:
        child_regret_bundle = read_json(p["regret_bundle"])
        child_regret_outcome = read_json(p["regret_outcome"])
        effect = read_json(p["effect"])
        current_gauge_bundle = read_json(p["gauge_bundle"])
        if (
            child_regret_outcome.get("version") != REGRET_OUTCOME_VERSION
            or child_regret_outcome.get("regret_outcome_digest")
            != regret_outcome_digest(child_regret_outcome)
        ):
            blockers.append("child_regret_outcome_invalid")
        if (
            effect.get("version") != EFFECT_VERSION
            or effect.get("effect_receipt_digest") != effect_digest(effect)
        ):
            blockers.append("child_effect_receipt_invalid")
        if effect.get("effect_receipt_digest") != child_result.get("child_effect_receipt_digest"):
            blockers.append("child_effect_receipt_digest_mismatch")
        if child_regret_outcome.get("child_policy_mode") != child_result.get("child_policy_mode"):
            blockers.append("child_policy_mode_mismatch")

    if not blockers:
        regret_outcome_view = dict(child_regret_outcome)
        regret_outcome_view["child_live_adapter_id"] = child_result.get("child_live_adapter_id", "")
        regret_outcome_view["child_live_domain_action"] = child_result.get("child_live_domain_action", "")
        updated_horizon_bundle, outcome, replayed_update = commit_horizon_outcome(
            horizon_run_id=run_id,
            cycle_index=cycle_index,
            previous_bundle=horizon_bundle,
            child_regret_bundle=child_regret_bundle,
            child_regret_outcome=regret_outcome_view,
            effect=effect,
            gauge_bundle=current_gauge_bundle,
            decision=decision,
            plan=plan,
            max_outcomes=integer(plan.get("max_horizon_outcomes"), 256),
            max_holonomy=integer(plan.get("max_horizon_holonomy"), 256),
        )
        if replayed_update:
            warnings.append("child_regret_outcome_already_processed_for_horizon")
        write_json(p["outcome"], outcome)
        write_json(p["bundle"], updated_horizon_bundle)

    status = READY if not blockers else BLOCKED
    if status == READY:
        state_base = horizon_state
        if pending is not None and horizon_state.get("horizon_run_id") == run_id:
            mode = str(outcome.get("child_policy_mode", ""))
            state_base = {
                "horizon_state_digest": pending.get("previous_horizon_state_digest", ""),
                "total_cycles": max(0, integer(horizon_state.get("total_cycles"), 1) - 1),
                "total_experiment_children": max(0, integer(horizon_state.get("total_experiment_children"), 0) - (mode == "experiment")),
                "total_reobserve_children": max(0, integer(horizon_state.get("total_reobserve_children"), 0) - (mode == "reobserve")),
                "total_exploit_children": max(0, integer(horizon_state.get("total_exploit_children"), 0) - (mode == "exploit")),
                "total_progress_positive_cycles": max(0, integer(horizon_state.get("total_progress_positive_cycles"), 0) - (float(outcome.get("commitment_progress_score", 0.0)) > 0.0)),
                "total_recovery_cost_positive_cycles": max(0, integer(horizon_state.get("total_recovery_cost_positive_cycles"), 0) - (float(outcome.get("recovery_cost", 0.0)) > 0.0)),
            }
        state, row = build_state_and_record(
            previous_state=state_base,
            packet_id=packet_id,
            run_id=run_id,
            plan=plan,
            cycle_index=cycle_index,
            decision=decision,
            outcome=outcome,
            horizon_bundle=updated_horizon_bundle,
            child_regret_bundle=child_regret_bundle,
            child_regret_outcome=child_regret_outcome,
        )
        write_json(p["state"], state)
        append_jsonl(p["ledger"], row)

    receipt = build_receipt(
        status=status,
        packet_id=packet_id,
        run_id=run_id,
        cycle_index=cycle_index,
        decision=decision,
        outcome=outcome,
        horizon_bundle=updated_horizon_bundle,
        child_regret_bundle=child_regret_bundle,
        child_regret_outcome=child_regret_outcome,
        blockers=blockers,
        warnings=warnings,
    )
    if license_packet.get("receipt_write_allowed") is True:
        write_json(p["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(p["audit"], {**receipt, "audit_record_digest": sha(receipt)})

    section = section_for(updated_horizon_bundle, str(decision.get("context_key", "")))
    support = outcome.get("aggregate_support_after", {})
    return DelayedCreditMultiHorizonResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        horizon_run_id=run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        context_key=str(decision.get("context_key", "")),
        child_policy_mode=str(outcome.get("child_policy_mode", "")),
        child_live_adapter_id=str(child_result.get("child_live_adapter_id", "")),
        child_live_domain_action=str(outcome.get("child_live_domain_action", "")),
        commitment_progress_score=float(outcome.get("commitment_progress_score", 0.0)),
        recovery_cost=float(outcome.get("recovery_cost", 0.0)),
        terminal_section_ratio=float(outcome.get("terminal_section_ratio", 0.0)),
        mean_curvature_norm=float(outcome.get("mean_curvature_norm", 0.0)),
        delayed_compatible_evidence_count=integer(outcome.get("delayed_compatible_evidence_count"), 0),
        short_experiment_credit=float(section.get("short_experiment_credit", 0.0)),
        short_reobserve_credit=float(section.get("short_reobserve_credit", 0.0)),
        short_exploit_credit=float(section.get("short_exploit_credit", 0.0)),
        medium_experiment_credit=float(section.get("medium_experiment_credit", 0.0)),
        medium_reobserve_credit=float(section.get("medium_reobserve_credit", 0.0)),
        medium_exploit_credit=float(section.get("medium_exploit_credit", 0.0)),
        long_experiment_credit=float(section.get("long_experiment_credit", 0.0)),
        long_reobserve_credit=float(section.get("long_reobserve_credit", 0.0)),
        long_exploit_credit=float(section.get("long_exploit_credit", 0.0)),
        aggregate_experiment_support=float(support.get("experiment", 0.0)),
        aggregate_reobserve_support=float(support.get("reobserve", 0.0)),
        aggregate_exploit_support=float(support.get("exploit", 0.0)),
        adapted_base_experiment_threshold=float(decision.get("adapted_base_experiment_threshold", 0.0)),
        adapted_base_reobserve_threshold=float(decision.get("adapted_base_reobserve_threshold", 0.0)),
        adapted_base_experiment_interval=integer(decision.get("adapted_base_experiment_interval"), 0),
        adapted_base_reobserve_interval=integer(decision.get("adapted_base_reobserve_interval"), 0),
        horizon_bundle_digest=str(updated_horizon_bundle.get("horizon_bundle_digest", "")),
        child_regret_bundle_digest=str(child_regret_bundle.get("regret_bundle_digest", "")),
        child_regret_outcome_digest=str(child_regret_outcome.get("regret_outcome_digest", "")),
        child_effect_receipt_digest=str(effect.get("effect_receipt_digest", "")),
        idempotent_replay=False,
        recovered_pending_run=recovered_pending,
        state_path=str(p["state"]), bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]), outcome_path=str(p["outcome"]),
        child_plan_path=str(p["child_plan"]), child_license_path=str(p["child_license"]),
        receipt_path=str(p["receipt"]), ledger_path=str(p["ledger"]), audit_path=str(p["audit"]),
        blockers=blockers, warnings=warnings,
    )
