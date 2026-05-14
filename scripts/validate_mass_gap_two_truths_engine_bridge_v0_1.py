#!/usr/bin/env python3
"""Validate the Mass Gap to Two Truths Engine bridge surface.

This validator is intentionally lightweight and dependency-free. It checks for
required bridge, authority-separation, and non-collapse markers in the KuuOS
public-core files.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "docs" / "MASS_GAP_TO_TWO_TRUTHS_ENGINE_FORMAL_BRIDGE_v0_1.md",
    ROOT / "docs" / "MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md",
    ROOT / "specs" / "mass_gap_two_truths_engine_bridge_v0_1.yaml",
]

REQUIRED_MARKERS = {
    "docs/MASS_GAP_TO_TWO_TRUTHS_ENGINE_FORMAL_BRIDGE_v0_1.md": [
        "itakura-hidetoshi/4d-mass-gap",
        "TwoTruthsMassGapBridgeCarrier",
        "paramartha_non_reification_guard",
        "samvrti_excitation_admissibility",
        "two_truths_non_collapse_barrier",
        "bridge_authority = reference_only",
        "final_theorem_authority = false",
        "execution_authority = false",
        "public theorem boundary: held",
    ],
    "docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md": [
        "itakura-hidetoshi/4d-mass-gap",
        "canonical Lean proof source",
        "itakura-hidetoshi/KuuOS",
        "public-core governance / interpretation / bridge reference",
    ],
    "specs/mass_gap_two_truths_engine_bridge_v0_1.yaml": [
        "id: mass_gap_two_truths_engine_bridge_v0_1",
        "repository: itakura-hidetoshi/4d-mass-gap",
        "bridge_authority: reference_only",
        "paramartha_non_reification_guard: active",
        "samvrti_excitation_admissibility: checkpoint_conditioned",
        "two_truths_non_collapse_barrier: active",
        "final_theorem_authority: false",
        "execution_authority: false",
        "public_theorem_boundary: held",
    ],
}


def fail(message: str) -> int:
    print(f"[mass-gap-two-truths-bridge] FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    for path in REQUIRED_FILES:
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    for rel_path, markers in REQUIRED_MARKERS.items():
        path = ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                return fail(f"missing marker in {rel_path}: {marker}")

    print("[mass-gap-two-truths-bridge] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
