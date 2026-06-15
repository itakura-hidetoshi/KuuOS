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

from runtime.kuuos_indra_qi_bounded_plural_shadow_routing_core_v0_20 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_bounded_plural_shadow_routing_runtime_v0_20 import (
    BLOCKED,
    READY,
    build_bounded_plural_shadow_routing,
)


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def sources(root: pathlib.Path, decision: str) -> dict[str, Any]:
    world = {
        "version": "indra_qi_world_model_v0_1",
        "world_model_id": "world-a",
        "mandala_inclusion": {"multi_world_noncollapse": True, "single_ontology_forced": False},
        "epoch": 1,
    }
    world["indra_qi_world_state_digest"] = sha(world)

    lineage_summaries = [
        {
            "lineage_id": "l0",
            "lineage_kind": "explore",
            "coverage_ratio": 1.0,
            "frontier_participation_ratio": 0.67,
            "sustained_benefit_ratio": 1.0,
            "metric_volatility": {},
            "metric_trend": {},
        },
        {
            "lineage_id": "l1",
            "lineage_kind": "recovery",
            "coverage_ratio": 1.0,
            "frontier_participation_ratio": 0.67,
            "sustained_benefit_ratio": 1.0,
            "metric_volatility": {},
            "metric_trend": {},
        },
        {
            "lineage_id": "l2",
            "lineage_kind": "minority_preservation",
            "coverage_ratio": 1.0,
            "frontier_participation_ratio": 0.67,
            "sustained_benefit_ratio": 1.0,
            "metric_volatility": {},
            "metric_trend": {},
        },
    ]
    analysis = {
        "cycle_count": 3,
        "lineage_count": 3,
        "lineage_summaries": lineage_summaries,
        "persistent_frontier_lineage_ids": ["l0", "l1", "l2"],
        "persistent_frontier_lineage_count": 3,
        "minimum_lineage_coverage_ratio": 1.0,
        "aggregate_sustained_benefit_ratio": 1.0,
        "maximum_metric_volatility": 0.1,
        "maximum_single_lineage_frontier_share": 0.5,
        "maximum_single_lineage_only_frontier_streak": 0,
        "recovery_persistence_ratio": 1.0,
        "minority_persistence_ratio": 1.0,
        "boundary_breach_count": 0,
        "collapse_gates": {},
        "evidence_gates": {},
        "all_gates": {},
    }
    summary = {
        "version": "indra_qi_longitudinal_shadow_evidence_summary_v0_19",
        "evidence_program_id": "evidence-program-a",
        "evidence_run_id": "evidence-run-a",
        "world_model_id": "world-a",
        "source_counterfactual_decision": "shadow_counterfactual_cycle_ready",
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_latest_comparison_digest": sha({"comparison": 1}),
        "source_observation_state_digest": sha({"observation-state": 1}),
        "source_observation_recommendation_digest": sha({"observation-rec": 1}),
        "longitudinal_evidence_report_digest": sha({"report": 1}),
        "longitudinal_analysis": analysis,
        "stability_without_collapse": decision == "longitudinal_shadow_evidence_ready",
        "winner_selected": False,
        "single_lineage_truth_claimed": False,
        "recommendation_only": True,
        "epoch": 10,
    }
    summary["longitudinal_evidence_summary_digest"] = sha(summary)

    state = {
        "version": "indra_qi_longitudinal_shadow_evidence_state_v0_19",
        "evidence_program_id": "evidence-program-a",
        "world_model_id": "world-a",
        "last_evidence_run_id": "evidence-run-a",
        "last_source_world_state_digest": world["indra_qi_world_state_digest"],
        "last_source_latest_comparison_digest": summary["source_latest_comparison_digest"],
        "last_source_observation_state_digest": summary["source_observation_state_digest"],
        "last_source_observation_recommendation_digest": summary[
            "source_observation_recommendation_digest"
        ],
        "last_longitudinal_evidence_report_digest": summary["longitudinal_evidence_report_digest"],
        "latest_source_counterfactual_decision": "shadow_counterfactual_cycle_ready",
        "latest_longitudinal_evidence_decision": decision,
        "latest_longitudinal_evidence_summary_digest": summary[
            "longitudinal_evidence_summary_digest"
        ],
        "latest_longitudinal_analysis": analysis,
        "latest_longitudinal_record_digest": sha({"record": 1}),
        "prev_longitudinal_evidence_state_digest": "GENESIS",
        "boundary": {"longitudinal_evidence_state_only": True},
        "epoch": 11,
    }
    state["longitudinal_evidence_state_digest"] = sha(state)

    recommendation = {
        "version": "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19",
        "evidence_program_id": "evidence-program-a",
        "evidence_run_id": "evidence-run-a",
        "world_model_id": "world-a",
        "source_counterfactual_decision": "shadow_counterfactual_cycle_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "longitudinal_evidence_ready": decision == "longitudinal_shadow_evidence_ready",
        "winner_selected": False,
        "longitudinal_evidence_summary_digest": summary["longitudinal_evidence_summary_digest"],
        "longitudinal_analysis": analysis,
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_latest_comparison_digest": summary["source_latest_comparison_digest"],
        "source_observation_state_digest": summary["source_observation_state_digest"],
        "source_observation_recommendation_digest": summary[
            "source_observation_recommendation_digest"
        ],
        "longitudinal_evidence_report_digest": summary["longitudinal_evidence_report_digest"],
        "recommendation_only": True,
        "stability_without_collapse_not_winner_selection": True,
        "direct_winner_selection_authority": False,
        "direct_live_route_authority": False,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "epoch": 11,
    }
    recommendation["longitudinal_evidence_recommendation_digest"] = sha(recommendation)

    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_longitudinal_shadow_evidence_summary_v0_19.json", summary)
    write(root / "indra_qi_longitudinal_shadow_evidence_state_v0_19.json", state)
    write(root / "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19.json", recommendation)
    return {
        "world": world,
        "summary": summary,
        "state": state,
        "recommendation": recommendation,
    }


def plan(source: Mapping[str, Any], run_id: str = "proposal-run-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "routing_program_id": "routing-program-a",
        "proposal_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_longitudinal_summary_digest": source["summary"][
            "longitudinal_evidence_summary_digest"
        ],
        "expected_source_longitudinal_state_digest": source["state"][
            "longitudinal_evidence_state_digest"
        ],
        "expected_source_longitudinal_recommendation_digest": source["recommendation"][
            "longitudinal_evidence_recommendation_digest"
        ],
        "routing_policy": {
            "minimum_routed_lineages": 3,
            "maximum_routed_lineages": 4,
            "minimum_recovery_lineages": 1,
            "minimum_minority_lineages": 1,
            "minimum_route_share": 0.15,
            "maximum_single_route_share": 0.50,
            "maximum_total_observation_traffic_fraction": 0.25,
            "minimum_persistent_frontier_coverage_ratio": 1.0,
            "minimum_sustained_benefit_ratio": 0.66,
            "maximum_route_cycles": 3,
            "maximum_observation_budget_per_lineage": 8,
            "maximum_total_observation_budget": 20,
            "require_persistent_frontier_only": True,
            "require_recovery_lineage": True,
            "require_minority_lineage": True,
            "require_shadow_return_material": True,
            "require_proposal_only": True,
            "require_live_route_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["plural_routing_plan_digest"] = plan_digest(value)
    return value


def entry(
    lineage_id: str,
    share: float,
    *,
    activate: bool = False,
    budget: int = 5,
) -> dict[str, Any]:
    return {
        "route_slot_id": "route-" + lineage_id,
        "lineage_id": lineage_id,
        "allocation_share": share,
        "requested_route_cycles": 2,
        "observation_budget": budget,
        "shadow_return_token_digest": sha({"return": lineage_id}),
        "route_overlay_digest": sha({"overlay": lineage_id}),
        "observation_scope_digest": sha({"scope": lineage_id}),
        "routing_activation_enabled": activate,
        "live_route_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "policy_boundary_preserved": True,
    }


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    entries = [entry("l0", 0.34), entry("l1", 0.33), entry("l2", 0.33)]
    total_fraction = 0.20
    if mode == "concentrated":
        entries = [entry("l0", 0.70), entry("l1", 0.15), entry("l2", 0.15)]
    elif mode == "missing-minority":
        entries = [entry("l0", 0.50), entry("l1", 0.50)]
    elif mode == "budget":
        entries = [entry("l0", 0.34, budget=10), entry("l1", 0.33, budget=10), entry("l2", 0.33, budget=10)]
    elif mode == "activate":
        entries[0] = entry("l0", 0.34, activate=True)
    elif mode == "traffic":
        total_fraction = 0.50
    value = {
        "version": REPORT_VERSION,
        "proposal_run_id": plan_value["proposal_run_id"],
        "source_longitudinal_summary_digest": source["summary"][
            "longitudinal_evidence_summary_digest"
        ],
        "source_longitudinal_recommendation_digest": source["recommendation"][
            "longitudinal_evidence_recommendation_digest"
        ],
        "proposal_only": True,
        "routing_activation_requested": False,
        "total_observation_traffic_fraction": total_fraction,
        "route_entries": entries,
    }
    value["plural_routing_report_digest"] = report_digest(value)
    return value


def license_value(
    plan_value: Mapping[str, Any],
    report_value: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["proposal_run_id"]),
        "bound_plural_routing_plan_digest": plan_value["plural_routing_plan_digest"],
        "bound_plural_routing_report_digest": report_value["plural_routing_report_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_longitudinal_summary_digest": source["summary"][
            "longitudinal_evidence_summary_digest"
        ],
        "bound_source_longitudinal_state_digest": source["state"][
            "longitudinal_evidence_state_digest"
        ],
        "bound_source_longitudinal_recommendation_digest": source["recommendation"][
            "longitudinal_evidence_recommendation_digest"
        ],
        "state_write_allowed": True,
        "proposal_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "routing_activation_authority_granted": False,
        "winner_selection_authority_granted": False,
        "external_actuation_authority_granted": False,
        "world_update_authority_granted": False,
        "lineage_selection_authority_granted": False,
        "lineage_execution_authority_granted": False,
        "truth_authority_granted": False,
        "direct_promotion_authority_granted": False,
        "direct_rollback_authority_granted": False,
        "direct_quarantine_authority_granted": False,
    }


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_bounded_plural_shadow_routing_v0_20_enabled": True,
        "apply_indra_qi_bounded_plural_shadow_routing_v0_20": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_longitudinal_shadow_evidence_summary_v0_19.json",
        "indra_qi_longitudinal_shadow_evidence_state_v0_19.json",
        "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_bounded_plural_shadow_routing(
        runtime_context=context(root),
        plural_routing_plan=plan_value,
        plural_routing_license=license_value(plan_value, report_value, source),
        plural_routing_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(
            root, "longitudinal_shadow_evidence_ready", "ready"
        )
        assert result.status == READY
        assert result.decision == "plural_shadow_routing_proposal_ready"
        assert result.routing_activated is False
        proposal = json.loads(
            (root / "indra_qi_bounded_plural_shadow_routing_proposal_v0_20.json").read_text()
        )
        recommendation = json.loads(
            (
                root
                / "indra_qi_bounded_plural_shadow_routing_recommendation_v0_20.json"
            ).read_text()
        )
        assert proposal["proposal_only"] is True
        assert proposal["routing_activated"] is False
        assert recommendation["direct_routing_activation_authority"] is False
        replay = build_bounded_plural_shadow_routing(
            runtime_context=context(root),
            plural_routing_plan=plan_value,
            plural_routing_license=license_value(plan_value, report_value, source),
            plural_routing_report=report_value,
        )
        assert replay.status == BLOCKED
        assert "plural_routing_replay_detected" in replay.blockers

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "longitudinal_shadow_evidence_ready", "concentrated"
        )
        assert result.status == READY
        assert result.decision == "restore_shadow_diversity_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "longitudinal_shadow_evidence_ready", "missing-minority"
        )
        assert result.status == READY
        assert result.decision == "restore_shadow_diversity_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "longitudinal_shadow_evidence_ready", "budget"
        )
        assert result.status == READY
        assert result.decision == "redesign_plural_shadow_routing_proposal_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "longitudinal_shadow_evidence_ready", "traffic"
        )
        assert result.status == READY
        assert result.decision == "redesign_plural_shadow_routing_proposal_recommended"

    with tempfile.TemporaryDirectory() as directory:
        _, _, _, result = execute(
            pathlib.Path(directory), "longitudinal_shadow_evidence_ready", "activate"
        )
        assert result.status == READY
        assert result.decision == "quarantine_recommended"

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        (
            "extend_longitudinal_observation_recommended",
            "extend_longitudinal_observation_recommended",
        ),
        ("restore_shadow_diversity_recommended", "restore_shadow_diversity_recommended"),
        ("rollback_recommended", "rollback_recommended"),
        ("quarantine_recommended", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, "ready")
            assert result.status == READY
            assert result.decision == expected

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "longitudinal_shadow_evidence_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["route_entries"][0]["observation_budget"] = 999
        result = build_bounded_plural_shadow_routing(
            runtime_context=context(root),
            plural_routing_plan=plan_value,
            plural_routing_license=license_value(plan_value, report_value, source),
            plural_routing_report=report_value,
        )
        assert result.status == BLOCKED
        assert "plural_routing_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "longitudinal_shadow_evidence_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_bounded_plural_shadow_routing(
            runtime_context=context(root),
            plural_routing_plan=plan_value,
            plural_routing_license=license_value(plan_value, report_value, source),
            plural_routing_report=report_value,
        )
        assert result.status == BLOCKED
        assert "plural_routing_source_world_invalid" in result.blockers

    manifest = json.loads(
        (ROOT / "manifests/qi_bounded_plural_shadow_routing_v0_20.json").read_text()
    )
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_bounded_plural_shadow_routing_v0_20 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
