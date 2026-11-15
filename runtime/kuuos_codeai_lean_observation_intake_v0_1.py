"""MemoryOS read-only GitHub evidence seed intake. No Git/Lean authority."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Mapping

from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import (
    ENTRY_VERSION, make_case,
)

MANIFEST_VERSION = "memoryos_codeai_lean_observations_v0_1"

def read_observation_seed(path: str | Path) -> list[dict]:
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    if (not isinstance(manifest, Mapping)
        or manifest.get("profile") != MANIFEST_VERSION
        or manifest.get("authority") != "external_pointer_only"
        or manifest.get("repository") != "itakura-hidetoshi/KuuOS"):
        raise ValueError("MemoryOS external GitHub seed governance mismatch")
    rows = manifest.get("observations")
    if not isinstance(rows, list) or not rows:
        raise ValueError("MemoryOS seed has no observations")
    names = {"source_head", "source_tree", "imported_blob", "variant",
             "candidate_blob", "producer_run", "outcome", "errors"}
    result, seen = [], set()
    for row in rows:
        if not isinstance(row, Mapping) or set(row) != names:
            raise ValueError("MemoryOS missing/extra observation fields")
        if not isinstance(row["errors"], list) or not all(isinstance(x, str) for x in row["errors"]):
            raise ValueError("MemoryOS observations need actual diagnostic strings")
        case = make_case(**row)
        if case["id"] in seen:
            raise ValueError("MemoryOS observation duplicate")
        result.append(case)
        seen.add(case["id"])
    return result

def checked_independent_pointers(path: str | Path) -> list[dict]:
    """Only source pointers. The pointer list cannot certify a theorem."""
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = manifest.get("independent_certification_pointers")
    if not isinstance(rows, list):
        raise ValueError("MemoryOS independent pointers malformed")
    out=[]
    for item in rows:
        if not isinstance(item, dict) or set(item) != {"scope","run_id","exact_source_blob","certified_head"}:
            raise ValueError("MemoryOS independent pointer schema changed")
        out.append({**item,"requires_external_completed_CI_reobservation":True,
                    "grant_proof_authority":False})
    return out
