#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_longitudinal_shadow_evidence_core_v0_19 import (
    DECISIONS,
    LEDGER_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    analyze_longitudinal,
    evaluate_longitudinal,
    mapping,
    sha,
    state_digest,
    valid_digest,
    validate_license,
    validate_plan,
    validate_report,
    validate_sources,
)

VERSION = "indra_qi_longitudinal_shadow_evidence_v0_19"
READY = "INDRA_QI_LONGITUDINAL_SHADOW_EVIDENCE_V0_19_READY"
BLOCKED = "INDRA_QI_LONGITUDINAL_SHADOW_EVIDENCE_V0_19_BLOCKED"


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    evidence_program_id: str
    evidence_run_id: str
    world_model_id: str
    source_counterfactual_decision: str
    decision: str
    recommendation_only: bool
    source_world_state_digest: str
    source_latest_comparison_digest: str
    source_observation_state_digest: str
    source_observation_recommendation_digest: str
    longitudinal_evidence_report_digest: str
    longitudinal_evidence_state_digest: str
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
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for line in lines:
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
    runs: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    reports: set[str] = set()
    for index, record in enumerate(records):
        run_id = str(record.get("evidence_run_id", ""))
        pair = (
            str(record.get("source_latest_comparison_digest", "")),
            str(record.get("source_observation_recommendation_digest", "")),
        )
        report_sha = str(record.get("longitudinal_evidence_report_digest", ""))
        valid = (
            record.get("version") == LEDGER_VERSION
            and valid_digest(record, "record_digest")
            and record.get("prev_record_digest") == previous
            and record.get("evidence_program_id") == program_id
            and record.get("world_model_id") == world_model_id
            and bool(run_id) and run_id not in runs
            and all(pair) and pair not in pairs
            and bool(report_sha) and report_sha not in reports
        )
        if record.get("_invalid") or not valid:
            blockers.append(f"longitudinal_ledger_record_{index}_invalid")
        runs.add(run_id)
        pairs.add(pair)
        reports.add(report_sha)
        previous = str(record.get("record_digest", ""))
    return records


def build_longitudinal_shadow_evidence(
    *,
    runtime_context: Mapping[str, Any],
    longitudinal_evidence_plan: Mapping[str, Any],
    longitudinal_evidence_license: Mapping[str, Any],
    longitudinal_evidence_report: Mapping[str, Any],
) -> Result:
    context = mapping(runtime_context)
    plan = dict(mapping(longitudinal_evidence_plan))
    license_value = mapping(longitudinal_evidence_license)
    report = dict(mapping(longitudinal_evidence_report))
    blockers: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_longitudinal_shadow_evidence_v0_19_enabled") is not True:
        blockers.append("longitudinal_enabled_not_true")
    if context.get("apply_indra_qi_longitudinal_shadow_evidence_v0_19") is not True:
        blockers.append("longitudinal_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    comparison = read_json(root / "indra_qi_shadow_counterfactual_comparison_v0_18.json")
    observation_state = read_json(root / "indra_qi_shadow_counterfactual_observation_state_v0_18.json")
    observation_recommendation = read_json(root / "indra_qi_shadow_counterfactual_observation_recommendation_v0_18.json")
    source = validate_sources(world, comparison, observation_state, observation_recommendation, plan, blockers)
    cycles = validate_report(report, plan, source, blockers)
    validate_license(license_value, plan, report, source, blockers)

    program_id = str(plan.get("evidence_program_id", ""))
    run_id = str(plan.get("evidence_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_longitudinal_shadow_evidence_ledger_v0_19.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), program_id, world_model_id, blockers)
    pair = (
        str(source.get("latest_comparison_digest", "")),
        str(source.get("observation_recommendation_digest", "")),
    )
    report_sha = str(report.get("longitudinal_evidence_report_digest", ""))
    if any(
        record.get("evidence_run_id") == run_id
        or (
            record.get("source_latest_comparison_digest"),
            record.get("source_observation_recommendation_digest"),
        ) == pair
        or record.get("longitudinal_evidence_report_digest") == report_sha
        for record in prior
    ):
        blockers.append("longitudinal_replay_detected")

    prior_state = read_json(root / "indra_qi_longitudinal_shadow_evidence_state_v0_19.json")
    if prior_state and not valid_digest(prior_state, "longitudinal_evidence_state_digest"):
        blockers.append("longitudinal_prior_state_digest_invalid")
    if prior_state:
        if prior_state.get("evidence_program_id") != program_id or prior_state.get("world_model_id") != world_model_id:
            blockers.append("longitudinal_prior_state_scope_mismatch")
        if prior_state.get("last_source_observation_state_digest") == source.get("observation_state_digest"):
            blockers.append("longitudinal_source_observation_state_not_advanced")

    analysis = analyze_longitudinal(cycles, plan)
    evaluation = evaluate_longitudinal(analysis, str(source.get("source_decision", "")))
    decision = str(evaluation.get("decision", "hold_for_observation"))
    if decision not in DECISIONS:
        blockers.append("longitudinal_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        evaluation = {
            "decision_reasons": ["fail_closed_on_validation_or_integrity_loss"],
            "longitudinal_evidence_ready": False,
            "winner_selected": False,
        }

    now = int(time.time())
    source_fields = {
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_latest_comparison_digest": str(source.get("latest_comparison_digest", "")),
        "source_observation_state_digest": str(source.get("observation_state_digest", "")),
        "source_observation_recommendation_digest": str(source.get("observation_recommendation_digest", "")),
        "longitudinal_evidence_report_digest": report_sha,
    }
    no_authority = {
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
    }
    summary = {
        "version": "indra_qi_longitudinal_shadow_evidence_summary_v0_19",
        "evidence_program_id": program_id,
        "evidence_run_id": run_id,
        "world_model_id": world_model_id,
        "source_counterfactual_decision": str(source.get("source_decision", "")),
        **source_fields,
        "longitudinal_analysis": dict(analysis),
        "stability_without_collapse": decision == "longitudinal_shadow_evidence_ready",
        "winner_selected": False,
        "single_lineage_truth_claimed": False,
        "recommendation_only": True,
        "epoch": now,
    }
    summary["longitudinal_evidence_summary_digest"] = sha(summary)

    recommendation = {
        "version": "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19",
        "evidence_program_id": program_id,
        "evidence_run_id": run_id,
        "world_model_id": world_model_id,
        "source_counterfactual_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "decision_reasons": list(evaluation.get("decision_reasons", [])),
        "longitudinal_evidence_ready": bool(evaluation.get("longitudinal_evidence_ready")),
        "winner_selected": False,
        "longitudinal_evidence_summary_digest": summary["longitudinal_evidence_summary_digest"],
        "longitudinal_analysis": dict(analysis),
        **source_fields,
        "recommendation_only": True,
        "stability_without_collapse_not_winner_selection": True,
        **no_authority,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation["longitudinal_evidence_recommendation_digest"] = sha(recommendation)

    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "longitudinal_shadow_evidence_observation",
        "evidence_program_id": program_id,
        "evidence_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "source_counterfactual_decision": str(source.get("source_decision", "")),
        "longitudinal_evidence_summary_digest": summary["longitudinal_evidence_summary_digest"],
        "longitudinal_analysis": dict(analysis),
        "decision": decision,
        "winner_selected": False,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {
            **REQUIRED_BOUNDARY,
            "source_files_unchanged": True,
            "no_winner_selected": True,
            "no_live_route_activated": True,
            "no_lineage_executed": True,
            "no_world_transition_executed": True,
            "no_external_actuation_executed": True,
        },
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)

    state = {
        "version": STATE_VERSION,
        "evidence_program_id": program_id,
        "world_model_id": world_model_id,
        "last_evidence_run_id": run_id,
        "last_source_world_state_digest": source_fields["source_world_state_digest"],
        "last_source_latest_comparison_digest": source_fields["source_latest_comparison_digest"],
        "last_source_observation_state_digest": source_fields["source_observation_state_digest"],
        "last_source_observation_recommendation_digest": source_fields["source_observation_recommendation_digest"],
        "last_longitudinal_evidence_report_digest": report_sha,
        "latest_source_counterfactual_decision": str(source.get("source_decision", "")),
        "latest_longitudinal_evidence_decision": decision,
        "latest_longitudinal_evidence_summary_digest": summary["longitudinal_evidence_summary_digest"],
        "latest_longitudinal_analysis": dict(analysis),
        "latest_longitudinal_record_digest": ledger["record_digest"],
        "prev_longitudinal_evidence_state_digest": str(prior_state.get("longitudinal_evidence_state_digest", "GENESIS")) if prior_state else "GENESIS",
        "boundary": {
            "longitudinal_evidence_state_only": True,
            "stability_without_collapse_not_winner_selection": True,
            "winner_selected": False,
            "recommendation_only": True,
            "not_lineage_selection_authority": True,
            "not_lineage_execution_authority": True,
            "not_world_update_authority": True,
            "not_external_actuation_authority": True,
            "multi_world_noncollapse_preserved": True,
        },
        "epoch": now,
    }
    state["longitudinal_evidence_state_digest"] = state_digest(state)

    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "evidence_program_id": program_id,
        "evidence_run_id": run_id,
        "world_model_id": world_model_id,
        "source_counterfactual_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "winner_selected": False,
        "recommendation_only": True,
        **source_fields,
        "longitudinal_evidence_summary_digest": summary["longitudinal_evidence_summary_digest"] if not blockers else "",
        "longitudinal_evidence_state_digest": str(state.get("longitudinal_evidence_state_digest", "")) if not blockers else str(prior_state.get("longitudinal_evidence_state_digest", "")),
        "ledger_record_digest": str(ledger.get("record_digest", "")) if not blockers else "",
        "blockers": blockers,
        "boundary": {**REQUIRED_BOUNDARY, "longitudinal_evidence_committed": not blockers},
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-longitudinal-shadow-evidence-" + sha(receipt)[:16]

    if not blockers:
        write_json(root / "indra_qi_longitudinal_shadow_evidence_summary_v0_19.json", summary)
        write_json(root / "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19.json", recommendation)
        write_json(root / "indra_qi_longitudinal_shadow_evidence_state_v0_19.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_longitudinal_shadow_evidence_receipt_v0_19.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(root / "indra_qi_longitudinal_shadow_evidence_audit_v0_19.jsonl", {**receipt, "audit_record_digest": sha(receipt)})

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
        source_fields["source_world_state_digest"],
        source_fields["source_latest_comparison_digest"],
        source_fields["source_observation_state_digest"],
        source_fields["source_observation_recommendation_digest"],
        report_sha,
        str(state.get("longitudinal_evidence_state_digest", "")) if not blockers else str(prior_state.get("longitudinal_evidence_state_digest", "")),
        str(ledger.get("record_digest", "")) if not blockers else "",
        blockers,
    )
