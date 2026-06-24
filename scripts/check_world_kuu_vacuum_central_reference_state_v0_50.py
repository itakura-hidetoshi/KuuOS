#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/KuuVacuumCentralReferenceStateBridgeV0_50.lean"
    require_tokens(
        formal,
        (
            "WorldKuuVacuumCentralReferenceStateBridge",
            "vacuumIsModularReference",
            "vacuumTwoPointCorrelation",
            "vacuum_modular_stationary",
            "vacuum_exactly_recovered",
            "excitationVector",
            "runtime_grants_no_central_reference_authority",
            "central_reference_boundary_preserved",
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_50.lean",
        ("KuuVacuumCentralReferenceStateBridgeV0_50",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.KuuVacuumCentralReferenceStateBridgeV0_50",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_50",))
    require_tokens(
        ROOT / "docs/KU_WORLD_KUU_VACUUM_CENTRAL_REFERENCE_STATE_v0_50.md",
        (
            "OS reflection positivity",
            "relative entropy against comparison states",
            "Petz recovery preserving the vacuum reference",
            "central reference != algebraic center",
        ),
    )

    manifest_path = ROOT / "manifests/world_kuu_vacuum_central_reference_state_v0_50.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(
        manifest["manifest_version"]
        == "world_kuu_vacuum_central_reference_state_v0_50",
        "manifest version mismatch",
    )
    require(
        manifest["predecessor"]
        == "world_kuu_vacuum_os_hilbert_completion_v0_49",
        "predecessor mismatch",
    )
    for path_key in (
        "formal_module",
        "formal_root",
        "documentation",
        "validator",
        "full_check",
        "workflow",
    ):
        relative = manifest[path_key]
        require((ROOT / relative).is_file(), f"manifest path missing: {relative}")
    for surface in (
        "os_reflection_positivity",
        "completed_hilbert_vacuum",
        "vacuum_correlations",
        "modular_reference_state",
        "araki_relative_entropy",
        "petz_recovery",
        "vacuum_generated_excitations",
    ):
        require(surface in manifest["unified_surfaces"], f"surface missing: {surface}")
    for boundary in (
        "central_reference_not_algebraic_center",
        "vacuum_not_truth_authority",
        "excitation_not_truth_authority",
        "relative_entropy_not_ontological_distance",
        "petz_recovery_not_world_overwrite",
        "modular_time_not_physical_time",
        "world_not_vacuum",
        "kuu_not_zero_vector",
        "runtime_read_only",
    ):
        require(boundary in manifest["boundaries"], f"boundary missing: {boundary}")

    print("WORLD Kuu vacuum central reference state v0.50 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
