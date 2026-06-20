#!/usr/bin/env python3
"""Canonical entrypoint for MemoryOS GitHub/chat writeback v0.2 validation."""

from __future__ import annotations

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "scripts" / "validate_github_handoff_sequence_v0_2.py"

if not IMPLEMENTATION.exists():
    raise SystemExit(f"missing validator implementation: {IMPLEMENTATION.relative_to(ROOT)}")

runpy.run_path(str(IMPLEMENTATION), run_name="__main__")
