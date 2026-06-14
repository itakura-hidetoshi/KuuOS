#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import (
    REQUIRED_BOUNDARY,
    build_seed_entry,
    cycle_state_digest,
    evolve_channel,
    items,
    mapping,
    previous_channel_map,
    seed_admissible,
    sha,
    valid_digest,
    validate_overlay_chain,
    validate_plan,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    REQUIRED_PROCESS_CONTEXT,
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_process_tensor_cycle_v0_5"
READY = "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_READY"
BLOCKED = "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_BLOCKED"
LICENSE_READY = "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiProcessTensorCycleV0_5Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    cycle_id: str
    cycle_index: int
    source_activation_id: str
    cycle_status: str
    channel_count: int
    seed_entry_count: int
    source_world_state_unchanged: bool
    source_world_state_digest: str
    previous_cycle_state_digest: str
    process_tensor_cycle_state_digest: str
    next_cycle_seed_packet_digest: str
    state_path: str
    seed_packet_path: str
    cycle_ledger_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    result: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            result.append(value)
    return result


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _average(channels: list[Mapping[str, Any]], field: str) -> float:
    if not channels:
        return 0.0
    values: list[float] = []
    for channel in channels:
        raw = channel.get(field, 0.0)
        values.append(float(raw) if isinstance(raw, (int, float)) and not isinstance(raw, bool) else 0.0)
    return round(sum(values) / len(values), 8)


def _validate_sources(
    *,
    world_state: Mapping[str, Any],
    activation: Mapping[str, Any],
    review: Mapping[str, Any],
    feedback: Mapping[str, Any],
    mutation_records: list[dict[str, Any]],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> tuple[list[Mapping[str, Any]], dict[str, Mapping[str, Any]], Mapping[str, Any]]:
    if not world_state:
        blockers.append("source_indra_qi_world_state_missing_or_invalid")
    if not activation:
        blockers.append("source_v0_4_activation_record_missing_or_invalid")
    if not review:
        blockers.append("source_v0_4_process_tensor_review_missing_or_invalid")
    if not feedback:
        blockers.append("source_v0_3_feedback_packet_missing_or_invalid")

    if activation:
        if activation.get("version") != "indra_qi_process_tensor_activation_record_v0_4":
            blockers.append("source_v0_4_activation_record_version_invalid")
        if activation.get("activation_status") != "process_tensor_activation_completed":
            blockers.append("source_v0_4_activation_not_completed")
        if not valid_digest(activation, "activation_record_digest"):
            blockers.append("source_v0_4_activation_record_digest_invalid")
        if activation.get("protected_structure_preserved") is not True:
            blockers.append("source_v0_4_protected_structure_not_preserved")
        boundary = mapping(activation.get("boundary"))
        for field in (
            "runtime_observation_overlay_only",
            "operator_algebra_unchanged",
            "gauge_connection_unchanged",
            "holonomy_preserved",
            "non_markov_feedback_preserved",
            "candidate_weighting_not_truth",
            "not_direct_execution_authority",
            "external_world_actuation_authority",
        ):
            expected = False if field == "external_world_actuation_authority" else True
            if boundary.get(field) is not expected:
                blockers.append(f"source_v0_4_activation_boundary_{field}_mismatch")

    if review:
        if review.get("version") != "indra_qi_process_tensor_review_v0_4":
            blockers.append("source_v0_4_process_tensor_review_version_invalid")
        if review.get("review_status") != "admissible":
            blockers.append("source_v0_4_process_tensor_review_not_admissible")
        if not valid_digest(review, "process_tensor_review_digest"):
            blockers.append("source_v0_4_process_tensor_review_digest_invalid")
        if str(activation.get("process_tensor_review_digest", "")) != str(
            review.get("process_tensor_review_digest", "")
        ):
            blockers.append("source_v0_4_activation_review_digest_mismatch")

    if feedback:
        if feedback.get("version") != "indra_qi_causal_feedback_bridge_v0_3":
            blockers.append("source_v0_3_feedback_packet_version_invalid")
        if feedback.get("feedback_status") != "feedback_candidates_ready":
            blockers.append("source_v0_3_feedback_packet_not_ready")
        if not valid_digest(feedback, "feedback_packet_digest"):
            blockers.append("source_v0_3_feedback_packet_digest_invalid")
        if str(activation.get("source_feedback_packet_digest", "")) != str(
            feedback.get("feedback_packet_digest", "")
        ):
            blockers.append("source_v0_4_activation_feedback_digest_mismatch")
        context = mapping(feedback.get("source_process_tensor_context"))
        for field in REQUIRED_PROCESS_CONTEXT:
            if not str(context.get(field, "")).strip():
                blockers.append(f"source_v0_3_feedback_process_context_{field}_missing")

    world_digest = str(world_state.get("indra_qi_world_state_digest", ""))
    if world_state and compute_indra_qi_world_state_digest(world_state) != world_digest:
        blockers.append("source_indra_qi_world_state_digest_invalid")
    if str(activation.get("after_world_state_digest", "")) != world_digest:
        blockers.append("source_v0_4_activation_world_state_digest_mismatch")
    if str(plan.get("source_world_state_digest", "")) != world_digest:
        blockers.append("process_tensor_cycle_plan_world_state_digest_mismatch")
    if str(plan.get("source_activation_id", "")) != str(activation.get("activation_id", "")):
        blockers.append("process_tensor_cycle_plan_activation_id_mismatch")
    if str(plan.get("source_activation_record_digest", "")) != str(
        activation.get("activation_record_digest", "")
    ):
        blockers.append("process_tensor_cycle_plan_activation_digest_mismatch")
    if str(plan.get("source_process_tensor_review_digest", "")) != str(
        review.get("process_tensor_review_digest", "")
    ):
        blockers.append("process_tensor_cycle_plan_review_digest_mismatch")

    matching_record: Mapping[str, Any] = {}
    activation_id = str(activation.get("activation_id", ""))
    for record in reversed(mutation_records):
        if str(record.get("activation_id", "")) == activation_id:
            matching_record = record
            break
    if not matching_record:
        blockers.append("source_v0_4_mutation_ledger_record_missing")
    else:
        if not valid_digest(matching_record, "record_digest"):
            blockers.append("source_v0_4_mutation_ledger_record_digest_invalid")
        if str(matching_record.get("source_activation_record_digest", "")) != str(
            activation.get("activation_record_digest", "")
        ):
            blockers.append("source_v0_4_mutation_ledger_activation_digest_mismatch")
        if str(matching_record.get("after_world_state_digest", "")) != world_digest:
            blockers.append("source_v0_4_mutation_ledger_world_digest_mismatch")

    all_overlays = [mapping(value) for value in items(world_state.get("runtime_observation_overlays"))]
    validate_overlay_chain(all_overlays, blockers)
    selected = [
        overlay
        for overlay in all_overlays
        if str(overlay.get("activation_id", "")) == activation_id
    ]
    approved_ids = [str(value) for value in items(activation.get("approved_candidate_ids"))]
    selected_ids = [str(overlay.get("source_candidate_id", "")) for overlay in selected]
    if selected_ids != approved_ids:
        blockers.append("source_v0_4_activation_overlay_candidate_order_mismatch")
    if len(selected) != int(activation.get("overlays_applied", -1) or -1):
        blockers.append("source_v0_4_activation_overlay_count_mismatch")

    assessment_map: dict[str, Mapping[str, Any]] = {}
    for raw in items(review.get("assessments")):
        assessment = mapping(raw)
        candidate_id = str(assessment.get("candidate_id", ""))
        if not valid_digest(assessment, "assessment_digest"):
            blockers.append(f"source_v0_4_assessment_{candidate_id}_digest_invalid")
        if candidate_id:
            assessment_map[candidate_id] = assessment
    if set(approved_ids) - set(assessment_map):
        blockers.append("source_v0_4_approved_candidate_assessment_missing")
    for overlay in selected:
        candidate_id = str(overlay.get("source_candidate_id", ""))
        assessment = assessment_map.get(candidate_id, {})
        if str(overlay.get("process_tensor_assessment_digest", "")) != str(
            assessment.get("assessment_digest", "")
        ):
            blockers.append(f"source_v0_4_overlay_{candidate_id}_assessment_digest_mismatch")
        if assessment.get("admitted") is not True:
            blockers.append(f"source_v0_4_assessment_{candidate_id}_not_admitted")

    return selected, assessment_map, matching_record


def build_indra_qi_process_tensor_cycle_v0_5(
    *,
    runtime_context: Mapping[str, Any],
    cycle_plan: Mapping[str, Any],
    cycle_license: Mapping[str, Any],
) -> IndraQiProcessTensorCycleV0_5Result:
    context = mapping(runtime_context)
    plan = dict(mapping(cycle_plan))
    license_value = mapping(cycle_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    world_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    activation_path = root / "indra_qi_process_tensor_activation_record_v0_4.json"
    review_path = root / "indra_qi_process_tensor_review_v0_4.json"
    feedback_path = root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    mutation_ledger_path = root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl"
    state_path = root / "indra_qi_process_tensor_cycle_state_v0_5.json"
    seed_path = root / "indra_qi_next_cycle_projection_seed_v0_5.json"
    cycle_ledger_path = root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl"
    receipt_path = root / "indra_qi_process_tensor_cycle_receipt_v0_5.json"
    audit_path = root / "indra_qi_process_tensor_cycle_audit_v0_5.jsonl"

    if context.get("indra_qi_process_tensor_cycle_v0_5_enabled") is not True:
        blockers.append("indra_qi_process_tensor_cycle_v0_5_enabled_not_true")
    if context.get("evolve_indra_qi_process_tensor_cycle_v0_5") is not True:
        blockers.append("evolve_indra_qi_process_tensor_cycle_v0_5_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("indra_qi_process_tensor_cycle_license_not_ready")
    for flag in (
        "world_state_read_allowed",
        "activation_record_read_allowed",
        "process_tensor_review_read_allowed",
        "feedback_packet_read_allowed",
        "mutation_ledger_read_allowed",
        "previous_cycle_state_read_allowed",
        "cycle_plan_validate_allowed",
        "cycle_state_write_allowed",
        "next_cycle_seed_write_allowed",
        "cycle_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    plan_digest = str(plan.get("cycle_plan_digest", ""))
    if str(license_value.get("bound_cycle_plan_digest", "")) != plan_digest:
        blockers.append("process_tensor_cycle_license_plan_digest_mismatch")
    cycle_id = str(plan.get("cycle_id", ""))

    world_state = _read_json(world_path)
    activation = _read_json(activation_path)
    review = _read_json(review_path)
    feedback = _read_json(feedback_path)
    mutation_records = _records(mutation_ledger_path)
    selected_overlays, assessment_map, _ = _validate_sources(
        world_state=world_state,
        activation=activation,
        review=review,
        feedback=feedback,
        mutation_records=mutation_records,
        plan=plan,
        blockers=blockers,
    )

    cycle_records = _records(cycle_ledger_path)
    source_activation_id = str(activation.get("activation_id", ""))
    if cycle_id and any(str(record.get("cycle_id", "")) == cycle_id for record in cycle_records):
        blockers.append("process_tensor_cycle_id_replay")
    if source_activation_id and any(
        str(record.get("source_activation_id", "")) == source_activation_id
        for record in cycle_records
    ):
        blockers.append("source_activation_cycle_replay")

    previous_state = _read_json(state_path)
    previous_digest = "GENESIS"
    cycle_index = 1
    previous_channels: dict[str, Mapping[str, Any]] = {}
    expected_previous = str(plan.get("expected_previous_cycle_state_digest", ""))
    if previous_state:
        if previous_state.get("version") != VERSION:
            blockers.append("previous_process_tensor_cycle_state_version_invalid")
        if previous_state.get("cycle_status") != "process_tensor_cycle_evolved":
            blockers.append("previous_process_tensor_cycle_state_not_evolved")
        if cycle_state_digest(previous_state) != str(
            previous_state.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("previous_process_tensor_cycle_state_digest_invalid")
        previous_digest = str(previous_state.get("process_tensor_cycle_state_digest", ""))
        previous_index_raw = previous_state.get("cycle_index", 0)
        if isinstance(previous_index_raw, bool) or not isinstance(previous_index_raw, int) or previous_index_raw < 1:
            blockers.append("previous_process_tensor_cycle_index_invalid")
        else:
            cycle_index = previous_index_raw + 1
        previous_channels = previous_channel_map(previous_state)
        if not cycle_records:
            blockers.append("previous_process_tensor_cycle_ledger_missing")
        elif str(cycle_records[-1].get("process_tensor_cycle_state_digest", "")) != previous_digest:
            blockers.append("previous_process_tensor_cycle_ledger_state_digest_mismatch")
    if expected_previous != previous_digest:
        blockers.append("process_tensor_cycle_expected_previous_state_digest_mismatch")

    policy = mapping(plan.get("evolution_policy"))
    maximum = policy.get("max_channels", 0)
    if isinstance(maximum, int) and not isinstance(maximum, bool) and len(selected_overlays) > maximum:
        blockers.append("process_tensor_cycle_channel_limit_exceeded")

    event_kind = str(feedback.get("source_causal_event_kind", ""))
    if event_kind not in {"observe", "intervene", "counterfactual", "undo"}:
        blockers.append("source_feedback_event_kind_invalid")
    process_context = dict(mapping(feedback.get("source_process_tensor_context")))
    process_context.update(
        {
            "source_feedback_packet_digest": str(feedback.get("feedback_packet_digest", "")),
            "source_activation_record_digest": str(activation.get("activation_record_digest", "")),
            "source_process_tensor_review_digest": str(review.get("process_tensor_review_digest", "")),
            "previous_cycle_state_digest": previous_digest,
        }
    )

    channels: list[dict[str, Any]] = []
    for overlay in selected_overlays:
        candidate_id = str(overlay.get("source_candidate_id", ""))
        target = mapping(overlay.get("target"))
        key = (
            f"flow:{target.get('flow_id')}:{target.get('observable_id', '')}"
            if str(target.get("flow_id", ""))
            else f"patch:{target.get('patch_id', '')}:{target.get('observable_id', '')}"
        )
        channels.append(
            evolve_channel(
                overlay=overlay,
                assessment=assessment_map.get(candidate_id, {}),
                previous=previous_channels.get(key, {}),
                event_kind=event_kind,
                policy=policy,
                cycle_index=cycle_index,
            )
        )

    seed_entries = [
        build_seed_entry(channel, process_context)
        for channel in channels
        if seed_admissible(channel, policy)
    ]
    if channels and not seed_entries:
        blockers.append("process_tensor_cycle_no_admissible_next_cycle_seeds")

    world_digest_before = str(world_state.get("indra_qi_world_state_digest", ""))
    state_record: dict[str, Any] = {}
    seed_packet: dict[str, Any] = {}
    state_digest = ""
    seed_digest = ""
    if not blockers:
        state_record = {
            "version": VERSION,
            "cycle_status": "process_tensor_cycle_evolved",
            "cycle_id": cycle_id,
            "cycle_index": cycle_index,
            "source_world_model_id": str(world_state.get("world_model_id", "")),
            "source_world_state_digest": world_digest_before,
            "source_activation_id": source_activation_id,
            "source_activation_record_digest": str(activation.get("activation_record_digest", "")),
            "source_process_tensor_review_digest": str(review.get("process_tensor_review_digest", "")),
            "source_feedback_packet_digest": str(feedback.get("feedback_packet_digest", "")),
            "source_event_kind": event_kind,
            "previous_cycle_state_digest": previous_digest,
            "channels": channels,
            "reviewed_nonactivated_evidence_count": len(items(review.get("rejected_candidate_ids"))),
            "global_metrics": {
                "mean_memory_kernel_strength": _average(channels, "memory_kernel_strength"),
                "mean_intervention_residue": _average(channels, "intervention_residue"),
                "mean_nonmarkov_coupling": _average(channels, "nonmarkov_coupling"),
                "mean_recoverability_reserve": _average(channels, "recoverability_reserve"),
                "mean_observation_debt": _average(channels, "observation_debt"),
                "mean_relational_resonance": _average(channels, "relational_resonance"),
                "mean_next_cycle_prior_weight": _average(channels, "next_cycle_prior_weight"),
            },
            "process_tensor_context": process_context,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "state_is_cycle_conditioning_surface": True,
                "state_does_not_mutate_indra_world": True,
                "channel_history_digest_chained": True,
            },
            "epoch": int(time.time()),
        }
        state_record["process_tensor_cycle_state_digest"] = cycle_state_digest(state_record)
        state_digest = state_record["process_tensor_cycle_state_digest"]

        seed_packet = {
            "version": "indra_qi_next_cycle_projection_seed_v0_5",
            "seed_status": "next_cycle_projection_seed_ready",
            "cycle_id": cycle_id,
            "cycle_index": cycle_index,
            "source_process_tensor_cycle_state_digest": state_digest,
            "source_world_model_id": str(world_state.get("world_model_id", "")),
            "source_world_state_digest": world_digest_before,
            "seed_entries": seed_entries,
            "seed_entry_order": [entry["seed_id"] for entry in seed_entries],
            "process_tensor_context": process_context,
            "boundary": {
                "next_cycle_seed_not_fact": True,
                "next_cycle_seed_not_truth": True,
                "next_cycle_seed_not_direct_execution_authority": True,
                "next_cycle_seed_requires_new_projection_license": True,
                "candidate_weighting_not_truth": True,
                "non_markov_feedback_preserved": True,
            },
            "epoch": int(time.time()),
        }
        seed_packet["next_cycle_seed_packet_digest"] = sha(seed_packet)
        seed_digest = seed_packet["next_cycle_seed_packet_digest"]

        _write_json(state_path, state_record)
        _write_json(seed_path, seed_packet)

        ledger_record = {
            "version": "indra_qi_process_tensor_cycle_ledger_record_v0_5",
            "record_type": "indra_qi_process_tensor_cycle_evolution",
            "cycle_id": cycle_id,
            "cycle_index": cycle_index,
            "source_activation_id": source_activation_id,
            "source_activation_record_digest": str(activation.get("activation_record_digest", "")),
            "source_world_state_digest": world_digest_before,
            "previous_cycle_state_digest": previous_digest,
            "process_tensor_cycle_state_digest": state_digest,
            "next_cycle_seed_packet_digest": seed_digest,
            "channel_count": len(channels),
            "seed_entry_count": len(seed_entries),
            "prev_record_digest": str(cycle_records[-1].get("record_digest", "GENESIS")) if cycle_records else "GENESIS",
            "boundary": {
                "append_only_cycle_lineage": True,
                "runtime_local_external_state_only": True,
                "source_world_state_not_mutated": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = sha(ledger_record)
        _append_jsonl(cycle_ledger_path, ledger_record)

    world_after = _read_json(world_path)
    world_unchanged = bool(world_state) and bool(world_after) and (
        str(world_after.get("indra_qi_world_state_digest", "")) == world_digest_before
        and compute_indra_qi_world_state_digest(world_after) == world_digest_before
    )
    if not world_unchanged:
        blockers.append("source_indra_qi_world_state_changed_during_cycle_evolution")

    cycle_status = "process_tensor_cycle_evolved" if state_record and not blockers else "process_tensor_cycle_blocked"
    status = READY if cycle_status == "process_tensor_cycle_evolved" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-process-tensor-cycle-"
        + sha(
            {
                "cycle_id": cycle_id,
                "cycle_index": cycle_index,
                "state_digest": state_digest,
                "seed_digest": seed_digest,
                "blockers": blockers,
            }
        )[:16],
        "cycle_id": cycle_id,
        "cycle_index": cycle_index,
        "source_activation_id": source_activation_id,
        "cycle_status": cycle_status,
        "channel_count": len(channels),
        "seed_entry_count": len(seed_entries),
        "source_world_state_unchanged": world_unchanged,
        "source_world_state_digest": world_digest_before,
        "previous_cycle_state_digest": previous_digest,
        "process_tensor_cycle_state_digest": state_digest,
        "next_cycle_seed_packet_digest": seed_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "cycle_state_written": bool(state_record),
            "next_cycle_seed_written": bool(seed_packet),
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiProcessTensorCycleV0_5Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        cycle_id,
        cycle_index,
        source_activation_id,
        cycle_status,
        len(channels),
        len(seed_entries),
        world_unchanged,
        world_digest_before,
        previous_digest,
        state_digest,
        seed_digest,
        str(state_path),
        str(seed_path),
        str(cycle_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
