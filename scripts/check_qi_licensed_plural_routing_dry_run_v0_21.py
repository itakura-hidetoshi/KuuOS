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

from runtime.kuuos_indra_qi_licensed_plural_routing_dry_run_core_v0_21 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_licensed_plural_routing_dry_run_runtime_v0_21 import (
    BLOCKED,
    READY,
    build_licensed_plural_routing_dry_run,
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
    entries = [
        {
            "route_slot_id": "route-l0",
            "lineage_id": "l0",
            "allocation_share": 0.34,
            "requested_route_cycles": 2,
            "observation_budget": 5,
            "shadow_return_token_digest": sha({"return": "l0"}),
            "route_overlay_digest": sha({"overlay": "l0"}),
            "observation_scope_digest": sha({"scope": "l0"}),
            "lineage_kind": "explore",
            "persistent_frontier_member": True,
            "sustained_benefit_qualified": True,
            "proposal_boundary_preserved": True,
            "routing_activation_enabled": False,
            "live_route_enabled": False,
            "external_actuation_enabled": False,
            "world_update_enabled": False,
            "policy_boundary_preserved": True,
        },
        {
            "route_slot_id": "route-l1",
            "lineage_id": "l1",
            "allocation_share": 0.33,
            "requested_route_cycles": 2,
            "observation_budget": 5,
            "shadow_return_token_digest": sha({"return": "l1"}),
            "route_overlay_digest": sha({"overlay": "l1"}),
            "observation_scope_digest": sha({"scope": "l1"}),
            "lineage_kind": "recovery",
            "persistent_frontier_member": True,
            "sustained_benefit_qualified": True,
            "proposal_boundary_preserved": True,
            "routing_activation_enabled": False,
            "live_route_enabled": False,
            "external_actuation_enabled": False,
            "world_update_enabled": False,
            "policy_boundary_preserved": True,
        },
        {
            "route_slot_id": "route-l2",
            "lineage_id": "l2",
            "allocation_share": 0.33,
            "requested_route_cycles": 2,
            "observation_budget": 5,
            "shadow_return_token_digest": sha({"return": "l2"}),
            "route_overlay_digest": sha({"overlay": "l2"}),
            "observation_scope_digest": sha({"scope": "l2"}),
            "lineage_kind": "minority_preservation",
            "persistent_frontier_member": True,
            "sustained_benefit_qualified": True,
            "proposal_boundary_preserved": True,
            "routing_activation_enabled": False,
            "live_route_enabled": False,
            "external_actuation_enabled": False,
            "world_update_enabled": False,
            "policy_boundary_preserved": True,
        },
    ]
    proposal = {
        "version": "indra_qi_bounded_plural_shadow_routing_proposal_v0_20",
        "routing_program_id": "routing-program-a",
        "proposal_run_id": "proposal-run-a",
        "world_model_id": "world-a",
        "source_longitudinal_decision": "longitudinal_shadow_evidence_ready",
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_longitudinal_summary_digest": sha({"summary": 1}),
        "source_longitudinal_state_digest": sha({"state": 1}),
        "source_longitudinal_recommendation_digest": sha({"rec": 1}),
        "plural_routing_report_digest": sha({"report": 1}),
        "total_observation_traffic_fraction": 0.2,
        "route_entries": entries,
        "proposal_analysis": {},
        "proposal_only": True,
        "routing_activated": False,
        "live_route_enabled": False,
        "winner_selected": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": 10,
    }
    proposal["plural_shadow_routing_proposal_digest"] = sha(proposal)
    state = {
        "version": "indra_qi_bounded_plural_shadow_routing_state_v0_20",
        "routing_program_id": "routing-program-a",
        "world_model_id": "world-a",
        "last_proposal_run_id": "proposal-run-a",
        "latest_plural_routing_decision": decision,
        "latest_plural_shadow_routing_proposal_digest": proposal[
            "plural_shadow_routing_proposal_digest"
        ],
        "epoch": 11,
    }
    state["plural_routing_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_bounded_plural_shadow_routing_recommendation_v0_20",
        "routing_program_id": "routing-program-a",
        "proposal_run_id": "proposal-run-a",
        "world_model_id": "world-a",
        "source_longitudinal_decision": "longitudinal_shadow_evidence_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "proposal_ready": decision == "plural_shadow_routing_proposal_ready",
        "routing_activated": False,
        "winner_selected": False,
        "plural_shadow_routing_proposal_digest": proposal[
            "plural_shadow_routing_proposal_digest"
        ],
        "proposal_analysis": {},
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "recommendation_only": True,
        "proposal_not_routing_activation": True,
        "direct_routing_activation_authority": False,
        "direct_winner_selection_authority": False,
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
    recommendation["plural_routing_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_bounded_plural_shadow_routing_proposal_v0_20.json", proposal)
    write(root / "indra_qi_bounded_plural_shadow_routing_state_v0_20.json", state)
    write(root / "indra_qi_bounded_plural_shadow_routing_recommendation_v0_20.json", recommendation)
    return {"world": world, "proposal": proposal, "state": state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], run_id: str = "dry-run-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "dry_run_program_id": "dry-run-program-a",
        "dry_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_plural_routing_proposal_digest": source["proposal"][
            "plural_shadow_routing_proposal_digest"
        ],
        "expected_source_plural_routing_state_digest": source["state"][
            "plural_routing_state_digest"
        ],
        "expected_source_plural_routing_recommendation_digest": source["recommendation"][
            "plural_routing_recommendation_digest"
        ],
        "dry_run_policy": {
            "minimum_schedule_ticks": 9,
            "maximum_schedule_ticks": 18,
            "maximum_consecutive_ticks_per_lineage": 3,
            "maximum_idle_ticks": 1,
            "maximum_allocation_error": 0.10,
            "minimum_jain_fairness_index": 0.80,
            "minimum_lineage_service_ratio": 1.0,
            "maximum_replica_failure_ratio": 0.0,
            "require_exact_replica_input_binding": True,
            "require_deterministic_replay": True,
            "require_rollback_receipt": True,
            "require_replica_restore": True,
            "require_routing_activation_disabled": True,
            "require_live_route_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["plural_routing_dry_run_plan_digest"] = plan_digest(value)
    return value


def tick(
    index: int,
    lineage_id: str,
    source: Mapping[str, Any],
    replica_input: str,
    *,
    nondeterministic: bool = False,
    bad_rollback: bool = False,
    activate: bool = False,
) -> dict[str, Any]:
    route = next(
        value for value in source["proposal"]["route_entries"] if value["lineage_id"] == lineage_id
    )
    output = sha({"output": index, "lineage": lineage_id})
    rollback = sha({"rollback": index, "lineage": lineage_id})
    return {
        "tick_index": index,
        "lineage_id": lineage_id,
        "route_slot_id": route["route_slot_id"],
        "replica_input_digest": replica_input,
        "replica_snapshot_digest": sha({"snapshot": index}),
        "output_digest": output,
        "replay_output_digest": sha({"different": index}) if nondeterministic else output,
        "rollback_receipt_digest": sha({"bad": index}) if bad_rollback else rollback,
        "expected_rollback_receipt_digest": rollback,
        "routing_activation_attempted": activate,
        "live_route_attempted": False,
        "external_actuation_attempted": False,
        "world_update_attempted": False,
        "policy_boundary_preserved": True,
        "replica_restored": True,
    }


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    replica_input = sha({"replica-input": 1})
    if mode == "unfair":
        sequence = ["l0"] * 12
    elif mode == "allocation":
        sequence = ["l0"] * 6 + ["l1"] * 3 + ["l2"] * 3
    else:
        sequence = ["l0", "l1", "l2"] * 4
    ticks = [
        tick(
            index,
            lineage_id,
            source,
            replica_input,
            nondeterministic=(mode == "nondeterministic" and index == 2),
            bad_rollback=(mode == "rollback" and index == 3),
            activate=(mode == "activate" and index == 1),
        )
        for index, lineage_id in enumerate(sequence, start=1)
    ]
    value = {
        "version": REPORT_VERSION,
        "dry_run_id": plan_value["dry_run_id"],
        "source_plural_routing_proposal_digest": source["proposal"][
            "plural_shadow_routing_proposal_digest"
        ],
        "replica_input_digest": replica_input,
        "routing_activation_requested": False,
        "schedule_ticks": ticks,
    }
    value["plural_routing_dry_run_report_digest"] = report_digest(value)
    return value


def license_value(
    plan_value: Mapping[str, Any],
    report_value: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["dry_run_id"]),
        "bound_plural_routing_dry_run_plan_digest": plan_value[
            "plural_routing_dry_run_plan_digest"
        ],
        "bound_plural_routing_dry_run_report_digest": report_value[
            "plural_routing_dry_run_report_digest"
        ],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_plural_routing_proposal_digest": source["proposal"][
            "plural_shadow_routing_proposal_digest"
        ],
        "bound_source_plural_routing_state_digest": source["state"][
            "plural_routing_state_digest"
        ],
        "bound_source_plural_routing_recommendation_digest": source["recommendation"][
            "plural_routing_recommendation_digest"
        ],
        "state_write_allowed": True,
        "summary_write_allowed": True,
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
        "indra_qi_licensed_plural_routing_dry_run_v0_21_enabled": True,
        "apply_indra_qi_licensed_plural_routing_dry_run_v0_21": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_bounded_plural_shadow_routing_proposal_v0_20.json",
        "indra_qi_bounded_plural_shadow_routing_state_v0_20.json",
        "indra_qi_bounded_plural_shadow_routing_recommendation_v0_20.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_licensed_plural_routing_dry_run(
        runtime_context=context(root),
        plural_routing_dry_run_plan=plan_value,
        plural_routing_dry_run_license=license_value(plan_value, report_value, source),
        plural_routing_dry_run_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(
            root, "plural_shadow_routing_proposal_ready", "ready"
        )
        assert result.status == READY
        assert result.decision == "plural_routing_dry_run_ready"
        summary = json.loads(
            (root / "indra_qi_licensed_plural_routing_dry_run_summary_v0_21.json").read_text()
        )
        recommendation = json.loads(
            (
                root
                / "indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21.json"
            ).read_text()
        )
        assert summary["routing_activated"] is False
        assert summary["dry_run_analysis"]["jain_fairness_index"] >= 0.8
        assert recommendation["direct_routing_activation_authority"] is False
        replay = build_licensed_plural_routing_dry_run(
            runtime_context=context(root),
            plural_routing_dry_run_plan=plan_value,
            plural_routing_dry_run_license=license_value(plan_value, report_value, source),
            plural_routing_dry_run_report=report_value,
        )
        assert replay.status == BLOCKED
        assert "dry_run_replay_detected" in replay.blockers

    for mode, expected in (
        ("unfair", "restore_shadow_diversity_recommended"),
        ("allocation", "redesign_plural_routing_schedule_recommended"),
        ("nondeterministic", "redesign_plural_routing_schedule_recommended"),
        ("rollback", "redesign_plural_routing_schedule_recommended"),
        ("activate", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(
                pathlib.Path(directory), "plural_shadow_routing_proposal_ready", mode
            )
            assert result.status == READY
            assert result.decision == expected, (mode, result)

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        (
            "redesign_plural_shadow_routing_proposal_recommended",
            "redesign_plural_routing_schedule_recommended",
        ),
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
        source = sources(root, "plural_shadow_routing_proposal_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["schedule_ticks"][0]["replica_restored"] = False
        result = build_licensed_plural_routing_dry_run(
            runtime_context=context(root),
            plural_routing_dry_run_plan=plan_value,
            plural_routing_dry_run_license=license_value(plan_value, report_value, source),
            plural_routing_dry_run_report=report_value,
        )
        assert result.status == BLOCKED
        assert "dry_run_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "plural_shadow_routing_proposal_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_licensed_plural_routing_dry_run(
            runtime_context=context(root),
            plural_routing_dry_run_plan=plan_value,
            plural_routing_dry_run_license=license_value(plan_value, report_value, source),
            plural_routing_dry_run_report=report_value,
        )
        assert result.status == BLOCKED
        assert "dry_run_source_world_invalid" in result.blockers

    manifest = json.loads(
        (ROOT / "manifests/qi_licensed_plural_routing_dry_run_v0_21.json").read_text()
    )
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_licensed_plural_routing_dry_run_v0_21 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
