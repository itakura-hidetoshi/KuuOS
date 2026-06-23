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
    formal = ROOT / "formal/KUOS/WORLD/VacuumExpectationObservationCandidateBridgeV0_50.lean"
    require_tokens(
        formal,
        (
            "WorldVacuumExpectationObservationBridge",
            "VacuumExpectationObservationCandidate",
            "candidateOfObservable",
            "candidate_source_exact",
            "identity_candidate_normalized",
            "star_square_candidate_nonnegative",
            "gauge_candidate_value_eq",
            "observation_boundary_preserved",
            "runtime_remains_read_only",
        ),
    )
    require_tokens(
        ROOT / "formal/KuuOSFormalV0_50.lean",
        ("VacuumExpectationObservationCandidateBridgeV0_50",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.VacuumExpectationObservationCandidateBridgeV0_50",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_50",))
    require_tokens(
        ROOT / "docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVATION_CANDIDATE_v0_50.md",
        (
            "vacuum expectation != fact",
            "observation candidate != PlanOS activation",
            "runtime remains read-only",
        ),
    )

    # README and ROADMAP advance with the public frontier. Historical
    # validators retain strict checks for v0.50 artifacts while checking only
    # invariant public boundaries on the moving orientation surfaces.
    require_tokens(
        ROOT / "README.md",
        (
            "WORLD read-only mathematical sidecar",
            "vacuum expectation != fact",
            "observation candidate != PlanOS activation",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "WORLD mathematical sidecar",
            "vacuum-expectation observation candidates",
            "observation candidate != PlanOS activation",
        ),
    )
    assert (ROOT / "scripts/run_kuuos_runtime_full_check_v0_50.py").is_file()

    manifest_path = ROOT / "manifests/world_vacuum_expectation_observation_candidate_v0_50.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "world_vacuum_expectation_observation_candidate_v0_50"
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_50.lean"
    assert manifest["formal_module"] == str(formal.relative_to(ROOT))
    assert "candidate_not_plan_activation" in manifest["boundaries"]
    assert "runtime_read_only" in manifest["boundaries"]
    assert "gauge_candidate_value_eq" in manifest["derived_results"]

    print("world_vacuum_expectation_observation_candidate_v0_50 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
