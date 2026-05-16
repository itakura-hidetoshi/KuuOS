#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
from fractions import Fraction
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "examples" / "kustring_runtime_v0_2.py"
PACKETS = ROOT / "specs" / "kustring_runtime_packets_v0_2.json"
OUT = ROOT / "specs" / "kustring_runtime_audit_events_v0_2.generated.jsonl"

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}


def load_runtime() -> Any:
    spec = importlib.util.spec_from_file_location("kustring_runtime_v0_2", RUNTIME_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load runtime module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def coerce_value(key: str, value: Any) -> Any:
    if key == "psi_gap" and isinstance(value, str):
        return Fraction(value)
    return value


def main() -> int:
    runtime = load_runtime()
    data = json.loads(PACKETS.read_text(encoding="utf-8"))
    events = []
    for sequence, item in enumerate(data.get("packets", []), start=1):
        packet_id = item.get("id", f"packet_{sequence}")
        packet_data = item.get("packet", {})
        packet = runtime.Packet(**{key: coerce_value(key, value) for key, value in packet_data.items()})
        result = runtime.evaluate(packet)
        event = {
            "event_id": f"kustring_runtime_v0_2:{sequence}:{packet_id}",
            "sequence": sequence,
            "runtime": "kustring_runtime_v0_2",
            "packet_id": packet_id,
            "expected_status": item.get("expected_status"),
            "status": result.get("status"),
            "reason": result.get("reason"),
            "gap": result.get("gap"),
            "gap_domain": result.get("gap_domain"),
            "centered_observable": result.get("centered_observable"),
            "authority_note": "runtime_audit_event_is_record_surface_only",
            **FLAGS,
        }
        events.append(event)

    OUT.write_text("".join(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n" for e in events), encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"events: {len(events)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())