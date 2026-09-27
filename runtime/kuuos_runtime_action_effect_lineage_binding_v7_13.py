#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_transactional_effect_reconciliation_kernel_v0_24 import (
    validate_transaction_state,
)

VERSION = "kuuos_runtime_action_effect_lineage_binding_v7_13"
PLAN_VERSION = "kuuos_action_effect_lineage_binding_plan_v7_13"
INPUT_VERSION = "kuuos_action_effect_lineage_bindings_input_v7_13"
SOURCE_VERSION = "kuuos_runtime_middle_way_action_lifting_v7_12"

READY = "KUUOS_ACTION_EFFECT_LINEAGE_BINDING_READY"
PARTIAL = "KUUOS_ACTION_EFFECT_LINEAGE_BINDING_PARTIAL"
OBSTRUCTED = "KUUOS_ACTION_EFFECT_LINEAGE_BINDING_OBSTRUCTED"
BLOCKED = "KUUOS_ACTION_EFFECT_LINEAGE_BINDING_BLOCKED"

AUTHORIZED_PREPARED = "authorized_prepared"
TRANSACTION_IN_PROGRESS = "transaction_in_progress"
EFFECT_CONFIRMED = "effect_confirmed"
REOBSERVATION_REQUIRED = "reobservation_required"
COMPENSATION_PROPOSED = "compensation_proposed"
HANDOVER_REQUIRED = "handover_required"
NO_EFFECT_RECORDED = "no_effect_recorded"
AWAITING_LOWER_AUTHORITY = "awaiting_lower_authority"
AWAITING_WORLD_RESOLUTION = "awaiting_world_resolution"
PROPOSAL_ONLY = "proposal_only"
BINDING_OBSTRUCTED = "binding_obstructed"

EXECUTION_ROUTES = {
    "licensed_execution_candidate_exact_world",
    "licensed_execution_candidate_transferred_world",
    "licensed_execution_candidate_world_independent",
    "execution_eligible_not_requested",
    "bounded_probe_candidate",
}
AUTHORITY_PENDING_ROUTES = {
    "fresh_authority_required",
    "authority_renewal_or_replan_required",
}
WORLD_PENDING_ROUTES = {"world_transfer_or_reconciliation_required"}
PROPOSAL_ROUTES = {
    "advisory_or_plan_candidate",
    "evidence_required",
    "review_required",
    "review_or_replan_required",
}
PROHIBITED_ROUTE = "explicitly_prohibited"

TRANSACTION_OUTCOME_MAP = {
    "EFFECT_CONFIRMED": EFFECT_CONFIRMED,
    "REOBSERVATION_REQUIRED": REOBSERVATION_REQUIRED,
    "COMPENSATION_PROPOSED": COMPENSATION_PROPOSED,
    "HANDOVER_REQUIRED": HANDOVER_REQUIRED,
    "NO_EFFECT_RECORDED": NO_EFFECT_RECORDED,
}


@dataclass(frozen=True)
class ActionEffectLineageBindingResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    binding_count: int
    authorized_prepared_count: int
    transaction_in_progress_count: int
    effect_confirmed_count: int
    reobservation_required_count: int
    compensation_proposed_count: int
    handover_required_count: int
    no_effect_recorded_count: int
    awaiting_count: int
    proposal_only_count: int
    obstructed_count: int
    output_path: str
    receipt_path: str
    audit_path: str
    output_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(dict(value), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(value), ensure_ascii=False, sort_keys=True) + "\n")


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("semantic_route_is_execution_authority") is not False:
        blockers.append("semantic_route_execution_authority_must_be_false")
    if plan.get("binding_layer_executes_effect") is not False:
        blockers.append("binding_layer_executes_effect_must_be_false")
    if plan.get("lower_authority_can_resolve_prior_authority_pending") is not True:
        blockers.append("lower_authority_resolution_not_true")
    if plan.get("new_world_witness_can_resolve_prior_world_pending") is not True:
        blockers.append("world_witness_resolution_not_true")
    if plan.get("transaction_outcome_may_refine_action_status") is not True:
        blockers.append("transaction_outcome_refinement_not_true")
    if plan.get("execution_success_implies_mission_success") is not False:
        blockers.append("execution_success_mission_success_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")


def _source_actions(
    source: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = source.get("action_assessments", [])
    if not isinstance(raw, list):
        blockers.append("source_action_assessments_not_list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"source_action_{index}_not_object")
            continue
        action_id = str(item.get("action_id", "")).strip()
        if not action_id:
            blockers.append(f"source_action_{index}_id_missing")
            continue
        if action_id in result:
            blockers.append("duplicate_source_action_id")
            continue
        result[action_id] = dict(item)
    return result


def _validated_prepared_act(
    raw: Any,
    errors: list[str],
) -> dict[str, Any]:
    if raw in (None, {}):
        return {}
    if not isinstance(raw, Mapping):
        errors.append("prepared_act_state_not_object")
        return {}
    state = dict(raw)
    act_errors = validate_act_state(state)
    if act_errors:
        errors.extend("prepared_act:" + item for item in act_errors)
        return state
    if state.get("current_phase") != "project":
        errors.append("prepared_act_not_project_phase")
    if state.get("route") != "PENDING":
        errors.append("prepared_act_not_pending")
    for field in (
        "act_state_digest",
        "step_authorization_digest",
        "host_license_digest",
        "host_projection_digest",
        "operation_id",
        "operation_input_digest",
    ):
        if not str(state.get(field, "")).strip():
            errors.append("prepared_act_" + field + "_missing")
    return state


def _validated_transaction(
    raw: Any,
    errors: list[str],
) -> dict[str, Any]:
    if raw in (None, {}):
        return {}
    if not isinstance(raw, Mapping):
        errors.append("transaction_state_not_object")
        return {}
    state = dict(raw)
    tx_errors = validate_transaction_state(state)
    if tx_errors:
        errors.extend("transaction:" + item for item in tx_errors)
    return state


def _lower_fields(
    prepared_act: Mapping[str, Any],
    transaction: Mapping[str, Any],
) -> dict[str, str]:
    if transaction:
        intent = _m(transaction.get("transaction_intent"))
        return {
            "act_id": str(intent.get("source_act_id", "")),
            "prepared_act_state_digest": str(
                intent.get("source_prepared_act_state_digest", "")
            ),
            "operation_id": str(intent.get("operation_id", "")),
            "operation_input_digest": str(intent.get("operation_input_digest", "")),
            "intended_effect_digest": str(intent.get("intended_effect_digest", "")),
            "step_authorization_digest": str(
                intent.get("step_authorization_digest", "")
            ),
            "capability_lease_digest": str(
                intent.get("capability_lease_digest", "")
            ),
            "host_projection_digest": str(intent.get("host_projection_digest", "")),
            "transaction_intent_digest": str(
                transaction.get("transaction_intent_digest", "")
            ),
            "transaction_state_digest": str(
                transaction.get("transaction_state_digest", "")
            ),
            "transaction_final_receipt_digest": str(
                transaction.get("transaction_final_receipt_digest", "")
            ),
        }
    if prepared_act:
        return {
            "act_id": str(prepared_act.get("act_id", "")),
            "prepared_act_state_digest": str(prepared_act.get("act_state_digest", "")),
            "operation_id": str(prepared_act.get("operation_id", "")),
            "operation_input_digest": str(
                prepared_act.get("operation_input_digest", "")
            ),
            "intended_effect_digest": "",
            "step_authorization_digest": str(
                prepared_act.get("step_authorization_digest", "")
            ),
            "capability_lease_digest": str(
                prepared_act.get("host_license_digest", "")
            ),
            "host_projection_digest": str(
                prepared_act.get("host_projection_digest", "")
            ),
            "transaction_intent_digest": "",
            "transaction_state_digest": "",
            "transaction_final_receipt_digest": "",
        }
    return {
        "act_id": "",
        "prepared_act_state_digest": "",
        "operation_id": "",
        "operation_input_digest": "",
        "intended_effect_digest": "",
        "step_authorization_digest": "",
        "capability_lease_digest": "",
        "host_projection_digest": "",
        "transaction_intent_digest": "",
        "transaction_state_digest": "",
        "transaction_final_receipt_digest": "",
    }


def _check_exact_binding(
    *,
    action: Mapping[str, Any],
    binding: Mapping[str, Any],
    prepared_act: Mapping[str, Any],
    transaction: Mapping[str, Any],
    errors: list[str],
) -> dict[str, str]:
    lower = _lower_fields(prepared_act, transaction)

    expected_action_digest = str(binding.get("expected_action_digest", "")).strip()
    if expected_action_digest != str(action.get("action_digest", "")):
        errors.append("action_digest_mismatch")

    mapped_operation_id = str(binding.get("mapped_operation_id", "")).strip()
    mapped_input_digest = str(
        binding.get("mapped_operation_input_digest", "")
    ).strip()
    intended_effect_digest = str(binding.get("intended_effect_digest", "")).strip()

    if not mapped_operation_id:
        errors.append("mapped_operation_id_missing")
    if not mapped_input_digest:
        errors.append("mapped_operation_input_digest_missing")
    if lower["operation_id"] and lower["operation_id"] != mapped_operation_id:
        errors.append("operation_id_mismatch")
    if (
        lower["operation_input_digest"]
        and lower["operation_input_digest"] != mapped_input_digest
    ):
        errors.append("operation_input_digest_mismatch")
    if transaction:
        if not intended_effect_digest:
            errors.append("intended_effect_digest_missing")
        elif lower["intended_effect_digest"] != intended_effect_digest:
            errors.append("intended_effect_digest_mismatch")

    if prepared_act and transaction:
        if (
            lower["prepared_act_state_digest"]
            != str(prepared_act.get("act_state_digest", ""))
        ):
            errors.append("transaction_prepared_act_state_digest_mismatch")
        intent = _m(transaction.get("transaction_intent"))
        for intent_field, act_field in (
            ("step_authorization_digest", "step_authorization_digest"),
            ("capability_lease_digest", "host_license_digest"),
            ("host_projection_digest", "host_projection_digest"),
        ):
            if str(intent.get(intent_field, "")) != str(prepared_act.get(act_field, "")):
                errors.append("transaction_" + intent_field + "_mismatch")

    world_dependence = str(action.get("world_dependence", ""))
    target_world_id = str(action.get("target_samvrti_world_id", ""))
    world_binding_evidence_digest = str(
        binding.get("world_binding_evidence_digest", "")
    ).strip()
    world_transfer_resolution_digest = str(
        binding.get("world_transfer_resolution_digest", "")
    ).strip()

    if world_dependence != "none" and not world_binding_evidence_digest:
        errors.append("world_binding_evidence_digest_missing")

    semantic_effect_binding_digest = _sha(
        {
            "action_id": action.get("action_id"),
            "action_digest": action.get("action_digest"),
            "semantic_subject_id": action.get("semantic_subject_id"),
            "paramartha_carrier_element_id": action.get(
                "paramartha_carrier_element_id"
            ),
            "target_samvrti_world_id": target_world_id,
            "world_relation": action.get("world_relation"),
            "world_binding_evidence_digest": world_binding_evidence_digest,
            "world_transfer_resolution_digest": world_transfer_resolution_digest,
            "mapped_operation_id": mapped_operation_id,
            "mapped_operation_input_digest": mapped_input_digest,
            "intended_effect_digest": intended_effect_digest,
            "act_id": lower["act_id"],
            "prepared_act_state_digest": lower["prepared_act_state_digest"],
            "step_authorization_digest": lower["step_authorization_digest"],
            "capability_lease_digest": lower["capability_lease_digest"],
            "host_projection_digest": lower["host_projection_digest"],
            "transaction_intent_digest": lower["transaction_intent_digest"],
        }
    )
    lower["semantic_effect_binding_digest"] = semantic_effect_binding_digest
    lower["world_binding_evidence_digest"] = world_binding_evidence_digest
    lower["world_transfer_resolution_digest"] = world_transfer_resolution_digest
    return lower


def _binding_state(
    *,
    action: Mapping[str, Any],
    binding: Mapping[str, Any],
    prepared_act: Mapping[str, Any],
    transaction: Mapping[str, Any],
    errors: list[str],
) -> tuple[str, list[str]]:
    source_route = str(action.get("action_route", ""))
    reasons: list[str] = []

    if source_route == PROHIBITED_ROUTE:
        if prepared_act or transaction:
            errors.append("lower_effect_binding_for_explicitly_prohibited_action")
            return BINDING_OBSTRUCTED, reasons
        return PROPOSAL_ONLY, ["explicit_prohibition_preserved"]

    if not prepared_act and not transaction:
        if source_route in AUTHORITY_PENDING_ROUTES:
            return AWAITING_LOWER_AUTHORITY, ["lower_authority_not_yet_bound"]
        if source_route in WORLD_PENDING_ROUTES:
            return AWAITING_WORLD_RESOLUTION, ["world_resolution_not_yet_bound"]
        return PROPOSAL_ONLY, ["no_lower_effect_artifact_bound"]

    if errors:
        return BINDING_OBSTRUCTED, reasons

    if source_route in WORLD_PENDING_ROUTES:
        resolution = str(binding.get("world_transfer_resolution_digest", "")).strip()
        if not resolution:
            return AWAITING_WORLD_RESOLUTION, [
                "new_world_resolution_witness_required"
            ]
        reasons.append("prior_world_pending_resolved_by_new_witness")

    if source_route in AUTHORITY_PENDING_ROUTES:
        reasons.append("prior_authority_pending_resolved_by_valid_lower_artifact")

    if source_route in PROPOSAL_ROUTES:
        override = bool(binding.get("explicit_reassessment_authorized", False))
        if not override:
            return PROPOSAL_ONLY, ["source_route_requires_reassessment"]
        reasons.append("explicit_reassessment_authorized")

    if transaction:
        phase = str(transaction.get("current_phase", ""))
        route = str(transaction.get("route", ""))
        if phase == "committed":
            mapped = TRANSACTION_OUTCOME_MAP.get(route)
            if mapped is None:
                errors.append("committed_transaction_route_unrecognized")
                return BINDING_OBSTRUCTED, reasons
            if not str(transaction.get("transaction_final_receipt_digest", "")):
                errors.append("committed_transaction_final_receipt_missing")
                return BINDING_OBSTRUCTED, reasons
            return mapped, reasons
        return TRANSACTION_IN_PROGRESS, reasons

    return AUTHORIZED_PREPARED, reasons


def build_action_effect_lineage_binding(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ActionEffectLineageBindingResult:
    ctx = _m(runtime_context)
    authority_packet = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "action_effect_lineage_binding_plan_v7_13.json"
    source_path = root / "middle_way_action_lifting_packet_v7_12.json"
    input_path = root / "action_effect_lineage_bindings_input_v7_13.json"
    output_path = root / "action_effect_lineage_binding_packet_v7_13.json"
    receipt_path = root / "action_effect_lineage_binding_receipt_v7_13.json"
    audit_path = root / "action_effect_lineage_binding_audit_v7_13.jsonl"

    if ctx.get("action_effect_lineage_binding_enabled") is not True:
        blockers.append("action_effect_lineage_binding_enabled_not_true")
    if ctx.get("apply_action_effect_lineage_binding") is not True:
        blockers.append("apply_action_effect_lineage_binding_not_true")
    if (
        authority_packet.get("authority_status")
        != "KUUOS_ACTION_EFFECT_LINEAGE_BINDING_AUTHORITY_READY"
    ):
        blockers.append("action_effect_lineage_binding_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "source_action_packet_read_allowed",
        "lineage_bindings_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority_packet.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)
    bindings_packet = _read_json(input_path)

    if not plan:
        blockers.append("lineage_binding_plan_missing_or_invalid")
    else:
        _validate_plan(plan, blockers)

    if not source:
        blockers.append("middle_way_action_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("middle_way_action_packet_version_invalid")

    if not bindings_packet:
        blockers.append("lineage_bindings_input_missing_or_invalid")
    elif bindings_packet.get("version") != INPUT_VERSION:
        blockers.append("lineage_bindings_input_version_invalid")

    if plan and source and bindings_packet:
        source_digest = _sha(source)
        if str(plan.get("source_action_packet_digest", "")) != source_digest:
            blockers.append("source_action_packet_digest_mismatch")
        if (
            str(bindings_packet.get("source_action_packet_digest", ""))
            != source_digest
        ):
            blockers.append("bindings_source_action_packet_digest_mismatch")

        boundary = _m(source.get("middle_way_action_boundary"))
        if boundary.get("semantic_route_is_execution_authority") is True:
            blockers.append("source_semantic_route_authority_invalid")
        if boundary.get("runtime_assessment_executes_action") is not False:
            blockers.append("source_runtime_execution_boundary_invalid")
        if (
            boundary.get("transactional_effect_reconciliation_still_required_after_effect")
            is not True
        ):
            blockers.append("source_transaction_reconciliation_boundary_missing")

    actions = _source_actions(source, blockers) if source else {}
    raw_bindings = bindings_packet.get("bindings", []) if bindings_packet else []
    if bindings_packet and not isinstance(raw_bindings, list):
        blockers.append("bindings_not_list")
        raw_bindings = []
    if bindings_packet and not raw_bindings:
        blockers.append("bindings_empty")

    records: list[dict[str, Any]] = []
    seen: set[str] = set()

    if not blockers:
        for index, raw in enumerate(raw_bindings):
            if not isinstance(raw, Mapping):
                blockers.append(f"binding_{index}_not_object")
                continue

            action_id = str(raw.get("action_id", "")).strip()
            if not action_id:
                blockers.append(f"binding_{index}_action_id_missing")
                continue
            if action_id in seen:
                blockers.append("duplicate_binding_action_id")
                continue
            seen.add(action_id)

            action = actions.get(action_id)
            if action is None:
                blockers.append(f"binding_{index}_unknown_action_id")
                continue

            errors: list[str] = []
            prepared_act = _validated_prepared_act(
                raw.get("prepared_act_state"),
                errors,
            )
            transaction = _validated_transaction(
                raw.get("transaction_state"),
                errors,
            )
            lower = _check_exact_binding(
                action=action,
                binding=raw,
                prepared_act=prepared_act,
                transaction=transaction,
                errors=errors,
            )
            state, reasons = _binding_state(
                action=action,
                binding=raw,
                prepared_act=prepared_act,
                transaction=transaction,
                errors=errors,
            )
            if errors:
                state = BINDING_OBSTRUCTED

            records.append(
                {
                    "action_id": action_id,
                    "action_digest": action.get("action_digest"),
                    "source_action_route": action.get("action_route"),
                    "semantic_subject_id": action.get("semantic_subject_id"),
                    "paramartha_carrier_element_id": action.get(
                        "paramartha_carrier_element_id"
                    ),
                    "target_samvrti_world_id": action.get(
                        "target_samvrti_world_id"
                    ),
                    "world_relation": action.get("world_relation"),
                    "action_effect_lineage_state": state,
                    "semantic_effect_binding_digest": lower[
                        "semantic_effect_binding_digest"
                    ],
                    "act_id": lower["act_id"],
                    "prepared_act_state_digest": lower[
                        "prepared_act_state_digest"
                    ],
                    "step_authorization_digest": lower[
                        "step_authorization_digest"
                    ],
                    "capability_lease_digest": lower[
                        "capability_lease_digest"
                    ],
                    "host_projection_digest": lower[
                        "host_projection_digest"
                    ],
                    "transaction_intent_digest": lower[
                        "transaction_intent_digest"
                    ],
                    "transaction_state_digest": lower[
                        "transaction_state_digest"
                    ],
                    "transaction_final_receipt_digest": lower[
                        "transaction_final_receipt_digest"
                    ],
                    "world_binding_evidence_digest": lower[
                        "world_binding_evidence_digest"
                    ],
                    "world_transfer_resolution_digest": lower[
                        "world_transfer_resolution_digest"
                    ],
                    "binding_errors": sorted(set(errors)),
                    "binding_reasons": sorted(set(reasons)),
                    "semantic_route_grants_execution_authority": False,
                    "binding_layer_executes_effect": False,
                    "lower_receipts_remain_canonical": True,
                }
            )

    counts = {
        "prepared": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == AUTHORIZED_PREPARED
        ),
        "in_progress": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == TRANSACTION_IN_PROGRESS
        ),
        "confirmed": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == EFFECT_CONFIRMED
        ),
        "reobserve": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == REOBSERVATION_REQUIRED
        ),
        "compensation": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == COMPENSATION_PROPOSED
        ),
        "handover": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == HANDOVER_REQUIRED
        ),
        "no_effect": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == NO_EFFECT_RECORDED
        ),
        "awaiting": sum(
            1 for record in records
            if record["action_effect_lineage_state"]
            in {AWAITING_LOWER_AUTHORITY, AWAITING_WORLD_RESOLUTION}
        ),
        "proposal": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == PROPOSAL_ONLY
        ),
        "obstructed": sum(
            1 for record in records
            if record["action_effect_lineage_state"] == BINDING_OBSTRUCTED
        ),
    }

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        if counts["obstructed"] > 0:
            status = OBSTRUCTED
        elif (
            counts["awaiting"] > 0
            or counts["proposal"] > 0
            or counts["in_progress"] > 0
        ):
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_action_packet_digest": _sha(source),
            "action_effect_lineages": records,
            "summary": {
                "binding_count": len(records),
                "authorized_prepared_count": counts["prepared"],
                "transaction_in_progress_count": counts["in_progress"],
                "effect_confirmed_count": counts["confirmed"],
                "reobservation_required_count": counts["reobserve"],
                "compensation_proposed_count": counts["compensation"],
                "handover_required_count": counts["handover"],
                "no_effect_recorded_count": counts["no_effect"],
                "awaiting_count": counts["awaiting"],
                "proposal_only_count": counts["proposal"],
                "obstructed_count": counts["obstructed"],
            },
            "dependent_origination_effect_boundary": {
                "semantic_route_is_execution_authority": False,
                "binding_layer_executes_effect": False,
                "lower_actos_authorization_is_independently_validated": True,
                "capability_lease_is_independently_validated": True,
                "host_projection_is_independently_validated": True,
                "semantic_world_to_host_projection_binding_is_explicit": True,
                "prior_authority_pending_can_be_resolved_by_fresh_lower_authority": True,
                "prior_world_pending_can_be_resolved_by_new_world_witness": True,
                "transaction_outcome_refines_action_status_without_rewriting_source_semantics": True,
                "effect_confirmation_requires_transaction_reconciliation_and_verification": True,
                "compensation_proposal_requires_new_authorized_transaction": True,
                "lower_receipts_remain_canonical": True,
                "execution_success_implies_mission_success": False,
                "source_authority_transferred": False,
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-action-effect-lineage-binding-" + _sha(
        {
            "plan": plan,
            "source_digest": _sha(source),
            "bindings_digest": _sha(bindings_packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "binding_count": len(records),
        "authorized_prepared_count": counts["prepared"],
        "transaction_in_progress_count": counts["in_progress"],
        "effect_confirmed_count": counts["confirmed"],
        "reobservation_required_count": counts["reobserve"],
        "compensation_proposed_count": counts["compensation"],
        "handover_required_count": counts["handover"],
        "no_effect_recorded_count": counts["no_effect"],
        "awaiting_count": counts["awaiting"],
        "proposal_only_count": counts["proposal"],
        "obstructed_count": counts["obstructed"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "semantic_route_is_execution_authority": False,
        "binding_layer_executes_effect": False,
        "lower_receipts_remain_canonical": True,
        "execution_success_implies_mission_success": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return ActionEffectLineageBindingResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(records),
        counts["prepared"],
        counts["in_progress"],
        counts["confirmed"],
        counts["reobserve"],
        counts["compensation"],
        counts["handover"],
        counts["no_effect"],
        counts["awaiting"],
        counts["proposal"],
        counts["obstructed"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
