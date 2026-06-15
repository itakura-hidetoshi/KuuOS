#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_licensed_canary_observation_trial_support_v0_25 import *

@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    trial_program_id: str
    trial_run_id: str
    world_model_id: str
    source_canary_decision: str
    decision: str
    recommendation_only: bool
    live_canary_activated: bool
    source_world_state_digest: str
    source_canary_proposal_digest: str
    source_canary_state_digest: str
    source_canary_recommendation_digest: str
    canary_trial_report_digest: str
    canary_trial_state_digest: str
    ledger_record_digest: str
    blockers: list[str]


def validate_ledger(
    records: list[dict[str, Any]],
    program_id: str,
    world_model_id: str,
    blockers: list[str],
) -> list[dict[str, Any]]:
    previous = "GENESIS"
    runs: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    reports: set[str] = set()
    for index, record in enumerate(records):
        run_id = str(record.get("trial_run_id", ""))
        pair = (
            str(record.get("source_canary_proposal_digest", "")),
            str(record.get("source_canary_recommendation_digest", "")),
        )
        report_sha = str(record.get("canary_trial_report_digest", ""))
        valid = (
            record.get("version") == LEDGER_VERSION
            and valid_digest(record, "record_digest")
            and record.get("prev_record_digest") == previous
            and record.get("trial_program_id") == program_id
            and record.get("world_model_id") == world_model_id
            and bool(run_id)
            and run_id not in runs
            and all(pair)
            and pair not in pairs
            and bool(report_sha)
            and report_sha not in reports
        )
        if record.get("_invalid") or not valid:
            blockers.append(f"canary_trial_ledger_record_{index}_invalid")
        runs.add(run_id)
        pairs.add(pair)
        reports.add(report_sha)
        previous = str(record.get("record_digest", ""))
    return records


def build_licensed_canary_observation_trial(
    *,
    runtime_context: Mapping[str, Any],
    canary_trial_plan: Mapping[str, Any],
    canary_trial_license: Mapping[str, Any],
    canary_trial_report: Mapping[str, Any],
) -> Result:
    context = mapping(runtime_context)
    plan = dict(mapping(canary_trial_plan))
    license_value = mapping(canary_trial_license)
    report = dict(mapping(canary_trial_report))
    blockers: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_licensed_canary_observation_trial_v0_25_enabled") is not True:
        blockers.append("canary_trial_enabled_not_true")
    if context.get("apply_indra_qi_licensed_canary_observation_trial_v0_25") is not True:
        blockers.append("canary_trial_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    proposal = read_json(root / "indra_qi_bounded_canary_observation_proposal_v0_24.json")
    source_state = read_json(root / "indra_qi_bounded_canary_observation_state_v0_24.json")
    source_recommendation = read_json(root / "indra_qi_bounded_canary_observation_recommendation_v0_24.json")
    source = validate_sources(world, proposal, source_state, source_recommendation, plan, blockers)
    trial_lanes, events = validate_report(report, plan, source, blockers)
    validate_license(license_value, plan, report, source, blockers)

    program_id = str(plan.get("trial_program_id", ""))
    run_id = str(plan.get("trial_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_licensed_canary_observation_trial_ledger_v0_25.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), program_id, world_model_id, blockers)
    pair = (str(source.get("proposal_digest", "")), str(source.get("recommendation_digest", "")))
    report_sha = str(report.get("canary_trial_report_digest", ""))
    if any(
        record.get("trial_run_id") == run_id
        or (
            record.get("source_canary_proposal_digest"),
            record.get("source_canary_recommendation_digest"),
        )
        == pair
        or record.get("canary_trial_report_digest") == report_sha
        for record in prior
    ):
        blockers.append("canary_trial_replay_detected")

    prior_state = read_json(root / "indra_qi_licensed_canary_observation_trial_state_v0_25.json")
    if prior_state and not valid_digest(prior_state, "canary_trial_state_digest"):
        blockers.append("canary_trial_prior_state_digest_invalid")
    if prior_state and prior_state.get("last_source_canary_state_digest") == source.get("state_digest"):
        blockers.append("canary_trial_source_canary_state_not_advanced")

    analysis = analyze_trial(trial_lanes, events, report, plan, source)
    decision, reason = evaluate_trial(analysis, str(source.get("source_decision", "")))
    if decision not in DECISIONS:
        blockers.append("canary_trial_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        reason = "fail_closed_on_validation_or_integrity_loss"

    now = int(time.time())
    source_fields = {
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_canary_proposal_digest": str(source.get("proposal_digest", "")),
        "source_canary_state_digest": str(source.get("state_digest", "")),
        "source_canary_recommendation_digest": str(source.get("recommendation_digest", "")),
        "canary_trial_report_digest": report_sha,
    }
    summary = {
        "version": "indra_qi_licensed_canary_observation_trial_summary_v0_25",
        "trial_program_id": program_id,
        "trial_run_id": run_id,
        "world_model_id": world_model_id,
        "source_canary_decision": str(source.get("source_decision", "")),
        **source_fields,
        "trial_analysis": analysis,
        "observation_copy_trial_completed": True,
        "raw_payload_stored": False,
        "live_canary_activated": False,
        "live_response_influenced": False,
        "feedback_to_live_path_enabled": False,
        "winner_selected": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": now,
    }
    summary["canary_trial_summary_digest"] = sha(summary)
    authority = {
        "direct_live_canary_activation_authority": False,
        "direct_live_response_influence_authority": False,
        "direct_feedback_to_live_path_authority": False,
        "direct_winner_selection_authority": False,
        "direct_lineage_selection_authority": False,
        "direct_live_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
    }
    recommendation = {
        "version": "indra_qi_licensed_canary_observation_trial_recommendation_v0_25",
        "trial_program_id": program_id,
        "trial_run_id": run_id,
        "world_model_id": world_model_id,
        "source_canary_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "decision_reasons": [reason],
        "trial_ready": decision == "licensed_canary_observation_trial_ready",
        "live_canary_activated": False,
        "live_response_influenced": False,
        "winner_selected": False,
        "canary_trial_summary_digest": summary["canary_trial_summary_digest"],
        "trial_analysis": {key: value for key, value in analysis.items() if key not in {"trial_lanes", "trial_events"}},
        **source_fields,
        "recommendation_only": True,
        "observation_copy_trial_not_live_canary_activation": True,
        **authority,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation["canary_trial_recommendation_digest"] = sha(recommendation)
    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "licensed_canary_observation_trial",
        "trial_program_id": program_id,
        "trial_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "source_proposal_run_id": str(source.get("source_proposal_run_id", "")),
        "source_canary_decision": str(source.get("source_decision", "")),
        "canary_trial_summary_digest": summary["canary_trial_summary_digest"],
        "trial_analysis": {key: value for key, value in analysis.items() if key not in {"trial_lanes", "trial_events"}},
        "decision": decision,
        "live_canary_activated": False,
        "live_response_influenced": False,
        "winner_selected": False,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {
            **REQUIRED_BOUNDARY,
            "source_files_unchanged": True,
            "observation_copy_trial_completed": not blockers,
            "no_live_canary_activated": True,
            "no_live_response_influence": True,
            "no_feedback_to_live_path": True,
            "no_winner_selected": True,
        },
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)
    state = {
        "version": STATE_VERSION,
        "trial_program_id": program_id,
        "world_model_id": world_model_id,
        "last_trial_run_id": run_id,
        "last_source_world_state_digest": source_fields["source_world_state_digest"],
        "last_source_canary_proposal_digest": source_fields["source_canary_proposal_digest"],
        "last_source_canary_state_digest": source_fields["source_canary_state_digest"],
        "last_source_canary_recommendation_digest": source_fields["source_canary_recommendation_digest"],
        "last_canary_trial_report_digest": report_sha,
        "latest_source_canary_decision": str(source.get("source_decision", "")),
        "latest_canary_trial_decision": decision,
        "latest_canary_trial_summary_digest": summary["canary_trial_summary_digest"],
        "latest_trial_analysis": {
            key: value for key, value in analysis.items() if key not in {"trial_lanes", "trial_events"}
        },
        "latest_canary_trial_record_digest": ledger["record_digest"],
        "prev_canary_trial_state_digest": str(prior_state.get("canary_trial_state_digest", "GENESIS"))
        if prior_state
        else "GENESIS",
        "boundary": {
            "canary_trial_state_only": True,
            "observation_copy_trial_completed": not blockers,
            "live_canary_activated": False,
            "live_response_influenced": False,
            "feedback_to_live_path_enabled": False,
            "winner_selected": False,
            "recommendation_only": True,
            "multi_world_noncollapse_preserved": True,
        },
        "epoch": now,
    }
    state["canary_trial_state_digest"] = state_digest(state)
    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "trial_program_id": program_id,
        "trial_run_id": run_id,
        "world_model_id": world_model_id,
        "source_canary_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "live_canary_activated": False,
        "live_response_influenced": False,
        "winner_selected": False,
        "recommendation_only": True,
        **source_fields,
        "canary_trial_summary_digest": summary["canary_trial_summary_digest"] if not blockers else "",
        "canary_trial_state_digest": state["canary_trial_state_digest"]
        if not blockers
        else str(prior_state.get("canary_trial_state_digest", "")),
        "ledger_record_digest": ledger["record_digest"] if not blockers else "",
        "blockers": blockers,
        "boundary": {**REQUIRED_BOUNDARY, "canary_trial_observation_committed": not blockers},
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-licensed-canary-observation-trial-" + sha(receipt)[:16]

    if not blockers:
        write_json(root / "indra_qi_licensed_canary_observation_trial_summary_v0_25.json", summary)
        write_json(
            root / "indra_qi_licensed_canary_observation_trial_recommendation_v0_25.json",
            recommendation,
        )
        write_json(root / "indra_qi_licensed_canary_observation_trial_state_v0_25.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_licensed_canary_observation_trial_receipt_v0_25.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(
            root / "indra_qi_licensed_canary_observation_trial_audit_v0_25.jsonl",
            {**receipt, "audit_record_digest": sha(receipt)},
        )

    return Result(
        VERSION,
        status,
        str(receipt["packet_id"]),
        str(root),
        program_id,
        run_id,
        world_model_id,
        str(source.get("source_decision", "")),
        decision,
        True,
        False,
        source_fields["source_world_state_digest"],
        source_fields["source_canary_proposal_digest"],
        source_fields["source_canary_state_digest"],
        source_fields["source_canary_recommendation_digest"],
        report_sha,
        state["canary_trial_state_digest"]
        if not blockers
        else str(prior_state.get("canary_trial_state_digest", "")),
        ledger["record_digest"] if not blockers else "",
        blockers,
    )
