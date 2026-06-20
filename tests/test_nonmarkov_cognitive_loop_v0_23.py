from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_nonmarkov_cognitive_loop_kernel_v0_23 import (
    build_future_strategy_delta,
    build_nonmarkov_cognitive_episode,
    validate_nonmarkov_cognitive_episode,
)
from runtime.kuuos_nonmarkov_cognitive_loop_scenarios_v0_23 import (
    _all_expected_labels,
    _process_packet,
    _success_receipt,
    run_nonmarkov_cognitive_loop_scenarios,
)
from runtime.kuuos_nonmarkov_cognitive_loop_store_v0_23 import (
    initialize_store,
    persist_episode,
    recover_store,
)
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _build_plan,
    _fixture,
    _ready_belief_state,
)


class NonMarkovCognitiveLoopV023Tests(unittest.TestCase):
    def _basis(self):
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        plan = _build_plan(contract, mission_state, belief, goal, portfolio)
        success = _success_receipt(
            contract, mission_state, belief, goal, portfolio, plan
        )
        return contract, mission_state, goal, portfolio, belief, plan, success

    def test_full_scenarios(self) -> None:
        result = run_nonmarkov_cognitive_loop_scenarios()
        self.assertEqual(
            "KUUOS_NONMARKOV_COGNITIVE_LOOP_V0_23_OK", result["status"]
        )
        self.assertEqual("complete_candidate", result["passed_route"])
        self.assertEqual("replan", result["failed_route"])
        self.assertEqual("reobserve", result["indeterminate_route"])
        self.assertEqual("rerotate_required", result["rerotation_route"])
        self.assertTrue(result["history_replay_ready"])
        self.assertTrue(result["belief_plurality_preserved"])
        self.assertTrue(result["observation_not_verification"])
        self.assertTrue(result["verification_not_truth"])
        self.assertTrue(result["learning_future_only"])
        self.assertTrue(result["memory_append_only"])
        self.assertFalse(result["execution_authority_granted"])

    def test_invalid_process_tensor_fails_closed(self) -> None:
        contract, mission_state, goal, portfolio, belief, plan, success = self._basis()
        packet = _process_packet()
        packet["process_tensor"]["history_state_not_replaced_by_snapshot"] = False
        with self.assertRaisesRegex(ValueError, "qi_process_tensor_invalid"):
            build_nonmarkov_cognitive_episode(
                contract=contract,
                mission_state=mission_state,
                belief_state=belief,
                goal=goal,
                goal_portfolio=portfolio,
                plan=plan,
                verification_receipt=success,
                qi_process_tensor_packet=packet,
                prior_memory_entries=[],
                actual_observation_labels=_all_expected_labels(plan),
                step_outcomes=[],
                coherence_defect=0.1,
                cycle_index=1,
                created_at_ms=60,
            )

    def test_coherence_defect_only_widens_uncertainty(self) -> None:
        contract, mission_state, goal, portfolio, belief, plan, success = self._basis()
        episode = build_nonmarkov_cognitive_episode(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verification_receipt=success,
            qi_process_tensor_packet=_process_packet(),
            prior_memory_entries=[],
            actual_observation_labels=_all_expected_labels(plan),
            step_outcomes=[],
            coherence_defect=0.4,
            cycle_index=1,
            created_at_ms=60,
        )
        projection = episode["coherence_projection"]
        self.assertLessEqual(
            projection["coherent_lower"], projection["base_confidence"]
        )
        self.assertGreaterEqual(
            projection["coherent_upper"], projection["base_confidence"]
        )
        self.assertTrue(projection["plurality_preserved"])
        self.assertFalse(projection["global_winner_selected"])
        self.assertFalse(projection["residue_grants_authority"])

    def test_strategy_learning_is_future_only(self) -> None:
        contract, mission_state, goal, portfolio, belief, plan, success = self._basis()
        delta = build_future_strategy_delta(
            contract=contract,
            plan=plan,
            verification_receipt=success,
            step_outcomes=[
                {
                    "step_id": plan["steps"][0]["step_id"],
                    "outcome": "succeeded",
                    "evidence_refs": [success["verification_receipt_digest"]],
                }
            ],
            memory_replay={"probe_planner_reuse_hint": "retain_history"},
            created_at_ms=60,
        )
        self.assertTrue(delta["future_only"])
        self.assertFalse(delta["automatic_application"])
        self.assertFalse(delta["current_plan_mutated"])
        self.assertFalse(delta["current_belief_root_mutated"])
        self.assertFalse(delta["memory_root_overwritten"])
        self.assertTrue(delta["candidate_weighting_not_truth"])

    def test_memory_replay_changes_mode_without_granting_authority(self) -> None:
        contract, mission_state, goal, portfolio, belief, plan, success = self._basis()
        first = build_nonmarkov_cognitive_episode(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verification_receipt=success,
            qi_process_tensor_packet=_process_packet(),
            prior_memory_entries=[],
            actual_observation_labels=_all_expected_labels(plan),
            step_outcomes=[],
            coherence_defect=0.1,
            cycle_index=1,
            created_at_ms=60,
        )
        memory_entry = first["handoff"]["memoryos"]["append_writeback_receipt"]
        second = build_nonmarkov_cognitive_episode(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verification_receipt=success,
            qi_process_tensor_packet=_process_packet(),
            prior_memory_entries=[memory_entry],
            actual_observation_labels=_all_expected_labels(plan),
            step_outcomes=[],
            coherence_defect=0.1,
            cycle_index=2,
            created_at_ms=70,
        )
        self.assertEqual("history_replay_ready", second["memory_mode"])
        self.assertFalse(
            second["handoff"]["memoryos"]["retrieval_replay"][
                "grants_probe_execution_authority"
            ]
        )
        self.assertFalse(
            second["handoff"]["qi_process_tensor"]["authority_granted"]
        )

    def test_store_replay_and_snapshot_repair(self) -> None:
        contract, mission_state, goal, portfolio, belief, plan, success = self._basis()
        episode = build_nonmarkov_cognitive_episode(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verification_receipt=success,
            qi_process_tensor_packet=_process_packet(),
            prior_memory_entries=[],
            actual_observation_labels=_all_expected_labels(plan),
            step_outcomes=[],
            coherence_defect=0.1,
            cycle_index=1,
            created_at_ms=60,
        )
        with TemporaryDirectory() as directory:
            initialize_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                chart_id=belief["chart_id"],
                now_ms=59,
            )
            first = persist_episode(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                episode=episode,
            )
            replay = persist_episode(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                episode=episode,
            )
            self.assertEqual("APPLIED", first["status"])
            self.assertEqual("REPLAYED", replay["status"])
            ledger = Path(directory) / "nonmarkov-cognitive-loop-ledger.jsonl"
            self.assertEqual(1, len(ledger.read_text(encoding="utf-8").splitlines()))
            (Path(directory) / "snapshot.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "snapshot_ledger_mismatch"):
                recover_store(
                    store_dir=directory,
                    contract=contract,
                    mission_state=mission_state,
                )
            repaired = recover_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                repair_snapshot=True,
            )
            self.assertEqual(1, repaired["revision"])
            self.assertTrue(repaired["append_only"])
            self.assertFalse(repaired["memory_overwrite"])

    def test_tampered_authority_is_rejected(self) -> None:
        contract, mission_state, goal, portfolio, belief, plan, success = self._basis()
        episode = build_nonmarkov_cognitive_episode(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            goal=goal,
            goal_portfolio=portfolio,
            plan=plan,
            verification_receipt=success,
            qi_process_tensor_packet=_process_packet(),
            prior_memory_entries=[],
            actual_observation_labels=_all_expected_labels(plan),
            step_outcomes=[],
            coherence_defect=0.1,
            cycle_index=1,
            created_at_ms=60,
        )
        tampered = deepcopy(episode)
        tampered["handoff"]["planos"]["execution_granted"] = True
        self.assertIn(
            "episode_planos_execution_granted_forbidden",
            validate_nonmarkov_cognitive_episode(tampered),
        )


if __name__ == "__main__":
    unittest.main()
