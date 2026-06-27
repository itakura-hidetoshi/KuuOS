#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ".github/workflows/emptiness_two_truths_runtime_audit_validation.yml"
NEW = ".github/workflows/all_governance_validation.yml"
TARGETS = [
    ROOT / "specs" / "kuos_core_release_packet_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml",
    ROOT / "specs" / "kuos_core_release_bundle_manifest_v0_1_138_emptiness_dependent_origination_two_truths_runtime_audit_chain_v0_1.yaml",
    ROOT / "docs" / "ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md",
    ROOT / "docs" / "CI_LEDGER_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
    ROOT / "docs" / "ZENODO_METADATA_EMPTINESS_DO_TWO_TRUTHS_RUNTIME_AUDIT_CHAIN_v0_1.md",
]


def main() -> int:
    changed = 0
    for path in TARGETS:
        if not path.is_file():
            raise FileNotFoundError(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8")
        migrated = text.replace(OLD, NEW)
        if migrated != text:
            path.write_text(migrated, encoding="utf-8")
            print(path.relative_to(ROOT))
            changed += 1
    print(f"updated={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
