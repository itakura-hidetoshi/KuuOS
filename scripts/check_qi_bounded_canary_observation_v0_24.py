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

from runtime.kuuos_indra_qi_bounded_canary_observation_core_v0_24 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
    report_digest,
    sha,
)
from runtime.kuuos_indra_qi_bounded_canary_observation_runtime_v0_24 import (
    BLOCKED,
    READY,
    build_bounded_canary_observation,
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
    analysis = {
        "evidence_cycle_count": 3,
        "metric_means": {},
        "metric_maximums": {},
        "metric_trends": {},
        "cumulative_latency_delta_ratio": 0.18,
        "cumulative_output_divergence_score": 0.075,
        "fairness_decay": 0.01,
        "boundary_breach_count": 0,
        "diversity_gates": {},
        "stability_gates": {},
        "all_gates": {},
    }
    summary = {
        "version": "indra_qi_longitudinal_mirror_noninterference_summary_v0_23",
        "evidence_program_id": "longitudinal-mirror-program-a",
        "evidence_run_id": "longitudinal-mirror-run-a",
        "world_model_id": "world-a",
        "source_mirror_decision": "mirror_observation_admission_ready",
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_mirror_summary_digest": sha({"mirror-summary": 1}),
        "source_mirror_state_digest": sha({"mirror-state": 1}),
        "source_mirror_recommendation_digest": sha({"mirror-rec": 1}),
        "longitudinal_mirror_report_digest": sha({"longitudinal-report": 1}),
        "longitudinal_analysis": analysis,
        "raw_payload_stored": False,
        "live_response_influenced": False,
        "feedback_to_live_path_enabled": False,
        "routing_activated": False,
        "winner_selected": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": 40,
    }
    summary["longitudinal_mirror_summary_digest"] = sha(summary)
    state = {
        "version": "indra_qi_longitudinal_mirror_noninterference_state_v0_23",
        "evidence_program_id": "longitudinal-mirror-program-a",
        "world_model_id": "world-a",
        "last_evidence_run_id": "longitudinal-mirror-run-a",
        "latest_longitudinal_mirror_decision": decision,
        "latest_longitudinal_mirror_summary_digest": summary["longitudinal_mirror_summary_digest"],
        "epoch": 41,
    }
    state["longitudinal_mirror_state_digest"] = sha(state)
    recommendation = {
        "version": "indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23",
        "evidence_program_id": "longitudinal-mirror-program-a",
        "evidence_run_id": "longitudinal-mirror-run-a",
        "world_model_id": "world-a",
        "source_mirror_decision": "mirror_observation_admission_ready",
        "decision": decision,
        "decision_reasons": ["test"],
        "longitudinal_noninterference_ready": decision == "longitudinal_mirror_noninterference_ready",
        "live_response_influenced": False,
        "routing_activated": False,
        "winner_selected": False,
        "longitudinal_mirror_summary_digest": summary["longitudinal_mirror_summary_digest"],
        "longitudinal_analysis": analysis,
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "recommendation_only": True,
        "direct_live_response_influence_authority": False,
        "direct_feedback_to_live_path_authority": False,
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
        "epoch": 41,
    }
    recommendation["longitudinal_mirror_recommendation_digest"] = sha(recommendation)
    write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
    write(root / "indra_qi_longitudinal_mirror_noninterference_summary_v0_23.json", summary)
    write(root / "indra_qi_longitudinal_mirror_noninterference_state_v0_23.json", state)
    write(
        root / "indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23.json",
        recommendation,
    )
    return {"world": world, "summary": summary, "state": state, "recommendation": recommendation}


def plan(source: Mapping[str, Any], run_id: str = "canary-proposal-run-a") -> dict[str, Any]:
    value = {
        "version": PLAN_VERSION,
        "proposal_program_id": "canary-proposal-program-a",
        "proposal_run_id": run_id,
        "world_model_id": "world-a",
        "expected_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "expected_longitudinal_summary_digest": source["summary"]["longitudinal_mirror_summary_digest"],
        "expected_source_longitudinal_state_digest": source["state"]["longitudinal_mirror_state_digest"],
        "expected_source_longitudinal_recommendation_digest": source["recommendation"][
            "longitudinal_mirror_recommendation_digest"
        ],
        "canary_policy": {
            "minimum_canary_lanes": 3,
            "maximum_canary_lanes": 4,
            "minimum_recovery_lanes": 1,
            "minimum_minority_lanes": 1,
            "maximum_total_canary_fraction": 0.05,
            "maximum_single_lane_fraction": 0.025,
            "maximum_duration_seconds": 300,
            "maximum_event_budget": 30,
            "maximum_event_budget_per_lane": 12,
            "maximum_latency_guardrail_ratio": 0.20,
            "maximum_output_divergence_guardrail": 0.10,
            "minimum_fairness_guardrail_ratio": 0.80,
            "require_expiry_epoch": True,
            "require_automatic_revocation": True,
            "require_shadow_return_token": True,
            "require_rollback_receipt": True,
            "require_proposal_only": True,
            "require_canary_activation_disabled": True,
            "require_live_response_influence_disabled": True,
            "require_feedback_to_live_path_disabled": True,
            "require_external_actuation_disabled": True,
            "require_world_update_disabled": True,
            "require_policy_boundary_preserved": True,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    value["bounded_canary_plan_digest"] = plan_digest(value)
    return value


def lane(
    lineage_id: str,
    kind: str,
    fraction: float,
    proposal_epoch: int,
    *,
    budget: int = 8,
    duration: int = 240,
    activate: bool = False,
) -> dict[str, Any]:
    return {
        "lane_id": "lane-" + lineage_id,
        "lineage_id": lineage_id,
        "lineage_kind": kind,
        "canary_fraction": fraction,
        "event_budget": budget,
        "expiry_epoch": proposal_epoch + duration,
        "shadow_return_token_digest": sha({"return": lineage_id}),
        "rollback_receipt_template_digest": sha({"rollback": lineage_id}),
        "latency_guardrail_ratio": 0.15,
        "output_divergence_guardrail": 0.08,
        "fairness_guardrail_ratio": 0.90,
        "automatic_revocation_enabled": True,
        "canary_activation_enabled": activate,
        "live_response_influence_enabled": False,
        "feedback_to_live_path_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "winner_selected": False,
        "policy_boundary_preserved": True,
    }


def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str = "ready") -> dict[str, Any]:
    proposal_epoch = 1000
    lanes = [
        lane("l0", "explore", 0.020, proposal_epoch),
        lane("l1", "recovery", 0.015, proposal_epoch),
        lane("l2", "minority_preservation", 0.015, proposal_epoch),
    ]
    duration = 240
    if mode == "fraction":
        lanes[0]["canary_fraction"] = 0.040
    elif mode == "duration":
        duration = 600
        for value in lanes:
            value["expiry_epoch"] = proposal_epoch + duration
    elif mode == "budget":
        for value in lanes:
            value["event_budget"] = 15
    elif mode == "missing-minority":
        lanes = lanes[:2]
    elif mode == "activate":
        lanes[0]["canary_activation_enabled"] = True
    value = {
        "version": REPORT_VERSION,
        "proposal_run_id": plan_value["proposal_run_id"],
        "source_longitudinal_summary_digest": source["summary"]["longitudinal_mirror_summary_digest"],
        "proposal_only": True,
        "canary_activation_requested": False,
        "duration_seconds": duration,
        "proposal_epoch": proposal_epoch,
        "canary_lanes": lanes,
    }
    value["bounded_canary_report_digest"] = report_digest(value)
    return value


def license_value(
    plan_value: Mapping[str, Any],
    report_value: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "version": LICENSE_VERSION,
        "license_id": "license-" + str(plan_value["proposal_run_id"]),
        "bound_bounded_canary_plan_digest": plan_value["bounded_canary_plan_digest"],
        "bound_bounded_canary_report_digest": report_value["bounded_canary_report_digest"],
        "bound_source_world_state_digest": source["world"]["indra_qi_world_state_digest"],
        "bound_longitudinal_summary_digest": source["summary"]["longitudinal_mirror_summary_digest"],
        "bound_source_longitudinal_state_digest": source["state"]["longitudinal_mirror_state_digest"],
        "bound_source_longitudinal_recommendation_digest": source["recommendation"][
            "longitudinal_mirror_recommendation_digest"
        ],
        "state_write_allowed": True,
        "proposal_write_allowed": True,
        "ledger_append_allowed": True,
        "recommendation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "canary_activation_authority_granted": False,
        "live_response_influence_authority_granted": False,
        "feedback_to_live_path_authority_granted": False,
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
        "indra_qi_bounded_canary_observation_v0_24_enabled": True,
        "apply_indra_qi_bounded_canary_observation_v0_24": True,
    }


def execute(root: pathlib.Path, source_decision: str, mode: str = "ready"):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = (
        "ku_indra_qi_noncommutative_mandala_world_state.json",
        "indra_qi_longitudinal_mirror_noninterference_summary_v0_23.json",
        "indra_qi_longitudinal_mirror_noninterference_state_v0_23.json",
        "indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23.json",
    )
    before = {name: (root / name).read_bytes() for name in names}
    result = build_bounded_canary_observation(
        runtime_context=context(root),
        bounded_canary_plan=plan_value,
        bounded_canary_license=license_value(plan_value, report_value, source),
        bounded_canary_report=report_value,
    )
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return source, plan_value, report_value, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(
            root, "longitudinal_mirror_noninterference_ready", "ready"
        )
        assert result.status == READY
        assert result.decision == "bounded_canary_observation_proposal_ready"
        proposal = json.loads((root / "indra_qi_bounded_canary_observation_proposal_v0_24.json").read_text())
        recommendation = json.loads(
            (root / "indra_qi_bounded_canary_observation_recommendation_v0_24.json").read_text()
        )
        assert proposal["proposal_only"] is True
        assert proposal["canary_activated"] is False
        assert recommendation["direct_canary_activation_authority"] is False
        replay = build_bounded_canary_observation(
            runtime_context=context(root),
            bounded_canary_plan=plan_value,
            bounded_canary_license=license_value(plan_value, report_value, source),
            bounded_canary_report=report_value,
        )
        assert replay.status == BLOCKED
        assert "bounded_canary_replay_detected" in replay.blockers

    for mode, expected in (
        ("fraction", "redesign_bounded_canary_observation_proposal_recommended"),
        ("duration", "redesign_bounded_canary_observation_proposal_recommended"),
        ("budget", "redesign_bounded_canary_observation_proposal_recommended"),
        ("missing-minority", "restore_shadow_diversity_recommended"),
        ("activate", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(
                pathlib.Path(directory), "longitudinal_mirror_noninterference_ready", mode
            )
            assert result.status == READY
            assert result.decision == expected, (mode, result)

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        ("extend_mirror_observation_recommended", "extend_mirror_observation_recommended"),
        (
            "redesign_longitudinal_mirror_observation_recommended",
            "redesign_bounded_canary_observation_proposal_recommended",
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
        source = sources(root, "longitudinal_mirror_noninterference_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["canary_lanes"][0]["event_budget"] = 999
        result = build_bounded_canary_observation(
            runtime_context=context(root),
            bounded_canary_plan=plan_value,
            bounded_canary_license=license_value(plan_value, report_value, source),
            bounded_canary_report=report_value,
        )
        assert result.status == BLOCKED
        assert "bounded_canary_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "longitudinal_mirror_noninterference_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_bounded_canary_observation(
            runtime_context=context(root),
            bounded_canary_plan=plan_value,
            bounded_canary_license=license_value(plan_value, report_value, source),
            bounded_canary_report=report_value,
        )
        assert result.status == BLOCKED
        assert "bounded_canary_source_world_invalid" in result.blockers

    manifest = json.loads((ROOT / "manifests/qi_bounded_canary_observation_v0_24.json").read_text())
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_bounded_canary_observation_v0_24 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
