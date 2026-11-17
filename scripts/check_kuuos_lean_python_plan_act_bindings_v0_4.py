#!/usr/bin/env python3
"""Byte-specific source correspondence and mandatory cumulative registration.

No Lean compiler or formal refinement proof is executed by this checker.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

SOURCE_COMMIT = '0d77ba4c72d0d183ec76cb14df18dbf50630ec74'
SOURCE_BLOBS = {
    'runtime/kuuos_belief_os_types_v0_1.py': '32eac0fa0b1cb52a999f0a17e67015905a541ba7',
    'runtime/kuuos_plan_os_types_v0_1.py': 'fa3945092610c38d748342e0c7aba1c7cebf08dc',
    'runtime/kuuos_plan_os_state_v0_1.py': '20ebe52c2d8696281968fb4870f1904c976dac37',
    'runtime/kuuos_plan_os_kernel_v0_1.py': '6942b32353b476fe8848d39c548d3cd2fe93ccff',
    'runtime/kuuos_act_os_types_v0_1.py': '6894f380cfbeee008610cf93d5357daac38e93cc',
    'runtime/kuuos_act_os_kernel_v0_1.py': 'db91d45cefd8982309f4a8d58e792f0df0c2c5d4',
    'runtime/kuuos_act_os_fixture_v0_1.py': 'dbb1bc7426172f98d41ebc38186be16ef6199808',
    'formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean': '0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676',
    'formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean': 'c08c8412d435553d9c2a20e309c7cdd4d649f360',
}
DECLARATIONS = {
    'formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean': (
        'plan_does_not_execute', 'plan_does_not_grant_host_license',
        'planActivation_requires_plan_phase', 'planActivation_requires_replan_receipt',
        'planActivation_does_not_execute', 'planActivation_does_not_grant_host_license',
    ),
    'formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean': (
        'invocation_requires_committed_plan', 'invocation_requires_exact_step',
        'invocation_requires_act_phase', 'invocation_requires_host_license',
        'invocation_requires_projection_receipt_binding',
    ),
}
RUNNER = 'scripts/run_kuuos_runtime_full_check_v0_55.py'
CHECKER = 'scripts/check_kuuos_lean_python_plan_act_bindings_v0_4.py'
REQUIRED_TEST_MODULES = (
    'tests.test_kuuos_lean_python_plan_act_admission_v0_4',
    'tests.test_kuuos_lean_python_plan_act_checker_v0_4',
    'tests.test_kuuos_lean_python_plan_act_native_v0_4',
)
BASE_STEPS = (
    ('scripts/check_kuuos_live_v096.py', 'tests.test_kuuos_repository_reference_update_authorization_v0_96'),
    ('scripts/check_kuuos_live_v097.py', 'tests.test_kuuos_repository_atomic_reference_update_v0_97'),
    ('scripts/check_kuuos_live_v098.py', 'tests.test_kuuos_repository_reference_update_receipt_v0_98'),
    ('scripts/check_kuuos_live_v099.py', 'tests.test_kuuos_repository_reference_stability_v0_99'),
    ('scripts/check_kuuos_live_v100.py', 'tests.test_kuuos_repository_local_frontier_finality_v1_00'),
    ('scripts/check_kuuos_live_v101.py', 'tests.test_kuuos_repository_local_frontier_checkpoint_authorization_v1_01'),
    ('scripts/check_kuuos_live_v102.py', 'tests.test_kuuos_repository_atomic_checkpoint_creation_v1_02'),
    ('scripts/check_kuuos_adaptive_retrieval_policy_v0_1.py', 'tests.test_kuuos_adaptive_retrieval_policy_v0_1'),
    ('scripts/check_kuuos_lean_python_contract_bindings_v0_1.py', 'tests.test_kuuos_lean_python_contract_bridge_v0_1'),
    ('scripts/check_kuuos_lean_python_lineage_bindings_v0_2.py', 'tests.test_kuuos_lean_python_lineage_handoff_v0_2'),
    ('scripts/check_kuuos_lean_python_decision_plan_bindings_v0_3.py', 'tests.test_kuuos_lean_python_decision_plan_handoff_v0_3'),
)
EXPECTED_STEPS = BASE_STEPS + tuple((CHECKER, name) for name in REQUIRED_TEST_MODULES)


def _registration(root: Path, missing: list[str], violations: list[str]) -> None:
    runner = root / RUNNER
    if not runner.is_file():
        missing.append(RUNNER)
        return
    try:
        body = ast.parse(runner.read_text(encoding='utf-8')).body
        matches = []
        for node in body:
            targets = ([node.target] if isinstance(node, ast.AnnAssign) else
                       node.targets if isinstance(node, ast.Assign) else [])
            if any(isinstance(t, ast.Name) and t.id == 'FRONTIER_STEPS_AFTER_V095' for t in targets):
                matches.append(ast.literal_eval(node.value))
        if len(matches) != 1 or type(matches[0]) is not tuple:
            violations.append('cumulative_registry_must_be_one_literal_tuple')
        elif matches[0][:len(EXPECTED_STEPS)] != EXPECTED_STEPS:
            violations.append('cumulative_registry_missing_or_reordered_steps')
    except (OSError, UnicodeError, SyntaxError, ValueError, TypeError):
        violations.append('cumulative_registry_unreadable_or_nonliteral')
    for module in REQUIRED_TEST_MODULES:
        relative = module.replace('.', '/') + '.py'
        if not (root / relative).is_file():
            missing.append(relative)


def check_sources(root: Path, *, check_registration: bool = True) -> dict:
    missing: list[str] = []
    violations: list[str] = []
    observed: dict[str, str] = {}
    for relative, expected in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file():
            missing.append(relative)
            continue
        try:
            raw = path.read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            observed[relative] = actual
            if actual != expected:
                violations.append(f'source_blob_drift:{relative}')
            for name in DECLARATIONS.get(relative, ()):
                if not re.search(r'^\s*theorem\s+' + re.escape(name) + r'\b',
                                 raw.decode('utf-8'), re.MULTILINE):
                    violations.append(f'theorem_declaration_missing:{relative}:{name}')
        except (OSError, UnicodeError):
            violations.append(f'source_unreadable:{relative}')
    if check_registration:
        _registration(root, missing, violations)
    status = ('BLOCKED' if violations else 'NO_DATA' if missing else
              'STATIC_MATCH' if check_registration else 'SOURCE_BYTES_MATCH')
    return {
        'status': status, 'source_reference_commit': SOURCE_COMMIT,
        'observed_git_blob_sha1': observed, 'missing': sorted(set(missing)),
        'violations': sorted(set(violations)), 'formal_certified': False,
        'native_integration_executed': False,
        'scope': 'nine_selected_sources_and_cumulative_test_registration_only',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = check_sources(args.repository_root.resolve())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result['status'] == 'STATIC_MATCH' else 2 if result['status'] == 'NO_DATA' else 1


if __name__ == '__main__':
    raise SystemExit(main())
