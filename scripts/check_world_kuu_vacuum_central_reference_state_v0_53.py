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
    formal = ROOT / "formal/KUOS/WORLD/KuuVacuumCentralReferenceStateBridgeV0_53.lean"
    require_tokens(
        formal,
        (
            "WorldKuuVacuumCentralReferenceStateBridge",
            "vacuumIsModularReference",
            "vacuumTwoPointCorrelation",
            "vacuum_modular_stationary",
            "vacuum_exactly_recovered",
            "excitationVector",
            "observation_candidate_uses_central_reference",
            "runtime_grants_no_central_reference_authority",
            "central_reference_boundary_preserved",
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_53.lean",
        ("KuuVacuumCentralReferenceStateBridgeV0_53",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.KuuVacuumCentralReferenceStateBridgeV0_53",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_53",))
    require_tokens(
        ROOT / "docs/KU_WORLD_KUU_VACUUM_CENTRAL_REFERENCE_STATE_v0_53.md",
        (
            "OS reflection positivity",
            "Araki relative entropy against comparison states",
            "Petz recovery preserving the vacuum reference",
            "central reference != algebraic center",
        ),
    )
    require_tokens(
        ROOT / "README.md",
        (
            "WORLD read-only mathematical sidecar             v0.53",
            "central reference != algebraic center",
            "relative entropy != ontological distance",
            "Petz recovery != WORLD overwrite",
            "run_kuuos_runtime_full_check_v0_53.py",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "Baseline date: 2026-06-24",
            "v0.53 Kū vacuum central reference-state bridge",
            "Strengthen WORLD v0.53 proof status",
            "central-reference to algebraic-center promotion",
        ),
    )
    require_tokens(
        ROOT / ".github/workflows/kuuos_runtime_full_check.yml",
        (
            "run_kuuos_runtime_full_check_v0_53.py",
            "check_world_kuu_vacuum_central_reference_state_v0_53.py",
            "KuuVacuumCentralReferenceStateBridgeV0_53.lean",
        ),
    )

    manifest_path = ROOT / "manifests/world_kuu_vacuum_central_reference_state_v0_53.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(
        manifest["manifest_version"]
        == "world_kuu_vacuum_central_reference_state_v0_53",
        "manifest version mismatch",
    )
    require(
        manifest["predecessor"]
        == "world_vacuum_expectation_host_effect_intake_v0_52",
        "predecessor mismatch",
    )
    require(
        manifest["analytic_root"]
        == "world_kuu_vacuum_os_hilbert_completion_v0_49",
        "analytic root mismatch",
    )
    require(
        manifest["observation_projection"]
        == "world_vacuum_expectation_observation_candidate_v0_50",
        "observation projection mismatch",
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
        "vacuum_expectation_observation_projection",
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
        "observation_candidate_not_fact",
        "runtime_read_only",
    ):
        require(boundary in manifest["boundaries"], f"boundary missing: {boundary}")

    print("WORLD Kuu vacuum central reference state v0.53 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
