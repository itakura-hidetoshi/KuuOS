#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from runtime.kuuos_gauge_invariant_dependent_origination_descent_v0_1 import (
    GaugeInvariantDependentOriginationDescentClaim,
    evaluate_gauge_invariant_dependent_origination_descent,
)


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ROOT / "docs" / "GAUGE_INVARIANT_DEPENDENT_ORIGINATION_DESCENT_v0_1.md",
    ROOT / "specs" / "gauge_invariant_dependent_origination_descent_contract_v0_1.yaml",
    ROOT / "runtime" / "kuuos_gauge_invariant_dependent_origination_descent_v0_1.py",
    ROOT / "tests" / "test_gauge_invariant_dependent_origination_descent_v0_1.py",
)

REQUIRED_DOC_TOKENS = (
    "52e45c33b56a34c905c94b63d4ced7cbbb5a29d2",
    "boundedContinuous_gaugeInvariant_of_dense_interpolation",
    "interpolationReadoutCompatible_of_boundedContinuous_readout",
    "observable_unique_of_dense_interpolation",
    "Exact same-root readout",
    "Equivariant interpolation",
    "Local gauge invariance",
    "Dense local-to-global coverage",
    "Continuous global extension witness",
    "Cross-scale compatibility",
    "no privileged gauge representative",
    "Gauge invariance does not convert a conventional observable into an ultimate substance",
)

REQUIRED_SPEC_TOKENS = (
    "append-only",
    "tighten_only: true",
    "same_root_required: true",
    "semantic_invariance_and_presentation_equivariance_are_distinct",
    "continuous_global_extension_existence_from_compatibility_and_density_alone: true",
    "no_authority_expansion",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    for path in REQUIRED_FILES:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

    doc = REQUIRED_FILES[0].read_text(encoding="utf-8")
    for token in REQUIRED_DOC_TOKENS:
        require(token in doc, f"documentation token missing: {token}")

    spec = REQUIRED_FILES[1].read_text(encoding="utf-8")
    for token in REQUIRED_SPEC_TOKENS:
        require(token in spec, f"contract token missing: {token}")

    default = evaluate_gauge_invariant_dependent_origination_descent(
        GaugeInvariantDependentOriginationDescentClaim()
    )
    require(default["status"] == "CANDIDATE", "default descent claim must be CANDIDATE")
    require(
        default["global_gauge_invariance_theorem_schema_eligible"] is True,
        "complete bridge conditions must enable the global gauge-invariance theorem schema",
    )
    require(
        default["continuous_extension_existence_theorem_generated"] is False,
        "runtime must never infer extension existence from compatibility/density alone",
    )

    missing_extension = evaluate_gauge_invariant_dependent_origination_descent(
        GaugeInvariantDependentOriginationDescentClaim(
            continuous_global_extension_witness=False
        )
    )
    require(missing_extension["status"] == "HOLD", "missing extension witness must HOLD")
    require(
        missing_extension["global_gauge_invariance_theorem_schema_eligible"] is False,
        "missing extension witness must block global gauge-invariance promotion",
    )

    representative_reification = evaluate_gauge_invariant_dependent_origination_descent(
        GaugeInvariantDependentOriginationDescentClaim(
            privileges_local_representative_as_real=True
        )
    )
    require(
        representative_reification["status"] == "REJECT",
        "privileged gauge representative must REJECT",
    )

    type_conflation = evaluate_gauge_invariant_dependent_origination_descent(
        GaugeInvariantDependentOriginationDescentClaim(
            conflates_invariance_and_equivariance=True
        )
    )
    require(type_conflation["status"] == "REPAIR", "invariant/equivariant conflation must REPAIR")

    two_truths_collapse = evaluate_gauge_invariant_dependent_origination_descent(
        GaugeInvariantDependentOriginationDescentClaim(two_truths_noncollapse=False)
    )
    require(two_truths_collapse["status"] == "REJECT", "Two Truths collapse must REJECT")

    print("PASS: gauge-invariant dependent origination descent v0.1")


if __name__ == "__main__":
    main()
