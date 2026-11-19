#!/usr/bin/env python3
"""Fail-closed source/Lean-declaration checks for 12 per-OS Python adapters.

Static source identity and declaration presence are NOT Lean elaboration,
a compiler receipt, Python semantic refinement, or execution authority.
All existing OS kernels / registry are immutable and source-pinned.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "c25f03b8ecc33df82c8ef678243cc66f0ecec90b"
PROOF_SOURCES = {
    "BeliefOS": ("formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean", "92b7bc167bbb68d574a8a19bcbe1754e40b65660"),
    "DecisionOS": ("formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean", "9891ab2aa20c8d2ea4df08abe3bf12d99aad6726"),
    "PlanOS": ("formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean", "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676"),
    "ActOS": ("formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean", "c08c8412d435553d9c2a20e309c7cdd4d649f360"),
    "ObserveOS": ("formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean", "0dccacb16696fc05a8c0f8d70bc09c34a50828f5"),
    "VerifyOS": ("formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean", "cb022ee1b0d43d5a67f38f879cc7e06f60092f9c"),
    "LearnOS": ("formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean", "6dc7ba9d3bf1b4d12ca11e21560ab94d664e8097"),
    "MemoryOS": ("formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean", "b566f668f7bfb8fa8d93f12c1996964d571a7012"),
    "CodeAI": ("formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean", "eecfc1fe1efcac83c669d46edb693d3b833ba967"),
    "DecisionOSPlural": ("formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean", "4b6588305193fb8d41e1fef9c66433a8b5ea67e5"),
    "DecisionOSWa": ("formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean", "c278f21eb3459bef28df8f99c42e5f6cccedc22e"),
    "WORLD": ("formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean", "ed0a9932efb423eb22fbacca2b6536d5a014d67f"),
}
MODULES = {
    "BeliefOS": "runtime/kuuos_lean_python_belief_obligations_v0_27.py",
    "DecisionOS": "runtime/kuuos_lean_python_decision_obligations_v0_27.py",
    "PlanOS": "runtime/kuuos_lean_python_plan_obligations_v0_27.py",
    "ActOS": "runtime/kuuos_lean_python_act_obligations_v0_27.py",
    "ObserveOS": "runtime/kuuos_lean_python_observe_obligations_v0_27.py",
    "VerifyOS": "runtime/kuuos_lean_python_verify_obligations_v0_27.py",
    "LearnOS": "runtime/kuuos_lean_python_learn_obligations_v0_27.py",
    "MemoryOS": "runtime/kuuos_lean_python_memory_obligations_v0_27.py",
    "CodeAI": "runtime/kuuos_lean_python_codeai_obligations_v0_27.py",
    "DecisionOSPlural": "runtime/kuuos_lean_python_decision_plural_obligations_v0_27.py",
    "DecisionOSWa": "runtime/kuuos_lean_python_decision_wa_obligations_v0_27.py",
    "WORLD": "runtime/kuuos_lean_python_world_obligations_v0_27.py",
}
BASE_BLOBS = {
    "runtime/kuuos_lean_python_contract_bridge_v0_1.py": "f6c3f570a996f9fc6c65f026b2fb001ae03c0097",
    "runtime/kuuos_lean_python_os_registry_v0_5.py": "7bb5e7cf2e0fea1a14029a00301708604510b371",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py": "068158c2e4f90f5040f83504218e60752a5472ed",
}
ADDITIVE = (
    "runtime/kuuos_lean_python_per_os_contracts_v0_27.py",
    "tests/lean_python_extensions/test_per_os_contracts_v0_27.py",
    "tests/lean_python_extensions/test_per_os_contract_sources_v0_27.py",
    "docs/KUUOS_LEAN_PYTHON_PER_OS_CONTRACTS_v0_27.md",
)
MODULE_THEOREMS = {}


def _read(root: Path, path: str) -> tuple[bytes | None, str | None]:
    item = root / path
    try:
        if any(part.is_symlink() for part in (item, *item.parents)
               if part != root and root in part.parents):
            return None, "symlink_forbidden"
        if not item.is_file():
            return None, "not_regular_file"
        return item.read_bytes(), None
    except (OSError, ValueError, TypeError):
        return None, "unreadable"


def _blob(raw: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()


def _constant(module: ast.Module, name: str):
    found = [
        a.value for a in module.body
        if isinstance(a, ast.Assign)
        and len(a.targets) == 1
        and isinstance(a.targets[0], ast.Name)
        and a.targets[0].id == name
    ]
    if len(found) != 1:
        raise ValueError("not_one_constant:" + name)
    return ast.literal_eval(found[0])


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    """Read-only and fail closed. Do not execute imported source modules."""
    if type(root) is not Path:
        return ("root:trusted_path_required",)
    errors: list[str] = []
    if set(PROOF_SOURCES) != set(MODULES) or len(MODULES) != 12:
        errors.append("coverage:exact_twelve_required")
    for path, pin in BASE_BLOBS.items():
        raw, problem = _read(root, path)
        if problem:
            errors.append("original_missing:" + path + ":" + problem)
        elif _blob(raw) != pin:
            errors.append("original_source_changed:" + path)
    for name, (path, pin) in PROOF_SOURCES.items():
        raw, problem = _read(root, path)
        if problem:
            errors.append("lean_missing:" + name + ":" + problem)
            continue
        if _blob(raw) != pin:
            errors.append("lean_blob_changed:" + name)
        try:
            lean = raw.decode("utf-8")
        except UnicodeError:
            errors.append("lean_encoding_invalid:" + name)
            continue
        module_path = MODULES.get(name)
        if not module_path:
            errors.append("module_mapping_missing:" + name)
            continue
        python, issue = _read(root, module_path)
        if issue:
            errors.append("python_missing:" + name + ":" + issue)
            continue
        try:
            tree = ast.parse(python.decode("utf-8"))
            actual_name = _constant(tree, "OS_NAME")
            actual_path = _constant(tree, "LEAN_FILE")
            declarations = _constant(tree, "THEOREMS")
            fields = _constant(tree, "FIELDS")
        except (UnicodeError, SyntaxError, ValueError, TypeError, RecursionError):
            errors.append("python_contract_unreadable:" + name)
            continue
        if actual_name != name or actual_path != path:
            errors.append("python_lean_binding_mismatch:" + name)
        if (type(declarations) not in (tuple, list) or not declarations or
                len(set(declarations)) != len(declarations)):
            errors.append("python_theorem_inventory_invalid:" + name)
            continue
        if type(fields) not in (tuple, list) or not fields or len(set(fields)) != len(fields):
            errors.append("python_field_inventory_invalid:" + name)
        for theorem in declarations:
            if type(theorem) is not str or not re.search(
                r"^\s*(?:theorem|lemma)\s+" + re.escape(theorem) + r"\b",
                lean, re.MULTILINE,
            ):
                errors.append("lean_declaration_not_found:" + name + ":" + str(theorem))
    for path in ADDITIVE:
        raw, issue = _read(root, path)
        if issue:
            errors.append("required_new_file:" + path + ":" + issue)
        elif path.endswith(".py"):
            try:
                ast.parse(raw.decode("utf-8"))
            except (UnicodeError, SyntaxError, ValueError, RecursionError):
                errors.append("new_python_syntax_invalid:" + path)
    return tuple(sorted(set(errors)))


def main() -> int:
    problems = check_sources()
    for issue in problems:
        print("BLOCKED:", issue)
    if not problems:
        print("STATIC_MATCH: 12 OS modules, original Lean blobs/theorem declarations,"
              " original v0.1/v0.5/v0.6 bridges unchanged; no semantic refinement claim")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
