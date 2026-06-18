from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v02_belief_os_context_gauge_transport import run_kernel


if __name__ == "__main__":
    result = run_kernel()
    if result.get("status") != "BELIEF_OS_CONTEXT_GAUGE_TRANSPORT_V0_2_OK":
        raise SystemExit(1)
    print(result)
