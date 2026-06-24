#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
COMMAND = [sys.executable, "scripts/check_kustring_runtime_attestation_v0_2.py"]


def main() -> int:
    print("\n>>> " + " ".join(COMMAND), flush=True)
    code = subprocess.run(COMMAND, cwd=ROOT).returncode
    if code != 0:
        return code
    print("\nPASS: KuString runtime compatibility entry completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
