#!/usr/bin/env python3
"""Demo for Physical Quantum Qi IndraNet PlanOS handoff v0.2D.

Loads the v0.2D IndraNet gauge transport packet, evaluates transport runtime,
and emits a PlanOS.transport_candidate handoff payload. This is not an audit
layer and grants no execution, commit, memory overwrite, world rewrite, proof,
truth, ontology, clinical, or safety override authority.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_indranet_planos_handoff_v0_2D import (  # noqa: E402
    build_and_validate_planos_transport_handoff,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_indranet_gauge_transport_packet_v0_2D.json"


def load_packet() -> Dict[str, Any]:
    with PACKET_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    handoff = build_and_validate_planos_transport_handoff(load_packet())
    print(json.dumps({"planos_handoff": handoff}, indent=2, ensure_ascii=False, sort_keys=True))
    return 1 if handoff.get("validation_errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
