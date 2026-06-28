#!/usr/bin/env python3
"""Run the cumulative DecisionOS validation surface.

All independent version checks are attempted so one audit run can report every
visible failure. Validation remains structural evidence and does not create
truth, theorem, release, or execution authority.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
from collections.abc import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "-m", "runtime.v01_decision_os_relational_deliberation"),
    (sys.executable, "scripts/check_decision_os_relational_deliberation_v0_1.py"),
    (sys.executable, "-m", "runtime.v02_decision_os_plural_harmony_appeal"),
    (sys.executable, "scripts/check_decision_os_plural_harmony_appeal_v0_2.py"),
    (sys.executable, "-m", "runtime.v03_decision_os_wa_relational_harmony"),
    (sys.executable, "scripts/check_decision_os_wa_relational_harmony_v0_3.py"),
    (sys.executable, "scripts/check_decisionos_admissible_candidate_selection_v0_4.py"),
)


def run_command(command: Sequence[str], env: dict[str, str]) -> int:
    print("\n>>> " + " ".join(command), flush=True)
    return subprocess.run(list(command), cwd=ROOT, env=env, check=False).returncode


def main() -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        item for item in (str(ROOT), env.get("PYTHONPATH", "")) if item
    )
    env.setdefault("PYTHONUNBUFFERED", "1")

    failures: list[tuple[Sequence[str], int]] = []
    for command in COMMANDS:
        code = run_command(command, env)
        if code != 0:
            failures.append((command, code))

    if failures:
        for command, code in failures:
            print(f"FAIL: {' '.join(command)} exited with {code}")
        return 1

    print("\nPASS: DecisionOS v0.1-v0.4 validation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
