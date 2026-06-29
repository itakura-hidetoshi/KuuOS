#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_kuuos_runtime_full_check_v0_55 import main as run_previous


def main() -> int:
    if run_previous() != 0:
        return 1
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "tests.test_kuuos_repository_reference_update_authorization_v0_96"],
        cwd=ROOT,
        check=False,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
