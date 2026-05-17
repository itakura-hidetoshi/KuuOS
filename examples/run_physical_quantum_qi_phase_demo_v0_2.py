#!/usr/bin/env python3
"""Run the Physical Quantum Qi phase classifier and OS bridge demo v0.2.

This is a runtime-facing demo, not a governance packet. It loads the
machine-readable equation packet and computes:

1. Qi phase:
   NonQi -> PreQi -> ProtoQi -> BoundaryQi -> TransportQi -> PhysicalQi -> FullPathQi

2. KuuOS handoff surface:
   FullPathQi -> DecisionOS safety evaluation, MemoryOS recordable history,
   and ReflectionOS residue analysis, without execution or commit authority.

3. OS bridge packet:
   A concrete candidate-only payload for BeliefOS, PlanOS, DecisionOS,
   MemoryOS, and ReflectionOS.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_phase_runtime_v0_2 import (  # noqa: E402
    classify_qi_phase,
    handoff_to_dict,
    qi_phase_handoff,
    result_to_dict,
    state_from_packet,
)
from physical_quantum_qi_os_bridge_v0_2 import (  # noqa: E402
    bridge_packet_to_dict,
    build_qi_os_bridge_packet,
    validate_qi_os_bridge_packet,
)

PACKET_PATH = ROOT / "examples" / "physical_quantum_qi_equation_packet_v0_2.json"


def main() -> int:
    with PACKET_PATH.open("r", encoding="utf-8") as f:
        packet = json.load(f)

    state = state_from_packet(packet)
    result = classify_qi_phase(state)
    handoff = qi_phase_handoff(result)
    bridge_packet = build_qi_os_bridge_packet(handoff)
    bridge_payload = bridge_packet_to_dict(bridge_packet)
    bridge_errors = validate_qi_os_bridge_packet(bridge_payload)

    payload = {
        "phase_result": result_to_dict(result),
        "handoff": handoff_to_dict(handoff),
        "os_bridge_packet": bridge_payload,
        "os_bridge_validation_errors": bridge_errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if result.phase.value != "FullPathQi":
        return 1
    if handoff.execution_authority or handoff.commit_authority:
        return 1
    if bridge_errors:
        return 1
    if "MemoryOS.recordable_history_candidate" not in handoff.allowed_surfaces:
        return 1
    if "ReflectionOS.residue_analysis_candidate" not in handoff.allowed_surfaces:
        return 1
    if bridge_payload["os_payloads"]["MemoryOS"]["recordable_history_candidate"] is not True:
        return 1
    if bridge_payload["os_payloads"]["ReflectionOS"]["residue_analysis_candidate"] is not True:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
