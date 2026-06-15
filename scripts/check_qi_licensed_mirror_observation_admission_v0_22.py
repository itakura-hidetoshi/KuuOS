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

from runtime.kuuos_indra_qi_licensed_mirror_observation_admission_core_v0_22 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_licensed_mirror_observation_admission_runtime_v0_22 import (
    BLOCKED,
    READY,
    build_licensed_mirror_observation_admission,
)


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def source_tick(index: int, lineage_id: str) -> dict[str, Any]:
    output = sha({"dry-output": index, "lineage": lineage_id})
    return {
        "tick_index": index,
        "lineage_id": lineage_id,
        "route_slot_id": "route-" + lineage_id,
        "replica_input_digest": sha({"replica-input": 1}),
        "replica_snapshot_digest": sha({"snapshot": index}),
        "output_digest": output,
        "replay_output_digest": output,
        "rollback_receipt_digest": sha({"rollback": index}),
        "expected_rollback_receipt_digest": sha({"rollback": index}),
        "routing_activation_attempted": False,
        "live_route_attempted": False,
        "external_actuation_attempted": False,
        "world_update_attempted": False,
        "policy_boundary_preserved": True,
        "replica_restored": True,
        "deterministic_replay": True,
        "rollback_receipt_match": True,
        "replica_restore_verified": True,
        "isolation_boundary_preserved": True,
    }


def sources(root: pathlib.Path, decision: str) -> dict[str, Any]:
    world = {
        "version": "indra_qi_world_model_v0_1",
        "world_model_id": "world-a",
        "mandala_inclusion": {"multi_world_noncollapse": True, "single_ontology_forced": False},
        "epoch": 1,
    }
    world["indra_qi_world_state_digest"] = sha(world)
    sequence = ["l0", "l1", "l2"] * 4
    ticks = [source_tick(index, lineage) for index, lineage in enumerate(sequence, start=1)]
    analysis = {
        "schedule_tick_count": len(ticks),
        "lineage_count": 3,
        "target_allocation": {"l0": 0.34, "l1": 0.33, "l2": 0.33},
        "realized_allocation": {"l0": 0.33333333, "l1": 0.33333333, "l2": 0.33333333},
        "allocation_error": {"l0": 0.00666667, "l1": 0.00333333, "l2": 0.00333333},
        "maximum_allocation_error": 0.00666667,
        "lineage_service_ratio": 1.0,
        "jain_fairness_index": 1.0,
        "maximum_consecutive_ticks_per_lineage": 1,
        "replica_failure_ratio": 0.0,
        "boundary_breach_count": 0,
        "tick_results": ticks,
        "diversity_gates": {},
        "schedule_gates": {},
        "all_gates": {},
    }
    summary = {
        "version": "indra_qi_licensed_plural_routing_dry_run_summary_v0_21",
        "dry_run_program_id": "dry-run-program-a",
        "dry_run_id": "dry-run-a",
        "world_model_id": "world-a",
        "source_plural_routing_decision": "plural_shadow_routing_proposal_ready",
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_plural_routing_proposal_digest": sha({"proposal": 1}),
        "source_plural_routing_state_digest": sha({"state": 1}),
        "source_plural_routing_recommendation_digest": sha({"recommendation": 1}),
        "plural_routing_dry_run_report_digest": sha({"dry-report": 1}),
        "replica_input_digest": sha({"replica-input": 1}),
        "dry_run_analysis": analysis,
        "isolated_replica_stream_only": True,
        "routing_activated": False,
        "live_route_enabled": False,
        "winner_selected": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": 20,
    }
    summary["plural_routing_dry_run_summary_digest"] = sha(summary)
    state = {
        "version": "indra_qi_licensed_plural_routing_dry_run_state_v0_21",
        "dry_run_program_id": "dry-run-program-a",
        "world_model_id": "world-a",
        "last_dry_run_id": "dry-run-a",
        "latest_plural_routing_dry_run_decision": decision,
        "latest_plural_routing_dry_run_summary_digest": summary[
            "plural_routing_dry_run_summary_digest"
        ],
        "epoch": 21,
    }
    state["plural_routing_dry_run_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21",
        "dry_run_program_id": "dry-run-program-a",
        "dry_run_id": "dry-run-a",
        "world_model_id": "world-a",
        "source_plural_routing_decision": "plural_shadow_routing_proposal_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "dry_run_ready": decision == "plural_routing_dry_run_ready",
        "routing_activated": False,
        "winner_selected": False,
        "plural_routing_dry_run_summary_digest": summary[
            "plural_routing_dry_run_summary_digest"
        ],
        "dry_run_analysis": {key: value for key, value in analysis.items() if key != "tick_results"},
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "recommendation_only": True,
        "dry_run_not_routing_activation": True,
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
        "epoch": 21,
    }
    recommendation["plural_routing_dry_run_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_licensed_plural_routing_dry_run_summary_v0_21.json", summary)
    write(root / "indra_qi_licensed_plural_routing_dry_run_state_v0_21.json", state)
    write(
        root / "indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21.json",
        recommendation,
    )
    return {
        "world": world,
        "summary": summary,
        "state": state,
        "recommendation": recommendation,
    }


def plan(source: Mapping[str, Any], admission_id: str = "mirror-admission-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "mirror_program_id": "mirror-program-a",
        "mirror_admission_id": admission_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_dry_run_summary_digest": source["summary"][
            "plural_routing_dry_run_summary_digest"
        ],
        "expected_source_dry_run_state_digest": source["state"][
            "plural_routing_dry_run_state_digest"
        ],
        "expected_source_dry_run_recommendation_digest": source["recommendation"][
            "plural_routing_dry_run_recommendation_digest"
        ],
        "mirror_policy": {
            "minimum_mirror_events": 4,
            "maximum_mirror_events": 16,
            "maximum_capture_fraction": 0.20,
            "maximum_latency_delta_ratio": 0.20,
            "maximum_output_divergence_score": 0.10,
            "maximum_allocation_drift": 0.10,
            "minimum_schedule_agreement_ratio": 1.0,
            "minimum_fairness_preservation_ratio": 0.80,
            "maximum_redaction_failure_ratio": 0.0,
            "maximum_live_response_influence_ratio": 0.0,
            "maximum_mirror_delivery_failure_ratio": 0.0,
            "require_exact_source_input_binding": True,
            "require_redaction_receipt": True,
            "require_deterministic_mirror_replay": True,
            "require_replica_restore": True,
            "require_live_response_unchanged": True,
            "require_feedback_to_live_path_disabled": True,
            "require_routing_activation_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["mirror_observation_plan_digest"] = plan_digest(value)
    return value


def event(
    event_index: int,
    dry_tick: Mapping[str, Any],
    *,
    latency: float = 0.05,
    divergence: float = 0.02,
    nondeterministic: bool = False,
    bad_redaction: bool = False,
    live_influence: bool = False,
    restore: bool = True,
) -> dict[str, Any]:
    source_request = sha({"source-request": event_index})
    redaction = sha({"redaction": event_index})
    expected_redaction = sha({"wrong-redaction": event_index}) if bad_redaction else redaction
    mirrored = sha(
        {
            "source_request_digest": source_request,
            "redaction_receipt_digest": redaction,
        }
    )
    mirror_output = sha({"mirror-output": event_index, "lineage": dry_tick["lineage_id"]})
    live_before = sha({"live-response": event_index})
    live_after = sha({"changed-live-response": event_index}) if live_influence else live_before
    return {
        "event_index": event_index,
        "dry_run_tick_index": dry_tick["tick_index"],
        "lineage_id": dry_tick["lineage_id"],
        "route_slot_id": dry_tick["route_slot_id"],
        "source_request_digest": source_request,
        "mirrored_request_digest": mirrored,
        "redaction_receipt_digest": redaction,
        "expected_redaction_receipt_digest": expected_redaction,
        "dry_run_output_digest": dry_tick["output_digest"],
        "mirror_output_digest": mirror_output,
        "replay_output_digest": sha({"different": event_index})
        if nondeterministic
        else mirror_output,
        "live_response_digest_before": live_before,
        "live_response_digest_after": live_after,
        "replica_snapshot_digest": sha({"mirror-snapshot": event_index}),
        "latency_delta_ratio": latency,
        "output_divergence_score": divergence,
        "feedback_to_live_path_attempted": live_influence,
        "routing_activation_attempted": False,
        "external_actuation_attempted": False,
        "world_update_attempted": False,
        "policy_boundary_preserved": True,
        "replica_restored": restore,
    }


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    ticks = source["summary"]["dry_run_analysis"]["tick_results"]
    if mode == "unfair":
        selected = [tick for tick in ticks if tick["lineage_id"] == "l0"]
    else:
        selected = ticks[:12]
    events = [
        event(
            index,
            tick_value,
            latency=0.40 if mode == "latency" and index == 2 else 0.05,
            divergence=0.30 if mode == "divergence" and index == 3 else 0.02,
            nondeterministic=mode == "nondeterministic" and index == 4,
            bad_redaction=mode == "redaction" and index == 5,
            live_influence=mode == "live" and index == 1,
            restore=not (mode == "restore" and index == 6),
        )
        for index, tick_value in enumerate(selected, start=1)
    ]
    value = {
        "version": REPORT_VERSION,
        "mirror_admission_id": plan_value["mirror_admission_id"],
        "source_dry_run_summary_digest": source["summary"][
            "plural_routing_dry_run_summary_digest"
        ],
        "capture_fraction": 0.10,
        "raw_payload_stored": False,
        "mirror_events": events,
    }
    value["mirror_observation_report_digest"] = report_digest(value)
    return value


def license_value(
    plan_value: Mapping[str, Any],
    report_value: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["mirror_admission_id"]),
        "bound_mirror_observation_plan_digest": plan_value["mirror_observation_plan_digest"],
        "bound_mirror_observation_report_digest": report_value[
            "mirror_observation_report_digest"
        ],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_dry_run_summary_digest": source["summary"][
            "plural_routing_dry_run_summary_digest"
        ],
        "bound_source_dry_run_state_digest": source["state"][
            "plural_routing_dry_run_state_digest"
        ],
        "bound_source_dry_run_recommendation_digest": source["recommendation"][
            "plural_routing_dry_run_recommendation_digest"
        ],
        "state_write_allowed": True,
        "summary_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "live_response_influence_authority_granted": False,
        "feedback_to_live_path_authority_granted": False,
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
        "indra_qi_licensed_mirror_observation_admission_v0_22_enabled": True,
        "apply_indra_qi_licensed_mirror_observation_admission_v0_22": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_licensed_plural_routing_dry_run_summary_v0_21.json",
        "indra_qi_licensed_plural_routing_dry_run_state_v0_21.json",
        "indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_licensed_mirror_observation_admission(
        runtime_context=context(root),
        mirror_observation_plan=plan_value,
        mirror_observation_license=license_value(plan_value, report_value, source),
        mirror_observation_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(
            root, "plural_routing_dry_run_ready", "ready"
        )
        assert result.status == READY
        assert result.decision == "mirror_observation_admission_ready"
        summary = json.loads(
            (
                root
                / "indra_qi_licensed_mirror_observation_admission_summary_v0_22.json"
            ).read_text()
        )
        recommendation = json.loads(
            (
                root
                / "indra_qi_licensed_mirror_observation_admission_recommendation_v0_22.json"
            ).read_text()
        )
        assert summary["raw_payload_stored"] is False
        assert summary["live_response_influenced"] is False
        assert recommendation["direct_live_response_influence_authority"] is False
        replay = build_licensed_mirror_observation_admission(
            runtime_context=context(root),
            mirror_observation_plan=plan_value,
            mirror_observation_license=license_value(plan_value, report_value, source),
            mirror_observation_report=report_value,
        )
        assert replay.status == BLOCKED
        assert "mirror_replay_detected" in replay.blockers

    for mode, expected in (
        ("unfair", "restore_shadow_diversity_recommended"),
        ("latency", "redesign_mirror_observation_admission_recommended"),
        ("divergence", "redesign_mirror_observation_admission_recommended"),
        ("nondeterministic", "redesign_mirror_observation_admission_recommended"),
        ("redaction", "redesign_mirror_observation_admission_recommended"),
        ("restore", "redesign_mirror_observation_admission_recommended"),
        ("live", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(
                pathlib.Path(directory), "plural_routing_dry_run_ready", mode
            )
            assert result.status == READY
            assert result.decision == expected, (mode, result)

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        (
            "redesign_plural_routing_schedule_recommended",
            "redesign_mirror_observation_admission_recommended",
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
        source = sources(root, "plural_routing_dry_run_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["mirror_events"][0]["replica_restored"] = False
        result = build_licensed_mirror_observation_admission(
            runtime_context=context(root),
            mirror_observation_plan=plan_value,
            mirror_observation_license=license_value(plan_value, report_value, source),
            mirror_observation_report=report_value,
        )
        assert result.status == BLOCKED
        assert "mirror_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "plural_routing_dry_run_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_licensed_mirror_observation_admission(
            runtime_context=context(root),
            mirror_observation_plan=plan_value,
            mirror_observation_license=license_value(plan_value, report_value, source),
            mirror_observation_report=report_value,
        )
        assert result.status == BLOCKED
        assert "mirror_source_world_invalid" in result.blockers

    manifest = json.loads(
        (ROOT / "manifests/qi_licensed_mirror_observation_admission_v0_22.json").read_text()
    )
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_licensed_mirror_observation_admission_v0_22 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
