#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "specs" / "kustring_runtime_bundle_v0_2.generated.json"

PREPARE_COMMANDS: list[list[str]] = [
    [sys.executable, "examples/kustring_runtime_v0_2.py"],
    [sys.executable, "-m", "unittest", "tests/test_kustring_runtime_v0_2.py"],
    [sys.executable, "scripts/eval_kustring_runtime_packets_v0_2.py"],
    [sys.executable, "scripts/eval_kustring_runtime_packets_v0_2.py", "--json"],
    [sys.executable, "scripts/check_kustring_runtime_audit_v0_2.py"],
    [sys.executable, "scripts/check_kustring_runtime_audit_chain_v0_2.py"],
    [sys.executable, "scripts/check_kustring_runtime_worm_receipt_v0_2.py"],
]

FILES = [
    "examples/kustring_runtime_v0_2.py",
    "tests/test_kustring_runtime_v0_2.py",
    "specs/kustring_runtime_packets_v0_2.json",
    "scripts/eval_kustring_runtime_packets_v0_2.py",
    "scripts/export_kustring_runtime_audit_v0_2.py",
    "scripts/check_kustring_runtime_audit_v0_2.py",
    "scripts/build_kustring_runtime_audit_chain_v0_2.py",
    "scripts/check_kustring_runtime_audit_chain_v0_2.py",
    "scripts/export_kustring_runtime_worm_receipt_v0_2.py",
    "scripts/check_kustring_runtime_worm_receipt_v0_2.py",
    "scripts/build_kustring_runtime_bundle_v0_2.py",
    "scripts/check_kustring_runtime_bundle_v0_2.py",
    "scripts/build_kustring_runtime_attestation_v0_2.py",
    "scripts/check_kustring_runtime_attestation_v0_2.py",
    "specs/kustring_runtime_audit_events_v0_2.generated.jsonl",
    "specs/kustring_runtime_audit_chain_v0_2.generated.jsonl",
    "specs/kustring_runtime_worm_receipt_v0_2.generated.json",
]


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    return subprocess.run(list(cmd), cwd=ROOT).returncode


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    for cmd in PREPARE_COMMANDS:
        code = run_command(cmd)
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
        "id": "kustring_runtime_bundle_v0_2",
        "version": "0.2",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "authority_note": "runtime_integrity_surface_only",
        "implementation_not_proof": True,
        "files": entries,
        "bundle_root_hash": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
