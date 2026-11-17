"""Scoped path composition tests; mocks cover routing, native fixtures cover real edges.

This suite is imported by the already-registered v0.5 cumulative test module,
retaining its exact runner/checker registration without weakening earlier gates.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_lean_python_os_path_composition_v0_6 as composite
from runtime.kuuos_lean_python_os_registry_v0_5 import ScopedAudit


def synthetic_states():
    return {
        name: {
            "lineage_id": "common-lineage",
            "mission_contract_digest": "common-mission",
            "updated_at_ms": i * 10,
        }
        for i, name in enumerate(composite.PATH)
    }


def synthetic_receipts():
    return {key: {"external_only": "synthetic; never authenticated"}
            for key in composite.RECEIPT_EDGE_NAMES}


def fake_success(*args, **kwargs):
    return ScopedAudit(
        status="RUNTIME_CHECK_PASSED",
        name=args[0] + "->" + args[1], scope="synthetic_dispatch_only",
        original_status="RUNTIME_CHECK_PASSED", runtime_checked=True,
    )


class CompositionContractTests(unittest.TestCase):
    def test_the_route_covers_all_seven_declared_edges_without_shortcuts(self):
        from runtime.kuuos_lean_python_os_registry_v0_5 import EDGES
        self.assertEqual(set(zip(composite.PATH, composite.PATH[1:])),
                         set(EDGES))
        self.assertEqual(len(composite.PATH), 8)
        self.assertEqual(len(EDGES), 7)

    def test_full_synthetic_dispatch_checks_exactly_seven_edges(self):
        with patch.object(composite, "audit_edge", side_effect=fake_success) as auditor:
            result = composite.audit_typed_path(
                synthetic_states(), receipts=synthetic_receipts(),
            )
        self.assertEqual(result.status, composite.PASS, result)
        self.assertEqual(len(result.edge_audits), 7)
        self.assertEqual(auditor.call_count, 7)
        self.assertFalse(result.formal_descent_certified)
        self.assertFalse(result.lean_python_refinement_proved)
        self.assertFalse(result.external_receipt_authenticated)
        self.assertFalse(result.execution_authority_granted)
        self.assertFalse(result.truth_authority_granted)
        self.assertFalse(result.merge_authority_granted)

    def test_mock_no_validator_receipt_does_not_produce_scoped_pass(self):
        def no_native(*args, **kwargs):
            return ScopedAudit("PASS", "x", "synthetic", "PASS", runtime_checked=False)
        with patch.object(composite, "audit_edge", side_effect=no_native):
            result = composite.audit_typed_path(
                synthetic_states(), receipts=synthetic_receipts(),
            )
        self.assertEqual(result.status, "NO_DATA")
        self.assertIn("native_checks_unconfirmed", " ".join(result.missing))

    def test_missing_intermediate_even_with_passing_stub_remains_no_data(self):
        states = synthetic_states()
        del states["DecisionOSPlural"]
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(
                states, receipts=synthetic_receipts(),
                start="DecisionOS", end="PlanOS",
            )
        self.assertEqual(result.status, "NO_DATA")
        self.assertIn("state:DecisionOSPlural:missing", result.missing)
        self.assertFalse(result.local_python_checks_completed)

    def test_missing_plan_phase_receipt_remains_no_data(self):
        states = synthetic_states()
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(
                states, receipts={"DecisionOSWa->PlanOS": {}},
                start="PlanOS", end="ActOS",
            )
        self.assertEqual(result.status, "NO_DATA")
        self.assertIn("receipt:PlanOS->ActOS:missing", result.missing)

    def test_missing_wa_replan_receipt_remains_no_data(self):
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(
                synthetic_states(), receipts={},
                start="DecisionOSWa", end="PlanOS",
            )
        self.assertEqual(result.status, "NO_DATA")

    def test_direct_nonadjacent_jump_never_shortcuts_mediators(self):
        states = {key: val for key, val in synthetic_states().items()
                  if key in ("DecisionOS", "PlanOS")}
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(
                states, receipts=synthetic_receipts(),
                start="DecisionOS", end="PlanOS",
            )
        self.assertEqual(result.status, "NO_DATA")
        self.assertLess(len(result.edge_audits), 3)

    def test_context_divergence_blocks_even_if_all_edges_are_mocked_green(self):
        states = synthetic_states()
        states["ActOS"]["lineage_id"] = "other-lineage"
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(
                states, receipts=synthetic_receipts(),
            )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("state:ActOS:cross_context_mismatch", result.violations)

    def test_mission_digest_divergence_blocks_even_if_edges_are_mocked_green(self):
        states = synthetic_states()
        states["VerifyOS"]["mission_contract_digest"] = "other-mission"
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(states, receipts=synthetic_receipts())
        self.assertEqual(result.status, "BLOCKED")

    def test_time_regression_blocks_even_if_edges_are_mocked_green(self):
        states = synthetic_states()
        states["PlanOS"]["updated_at_ms"] = 999
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(states, receipts=synthetic_receipts())
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("PlanOS->ActOS:time_regression", result.violations)

    def test_unknown_or_reverse_path_does_not_pass(self):
        for start, end in (
            ("CodeAI", "LearnOS"), ("DecisionOS", "WORLD"),
            ("VerifyOS", "ActOS"), ("ActOS", "ActOS"),
        ):
            with self.subTest(start=start, end=end):
                result = composite.audit_typed_path(
                    synthetic_states(), receipts=synthetic_receipts(),
                    start=start, end=end,
                )
                self.assertNotEqual(result.status, composite.PASS)

    def test_real_edge_auditor_does_not_accept_synthetic_packets(self):
        result = composite.audit_typed_path(
            synthetic_states(), receipts=synthetic_receipts(),
            start="PlanOS", end="ActOS",
        )
        self.assertNotEqual(result.status, composite.PASS)
        self.assertFalse(result.local_python_checks_completed)

    def test_unknown_state_key_is_blocked(self):
        states = synthetic_states()
        states["FakeOS"] = {"lineage_id": "x"}
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(states, receipts=synthetic_receipts())
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("states:unknown_name", result.violations)

    def test_unknown_receipt_edge_is_blocked(self):
        receipts = synthetic_receipts()
        receipts["DecisionOS->PlanOS"] = {}
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(synthetic_states(), receipts=receipts)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("receipts:unknown_edge", result.violations)

    def test_observed_blockers_and_missing_data_are_both_preserved(self):
        states = synthetic_states()
        del states["LearnOS"]
        states["ActOS"]["lineage_id"] = "wrong"
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(states, receipts=synthetic_receipts())
        self.assertEqual(result.status, "BLOCKED")
        self.assertTrue(result.violations)
        self.assertTrue(result.missing)

    def test_one_blocked_edge_prevents_global_success(self):
        def one_bad(source, target, *_args, **_kwargs):
            if source == "DecisionOSWa":
                return ScopedAudit("BLOCKED", "x", "test", "BLOCKED", issues=("bad",))
            return fake_success(source, target)
        with patch.object(composite, "audit_edge", side_effect=one_bad):
            result = composite.audit_typed_path(
                synthetic_states(), receipts=synthetic_receipts(),
            )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("edge:DecisionOSWa->PlanOS:blocked", result.violations)

    def test_missing_edge_data_retains_no_data(self):
        def one_missing(source, target, *_args, **_kwargs):
            if source == "ActOS":
                return ScopedAudit("NO_DATA", "x", "test", "NO_DATA", issues=("source_missing",))
            return fake_success(source, target)
        with patch.object(composite, "audit_edge", side_effect=one_missing):
            result = composite.audit_typed_path(
                synthetic_states(), receipts=synthetic_receipts(),
            )
        self.assertEqual(result.status, "NO_DATA")

    def test_mutating_auditor_cannot_mutate_caller_or_succeed(self):
        states = synthetic_states()
        old = deepcopy(states)
        def mutator(source, target, first, second, **kwargs):
            first["lineage_id"] = "mutated_by_validator"
            return fake_success(source, target)
        with patch.object(composite, "audit_edge", side_effect=mutator):
            result = composite.audit_typed_path(states, receipts=synthetic_receipts())
        self.assertEqual(states, old)
        self.assertEqual(result.status, "BLOCKED")
        self.assertTrue(any("validator_mutated_snapshot" in x for x in result.violations))

    def test_auditor_mutation_to_unserializable_object_fails_closed(self):
        original = synthetic_states()
        prior = deepcopy(original)
        def corrupt(source, target, first, second, **kwargs):
            first["injected_object"] = object()
            return fake_success(source, target)
        with patch.object(composite, "audit_edge", side_effect=corrupt):
            result = composite.audit_typed_path(original, receipts=synthetic_receipts())
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(original, prior)
        self.assertTrue(any("validator_mutated_to_invalid_json" in x
                            for x in result.violations))

    def test_auditor_exception_blocks(self):
        with patch.object(composite, "audit_edge", side_effect=RuntimeError("unexpected")):
            result = composite.audit_typed_path(
                synthetic_states(), receipts=synthetic_receipts(),
            )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("audit_exception:RuntimeError", " ".join(result.violations))

    def test_bad_result_cannot_appear_green(self):
        with patch.object(composite, "audit_edge", return_value=None):
            result = composite.audit_typed_path(
                synthetic_states(), receipts=synthetic_receipts(),
            )
        self.assertEqual(result.status, "BLOCKED")

    def test_input_snapshot_hash_is_stable_and_binds_exact_payloads(self):
        states = synthetic_states()
        receipt = synthetic_receipts()
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            first = composite.audit_typed_path(states, receipts=receipt)
            second = composite.audit_typed_path(states, receipts=receipt)
            modified = deepcopy(states)
            modified["VerifyOS"]["updated_at_ms"] += 1
            third = composite.audit_typed_path(modified, receipts=receipt)
        self.assertEqual(first.input_sha256, second.input_sha256)
        self.assertNotEqual(first.input_sha256, third.input_sha256)

    def test_nonjson_input_cannot_execute_custom_objects(self):
        class CustomMap(dict):
            def items(self):
                raise AssertionError("not permitted")
        for value in (CustomMap(), object(), float("nan"), {1: "bad"}):
            with self.subTest(kind=type(value).__name__):
                states = synthetic_states()
                states["ActOS"]["extra"] = value
                with patch.object(composite, "audit_edge", side_effect=fake_success):
                    result = composite.audit_typed_path(states, receipts=synthetic_receipts())
                self.assertEqual(result.status, "BLOCKED")

    def test_cyclic_json_is_blocked_without_crash(self):
        states = synthetic_states()
        states["PlanOS"]["cycle"] = states["PlanOS"]
        with patch.object(composite, "audit_edge", side_effect=fake_success):
            result = composite.audit_typed_path(states, receipts=synthetic_receipts())
        self.assertEqual(result.status, "BLOCKED")

    def test_bad_time_type_is_blocked_not_coerced(self):
        for bad in (True, 8.0, "8", -1):
            with self.subTest(bad=bad):
                states = synthetic_states()
                states["ActOS"]["updated_at_ms"] = bad
                with patch.object(composite, "audit_edge", side_effect=fake_success):
                    result = composite.audit_typed_path(states, receipts=synthetic_receipts())
                self.assertEqual(result.status, "BLOCKED")

    def test_immutability_of_evidence(self):
        from dataclasses import FrozenInstanceError
        result = composite.audit_typed_path(None)
        with self.assertRaises(FrozenInstanceError):
            result.status = "PASS"


class NativeCompositionTests(unittest.TestCase):
    """Genuine KuuOS constructors, validators and receipts; no fake PASS."""

    def test_genuine_decision_plural_wa_plan_segment(self):
        from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
            _build_belief, _build_decision, _build_plural, _build_wa,
        )
        from runtime.kuuos_belief_os_types_v0_1 import sha
        from runtime.kuuos_decision_os_wa_kernel_v0_3 import build_replan_wa_activation_receipt
        from runtime.kuuos_plan_os_state_v0_1 import build_initial_plan_state
        with TemporaryDirectory(prefix="kuuos-v06-decision-plan-") as folder:
            root = Path(folder)
            lineage = "v06-native-route"
            _, belief = _build_belief(root / "belief", lineage)
            decision = _build_decision(root / "decision", lineage, sha("v06-mission"), belief)
            plural = _build_plural(root / "plural", lineage, decision)
            wa = _build_wa(root / "wa", plural)
            receipt = build_replan_wa_activation_receipt(
                state=wa, mission_cycle_phase="replan",
                mission_cycle_state_digest=sha("v06-replan-state"),
                replan_receipt_digest=sha("v06-replan"),
                next_plan_basis_digest=sha("v06-next-plan"), now_ms=50_000,
            )
            plan = build_initial_plan_state(
                plan_id="v06-plan", source_wa_state=wa,
                replan_activation_receipt=receipt,
                plan_budget=2.0, maximum_step_risk=0.40, now_ms=60_000,
            )
            states = dict(zip(composite.PATH[:4], (decision, plural, wa, plan)))
            before = deepcopy((states, receipt))
            result = composite.audit_typed_path(
                states, receipts={"DecisionOSWa->PlanOS": receipt},
                start="DecisionOS", end="PlanOS",
            )
            self.assertEqual(result.status, composite.PASS, result)
            self.assertEqual(len(result.edge_audits), 3)
            self.assertEqual((states, receipt), before)

    def test_genuine_committed_plan_activation_initial_act_segment(self):
        from runtime.kuuos_act_os_fixture_v0_1 import source_plan
        from runtime.kuuos_act_os_kernel_v0_1 import build_initial_act_state
        with TemporaryDirectory(prefix="kuuos-v06-plan-act-") as folder:
            plan, receipt = source_plan(Path(folder))
            act = build_initial_act_state(
                act_id="v06-native-act", plan_state=plan,
                plan_activation_receipt=receipt, now_ms=90_000,
            )
            old = deepcopy((plan, receipt, act))
            result = composite.audit_typed_path(
                {"PlanOS": plan, "ActOS": act},
                receipts={"PlanOS->ActOS": receipt},
                start="PlanOS", end="ActOS",
            )
            self.assertEqual(result.status, composite.PASS, result)
            self.assertEqual((plan, receipt, act), old)

    def test_genuine_act_observe_segment(self):
        from runtime.kuuos_observe_os_fixture_v0_1 import source_act_state
        from runtime.kuuos_observe_os_kernel_v0_1 import build_initial_observe_state
        with TemporaryDirectory(prefix="kuuos-v06-act-observe-") as folder:
            act = source_act_state(Path(folder) / "act")
            observe = build_initial_observe_state(
                observe_id="v06-observe", act_state=act, now_ms=100_000,
            )
            result = composite.audit_typed_path(
                {"ActOS": act, "ObserveOS": observe},
                start="ActOS", end="ObserveOS",
            )
            self.assertEqual(result.status, composite.PASS, result)

    def test_genuine_observe_verify_segment(self):
        from runtime.kuuos_verify_os_fixture_v0_1 import source_observe_state
        from runtime.kuuos_verify_os_kernel_v0_1 import build_initial_verify_state
        with TemporaryDirectory(prefix="kuuos-v06-observe-verify-") as folder:
            observe = source_observe_state(Path(folder) / "observe", verdict="MATCHED")
            verify = build_initial_verify_state(
                verify_id="v06-verify", observe_state=observe, now_ms=110_000,
            )
            result = composite.audit_typed_path(
                {"ObserveOS": observe, "VerifyOS": verify},
                start="ObserveOS", end="VerifyOS",
            )
            self.assertEqual(result.status, composite.PASS, result)

    def test_genuine_verify_learn_segment(self):
        from runtime.kuuos_learn_os_fixture_v0_1 import source_verify_state
        from runtime.kuuos_learn_os_kernel_v0_1 import build_initial_learn_state
        with TemporaryDirectory(prefix="kuuos-v06-verify-learn-") as folder:
            verify = source_verify_state(Path(folder) / "verify", verdict="PASSED")
            learn = build_initial_learn_state(
                learn_id="v06-learn", verify_state=verify, now_ms=200_000,
            )
            result = composite.audit_typed_path(
                {"VerifyOS": verify, "LearnOS": learn},
                start="VerifyOS", end="LearnOS",
            )
            self.assertEqual(result.status, composite.PASS, result)


if __name__ == "__main__":
    unittest.main()
