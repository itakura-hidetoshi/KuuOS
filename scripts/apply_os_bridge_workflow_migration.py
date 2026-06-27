#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = ".github/workflows/kuuos_os_bridge_validation.yml"
EXCLUDED = {
    ROOT / "scripts" / "apply_os_bridge_workflow_migration.py",
    ROOT / "scripts" / "check_workflow_consolidation_integrity.py",
}

OLD_WORKFLOWS = [
    ".github/workflows/kuuos_two_truths_os_bridge_validation.yml",
    ".github/workflows/kuuos_dependent_origination_os_bridge_validation.yml",
    ".github/workflows/kuuos_indranet_os_dependency_bridge_validation.yml",
    ".github/workflows/kuuos_gauge_os_transport_bridge_validation.yml",
    ".github/workflows/kuuos_sheaf_os_gluing_bridge_validation.yml",
    ".github/workflows/kuuos_cech_obstruction_os_bridge_validation.yml",
    ".github/workflows/kuuos_descent_os_bridge_validation.yml",
    ".github/workflows/kuuos_hyperdescent_os_bridge_validation.yml",
    ".github/workflows/kuuos_infinity_topos_os_bridge_validation.yml",
    ".github/workflows/kuuos_cohesive_os_bridge_validation.yml",
    ".github/workflows/kuuos_differential_cohesive_os_bridge_validation.yml",
    ".github/workflows/kuuos_jet_stability_os_bridge_validation.yml",
    ".github/workflows/kuuos_variational_stability_os_bridge_validation.yml",
    ".github/workflows/kuuos_policy_barrier_os_bridge_validation.yml",
    ".github/workflows/kuuos_selector_boundary_os_bridge_validation.yml",
]


def main() -> int:
    changed: list[Path] = []

    for path in sorted(ROOT.rglob("*")):
        if (
            not path.is_file()
            or path in EXCLUDED
            or ".git" in path.parts
            or ".github/workflows" in path.as_posix()
        ):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        migrated = text
        for old in OLD_WORKFLOWS:
            migrated = migrated.replace(old, NEW)

        if migrated != text:
            path.write_text(migrated, encoding="utf-8")
            changed.append(path.relative_to(ROOT))

    for path in changed:
        print(path)
    print(f"updated={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
