#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CMDS = [
    [sys.executable, "examples/emptiness_runtime_v0_1.py"],
    [sys.executable, "examples/dependent_origination_sheaf_gauge_runtime_v0_2.py"],
    [sys.executable, "examples/two_truths_runtime_v0_1.py"],
    [sys.executable, "examples/emptiness_dependent_origination_two_truths_runtime_v0_1.py"],
    [sys.executable, "scripts/eval_emptiness_do_two_truths_runtime_claims_v0_1.py"],
    [sys.executable, "scripts/eval_emptiness_do_two_truths_runtime_claims_v0_1.py", "--json"],
    [sys.executable, "scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py"],
    [sys.executable, "scripts/check_emptiness_do_two_truths_runtime_worm_receipt_v0_1.py"],
    [sys.executable, "-m", "unittest", "tests/test_emptiness_do_two_truths_runtime_v0_1.py"],
]


def main() -> int:
    for cmd in CMDS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            return code
    print("\nPASS: Integrated emptiness dependent origination two truths runtime v0.1 checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
