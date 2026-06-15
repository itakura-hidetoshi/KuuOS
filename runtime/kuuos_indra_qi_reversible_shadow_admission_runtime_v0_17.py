#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_reversible_shadow_admission_core_v0_17 import (
    DECISIONS,
    LEDGER_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    analyze_roster,
    evaluate_admission,
    mapping,
    sha,
    state_digest,
    valid_digest,
    validate_license,
    validate_plan,
    validate_proposal,
    validate_sources,
)

VERSION = "indra_qi_reversible_shadow_admission_v0_17"
READY = "INDRA_QI_REVERSIBLE_SHADOW_ADMISSION_V0_17_READY"
BLOCKED = "INDRA_QI_REVERSIBLE_SHADOW_ADMISSION_V0_17_BLOCKED"


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    shadow_program_id: str
    admission_run_id: str
    world_model_id: str
    source_trial_decision: str
    decision: str
    recommendation_only: bool
    source_world_state_digest: str
    source_candidate_set_digest: str
    source_trial_state_digest: str
    source_trial_recommendation_digest: str
    shadow_admission_proposal_digest: str
    shadow_admission_state_digest: str
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
    source_pairs: set[tuple[str, str]] = set()
    proposals: set[str] = set()
    for index, record in enumerate(records):
        if record.get("_invalid") or record.get("version") != LEDGER_VERSION or not valid_digest(record, "record_digest"):
            blockers.append(f"shadow_admission_ledger_record_{index}_invalid")
        if record.get("prev_record_digest") != previous:
            blockers.append(f"shadow_admission_ledger_record_{index}_chain_invalid")
        if record.get("shadow_program_id") != program_id or record.get("world_model_id") != world_model_id:
            blockers.append(f"shadow_admission_ledger_record_{index}_scope_mismatch")
        run_id = str(record.get("admission_run_id", ""))
        pair = (str(record.get("source_candidate_set_digest", "")), str(record.get("source_trial_recommendation_digest", "")))
        proposal_sha = str(record.get("shadow_admission_proposal_digest", ""))
        if not run_id or run_id in runs or not all(pair) or pair in source_pairs or not proposal_sha or proposal_sha in proposals:
            blockers.append(f"shadow_admission_ledger_record_{index}_replay")
        runs.add(run_id)
        source_pairs.add(pair)
        proposals.add(proposal_sha)
        previous = str(record.get("record_digest", ""))
    return records


def build_reversible_shadow_admission(
    *,
    runtime_context: Mapping[str, Any],
    shadow_admission_plan: Mapping[str, Any],
    shadow_admission_license: Mapping[str, Any],
    shadow_admission_proposal: Mapping[str, Any],
) -> Result:
    context = mapping(runtime_context)
    plan = dict(mapping(shadow_admission_plan))
    license_value = mapping(shadow_admission_license)
    proposal = dict(mapping(shadow_admission_proposal))
    blockers: list[str] = []
    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    if context.get("indra_qi_reversible_shadow_admission_v0_17_enabled") is not True:
        blockers.append("shadow_admission_enabled_not_true")
    if context.get("apply_indra_qi_reversible_shadow_admission_v0_17") is not True:
        blockers.append("shadow_admission_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    candidate_set = read_json(root / "indra_qi_multi_lineage_candidate_set_v0_15.json")
    trial_state = read_json(root / "indra_qi_licensed_sandbox_lineage_trial_state_v0_16.json")
    trial_recommendation = read_json(root / "indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16.json")
    source = validate_sources(world, candidate_set, trial_state, trial_recommendation, plan, blockers)
    entries = validate_proposal(proposal, plan, source, blockers)
    validate_license(license_value, plan, proposal, source, blockers)

    program_id = str(plan.get("shadow_program_id", ""))
    run_id = str(plan.get("admission_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_reversible_shadow_admission_ledger_v0_17.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), program_id, world_model_id, blockers)
    current_pair = (str(source.get("candidate_set_digest", "")), str(source.get("trial_recommendation_digest", "")))
    current_proposal_sha = str(proposal.get("shadow_admission_proposal_digest", ""))
    if any(
        record.get("admission_run_id") == run_id
        or (record.get("source_candidate_set_digest"), record.get("source_trial_recommendation_digest")) == current_pair
        or record.get("shadow_admission_proposal_digest") == current_proposal_sha
        for record in prior
    ):
        blockers.append("shadow_admission_replay_detected")

    prior_state = read_json(root / "indra_qi_reversible_shadow_admission_state_v0_17.json")
    if prior_state and not valid_digest(prior_state, "shadow_admission_state_digest"):
        blockers.append("shadow_admission_prior_state_digest_invalid")
    if prior_state:
        if prior_state.get("shadow_program_id") != program_id or prior_state.get("world_model_id") != world_model_id:
            blockers.append("shadow_admission_prior_state_scope_mismatch")
        if prior_state.get("last_source_trial_state_digest") == source.get("trial_state_digest"):
            blockers.append("shadow_admission_source_trial_state_not_advanced")

    analysis = analyze_roster(entries, plan, source)
    evaluation = evaluate_admission(analysis, str(source.get("source_decision", "")))
    decision = str(evaluation.get("decision", "hold_for_observation"))
    if decision not in DECISIONS:
        blockers.append("shadow_admission_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        evaluation = {**evaluation, "decision": decision, "decision_reasons": ["fail_closed_on_validation_or_integrity_loss"], "shadow_roster_ready": False}

    now = int(time.time())
    roster = {
        "version": "indra_qi_reversible_shadow_roster_v0_17",
        "shadow_program_id": program_id,
        "admission_run_id": run_id,
        "world_model_id": world_model_id,
        "source_trial_decision": str(source.get("source_decision", "")),
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "source_trial_state_digest": str(source.get("trial_state_digest", "")),
        "source_trial_recommendation_digest": str(source.get("trial_recommendation_digest", "")),
        "shadow_admission_proposal_digest": current_proposal_sha,
        "shadow_entries": list(analysis.get("shadow_entries", [])),
        "shadow_roster_analysis": {key: value for key, value in analysis.items() if key != "shadow_entries"},
        "shadow_only": True,
        "live_route_enabled": False,
        "external_actuation_enabled": False,
        "world_update_enabled": False,
        "candidate_weighting_not_truth": True,
        "recommendation_only": True,
        "epoch": now,
    }
    roster["shadow_roster_digest"] = sha(roster)

    recommendation = {
        "version": "indra_qi_reversible_shadow_admission_recommendation_v0_17",
        "shadow_program_id": program_id,
        "admission_run_id": run_id,
        "world_model_id": world_model_id,
        "source_trial_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "decision_reasons": list(evaluation.get("decision_reasons", [])),
        "shadow_roster_ready": bool(evaluation.get("shadow_roster_ready")),
        "shadow_roster_digest": roster["shadow_roster_digest"],
        "shadow_roster_analysis": {key: value for key, value in analysis.items() if key != "shadow_entries"},
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "source_trial_state_digest": str(source.get("trial_state_digest", "")),
        "source_trial_recommendation_digest": str(source.get("trial_recommendation_digest", "")),
        "shadow_admission_proposal_digest": current_proposal_sha,
        "recommendation_only": True,
        "shadow_admission_not_live_routing": True,
        "direct_live_route_authority": False,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_external_actuation_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation["shadow_admission_recommendation_digest"] = sha(recommendation)

    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "reversible_shadow_admission_observation",
        "shadow_program_id": program_id,
        "admission_run_id": run_id,
        "world_model_id": world_model_id,
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "source_trial_state_digest": str(source.get("trial_state_digest", "")),
        "source_trial_recommendation_digest": str(source.get("trial_recommendation_digest", "")),
        "source_trial_run_id": str(source.get("source_trial_run_id", "")),
        "source_trial_decision": str(source.get("source_decision", "")),
        "shadow_admission_proposal_digest": current_proposal_sha,
        "shadow_roster_digest": roster["shadow_roster_digest"],
        "shadow_roster_analysis": {key: value for key, value in analysis.items() if key != "shadow_entries"},
        "decision": decision,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {
            **REQUIRED_BOUNDARY,
            "source_world_files_unchanged": True,
            "source_candidate_set_files_unchanged": True,
            "source_trial_files_unchanged": True,
            "no_live_route_activated": True,
            "no_lineage_selected": True,
            "no_lineage_executed": True,
            "no_world_transition_executed": True,
            "no_external_actuation_executed": True,
        },
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)

    state = {
        "version": STATE_VERSION,
        "shadow_program_id": program_id,
        "world_model_id": world_model_id,
        "last_admission_run_id": run_id,
        "last_source_world_state_digest": str(source.get("world_digest", "")),
        "last_source_candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "last_source_trial_state_digest": str(source.get("trial_state_digest", "")),
        "last_source_trial_recommendation_digest": str(source.get("trial_recommendation_digest", "")),
        "last_shadow_admission_proposal_digest": current_proposal_sha,
        "latest_source_trial_decision": str(source.get("source_decision", "")),
        "latest_shadow_admission_decision": decision,
        "latest_shadow_roster_digest": roster["shadow_roster_digest"],
        "latest_shadow_roster_analysis": {key: value for key, value in analysis.items() if key != "shadow_entries"},
        "latest_shadow_admission_record_digest": ledger["record_digest"],
        "prev_shadow_admission_state_digest": str(prior_state.get("shadow_admission_state_digest", "GENESIS")) if prior_state else "GENESIS",
        "boundary": {
            "shadow_admission_state_only": True,
            "recommendation_only": True,
            "shadow_admission_not_live_routing": True,
            "not_lineage_selection_authority": True,
            "not_lineage_execution_authority": True,
            "not_world_update_authority": True,
            "not_external_actuation_authority": True,
            "multi_world_noncollapse_preserved": True,
        },
        "epoch": now,
    }
    state["shadow_admission_state_digest"] = state_digest(state)

    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "shadow_program_id": program_id,
        "admission_run_id": run_id,
        "world_model_id": world_model_id,
        "source_trial_decision": str(source.get("source_decision", "")),
        "decision": decision,
        "recommendation_only": True,
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "source_trial_state_digest": str(source.get("trial_state_digest", "")),
        "source_trial_recommendation_digest": str(source.get("trial_recommendation_digest", "")),
        "shadow_admission_proposal_digest": current_proposal_sha,
        "shadow_roster_digest": roster["shadow_roster_digest"] if not blockers else "",
        "shadow_admission_state_digest": str(state.get("shadow_admission_state_digest", "")) if not blockers else str(prior_state.get("shadow_admission_state_digest", "")),
        "ledger_record_digest": str(ledger.get("record_digest", "")) if not blockers else "",
        "blockers": blockers,
        "boundary": {**REQUIRED_BOUNDARY, "shadow_admission_observation_committed": not blockers},
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-reversible-shadow-admission-" + sha(receipt)[:16]

    if not blockers:
        write_json(root / "indra_qi_reversible_shadow_roster_v0_17.json", roster)
        write_json(root / "indra_qi_reversible_shadow_admission_recommendation_v0_17.json", recommendation)
        write_json(root / "indra_qi_reversible_shadow_admission_state_v0_17.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_reversible_shadow_admission_receipt_v0_17.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(root / "indra_qi_reversible_shadow_admission_audit_v0_17.jsonl", {**receipt, "audit_record_digest": sha(receipt)})

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
        str(source.get("world_digest", "")),
        str(source.get("candidate_set_digest", "")),
        str(source.get("trial_state_digest", "")),
        str(source.get("trial_recommendation_digest", "")),
        current_proposal_sha,
        str(state.get("shadow_admission_state_digest", "")) if not blockers else str(prior_state.get("shadow_admission_state_digest", "")),
        str(ledger.get("record_digest", "")) if not blockers else "",
        blockers,
    )
