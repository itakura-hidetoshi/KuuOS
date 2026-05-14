#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "examples" / "dependent_origination_sheaf_gauge_runtime_v0_2.py"
INP = ROOT / "specs" / "dependent_origination_sheaf_gauge_runtime_claims_v0_2.json"
OUT = ROOT / "specs" / "do_sheaf_gauge_runtime_audit_events_v0_2.generated.jsonl"

spec = importlib.util.spec_from_file_location("do_sheaf_gauge_runtime_v0_2", RUNTIME)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load sheaf gauge runtime")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def h(obj: Any) -> str:
    data = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def event(claim_id: str, claim: dict[str, Any]) -> dict[str, Any]:
    result = mod.evaluate_sheaf_gauge_dependent_origination(mod.SheafGaugeDependentOriginationClaim(**claim))
    payload = {
        "runtime": "dependent_origination_sheaf_gauge_runtime_v0_2",
        "claim_id": claim_id,
        "status": result["status"],
        "reason": result["reason"],
        "principle": result["principle"],
        "graph_only_model_allowed": result["graph_only_model_allowed"],
        "site_cover_required": result["site_cover_required"],
        "gluing_required": result["gluing_required"],
        "gauge_connection_required": result["gauge_connection_required"],
        "holonomy_record_required": result["holonomy_record_required"],
        "curvature_visibility_required": result["curvature_visibility_required"],
        **{k: result[k] for k in FLAGS},
    }
    return {"event_id": h(payload), "timestamp": "2026-05-14T00:00:00Z", **payload}


def main() -> int:
    data = json.loads(INP.read_text(encoding="utf-8"))
    rows = [event(x.get("id", "unnamed"), x.get("claim", {})) for x in data.get("claims", [])]
    OUT.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows), encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"events: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
