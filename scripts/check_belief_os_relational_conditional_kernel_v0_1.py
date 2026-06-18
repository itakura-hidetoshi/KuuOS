from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v01_belief_os_relational_conditional_kernel import run_kernel


if __name__ == "__main__":
    result = run_kernel()
    if result.get("status") != "BELIEF_OS_V0_1_OK":
        raise SystemExit(1)
    print(result)
