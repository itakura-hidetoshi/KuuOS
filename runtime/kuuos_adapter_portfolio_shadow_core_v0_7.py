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
from runtime.kuuos_adapter_capability_gauge_model_v0_6 import (
    empty_bundle as empty_capability_bundle,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    READY as CAPABILITY_READY,
    REPLAYED as CAPABILITY_REPLAYED,
    STATE_VERSION as CAPABILITY_STATE_VERSION,
)
from runtime.kuuos_adapter_portfolio_shadow_bridge_v0_7 import (
    build_child_capability_packets,
    derived_live_registry,
)
from runtime.kuuos_adapter_portfolio_shadow_model_v0_7 import (
    build_portfolio_selection,
    build_shadow_projections,
    commit_portfolio_update,
    empty_bundle,
    resolve_previous_shadow,
)
from runtime.kuuos_adapter_portfolio_shadow_records_v0_7 import (
    build_receipt,
    build_state_and_record,
    paths,
    pending_record,
    replay_result,
)
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    BLOCKED,
    READY,
    RESOLUTION_VERSION,
    SELECTION_VERSION,
    VERSION,
    AdapterPortfolioShadowResult,
    append_jsonl,
    as_list,
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
from runtime.kuuos_adapter_portfolio_shadow_validation_v0_7 import (
    validate_bundle as validate_portfolio_bundle,
    validate_inputs,
)


def _pending_validation(
    *,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    sources: list[Mapping[str, Any]],
    capability_state: Mapping[str, Any],
    capability_bundle: Mapping[str, Any],
    portfolio_state: Mapping[str, Any],
    portfolio_bundle: Mapping[str, Any],
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
        portfolio_bundle, str(plan.get("agent_id", "")), blockers
    )
    if capability_state and (
        capability_state.get("version") != CAPABILITY_STATE_VERSION
        or not valid_digest(capability_state, "capability_state_digest")
    ):
        blockers.append("current_capability_state_invalid_during_recovery")
    if not valid_digest(plan, "portfolio_plan_digest"):
        blockers.append("portfolio_plan_digest_invalid")
    if pending.get("portfolio_plan_digest") != plan.get("portfolio_plan_digest"):
        blockers.append("pending_portfolio_plan_digest_mismatch")
    if pending.get("source_batch_digest") != source_batch:
        blockers.append("pending_source_batch_digest_mismatch")
    expected_pending = {
        "expected_previous_capability_state_digest": pending.get(
            "previous_capability_state_digest", ""
        ),
        "expected_previous_capability_bundle_digest": pending.get(
            "previous_capability_bundle_digest", ""
        ),
        "expected_previous_portfolio_state_digest": pending.get(
            "previous_portfolio_state_digest", ""
        ),
        "expected_previous_portfolio_bundle_digest": pending.get(
            "previous_portfolio_bundle_digest", ""
        ),
    }
    for field, expected in expected_pending.items():
        if plan.get(field, "") != expected:
            blockers.append(f"pending_{field}_mismatch")
    if license_packet.get("bound_portfolio_plan_digest") != plan.get(
        "portfolio_plan_digest"
    ):
        blockers.append("pending_license_plan_digest_mismatch")
    if license_packet.get("bound_source_batch_digest") != source_batch:
        blockers.append("pending_license_source_batch_digest_mismatch")
    if license_packet.get("bound_previous_capability_bundle_digest") != pending.get(
        "previous_capability_bundle_digest", ""
    ):
        blockers.append("pending_license_capability_bundle_digest_mismatch")
    if license_packet.get("bound_previous_portfolio_bundle_digest") != pending.get(
        "previous_portfolio_bundle_digest", ""
    ):
        blockers.append("pending_license_portfolio_bundle_digest_mismatch")
    for field in (
        "one_live_capability_cycle_allowed",
        "shadow_projection_allowed",
        "shadow_resolution_allowed",
        "portfolio_bundle_write_allowed",
        "portfolio_state_write_allowed",
        "selection_write_allowed",
        "projection_write_allowed",
        "resolution_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in (
        "shadow_execution_allowed",
        "shadow_external_actuation_allowed",
        "shadow_world_update_allowed",
        "shadow_capability_connection_update_allowed",
        "external_network_effect_allowed",
    ):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))


def build_adapter_portfolio_shadow(
    *,
    runtime_context: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    portfolio_plan: Mapping[str, Any],
    portfolio_license: Mapping[str, Any],
) -> AdapterPortfolioShadowResult:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(portfolio_plan)
    license_packet = mapping(portfolio_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    p = paths(root)
    capability_state = read_json(p["capability_state"])
    capability_bundle = read_json(p["capability_bundle"])
    if not capability_bundle:
        capability_bundle = empty_capability_bundle(str(plan.get("agent_id", "")))
    portfolio_state = read_json(p["state"])
    portfolio_bundle = read_json(p["bundle"])
    if not portfolio_bundle:
        portfolio_bundle = empty_bundle(str(plan.get("agent_id", "")))
    ledger = read_jsonl(p["ledger"])
    run_id = str(plan.get("portfolio_run_id", ""))
    source_batch = batch_digest(sources)

    if any(row.get("_invalid") for row in ledger):
        blockers.append("portfolio_ledger_invalid")
    committed = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "committed"
            and row.get("portfolio_run_id") == run_id
        ),
        None,
    )
    if committed is not None:
        if committed.get("portfolio_plan_digest") == plan.get(
            "portfolio_plan_digest"
        ):
            return replay_result(committed, root, p)
        blockers.append("portfolio_run_id_reused_with_different_plan")
    pending = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "pending"
            and row.get("portfolio_run_id") == run_id
        ),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_portfolio_run")

    if context.get("adapter_portfolio_shadow_enabled") is not True:
        blockers.append("adapter_portfolio_shadow_enabled_not_true")
    if context.get("execute_one_portfolio_cycle") is not True:
        blockers.append("execute_one_portfolio_cycle_not_true")
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")
    if pending is None:
        validate_inputs(
            root_packet=root_packet,
            registry=registry,
            sources=sources,
            capability_state=capability_state,
            capability_bundle=capability_bundle,
            portfolio_state=portfolio_state,
            portfolio_bundle=portfolio_bundle,
            plan=plan,
            license_packet=license_packet,
            source_batch_digest=source_batch,
            blockers=blockers,
        )
    else:
        _pending_validation(
            root_packet=root_packet,
            registry=registry,
            sources=sources,
            capability_state=capability_state,
            capability_bundle=capability_bundle,
            portfolio_state=portfolio_state,
            portfolio_bundle=portfolio_bundle,
            plan=plan,
            license_packet=license_packet,
            pending=pending,
            source_batch=source_batch,
            blockers=blockers,
        )

    cycle_index = (
        integer(pending.get("cycle_index"), 0)
        if pending is not None
        else integer(portfolio_state.get("cycle_index"), 0) + 1
    )
    packet_id = "kuuos-adapter-portfolio-" + sha(
        {"run": run_id, "source_batch": source_batch, "cycle": cycle_index}
    )[:18]
    normalized_wake = normalize_sources(sources) if not blockers else {}
    selection: dict[str, Any] = {}
    live_entry: dict[str, Any] = {}

    if not blockers and pending is not None:
        candidate = read_json(p["selection"])
        if (
            candidate.get("version") == SELECTION_VERSION
            and valid_digest(candidate, "portfolio_selection_digest")
            and candidate.get("portfolio_run_id") == run_id
            and candidate.get("source_batch_digest") == source_batch
            and candidate.get("portfolio_selection_digest")
            == pending.get("portfolio_selection_digest")
        ):
            selection = candidate
            live_entry = next(
                (
                    dict(mapping(item))
                    for item in as_list(registry.get("adapters"))
                    if mapping(item).get("federation_adapter_id")
                    == selection.get("live_adapter_id")
                ),
                {},
            )
        else:
            blockers.append("pending_portfolio_selection_invalid")
    elif not blockers:
        selection, live_entry = build_portfolio_selection(
            portfolio_run_id=run_id,
            capability_bundle=capability_bundle,
            portfolio_bundle=portfolio_bundle,
            registry=registry,
            source_packets=sources,
            normalized_wake=normalized_wake,
            exploration_weight=clamp(plan.get("exploration_weight")),
            max_exploration_bonus=clamp(plan.get("max_exploration_bonus")),
            curvature_penalty=clamp(plan.get("curvature_penalty")),
            resolved_evidence_weight=clamp(plan.get("resolved_evidence_weight")),
            max_portfolio_adjustment=clamp(plan.get("max_portfolio_adjustment")),
            blockers=blockers,
        )
        if not blockers:
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
                    previous_portfolio_state_digest=portfolio_state.get(
                        "portfolio_state_digest", ""
                    ),
                    previous_portfolio_bundle_digest=portfolio_bundle.get(
                        "portfolio_bundle_digest", ""
                    ),
                    selection=selection,
                    cycle_index=cycle_index,
                ),
            )

    child_result: dict[str, Any] = {}
    if not blockers:
        live_registry = derived_live_registry(registry, selection)
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
        child_plan, child_license = build_child_capability_packets(
            portfolio_plan=plan,
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
                "allowed_domain_actions": as_list(
                    context.get("allowed_domain_actions")
                ),
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
        if child.selected_federation_adapter_id != selection.get("live_adapter_id"):
            blockers.append("portfolio_live_adapter_child_mismatch")

    effect: dict[str, Any] = {}
    live_observed_utility = 0.0
    live_effect_digest = ""
    covariant_step_kind = ""
    if not blockers:
        calibration = read_json(p["capability_calibration"])
        effect = read_json(p["effect"])
        intervention_receipt = read_json(p["intervention_receipt"])
        if effect.get("version") != EFFECT_VERSION:
            blockers.append("portfolio_live_effect_version_invalid")
        elif effect.get("effect_receipt_digest") != effect_digest(effect):
            blockers.append("portfolio_live_effect_digest_invalid")
        live_effect_digest = str(effect.get("effect_receipt_digest", ""))
        if live_effect_digest != child_result.get("effect_receipt_digest"):
            blockers.append("portfolio_live_effect_child_mismatch")
        if calibration.get("effect_receipt_digest") != live_effect_digest:
            blockers.append("portfolio_live_calibration_effect_mismatch")
        live_observed_utility = clamp(calibration.get("observed_utility"), 0.0)
        covariant_step_kind = str(
            intervention_receipt.get("covariant_step_kind", "")
        )
        if not covariant_step_kind:
            blockers.append("portfolio_covariant_step_kind_missing")

    resolution: dict[str, Any] = {}
    projection: dict[str, Any] = {}
    updated_bundle = portfolio_bundle
    if not blockers:
        processed = {
            str(item)
            for item in as_list(
                portfolio_bundle.get("processed_live_effect_digests")
            )
        }
        if live_effect_digest in processed:
            resolution = read_json(p["resolution"])
            projection = read_json(p["projection"])
            updated_bundle = portfolio_bundle
            warnings.append("portfolio_update_recovered_without_duplicate_write")
        else:
            resolved_bundle, resolution, _ = resolve_previous_shadow(
                portfolio_run_id=run_id,
                bundle=portfolio_bundle,
                live_adapter_id=str(selection.get("live_adapter_id", "")),
                context_key=str(selection.get("context_key", "")),
                covariant_step_kind=covariant_step_kind,
                live_observed_utility=live_observed_utility,
                live_effect_receipt_digest=live_effect_digest,
                shadow_learning_rate=clamp(plan.get("shadow_learning_rate")),
                reliability_prior_mass=float(
                    plan.get("reliability_prior_mass", 2.0)
                ),
            )
            projection, projections = build_shadow_projections(
                portfolio_run_id=run_id,
                selection=selection,
                bundle=resolved_bundle,
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
            updated_bundle, replayed_update = commit_portfolio_update(
                portfolio_run_id=run_id,
                bundle=resolved_bundle,
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
            if replayed_update:
                warnings.append("portfolio_effect_already_processed")
            write_json(p["resolution"], resolution)
            write_json(p["projection"], projection)
            write_json(p["bundle"], updated_bundle)

    status = READY if not blockers else BLOCKED
    if status == READY:
        state_base = portfolio_state
        if pending is not None and portfolio_state.get("portfolio_run_id") == run_id:
            state_base = {
                "portfolio_state_digest": pending.get(
                    "previous_portfolio_state_digest", ""
                ),
                "total_live_cycles": max(
                    0, integer(portfolio_state.get("total_live_cycles"), 1) - 1
                ),
                "total_shadow_projections": max(
                    0,
                    integer(portfolio_state.get("total_shadow_projections"), 0)
                    - integer(projection.get("projection_count"), 0),
                ),
                "total_shadow_resolutions": max(
                    0,
                    integer(portfolio_state.get("total_shadow_resolutions"), 0)
                    - (1 if resolution.get("resolved") is True else 0),
                ),
            }
        state, row = build_state_and_record(
            previous_state=state_base,
            packet_id=packet_id,
            run_id=run_id,
            plan=plan,
            cycle_index=cycle_index,
            selection=selection,
            projection=projection,
            resolution=resolution,
            bundle=updated_bundle,
            child_result=child_result,
            live_observed_utility=live_observed_utility,
            live_effect_receipt_digest=live_effect_digest,
        )
        write_json(p["state"], state)
        append_jsonl(p["ledger"], row)

    receipt = build_receipt(
        status=status,
        packet_id=packet_id,
        run_id=run_id,
        cycle_index=cycle_index,
        selection=selection,
        projection=projection,
        resolution=resolution,
        bundle=updated_bundle,
        child_result=child_result,
        live_observed_utility=live_observed_utility,
        live_effect_receipt_digest=live_effect_digest,
        blockers=blockers,
        warnings=warnings,
    )
    if license_packet.get("receipt_write_allowed") is True:
        write_json(p["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(p["audit"], {**receipt, "audit_record_digest": sha(receipt)})

    return AdapterPortfolioShadowResult(
        version=VERSION,
        status=status,
        packet_id=packet_id,
        portfolio_run_id=run_id,
        cycle_index=cycle_index,
        runtime_root=str(root),
        context_key=str(selection.get("context_key", "")),
        live_adapter_id=str(selection.get("live_adapter_id", "")),
        live_adapter_profile_digest=str(
            selection.get("live_adapter_profile_digest", "")
        ),
        live_base_score=float(selection.get("live_base_score", 0.0)),
        live_portfolio_adjustment=float(
            selection.get("live_portfolio_adjustment", 0.0)
        ),
        live_adjusted_score=float(selection.get("live_adjusted_score", 0.0)),
        live_observed_utility=live_observed_utility,
        shadow_projection_count=integer(projection.get("projection_count"), 0),
        resolved_shadow_count=1 if resolution.get("resolved") is True else 0,
        pending_shadow_count=len(as_list(updated_bundle.get("pending_predictions"))),
        child_capability_status=str(child_result.get("status", "")),
        child_capability_run_id=str(child_result.get("capability_run_id", "")),
        live_effect_receipt_digest=live_effect_digest,
        portfolio_bundle_digest=str(
            updated_bundle.get("portfolio_bundle_digest", "")
        ),
        idempotent_replay=False,
        recovered_pending_run=recovered_pending,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        selection_path=str(p["selection"]),
        projection_path=str(p["projection"]),
        resolution_path=str(p["resolution"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=blockers,
        warnings=warnings,
    )
