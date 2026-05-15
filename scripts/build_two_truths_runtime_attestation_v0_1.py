#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUNDLE_BUILDER = ROOT / "scripts" / "build_two_truths_runtime_bundle_v0_1.py"
BUNDLE = ROOT / "specs" / "two_truths_runtime_bundle_v0_1.generated.json"
CHAIN = ROOT / "specs" / "two_truths_runtime_audit_chain_v0_1.generated.jsonl"
WORM = ROOT / "specs" / "two_truths_runtime_worm_receipt_v0_1.generated.json"
OUT = ROOT / "specs" / "two_truths_runtime_attestation_v0_1.generated.json"

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def chain_root() -> str:
    rows = [line for line in CHAIN.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("empty two truths runtime audit chain")
    return json.loads(rows[-1])["entry_hash"]


def main() -> int:
    code = subprocess.run([sys.executable, str(BUNDLE_BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    bundle = read_json(BUNDLE)
    worm = read_json(WORM)
    root = chain_root()
    attestation = {
        "id": "two_truths_runtime_attestation_v0_1",
        "version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "adapter": "examples/two_truths_mass_gap_runtime_adapter_minimal.py",
        "bundle_manifest": "specs/two_truths_runtime_bundle_v0_1.generated.json",
        "bundle_root_hash": bundle["bundle_root_hash"],
        "audit_chain": "specs/two_truths_runtime_audit_chain_v0_1.generated.jsonl",
        "audit_chain_root_hash": root,
        "worm_receipt": "specs/two_truths_runtime_worm_receipt_v0_1.generated.json",
        "worm_receipt_source_chain_root_hash": worm["source_chain_root_hash"],
        "authority_note": "two_truths_runtime_attestation_is_integrity_summary_only",
        "implementation_not_proof": True,
        "mass_gap_bridge_role": "reference_only_non_collapse_barrier",
        "mass_gap_bridge_authority": "forbidden",
        "paramartha_objectification_allowed": False,
        "samvrti_denial_allowed": False,
        "ultimate_to_conventional_collapse_allowed": False,
        "conventional_to_ultimate_collapse_allowed": False,
        **FLAGS,
    }
    OUT.write_text(json.dumps(attestation, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {attestation['bundle_root_hash']}")
    print(f"audit_chain_root_hash: {attestation['audit_chain_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
