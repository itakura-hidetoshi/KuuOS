#!/usr/bin/env python3
"""Validate Physical Quantum Qi Trajectory Phase Transition Detector packet v0.2P."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_trajectory_phase_transition_detector_v0_2P import (  # noqa: E402
    build_qi_trajectory_phase_transition_candidate,
    validate_qi_trajectory_phase_transition_detector_packet,
)

DEFAULT_PACKET = ROOT / "examples" / "physical_quantum_qi_trajectory_phase_transition_detector_packet_v0_2P.json"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    packet = load_json(path)
    errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
    result = build_qi_trajectory_phase_transition_candidate(packet)

    if errors:
        print("Physical Quantum Qi Trajectory Phase Transition Detector v0.2P validation failed:")
        for err in errors:
            print(f"- {err}")
        print(json.dumps({"phase_transition": result}, indent=2, ensure_ascii=False, sort_keys=True))
        return 1

    print("Physical Quantum Qi Trajectory Phase Transition Detector v0.2P validation passed.")
    print(json.dumps({"phase_transition": result}, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
