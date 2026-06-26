#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str, *tokens: str) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def main() -> int:
    formal = "formal/KUOS/WORLD/KuuVacuumOSHilbertCompletionBridgeV0_49.lean"
    require(formal, "WorldKuuVacuumOSHilbertCompletionBridge", "osReflectionPositive",
            "osHilbertIdentification", "kuuVacuum", "vacuumState_positive",
            "modular_vacuum_invariant", "physical_vacuum_invariant",
            "kuu_vacuum_mem_vacuumSector", "runtime_grants_no_vacuum_authority",
            "vacuum_representation_boundary_preserved")
    require("formal/KuuOSFormalV0_49.lean", "KuuVacuumOSHilbertCompletionBridgeV0_49")
    require("formal/KUOS.lean", "KUOS.WORLD.KuuVacuumOSHilbertCompletionBridgeV0_49")
    require("lakefile.toml", "KuuOSFormalV0_49")
    require("docs/KU_WORLD_KUU_VACUUM_OS_HILBERT_COMPLETION_v0_49.md",
            "Kū != zero vector", "modular time != physical time")
    stable = ("Kū != zero vector", "analytic vacuum != exact WORLD",
              "modular time != physical time")
    require("README.md", *stable)
    require("ROADMAP.md", *stable)
    manifest = json.loads((ROOT / "manifests/world_kuu_vacuum_os_hilbert_completion_v0_49.json").read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "world_kuu_vacuum_os_hilbert_completion_v0_49"
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_49.lean"
    assert manifest["formal_module"] == formal
    assert "runtime_read_only" in manifest["boundaries"]
    assert "modular_time_not_physical_time" in manifest["boundaries"]
    print("world_kuu_vacuum_os_hilbert_completion_v0_49 checks passed")
    return 0


if __name__ == "__main__":
    main()
