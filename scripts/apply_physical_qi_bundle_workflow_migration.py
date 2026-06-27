#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "specs" / "physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json"
OLD = ".github/workflows/physical_quantum_qi_runtime_evolution_validation.yml"
NEW = ".github/workflows/all_governance_validation.yml"


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    if OLD not in text:
        raise RuntimeError("old workflow path not found")
    PATH.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
