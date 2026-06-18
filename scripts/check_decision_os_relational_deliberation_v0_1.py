from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v01_decision_os_relational_deliberation import run_kernel


if __name__ == "__main__":
    result = run_kernel()
    if result.get("status") != "DECISION_OS_RELATIONAL_DELIBERATION_V0_1_OK":
        raise SystemExit(1)
    print(result)
