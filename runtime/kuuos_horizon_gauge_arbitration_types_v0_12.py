#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
    append_jsonl,
    as_list,
    clamp,
    contains_graph_keys,
    integer,
    mapping,
    nonnegative,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    signed,
    without,
    write_json,
)

VERSION = "kuuos_horizon_gauge_arbitration_v0_12"
PLAN_VERSION = "kuuos_horizon_gauge_arbitration_plan_v0_12"
LICENSE_VERSION = "kuuos_horizon_gauge_arbitration_license_v0_12"
BUNDLE_VERSION = "kuuos_horizon_gauge_arbitration_bundle_v0_12"
SECTION_VERSION = "kuuos_horizon_gauge_arbitration_section_v0_12"
DECISION_VERSION = "kuuos_horizon_gauge_arbitration_decision_v0_12"
OUTCOME_VERSION = "kuuos_horizon_gauge_arbitration_outcome_v0_12"
STATE_VERSION = "kuuos_horizon_gauge_arbitration_state_v0_12"
LEDGER_VERSION = "kuuos_horizon_gauge_arbitration_ledger_record_v0_12"
READY = "KUUOS_HORIZON_GAUGE_ARBITRATION_V0_12_READY"
BLOCKED = "KUUOS_HORIZON_GAUGE_ARBITRATION_V0_12_BLOCKED"
REPLAYED = "KUUOS_HORIZON_GAUGE_ARBITRATION_V0_12_REPLAYED"

HORIZONS = ("short", "medium", "long")
MODES = ("experiment", "reobserve", "exploit")
OUTCOME_CLASSES = (
    "exploring",
    "progressing",
    "repairing",
    "stabilizing",
    "plural_conflict",
    "holding",
)

REQUIRED_BOUNDARY = {
    "one_v0_11_child_cycle_per_arbitration_run": True,
    "horizon_local_sections_preserved": True,
    "active_parallel_transport_enabled": True,
    "gauge_curvature_is_not_a_veto": True,
    "plurality_floor_preserved": True,
    "winner_take_all_collapse_forbidden": True,
    "commitment_outcome_is_effect_grounded": True,
    "v0_11_credit_authority_unchanged": True,
    "v0_10_regret_authority_unchanged": True,
    "v0_8_hard_gates_preserved": True,
    "one_live_adapter_per_descendant_cycle": True,
    "shadow_candidates_non_actuating": True,
    "counterfactual_estimate_not_outcome": True,
    "source_authority_unchanged": True,
    "adapter_authority_unchanged": True,
    "external_network_effect_not_inferred": True,
    "world_update_not_inferred": True,
    "memory_overwrite_not_inferred": True,
    "deterministic_replay_required": True,
    "non_markov_arbitration_holonomy_preserved": True,
    "graph_semantics_forbidden": True,
}


@dataclass(frozen=True)
class HorizonGaugeArbitrationResult:
    version: str
    status: str
    packet_id: str
    arbitration_run_id: str
    cycle_index: int
    runtime_root: str
    context_key: str
    arbitration_class: str
    commitment_outcome_class: str
    consensus_mode: str
    short_dominant_mode: str
    medium_dominant_mode: str
    long_dominant_mode: str
    short_medium_residual: float
    medium_long_residual: float
    short_long_residual: float
    arbitration_curvature: float
    transported_short_weight: float
    transported_medium_weight: float
    transported_long_weight: float
    child_policy_mode: str
    child_live_adapter_id: str
    child_live_domain_action: str
    commitment_progress_score: float
    recovery_cost: float
    terminal_section_ratio: float
    arbitration_bundle_digest: str
    child_horizon_bundle_digest: str
    child_horizon_outcome_digest: str
    child_effect_receipt_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    bundle_path: str
    decision_path: str
    outcome_path: str
    child_plan_path: str
    child_license_path: str
    receipt_path: str
    ledger_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    digest = str(value.get(field, ""))
    return bool(digest) and digest == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "arbitration_plan_digest"))


def bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "arbitration_bundle_digest"))


def section_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "arbitration_section_digest"))


def decision_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "arbitration_decision_digest"))


def outcome_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "arbitration_outcome_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "arbitration_state_digest"))
