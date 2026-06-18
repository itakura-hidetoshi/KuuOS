from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v03_belief_os_context_gerbe_coherence import run_kernel


if __name__ == "__main__":
    result = run_kernel()
    if result.get("status") != "BELIEF_OS_CONTEXT_GERBE_COHERENCE_V0_3_OK":
        raise SystemExit(1)
    print(result)
