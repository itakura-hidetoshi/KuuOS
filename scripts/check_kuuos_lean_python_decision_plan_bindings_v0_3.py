#!/usr/bin/env python3
"""Static source correspondence only, not Lean compilation or Python refinement."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import (
    CHAIN, EDGE_SPECS, STATE_SPECS, PLURAL_HASH_FIELDS, WA_RECEIPT_FIELDS, RECEIPT_PLAN_FIELDS,
)

# Exact blobs observed through GitHub MCP at SOURCE_COMMIT in the bridge.
# A source change requires a reviewed mapping update, not silent acceptance.
PINNED_BLOBS = {
    'formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean': '4b6588305193fb8d41e1fef9c66433a8b5ea67e5',
    'formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean': 'c278f21eb3459bef28df8f99c42e5f6cccedc22e',
    'formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean': '0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676',
    'runtime/kuuos_decision_os_plural_kernel_v0_2.py': 'fd7a336640c5f25e6596be5ec29ec36ff7fce03d',
    'runtime/kuuos_decision_os_wa_state_v0_3.py': 'b0e6ea237d14f3b41e7cd2caf9cc1813d0918734',
    'runtime/kuuos_plan_os_state_v0_1.py': '20ebe52c2d8696281968fb4870f1904c976dac37',
    'runtime/kuuos_decision_os_wa_kernel_v0_3.py': '0ebc222ac5c73da86fea8c4e09f03782f84314b3',
}
RUNNER = 'scripts/run_kuuos_runtime_full_check_v0_55.py'
CHECKER = 'scripts/check_kuuos_lean_python_decision_plan_bindings_v0_3.py'
TEST_MODULE = 'tests.test_kuuos_lean_python_decision_plan_handoff_v0_3'


def required_paths():
    paths = set(PINNED_BLOBS) | {RUNNER}
    for spec in STATE_SPECS.values():
        paths.add(spec.types_module.replace('.', '/') + '.py')
        paths.add(spec.validator_module.replace('.', '/') + '.py')
    return tuple(sorted(paths))


def _functions(source):
    return {n.name: n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}


def _dictionary_fields(function, variable):
    for node in ast.walk(function):
        if (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == variable for t in node.targets)
                and isinstance(node.value, ast.Dict)):
            return {k.value for k in node.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    return set()


def check_bindings(root: Path = ROOT) -> list[str]:
    issues = []
    sources = {}
    for path in required_paths():
        try:
            raw = (root / path).read_bytes()
            sources[path] = raw.decode('utf-8')
        except (OSError, UnicodeError) as exc:
            issues.append(f'source_unavailable:{path}:{type(exc).__name__}')
            continue
        expected = PINNED_BLOBS.get(path)
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if expected and actual != expected:
            issues.append(f'source_blob_changed:{path}')
    for edge, spec in EDGE_SPECS.items():
        lean = sources.get(spec.lean_source, '')
        for theorem in spec.theorem_names:
            if not re.search(r'(?m)^theorem\s+' + re.escape(theorem) + r'\b', lean):
                issues.append(f'lean_declaration_missing:{theorem}')
        try:
            function = _functions(sources.get(spec.constructor_source, ''))[spec.constructor_name]
            fields = _dictionary_fields(function, 'state')
            required = {right for _, right in spec.equal_fields}
            if edge == CHAIN[:2]: required.update(('source_options', 'source_options_digest'))
            elif edge == CHAIN[1:3]:
                required.update(('source_option_digest_by_id', *(right for _, right in PLURAL_HASH_FIELDS)))
            else: required.update(right for _, right in RECEIPT_PLAN_FIELDS)
            for name in sorted(required - fields):
                issues.append(f'constructor_field_missing:{spec.constructor_name}:{name}')
        except (SyntaxError, KeyError):
            issues.append(f'constructor_unavailable:{spec.constructor_name}')
    for name, spec in STATE_SPECS.items():
        path = spec.validator_module.replace('.', '/') + '.py'
        try:
            if spec.validator_name not in _functions(sources.get(path, '')):
                issues.append(f'validator_missing:{name}')
            types = ast.parse(sources.get(spec.types_module.replace('.', '/') + '.py', ''))
            constants = {t.id for node in types.body if isinstance(node, ast.Assign)
                         for t in node.targets if isinstance(t, ast.Name)}
            for constant in ('STATE_VERSION', 'PHASES', spec.authority_constant, spec.boundary_constant):
                if constant not in constants: issues.append(f'type_constant_missing:{name}:{constant}')
        except SyntaxError:
            issues.append(f'python_source_parse_failed:{name}')
    try:
        function = _functions(sources.get('runtime/kuuos_decision_os_wa_kernel_v0_3.py', ''))['build_replan_wa_activation_receipt']
        fields = _dictionary_fields(function, 'receipt')
        required = {right for _, right in WA_RECEIPT_FIELDS} | {left for left, _ in RECEIPT_PLAN_FIELDS}
        for name in sorted(required - fields): issues.append(f'receipt_field_missing:{name}')
    except (SyntaxError, KeyError):
        issues.append('activation_receipt_constructor_unavailable')
    try:
        tree = ast.parse(sources.get(RUNNER, ''))
        value = next(n.value for n in tree.body if isinstance(n, ast.AnnAssign)
                     and isinstance(n.target, ast.Name) and n.target.id == 'FRONTIER_STEPS_AFTER_V095')
        steps = ast.literal_eval(value)
        for pair in ((CHECKER, TEST_MODULE),
                     ('scripts/check_kuuos_lean_python_contract_bindings_v0_1.py', 'tests.test_kuuos_lean_python_contract_bridge_v0_1'),
                     ('scripts/check_kuuos_lean_python_lineage_bindings_v0_2.py', 'tests.test_kuuos_lean_python_lineage_handoff_v0_2')):
            if pair not in steps: issues.append(f'cumulative_registration_missing:{pair[0]}')
    except (SyntaxError, StopIteration, ValueError, TypeError):
        issues.append('cumulative_registration_unreadable')
    return issues


def main() -> int:
    issues = check_bindings()
    if issues:
        print('\n'.join(issues), file=sys.stderr)
        return 1
    print('Lean/Python v0.3 static correspondence: 4 nodes, 3 edges, 7 pinned blobs, cumulative registration PASS; not a refinement proof')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
