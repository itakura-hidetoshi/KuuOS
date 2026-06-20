#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_licensed_effect_evidence_closure_public_scenarios_v1_8 import (
    run_licensed_effect_evidence_closure_scenarios,
)


def main() -> int:
    result = run_licensed_effect_evidence_closure_scenarios()
    if result.get("status") != "KUUOS_QI_WORLD_LICENSED_EFFECT_EVIDENCE_CLOSURE_V1_8_OK":
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
