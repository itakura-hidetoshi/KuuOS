from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_observation_belief_state_kernel_v0_21 import apply_observation
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    build_plan_invalidation_receipt,
    build_semantic_plan,
    build_verification_receipt,
    validate_semantic_plan_static,
)
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _build_plan,
    _fixture,
    _observation,
    _plan_parts,
    _ready_belief_state,
    run_semantic_planner_verifier_scenarios,
)
from runtime.kuuos_semantic_planner_verifier_store_v0_22 import (
    initialize_planner_verifier_store,
    persist_plan,
    recover_planner_verifier_store,
)


class SemanticPlannerVerifierV022Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_semantic_planner_verifier_scenarios()
        self.assertEqual("KUUOS_SEMANTIC_PLANNER_VERIFIER_V0_22_OK", result["status"])
        self.assertTrue(result["verified_success"])
        self.assertTrue(result["execution_only_inconclusive"])
        self.assertTrue(result["contradiction_detected"])
        self.assertTrue(result["plan_invalidated"])
        self.assertTrue(result["replan_ready"])
        self.assertFalse(result["effect_authority_granted"])

    def test_unknown_claim_blocks_plan_without_authority(self) -> None:
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        unknown = _observation(
            contract,
            mission_state,
            "obs-deployment-unknown",
            "deployment-ready",
            "The deployment is ready",
            "unknown",
            "observer-deployment",
            7,
        )
        belief = apply_observation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            observation=unknown,
        )["result_state"]
        plan = _build_plan(
            contract,
            mission_state,
            belief,
            goal,
            portfolio,
            required_claim_ids=[
                "repository-clean",
                "ci-baseline-green",
                "deployment-ready",
            ],
        )
        self.assertEqual("blocked_unknown", plan["status"])
        self.assertFalse(plan["effect_authority_granted"])
        self.assertFalse(plan["non_authority"]["grants_execution_authority"])

    def test_capability_resource_and_dependency_bounds(self) -> None:
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        subgoals, steps, alternatives = _plan_parts()
        capability_blocked = build_semantic_plan(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            planner_id="planner-v022",
            plan_id="capability-blocked",
            required_claim_ids=["repository-clean"],
            available_capabilities=["observe.read"],
            subgoals=subgoals,
            steps=steps,
            alternatives=alternatives,
            created_at_ms=10,
            valid_until_ms=100,
        )
        self.assertEqual("capability_gap", capability_blocked["status"])

        costly_steps = deepcopy(steps)
        costly_steps[1]["cost_bound"] = 20.0
        resource_blocked = build_semantic_plan(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            planner_id="planner-v022",
            plan_id="resource-blocked",
            required_claim_ids=["repository-clean"],
            available_capabilities=["observe.read", "plan.propose"],
            subgoals=subgoals,
            steps=costly_steps,
            alternatives=alternatives,
            created_at_ms=10,
            valid_until_ms=100,
        )
        self.assertEqual("resource_blocked", resource_blocked["status"])

        cyclic_steps = deepcopy(steps)
        cyclic_steps[0]["dependencies"] = ["step-propose"]
        with self.assertRaisesRegex(ValueError, "step_dependency_cycle"):
            build_semantic_plan(
                contract=contract,
                mission_state=mission_state,
                belief_state=belief,
                goal=goal,
                goal_portfolio=portfolio,
                planner_id="planner-v022",
                plan_id="cycle",
                required_claim_ids=["repository-clean"],
                available_capabilities=["observe.read", "plan.propose"],
                subgoals=subgoals,
                steps=cyclic_steps,
                alternatives=alternatives,
                created_at_ms=10,
                valid_until_ms=100,
            )

    def test_verifier_must_be_independent(self) -> None:
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        plan = _build_plan(contract, mission_state, belief, goal, portfolio)
        with self.assertRaisesRegex(ValueError, "planner_self_verification_forbidden"):
            build_verification_receipt(
                contract=contract,
                mission_state=mission_state,
                source_belief_state=belief,
                goal=goal,
                goal_portfolio=portfolio,
                plan=plan,
                verifier_id=plan["planner_id"],
                independent_observations=[],
                criterion_assessments=[],
                execution_receipt_digests=[],
                observed_at_ms=20,
            )

        planning_observation = belief["observation_history"][0]
        with self.assertRaisesRegex(
            ValueError, "planning_evidence_reused_as_independent_verification"
        ):
            build_verification_receipt(
                contract=contract,
                mission_state=mission_state,
                source_belief_state=belief,
                goal=goal,
                goal_portfolio=portfolio,
                plan=plan,
                verifier_id="independent-verifier",
                independent_observations=[planning_observation],
                criterion_assessments=[],
                execution_receipt_digests=[],
                observed_at_ms=20,
            )

    def test_exact_belief_change_invalidates_plan(self) -> None:
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        plan = _build_plan(contract, mission_state, belief, goal, portfolio)
        changed = apply_observation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            observation=_observation(
                contract,
                mission_state,
                "obs-unrelated",
                "unrelated-claim",
                "An unrelated fact changed",
                "supports",
                "observer-unrelated",
                12,
            ),
        )["result_state"]
        receipt = build_plan_invalidation_receipt(
            contract=contract,
            mission_state=mission_state,
            source_belief_state=belief,
            current_belief_state=changed,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            checked_at_ms=13,
        )
        self.assertEqual("invalidated", receipt["status"])
        self.assertEqual([], receipt["changed_claim_ids"])
        self.assertTrue(receipt["exact_basis_changed"])

    def test_store_replay_and_snapshot_repair(self) -> None:
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        plan = _build_plan(contract, mission_state, belief, goal, portfolio)
        with TemporaryDirectory() as directory:
            initialize_planner_verifier_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                chart_id="github-main",
                now_ms=9,
            )
            first = persist_plan(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                belief_state=belief,
                goal=goal,
                goal_portfolio=portfolio,
                plan=plan,
            )
            replay = persist_plan(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                belief_state=belief,
                goal=goal,
                goal_portfolio=portfolio,
                plan=plan,
            )
            self.assertEqual("APPLIED", first["status"])
            self.assertEqual("REPLAYED", replay["status"])
            self.assertEqual(
                1,
                len(
                    (Path(directory) / "planner-verifier-ledger.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ),
            )
            (Path(directory) / "snapshot.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "snapshot_ledger_mismatch"):
                recover_planner_verifier_store(
                    store_dir=directory,
                    contract=contract,
                    mission_state=mission_state,
                )
            repaired = recover_planner_verifier_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                repair_snapshot=True,
            )
            self.assertEqual(1, repaired["revision"])

    def test_tampered_authority_fails_static_validation(self) -> None:
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        plan = _build_plan(contract, mission_state, belief, goal, portfolio)
        tampered = deepcopy(plan)
        tampered["non_authority"]["grants_execution_authority"] = True
        self.assertIn("plan_non_authority_invalid", validate_semantic_plan_static(tampered))


if __name__ == "__main__":
    unittest.main()
