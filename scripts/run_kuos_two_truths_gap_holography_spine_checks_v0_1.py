#!/usr/bin/env python3
"""
Run KuuOS Two-Truth Gap-Holography Spine v0.1 checks.

This runner delegates to the standalone validator. A PASS is a consistency
receipt only; it is not truth, theorem, execution, kernel-zero, ultimate-identity,
or ultimate-exhaustion authority.
"""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "validators" / "validate_kuos_two_truths_gap_holography_spine_v0_1.py"


def main() -> int:
    runpy.run_path(str(VALIDATOR), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
