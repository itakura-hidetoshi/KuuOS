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
        "calculus_module",
        "calculus_root",
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
    require(
        manifest["scope"]["exponential_arc_response_constructed_from_mathlib_primitives"] is False,
        "response derivative promoted to first-principles construction",
    )
    require(all(value is False for value in manifest["boundaries"].values()), "boundary promotion")

    require_tokens(
        ROOT / manifest["calculus_module"],
        (
            "ArakiBoundedExponentialArcCalculus",
            "firstVariation",
            "mixedHessian",
            "firstVariation_hasDerivAt",
            "mixedHessian_eq_bkm",
            "mixedHessian_symmetric",
            "mixedHessian_nonnegative",
        ),
    )
    require_tokens(
        ROOT / manifest["formal_module"],
        (
            "WorldKuuVacuumArakiHessianOSTransport",
            "¬ FiniteDimensional ℂ M.H",
            "hessian_eq_quantum_fisher",
            "hessian_eq_araki_hessian_shadow",
            "hessian_eq_physical_excitation_gram",
            "hessian_eq_os_reflection_form_re",
            "osHilbertIdentification.inner_map_map",
        ),
    )
    require_tokens(ROOT / manifest["calculus_root"], ("ArakiBoundedExponentialArcCalculusV0_56",))
    require_tokens(ROOT / manifest["formal_root"], ("KuuVacuumArakiHessianOSTransportV0_56",))
    require_tokens(ROOT / manifest["aggregate_formal_root"], ("KUOS.WORLD.KuuVacuumArakiHessianOSTransportV0_56",))
    require_tokens(ROOT / "lakefile.toml", ("KuuOSArakiCalculusV0_56", "KuuOSFormalV0_56"))
    require_tokens(
        ROOT / manifest["documentation"],
        (
            "Araki Hessian",
            "BKM",
            "量子Fisher計量",
            "OS反射形式",
            "¬ FiniteDimensional ℂ H_phys",
            "任意の無界生成子は対象に含めない",
        ),
    )

    print("WORLD v0.56 Araki Hessian OS transport checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
