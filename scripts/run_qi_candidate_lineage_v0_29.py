#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_candidate_lineage_scenarios_v0_29 import (
    run_candidate_lineage_scenarios,
)


def main() -> int:
    result = run_candidate_lineage_scenarios()
    print(result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
