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
from runtime.kuuos_adapter_capability_gauge_core_v0_6 import (
    build_adapter_capability_gauge,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    READY as CAPABILITY_READY,
    REPLAYED as CAPABILITY_REPLAYED,
)
from runtime.kuuos_adapter_portfolio_shadow_model_v0_7 import (
    build_shadow_projections,
    commit_portfolio_update,
    resolve_previous_shadow,
)
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    SELECTION_VERSION as PORTFOLIO_SELECTION_VERSION,
    selection_digest as portfolio_selection_digest,
)
from runtime.kuuos_adapter_portfolio_shadow_validation_v0_7 import (
    validate_bundle as validate_source_portfolio_bundle,
)
from runtime.kuuos_bounded_portfolio_experiment_bridge_v0_8 import (
    build_experiment_child_packets,
    build_experiment_live_registry,
)
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import (
    build_execution_selection,
    build_experiment_decision,
    commit_cycle,
    empty_bundle,
    portfolio_view,
)
from runtime.kuuos_bounded_portfolio_experiment_records_v0_8 import (
    build_receipt,
    build_state_and_record,
    paths,
    pending_record,
    replay_result,
)
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    BLOCKED,
    DECISION_VERSION,
    READY,
    VERSION,
    BoundedPortfolioExperimentResult,
    append_jsonl,
    as_list,
    clamp,
    contains_graph_keys,
    decision_digest,
    integer,
    mapping,
    nonnegative,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    valid_digest,
    write_json,
)
from runtime.kuuos_bounded_portfolio_experiment_validation_v0_8 import (
    validate_bundle as validate_experiment_bundle,
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
    validate_source_portfolio_bundle(
        source_portfolio_bundle, str(plan.get("agent_id", "")), blockers
    )
    validate_experiment_bundle(
        experiment_bundle,
        str(plan.get("agent_id", "")),
        str(source_portfolio_bundle.get("portfolio_bundle_digest", "")),
        blockers,
    )
    if not valid_digest(plan, "experiment_plan_digest"):
        blockers.append("experiment_plan_digest_invalid")
    if pending.get("experiment_plan_digest") != plan.get("experiment_plan_digest"):
        blockers.append("pending_experiment_plan_digest_mismatch")
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
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"pending_{field}_mismatch")
    license_expected = {
        "bound_experiment_plan_digest": plan.get("experiment_plan_digest", ""),
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
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"pending_license_{field}_mismatch")
    for field in (
        "one_live_capability_cycle_allowed",
        "licensed_live_trial_allowed",
        "baseline_exploitation_allowed",
        "shadow_projection_allowed",
        "shadow_resolution_allowed",
        "trial_budget_debit_allowed",
        "experiment_bundle_write_allowed",
        "experiment_state_write_allowed",
        "decision_write_allowed",
        "selection_write_allowed",
        "projection_write_allowed",
        "resolution_write_allowed",
        "trial_record_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in (
        "multiple_live_adapters_allowed",
        "unbudgeted_trial_allowed",
        "shadow_execution_allowed",
        "shadow_external_actuation_allowed",
        "external_network_effect_allowed",
        "world_update_allowed",
        "memory_overwrite_allowed",
    ):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))


def _load_recovery_packets(
    *,
    run_id: str,
    source_batch: str,
    pending: Mapping[str, Any],
    decision_path,
    selection_path,
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    decision = read_json(decision_path)
    selection = read_json(selection_path)
    if (
        decision.get("version") != DECISION_VERSION
        or not valid_digest(decision, "experiment_decision_digest")
        or decision.get("experiment_run_id") != run_id
        or decision.get("source_batch_digest") != source_batch
        or decision.get("experiment_decision_digest")
        != pending.get("experiment_decision_digest")
    ):
        blockers.append("pending_experiment_decision_invalid")
    if (
        selection.get("version") != PORTFOLIO_SELECTION_VERSION
        or selection.get("portfolio_selection_digest")
        != portfolio_selection_digest(selection)
        or selection.get("experiment_decision_digest")
        != decision.get("experiment_decision_digest")
        or selection.get("live_adapter_id") != decision.get("live_adapter_id")
    ):
        blockers.append("pending_experiment_selection_invalid")
    return decision, selection


def build_bounded_portfolio_experiment(
    *,
    runtime_context: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    experiment_plan: Mapping[str, Any],
    experiment_license: Mapping[str, Any],
) -> BoundedPortfolioExperimentResult:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(experiment_plan)
    license_packet = mapping(experiment_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    p = paths(root)
    capability_state = read_json(p["capability_state"])
    capability_bundle = read_json(p["capability_bundle"])
    source_portfolio_bundle = read_json(p["source_portfolio_bundle"])
    experiment_state = read_json(p["state"])
    experiment_bundle = read_json(p["bundle"])
    if not experiment_bundle and source_portfolio_bundle:
        experiment_bundle = empty_bundle(
            str(plan.get("agent_id", "")), source_portfolio_bundle
        )
    ledger = read_jsonl(p["ledger"])
    run_id = str(plan.get("experiment_run_id", ""))
    source_batch = batch_digest(sources)

    if any(row.get("_invalid") for row in ledger):
        blockers.append("experiment_ledger_invalid")
    committed = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "committed"
            and row.get("experiment_run_id") == run_id
        ),
        None,
    )
    if committed is not None:
        if committed.get("experiment_plan_digest") == plan.get(
            "experiment_plan_digest"
        ):
            return replay_result(committed, root, p)
        blockers.append("experiment_run_id_reused_with_different_plan")
    pending = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "pending"
            and row.get("experiment_run_id") == run_id
        ),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_experiment_run")

    if context.get("bounded_portfolio_experiment_enabled") is not True:
        blockers.append("bounded_portfolio_experiment_enabled_not_true")
    if context.get("execute_one_experiment_cycle") is not True:
        blockers.append("execute_one_experiment_cycle_not_true")
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")
    if not source_portfolio_bundle:
        blockers.append("source_v0_7_portfolio_bundle_missing")
    if not capability_bundle:
        blockers.append("source_v0_6_capability_bundle_missing")

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
            plan=plan,
            license_packet=license_packet,
            pending=pending,
            source_batch=source_batch,
            blockers=blockers,
        )

    cycle_index = (
        integer(pending.get("cycle_index"), 0)
        if pending is not None
        else integer(experiment_state.get("cycle_index"), 0) + 1
    )
    packet_id = "kuuos-bounded-experiment-" + sha(
        {"run": run_id, "source_batch": source_batch, "cycle": cycle_index}
    )[:18]
    normalized_wake = normalize_sources(sources) if not blockers else {}
    decision: dict[str, Any] = {}
    selection: dict[str, Any] = {}

    if not blockers and pending is not None:
        decision, selection = _load_recovery_packets(
            run_id=run_id,
            source_batch=source_batch,
            pending=pending,
            decision_path=p["decision"],
            selection_path=p["selection"],
            blockers=blockers,
        )
    elif not blockers:
        decision, _ = build_experiment_decision(
            experiment_run_id=run_id,
            cycle_index=cycle_index,
            capability_bundle=capability_bundle,
            experiment_bundle=experiment_bundle,
            registry=registry,
            source_packets=sources,
            normalized_wake=normalized_wake,
            plan=plan,
            license_packet=license_packet,
            blockers=blockers,
        )
        selection = build_execution_selection(
            experiment_run_id=run_id,
            decision=decision,
            capability_bundle=capability_bundle,
            experiment_bundle=experiment_bundle,
            registry=registry,
            source_packets=sources,
            normalized_wake=normalized_wake,
            plan=plan,
            blockers=blockers,
        )
        if not blockers:
            write_json(p["decision"], decision)
            write_json(p["selection"], selection)
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
                    decision=decision,
                    cycle_index=cycle_index,
                ),
            )

    child_result: dict[str, Any] = {}
    if not blockers:
        live_registry = build_experiment_live_registry(registry, decision)
        prior_capability_state = capability_state
        prior_capability_bundle = capability_bundle
        if pending is not None:
            prior_capability_state = {
                "capability_state_digest": pending.get(
                    "previous_capability_state_digest", ""
                )
            }
            prior_capability_bundle = {
                "capability_bundle_digest": pending.get(
                    "previous_capability_bundle_digest", ""
                )
            }
        child_plan, child_license = build_experiment_child_packets(
            experiment_plan=plan,
            source_packets=sources,
            root_packet=root_packet,
            derived_registry=live_registry,
            previous_capability_state=prior_capability_state,
            previous_capability_bundle=prior_capability_bundle,
        )
        child = build_adapter_capability_gauge(
            runtime_context={
                "runtime_root": str(root),
                "adapter_capability_gauge_enabled": True,
                "execute_one_capability_cycle": True,
                "allowed_domain_actions": as_list(context.get("allowed_domain_actions")),
            },
            source_packets=sources,
            root_principles_packet=root_packet,
            adapter_registry=live_registry,
            capability_plan=child_plan,
            capability_license=child_license,
        )
        child_result = child.to_dict()
        if child.status not in {CAPABILITY_READY, CAPABILITY_REPLAYED}:
            blockers.extend([f"capability_{item}" for item in child.blockers])
        if child.selected_federation_adapter_id != decision.get("live_adapter_id"):
            blockers.append("experiment_live_adapter_child_mismatch")

    live_effect_digest = ""
    live_observed_utility = 0.0
    effect_outcome = ""
    covariant_step_kind = ""
    if not blockers:
        calibration = read_json(p["capability_calibration"])
        effect = read_json(p["effect"])
        intervention_receipt = read_json(p["intervention_receipt"])
        if effect.get("version") != EFFECT_VERSION:
            blockers.append("experiment_live_effect_version_invalid")
        elif effect.get("effect_receipt_digest") != effect_digest(effect):
            blockers.append("experiment_live_effect_digest_invalid")
        live_effect_digest = str(effect.get("effect_receipt_digest", ""))
        if live_effect_digest != child_result.get("effect_receipt_digest"):
            blockers.append("experiment_live_effect_child_mismatch")
        if calibration.get("effect_receipt_digest") != live_effect_digest:
            blockers.append("experiment_live_calibration_effect_mismatch")
        live_observed_utility = clamp(calibration.get("observed_utility"), 0.0)
        effect_outcome = str(effect.get("outcome", ""))
        covariant_step_kind = str(intervention_receipt.get("covariant_step_kind", ""))
        if not covariant_step_kind:
            blockers.append("experiment_covariant_step_kind_missing")

    resolution: dict[str, Any] = {}
    projection: dict[str, Any] = {}
    trial_record: dict[str, Any] = {}
    updated_bundle = experiment_bundle
    if not blockers:
        processed = {
            str(item)
            for item in as_list(
                experiment_bundle.get("processed_experiment_effect_digests")
            )
        }
        if live_effect_digest in processed:
            resolution = read_json(p["resolution"])
            projection = read_json(p["projection"])
            trial_record = read_json(p["trial"])
            updated_bundle = experiment_bundle
            warnings.append("experiment_update_recovered_without_duplicate_budget_debit")
        else:
            working_portfolio = portfolio_view(experiment_bundle)
            resolved_portfolio, resolution, _ = resolve_previous_shadow(
                portfolio_run_id=run_id + ":experiment",
                bundle=working_portfolio,
                live_adapter_id=str(decision.get("live_adapter_id", "")),
                context_key=str(decision.get("context_key", "")),
                covariant_step_kind=covariant_step_kind,
                live_observed_utility=live_observed_utility,
                live_effect_receipt_digest=live_effect_digest,
                shadow_learning_rate=clamp(plan.get("shadow_learning_rate")),
                reliability_prior_mass=float(plan.get("reliability_prior_mass", 2.0)),
            )
            projection, projections = build_shadow_projections(
                portfolio_run_id=run_id + ":experiment",
                selection=selection,
                bundle=resolved_portfolio,
                registry=registry,
                covariant_step_kind=covariant_step_kind,
                live_observed_utility=live_observed_utility,
                live_effect_receipt_digest=live_effect_digest,
                action_utility=mapping(plan.get("shadow_action_utility")),
                shadow_model_weight=clamp(plan.get("shadow_model_weight")),
                max_shadow_candidates=integer(plan.get("max_shadow_candidates"), 1),
                default_prediction_confidence=clamp(
                    plan.get("default_prediction_confidence")
                ),
            )
            updated_portfolio, replayed_portfolio = commit_portfolio_update(
                portfolio_run_id=run_id + ":experiment",
                bundle=resolved_portfolio,
                selection=selection,
                resolution=resolution,
                projections=projections,
                live_observed_utility=live_observed_utility,
                live_effect_receipt_digest=live_effect_digest,
                max_pending_predictions=integer(
                    plan.get("max_pending_predictions"), 256
                ),
                max_resolved_predictions=integer(
                    plan.get("max_resolved_predictions"), 256
                ),
                max_holonomy=integer(plan.get("max_portfolio_holonomy"), 256),
            )
            if replayed_portfolio:
                warnings.append("working_portfolio_effect_already_processed")
            updated_bundle, trial_record, replayed_cycle = commit_cycle(
                experiment_run_id=run_id,
                previous_bundle=experiment_bundle,
                updated_portfolio=updated_portfolio,
                decision=decision,
                live_observed_utility=live_observed_utility,
                live_effect_receipt_digest=live_effect_digest,
                effect_outcome=effect_outcome,
                resolved_shadow=resolution.get("resolved") is True,
                max_trial_records=integer(plan.get("max_trial_records"), 256),
                max_decision_holonomy=integer(
                    plan.get("max_decision_holonomy"), 256
                ),
            )
            if replayed_cycle:
                warnings.append("experiment_effect_already_processed")
            write_json(p["resolution"], resolution)
            write_json(p["projection"], projection)
            write_json(p["trial"], trial_record)
            write_json(p["bundle"], updated_bundle)

    status = READY if not blockers else BLOCKED
    if status == READY:
        state_base = experiment_state
        if pending is not None and experiment_state.get("experiment_run_id") == run_id:
            state_base = {
                "experiment_state_digest": pending.get(
                    "previous_experiment_state_digest", ""
                ),
                "total_cycles": max(
                    0, integer(experiment_state.get("total_cycles"), 1) - 1
                ),
            }
        state, row = build_state_and_record(
            previous_state=state_base,
            packet_id=packet_id,
            run_id=run_id,
            plan=plan,
            cycle_index=cycle_index,
            decision=decision,
            selection=selection,
            projection=projection,
            resolution=resolution,
            trial_record=trial_record,
            bundle=updated_bundle,
            child_result=child_result,
            live_effect_receipt_digest=live_effect_digest,
        )
        write_json(p["state"], state)
        append_jsonl(p["ledger"], row)

    receipt = build_receipt(
        status=status,
        packet_id=packet_id,
        run_id=run_id,
        cycle_index=cycle_index,
        plan=plan,
        decision=decision,
        projection=projection,
        resolution=resolution,
        trial_record=trial_record,
        bundle=updated_bundle,
        child_result=child_result,
        live_effect_receipt_digest=live_effect_digest,
        blockers=blockers,
        warnings=warnings,
    )
    if license_packet.get("receipt_write_allowed") is True:
        write_json(p["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(p["audit"], {**receipt, "audit_record_digest": sha(receipt)})

    total_budget = nonnegative(plan.get("total_trial_budget"), 0.0)
    spent_after = nonnegative(updated_bundle.get("trial_budget_spent"), 0.0)
    spent_before = nonnegative(trial_record.get("trial_budget_spent_before"), spent_after)
    return BoundedPortfolioExperimentResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        experiment_run_id=run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        context_key=str(decision.get("context_key", "")),
        decision_mode=str(decision.get("decision_mode", "")),
        baseline_adapter_id=str(decision.get("baseline_adapter_id", "")),
        live_adapter_id=str(decision.get("live_adapter_id", "")),
        experiment_adapter_id=str(decision.get("experiment_adapter_id", "")),
        expected_information_gain=float(
            decision.get("expected_information_gain", 0.0)
        ),
        trial_cost=float(trial_record.get("trial_cost", 0.0)),
        trial_risk=float(decision.get("trial_risk", 0.0)),
        trial_recoverability=float(decision.get("trial_recoverability", 1.0)),
        trial_budget_before=max(0.0, total_budget - spent_before),
        trial_budget_after=max(0.0, total_budget - spent_after),
        total_trial_count=integer(updated_bundle.get("total_trial_count"), 0),
        total_exploit_count=integer(updated_bundle.get("total_exploit_count"), 0),
        shadow_projection_count=integer(projection.get("projection_count"), 0),
        resolved_shadow_count=1 if resolution.get("resolved") is True else 0,
        child_capability_status=str(child_result.get("status", "")),
        child_capability_run_id=str(child_result.get("capability_run_id", "")),
        live_effect_receipt_digest=live_effect_digest,
        experiment_bundle_digest=str(
            updated_bundle.get("experiment_bundle_digest", "")
        ),
        idempotent_replay=False,
        recovered_pending_run=recovered_pending,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]),
        selection_path=str(p["selection"]),
        projection_path=str(p["projection"]),
        resolution_path=str(p["resolution"]),
        trial_path=str(p["trial"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=blockers,
        warnings=warnings,
    )
