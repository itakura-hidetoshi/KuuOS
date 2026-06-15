#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_bounded_plural_shadow_routing_core_v0_20 import (
    DECISIONS,
    LEDGER_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    analyze_proposal,
    evaluate_proposal,
    mapping,
    sha,
    state_digest,
    valid_digest,
    validate_license,
    validate_plan,
    validate_report,
    validate_sources,
)

VERSION = "indra_qi_bounded_plural_shadow_routing_v0_20"
READY = "INDRA_QI_BOUNDED_PLURAL_SHADOW_ROUTING_V0_20_READY"
BLOCKED = "INDRA_QI_BOUNDED_PLURAL_SHADOW_ROUTING_V0_20_BLOCKED"


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    routing_program_id: str
    proposal_run_id: str
    world_model_id: str
    source_longitudinal_decision: str
    decision: str
    recommendation_only: bool
    routing_activated: bool
    source_world_state_digest: str
    source_longitudinal_summary_digest: str
    source_longitudinal_state_digest: str
    source_longitudinal_recommendation_digest: str
    plural_routing_report_digest: str
    plural_routing_state_digest: str
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
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


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
        run_id = str(record.get("proposal_run_id", ""))
        pair = (
            str(record.get("source_longitudinal_summary_digest", "")),
            str(record.get("source_longitudinal_recommendation_digest", "")),
        )
        report_sha = str(record.get("plural_routing_report_digest", ""))
        valid = (
            record.get("version") == LEDGER_VERSION
            and valid_digest(record, "record_digest")
            and record.get("prev_record_digest") == previous
            and record.get("routing_program_id") == program_id
            and record.get("world_model_id") == world_model_id
            and bool(run_id)
            and run_id not in runs
            and all(pair)
            and pair not in pairs
            and bool(report_sha)
            and report_sha not in reports
        )
        if record.get("_invalid") or not valid:
            blockers.append(f"plural_routing_ledger_record_{index}_invalid")
        runs.add(run_id)
        pairs.add(pair)
        reports.add(report_sha)
        previous = str(record.get("record_digest", ""))
    return records


def build_bounded_plural_shadow_routing(
    *,
    runtime_context: Mapping[str, Any],
    plural_routing_plan: Mapping[str, Any],
    plural_routing_license: Mapping[str, Any],
    plural_routing_report: Mapping[str, Any],
) -> Result:
    context = mapping(runtime_context)
    plan = dict(mapping(plural_routing_plan))
    license_value = mapping(plural_routing_license)
    report = dict(mapping(plural_routing_report))
    blockers: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_bounded_plural_shadow_routing_v0_20_enabled") is not True:
        blockers.append("plural_routing_enabled_not_true")
    if context.get("apply_indra_qi_bounded_plural_shadow_routing_v0_20") is not True:
        blockers.append("plural_routing_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    summary = read_json(root / "indra_qi_longitudinal_shadow_evidence_summary_v0_19.json")
    source_state = read_json(root / "indra_qi_longitudinal_shadow_evidence_state_v0_19.json")
    source_recommendation = read_json(root / "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19.json")
    source = validate_sources(world, summary, source_state, source_recommendation, plan, blockers)
    entries = validate_report(report, plan, source, blockers)
    validate_license(license_value, plan, report, source, blockers)

    program_id = str(plan.get("routing_program_id", ""))
    run_id = str(plan.get("proposal_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_bounded_plural_shadow_routing_ledger_v0_20.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), program_id, world_model_id, blockers)
    pair = (
        str(source.get("summary_digest", "")),
        str(source.get("recommendation_digest", "")),
    )
    report_sha = str(report.get("plural_routing_report_digest", ""))
    if any(
        record.get("proposal_run_id") == run_id
        or (
            record.get("source_longitudinal_summary_digest"),
            record.get("source_longitudinal_recommendation_digest"),
        )
        == pair
        or record.get("plural_routing_report_digest") == report_sha
        for record in prior
    ):
        blockers.append("plural_routing_replay_detected")

    prior_state = read_json(root / "indra_qi_bounded_plural_shadow_routing_state_v0_20.json")
    if prior_state and not valid_digest(prior_state, "plural_routing_state_digest"):
        blockers.append("plural_routing_prior_state_digest_invalid")
    if prior_state:
        if prior_state.get("routing_program_id") != program_id or prior_state.get("world_model_id") != world_model_id:
            blockers.append("plural_routing_prior_state_scope_mismatch")
        if prior_state.get("last_source_longitudinal_state_digest") == source.get("state_digest"):
            blockers.append("plural_routing_source_longitudinal_state_not_advanced")

    analysis = analyze_proposal(entries, report, plan, source)
    evaluation = evaluate_proposal(analysis, str(source.get("source_decision", "")))
    decision = str(evaluation.get("decision", "hold_for_observation"))
    if decision not in DECISIONS:
        blockers.append("plural_routing_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        evaluation = {
            "decision_reasons": ["fail_closed_on_validation_or_integrity_loss"],
            "proposal_ready": False,
            "routing_activated": False,
            "winner_selected": False,
        }

    now = int(time.time())
    source_fields = {
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_longitudinal_summary_digest": str(source.get("summary_digest", "")),
        "source_longitudinal_state_digest": str(source.get("state_digest", "")),
        "source_longitudinal_recommendation_digest": str(source.get("recommendation_digest", "")),
        "plural_routing_report_digest": report_sha,
    }
    no_authority = {
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
    }

    proposal = {
        "version": "indra_qi_bounded_plural_shadow_routing_proposal_v0_20",
        "routing_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        **source_fields,
        "total_observation_traffic_fraction": analysis.get("total_observation_traffic_fraction", 0.0),
        "route_entries": list(analysis.get("route_entries", [])),
        "proposal_analysis": {key: value for key, value in analysis.items() if key != "route_entries"},
        "proposal_only": True,
        "routing_activated": False,
        "live_route_enabled": False,
        "winner_selected": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "recommendation_only": True,
        "epoch": now,
    }
    proposal["plural_shadow_routing_proposal_digest"] = sha(proposal)

    recommendation = {
        "version": "indra_qi_bounded_plural_shadow_routing_recommendation_v0_20",
        "routing_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "decision_reasons": list(evaluation.get("decision_reasons", [])),
        "proposal_ready": bool(evaluation.get("proposal_ready")),
        "routing_activated": False,
        "winner_selected": False,
        "plural_shadow_routing_proposal_digest": proposal["plural_shadow_routing_proposal_digest"],
        "proposal_analysis": {key: value for key, value in analysis.items() if key != "route_entries"},
        **source_fields,
        "recommendation_only": True,
        "proposal_not_routing_activation": True,
        **no_authority,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation["plural_routing_recommendation_digest"] = sha(recommendation)

    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "bounded_plural_shadow_routing_proposal",
        "routing_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        **source_fields,
        "source_evidence_run_id": str(source.get("source_evidence_run_id", "")),
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        "plural_shadow_routing_proposal_digest": proposal["plural_shadow_routing_proposal_digest"],
        "proposal_analysis": {key: value for key, value in analysis.items() if key != "route_entries"},
        "decision": decision,
        "routing_activated": False,
        "winner_selected": False,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {
            **REQUIRED_BOUNDARY,
            "source_files_unchanged": True,
            "no_routing_activated": True,
            "no_winner_selected": True,
            "no_lineage_executed": True,
            "no_world_transition_executed": True,
            "no_external_actuation_executed": True,
        },
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)

    state = {
        "version": STATE_VERSION,
        "routing_program_id": program_id,
        "world_model_id": world_model_id,
        "last_proposal_run_id": run_id,
        "last_source_world_state_digest": source_fields["source_world_state_digest"],
        "last_source_longitudinal_summary_digest": source_fields["source_longitudinal_summary_digest"],
        "last_source_longitudinal_state_digest": source_fields["source_longitudinal_state_digest"],
        "last_source_longitudinal_recommendation_digest": source_fields[
            "source_longitudinal_recommendation_digest"
        ],
        "last_plural_routing_report_digest": report_sha,
        "latest_source_longitudinal_decision": str(source.get("source_decision", "")),
        "latest_plural_routing_decision": decision,
        "latest_plural_shadow_routing_proposal_digest": proposal["plural_shadow_routing_proposal_digest"],
        "latest_proposal_analysis": {key: value for key, value in analysis.items() if key != "route_entries"},
        "latest_plural_routing_record_digest": ledger["record_digest"],
        "prev_plural_routing_state_digest": str(prior_state.get("plural_routing_state_digest", "GENESIS"))
        if prior_state
        else "GENESIS",
        "boundary": {
            "plural_routing_state_only": True,
            "proposal_not_routing_activation": True,
            "routing_activated": False,
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
    state["plural_routing_state_digest"] = state_digest(state)

    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "routing_program_id": program_id,
        "proposal_run_id": run_id,
        "world_model_id": world_model_id,
        "source_longitudinal_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "routing_activated": False,
        "winner_selected": False,
        "recommendation_only": True,
        **source_fields,
        "plural_shadow_routing_proposal_digest": proposal["plural_shadow_routing_proposal_digest"]
        if not blockers
        else "",
        "plural_routing_state_digest": str(state.get("plural_routing_state_digest", ""))
        if not blockers
        else str(prior_state.get("plural_routing_state_digest", "")),
        "ledger_record_digest": str(ledger.get("record_digest", "")) if not blockers else "",
        "blockers": blockers,
        "boundary": {**REQUIRED_BOUNDARY, "plural_routing_proposal_committed": not blockers},
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-bounded-plural-shadow-routing-" + sha(receipt)[:16]

    if not blockers:
        write_json(root / "indra_qi_bounded_plural_shadow_routing_proposal_v0_20.json", proposal)
        write_json(root / "indra_qi_bounded_plural_shadow_routing_recommendation_v0_20.json", recommendation)
        write_json(root / "indra_qi_bounded_plural_shadow_routing_state_v0_20.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_bounded_plural_shadow_routing_receipt_v0_20.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(
            root / "indra_qi_bounded_plural_shadow_routing_audit_v0_20.jsonl",
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
        source_fields["source_longitudinal_summary_digest"],
        source_fields["source_longitudinal_state_digest"],
        source_fields["source_longitudinal_recommendation_digest"],
        report_sha,
        str(state.get("plural_routing_state_digest", ""))
        if not blockers
        else str(prior_state.get("plural_routing_state_digest", "")),
        str(ledger.get("record_digest", "")) if not blockers else "",
        blockers,
    )
