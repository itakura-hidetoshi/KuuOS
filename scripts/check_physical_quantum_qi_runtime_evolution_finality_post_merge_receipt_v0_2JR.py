#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_POST_MERGE_RECEIPT_v0_2JR.md"

REQUIRED = [
    "Physical Quantum Qi Runtime Evolution Finality Post-Merge Receipt v0.2J-R",
    "Status: FINALITY_POST_MERGE_RECEIPT_RECORDED",
    "Date: 2026-05-21",
    "Repository: itakura-hidetoshi/KuuOS",
    "Receipt kind: PR #31 finality post-merge receipt",
    "Pull request: `#31`",
    "PR head commit: `98e4279fa548f28470aea6ee7a76669c85c247be`",
    "Squash merge commit: `a57293ca63e69c92f648e1b8c7ef517957e900ac`",
    "Merged at: `2026-05-21T02:31:26Z`",
    "Workflow run ID: `26201842395`",
    "Job ID: `77093258898`",
    "Result: `success`",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_PACKET_v0_2JR.md",
    "scripts/check_physical_quantum_qi_runtime_evolution_finality_packet_v0_2JR.py",
    "specs/physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json",
    "make physical-quantum-qi-runtime-evolution-checks",
    "make physical-quantum-qi-runtime-evolution-finality-checks",
]


def main() -> int:
    if not RECEIPT.is_file():
        print(f"ERROR: missing file: {RECEIPT.relative_to(ROOT)}")
        return 1

    text = RECEIPT.read_text(encoding="utf-8")
    errors = [token for token in REQUIRED if token not in text]
    if errors:
        for token in errors:
            print(f"ERROR: missing token: {token}")
        return 1

    print("PASS: Physical Quantum Qi runtime evolution finality post-merge receipt v0.2J-R checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
