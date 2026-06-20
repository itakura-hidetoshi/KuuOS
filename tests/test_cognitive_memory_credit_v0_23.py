from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_cognitive_memory_credit_kernel_v0_23 import (
    build_cognitive_memory_consolidation,
    consolidation_digest,
    validate_cognitive_memory_consolidation_static,
)
from runtime.kuuos_cognitive_memory_credit_scenarios_v0_23 import (
    _observe_envelope,
    _qi_state,
    _verification,
    _verify_envelope,
    run_cognitive_memory_credit_scenarios,
)
from runtime.kuuos_cognitive_memory_credit_store_v0_23 import (
    initialize_cognitive_memory_store,
    persist_cognitive_memory_consolidation,
    recover_cognitive_memory_store,
)
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _build_plan,
    _fixture,
    _ready_belief_state,
)


class CognitiveMemoryCreditV023Tests(unittest.TestCase):
    def _success_fixture(self):
        contract, mission_state, goal, portfolio = _fixture()
        belief = _ready_belief_state(contract, mission_state)
        plan = _build_plan(contract, mission_state, belief, goal, portfolio)
        verification, observations = _verification(
            contract=contract,
            mission_state=mission_state,
            belief=belief,
            goal=goal,
            portfolio=portfolio,
            plan=plan,
            status="verified_success",
            observed_at_ms=100,
        )
        observe = _observe_envelope(
            plan=plan,
            observation_digest=observations[-1]["observation_digest"],
            suffix="test-success",
        )
        verify = _verify_envelope(
            observe_envelope=observe,
            verification=verification,
            verdict="PASSED",
            suffix="test-success",
        )
        return contract, mission_state, belief, plan, verification, observe, verify

    def test_full_scenarios(self) -> None:
        result = run_cognitive_memory_credit_scenarios()
        self.assertEqual("KUUOS_COGNITIVE_MEMORY_CREDIT_V0_23_OK", result["status"])
        self.assertTrue(result["success_consolidated"])
        self.assertTrue(result["contradiction_preserved"])
        self.assertTrue(result["memory_replay_ready"])
        self.assertTrue(result["beliefos_candidate_only"])
        self.assertTrue(result["planos_future_only"])
        self.assertTrue(result["credit_is_noncausal"])
        self.assertFalse(result["memory_overwrite_performed"])
        self.assertFalse(result["automatic_learning"])
        self.assertFalse(result["execution_performed"])

    def test_credit_is_bounded_and_noncausal(self) -> None:
        contract, mission_state, belief, plan, verification, observe, verify = (
            self._success_fixture()
        )
        receipt = build_cognitive_memory_consolidation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            semantic_plan=plan,
            verification_receipt=verification,
            observe_envelope=observe,
            verify_envelope=verify,
            qi_state=_qi_state("credit-bounds"),
            memory_entries=[],
            consolidator_id="test-consolidator",
            episode_id="credit-bounds-episode",
            consolidated_at_ms=120,
        )
        for assignment in receipt["credit_assignments"]:
            self.assertGreaterEqual(assignment["signed_credit"], -1.0)
            self.assertLessEqual(assignment["signed_credit"], 1.0)
            self.assertFalse(assignment["causal_claim"])
            self.assertTrue(assignment["future_only"])
            self.assertFalse(assignment["active_now"])

    def test_qi_context_cannot_grant_authority(self) -> None:
        contract, mission_state, belief, plan, verification, observe, verify = (
            self._success_fixture()
        )
        qi = _qi_state("authority-test")
        qi["grants_execution_authority"] = True
        receipt = build_cognitive_memory_consolidation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            semantic_plan=plan,
            verification_receipt=verification,
            observe_envelope=observe,
            verify_envelope=verify,
            qi_state=qi,
            memory_entries=[],
            consolidator_id="test-consolidator",
            episode_id="authority-test-episode",
            consolidated_at_ms=121,
        )
        self.assertFalse(receipt["non_authority"]["grants_execution_authority"])
        self.assertFalse(receipt["plan_strategy_candidate"]["execution_permission"])
        self.assertFalse(receipt["execution_performed"])

    def test_observation_verification_separation_is_required(self) -> None:
        contract, mission_state, belief, plan, verification, observe, verify = (
            self._success_fixture()
        )
        broken = deepcopy(observe)
        broken["observation_not_verification"] = False
        with self.assertRaisesRegex(ValueError, "observe_verification_separation_missing"):
            build_cognitive_memory_consolidation(
                contract=contract,
                mission_state=mission_state,
                belief_state=belief,
                semantic_plan=plan,
                verification_receipt=verification,
                observe_envelope=broken,
                verify_envelope=verify,
                qi_state=_qi_state("broken-observe"),
                memory_entries=[],
                consolidator_id="test-consolidator",
                episode_id="broken-observe-episode",
                consolidated_at_ms=122,
            )

    def test_verify_future_only_boundary_is_required(self) -> None:
        contract, mission_state, belief, plan, verification, observe, verify = (
            self._success_fixture()
        )
        broken = deepcopy(verify)
        broken["learning_must_be_future_only"] = False
        with self.assertRaisesRegex(ValueError, "verify_future_only_missing"):
            build_cognitive_memory_consolidation(
                contract=contract,
                mission_state=mission_state,
                belief_state=belief,
                semantic_plan=plan,
                verification_receipt=verification,
                observe_envelope=observe,
                verify_envelope=broken,
                qi_state=_qi_state("broken-verify"),
                memory_entries=[],
                consolidator_id="test-consolidator",
                episode_id="broken-verify-episode",
                consolidated_at_ms=123,
            )

    def test_missing_qi_process_tensor_blocks_consolidation(self) -> None:
        contract, mission_state, belief, plan, verification, observe, verify = (
            self._success_fixture()
        )
        qi = _qi_state("missing-process")
        qi["process_history"] = []
        qi["process_tensor_visible"] = False
        receipt = build_cognitive_memory_consolidation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            semantic_plan=plan,
            verification_receipt=verification,
            observe_envelope=observe,
            verify_envelope=verify,
            qi_state=qi,
            memory_entries=[],
            consolidator_id="test-consolidator",
            episode_id="missing-process-episode",
            consolidated_at_ms=124,
        )
        self.assertEqual("blocked", receipt["status"])
        self.assertIn("qi_process_tensor_not_visible", receipt["blockers"])
        self.assertFalse(receipt["memory_append_candidate"]["memory_append_requested"])

    def test_store_replay_and_snapshot_repair(self) -> None:
        contract, mission_state, belief, plan, verification, observe, verify = (
            self._success_fixture()
        )
        receipt = build_cognitive_memory_consolidation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            semantic_plan=plan,
            verification_receipt=verification,
            observe_envelope=observe,
            verify_envelope=verify,
            qi_state=_qi_state("store-test"),
            memory_entries=[],
            consolidator_id="test-consolidator",
            episode_id="store-test-episode",
            consolidated_at_ms=125,
        )
        with TemporaryDirectory() as directory:
            initialize_cognitive_memory_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                chart_id=belief["chart_id"],
                now_ms=124,
            )
            first = persist_cognitive_memory_consolidation(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                receipt=receipt,
            )
            replay = persist_cognitive_memory_consolidation(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                receipt=receipt,
            )
            self.assertEqual("APPLIED", first["status"])
            self.assertEqual("REPLAYED", replay["status"])
            self.assertEqual(
                1,
                len(
                    (Path(directory) / "cognitive-memory-ledger.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ),
            )
            (Path(directory) / "snapshot.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "snapshot_ledger_mismatch"):
                recover_cognitive_memory_store(
                    store_dir=directory,
                    contract=contract,
                    mission_state=mission_state,
                )
            repaired = recover_cognitive_memory_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                repair_snapshot=True,
            )
            self.assertEqual(1, repaired["revision"])
            self.assertFalse(repaired["memory_overwrite_performed"])

    def test_tampered_automatic_learning_and_overwrite_fail(self) -> None:
        contract, mission_state, belief, plan, verification, observe, verify = (
            self._success_fixture()
        )
        receipt = build_cognitive_memory_consolidation(
            contract=contract,
            mission_state=mission_state,
            belief_state=belief,
            semantic_plan=plan,
            verification_receipt=verification,
            observe_envelope=observe,
            verify_envelope=verify,
            qi_state=_qi_state("tamper-test"),
            memory_entries=[],
            consolidator_id="test-consolidator",
            episode_id="tamper-test-episode",
            consolidated_at_ms=126,
        )
        tampered = deepcopy(receipt)
        tampered["automatic_learning"] = True
        tampered["memory_overwrite_performed"] = True
        tampered["cognitive_memory_consolidation_digest"] = consolidation_digest(tampered)
        errors = validate_cognitive_memory_consolidation_static(tampered)
        self.assertIn("automatic_learning_forbidden", errors)
        self.assertIn("consolidation_memory_overwrite_forbidden", errors)


if __name__ == "__main__":
    unittest.main()
