#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_emptiness_do_two_truths_runtime_audit_chain_v0_1.py"
CHAIN = ROOT / "specs" / "emptiness_do_two_truths_runtime_audit_chain_v0_1.generated.jsonl"
FALSE_FIELDS = [
    "K_is_object_allowed",
    "K_direct_observation_allowed",
    "flat_graph_dependent_origination_allowed",
    "string_or_brane_identified_with_K_allowed",
    "gap_reifies_ultimate_truth_allowed",
    "observable_directly_measures_K_allowed",
    "paramartha_samvrti_collapse_allowed",
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def canonical_hash(obj: Any) -> str:
    data = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    prev = "GENESIS"
    rows = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not rows:
        errors.append("empty audit chain")
    for i, raw in enumerate(rows, start=1):
        entry = json.loads(raw)
        if entry.get("sequence") != i:
            errors.append(f"line {i}: sequence mismatch")
        if entry.get("previous_hash") != prev:
            errors.append(f"line {i}: previous_hash mismatch")
        if entry.get("event_hash") != canonical_hash(entry.get("event")):
            errors.append(f"line {i}: event_hash mismatch")
        payload = {"sequence": entry.get("sequence"), "previous_hash": entry.get("previous_hash"), "event_hash": entry.get("event_hash")}
        if entry.get("entry_hash") != canonical_hash(payload):
            errors.append(f"line {i}: entry_hash mismatch")
        event = entry.get("event", {})
        if event.get("mass_gap_bridge_role") != "reference_only_non_collapse_barrier":
            errors.append(f"line {i}: mass_gap_bridge_role mismatch")
        for field in FALSE_FIELDS:
            if event.get(field) is not False:
                errors.append(f"line {i}: {field} must be false")
        prev = entry.get("entry_hash")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"PASS: Integrated emptiness DO two truths audit chain checked root={prev} entries={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
