#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_emptiness_do_two_truths_runtime_audit_chain_v0_1.py"
CHAIN = ROOT / "specs" / "emptiness_do_two_truths_runtime_audit_chain_v0_1.generated.jsonl"
OUT = ROOT / "specs" / "emptiness_do_two_truths_runtime_worm_receipt_v0_1.generated.json"

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}

FALSE_FIELDS = {
    "K_is_object_allowed": False,
    "K_direct_observation_allowed": False,
    "flat_graph_dependent_origination_allowed": False,
    "string_or_brane_identified_with_K_allowed": False,
    "gap_reifies_ultimate_truth_allowed": False,
    "observable_directly_measures_K_allowed": False,
    "paramartha_samvrti_collapse_allowed": False,
}


def chain_root_and_count() -> tuple[str, int]:
    rows = [line for line in CHAIN.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("empty integrated emptiness dependent origination two truths audit chain")
    return json.loads(rows[-1])["entry_hash"], len(rows)


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    root, count = chain_root_and_count()
    receipt = {
        "id": "emptiness_do_two_truths_runtime_worm_receipt_v0_1",
        "version": "0.1",
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_chain": "specs/emptiness_do_two_truths_runtime_audit_chain_v0_1.generated.jsonl",
        "source_chain_root_hash": root,
        "exported_entry_count": count,
        "export_mode": "WORM",
        "retention_policy": "local_fixture_append_only",
        "object_lock_mode": "local_fixture",
        "authority_note": "integrated_emptiness_do_two_truths_worm_receipt_is_record_surface_only",
        "implementation_not_proof": True,
        "triangle": "K -> delta_rel -> String/Brane -> K_perp -> H_world_gap -> two_truths_non_collapse_barrier",
        "mass_gap_bridge_role": "reference_only_non_collapse_barrier",
        **FALSE_FIELDS,
        **FLAGS,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"root: {root}")
    print(f"entries: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
