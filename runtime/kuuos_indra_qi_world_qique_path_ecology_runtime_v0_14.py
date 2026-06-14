#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_world_qique_path_ecology_core_v0_14 import (
    DECISIONS,
    LEDGER_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    compute_observables,
    evaluate_ecology,
    mapping,
    sha,
    state_digest,
    valid_digest,
    validate_license,
    validate_plan,
    validate_sources,
)

VERSION = "indra_qi_world_qique_path_ecology_v0_14"
READY = "INDRA_QI_WORLD_QIQUE_PATH_ECOLOGY_V0_14_READY"
BLOCKED = "INDRA_QI_WORLD_QIQUE_PATH_ECOLOGY_V0_14_BLOCKED"


@dataclass(frozen=True)
class IndraQiWorldQiQuePathEcologyV0_14Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    ecology_id: str
    review_run_id: str
    world_model_id: str
    source_governance_decision: str
    qique_regime: str
    decision: str
    recommendation_only: bool
    source_world_state_digest: str
    source_governance_state_digest: str
    source_governance_recommendation_digest: str
    path_ecology_state_digest: str
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
    records: list[dict[str, Any]], ecology_id: str, world_model_id: str, blockers: list[str]
) -> list[dict[str, Any]]:
    previous = "GENESIS"
    reviews: set[str] = set()
    source_pairs: set[tuple[str, str]] = set()
    for index, record in enumerate(records):
        if record.get("_invalid") or record.get("version") != LEDGER_VERSION:
            blockers.append(f"world_qique_ledger_record_{index}_invalid")
        if not valid_digest(record, "record_digest"):
            blockers.append(f"world_qique_ledger_record_{index}_digest_invalid")
        if record.get("prev_record_digest") != previous:
            blockers.append(f"world_qique_ledger_record_{index}_chain_invalid")
        if record.get("ecology_id") != ecology_id or record.get("world_model_id") != world_model_id:
            blockers.append(f"world_qique_ledger_record_{index}_scope_mismatch")
        review = str(record.get("review_run_id", ""))
        pair = (
            str(record.get("source_world_state_digest", "")),
            str(record.get("source_governance_recommendation_digest", "")),
        )
        if not review or review in reviews or not all(pair) or pair in source_pairs:
            blockers.append(f"world_qique_ledger_record_{index}_replay")
        reviews.add(review)
        source_pairs.add(pair)
        previous = str(record.get("record_digest", ""))
    return records


def build_path_ecology(
    *,
    runtime_context: Mapping[str, Any],
    path_ecology_plan: Mapping[str, Any],
    path_ecology_license: Mapping[str, Any],
) -> IndraQiWorldQiQuePathEcologyV0_14Result:
    context = mapping(runtime_context)
    plan = dict(mapping(path_ecology_plan))
    license_value = mapping(path_ecology_license)
    blockers: list[str] = []
    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    if context.get("indra_qi_world_qique_path_ecology_v0_14_enabled") is not True:
        blockers.append("world_qique_enabled_not_true")
    if context.get("apply_indra_qi_world_qique_path_ecology_v0_14") is not True:
        blockers.append("world_qique_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    governance_state = read_json(root / "indra_qi_generational_governance_state_v0_13.json")
    recommendation = read_json(root / "indra_qi_generational_governance_recommendation_v0_13.json")
    source = validate_sources(world, governance_state, recommendation, plan, blockers)
    validate_license(
        license_value,
        plan,
        str(source.get("world_digest", "")),
        str(source.get("governance_state_digest", "")),
        str(source.get("recommendation_digest", "")),
        blockers,
    )

    ecology_id = str(plan.get("ecology_id", ""))
    review_run_id = str(plan.get("review_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_world_qique_path_ecology_ledger_v0_14.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), ecology_id, world_model_id, blockers)
    source_pair = (
        str(source.get("world_digest", "")),
        str(source.get("recommendation_digest", "")),
    )
    if any(
        record.get("review_run_id") == review_run_id
        or (
            record.get("source_world_state_digest"),
            record.get("source_governance_recommendation_digest"),
        )
        == source_pair
        for record in prior
    ):
        blockers.append("world_qique_replay_detected")

    prior_state = read_json(root / "indra_qi_world_qique_path_ecology_state_v0_14.json")
    if prior_state and not valid_digest(prior_state, "path_ecology_state_digest"):
        blockers.append("world_qique_prior_state_digest_invalid")
    if prior_state:
        if prior_state.get("ecology_id") != ecology_id or prior_state.get("world_model_id") != world_model_id:
            blockers.append("world_qique_prior_state_scope_mismatch")
        if prior_state.get("last_source_governance_state_digest") == source.get("governance_state_digest"):
            blockers.append("world_qique_source_governance_state_not_advanced")

    policy = mapping(plan.get("ecology_policy"))
    observables = compute_observables(world, policy)
    evaluation = evaluate_ecology(
        observables, policy, str(source.get("source_governance_decision", ""))
    )
    decision = str(evaluation.get("decision", "hold_for_observation"))
    qique_regime = str(evaluation.get("qique_regime", "WORLD_QIQUE_OBSERVATION_HOLD"))
    if decision not in DECISIONS:
        blockers.append("world_qique_decision_invalid")
    if blockers:
        decision = "quarantine_recommended"
        qique_regime = "WORLD_QIQUE_INTEGRITY_QUARANTINE"
        evaluation = {
            **evaluation,
            "decision": decision,
            "qique_regime": qique_regime,
            "decision_reasons": ["fail_closed_on_validation_or_integrity_loss"],
            "promotion_ecology_compatible": False,
        }

    now = int(time.time())
    ledger = {
        "version": LEDGER_VERSION,
        "record_type": "world_qique_path_ecology_observation",
        "ecology_id": ecology_id,
        "review_run_id": review_run_id,
        "world_model_id": world_model_id,
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_governance_state_digest": str(source.get("governance_state_digest", "")),
        "source_governance_recommendation_digest": str(source.get("recommendation_digest", "")),
        "source_governance_review_run_id": str(source.get("source_governance_review_run_id", "")),
        "source_governance_decision": str(source.get("source_governance_decision", "")),
        "qique_observables": dict(observables),
        "ecology_evaluation": dict(evaluation),
        "decision": decision,
        "recommendation_only": True,
        "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS",
        "boundary": {
            **REQUIRED_BOUNDARY,
            "source_world_files_unchanged": True,
            "source_governance_files_unchanged": True,
            "no_direct_world_transition_executed": True,
        },
        "epoch": now,
    }
    ledger["record_digest"] = sha(ledger)

    recommendation_value = {
        "version": "indra_qi_world_qique_path_ecology_recommendation_v0_14",
        "ecology_id": ecology_id,
        "review_run_id": review_run_id,
        "world_model_id": world_model_id,
        "source_governance_decision": str(source.get("source_governance_decision", "")),
        "qique_regime": qique_regime,
        "decision": decision,
        "decision_reasons": list(evaluation.get("decision_reasons", [])),
        "promotion_ecology_compatible": bool(evaluation.get("promotion_ecology_compatible")),
        "qique_observables": dict(observables),
        "gates": dict(mapping(evaluation.get("gates"))),
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_governance_state_digest": str(source.get("governance_state_digest", "")),
        "source_governance_recommendation_digest": str(source.get("recommendation_digest", "")),
        "recommendation_only": True,
        "direct_execution_authority": False,
        "direct_world_update_authority": False,
        "direct_promotion_authority": False,
        "direct_rollback_authority": False,
        "direct_quarantine_authority": False,
        "truth_authority": False,
        "boundary": dict(REQUIRED_BOUNDARY),
        "epoch": now,
    }
    recommendation_value["path_ecology_recommendation_digest"] = sha(recommendation_value)

    state = {
        "version": STATE_VERSION,
        "ecology_id": ecology_id,
        "world_model_id": world_model_id,
        "last_review_run_id": review_run_id,
        "last_source_world_state_digest": str(source.get("world_digest", "")),
        "last_source_governance_state_digest": str(source.get("governance_state_digest", "")),
        "last_source_governance_recommendation_digest": str(source.get("recommendation_digest", "")),
        "latest_source_governance_decision": str(source.get("source_governance_decision", "")),
        "latest_qique_regime": qique_regime,
        "latest_path_ecology_decision": decision,
        "latest_qique_observables": dict(observables),
        "latest_ecology_record_digest": ledger["record_digest"],
        "prev_path_ecology_state_digest": str(
            prior_state.get("path_ecology_state_digest", "GENESIS")
        )
        if prior_state
        else "GENESIS",
        "boundary": {
            "world_qique_path_ecology_state_only": True,
            "recommendation_only": True,
            "not_truth_authority": True,
            "not_world_update_authority": True,
            "multi_world_noncollapse_preserved": True,
            "non_markov_feedback_preserved": True,
        },
        "epoch": now,
    }
    state["path_ecology_state_digest"] = state_digest(state)

    status = READY if not blockers else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "ecology_id": ecology_id,
        "review_run_id": review_run_id,
        "world_model_id": world_model_id,
        "source_governance_decision": str(source.get("source_governance_decision", "")),
        "qique_regime": qique_regime,
        "decision": decision,
        "recommendation_only": True,
        "source_world_state_digest": str(source.get("world_digest", "")),
        "source_governance_state_digest": str(source.get("governance_state_digest", "")),
        "source_governance_recommendation_digest": str(source.get("recommendation_digest", "")),
        "path_ecology_state_digest": str(state.get("path_ecology_state_digest", ""))
        if not blockers
        else str(prior_state.get("path_ecology_state_digest", "")),
        "ledger_record_digest": str(ledger.get("record_digest", "")) if not blockers else "",
        "blockers": blockers,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "path_ecology_observation_committed": not blockers,
        },
        "epoch": now,
    }
    receipt["packet_id"] = "indra-qi-world-qique-path-ecology-" + sha(receipt)[:16]

    if not blockers:
        write_json(
            root / "indra_qi_world_qique_path_ecology_recommendation_v0_14.json",
            recommendation_value,
        )
        write_json(root / "indra_qi_world_qique_path_ecology_state_v0_14.json", state)
        append_jsonl(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_world_qique_path_ecology_receipt_v0_14.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(
            root / "indra_qi_world_qique_path_ecology_audit_v0_14.jsonl",
            {**receipt, "audit_record_digest": sha(receipt)},
        )

    return IndraQiWorldQiQuePathEcologyV0_14Result(
        VERSION,
        status,
        str(receipt["packet_id"]),
        str(root),
        ecology_id,
        review_run_id,
        world_model_id,
        str(source.get("source_governance_decision", "")),
        qique_regime,
        decision,
        True,
        str(source.get("world_digest", "")),
        str(source.get("governance_state_digest", "")),
        str(source.get("recommendation_digest", "")),
        str(state.get("path_ecology_state_digest", ""))
        if not blockers
        else str(prior_state.get("path_ecology_state_digest", "")),
        str(ledger.get("record_digest", "")) if not blockers else "",
        blockers,
    )
