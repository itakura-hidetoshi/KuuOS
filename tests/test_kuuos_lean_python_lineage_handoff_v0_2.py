"""No-authority lineage tests; confirm exact field pairings and fail-closed behavior."""
from __future__ import annotations

from copy import deepcopy
from types import ModuleType
from unittest import TestCase, main
from unittest.mock import patch
import sys

from runtime.kuuos_lean_python_contract_bridge_v0_1 import BLOCKED, NO_DATA, PASSED, CORE_CONTRACTS
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import HANDOFF_CONTRACTS, audit_handoff


class LeanPythonLineageHandoffTests(TestCase):
    @staticmethod
    def fixtures(edge):
        """Fully-populated *contract* fixtures; original validators are mocked.

        These only test the bridge, NOT the real source kernel schemas.
        """
        c = HANDOFF_CONTRACTS[edge]
        src = CORE_CONTRACTS[c.source_os]
        tgt = CORE_CONTRACTS[c.target_os]
        source = {
            "version": "v-state", "current_phase": "commit", "route": c.source_route or "VERIFICATION_PASSED",
            "event_index": 0, "event_history": [], "processed_event_digests": [],
            "non_authority": {"truth_authority_granted": False},
            "boundary": {"append_only_history_required": True},
            src.digest_key: "source-digest", "updated_at_ms": 123,
        }
        target = {
            "version": "v-state", "current_phase": tgt.phases[0], "route": "PENDING",
            "event_index": 0, "event_history": [], "processed_event_digests": [],
            "non_authority": {"truth_authority_granted": False},
            "boundary": {"append_only_history_required": True},
            tgt.digest_key: "target-digest", "updated_at_ms": 124, "active_now": False,
        }
        for field in c.required_source_flags:
            source[field] = True
        for index, (source_field, target_field) in enumerate(c.equal_fields):
            if source_field not in source:
                source[source_field] = f"id-{index}"
            target[target_field] = source[source_field]
        # Do not allow any accidental key aliasing to bypass exact bindings.
        return source, target

    @staticmethod
    def stub_modules(edge):
        c = HANDOFF_CONTRACTS[edge]
        module_dict = {}
        for os_name in (c.source_os, c.target_os):
            spec = CORE_CONTRACTS[os_name]
            types = ModuleType(spec.runtime_types)
            types.PHASES = spec.phases
            types.STATE_VERSION = "v-state"
            types.NON_AUTHORITY_FLAGS = {"truth_authority_granted": False}
            types.REQUIRED_BOUNDARY = {"append_only_history_required": True}
            kernel = ModuleType(spec.runtime_kernel)
            setattr(kernel, f"validate_{spec.stem}_state", lambda state: [])
            module_dict[spec.runtime_types] = types
            module_dict[spec.runtime_kernel] = kernel
        return module_dict

    def test_each_exact_edge_passes_and_is_read_only(self):
        self.assertEqual(set(HANDOFF_CONTRACTS), {
            ("ActOS", "ObserveOS"), ("ObserveOS", "VerifyOS"), ("VerifyOS", "LearnOS")
        })
        for edge in HANDOFF_CONTRACTS:
            with self.subTest(edge=edge), patch.dict(sys.modules, self.stub_modules(edge)):
                source, target = self.fixtures(edge)
                original_source, original_target = deepcopy(source), deepcopy(target)
                result = audit_handoff(*edge, source, target)
                self.assertEqual(result.status, PASSED, result.issues)
                self.assertEqual(source, original_source)
                self.assertEqual(target, original_target)
                self.assertTrue(all(result.lean_theorems))

    def test_tamper_in_every_exact_binding_is_blocked(self):
        for edge, c in HANDOFF_CONTRACTS.items():
            with self.subTest(edge=edge), patch.dict(sys.modules, self.stub_modules(edge)):
                for _, target_field in c.equal_fields:
                    source, target = self.fixtures(edge)
                    target[target_field] = "TAMPERED"
                    outcome = audit_handoff(*edge, source, target)
                    self.assertEqual(outcome.status, BLOCKED, (edge, target_field, outcome.issues))

    def test_missing_binding_is_no_data(self):
        for edge, c in HANDOFF_CONTRACTS.items():
            with self.subTest(edge=edge), patch.dict(sys.modules, self.stub_modules(edge)):
                source, target = self.fixtures(edge)
                target.pop(c.equal_fields[-1][1])
                self.assertEqual(audit_handoff(*edge, source, target).status, NO_DATA)

    def test_uncommitted_or_debt_lost_is_blocked(self):
        for edge, c in HANDOFF_CONTRACTS.items():
            with self.subTest(edge=edge), patch.dict(sys.modules, self.stub_modules(edge)):
                source, target = self.fixtures(edge)
                source["current_phase"] = "bind"
                self.assertEqual(audit_handoff(*edge, source, target).status, BLOCKED)
                for required in c.required_source_flags:
                    source, target = self.fixtures(edge)
                    source[required] = False
                    self.assertEqual(audit_handoff(*edge, source, target).status, BLOCKED)

    def test_source_version_drift_and_validator_failure_block(self):
        edge = ("ActOS", "ObserveOS")
        with patch.dict(sys.modules, self.stub_modules(edge)):
            source, target = self.fixtures(edge)
            source["version"] = "stale"
            self.assertEqual(audit_handoff(*edge, source, target).status, BLOCKED)
        modules = self.stub_modules(edge)
        setattr(modules[CORE_CONTRACTS["ActOS"].runtime_kernel], "validate_act_state", lambda state: ["source_invalid"])
        with patch.dict(sys.modules, modules):
            source, target = self.fixtures(edge)
            result = audit_handoff(*edge, source, target)
            self.assertEqual(result.status, BLOCKED)
            self.assertTrue(any("original_validator:source_invalid" in i for i in result.issues))

    def test_original_validator_cannot_mutate_caller(self):
        edge = ("ActOS", "ObserveOS")
        modules = self.stub_modules(edge)
        def mutate_then_succeed(state):
            state["source_tampered"] = True
            return []
        setattr(modules[CORE_CONTRACTS["ActOS"].runtime_kernel], "validate_act_state", mutate_then_succeed)
        with patch.dict(sys.modules, modules):
            source, target = self.fixtures(edge)
            before = deepcopy(source)
            result = audit_handoff(*edge, source, target)
            self.assertEqual(result.status, BLOCKED)
            self.assertIn("original_validator_mutated_state_copy", result.issues)
            self.assertEqual(source, before)

    def test_future_only_learning_does_not_auto_activate(self):
        edge = ("VerifyOS", "LearnOS")
        with patch.dict(sys.modules, self.stub_modules(edge)):
            source, target = self.fixtures(edge)
            target["active_now"] = True
            self.assertEqual(audit_handoff(*edge, source, target).status, BLOCKED)

    def test_different_time_or_unknown_edge_is_not_silently_certified(self):
        edge = ("ObserveOS", "VerifyOS")
        with patch.dict(sys.modules, self.stub_modules(edge)):
            source, target = self.fixtures(edge)
            target["updated_at_ms"] = 122
            self.assertEqual(audit_handoff(*edge, source, target).status, BLOCKED)
        self.assertEqual(audit_handoff("DecisionOS", "PlanOS", {}, {}).status, NO_DATA)


class RealKernelLineageTests(TestCase):
    """Exercise genuine source constructors and validators, not mock validators."""

    def test_real_act_observe_verify_learn_handoff(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from runtime.kuuos_observe_os_fixture_v0_1 import source_act_state
        from runtime.kuuos_verify_os_fixture_v0_1 import source_observe_state
        from runtime.kuuos_learn_os_fixture_v0_1 import source_verify_state
        from runtime.kuuos_observe_os_kernel_v0_1 import build_initial_observe_state
        from runtime.kuuos_verify_os_kernel_v0_1 import build_initial_verify_state
        from runtime.kuuos_learn_os_kernel_v0_1 import build_initial_learn_state

        with TemporaryDirectory(prefix="kuuos-lean-python-real-") as folder:
            root = Path(folder)
            act = source_act_state(root / "edge-act")
            observe = build_initial_observe_state(
                observe_id="lean-python-real-observe", act_state=act, now_ms=100_000,
            )
            outcome = audit_handoff("ActOS", "ObserveOS", act, observe)
            self.assertEqual(outcome.status, PASSED, outcome.issues)

            observed = source_observe_state(root / "edge-observe", verdict="MATCHED")
            verify = build_initial_verify_state(
                verify_id="lean-python-real-verify", observe_state=observed, now_ms=110_000,
            )
            outcome = audit_handoff("ObserveOS", "VerifyOS", observed, verify)
            self.assertEqual(outcome.status, PASSED, outcome.issues)

            verified = source_verify_state(root / "edge-verify", verdict="PASSED")
            learn = build_initial_learn_state(
                learn_id="lean-python-real-learn", verify_state=verified, now_ms=200_000,
            )
            outcome = audit_handoff("VerifyOS", "LearnOS", verified, learn)
            self.assertEqual(outcome.status, PASSED, outcome.issues)


if __name__ == "__main__":
    main()
