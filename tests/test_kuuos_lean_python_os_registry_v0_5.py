"""Repository-level tests for named Lean/Python OS registry v0.5.

These confirm registry/existing runtime behavior; they are not Lean proofs.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from importlib.util import find_spec
import unittest

from runtime import kuuos_lean_python_os_registry_v0_5 as registry
from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    ADDITIONAL_PROOF_LINKS, CORE_CONTRACTS,
)
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import HANDOFF_CONTRACTS
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import EDGE_SPECS


class ProofRegistryTests(unittest.TestCase):
    def test_every_existing_core_os_registered_without_renaming(self):
        self.assertTrue(set(CORE_CONTRACTS).issubset(registry.OS_BINDINGS))
        for name, original in CORE_CONTRACTS.items():
            with self.subTest(name=name):
                binding = registry.get_os(name)
                self.assertEqual(binding.lean_file, original.lean_source)
                self.assertEqual(binding.runtime_module, original.runtime_kernel)
                self.assertEqual(
                    binding.theorem_names,
                    (original.phase_theorem, original.event_theorem,
                     original.authority_theorem),
                )
                self.assertEqual(binding.audit_kind, "core_original_validator")

    def test_specialized_os_keep_original_lean_and_python_links(self):
        for name, (lean_file, theorem, module) in ADDITIONAL_PROOF_LINKS.items():
            with self.subTest(name=name):
                item = registry.get_os(name)
                self.assertEqual(item.lean_file, lean_file)
                self.assertEqual(item.runtime_module, module)
                self.assertEqual(item.theorem_names, ((theorem,) if theorem else ()))

    def test_plural_and_wa_are_explicit_mediators_not_shortcuts(self):
        self.assertIn("DecisionOSPlural", registry.list_os())
        self.assertIn("DecisionOSWa", registry.list_os())
        self.assertIn(("DecisionOS", "DecisionOSPlural"), registry.list_edges())
        self.assertIn(("DecisionOSPlural", "DecisionOSWa"), registry.list_edges())
        self.assertIn(("DecisionOSWa", "PlanOS"), registry.list_edges())
        self.assertNotIn(("DecisionOS", "PlanOS"), registry.list_edges())

    def test_all_prior_handoff_edges_are_retained(self):
        self.assertTrue(set(HANDOFF_CONTRACTS).issubset(registry.EDGES))
        self.assertTrue(set(EDGE_SPECS).issubset(registry.EDGES))
        self.assertIn(("PlanOS", "ActOS"), registry.EDGES)
        self.assertEqual(len(registry.EDGES), 7)

    def test_all_twelve_selected_os_have_nonempty_source_reference(self):
        self.assertEqual(len(registry.OS_BINDINGS), 12)
        self.assertEqual(registry.list_os(), tuple(sorted(registry.OS_BINDINGS)))
        for name, binding in registry.OS_BINDINGS.items():
            self.assertTrue(binding.lean_file.endswith(".lean"), name)
            self.assertTrue(binding.python_path.endswith(".py"), name)
            self.assertFalse(binding.runtime_module.startswith("tests."), name)
            self.assertEqual(binding.name, name)

    def test_previous_proof_theorem_names_are_not_renamed(self):
        for name, contract in CORE_CONTRACTS.items():
            binding = registry.get_os(name)
            self.assertEqual(binding.theorem_names[2], contract.authority_theorem)

    def test_os_binding_is_immutable(self):
        binding = registry.get_os("ActOS")
        with self.assertRaises(FrozenInstanceError):
            binding.audit_kind = "execution"
        with self.assertRaises(TypeError):
            registry.OS_BINDINGS["InventedOS"] = binding

    def test_edge_binding_is_immutable(self):
        edge = registry.get_edge("PlanOS", "ActOS")
        with self.assertRaises(FrozenInstanceError):
            edge.receipt_required = False
        with self.assertRaises(TypeError):
            registry.EDGES[("DecisionOS", "PlanOS")] = edge

    def test_plan_act_requires_real_activation_receipt(self):
        result = registry.audit_edge("PlanOS", "ActOS", None, None)
        self.assertEqual(result.status, "NO_DATA")
        self.assertIn("original_activation_receipt_required", result.issues)
        self.assertFalse(result.execution_authority_granted)

    def test_wa_to_plan_requires_real_replan_receipt(self):
        result = registry.audit_edge("DecisionOSWa", "PlanOS", None, None)
        self.assertEqual(result.status, "NO_DATA")
        self.assertIn("original_activation_receipt_required", result.issues)

    def test_direct_decision_plan_skip_is_no_data(self):
        result = registry.audit_edge("DecisionOS", "PlanOS", {}, {})
        self.assertEqual(result.status, "NO_DATA")
        self.assertIn("unsupported_edge_no_descent", result.issues)

    def test_missing_ordinary_handoff_keeps_no_data(self):
        result = registry.audit_edge("ActOS", "ObserveOS", None, None)
        self.assertEqual(result.status, "NO_DATA")
        self.assertFalse(result.runtime_checked)

    def test_edge_does_not_infer_auth_from_synthetic_receipt(self):
        result = registry.audit_edge("PlanOS", "ActOS", {}, {}, activation_receipt={})
        self.assertNotIn(result.status, ("PASS", "RUNTIME_CHECK_PASSED"))
        self.assertFalse(result.execution_authority_granted)
        self.assertFalse(result.truth_authority_granted)
        self.assertFalse(result.lean_python_refinement_proved)

    def test_world_is_source_only_never_python_certified(self):
        result = registry.audit_os("WORLD", {})
        self.assertEqual(result.status, "NO_DATA")
        self.assertIn("source_reference_only_no_runtime_equivalence", result.issues)

    def test_plural_and_wa_require_typed_edge(self):
        for name in ("DecisionOSPlural", "DecisionOSWa"):
            with self.subTest(name=name):
                result = registry.audit_os(name, {})
                self.assertEqual(result.status, "NO_DATA")
                self.assertIn("typed_source_target_edge_required", result.issues)

    def test_missing_core_state_stays_no_data(self):
        for name in CORE_CONTRACTS:
            with self.subTest(name=name):
                result = registry.audit_os(name, None)
                self.assertEqual(result.status, "NO_DATA")
                self.assertFalse(result.runtime_checked)

    def test_specialized_boundary_does_not_infer_whole_os_truth(self):
        for name in ("MemoryOS", "CodeAI"):
            with self.subTest(name=name):
                result = registry.audit_os(name, {})
                self.assertEqual(result.status, "NO_DATA")
                self.assertFalse(result.execution_authority_granted)

    def test_unknown_os_never_promoted(self):
        result = registry.audit_os("MadeUpOS", {"status": "PASS"})
        self.assertEqual(result.status, "NO_DATA")
        self.assertIsNone(registry.get_os("MadeUpOS"))

    def test_unknown_edge_never_promoted(self):
        result = registry.audit_edge("MemoryOS", "ActOS", {}, {})
        self.assertEqual(result.status, "NO_DATA")
        self.assertIsNone(registry.get_edge("MemoryOS", "ActOS"))

    def test_registry_does_not_proclaim_refinement(self):
        for result in (
            registry.audit_os("WORLD", {}),
            registry.audit_os("ActOS", None),
            registry.audit_edge("PlanOS", "ActOS", None, None),
        ):
            self.assertFalse(result.lean_python_refinement_proved)
            self.assertFalse(result.execution_authority_granted)
            self.assertFalse(result.truth_authority_granted)
            self.assertFalse(result.merge_authority_granted)

    def test_source_modules_exist_in_the_checked_repo(self):
        for binding in registry.OS_BINDINGS.values():
            self.assertIsNotNone(find_spec(binding.runtime_module),
                                 binding.runtime_module)


# v0.6 is loaded by the already-registered cumulative v0.5 suite.
# Do not weaken or rewrite the previously pinned exact runner registry.
from tests.test_kuuos_lean_python_os_path_composition_v0_6 import (
    CompositionContractTests,
    NativeCompositionTests,
)

# v0.7 genuine native full-cycle ledger replay and static source pins are
# additive to v0.5/v0.6, with no weakening of the cumulative runner.
from tests.test_kuuos_lean_python_native_cycle_ledger_replay_v0_7 import (
    SourcePinTests,
    NativeCycleLedgerReplayTests,
)

# v0.8 explicitly observes the original local fixture constructor returns;
# the audit grants no external receipt authenticity or formal Lean refinement.
# Registered here to preserve the exact v0.5 cumulative CI runner/checker.
from tests.test_kuuos_lean_python_native_cycle_receipt_capture_v0_8 import (
    NativeCaptureV08Tests,
    CaptureSourceV08Tests,
)


# v0.9 child-process native fixture evidence is mandatory via this already
# registered cumulative Python test module; prior v0.1–v0.8 tests retained.
from tests.test_kuuos_lean_python_isolated_native_evidence_v0_9 import (
    IsolatedNativeEvidenceTests,
    EvidenceSourcePinTests,
)


# v0.10 checks original core transitions before local store commits, in
# a separate fixture child. Previous classes and runner order stay intact.
from tests.test_kuuos_lean_python_checked_transition_v0_10 import (
    CheckedTransitionTests,
)
from tests.test_kuuos_lean_python_guarded_native_cycle_v0_10 import (
    GuardedNativeCycleTests,
)
from tests.test_kuuos_lean_python_checked_transition_sources_v0_10 import (
    CheckedTransitionSourceTests,
)


if __name__ == "__main__":
    unittest.main()
