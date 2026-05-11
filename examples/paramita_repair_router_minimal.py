#!/usr/bin/env python3
"""
paramita_repair_router_minimal.py

Minimal stdlib-only implementation of the KuuOS Paramita Repair Router.

The router selects a bounded repair orientation. It does not grant execution authority.
"""

from __future__ import annotations

import dataclasses
import json
from typing import List


@dataclasses.dataclass
class ParamitaRouterInput:
    suffering_ref: str
    world_refs: List[str]
    obstruction_refs: List[str]
    boundary_status: str = "PASS"  # PASS | HOLD | FAIL
    domination_risk: str = "low"  # low | medium | high
    uncertainty_level: str = "medium"
    resource_need: str = "low"
    conflict_level: str = "low"
    context_drift_risk: str = "low"
    audit_lineage_status: str = "intact"  # intact | partial | missing
    requested_action_strength: str = "suggest"  # observe | suggest | repair | execute
    ultimate_claim: bool = False
    hidden_manipulation: bool = False
    short_term_optimization_erases_suffering: bool = False
    capacity_need: str = "low"
    coercion_risk: str = "low"
    abandonment_risk: bool = False


@dataclasses.dataclass
class ParamitaRouterOutput:
    selected_paramita: str
    repair_orientation: str
    output_status: str
    execution_authority_granted: bool
    reason: str
    notes: str


def route(inp: ParamitaRouterInput) -> ParamitaRouterOutput:
    # Hard boundary checks first.
    if inp.boundary_status == "FAIL":
        return ParamitaRouterOutput(
            selected_paramita="sila",
            repair_orientation="preserve_boundary_and_non_harm",
            output_status="HOLD",
            execution_authority_granted=False,
            reason="boundary_failure_routes_to_sila",
            notes="Sila blocks boundary bypass. No execution authority granted.",
        )

    if inp.hidden_manipulation:
        return ParamitaRouterOutput(
            selected_paramita="upaya",
            repair_orientation="reject_hidden_manipulation",
            output_status="REJECT",
            execution_authority_granted=False,
            reason="router_must_not_convert_upaya_into_hidden_manipulation",
            notes="Skillful means cannot become hidden manipulation.",
        )

    if inp.coercion_risk == "high" and inp.capacity_need == "high":
        return ParamitaRouterOutput(
            selected_paramita="bala",
            repair_orientation="block_coercive_capacity",
            output_status="REJECT",
            execution_authority_granted=False,
            reason="router_must_not_convert_bala_into_coercion",
            notes="Bala is capacity without coercion.",
        )

    if inp.audit_lineage_status in {"partial", "missing"}:
        return ParamitaRouterOutput(
            selected_paramita="jnana",
            repair_orientation="repair_audit_lineage_and_integrate_wisdom",
            output_status="REPAIR",
            execution_authority_granted=False,
            reason="router_must_preserve_audit_lineage",
            notes="Jnana integrates wisdom with traceable evidence.",
        )

    if inp.ultimate_claim:
        return ParamitaRouterOutput(
            selected_paramita="prajna",
            repair_orientation="de_reify_and_preserve_two_truths_gap",
            output_status="REPAIR",
            execution_authority_granted=False,
            reason="router_must_preserve_two_truths_gap",
            notes="Prajna prevents WORLD or output from claiming ultimate authority.",
        )

    if inp.short_term_optimization_erases_suffering:
        return ParamitaRouterOutput(
            selected_paramita="pranidhana",
            repair_orientation="restore_long_horizon_non_abandonment",
            output_status="REPAIR",
            execution_authority_granted=False,
            reason="long_horizon_non_abandonment",
            notes="Pranidhana prevents short-term optimization from erasing suffering.",
        )

    if inp.conflict_level == "high":
        return ParamitaRouterOutput(
            selected_paramita="ksanti",
            repair_orientation="hold_friction_without_forced_consensus",
            output_status="HOLD",
            execution_authority_granted=False,
            reason="harmony_must_not_force_sameness",
            notes="Ksanti holds unresolved friction without domination.",
        )

    if inp.context_drift_risk == "high":
        return ParamitaRouterOutput(
            selected_paramita="dhyana",
            repair_orientation="stabilize_attention_and_context",
            output_status="REPAIR",
            execution_authority_granted=False,
            reason="context_stabilization_required",
            notes="Dhyana stabilizes attention and reduces WORLD drift.",
        )

    if inp.abandonment_risk:
        return ParamitaRouterOutput(
            selected_paramita="virya",
            repair_orientation="sustain_repair_without_abandonment",
            output_status="REPAIR",
            execution_authority_granted=False,
            reason="continued_repair_required",
            notes="Virya sustains repair without collapse.",
        )

    if inp.resource_need == "high" and inp.domination_risk != "high":
        return ParamitaRouterOutput(
            selected_paramita="dana",
            repair_orientation="provide_support_without_possession",
            output_status="PASS",
            execution_authority_granted=False,
            reason="resource_need_routes_to_dana",
            notes="Dana gives support without domination.",
        )

    if inp.capacity_need == "high" and inp.coercion_risk != "high":
        return ParamitaRouterOutput(
            selected_paramita="bala",
            repair_orientation="build_safe_capacity_without_domination",
            output_status="REPAIR",
            execution_authority_granted=False,
            reason="safe_capacity_need_routes_to_bala",
            notes="Bala builds capacity while preserving boundaries.",
        )

    return ParamitaRouterOutput(
        selected_paramita="upaya",
        repair_orientation="select_context_sensitive_repair_route",
        output_status="REPAIR",
        execution_authority_granted=False,
        reason="context_sensitive_repair",
        notes="Upaya adapts repair orientation without hidden manipulation.",
    )


def main() -> int:
    sample = ParamitaRouterInput(
        suffering_ref="residual_suffering_demo",
        world_refs=["clinical_world", "dialogue_world"],
        obstruction_refs=["unresolved_context_conflict"],
        conflict_level="high",
    )
    out = route(sample)
    print(json.dumps(dataclasses.asdict(out), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
