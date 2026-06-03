#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_qi_append_only_rhythm_receipt_ledger_v0_1.py"


def main() -> int:
    completed = subprocess.run([sys.executable, str(CHECK)], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        return completed.returncode
    print("PASS: Qi append-only rhythm receipt ledger checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
