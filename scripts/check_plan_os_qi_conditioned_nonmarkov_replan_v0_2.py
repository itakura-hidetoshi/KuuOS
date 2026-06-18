from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v02_plan_os_qi_conditioned_nonmarkov_replan import run_kernel


def main() -> int:
    result = run_kernel()
    if result.get("status") != "PLAN_OS_QI_CONDITIONED_NONMARKOV_REPLAN_V0_2_OK":
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
