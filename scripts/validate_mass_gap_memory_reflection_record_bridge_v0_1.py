#!/usr/bin/env python3
"""Validate the Mass Gap MemoryOS / ReflectionOS record bridge.

Stdlib-only structural validator. It checks that the record bridge, spec, and
minimal adapter keep the mass-gap bridge result as append-only record and
review-only surface.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "docs" / "MASS_GAP_MEMORY_REFLECTION_RECORD_BRIDGE_v0_1.md",
    ROOT / "specs" / "mass_gap_memory_reflection_record_bridge_v0_1.yaml",
    ROOT / "examples" / "mass_gap_memory_reflection_record_adapter_minimal.py",
]

REQUIRED_MARKERS = {
    "docs/MASS_GAP_MEMORY_REFLECTION_RECORD_BRIDGE_v0_1.md": [
        "MassGapMemoryRecord",
        "MassGapReflectionReviewSurface",
        "append_only_record",
        "review_surface",
        "public_theorem_boundary: held",
        "append-only / tighten-only / overwrite-forbidden",
    ],
    "specs/mass_gap_memory_reflection_record_bridge_v0_1.yaml": [
        "id: mass_gap_memory_reflection_record_bridge_v0_1",
        "record_id: MassGapMemoryRecord",
        "surface_id: MassGapReflectionReviewSurface",
        "memory_role: append_only_record",
        "reflection_role: review_surface",
        "public_theorem_boundary: held",
        "mass_gap_boundary_preserved",
    ],
    "examples/mass_gap_memory_reflection_record_adapter_minimal.py": [
        "MassGapMemoryRecord",
        "MassGapReflectionReviewSurface",
        "to_memory_record",
        "to_reflection_surface",
        "mass_gap_boundary_review_recorded",
        "preserve_non_collapse_trace",
    ],
}


def fail(message: str) -> int:
    print(f"[mass-gap-memory-reflection-record] FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    for path in REQUIRED_FILES:
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    for rel_path, markers in REQUIRED_MARKERS.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                return fail(f"missing marker in {rel_path}: {marker}")

    print("[mass-gap-memory-reflection-record] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
