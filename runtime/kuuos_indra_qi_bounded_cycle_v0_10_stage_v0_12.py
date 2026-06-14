#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import mapping, valid_digest
from runtime.kuuos_indra_qi_bounded_cycle_plans_v0_12 import (
    approved_feedback_candidate_ids,
    build_bridge_plan,
)
from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import (
    latest_matching,
    read_json,
    records,
)
from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import cycle_state_digest
from runtime.kuuos_runtime_daemon_qi_child_feedback_parent_cycle_v0_10 import (
    build_indra_qi_child_feedback_parent_cycle_v0_10,
)


def _nested(result: Mapping[str, Any]) -> list[str]:
    raw = result.get("blockers", [])
    return [f"nested_v0_10:{value}" for value in raw if isinstance(value, str)]


def run_v0_10_stage(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    license_value: Mapping[str, Any],
    source_reentry: Mapping[str, Any],
    child_output: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    output: dict[str, Any] = {
        "v0_10_invoked": False,
        "v0_10_ready": False,
        "process_tensor_cycle_state_digest": "",
        "bridge_handoff": {},
        "bridge_record": {},
        "bridge_ledger": {},
        "cycle_state": {},
        "cycle_seed": {},
    }
    if blockers:
        return output

    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    previous = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
    previous_digest = (
        str(previous.get("process_tensor_cycle_state_digest", ""))
        if previous
        else "GENESIS"
    )
    if previous and cycle_state_digest(previous) != previous_digest:
        blockers.append("bounded_cycle_previous_cycle_digest_invalid")
        return output

    feedback = mapping(child_output.get("feedback"))
    approved_ids = approved_feedback_candidate_ids(feedback, blockers)
    bridge_plan = build_bridge_plan(
        plan=plan,
        world=world,
        reentry=source_reentry,
        execution=mapping(child_output.get("execution_record")),
        execution_ledger=mapping(child_output.get("execution_ledger")),
        feedback=feedback,
        feedback_handoff=mapping(child_output.get("feedback_handoff")),
        previous_cycle_digest=previous_digest,
        approved_ids=approved_ids,
    )
    if blockers:
        return output

    bridge_license = dict(mapping(license_value.get("v0_10_license_template")))
    bridge_license["bound_bridge_plan_digest"] = bridge_plan["bridge_plan_digest"]
    output["v0_10_invoked"] = True
    result = build_indra_qi_child_feedback_parent_cycle_v0_10(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_child_feedback_parent_cycle_v0_10_enabled": True,
            "apply_indra_qi_child_feedback_parent_cycle_v0_10": True,
        },
        bridge_plan=bridge_plan,
        bridge_license=bridge_license,
    ).to_dict()
    if result.get("status") != "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_READY":
        blockers.append("bounded_cycle_v0_10_not_ready")
        blockers.extend(_nested(result))
        return output

    output["v0_10_ready"] = True
    handoff = read_json(root / "indra_qi_child_feedback_parent_cycle_handoff_v0_10.json")
    record = read_json(root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json")
    ledger = latest_matching(
        records(root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl"),
        "bridge_id",
        str(plan.get("parent_bridge_id", "")),
    )
    cycle = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
    seed = read_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json")
    output.update(
        {
            "bridge_handoff": handoff,
            "bridge_record": record,
            "bridge_ledger": ledger,
            "cycle_state": cycle,
            "cycle_seed": seed,
        }
    )
    if not valid_digest(handoff, "handoff_packet_digest"):
        blockers.append("bounded_cycle_v0_10_handoff_digest_invalid")
    if not valid_digest(record, "bridge_record_digest"):
        blockers.append("bounded_cycle_v0_10_record_digest_invalid")
    if not valid_digest(ledger, "record_digest"):
        blockers.append("bounded_cycle_v0_10_ledger_digest_invalid")
    if cycle_state_digest(cycle) != str(
        cycle.get("process_tensor_cycle_state_digest", "")
    ):
        blockers.append("bounded_cycle_v0_10_cycle_digest_invalid")
    if not valid_digest(seed, "next_cycle_seed_packet_digest"):
        blockers.append("bounded_cycle_v0_10_seed_digest_invalid")
    output["process_tensor_cycle_state_digest"] = str(
        cycle.get("process_tensor_cycle_state_digest", "")
    )
    return output
