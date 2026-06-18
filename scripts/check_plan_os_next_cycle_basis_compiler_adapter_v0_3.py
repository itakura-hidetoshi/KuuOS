from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v03_plan_os_next_cycle_basis_compiler_adapter import run_kernel


def main() -> int:
    result = run_kernel()
    if result.get("status") != "PLAN_OS_NEXT_CYCLE_BASIS_COMPILER_ADAPTER_V0_3_OK":
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
