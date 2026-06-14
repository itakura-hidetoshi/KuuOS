#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import pathlib
import shutil
import time
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_parent_cycle_reentry_core_v0_11 import (
    REQUIRED_BOUNDARY,
    build_assimilation_plan,
    build_reentry_plan,
    items,
    loop_plan_digest,
    mapping,
    sha,
    valid_digest,
    validate_assimilation_license_template,
    validate_plan,
    validate_reentry_license_template,
)
from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import cycle_state_digest
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    dynamic_world_state_digest,
    overlay_history_digest,
    protected_constitution_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_post_assimilation_reentry_v0_7 import (
    build_indra_qi_post_assimilation_causal_reentry_v0_7,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_assimilation_v0_6 import (
    build_indra_qi_process_tensor_world_assimilation_v0_6,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_parent_cycle_assimilation_reentry_v0_11"
READY = "INDRA_QI_PARENT_CYCLE_ASSIMILATION_REENTRY_V0_11_READY"
BLOCKED = "INDRA_QI_PARENT_CYCLE_ASSIMILATION_REENTRY_V0_11_BLOCKED"
LICENSE_READY = "INDRA_QI_PARENT_CYCLE_ASSIMILATION_REENTRY_V0_11_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiParentCycleAssimilationReentryV0_11Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    loop_id: str
    source_v0_10_bridge_id: str
    source_cycle_id: str
    loop_status: str
    v0_6_assimilation_invoked: bool
    v0_6_assimilation_ready: bool
    v0_7_reentry_invoked: bool
    v0_7_reentry_ready: bool
    transaction_committed: bool
    transaction_rolled_back: bool
    rollback_reason: str
    before_parent_world_state_digest: str
    after_assimilation_world_state_digest: str
    previous_dynamic_world_state_digest: str
    dynamic_world_state_digest: str
    dynamic_revision: int
    post_assimilation_seed_packet_digest: str
    reentry_id: str
    child_runtime_root: str
    projection_packet_digest: str
    projection_activation_digest: str
    v14_world_model_digest: str
    loop_handoff_packet_digest: str
    loop_handoff_path: str
    loop_record_path: str
    loop_ledger_path: str
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
    return "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in value)[:128] or "invalid"


def _latest_matching(
    records: list[dict[str, Any]], field: str, expected: str
) -> Mapping[str, Any]:
    for record in reversed(records):
        if str(record.get(field, "")) == expected:
            return record
    return {}


def _snapshot_files(paths: list[pathlib.Path]) -> dict[pathlib.Path, bytes | None]:
    return {path: path.read_bytes() if path.is_file() else None for path in paths}


def _restore_files(snapshot: Mapping[pathlib.Path, bytes | None]) -> None:
    for path, content in snapshot.items():
        if content is None:
            if path.exists():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".restore.tmp")
        temporary.write_bytes(content)
        os.replace(temporary, path)


def _validate_source_v0_10(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    blockers: list[str],
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    handoff = _read_json(root / "indra_qi_child_feedback_parent_cycle_handoff_v0_10.json")
    bridge_record = _read_json(root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json")
    bridge_records = _records(root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl")
    world = _read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    cycle = _read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
    seed = _read_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json")
    cycle_records = _records(root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl")

    if not handoff:
        blockers.append("parent_cycle_reentry_source_v0_10_handoff_missing_or_invalid")
    else:
        if handoff.get("version") != "indra_qi_child_feedback_parent_cycle_handoff_packet_v0_10":
            blockers.append("parent_cycle_reentry_source_v0_10_handoff_version_invalid")
        if handoff.get("handoff_status") != "child_feedback_activated_and_parent_cycle_evolved":
            blockers.append("parent_cycle_reentry_source_v0_10_handoff_not_ready")
        if not valid_digest(handoff, "handoff_packet_digest"):
            blockers.append("parent_cycle_reentry_source_v0_10_handoff_digest_invalid")
        boundary = mapping(handoff.get("boundary"))
        for field in (
            "child_feedback_handoff_not_truth",
            "parent_world_mutation_only_via_v0_4",
            "runtime_observation_overlay_only",
            "runtime_local_external_state_only",
            "non_markov_feedback_preserved",
            "uses_process_tensor_feedback",
            "candidate_weighting_not_truth",
            "not_direct_execution_authority",
            "child_feedback_staged_into_parent_runtime",
            "v0_4_activation_completed",
            "v0_5_cycle_completed",
            "parent_world_mutation_traceable",
            "child_runtime_unchanged",
        ):
            if boundary.get(field) is not True:
                blockers.append(f"parent_cycle_reentry_source_v0_10_boundary_{field}_not_true")
        if boundary.get("not_external_world_actuation_authority") is not True:
            blockers.append("parent_cycle_reentry_source_v0_10_external_boundary_invalid")

    if not bridge_record:
        blockers.append("parent_cycle_reentry_source_v0_10_record_missing_or_invalid")
    else:
        if bridge_record.get("version") != "indra_qi_child_feedback_parent_cycle_record_v0_10":
            blockers.append("parent_cycle_reentry_source_v0_10_record_version_invalid")
        if bridge_record.get("handoff_status") != "child_feedback_activated_and_parent_cycle_evolved":
            blockers.append("parent_cycle_reentry_source_v0_10_record_not_ready")
        if not valid_digest(bridge_record, "bridge_record_digest"):
            blockers.append("parent_cycle_reentry_source_v0_10_record_digest_invalid")
        if str(bridge_record.get("source_handoff_packet_digest", "")) != str(
            handoff.get("handoff_packet_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_v0_10_record_handoff_mismatch")

    bridge_id = str(handoff.get("bridge_id", ""))
    bridge_ledger = _latest_matching(bridge_records, "bridge_id", bridge_id)
    if not bridge_ledger:
        blockers.append("parent_cycle_reentry_source_v0_10_ledger_missing")
    else:
        if not valid_digest(bridge_ledger, "record_digest"):
            blockers.append("parent_cycle_reentry_source_v0_10_ledger_digest_invalid")
        if str(bridge_ledger.get("source_handoff_packet_digest", "")) != str(
            handoff.get("handoff_packet_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_v0_10_ledger_handoff_mismatch")
        if str(bridge_ledger.get("source_bridge_record_digest", "")) != str(
            bridge_record.get("bridge_record_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_v0_10_ledger_record_mismatch")

    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    if not world:
        blockers.append("parent_cycle_reentry_parent_world_missing_or_invalid")
    elif compute_indra_qi_world_state_digest(world) != world_digest:
        blockers.append("parent_cycle_reentry_parent_world_digest_invalid")
    if world_digest != str(handoff.get("after_parent_world_state_digest", "")):
        blockers.append("parent_cycle_reentry_parent_world_v0_10_digest_mismatch")

    if not cycle:
        blockers.append("parent_cycle_reentry_source_cycle_missing_or_invalid")
    else:
        if cycle.get("version") != "indra_qi_process_tensor_cycle_v0_5":
            blockers.append("parent_cycle_reentry_source_cycle_version_invalid")
        if cycle.get("cycle_status") != "process_tensor_cycle_evolved":
            blockers.append("parent_cycle_reentry_source_cycle_not_evolved")
        if cycle_state_digest(cycle) != str(cycle.get("process_tensor_cycle_state_digest", "")):
            blockers.append("parent_cycle_reentry_source_cycle_digest_invalid")
        if str(cycle.get("source_world_state_digest", "")) != world_digest:
            blockers.append("parent_cycle_reentry_source_cycle_world_digest_mismatch")
        if str(cycle.get("process_tensor_cycle_state_digest", "")) != str(
            handoff.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_cycle_v0_10_digest_mismatch")

    if not seed:
        blockers.append("parent_cycle_reentry_source_cycle_seed_missing_or_invalid")
    else:
        if seed.get("version") != "indra_qi_next_cycle_projection_seed_v0_5":
            blockers.append("parent_cycle_reentry_source_cycle_seed_version_invalid")
        if seed.get("seed_status") != "next_cycle_projection_seed_ready":
            blockers.append("parent_cycle_reentry_source_cycle_seed_not_ready")
        if not valid_digest(seed, "next_cycle_seed_packet_digest"):
            blockers.append("parent_cycle_reentry_source_cycle_seed_digest_invalid")
        if str(seed.get("source_process_tensor_cycle_state_digest", "")) != str(
            cycle.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_cycle_seed_state_mismatch")
        if str(seed.get("source_world_state_digest", "")) != world_digest:
            blockers.append("parent_cycle_reentry_source_cycle_seed_world_mismatch")
        if str(seed.get("next_cycle_seed_packet_digest", "")) != str(
            handoff.get("next_cycle_seed_packet_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_cycle_seed_v0_10_mismatch")

    cycle_id = str(cycle.get("cycle_id", ""))
    cycle_ledger = _latest_matching(cycle_records, "cycle_id", cycle_id)
    if not cycle_ledger:
        blockers.append("parent_cycle_reentry_source_cycle_ledger_missing")
    else:
        if not valid_digest(cycle_ledger, "record_digest"):
            blockers.append("parent_cycle_reentry_source_cycle_ledger_digest_invalid")
        if str(cycle_ledger.get("process_tensor_cycle_state_digest", "")) != str(
            cycle.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_cycle_ledger_state_mismatch")
        if str(cycle_ledger.get("next_cycle_seed_packet_digest", "")) != str(
            seed.get("next_cycle_seed_packet_digest", "")
        ):
            blockers.append("parent_cycle_reentry_source_cycle_ledger_seed_mismatch")

    expected = {
        "source_v0_10_bridge_id": bridge_id,
        "source_v0_10_handoff_packet_digest": str(handoff.get("handoff_packet_digest", "")),
        "source_v0_10_bridge_record_digest": str(bridge_record.get("bridge_record_digest", "")),
        "source_v0_10_ledger_record_digest": str(bridge_ledger.get("record_digest", "")),
        "source_parent_world_state_digest": world_digest,
        "source_cycle_id": cycle_id,
        "source_cycle_state_digest": str(cycle.get("process_tensor_cycle_state_digest", "")),
        "source_cycle_seed_packet_digest": str(seed.get("next_cycle_seed_packet_digest", "")),
    }
    for field, expected_value in expected.items():
        if str(plan.get(field, "")) != expected_value:
            blockers.append(f"parent_cycle_reentry_plan_{field}_mismatch")

    return handoff, bridge_record, dict(bridge_ledger), world, cycle, seed, dict(cycle_ledger)


def build_indra_qi_parent_cycle_assimilation_reentry_v0_11(
    *,
    runtime_context: Mapping[str, Any],
    loop_plan: Mapping[str, Any],
    loop_license: Mapping[str, Any],
) -> IndraQiParentCycleAssimilationReentryV0_11Result:
    context = mapping(runtime_context)
    plan = dict(mapping(loop_plan))
    license_value = mapping(loop_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    if context.get("indra_qi_parent_cycle_assimilation_reentry_v0_11_enabled") is not True:
        blockers.append("indra_qi_parent_cycle_assimilation_reentry_v0_11_enabled_not_true")
    if context.get("apply_indra_qi_parent_cycle_assimilation_reentry_v0_11") is not True:
        blockers.append("apply_indra_qi_parent_cycle_assimilation_reentry_v0_11_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("parent_cycle_reentry_loop_license_not_ready")
    for flag in (
        "source_v0_10_read_allowed",
        "parent_world_read_allowed",
        "cycle_state_read_allowed",
        "transaction_snapshot_allowed",
        "transaction_restore_allowed",
        "child_runtime_remove_on_failure_allowed",
        "v0_6_assimilation_invoke_allowed",
        "v0_7_reentry_invoke_allowed",
        "loop_handoff_write_allowed",
        "loop_record_write_allowed",
        "loop_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    validate_plan(plan, blockers)
    plan_digest = str(plan.get("loop_plan_digest", ""))
    if str(license_value.get("bound_loop_plan_digest", "")) != plan_digest:
        blockers.append("parent_cycle_reentry_loop_license_plan_digest_mismatch")
    assimilation_template = mapping(license_value.get("v0_6_assimilation_license_template"))
    reentry_template = mapping(license_value.get("v0_7_reentry_license_template"))
    validate_assimilation_license_template(assimilation_template, blockers)
    projection_limit = int(mapping(plan.get("projection_policy")).get("max_projection_variables", 0) or 0)
    validate_reentry_license_template(reentry_template, projection_limit, blockers)

    handoff, bridge_record, bridge_ledger, world, cycle, seed, cycle_ledger = _validate_source_v0_10(
        root=root,
        plan=plan,
        blockers=blockers,
    )

    loop_id = str(plan.get("loop_id", ""))
    source_bridge_id = str(handoff.get("bridge_id", ""))
    source_handoff_digest = str(handoff.get("handoff_packet_digest", ""))
    source_cycle_id = str(cycle.get("cycle_id", ""))
    before_world_digest = str(world.get("indra_qi_world_state_digest", ""))
    previous_dynamic_digest = str(world.get("process_tensor_dynamic_world_state_digest", "")) or "GENESIS"
    if previous_dynamic_digest != "GENESIS" and dynamic_world_state_digest(world) != previous_dynamic_digest:
        blockers.append("parent_cycle_reentry_previous_dynamic_world_digest_invalid")
    if str(plan.get("expected_previous_dynamic_world_state_digest", "")) != previous_dynamic_digest:
        blockers.append("parent_cycle_reentry_expected_previous_dynamic_digest_mismatch")

    loop_ledger_path = root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl"
    prior_loop_records = _records(loop_ledger_path)
    if loop_id and any(str(value.get("loop_id", "")) == loop_id for value in prior_loop_records):
        blockers.append("parent_cycle_reentry_loop_id_replay")
    if source_handoff_digest and any(
        str(value.get("source_v0_10_handoff_packet_digest", "")) == source_handoff_digest
        for value in prior_loop_records
    ):
        blockers.append("parent_cycle_reentry_source_v0_10_handoff_replay")

    reentry_id = str(plan.get("reentry_id", ""))
    child_root = root / "indra_qi_causal_reentry_cycles_v0_7" / _safe_id(reentry_id)
    allowed_child_parent = (root / "indra_qi_causal_reentry_cycles_v0_7").resolve()
    try:
        child_root.resolve().relative_to(allowed_child_parent)
    except ValueError:
        blockers.append("parent_cycle_reentry_child_runtime_outside_allowed_root")
    if child_root.exists():
        blockers.append("parent_cycle_reentry_child_runtime_already_exists")

    world_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    assimilation_id = str(plan.get("assimilation_id", ""))
    assimilation_snapshot_path = root / (
        "indra_qi_world_assimilation_rollback_snapshot_v0_6_"
        + _safe_id(assimilation_id)
        + ".json"
    )
    assimilation_seed_path = root / "indra_qi_post_assimilation_projection_seed_v0_6.json"
    assimilation_record_path = root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json"
    assimilation_ledger_path = root / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
    assimilation_receipt_path = root / "indra_qi_process_tensor_world_assimilation_receipt_v0_6.json"
    assimilation_audit_path = root / "indra_qi_process_tensor_world_assimilation_audit_v0_6.jsonl"
    reentry_record_path = root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json"
    reentry_ledger_path = root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl"
    reentry_receipt_path = root / "indra_qi_post_assimilation_causal_reentry_receipt_v0_7.json"
    reentry_audit_path = root / "indra_qi_post_assimilation_causal_reentry_audit_v0_7.jsonl"

    touched_paths = [
        world_path,
        assimilation_snapshot_path,
        assimilation_seed_path,
        assimilation_record_path,
        assimilation_ledger_path,
        assimilation_receipt_path,
        assimilation_audit_path,
        reentry_record_path,
        reentry_ledger_path,
        reentry_receipt_path,
        reentry_audit_path,
    ]
    transaction_snapshot = _snapshot_files(touched_paths) if not blockers else {}
    before_constitution = protected_constitution_digest(world) if world else ""
    before_overlay_history = overlay_history_digest(world) if world else ""

    assimilation_invoked = False
    assimilation_ready = False
    reentry_invoked = False
    reentry_ready = False
    transaction_committed = False
    rolled_back = False
    rollback_reason = ""
    after_assimilation_world_digest = before_world_digest
    after_dynamic_digest = previous_dynamic_digest if previous_dynamic_digest != "GENESIS" else ""
    dynamic_revision = int(world.get("world_dynamic_revision", 0) or 0) if world else 0
    post_seed_digest = ""
    child_runtime_root = str(child_root)
    projection_packet_digest = ""
    projection_activation_digest = ""
    v14_world_model_digest = ""
    assimilation_plan: dict[str, Any] = {}
    reentry_plan: dict[str, Any] = {}
    assimilation_record: dict[str, Any] = {}
    post_seed: dict[str, Any] = {}
    reentry_record: dict[str, Any] = {}

    if not blockers:
        assimilation_plan = build_assimilation_plan(
            plan=plan,
            cycle_state=cycle,
            seed_packet=seed,
            parent_world_digest=before_world_digest,
            previous_dynamic_digest=previous_dynamic_digest,
        )
        assimilation_license = dict(assimilation_template)
        assimilation_license["bound_assimilation_plan_digest"] = assimilation_plan[
            "assimilation_plan_digest"
        ]
        assimilation_invoked = True
        assimilation_result = build_indra_qi_process_tensor_world_assimilation_v0_6(
            runtime_context={
                "runtime_root": str(root),
                "indra_qi_process_tensor_world_assimilation_v0_6_enabled": True,
                "apply_indra_qi_process_tensor_world_assimilation_v0_6": True,
            },
            assimilation_plan=assimilation_plan,
            assimilation_license=assimilation_license,
        ).to_dict()
        if assimilation_result.get("status") != "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_READY":
            blockers.append("parent_cycle_reentry_v0_6_assimilation_not_ready")
            blockers.extend(
                f"nested_v0_6:{value}" for value in items(assimilation_result.get("blockers"))
            )
        else:
            assimilation_ready = True
            dynamic_revision = int(assimilation_result.get("dynamic_revision", 0) or 0)

    if assimilation_ready and not blockers:
        assimilated_world = _read_json(world_path)
        after_assimilation_world_digest = str(
            assimilated_world.get("indra_qi_world_state_digest", "")
        )
        after_dynamic_digest = str(
            assimilated_world.get("process_tensor_dynamic_world_state_digest", "")
        )
        if compute_indra_qi_world_state_digest(assimilated_world) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_assimilated_world_digest_invalid")
        if dynamic_world_state_digest(assimilated_world) != after_dynamic_digest:
            blockers.append("parent_cycle_reentry_assimilated_dynamic_digest_invalid")
        if after_assimilation_world_digest == before_world_digest:
            blockers.append("parent_cycle_reentry_v0_6_world_digest_not_changed")
        if protected_constitution_digest(assimilated_world) != before_constitution:
            blockers.append("parent_cycle_reentry_parent_constitution_changed")
        if overlay_history_digest(assimilated_world) != before_overlay_history:
            blockers.append("parent_cycle_reentry_overlay_history_changed")

        assimilation_record = _read_json(assimilation_record_path)
        post_seed = _read_json(assimilation_seed_path)
        assimilation_records = _records(assimilation_ledger_path)
        assimilation_ledger = _latest_matching(
            assimilation_records,
            "assimilation_id",
            assimilation_id,
        )
        if not valid_digest(assimilation_record, "assimilation_record_digest"):
            blockers.append("parent_cycle_reentry_v0_6_record_digest_invalid")
        if assimilation_record.get("assimilation_status") != "dynamic_world_state_assimilated":
            blockers.append("parent_cycle_reentry_v0_6_record_not_assimilated")
        if str(assimilation_record.get("after_world_state_digest", "")) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_v0_6_record_world_digest_mismatch")
        if str(assimilation_record.get("dynamic_world_state_digest", "")) != after_dynamic_digest:
            blockers.append("parent_cycle_reentry_v0_6_record_dynamic_digest_mismatch")
        if str(assimilation_record.get("source_cycle_state_digest", "")) != str(
            cycle.get("process_tensor_cycle_state_digest", "")
        ):
            blockers.append("parent_cycle_reentry_v0_6_record_cycle_digest_mismatch")
        if not valid_digest(post_seed, "post_assimilation_seed_packet_digest"):
            blockers.append("parent_cycle_reentry_v0_6_seed_digest_invalid")
        if str(post_seed.get("source_world_state_digest", "")) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_v0_6_seed_world_digest_mismatch")
        if str(post_seed.get("source_dynamic_world_state_digest", "")) != after_dynamic_digest:
            blockers.append("parent_cycle_reentry_v0_6_seed_dynamic_digest_mismatch")
        if not valid_digest(assimilation_ledger, "record_digest"):
            blockers.append("parent_cycle_reentry_v0_6_ledger_digest_invalid")
        if str(assimilation_ledger.get("source_assimilation_record_digest", "")) != str(
            assimilation_record.get("assimilation_record_digest", "")
        ):
            blockers.append("parent_cycle_reentry_v0_6_ledger_record_mismatch")
        post_seed_digest = str(post_seed.get("post_assimilation_seed_packet_digest", ""))

    if assimilation_ready and not blockers:
        reentry_plan = build_reentry_plan(
            plan=plan,
            assimilation_record=assimilation_record,
            post_assimilation_seed=post_seed,
            parent_world_digest=after_assimilation_world_digest,
        )
        reentry_license = dict(reentry_template)
        reentry_license["bound_reentry_plan_digest"] = reentry_plan["reentry_plan_digest"]
        reentry_invoked = True
        reentry_result = build_indra_qi_post_assimilation_causal_reentry_v0_7(
            runtime_context={
                "runtime_root": str(root),
                "indra_qi_post_assimilation_causal_reentry_v0_7_enabled": True,
                "invoke_indra_qi_post_assimilation_causal_reentry_v0_7": True,
            },
            reentry_plan=reentry_plan,
            reentry_license=reentry_license,
        ).to_dict()
        child_runtime_root = str(reentry_result.get("child_runtime_root", child_root))
        if reentry_result.get("status") != "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_READY":
            blockers.append("parent_cycle_reentry_v0_7_reentry_not_ready")
            blockers.extend(
                f"nested_v0_7:{value}" for value in items(reentry_result.get("blockers"))
            )
        else:
            reentry_ready = True
            projection_packet_digest = str(reentry_result.get("projection_packet_digest", ""))
            projection_activation_digest = str(
                reentry_result.get("projection_activation_digest", "")
            )
            v14_world_model_digest = str(reentry_result.get("v14_world_model_digest", ""))

    if reentry_ready and not blockers:
        parent_after_reentry = _read_json(world_path)
        if str(parent_after_reentry.get("indra_qi_world_state_digest", "")) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_parent_world_changed_during_v0_7")
        if compute_indra_qi_world_state_digest(parent_after_reentry) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_parent_world_after_v0_7_digest_invalid")

        child = pathlib.Path(child_runtime_root).resolve()
        try:
            child.relative_to(allowed_child_parent)
        except ValueError:
            blockers.append("parent_cycle_reentry_result_child_runtime_outside_allowed_root")
        if not child.is_dir():
            blockers.append("parent_cycle_reentry_child_runtime_missing_after_v0_7")
        child_world = _read_json(child / "ku_indra_qi_noncommutative_mandala_world_state.json")
        generated_plan = _read_json(child / "indra_qi_generated_causal_projection_plan_v0_7.json")
        projection_packet = _read_json(child / "indra_qi_causal_projection_packet_v0_2.json")
        projection_activation = _read_json(
            child / "indra_qi_causal_projection_activation_record_v0_2.json"
        )
        v14_state = _read_json(child / "kuuos_causal_world_model_state_v14_0.json")
        reentry_record = _read_json(reentry_record_path)
        reentry_records = _records(reentry_ledger_path)
        reentry_ledger = _latest_matching(reentry_records, "reentry_id", reentry_id)

        if str(child_world.get("indra_qi_world_state_digest", "")) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_child_world_digest_mismatch")
        if compute_indra_qi_world_state_digest(child_world) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_child_world_digest_invalid")
        if str(generated_plan.get("source_indra_qi_world_state_digest", "")) != after_assimilation_world_digest:
            blockers.append("parent_cycle_reentry_generated_projection_world_mismatch")
        if not valid_digest(projection_packet, "projection_packet_digest"):
            blockers.append("parent_cycle_reentry_projection_packet_digest_invalid")
        if not valid_digest(projection_activation, "activation_record_digest"):
            blockers.append("parent_cycle_reentry_projection_activation_digest_invalid")
        if not valid_v14_digest(v14_state, "world_model_digest"):
            blockers.append("parent_cycle_reentry_v14_world_model_digest_invalid")
        if str(v14_state.get("world_id", "")) != str(plan.get("causal_world_id", "")):
            blockers.append("parent_cycle_reentry_v14_world_id_mismatch")
        if not valid_digest(reentry_record, "reentry_record_digest"):
            blockers.append("parent_cycle_reentry_v0_7_record_digest_invalid")
        if reentry_record.get("reentry_status") != "post_assimilation_causal_world_initialized":
            blockers.append("parent_cycle_reentry_v0_7_record_not_initialized")
        if str(reentry_record.get("source_assimilation_record_digest", "")) != str(
            assimilation_record.get("assimilation_record_digest", "")
        ):
            blockers.append("parent_cycle_reentry_v0_7_record_assimilation_mismatch")
        if str(reentry_record.get("projection_packet_digest", "")) != str(
            projection_packet.get("projection_packet_digest", "")
        ):
            blockers.append("parent_cycle_reentry_v0_7_record_projection_mismatch")
        if not valid_digest(reentry_ledger, "record_digest"):
            blockers.append("parent_cycle_reentry_v0_7_ledger_digest_invalid")
        if str(reentry_ledger.get("source_reentry_record_digest", "")) != str(
            reentry_record.get("reentry_record_digest", "")
        ):
            blockers.append("parent_cycle_reentry_v0_7_ledger_record_mismatch")
        projection_packet_digest = str(projection_packet.get("projection_packet_digest", ""))
        projection_activation_digest = str(
            projection_activation.get("activation_record_digest", "")
        )
        v14_world_model_digest = str(v14_state.get("world_model_digest", ""))

    if blockers and transaction_snapshot:
        _restore_files(transaction_snapshot)
        if child_root.exists() and license_value.get("child_runtime_remove_on_failure_allowed") is True:
            shutil.rmtree(child_root)
        rolled_back = True
        rollback_reason = blockers[0]
        transaction_committed = False
        restored_world = _read_json(world_path)
        restored_world_digest = str(restored_world.get("indra_qi_world_state_digest", ""))
        restored_dynamic_digest = str(
            restored_world.get("process_tensor_dynamic_world_state_digest", "")
        ) or "GENESIS"
        if restored_world_digest != before_world_digest:
            blockers.append("parent_cycle_reentry_transaction_restore_world_digest_mismatch")
        if restored_dynamic_digest != previous_dynamic_digest:
            blockers.append("parent_cycle_reentry_transaction_restore_dynamic_digest_mismatch")
        if child_root.exists():
            blockers.append("parent_cycle_reentry_transaction_restore_child_runtime_remains")
        after_assimilation_world_digest = before_world_digest
        after_dynamic_digest = previous_dynamic_digest if previous_dynamic_digest != "GENESIS" else ""
        dynamic_revision = int(restored_world.get("world_dynamic_revision", 0) or 0)
        post_seed_digest = ""
        projection_packet_digest = ""
        projection_activation_digest = ""
        v14_world_model_digest = ""
        child_runtime_root = str(child_root)

    loop_status = (
        "parent_cycle_assimilated_and_causal_reentry_initialized"
        if reentry_ready and not blockers
        else "parent_cycle_assimilation_reentry_blocked"
    )
    transaction_committed = loop_status == "parent_cycle_assimilated_and_causal_reentry_initialized"

    loop_handoff_path = root / "indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json"
    loop_record_path = root / "indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json"
    receipt_path = root / "indra_qi_parent_cycle_assimilation_reentry_receipt_v0_11.json"
    audit_path = root / "indra_qi_parent_cycle_assimilation_reentry_audit_v0_11.jsonl"
    loop_handoff_digest = ""

    if transaction_committed:
        loop_handoff = {
            "version": "indra_qi_parent_cycle_assimilation_reentry_handoff_packet_v0_11",
            "loop_status": loop_status,
            "loop_id": loop_id,
            "source_v0_10_bridge_id": source_bridge_id,
            "source_v0_10_handoff_packet_digest": source_handoff_digest,
            "source_v0_10_bridge_record_digest": str(bridge_record.get("bridge_record_digest", "")),
            "source_v0_10_ledger_record_digest": str(bridge_ledger.get("record_digest", "")),
            "source_cycle_id": source_cycle_id,
            "source_cycle_state_digest": str(cycle.get("process_tensor_cycle_state_digest", "")),
            "source_cycle_seed_packet_digest": str(seed.get("next_cycle_seed_packet_digest", "")),
            "before_parent_world_state_digest": before_world_digest,
            "after_assimilation_world_state_digest": after_assimilation_world_digest,
            "previous_dynamic_world_state_digest": previous_dynamic_digest,
            "dynamic_world_state_digest": after_dynamic_digest,
            "assimilation_plan_digest": str(assimilation_plan.get("assimilation_plan_digest", "")),
            "assimilation_record_digest": str(assimilation_record.get("assimilation_record_digest", "")),
            "post_assimilation_seed_packet_digest": post_seed_digest,
            "reentry_plan_digest": str(reentry_plan.get("reentry_plan_digest", "")),
            "reentry_id": reentry_id,
            "reentry_record_digest": str(reentry_record.get("reentry_record_digest", "")),
            "child_runtime_root": child_runtime_root,
            "projection_packet_digest": projection_packet_digest,
            "projection_activation_digest": projection_activation_digest,
            "v14_world_model_digest": v14_world_model_digest,
            "boundary": {
                **REQUIRED_BOUNDARY,
                "v0_6_assimilation_completed": True,
                "v0_7_reentry_completed": True,
                "parent_world_dynamic_update_traceable": True,
                "new_child_causal_world_traceable": True,
                "transaction_committed": True,
            },
            "epoch": int(time.time()),
        }
        loop_handoff["loop_handoff_packet_digest"] = sha(loop_handoff)
        loop_handoff_digest = str(loop_handoff["loop_handoff_packet_digest"])
        _write_json(loop_handoff_path, loop_handoff)

        loop_record = {
            "version": "indra_qi_parent_cycle_assimilation_reentry_record_v0_11",
            "loop_status": loop_status,
            "loop_id": loop_id,
            "source_v0_10_handoff_packet_digest": source_handoff_digest,
            "source_loop_handoff_packet_digest": loop_handoff_digest,
            "after_assimilation_world_state_digest": after_assimilation_world_digest,
            "dynamic_world_state_digest": after_dynamic_digest,
            "assimilation_record_digest": str(assimilation_record.get("assimilation_record_digest", "")),
            "reentry_record_digest": str(reentry_record.get("reentry_record_digest", "")),
            "child_runtime_root": child_runtime_root,
            "v14_world_model_digest": v14_world_model_digest,
            "transaction_rolled_back": False,
            "boundary": {
                "append_only_loop_record": True,
                "world_assimilation_delegated_to_v0_6": True,
                "causal_reentry_delegated_to_v0_7": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        loop_record["loop_record_digest"] = sha(loop_record)
        _write_json(loop_record_path, loop_record)

        loop_ledger = {
            "version": "indra_qi_parent_cycle_assimilation_reentry_ledger_record_v0_11",
            "record_type": "parent_cycle_assimilation_causal_reentry",
            "loop_id": loop_id,
            "source_v0_10_bridge_id": source_bridge_id,
            "source_v0_10_handoff_packet_digest": source_handoff_digest,
            "source_loop_handoff_packet_digest": loop_handoff_digest,
            "source_loop_record_digest": loop_record["loop_record_digest"],
            "assimilation_record_digest": str(assimilation_record.get("assimilation_record_digest", "")),
            "reentry_record_digest": str(reentry_record.get("reentry_record_digest", "")),
            "after_assimilation_world_state_digest": after_assimilation_world_digest,
            "dynamic_world_state_digest": after_dynamic_digest,
            "child_runtime_root": child_runtime_root,
            "v14_world_model_digest": v14_world_model_digest,
            "prev_record_digest": str(prior_loop_records[-1].get("record_digest", "GENESIS"))
            if prior_loop_records
            else "GENESIS",
            "boundary": {
                "append_only_loop_lineage": True,
                "source_v0_10_handoff_consumed_once": True,
                "v0_6_and_v0_7_completed": True,
                "new_child_runtime_created_once": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        loop_ledger["record_digest"] = sha(loop_ledger)
        _append_jsonl(loop_ledger_path, loop_ledger)

    status = READY if transaction_committed else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-parent-cycle-reentry-"
        + sha(
            {
                "loop_id": loop_id,
                "source_handoff": source_handoff_digest,
                "assimilation": str(assimilation_record.get("assimilation_record_digest", "")),
                "reentry": str(reentry_record.get("reentry_record_digest", "")),
                "blockers": blockers,
            }
        )[:16],
        "loop_id": loop_id,
        "source_v0_10_bridge_id": source_bridge_id,
        "source_cycle_id": source_cycle_id,
        "loop_status": loop_status,
        "v0_6_assimilation_invoked": assimilation_invoked,
        "v0_6_assimilation_ready": assimilation_ready,
        "v0_7_reentry_invoked": reentry_invoked,
        "v0_7_reentry_ready": reentry_ready,
        "transaction_committed": transaction_committed,
        "transaction_rolled_back": rolled_back,
        "rollback_reason": rollback_reason,
        "before_parent_world_state_digest": before_world_digest,
        "after_assimilation_world_state_digest": after_assimilation_world_digest,
        "previous_dynamic_world_state_digest": previous_dynamic_digest,
        "dynamic_world_state_digest": after_dynamic_digest,
        "dynamic_revision": dynamic_revision,
        "post_assimilation_seed_packet_digest": post_seed_digest,
        "reentry_id": reentry_id,
        "child_runtime_root": child_runtime_root,
        "projection_packet_digest": projection_packet_digest,
        "projection_activation_digest": projection_activation_digest,
        "v14_world_model_digest": v14_world_model_digest,
        "loop_handoff_packet_digest": loop_handoff_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "loop_completed": transaction_committed,
            "rollback_completed_on_failure": rolled_back,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": sha(receipt)})

    return IndraQiParentCycleAssimilationReentryV0_11Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        loop_id,
        source_bridge_id,
        source_cycle_id,
        loop_status,
        assimilation_invoked,
        assimilation_ready,
        reentry_invoked,
        reentry_ready,
        transaction_committed,
        rolled_back,
        rollback_reason,
        before_world_digest,
        after_assimilation_world_digest,
        previous_dynamic_digest,
        after_dynamic_digest,
        dynamic_revision,
        post_seed_digest,
        reentry_id,
        child_runtime_root,
        projection_packet_digest,
        projection_activation_digest,
        v14_world_model_digest,
        loop_handoff_digest,
        str(loop_handoff_path),
        str(loop_record_path),
        str(loop_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
