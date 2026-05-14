#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "examples" / "two_truths_runtime_v0_1.py"
CLAIMS = ROOT / "specs" / "two_truths_runtime_claims_v0_1.json"
OUT = ROOT / "specs" / "two_truths_runtime_audit_events_v0_1.generated.jsonl"

spec = importlib.util.spec_from_file_location("two_truths_runtime_v0_1", RUNTIME_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load two truths runtime module")
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
    result = runtime.evaluate_two_truths(runtime.TwoTruthsClaim(**claim_data))
    bridge_decision = result.get("bridge_decision", {})
    payload = {
        "runtime": "two_truths_runtime_v0_1",
        "adapter": "examples/two_truths_mass_gap_runtime_adapter_minimal.py",
        "claim_id": claim_id,
        "status": result["status"],
        "reason": result["reason"],
        "principle": result["principle"],
        "paramartha_objectification_allowed": result["paramartha_objectification_allowed"],
        "samvrti_denial_allowed": result["samvrti_denial_allowed"],
        "ultimate_to_conventional_collapse_allowed": result["ultimate_to_conventional_collapse_allowed"],
        "conventional_to_ultimate_collapse_allowed": result["conventional_to_ultimate_collapse_allowed"],
        "mass_gap_bridge_authority": result["mass_gap_bridge_authority"],
        "mass_gap_reference_barrier_status": result["mass_gap_reference_barrier_status"],
        "bridge_decision_status": bridge_decision.get("decision_status"),
        "bridge_final_theorem_authority": bridge_decision.get("final_theorem_authority"),
        "bridge_execution_authority": bridge_decision.get("execution_authority"),
        **{flag: result[flag] for flag in FLAGS},
    }
    return {
        "event_id": canonical_hash(payload),
        "timestamp": "2026-05-15T00:00:00Z",
        **payload,
    }


def main() -> int:
    data = json.loads(CLAIMS.read_text(encoding="utf-8"))
    rows = [make_event(item.get("id", "unnamed"), item.get("claim", {})) for item in data.get("claims", [])]
    OUT.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"events: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
