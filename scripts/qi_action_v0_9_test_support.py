#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_approved_action_core_v0_9 import (
    APPROVAL_BOUNDARY,
    APPROVAL_VERSION,
    EVIDENCE_BOUNDARY,
    EVIDENCE_VERSION,
    REQUIRED_BOUNDARY,
    SELECTABLE_ACTION_KINDS,
    approval_digest,
    evidence_digest,
    execution_plan_digest,
)
from runtime.kuuos_indra_qi_feedback_core_v0_3 import ALLOWED_FEEDBACK_KINDS
from runtime.kuuos_runtime_daemon_qi_approved_action_execution_v0_9 import (
    build_indra_qi_approved_recovery_action_execution_v0_9,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import read_json
from scripts.qi_recovery_action_v0_8_test_support import (
    build_plan as envelope_plan,
    prepare_reentry,
    run_action as build_envelope,
)


def prepare_envelope(
    root: pathlib.Path,
    suffix: str,
    mode: str,
) -> tuple[dict[str, Any], dict[str, Any], pathlib.Path, dict[str, Any], dict[str, Any]]:
    world, _, reentry, child, _, causal = prepare_reentry(root, f"execute-{suffix}")
    plan = envelope_plan(world, reentry, suffix=f"execute-{suffix}")
    policy = plan["gate_policy"]
    if mode == "bounded":
        policy.update(
            {
                "observe_only_risk_threshold": 1.0,
                "counterfactual_first_risk_threshold": 1.0,
                "minimum_intervention_recoverability": 0.0,
                "maximum_intervention_debt": 1.0,
                "minimum_intervention_corridor_openness": 0.0,
            }
        )
    elif mode == "counterfactual":
        policy.update(
            {
                "observe_only_risk_threshold": 1.0,
                "counterfactual_first_risk_threshold": 0.0,
                "minimum_intervention_recoverability": 0.0,
                "maximum_intervention_debt": 1.0,
                "minimum_intervention_corridor_openness": 0.0,
            }
        )
    elif mode == "observe":
        policy.update(
            {
                "observe_only_risk_threshold": 0.0,
                "counterfactual_first_risk_threshold": 0.0,
            }
        )
    else:
        raise AssertionError(f"unknown mode: {mode}")
    from runtime.kuuos_indra_qi_recovery_action_core_v0_8 import action_plan_digest

    plan["action_plan_digest"] = action_plan_digest(plan)
    result = build_envelope(root, plan)
    assert result["status"] == "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_READY", result
    envelope = read_json(root / "indra_qi_recoverability_action_envelope_v0_8.json")
    activation = read_json(
        root / "indra_qi_recoverability_action_envelope_record_v0_8.json"
    )
    return world, reentry, child, causal, {
        "envelope": envelope,
        "activation": activation,
    }


def candidate_from(envelope: dict[str, Any], kind: str) -> dict[str, Any]:
    field = {
        "observation_request": "observation_requests",
        "counterfactual_candidate": "counterfactual_candidates",
        "bounded_intervention_candidate": "bounded_intervention_candidates",
    }[kind]
    values = envelope[field]
    assert values, (field, envelope)
    if kind == "observation_request":
        local = [
            value
            for value in values
            if value["candidate_payload"]["binding"]["binding_kind"]
            == "local_patch_observable"
        ]
        return local[0] if local else values[0]
    return values[0]


def build_execution_plan(
    *,
    world: dict[str, Any],
    reentry: dict[str, Any],
    causal: dict[str, Any],
    envelope: dict[str, Any],
    activation: dict[str, Any],
    kind: str,
    suffix: str,
) -> dict[str, Any]:
    candidate = candidate_from(envelope, kind)
    variable_name = candidate["source_causal_variable"]
    current = causal["variables"][variable_name]
    current_value = float(current["value"])
    if kind == "observation_request":
        approved_value = current_value
    elif kind == "counterfactual_candidate":
        interval = candidate["candidate_payload"]["candidate_value_interval"]
        approved_value = round((float(interval[0]) + float(interval[1])) / 2.0, 8)
        if approved_value == current_value:
            approved_value = float(interval[1])
    else:
        delta = float(candidate["candidate_payload"]["maximum_delta"])
        approved_value = round(current_value + delta / 2.0, 8)

    evidence = {
        "version": EVIDENCE_VERSION,
        "evidence_id": f"fresh-evidence-{suffix}",
        "variable_name": variable_name,
        "observed_value": current_value,
        "observed_uncertainty": float(current.get("uncertainty", 0.0)),
        "source_v14_world_model_digest": causal["world_model_digest"],
        "source_action_envelope_digest": envelope["action_envelope_digest"],
        "instrument_trace_digest": f"instrument-trace-{suffix}",
        "boundary": dict(EVIDENCE_BOUNDARY),
    }
    evidence["evidence_digest"] = evidence_digest(evidence)
    approval = {
        "version": APPROVAL_VERSION,
        "approval_id": f"approval-{suffix}",
        "approved_candidate_id": candidate["candidate_id"],
        "approved_candidate_digest": candidate["action_candidate_digest"],
        "approved_action_kind": kind,
        "approved_transaction_id": f"action-{suffix}",
        "source_action_envelope_digest": envelope["action_envelope_digest"],
        "source_evidence_digest": evidence["evidence_digest"],
        "approval_scope": "single_candidate_single_transaction",
        "boundary": dict(APPROVAL_BOUNDARY),
    }
    approval["approval_digest"] = approval_digest(approval)
    plan = {
        "version": "indra_qi_approved_recovery_action_plan_v0_9",
        "execution_id": f"approved-action-execution-{suffix}",
        "source_action_envelope_id": envelope["action_envelope_id"],
        "source_action_envelope_digest": envelope["action_envelope_digest"],
        "source_action_activation_record_digest": activation[
            "activation_record_digest"
        ],
        "source_reentry_id": reentry["reentry_id"],
        "source_reentry_record_digest": reentry["reentry_record_digest"],
        "source_world_state_digest": world["indra_qi_world_state_digest"],
        "source_dynamic_world_state_digest": world[
            "process_tensor_dynamic_world_state_digest"
        ],
        "source_v14_world_model_digest": causal["world_model_digest"],
        "selected_candidate_id": candidate["candidate_id"],
        "selected_candidate_digest": candidate["action_candidate_digest"],
        "selected_action_kind": kind,
        "action_transaction_id": f"action-{suffix}",
        "undo_transaction_id": f"undo-action-{suffix}",
        "feedback_id": f"feedback-after-action-{suffix}",
        "approved_value": approved_value,
        "approved_uncertainty": float(current.get("uncertainty", 0.0)),
        "fresh_observation_evidence": evidence,
        "approval": approval,
        "feedback_policy": {
            "event_kind_base_weight": {
                "observe": 0.9,
                "intervene": 0.75,
                "counterfactual": 0.45,
                "undo": 0.65,
            },
            "uncertainty_penalty": 0.5,
            "minimum_candidate_weight": 0.1,
            "maximum_candidate_weight": 0.95,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    plan["execution_plan_digest"] = execution_plan_digest(plan)
    return plan


def v14_action_template(
    variables: list[str], command_kind: str, **overrides: Any
) -> dict[str, Any]:
    value = {
        "license_status": "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY",
        "allowed_command_kinds": [command_kind],
        "allowed_variables": list(variables),
        "protected_variables": [],
        "state_read_allowed": True,
        "event_ledger_append_allowed": True,
        "result_write_allowed": True,
        "audit_append_allowed": True,
        "state_write_allowed": command_kind != "counterfactual",
        "snapshot_write_allowed": command_kind in {"observe", "intervene"},
        "direct_world_model_mutation_allowed": command_kind in {"observe", "intervene"},
        "observation_update_allowed": command_kind == "observe",
        "intervention_allowed": command_kind == "intervene",
        "counterfactual_allowed": command_kind == "counterfactual",
    }
    value.update(overrides)
    return value


def v14_undo_template(variables: list[str], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY",
        "allowed_command_kinds": ["undo"],
        "allowed_variables": list(variables),
        "protected_variables": [],
        "state_read_allowed": True,
        "event_ledger_append_allowed": True,
        "result_write_allowed": True,
        "audit_append_allowed": True,
        "undo_allowed": True,
        "state_write_allowed": True,
        "snapshot_read_allowed": True,
        "snapshot_write_allowed": True,
        "direct_world_model_mutation_allowed": True,
    }
    value.update(overrides)
    return value


def feedback_template(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_LICENSE_READY",
        "source_indra_state_read_allowed": True,
        "source_projection_read_allowed": True,
        "source_causal_state_read_allowed": True,
        "source_causal_event_read_allowed": True,
        "source_causal_result_read_allowed": True,
        "feedback_plan_validate_allowed": True,
        "feedback_packet_write_allowed": True,
        "approval_handoff_write_allowed": True,
        "feedback_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allowed_feedback_kinds": sorted(ALLOWED_FEEDBACK_KINDS),
    }
    value.update(overrides)
    return value


def execution_license(
    plan: dict[str, Any], causal: dict[str, Any], **overrides: Any
) -> dict[str, Any]:
    command_kind = {
        "observation_request": "observe",
        "counterfactual_candidate": "counterfactual",
        "bounded_intervention_candidate": "intervene",
    }[plan["selected_action_kind"]]
    variables = list(causal["variables"])
    value = {
        "license_status": "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_LICENSE_READY",
        "bound_execution_plan_digest": plan["execution_plan_digest"],
        "allowed_action_kinds": sorted(SELECTABLE_ACTION_KINDS),
        "world_state_read_allowed": True,
        "assimilation_lineage_read_allowed": True,
        "reentry_lineage_read_allowed": True,
        "action_envelope_lineage_read_allowed": True,
        "child_runtime_read_allowed": True,
        "execution_plan_validate_allowed": True,
        "v14_action_invoke_allowed": True,
        "v0_3_feedback_invoke_allowed": True,
        "execution_record_write_allowed": True,
        "execution_ledger_append_allowed": True,
        "undo_readiness_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v14_action_license_template": v14_action_template(
            variables, command_kind
        ),
        "v14_undo_license_template": v14_undo_template(variables),
        "v0_3_feedback_license_template": feedback_template(),
    }
    value.update(overrides)
    return value


def run_execution(
    root: pathlib.Path,
    plan: dict[str, Any],
    causal: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_approved_recovery_action_execution_v0_9(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_approved_recovery_action_execution_v0_9_enabled": True,
            "execute_indra_qi_approved_recovery_action_v0_9": True,
        },
        execution_plan=plan,
        execution_license=license_value or execution_license(plan, causal),
    ).to_dict()
