from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v01_act_os_authority_bound_invocation import run_kernel


def main() -> int:
    result = run_kernel()
    if result.get("status") != "ACT_OS_AUTHORITY_BOUND_INVOCATION_V0_1_OK":
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
