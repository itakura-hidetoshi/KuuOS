#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_KERNEL = "PlanOS Middle-Way Bounded Synthesis Intake Kernel"
SOURCE_KERNEL_VERSION = "v0.1"
SOURCE_PLANOS_VERSION = "v1.03"
SOURCE_STATUS = "PLANOS_MIDDLE_WAY_BOUNDED_SYNTHESIS_INTAKE_ROUTED"
REQUIRED_SOURCE_DISPOSITION = "bounded_synthesis_intake_ready"
FIXED_FORBIDDEN_EFFECTS = (
    "active_now",
    "candidate_substitution",
    "execution_permission",
    "external_side_effect",
    "persistent_world_mutation",
    "selection_authority_transfer",
    "tool_invocation",
    "unreviewed_scope_expansion",
)
ALLOWED_ACTION_CLASSES = (
    "analyze",
    "condition_reassessment",
    "evidence_collection",
    "hold",
    "prepare_reversible",
    "request_revision",
    "review_checkpoint",
    "terminate",
)
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
    "world_state_dependency_digest",
    "stop_condition_digests",
    "retained_alternative_records",
    "preserved_evidence_lineage_digests",
    "steps",
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


@dataclass
class PlanOSBoundedSynthesisReceiptResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return sha256(payload).hexdigest()


def _canonical_string_list(
    value: Any, *, allow_empty: bool = False
) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def compute_synthesis_constraint_digest(constraints: Mapping[str, Any]) -> str:
    return canonical_digest(dict(constraints))


def compute_proposed_plan_digest(proposed_plan: Mapping[str, Any]) -> str:
    return canonical_digest(dict(proposed_plan))


def compute_bounded_synthesis_bundle_digest(
    *,
    source_intake_certificate_digest: str,
    expected_source_intake_certificate_digest: str,
    expected_world_binding_digest: str,
    expected_world_model_state_digest: str,
    expected_world_model_revision: int,
    expected_world_lineage_digest: str,
    expected_selected_candidate_id: str,
    expected_selected_candidate_plan_intent_digest: str,
    expected_synthesis_constraint_digest: str,
    synthesis_constraint_digest: str,
    synthesis_policy_digest: str,
    planos_synthesis_responsibility_digest: str,
    synthesis_request_id: str,
    proposed_plan_digest: str,
    alternative_lineage_bundle_digest: str,
) -> str:
    return canonical_digest(
        {
            "source_intake_certificate_digest": source_intake_certificate_digest,
            "expected_source_intake_certificate_digest": (
                expected_source_intake_certificate_digest
            ),
            "expected_world_binding_digest": expected_world_binding_digest,
            "expected_world_model_state_digest": expected_world_model_state_digest,
            "expected_world_model_revision": expected_world_model_revision,
            "expected_world_lineage_digest": expected_world_lineage_digest,
            "expected_selected_candidate_id": expected_selected_candidate_id,
            "expected_selected_candidate_plan_intent_digest": (
                expected_selected_candidate_plan_intent_digest
            ),
            "expected_synthesis_constraint_digest": (
                expected_synthesis_constraint_digest
            ),
            "synthesis_constraint_digest": synthesis_constraint_digest,
            "synthesis_policy_digest": synthesis_policy_digest,
            "planos_synthesis_responsibility_digest": (
                planos_synthesis_responsibility_digest
            ),
            "synthesis_request_id": synthesis_request_id,
            "proposed_plan_digest": proposed_plan_digest,
            "alternative_lineage_bundle_digest": alternative_lineage_bundle_digest,
        }
    )


def build_planos_bounded_synthesis_receipt(
    *,
    source_intake_certificate: Mapping[str, Any],
    expected_source_intake_certificate_digest: str,
    expected_world_binding_digest: str,
    expected_world_model_state_digest: str,
    expected_world_model_revision: int,
    expected_world_lineage_digest: str,
    expected_selected_candidate_id: str,
    expected_selected_candidate_plan_intent_digest: str,
    expected_synthesis_constraint_digest: str,
    synthesis_constraints: Mapping[str, Any],
    synthesis_constraint_digest: str,
    synthesis_policy_digest: str,
    planos_synthesis_responsibility_digest: str,
    synthesis_request_id: str,
    proposed_plan: Mapping[str, Any],
    proposed_plan_digest: str,
    alternative_lineage_bundle_digest: str,
    synthesis_bundle_digest: str,
) -> PlanOSBoundedSynthesisReceiptResult:
    blockers: list[str] = []
    source = (
        dict(source_intake_certificate)
        if isinstance(source_intake_certificate, Mapping)
        else {}
    )
    constraints = (
        dict(synthesis_constraints) if isinstance(synthesis_constraints, Mapping) else {}
    )
    plan = dict(proposed_plan) if isinstance(proposed_plan, Mapping) else {}

    text_inputs = {
        "expected_source_intake_certificate_digest": (
            expected_source_intake_certificate_digest
        ),
        "expected_world_binding_digest": expected_world_binding_digest,
        "expected_world_model_state_digest": expected_world_model_state_digest,
        "expected_world_lineage_digest": expected_world_lineage_digest,
        "expected_selected_candidate_id": expected_selected_candidate_id,
        "expected_selected_candidate_plan_intent_digest": (
            expected_selected_candidate_plan_intent_digest
        ),
        "expected_synthesis_constraint_digest": (
            expected_synthesis_constraint_digest
        ),
        "synthesis_constraint_digest": synthesis_constraint_digest,
        "synthesis_policy_digest": synthesis_policy_digest,
        "planos_synthesis_responsibility_digest": (
            planos_synthesis_responsibility_digest
        ),
        "synthesis_request_id": synthesis_request_id,
        "proposed_plan_digest": proposed_plan_digest,
        "alternative_lineage_bundle_digest": alternative_lineage_bundle_digest,
        "synthesis_bundle_digest": synthesis_bundle_digest,
    }
    for name, value in text_inputs.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    if (
        not isinstance(expected_world_model_revision, int)
        or isinstance(expected_world_model_revision, bool)
        or expected_world_model_revision < 0
    ):
        blockers.append("expected_world_model_revision_invalid")

    source_digest = ""
    source_transition_spec: dict[str, Any] = {}
    source_resulting_lineage: list[str] = []
    source_resulting_responsibility: list[str] = []
    source_dissent: list[str] = []
    source_minority: list[str] = []
    if not source:
        blockers.append("source_intake_certificate_missing")
    else:
        exact_headers = {
            "kernel": SOURCE_KERNEL,
            "kernel_version": SOURCE_KERNEL_VERSION,
            "planos_version": SOURCE_PLANOS_VERSION,
            "status": SOURCE_STATUS,
            "conditional_validity_status": "valid",
            "transition_kind": "retain",
            "intake_disposition": REQUIRED_SOURCE_DISPOSITION,
        }
        for name, expected in exact_headers.items():
            if source.get(name) != expected:
                blockers.append(f"source_{name}_invalid")

        raw_digest = source.get(
            "planos_middle_way_bounded_synthesis_intake_certificate_digest"
        )
        if not isinstance(raw_digest, str) or not raw_digest:
            blockers.append("source_intake_certificate_digest_missing")
        else:
            source_digest = raw_digest
            unsigned = dict(source)
            unsigned.pop(
                "planos_middle_way_bounded_synthesis_intake_certificate_digest",
                None,
            )
            if raw_digest != canonical_digest(unsigned):
                blockers.append("source_intake_certificate_digest_mismatch")
            if raw_digest != expected_source_intake_certificate_digest:
                blockers.append("source_intake_certificate_expected_binding_mismatch")

        expected_bindings = {
            "source_world_binding_digest": expected_world_binding_digest,
            "source_world_model_state_digest": expected_world_model_state_digest,
            "source_world_lineage_digest": expected_world_lineage_digest,
            "selected_candidate_id": expected_selected_candidate_id,
            "selected_candidate_plan_intent_digest": (
                expected_selected_candidate_plan_intent_digest
            ),
            "source_synthesis_constraint_digest": (
                expected_synthesis_constraint_digest
            ),
        }
        for name, expected in expected_bindings.items():
            if source.get(name) != expected:
                blockers.append(f"source_{name}_expected_binding_mismatch")
        if source.get("source_world_model_revision") != expected_world_model_revision:
            blockers.append("source_world_model_revision_expected_binding_mismatch")

        required_true = (
            "bounded_synthesis_request_admitted",
            "bounded_synthesis_intake_ready",
            "conditional_validity_enforced",
            "only_valid_status_admitted",
            "nonvalid_status_not_synthesized",
            "source_conditions_preserved",
            "source_changed_conditions_preserved",
            "source_lineage_preserved",
            "source_predecessor_preserved",
            "source_responsibility_preserved",
            "source_dissent_preserved",
            "source_minority_evidence_preserved",
            "responsibility_extended_not_replaced",
            "selection_remains_decisionos_owned",
            "persistent_world_state_unchanged",
            "world_model_prediction_not_truth",
            "world_mutation_not_granted",
            "history_read_only",
            "qi_grants_no_authority",
            "future_only",
        )
        required_false = (
            "awaiting_condition_change",
            "decisionos_revision_required",
            "successor_lineage_reverification_required",
            "close_without_synthesis",
            "terminate_without_synthesis",
            "selection_authority_granted_to_planos",
            "plan_synthesis_performed",
            "concrete_plan_issued",
            "plan_receipt_issued",
            "execution_authority_granted",
            "execution_permission",
            "active_now",
        )
        for name in required_true:
            if source.get(name) is not True:
                blockers.append(f"source_boundary_{name}_missing")
        for name in required_false:
            if source.get(name) is not False:
                blockers.append(f"source_boundary_{name}_promoted")

        raw_spec = source.get("source_transition_spec")
        if not isinstance(raw_spec, dict) or not raw_spec:
            blockers.append("source_transition_spec_invalid")
        else:
            source_transition_spec = dict(raw_spec)
            if source.get("source_transition_spec_digest") != canonical_digest(
                source_transition_spec
            ):
                blockers.append("source_transition_spec_digest_mismatch")
            for name, allow_empty in (
                ("resulting_lineage_digests", False),
                ("resulting_responsibility_lineage_digests", False),
                ("preserved_dissent_evidence_digests", True),
                ("preserved_minority_evidence_digests", True),
            ):
                valid, values = _canonical_string_list(
                    source_transition_spec.get(name), allow_empty=allow_empty
                )
                if not valid:
                    blockers.append(f"source_{name}_invalid")
                if name == "resulting_lineage_digests":
                    source_resulting_lineage = values
                elif name == "resulting_responsibility_lineage_digests":
                    source_resulting_responsibility = values
                elif name == "preserved_dissent_evidence_digests":
                    source_dissent = values
                else:
                    source_minority = values

        valid_source_resp, source_output_resp = _canonical_string_list(
            source.get("resulting_responsibility_lineage_digests")
        )
        if not valid_source_resp:
            blockers.append("source_resulting_responsibility_output_invalid")
        elif not set(source_resulting_responsibility).issubset(set(source_output_resp)):
            blockers.append("source_responsibility_output_lost_transition_lineage")
        elif source.get("planos_intake_responsibility_digest") not in source_output_resp:
            blockers.append("source_planos_intake_responsibility_not_retained")
        else:
            source_resulting_responsibility = source_output_resp

    if set(constraints) != CONSTRAINT_FIELDS:
        blockers.append("synthesis_constraint_schema_invalid")
    horizon = constraints.get("planning_horizon")
    max_steps = constraints.get("maximum_plan_steps")
    max_branching = constraints.get("maximum_branching_factor")
    max_revisions = constraints.get("maximum_revision_cycles")
    for name, value, lower, upper in (
        ("planning_horizon", horizon, 1, 64),
        ("maximum_plan_steps", max_steps, 1, 32),
        ("maximum_branching_factor", max_branching, 1, 8),
        ("maximum_revision_cycles", max_revisions, 0, 8),
    ):
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not lower <= value <= upper
        ):
            blockers.append(f"{name}_invalid")
    if isinstance(horizon, int) and isinstance(max_steps, int) and max_steps > horizon:
        blockers.append("maximum_plan_steps_exceeds_horizon")
    if constraints.get("reversible_actions_required") is not True:
        blockers.append("reversible_actions_requirement_missing")
    if constraints.get("irreversible_step_requires_checkpoint") is not True:
        blockers.append("irreversible_checkpoint_requirement_missing")
    stop_valid, constraint_stops = _canonical_string_list(
        constraints.get("stop_condition_digests")
    )
    if not stop_valid:
        blockers.append("constraint_stop_conditions_invalid")
    forbidden_valid, forbidden_effects = _canonical_string_list(
        constraints.get("forbidden_effects")
    )
    if not forbidden_valid or tuple(forbidden_effects) != FIXED_FORBIDDEN_EFFECTS:
        blockers.append("forbidden_effects_not_fixed")
    if constraints and synthesis_constraint_digest != compute_synthesis_constraint_digest(
        constraints
    ):
        blockers.append("synthesis_constraint_digest_mismatch")
    if synthesis_constraint_digest != expected_synthesis_constraint_digest:
        blockers.append("synthesis_constraint_source_binding_mismatch")

    if set(plan) != PLAN_FIELDS:
        blockers.append("proposed_plan_schema_invalid")
    for name in (
        "plan_id",
        "selected_candidate_id",
        "selected_candidate_plan_intent_digest",
        "world_state_dependency_digest",
    ):
        if not isinstance(plan.get(name), str) or not plan.get(name):
            blockers.append(f"proposed_{name}_missing")
    if plan.get("selected_candidate_id") != expected_selected_candidate_id:
        blockers.append("proposed_selected_candidate_substituted")
    if (
        plan.get("selected_candidate_plan_intent_digest")
        != expected_selected_candidate_plan_intent_digest
    ):
        blockers.append("proposed_plan_intent_binding_mismatch")
    if plan.get("world_state_dependency_digest") != expected_world_model_state_digest:
        blockers.append("proposed_world_state_dependency_mismatch")
    if plan.get("plan_revision") != 0:
        blockers.append("initial_plan_revision_invalid")
    plan_stop_valid, plan_stops = _canonical_string_list(
        plan.get("stop_condition_digests")
    )
    if not plan_stop_valid or plan_stops != constraint_stops:
        blockers.append("proposed_stop_conditions_mismatch")

    alternatives = plan.get("retained_alternative_records")
    normalized_alternatives: list[dict] = []
    if not isinstance(alternatives, list):
        blockers.append("retained_alternative_records_invalid")
    else:
        seen_alternatives: set[str] = set()
        for index, record in enumerate(alternatives):
            if not isinstance(record, dict) or set(record) != ALTERNATIVE_FIELDS:
                blockers.append(f"alternative_schema_invalid_{index}")
                continue
            candidate_id = record.get("candidate_id")
            reason = record.get("nonselection_reason_digest")
            if not isinstance(candidate_id, str) or not candidate_id:
                blockers.append(f"alternative_candidate_invalid_{index}")
                continue
            if candidate_id == expected_selected_candidate_id:
                blockers.append("selected_candidate_in_alternative_records")
            if candidate_id in seen_alternatives:
                blockers.append("duplicate_alternative_candidate")
            seen_alternatives.add(candidate_id)
            if not isinstance(reason, str) or not reason:
                blockers.append(f"alternative_reason_missing_{index}")
            if record.get("retained_for_revision") is not True:
                blockers.append(f"alternative_not_retained_{index}")
            normalized_alternatives.append(dict(record))
        if alternatives != sorted(alternatives, key=lambda r: r.get("candidate_id", "")):
            blockers.append("alternative_records_not_canonical")
    if alternatives is not None and alternative_lineage_bundle_digest != canonical_digest(
        alternatives
    ):
        blockers.append("alternative_lineage_bundle_digest_mismatch")

    evidence_valid, preserved_evidence = _canonical_string_list(
        plan.get("preserved_evidence_lineage_digests")
    )
    if not evidence_valid:
        blockers.append("preserved_evidence_lineage_invalid")
    if not set(source_dissent).issubset(set(preserved_evidence)):
        blockers.append("source_dissent_not_preserved_in_plan")
    if not set(source_minority).issubset(set(preserved_evidence)):
        blockers.append("source_minority_not_preserved_in_plan")

    steps = plan.get("steps")
    normalized_steps: list[dict] = []
    if not isinstance(steps, list) or not steps:
        blockers.append("proposed_plan_steps_empty")
    elif isinstance(max_steps, int) and len(steps) > max_steps:
        blockers.append("proposed_plan_step_count_exceeds_bound")
    else:
        seen_step_ids: set[str] = set()
        seen_action_digests: set[str] = set()
        checkpoint_ids: set[str] = set()
        all_branch_ids: set[str] = set()
        for index, step in enumerate(steps):
            if not isinstance(step, dict) or set(step) != STEP_FIELDS:
                blockers.append(f"plan_step_schema_invalid_{index}")
                continue
            step_id = step.get("step_id")
            action_class = step.get("action_class")
            action_digest = step.get("action_spec_digest")
            sequence_index = step.get("sequence_index")
            if not isinstance(step_id, str) or not step_id:
                blockers.append(f"plan_step_id_invalid_{index}")
                continue
            if step_id in seen_step_ids:
                blockers.append("duplicate_plan_step_id")
            seen_step_ids.add(step_id)
            if sequence_index != index + 1:
                blockers.append(f"plan_step_sequence_not_contiguous_{index}")
            if action_class not in ALLOWED_ACTION_CLASSES:
                blockers.append(f"plan_step_action_class_invalid_{index}")
            if not isinstance(action_digest, str) or not action_digest:
                blockers.append(f"plan_step_action_digest_invalid_{index}")
            elif action_digest in seen_action_digests:
                blockers.append("duplicate_plan_step_action_digest")
            else:
                seen_action_digests.add(action_digest)
            for name, allow_empty in (
                ("precondition_digests", False),
                ("expected_effect_digests", True),
                ("effect_tags", True),
                ("evidence_lineage_digests", False),
                ("stop_condition_digests", False),
                ("branch_ids", True),
            ):
                valid, values = _canonical_string_list(
                    step.get(name), allow_empty=allow_empty
                )
                if not valid:
                    blockers.append(f"plan_step_{name}_invalid_{index}")
                    values = []
                if name == "effect_tags" and set(values).intersection(
                    set(FIXED_FORBIDDEN_EFFECTS)
                ):
                    blockers.append(f"plan_step_forbidden_effect_{index}")
                if name == "evidence_lineage_digests" and not set(values).issubset(
                    set(preserved_evidence)
                ):
                    blockers.append(f"plan_step_unbound_evidence_{index}")
                if name == "stop_condition_digests" and not set(
                    constraint_stops
                ).issubset(set(values)):
                    blockers.append(f"plan_step_stop_conditions_incomplete_{index}")
                if name == "branch_ids":
                    all_branch_ids.update(values)
            reversible = step.get("reversible")
            irreversible = step.get("irreversible")
            if not isinstance(reversible, bool) or not isinstance(irreversible, bool):
                blockers.append(f"plan_step_reversibility_invalid_{index}")
            elif reversible == irreversible:
                blockers.append(f"plan_step_reversibility_not_exclusive_{index}")
            checkpoint_step_id = step.get("checkpoint_step_id")
            if not isinstance(checkpoint_step_id, str):
                blockers.append(f"plan_step_checkpoint_reference_invalid_{index}")
            elif irreversible:
                if not checkpoint_step_id:
                    blockers.append(f"irreversible_step_checkpoint_missing_{index}")
                elif checkpoint_step_id not in checkpoint_ids:
                    blockers.append(f"irreversible_step_checkpoint_not_prior_{index}")
            elif checkpoint_step_id:
                blockers.append(f"reversible_step_checkpoint_reference_forbidden_{index}")
            if action_class == "review_checkpoint":
                checkpoint_ids.add(step_id)
            normalized_steps.append(dict(step))
        if isinstance(max_branching, int) and len(all_branch_ids) > max_branching:
            blockers.append("plan_branching_factor_exceeds_bound")

    if plan and proposed_plan_digest != compute_proposed_plan_digest(plan):
        blockers.append("proposed_plan_digest_mismatch")

    if not blockers:
        expected_bundle = compute_bounded_synthesis_bundle_digest(
            source_intake_certificate_digest=source_digest,
            expected_source_intake_certificate_digest=(
                expected_source_intake_certificate_digest
            ),
            expected_world_binding_digest=expected_world_binding_digest,
            expected_world_model_state_digest=expected_world_model_state_digest,
            expected_world_model_revision=expected_world_model_revision,
            expected_world_lineage_digest=expected_world_lineage_digest,
            expected_selected_candidate_id=expected_selected_candidate_id,
            expected_selected_candidate_plan_intent_digest=(
                expected_selected_candidate_plan_intent_digest
            ),
            expected_synthesis_constraint_digest=(
                expected_synthesis_constraint_digest
            ),
            synthesis_constraint_digest=synthesis_constraint_digest,
            synthesis_policy_digest=synthesis_policy_digest,
            planos_synthesis_responsibility_digest=(
                planos_synthesis_responsibility_digest
            ),
            synthesis_request_id=synthesis_request_id,
            proposed_plan_digest=proposed_plan_digest,
            alternative_lineage_bundle_digest=alternative_lineage_bundle_digest,
        )
        if synthesis_bundle_digest != expected_bundle:
            blockers.append("synthesis_bundle_digest_mismatch")

    if blockers:
        return PlanOSBoundedSynthesisReceiptResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    resulting_lineage = sorted(
        set(source_resulting_lineage)
        | {
            source_digest,
            proposed_plan_digest,
            synthesis_constraint_digest,
            synthesis_bundle_digest,
        }
    )
    resulting_responsibility = sorted(
        set(source_resulting_responsibility)
        | {planos_synthesis_responsibility_digest}
    )
    receipt = {
        "kernel": "PlanOS Bounded Synthesis Receipt Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.04",
        "status": "PLANOS_BOUNDED_SYNTHESIS_RECEIPT_ISSUED",
        "source_intake_certificate_digest": source_digest,
        "source_verifyos_certificate_digest": source[
            "source_verifyos_certificate_digest"
        ],
        "source_decisionos_handoff_receipt_digest": source[
            "source_decisionos_handoff_receipt_digest"
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "source_synthesis_constraint_digest": source[
            "source_synthesis_constraint_digest"
        ],
        "selected_candidate_id": expected_selected_candidate_id,
        "selected_candidate_plan_intent_digest": (
            expected_selected_candidate_plan_intent_digest
        ),
        "synthesis_constraints": constraints,
        "synthesis_constraint_digest": synthesis_constraint_digest,
        "synthesis_policy_digest": synthesis_policy_digest,
        "planos_synthesis_responsibility_digest": (
            planos_synthesis_responsibility_digest
        ),
        "synthesis_request_id": synthesis_request_id,
        "proposed_plan_digest": proposed_plan_digest,
        "alternative_lineage_bundle_digest": alternative_lineage_bundle_digest,
        "synthesis_bundle_digest": synthesis_bundle_digest,
        "plan_id": plan["plan_id"],
        "plan_revision": plan["plan_revision"],
        "planning_horizon": constraints["planning_horizon"],
        "maximum_plan_steps": constraints["maximum_plan_steps"],
        "maximum_branching_factor": constraints["maximum_branching_factor"],
        "maximum_revision_cycles": constraints["maximum_revision_cycles"],
        "plan_step_count": len(normalized_steps),
        "plan_steps": normalized_steps,
        "stop_condition_digests": plan_stops,
        "retained_alternative_records": normalized_alternatives,
        "preserved_evidence_lineage_digests": preserved_evidence,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
        "selected_candidate_not_substituted": True,
        "plan_intent_binding_preserved": True,
        "world_state_dependency_preserved": True,
        "finite_plan_constructed": True,
        "planning_horizon_bounded": True,
        "plan_step_count_bounded": True,
        "branching_factor_bounded": True,
        "revision_cycles_bounded": True,
        "reversible_actions_default_preserved": True,
        "irreversible_steps_checkpoint_guarded": True,
        "stop_conditions_preserved": True,
        "forbidden_effects_absent": True,
        "alternative_candidates_retained": True,
        "dissent_evidence_preserved": True,
        "minority_evidence_preserved": True,
        "lineage_extended_not_replaced": True,
        "responsibility_extended_not_replaced": True,
        "plan_is_conditionally_binding": True,
        "plan_is_not_absolute_command": True,
        "plan_is_not_contentless_proposal": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_planos": False,
        "plan_synthesis_performed": True,
        "concrete_plan_issued": True,
        "plan_receipt_issued": True,
        "plan_activated": False,
        "materialization_performed": False,
        "actos_authorization_required": True,
        "verifyos_reverification_required_before_irreversible_step": True,
        "execution_authority_granted": False,
        "execution_permission": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
    }
    receipt["concrete_plan_digest"] = canonical_digest(
        {
            "plan_id": receipt["plan_id"],
            "plan_revision": receipt["plan_revision"],
            "selected_candidate_id": receipt["selected_candidate_id"],
            "selected_candidate_plan_intent_digest": receipt[
                "selected_candidate_plan_intent_digest"
            ],
            "source_world_model_state_digest": receipt[
                "source_world_model_state_digest"
            ],
            "plan_steps": receipt["plan_steps"],
            "stop_condition_digests": receipt["stop_condition_digests"],
            "retained_alternative_records": receipt[
                "retained_alternative_records"
            ],
            "preserved_evidence_lineage_digests": receipt[
                "preserved_evidence_lineage_digests"
            ],
        }
    )
    receipt["planos_bounded_synthesis_receipt_digest"] = canonical_digest(receipt)
    return PlanOSBoundedSynthesisReceiptResult(STATUS_READY, [], receipt)
