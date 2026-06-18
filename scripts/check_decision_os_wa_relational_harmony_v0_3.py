from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v03_decision_os_wa_relational_harmony import run_kernel


def main() -> int:
    result = run_kernel()
    if result.get("status") != "DECISION_OS_WA_RELATIONAL_HARMONY_V0_3_OK":
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
