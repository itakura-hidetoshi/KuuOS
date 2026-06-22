#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_operational_agent_scenarios_v1_1 import run_reference_scenarios


def main() -> int:
    result = run_reference_scenarios()
    assert result["status"] == "KUUOS_OPERATIONAL_AGENT_CONTROLLER_V1_1_OK"
    assert result["nominal_status"] == "COMPLETED"
    assert result["nominal_final_stage"] == "PLAN"
    assert result["independent_observation"] is True
    assert result["future_only_learning"] is True
    assert result["external_commit_status"] == "HOLD"
    assert result["external_commit_recovery"] == "REQUEST_HUMAN"
    assert result["external_commit_performed"] is False
    assert result["stale_epoch_recovery"] == "REROTATE"
    assert result["replay_recovery"] == "REVALIDATE"
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    print("PASS: KuuOS Operational Agent Controller v1.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
