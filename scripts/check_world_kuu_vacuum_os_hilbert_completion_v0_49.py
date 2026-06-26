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

    # Entry documents evolve as the repository baseline advances. Validate only
    # stable semantic boundaries here; version-specific wording belongs to the
    # dedicated v0.49 document above.
    stable_boundaries = (
        "Kū != zero vector",
        "analytic vacuum != exact WORLD",
        "modular time != physical time",
    )
    require_tokens(ROOT / "README.md", stable_boundaries)
    require_tokens(ROOT / "ROADMAP.md", stable_boundaries)

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
