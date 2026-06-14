#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import mapping, valid_digest
from runtime.kuuos_indra_qi_bounded_cycle_plans_v0_12 import (
    build_action_plan,
    build_execution_plan,
    select_candidate,
)
from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import (
    latest_matching,
    read_json,
    records,
)
from runtime.kuuos_runtime_daemon_qi_approved_action_execution_v0_9 import (
    build_indra_qi_approved_recovery_action_execution_v0_9,
)
from runtime.kuuos_runtime_daemon_qi_recoverability_action_envelope_v0_8 import (
    build_indra_qi_recoverability_action_envelope_v0_8,
)


def _nested(prefix: str, result: Mapping[str, Any]) -> list[str]:
    raw = result.get("blockers", [])
    return [f"{prefix}:{value}" for value in raw if isinstance(value, str)]


def run_child_stages(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    license_value: Mapping[str, Any],
    world: Mapping[str, Any],
    reentry: Mapping[str, Any],
    causal: Mapping[str, Any],
    child: pathlib.Path,
    blockers: list[str],
) -> dict[str, Any]:
    output: dict[str, Any] = {
        "v0_8_invoked": False,
        "v0_8_ready": False,
        "v0_9_invoked": False,
        "v0_9_ready": False,
        "selected_candidate_id": "",
        "action_envelope_digest": "",
        "execution_record_digest": "",
        "feedback_packet_digest": "",
        "envelope": {},
        "activation": {},
        "execution_record": {},
        "execution_ledger": {},
        "feedback": {},
        "feedback_handoff": {},
    }
    if blockers:
        return output

    action_plan = build_action_plan(plan, world, reentry)
    action_license = dict(mapping(license_value.get("v0_8_license_template")))
    action_license["bound_action_plan_digest"] = action_plan["action_plan_digest"]
    output["v0_8_invoked"] = True
    result = build_indra_qi_recoverability_action_envelope_v0_8(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_recoverability_action_envelope_v0_8_enabled": True,
            "build_indra_qi_recoverability_action_envelope_v0_8": True,
        },
        action_plan=action_plan,
        action_license=action_license,
    ).to_dict()
    if result.get("status") != "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_READY":
        blockers.append("bounded_cycle_v0_8_not_ready")
        blockers.extend(_nested("nested_v0_8", result))
        return output

    output["v0_8_ready"] = True
    envelope = read_json(root / "indra_qi_recoverability_action_envelope_v0_8.json")
    activation = read_json(
        root / "indra_qi_recoverability_action_envelope_record_v0_8.json"
    )
    output["envelope"] = envelope
    output["activation"] = activation
    if not valid_digest(envelope, "action_envelope_digest"):
        blockers.append("bounded_cycle_v0_8_envelope_digest_invalid")
    if not valid_digest(activation, "activation_record_digest"):
        blockers.append("bounded_cycle_v0_8_record_digest_invalid")
    candidate = select_candidate(
        envelope,
        str(plan.get("selected_action_kind", "")),
        blockers,
    )
    output["selected_candidate_id"] = str(candidate.get("candidate_id", ""))
    output["action_envelope_digest"] = str(
        envelope.get("action_envelope_digest", "")
    )
    if blockers:
        return output

    execution_plan = build_execution_plan(
        plan=plan,
        world=world,
        reentry=reentry,
        causal=causal,
        envelope=envelope,
        activation=activation,
        candidate=candidate,
    )
    execution_license = dict(mapping(license_value.get("v0_9_license_template")))
    execution_license["bound_execution_plan_digest"] = execution_plan[
        "execution_plan_digest"
    ]
    output["v0_9_invoked"] = True
    result = build_indra_qi_approved_recovery_action_execution_v0_9(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_approved_recovery_action_execution_v0_9_enabled": True,
            "execute_indra_qi_approved_recovery_action_v0_9": True,
        },
        execution_plan=execution_plan,
        execution_license=execution_license,
    ).to_dict()
    if result.get("status") != "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_READY":
        blockers.append("bounded_cycle_v0_9_not_ready")
        blockers.extend(_nested("nested_v0_9", result))
        return output

    output["v0_9_ready"] = True
    execution_record = read_json(
        root / "indra_qi_approved_recovery_action_execution_record_v0_9.json"
    )
    execution_ledger = latest_matching(
        records(
            root / "indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl"
        ),
        "execution_id",
        str(plan.get("execution_id", "")),
    )
    feedback = read_json(child / "indra_qi_causal_feedback_candidate_packet_v0_3.json")
    feedback_handoff = read_json(
        child / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    )
    output.update(
        {
            "execution_record": execution_record,
            "execution_ledger": execution_ledger,
            "feedback": feedback,
            "feedback_handoff": feedback_handoff,
        }
    )
    if not valid_digest(execution_record, "execution_record_digest"):
        blockers.append("bounded_cycle_v0_9_record_digest_invalid")
    if not valid_digest(execution_ledger, "record_digest"):
        blockers.append("bounded_cycle_v0_9_ledger_digest_invalid")
    if not valid_digest(feedback, "feedback_packet_digest"):
        blockers.append("bounded_cycle_v0_9_feedback_digest_invalid")
    if not valid_digest(feedback_handoff, "approval_handoff_digest"):
        blockers.append("bounded_cycle_v0_9_feedback_handoff_digest_invalid")
    output["execution_record_digest"] = str(
        execution_record.get("execution_record_digest", "")
    )
    output["feedback_packet_digest"] = str(
        feedback.get("feedback_packet_digest", "")
    )
    return output
