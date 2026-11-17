#!/usr/bin/env python3
"""Source-level Lean declaration and Python handoff-key alignment check.

This is static linkage, not Lean elaboration, runtime equivalence or CI proof.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

from runtime.kuuos_lean_python_contract_bridge_v0_1 import CORE_CONTRACTS
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import HANDOFF_CONTRACTS

ROOT = Path(__file__).resolve().parents[1]


def _builder_state_keys(source: str, function_name: str) -> set[str]:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Dict):
                    if any(isinstance(t, ast.Name) and t.id == "state" for t in stmt.targets):
                        return {key.value for key in stmt.value.keys
                                if isinstance(key, ast.Constant) and isinstance(key.value, str)}
    raise ValueError(f"initial_state_literal_not_found:{function_name}")


def _declared(source: str, theorem_name: str) -> bool:
    return re.search(r"(?m)^\s*theorem\s+" + re.escape(theorem_name) + r"(?:\s|$)", source) is not None


def check(root: Path = ROOT) -> list[str]:
    issues: list[str] = []
    for (source_os, target_os), contract in HANDOFF_CONTRACTS.items():
        lean_path = root / contract.lean_source
        if not lean_path.is_file():
            issues.append(f"lean_file_missing:{contract.lean_source}")
            continue
        lean_source = lean_path.read_text(encoding="utf-8")
        for theorem in (contract.premise_theorem, contract.lineage_theorem):
            if not _declared(lean_source, theorem):
                issues.append(f"theorem_missing:{target_os}:{theorem}")
        specs = ((source_os, "source"), (target_os, "target"))
        field_keys: dict[str, set[str]] = {}
        for name, direction in specs:
            stem = CORE_CONTRACTS[name].stem
            path = root / f"runtime/kuuos_{stem}_os_kernel_v0_1.py"
            if not path.is_file():
                issues.append(f"runtime_file_missing:{name}:{path.name}")
                continue
            try:
                field_keys[direction] = _builder_state_keys(path.read_text(encoding="utf-8"), f"build_initial_{stem}_state")
            except (SyntaxError, ValueError) as exc:
                issues.append(f"runtime_schema_unavailable:{name}:{type(exc).__name__}")
        for source_key, target_key in contract.equal_fields:
            if "source" in field_keys and source_key not in field_keys["source"]:
                issues.append(f"source_field_missing:{source_os}:{source_key}")
            if "target" in field_keys and target_key not in field_keys["target"]:
                issues.append(f"target_field_missing:{target_os}:{target_key}")
        if "source" in field_keys:
            for name in ("current_phase", "route", "updated_at_ms") + contract.required_source_flags:
                if name not in field_keys["source"]:
                    issues.append(f"source_required_flag_missing:{source_os}:{name}")
        if "target" in field_keys:
            for name in ("current_phase", "updated_at_ms"):
                if name not in field_keys["target"]:
                    issues.append(f"target_required_field_missing:{target_os}:{name}")
            if target_os == "LearnOS" and "active_now" not in field_keys["target"]:
                issues.append("learning_activation_boundary_missing")
    return issues


def main() -> int:
    issues = check()
    if issues:
        for issue in issues:
            print(f"BLOCKED {issue}")
        return 1
    print(f"PASS lean_python_handoff_links={len(HANDOFF_CONTRACTS)} "
          "(declaration + original constructor field names only; no Lean proof of Python)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
