#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def require_tokens(path: pathlib.Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def require_tokens_across(
    paths: tuple[pathlib.Path, ...], tokens: tuple[str, ...]
) -> None:
    texts = {
        path: path.read_text(encoding="utf-8")
        for path in paths
    }
    for token in tokens:
        assert any(token in text for text in texts.values()), (
            f"{', '.join(str(path) for path in paths)}: {token}"
        )


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

    # Rolling repository documents are layered. Durable observation boundaries
    # may live in the root overview, roadmap, or ObserveOS subsystem index.
    require_tokens_across(
        (
            ROOT / "README.md",
            ROOT / "ROADMAP.md",
            ROOT / "docs/ObserveOS/README.md",
        ),
        (
            "WORLD candidate != empirical fact",
            "WORLD sidecar != exact WORLD",
            "observation != verification",
        ),
    )

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
