#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "specs" / "two_truths_runtime_bundle_v0_1.generated.json"
FORBIDDEN = "for" + "bidden"

PRECHECKS = [
    [sys.executable, "examples/two_truths_mass_gap_runtime_adapter_minimal.py"],
    [sys.executable, "examples/two_truths_runtime_v0_1.py"],
    [sys.executable, "scripts/eval_two_truths_runtime_claims_v0_1.py"],
    [sys.executable, "scripts/eval_two_truths_runtime_claims_v0_1.py", "--json"],
    [sys.executable, "scripts/check_two_truths_runtime_audit_chain_v0_1.py"],
    [sys.executable, "scripts/check_two_truths_runtime_worm_receipt_v0_1.py"],
    [sys.executable, "-m", "unittest", "tests/test_two_truths_runtime_v0_1.py"],
]

FILES = [
    "examples/two_truths_mass_gap_runtime_adapter_minimal.py",
    "examples/two_truths_runtime_v0_1.py",
    "tests/test_two_truths_runtime_v0_1.py",
    "specs/two_truths_runtime_claims_v0_1.json",
    "scripts/eval_two_truths_runtime_claims_v0_1.py",
    "scripts/export_two_truths_runtime_audit_v0_1.py",
    "scripts/build_two_truths_runtime_audit_chain_v0_1.py",
    "scripts/check_two_truths_runtime_audit_chain_v0_1.py",
    "scripts/export_two_truths_runtime_worm_receipt_v0_1.py",
    "scripts/check_two_truths_runtime_worm_receipt_v0_1.py",
    "specs/two_truths_runtime_audit_events_v0_1.generated.jsonl",
    "specs/two_truths_runtime_audit_chain_v0_1.generated.jsonl",
    "specs/two_truths_runtime_worm_receipt_v0_1.generated.json",
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_prechecks() -> int:
    for cmd in PRECHECKS:
        print("\n>>> " + " ".join(cmd), flush=True)
        code = subprocess.run(cmd, cwd=ROOT).returncode
        if code != 0:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
            return code
    return 0


def main() -> int:
    code = run_prechecks()
    if code != 0:
        return code
    entries = []
    for rel in sorted(FILES):
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        entries.append({"path": rel, "sha256": sha256_file(path), "size_bytes": path.stat().st_size})
    payload = "".join(e["path"] + e["sha256"] for e in entries)
    manifest = {
        "id": "two_truths_runtime_bundle_v0_1",
        "version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "authority_note": "two_truths_runtime_integrity_surface_only",
        "implementation_not_proof": True,
        "adapter": "examples/two_truths_mass_gap_runtime_adapter_minimal.py",
        "mass_gap_bridge_role": "reference_only_non_collapse_barrier",
        "mass_gap_bridge_authority": FORBIDDEN,
        "paramartha_objectification_allowed": False,
        "samvrti_denial_allowed": False,
        "ultimate_to_conventional_collapse_allowed": False,
        "conventional_to_ultimate_collapse_allowed": False,
        "files": entries,
        "bundle_root_hash": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
