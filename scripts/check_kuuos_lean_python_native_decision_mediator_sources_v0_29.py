#!/usr/bin/env python3
"""Native Decision/Plural/Wa/Belief v0.29 exact source immutability audit.

This checker inherits every earlier source pin, verifies original Lean
and native implementation blobs, and confirms new Python entrypoints.
Static pins are NOT a new Lean elaboration, runtime semantic refinement,
or independent CI success.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from scripts import check_kuuos_lean_python_native_os_source_bindings_v0_28 as previous

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "66a9f5b2d895d2182f6ee9462f18c6a2a3832e4a"
SOURCE_BLOBS = {
    "runtime/kuuos_lean_python_native_os_source_binding_v0_28.py": "df213293bbdd4037a6a49f75cfc240538eaafcd4",
    "scripts/check_kuuos_lean_python_native_os_source_bindings_v0_28.py": "03fbc86366f07edf06da7b91206ebf6806d0e1c8",
    "runtime/kuuos_lean_python_decision_obligations_v0_27.py": "5748a76e42ed80ab865a6612e9d112a0f5eefa4d",
    "runtime/kuuos_lean_python_decision_plural_obligations_v0_27.py": "3d651e4cd7ad2d64e2b42bec73bec5bdd71365db",
    "runtime/kuuos_lean_python_decision_wa_obligations_v0_27.py": "21741db7a2dda58949cc70ed8cedf74dbd148907",
    "runtime/kuuos_decision_os_phase_v0_1.py": "5d596f0362d032d4ca4c08608cd2546744564159",
    "runtime/kuuos_decision_os_state_v0_1.py": "80ea719c2a77fb30cef488fe5f9f1f9ae597991a",
    "runtime/kuuos_decision_os_plural_kernel_v0_2.py": "fd7a336640c5f25e6596be5ec29ec36ff7fce03d",
    "runtime/kuuos_decision_os_wa_kernel_v0_3.py": "0ebc222ac5c73da86fea8c4e09f03782f84314b3",
    "runtime/kuuos_belief_os_gerbe_store_v0_3.py": "9982c835c1f828ac608a038b24d66ed350c3af67",
    "runtime/kuuos_belief_os_gerbe_types_v0_3.py": "2b751413296450a38cd975e7680adc99d1f7a462",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py": "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean": "9891ab2aa20c8d2ea4df08abe3bf12d99aad6726",
    "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean": "4b6588305193fb8d41e1fef9c66433a8b5ea67e5",
    "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean": "c278f21eb3459bef28df8f99c42e5f6cccedc22e",
    "formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean": "92b7bc167bbb68d574a8a19bcbe1754e40b65660",
    "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean": "b4023e192f78ac10495c851ba68d63ee9fb22048",
    "runtime/kuuos_belief_os_gerbe_coherence_v0_3.py": "566d2f1b923093c4c1ca12f98506841062a8e6a2"
}
NEW_PATHS = (
    "runtime/kuuos_lean_python_decision_mediator_source_v0_29.py",
    "runtime/kuuos_lean_python_decision_native_binding_v0_29.py",
    "runtime/kuuos_lean_python_plural_native_binding_v0_29.py",
    "runtime/kuuos_lean_python_wa_native_binding_v0_29.py",
    "runtime/kuuos_lean_python_belief_gerbe_native_binding_v0_29.py",
    "scripts/check_kuuos_lean_python_native_decision_mediator_sources_v0_29.py",
    "tests/lean_python_extensions/test_native_decision_mediator_bindings_v0_29.py",
    "tests/lean_python_extensions/test_native_decision_mediator_sources_v0_29.py",
    "docs/KUUOS_LEAN_PYTHON_NATIVE_DECISION_MEDIATOR_v0_29.md",
)
ENTRYPOINTS = {
    "runtime/kuuos_lean_python_decision_native_binding_v0_29.py":
        "audit_native_decision_from_belief",
    "runtime/kuuos_lean_python_plural_native_binding_v0_29.py":
        "audit_native_plural_consensus",
    "runtime/kuuos_lean_python_wa_native_binding_v0_29.py":
        "audit_native_wa_endorsement",
    "runtime/kuuos_lean_python_belief_gerbe_native_binding_v0_29.py":
        "audit_native_belief_gerbe_source",
}
TEST_CLASSES = {
    "tests/lean_python_extensions/test_native_decision_mediator_bindings_v0_29.py":
        "NativeDecisionMediatorBindingsTests",
    "tests/lean_python_extensions/test_native_decision_mediator_sources_v0_29.py":
        "NativeDecisionMediatorSourceTests",
}
THEOREMS = {
    "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean":
        ("admissibleOption_is_not_prohibited", "decisionCommit_does_not_overwrite_memory"),
    "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean":
        ("consensusCertificate_has_no_validated_veto",
         "consensusCertificate_meets_support_floor",
         "consensusCertificate_meets_opposition_ceiling",
         "consensusCertificate_meets_worst_case_floor"),
    "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean":
        ("endorsedWa_has_no_confirmed_false_harmony",
         "endorsedWa_preserves_minority", "endorsedWa_considers_dissent"),
    "formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean":
        ("beliefActivation_requires_replan",),
    "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean":
        ("gerbeBelief_preserves_locality",
         "gerbeBelief_preserves_plurality",
         "gerbeBelief_preserves_two_truths",
         "gerbeBelief_is_non_reified",
         "gerbeBelief_does_not_search_paths",
         "gerbeBelief_does_not_select_global_winner",
         "gerbeBelief_does_not_globally_trivialize"),
}


def inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    names = {}
    for path, classname in TEST_CLASSES.items():
        raw, err = previous.prior._read(root, path)
        if err:
            continue
        try:
            tree = ast.parse(raw.decode("utf-8"))
        except (UnicodeError, SyntaxError, ValueError, RecursionError):
            continue
        cls = [x for x in tree.body
               if isinstance(x, ast.ClassDef) and x.name == classname]
        if len(cls) != 1:
            continue
        methods = [x.name for x in cls[0].body
                   if isinstance(x, ast.FunctionDef) and x.name.startswith("test_")]
        if methods and len(set(methods)) == len(methods):
            names[path] = tuple(sorted(methods))
    return names


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    problems = list(previous.check_sources(root))
    for path, pin in SOURCE_BLOBS.items():
        raw, error = previous.prior._read(root, path)
        if error:
            problems.append("predecessor_source_missing:" + path + ":" + error)
        elif previous.prior._blob(raw) != pin:
            problems.append("predecessor_source_drift:" + path)
    for path in NEW_PATHS:
        raw, error = previous.prior._read(root, path)
        if error:
            problems.append("new_source_missing:" + path + ":" + error)
            continue
        if path.endswith(".py"):
            try:
                tree = ast.parse(raw.decode("utf-8"))
            except (SyntaxError, UnicodeError, ValueError, RecursionError):
                problems.append("new_python_unreadable:" + path)
                continue
            if path in ENTRYPOINTS:
                defs = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
                if ENTRYPOINTS[path] not in defs:
                    problems.append("native_entrypoint_missing:" + path)
    for path, theorem_names in THEOREMS.items():
        raw, issue = previous.prior._read(root, path)
        if issue:
            problems.append("theorem_source_missing:" + path)
            continue
        lean = raw.decode("utf-8", errors="replace")
        for name in theorem_names:
            if not re.search(r"^\s*theorem\s+" + re.escape(name) + r"\b",
                             lean, flags=re.MULTILINE):
                problems.append("native_theorem_name_missing:" + path + ":" + name)
    tested = inventory(root)
    for path in TEST_CLASSES:
        if path not in tested:
            problems.append("new_native_tests_not_registered:" + path)
    return tuple(sorted(set(problems)))


def main() -> int:
    problems = check_sources()
    for problem in problems:
        print("BLOCKED:", problem)
    if not problems:
        print("STATIC_MATCH: 18 predecessor blobs, original theorem names,"
              " 4 native decision/mediator source entrypoints and test inventory")
        print("NOT_LEAN_PROOF: original v0.1-v0.3 Lean untouched")
        print("Belief v0.3 local theorem DATA checked; v0.3→v0.1 proof type NO_DATA")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
