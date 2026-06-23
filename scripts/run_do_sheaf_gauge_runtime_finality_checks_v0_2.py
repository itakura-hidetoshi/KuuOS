#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CMDS = [
    [sys.executable, "scripts/check_do_sheaf_gauge_runtime_finality_v0_2.py"],
    [sys.executable, "scripts/check_do_sheaf_gauge_runtime_finality_ci_v0_2.py"],
]


def main() -> int:
    for cmd in CMDS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            return code
    print("\nPASS: DO sheaf gauge runtime finality v0.2 checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
