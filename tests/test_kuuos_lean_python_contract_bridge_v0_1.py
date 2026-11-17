"""Regression cases for the read-only Lean/Python contract projections."""
from __future__ import annotations

from types import ModuleType
from unittest import TestCase, main
from unittest.mock import patch
import sys

from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    BLOCKED, NO_DATA, PASSED, CORE_CONTRACTS,
    audit_core_state, audit_core_transition, codeai_candidate_eligible,
    codeai_selection_boundary_check, memory_blocker_boundary_check,
)


class CoreContractTests(TestCase):
    @staticmethod
    def state_fixture(contract):
        return {
            "version": f"stub_{contract.stem}_state_v0_1",
            "current_phase": contract.phases[0],
            contract.digest_key: "hash0",
            "event_index": 0,
            "event_history": [],
            "processed_event_digests": [],
            "non_authority": {"truth_authority_granted": False},
            "boundary": {"append_only_history_required": True},
        }

    def test_all_core_os_contracts_have_pinned_proof(self):
        self.assertEqual(set(CORE_CONTRACTS), {
            "BeliefOS", "DecisionOS", "PlanOS", "ActOS",
            "ObserveOS", "VerifyOS", "LearnOS",
        })
        for contract in CORE_CONTRACTS.values():
            self.assertTrue(contract.lean_source.startswith("formal/KUOS/"))
            self.assertTrue(contract.phase_theorem)
            self.assertTrue(contract.event_theorem)
            self.assertTrue(contract.authority_theorem)

    def test_missing_state_fails_as_no_data(self):
        self.assertEqual(audit_core_state("BeliefOS", None).status, NO_DATA)

    def test_runtime_original_validator_and_non_authority_gate(self):
        for os_name, contract in CORE_CONTRACTS.items():
            with self.subTest(os_name=os_name):
                types = ModuleType(contract.runtime_types)
                types.PHASES = contract.phases
                types.STATE_VERSION = f"stub_{contract.stem}_state_v0_1"
                types.NON_AUTHORITY_FLAGS = {"truth_authority_granted": False}
                types.REQUIRED_BOUNDARY = {"append_only_history_required": True}
                kernel = ModuleType(contract.runtime_kernel)
                setattr(kernel, f"validate_{contract.stem}_state", lambda state: [])
                with patch.dict(sys.modules, {
                    contract.runtime_types: types, contract.runtime_kernel: kernel,
                }):
                    state = self.state_fixture(contract)
                    self.assertEqual(audit_core_state(os_name, state).status, PASSED)
                    state["non_authority"]["truth_authority_granted"] = True
                    self.assertEqual(audit_core_state(os_name, state).status, BLOCKED)
                    state["non_authority"].pop("truth_authority_granted")
                    self.assertEqual(audit_core_state(os_name, state).status, NO_DATA)

    def test_core_transition_prevents_skips_rewrites_and_fake_replay(self):
        for os_name, contract in CORE_CONTRACTS.items():
            with self.subTest(os_name=os_name):
                before = self.state_fixture(contract)
                target = contract.phases[1]
                event = {"source_phase": contract.phases[0], "target_phase": target,
                         contract.event_key: "event1", "event_index": 1}
                after = dict(before,
                             current_phase=target,
                             event_index=1,
                             event_history=[{"event": "event1"}],
                             processed_event_digests=["event1"])
                after[f"predecessor_{contract.digest_key}"] = "hash0"
                result = {"status": "APPLIED", "state": after}
                self.assertEqual(audit_core_transition(os_name, before, event, result).status, PASSED)
                after_wrong = dict(after, event_index=2)
                self.assertEqual(audit_core_transition(os_name, before, event,
                                                       {"status": "APPLIED", "state": after_wrong}).status,
                                 BLOCKED)
                event_wrong = dict(event, target_phase=contract.phases[2])
                self.assertEqual(audit_core_transition(os_name, before, event_wrong, result).status, BLOCKED)
                self.assertEqual(audit_core_transition(os_name, before, event,
                                                       {"status": "REPLAYED", "state": after}).status,
                                 BLOCKED)
                self.assertEqual(audit_core_transition(os_name, before, event,
                                                       {"status": "REPLAYED", "state": before}).status,
                                 PASSED)

    def test_belief_cycle_only_wraps_after_commit(self):
        contract = CORE_CONTRACTS["BeliefOS"]
        before = self.state_fixture(contract)
        before["current_phase"] = "commit"
        event = {"source_phase": "commit", "target_phase": "propose", contract.event_key: "e", "event_index": 1}
        after = dict(before, current_phase="propose", event_index=1,
                     event_history=[{"event": "e"}], processed_event_digests=["e"])
        after[f"predecessor_{contract.digest_key}"] = "hash0"
        self.assertEqual(audit_core_transition("BeliefOS", before, event,
                                               {"status": "APPLIED", "state": after}).status, PASSED)
        self.assertEqual(audit_core_transition("DecisionOS", before, event,
                                               {"status": "APPLIED", "state": after}).status, BLOCKED)

    def test_codeai_score_never_overrides_failed_gate(self):
        self.assertTrue(codeai_candidate_eligible("admissible", "allPassed"))
        self.assertFalse(codeai_candidate_eligible("repairable", "allPassed"))
        self.assertFalse(codeai_candidate_eligible("admissible", "incomplete"))
        self.assertFalse(codeai_candidate_eligible("admissible", "hasFailure"))

    def test_codeai_receipt_does_not_gain_authority(self):
        receipt = {key: False for key in (
            "test_execution_performed_by_kernel", "repair_executed", "repository_mutation_performed",
            "git_effect_performed", "verification_authority_granted", "repair_authority_granted",
            "execution_authority_granted", "git_authority_granted", "score_treated_as_probability",
            "score_treated_as_correctness_proof", "selection_treated_as_correctness_proof",
            "abstention_treated_as_rejection",
        )}
        self.assertEqual(codeai_selection_boundary_check(receipt).status, PASSED)
        receipt["git_effect_performed"] = True
        self.assertEqual(codeai_selection_boundary_check(receipt).status, BLOCKED)

    def test_memoryos_blocker_not_silently_discharged(self):
        boundary = {
            "blockerStoredAsContext": True, "blockerReleasedByMemory": False,
            "missingEvidenceSilentlyRepaired": False, "worldProjectionReadOnly": True,
            "worldChangedByMemory": False, "retrievalCandidateOnly": True,
            "durableAppendClaimed": False,
        }
        self.assertEqual(memory_blocker_boundary_check(boundary).status, PASSED)
        boundary["blockerReleasedByMemory"] = True
        self.assertEqual(memory_blocker_boundary_check(boundary).status, BLOCKED)


if __name__ == "__main__":
    main()
