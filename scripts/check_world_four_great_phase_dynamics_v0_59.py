#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests/world_four_great_phase_dynamics_v0_59.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(
        manifest["manifest_version"] == "world_four_great_phase_dynamics_v0_59",
        "manifest version mismatch",
    )
    require(
        manifest["predecessor"]
        == "world_kuu_vacuum_araki_hessian_physical_realization_v0_56",
        "predecessor mismatch",
    )
    require(
        manifest["stack_base"] == "world_tomita_conjugate_adjoint_v0_58",
        "stack base mismatch",
    )
    require(
        manifest["analytic_dependency"]
        == "world_kuu_vacuum_araki_hessian_physical_realization_v0_56",
        "analytic dependency mismatch",
    )

    for key in (
        "formal_module",
        "formal_root",
        "aggregate_formal_root",
        "documentation",
        "validator",
        "workflow",
    ):
        require((ROOT / manifest[key]).is_file(), f"missing manifest path: {key}")

    require(
        manifest["four_greats"]
        == {
            "earth": "araki_hessian_stiffness",
            "water": "physical_excitation_gram_correlation",
            "fire": "nonnegative_effective_information_loss_after_coarse_graining",
            "air": "reversible_inner_product_preserving_physical_flow",
        },
        "four-great mapping mismatch",
    )
    require(manifest["scope"]["bounded_generator_araki_hessian"] is True, "earth scope missing")
    require(manifest["scope"]["completed_physical_hilbert_correlation"] is True, "water scope missing")
    require(manifest["scope"]["abstract_reversible_physical_flow"] is True, "air scope missing")
    require(manifest["scope"]["effective_fire_after_coarse_graining"] is True, "fire scope missing")
    require(manifest["scope"]["first_principles_quantum_markov_fire"] is False, "fire promoted")
    require(manifest["scope"]["phase_transition_nonregularity_proved"] is False, "phase transition promoted")
    require(manifest["scope"]["world_state_mutation"] is False, "WORLD mutation promoted")
    require(all(value is False for value in manifest["boundaries"].values()), "boundary promotion")

    require_tokens(
        ROOT / manifest["formal_module"],
        (
            "WorldFourGreatDiagnostic",
            "WorldFourGreatPhaseDynamics",
            "earthStiffness",
            "waterCorrelation",
            "fireLoss_nonnegative",
            "airEvolution",
            "earth_eq_water",
            "air_inverse",
            "air_preserves_physical_inner",
            "diagnostic_earth_eq_water",
            "osContractionIsNotPhysicalFire",
            "readOnlyDiagnostic",
        ),
    )
    require_tokens(
        ROOT / manifest["formal_root"],
        ("FourGreatPhaseDynamicsV0_59",),
    )
    require(
        "KuuOSFormalV0_58" not in (ROOT / manifest["formal_root"]).read_text(encoding="utf-8"),
        "unrelated v0.58 formal root leaked into v0.59 validation",
    )
    require_tokens(
        ROOT / manifest["aggregate_formal_root"],
        ("KUOS.WORLD.FourGreatPhaseDynamicsV0_59",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_59",))
    require_tokens(
        ROOT / manifest["documentation"],
        (
            "地大 = 構造安定性",
            "水大 = 相関形成",
            "火大 = 粗視化後の不可逆情報損失",
            "風大 = 可逆な物理時間輸送",
            "Earth(h) = Water(h)",
            "OS Euclidean contraction != physical Fire",
            "read-only diagnosis != execution authority",
        ),
    )

    print("WORLD v0.59 four-great phase dynamics checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
