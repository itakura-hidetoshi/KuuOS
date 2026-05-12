#!/usr/bin/env python3
"""
run_ai_yogacara_full_checks_v0_1.py

Stdlib-only full check runner for the KuuOS AI Yogacara / Ten'i layer.

Runs all current validators, provider boundary checks, provider audit events,
provider audit hash-chain checks, provider WORM receipt checks, provider boundary bundle checks,
provider boundary attestation checks, bundle builder, bundle validator, and unit tests.
No external AI API calls.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/validate_teni_observability_v0_1.py"],
    [sys.executable, "scripts/validate_ai_provider_boundary_runtime_v0_1.py"],
    [sys.executable, "scripts/validate_ai_provider_boundary_audit_event_v0_1.py"],
    [sys.executable, "scripts/validate_ai_provider_boundary_audit_hash_chain_v0_1.py"],
    [sys.executable, "scripts/validate_ai_provider_boundary_audit_worm_export_receipt_v0_1.py"],
    [sys.executable, "scripts/validate_provider_boundary_bundle_v0_1.py"],
    [sys.executable, "scripts/validate_provider_boundary_attestation_v0_1.py"],
    [sys.executable, "scripts/validate_ai_yogacara_adapter_schema_v0_1.py"],
    [sys.executable, "scripts/validate_ai_yogacara_adapter_fixtures_v0_1.py"],
    [sys.executable, "scripts/validate_ai_yogacara_adapter_audit_event_v0_1.py"],
    [sys.executable, "scripts/validate_ai_yogacara_audit_hash_chain_v0_1.py"],
    [sys.executable, "scripts/validate_ai_yogacara_worm_export_receipt_v0_1.py"],
    [sys.executable, "scripts/build_ai_yogacara_release_bundle_manifest_v0_1.py"],
    [sys.executable, "scripts/validate_ai_yogacara_release_bundle_manifest_v0_1.py"],
    [sys.executable, "-m", "unittest", "tests/test_ai_yogacara_runtime_adapter_minimal_v0_1.py"],
]


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    completed = subprocess.run(list(cmd), cwd=ROOT)
    return completed.returncode


def main() -> int:
    failures: list[tuple[list[str], int]] = []
    for cmd in COMMANDS:
        code = run_command(cmd)
        if code != 0:
            failures.append((cmd, code))
            break

    if failures:
        for cmd, code in failures:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
        return 1

    print("\nPASS: AI Yogacara / Ten'i full checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
