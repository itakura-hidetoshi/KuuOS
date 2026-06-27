#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_CI_POST_MERGE_RECEIPT_v0_2JR.md"
OLD = "- `.github/workflows/physical_quantum_qi_runtime_evolution_validation.yml`"
NEW = "- `.github/workflows/all_governance_validation.yml`\n\nPR #27 originally introduced a dedicated workflow named `Physical Quantum Qi Runtime Evolution Validation`. Its checks are now preserved by the consolidated `All Governance Validation` workflow."


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    if OLD not in text:
        raise RuntimeError("historical workflow path not found")
    PATH.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print(PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
