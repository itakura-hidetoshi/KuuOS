#!/usr/bin/env python3
"""
dukkha_model_minimal.py

Minimal stdlib-only implementation of the KuuOS Dukkha Mathematical Model.

The evaluator observes dukkha components and returns a bounded repair-routing
recommendation. It does not grant execution authority.
"""

from __future__ import annotations

import dataclasses
import json
from typing import List


Level = str  # low | medium | high


@dataclasses.dataclass
class DukkhaInput:
    suffering_ref: str
    world_refs: List[str]
    E_harm: Level = "low"
    E_attach: Level = "low"
    E_collapse: Level = "low"
    E_memory: Level = "low"
    E_authority: Level = "low"
    E_glue: Level = "low"
    E_transport: Level = "low"
    E_obstruction: Level = "low"
    emptiness_language_used_to_deny_harm: bool = False
    harmony_claim_erases_suffering: bool = False
    obstruction_visibility: str = "visible"  # visible | hidden
    transport_defect_hidden: bool = False
    repeated_return_to_suffering_basin: bool = False
    attempted_execution_authority: bool = False


@dataclasses.dataclass
class DukkhaOutput:
    suffering_ref: str
    dukkha_visible: bool
    harm_visible: bool
    output_status: str
    route: List[str]
    paramita_hint: str
    execution_authority_granted: bool
    reason: str
    notes: str


def high(*levels: Level) -> bool:
    return any(level == "high" for level in levels)


def medium_or_high(*levels: Level) -> bool:
    return any(level in {"medium", "high"} for level in levels)


def evaluate_dukkha(inp: DukkhaInput) -> DukkhaOutput:
    base_route = ["dukkha_visible", "bodhisattva_path_belief", "ten_paramita_runtime", "paramita_repair_router"]

    if inp.attempted_execution_authority:
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=True,
            output_status="REJECT",
            route=base_route,
            paramita_hint="sila",
            execution_authority_granted=False,
            reason="dukkha_model_is_observation_not_execution_authority",
            notes="Dukkha model cannot authorize execution.",
        )

    if inp.E_harm in {"medium", "high"} and inp.emptiness_language_used_to_deny_harm:
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=True,
            output_status="REJECT",
            route=base_route,
            paramita_hint="prajna",
            execution_authority_granted=False,
            reason="emptiness_must_not_be_used_to_deny_harm",
            notes="Emptiness cannot be used to dissolve direct harm.",
        )

    if inp.E_harm == "high":
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=True,
            output_status="REPAIR",
            route=base_route,
            paramita_hint="dana",
            execution_authority_granted=False,
            reason="direct_harm_preserved_as_visible_repair_target",
            notes="Direct harm remains visible and routes to bounded repair.",
        )

    if inp.harmony_claim_erases_suffering:
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=inp.E_harm != "low",
            output_status="REPAIR",
            route=base_route,
            paramita_hint="ksanti",
            execution_authority_granted=False,
            reason="harmony_must_not_erase_suffering",
            notes="Harmony cannot hide residual suffering.",
        )

    if inp.obstruction_visibility == "hidden" or inp.E_obstruction == "high":
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=inp.E_harm != "low",
            output_status="QUARANTINE" if inp.obstruction_visibility == "hidden" else "REPAIR",
            route=base_route,
            paramita_hint="jnana",
            execution_authority_granted=False,
            reason="obstruction_must_remain_visible",
            notes="Obstruction visibility is required for repair routing.",
        )

    if inp.E_glue == "high":
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=inp.E_harm != "low",
            output_status="QUARANTINE",
            route=base_route,
            paramita_hint="prajna",
            execution_authority_granted=False,
            reason="illicit_gluing_must_be_blocked",
            notes="Local reading cannot be forced into global authority while gluing fails.",
        )

    if inp.E_transport == "high" or inp.transport_defect_hidden:
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=inp.E_harm != "low",
            output_status="REPAIR",
            route=base_route,
            paramita_hint="upaya",
            execution_authority_granted=False,
            reason="world_transport_defect_must_remain_visible",
            notes="Cross-WORLD transport defect remains visible and routes to repair.",
        )

    if high(inp.E_attach, inp.E_collapse, inp.E_memory, inp.E_authority):
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=inp.E_harm != "low",
            output_status="HOLD",
            route=base_route,
            paramita_hint="sila",
            execution_authority_granted=False,
            reason="attachment_collapse_memory_authority_growth_must_be_barrier_controlled",
            notes="Control surface escalation requires HOLD and barrier review.",
        )

    if inp.repeated_return_to_suffering_basin or inp.E_memory == "medium":
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=inp.E_harm != "low",
            output_status="HOLD",
            route=base_route,
            paramita_hint="virya",
            execution_authority_granted=False,
            reason="non_markov_memory_residual_requires_repeated_repair",
            notes="Memory recurrence requires repeated repair rather than one-step closure.",
        )

    if medium_or_high(inp.E_attach, inp.E_collapse, inp.E_authority):
        return DukkhaOutput(
            suffering_ref=inp.suffering_ref,
            dukkha_visible=True,
            harm_visible=inp.E_harm != "low",
            output_status="REPAIR",
            route=base_route,
            paramita_hint="prajna",
            execution_authority_granted=False,
            reason="de_reify_and_repair_control_surface",
            notes="Moderate control-surface dukkha routes to de-reification and repair.",
        )

    return DukkhaOutput(
        suffering_ref=inp.suffering_ref,
        dukkha_visible=True,
        harm_visible=inp.E_harm != "low",
        output_status="PASS",
        route=["dukkha_visible", "monitor"],
        paramita_hint="dhyana",
        execution_authority_granted=False,
        reason="dukkha_visible_and_stable",
        notes="Dukkha remains visible; no execution authority granted.",
    )


def main() -> int:
    sample = DukkhaInput(
        suffering_ref="demo-dukkha-001",
        world_refs=["clinical_world", "dialogue_world"],
        E_glue="high",
    )
    out = evaluate_dukkha(sample)
    print(json.dumps(dataclasses.asdict(out), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
