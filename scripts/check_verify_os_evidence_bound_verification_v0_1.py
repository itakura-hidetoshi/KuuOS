from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v01_verify_os_evidence_bound_verification import run_kernel


def main() -> int:
    result = run_kernel()
    if result.get("status") != "VERIFY_OS_EVIDENCE_BOUND_VERIFICATION_V0_1_OK":
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
