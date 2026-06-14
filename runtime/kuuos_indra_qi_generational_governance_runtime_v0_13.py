#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_generational_governance_core_v0_13 import DECISIONS, LEDGER_VERSION, REQUIRED_BOUNDARY, STATE_VERSION, analyze, mapping, sha, state_digest, valid_digest, validate_license, validate_plan, validate_replay, validate_source

VERSION = "indra_qi_generational_governance_v0_13"
READY = "INDRA_QI_GENERATIONAL_GOVERNANCE_V0_13_READY"
BLOCKED = "INDRA_QI_GENERATIONAL_GOVERNANCE_V0_13_BLOCKED"


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    monitor_id: str
    review_run_id: str
    runner_id: str
    generation_index: int
    decision: str
    recommendation_only: bool
    source_v0_12_runner_state_digest: str
    source_generation_handoff_digest: str
    governance_state_digest: str
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


def validate_ledger(records: list[dict[str, Any]], monitor: str, runner: str, blockers: list[str]) -> list[dict[str, Any]]:
    previous, generation = "GENESIS", -1
    reviews: set[str] = set()
    handoffs: set[str] = set()
    for index, record in enumerate(records):
        if record.get("_invalid") or record.get("version") != LEDGER_VERSION or not valid_digest(record, "record_digest"):
            blockers.append(f"generational_governance_ledger_record_{index}_invalid")
        if record.get("prev_record_digest") != previous or record.get("monitor_id") != monitor or record.get("runner_id") != runner:
            blockers.append(f"generational_governance_ledger_record_{index}_chain_invalid")
        current = record.get("generation_index")
        if isinstance(current, bool) or not isinstance(current, int) or current <= generation:
            blockers.append(f"generational_governance_ledger_record_{index}_generation_not_monotone")
        review, handoff = str(record.get("review_run_id", "")), str(record.get("source_generation_handoff_digest", ""))
        if not review or review in reviews or not handoff or handoff in handoffs:
            blockers.append(f"generational_governance_ledger_record_{index}_replay")
        reviews.add(review)
        handoffs.add(handoff)
        previous = str(record.get("record_digest", ""))
        generation = current if isinstance(current, int) else generation
    return records


def build_governance(*, runtime_context: Mapping[str, Any], governance_plan: Mapping[str, Any], governance_license: Mapping[str, Any], replay_report: Mapping[str, Any]) -> Result:
    context, plan, license_value = mapping(runtime_context), dict(mapping(governance_plan)), mapping(governance_license)
    blockers: list[str] = []
    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/"):
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_generational_governance_v0_13_enabled") is not True or context.get("apply_indra_qi_generational_governance_v0_13") is not True:
        blockers.append("generational_governance_not_enabled")
    validate_plan(plan, blockers)
    handoff = read_json(root / "indra_qi_bounded_cycle_handoff_v0_12.json")
    record = read_json(root / "indra_qi_bounded_cycle_record_v0_12.json")
    source_state = read_json(root / "indra_qi_bounded_cycle_state_v0_12.json")
    source = validate_source(handoff, record, source_state, plan, blockers)
    validate_license(license_value, plan, str(source.get("state_digest", "")), str(source.get("handoff_digest", "")), blockers)
    replay = validate_replay(mapping(replay_report), plan, str(source.get("handoff_digest", "")), blockers)
    monitor, review, runner = str(plan.get("monitor_id", "")), str(plan.get("review_run_id", "")), str(plan.get("runner_id", ""))
    ledger_path = root / "indra_qi_generational_governance_ledger_v0_13.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), monitor, runner, blockers)
    if any(v.get("review_run_id") == review or v.get("source_generation_handoff_digest") == source.get("handoff_digest") for v in prior):
        blockers.append("generational_governance_replay_detected")
    if prior:
        latest = prior[-1]
        if source.get("generation_index") != latest.get("generation_index", -2) + 1:
            blockers.append("generational_governance_generation_index_not_next")
        if source.get("prev_state_digest") != latest.get("source_v0_12_runner_state_digest"):
            blockers.append("generational_governance_v0_12_state_chain_discontinuous")
        if source.get("source_v0_11_handoff_digest") != latest.get("target_v0_11_handoff_digest"):
            blockers.append("generational_governance_v0_11_lineage_discontinuous")
    observations = [{"generation_index": v.get("generation_index", -1), "dynamic_metrics": mapping(v.get("dynamic_metrics"))} for v in prior]
    observations.append({"generation_index": source.get("generation_index", -1), "dynamic_metrics": mapping(source.get("metrics"))})
    analysis = analyze(observations, replay, mapping(plan.get("governance_policy")))
    decision = str(analysis.get("decision", "hold_for_observation"))
    if decision not in DECISIONS:
        blockers.append("generational_governance_decision_invalid")
    prior_state = read_json(root / "indra_qi_generational_governance_state_v0_13.json")
    if prior_state and not valid_digest(prior_state, "governance_state_digest"):
        blockers.append("generational_governance_prior_state_digest_invalid")
    if blockers:
        decision = "quarantine_recommended"
        analysis = {**analysis, "decision": decision, "decision_reasons": ["fail_closed_on_validation_or_integrity_loss"]}
    safe_generation = int(prior_state.get("latest_safe_generation_index", -1) or -1)
    safe_handoff = str(prior_state.get("latest_safe_generation_handoff_digest", ""))
    if not blockers and decision == "promote_bounded":
        safe_generation, safe_handoff = int(source.get("generation_index", -1)), str(source.get("handoff_digest", ""))
    now = int(time.time())
    ledger = {"version": LEDGER_VERSION, "record_type": "generational_governance_observation", "monitor_id": monitor, "review_run_id": review, "runner_id": runner, "generation_index": int(source.get("generation_index", -1)), "source_generation_run_id": str(source.get("generation_run_id", "")), "source_generation_handoff_digest": str(source.get("handoff_digest", "")), "source_generation_record_digest": str(source.get("record_digest", "")), "source_v0_12_runner_state_digest": str(source.get("state_digest", "")), "source_v0_12_prev_runner_state_digest": str(source.get("prev_state_digest", "")), "source_v0_11_handoff_digest": str(source.get("source_v0_11_handoff_digest", "")), "target_v0_11_handoff_digest": str(source.get("target_v0_11_handoff_digest", "")), "dynamic_metrics": dict(mapping(source.get("metrics"))), "replay_summary": dict(replay), "governance_analysis": dict(analysis), "decision": decision, "recommendation_only": True, "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS", "boundary": {**REQUIRED_BOUNDARY, "source_v0_12_files_unchanged": True, "no_direct_state_transition_executed": True}, "epoch": now}
    ledger["record_digest"] = sha(ledger)
    recommendation = {"version": "indra_qi_generational_governance_recommendation_v0_13", "monitor_id": monitor, "review_run_id": review, "runner_id": runner, "generation_index": int(source.get("generation_index", -1)), "decision": decision, "decision_reasons": list(analysis.get("decision_reasons", [])), "source_generation_handoff_digest": str(source.get("handoff_digest", "")), "source_v0_12_runner_state_digest": str(source.get("state_digest", "")), "rollback_target_generation_index": int(prior_state.get("latest_safe_generation_index", -1) or -1) if decision == "rollback_recommended" else -1, "rollback_target_generation_handoff_digest": str(prior_state.get("latest_safe_generation_handoff_digest", "")) if decision == "rollback_recommended" else "", "recommendation_only": True, "direct_execution_authority": False, "direct_promotion_authority": False, "direct_rollback_authority": False, "direct_quarantine_authority": False, "boundary": dict(REQUIRED_BOUNDARY), "epoch": now}
    recommendation["recommendation_digest"] = sha(recommendation)
    state = {"version": STATE_VERSION, "monitor_id": monitor, "runner_id": runner, "last_review_run_id": review, "last_generation_index": int(source.get("generation_index", -1)), "last_source_generation_handoff_digest": str(source.get("handoff_digest", "")), "last_source_v0_12_runner_state_digest": str(source.get("state_digest", "")), "latest_governance_decision": decision, "latest_governance_record_digest": ledger["record_digest"], "latest_safe_generation_index": safe_generation, "latest_safe_generation_handoff_digest": safe_handoff, "quarantine_recommended": decision == "quarantine_recommended", "prev_governance_state_digest": str(prior_state.get("governance_state_digest", "GENESIS")) if prior_state else "GENESIS", "boundary": {"generational_governance_state_only": True, "recommendation_only": True, "not_truth_authority": True, "not_execution_authority": True, "non_markov_feedback_preserved": True}, "epoch": now}
    state["governance_state_digest"] = state_digest(state)
    status = READY if not blockers else BLOCKED
    receipt = {"version": VERSION, "status": status, "monitor_id": monitor, "review_run_id": review, "runner_id": runner, "generation_index": int(source.get("generation_index", -1)), "decision": decision, "recommendation_only": True, "source_generation_handoff_digest": str(source.get("handoff_digest", "")), "source_v0_12_runner_state_digest": str(source.get("state_digest", "")), "governance_state_digest": str(state.get("governance_state_digest", "")) if not blockers else str(prior_state.get("governance_state_digest", "")), "ledger_record_digest": str(ledger.get("record_digest", "")) if not blockers else "", "blockers": blockers, "boundary": {**REQUIRED_BOUNDARY, "governance_observation_committed": not blockers}, "epoch": now}
    receipt["packet_id"] = "indra-qi-generational-governance-" + sha(receipt)[:16]
    if not blockers:
        write_json(root / "indra_qi_generational_governance_recommendation_v0_13.json", recommendation)
        write_json(root / "indra_qi_generational_governance_state_v0_13.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_generational_governance_receipt_v0_13.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(root / "indra_qi_generational_governance_audit_v0_13.jsonl", {**receipt, "audit_record_digest": sha(receipt)})
    return Result(VERSION, status, str(receipt["packet_id"]), str(root), monitor, review, runner, int(source.get("generation_index", -1)), decision, True, str(source.get("state_digest", "")), str(source.get("handoff_digest", "")), str(state.get("governance_state_digest", "")) if not blockers else str(prior_state.get("governance_state_digest", "")), str(ledger.get("record_digest", "")) if not blockers else "", blockers)
