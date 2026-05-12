#!/usr/bin/env python3
"""
run_core_governance_full_checks_v0_1.py

Stdlib-only full check runner for KuuOS Core Governance layers.

Runs Emptiness / Dependent Origination / Two Truths / Middle Way,
including core audit event, hash-chain, WORM receipt, and bundle validation,
Mandala Multi-WORLD, Bodhisattva Ten Paramita, Paramita Repair Router,
Dukkha Mathematical Model, Dukkha-as-Qi, Formal Invariant Spine,
Super-Relativity Invariant Bridge, Invariant Preservation Matrix, Invariant Gate,
and Invariant Governance Pipeline validators.
No external dependencies and no external API calls.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/validate_emptiness_middle_way_core_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_audit_event_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_audit_hash_chain_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_audit_worm_export_receipt_v0_1.py"],
    [sys.executable, "scripts/validate_emptiness_middle_way_core_bundle_v0_1.py"],
    [sys.executable, "scripts/validate_mandala_multi_world_v0_1.py"],
    [sys.executable, "scripts/validate_bodhisattva_ten_paramita_v0_1.py"],
    [sys.executable, "scripts/validate_paramita_repair_router_v0_1.py"],
    [sys.executable, "scripts/validate_paramita_repair_router_fixtures_v0_1.py"],
    [sys.executable, "scripts/validate_dukkha_mathematical_model_v0_1.py"],
    [sys.executable, "scripts/validate_dukkha_model_fixtures_v0_1.py"],
    [sys.executable, "scripts/validate_dukkha_as_qi_mode_v0_1.py"],
    [sys.executable, "scripts/validate_formal_invariant_spine_v0_1.py"],
    [sys.executable, "scripts/validate_super_relativity_invariant_bridge_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_preservation_matrix_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_preservation_matrix_fixtures_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_gate_fixtures_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_governance_pipeline_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_governance_pipeline_fixtures_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_pipeline_audit_event_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_pipeline_audit_hash_chain_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_pipeline_audit_worm_export_receipt_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_pipeline_bundle_closure_inclusion_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_pipeline_release_attestation_v0_1.py"],
    [sys.executable, "scripts/validate_invariant_pipeline_release_closure_packet_v0_1.py"],
    [sys.executable, "scripts/check_invariant_pipeline_finality_packet_v0_1.py"],
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

    print("\nPASS: KuuOS core governance full checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
