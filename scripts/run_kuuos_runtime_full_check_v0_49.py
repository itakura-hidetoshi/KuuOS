#!/usr/bin/env python3
from __future__ import annotations

from scripts.check_world_kuu_vacuum_os_hilbert_completion_v0_49 import (
    main as check_v049,
)
from scripts.run_kuuos_runtime_full_check_v0_48 import main as run_v048_full_check


def main() -> int:
    if check_v049() != 0:
        return 1
    return run_v048_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
