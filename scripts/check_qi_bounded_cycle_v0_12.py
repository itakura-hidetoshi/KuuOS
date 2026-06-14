#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.qi_bounded_cycle_v0_12_check_compensation import check_compensation
from scripts.qi_bounded_cycle_v0_12_check_gate import check_gate
from scripts.qi_bounded_cycle_v0_12_check_replay import check_replay
from scripts.qi_bounded_cycle_v0_12_check_source import check_source_digest
from scripts.qi_bounded_cycle_v0_12_check_success import (
    check_convergence,
    check_two_generations,
)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        check_two_generations(base)
        check_convergence(base)
        check_compensation(base)
        check_replay(base)
        check_gate(base)
        check_source_digest(base)
    print("qi_bounded_cycle_v0_12 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
