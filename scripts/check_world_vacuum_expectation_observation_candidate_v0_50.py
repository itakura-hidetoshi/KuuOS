#!/usr/bin/env python3
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]


def req(path, *tokens):
    text = (R / path).read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def main():
    formal = "formal/KUOS/WORLD/VacuumExpectationObservationCandidateBridgeV0_50.lean"
    req(formal, "WorldVacuumExpectationObservationBridge",
        "VacuumExpectationObservationCandidate", "candidateOfObservable",
        "candidate_source_exact", "identity_candidate_normalized",
        "star_square_candidate_nonnegative", "gauge_candidate_value_eq",
        "observation_boundary_preserved", "runtime_remains_read_only")
    req("formal/KuuOSFormalV0_50.lean", "VacuumExpectationObservationCandidateBridgeV0_50")
    req("formal/KUOS.lean", "KUOS.WORLD.VacuumExpectationObservationCandidateBridgeV0_50")
    req("lakefile.toml", "KuuOSFormalV0_50")
    req("docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVATION_CANDIDATE_v0_50.md",
        "vacuum expectation != fact", "observation candidate != PlanOS activation",
        "runtime remains read-only")
    stable = ("WORLD candidate != empirical fact", "WORLD sidecar != exact WORLD",
              "observation != verification")
    req("README.md", *stable)
    req("ROADMAP.md", *stable)
    manifest = json.loads((R / "manifests/world_vacuum_expectation_observation_candidate_v0_50.json").read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == "world_vacuum_expectation_observation_candidate_v0_50"
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_50.lean"
    assert manifest["formal_module"] == formal
    assert "candidate_not_plan_activation" in manifest["boundaries"]
    assert "runtime_read_only" in manifest["boundaries"]
    assert "gauge_candidate_value_eq" in manifest["derived_results"]
    print("world_vacuum_expectation_observation_candidate_v0_50 checks passed")


if __name__ == "__main__":
    main()
