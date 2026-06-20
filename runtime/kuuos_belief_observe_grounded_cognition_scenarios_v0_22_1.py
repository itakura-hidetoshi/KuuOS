from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from runtime.kuuos_belief_observe_grounded_cognition_bridge_v0_22_1 import (
    adapt_observe_state_to_epistemic_observation,
    build_belief_grounded_plan_bundle,
    build_belief_planning_basis_receipt,
    build_observe_adapter_receipt,
    build_observe_grounded_verification_bundle,
    build_observe_to_belief_trace_proposal,
)
from runtime.kuuos_belief_os_context_transport_v0_2 import (
    build_atlas_transition,
    build_transport_packet,
    transport_belief_sections,
)
from runtime.kuuos_belief_os_kernel_v0_1 import (
    apply_belief_event,
    build_belief_event,
    build_initial_belief_state,
)
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_observe_os_fixture_v0_1 import prepared_assessed_state, source_act_state
from runtime.kuuos_observe_os_types_v0_1 import state_digest as observe_state_digest
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _build_plan,
    _fixture,
    _ready_belief_state,
)
from runtime.v01_observe_os_effect_grounded_observation import _finish
from runtime.v02_belief_os_context_gauge_transport import _committed_belief


def _belief_transport(contract: dict[str, Any], chart_id: str) -> dict[str, Any]:
    lineage = contract["lineage_id"]
    source_a = _committed_belief(
        belief_id="grounded-belief-a",
        lineage_id=lineage,
        context_id="context-a",
        lower=0.66,
        upper=0.78,
        evidence_label="grounded-evidence-a",
        counterevidence_label="grounded-counter-a",
        qi_label="grounded-a",
        tick_base=100,
    )
    source_b = _committed_belief(
        belief_id="grounded-belief-b",
        lineage_id=lineage,
        context_id="context-b",
        lower=0.61,
        upper=0.76,
        evidence_label="grounded-evidence-b",
        counterevidence_label="grounded-counter-b",
        qi_label="grounded-b",
        tick_base=200,
    )
    transitions = [
        build_atlas_transition(
            source_context_id="context-a",
            target_context_id=chart_id,
            declared_path=["context-a", chart_id],
            overlap=0.98,
            curvature=0.01,
            cocycle_defect=0.01,
            holonomy_residual=0.01,
            qi_history_compatibility=0.99,
            atlas_receipt_digest=sha("grounded-atlas-a"),
        ),
        build_atlas_transition(
            source_context_id="context-b",
            target_context_id=chart_id,
            declared_path=["context-b", "context-bridge", chart_id],
            overlap=0.97,
            curvature=0.01,
            cocycle_defect=0.01,
            holonomy_residual=0.01,
            qi_history_compatibility=0.99,
            atlas_receipt_digest=sha("grounded-atlas-b"),
        ),
    ]
    packet = build_transport_packet(
        packet_id="grounded-belief-transport",
        lineage_id=lineage,
        target_context_id=chart_id,
        target_context_signature_digest=sha(chart_id),
        atlas_bundle_digest=sha("grounded-atlas-bundle"),
        source_belief_states=[source_a, source_b],
        transitions=transitions,
        candidate_max_width=0.60,
        observe_max_width=0.85,
        candidate_max_conflict=0.20,
        created_at_ms=10_000,
    )
    receipt = transport_belief_sections(packet)
    assert receipt["route"] == "CANDIDATE"
    return receipt


def _matched_observe_state(
    root: Path,
    contract: dict[str, Any],
    observe_id: str,
    tick: int,
) -> dict[str, Any]:
    act_state = source_act_state(root / (observe_id + "-act"))
    store, assessed = prepared_assessed_state(
        root=root / observe_id,
        observe_id=observe_id,
        act_state=act_state,
    )
    observed, _ = _finish(store=store, state=assessed, verdict="MATCHED", tick=tick)
    observed["lineage_id"] = contract["lineage_id"]
    observed["mission_contract_digest"] = contract["mission_contract_digest"]
    observed["observe_state_digest"] = ""
    observed["observe_state_digest"] = observe_state_digest(observed)
    return observed


def _contextualized_belief(contract: dict[str, Any]) -> dict[str, Any]:
    state = build_initial_belief_state(
        belief_id="observe-feedback-belief",
        lineage_id=contract["lineage_id"],
        claim="The observed effect is conditionally compatible with the current strategy.",
        claim_digest=sha("observe-feedback-claim"),
        hypothesis_space_digest=sha(["compatible", "incompatible", "unknown"]),
        source_memory_digest=sha("observe-feedback-memory"),
        now_ms=50_000,
    )
    event = build_belief_event(
        state=state,
        target_phase="contextualize",
        artifact_digest=sha("observe-feedback-context"),
        payload={
            "context": {
                "context_id": "github-main",
                "observer_id": "observeos-adapter",
                "observer_role": "independent-observer",
                "temporal_scope": "current-cycle",
                "scale": "repository-local",
                "task_scope": "effect-grounded-feedback",
                "world_model_id": "kuuos-open-horizon",
            }
        },
        now_ms=50_001,
    )
    result = apply_belief_event(state, event)
    assert result["status"] == "APPLIED"
    return result["state"]


def run_belief_observe_grounded_cognition_scenarios() -> dict[str, Any]:
    contract, mission_state, goal, portfolio = _fixture()
    epistemic = _ready_belief_state(contract, mission_state)
    plan = _build_plan(contract, mission_state, epistemic, goal, portfolio)
    transport = _belief_transport(contract, epistemic["chart_id"])
    basis = build_belief_planning_basis_receipt(
        contract=contract,
        mission_state=mission_state,
        epistemic_belief_state=epistemic,
        goal=goal,
        goal_portfolio=portfolio,
        belief_transport_receipt=transport,
        created_at_ms=10_100,
    )
    plan_bundle = build_belief_grounded_plan_bundle(
        contract=contract,
        mission_state=mission_state,
        epistemic_belief_state=epistemic,
        goal=goal,
        goal_portfolio=portfolio,
        semantic_plan=plan,
        belief_basis_receipt=basis,
    )

    with tempfile.TemporaryDirectory(prefix="kuuos-belief-observe-v0221-") as temporary:
        root = Path(temporary)
        observed_a = _matched_observe_state(root, contract, "grounded-observe-a", 10)
        observed_b = _matched_observe_state(root, contract, "grounded-observe-b", 20)
        verification_bundle = build_observe_grounded_verification_bundle(
            contract=contract,
            mission_state=mission_state,
            source_epistemic_belief_state=epistemic,
            goal=goal,
            goal_portfolio=portfolio,
            semantic_plan=plan,
            verifier_id="verifyos-independent-v0221",
            criterion_bindings=[
                {
                    "criterion": contract["success_criteria"][0],
                    "observe_state": observed_a,
                    "claim_id": "observe-plan-output",
                    "proposition": "ObserveOS confirms the expected plan output.",
                },
                {
                    "criterion": contract["success_criteria"][1],
                    "observe_state": observed_b,
                    "claim_id": "observe-goal-confirmation",
                    "proposition": "ObserveOS confirms the bounded goal outcome.",
                },
            ],
            execution_receipt_digests=[sha("grounded-execution-receipt")],
            observed_at_ms=101_000,
            valid_until_ms=200_000,
        )
        assert verification_bundle["verification_status"] == "verified_success"

        adapted = adapt_observe_state_to_epistemic_observation(
            contract=contract,
            mission_state=mission_state,
            observe_state=observed_a,
            chart_id=epistemic["chart_id"],
            claim_id="observe-feedback",
            proposition="ObserveOS effect evidence supports the current strategy.",
            planner_id=plan["planner_id"],
            valid_until_ms=200_000,
        )
        adapter = build_observe_adapter_receipt(
            observe_state=observed_a,
            adapted_observation=adapted,
            planner_id=plan["planner_id"],
        )
        trace = build_observe_to_belief_trace_proposal(
            belief_state=_contextualized_belief(contract),
            adapted_observation=adapted,
            observe_adapter_receipt=adapter,
            now_ms=102_000,
        )
        assert trace["automatic_apply"] is False
        assert trace["belief_event"]["target_phase"] == "trace"

        try:
            build_belief_planning_basis_receipt(
                contract=contract,
                mission_state=mission_state,
                epistemic_belief_state=epistemic,
                goal=goal,
                goal_portfolio=portfolio,
                belief_transport_receipt={**transport, "route": "OBSERVE"},
                created_at_ms=10_200,
            )
            raise AssertionError("non-candidate belief transport accepted")
        except ValueError as exc:
            assert "belief_transport_candidate_required" in str(exc)

        return {
            "status": "KUUOS_BELIEF_OBSERVE_GROUNDED_COGNITION_V0_22_1_OK",
            "belief_basis_route": basis["route"],
            "plan_bundle_route": plan_bundle["route"],
            "verification_status": verification_bundle["verification_status"],
            "effect_grounded": verification_bundle["effect_grounded"],
            "counterevidence_preserved": len(basis["counterevidence_digests"]),
            "trace_is_proposal_only": trace["automatic_apply"] is False,
            "execution_authority_granted": False,
        }


__all__ = ["run_belief_observe_grounded_cognition_scenarios"]
