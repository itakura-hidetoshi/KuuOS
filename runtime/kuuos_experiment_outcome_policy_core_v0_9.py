#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    EFFECT_VERSION,
    effect_digest,
)
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    normalize_sources,
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_adapter_capability_bundle_validation_v0_6 import (
    validate_bundle as validate_capability_bundle,
    validate_root,
)
from runtime.kuuos_adapter_portfolio_shadow_validation_v0_7 import (
    validate_bundle as validate_portfolio_bundle,
)
from runtime.kuuos_bounded_portfolio_experiment_core_v0_8 import (
    build_bounded_portfolio_experiment,
)
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import (
    build_experiment_decision,
    empty_bundle as empty_experiment_bundle,
)
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    READY as EXPERIMENT_READY,
    REPLAYED as EXPERIMENT_REPLAYED,
    plan_digest as experiment_plan_digest,
)
from runtime.kuuos_bounded_portfolio_experiment_validation_v0_8 import (
    validate_bundle as validate_experiment_bundle,
)
from runtime.kuuos_experiment_outcome_policy_bridge_v0_9 import (
    build_experiment_license,
    build_experiment_plan,
    derive_policy_registry,
)
from runtime.kuuos_experiment_outcome_policy_model_v0_9 import (
    build_policy_decision,
    commit_policy_outcome,
    empty_bundle,
    section_for,
)
from runtime.kuuos_experiment_outcome_policy_records_v0_9 import (
    build_receipt,
    build_state_and_record,
    paths,
    pending_record,
    replay_result,
)
from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
    BLOCKED,
    DECISION_VERSION,
    READY,
    VERSION,
    ExperimentOutcomePolicyResult,
    append_jsonl,
    as_list,
    clamp,
    contains_graph_keys,
    decision_digest,
    integer,
    mapping,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    valid_digest,
    write_json,
)
from runtime.kuuos_experiment_outcome_policy_validation_v0_9 import (
    validate_bundle as validate_policy_bundle,
    validate_inputs,
)


def _pending_validation(
    *,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    sources: list[Mapping[str, Any]],
    capability_bundle: Mapping[str, Any],
    source_portfolio_bundle: Mapping[str, Any],
    experiment_bundle: Mapping[str, Any],
    policy_bundle: Mapping[str, Any],
    plan: Mapping[str, Any],
    license_packet: Mapping[str, Any],
    pending: Mapping[str, Any],
    source_batch: str,
    blockers: list[str],
) -> None:
    validate_root(root_packet, blockers)
    validate_adapter_registry(registry, blockers)
    validate_source_packets(
        sources,
        max_sources=integer(plan.get("max_sources_per_cycle"), 0),
        max_signals_per_source=integer(plan.get("max_signals_per_source"), 0),
        max_total_signals=integer(plan.get("max_total_signals"), 0),
        blockers=blockers,
    )
    validate_capability_bundle(
        capability_bundle, str(plan.get("agent_id", "")), blockers
    )
    validate_portfolio_bundle(
        source_portfolio_bundle, str(plan.get("agent_id", "")), blockers
    )
    validate_experiment_bundle(
        experiment_bundle,
        str(plan.get("agent_id", "")),
        str(source_portfolio_bundle.get("portfolio_bundle_digest", "")),
        blockers,
    )
    validate_policy_bundle(
        policy_bundle, str(plan.get("agent_id", "")), blockers
    )
    if not valid_digest(plan, "policy_plan_digest"):
        blockers.append("policy_plan_digest_invalid")
    if pending.get("policy_plan_digest") != plan.get("policy_plan_digest"):
        blockers.append("pending_policy_plan_digest_mismatch")
    if pending.get("source_batch_digest") != source_batch:
        blockers.append("pending_source_batch_digest_mismatch")
    expected = {
        "expected_previous_capability_state_digest": pending.get(
            "previous_capability_state_digest", ""
        ),
        "expected_previous_capability_bundle_digest": pending.get(
            "previous_capability_bundle_digest", ""
        ),
        "expected_source_portfolio_bundle_digest": pending.get(
            "source_portfolio_bundle_digest", ""
        ),
        "expected_previous_experiment_state_digest": pending.get(
            "previous_experiment_state_digest", ""
        ),
        "expected_previous_experiment_bundle_digest": pending.get(
            "previous_experiment_bundle_digest", ""
        ),
        "expected_previous_policy_state_digest": pending.get(
            "previous_policy_state_digest", ""
        ),
        "expected_previous_policy_bundle_digest": pending.get(
            "previous_policy_bundle_digest", ""
        ),
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"pending_{field}_mismatch")
    license_expected = {
        "bound_policy_plan_digest": plan.get("policy_plan_digest", ""),
        "bound_source_batch_digest": source_batch,
        "bound_previous_capability_bundle_digest": pending.get(
            "previous_capability_bundle_digest", ""
        ),
        "bound_source_portfolio_bundle_digest": pending.get(
            "source_portfolio_bundle_digest", ""
        ),
        "bound_previous_experiment_bundle_digest": pending.get(
            "previous_experiment_bundle_digest", ""
        ),
        "bound_previous_policy_bundle_digest": pending.get(
            "previous_policy_bundle_digest", ""
        ),
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"pending_license_{field}_mismatch")
    for field in (
        "one_child_experiment_cycle_allowed",
        "reobserve_routing_allowed",
        "policy_update_allowed",
        "policy_bundle_write_allowed",
        "policy_state_write_allowed",
        "decision_write_allowed",
        "outcome_write_allowed",
        "child_packet_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in (
        "multiple_child_cycles_allowed",
        "v0_8_hard_gate_bypass_allowed",
        "unbudgeted_trial_allowed",
        "shadow_execution_allowed",
        "external_network_effect_allowed",
        "world_update_allowed",
        "memory_overwrite_allowed",
    ):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))


def _load_recovery_packets(
    *,
    run_id: str,
    pending: Mapping[str, Any],
    p: Mapping[str, Any],
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    decision = read_json(p["decision"])
    child_plan = read_json(p["child_plan"])
    child_license = read_json(p["child_license"])
    child_registry = read_json(p["child_registry"])
    if (
        decision.get("version") != DECISION_VERSION
        or decision.get("policy_run_id") != run_id
        or decision.get("policy_decision_digest") != decision_digest(decision)
        or decision.get("policy_decision_digest")
        != pending.get("policy_decision_digest")
    ):
        blockers.append("pending_policy_decision_invalid")
    if (
        child_plan.get("experiment_plan_digest")
        != experiment_plan_digest(child_plan)
        or child_plan.get("experiment_plan_digest")
        != pending.get("child_experiment_plan_digest")
    ):
        blockers.append("pending_child_experiment_plan_invalid")
    if child_registry.get("adapter_registry_digest") != pending.get(
        "child_adapter_registry_digest"
    ):
        blockers.append("pending_child_registry_invalid")
    if child_license.get("bound_experiment_plan_digest") != child_plan.get(
        "experiment_plan_digest"
    ):
        blockers.append("pending_child_license_invalid")
    return decision, child_plan, child_license, child_registry


def build_experiment_outcome_policy(
    *,
    runtime_context: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    policy_plan: Mapping[str, Any],
    policy_license: Mapping[str, Any],
) -> ExperimentOutcomePolicyResult:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(policy_plan)
    license_packet = mapping(policy_license)
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
        experiment_bundle = empty_experiment_bundle(
            str(plan.get("agent_id", "")), source_portfolio_bundle
        )
        write_json(p["experiment_bundle"], experiment_bundle)
    policy_state = read_json(p["state"])
    policy_bundle = read_json(p["bundle"])
    if not policy_bundle:
        policy_bundle = empty_bundle(str(plan.get("agent_id", "")))
    ledger = read_jsonl(p["ledger"])
    run_id = str(plan.get("policy_run_id", ""))
    source_batch = batch_digest(sources)

    if any(row.get("_invalid") for row in ledger):
        blockers.append("policy_ledger_invalid")
    committed = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "committed"
            and row.get("policy_run_id") == run_id
        ),
        None,
    )
    if committed is not None:
        if committed.get("policy_plan_digest") == plan.get("policy_plan_digest"):
            return replay_result(committed, root, p)
        blockers.append("policy_run_id_reused_with_different_plan")
    pending = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "pending"
            and row.get("policy_run_id") == run_id
        ),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_policy_run")

    if context.get("experiment_outcome_policy_enabled") is not True:
        blockers.append("experiment_outcome_policy_enabled_not_true")
    if context.get("execute_one_policy_cycle") is not True:
        blockers.append("execute_one_policy_cycle_not_true")
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")
    if not capability_bundle:
        blockers.append("source_v0_6_capability_bundle_missing")
    if not source_portfolio_bundle:
        blockers.append("source_v0_7_portfolio_bundle_missing")
    if not experiment_bundle:
        blockers.append("source_v0_8_experiment_bundle_missing")

    if not blockers and pending is None:
        validate_inputs(
            root_packet=root_packet,
            registry=registry,
            sources=sources,
            capability_state=capability_state,
            capability_bundle=capability_bundle,
            source_portfolio_bundle=source_portfolio_bundle,
            experiment_state=experiment_state,
            experiment_bundle=experiment_bundle,
            policy_state=policy_state,
            policy_bundle=policy_bundle,
            plan=plan,
            license_packet=license_packet,
            source_batch_digest=source_batch,
            blockers=blockers,
        )
    elif not blockers:
        _pending_validation(
            root_packet=root_packet,
            registry=registry,
            sources=sources,
            capability_bundle=capability_bundle,
            source_portfolio_bundle=source_portfolio_bundle,
            experiment_bundle=experiment_bundle,
            policy_bundle=policy_bundle,
            plan=plan,
            license_packet=license_packet,
            pending=pending,
            source_batch=source_batch,
            blockers=blockers,
        )

    cycle_index = (
        integer(pending.get("cycle_index"), 0)
        if pending is not None
        else integer(policy_state.get("cycle_index"), 0) + 1
    )
    packet_id = "kuuos-experiment-policy-" + sha(
        {"run": run_id, "source_batch": source_batch, "cycle": cycle_index}
    )[:18]
    normalized_wake = normalize_sources(sources) if not blockers else {}
    decision: dict[str, Any] = {}
    child_plan: dict[str, Any] = {}
    child_license: dict[str, Any] = {}
    child_registry: dict[str, Any] = {}

    if not blockers and pending is not None:
        decision, child_plan, child_license, child_registry = _load_recovery_packets(
            run_id=run_id, pending=pending, p=p, blockers=blockers
        )
    elif not blockers:
        preview_registry = derive_policy_registry(registry, "preview")
        preview_plan = build_experiment_plan(
            policy_plan=plan,
            policy_decision={},
            source_packets=sources,
            root_packet=root_packet,
            child_registry=preview_registry,
            previous_capability_state=capability_state,
            previous_capability_bundle=capability_bundle,
            source_portfolio_bundle=source_portfolio_bundle,
            previous_experiment_state=experiment_state,
            previous_experiment_bundle=experiment_bundle,
            preview=True,
        )
        preview_license = build_experiment_license(
            child_plan=preview_plan,
            source_packets=sources,
            root_packet=root_packet,
            child_registry=preview_registry,
            previous_capability_bundle=capability_bundle,
            source_portfolio_bundle=source_portfolio_bundle,
            previous_experiment_bundle=experiment_bundle,
        )
        preview_decision, _ = build_experiment_decision(
            experiment_run_id=str(plan.get("policy_run_id", "")) + ":preview",
            cycle_index=integer(experiment_state.get("cycle_index"), 0) + 1,
            capability_bundle=capability_bundle,
            experiment_bundle=experiment_bundle,
            registry=preview_registry,
            source_packets=sources,
            normalized_wake=normalized_wake,
            plan=preview_plan,
            license_packet=preview_license,
            blockers=blockers,
        )
        if not blockers:
            decision = build_policy_decision(
                policy_run_id=run_id,
                cycle_index=cycle_index,
                policy_bundle=policy_bundle,
                experiment_bundle=experiment_bundle,
                preview_decision=preview_decision,
                plan=plan,
            )
            child_registry = derive_policy_registry(
                registry, str(decision.get("policy_mode", ""))
            )
            child_plan = build_experiment_plan(
                policy_plan=plan,
                policy_decision=decision,
                source_packets=sources,
                root_packet=root_packet,
                child_registry=child_registry,
                previous_capability_state=capability_state,
                previous_capability_bundle=capability_bundle,
                source_portfolio_bundle=source_portfolio_bundle,
                previous_experiment_state=experiment_state,
                previous_experiment_bundle=experiment_bundle,
            )
            child_license = build_experiment_license(
                child_plan=child_plan,
                source_packets=sources,
                root_packet=root_packet,
                child_registry=child_registry,
                previous_capability_bundle=capability_bundle,
                source_portfolio_bundle=source_portfolio_bundle,
                previous_experiment_bundle=experiment_bundle,
            )
            write_json(p["decision"], decision)
            write_json(p["child_plan"], child_plan)
            write_json(p["child_license"], child_license)
            write_json(p["child_registry"], child_registry)
            append_jsonl(
                p["ledger"],
                pending_record(
                    packet_id=packet_id,
                    run_id=run_id,
                    plan=plan,
                    source_batch_digest=source_batch,
                    previous_capability_state_digest=capability_state.get(
                        "capability_state_digest", ""
                    ),
                    previous_capability_bundle_digest=capability_bundle.get(
                        "capability_bundle_digest", ""
                    ),
                    source_portfolio_bundle_digest=source_portfolio_bundle.get(
                        "portfolio_bundle_digest", ""
                    ),
                    previous_experiment_state_digest=experiment_state.get(
                        "experiment_state_digest", ""
                    ),
                    previous_experiment_bundle_digest=experiment_bundle.get(
                        "experiment_bundle_digest", ""
                    ),
                    previous_policy_state_digest=policy_state.get(
                        "policy_state_digest", ""
                    ),
                    previous_policy_bundle_digest=policy_bundle.get(
                        "policy_bundle_digest", ""
                    ),
                    decision=decision,
                    child_plan=child_plan,
                    child_registry=child_registry,
                    cycle_index=cycle_index,
                ),
            )

    child_result: dict[str, Any] = {}
    if not blockers:
        child = build_bounded_portfolio_experiment(
            runtime_context={
                "runtime_root": str(root),
                "bounded_portfolio_experiment_enabled": True,
                "execute_one_experiment_cycle": True,
                "allowed_domain_actions": as_list(context.get("allowed_domain_actions")),
            },
            source_packets=sources,
            root_principles_packet=root_packet,
            adapter_registry=child_registry,
            experiment_plan=child_plan,
            experiment_license=child_license,
        )
        child_result = child.to_dict()
        if child.status not in {EXPERIMENT_READY, EXPERIMENT_REPLAYED}:
            blockers.extend([f"experiment_{item}" for item in child.blockers])

    child_experiment_bundle: dict[str, Any] = {}
    child_trial_record: dict[str, Any] = {}
    child_effect: dict[str, Any] = {}
    outcome: dict[str, Any] = {}
    updated_policy_bundle = policy_bundle
    if not blockers:
        child_experiment_bundle = read_json(p["experiment_bundle"])
        child_trial_record = read_json(p["experiment_trial"])
        child_effect = read_json(p["effect"])
        if child_effect.get("version") != EFFECT_VERSION:
            blockers.append("policy_child_effect_version_invalid")
        elif child_effect.get("effect_receipt_digest") != effect_digest(child_effect):
            blockers.append("policy_child_effect_digest_invalid")
        if child_effect.get("effect_receipt_digest") != child_result.get(
            "live_effect_receipt_digest"
        ):
            blockers.append("policy_child_effect_result_mismatch")
        if child_trial_record.get("live_effect_receipt_digest") != child_effect.get(
            "effect_receipt_digest"
        ):
            blockers.append("policy_child_trial_effect_mismatch")
        if child_result.get("decision_mode") != child_trial_record.get("decision_mode"):
            blockers.append("policy_child_decision_mode_mismatch")
        if decision.get("policy_mode") == "reobserve" and child_effect.get(
            "domain_action"
        ) != "observe":
            blockers.append("policy_reobserve_did_not_route_to_observe")

    if not blockers:
        updated_policy_bundle, outcome, replayed_update = commit_policy_outcome(
            policy_run_id=run_id,
            previous_bundle=policy_bundle,
            decision=decision,
            child_trial_record=child_trial_record,
            child_experiment_bundle=child_experiment_bundle,
            live_effect=child_effect,
            plan=plan,
            max_outcomes=integer(plan.get("max_policy_outcomes"), 256),
            max_holonomy=integer(plan.get("max_policy_holonomy"), 256),
        )
        if replayed_update:
            warnings.append("policy_effect_already_processed")
        write_json(p["outcome"], outcome)
        write_json(p["bundle"], updated_policy_bundle)

    status = READY if not blockers else BLOCKED
    if status == READY:
        state_base = policy_state
        if pending is not None and policy_state.get("policy_run_id") == run_id:
            state_base = {
                "policy_state_digest": pending.get("previous_policy_state_digest", ""),
                "total_cycles": max(0, integer(policy_state.get("total_cycles"), 1) - 1),
                "total_experiment_policy_cycles": max(
                    0,
                    integer(policy_state.get("total_experiment_policy_cycles"), 0)
                    - (1 if decision.get("policy_mode") == "experiment" else 0),
                ),
                "total_reobserve_policy_cycles": max(
                    0,
                    integer(policy_state.get("total_reobserve_policy_cycles"), 0)
                    - (1 if decision.get("policy_mode") == "reobserve" else 0),
                ),
                "total_exploit_policy_cycles": max(
                    0,
                    integer(policy_state.get("total_exploit_policy_cycles"), 0)
                    - (1 if decision.get("policy_mode") == "exploit" else 0),
                ),
            }
        state, row = build_state_and_record(
            previous_state=state_base,
            packet_id=packet_id,
            run_id=run_id,
            plan=plan,
            cycle_index=cycle_index,
            decision=decision,
            outcome=outcome,
            policy_bundle=updated_policy_bundle,
            child_experiment_bundle=child_experiment_bundle,
            child_effect=child_effect,
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
        policy_bundle=updated_policy_bundle,
        child_experiment_bundle=child_experiment_bundle,
        child_effect=child_effect,
        blockers=blockers,
        warnings=warnings,
    )
    if license_packet.get("receipt_write_allowed") is True:
        write_json(p["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(p["audit"], {**receipt, "audit_record_digest": sha(receipt)})

    section = section_for(
        updated_policy_bundle, str(decision.get("context_key", ""))
    )
    alpha = float(section.get("experiment_success_alpha", 1.0))
    beta = float(section.get("experiment_success_beta", 1.0))
    return ExperimentOutcomePolicyResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        policy_run_id=run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        context_key=str(decision.get("context_key", "")),
        policy_mode=str(decision.get("policy_mode", "")),
        policy_reason=str(decision.get("policy_reason", "")),
        preview_baseline_adapter_id=str(
            decision.get("preview_baseline_adapter_id", "")
        ),
        preview_experiment_adapter_id=str(
            decision.get("preview_experiment_adapter_id", "")
        ),
        child_decision_mode=str(outcome.get("child_decision_mode", "")),
        child_live_adapter_id=str(outcome.get("child_live_adapter_id", "")),
        adapted_minimum_information_gain=float(
            decision.get("adapted_minimum_information_gain", 0.0)
        ),
        adapted_trial_cooldown_cycles=integer(
            decision.get("adapted_trial_cooldown_cycles"), 0
        ),
        experiment_pressure=float(decision.get("experiment_pressure", 0.0)),
        reobserve_pressure=float(decision.get("reobserve_pressure", 0.0)),
        posterior_experiment_success=(alpha / (alpha + beta)) if alpha + beta else 0.5,
        mean_net_experiment_value=float(
            section.get("mean_net_experiment_value", 0.0)
        ),
        live_observed_utility=float(outcome.get("live_observed_utility", 0.0)),
        live_domain_action=str(outcome.get("live_domain_action", "")),
        compatible_shadow_resolved=outcome.get("compatible_shadow_resolved") is True,
        policy_bundle_digest=str(
            updated_policy_bundle.get("policy_bundle_digest", "")
        ),
        child_experiment_bundle_digest=str(
            child_experiment_bundle.get("experiment_bundle_digest", "")
        ),
        child_effect_receipt_digest=str(child_effect.get("effect_receipt_digest", "")),
        idempotent_replay=False,
        recovered_pending_run=recovered_pending,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]),
        outcome_path=str(p["outcome"]),
        child_plan_path=str(p["child_plan"]),
        child_license_path=str(p["child_license"]),
        child_registry_path=str(p["child_registry"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=blockers,
        warnings=warnings,
    )
