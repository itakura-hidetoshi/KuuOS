#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "world_kuu_vacuum_information_geometry_v0_55"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    manifest_path = ROOT / "manifests/world_kuu_vacuum_information_geometry_v0_55.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["manifest_version"] == VERSION, "manifest version mismatch")
    require(
        manifest["predecessor"] == "world_kuu_vacuum_central_reference_state_v0_54",
        "predecessor mismatch",
    )
    for key in (
        "formal_module",
        "formal_root",
        "aggregate_formal_root",
        "documentation",
        "validator",
        "full_check",
        "workflow",
    ):
        require((ROOT / manifest[key]).is_file(), f"manifest file missing: {key}")

    expected_spine = [
        "completed_hilbert_vacuum",
        "central_vacuum_state",
        "vacuum_parameter_origin",
        "araki_relative_entropy_hessian",
        "quantum_fisher_metric",
        "hilbert_excitation_gram_form",
        "petz_recovered_tangent",
        "information_loss_pythagorean_decomposition",
    ]
    require(manifest["information_geometric_spine"] == expected_spine, "spine mismatch")
    require(all(value is False for value in manifest["boundaries"].values()), "boundary mismatch")

    formal = ROOT / manifest["formal_module"]
    require_tokens(
        formal,
        (
            "WorldKuuVacuumInformationGeometryBridge",
            "vacuumParameter",
            "vacuumTangentExcitation",
            "vacuumInformationDivergence",
            "vacuumInformationLoss",
            "vacuumRecoveredTangent",
            "vacuum_divergence_zero_iff",
            "araki_from_vacuum_zero_iff",
            "vacuum_excitation_gram_eq_araki_hessian",
            "vacuum_information_loss_zero_iff_recoverable",
            "vacuum_recovered_pythagorean",
            "vacuum_recovered_observable_is_petz_channel",
            "vacuum_information_geometry_boundary_preserved",
        ),
    )
    require_tokens(ROOT / manifest["formal_root"], ("KuuVacuumInformationGeometryBridgeV0_55",))
    require_tokens(ROOT / manifest["aggregate_formal_root"], ("KUOS.WORLD.KuuVacuumInformationGeometryBridgeV0_55",))
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_55",))

    documentation = ROOT / manifest["documentation"]
    require_tokens(
        documentation,
        (
            "非可換情報幾何",
            "真空基準パラメータ",
            "Araki相対エントロピー",
            "量子Fisher計量",
            "励起方向",
            "Petz回復",
            "Pythagoras分解",
            "vacuum parameter != exact WORLD",
            "zero divergence != ontological identity",
            "modular time != physical time",
        ),
    )

    predecessor_path = ROOT / "manifests/world_kuu_vacuum_central_reference_state_v0_54.json"
    predecessor = json.loads(predecessor_path.read_text(encoding="utf-8"))
    require(predecessor["manifest_version"] == manifest["predecessor"], "predecessor manifest mismatch")

    print("WORLD Kuu vacuum information geometry v0.55 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
