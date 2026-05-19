#!/usr/bin/env python3
"""Validate Physical Quantum Qi Process Tensor packet v0.2F."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_quantum_qi_process_tensor_runtime_v0_2F import (  # noqa: E402
    build_qi_process_tensor_candidate,
    validate_qi_process_tensor_packet,
)

DEFAULT_PACKET = ROOT / "examples" / "physical_quantum_qi_process_tensor_packet_v0_2F.json"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    packet = load_json(path)
    errors = validate_qi_process_tensor_packet(packet)
    result = build_qi_process_tensor_candidate(packet)

    if errors:
        print("Physical Quantum Qi Process Tensor v0.2F validation failed:")
        for err in errors:
            print(f"- {err}")
        print(json.dumps({"candidate": result}, indent=2, ensure_ascii=False, sort_keys=True))
        return 1

    print("Physical Quantum Qi Process Tensor v0.2F validation passed.")
    print(json.dumps({"candidate": result}, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
