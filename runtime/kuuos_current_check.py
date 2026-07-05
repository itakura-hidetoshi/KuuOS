#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_ci_continuation_v0_45

CURRENT_RUNTIME_ROOT = "runtime/kuuos_current_check.py"
CURRENT_ROOT_SEQUENCE_FRONTIER = "kuuos_ci_continuation_v0_45"


def run_current() -> int:
    return kuuos_ci_continuation_v0_45.run_current_continuation()


if __name__ == "__main__":
    raise SystemExit(run_current())
