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

from runtime.kuuos_indra_qi_multi_lineage_evolution_core_v0_15 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    PROPOSAL_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    proposal_digest,
    sha,
)
from runtime.kuuos_indra_qi_multi_lineage_evolution_runtime_v0_15 import (
    BLOCKED,
    READY,
    build_multi_lineage_evolution,
)


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def world_state(root: pathlib.Path) -> dict[str, Any]:
    patches = [{"patch_id": f"p{index}"} for index in range(4)]
    edge_pairs = [
        ("p0", "p1"),
        ("p1", "p2"),
        ("p0", "p2"),
        ("p2", "p3"),
        ("p0", "p3"),
        ("p3", "p1"),
        ("p1", "p3"),
        ("p3", "p0"),
    ]
    connections = [
        {"connection_id": f"c{index}", "source_patch": source, "target_patch": target}
        for index, (source, target) in enumerate(edge_pairs)
    ]
    flows = [
        {
            "flow_id": f"f{index}",
            "source_patch": edge_pairs[connection_index][0],
            "target_patch": edge_pairs[connection_index][1],
            "connection_id": f"c{connection_index}",
            "flow_weight": weight,
        }
        for index, (connection_index, weight) in enumerate(
            [(0, 3.0), (1, 3.0), (3, 3.0), (7, 3.0), (2, 0.5), (4, 0.5)]
        )
    ]
    world = {
        "version": "indra_qi_world_model_v0_1",
        "world_model_id": "world-a",
        "local_world_patches": patches,
        "indra_connections": connections,
        "qi_flow_channels": flows,
        "holonomy_cycles": [
            {
                "cycle_id": "scar-cycle",
                "connection_ids": ["c0", "c1", "c3", "c7"],
                "transport_residue_digest": sha({"scar": 1}),
            },
            {
                "cycle_id": "alternate-cycle",
                "connection_ids": ["c2", "c3", "c7"],
                "transport_residue_digest": sha({"scar": 2}),
            },
        ],
        "mandala_inclusion": {
            "included_patch_ids": [value["patch_id"] for value in patches],
            "multi_world_noncollapse": True,
            "single_ontology_forced": False,
            "contradiction_visibility_preserved": True,
        },
        "epoch": 1,
    }
    world["indra_qi_world_state_digest"] = sha(world)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    return world


def ecology_sources(root: pathlib.Path, decision: str) -> dict[str, Any]:
    world = world_state(root)
    state = {
        "version": "indra_qi_world_qique_path_ecology_state_v0_14",
        "ecology_id": "ecology-a",
        "world_model_id": "world-a",
        "last_review_run_id": "ecology-review-a",
        "last_source_world_state_digest": world["indra_qi_world_state_digest"],
        "latest_path_ecology_decision": decision,
        "latest_qique_regime": "WORLD_QIQUE_LOCALIZED_OR_BRANCH_POOR"
        if decision == "reopen_branches_recommended"
        else "WORLD_QIQUE_BALANCED_BOUNDED_FLOW",
        "epoch": 2,
    }
    state["path_ecology_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_world_qique_path_ecology_recommendation_v0_14",
        "ecology_id": "ecology-a",
        "review_run_id": "ecology-review-a",
        "world_model_id": "world-a",
        "source_governance_decision": "promote_bounded",
        "qique_regime": state["latest_qique_regime"],
        "decision": decision,
        "decision_reasons": ["test"],
        "promotion_ecology_compatible": decision == "ecology_compatible_bounded_promotion",
        "qique_observables": {
            "dominant_patch_id": "p0",
            "patch_participation_ratio": 0.5,
            "branch_energy": 0.4,
            "loop_mode_lock": 0.4,
            "scar_reentry_score": 0.3,
            "multi_world_diversity": 0.5,
        },
        "gates": {},
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_governance_state_digest": sha({"governance": 1}),
        "source_governance_recommendation_digest": sha({"recommendation": 1}),
        "recommendation_only": True,
        "direct_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "epoch": 2,
    }
    recommendation["path_ecology_recommendation_digest"] = sha(recommendation)
    write(root / "indra_qi_world_qique_path_ecology_state_v0_14.json", state)
    write(root / "indra_qi_world_qique_path_ecology_recommendation_v0_14.json", recommendation)
    return {"world": world, "state": state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], run_id: str) -> dict[str, Any]:
    result = {
        "version": PLAN_VERSION,
        "evolution_id": "evolution-a",
        "evolution_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_source_path_ecology_state_digest": source["state"]["path_ecology_state_digest"],
        "expected_source_path_ecology_recommendation_digest": source["recommendation"]["path_ecology_recommendation_digest"],
        "evolution_policy": {
            "minimum_candidate_lineages": 3,
            "maximum_candidate_lineages": 8,
            "maximum_path_length": 4,
            "maximum_single_lineage_weight": 0.55,
            "maximum_pairwise_connection_overlap": 0.75,
            "minimum_lineage_diversity_score": 0.45,
            "minimum_target_patch_diversity": 0.50,
            "minimum_recovery_lineages": 1,
            "minimum_minority_lineages": 1,
            "minimum_reobserve_lineages": 1,
            "minimum_dominant_patch_egress_lineages": 1,
            "minimum_holonomy_scar_avoidance_ratio": 0.50,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    result["evolution_plan_digest"] = plan_digest(result)
    return result


def lineage(
    lineage_id: str,
    kind: str,
    source: str,
    target: str,
    connections: list[str],
    weight: float,
    *,
    minority: bool = False,
    recovery: bool = False,
    reobserve: bool = False,
) -> dict[str, Any]:
    return {
        "lineage_id": lineage_id,
        "lineage_kind": kind,
        "source_patch": source,
        "target_patch": target,
        "connection_ids": connections,
        "candidate_weight": weight,
        "preserves_minority_path": minority,
        "recovery_path": recovery,
        "reobserve_path": reobserve,
        "rollback_corridor_digest": sha({"rollback": lineage_id}),
        "observation_projection_digest": sha({"observation": lineage_id}),
        "process_tensor_context_digest": sha({"process": lineage_id}),
        "non_markov_context_digest": sha({"memory": lineage_id}),
    }


def proposal(
    plan_value: Mapping[str, Any],
    source: Mapping[str, Any],
    mode: str,
) -> dict[str, Any]:
    if mode == "diverse":
        lineages = [
            lineage("l0", "explore", "p0", "p2", ["c2"], 0.40, minority=True),
            lineage("l1", "recovery", "p2", "p3", ["c3"], 0.30, recovery=True),
            lineage("l2", "minority_preservation", "p1", "p3", ["c6"], 0.30, minority=True),
        ]
    elif mode == "reopen":
        lineages = [
            lineage("l0", "explore", "p0", "p2", ["c2"], 0.36, minority=True),
            lineage("l1", "recovery", "p0", "p3", ["c4"], 0.34, minority=True, recovery=True),
            lineage("l2", "minority_preservation", "p1", "p3", ["c6"], 0.30, minority=True),
        ]
    elif mode == "focus":
        lineages = [
            lineage("l0", "focus", "p0", "p2", ["c2"], 0.38),
            lineage("l1", "reobserve", "p2", "p3", ["c3"], 0.32, reobserve=True),
            lineage("l2", "recovery", "p1", "p3", ["c6"], 0.30, recovery=True, minority=True),
        ]
    elif mode == "duplicate":
        lineages = [
            lineage("l0", "explore", "p0", "p2", ["c2"], 0.80, minority=True),
            lineage("l1", "explore", "p0", "p2", ["c2"], 0.10, minority=True),
            lineage("l2", "explore", "p0", "p2", ["c2"], 0.10, minority=True),
        ]
    else:
        raise ValueError(mode)
    result = {
        "version": PROPOSAL_VERSION,
        "evolution_run_id": plan_value["evolution_run_id"],
        "source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "source_path_ecology_recommendation_digest": source["recommendation"]["path_ecology_recommendation_digest"],
        "candidate_lineages": lineages,
    }
    result["lineage_proposal_digest"] = proposal_digest(result)
    return result


def license_value(
    plan_value: Mapping[str, Any],
    proposal_value: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["evolution_run_id"]),
        "bound_evolution_plan_digest": plan_value["evolution_plan_digest"],
        "bound_lineage_proposal_digest": proposal_value["lineage_proposal_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_source_path_ecology_state_digest": source["state"]["path_ecology_state_digest"],
        "bound_source_path_ecology_recommendation_digest": source["recommendation"]["path_ecology_recommendation_digest"],
        "state_write_allowed": True,
        "candidate_set_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "execution_authority_granted": False,
        "truth_authority_granted": False,
        "world_update_authority_granted": False,
        "lineage_selection_authority_granted": False,
        "lineage_execution_authority_granted": False,
        "direct_promotion_authority_granted": False,
        "direct_rollback_authority_granted": False,
        "direct_quarantine_authority_granted": False,
    }


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_multi_lineage_evolution_v0_15_enabled": True,
        "apply_indra_qi_multi_lineage_evolution_v0_15": True,
    }


def execute(root: pathlib.Path, ecology_decision: str, mode: str):
    source = ecology_sources(root, ecology_decision)
    plan_value = plan(source, "evolution-run-a")
    proposal_value = proposal(plan_value, source, mode)
    source_names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_world_qique_path_ecology_state_v0_14.json",
        "indra_qi_world_qique_path_ecology_recommendation_v0_14.json",
    )
    before = {name: (root / name).read_bytes() for name in source_names}
    result = build_multi_lineage_evolution(
        runtime_context=context(root),
        evolution_plan=plan_value,
        evolution_license=license_value(plan_value, proposal_value, source),
        lineage_proposal=proposal_value,
    )
    after = {name: (root / name).read_bytes() for name in source_names}
    assert before == after
    return source, plan_value, proposal_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, proposal_value, result = execute(
            root, "ecology_compatible_bounded_promotion", "diverse"
        )
        assert result.status == READY
        assert result.decision == "diverse_bounded_evolution_ready"
        packet = json.loads((root / "indra_qi_multi_lineage_candidate_set_v0_15.json").read_text())
        recommendation = json.loads(
            (root / "indra_qi_multi_lineage_evolution_recommendation_v0_15.json").read_text()
        )
        assert packet["candidate_weighting_not_truth"] is True
        assert packet["candidate_set_not_selection"] is True
        assert recommendation["direct_lineage_selection_authority"] is False
        assert recommendation["direct_lineage_execution_authority"] is False
        assert recommendation["direct_world_update_authority"] is False
        replay = build_multi_lineage_evolution(
            runtime_context=context(root),
            evolution_plan=plan_value,
            evolution_license=license_value(plan_value, proposal_value, source),
            lineage_proposal=proposal_value,
        )
        assert replay.status == BLOCKED
        assert "multi_lineage_replay_detected" in replay.blockers

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "reopen_branches_recommended", "reopen"
        )
        assert result.status == READY
        assert result.decision == "branch_reopening_candidate_set_ready"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "reopen_branches_recommended", "duplicate"
        )
        assert result.status == READY
        assert result.decision == "redesign_candidate_set_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "focus_or_reobserve_recommended", "focus"
        )
        assert result.status == READY
        assert result.decision == "focus_reobserve_candidate_set_ready"

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        ("rollback_recommended", "rollback_recommended"),
        ("quarantine_recommended", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, "diverse")
            assert result.status == READY
            assert result.decision == expected

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = ecology_sources(root, "ecology_compatible_bounded_promotion")
        plan_value = plan(source, "evolution-run-a")
        proposal_value = proposal(plan_value, source, "diverse")
        proposal_value["candidate_lineages"][0]["candidate_weight"] = 99.0
        result = build_multi_lineage_evolution(
            runtime_context=context(root),
            evolution_plan=plan_value,
            evolution_license=license_value(plan_value, proposal_value, source),
            lineage_proposal=proposal_value,
        )
        assert result.status == BLOCKED
        assert "multi_lineage_proposal_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = ecology_sources(root, "ecology_compatible_bounded_promotion")
        plan_value = plan(source, "evolution-run-a")
        proposal_value = proposal(plan_value, source, "diverse")
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_multi_lineage_evolution(
            runtime_context=context(root),
            evolution_plan=plan_value,
            evolution_license=license_value(plan_value, proposal_value, source),
            lineage_proposal=proposal_value,
        )
        assert result.status == BLOCKED
        assert "multi_lineage_source_world_digest_invalid" in result.blockers

    manifest = json.loads((ROOT / "manifests/qi_multi_lineage_evolution_v0_15.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("qi_multi_lineage_evolution_v0_15 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
