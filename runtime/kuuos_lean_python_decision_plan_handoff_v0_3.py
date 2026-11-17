"""Read-only Decision -> Plural -> Wa -> Plan lineage checks.

Lean references motivate named boundaries under their original hypotheses;
they do not prove this Python implementation or authenticate supplied evidence.
No kernel transition, receipt issuance, store write, or host invocation occurs.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from importlib import import_module
import math
from types import MappingProxyType
from typing import Any

from runtime.kuuos_lean_python_contract_bridge_v0_1 import BLOCKED, NO_DATA, PASSED

VERSION = 'kuuos_lean_python_decision_plan_handoff_v0_3'
SOURCE_COMMIT = '3879c5c286ff469dcbf21f18af08db853f76c827'
CHAIN = ('DecisionOS', 'DecisionOSPlural', 'DecisionOSWa', 'PlanOS')
_MISSING = object()


@dataclass(frozen=True)
class StateSpec:
    types_module: str
    validator_module: str
    validator_name: str
    digest_key: str
    authority_constant: str = 'NON_AUTHORITY_FLAGS'
    boundary_constant: str = 'REQUIRED_BOUNDARY'


STATE_SPECS = MappingProxyType({
    'DecisionOS': StateSpec('runtime.kuuos_decision_os_types_v0_1',
                           'runtime.kuuos_decision_os_state_v0_1', 'validate_decision_state', 'decision_state_digest'),
    'DecisionOSPlural': StateSpec('runtime.kuuos_decision_os_plural_types_v0_2',
                                 'runtime.kuuos_decision_os_plural_kernel_v0_2', 'validate_plural_state',
                                 'plural_state_digest', 'NON_AUTHORITY', 'BOUNDARY'),
    'DecisionOSWa': StateSpec('runtime.kuuos_decision_os_wa_types_v0_3',
                             'runtime.kuuos_decision_os_wa_state_v0_3', 'validate_wa_state', 'wa_state_digest'),
    'PlanOS': StateSpec('runtime.kuuos_plan_os_types_v0_1',
                       'runtime.kuuos_plan_os_state_v0_1', 'validate_plan_state', 'plan_state_digest'),
})


@dataclass(frozen=True)
class EdgeSpec:
    lean_source: str
    theorem_names: tuple[str, ...]
    constructor_source: str
    constructor_name: str
    equal_fields: tuple[tuple[str, str], ...]


_COMMON = (('lineage_id', 'lineage_id'), ('mission_contract_digest', 'mission_contract_digest'))
EDGE_SPECS = MappingProxyType({
    CHAIN[:2]: EdgeSpec(
        'formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean',
        ('pluralCommit_preserves_v01', 'pluralCommit_does_not_execute'),
        'runtime/kuuos_decision_os_plural_kernel_v0_2.py', 'build_initial_plural_state',
        _COMMON + (
            ('decision_state_digest', 'source_decision_state_digest'),
            ('decision_basis_digest', 'source_decision_basis_digest'),
            ('latest_committed_decision_digest', 'source_committed_decision_digest'),
            ('route', 'source_route'), ('selected_option_id', 'source_selected_option_id'),
            ('admissible_option_ids', 'source_option_ids'),
        )),
    CHAIN[1:3]: EdgeSpec(
        'formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean',
        ('waPlurality_preserves_veto_appeal_history', 'waPlurality_forbids_silent_substitution', 'wa_does_not_execute'),
        'runtime/kuuos_decision_os_wa_state_v0_3.py', 'build_initial_wa_state',
        _COMMON + (
            ('plural_id', 'source_plural_id'), ('plural_state_digest', 'source_plural_state_digest'),
            ('latest_committed_plural_digest', 'source_committed_plural_digest'),
            ('plural_decision_basis_digest', 'source_plural_decision_basis_digest'),
            ('source_decision_basis_digest', 'source_decision_basis_digest'),
            ('source_committed_decision_digest', 'source_committed_decision_digest'),
            ('route', 'source_route'), ('selected_option_id', 'source_selected_option_id'),
            ('source_option_ids', 'source_option_ids'), ('retained_alternative_ids', 'source_retained_alternative_ids'),
            ('source_options_digest', 'source_options_digest'),
            ('stakeholder_registry_digest', 'source_stakeholder_registry_digest'),
        )),
    CHAIN[2:]: EdgeSpec(
        'formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean',
        ('plan_preserves_source_option_identity', 'plan_preserves_veto_appeal_history', 'plan_does_not_execute'),
        'runtime/kuuos_plan_os_state_v0_1.py', 'build_initial_plan_state',
        _COMMON + (
            ('wa_id', 'source_wa_id'), ('wa_state_digest', 'source_wa_state_digest'),
            ('latest_committed_wa_digest', 'source_committed_wa_digest'), ('wa_basis_digest', 'source_wa_basis_digest'),
            ('source_plural_decision_basis_digest', 'source_plural_decision_basis_digest'),
            ('source_decision_basis_digest', 'source_decision_basis_digest'), ('route', 'source_wa_route'),
            ('endorsed_option_ids', 'source_endorsed_option_ids'), ('review_option_ids', 'source_review_option_ids'),
            ('source_selected_option_id', 'source_selected_option_id'), ('source_option_ids', 'source_option_ids'),
            ('source_retained_alternative_ids', 'source_retained_alternative_ids'),
            ('source_stakeholder_registry_digest', 'source_stakeholder_registry_digest'),
            ('source_utility_records_digest', 'source_utility_records_digest'),
            ('source_veto_records_digest', 'source_veto_records_digest'),
            ('source_appeal_history_digest', 'source_appeal_history_digest'),
        )),
})
PLURAL_HASH_FIELDS = (
    ('utility_records', 'source_utility_records_digest'), ('veto_records', 'source_veto_records_digest'),
    ('aggregate_records', 'source_aggregate_records_digest'), ('appeal_history', 'source_appeal_history_digest'),
)
WA_RECEIPT_FIELDS = (
    ('wa_id', 'wa_id'), ('lineage_id', 'lineage_id'), ('wa_state_digest', 'wa_state_digest'),
    ('latest_committed_wa_digest', 'committed_wa_digest'), ('wa_basis_digest', 'wa_basis_digest'),
    ('source_plural_decision_basis_digest', 'source_plural_decision_basis_digest'),
    ('route', 'route'), ('endorsed_option_ids', 'endorsed_option_ids'), ('review_option_ids', 'review_option_ids'),
)
RECEIPT_PLAN_FIELDS = (
    ('wa_activation_receipt_digest', 'replan_activation_receipt_digest'),
    ('replan_receipt_digest', 'replan_receipt_digest'), ('mission_cycle_state_digest', 'mission_cycle_state_digest'),
    ('next_plan_basis_digest', 'next_plan_basis_digest'),
)


@dataclass(frozen=True)
class DecisionPlanAudit:
    source_os: str
    target_os: str
    status: str
    issues: tuple[str, ...]
    lean_source: str | None
    theorem_names: tuple[str, ...]
    source_commit: str = SOURCE_COMMIT
    execution_authority_granted: bool = field(default=False, init=False)
    lean_python_refinement_proved: bool = field(default=False, init=False)


@dataclass(frozen=True)
class DecisionPlanChainAudit:
    status: str
    issues: tuple[str, ...]
    edges: tuple[DecisionPlanAudit, ...]
    source_commit: str = SOURCE_COMMIT
    execution_authority_granted: bool = field(default=False, init=False)
    lean_python_refinement_proved: bool = field(default=False, init=False)


def _same(left: Any, right: Any) -> bool:
    """Type-preserving JSON equality: False is not 0 and True is not 1."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(_same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def _json_data(value: Any) -> None:
    # Exact built-in types avoid executing custom copy/equality hooks in payloads.
    if type(value) is dict:
        if any(type(k) is not str for k in value):
            raise TypeError('non_string_key')
        for item in value.values():
            _json_data(item)
    elif type(value) is list:
        for item in value:
            _json_data(item)
    elif type(value) is float:
        if not math.isfinite(value):
            raise ValueError('nonfinite_number')
    elif value is not None and type(value) not in (str, bool, int):
        raise TypeError('non_json_value')


class _Checks:
    def __init__(self):
        self.errors: list[str] = []
        self.missing: list[str] = []

    @property
    def status(self):
        return BLOCKED if self.errors else NO_DATA if self.missing else PASSED

    @property
    def issues(self):
        return tuple(dict.fromkeys(self.errors + self.missing))

    def snapshot(self, value, label):
        if value is None:
            self.missing.append(label + ':missing')
            return None
        try:
            if type(value) is not dict:
                raise TypeError('mapping_required')
            _json_data(value)
            return deepcopy(value)
        except (TypeError, ValueError, RecursionError) as exc:
            self.errors.append(f'{label}:invalid_payload:{type(exc).__name__}')
            return None

    def get(self, obj, key, label):
        if key not in obj or obj[key] is None:
            self.missing.append(f'{label}.{key}:missing')
            return _MISSING
        return obj[key]

    def expect(self, obj, key, expected, label):
        actual = self.get(obj, key, label)
        if actual is not _MISSING and expected is not _MISSING and not _same(actual, expected):
            self.errors.append(f'{label}.{key}:binding_mismatch')

    def transfer(self, source, target, pairs, source_label='source', target_label='target'):
        for left, right in pairs:
            self.expect(target, right, self.get(source, left, source_label), target_label)

    def natural(self, obj, key, label):
        value = self.get(obj, key, label)
        if value is _MISSING:
            return None
        if type(value) is not int or value < 0:
            self.errors.append(f'{label}.{key}:nonnegative_int_required')
            return None
        return value

    def dependency(self, name):
        try:
            return import_module(name)
        except ImportError:
            self.missing.append(f'dependency_unavailable:{name}')
        except Exception as exc:
            self.errors.append(f'dependency_failed:{name}:{type(exc).__name__}')
        return None

    def hash(self, value, label):
        module = self.dependency('runtime.kuuos_belief_os_types_v0_1')
        if module is None:
            return _MISSING
        function = getattr(module, 'sha', None)
        if not callable(function):
            self.missing.append('canonical_digest_function_unavailable')
            return _MISSING
        try:
            result = function(deepcopy(value))
            if type(result) is not str or not result:
                raise ValueError('digest_result_invalid')
            return result
        except Exception as exc:
            self.errors.append(f'{label}:digest_failed:{type(exc).__name__}')
            return _MISSING

    def state(self, name, value, required_fields=()):
        spec = STATE_SPECS[name]
        types = self.dependency(spec.types_module)
        kernel = self.dependency(spec.validator_module)
        if types is None or kernel is None:
            return
        old_missing = len(self.missing)
        for key in required_fields:
            self.get(value, key, name)
        for constant, key in (('STATE_VERSION', 'version'), (spec.authority_constant, 'non_authority'),
                              (spec.boundary_constant, 'boundary')):
            expected = getattr(types, constant, _MISSING)
            if expected is _MISSING:
                self.missing.append(f'{name}:schema_constant_unavailable:{constant}')
            else:
                self.expect(value, key, expected, name)
        phase = self.get(value, 'current_phase', name)
        phases = getattr(types, 'PHASES', None)
        if not phases:
            self.missing.append(f'{name}:phase_schema_unavailable')
        elif phase is not _MISSING and phase not in phases:
            self.errors.append(f'{name}:invalid_phase')
        for key in ('route', spec.digest_key):
            self.get(value, key, name)
        self.natural(value, 'updated_at_ms', name)
        self.natural(value, 'event_index', name)
        validator = getattr(kernel, spec.validator_name, None)
        if not callable(validator):
            self.missing.append(f'{name}:validator_unavailable')
        elif len(self.missing) == old_missing:
            copy = deepcopy(value)
            try:
                issues = validator(copy)
                if type(issues) not in (list, tuple) or any(type(x) is not str for x in issues):
                    self.errors.append(f'{name}:validator_result_invalid')
                else:
                    self.errors.extend(f'{name}:original_validator:{x}' for x in issues)
            except Exception as exc:
                self.errors.append(f'{name}:validator_raised:{type(exc).__name__}')
            if not _same(copy, value):
                self.errors.append(f'{name}:validator_mutated_copy')


def _options(check, source, key):
    options = check.get(source, key, 'source')
    if options is _MISSING:
        return None
    if type(options) is not list or any(type(o) is not dict for o in options):
        check.errors.append(f'source.{key}:option_list_required')
        return None
    ids = []
    for option in options:
        identity = check.get(option, 'option_id', 'source.option')
        if identity is _MISSING:
            return None
        if type(identity) is not str or not identity:
            check.errors.append('source.option:invalid_id')
            return None
        ids.append(identity)
    if len(ids) != len(set(ids)):
        check.errors.append('source.options:duplicate_id')
        return None
    return options


def _derived(check, edge, source, target):
    if edge == CHAIN[:2]:
        options = _options(check, source, 'options')
        eligible = check.get(source, 'admissible_option_ids', 'source')
        if eligible is _MISSING or options is None:
            return
        if (type(eligible) is not list or any(type(i) is not str or not i for i in eligible)
                or len(eligible) != len(set(eligible))):
            check.errors.append('source.admissible_option_ids:invalid')
            return
        if not set(eligible).issubset({o['option_id'] for o in options}):
            check.errors.append('source.admissible_option_ids:unknown_id')
        projection = [o for o in options if o['option_id'] in set(eligible)]
        check.expect(target, 'source_options', projection, 'target')
        check.expect(target, 'source_options_digest', check.hash(projection, 'projection'), 'target')
    elif edge == CHAIN[1:3]:
        options = _options(check, source, 'source_options')
        if options is not None:
            option_map = {}
            for option in options:
                value = check.get(option, 'option_digest', 'source.option')
                if value is _MISSING:
                    continue
                if type(value) is not str or not value:
                    check.errors.append('source.option:invalid_digest')
                option_map[option['option_id']] = value
            if len(option_map) == len(options):
                check.expect(target, 'source_option_digest_by_id', option_map, 'target')
            check.expect(source, 'source_options_digest', check.hash(options, 'source_options'), 'source')
        for left, right in PLURAL_HASH_FIELDS:
            value = check.get(source, left, 'source')
            if value is _MISSING:
                continue
            if type(value) is not list:
                check.errors.append(f'source.{left}:list_required')
            else:
                check.expect(target, right, check.hash(value, left), 'target')


def _activation(check, source, target, receipt):
    check.expect(source, 'pending_replan_activation', True, 'source')
    types = check.dependency(STATE_SPECS['PlanOS'].types_module)
    if types is not None:
        routes = getattr(types, 'SOURCE_ROUTE_MAP', None)
        route = check.get(source, 'route', 'source')
        if type(routes) is not dict:
            check.missing.append('plan_source_route_map_unavailable')
        elif route is not _MISSING:
            if type(route) is not str or route not in routes:
                check.errors.append('source.route:unsupported')
            else:
                check.expect(target, 'route', routes[route], 'target')
    packet = check.snapshot(receipt, 'replan_receipt')
    if packet is None:
        return
    check.transfer(source, packet, WA_RECEIPT_FIELDS, target_label='replan_receipt')
    check.transfer(packet, target, RECEIPT_PLAN_FIELDS, source_label='replan_receipt')
    for key, expected in (('mission_cycle_phase', 'replan'), ('future_only', True),
                          ('memory_overwrite', False), ('wa_not_truth', True),
                          ('wa_not_execution', True), ('wa_not_moral_veto', True), ('host_license_granted', False)):
        check.expect(packet, key, expected, 'replan_receipt')
    times = (check.natural(source, 'updated_at_ms', 'source'),
             check.natural(packet, 'created_at_ms', 'replan_receipt'),
             check.natural(target, 'updated_at_ms', 'target'))
    if all(t is not None for t in times) and not times[0] <= times[1] <= times[2]:
        check.errors.append('replan_receipt:time_order_invalid')
    types = check.dependency(STATE_SPECS['DecisionOSWa'].types_module)
    if types is None:
        return
    for constant, key in (('ACTIVATION_RECEIPT_VERSION', 'version'), ('NON_AUTHORITY_FLAGS', 'non_authority')):
        expected = getattr(types, constant, _MISSING)
        if expected is _MISSING:
            check.missing.append(f'replan_receipt:schema_unavailable:{constant}')
        else:
            check.expect(packet, key, expected, 'replan_receipt')
    function = getattr(types, 'wa_activation_receipt_digest', None)
    if not callable(function):
        check.missing.append('replan_receipt:digest_function_unavailable')
    else:
        try:
            check.expect(packet, 'wa_activation_receipt_digest', function(deepcopy(packet)), 'replan_receipt')
        except Exception as exc:
            check.errors.append(f'replan_receipt:digest_failed:{type(exc).__name__}')


def audit_decision_plan_edge(source_os: str, target_os: str, source_state: Any, target_state: Any,
                             *, replan_activation_receipt: Any = None) -> DecisionPlanAudit:
    """Audit one supported edge. PASS concerns supplied data, never its authenticity."""
    edge = (source_os, target_os)
    spec = EDGE_SPECS.get(edge)
    if spec is None:
        return DecisionPlanAudit(source_os, target_os, NO_DATA, ('unsupported_edge_no_shortcut',), None, ())
    check = _Checks()
    source = check.snapshot(source_state, 'source')
    target = check.snapshot(target_state, 'target')
    source_fields = {a for a, _ in spec.equal_fields}
    target_fields = {b for _, b in spec.equal_fields}
    if edge == CHAIN[:2]:
        source_fields.add('options')
        target_fields.update(('source_options', 'source_options_digest'))
    elif edge == CHAIN[1:3]:
        source_fields.update(('source_options', *(a for a, _ in PLURAL_HASH_FIELDS)))
        target_fields.update(('source_option_digest_by_id', *(b for _, b in PLURAL_HASH_FIELDS)))
    elif edge == CHAIN[2:]:
        source_fields.add('pending_replan_activation')
        target_fields.update(b for _, b in RECEIPT_PLAN_FIELDS)
    if source is not None:
        check.expect(source, 'current_phase', 'commit', 'source')
        check.state(source_os, source, sorted(source_fields))
    if target is not None:
        check.state(target_os, target, sorted(target_fields))
    if source is not None and target is not None:
        check.transfer(source, target, spec.equal_fields)
        before = check.natural(source, 'updated_at_ms', 'source')
        after = check.natural(target, 'updated_at_ms', 'target')
        if before is not None and after is not None and after < before:
            check.errors.append('target_precedes_source')
        _derived(check, edge, source, target)
        if edge == CHAIN[2:]:
            _activation(check, source, target, replan_activation_receipt)
    return DecisionPlanAudit(source_os, target_os, check.status, check.issues, spec.lean_source, spec.theorem_names)


def audit_decision_plan_chain(states: Any, *, replan_activation_receipt: Any = None) -> DecisionPlanChainAudit:
    """Require all four states and the three actual edges, not a direct quotient."""
    check = _Checks()
    snapshot = check.snapshot(states, 'chain')
    if snapshot is None:
        return DecisionPlanChainAudit(check.status, check.issues, ())
    edges = tuple(audit_decision_plan_edge(a, b, snapshot.get(a), snapshot.get(b),
                  replan_activation_receipt=replan_activation_receipt) for a, b in EDGE_SPECS)
    for result in edges:
        destination = check.errors if result.status == BLOCKED else check.missing
        if result.status != PASSED:
            destination.extend(f'{result.source_os}->{result.target_os}:{issue}' for issue in result.issues)
    return DecisionPlanChainAudit(check.status, check.issues, edges)
