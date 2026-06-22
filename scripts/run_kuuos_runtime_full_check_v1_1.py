#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_operational_agent_controller_v1_1 import main as check_v11
from scripts.run_kuuos_runtime_full_check_v0_48 import main as run_v048_full_check
from scripts.validate_operational_agent_controller_manifest_v1_1 import (
    main as validate_manifest,
)


def main() -> int:
    if run_v048_full_check() != 0:
        return 1
    if validate_manifest() != 0:
        return 1
    return check_v11()


if __name__ == "__main__":
    raise SystemExit(main())
