#!/usr/bin/env python3
"""Validate Physical Quantum Qi State Transition Kernel packet v0.2N."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_state_transition_kernel_v0_2N import (  # noqa: E402
    build_qi_state_transition_candidate,
    validate_qi_state_transition_packet,
)

DEFAULT_PACKET = ROOT / "examples" / "physical_quantum_qi_state_transition_kernel_packet_v0_2N.json"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    packet = load_json(path)
    errors = validate_qi_state_transition_packet(packet)
    result = build_qi_state_transition_candidate(packet)

    if errors:
        print("Physical Quantum Qi State Transition Kernel v0.2N validation failed:")
        for err in errors:
            print(f"- {err}")
        print(json.dumps({"transition": result}, indent=2, ensure_ascii=False, sort_keys=True))
        return 1

    print("Physical Quantum Qi State Transition Kernel v0.2N validation passed.")
    print(json.dumps({"transition": result}, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
