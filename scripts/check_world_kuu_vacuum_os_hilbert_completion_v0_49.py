#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def require_tokens(path: pathlib.Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/KuuVacuumOSHilbertCompletionBridgeV0_49.lean"
    require_tokens(
        formal,
        (
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
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_49.lean",
        ("KuuVacuumOSHilbertCompletionBridgeV0_49",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.KuuVacuumOSHilbertCompletionBridgeV0_49",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_49",))
    require_tokens(
        ROOT / "docs/KU_WORLD_KUU_VACUUM_OS_HILBERT_COMPLETION_v0_49.md",
        ("Kū != zero vector", "modular time != physical time"),
    )

    # Public orientation is a moving current-baseline surface. Historical
    # validators therefore check invariant boundaries rather than requiring
    # README or ROADMAP to continue presenting v0.49 as the current version.
    require_tokens(
        ROOT / "README.md",
        (
            "WORLD read-only mathematical sidecar",
            "analytic vacuum != exact WORLD",
            "modular time != physical time",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "Baseline date: 2026-06-23",
            "WORLD mathematical sidecar",
            "modular-time and physical-time invariance",
        ),
    )
    assert (ROOT / "scripts/run_kuuos_runtime_full_check_v0_49.py").is_file()

    manifest_path = ROOT / "manifests/world_kuu_vacuum_os_hilbert_completion_v0_49.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "world_kuu_vacuum_os_hilbert_completion_v0_49"
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_49.lean"
    assert manifest["formal_module"] == str(formal.relative_to(ROOT))
    assert "runtime_read_only" in manifest["boundaries"]
    assert "modular_time_not_physical_time" in manifest["boundaries"]

    print("world_kuu_vacuum_os_hilbert_completion_v0_49 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
