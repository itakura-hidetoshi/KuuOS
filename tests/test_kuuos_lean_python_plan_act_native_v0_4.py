"""Mandatory repository integration tests; missing native modules are NOT skipped.

Only the host-invocation function is intercepted as a forbidden-effect sentinel.
The state builders and both native validators are genuine repository functions.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime.kuuos_lean_python_plan_act_admission_v0_4 import (
    audit_plan_act_admission, inspect_plan_act_admission, RECEIPT_KEYS,
)


class NativePlanActTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from runtime.kuuos_act_os_fixture_v0_1 import source_plan
            from runtime.kuuos_act_os_kernel_v0_1 import (
                build_initial_act_state, validate_act_state,
            )
            from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state
            from runtime.kuuos_plan_os_types_v0_1 import plan_activation_receipt_digest
            from runtime.kuuos_act_os_types_v0_1 import state_digest
        except ImportError as exc:
            raise RuntimeError(
                'NO_DATA: genuine repository modules unavailable; native suite '
                'was not run. A unit-only run is not a green repository suite.'
            ) from exc
        cls.build_act = staticmethod(build_initial_act_state)
        cls.validate_plan = staticmethod(validate_plan_state)
        cls.validate_act = staticmethod(validate_act_state)
        cls.receipt_hash = staticmethod(plan_activation_receipt_digest)
        cls.act_hash = staticmethod(state_digest)
        with TemporaryDirectory(prefix='kuuos-v04-native-') as directory:
            with patch('runtime.kuuos_act_os_kernel_v0_1.run_host_tick',
                       side_effect=AssertionError('admission audit must not invoke host')) as host:
                cls.plan, cls.receipt = source_plan(Path(directory))
                cls.act = cls.build_act(
                    act_id='v04-native-admission', plan_state=cls.plan,
                    plan_activation_receipt=cls.receipt, now_ms=90_000,
                )
                host.assert_not_called()
        if cls.validate_plan(cls.plan) or cls.validate_act(cls.act):
            raise AssertionError('native fixtures must pass original validators')

    def setUp(self):
        self.p, self.r, self.a = deepcopy((self.plan, self.receipt, self.act))

    def reseal_receipt_and_act(self):
        self.r['plan_activation_receipt_digest'] = self.receipt_hash(self.r)
        self.a['plan_activation_receipt_digest'] = self.r['plan_activation_receipt_digest']
        self.a['act_state_digest'] = self.act_hash(self.a)

    def test_real_constructors_and_validators_pass_without_invocation_or_mutation(self):
        before = deepcopy((self.p, self.r, self.a))
        with patch('runtime.kuuos_act_os_kernel_v0_1.run_host_tick',
                   side_effect=AssertionError('unexpected effect')) as host:
            result = audit_plan_act_admission(self.p, self.r, self.a)
            host.assert_not_called()
        self.assertEqual(result.status, 'PASS', result)
        self.assertTrue(result.runtime_checked)
        self.assertFalse(result.execution_authority_granted)
        self.assertEqual((self.p, self.r, self.a), before)

    def test_resealed_receipt_cannot_substitute_source_identifiers(self):
        for key in ('plan_id', 'lineage_id', 'source_wa_basis_digest',
                    'replan_activation_receipt_digest', 'next_plan_basis_digest'):
            with self.subTest(key=key):
                self.setUp()
                self.r[key] = 'substituted-source'
                self.reseal_receipt_and_act()
                self.assertEqual(audit_plan_act_admission(self.p, self.r, self.a).status, 'BLOCKED')

    def test_resealed_receipt_cannot_change_topological_order(self):
        self.r['topological_order'] = list(reversed(self.r['topological_order']))
        self.reseal_receipt_and_act()
        self.assertEqual(audit_plan_act_admission(self.p, self.r, self.a).status, 'BLOCKED')

    def test_resealed_clock_regressions_block(self):
        self.r['created_at_ms'] = self.p['updated_at_ms'] - 1
        self.reseal_receipt_and_act()
        self.assertEqual(audit_plan_act_admission(self.p, self.r, self.a).status, 'BLOCKED')

    def test_initial_act_cannot_preclaim_an_effect(self):
        self.a['effect_recorded'] = True
        self.a['act_state_digest'] = self.act_hash(self.a)
        self.assertEqual(audit_plan_act_admission(self.p, self.r, self.a).status, 'BLOCKED')

    def test_actual_constructor_schema_matches_exact_audit_schema(self):
        self.assertEqual(set(self.r), RECEIPT_KEYS)
        self.assertIn('replan_activation_receipt_digest', self.r)
        self.assertNotIn('step_digests', self.r)

    def test_missing_receipt_remains_no_data(self):
        result = inspect_plan_act_admission(self.p, None, self.a)
        self.assertEqual(result.status, 'NO_DATA', result)
        self.assertFalse(result.runtime_checked)


# v0.12 adds ordinary discovery for additive Lean/Python extension tests.
def load_tests(loader, tests, pattern):
    from tests.lean_python_extensions import load_extension_tests

    tests.addTests(load_extension_tests(loader))
    return tests


if __name__ == '__main__':
    unittest.main()
