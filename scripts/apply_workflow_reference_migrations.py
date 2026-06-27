#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAPPINGS = {
    ".github/workflows/kuuos_runtime_full_check.yml": ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/memoryos-world-observe-intake-v0-39.yml": ".github/workflows/memoryos-world-observe-intake-v0-39.yml",
    ".github/workflows/memoryos-qi-world-validation-matrix-v0-36.yml": ".github/workflows/memoryos-qi-world-validation-matrix-v0-36.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/kuuos_runtime_full_check.yml": ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/kuuos_qi_naming_cleanup_validation.yml": ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
    ".github/workflows/kuuos_qi_naming_cleanup_validation.yml": ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/kuuos_runtime_full_check.yml": ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/kuuos_runtime_full_check.yml": ".github/workflows/kuuos_runtime_full_check.yml",
}


def main() -> int:
    changed: list[Path] = []
    for directory, suffixes in (("scripts", {".py"}), ("manifests", {".json"})):
        for path in sorted((ROOT / directory).rglob("*")):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            text = path.read_text(encoding="utf-8")
            migrated = text
            for old, new in MAPPINGS.items():
                migrated = migrated.replace(old, new)
            if migrated != text:
                path.write_text(migrated, encoding="utf-8")
                changed.append(path.relative_to(ROOT))

    for path in changed:
        print(path)
    print(f"updated={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
