#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "examples" / "emptiness_dependent_origination_two_truths_runtime_v0_1.py"
CLAIMS = ROOT / "specs" / "emptiness_do_two_truths_runtime_claims_v0_1.json"
OUT = ROOT / "specs" / "emptiness_do_two_truths_runtime_audit_events_v0_1.generated.jsonl"

spec = importlib.util.spec_from_file_location("emptiness_dependent_origination_two_truths_runtime_v0_1", RUNTIME_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load integrated runtime")
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

FALSE_FIELDS = [
    "K_is_object_allowed",
    "K_direct_observation_allowed",
    "flat_graph_dependent_origination_allowed",
    "string_or_brane_identified_with_K_allowed",
    "gap_reifies_ultimate_truth_allowed",
    "observable_directly_measures_K_allowed",
    "paramartha_samvrti_collapse_allowed",
]


def canonical_hash(obj: Any) -> str:
    data = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def make_event(claim_id: str, claim_data: dict[str, Any]) -> dict[str, Any]:
    result = runtime.evaluate_ku_string_emptiness_do_two_truths(
        runtime.KuStringEmptinessDependentOriginationTwoTruthsClaim(**claim_data)
    )
    payload = {
        "runtime": "emptiness_dependent_origination_two_truths_runtime_v0_1",
        "claim_id": claim_id,
        "status": result["status"],
        "reason": result["reason"],
        "principle": result["principle"],
        "triangle": result["triangle"],
        "mass_gap_bridge_role": result["mass_gap_bridge_role"],
        **{field: result[field] for field in FALSE_FIELDS},
        **{flag: result[flag] for flag in FLAGS},
        "emptiness_status": result["emptiness"]["status"],
        "dependent_origination_status": result["dependent_origination"]["status"],
        "two_truths_status": result["two_truths"]["status"],
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
