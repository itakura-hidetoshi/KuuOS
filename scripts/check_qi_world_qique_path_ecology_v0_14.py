#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_world_qique_path_ecology_core_v0_14 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    sha,
)
from runtime.kuuos_indra_qi_world_qique_path_ecology_runtime_v0_14 import (
    BLOCKED,
    READY,
    build_path_ecology,
)


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def topology(kind: str) -> dict[str, Any]:
    if kind == "balanced":
        patch_ids = ["p0", "p1", "p2", "p3"]
        edges = [("p0", "p1"), ("p0", "p2"), ("p1", "p2"), ("p1", "p3"), ("p2", "p3"), ("p2", "p0"), ("p3", "p0"), ("p3", "p1")]
        used = list(range(len(edges)))
        weights = [1.0] * len(used)
        cycles = [[0, 2], [4, 6]]
    elif kind == "localized":
        patch_ids = ["p0", "p1", "p2", "p3"]
        edges = [("p0", "p1"), ("p0", "p2"), ("p1", "p2"), ("p1", "p3"), ("p2", "p3"), ("p3", "p0")]
        used = [0, 0, 0, 1]
        weights = [8.0, 1.0, 1.0, 0.5]
        cycles = [[2, 3]]
    elif kind == "overdiffused":
        patch_ids = [f"p{i}" for i in range(6)]
        edges = [(f"p{i}", f"p{j}") for i in range(6) for j in range(6) if i != j]
        used = [0, 12, 24]
        weights = [1.0, 1.0, 1.0]
        cycles = [[1, 2]]
    elif kind == "scar_locked":
        patch_ids = ["p0", "p1", "p2", "p3"]
        edges = [("p0", "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p0"), ("p0", "p2"), ("p1", "p3")]
        used = [0]
        weights = [1.0]
        cycles = [[0, 1, 2, 3]]
    else:
        raise ValueError(kind)
    patches = [{"patch_id": value} for value in patch_ids]
    connections = [
        {"connection_id": f"c{index}", "source_patch": source, "target_patch": target}
        for index, (source, target) in enumerate(edges)
    ]
    flows = [
        {
            "flow_id": f"f{index}",
            "source_patch": edges[edge_index][0],
            "target_patch": edges[edge_index][1],
            "connection_id": f"c{edge_index}",
            "flow_weight": weight,
        }
        for index, (edge_index, weight) in enumerate(zip(used, weights))
    ]
    holonomy = [
        {
            "cycle_id": f"h{index}",
            "connection_ids": [f"c{value}" for value in cycle],
            "transport_residue_digest": sha({"cycle": index, "kind": kind}),
        }
        for index, cycle in enumerate(cycles)
    ]
    return {"patches": patches, "connections": connections, "flows": flows, "cycles": holonomy}


def source_files(root: pathlib.Path, kind: str, decision: str = "promote_bounded") -> dict[str, Any]:
    graph = topology(kind)
    world = {
        "version": "indra_qi_world_model_v0_1",
        "world_model_id": "world-a",
        "local_world_patches": graph["patches"],
        "indra_connections": graph["connections"],
        "qi_flow_channels": graph["flows"],
        "holonomy_cycles": graph["cycles"],
        "mandala_inclusion": {
            "included_patch_ids": [value["patch_id"] for value in graph["patches"]],
            "multi_world_noncollapse": True,
            "single_ontology_forced": False,
            "contradiction_visibility_preserved": True,
        },
        "epoch": 1,
    }
    world["indra_qi_world_state_digest"] = sha(world)
    governance_state = {
        "version": "indra_qi_generational_governance_state_v0_13",
        "monitor_id": "monitor-a",
        "runner_id": "runner-a",
        "last_review_run_id": "generation-review-a",
        "latest_governance_decision": decision,
        "epoch": 2,
    }
    governance_state["governance_state_digest"] = sha(governance_state)
    recommendation = {
        "version": "indra_qi_generational_governance_recommendation_v0_13",
        "monitor_id": "monitor-a",
        "review_run_id": "generation-review-a",
        "runner_id": "runner-a",
        "generation_index": 1,
        "decision": decision,
        "recommendation_only": True,
        "direct_execution_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "epoch": 2,
    }
    recommendation["recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_generational_governance_state_v0_13.json", governance_state)
    write(root / "indra_qi_generational_governance_recommendation_v0_13.json", recommendation)
    return {"world": world, "state": governance_state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], review: str, licensed: list[str] | None = None) -> dict[str, Any]:
    result = {
        "version": PLAN_VERSION,
        "ecology_id": "ecology-a",
        "review_run_id": review,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_source_governance_state_digest": source["state"]["governance_state_digest"],
        "expected_source_governance_recommendation_digest": source["recommendation"]["recommendation_digest"],
        "ecology_policy": {
            "minimum_patch_participation_ratio": 0.55,
            "maximum_flow_concentration": 0.45,
            "maximum_overdiffusion_score": 0.55,
            "maximum_loop_mode_lock": 0.55,
            "minimum_branch_energy": 0.45,
            "maximum_scar_reentry_score": 0.55,
            "minimum_multi_world_diversity": 0.55,
            "maximum_false_stability_pressure": 0.45,
            "quarantine_false_stability_pressure": 0.75,
            "licensed_localization_relief": 0.20,
            "licensed_localization_patch_ids": list(licensed or []),
            "false_stability_weights": {
                "localization": 0.25,
                "branch_loss": 0.25,
                "loop_lock": 0.20,
                "scar_reentry": 0.15,
                "diversity_loss": 0.15,
            },
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    result["path_ecology_plan_digest"] = plan_digest(result)
    return result


def license_value(plan_value: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["review_run_id"]),
        "bound_path_ecology_plan_digest": plan_value["path_ecology_plan_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_source_governance_state_digest": source["state"]["governance_state_digest"],
        "bound_source_governance_recommendation_digest": source["recommendation"]["recommendation_digest"],
        "state_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "execution_authority_granted": False,
        "truth_authority_granted": False,
        "world_update_authority_granted": False,
        "direct_promotion_authority_granted": False,
        "direct_rollback_authority_granted": False,
        "direct_quarantine_authority_granted": False,
    }


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_world_qique_path_ecology_v0_14_enabled": True,
        "apply_indra_qi_world_qique_path_ecology_v0_14": True,
    }


def execute(root: pathlib.Path, kind: str, decision: str = "promote_bounded", licensed: list[str] | None = None):
    source = source_files(root, kind, decision)
    plan_value = plan(source, "ecology-review-a", licensed)
    before = {
        name: (root / name).read_bytes()
        for name in (
            "ku_indra_qi_noncommutative_mandala_world_state.json",
            "indra_qi_generational_governance_state_v0_13.json",
            "indra_qi_generational_governance_recommendation_v0_13.json",
        )
    }
    result = build_path_ecology(
        runtime_context=context(root),
        path_ecology_plan=plan_value,
        path_ecology_license=license_value(plan_value, source),
    )
    after = {name: (root / name).read_bytes() for name in before}
    assert before == after
    return source, plan_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, result = execute(root, "balanced")
        assert result.status == READY
        assert result.decision == "ecology_compatible_bounded_promotion"
        output = json.loads((root / "indra_qi_world_qique_path_ecology_recommendation_v0_14.json").read_text())
        assert output["recommendation_only"] is True
        assert output["direct_world_update_authority"] is False
        assert output["promotion_ecology_compatible"] is True
        replay = build_path_ecology(
            runtime_context=context(root),
            path_ecology_plan=plan_value,
            path_ecology_license=license_value(plan_value, source),
        )
        assert replay.status == BLOCKED and "world_qique_replay_detected" in replay.blockers

    with tempfile.TemporaryDirectory() as directory:
        _, _, result = execute(pathlib.Path(directory), "localized")
        assert result.status == READY and result.decision == "reopen_branches_recommended"

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        _, _, result = execute(root, "localized", licensed=["p0"])
        assert result.status == READY and result.decision == "reopen_branches_recommended"
        output = json.loads((root / "indra_qi_world_qique_path_ecology_recommendation_v0_14.json").read_text())
        assert output["qique_observables"]["licensed_localization_active"] is True
        assert output["gates"]["flow_concentration_bounded"] is True
        assert output["gates"]["branch_energy_sufficient"] is False

    with tempfile.TemporaryDirectory() as directory:
        _, _, result = execute(pathlib.Path(directory), "overdiffused")
        assert result.status == READY and result.decision == "focus_or_reobserve_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, result = execute(pathlib.Path(directory), "scar_locked")
        assert result.status == READY and result.decision == "quarantine_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, result = execute(pathlib.Path(directory), "balanced", "hold_for_observation")
        assert result.status == READY and result.decision == "hold_for_observation"

    with tempfile.TemporaryDirectory() as directory:
        _, _, result = execute(pathlib.Path(directory), "balanced", "rollback_recommended")
        assert result.status == READY and result.decision == "rollback_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, result = execute(pathlib.Path(directory), "balanced", "quarantine_recommended")
        assert result.status == READY and result.decision == "quarantine_recommended"

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = source_files(root, "balanced")
        plan_value = plan(source, "ecology-review-a")
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_path_ecology(
            runtime_context=context(root),
            path_ecology_plan=plan_value,
            path_ecology_license=license_value(plan_value, source),
        )
        assert result.status == BLOCKED
        assert "world_qique_source_world_digest_invalid" in result.blockers

    manifest = json.loads((ROOT / "manifests/qi_world_qique_path_ecology_v0_14.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_world_qique_path_ecology_v0_14 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
