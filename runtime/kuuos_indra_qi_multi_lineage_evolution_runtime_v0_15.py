#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_multi_lineage_evolution_core_v0_15 import (
    DECISIONS,
    LEDGER_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    analyze_candidate_set,
    evaluate_evolution,
    mapping,
    sha,
    state_digest,
    valid_digest,
    validate_license,
    validate_plan,
    validate_proposal,
    validate_sources,
)

VERSION = "indra_qi_multi_lineage_evolution_v0_15"
READY = "INDRA_QI_MULTI_LINEAGE_EVOLUTION_V0_15_READY"
BLOCKED = "INDRA_QI_MULTI_LINEAGE_EVOLUTION_V0_15_BLOCKED"


@dataclass(frozen=True)
class IndraQiMultiLineageEvolutionV0_15Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    evolution_id: str
    evolution_run_id: str
    world_model_id: str
    source_ecology_decision: str
    decision: str
    recommendation_only: bool
    source_world_state_digest: str
    source_path_ecology_state_digest: str
    source_path_ecology_recommendation_digest: str
    lineage_proposal_digest: str
    multi_lineage_state_digest: str
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
    evolution_id: str,
    world_model_id: str,
    blockers: list[str],
) -> list[dict[str, Any]]:
    previous = "GENESIS"
    runs: set[str] = set()
    source_pairs: set[tuple[str, str]] = set()
    proposal_digests: set[str] = set()
    for index, record in enumerate(records):
        if record.get("_invalid") or record.get("version") != LEDGER_VERSION:
            blockers.append(f"multi_lineage_ledger_record_{index}_invalid")
        if not valid_digest(record, "record_digest"):
            blockers.append(f"multi_lineage_ledger_record_{index}_digest_invalid")
        if record.get("prev_record_digest") != previous:
            blockers.append(f"multi_lineage_ledger_record_{index}_chain_invalid")
        if record.get("evolution_id") != evolution_id or record.get("world_model_id") != world_model_id:
            blockers.append(f"multi_lineage_ledger_record_{index}_scope_mismatch")
        run_id = str(record.get("evolution_run_id", ""))
        source_pair = (
            str(record.get("source_world_state_digest", "")),
            str(record.get("source_path_ecology_recommendation_digest", "")),
        )
        proposal_sha = str(record.get("lineage_proposal_digest", ""))
        if not run_id or run_id in runs or not all(source_pair) or source_pair in source_pairs:
            blockers.append(f"multi_lineage_ledger_record_{index}_replay")
        if not proposal_sha or proposal_sha in proposal_digests:
            blockers.append(f"multi_lineage_ledger_record_{index}_proposal_replay")
        runs.add(run_id)
        source_pairs.add(source_pair)
        proposal_digests.add(proposal_sha)
        previous = str(record.get("record_digest", ""))
    return records


def build_multi_lineage_evolution(
    *,
    runtime_context: Mapping[str, Any],
    evolution_plan: Mapping[str, Any],
    evolution_license: Mapping[str, Any],
    lineage_proposal: Mapping[str, Any],
) -> IndraQiMultiLineageEvolutionV0_15Result:
    context = mapping(runtime_context)
    plan = dict(mapping(evolution_plan))
    license_value = mapping(evolution_license)
    proposal = dict(mapping(lineage_proposal))
    blockers: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    if context.get("indra_qi_multi_lineage_evolution_v0_15_enabled") is not True:
        blockers.append("multi_lineage_enabled_not_true")
    if context.get("apply_indra_qi_multi_lineage_evolution_v0_15") is not True:
        blockers.append("multi_lineage_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    ecology_state = read_json(root / "indra_qi_world_qique_path_ecology_state_v0_14.json")
    ecology_recommendation = read_json(root / "indra_qi_world_qique_path_ecology_recommendation_v0_14.json")
    source = validate_sources(world, ecology_state, ecology_recommendation, plan, blockers)
    lineages = validate_proposal(proposal, plan, world, source, blockers)
    validate_license(
        license_value,
        plan,
        proposal,
        str(source.get("world_digest", "")),
        str(source.get("ecology_state_digest", "")),
        str(source.get("ecology_recommendation_digest", "")),
        blockers,
    )

    evolution_id = str(plan.get("evolution_id", ""))
    evolution_run_id = str(plan.get("evolution_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_multi_lineage_evolution_ledger_v0_15.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), evolution_id, world_model_id, blockers)
    source_pair = (
        str(source.get("world_digest", "")),
        str(source.get("ecology_recommendation_digest", "")),
    )
    current_proposal_digest = str(proposal.get("lineage_proposal_digest", ""))
    if any(
        record.get("evolution_run_id") == evolution_run_id
        or (
            record.get("source_world_state_digest"),
            record.get("source_path_ecology_recommendation_digest"),
        )
        == source_pair
        or record.get("lineage_proposal_digest") == current_proposal_digest
        for record in prior
    ):
        blockers.append("multi_lineage_replay_detected")

    prior_state = read_json(root / "indra_qi_multi_lineage_evolution_state_v0_15.json")
    if prior_state and not valid_digest(prior_state, "multi_lineage_state_digest"):
        blockers.append("multi_lineage_prior_state_digest_invalid")
    if prior_state:
        if prior_state.get("evolution_id") != evolution_id or prior_state.get("world_model_id") != world_model_id:
            blockers.append("multi_lineage_prior_state_scope_mismatch")
        if prior_state.get("last_source_path_ecology_state_digest") == source.get("ecology_state_digest"):
            blockers.append("multi_lineage_source_path_ecology_state_not_advanced")

    analysis = analyze_candidate_set(lineages, plan, world, source)
    evaluation = evaluate_evolution(analysis, str(source.get("source_ecology_decision", "")))
    decision = str(evaluation.get("decision", "hold_for_observation"))
    if decision not in DECISIONS:
        blockers.append("multi_lineage_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        evaluation = {
            **evaluation,
            "decision": decision,
            "decision_reasons": ["fail_closed_on_validation_or_integrity_loss"],
            "candidate_set_ready": False,
            "recommendation_only": True,
        }

    now = int(time.time())
    candidate_packet = {
        "version": "indra_qi_multi_lineage_candidate_set_v0_15",
        "evolution_id": evolution_id,
        "evolution_run_id": evolution_run_id,
        "world_model_id": world_model_id,
        "source_ecology_decision": str(source.get("source_ecology_decision", "")),
        "qique_regime": str(source.get("qique_regime", "")),
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_path_ecology_state_digest": str(source.get("ecology_state_digest", "")),
        "source_path_ecology_recommendation_digest": str(source.get("ecology_recommendation_digest", "")),
        "lineage_proposal_digest": current_proposal_digest,
        "candidate_lineages": list(analysis.get("candidate_lineages", [])),
        "candidate_set_analysis": {
            key: value for key, value in analysis.items() if key != "candidate_lineages"
        },
        "candidate_weighting_not_truth": True,
        "candidate_set_not_selection": True,
        "candidate_set_not_execution": True,
        "recommendation_only": True,
        "epoch": now,
    }
    candidate_packet["candidate_set_digest"] = sha(candidate_packet)

    recommendation_value = {
        "version": "indra_qi_multi_lineage_evolution_recommendation_v0_15",
        "evolution_id": evolution_id,
        "evolution_run_id": evolution_run_id,
        "world_model_id": world_model_id,
        "source_ecology_decision": str(source.get("source_ecology_decision", "")),
        "qique_regime": str(source.get("qique_regime", "")),
        "decision": decision,
        "decision_reasons": list(evaluation.get("decision_reasons", [])),
        "candidate_set_ready": bool(evaluation.get("candidate_set_ready")),
        "candidate_set_digest": candidate_packet["candidate_set_digest"],
        "candidate_set_analysis": {
            key: value for key, value in analysis.items() if key != "candidate_lineages"
        },
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_path_ecology_state_digest": str(source.get("ecology_state_digest", "")),
        "source_path_ecology_recommendation_digest": str(source.get("ecology_recommendation_digest", "")),
        "lineage_proposal_digest": current_proposal_digest,
        "recommendation_only": True,
        "candidate_weighting_not_truth": True,
        "direct_lineage_selection_authority": False,
        "direct_lineage_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation_value["multi_lineage_recommendation_digest"] = sha(recommendation_value)

    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "multi_lineage_candidate_set_observation",
        "evolution_id": evolution_id,
        "evolution_run_id": evolution_run_id,
        "world_model_id": world_model_id,
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_path_ecology_state_digest": str(source.get("ecology_state_digest", "")),
        "source_path_ecology_recommendation_digest": str(source.get("ecology_recommendation_digest", "")),
        "source_ecology_review_run_id": str(source.get("source_ecology_review_run_id", "")),
        "source_ecology_decision": str(source.get("source_ecology_decision", "")),
        "lineage_proposal_digest": current_proposal_digest,
        "candidate_set_digest": candidate_packet["candidate_set_digest"],
        "candidate_set_analysis": {
            key: value for key, value in analysis.items() if key != "candidate_lineages"
        },
        "decision": decision,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {
            **REQUIRED_BOUNDARY,
            "source_world_files_unchanged": True,
            "source_path_ecology_files_unchanged": True,
            "no_lineage_selected": True,
            "no_lineage_executed": True,
            "no_world_transition_executed": True,
        },
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)

    state = {
        "version": STATE_VERSION,
        "evolution_id": evolution_id,
        "world_model_id": world_model_id,
        "last_evolution_run_id": evolution_run_id,
        "last_source_world_state_digest": str(source.get("world_digest", "")),
        "last_source_path_ecology_state_digest": str(source.get("ecology_state_digest", "")),
        "last_source_path_ecology_recommendation_digest": str(source.get("ecology_recommendation_digest", "")),
        "last_lineage_proposal_digest": current_proposal_digest,
        "latest_source_ecology_decision": str(source.get("source_ecology_decision", "")),
        "latest_multi_lineage_decision": decision,
        "latest_candidate_set_digest": candidate_packet["candidate_set_digest"],
        "latest_candidate_set_analysis": {
            key: value for key, value in analysis.items() if key != "candidate_lineages"
        },
        "latest_evolution_record_digest": ledger["record_digest"],
        "prev_multi_lineage_state_digest": str(
            prior_state.get("multi_lineage_state_digest", "GENESIS")
        )
        if prior_state
        else "GENESIS",
        "boundary": {
            "multi_lineage_state_only": True,
            "recommendation_only": True,
            "candidate_weighting_not_truth": True,
            "not_lineage_selection_authority": True,
            "not_lineage_execution_authority": True,
            "not_world_update_authority": True,
            "multi_world_noncollapse_preserved": True,
            "non_markov_feedback_preserved": True,
        },
        "epoch": now,
    }
    state["multi_lineage_state_digest"] = state_digest(state)

    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "evolution_id": evolution_id,
        "evolution_run_id": evolution_run_id,
        "world_model_id": world_model_id,
        "source_ecology_decision": str(source.get("source_ecology_decision", "")),
        "decision": decision,
        "recommendation_only": True,
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_path_ecology_state_digest": str(source.get("ecology_state_digest", "")),
        "source_path_ecology_recommendation_digest": str(source.get("ecology_recommendation_digest", "")),
        "lineage_proposal_digest": current_proposal_digest,
        "candidate_set_digest": candidate_packet["candidate_set_digest"] if not blockers else "",
        "multi_lineage_state_digest": str(state.get("multi_lineage_state_digest", ""))
        if not blockers
        else str(prior_state.get("multi_lineage_state_digest", "")),
        "ledger_record_digest": str(ledger.get("record_digest", "")) if not blockers else "",
        "blockers": blockers,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "multi_lineage_observation_committed": not blockers,
        },
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-multi-lineage-evolution-" + sha(receipt)[:16]

    if not blockers:
        write_json(root / "indra_qi_multi_lineage_candidate_set_v0_15.json", candidate_packet)
        write_json(
            root / "indra_qi_multi_lineage_evolution_recommendation_v0_15.json",
            recommendation_value,
        )
        write_json(root / "indra_qi_multi_lineage_evolution_state_v0_15.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_multi_lineage_evolution_receipt_v0_15.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(
            root / "indra_qi_multi_lineage_evolution_audit_v0_15.jsonl",
            {**receipt, "audit_record_digest": sha(receipt)},
        )

    return IndraQiMultiLineageEvolutionV0_15Result(
        VERSION,
        status,
        str(receipt["packet_id"]),
        str(root),
        evolution_id,
        evolution_run_id,
        world_model_id,
        str(source.get("source_ecology_decision", "")),
        decision,
        True,
        str(source.get("world_digest", "")),
        str(source.get("ecology_state_digest", "")),
        str(source.get("ecology_recommendation_digest", "")),
        current_proposal_digest,
        str(state.get("multi_lineage_state_digest", ""))
        if not blockers
        else str(prior_state.get("multi_lineage_state_digest", "")),
        str(ledger.get("record_digest", "")) if not blockers else "",
        blockers,
    )
