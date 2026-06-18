from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v02_decision_os_wa_relational_harmony import run_kernel


if __name__ == "__main__":
    result = run_kernel()
    if result.get("status") != "DECISION_OS_WA_RELATIONAL_HARMONY_V0_2_OK":
        raise SystemExit(1)
    print(result)
