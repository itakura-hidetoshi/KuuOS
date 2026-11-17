#!/usr/bin/env python3
"""Direct source pins and cumulative discovery for checked transitions v0.10.

Only these selected direct source bytes are pinned, not the transitive import
closure or the interpreter. Inspect a quiescent checkout. This does not import
runtime modules, execute Lean, authenticate issuers, or prove Python refinement.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "8b855cf1f1c2296dbe0d8d3057cd391729d572d1"
SOURCE_BLOBS = {
    "runtime/kuuos_lean_python_contract_bridge_v0_1.py":
        "f6c3f570a996f9fc6c65f026b2fb001ae03c0097",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py":
        "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_lean_python_native_cycle_ledger_replay_v0_7.py":
        "e1d4cdc5dd698b7c1aad1f2fcc3a9499a0eced49",
    "runtime/kuuos_lean_python_native_cycle_receipt_capture_v0_8.py":
        "219ace2ec190cd8bf91284d413914afa4c696aef",
    "runtime/kuuos_lean_python_isolated_native_receipt_evidence_v0_9.py":
        "4cfda1477ba5beac6b469668228cd3dda789c31c",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py":
        "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_decision_os_kernel_v0_1.py":
        "7fbe347c0ae22f7efea0cb0147f1e1934ee743d4",
    "runtime/kuuos_decision_os_types_v0_1.py":
        "7a8432fad3eca3d04ac14e17cc4178833fd3c9aa",
    "runtime/kuuos_decision_os_store_v0_1.py":
        "7ddcc08cc7f3d4a6e274ff0406805ef632457931",
    "runtime/kuuos_plan_os_kernel_v0_1.py":
        "6942b32353b476fe8848d39c548d3cd2fe93ccff",
    "runtime/kuuos_plan_os_types_v0_1.py":
        "fa3945092610c38d748342e0c7aba1c7cebf08dc",
    "runtime/kuuos_plan_os_store_v0_1.py":
        "106a4adae2750bc543786c1ff36cd746a4d838d4",
    "runtime/kuuos_act_os_kernel_v0_1.py":
        "db91d45cefd8982309f4a8d58e792f0df0c2c5d4",
    "runtime/kuuos_act_os_types_v0_1.py":
        "6894f380cfbeee008610cf93d5357daac38e93cc",
    "runtime/kuuos_act_os_store_v0_1.py":
        "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_observe_os_kernel_v0_1.py":
        "670b205f975149cacc3d6a82c3f27edcded8c4ca",
    "runtime/kuuos_observe_os_types_v0_1.py":
        "2bed5ca44ad3de69daa0ac0d2cc3c462ea30c0c9",
    "runtime/kuuos_observe_os_store_v0_1.py":
        "7c6433b04fe83da4ac669a93d85f447591117897",
    "runtime/kuuos_verify_os_kernel_v0_1.py":
        "81a415d4eac83d0e828dca2a9e23a0dcfaedf4f0",
    "runtime/kuuos_verify_os_types_v0_1.py":
        "2889e0963f2171842e49ec477eec23e3a705eb6c",
    "runtime/kuuos_verify_os_store_v0_1.py":
        "6f08033b55fdde4d36cf2cb491da48cc4c40d00d",
    "runtime/kuuos_learn_os_kernel_v0_1.py":
        "8eeaf80af8522df2dc99a1df546b3145aafa2612",
    "runtime/kuuos_learn_os_types_v0_1.py":
        "3e74b2e672064c435ff785e03ea85b8c6ab5f5eb",
    "runtime/kuuos_learn_os_store_v0_1.py":
        "1a462212f9488c2b3dc2ca2ec96efcd7a20e0713",
    "runtime/kuuos_decision_os_state_v0_1.py":
        "80ea719c2a77fb30cef488fe5f9f1f9ae597991a",
    "runtime/kuuos_plan_os_state_v0_1.py":
        "20ebe52c2d8696281968fb4870f1904c976dac37",
    "scripts/run_kuuos_runtime_full_check_v0_55.py":
        "e529fca18f44687c271c3c958890dfb3940bc62a",
    "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean":
        "9891ab2aa20c8d2ea4df08abe3bf12d99aad6726",
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
REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_checked_transition_v0_10.py",
    "runtime/kuuos_lean_python_guarded_native_cycle_v0_10.py",
    "tests/test_kuuos_lean_python_checked_transition_v0_10.py",
    "tests/test_kuuos_lean_python_guarded_native_cycle_v0_10.py",
    "scripts/check_kuuos_lean_python_checked_transition_sources_v0_10.py",
    "tests/test_kuuos_lean_python_checked_transition_sources_v0_10.py",
    "docs/KUUOS_LEAN_PYTHON_CHECKED_NATIVE_TRANSITIONS_v0_10.md",
)
REGISTERED_TEST_PATH = "tests/test_kuuos_lean_python_os_registry_v0_5.py"
NEW_TEST_CLASSES = {
    "tests.test_kuuos_lean_python_checked_transition_v0_10":
        ("CheckedTransitionTests",),
    "tests.test_kuuos_lean_python_guarded_native_cycle_v0_10":
        ("GuardedNativeCycleTests",),
    "tests.test_kuuos_lean_python_checked_transition_sources_v0_10":
        ("CheckedTransitionSourceTests",),
}
# Exact original top-level import signatures, including the accepted registry
# alias. No whole-file pin: the three new direct imports are additive.
PRIOR_IMPORTS = (
    ("ImportFrom", "__future__", 0, (("annotations", None),)),
    ("ImportFrom", "dataclasses", 0, (("FrozenInstanceError", None),)),
    ("ImportFrom", "importlib.util", 0, (("find_spec", None),)),
    ("Import", None, 0, (("unittest", None),)),
    ("ImportFrom", "runtime", 0,
     (("kuuos_lean_python_os_registry_v0_5", "registry"),)),
    ("ImportFrom", "runtime.kuuos_lean_python_contract_bridge_v0_1", 0,
     (("ADDITIONAL_PROOF_LINKS", None), ("CORE_CONTRACTS", None))),
    ("ImportFrom", "runtime.kuuos_lean_python_lineage_handoff_v0_2", 0,
     (("HANDOFF_CONTRACTS", None),)),
    ("ImportFrom", "runtime.kuuos_lean_python_decision_plan_handoff_v0_3", 0,
     (("EDGE_SPECS", None),)),
    ("ImportFrom", "tests.test_kuuos_lean_python_os_path_composition_v0_6", 0,
     (("CompositionContractTests", None), ("NativeCompositionTests", None))),
    ("ImportFrom", "tests.test_kuuos_lean_python_native_cycle_ledger_replay_v0_7", 0,
     (("SourcePinTests", None), ("NativeCycleLedgerReplayTests", None))),
    ("ImportFrom", "tests.test_kuuos_lean_python_native_cycle_receipt_capture_v0_8", 0,
     (("NativeCaptureV08Tests", None), ("CaptureSourceV08Tests", None))),
    ("ImportFrom", "tests.test_kuuos_lean_python_isolated_native_evidence_v0_9", 0,
     (("IsolatedNativeEvidenceTests", None), ("EvidenceSourcePinTests", None))),
)


def _read_file(root: Path, relative: str) -> tuple[bytes | None, str | None]:
    """Read a regular file only after excluding symlinks in its whole path."""
    path = (root / relative).absolute()
    try:
        for parent in reversed(path.parents):
            mode = parent.lstat().st_mode
            if stat.S_ISLNK(mode):
                return None, "symlink_not_allowed"
            if not stat.S_ISDIR(mode):
                return None, "not_regular_file"
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            return None, "symlink_not_allowed"
        if not stat.S_ISREG(mode):
            return None, "not_regular_file"
        return path.read_bytes(), None
    except FileNotFoundError:
        return None, "missing"
    except OSError:
        return None, "unreadable"


def _signature(node: ast.Import | ast.ImportFrom) -> tuple:
    return (
        type(node).__name__, getattr(node, "module", None),
        getattr(node, "level", 0),
        tuple((alias.name, alias.asname) for alias in node.names),
    )


def _registration_issues(root: Path) -> list[str]:
    raw, issue = _read_file(root, REGISTERED_TEST_PATH)
    if issue:
        return ["cumulative_test_module_" + issue]
    try:
        body = ast.parse(raw.decode("utf-8")).body
    except (SyntaxError, UnicodeError, ValueError, RecursionError):
        return ["cumulative_test_registration_invalid"]
    imports = [node for node in body if isinstance(node, (ast.Import, ast.ImportFrom))]
    prior = tuple(
        _signature(node) for node in imports
        if not isinstance(node, ast.ImportFrom) or node.module not in NEW_TEST_CLASSES
    )
    issues = []
    if prior != PRIOR_IMPORTS:
        issues.append("prior_imports_not_preserved")
    for module, names in NEW_TEST_CLASSES.items():
        matching = [
            node for node in imports
            if isinstance(node, ast.ImportFrom) and node.module == module
        ]
        if (len(matching) != 1 or matching[0].level != 0
                or tuple((alias.name, alias.asname) for alias in matching[0].names)
                != tuple((name, None) for name in names)):
            issues.append("v010_tests_not_registered:" + module)
    return issues


def check_sources(root: Path = ROOT, check_registration: bool = True) -> tuple[str, ...]:
    """Check selected original bytes, new-file inventory, and direct imports.

    No module in the checkout is imported or executed. Missing, unreadable,
    symlinked or byte-drifted inputs fail closed. This is a local static check.
    """
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    issues: list[str] = []
    for relative, expected in SOURCE_BLOBS.items():
        raw, issue = _read_file(root, relative)
        if issue:
            issues.append("source_" + issue + ":" + relative)
            continue
        actual = hashlib.sha1(
            b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
        ).hexdigest()
        if actual != expected:
            issues.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        _, issue = _read_file(root, relative)
        if issue:
            issues.append("required_v010_file_" + issue + ":" + relative)
    if check_registration:
        issues.extend(_registration_issues(root))
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print(
            f"STATIC_MATCH: {len(SOURCE_BLOBS)} selected direct Git blobs, "
            "v0.10 file inventory and cumulative test imports; "
            "no transitive-source authentication, Lean execution or refinement"
        )
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
