#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.v1_0_adaptive_agent_reference_architecture import run_kernel


def main() -> int:
    result = run_kernel()
    assert result["status"] == "KUUOS_ADAPTIVE_AGENT_REFERENCE_ARCHITECTURE_V1_0_OK"
    assert result["model_count"] == 12
    assert result["relation_count"] == 11
    assert result["planos_mapping_count"] == 17
    assert result["nominal_stage"] == "PLAN"
    assert result["rerotation_epoch"] == 1
    assert result["terminal_session_count"] == 1
    assert result["abort_mode"] == "TERMINATED"
    assert result["execution_allowed"] is False
    print("PASS: KuuOS Adaptive Agent Reference Architecture v1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
