#!/usr/bin/env python3
"""v0.28 source pins for real native OS→Lean condition bindings.

Inherits all original v0.27 per-OS source/Lean checks and pins the
unchanged original Python kernels and native full-cycle fixture builder.
Static string checks are NOT Lean elaboration or semantic refinement.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
from scripts import check_kuuos_lean_python_per_os_contracts_v0_27 as prior

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "bf2eda97f843093b3be538495839b08c1b45d298"
PINNED = {
    "runtime/kuuos_lean_python_per_os_contracts_v0_27.py":
        "1062cb89f1f55c52019e4f7ba4fd61daa7e25962",
    "scripts/check_kuuos_lean_python_per_os_contracts_v0_27.py":
        "30414f8642f06abec6e54f9c431e639b7b087cd7",
    "tests/lean_python_extensions/test_per_os_contracts_v0_27.py":
        "9fdacf67fd891511bdac3f35c5513f9b31068ce4",
    "tests/lean_python_extensions/test_per_os_contract_sources_v0_27.py":
        "dba32dd6c92a659f68dced44c93ef7f956ab2031",
    "runtime/kuuos_plan_os_kernel_v0_1.py":
        "6942b32353b476fe8848d39c548d3cd2fe93ccff",
    "runtime/kuuos_act_os_kernel_v0_1.py":
        "db91d45cefd8982309f4a8d58e792f0df0c2c5d4",
    "runtime/kuuos_observe_os_kernel_v0_1.py":
        "670b205f975149cacc3d6a82c3f27edcded8c4ca",
    "runtime/kuuos_verify_os_kernel_v0_1.py":
        "81a415d4eac83d0e828dca2a9e23a0dcfaedf4f0",
    "runtime/kuuos_learn_os_kernel_v0_1.py":
        "8eeaf80af8522df2dc99a1df546b3145aafa2612",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean":
        "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676",
    "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean":
        "c08c8412d435553d9c2a20e309c7cdd4d649f360",
    "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean":
        "0dccacb16696fc05a8c0f8d70bc09c34a50828f5",
    "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean":
        "cb022ee1b0d43d5a67f38f879cc7e06f60092f9c",
    "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean":
        "6dc7ba9d3bf1b4d12ca11e21560ab94d664e8097",
}
NEW = (
    "runtime/kuuos_lean_python_native_os_source_binding_v0_28.py",
    "runtime/kuuos_lean_python_plan_native_binding_v0_28.py",
    "runtime/kuuos_lean_python_act_native_binding_v0_28.py",
    "runtime/kuuos_lean_python_observe_native_binding_v0_28.py",
    "runtime/kuuos_lean_python_verify_native_binding_v0_28.py",
    "runtime/kuuos_lean_python_learn_native_binding_v0_28.py",
    "scripts/check_kuuos_lean_python_native_os_source_bindings_v0_28.py",
    "tests/lean_python_extensions/test_native_os_source_bindings_v0_28.py",
    "tests/lean_python_extensions/test_native_os_source_bindings_sources_v0_28.py",
    "docs/KUUOS_LEAN_PYTHON_NATIVE_OS_SOURCE_BINDINGS_v0_28.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_native_os_source_bindings_v0_28.py":
        "NativePerOSSourceBindingsTests",
    "tests/lean_python_extensions/test_native_os_source_bindings_sources_v0_28.py":
        "NativeOSSourceBindingSourceTests",
}
EXPECTED_BINDING_FUNCTIONS = {
    "runtime/kuuos_lean_python_plan_native_binding_v0_28.py":
        "audit_native_plan_effect_guards",
    "runtime/kuuos_lean_python_act_native_binding_v0_28.py":
        "audit_native_act_authorization",
    "runtime/kuuos_lean_python_observe_native_binding_v0_28.py":
        "audit_native_observe_from_act",
    "runtime/kuuos_lean_python_verify_native_binding_v0_28.py":
        "audit_native_verify_from_observe",
    "runtime/kuuos_lean_python_learn_native_binding_v0_28.py":
        "audit_native_learn_from_verify",
}


def _test_inventory(root: Path) -> dict[str, tuple[str, ...]]:
    found: dict[str, tuple[str, ...]] = {}
    for path, classname in TEST_CLASSES.items():
        raw, problem = prior._read(root, path)
        if problem:
            continue
        try:
            root_ast = ast.parse(raw.decode("utf-8"))
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            continue
        classes = [node for node in root_ast.body
                   if isinstance(node, ast.ClassDef) and node.name == classname]
        if len(classes) != 1:
            continue
        methods = [node.name for node in classes[0].body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
        if methods and len(methods) == len(set(methods)):
            found[path] = tuple(sorted(methods))
    return found


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(prior.check_sources(root))
    for path, sha in PINNED.items():
        raw, issue = prior._read(root, path)
        if issue:
            problems.append("original_source_missing:" + path + ":" + issue)
        elif prior._blob(raw) != sha:
            problems.append("original_source_drift:" + path)
    for path in NEW:
        raw, issue = prior._read(root, path)
        if issue:
            problems.append("required_new_file_missing:" + path + ":" + issue)
            continue
        if path.endswith(".py"):
            try:
                nodes = ast.parse(raw.decode("utf-8")).body
            except (SyntaxError, UnicodeError, ValueError, RecursionError):
                problems.append("new_python_syntax_error:" + path)
                continue
            if path in EXPECTED_BINDING_FUNCTIONS:
                found = [x.name for x in nodes if isinstance(x, ast.FunctionDef)]
                if EXPECTED_BINDING_FUNCTIONS[path] not in found:
                    problems.append("native_binding_entrypoint_missing:" + path)
    tests = _test_inventory(root)
    for path in TEST_CLASSES:
        if path not in tests:
            problems.append("native_test_registration_invalid:" + path)
    return tuple(sorted(set(problems)))


def main() -> int:
    problems = check_sources()
    for p in problems:
        print("BLOCKED:", p)
    if not problems:
        print("STATIC_MATCH: 15 source blobs + inherited v0.27 exact pins,"
              " 5 native OS entrypoints + strict NO_DATA Act boundary")
        print("NOT_PROOF: native fixture/local Python checks != all-CPython Lean semantics")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
