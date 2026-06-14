#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import (
    REQUIRED_BOUNDARY,
    cycle_plan_digest,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import read_json, records
from scripts.qi_parent_cycle_reentry_v0_11_test_support import (
    build_plan as build_v0_11_plan,
    prepare_v0_10_cycle,
    run_loop,
)


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def prepare_source(root: pathlib.Path, suffix: str) -> dict[str, Any]:
    world, handoff, record, ledger, cycle, seed = prepare_v0_10_cycle(
        root, f"v0-12-source-{suffix}"
    )
    plan = build_v0_11_plan(
        world=world,
        handoff=handoff,
        bridge_record=record,
        bridge_ledger=ledger,
        cycle=cycle,
        seed=seed,
        suffix=f"v0-12-source-{suffix}",
    )
    result = run_loop(root, plan)
    assert result["status"] == "INDRA_QI_PARENT_CYCLE_ASSIMILATION_REENTRY_V0_11_READY", result
    reentry = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
    child = pathlib.Path(reentry["child_runtime_root"])
    return {
        "world": read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json"),
        "handoff": read_json(root / "indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json"),
        "record": read_json(root / "indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json"),
        "ledger": latest(root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl"),
        "reentry": reentry,
        "child": child,
        "causal": read_json(child / "kuuos_causal_world_model_state_v14_0.json"),
    }


def gate_policy() -> dict[str, Any]:
    return {
        "debt_risk_weight": 0.35,
        "residue_risk_weight": 0.25,
        "tension_risk_weight": 0.20,
        "recovery_loss_risk_weight": 0.20,
        "observe_only_risk_threshold": 1.0,
        "counterfactual_first_risk_threshold": 1.0,
        "minimum_intervention_recoverability": 0.0,
        "maximum_intervention_debt": 1.0,
        "minimum_intervention_corridor_openness": 0.0,
        "maximum_intervention_delta": 0.2,
        "observation_priority_debt_weight": 0.45,
        "observation_priority_uncertainty_weight": 0.35,
        "observation_priority_recovery_loss_weight": 0.20,
        "max_observation_requests": 8,
        "max_counterfactual_candidates": 8,
        "max_intervention_candidates": 8,
    }


def build_plan(
    *,
    root: pathlib.Path,
    source: dict[str, Any],
    runner_id: str,
    generation: int,
    maximum: int,
    suffix: str,
    selected_action_kind: str = "bounded_intervention_candidate",
    convergence_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state = read_json(root / "indra_qi_bounded_cycle_state_v0_12.json")
    handoff = source["handoff"]
    plan = {
        "version": "indra_qi_bounded_generational_cycle_plan_v0_12",
        "runner_id": runner_id,
        "generation_run_id": f"{runner_id}-generation-{generation}-{suffix}",
        "generation_index": generation,
        "max_generations": maximum,
        "source_v0_11_loop_id": handoff["loop_id"],
        "source_v0_11_handoff_packet_digest": handoff["loop_handoff_packet_digest"],
        "source_v0_11_record_digest": source["record"]["loop_record_digest"],
        "source_v0_11_ledger_record_digest": source["ledger"]["record_digest"],
        "expected_previous_runner_state_digest": state.get("runner_state_digest", "GENESIS") if state else "GENESIS",
        "selected_action_kind": selected_action_kind,
        "action_envelope_id": f"action-envelope-g{generation}-{suffix}",
        "execution_id": f"approved-execution-g{generation}-{suffix}",
        "action_transaction_id": f"action-tx-g{generation}-{suffix}",
        "undo_transaction_id": f"undo-tx-g{generation}-{suffix}",
        "feedback_id": f"feedback-g{generation}-{suffix}",
        "evidence_id": f"evidence-g{generation}-{suffix}",
        "approval_id": f"approval-g{generation}-{suffix}",
        "parent_bridge_id": f"parent-bridge-g{generation}-{suffix}",
        "activation_id": f"activation-g{generation}-{suffix}",
        "process_tensor_cycle_id": f"process-cycle-g{generation}-{suffix}",
        "assimilation_id": f"assimilation-g{generation}-{suffix}",
        "reentry_id": f"reentry-g{generation}-{suffix}",
        "projection_id": f"projection-g{generation}-{suffix}",
        "causal_world_id": f"causal-world-g{generation}-{suffix}",
        "causal_transaction_id": f"causal-init-g{generation}-{suffix}",
        "derived_response_patch_id": "world-b",
        "derived_response_observable_id": f"world-b-adaptive-g{generation}-{suffix}",
        "cycle_mode": "one_compensated_generation",
        "gate_policy": gate_policy(),
        "feedback_policy": {
            "event_kind_base_weight": {"observe": 0.9, "intervene": 0.75, "counterfactual": 0.45, "undo": 0.65},
            "uncertainty_penalty": 0.5,
            "minimum_candidate_weight": 0.1,
            "maximum_candidate_weight": 0.95,
        },
        "process_tensor_policy": {
            "min_history_depth": 3,
            "min_transition_continuity_score": 0.75,
            "min_memory_continuity_score": 0.75,
            "min_nonmarkov_link_density": 0.5,
            "min_recoverability_branching_capacity": 0.75,
            "max_observation_debt_pressure": 0.1,
            "min_candidate_weight": 0.5,
            "require_process_tensor_visible": True,
            "require_transition_continuity_visible": True,
            "require_memory_continuity_visible": True,
            "require_nonmarkov_memory_visible": True,
            "require_recoverability_witness": True,
        },
        "evolution_policy": {
            "memory_retention": 0.75,
            "intervention_residue_retention": 0.70,
            "nonmarkov_retention": 0.75,
            "recoverability_retention": 0.70,
            "observation_debt_retention": 0.80,
            "min_next_cycle_prior_weight": 0.50,
            "max_next_cycle_observation_debt": 0.20,
            "min_next_cycle_recoverability": 0.25,
            "max_channels": 16,
        },
        "assimilation_policy": {
            "world_memory_retention": 0.70,
            "world_residue_retention": 0.70,
            "world_nonmarkov_retention": 0.70,
            "world_recoverability_retention": 0.70,
            "world_debt_retention": 0.75,
            "tension_debt_gain": 0.45,
            "tension_residue_gain": 0.35,
            "tension_recovery_loss_gain": 0.20,
            "transport_resistance_gain": 0.65,
            "holonomy_residue_gain": 0.60,
            "seed_source_retention": 0.60,
            "min_post_assimilation_seed_weight": 0.35,
            "max_recoverability_branches": 8,
        },
        "projection_policy": {
            "minimum_seed_count": 2,
            "max_projection_variables": 16,
            "debt_uncertainty_gain": 0.65,
            "residue_uncertainty_gain": 0.35,
            "minimum_uncertainty": 0.01,
            "maximum_uncertainty": 0.95,
            "mechanism_weight_floor": 0.10,
            "mechanism_weight_ceiling": 0.95,
            "mechanism_noise_debt_gain": 0.50,
            "mechanism_bias": 0.05,
        },
        "convergence_policy": convergence_policy or {
            "maximum_observation_debt": 0.0,
            "minimum_recoverability_reserve": 1.0,
            "maximum_intervention_residue": 0.0,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    plan["cycle_plan_digest"] = cycle_plan_digest(plan)
    return plan
