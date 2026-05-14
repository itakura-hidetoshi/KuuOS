#!/usr/bin/env python3
"""Minimal Mass Gap -> BeliefOS / DecisionOS HOLD adapter.

This stdlib-only adapter receives a TwoTruthsEngineMassGapDecision-like input
and produces conservative BeliefOS / DecisionOS guard outputs.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json


@dataclass(frozen=True)
class TwoTruthsEngineMassGapDecision:
    canonical_repo: str = "itakura-hidetoshi/4d-mass-gap"
    bridge_authority: str = "reference_only"
    public_theorem_boundary: str = "held"
    paramartha_non_reification_guard: str = "active"
    samvrti_excitation_admissibility: str = "checkpoint_conditioned"
    two_truths_non_collapse_barrier: str = "active"
    final_theorem_authority: bool = False
    action_authority: bool = False


@dataclass(frozen=True)
class MassGapBeliefDecisionHoldOutput:
    belief_guard: str
    decision_guard: str
    allowed_effects: tuple[str, ...]
    forbidden_effects: tuple[str, ...]
    status: str


def evaluate_hold_bridge(
    decision: TwoTruthsEngineMassGapDecision,
) -> MassGapBeliefDecisionHoldOutput:
    hold = any(
        [
            decision.canonical_repo != "itakura-hidetoshi/4d-mass-gap",
            decision.bridge_authority != "reference_only",
            decision.public_theorem_boundary != "held",
            decision.final_theorem_authority is not False,
            decision.action_authority is not False,
            decision.paramartha_non_reification_guard != "active",
            decision.samvrti_excitation_admissibility == "unconditional_action",
            decision.two_truths_non_collapse_barrier != "active",
        ]
    )

    forbidden = (
        "set_belief_truth",
        "set_world_fact",
        "release_decision",
        "perform_action",
        "open_final_theorem_boundary",
    )

    if hold:
        return MassGapBeliefDecisionHoldOutput(
            belief_guard="hold",
            decision_guard="hold",
            allowed_effects=("request_reobserve_if_boundary_unstable", "handover_if_public_theorem_boundary_is_requested"),
            forbidden_effects=forbidden,
            status="mass_gap_belief_decision_hold",
        )

    return MassGapBeliefDecisionHoldOutput(
        belief_guard="active",
        decision_guard="active",
        allowed_effects=(
            "prevent_two_truths_collapse",
            "request_reobserve_if_boundary_unstable",
            "hold_if_authority_expands",
            "handover_if_public_theorem_boundary_is_requested",
        ),
        forbidden_effects=forbidden,
        status="mass_gap_belief_decision_guard_active",
    )


def main() -> int:
    decision = TwoTruthsEngineMassGapDecision()
    output = evaluate_hold_bridge(decision)
    print(json.dumps({"input": asdict(decision), "output": asdict(output)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
