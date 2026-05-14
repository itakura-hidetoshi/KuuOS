#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "examples" / "emptiness_runtime_v0_1.py"
DEFAULT_IN = ROOT / "specs" / "emptiness_runtime_claims_v0_1.json"
DEFAULT_OUT = ROOT / "specs" / "emptiness_runtime_audit_events_v0_1.generated.jsonl"

spec = importlib.util.spec_from_file_location("emptiness_runtime_v0_1", RUNTIME_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load emptiness runtime module")
runtime = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runtime
spec.loader.exec_module(runtime)

FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def make_event(claim_id: str, claim_data: dict[str, Any]) -> dict[str, Any]:
    result = runtime.evaluate_emptiness(runtime.EmptinessClaim(**claim_data))
    payload = {
        "runtime": "emptiness_runtime_v0_1",
        "claim_id": claim_id,
        "status": result["status"],
        "reason": result["reason"],
        "emptiness_ground": result["emptiness_ground"],
        "appearance_space": result["appearance_space"],
        "direct_K_observable": result["direct_K_observable"],
        **{flag: result[flag] for flag in FLAGS},
    }
    return {
        "event_id": canonical_hash(payload),
        "timestamp": "2026-05-13T00:00:00Z",
        **payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_IN.relative_to(ROOT)))
    parser.add_argument("--output", default=str(DEFAULT_OUT.relative_to(ROOT)))
    args = parser.parse_args()

    data = json.loads((ROOT / args.input).read_text(encoding="utf-8"))
    events = [make_event(item.get("id", "unnamed"), item.get("claim", {})) for item in data.get("claims", [])]
    out_path = ROOT / args.output
    out_path.write_text("".join(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n" for e in events), encoding="utf-8")
    print(f"WROTE: {out_path.relative_to(ROOT)}")
    print(f"events: {len(events)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
