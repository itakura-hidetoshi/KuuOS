#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAPPINGS = {
    'ROOT / "scripts" / "run_core_governance_full_checks_v0_1.py"':
        'ROOT / "scripts" / "run_core_governance_full_checks_v0_1.py"',
    'ROOT / ".github" / "workflows" / "kuuos_qi_naming_cleanup_validation.yml"':
        'ROOT / ".github" / "workflows" / "kuuos_qi_naming_cleanup_validation.yml"',
    'ROOT / ".github" / "workflows" / "kuuos_qi_naming_cleanup_validation.yml"':
        'ROOT / ".github" / "workflows" / "kuuos_qi_naming_cleanup_validation.yml"',
}


def main() -> int:
    changed: list[Path] = []
    for path in sorted((ROOT / "scripts").rglob("*.py")):
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
