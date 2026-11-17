"""Static linkage regression for existing KuuOS Lean and Python contracts.

Run only after source files are available locally. This is *not* Strict Lean,
axiom audit, independent CI, or a proof of Python/Lean semantic equivalence.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    ADDITIONAL_PROOF_LINKS, CORE_CONTRACTS,
)

ROOT = Path(__file__).resolve().parents[1]


def _declared(content: str, theorem: str) -> bool:
    return re.search(r"(?m)^\s*theorem\s+" + re.escape(theorem) + r"(?:\s|$)", content) is not None


def _literal_phases(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "PHASES" for target in node.targets):
            return tuple(ast.literal_eval(node.value))
    raise ValueError(f"phases_declaration_missing:{path}")


def main() -> int:
    issues: list[str] = []
    for contract in CORE_CONTRACTS.values():
        lean_path = ROOT / contract.lean_source
        runtime_path = ROOT / (contract.runtime_kernel.replace(".", "/") + ".py")
        type_path = ROOT / (contract.runtime_types.replace(".", "/") + ".py")
        for path in (lean_path, runtime_path, type_path):
            if not path.is_file():
                issues.append(f"missing_file:{path.relative_to(ROOT)}")
        if lean_path.is_file():
            source = lean_path.read_text(encoding="utf-8")
            for theorem in (contract.phase_theorem, contract.event_theorem, contract.authority_theorem):
                if not _declared(source, theorem):
                    issues.append(f"missing_declaration:{contract.os_name}:{theorem}")
        if type_path.is_file():
            try:
                phases = _literal_phases(type_path)
            except (SyntaxError, ValueError, TypeError) as exc:
                issues.append(f"phase_ast_unavailable:{contract.os_name}:{type(exc).__name__}")
            else:
                if phases != contract.phases:
                    issues.append(f"phase_drift:{contract.os_name}")
    for os_name, (lean, theorem, runtime) in ADDITIONAL_PROOF_LINKS.items():
        lean_path = ROOT / lean
        runtime_path = ROOT / (runtime.replace(".", "/") + ".py")
        if not lean_path.is_file() or not runtime_path.is_file():
            issues.append(f"missing_additional_source:{os_name}")
        elif theorem and not _declared(lean_path.read_text(encoding="utf-8"), theorem):
            issues.append(f"missing_additional_declaration:{os_name}:{theorem}")
    for item in issues:
        print(f"BLOCKED {item}")
    if issues:
        return 1
    print(f"PASS source_linkage={len(CORE_CONTRACTS)+len(ADDITIONAL_PROOF_LINKS)} "
          "(source declarations only; Lean/CI not run)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
