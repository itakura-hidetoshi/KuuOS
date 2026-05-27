#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECKS = [
    "scripts/check_qi_probe_scheduler_proposal_v0_1.py",
    "scripts/check_qi_process_tensor_aware_scheduler_state_v0_1.py",
    "scripts/check_qi_process_tensor_aware_scheduler_addendum_v0_1.py",
]


def main() -> int:
    failed = 0
    for item in CHECKS:
        path = ROOT / item
        if not path.is_file():
            print(f"ERROR: missing:{item}")
            failed += 1
            continue
        completed = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            print(f"ERROR: failed:{item}")
            print(completed.stdout)
            print(completed.stderr)
            failed += 1
    if failed:
        return 1
    print("PASS: Qi process tensor scheduler checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
