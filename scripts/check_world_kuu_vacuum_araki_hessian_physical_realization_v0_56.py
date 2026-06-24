#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests/world_kuu_vacuum_araki_hessian_physical_realization_v0_56.json"


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
        == "world_kuu_vacuum_araki_hessian_physical_realization_v0_56",
        "manifest version mismatch",
    )
    require(
        manifest["predecessor"] == "world_kuu_vacuum_information_geometry_v0_55",
        "predecessor mismatch",
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

    require(manifest["scope"]["bounded_selfadjoint_generators"] is True, "bounded scope missing")
    require(manifest["scope"]["infinite_dimensional_physical_hilbert"] is True, "infinite dimension missing")
    require(manifest["scope"]["arbitrary_unbounded_generators"] is False, "unbounded scope promoted")
    require(all(value is False for value in manifest["boundaries"].values()), "boundary promotion")

    require_tokens(
        ROOT / manifest["formal_module"],
        (
            "ArakiBoundedExponentialArcKernel",
            "arakiFirstVariation",
            "arakiMixedHessian",
            "araki_first_variation_hasDerivAt",
            "araki_mixed_hessian_eq_bkm",
            "WorldKuuVacuumArakiHessianPhysicalRealization",
            "InfiniteDimensional ℂ M.H",
            "araki_hessian_eq_quantum_fisher",
            "araki_hessian_eq_araki_hessian_shadow",
            "araki_hessian_eq_physical_excitation_gram",
            "araki_hessian_eq_os_reflection_form_re",
        ),
    )
    require_tokens(ROOT / manifest["formal_root"], ("KuuVacuumArakiHessianPhysicalRealizationV0_56",))
    require_tokens(ROOT / manifest["aggregate_formal_root"], ("KUOS.WORLD.KuuVacuumArakiHessianPhysicalRealizationV0_56",))
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_56",))
    require_tokens(
        ROOT / manifest["documentation"],
        (
            "Araki Hessian",
            "BKM",
            "量子Fisher計量",
            "OS反射形式",
            "InfiniteDimensional",
            "任意の無界生成子は対象に含めない",
        ),
    )

    print("WORLD v0.56 Araki Hessian physical realization checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
