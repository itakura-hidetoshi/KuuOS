#!/usr/bin/env python3
"""Run the Physical Quantum Qi phase classifier on the v0.2 equation packet.

This is a runtime-facing demo, not a governance packet. It loads the
machine-readable equation packet and computes the Qi phase:

NonQi -> PreQi -> ProtoQi -> BoundaryQi -> TransportQi -> PhysicalQi -> FullPathQi
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_phase_runtime_v0_2 import (  # noqa: E402
    classify_qi_phase,
    result_to_dict,
    state_from_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_equation_packet_v0_2.json"


def main() -> int:
    with PACKET_PATH.open("r", encoding="utf-8") as f:
        packet = json.load(f)

    state = state_from_packet(packet)
    result = classify_qi_phase(state)
    print(json.dumps(result_to_dict(result), ensure_ascii=False, indent=2))

    if result.phase.value != "FullPathQi":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
