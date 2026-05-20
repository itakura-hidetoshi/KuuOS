#!/usr/bin/env python3
"""Run the KuuOS Qi motion chain checks v0.1.

This runner orders the current Qi implementation checks from conventional Qi
observation through KuString bridge projection, bridge release/finality/baseline
validation, conservative evidence building, physical classification, dynamics
licensing, and motion pipeline validation.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]

CHECKS: List[Tuple[str, str]] = [
    ("samvrti-adapter", "examples/samvrti_qi_runtime_adapter_minimal.py"),
    ("samvrti-validator", "scripts/validate_samvrti_qi_runtime_v0_1.py"),
    ("kustring-qi-bridge", "examples/kustring_qi_bridge_minimal.py"),
    ("kustring-qi-bridge-validator", "scripts/validate_kustring_qi_bridge_v0_1.py"),
    (
        "kustring-qi-bridge-release-bundle",
        "scripts/validate_kustring_qi_bridge_release_bundle_v0_1.py",
    ),
    (
        "kustring-qi-bridge-finality",
        "scripts/check_kustring_qi_bridge_finality_packet_v0_1.py",
    ),
    (
        "kustring-qi-bridge-chain-index",
        "scripts/check_kustring_qi_bridge_chain_index_v0_1.py",
    ),
    (
        "samvrti-to-physical-motion-builder",
        "examples/samvrti_qi_to_physical_motion_evidence_builder_minimal.py",
    ),
    (
        "samvrti-to-physical-motion-builder-validator",
        "scripts/validate_samvrti_qi_to_physical_motion_evidence_builder_v0_1.py",
    ),
    (
        "physical-quantum-qi-runtime-contract",
        "scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py",
    ),
    (
        "physical-quantum-qi-runtime-release-packet",
        "scripts/validate_physical_quantum_qi_runtime_release_packet_v0_1.py",
    ),
    (
        "physical-quantum-qi-dynamics-kernel",
        "examples/physical_quantum_qi_dynamics_kernel_minimal.py",
    ),
    (
        "physical-quantum-qi-dynamics-validator",
        "scripts/validate_physical_quantum_qi_dynamics_kernel_v0_1.py",
    ),
    (
        "physical-quantum-qi-motion-pipeline",
        "examples/physical_quantum_qi_motion_pipeline_minimal.py",
    ),
    (
        "physical-quantum-qi-motion-pipeline-validator",
        "scripts/validate_physical_quantum_qi_motion_pipeline_v0_1.py",
    ),
]


def fail(message: str) -> int:
    print(f"[qi-motion-chain] FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    for label, rel_path in CHECKS:
        path = ROOT / rel_path
        if not path.exists():
            return fail(f"missing check {label}: {rel_path}")
        print(f"[qi-motion-chain] RUN {label}: {rel_path}")
        result = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), check=False)
        if result.returncode != 0:
            return fail(f"check failed {label}: {rel_path}")

    print("[qi-motion-chain] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())