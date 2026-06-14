#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

PLAN_VERSION = "indra_qi_process_tensor_world_assimilation_plan_v0_6"
REQUIRED_BOUNDARY = {
    "process_tensor_world_assimilation_not_truth": True,
    "explicit_world_mutation_license_required": True,
    "dynamic_world_state_layer_only": True,
    "source_cycle_state_not_authority": True,
    "debt_changes_world_state": True,
    "recoverability_changes_world_state": True,
    "effective_transport_not_base_connection_mutation": True,
    "effective_holonomy_not_base_holonomy_replacement": True,
    "operator_algebra_unchanged": True,
    "gauge_connection_identity_unchanged": True,
    "mandala_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "rollback_snapshot_required": True,
    "post_write_verification_required": True,
    "not_direct_execution_authority": True,
    "external_world_actuation_authority": False,
    "fail_closed_on_boundary_loss": True,
}
PROTECTED_CONSTITUTION_FIELDS = (
    "core_statement",
    "causal_world_model_bridge",
    "local_world_patches",
    "indra_connections",
    "qi_flow_channels",
    "holonomy_cycles",
    "ku_string_correspondences",
    "extended_m_brane_surfaces",
    "mandala_inclusion",
    "two_truths_boundary",
    "governance_boundary",
)
DYNAMIC_WORLD_FIELDS = (
    "local_patch_dynamic_states",
    "qi_flow_effective_states",
    "observation_debt_ledger",
    "recoverability_corridors",
    "effective_holonomy_states",
)


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def assimilation_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "assimilation_plan_digest"))


def protected_constitution_digest(state: Mapping[str, Any]) -> str:
    return sha({field: deepcopy(state.get(field)) for field in PROTECTED_CONSTITUTION_FIELDS})


def overlay_history_digest(state: Mapping[str, Any]) -> str:
    return sha(deepcopy(items(state.get("runtime_observation_overlays"))))


def dynamic_world_state_digest(state: Mapping[str, Any]) -> str:
    payload = {
        field: deepcopy(state.get(field))
        for field in DYNAMIC_WORLD_FIELDS
    }
    payload["process_tensor_world_state"] = deepcopy(state.get("process_tensor_world_state"))
    return sha(payload)


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("world_assimilation_plan_version_invalid")
    if str(plan.get("assimilation_plan_digest", "")) != assimilation_plan_digest(plan):
        blockers.append("world_assimilation_plan_digest_invalid")
    if not str(plan.get("assimilation_id", "")).strip():
        blockers.append("world_assimilation_id_missing")
    if plan.get("assimilation_mode") != "debt_recovery_transport_world_update":
        blockers.append("world_assimilation_mode_invalid")
    if plan.get("mutation_scope") != "process_tensor_dynamic_world_state_only":
        blockers.append("world_assimilation_mutation_scope_invalid")
    if plan.get("rollback_required") is not True:
        blockers.append("world_assimilation_rollback_required_not_true")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"world_assimilation_boundary_{field}_mismatch")
    policy = mapping(plan.get("assimilation_policy"))
    numeric_fields = (
        "world_memory_retention",
        "world_residue_retention",
        "world_nonmarkov_retention",
        "world_recoverability_retention",
        "world_debt_retention",
        "tension_debt_gain",
        "tension_residue_gain",
        "tension_recovery_loss_gain",
        "transport_resistance_gain",
        "holonomy_residue_gain",
        "seed_source_retention",
        "min_post_assimilation_seed_weight",
    )
    for field in numeric_fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"world_assimilation_policy_{field}_invalid")
    branches = policy.get("max_recoverability_branches")
    if isinstance(branches, bool) or not isinstance(branches, int) or branches <= 0:
        blockers.append("world_assimilation_policy_max_recoverability_branches_invalid")


def _retained(previous: float, current: float, retention: float) -> float:
    return clamp(retention * previous + (1.0 - retention) * current)


def previous_dynamic_map(state: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for field in ("local_patch_dynamic_states", "qi_flow_effective_states"):
        for raw in items(state.get(field)):
            value = mapping(raw)
            key = str(value.get("target_key", ""))
            if key:
                result[key] = value
    return result


def assimilate_channel(
    *,
    channel: Mapping[str, Any],
    previous: Mapping[str, Any],
    policy: Mapping[str, Any],
    assimilation_id: str,
    revision: int,
) -> dict[str, Any]:
    target = dict(mapping(channel.get("target")))
    target_key = str(channel.get("target_key", ""))
    is_flow = bool(str(target.get("flow_id", "")))

    memory = _retained(
        number(previous.get("memory_kernel_strength")),
        number(channel.get("memory_kernel_strength")),
        number(policy.get("world_memory_retention"), 0.70),
    )
    residue = _retained(
        number(previous.get("intervention_residue")),
        number(channel.get("intervention_residue")),
        number(policy.get("world_residue_retention"), 0.70),
    )
    nonmarkov = _retained(
        number(previous.get("nonmarkov_coupling")),
        number(channel.get("nonmarkov_coupling")),
        number(policy.get("world_nonmarkov_retention"), 0.70),
    )
    previous_recovery = number(previous.get("recoverability_reserve"), 1.0)
    recovery = _retained(
        previous_recovery,
        number(channel.get("recoverability_reserve")),
        number(policy.get("world_recoverability_retention"), 0.70),
    )
    debt = _retained(
        number(previous.get("observation_debt")),
        number(channel.get("observation_debt")),
        number(policy.get("world_debt_retention"), 0.75),
    )
    resonance = clamp(number(channel.get("relational_resonance")))

    tension = clamp(
        number(policy.get("tension_debt_gain"), 0.45) * debt
        + number(policy.get("tension_residue_gain"), 0.35) * residue
        + number(policy.get("tension_recovery_loss_gain"), 0.20) * (1.0 - recovery)
    )
    corridor_openness = clamp(
        0.45 * recovery + 0.25 * (1.0 - debt) + 0.15 * memory + 0.15 * resonance
    )
    max_branches = int(policy.get("max_recoverability_branches", 8) or 8)
    branch_capacity = max(0, min(max_branches, round(corridor_openness * max_branches)))
    corridor_status = (
        "open" if corridor_openness >= 0.67 else "constrained" if corridor_openness >= 0.34 else "critical"
    )

    common = {
        "target_key": target_key,
        "target": target,
        "assimilation_id": assimilation_id,
        "dynamic_revision": revision,
        "memory_kernel_strength": memory,
        "intervention_residue": residue,
        "nonmarkov_coupling": nonmarkov,
        "recoverability_reserve": recovery,
        "observation_debt": debt,
        "relational_resonance": resonance,
        "relational_tension": tension,
        "recoverability_corridor_openness": corridor_openness,
        "recoverability_branch_capacity": branch_capacity,
        "recoverability_corridor_status": corridor_status,
        "source_cycle_channel_digest": str(channel.get("channel_state_digest", "")),
        "previous_dynamic_state_digest": str(previous.get("dynamic_state_entry_digest", "GENESIS"))
        if previous
        else "GENESIS",
        "boundary": {
            "dynamic_world_state_not_truth": True,
            "debt_visible": True,
            "recoverability_visible": True,
            "memory_kernel_visible": True,
            "intervention_residue_visible": True,
            "base_world_structure_unchanged": True,
            "external_world_not_actuated": True,
        },
    }
    if is_flow:
        resistance = clamp(
            number(policy.get("transport_resistance_gain"), 0.65) * tension
            + (1.0 - number(policy.get("transport_resistance_gain"), 0.65)) * residue
        )
        common.update(
            {
                "state_kind": "qi_flow_effective_state",
                "effective_transport_resistance": resistance,
                "effective_transport_coefficient": clamp(1.0 - resistance),
                "effective_holonomy_residue_pressure": clamp(
                    number(policy.get("holonomy_residue_gain"), 0.60)
                    * (debt + residue)
                    * (1.0 - recovery)
                ),
                "qi_substance_claim": False,
            }
        )
    else:
        common.update(
            {
                "state_kind": "local_patch_dynamic_state",
                "effective_response_capacity": clamp(
                    recovery * (1.0 - debt) * (1.0 - 0.5 * residue)
                ),
                "observation_sensitivity": clamp(memory * (1.0 - debt)),
            }
        )
    common["dynamic_state_entry_digest"] = sha(common)
    return common


def debt_ledger_entry(
    *,
    dynamic_state: Mapping[str, Any],
    previous: Mapping[str, Any],
    cycle_id: str,
    cycle_digest: str,
) -> dict[str, Any]:
    previous_debt = number(previous.get("observation_debt"))
    current_debt = number(dynamic_state.get("observation_debt"))
    entry = {
        "entry_type": "observation_debt_transition",
        "target_key": str(dynamic_state.get("target_key", "")),
        "target": dict(mapping(dynamic_state.get("target"))),
        "cycle_id": cycle_id,
        "source_cycle_state_digest": cycle_digest,
        "previous_observation_debt": previous_debt,
        "current_observation_debt": current_debt,
        "observation_debt_delta": round(current_debt - previous_debt, 8),
        "source_dynamic_state_entry_digest": str(
            dynamic_state.get("dynamic_state_entry_digest", "")
        ),
        "boundary": {
            "debt_is_world_state": True,
            "debt_not_moral_blame": True,
            "debt_not_truth": True,
            "debt_transition_append_only": True,
        },
    }
    entry["debt_entry_digest"] = sha(entry)
    return entry


def corridor_entry(dynamic_state: Mapping[str, Any], cycle_digest: str) -> dict[str, Any]:
    entry = {
        "target_key": str(dynamic_state.get("target_key", "")),
        "target": dict(mapping(dynamic_state.get("target"))),
        "openness": dynamic_state.get("recoverability_corridor_openness"),
        "branch_capacity": dynamic_state.get("recoverability_branch_capacity"),
        "status": dynamic_state.get("recoverability_corridor_status"),
        "recoverability_reserve": dynamic_state.get("recoverability_reserve"),
        "observation_debt": dynamic_state.get("observation_debt"),
        "source_dynamic_state_entry_digest": str(
            dynamic_state.get("dynamic_state_entry_digest", "")
        ),
        "source_cycle_state_digest": cycle_digest,
        "boundary": {
            "corridor_is_repair_possibility": True,
            "corridor_not_execution_permission": True,
            "corridor_not_guaranteed_outcome": True,
        },
    }
    entry["corridor_digest"] = sha(entry)
    return entry


def build_effective_holonomy_states(
    *,
    world_state: Mapping[str, Any],
    flow_states: list[Mapping[str, Any]],
    cycle_digest: str,
) -> list[dict[str, Any]]:
    flow_connections = {
        str(mapping(raw).get("flow_id", "")): str(mapping(raw).get("connection_id", ""))
        for raw in items(world_state.get("qi_flow_channels"))
    }
    results: list[dict[str, Any]] = []
    for raw_cycle in items(world_state.get("holonomy_cycles")):
        base_cycle = mapping(raw_cycle)
        connection_ids = {str(value) for value in items(base_cycle.get("connection_ids"))}
        relevant = [
            state
            for state in flow_states
            if flow_connections.get(str(mapping(state.get("target")).get("flow_id", "")))
            in connection_ids
        ]
        pressures = [number(state.get("effective_holonomy_residue_pressure")) for state in relevant]
        debts = [number(state.get("observation_debt")) for state in relevant]
        recoveries = [number(state.get("recoverability_reserve")) for state in relevant]
        pressure = round(sum(pressures) / len(pressures), 8) if pressures else 0.0
        debt = round(sum(debts) / len(debts), 8) if debts else 0.0
        recovery = round(sum(recoveries) / len(recoveries), 8) if recoveries else 1.0
        status = "stable" if pressure < 0.34 else "loaded" if pressure < 0.67 else "critical"
        state = {
            "cycle_id": str(base_cycle.get("cycle_id", "")),
            "base_holonomy_digest": str(base_cycle.get("holonomy_digest", "")),
            "base_transport_residue_digest": str(
                base_cycle.get("transport_residue_digest", "")
            ),
            "connection_ids": sorted(connection_ids),
            "effective_residue_pressure": pressure,
            "observation_debt_load": debt,
            "recoverability_modulation": recovery,
            "effective_status": status,
            "source_cycle_state_digest": cycle_digest,
            "boundary": {
                "effective_holonomy_not_base_holonomy_replacement": True,
                "base_holonomy_preserved": True,
                "historical_residue_visible": True,
            },
        }
        state["effective_holonomy_state_digest"] = sha(state)
        results.append(state)
    return results


def adjusted_seed_weight(
    *,
    source_weight: float,
    dynamic_state: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> float:
    capacity = number(
        dynamic_state.get(
            "effective_transport_coefficient",
            dynamic_state.get("effective_response_capacity", 0.0),
        )
    )
    endogenous = clamp(
        0.25 * number(dynamic_state.get("memory_kernel_strength"))
        + 0.25 * number(dynamic_state.get("recoverability_reserve"))
        + 0.20 * (1.0 - number(dynamic_state.get("observation_debt")))
        + 0.20 * capacity
        + 0.10 * number(dynamic_state.get("relational_resonance"))
        - 0.10 * number(dynamic_state.get("intervention_residue"))
    )
    retention = number(policy.get("seed_source_retention"), 0.60)
    return clamp(retention * source_weight + (1.0 - retention) * endogenous)
