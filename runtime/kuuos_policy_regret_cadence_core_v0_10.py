#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_adapter_capability_gauge_model_v0_6 import context_signature
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import batch_digest
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import (
    empty_bundle as empty_experiment_bundle,
)
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    normalize_sources,
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_experiment_outcome_policy_core_v0_9 import (
    build_experiment_outcome_policy,
)
from runtime.kuuos_experiment_outcome_policy_model_v0_9 import (
    empty_bundle as empty_policy_bundle,
)
from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
    OUTCOME_VERSION as POLICY_OUTCOME_VERSION,
    READY as POLICY_READY,
    REPLAYED as POLICY_REPLAYED,
    outcome_digest as policy_outcome_digest,
    plan_digest as policy_plan_digest,
)
from runtime.kuuos_policy_regret_cadence_bridge_v0_10 import (
    build_child_policy_license,
    build_child_policy_plan,
)
from runtime.kuuos_policy_regret_cadence_model_v0_10 import (
    build_counterfactual_outcome,
    build_regret_decision,
    empty_bundle,
    section_for,
)
from runtime.kuuos_policy_regret_cadence_records_v0_10 import (
    build_receipt,
    build_state_and_record,
    paths,
    pending_record,
    replay_result,
)
from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
    BLOCKED,
    DECISION_VERSION,
    READY,
    VERSION,
    PolicyRegretCadenceResult,
    append_jsonl,
    as_list,
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
from runtime.kuuos_policy_regret_cadence_validation_v0_10 import (
    validate_inputs,
)


def _pending_validation(
    *,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    sources: list[Mapping[str, Any]],
    plan: Mapping[str, Any],
    license_packet: Mapping[str, Any],
    pending: Mapping[str, Any],
    source_batch: str,
    blockers: list[str],
) -> None:
    validate_adapter_registry(registry, blockers)
    validate_source_packets(
        sources,
        max_sources=integer(plan.get("max_sources_per_cycle"), 0),
        max_signals_per_source=integer(plan.get("max_signals_per_source"), 0),
        max_total_signals=integer(plan.get("max_total_signals"), 0),
        blockers=blockers,
    )
    if not valid_digest(plan, "regret_plan_digest"):
        blockers.append("regret_plan_digest_invalid")
    if pending.get("regret_plan_digest") != plan.get("regret_plan_digest"):
        blockers.append("pending_regret_plan_digest_mismatch")
    if pending.get("source_batch_digest") != source_batch:
        blockers.append("pending_source_batch_digest_mismatch")
    if plan.get("expected_root_principles_digest") != root_packet.get(
        "root_principles_digest", ""
    ):
        blockers.append("pending_root_principles_digest_mismatch")
    if plan.get("expected_adapter_registry_digest") != registry.get(
        "adapter_registry_digest", ""
    ):
        blockers.append("pending_adapter_registry_digest_mismatch")
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
        "expected_previous_regret_state_digest": pending.get(
            "previous_regret_state_digest", ""
        ),
        "expected_previous_regret_bundle_digest": pending.get(
            "previous_regret_bundle_digest", ""
        ),
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"pending_{field}_mismatch")
    license_expected = {
        "bound_regret_plan_digest": plan.get("regret_plan_digest", ""),
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
        "bound_previous_regret_bundle_digest": pending.get(
            "previous_regret_bundle_digest", ""
        ),
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"pending_license_{field}_mismatch")
    for field in (
        "one_child_policy_cycle_allowed",
        "counterfactual_estimation_allowed",
        "regret_update_allowed",
        "cadence_adaptation_allowed",
        "regret_bundle_write_allowed",
        "regret_state_write_allowed",
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
        "multiple_child_policy_cycles_allowed",
        "counterfactual_truth_promotion_allowed",
        "unexecuted_alternative_outcome_allowed",
        "v0_9_authority_bypass_allowed",
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
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    decision = read_json(p["decision"])
    child_plan = read_json(p["child_plan"])
    child_license = read_json(p["child_license"])
    if (
        decision.get("version") != DECISION_VERSION
        or decision.get("regret_run_id") != run_id
        or decision.get("regret_decision_digest") != decision_digest(decision)
        or decision.get("regret_decision_digest")
        != pending.get("regret_decision_digest")
    ):
        blockers.append("pending_regret_decision_invalid")
    if (
        child_plan.get("policy_plan_digest") != policy_plan_digest(child_plan)
        or child_plan.get("policy_plan_digest")
        != pending.get("child_policy_plan_digest")
    ):
        blockers.append("pending_child_policy_plan_invalid")
    if child_license.get("bound_policy_plan_digest") != child_plan.get(
        "policy_plan_digest"
    ):
        blockers.append("pending_child_policy_license_invalid")
    return decision, child_plan, child_license


def build_policy_regret_cadence(
    *,
    runtime_context: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    regret_plan: Mapping[str, Any],
    regret_license: Mapping[str, Any],
) -> PolicyRegretCadenceResult:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(regret_plan)
    license_packet = mapping(regret_license)
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
    policy_state = read_json(p["policy_state"])
    policy_bundle = read_json(p["policy_bundle"])
    if not policy_bundle:
        policy_bundle = empty_policy_bundle(str(plan.get("agent_id", "")))
        write_json(p["policy_bundle"], policy_bundle)
    regret_state = read_json(p["state"])
    regret_bundle = read_json(p["bundle"])
    if not regret_bundle:
        regret_bundle = empty_bundle(str(plan.get("agent_id", "")))

    ledger = read_jsonl(p["ledger"])
    run_id = str(plan.get("regret_run_id", ""))
    source_batch = batch_digest(sources)
    if any(row.get("_invalid") for row in ledger):
        blockers.append("regret_ledger_invalid")
    committed = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "committed"
            and row.get("regret_run_id") == run_id
        ),
        None,
    )
    if committed is not None:
        if committed.get("regret_plan_digest") == plan.get("regret_plan_digest"):
            return replay_result(committed, root, p)
        blockers.append("regret_run_id_reused_with_different_plan")
    pending = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "pending"
            and row.get("regret_run_id") == run_id
        ),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_regret_run")

    if context.get("policy_regret_cadence_enabled") is not True:
        blockers.append("policy_regret_cadence_enabled_not_true")
    if context.get("execute_one_regret_cycle") is not True:
        blockers.append("execute_one_regret_cycle_not_true")
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")
    if not capability_bundle:
        blockers.append("source_v0_6_capability_bundle_missing")
    if not source_portfolio_bundle:
        blockers.append("source_v0_7_portfolio_bundle_missing")
    if not experiment_bundle:
        blockers.append("source_v0_8_experiment_bundle_missing")
    if not policy_bundle:
        blockers.append("source_v0_9_policy_bundle_missing")

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
            regret_state=regret_state,
            regret_bundle=regret_bundle,
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
            plan=plan,
            license_packet=license_packet,
            pending=pending,
            source_batch=source_batch,
            blockers=blockers,
        )

    normalized_wake = normalize_sources(sources) if not blockers else {}
    context_key, _ = context_signature(sources, normalized_wake) if not blockers else ("", {})
    cycle_index = (
        integer(pending.get("cycle_index"), 0)
        if pending is not None
        else integer(regret_state.get("cycle_index"), 0) + 1
    )
    packet_id = "kuuos-regret-cadence-" + sha(
        {"run": run_id, "source_batch": source_batch, "cycle": cycle_index}
    )[:18]
    decision: dict[str, Any] = {}
    child_plan: dict[str, Any] = {}
    child_license: dict[str, Any] = {}

    if not blockers and pending is not None:
        decision, child_plan, child_license = _load_recovery_packets(
            run_id=run_id, pending=pending, p=p, blockers=blockers
        )
    elif not blockers:
        decision = build_regret_decision(
            regret_run_id=run_id,
            cycle_index=cycle_index,
            context_key=context_key,
            regret_bundle=regret_bundle,
            policy_bundle=policy_bundle,
            plan=plan,
        )
        child_plan = build_child_policy_plan(
            regret_plan=plan,
            regret_decision=decision,
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
        )
        child_license = build_child_policy_license(
            child_plan=child_plan,
            source_packets=sources,
            root_packet=root_packet,
            adapter_registry=registry,
            previous_capability_bundle=capability_bundle,
            source_portfolio_bundle=source_portfolio_bundle,
            previous_experiment_bundle=experiment_bundle,
            previous_policy_bundle=policy_bundle,
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
                previous_regret_state_digest=regret_state.get(
                    "regret_state_digest", ""
                ),
                previous_regret_bundle_digest=regret_bundle.get(
                    "regret_bundle_digest", ""
                ),
                decision=decision,
                child_plan=child_plan,
                cycle_index=cycle_index,
            ),
        )

    child_result: dict[str, Any] = {}
    if not blockers:
        child = build_experiment_outcome_policy(
            runtime_context={
                "runtime_root": str(root),
                "experiment_outcome_policy_enabled": True,
                "execute_one_policy_cycle": True,
                "allowed_domain_actions": as_list(context.get("allowed_domain_actions")),
            },
            source_packets=sources,
            root_principles_packet=root_packet,
            adapter_registry=registry,
            policy_plan=child_plan,
            policy_license=child_license,
        )
        child_result = child.to_dict()
        if child.status not in {POLICY_READY, POLICY_REPLAYED}:
            blockers.extend([f"policy_{item}" for item in child.blockers])

    child_policy_bundle: dict[str, Any] = {}
    child_policy_outcome: dict[str, Any] = {}
    current_experiment_bundle: dict[str, Any] = {}
    outcome: dict[str, Any] = {}
    updated_regret_bundle = regret_bundle
    if not blockers:
        child_policy_bundle = read_json(p["policy_bundle"])
        child_policy_outcome = read_json(p["policy_outcome"])
        current_experiment_bundle = read_json(p["experiment_bundle"])
        if child_policy_outcome.get("version") != POLICY_OUTCOME_VERSION:
            blockers.append("regret_child_policy_outcome_version_invalid")
        elif child_policy_outcome.get("policy_outcome_digest") != policy_outcome_digest(
            child_policy_outcome
        ):
            blockers.append("regret_child_policy_outcome_digest_invalid")
        if child_policy_outcome.get("policy_outcome_digest") != child_result.get(
            "policy_bundle_digest", ""
        ) and child_result.get("policy_bundle_digest") == child_policy_outcome.get(
            "policy_outcome_digest"
        ):
            blockers.append("regret_child_result_internal_digest_collision")
        if child_policy_outcome.get("policy_mode") != child_result.get("policy_mode"):
            blockers.append("regret_child_policy_mode_mismatch")
        if child_policy_outcome.get("child_effect_receipt_digest") != child_result.get(
            "child_effect_receipt_digest"
        ):
            blockers.append("regret_child_effect_digest_mismatch")

    if not blockers:
        updated_regret_bundle, outcome, replayed_update = build_counterfactual_outcome(
            regret_run_id=run_id,
            cycle_index=cycle_index,
            previous_regret_bundle=regret_bundle,
            previous_policy_bundle=policy_bundle,
            child_policy_bundle=child_policy_bundle,
            child_policy_outcome=child_policy_outcome,
            experiment_bundle=current_experiment_bundle,
            decision=decision,
            plan=plan,
            max_outcomes=integer(plan.get("max_regret_outcomes"), 256),
            max_holonomy=integer(plan.get("max_regret_holonomy"), 256),
        )
        if replayed_update:
            warnings.append("policy_outcome_already_processed_for_regret")
        write_json(p["outcome"], outcome)
        write_json(p["bundle"], updated_regret_bundle)

    status = READY if not blockers else BLOCKED
    if status == READY:
        state_base = regret_state
        if pending is not None and regret_state.get("regret_run_id") == run_id:
            state_base = {
                "regret_state_digest": pending.get("previous_regret_state_digest", ""),
                "total_cycles": max(0, integer(regret_state.get("total_cycles"), 1) - 1),
                "total_positive_regret_cycles": max(
                    0,
                    integer(regret_state.get("total_positive_regret_cycles"), 0)
                    - (1 if float(outcome.get("bounded_regret", 0.0)) > 0.0 else 0),
                ),
                "total_zero_regret_cycles": max(
                    0,
                    integer(regret_state.get("total_zero_regret_cycles"), 0)
                    - (1 if float(outcome.get("bounded_regret", 0.0)) <= 0.0 else 0),
                ),
                "total_experiment_children": max(
                    0,
                    integer(regret_state.get("total_experiment_children"), 0)
                    - (1 if outcome.get("child_policy_mode") == "experiment" else 0),
                ),
                "total_reobserve_children": max(
                    0,
                    integer(regret_state.get("total_reobserve_children"), 0)
                    - (1 if outcome.get("child_policy_mode") == "reobserve" else 0),
                ),
                "total_exploit_children": max(
                    0,
                    integer(regret_state.get("total_exploit_children"), 0)
                    - (1 if outcome.get("child_policy_mode") == "exploit" else 0),
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
            regret_bundle=updated_regret_bundle,
            child_policy_bundle=child_policy_bundle,
            child_policy_outcome=child_policy_outcome,
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
        regret_bundle=updated_regret_bundle,
        child_policy_bundle=child_policy_bundle,
        child_policy_outcome=child_policy_outcome,
        blockers=blockers,
        warnings=warnings,
    )
    if license_packet.get("receipt_write_allowed") is True:
        write_json(p["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(p["audit"], {**receipt, "audit_record_digest": sha(receipt)})

    section = section_for(updated_regret_bundle, str(decision.get("context_key", "")))
    return PolicyRegretCadenceResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        regret_run_id=run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        context_key=str(decision.get("context_key", "")),
        child_policy_mode=str(outcome.get("child_policy_mode", "")),
        child_policy_reason=str(child_policy_outcome.get("policy_reason", "")),
        child_live_adapter_id=str(
            child_policy_outcome.get("child_live_adapter_id", "")
        ),
        child_live_domain_action=str(
            child_policy_outcome.get("live_domain_action", "")
        ),
        chosen_value=float(outcome.get("chosen_value", 0.0)),
        best_alternative_mode=str(outcome.get("best_alternative_mode", "")),
        best_alternative_value=float(outcome.get("best_alternative_value", 0.0)),
        best_alternative_confidence=float(
            outcome.get("best_alternative_confidence", 0.0)
        ),
        bounded_regret=float(outcome.get("bounded_regret", 0.0)),
        experiment_regret_credit=float(
            section.get("experiment_regret_credit", 0.0)
        ),
        reobserve_regret_credit=float(
            section.get("reobserve_regret_credit", 0.0)
        ),
        exploit_regret_credit=float(section.get("exploit_regret_credit", 0.0)),
        adapted_experiment_pressure_threshold=float(
            decision.get("adapted_experiment_pressure_threshold", 0.0)
        ),
        adapted_reobserve_pressure_threshold=float(
            decision.get("adapted_reobserve_pressure_threshold", 0.0)
        ),
        adapted_experiment_interval=integer(
            decision.get("adapted_experiment_interval"), 0
        ),
        adapted_reobserve_interval=integer(
            decision.get("adapted_reobserve_interval"), 0
        ),
        delayed_compatible_evidence_count=integer(
            outcome.get("delayed_compatible_evidence_count"), 0
        ),
        pending_counterfactual_evidence_count=integer(
            outcome.get("pending_counterfactual_evidence_count"), 0
        ),
        regret_bundle_digest=str(updated_regret_bundle.get("regret_bundle_digest", "")),
        child_policy_bundle_digest=str(
            child_policy_bundle.get("policy_bundle_digest", "")
        ),
        child_policy_outcome_digest=str(
            child_policy_outcome.get("policy_outcome_digest", "")
        ),
        child_effect_receipt_digest=str(
            child_policy_outcome.get("child_effect_receipt_digest", "")
        ),
        idempotent_replay=False,
        recovered_pending_run=recovered_pending,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]),
        outcome_path=str(p["outcome"]),
        child_plan_path=str(p["child_plan"]),
        child_license_path=str(p["child_license"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=blockers,
        warnings=warnings,
    )
