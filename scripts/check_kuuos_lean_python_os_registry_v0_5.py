#!/usr/bin/env python3
"""Static Lean declaration/runtime registry check; NOT a Lean build/refinement proof.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

from runtime.kuuos_lean_python_os_registry_v0_5 import EDGES, OS_BINDINGS

ROOT = Path(__file__).resolve().parents[1]
RUNNER = "scripts/run_kuuos_runtime_full_check_v0_55.py"
DOC = "docs/KUUOS_LEAN_PYTHON_OS_REGISTRY_v0_5.md"
NEW_STEP = (
    "scripts/check_kuuos_lean_python_os_registry_v0_5.py",
    "tests.test_kuuos_lean_python_os_registry_v0_5",
)

# The v0.1-v0.4 cumulative pairs are retained in order; this file only appends.
PREVIOUS_STEPS = (
    ("scripts/check_kuuos_live_v096.py", "tests.test_kuuos_repository_reference_update_authorization_v0_96"),
    ("scripts/check_kuuos_live_v097.py", "tests.test_kuuos_repository_atomic_reference_update_v0_97"),
    ("scripts/check_kuuos_live_v098.py", "tests.test_kuuos_repository_reference_update_receipt_v0_98"),
    ("scripts/check_kuuos_live_v099.py", "tests.test_kuuos_repository_reference_stability_v0_99"),
    ("scripts/check_kuuos_live_v100.py", "tests.test_kuuos_repository_local_frontier_finality_v1_00"),
    ("scripts/check_kuuos_live_v101.py", "tests.test_kuuos_repository_local_frontier_checkpoint_authorization_v1_01"),
    ("scripts/check_kuuos_live_v102.py", "tests.test_kuuos_repository_atomic_checkpoint_creation_v1_02"),
    ("scripts/check_kuuos_adaptive_retrieval_policy_v0_1.py", "tests.test_kuuos_adaptive_retrieval_policy_v0_1"),
    ("scripts/check_kuuos_lean_python_contract_bindings_v0_1.py", "tests.test_kuuos_lean_python_contract_bridge_v0_1"),
    ("scripts/check_kuuos_lean_python_lineage_bindings_v0_2.py", "tests.test_kuuos_lean_python_lineage_handoff_v0_2"),
    ("scripts/check_kuuos_lean_python_decision_plan_bindings_v0_3.py", "tests.test_kuuos_lean_python_decision_plan_handoff_v0_3"),
    ("scripts/check_kuuos_lean_python_plan_act_bindings_v0_4.py", "tests.test_kuuos_lean_python_plan_act_admission_v0_4"),
    ("scripts/check_kuuos_lean_python_plan_act_bindings_v0_4.py", "tests.test_kuuos_lean_python_plan_act_checker_v0_4"),
    ("scripts/check_kuuos_lean_python_plan_act_bindings_v0_4.py", "tests.test_kuuos_lean_python_plan_act_native_v0_4"),
)


def check_root(root: Path) -> tuple[str, ...]:
    errors = []
    for path in (
        DOC, RUNNER, "runtime/kuuos_lean_python_os_registry_v0_5.py",
        "tests/test_kuuos_lean_python_os_registry_v0_5.py",
    ):
        if not (root / path).is_file():
            errors.append("missing:" + path)

    for key, binding in OS_BINDINGS.items():
        lean = root / binding.lean_file
        python = root / binding.python_path
        if not lean.is_file():
            errors.append("lean_missing:" + key + ":" + binding.lean_file)
            continue
        if not python.is_file():
            errors.append("python_missing:" + key + ":" + binding.python_path)
        source = lean.read_text(encoding="utf-8")
        for theorem in binding.theorem_names:
            pattern = r"^\s*(?:theorem|lemma)\s+" + re.escape(theorem) + r"\b"
            if not re.search(pattern, source, re.MULTILINE):
                errors.append("theorem_declaration_missing:" + key + ":" + theorem)

    for (source_name, target_name), edge in EDGES.items():
        for lean_path in edge.lean_files:
            path = root / lean_path
            if not path.is_file():
                errors.append("edge_lean_missing:" + lean_path)
                continue
            source = path.read_text(encoding="utf-8")
            for theorem in edge.theorem_names:
                # The edge may cite two files: a theorem must occur in at least one.
                if any(
                    re.search(
                        r"^\s*(?:theorem|lemma)\s+" + re.escape(theorem) + r"\b",
                        (root / candidate).read_text(encoding="utf-8"),
                        re.MULTILINE,
                    )
                    for candidate in edge.lean_files if (root / candidate).is_file()
                ):
                    continue
                errors.append("edge_theorem_declaration_missing:"
                              + source_name + "->" + target_name + ":" + theorem)

    runner = root / RUNNER
    if runner.is_file():
        try:
            body = ast.parse(runner.read_text(encoding="utf-8")).body
            nodes = []
            for node in body:
                targets = ([node.target] if isinstance(node, ast.AnnAssign)
                           else node.targets if isinstance(node, ast.Assign) else [])
                if any(isinstance(target, ast.Name)
                       and target.id == "FRONTIER_STEPS_AFTER_V095"
                       for target in targets):
                    nodes.append(node)
            if len(nodes) != 1:
                errors.append("runner_registry_not_unique")
            else:
                steps = ast.literal_eval(nodes[0].value)
                if steps != PREVIOUS_STEPS + (NEW_STEP,):
                    errors.append("cumulative_runner_steps_missing_or_reordered")
        except (OSError, SyntaxError, ValueError, TypeError, UnicodeError):
            errors.append("cumulative_runner_unreadable")

    if ("DecisionOS", "PlanOS") in EDGES:
        errors.append("forbidden_decision_plan_shortcut")
    if len(OS_BINDINGS) != 12 or len(EDGES) != 7:
        errors.append("unexpected_registry_coverage")
    return tuple(sorted(set(errors)))


def main() -> int:
    errors = check_root(ROOT)
    if errors:
        for issue in errors:
            print("BLOCKED:", issue)
        return 1
    print("STATIC_MATCH: 12 named OS + 7 typed edges, original Lean declarations,"
          " Python modules and cumulative regression; not Lean/Python refinement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
