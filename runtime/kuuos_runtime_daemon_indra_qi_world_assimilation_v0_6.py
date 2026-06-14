#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import cycle_state_digest
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    DYNAMIC_WORLD_FIELDS,
    REQUIRED_BOUNDARY,
    adjusted_seed_weight,
    assimilate_channel,
    assimilation_plan_digest,
    build_effective_holonomy_states,
    corridor_entry,
    debt_ledger_entry,
    dynamic_world_state_digest,
    items,
    mapping,
    number,
    overlay_history_digest,
    previous_dynamic_map,
    protected_constitution_digest,
    sha,
    valid_digest,
    validate_plan,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_process_tensor_world_assimilation_v0_6"
READY = "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_READY"
BLOCKED = "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_BLOCKED"
LICENSE_READY = "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiProcessTensorWorldAssimilationV0_6Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    assimilation_id: str
    source_cycle_id: str
    assimilation_status: str
    dynamic_revision: int
    local_patch_state_count: int
    qi_flow_state_count: int
    debt_ledger_entries_added: int
    corridor_count: int
    effective_holonomy_state_count: int
    post_assimilation_seed_count: int
    world_state_mutated: bool
    rollback_snapshot_written: bool
    rollback_performed: bool
    protected_constitution_preserved: bool
    overlay_history_preserved: bool
    before_world_state_digest: str
    after_world_state_digest: str
    dynamic_world_state_digest: str
    post_assimilation_seed_packet_digest: str
    world_state_path: str
    rollback_snapshot_path: str
    assimilation_record_path: str
    assimilation_ledger_path: str
    seed_packet_path: str
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


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", value)[:128] or "invalid"


def _average(values: list[Mapping[str, Any]], field: str) -> float:
    if not values:
        return 0.0
    return round(sum(number(value.get(field)) for value in values) / len(values), 8)


def _validate_cycle_sources(
    *,
    world_state: Mapping[str, Any],
    cycle_state: Mapping[str, Any],
    seed_packet: Mapping[str, Any],
    cycle_records: list[dict[str, Any]],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> tuple[list[Mapping[str, Any]], dict[str, Mapping[str, Any]], Mapping[str, Any]]:
    if not world_state:
        blockers.append("source_indra_qi_world_state_missing_or_invalid")
    if not cycle_state:
        blockers.append("source_v0_5_cycle_state_missing_or_invalid")
    if not seed_packet:
        blockers.append("source_v0_5_seed_packet_missing_or_invalid")

    world_digest = str(world_state.get("indra_qi_world_state_digest", ""))
    if world_state and compute_indra_qi_world_state_digest(world_state) != world_digest:
        blockers.append("source_indra_qi_world_state_digest_invalid")

    if cycle_state:
        if cycle_state.get("version") != "indra_qi_process_tensor_cycle_v0_5":
            blockers.append("source_v0_5_cycle_state_version_invalid")
        if cycle_state.get("cycle_status") != "process_tensor_cycle_evolved":
            blockers.append("source_v0_5_cycle_state_not_evolved")
        if cycle_state_digest(cycle_state) != str(
            cycle_state.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("source_v0_5_cycle_state_digest_invalid")
        if str(cycle_state.get("source_world_state_digest", "")) != world_digest:
            blockers.append("source_v0_5_cycle_world_state_digest_mismatch")
        boundary = mapping(cycle_state.get("boundary"))
        for field in (
            "cycle_evolution_not_truth",
            "process_tensor_state_not_execution_authority",
            "source_world_state_not_mutated",
            "runtime_local_external_state_only",
            "non_markov_feedback_preserved",
            "uses_process_tensor_feedback",
            "candidate_weighting_not_truth",
            "operator_algebra_unchanged",
            "gauge_connection_unchanged",
            "holonomy_preserved",
            "two_truths_gap_preserved",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"source_v0_5_cycle_boundary_{field}_not_true")

    cycle_digest = str(cycle_state.get("process_tensor_cycle_state_digest", ""))
    if seed_packet:
        if seed_packet.get("version") != "indra_qi_next_cycle_projection_seed_v0_5":
            blockers.append("source_v0_5_seed_packet_version_invalid")
        if seed_packet.get("seed_status") != "next_cycle_projection_seed_ready":
            blockers.append("source_v0_5_seed_packet_not_ready")
        if not valid_digest(seed_packet, "next_cycle_seed_packet_digest"):
            blockers.append("source_v0_5_seed_packet_digest_invalid")
        if str(seed_packet.get("source_process_tensor_cycle_state_digest", "")) != cycle_digest:
            blockers.append("source_v0_5_seed_cycle_state_digest_mismatch")
        if str(seed_packet.get("source_world_state_digest", "")) != world_digest:
            blockers.append("source_v0_5_seed_world_state_digest_mismatch")
        seed_boundary = mapping(seed_packet.get("boundary"))
        for field in (
            "next_cycle_seed_not_fact",
            "next_cycle_seed_not_truth",
            "next_cycle_seed_not_direct_execution_authority",
            "next_cycle_seed_requires_new_projection_license",
            "candidate_weighting_not_truth",
            "non_markov_feedback_preserved",
        ):
            if seed_boundary.get(field) is not True:
                blockers.append(f"source_v0_5_seed_boundary_{field}_not_true")

    cycle_id = str(cycle_state.get("cycle_id", ""))
    matching_record: Mapping[str, Any] = {}
    for record in reversed(cycle_records):
        if str(record.get("cycle_id", "")) == cycle_id:
            matching_record = record
            break
    if not matching_record:
        blockers.append("source_v0_5_cycle_ledger_record_missing")
    else:
        if not valid_digest(matching_record, "record_digest"):
            blockers.append("source_v0_5_cycle_ledger_record_digest_invalid")
        if str(matching_record.get("process_tensor_cycle_state_digest", "")) != cycle_digest:
            blockers.append("source_v0_5_cycle_ledger_state_digest_mismatch")
        if str(matching_record.get("next_cycle_seed_packet_digest", "")) != str(
            seed_packet.get("next_cycle_seed_packet_digest", "")
        ):
            blockers.append("source_v0_5_cycle_ledger_seed_digest_mismatch")
        if str(matching_record.get("source_world_state_digest", "")) != world_digest:
            blockers.append("source_v0_5_cycle_ledger_world_digest_mismatch")

    expected = {
        "source_cycle_id": cycle_id,
        "source_cycle_state_digest": cycle_digest,
        "source_seed_packet_digest": str(seed_packet.get("next_cycle_seed_packet_digest", "")),
        "source_world_state_digest": world_digest,
    }
    for field, value in expected.items():
        if str(plan.get(field, "")) != value:
            blockers.append(f"world_assimilation_plan_{field}_mismatch")

    channels = [mapping(value) for value in items(cycle_state.get("channels"))]
    if not channels:
        blockers.append("source_v0_5_cycle_channels_missing")
    channel_map: dict[str, Mapping[str, Any]] = {}
    for index, channel in enumerate(channels):
        key = str(channel.get("target_key", ""))
        if not key or key in channel_map:
            blockers.append(f"source_v0_5_cycle_channel_{index}_key_invalid_or_duplicate")
        if not valid_digest(channel, "channel_state_digest"):
            blockers.append(f"source_v0_5_cycle_channel_{index}_digest_invalid")
        channel_map[key] = channel

    seed_map: dict[str, Mapping[str, Any]] = {}
    seed_entries = [mapping(value) for value in items(seed_packet.get("seed_entries"))]
    seed_order = [str(value) for value in items(seed_packet.get("seed_entry_order"))]
    if seed_order != [str(entry.get("seed_id", "")) for entry in seed_entries]:
        blockers.append("source_v0_5_seed_entry_order_mismatch")
    for index, entry in enumerate(seed_entries):
        if not valid_digest(entry, "seed_entry_digest"):
            blockers.append(f"source_v0_5_seed_entry_{index}_digest_invalid")
        key = str(entry.get("target_key", ""))
        if not key or key in seed_map:
            blockers.append(f"source_v0_5_seed_entry_{index}_key_invalid_or_duplicate")
        if key not in channel_map:
            blockers.append(f"source_v0_5_seed_entry_{index}_channel_missing")
        elif str(entry.get("source_channel_state_digest", "")) != str(
            channel_map[key].get("channel_state_digest", "")
        ):
            blockers.append(f"source_v0_5_seed_entry_{index}_channel_digest_mismatch")
        seed_map[key] = entry
    return channels, seed_map, matching_record


def build_indra_qi_process_tensor_world_assimilation_v0_6(
    *,
    runtime_context: Mapping[str, Any],
    assimilation_plan: Mapping[str, Any],
    assimilation_license: Mapping[str, Any],
) -> IndraQiProcessTensorWorldAssimilationV0_6Result:
    context = mapping(runtime_context)
    plan = dict(mapping(assimilation_plan))
    license_value = mapping(assimilation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    world_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    cycle_state_path = root / "indra_qi_process_tensor_cycle_state_v0_5.json"
    source_seed_path = root / "indra_qi_next_cycle_projection_seed_v0_5.json"
    cycle_ledger_path = root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl"
    seed_path = root / "indra_qi_post_assimilation_projection_seed_v0_6.json"
    assimilation_record_path = root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json"
    assimilation_ledger_path = root / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
    receipt_path = root / "indra_qi_process_tensor_world_assimilation_receipt_v0_6.json"
    audit_path = root / "indra_qi_process_tensor_world_assimilation_audit_v0_6.jsonl"

    assimilation_id = str(plan.get("assimilation_id", ""))
    snapshot_path = root / f"indra_qi_world_assimilation_rollback_snapshot_v0_6_{_safe_id(assimilation_id)}.json"

    if context.get("indra_qi_process_tensor_world_assimilation_v0_6_enabled") is not True:
        blockers.append("indra_qi_process_tensor_world_assimilation_v0_6_enabled_not_true")
    if context.get("apply_indra_qi_process_tensor_world_assimilation_v0_6") is not True:
        blockers.append("apply_indra_qi_process_tensor_world_assimilation_v0_6_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("world_assimilation_license_not_ready")
    required_flags = (
        "world_state_read_allowed",
        "cycle_state_read_allowed",
        "source_seed_read_allowed",
        "cycle_ledger_read_allowed",
        "assimilation_plan_validate_allowed",
        "rollback_snapshot_write_allowed",
        "dynamic_world_state_write_allowed",
        "world_state_write_allowed",
        "post_write_verification_allowed",
        "post_assimilation_seed_write_allowed",
        "assimilation_record_write_allowed",
        "assimilation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "direct_world_model_mutation_allowed",
    )
    for flag in required_flags:
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    plan_digest = str(plan.get("assimilation_plan_digest", ""))
    if str(license_value.get("bound_assimilation_plan_digest", "")) != plan_digest:
        blockers.append("world_assimilation_license_plan_digest_mismatch")
    scopes = license_value.get("allowed_mutation_scopes", [])
    scope_set = {str(value) for value in scopes} if isinstance(scopes, list) else set()
    if scope_set != {"process_tensor_dynamic_world_state_only"}:
        blockers.append("world_assimilation_license_scope_not_exact")
    fields = license_value.get("allowed_dynamic_world_fields", [])
    field_set = {str(value) for value in fields} if isinstance(fields, list) else set()
    expected_fields = set(DYNAMIC_WORLD_FIELDS) | {"process_tensor_world_state"}
    if field_set != expected_fields:
        blockers.append("world_assimilation_license_dynamic_fields_not_exact")

    world_state = _read_json(world_path)
    cycle_state = _read_json(cycle_state_path)
    source_seed = _read_json(source_seed_path)
    cycle_records = _records(cycle_ledger_path)
    channels, source_seed_map, _ = _validate_cycle_sources(
        world_state=world_state,
        cycle_state=cycle_state,
        seed_packet=source_seed,
        cycle_records=cycle_records,
        plan=plan,
        blockers=blockers,
    )

    assimilation_records = _records(assimilation_ledger_path)
    source_cycle_id = str(cycle_state.get("cycle_id", ""))
    if assimilation_id and any(
        str(record.get("assimilation_id", "")) == assimilation_id
        for record in assimilation_records
    ):
        blockers.append("world_assimilation_id_replay")
    if source_cycle_id and any(
        str(record.get("source_cycle_id", "")) == source_cycle_id
        for record in assimilation_records
    ):
        blockers.append("source_cycle_world_assimilation_replay")

    previous_summary = mapping(world_state.get("process_tensor_world_state"))
    previous_dynamic_digest = "GENESIS"
    dynamic_revision = 1
    if previous_summary:
        previous_dynamic_digest = str(
            world_state.get("process_tensor_dynamic_world_state_digest", "")
        )
        if not previous_dynamic_digest or dynamic_world_state_digest(world_state) != previous_dynamic_digest:
            blockers.append("previous_dynamic_world_state_digest_invalid")
        previous_revision = previous_summary.get("dynamic_revision", 0)
        if isinstance(previous_revision, bool) or not isinstance(previous_revision, int) or previous_revision < 1:
            blockers.append("previous_dynamic_world_revision_invalid")
        else:
            dynamic_revision = previous_revision + 1
        if not assimilation_records:
            blockers.append("previous_world_assimilation_ledger_missing")
        elif str(assimilation_records[-1].get("dynamic_world_state_digest", "")) != previous_dynamic_digest:
            blockers.append("previous_world_assimilation_ledger_dynamic_digest_mismatch")
    if str(plan.get("expected_previous_dynamic_world_state_digest", "")) != previous_dynamic_digest:
        blockers.append("world_assimilation_expected_previous_dynamic_digest_mismatch")

    policy = mapping(plan.get("assimilation_policy"))
    previous_map = previous_dynamic_map(world_state)
    dynamic_states = [
        assimilate_channel(
            channel=channel,
            previous=previous_map.get(str(channel.get("target_key", "")), {}),
            policy=policy,
            assimilation_id=assimilation_id,
            revision=dynamic_revision,
        )
        for channel in channels
    ]
    patch_states = [state for state in dynamic_states if state.get("state_kind") == "local_patch_dynamic_state"]
    flow_states = [state for state in dynamic_states if state.get("state_kind") == "qi_flow_effective_state"]

    existing_debt_ledger = list(items(world_state.get("observation_debt_ledger")))
    new_debt_entries = [
        debt_ledger_entry(
            dynamic_state=state,
            previous=previous_map.get(str(state.get("target_key", "")), {}),
            cycle_id=source_cycle_id,
            cycle_digest=str(cycle_state.get("process_tensor_cycle_state_digest", "")),
        )
        for state in dynamic_states
    ]
    debt_ledger = existing_debt_ledger + new_debt_entries
    existing_corridors = {
        str(mapping(value).get("target_key", "")): mapping(value)
        for value in items(world_state.get("recoverability_corridors"))
        if str(mapping(value).get("target_key", ""))
    }
    for state in dynamic_states:
        corridor = corridor_entry(
            state,
            str(cycle_state.get("process_tensor_cycle_state_digest", "")),
        )
        existing_corridors[str(corridor.get("target_key", ""))] = corridor
    corridors = [existing_corridors[key] for key in sorted(existing_corridors)]
    holonomy_states = build_effective_holonomy_states(
        world_state=world_state,
        flow_states=flow_states,
        cycle_digest=str(cycle_state.get("process_tensor_cycle_state_digest", "")),
    )

    constitution_before = protected_constitution_digest(world_state) if world_state else ""
    overlay_before = overlay_history_digest(world_state) if world_state else ""
    before_digest = str(world_state.get("indra_qi_world_state_digest", ""))
    state_mutated = False
    snapshot_written = False
    rollback_performed = False
    constitution_preserved = False
    overlay_preserved = False
    after_digest = before_digest
    dynamic_digest = ""
    post_seed_digest = ""
    seed_entries: list[dict[str, Any]] = []
    snapshot_record: dict[str, Any] = {}

    if not blockers:
        snapshot_record = {
            "version": "indra_qi_world_assimilation_rollback_snapshot_v0_6",
            "assimilation_id": assimilation_id,
            "source_cycle_id": source_cycle_id,
            "before_world_state_digest": before_digest,
            "protected_constitution_digest": constitution_before,
            "overlay_history_digest": overlay_before,
            "previous_dynamic_world_state_digest": previous_dynamic_digest,
            "world_state": deepcopy(world_state),
            "epoch": int(time.time()),
        }
        snapshot_record["rollback_snapshot_digest"] = sha(snapshot_record)
        _write_json(snapshot_path, snapshot_record)
        snapshot_written = True

        next_state = deepcopy(world_state)
        next_state["local_patch_dynamic_states"] = patch_states
        next_state["qi_flow_effective_states"] = flow_states
        next_state["observation_debt_ledger"] = debt_ledger
        next_state["recoverability_corridors"] = corridors
        next_state["effective_holonomy_states"] = holonomy_states
        summary = {
            "version": VERSION,
            "assimilation_status": "dynamic_world_state_assimilated",
            "assimilation_id": assimilation_id,
            "dynamic_revision": dynamic_revision,
            "source_cycle_id": source_cycle_id,
            "source_cycle_state_digest": str(
                cycle_state.get("process_tensor_cycle_state_digest", "")
            ),
            "source_seed_packet_digest": str(
                source_seed.get("next_cycle_seed_packet_digest", "")
            ),
            "previous_dynamic_world_state_digest": previous_dynamic_digest,
            "local_patch_state_count": len(patch_states),
            "qi_flow_state_count": len(flow_states),
            "debt_ledger_entry_count": len(debt_ledger),
            "recoverability_corridor_count": len(corridors),
            "effective_holonomy_state_count": len(holonomy_states),
            "global_metrics": {
                "mean_memory_kernel_strength": _average(dynamic_states, "memory_kernel_strength"),
                "mean_intervention_residue": _average(dynamic_states, "intervention_residue"),
                "mean_nonmarkov_coupling": _average(dynamic_states, "nonmarkov_coupling"),
                "mean_recoverability_reserve": _average(dynamic_states, "recoverability_reserve"),
                "mean_observation_debt": _average(dynamic_states, "observation_debt"),
                "mean_relational_tension": _average(dynamic_states, "relational_tension"),
                "mean_corridor_openness": _average(
                    dynamic_states, "recoverability_corridor_openness"
                ),
            },
            "boundary": {
                **REQUIRED_BOUNDARY,
                "world_dynamic_state_mutated": True,
                "base_constitution_preserved": True,
                "observation_overlay_history_preserved": True,
            },
            "epoch": int(time.time()),
        }
        next_state["process_tensor_world_state"] = summary
        next_state["process_tensor_dynamic_world_state_digest"] = dynamic_world_state_digest(
            next_state
        )
        next_state["world_dynamic_revision"] = dynamic_revision
        next_state["last_world_assimilation_id"] = assimilation_id
        next_state["last_process_tensor_cycle_state_digest"] = str(
            cycle_state.get("process_tensor_cycle_state_digest", "")
        )
        next_state["indra_qi_world_state_digest"] = compute_indra_qi_world_state_digest(
            next_state
        )

        try:
            _write_json(world_path, next_state)
            verified = _read_json(world_path)
            after_digest = str(verified.get("indra_qi_world_state_digest", ""))
            world_valid = bool(after_digest) and compute_indra_qi_world_state_digest(
                verified
            ) == after_digest
            dynamic_digest = str(
                verified.get("process_tensor_dynamic_world_state_digest", "")
            )
            dynamic_valid = bool(dynamic_digest) and dynamic_world_state_digest(
                verified
            ) == dynamic_digest
            constitution_preserved = protected_constitution_digest(
                verified
            ) == constitution_before
            overlay_preserved = overlay_history_digest(verified) == overlay_before
            if not world_valid:
                blockers.append("post_write_world_state_digest_invalid")
            if not dynamic_valid:
                blockers.append("post_write_dynamic_world_state_digest_invalid")
            if not constitution_preserved:
                blockers.append("post_write_constitution_changed")
            if not overlay_preserved:
                blockers.append("post_write_observation_overlay_history_changed")
            if blockers:
                _write_json(world_path, world_state)
                rollback_performed = True
                after_digest = before_digest
                dynamic_digest = previous_dynamic_digest if previous_dynamic_digest != "GENESIS" else ""
            else:
                state_mutated = True
                source_seed_entries = {
                    str(entry.get("target_key", "")): entry
                    for entry in source_seed_map.values()
                }
                min_weight = number(
                    policy.get("min_post_assimilation_seed_weight"), 0.45
                )
                for state in dynamic_states:
                    key = str(state.get("target_key", ""))
                    source_entry = mapping(source_seed_entries.get(key, {}))
                    source_weight = number(source_entry.get("prior_weight"))
                    weight = adjusted_seed_weight(
                        source_weight=source_weight,
                        dynamic_state=state,
                        policy=policy,
                    )
                    if weight < min_weight:
                        continue
                    entry = {
                        "seed_id": f"post-assimilation-{key}",
                        "target_key": key,
                        "target": dict(mapping(state.get("target"))),
                        "assimilated_prior_weight": weight,
                        "memory_kernel_strength": state.get(
                            "memory_kernel_strength"
                        ),
                        "intervention_residue": state.get(
                            "intervention_residue"
                        ),
                        "nonmarkov_coupling": state.get("nonmarkov_coupling"),
                        "recoverability_reserve": state.get(
                            "recoverability_reserve"
                        ),
                        "observation_debt": state.get("observation_debt"),
                        "relational_tension": state.get("relational_tension"),
                        "recoverability_corridor_status": state.get(
                            "recoverability_corridor_status"
                        ),
                        "effective_capacity": state.get(
                            "effective_transport_coefficient",
                            state.get("effective_response_capacity"),
                        ),
                        "source_v0_5_seed_entry_digest": str(
                            source_entry.get("seed_entry_digest", "")
                        ),
                        "source_dynamic_state_entry_digest": str(
                            state.get("dynamic_state_entry_digest", "")
                        ),
                        "source_dynamic_world_state_digest": dynamic_digest,
                        "source_world_state_digest": after_digest,
                        "boundary": {
                            "seed_not_fact": True,
                            "seed_not_truth": True,
                            "seed_not_direct_execution_authority": True,
                            "seed_requires_new_projection_license": True,
                            "debt_and_recoverability_world_conditioned": True,
                            "candidate_weighting_not_truth": True,
                        },
                    }
                    entry["seed_entry_digest"] = sha(entry)
                    seed_entries.append(entry)
        except OSError:
            blockers.append("world_assimilation_write_failed")
            try:
                _write_json(world_path, world_state)
                rollback_performed = True
            except OSError:
                warnings.append("world_assimilation_rollback_restore_failed")

    assimilation_status = (
        "dynamic_world_state_assimilated"
        if state_mutated and not blockers
        else "dynamic_world_state_assimilation_blocked"
    )
    seed_packet: dict[str, Any] = {}
    assimilation_record: dict[str, Any] = {}
    if assimilation_status == "dynamic_world_state_assimilated":
        seed_packet = {
            "version": "indra_qi_post_assimilation_projection_seed_v0_6",
            "seed_status": "post_assimilation_projection_seed_ready",
            "assimilation_id": assimilation_id,
            "source_cycle_id": source_cycle_id,
            "source_cycle_state_digest": str(
                cycle_state.get("process_tensor_cycle_state_digest", "")
            ),
            "source_v0_5_seed_packet_digest": str(
                source_seed.get("next_cycle_seed_packet_digest", "")
            ),
            "source_dynamic_world_state_digest": dynamic_digest,
            "source_world_state_digest": after_digest,
            "seed_entries": seed_entries,
            "seed_entry_order": [entry["seed_id"] for entry in seed_entries],
            "boundary": {
                "post_assimilation_seed_not_fact": True,
                "post_assimilation_seed_not_truth": True,
                "post_assimilation_seed_not_direct_execution_authority": True,
                "post_assimilation_seed_requires_new_projection_license": True,
                "debt_changes_projection_conditions": True,
                "recoverability_changes_projection_conditions": True,
                "candidate_weighting_not_truth": True,
                "non_markov_feedback_preserved": True,
            },
            "epoch": int(time.time()),
        }
        seed_packet["post_assimilation_seed_packet_digest"] = sha(seed_packet)
        post_seed_digest = seed_packet["post_assimilation_seed_packet_digest"]
        _write_json(seed_path, seed_packet)

        assimilation_record = {
            "version": "indra_qi_process_tensor_world_assimilation_record_v0_6",
            "assimilation_status": assimilation_status,
            "assimilation_id": assimilation_id,
            "source_cycle_id": source_cycle_id,
            "source_cycle_state_digest": str(
                cycle_state.get("process_tensor_cycle_state_digest", "")
            ),
            "source_v0_5_seed_packet_digest": str(
                source_seed.get("next_cycle_seed_packet_digest", "")
            ),
            "assimilation_plan_digest": plan_digest,
            "rollback_snapshot_digest": str(
                snapshot_record.get("rollback_snapshot_digest", "")
            ),
            "before_world_state_digest": before_digest,
            "after_world_state_digest": after_digest,
            "previous_dynamic_world_state_digest": previous_dynamic_digest,
            "dynamic_world_state_digest": dynamic_digest,
            "post_assimilation_seed_packet_digest": post_seed_digest,
            "dynamic_revision": dynamic_revision,
            "local_patch_state_count": len(patch_states),
            "qi_flow_state_count": len(flow_states),
            "debt_ledger_entries_added": len(new_debt_entries),
            "recoverability_corridor_count": len(corridors),
            "effective_holonomy_state_count": len(holonomy_states),
            "protected_constitution_digest": constitution_before,
            "overlay_history_digest": overlay_before,
            "protected_constitution_preserved": constitution_preserved,
            "overlay_history_preserved": overlay_preserved,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "world_state_mutated": True,
                "mutation_restricted_to_dynamic_world_state": True,
                "post_write_verification_completed": True,
                "rollback_corridor_preserved": True,
            },
            "epoch": int(time.time()),
        }
        assimilation_record["assimilation_record_digest"] = sha(
            assimilation_record
        )
        _write_json(assimilation_record_path, assimilation_record)

        ledger_record = {
            "version": "indra_qi_process_tensor_world_assimilation_ledger_record_v0_6",
            "record_type": "process_tensor_dynamic_world_assimilation",
            "assimilation_id": assimilation_id,
            "source_cycle_id": source_cycle_id,
            "source_cycle_state_digest": str(
                cycle_state.get("process_tensor_cycle_state_digest", "")
            ),
            "source_assimilation_record_digest": assimilation_record[
                "assimilation_record_digest"
            ],
            "before_world_state_digest": before_digest,
            "after_world_state_digest": after_digest,
            "previous_dynamic_world_state_digest": previous_dynamic_digest,
            "dynamic_world_state_digest": dynamic_digest,
            "post_assimilation_seed_packet_digest": post_seed_digest,
            "prev_record_digest": str(
                assimilation_records[-1].get("record_digest", "GENESIS")
            )
            if assimilation_records
            else "GENESIS",
            "boundary": {
                "append_only_world_assimilation_lineage": True,
                "dynamic_world_state_layer_only": True,
                "base_constitution_preserved": True,
                "observation_overlay_history_preserved": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = sha(ledger_record)
        _append_jsonl(assimilation_ledger_path, ledger_record)

    status = READY if assimilation_status == "dynamic_world_state_assimilated" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-world-assimilation-"
        + sha(
            {
                "assimilation_id": assimilation_id,
                "before_digest": before_digest,
                "after_digest": after_digest,
                "dynamic_digest": dynamic_digest,
                "blockers": blockers,
            }
        )[:16],
        "assimilation_id": assimilation_id,
        "source_cycle_id": source_cycle_id,
        "assimilation_status": assimilation_status,
        "dynamic_revision": dynamic_revision,
        "local_patch_state_count": len(patch_states),
        "qi_flow_state_count": len(flow_states),
        "debt_ledger_entries_added": len(new_debt_entries),
        "corridor_count": len(corridors),
        "effective_holonomy_state_count": len(holonomy_states),
        "post_assimilation_seed_count": len(seed_entries),
        "world_state_mutated": state_mutated,
        "rollback_snapshot_written": snapshot_written,
        "rollback_performed": rollback_performed,
        "protected_constitution_preserved": constitution_preserved,
        "overlay_history_preserved": overlay_preserved,
        "before_world_state_digest": before_digest,
        "after_world_state_digest": after_digest,
        "dynamic_world_state_digest": dynamic_digest,
        "post_assimilation_seed_packet_digest": post_seed_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "assimilation_completed": assimilation_status
            == "dynamic_world_state_assimilated",
            "external_world_not_actuated": True,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(
            audit_path, {**receipt, "audit_record_digest": sha(receipt)}
        )

    return IndraQiProcessTensorWorldAssimilationV0_6Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        assimilation_id,
        source_cycle_id,
        assimilation_status,
        dynamic_revision,
        len(patch_states),
        len(flow_states),
        len(new_debt_entries),
        len(corridors),
        len(holonomy_states),
        len(seed_entries),
        state_mutated,
        snapshot_written,
        rollback_performed,
        constitution_preserved,
        overlay_preserved,
        before_digest,
        after_digest,
        dynamic_digest,
        post_seed_digest,
        str(world_path),
        str(snapshot_path),
        str(assimilation_record_path),
        str(assimilation_ledger_path),
        str(seed_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
