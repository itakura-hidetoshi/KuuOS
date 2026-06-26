#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests/world_four_great_phase_transition_declaration_v0_60.json"


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
        manifest["manifest_version"]
        == "world_four_great_phase_transition_declaration_v0_60",
        "manifest version mismatch",
    )
    require(
        manifest["predecessor"] == "world_four_great_phase_dynamics_v0_59",
        "predecessor mismatch",
    )

    for key in (
        "criteria_module",
        "declaration_module",
        "formal_root",
        "canonical_root",
        "aggregate_formal_root",
        "documentation",
        "validator",
        "workflow",
    ):
        require((ROOT / manifest[key]).is_file(), f"missing manifest path: {key}")

    require(
        manifest["declaration_channels"]
        == [
            "free_energy_nonanalyticity",
            "spectral_gap_closure",
            "fixed_point_subalgebra_change",
        ],
        "declaration channels mismatch",
    )
    require(
        manifest["hierarchy"]["strict_declaration"]
        == "three_channels_plus_four_great_change",
        "strict hierarchy mismatch",
    )
    require(all(value is False for value in manifest["boundaries"].values()),
            "boundary promotion")

    criteria = ROOT / manifest["criteria_module"]
    require_tokens(
        criteria,
        (
            "WorldFourGreatCoordinateSnapshot",
            "WorldPhaseTransitionChannel",
            "WorldFourGreatPhaseTransitionSystem",
            "AnalyticAt ℝ System.freeEnergy critical",
            "freeEnergyNonanalyticAt",
            "spectralGapClosesAt",
            "fixedPointAlgebraChangesAt",
            "fourGreatCoordinatesChangeAt",
            "spectralGap_at_critical_eq_zero",
            "spectralGap_nonnegative_at",
            "boundary_package",
        ),
    )

    declaration = ROOT / manifest["declaration_module"]
    require_tokens(
        declaration,
        (
            "WorldFourGreatPhaseTransitionCandidate",
            "WorldFourGreatConcordantPhaseTransitionCandidate",
            "WorldFourGreatPhaseTransitionDeclaration",
            "toConcordant",
            "toCandidate",
            "evidence_package",
        ),
    )

    require_tokens(
        ROOT / manifest["formal_root"],
        (
            "FourGreatPhaseTransitionCriteriaV0_60",
            "FourGreatPhaseTransitionDeclarationV0_60",
        ),
    )
    require_tokens(
        ROOT / manifest["canonical_root"],
        (
            "KUOS.WORLD.FourGreatPhaseTransitionCriteriaV0_60",
            "KUOS.WORLD.FourGreatPhaseTransitionDeclarationV0_60",
        ),
    )
    require_tokens(
        ROOT / manifest["aggregate_formal_root"],
        ("KUOS.WORLD.FourGreatPhaseTransitionDeclarationV0_60",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_60",))
    require_tokens(
        ROOT / manifest["documentation"],
        (
            "自由エネルギー証人",
            "ギャップ閉鎖証人",
            "固定点代数変化証人",
            "四大相転移宣言",
            "single witness != phase-transition declaration",
            "phase-transition declaration != execution authority",
        ),
    )

    predecessor = json.loads(
        (ROOT / "manifests/world_four_great_phase_dynamics_v0_59.json").read_text(
            encoding="utf-8"
        )
    )
    require(predecessor["manifest_version"] == manifest["predecessor"],
            "v0.59 predecessor manifest mismatch")

    print("WORLD v0.60 four-great phase-transition declaration checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
