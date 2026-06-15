#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_shadow_counterfactual_observation_core_v0_18 import (
    DECISIONS, LEDGER_VERSION, REQUIRED_BOUNDARY, STATE_VERSION,
    analyze_projections, evaluate_cycle, mapping, sha, state_digest,
    valid_digest, validate_license, validate_plan, validate_report, validate_sources,
)

VERSION = "indra_qi_shadow_counterfactual_observation_v0_18"
READY = "INDRA_QI_SHADOW_COUNTERFACTUAL_OBSERVATION_V0_18_READY"
BLOCKED = "INDRA_QI_SHADOW_COUNTERFACTUAL_OBSERVATION_V0_18_BLOCKED"


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    observation_program_id: str
    observation_cycle_id: str
    world_model_id: str
    source_shadow_admission_decision: str
    decision: str
    recommendation_only: bool
    source_world_state_digest: str
    source_shadow_roster_digest: str
    source_admission_state_digest: str
    source_admission_recommendation_digest: str
    counterfactual_observation_report_digest: str
    counterfactual_observation_state_digest: str
    ledger_record_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def read_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dict(value) if isinstance(value, Mapping) else {}


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    output: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid": True}
        output.append(dict(value) if isinstance(value, Mapping) else {"_invalid": True})
    return output


def write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def validate_ledger(records: list[dict[str, Any]], program_id: str, world_model_id: str, blockers: list[str]) -> list[dict[str, Any]]:
    previous = "GENESIS"
    cycles: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    reports: set[str] = set()
    for index, record in enumerate(records):
        cycle = str(record.get("observation_cycle_id", ""))
        pair = (str(record.get("source_shadow_roster_digest", "")), str(record.get("source_admission_recommendation_digest", "")))
        report = str(record.get("counterfactual_observation_report_digest", ""))
        valid = (
            record.get("version") == LEDGER_VERSION
            and valid_digest(record, "record_digest")
            and record.get("prev_record_digest") == previous
            and record.get("observation_program_id") == program_id
            and record.get("world_model_id") == world_model_id
            and bool(cycle) and cycle not in cycles
            and all(pair) and pair not in pairs
            and bool(report) and report not in reports
        )
        if record.get("_invalid") or not valid:
            blockers.append(f"counterfactual_ledger_record_{index}_invalid")
        cycles.add(cycle)
        pairs.add(pair)
        reports.add(report)
        previous = str(record.get("record_digest", ""))
    return records


def build_shadow_counterfactual_observation(
    *,
    runtime_context: Mapping[str, Any],
    counterfactual_observation_plan: Mapping[str, Any],
    counterfactual_observation_license: Mapping[str, Any],
    counterfactual_observation_report: Mapping[str, Any],
) -> Result:
    context = mapping(runtime_context)
    plan = dict(mapping(counterfactual_observation_plan))
    license_value = mapping(counterfactual_observation_license)
    report = dict(mapping(counterfactual_observation_report))
    blockers: list[str] = []
    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_shadow_counterfactual_observation_v0_18_enabled") is not True or context.get("apply_indra_qi_shadow_counterfactual_observation_v0_18") is not True:
        blockers.append("counterfactual_not_enabled")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    roster = read_json(root / "indra_qi_reversible_shadow_roster_v0_17.json")
    admission_state = read_json(root / "indra_qi_reversible_shadow_admission_state_v0_17.json")
    admission_recommendation = read_json(root / "indra_qi_reversible_shadow_admission_recommendation_v0_17.json")
    source = validate_sources(world, roster, admission_state, admission_recommendation, plan, blockers)
    projections = validate_report(report, plan, source, blockers)
    validate_license(license_value, plan, report, source, blockers)

    program_id = str(plan.get("observation_program_id", ""))
    cycle_id = str(plan.get("observation_cycle_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_shadow_counterfactual_observation_ledger_v0_18.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), program_id, world_model_id, blockers)
    source_pair = (str(source.get("roster_digest", "")), str(source.get("admission_recommendation_digest", "")))
    report_sha = str(report.get("counterfactual_observation_report_digest", ""))
    if any(
        row.get("observation_cycle_id") == cycle_id
        or (row.get("source_shadow_roster_digest"), row.get("source_admission_recommendation_digest")) == source_pair
        or row.get("counterfactual_observation_report_digest") == report_sha
        for row in prior
    ):
        blockers.append("counterfactual_replay_detected")

    prior_state = read_json(root / "indra_qi_shadow_counterfactual_observation_state_v0_18.json")
    if prior_state and not valid_digest(prior_state, "counterfactual_observation_state_digest"):
        blockers.append("counterfactual_prior_state_digest_invalid")
    if prior_state and prior_state.get("last_source_admission_state_digest") == source.get("admission_state_digest"):
        blockers.append("counterfactual_source_admission_state_not_advanced")

    analysis = analyze_projections(projections, plan, source)
    evaluation = evaluate_cycle(analysis, str(source.get("source_decision", "")))
    decision = str(evaluation.get("decision", "hold_for_observation"))
    if decision not in DECISIONS:
        blockers.append("counterfactual_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        evaluation = {"decision_reasons": ["fail_closed_on_validation_or_integrity_loss"], "counterfactual_cycle_ready": False}

    now = int(time.time())
    source_fields = {
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_shadow_roster_digest": str(source.get("roster_digest", "")),
        "source_admission_state_digest": str(source.get("admission_state_digest", "")),
        "source_admission_recommendation_digest": str(source.get("admission_recommendation_digest", "")),
        "counterfactual_observation_report_digest": report_sha,
    }
    no_authority = {
        "direct_live_route_authority": False,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
    }
    analysis_summary = {key: value for key, value in analysis.items() if key != "projections"}
    comparison = {
        "version": "indra_qi_shadow_counterfactual_comparison_v0_18",
        "observation_program_id": program_id,
        "observation_cycle_id": cycle_id,
        "world_model_id": world_model_id,
        "source_shadow_admission_decision": str(source.get("source_decision", "")),
        "shared_observation_input_digest": str(report.get("shared_observation_input_digest", "")),
        **source_fields,
        "projection_analysis": dict(analysis),
        "pareto_frontier_not_winner_selection": True,
        "winner_selected": False,
        "live_route_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": now,
    }
    comparison["counterfactual_comparison_digest"] = sha(comparison)
    recommendation = {
        "version": "indra_qi_shadow_counterfactual_observation_recommendation_v0_18",
        "observation_program_id": program_id,
        "observation_cycle_id": cycle_id,
        "world_model_id": world_model_id,
        "source_shadow_admission_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "decision_reasons": list(evaluation.get("decision_reasons", [])),
        "counterfactual_cycle_ready": bool(evaluation.get("counterfactual_cycle_ready")),
        "winner_selected": False,
        "counterfactual_comparison_digest": comparison["counterfactual_comparison_digest"],
        "pareto_frontier_lineage_ids": list(analysis.get("pareto_frontier_lineage_ids", [])),
        "projection_analysis": analysis_summary,
        **source_fields,
        "recommendation_only": True,
        "pareto_frontier_not_winner_selection": True,
        **no_authority,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation["counterfactual_observation_recommendation_digest"] = sha(recommendation)
    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "shadow_counterfactual_observation_cycle",
        "observation_program_id": program_id,
        "observation_cycle_id": cycle_id,
        "world_model_id": world_model_id,
        **source_fields,
        "source_admission_run_id": str(source.get("source_admission_run_id", "")),
        "source_shadow_admission_decision": str(source.get("source_decision", "")),
        "counterfactual_comparison_digest": comparison["counterfactual_comparison_digest"],
        "projection_analysis": analysis_summary,
        "decision": decision,
        "winner_selected": False,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {**REQUIRED_BOUNDARY, "source_files_unchanged": True, "no_route_or_execution": True},
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)
    state = {
        "version": STATE_VERSION,
        "observation_program_id": program_id,
        "world_model_id": world_model_id,
        "last_observation_cycle_id": cycle_id,
        "last_source_world_state_digest": source_fields["source_world_state_digest"],
        "last_source_shadow_roster_digest": source_fields["source_shadow_roster_digest"],
        "last_source_admission_state_digest": source_fields["source_admission_state_digest"],
        "last_source_admission_recommendation_digest": source_fields["source_admission_recommendation_digest"],
        "last_counterfactual_observation_report_digest": report_sha,
        "latest_source_shadow_admission_decision": str(source.get("source_decision", "")),
        "latest_counterfactual_observation_decision": decision,
        "latest_counterfactual_comparison_digest": comparison["counterfactual_comparison_digest"],
        "latest_projection_analysis": analysis_summary,
        "latest_counterfactual_record_digest": ledger["record_digest"],
        "prev_counterfactual_observation_state_digest": str(prior_state.get("counterfactual_observation_state_digest", "GENESIS")) if prior_state else "GENESIS",
        "boundary": {"counterfactual_observation_state_only": True, "winner_selected": False, "recommendation_only": True},
        "epoch": now,
    }
    state["counterfactual_observation_state_digest"] = state_digest(state)

    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "observation_program_id": program_id,
        "observation_cycle_id": cycle_id,
        "world_model_id": world_model_id,
        "source_shadow_admission_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "winner_selected": False,
        "recommendation_only": True,
        **source_fields,
        "counterfactual_comparison_digest": comparison["counterfactual_comparison_digest"] if not blockers else "",
        "counterfactual_observation_state_digest": str(state.get("counterfactual_observation_state_digest", "")) if not blockers else str(prior_state.get("counterfactual_observation_state_digest", "")),
        "ledger_record_digest": str(ledger.get("record_digest", "")) if not blockers else "",
        "blockers": blockers,
        "boundary": {**REQUIRED_BOUNDARY, "counterfactual_observation_committed": not blockers},
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-shadow-counterfactual-observation-" + sha(receipt)[:16]

    if not blockers:
        write_json(root / "indra_qi_shadow_counterfactual_comparison_v0_18.json", comparison)
        write_json(root / "indra_qi_shadow_counterfactual_observation_recommendation_v0_18.json", recommendation)
        write_json(root / "indra_qi_shadow_counterfactual_observation_state_v0_18.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_shadow_counterfactual_observation_receipt_v0_18.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(root / "indra_qi_shadow_counterfactual_observation_audit_v0_18.jsonl", {**receipt, "audit_record_digest": sha(receipt)})

    return Result(
        VERSION, status, str(receipt["packet_id"]), str(root), program_id, cycle_id, world_model_id,
        str(source.get("source_decision", "")), decision, True,
        source_fields["source_world_state_digest"], source_fields["source_shadow_roster_digest"],
        source_fields["source_admission_state_digest"], source_fields["source_admission_recommendation_digest"],
        report_sha,
        str(state.get("counterfactual_observation_state_digest", "")) if not blockers else str(prior_state.get("counterfactual_observation_state_digest", "")),
        str(ledger.get("record_digest", "")) if not blockers else "", blockers,
    )
