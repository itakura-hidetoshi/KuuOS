#!/usr/bin/env python3
from runtime.v02_observe_os_replan_lineage_observation_envelope import run_kernel


def main() -> int:
    result = run_kernel()
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
