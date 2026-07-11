#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_KERNEL = "PlanOS Bounded Synthesis Receipt Kernel"
SOURCE_KERNEL_VERSION = "v0.1"
SOURCE_PLANOS_VERSION = "v1.04"
SOURCE_STATUS = "PLANOS_BOUNDED_SYNTHESIS_RECEIPT_ISSUED"

CONSTRAINT_FIELDS = {
    "planning_horizon",
    "maximum_plan_steps",
    "maximum_branching_factor",
    "maximum_revision_cycles",
    "reversible_actions_required",
    "irreversible_step_requires_checkpoint",
    "stop_condition_digests",
    "forbidden_effects",
}
PLAN_FIELDS = {
    "plan_id",
    "plan_revision",
    "selected_candidate_id",
    "selected_candidate_plan_intent_digest",
    "source_world_model_state_digest",
    "plan_steps",
    "stop_condition_digests",
    "retained_alternative_records",
    "preserved_evidence_lineage_digests",
}
STEP_FIELDS = {
    "step_id",
    "sequence_index",
    "action_class",
    "action_spec_digest",
    "precondition_digests",
    "expected_effect_digests",
    "effect_tags",
    "evidence_lineage_digests",
    "stop_condition_digests",
    "reversible",
    "irreversible",
    "checkpoint_step_id",
    "branch_ids",
}
ALTERNATIVE_FIELDS = {
    "candidate_id",
    "nonselection_reason_digest",
    "retained_for_revision",
}
ALLOWED_ACTION_CLASSES = {
    "analyze",
    "condition_reassessment",
    "evidence_collection",
    "hold",
    "prepare_reversible",
    "request_revision",
    "review_checkpoint",
    "terminate",
}
FIXED_FORBIDDEN_EFFECTS = {
    "active_now",
    "candidate_substitution",
    "execution_permission",
    "external_side_effect",
    "persistent_world_mutation",
    "selection_authority_transfer",
    "tool_invocation",
    "unreviewed_scope_expansion",
}


@dataclass
class VerifyOSBoundedPlanMiddleWayVerificationResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256(payload).hexdigest()


def _canonical_string_list(
    value: Any,
    *,
    allow_empty: bool = False,
) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def compute_verifyos_bounded_plan_verification_bundle_digest(
    **fields: Any,
) -> str:
    return canonical_digest(fields)


def _concrete_plan_payload(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "plan_id": source.get("plan_id"),
        "plan_revision": source.get("plan_revision"),
        "selected_candidate_id": source.get("selected_candidate_id"),
        "selected_candidate_plan_intent_digest": source.get(
            "selected_candidate_plan_intent_digest"
        ),
        "source_world_model_state_digest": source.get(
            "source_world_model_state_digest"
        ),
        "plan_steps": source.get("plan_steps"),
        "stop_condition_digests": source.get("stop_condition_digests"),
        "retained_alternative_records": source.get(
            "retained_alternative_records"
        ),
        "preserved_evidence_lineage_digests": source.get(
            "preserved_evidence_lineage_digests"
        ),
    }


def build_verifyos_bounded_plan_middle_way_verification_certificate(
    *,
    source_plan_receipt: Mapping[str, Any],
    expected_source_plan_receipt_digest: str,
    current_world_binding_digest: str,
    current_world_model_state_digest: str,
    current_world_model_revision: int,
    current_world_lineage_digest: str,
    expected_selected_candidate_id: str,
    expected_selected_candidate_plan_intent_digest: str,
    verification_policy_digest: str,
    verification_owner_responsibility_digest: str,
    verification_request_id: str,
    verification_bundle_digest: str,
) -> VerifyOSBoundedPlanMiddleWayVerificationResult:
    blockers: list[str] = []
    source = (
        dict(source_plan_receipt)
        if isinstance(source_plan_receipt, Mapping)
        else {}
    )

    text_inputs = {
        "expected_source_plan_receipt_digest": expected_source_plan_receipt_digest,
        "current_world_binding_digest": current_world_binding_digest,
        "current_world_model_state_digest": current_world_model_state_digest,
        "current_world_lineage_digest": current_world_lineage_digest,
        "expected_selected_candidate_id": expected_selected_candidate_id,
        "expected_selected_candidate_plan_intent_digest": (
            expected_selected_candidate_plan_intent_digest
        ),
        "verification_policy_digest": verification_policy_digest,
        "verification_owner_responsibility_digest": (
            verification_owner_responsibility_digest
        ),
        "verification_request_id": verification_request_id,
        "verification_bundle_digest": verification_bundle_digest,
    }
    for name, value in text_inputs.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    if (
        not isinstance(current_world_model_revision, int)
        or isinstance(current_world_model_revision, bool)
        or current_world_model_revision < 0
    ):
        blockers.append("current_world_model_revision_invalid")

    if not source:
        return VerifyOSBoundedPlanMiddleWayVerificationResult(
            STATUS_BLOCKED,
            ["source_plan_receipt_missing"],
            None,
        )

    exact_headers = {
        "kernel": SOURCE_KERNEL,
        "kernel_version": SOURCE_KERNEL_VERSION,
        "planos_version": SOURCE_PLANOS_VERSION,
        "status": SOURCE_STATUS,
    }
    for name, expected in exact_headers.items():
        if source.get(name) != expected:
            blockers.append(f"source_{name}_invalid")

    source_receipt_digest = source.get(
        "planos_bounded_synthesis_receipt_digest"
    )
    if not isinstance(source_receipt_digest, str) or not source_receipt_digest:
        blockers.append("source_plan_receipt_digest_missing")
        source_receipt_digest = ""
    else:
        unsigned = dict(source)
        unsigned.pop("planos_bounded_synthesis_receipt_digest", None)
        if source_receipt_digest != canonical_digest(unsigned):
            blockers.append("source_plan_receipt_digest_mismatch")
        if source_receipt_digest != expected_source_plan_receipt_digest:
            blockers.append("source_plan_receipt_expected_binding_mismatch")

    required_text_fields = (
        "source_intake_certificate_digest",
        "source_verifyos_certificate_digest",
        "source_decisionos_handoff_receipt_digest",
        "source_world_binding_digest",
        "source_world_model_state_digest",
        "source_world_lineage_digest",
        "source_synthesis_constraint_digest",
        "selected_candidate_id",
        "selected_candidate_plan_intent_digest",
        "synthesis_constraint_digest",
        "synthesis_policy_digest",
        "planos_synthesis_responsibility_digest",
        "synthesis_request_id",
        "proposed_plan_digest",
        "alternative_lineage_bundle_digest",
        "synthesis_bundle_digest",
        "plan_id",
        "concrete_plan_digest",
    )
    for name in required_text_fields:
        if not isinstance(source.get(name), str) or not source.get(name):
            blockers.append(f"source_{name}_missing")

    source_world_revision = source.get("source_world_model_revision")
    if (
        not isinstance(source_world_revision, int)
        or isinstance(source_world_revision, bool)
        or source_world_revision < 0
    ):
        blockers.append("source_world_model_revision_invalid")

    if source.get("selected_candidate_id") != expected_selected_candidate_id:
        blockers.append("selected_candidate_expected_binding_mismatch")
    if source.get("selected_candidate_plan_intent_digest") != (
        expected_selected_candidate_plan_intent_digest
    ):
        blockers.append("plan_intent_expected_binding_mismatch")

    required_true_boundaries = (
        "selected_candidate_not_substituted",
        "plan_intent_binding_preserved",
        "world_state_dependency_preserved",
        "finite_plan_constructed",
        "planning_horizon_bounded",
        "plan_step_count_bounded",
        "branching_factor_bounded",
        "revision_cycles_bounded",
        "reversible_actions_default_preserved",
        "irreversible_steps_checkpoint_guarded",
        "stop_conditions_preserved",
        "forbidden_effects_absent",
        "alternative_candidates_retained",
        "dissent_evidence_preserved",
        "minority_evidence_preserved",
        "lineage_extended_not_replaced",
        "responsibility_extended_not_replaced",
        "plan_is_conditionally_binding",
        "plan_is_not_absolute_command",
        "plan_is_not_contentless_proposal",
        "selection_remains_decisionos_owned",
        "plan_synthesis_performed",
        "concrete_plan_issued",
        "plan_receipt_issued",
        "actos_authorization_required",
        "verifyos_reverification_required_before_irreversible_step",
        "persistent_world_state_unchanged",
        "world_model_prediction_not_truth",
        "world_mutation_not_granted",
        "history_read_only",
        "qi_grants_no_authority",
        "future_only",
    )
    required_false_boundaries = (
        "selection_authority_granted_to_planos",
        "plan_activated",
        "materialization_performed",
        "execution_authority_granted",
        "execution_permission",
        "active_now",
    )
    for name in required_true_boundaries:
        if source.get(name) is not True:
            blockers.append(f"source_boundary_{name}_missing")
    for name in required_false_boundaries:
        if source.get(name) is not False:
            blockers.append(f"source_boundary_{name}_promoted")

    constraints = source.get("synthesis_constraints")
    if not isinstance(constraints, Mapping) or set(constraints) != CONSTRAINT_FIELDS:
        blockers.append("synthesis_constraints_invalid")
        constraints = {}

    planning_horizon = constraints.get("planning_horizon")
    maximum_plan_steps = constraints.get("maximum_plan_steps")
    maximum_branching_factor = constraints.get("maximum_branching_factor")
    maximum_revision_cycles = constraints.get("maximum_revision_cycles")
    for name, value, lower, upper in (
        ("planning_horizon", planning_horizon, 1, 64),
        ("maximum_plan_steps", maximum_plan_steps, 1, 32),
        ("maximum_branching_factor", maximum_branching_factor, 1, 8),
        ("maximum_revision_cycles", maximum_revision_cycles, 0, 8),
    ):
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not lower <= value <= upper
        ):
            blockers.append(f"constraint_{name}_invalid")
    if (
        isinstance(planning_horizon, int)
        and isinstance(maximum_plan_steps, int)
        and maximum_plan_steps > planning_horizon
    ):
        blockers.append("maximum_plan_steps_exceeds_horizon")
    if constraints.get("reversible_actions_required") is not True:
        blockers.append("reversible_actions_required_missing")
    if constraints.get("irreversible_step_requires_checkpoint") is not True:
        blockers.append("irreversible_checkpoint_requirement_missing")

    constraint_stop_ok, constraint_stops = _canonical_string_list(
        constraints.get("stop_condition_digests")
    )
    if not constraint_stop_ok:
        blockers.append("constraint_stop_conditions_invalid")
    forbidden_effects = constraints.get("forbidden_effects")
    if (
        not isinstance(forbidden_effects, list)
        or forbidden_effects != sorted(FIXED_FORBIDDEN_EFFECTS)
    ):
        blockers.append("fixed_forbidden_effect_set_invalid")
    if constraints and source.get("synthesis_constraint_digest") != canonical_digest(
        dict(constraints)
    ):
        blockers.append("synthesis_constraint_digest_mismatch")
    if source.get("synthesis_constraint_digest") != source.get(
        "source_synthesis_constraint_digest"
    ):
        blockers.append("source_synthesis_constraint_lineage_mismatch")

    plan_revision = source.get("plan_revision")
    if plan_revision != 0:
        blockers.append("plan_revision_invalid")
    if source.get("planning_horizon") != planning_horizon:
        blockers.append("planning_horizon_output_mismatch")
    if source.get("maximum_plan_steps") != maximum_plan_steps:
        blockers.append("maximum_plan_steps_output_mismatch")
    if source.get("maximum_branching_factor") != maximum_branching_factor:
        blockers.append("maximum_branching_factor_output_mismatch")
    if source.get("maximum_revision_cycles") != maximum_revision_cycles:
        blockers.append("maximum_revision_cycles_output_mismatch")

    plan_stop_ok, plan_stops = _canonical_string_list(
        source.get("stop_condition_digests")
    )
    if not plan_stop_ok or plan_stops != constraint_stops:
        blockers.append("plan_stop_conditions_invalid")

    evidence_ok, preserved_evidence = _canonical_string_list(
        source.get("preserved_evidence_lineage_digests")
    )
    if not evidence_ok:
        blockers.append("preserved_evidence_lineage_invalid")

    alternatives = source.get("retained_alternative_records")
    normalized_alternatives: list[dict[str, Any]] = []
    if not isinstance(alternatives, list) or not alternatives:
        blockers.append("retained_alternative_records_empty")
    else:
        alternative_ids: list[str] = []
        for index, raw_alternative in enumerate(alternatives):
            if (
                not isinstance(raw_alternative, Mapping)
                or set(raw_alternative) != ALTERNATIVE_FIELDS
            ):
                blockers.append(f"alternative_schema_invalid_{index}")
                continue
            alternative = dict(raw_alternative)
            candidate_id = alternative.get("candidate_id")
            alternative_ids.append(candidate_id)
            if (
                not isinstance(candidate_id, str)
                or not candidate_id
                or candidate_id == expected_selected_candidate_id
            ):
                blockers.append(f"alternative_candidate_invalid_{index}")
            if (
                not isinstance(alternative.get("nonselection_reason_digest"), str)
                or not alternative.get("nonselection_reason_digest")
            ):
                blockers.append(f"alternative_reason_missing_{index}")
            if alternative.get("retained_for_revision") is not True:
                blockers.append(f"alternative_retention_missing_{index}")
            normalized_alternatives.append(alternative)
        if alternative_ids != sorted(alternative_ids) or len(
            alternative_ids
        ) != len(set(alternative_ids)):
            blockers.append("alternative_records_not_canonical")

    steps = source.get("plan_steps")
    normalized_steps: list[dict[str, Any]] = []
    if not isinstance(steps, list) or not steps:
        blockers.append("plan_steps_empty")
    else:
        if (
            isinstance(maximum_plan_steps, int)
            and len(steps) > maximum_plan_steps
        ):
            blockers.append("plan_step_count_exceeds_bound")
        if source.get("plan_step_count") != len(steps):
            blockers.append("plan_step_count_output_mismatch")

        step_ids: list[str] = []
        action_digests: list[str] = []
        prior_checkpoint_indices: dict[str, int] = {}
        all_branch_ids: set[str] = set()
        for sequence_index, raw_step in enumerate(steps, start=1):
            if not isinstance(raw_step, Mapping) or set(raw_step) != STEP_FIELDS:
                blockers.append(f"plan_step_schema_invalid_{sequence_index}")
                continue
            step = dict(raw_step)
            step_id = step.get("step_id")
            action_digest = step.get("action_spec_digest")
            step_ids.append(step_id)
            action_digests.append(action_digest)
            if not isinstance(step_id, str) or not step_id:
                blockers.append(f"plan_step_id_invalid_{sequence_index}")
            if not isinstance(action_digest, str) or not action_digest:
                blockers.append(f"plan_step_action_digest_invalid_{sequence_index}")
            if step.get("sequence_index") != sequence_index:
                blockers.append(f"plan_step_sequence_invalid_{sequence_index}")
            action_class = step.get("action_class")
            if action_class not in ALLOWED_ACTION_CLASSES:
                blockers.append(f"plan_step_action_class_invalid_{sequence_index}")

            normalized_lists: dict[str, list[str]] = {}
            for field, allow_empty in (
                ("precondition_digests", False),
                ("expected_effect_digests", False),
                ("effect_tags", False),
                ("evidence_lineage_digests", False),
                ("stop_condition_digests", False),
                ("branch_ids", True),
            ):
                valid, values = _canonical_string_list(
                    step.get(field),
                    allow_empty=allow_empty,
                )
                if not valid:
                    blockers.append(
                        f"plan_step_{field}_invalid_{sequence_index}"
                    )
                normalized_lists[field] = values

            if set(normalized_lists["effect_tags"]) & FIXED_FORBIDDEN_EFFECTS:
                blockers.append(f"plan_step_forbidden_effect_{sequence_index}")
            if not set(
                normalized_lists["evidence_lineage_digests"]
            ).issubset(set(preserved_evidence)):
                blockers.append(
                    f"plan_step_evidence_outside_plan_lineage_{sequence_index}"
                )
            if normalized_lists["stop_condition_digests"] != plan_stops:
                blockers.append(
                    f"plan_step_stop_conditions_incomplete_{sequence_index}"
                )
            if (
                isinstance(maximum_branching_factor, int)
                and len(normalized_lists["branch_ids"])
                > maximum_branching_factor
            ):
                blockers.append(
                    f"plan_step_branch_count_exceeds_bound_{sequence_index}"
                )
            all_branch_ids.update(normalized_lists["branch_ids"])

            reversible = step.get("reversible")
            irreversible = step.get("irreversible")
            if not isinstance(reversible, bool) or not isinstance(
                irreversible, bool
            ):
                blockers.append(
                    f"plan_step_reversibility_invalid_{sequence_index}"
                )
            elif reversible == irreversible:
                blockers.append(
                    f"plan_step_reversibility_not_exclusive_{sequence_index}"
                )

            checkpoint_step_id = step.get("checkpoint_step_id")
            if not isinstance(checkpoint_step_id, str):
                blockers.append(
                    f"plan_step_checkpoint_reference_invalid_{sequence_index}"
                )
            elif irreversible is True:
                checkpoint_index = prior_checkpoint_indices.get(
                    checkpoint_step_id
                )
                if not checkpoint_step_id:
                    blockers.append(
                        f"irreversible_step_checkpoint_missing_{sequence_index}"
                    )
                elif checkpoint_index is None or checkpoint_index >= sequence_index:
                    blockers.append(
                        f"irreversible_step_checkpoint_not_prior_{sequence_index}"
                    )
            elif checkpoint_step_id:
                blockers.append(
                    f"reversible_step_checkpoint_reference_forbidden_{sequence_index}"
                )

            if action_class == "review_checkpoint" and isinstance(step_id, str):
                prior_checkpoint_indices[step_id] = sequence_index
            normalized_steps.append(step)

        if len(step_ids) != len(set(step_ids)):
            blockers.append("duplicate_plan_step_id")
        if len(action_digests) != len(set(action_digests)):
            blockers.append("duplicate_plan_step_action_digest")
        if (
            isinstance(maximum_branching_factor, int)
            and len(all_branch_ids) > maximum_branching_factor
        ):
            blockers.append("plan_branching_factor_exceeds_bound")

    expected_concrete_plan_digest = canonical_digest(
        _concrete_plan_payload(source)
    )
    if source.get("concrete_plan_digest") != expected_concrete_plan_digest:
        blockers.append("concrete_plan_digest_mismatch")

    source_world_binding_digest = source.get("source_world_binding_digest")
    source_world_model_state_digest = source.get(
        "source_world_model_state_digest"
    )
    source_world_lineage_digest = source.get("source_world_lineage_digest")
    if not isinstance(source_world_binding_digest, str) or not (
        source_world_binding_digest
    ):
        blockers.append("source_world_binding_digest_missing")
    if not isinstance(source_world_model_state_digest, str) or not (
        source_world_model_state_digest
    ):
        blockers.append("source_world_model_state_digest_missing")
    if not isinstance(source_world_lineage_digest, str) or not (
        source_world_lineage_digest
    ):
        blockers.append("source_world_lineage_digest_missing")

    lineage_ok, source_lineage = _canonical_string_list(
        source.get("resulting_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    else:
        for required_digest in (
            source.get("source_intake_certificate_digest"),
            source.get("proposed_plan_digest"),
            source.get("synthesis_constraint_digest"),
            source.get("synthesis_bundle_digest"),
        ):
            if required_digest not in source_lineage:
                blockers.append("source_lineage_required_digest_missing")

    responsibility_ok, source_responsibility = _canonical_string_list(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    elif source.get(
        "planos_synthesis_responsibility_digest"
    ) not in source_responsibility:
        blockers.append("source_planos_synthesis_responsibility_missing")

    if not blockers:
        expected_bundle = compute_verifyos_bounded_plan_verification_bundle_digest(
            source_plan_receipt_digest=source_receipt_digest,
            expected_source_plan_receipt_digest=(
                expected_source_plan_receipt_digest
            ),
            current_world_binding_digest=current_world_binding_digest,
            current_world_model_state_digest=current_world_model_state_digest,
            current_world_model_revision=current_world_model_revision,
            current_world_lineage_digest=current_world_lineage_digest,
            expected_selected_candidate_id=expected_selected_candidate_id,
            expected_selected_candidate_plan_intent_digest=(
                expected_selected_candidate_plan_intent_digest
            ),
            verification_policy_digest=verification_policy_digest,
            verification_owner_responsibility_digest=(
                verification_owner_responsibility_digest
            ),
            verification_request_id=verification_request_id,
        )
        if verification_bundle_digest != expected_bundle:
            blockers.append("verification_bundle_digest_mismatch")

    if blockers:
        return VerifyOSBoundedPlanMiddleWayVerificationResult(
            STATUS_BLOCKED,
            sorted(set(blockers)),
            None,
        )

    world_conditions_current = (
        current_world_binding_digest == source_world_binding_digest
        and current_world_model_state_digest
        == source_world_model_state_digest
        and current_world_model_revision == source_world_revision
        and current_world_lineage_digest == source_world_lineage_digest
    )
    conditional_status = (
        "valid" if world_conditions_current else "revision_required"
    )
    disposition = (
        "bounded_plan_verified_for_materialization_intake"
        if world_conditions_current
        else "return_to_planos_revision"
    )
    verification_record = {
        "source_plan_receipt_digest": source_receipt_digest,
        "source_world_binding_digest": source_world_binding_digest,
        "source_world_model_state_digest": source_world_model_state_digest,
        "source_world_model_revision": source_world_revision,
        "source_world_lineage_digest": source_world_lineage_digest,
        "current_world_binding_digest": current_world_binding_digest,
        "current_world_model_state_digest": current_world_model_state_digest,
        "current_world_model_revision": current_world_model_revision,
        "current_world_lineage_digest": current_world_lineage_digest,
        "world_conditions_current": world_conditions_current,
        "conditional_validity_status": conditional_status,
        "verification_disposition": disposition,
    }
    verification_record_digest = canonical_digest(verification_record)

    certificate = {
        "kernel": "VerifyOS Bounded Plan Middle-Way Verification Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.5",
        "status": "VERIFYOS_BOUNDED_PLAN_MIDDLE_WAY_VERIFIED",
        "source_planos_version": source["planos_version"],
        "source_plan_receipt_digest": source_receipt_digest,
        "source_concrete_plan_digest": source["concrete_plan_digest"],
        "source_synthesis_constraint_digest": source[
            "synthesis_constraint_digest"
        ],
        "source_world_binding_digest": source_world_binding_digest,
        "source_world_model_state_digest": source_world_model_state_digest,
        "source_world_model_revision": source_world_revision,
        "source_world_lineage_digest": source_world_lineage_digest,
        "current_world_binding_digest": current_world_binding_digest,
        "current_world_model_state_digest": current_world_model_state_digest,
        "current_world_model_revision": current_world_model_revision,
        "current_world_lineage_digest": current_world_lineage_digest,
        "selected_candidate_id": expected_selected_candidate_id,
        "selected_candidate_plan_intent_digest": (
            expected_selected_candidate_plan_intent_digest
        ),
        "verification_policy_digest": verification_policy_digest,
        "verification_owner_responsibility_digest": (
            verification_owner_responsibility_digest
        ),
        "verification_request_id": verification_request_id,
        "verification_bundle_digest": verification_bundle_digest,
        "verification_record": verification_record,
        "verification_record_digest": verification_record_digest,
        "world_conditions_current": world_conditions_current,
        "conditional_validity_status": conditional_status,
        "verification_disposition": disposition,
        "bounded_plan_verified_for_materialization_intake": (
            world_conditions_current
        ),
        "plan_revision_required": not world_conditions_current,
        "materialization_intake_admitted": world_conditions_current,
        "structural_verification_passed": True,
        "source_receipt_digest_verified": True,
        "finite_plan_verified": True,
        "step_sequence_verified": True,
        "step_bound_verified": True,
        "branch_bound_verified": True,
        "revision_bound_verified": True,
        "checkpoint_order_verified": True,
        "stop_conditions_verified": True,
        "forbidden_effects_absent": True,
        "selected_candidate_preserved": True,
        "plan_intent_preserved": True,
        "world_dependency_explicit": True,
        "alternative_candidates_preserved": True,
        "preserved_evidence_lineage_digests": preserved_evidence,
        "source_dissent_preservation_attested": True,
        "source_minority_preservation_attested": True,
        "dissent_evidence_preserved": True,
        "minority_evidence_preserved": True,
        "source_lineage_preserved": True,
        "source_responsibility_preserved": True,
        "plan_remains_conditionally_binding": True,
        "plan_not_reified": True,
        "plan_not_erased": True,
        "condition_change_routes_to_revision": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_verifyos": False,
        "plan_revision_authority_granted_to_verifyos": False,
        "plan_activated": False,
        "materialization_performed": False,
        "execution_authority_granted": False,
        "execution_permission": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": sorted(
            set(source_lineage)
            | {
                source_receipt_digest,
                verification_record_digest,
                verification_bundle_digest,
            }
        ),
        "resulting_responsibility_lineage_digests": sorted(
            set(source_responsibility)
            | {verification_owner_responsibility_digest}
        ),
    }
    certificate[
        "verifyos_bounded_plan_middle_way_verification_certificate_digest"
    ] = canonical_digest(certificate)
    return VerifyOSBoundedPlanMiddleWayVerificationResult(
        STATUS_READY,
        [],
        certificate,
    )
