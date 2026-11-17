"""Pure boundary tests. Fixtures are synthetic, not native kernel receipts."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import math
import unittest
from unittest.mock import patch

MODULE = 'runtime.kuuos_lean_python_plan_act_admission_v0_4'


def digest(packet, field):
    return hashlib.sha256(json.dumps(
        {k: v for k, v in packet.items() if k != field}, ensure_ascii=False,
        sort_keys=True, separators=(',', ':'), allow_nan=False,
    ).encode()).hexdigest()


def seal(packet, field):
    packet[field] = digest(packet, field)
    return packet


PLAN_NON_AUTHORITY = dict.fromkeys((
    'truth_authority_granted', 'execution_authority_granted',
    'proof_authority_granted', 'clinical_authority_granted',
    'institutional_authority_granted', 'legal_authority_granted',
    'host_license_granted', 'memory_overwrite_authority_granted',
    'tool_authority_granted', 'network_authority_granted', 'shell_authority_granted',
), False)
ACT_NON_AUTHORITY = dict.fromkeys((
    'truth_authority_granted', 'final_commitment_authority_granted',
    'memory_overwrite_authority_granted', 'clinical_authority_granted',
    'legal_authority_granted', 'institutional_authority_granted',
    'theorem_authority_granted', 'unrestricted_tool_authority_granted',
    'unrestricted_shell_authority_granted', 'unrestricted_network_authority_granted',
), False)
PLAN_BOUNDARY = dict.fromkeys((
    'plan_is_structured_proposal', 'plan_is_not_decision', 'plan_is_not_execution',
    'plan_is_not_host_license', 'source_wa_state_is_read_only',
    'source_option_identity_preserved', 'stakeholder_veto_appeal_history_preserved',
    'dependency_dag_required', 'resource_bounds_required',
    'rollback_or_escalation_required', 'observation_checkpoint_required',
    'activation_requires_plan_phase',
), True)
ACT_BOUNDARY = dict.fromkeys((
    'plan_activation_is_not_execution_authority', 'explicit_act_phase_receipt_required',
    'exact_act_candidate_step_required', 'explicit_step_authorization_required',
    'valid_v017_host_license_required', 'exact_v017_projection_required',
    'one_host_invocation_at_most', 'one_job_per_invocation',
    'one_bounded_slice_per_invocation', 'lower_host_receipt_is_canonical',
    'duplicate_invocation_idempotent', 'observation_debt_preserved',
    'verification_debt_preserved', 'lower_authority_preserved',
), True)


def fixture():
    # A link-only fixture deliberately does not pretend to be a complete PlanOS
    # state. Full validity remains the existing validator's responsibility.
    plan = {
        'version': 'kuuos_plan_os_state_v0_1', 'plan_id': 'plan-a',
        'lineage_id': 'lineage-a', 'mission_contract_digest': 'mission-a',
        'current_phase': 'commit', 'route': 'PLAN_CANDIDATE',
        'pending_plan_phase_activation': True, 'updated_at_ms': 100,
        'latest_committed_plan_digest': 'committed-a', 'plan_basis_digest': 'basis-a',
        'source_wa_basis_digest': 'wa-basis-a', 'replan_activation_receipt_digest': 'replan-a',
        'next_plan_basis_digest': 'next-basis-a',
        'topological_order': ['prepare', 'act'],
        'steps': [
            {'step_id': 'prepare', 'step_digest': 'step-prepare'},
            {'step_id': 'act', 'step_digest': 'step-act'},
        ],
        'non_authority': copy.deepcopy(PLAN_NON_AUTHORITY),
        'boundary': copy.deepcopy(PLAN_BOUNDARY),
    }
    seal(plan, 'plan_state_digest')
    receipt = {
        'version': 'kuuos_plan_os_activation_receipt_v0_1',
        'plan_id': plan['plan_id'], 'lineage_id': plan['lineage_id'],
        'plan_state_digest': plan['plan_state_digest'],
        'committed_plan_digest': plan['latest_committed_plan_digest'],
        'plan_basis_digest': plan['plan_basis_digest'],
        'source_wa_basis_digest': plan['source_wa_basis_digest'],
        'route': plan['route'], 'topological_order': list(plan['topological_order']),
        'mission_cycle_phase': 'plan', 'mission_cycle_state_digest': 'cycle-a',
        'plan_phase_receipt_digest': 'plan-phase-a',
        'replan_activation_receipt_digest': plan['replan_activation_receipt_digest'],
        'next_plan_basis_digest': plan['next_plan_basis_digest'],
        'future_only': True, 'memory_overwrite': False,
        'plan_not_execution': True, 'host_license_granted': False,
        'non_authority': copy.deepcopy(PLAN_NON_AUTHORITY), 'created_at_ms': 110,
    }
    seal(receipt, 'plan_activation_receipt_digest')
    act = {
        'version': 'kuuos_act_os_state_v0_1', 'act_id': 'act-a',
        'lineage_id': plan['lineage_id'], 'source_plan_id': plan['plan_id'],
        'source_plan_state_digest': plan['plan_state_digest'],
        'source_committed_plan_digest': plan['latest_committed_plan_digest'],
        'source_plan_basis_digest': plan['plan_basis_digest'],
        'source_wa_basis_digest': plan['source_wa_basis_digest'],
        'mission_contract_digest': plan['mission_contract_digest'],
        'plan_activation_receipt_digest': receipt['plan_activation_receipt_digest'],
        'current_phase': 'bind', 'route': 'PENDING',
        'event_index': 0, 'act_version': 0, 'committed_records': 0,
        'updated_at_ms': 120, 'non_authority': copy.deepcopy(ACT_NON_AUTHORITY),
        'boundary': copy.deepcopy(ACT_BOUNDARY),
    }
    for k in (
        'predecessor_act_state_digest', 'selected_step_id', 'selected_step_digest',
        'operation_id', 'operation_input_digest', 'step_authorization_digest',
        'host_license_digest', 'host_projection_digest', 'host_tick_digest',
        'host_receipt_digest', 'host_invocation_digest', 'source_supervisor_bundle_digest',
        'result_supervisor_bundle_digest', 'expected_observation_digest',
        'verification_criterion_digest',
    ):
        act[k] = ''
    for k in ('selected_step', 'step_authorization', 'host_license',
              'host_projection', 'host_tick', 'host_receipt'):
        act[k] = {}
    for k in ('completed_step_ids', 'blockers', 'processed_event_digests',
              'event_history', 'record_summaries'):
        act[k] = []
    for k in ('effect_recorded', 'observation_required', 'verification_required',
              'automatic_truth_promotion', 'automatic_plan_completion',
              'automatic_rollback'):
        act[k] = False
    seal(act, 'act_state_digest')
    return plan, receipt, act


def reseal_all(p, r, a):
    seal(p, 'plan_state_digest')
    r['plan_state_digest'] = p['plan_state_digest']
    seal(r, 'plan_activation_receipt_digest')
    a['source_plan_state_digest'] = p['plan_state_digest']
    a['plan_activation_receipt_digest'] = r['plan_activation_receipt_digest']
    seal(a, 'act_state_digest')


class AvailabilityTests(unittest.TestCase):
    def test_admission_auditor_is_implemented(self):
        self.assertIsNotNone(importlib.util.find_spec(MODULE),
                             'v0.4 admission implementation is missing')


class AdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = __import__(MODULE, fromlist=['inspect_plan_act_admission'])

    def inspect(self, values):
        return self.m.inspect_plan_act_admission(*values)

    def assert_status(self, values, expected):
        result = self.inspect(values)
        self.assertEqual(result.status, expected, result)
        self.assertFalse(result.execution_authority_granted)
        self.assertFalse(result.formal_certified)
        self.assertFalse(result.external_phase_receipt_authenticated)
        return result

    def test_exact_links_do_not_claim_native_validation(self):
        result = self.assert_status(fixture(), 'LINKS_MATCH')
        self.assertFalse(result.runtime_checked)

    def test_callers_are_unchanged_and_audit_is_deterministic(self):
        data = fixture()
        before = copy.deepcopy(data)
        self.assertEqual(self.inspect(data), self.inspect(data))
        self.assertEqual(data, before)

    def test_every_source_identity_substitution_blocks_after_reseal(self):
        for field in (
            'source_plan_id', 'source_plan_state_digest', 'source_committed_plan_digest',
            'source_plan_basis_digest', 'source_wa_basis_digest',
            'lineage_id', 'mission_contract_digest', 'plan_activation_receipt_digest',
        ):
            with self.subTest(field=field):
                p, r, a = fixture()
                a[field] = 'substituted'
                seal(a, 'act_state_digest')
                self.assert_status((p, r, a), 'BLOCKED')

    def test_every_receipt_identity_substitution_blocks_after_reseal(self):
        for field in ('plan_id', 'lineage_id', 'committed_plan_digest',
                      'plan_basis_digest', 'source_wa_basis_digest',
                      'replan_activation_receipt_digest', 'next_plan_basis_digest'):
            with self.subTest(field=field):
                p, r, a = fixture()
                r[field] = 'substituted'
                reseal_all(p, r, a)
                self.assert_status((p, r, a), 'BLOCKED')

    def test_missing_input_is_no_data(self):
        for i in range(3):
            data = list(fixture())
            data[i] = None
            self.assert_status(data, 'NO_DATA')

    def test_missing_required_identity_never_passes(self):
        p, r, a = fixture()
        del a['source_plan_id']
        seal(a, 'act_state_digest')
        self.assert_status((p, r, a), 'NO_DATA')

    def test_missing_evidence_keeps_observed_contradictions(self):
        p, r, a = fixture()
        del r['plan_phase_receipt_digest']
        a['source_plan_id'] = 'wrong'
        reseal_all(p, r, a)
        result = self.assert_status((p, r, a), 'BLOCKED')
        self.assertTrue(result.missing)
        self.assertTrue(result.violations)

    def test_missing_packet_does_not_hide_other_packet_authority(self):
        p, r, a = fixture()
        p['non_authority']['execution_authority_granted'] = True
        seal(p, 'plan_state_digest')
        self.assert_status((p, None, None), 'BLOCKED')

    def test_source_must_be_committed_pending_candidate(self):
        for field, value in (('current_phase', 'verify'), ('route', 'HOLD'),
                             ('pending_plan_phase_activation', False)):
            with self.subTest(field=field):
                p, r, a = fixture()
                p[field] = value
                reseal_all(p, r, a)
                self.assert_status((p, r, a), 'BLOCKED')

    def test_advanced_act_snapshot_is_out_of_scope(self):
        p, r, a = fixture()
        a['current_phase'] = 'authorize'
        a['event_index'] = 2
        seal(a, 'act_state_digest')
        result = self.assert_status((p, r, a), 'NO_DATA')
        self.assertIn('act:initial_bind_snapshot_required', result.missing)

    def test_unknown_act_phase_is_blocked(self):
        p, r, a = fixture()
        a['current_phase'] = 'invented'
        seal(a, 'act_state_digest')
        self.assert_status((p, r, a), 'BLOCKED')

    def test_receipt_flags_cannot_be_escalated_or_type_aliased(self):
        for field, bad in (('future_only', False), ('memory_overwrite', True),
                           ('plan_not_execution', False), ('host_license_granted', True),
                           ('future_only', 1), ('host_license_granted', 0)):
            with self.subTest(field=field, bad=bad):
                p, r, a = fixture()
                r[field] = bad
                reseal_all(p, r, a)
                self.assert_status((p, r, a), 'BLOCKED')

    def test_receipt_requires_plan_phase(self):
        p, r, a = fixture()
        r['mission_cycle_phase'] = 'act'
        reseal_all(p, r, a)
        self.assert_status((p, r, a), 'BLOCKED')

    def test_time_order_is_nondecreasing(self):
        for packet, field, value in ((1, 'created_at_ms', 99), (2, 'updated_at_ms', 109)):
            data = fixture()
            data[packet][field] = value
            reseal_all(*data)
            self.assert_status(data, 'BLOCKED')
        p, r, a = fixture()
        r['created_at_ms'] = a['updated_at_ms'] = p['updated_at_ms']
        reseal_all(p, r, a)
        self.assert_status((p, r, a), 'LINKS_MATCH')

    def test_natural_numbers_do_not_accept_bool_float_string_or_negative(self):
        for packet, field in ((0, 'updated_at_ms'), (1, 'created_at_ms'),
                              (2, 'updated_at_ms'), (2, 'event_index')):
            for bad in (True, 1.0, '1', -1):
                with self.subTest(packet=packet, field=field, bad=bad):
                    data = fixture()
                    data[packet][field] = bad
                    reseal_all(*data)
                    self.assert_status(data, 'BLOCKED')

    def test_step_order_cannot_be_swapped(self):
        p, r, a = fixture()
        r['topological_order'].reverse()
        reseal_all(p, r, a)
        self.assert_status((p, r, a), 'BLOCKED')

    def test_invented_step_digest_extension_is_not_native_receipt(self):
        p, r, a = fixture()
        r['step_digests'] = [x['step_digest'] for x in p['steps']]
        reseal_all(p, r, a)
        self.assert_status((p, r, a), 'BLOCKED')

    def test_step_and_topological_identifiers_must_be_unique_and_exact(self):
        for mutation in ('duplicate_step', 'duplicate_order', 'unknown_order'):
            p, r, a = fixture()
            if mutation == 'duplicate_step':
                p['steps'].append(copy.deepcopy(p['steps'][0]))
            elif mutation == 'duplicate_order':
                p['topological_order'].append('prepare')
            else:
                p['topological_order'][0] = 'unknown'
            r['topological_order'] = list(p['topological_order'])
            reseal_all(p, r, a)
            self.assert_status((p, r, a), 'BLOCKED')

    def test_empty_or_nontext_external_references_are_not_evidence(self):
        for field in ('plan_phase_receipt_digest', 'mission_cycle_state_digest'):
            for bad in ('', '  ', None, 0):
                p, r, a = fixture()
                r[field] = bad
                reseal_all(p, r, a)
                self.assertNotIn(self.inspect((p, r, a)).status, ('PASS', 'LINKS_MATCH'))

    def test_all_no_authority_flags_are_strictly_false(self):
        for index in range(3):
            for field in fixture()[index]['non_authority']:
                data = fixture()
                data[index]['non_authority'][field] = True
                reseal_all(*data)
                self.assert_status(data, 'BLOCKED')

    def test_authority_numeric_alias_and_new_authority_flag_are_blocked(self):
        for index in range(3):
            data = fixture()
            first = next(iter(data[index]['non_authority']))
            data[index]['non_authority'][first] = 0
            reseal_all(*data)
            self.assert_status(data, 'BLOCKED')
            data = fixture()
            data[index]['non_authority']['new_permission'] = True
            reseal_all(*data)
            self.assert_status(data, 'BLOCKED')

    def test_boundary_mutation_and_alias_are_blocked(self):
        for index in (0, 2):
            for bad in (False, 1):
                data = fixture()
                first = next(iter(data[index]['boundary']))
                data[index]['boundary'][first] = bad
                reseal_all(*data)
                self.assert_status(data, 'BLOCKED')

    def test_bind_state_cannot_contain_an_effect_or_authorization(self):
        for field, bad in (
            ('effect_recorded', True), ('observation_required', True),
            ('verification_required', True), ('automatic_truth_promotion', True),
            ('automatic_plan_completion', True), ('automatic_rollback', True),
            ('step_authorization', {'license': 'fake'}), ('host_license', {'x': 1}),
            ('host_invocation_digest', 'invoked'), ('processed_event_digests', ['e']),
            ('event_history', [{}]), ('committed_records', 1), ('route', 'EFFECT_RECORDED'),
        ):
            with self.subTest(field=field):
                p, r, a = fixture()
                a[field] = bad
                seal(a, 'act_state_digest')
                self.assert_status((p, r, a), 'BLOCKED')

    def test_hash_mismatch_is_not_identity(self):
        for index, field in ((0, 'plan_state_digest'), (1, 'plan_activation_receipt_digest'),
                              (2, 'act_state_digest')):
            data = fixture()
            data[index][field] = '0' * 64
            self.assert_status(data, 'BLOCKED')

    def test_non_json_and_nonfinite_inputs_fail_closed(self):
        for bad in (float('nan'), float('inf'), object(), {1: 'bad-key'}, (1, 2)):
            p, r, a = fixture()
            p['extra'] = bad
            self.assert_status((p, r, a), 'BLOCKED')

    def test_cyclic_data_is_blocked(self):
        p, r, a = fixture()
        p['cycle'] = p
        self.assert_status((p, r, a), 'BLOCKED')

    def test_receipt_and_act_unknown_fields_fail_closed(self):
        for index in (1, 2):
            data = fixture()
            data[index]['execute_now'] = True
            reseal_all(*data)
            self.assert_status(data, 'BLOCKED')

    def test_runtime_missing_is_no_data_not_pass(self):
        with patch(self.m.__name__ + '.import_module', side_effect=ModuleNotFoundError('missing')):
            result = self.m.audit_plan_act_admission(*fixture())
        self.assertEqual(result.status, 'NO_DATA')
        self.assertFalse(result.runtime_checked)

    def test_runtime_errors_malformed_return_and_mutation_block(self):
        from types import SimpleNamespace
        def mutation(state):
            state['changed'] = True
            return []
        def error(state):
            raise ValueError('bad input')
        for validator in (lambda state: ['invalid'], lambda state: None,
                          lambda state: (), lambda state: [1], mutation, error):
            fake = SimpleNamespace(validate_plan_state=validator, validate_act_state=validator)
            data = fixture()
            before = copy.deepcopy(data)
            with patch(self.m.__name__ + '.import_module', return_value=fake):
                result = self.m.audit_plan_act_admission(*data)
            self.assertEqual(result.status, 'BLOCKED', result)
            self.assertEqual(data, before)

    def test_adapter_calls_both_original_module_names_on_isolated_copies(self):
        from types import SimpleNamespace
        calls = []
        def validator(state):
            calls.append(state['version'])
            return []
        fake = SimpleNamespace(validate_plan_state=validator, validate_act_state=validator)
        with patch(self.m.__name__ + '.import_module', return_value=fake) as loader:
            result = self.m.audit_plan_act_admission(*fixture())
        self.assertEqual(result.status, 'PASS')
        self.assertTrue(result.runtime_checked)
        self.assertEqual(calls, ['kuuos_plan_os_state_v0_1', 'kuuos_act_os_state_v0_1'])
        self.assertEqual([c.args[0] for c in loader.call_args_list], [
            'runtime.kuuos_plan_os_state_v0_1', 'runtime.kuuos_act_os_kernel_v0_1'])
        # This test covers adapter mechanics with explicit test doubles, not
        # native integration. The separate native suite must run in a checkout.

    def test_rejected_links_never_call_native_validators(self):
        data = fixture()
        data[1]['host_license_granted'] = True
        with patch(self.m.__name__ + '.import_module') as loader:
            result = self.m.audit_plan_act_admission(*data)
        self.assertEqual(result.status, 'BLOCKED')
        loader.assert_not_called()


    def test_large_integer_cannot_escape_fail_closed_json_boundary(self):
        p, r, a = fixture()
        r['future_only'] = 10 ** 5000
        self.assert_status((p, r, a), 'BLOCKED')

    def test_invalid_utf8_and_excessively_deep_json_block(self):
        p, r, a = fixture()
        p['bad_text'] = chr(0xD800)
        self.assert_status((p, r, a), 'BLOCKED')
        p, r, a = fixture()
        value = []
        for _ in range(70):
            value = [value]
        p['deep'] = value
        self.assert_status((p, r, a), 'BLOCKED')

    def test_custom_dict_and_nonobject_top_level_are_not_executed(self):
        class Unsafe(dict):
            def items(self):
                raise AssertionError('custom mapping hook must not execute')
        for value in ([], 1, False, Unsafe()):
            p, r, a = fixture()
            self.assert_status((value, r, a), 'BLOCKED')

    def test_broken_native_import_is_blocked_not_an_uncaught_exception(self):
        with patch(self.m.__name__ + '.import_module', side_effect=SyntaxError('bad module')):
            result = self.m.audit_plan_act_admission(*fixture())
        self.assertEqual(result.status, 'BLOCKED')
        self.assertFalse(result.runtime_checked)

    def test_result_is_bound_to_actual_supplied_snapshots(self):
        data = fixture()
        result = self.inspect(data)
        expected = tuple((name, hashlib.sha256(json.dumps(packet, ensure_ascii=False,
                          sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest())
                         for name, packet in zip(('plan', 'receipt', 'act'), data))
        self.assertEqual(result.input_sha256, expected)
        self.assertEqual(result.source_reference_commit, self.m.SOURCE_COMMIT)
        altered = fixture()
        altered[2]['updated_at_ms'] += 1
        seal(altered[2], 'act_state_digest')
        other = self.inspect(altered)
        self.assertEqual(other.status, result.status)
        self.assertNotEqual(other.input_sha256, result.input_sha256)

    def test_result_is_immutable(self):
        from dataclasses import FrozenInstanceError
        result = self.inspect(fixture())
        with self.assertRaises(FrozenInstanceError):
            result.status = 'PASS'


if __name__ == '__main__':
    unittest.main()
