"""Unit contracts use stubs; RealKernelTests below never replace validators."""
from __future__ import annotations

from copy import deepcopy
from importlib import import_module
import hashlib
import json
import sys
from types import ModuleType
from unittest import TestCase, main
from unittest.mock import patch

MODULE = 'runtime.kuuos_lean_python_decision_plan_handoff_v0_3'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class ContractTests(TestCase):
    def setUp(self):
        try:
            self.bridge = import_module(MODULE)
        except ModuleNotFoundError:
            self.fail('v0.3 decision/plural/wa/plan handoff implementation is missing')

    def modules(self):
        modules = {}
        for node, spec in self.bridge.STATE_SPECS.items():
            types = modules.setdefault(spec.types_module, ModuleType(spec.types_module))
            types.STATE_VERSION = node + '-state'
            types.PHASES = ('bind', 'commit')
            setattr(types, spec.authority_constant, {'execution_authority_granted': False})
            setattr(types, spec.boundary_constant, {'read_only': True})
            kernel = modules.setdefault(spec.validator_module, ModuleType(spec.validator_module))
            setattr(kernel, spec.validator_name, lambda state: [])
        wa_types = modules[self.bridge.STATE_SPECS['DecisionOSWa'].types_module]
        wa_types.ACTIVATION_RECEIPT_VERSION = 'wa-activation'
        wa_types.wa_activation_receipt_digest = lambda value: digest({k: v for k, v in value.items() if k != 'wa_activation_receipt_digest'})
        plan_types = modules[self.bridge.STATE_SPECS['PlanOS'].types_module]
        plan_types.SOURCE_ROUTE_MAP = {'ENDORSE': 'PLAN_CANDIDATE', 'HOLD': 'HOLD'}
        hashing = ModuleType('runtime.kuuos_belief_os_types_v0_1')
        hashing.sha = digest
        modules[hashing.__name__] = hashing
        return modules

    def fixture(self):
        b = self.bridge
        states = {}
        for index, (node, spec) in enumerate(b.STATE_SPECS.items()):
            states[node] = {
                'version': node + '-state', 'current_phase': 'commit',
                'route': 'ENDORSE' if node == 'DecisionOSWa' else 'HOLD',
                'lineage_id': 'same-lineage', 'mission_contract_digest': 'same-mission',
                'updated_at_ms': 100 + index * 100, 'event_index': 0,
                'event_history': [], 'processed_event_digests': [],
                'non_authority': {'execution_authority_granted': False},
                'boundary': {'read_only': True}, spec.digest_key: node + '-digest',
            }
        d, p, w, plan = (states[node] for node in b.CHAIN)
        d.update(admissible_option_ids=['a', 'b'], selected_option_id='',
                 options=[{'option_id': 'a', 'option_digest': 'a-digest', 'score': 0.2},
                          {'option_id': 'b', 'option_digest': 'b-digest', 'score': 0.1},
                          {'option_id': 'excluded', 'option_digest': 'x-digest', 'score': 1.0}])
        p.update(plural_id='plural', selected_option_id='a', retained_alternative_ids=['b'],
                 utility_records=[{'value': 2}], veto_records=[{'veto': 'veto-evidence'}],
                 aggregate_records=[{'sum': 3}], appeal_history=[{'appeal': 'appeal-evidence'}],
                 stakeholder_registry_digest='stakeholders')
        w.update(wa_id='wa', pending_replan_activation=True, endorsed_option_ids=['a'], review_option_ids=[])
        for edge, spec in b.EDGE_SPECS.items():
            src, tgt = states[edge[0]], states[edge[1]]
            for left, right in spec.equal_fields:
                if left not in src:
                    src[left] = left + '-value'
                tgt[right] = deepcopy(src[left])
            if edge[0] == 'DecisionOS':
                tgt['source_options'] = deepcopy(d['options'][:2])
                tgt['source_options_digest'] = digest(tgt['source_options'])
            if edge[0] == 'DecisionOSPlural':
                tgt['source_option_digest_by_id'] = {o['option_id']: o['option_digest'] for o in p['source_options']}
                for left, right in b.PLURAL_HASH_FIELDS:
                    tgt[right] = digest(src[left])
        plan['route'] = 'PLAN_CANDIDATE'
        receipt = {
            'version': 'wa-activation', 'mission_cycle_phase': 'replan',
            'future_only': True, 'memory_overwrite': False, 'wa_not_truth': True,
            'wa_not_execution': True, 'wa_not_moral_veto': True, 'host_license_granted': False,
            'non_authority': {'execution_authority_granted': False},
            'created_at_ms': 350, 'mission_cycle_state_digest': 'replan-state',
            'replan_receipt_digest': 'replan-evidence', 'next_plan_basis_digest': 'next-plan',
        }
        for left, right in b.WA_RECEIPT_FIELDS:
            receipt[right] = deepcopy(w[left])
        receipt['wa_activation_receipt_digest'] = digest(receipt)
        for left, right in b.RECEIPT_PLAN_FIELDS:
            plan[right] = deepcopy(receipt[left])
        return states, receipt

    def run_edge(self, edge, states, receipt):
        return self.bridge.audit_decision_plan_edge(*edge, states[edge[0]], states[edge[1]], replan_activation_receipt=receipt)

    def test_three_real_edges_and_complete_chain_are_read_only(self):
        b = self.bridge
        self.assertEqual(tuple(b.EDGE_SPECS), tuple(zip(b.CHAIN, b.CHAIN[1:])))
        with patch.dict(sys.modules, self.modules()):
            states, receipt = self.fixture()
            before = deepcopy((states, receipt))
            for edge in b.EDGE_SPECS:
                outcome = self.run_edge(edge, states, receipt)
                self.assertEqual(outcome.status, b.PASSED, outcome.issues)
            result = b.audit_decision_plan_chain(states, replan_activation_receipt=receipt)
            self.assertEqual(result.status, b.PASSED, result.issues)
            self.assertEqual(len(result.edges), 3)
            self.assertEqual((states, receipt), before)
            self.assertFalse(result.execution_authority_granted)
            self.assertFalse(result.lean_python_refinement_proved)

    def test_every_direct_binding_substitution_is_blocked(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            for edge, spec in b.EDGE_SPECS.items():
                for _, right in spec.equal_fields:
                    with self.subTest(edge=edge, field=right):
                        states, receipt = self.fixture()
                        states[edge[1]][right] = 'substituted'
                        self.assertEqual(self.run_edge(edge, states, receipt).status, b.BLOCKED)

    def test_missing_each_binding_is_never_promoted(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            for edge, spec in b.EDGE_SPECS.items():
                for _, right in spec.equal_fields:
                    states, receipt = self.fixture()
                    states[edge[1]].pop(right)
                    self.assertEqual(self.run_edge(edge, states, receipt).status, b.NO_DATA, (edge, right))

    def test_missing_intermediate_and_direct_shortcut_remain_no_data(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            states, receipt = self.fixture()
            for name in ('DecisionOSPlural', 'DecisionOSWa'):
                incomplete = deepcopy(states)
                incomplete.pop(name)
                self.assertEqual(b.audit_decision_plan_chain(incomplete, replan_activation_receipt=receipt).status, b.NO_DATA)
            self.assertEqual(b.audit_decision_plan_edge('DecisionOS', 'PlanOS', states['DecisionOS'], states['PlanOS']).status, b.NO_DATA)

    def test_admissible_projection_cannot_smuggle_or_reorder_candidates(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            for change in ('excluded', 'reverse', 'alter'):
                states, receipt = self.fixture()
                p = states['DecisionOSPlural']
                if change == 'excluded': p['source_options'].append(states['DecisionOS']['options'][-1])
                elif change == 'reverse': p['source_options'].reverse()
                else: p['source_options'][0]['score'] = 9
                p['source_options_digest'] = digest(p['source_options'])
                self.assertEqual(self.run_edge(b.CHAIN[:2], states, receipt).status, b.BLOCKED)

    def test_duplicate_candidate_id_is_blocked(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            states, receipt = self.fixture()
            states['DecisionOS']['options'].append(deepcopy(states['DecisionOS']['options'][0]))
            self.assertEqual(self.run_edge(b.CHAIN[:2], states, receipt).status, b.BLOCKED)

    def test_rehashed_veto_appeal_and_utility_replacement_is_blocked(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            for _, field in b.PLURAL_HASH_FIELDS:
                states, receipt = self.fixture()
                states['DecisionOSWa'][field] = digest([])
                self.assertEqual(self.run_edge(b.CHAIN[1:3], states, receipt).status, b.BLOCKED)
            states, receipt = self.fixture()
            states['DecisionOSWa']['source_option_digest_by_id']['a'] = 'other'
            self.assertEqual(self.run_edge(b.CHAIN[1:3], states, receipt).status, b.BLOCKED)

    def test_source_must_be_committed_and_time_cannot_regress(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            for edge in b.EDGE_SPECS:
                states, receipt = self.fixture()
                states[edge[0]]['current_phase'] = 'bind'
                self.assertEqual(self.run_edge(edge, states, receipt).status, b.BLOCKED)
                states, receipt = self.fixture()
                states[edge[1]]['updated_at_ms'] = 1
                self.assertEqual(self.run_edge(edge, states, receipt).status, b.BLOCKED)

    def test_required_receipt_and_all_receipt_bindings(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            states, receipt = self.fixture()
            self.assertEqual(self.run_edge(b.CHAIN[2:], states, None).status, b.NO_DATA)
            for _, field in b.WA_RECEIPT_FIELDS:
                states, receipt = self.fixture()
                receipt[field] = 'substituted'
                receipt['wa_activation_receipt_digest'] = digest({k:v for k,v in receipt.items() if k!='wa_activation_receipt_digest'})
                self.assertEqual(self.run_edge(b.CHAIN[2:], states, receipt).status, b.BLOCKED)
            for _, field in b.RECEIPT_PLAN_FIELDS:
                states, receipt = self.fixture()
                states['PlanOS'][field] = 'substituted'
                self.assertEqual(self.run_edge(b.CHAIN[2:], states, receipt).status, b.BLOCKED)

    def test_receipt_time_phase_authority_and_digest(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            mutations = {'created_at_ms': (True, 299, 401), 'mission_cycle_phase': ('act',),
                         'future_only': (False, 1), 'host_license_granted': (True, 0),
                         'memory_overwrite': (True,), 'wa_not_execution': (False,),
                         'wa_activation_receipt_digest': ('invalid',)}
            for field, values in mutations.items():
                for value in values:
                    states, receipt = self.fixture()
                    receipt[field] = value
                    self.assertEqual(self.run_edge(b.CHAIN[2:], states, receipt).status, b.BLOCKED, (field, value))

    def test_state_authority_and_bool_integer_alias_are_blocked(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            for node in b.CHAIN:
                states, receipt = self.fixture()
                states[node]['non_authority']['execution_authority_granted'] = 0
                self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=receipt).status, b.BLOCKED)
                states, receipt = self.fixture()
                states[node]['updated_at_ms'] = True
                self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=receipt).status, b.BLOCKED)
            states, receipt = self.fixture()
            states['DecisionOSPlural']['source_options'][0]['score'] = True
            states['DecisionOS']['options'][0]['score'] = 1
            self.assertEqual(self.run_edge(b.CHAIN[:2], states, receipt).status, b.BLOCKED)

    def test_missing_data_does_not_hide_observed_contradiction(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            states, receipt = self.fixture()
            states['PlanOS']['source_wa_state_digest'] = 'wrong'
            self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=None).status, b.BLOCKED)

    def test_validator_failure_exception_and_mutation_do_not_pass(self):
        b = self.bridge
        for mode in ('failed', 'raises', 'mutates', 'bad-result'):
            modules = self.modules()
            spec = b.STATE_SPECS['DecisionOSPlural']
            def validator(state):
                if mode == 'raises': raise ValueError('bad')
                if mode == 'mutates': state['source_options'][0]['score'] = 99
                if mode == 'failed': return ['invalid']
                if mode == 'bad-result': return None
                return []
            setattr(modules[spec.validator_module], spec.validator_name, validator)
            with patch.dict(sys.modules, modules):
                states, receipt = self.fixture()
                original = deepcopy(states)
                self.assertEqual(self.run_edge(b.CHAIN[:2], states, receipt).status, b.BLOCKED, mode)
                self.assertEqual(states, original)

    def test_dependency_unavailable_is_no_data(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            states, receipt = self.fixture()
            with patch.object(b, 'import_module', side_effect=ImportError('absent')):
                self.assertEqual(self.run_edge(b.CHAIN[:2], states, receipt).status, b.NO_DATA)

    def test_missing_identity_is_no_data_before_complete_schema_validation(self):
        b = self.bridge
        modules = self.modules()
        spec = b.STATE_SPECS['DecisionOSPlural']
        def require_source(state):
            return [] if 'source_decision_state_digest' in state else ['source_required']
        setattr(modules[spec.validator_module], spec.validator_name, require_source)
        with patch.dict(sys.modules, modules):
            states, receipt = self.fixture()
            states['DecisionOSPlural'].pop('source_decision_state_digest')
            result = self.run_edge(b.CHAIN[:2], states, receipt)
            self.assertEqual(result.status, b.NO_DATA, result.issues)

    def test_non_json_or_nonfinite_input_is_blocked(self):
        b = self.bridge
        with patch.dict(sys.modules, self.modules()):
            for value in (float('nan'), float('inf'), object()):
                states, receipt = self.fixture()
                states['DecisionOS']['bad'] = value
                self.assertEqual(self.run_edge(b.CHAIN[:2], states, receipt).status, b.BLOCKED)


class RealKernelTests(TestCase):
    """Actual original kernel/state constructors; no mocked validator or skip path."""
    @classmethod
    def setUpClass(cls):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
            _build_belief, _build_decision, _build_plural, _build_wa,
        )
        from runtime.kuuos_belief_os_types_v0_1 import sha
        from runtime.kuuos_decision_os_wa_kernel_v0_3 import build_replan_wa_activation_receipt
        from runtime.kuuos_plan_os_state_v0_1 import build_initial_plan_state
        cls.bridge = import_module(MODULE)
        cls.folder = TemporaryDirectory(prefix='kuuos-v03-real-')
        cls.addClassCleanup(cls.folder.cleanup)
        root = Path(cls.folder.name)
        lineage = 'v03-real-chain'
        _, belief = _build_belief(root / 'belief', lineage)
        decision = _build_decision(root / 'decision', lineage, sha('v03-mission'), belief)
        plural = _build_plural(root / 'plural', lineage, decision)
        wa = _build_wa(root / 'wa', plural)
        receipt = build_replan_wa_activation_receipt(
            state=wa, mission_cycle_phase='replan', mission_cycle_state_digest=sha('v03-replan-state'),
            replan_receipt_digest=sha('v03-replan'), next_plan_basis_digest=sha('v03-next-plan'), now_ms=50_000)
        plan = build_initial_plan_state(
            plan_id='v03-plan', source_wa_state=wa, replan_activation_receipt=receipt,
            plan_budget=2.0, maximum_step_risk=0.40, now_ms=60_000)
        cls.states = dict(zip(cls.bridge.CHAIN, (decision, plural, wa, plan)))
        cls.receipt = receipt
        # Deliberately stop before any ActOS or host invocation.

    def seal(self, node, state):
        spec = self.bridge.STATE_SPECS[node]
        types = import_module(spec.types_module)
        name = {'DecisionOSWa': 'wa_state_digest', 'PlanOS': 'plan_state_digest'}.get(node, 'state_digest')
        state[spec.digest_key] = getattr(types, name)(state)
        validator = getattr(import_module(spec.validator_module), spec.validator_name)
        self.assertEqual(validator(state), [], (node, 'original validator unexpectedly rejected fixture'))

    def test_actual_chain_builders_and_original_validators_pass_without_effect(self):
        b = self.bridge
        before = deepcopy((self.states, self.receipt))
        for name, state in self.states.items():
            spec = b.STATE_SPECS[name]
            self.assertEqual(getattr(import_module(spec.validator_module), spec.validator_name)(state), [])
        result = b.audit_decision_plan_chain(self.states, replan_activation_receipt=self.receipt)
        self.assertEqual(result.status, b.PASSED, result.issues)
        self.assertEqual(len(result.edges), 3)
        self.assertEqual((self.states, self.receipt), before)
        self.assertFalse(result.execution_authority_granted)

    def test_resealed_upstream_identity_substitution_is_rejected(self):
        b = self.bridge
        for node, key in (('DecisionOSPlural', 'source_decision_state_digest'),
                          ('DecisionOSWa', 'source_plural_state_digest'), ('PlanOS', 'source_wa_state_digest')):
            states = deepcopy(self.states)
            states[node][key] = 'f' * 64
            self.seal(node, states[node])
            result = b.audit_decision_plan_chain(states, replan_activation_receipt=self.receipt)
            self.assertEqual(result.status, b.BLOCKED, result.issues)

    def test_resealed_history_and_candidate_projection_tamper_is_rejected(self):
        from runtime.kuuos_belief_os_types_v0_1 import sha
        b = self.bridge
        for _, key in b.PLURAL_HASH_FIELDS:
            states = deepcopy(self.states)
            states['DecisionOSWa'][key] = sha(['substituted history'])
            self.seal('DecisionOSWa', states['DecisionOSWa'])
            self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=self.receipt).status, b.BLOCKED)
        states = deepcopy(self.states)
        plural = states['DecisionOSPlural']
        plural['source_options'][0]['option_digest'] = 'a' * 64
        plural['source_options_digest'] = sha(plural['source_options'])
        self.seal('DecisionOSPlural', plural)
        self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=self.receipt).status, b.BLOCKED)

    def test_resealed_receipt_cannot_replace_source_or_escalate_authority(self):
        from runtime.kuuos_decision_os_wa_types_v0_3 import wa_activation_receipt_digest
        b = self.bridge
        for field, value in (('wa_id', 'foreign-wa'), ('lineage_id', 'foreign-root'),
                             ('host_license_granted', True), ('future_only', 1), ('created_at_ms', 0)):
            states, receipt = deepcopy((self.states, self.receipt))
            receipt[field] = value
            receipt['wa_activation_receipt_digest'] = wa_activation_receipt_digest(receipt)
            states['PlanOS']['replan_activation_receipt_digest'] = receipt['wa_activation_receipt_digest']
            self.seal('PlanOS', states['PlanOS'])
            self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=receipt).status, b.BLOCKED, field)

    def test_missing_intermediates_receipt_and_observed_time_regression(self):
        b = self.bridge
        for name in ('DecisionOSPlural', 'DecisionOSWa'):
            states = deepcopy(self.states)
            states.pop(name)
            self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=self.receipt).status, b.NO_DATA)
        self.assertEqual(b.audit_decision_plan_chain(self.states).status, b.NO_DATA)
        states = deepcopy(self.states)
        states['PlanOS']['updated_at_ms'] = states['DecisionOSWa']['updated_at_ms'] - 1
        self.seal('PlanOS', states['PlanOS'])
        self.assertEqual(b.audit_decision_plan_chain(states, replan_activation_receipt=self.receipt).status, b.BLOCKED)

    def test_static_source_mapping_registration_and_drift_detection(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from scripts.check_kuuos_lean_python_decision_plan_bindings_v0_3 import check_bindings, required_paths
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(check_bindings(root), [])
        with TemporaryDirectory(prefix='kuuos-v03-drift-') as folder:
            target = Path(folder)
            for relative in required_paths():
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((root / relative).read_bytes())
            path = target / 'formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean'
            path.write_text(path.read_text().replace('theorem waPlurality_preserves_veto_appeal_history',
                                                     'theorem deliberately_removed_declaration'))
            errors = check_bindings(target)
            self.assertTrue(any('source_blob_changed:' in x for x in errors), errors)
            self.assertTrue(any('lean_declaration_missing:waPlurality_preserves_veto_appeal_history' in x for x in errors), errors)


if __name__ == '__main__':
    main()
