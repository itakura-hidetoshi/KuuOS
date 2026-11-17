"""Read-only PlanOS -> initial ActOS admission audit; never an execution license.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
Lean correspondence is conditional source grounding, not a proof of Python.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
from importlib import import_module
import json
import math
from typing import Any

VERSION = 'kuuos_lean_python_plan_act_admission_v0_4'
SOURCE_COMMIT = '0d77ba4c72d0d183ec76cb14df18dbf50630ec74'
PASS, LINKS_MATCH, NO_DATA, BLOCKED = 'PASS', 'LINKS_MATCH', 'NO_DATA', 'BLOCKED'

PLAN_NON_AUTHORITY = frozenset((
    'truth_authority_granted', 'execution_authority_granted',
    'proof_authority_granted', 'clinical_authority_granted',
    'institutional_authority_granted', 'legal_authority_granted',
    'host_license_granted', 'memory_overwrite_authority_granted',
    'tool_authority_granted', 'network_authority_granted', 'shell_authority_granted',
))
ACT_NON_AUTHORITY = frozenset((
    'truth_authority_granted', 'final_commitment_authority_granted',
    'memory_overwrite_authority_granted', 'clinical_authority_granted',
    'legal_authority_granted', 'institutional_authority_granted',
    'theorem_authority_granted', 'unrestricted_tool_authority_granted',
    'unrestricted_shell_authority_granted', 'unrestricted_network_authority_granted',
))
PLAN_BOUNDARY = frozenset((
    'plan_is_structured_proposal', 'plan_is_not_decision', 'plan_is_not_execution',
    'plan_is_not_host_license', 'source_wa_state_is_read_only',
    'source_option_identity_preserved', 'stakeholder_veto_appeal_history_preserved',
    'dependency_dag_required', 'resource_bounds_required',
    'rollback_or_escalation_required', 'observation_checkpoint_required',
    'activation_requires_plan_phase',
))
ACT_BOUNDARY = frozenset((
    'plan_activation_is_not_execution_authority', 'explicit_act_phase_receipt_required',
    'exact_act_candidate_step_required', 'explicit_step_authorization_required',
    'valid_v017_host_license_required', 'exact_v017_projection_required',
    'one_host_invocation_at_most', 'one_job_per_invocation',
    'one_bounded_slice_per_invocation', 'lower_host_receipt_is_canonical',
    'duplicate_invocation_idempotent', 'observation_debt_preserved',
    'verification_debt_preserved', 'lower_authority_preserved',
))
RECEIPT_PLAN_PAIRS = (
    ('plan_id', 'plan_id'), ('lineage_id', 'lineage_id'),
    ('plan_state_digest', 'plan_state_digest'),
    ('committed_plan_digest', 'latest_committed_plan_digest'),
    ('plan_basis_digest', 'plan_basis_digest'),
    ('source_wa_basis_digest', 'source_wa_basis_digest'), ('route', 'route'),
    ('replan_activation_receipt_digest', 'replan_activation_receipt_digest'),
    ('next_plan_basis_digest', 'next_plan_basis_digest'),
    ('topological_order', 'topological_order'),
)
ACT_PLAN_PAIRS = (
    ('source_plan_id', 'plan_id'), ('lineage_id', 'lineage_id'),
    ('source_plan_state_digest', 'plan_state_digest'),
    ('source_committed_plan_digest', 'latest_committed_plan_digest'),
    ('source_plan_basis_digest', 'plan_basis_digest'),
    ('source_wa_basis_digest', 'source_wa_basis_digest'),
    ('mission_contract_digest', 'mission_contract_digest'),
)
RECEIPT_KEYS = frozenset(key for key, _ in RECEIPT_PLAN_PAIRS) | frozenset((
    'version', 'mission_cycle_phase', 'mission_cycle_state_digest',
    'plan_phase_receipt_digest', 'future_only', 'memory_overwrite',
    'plan_not_execution', 'host_license_granted', 'non_authority',
    'created_at_ms', 'plan_activation_receipt_digest',
))
INITIAL_EMPTY_TEXT = (
    'predecessor_act_state_digest', 'selected_step_id', 'selected_step_digest',
    'operation_id', 'operation_input_digest', 'step_authorization_digest',
    'host_license_digest', 'host_projection_digest', 'host_tick_digest',
    'host_receipt_digest', 'host_invocation_digest', 'source_supervisor_bundle_digest',
    'result_supervisor_bundle_digest', 'expected_observation_digest',
    'verification_criterion_digest',
)
INITIAL_EMPTY_OBJECT = ('selected_step', 'step_authorization', 'host_license',
                        'host_projection', 'host_tick', 'host_receipt')
INITIAL_EMPTY_LIST = ('completed_step_ids', 'blockers', 'processed_event_digests',
                      'event_history', 'record_summaries')
INITIAL_FALSE = ('effect_recorded', 'observation_required', 'verification_required',
                 'automatic_truth_promotion', 'automatic_plan_completion',
                 'automatic_rollback')
INITIAL_ZERO = ('event_index', 'act_version', 'committed_records')
ACT_KEYS = frozenset(key for key, _ in ACT_PLAN_PAIRS) | frozenset((
    'version', 'act_id', 'plan_activation_receipt_digest', 'current_phase',
    'route', 'updated_at_ms', 'act_state_digest', 'non_authority', 'boundary',
)) | frozenset(INITIAL_EMPTY_TEXT + INITIAL_EMPTY_OBJECT + INITIAL_EMPTY_LIST
               + INITIAL_FALSE + INITIAL_ZERO)
ACT_PHASES = ('bind', 'select', 'authorize', 'project', 'invoke', 'verify', 'commit')
_MISSING = object()


@dataclass(frozen=True)
class AuditResult:
    status: str
    violations: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    runtime_checked: bool = False
    input_sha256: tuple[tuple[str, str], ...] = ()
    source_reference_commit: str = SOURCE_COMMIT
    formal_certified: bool = False
    execution_authority_granted: bool = False
    external_phase_receipt_authenticated: bool = False
    scope: str = 'PlanOS/activation-receipt/ActOS-initial-bind-only'


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def _snapshot(value: Any) -> Any:
    """Accept built-in finite JSON only; reject hooks, cycles and oversized trees."""
    remaining = [200_000]
    active: set[int] = set()

    def visit(item: Any, depth: int) -> Any:
        remaining[0] -= 1
        if depth > 64 or remaining[0] < 0:
            raise ValueError('json_budget_exceeded')
        kind = type(item)
        if kind in (str, int, bool) or item is None:
            if kind is str:
                item.encode('utf-8')  # reject unpaired surrogate code points
            return item
        if kind is float:
            if not math.isfinite(item):
                raise ValueError('nonfinite_number')
            return item
        if kind not in (dict, list):
            raise TypeError('not_builtin_json')
        identity = id(item)
        if identity in active:
            raise ValueError('cyclic_json')
        active.add(identity)
        try:
            if kind is list:
                return [visit(v, depth + 1) for v in item]
            if any(type(k) is not str for k in item):
                raise TypeError('nonstring_key')
            return {visit(k, depth + 1): visit(v, depth + 1) for k, v in item.items()}
        finally:
            active.remove(identity)

    result = visit(value, 0)
    _json(result)  # include the interpreter's integer-serialization limit
    return result


class _Inspection:
    def __init__(self) -> None:
        self.bad: set[str] = set()
        self.missing: set[str] = set()
        self.packets: dict[str, dict[str, Any]] = {}

    def get(self, name: str, key: str) -> Any:
        value = self.packets.get(name, {}).get(key, _MISSING)
        if value is _MISSING:
            self.missing.add(f'{name}:{key}:missing')
        return value

    def text(self, name: str, key: str) -> Any:
        value = self.get(name, key)
        if value is not _MISSING:
            if type(value) is not str:
                self.bad.add(f'{name}:{key}:text_required')
            elif not value.strip():
                self.missing.add(f'{name}:{key}:empty')
        return value

    def nat(self, name: str, key: str) -> int | None:
        value = self.get(name, key)
        if value is _MISSING:
            return None
        if type(value) is not int or value < 0:
            self.bad.add(f'{name}:{key}:natural_required')
            return None
        return value

    def expect(self, name: str, key: str, expected: Any) -> None:
        value = self.get(name, key)
        if value is not _MISSING and _json(value) != _json(expected):
            self.bad.add(f'{name}:{key}:unexpected_value_or_type')

    def equal(self, left: str, key: str, right: str, other: str) -> None:
        a, b = self.get(left, key), self.get(right, other)
        if a is not _MISSING and b is not _MISSING and _json(a) != _json(b):
            self.bad.add(f'{left}:{key}:source_mismatch:{right}:{other}')

    def flags(self, name: str, key: str, keys: frozenset[str], expected: bool) -> None:
        value = self.get(name, key)
        if value is _MISSING:
            return
        if type(value) is not dict:
            self.bad.add(f'{name}:{key}:object_required')
            return
        for field in keys:
            if field not in value:
                self.missing.add(f'{name}:{key}.{field}:missing')
            elif value[field] is not expected:
                self.bad.add(f'{name}:{key}.{field}:boundary_violation')
        if set(value) - keys:
            self.bad.add(f'{name}:{key}:unknown_flags')

    def strings(self, name: str, key: str, *, unique: bool = False) -> list[str] | None:
        value = self.get(name, key)
        if value is _MISSING:
            return None
        if type(value) is not list or any(type(x) is not str or not x.strip() for x in value):
            self.bad.add(f'{name}:{key}:text_list_required')
            return None
        if unique and len(value) != len(set(value)):
            self.bad.add(f'{name}:{key}:duplicate')
        return value

    def check_hash(self, name: str, key: str) -> None:
        value = self.text(name, key)
        if type(value) is str and value.strip():
            payload = {k: v for k, v in self.packets[name].items() if k != key}
            try:
                expected = hashlib.sha256(_json(payload).encode('utf-8')).hexdigest()
            except (TypeError, ValueError, UnicodeError):
                self.bad.add(f'{name}:unhashable_json')
                return
            if value != expected:
                self.bad.add(f'{name}:{key}:digest_mismatch')

    def finish(self, *, runtime_checked: bool = False) -> AuditResult:
        status = BLOCKED if self.bad else NO_DATA if self.missing else (
            PASS if runtime_checked else LINKS_MATCH)
        observations = tuple((name, hashlib.sha256(_json(packet).encode('utf-8')).hexdigest())
                             for name, packet in self.packets.items())
        return AuditResult(status, tuple(sorted(self.bad)), tuple(sorted(self.missing)),
                           runtime_checked=runtime_checked, input_sha256=observations)


def _inspect(plan: Any, receipt: Any, act: Any) -> _Inspection:
    q = _Inspection()
    for name, value in (('plan', plan), ('receipt', receipt), ('act', act)):
        if value is None:
            q.missing.add(f'{name}:packet_missing')
            continue
        if type(value) is not dict:
            q.bad.add(f'{name}:object_required')
            continue
        try:
            q.packets[name] = _snapshot(value)
        except (ValueError, TypeError, UnicodeError, RecursionError):
            q.bad.add(f'{name}:invalid_json')
    # Inspect all available packets: an absent packet cannot mask contradictions.
    for name, keys in (('plan', PLAN_NON_AUTHORITY), ('receipt', PLAN_NON_AUTHORITY),
                       ('act', ACT_NON_AUTHORITY)):
        if name in q.packets:
            q.flags(name, 'non_authority', keys, False)
    times: dict[str, int | None] = {}
    if 'plan' in q.packets:
        q.expect('plan', 'version', 'kuuos_plan_os_state_v0_1')
        q.expect('plan', 'current_phase', 'commit')
        q.expect('plan', 'route', 'PLAN_CANDIDATE')
        q.expect('plan', 'pending_plan_phase_activation', True)
        q.flags('plan', 'boundary', PLAN_BOUNDARY, True)
        for key in ('plan_id', 'lineage_id', 'mission_contract_digest',
                    'latest_committed_plan_digest', 'plan_basis_digest',
                    'source_wa_basis_digest', 'replan_activation_receipt_digest', 'next_plan_basis_digest'):
            q.text('plan', key)
        times['plan'] = q.nat('plan', 'updated_at_ms')
        q.check_hash('plan', 'plan_state_digest')
        order = q.strings('plan', 'topological_order', unique=True)
        steps = q.get('plan', 'steps')
        if steps is not _MISSING:
            if type(steps) is not list or not steps or any(type(s) is not dict for s in steps):
                q.bad.add('plan:steps:nonempty_object_list_required')
            else:
                ids = []
                for step in steps:
                    for key in ('step_id', 'step_digest'):
                        if key not in step:
                            q.missing.add(f'plan:steps:{key}:missing')
                        elif type(step[key]) is not str or not step[key].strip():
                            q.bad.add(f'plan:steps:{key}:text_required')
                    if type(step.get('step_id')) is str:
                        ids.append(step['step_id'])
                if len(ids) != len(set(ids)):
                    q.bad.add('plan:steps:duplicate_id')
                if order is not None and set(order) != set(ids):
                    q.bad.add('plan:topological_order:step_set_mismatch')
    if 'receipt' in q.packets:
        if set(q.packets['receipt']) - RECEIPT_KEYS:
            q.bad.add('receipt:unknown_fields')
        q.expect('receipt', 'version', 'kuuos_plan_os_activation_receipt_v0_1')
        q.expect('receipt', 'route', 'PLAN_CANDIDATE')
        q.expect('receipt', 'mission_cycle_phase', 'plan')
        for key, expected in (('future_only', True), ('memory_overwrite', False),
                              ('plan_not_execution', True), ('host_license_granted', False)):
            q.expect('receipt', key, expected)
        for key in ('plan_id', 'lineage_id', 'plan_state_digest', 'committed_plan_digest',
                    'plan_basis_digest', 'source_wa_basis_digest', 'replan_activation_receipt_digest',
                    'next_plan_basis_digest', 'mission_cycle_state_digest',
                    'plan_phase_receipt_digest'):
            q.text('receipt', key)
        q.strings('receipt', 'topological_order', unique=True)
        times['receipt'] = q.nat('receipt', 'created_at_ms')
        q.check_hash('receipt', 'plan_activation_receipt_digest')
    if 'act' in q.packets:
        q.expect('act', 'version', 'kuuos_act_os_state_v0_1')
        q.flags('act', 'boundary', ACT_BOUNDARY, True)
        for key in ('act_id', 'lineage_id', 'source_plan_id', 'source_plan_state_digest',
                    'source_committed_plan_digest', 'source_plan_basis_digest',
                    'source_wa_basis_digest', 'mission_contract_digest',
                    'plan_activation_receipt_digest'):
            q.text('act', key)
        times['act'] = q.nat('act', 'updated_at_ms')
        q.check_hash('act', 'act_state_digest')
        phase = q.get('act', 'current_phase')
        if phase == 'bind':
            if set(q.packets['act']) - ACT_KEYS:
                q.bad.add('act:unknown_fields')
            q.expect('act', 'route', 'PENDING')
            for fields, expected in ((INITIAL_EMPTY_TEXT, ''), (INITIAL_EMPTY_OBJECT, {}),
                                     (INITIAL_EMPTY_LIST, []), (INITIAL_FALSE, False),
                                     (INITIAL_ZERO, 0)):
                for key in fields:
                    q.expect('act', key, expected)
        elif type(phase) is str and phase in ACT_PHASES:
            q.missing.add('act:initial_bind_snapshot_required')
        elif phase is not _MISSING:
            q.bad.add('act:current_phase:unknown')
    for left, right in (('plan', 'receipt'), ('receipt', 'act')):
        earlier, later = times.get(left), times.get(right)
        if earlier is not None and later is not None and earlier > later:
            q.bad.add(f'{left}:{right}:time_regression')
    for key, source in RECEIPT_PLAN_PAIRS:
        q.equal('receipt', key, 'plan', source)
    for key, source in ACT_PLAN_PAIRS:
        q.equal('act', key, 'plan', source)
    q.equal('act', 'plan_activation_receipt_digest', 'receipt', 'plan_activation_receipt_digest')
    return q


def inspect_plan_act_admission(plan: Any, receipt: Any, act: Any) -> AuditResult:
    """Check exact admission links; never claim native validation or authority."""
    return _inspect(plan, receipt, act).finish()


def audit_plan_act_admission(plan: Any, receipt: Any, act: Any) -> AuditResult:
    """Also run existing validators. PASS applies only to this admission surface."""
    q = _inspect(plan, receipt, act)
    if q.bad or q.missing:
        return q.finish()
    checked = 0
    for name, module, function in (
        ('plan', 'runtime.kuuos_plan_os_state_v0_1', 'validate_plan_state'),
        ('act', 'runtime.kuuos_act_os_kernel_v0_1', 'validate_act_state'),
    ):
        try:
            validator = getattr(import_module(module), function)
        except (ImportError, AttributeError):
            q.missing.add(f'{name}:native_validator_unavailable')
            continue
        except Exception as exc:
            q.bad.add(f'{name}:native_import_exception:{type(exc).__name__}')
            continue
        candidate = deepcopy(q.packets[name])
        before = _json(candidate)
        try:
            errors = validator(candidate)
            if type(errors) is not list or any(type(e) is not str for e in errors):
                q.bad.add(f'{name}:validator_return_type_invalid')
            elif errors:
                q.bad.update(f'{name}:native:{e}' for e in errors)
            else:
                checked += 1
        except Exception as exc:
            q.bad.add(f'{name}:validator_exception:{type(exc).__name__}')
        try:
            after = _json(_snapshot(candidate))
        except (TypeError, ValueError, UnicodeError, RecursionError):
            after = None
        if before != after:
            q.bad.add(f'{name}:validator_mutated_input')
    return q.finish(runtime_checked=(checked == 2 and not q.bad and not q.missing))
