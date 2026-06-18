from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v02_act_os_replan_lineage_authority_envelope import run_kernel


def main() -> int:
    result = run_kernel()
    if result.get("status") != "ACT_OS_REPLAN_LINEAGE_AUTHORITY_ENVELOPE_V0_2_OK":
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
