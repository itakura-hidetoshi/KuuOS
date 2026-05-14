#!/usr/bin/env python3
"""Top-level KuuOS governance check runner."""

from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/run_ai_yogacara_full_checks_v0_1.py"],
    [sys.executable, "scripts/run_core_governance_full_checks_v0_1.py"],
    [sys.executable, "scripts/validate_gpt_github_integration_v0_1.py"],
    [sys.executable, "scripts/validate_mass_gap_two_truths_engine_bridge_v0_1.py"],
    [sys.executable, "scripts/validate_mass_gap_memory_reflection_record_bridge_v0_1.py"],
]


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    completed = subprocess.run(list(cmd), cwd=ROOT)
    return completed.returncode


def main() -> int:
    failures: list[tuple[list[str], int]] = []
    for cmd in COMMANDS:
        code = run_command(cmd)
        if code != 0:
            failures.append((cmd, code))
            break

    if failures:
        for cmd, code in failures:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
        return 1

    print("\nPASS: KuuOS all governance full checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
