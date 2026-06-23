#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/KuuVacuumOSHilbertCompletionBridgeV0_49.lean"
    text = formal.read_text(encoding="utf-8")
    required = (
        "WorldKuuVacuumOSHilbertCompletionBridge",
        "osReflectionPositive",
        "osHilbertIdentification",
        "kuuVacuum",
        "vacuumState_positive",
        "modular_vacuum_invariant",
        "physical_vacuum_invariant",
        "kuu_vacuum_mem_vacuumSector",
        "runtime_grants_no_vacuum_authority",
        "vacuum_representation_boundary_preserved",
    )
    for token in required:
        assert token in text, token
    print("world_kuu_vacuum_os_hilbert_completion_v0_49 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
