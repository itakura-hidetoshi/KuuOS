from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_autonomous_agent_completion_architecture_v0_19 import (
    assert_valid_architecture,
    readiness_report,
    validate_architecture,
)

MANIFEST_PATH = Path("manifests/kuuos_autonomous_agent_completion_architecture_v0_19.json")


def _load_manifest() -> dict:
    value = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("architecture_manifest_not_object")
    return value


def _component(manifest: dict, component_id: str) -> dict:
    for component in manifest.get("components", []):
        if component.get("component_id") == component_id:
            return component
    raise ValueError(f"component_not_found:{component_id}")


def main() -> bool:
    manifest = _load_manifest()
    report = assert_valid_architecture(manifest)
    assert report["valid"] is True
    assert report["execution_authority_opened"] is False
    assert report["component_count"] == 16
    assert report["status_counts"] == {
        "implemented": 1,
        "open_gap": 13,
        "partial_gap": 2,
    }
    assert report["open_component_count"] == 15
    assert report["next_dependency_rank"] == 1
    assert report["next_release"] == "v0.20"
    assert [item["component_id"] for item in report["next_components"]] == [
        "goal_portfolio_arbitration",
        "mission_contract_kernel",
        "mission_renewal_termination",
    ]

    reversed_rank = deepcopy(manifest)
    _component(reversed_rank, "mission_contract_kernel")["dependency_rank"] = 9
    reversed_errors = validate_architecture(reversed_rank)
    assert any(error.startswith("component_dependency_rank_reversed:goal_portfolio_arbitration") for error in reversed_errors)

    missing_non_authority = deepcopy(manifest)
    _component(missing_non_authority, "outcome_verifier")["non_authority"] = ""
    assert "component_non_authority_missing:outcome_verifier" in validate_architecture(missing_non_authority)

    missing_integration = deepcopy(manifest)
    _component(missing_integration, "integrated_indefinite_operation")["depends_on"].remove("outcome_verifier")
    assert any(
        error.startswith("integration_dependencies_missing:outcome_verifier")
        for error in validate_architecture(missing_integration)
    )

    missing_invariant = deepcopy(manifest)
    missing_invariant["global_invariants"].remove("plan_not_permission")
    assert any(
        error.startswith("global_invariants_missing:plan_not_permission")
        for error in validate_architecture(missing_invariant)
    )

    unknown_dependency = deepcopy(manifest)
    _component(unknown_dependency, "semantic_planner_replanner")["depends_on"].append("unknown_component")
    assert "component_dependency_unknown:semantic_planner_replanner:unknown_component" in validate_architecture(unknown_dependency)

    dependency_cycle = deepcopy(manifest)
    _component(dependency_cycle, "mission_contract_kernel")["depends_on"].append("goal_portfolio_arbitration")
    assert any(
        error.startswith("component_dependency_cycle:")
        for error in validate_architecture(dependency_cycle)
    )

    wrong_release = deepcopy(manifest)
    _component(wrong_release, "observation_belief_kernel")["target_release"] = "v0.26"
    assert "component_release_rank_mismatch:observation_belief_kernel:v0.26:v0.21" in validate_architecture(wrong_release)

    invalid_target = deepcopy(manifest)
    invalid_target["target_definition"]["explicit_non_equivalences"].remove("unbounded_authority")
    assert any(
        error.startswith("target_non_equivalences_missing:unbounded_authority")
        for error in validate_architecture(invalid_target)
    )

    print("PASS: autonomous agent completion architecture v0.19")
    print(json.dumps(readiness_report(manifest), ensure_ascii=False, sort_keys=True))
    return True


if __name__ == "__main__":
    main()
