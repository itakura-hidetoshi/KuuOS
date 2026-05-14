#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/run_emptiness_runtime_checks_v0_1.py"],
    [sys.executable, "scripts/run_dependent_origination_runtime_checks_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_vacuum_normalization_v0_1.py"],
    [sys.executable, "scripts/validate_kustring_mgap4d_emptiness_core_v0_2.py"],
    [sys.executable, "scripts/run_kustring_runtime_checks_v0_2.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_audit_event_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_audit_hash_chain_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_audit_worm_export_receipt_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_bundle_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_attestation_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_closure_packet_v0_1.py"],
]


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    return subprocess.run(list(cmd), cwd=ROOT).returncode


def main() -> int:
    for cmd in COMMANDS:
        code = run_command(cmd)
        if code != 0:
            print(f"FAIL: {' '.join(cmd)} exited with {code}")
            return code
    print("\nPASS: Emptiness Middle Way core full checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
