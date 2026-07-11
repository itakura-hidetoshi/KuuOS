#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DECISIONOS_VERSION = "v0.7"
SOURCE_STATUS = "DECISIONOS_WORLD_CONDITIONED_SELECTION_JUSTIFICATION_ISSUED"
CANDIDATE_FIELD = {
    "continue",
    "strengthen",
    "repair",
    "slow_down",
    "reobserve",
    "reroute",
    "hold",
    "terminate_candidate",
}
FORBIDDEN_EFFECTS = {
    "active_now",
    "candidate_substitution",
    "execution_permission",
    "external_side_effect",
    "persistent_world_mutation",
    "selection_authority_transfer",
    "tool_invocation",
    "unreviewed_scope_expansion",
}
CONSTRAINT_FIELDS = {
    "planning_horizon_steps",
    "maximum_plan_steps",
    "maximum_branching_factor",
    "maximum_revision_cycles",
    "require_reversible_actions",
    "require_checkpoint_before_irreversible_step",
    "required_checkpoint_digests",
    "stop_condition_digests",
    "preserved_evidence_digests",
    "forbidden_effects",
}
SOURCE_JUSTIFICATION_FIELDS = {
    "candidate_id",
    "source_deliberation_record_digest",
    "selected",
    "support_rationale_digests",
    "opposition_rationale_digests",
    "dissent_preservation_digests",
    "minority_preservation_digests",
    "review_resolution_digests",
    "nonselection_reason_digest",
    "candidate_selection_justification_digest",
}


@dataclass
class DecisionOSBoundedPlanSynthesisRequestHandoffResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def _string_list(value: Any) -> tuple[bool, list[str]]:
    if not isinstance(value, list):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def compute_source_candidate_selection_justification_digest(
    item: Mapping[str, Any],
) -> str:
    payload = dict(item)
    payload.pop("candidate_selection_justification_digest", None)
    return canonical_digest(payload)


def compute_source_selection_bundle_digest(source: Mapping[str, Any]) -> str:
    items = source.get("candidate_selection_justification_items", [])
    ordered = sorted(
        list(items) if isinstance(items, list) else [],
        key=lambda item: str(item.get("candidate_id", ""))
        if isinstance(item, Mapping)
        else "",
    )
    return canonical_digest(
        {
            "source_deliberation_receipt_digest": source.get(
                "source_deliberation_receipt_digest", ""
            ),
            "selection_policy_digest": source.get("selection_policy_digest", ""),
            "selector_responsibility_digest": source.get(
                "selector_responsibility_digest", ""
            ),
            "requested_selected_candidate_id": source.get(
                "selected_candidate_id", ""
            ),
            "hold_guard_resolution_digest": source.get(
                "hold_guard_resolution_digest", ""
            ),
            "candidate_selection_justification_items": ordered,
        }
    )


def compute_synthesis_constraint_digest(spec: Mapping[str, Any]) -> str:
    return canonical_digest(dict(spec))


def compute_synthesis_handoff_bundle_digest(
    *,
    source_selection_receipt_digest: str,
    synthesis_policy_digest: str,
    planos_recipient_digest: str,
    request_owner_responsibility_digest: str,
    synthesis_request_id: str,
    requested_selected_candidate_id: str,
    selected_candidate_plan_intent_digest: str,
    synthesis_constraint_digest: str,
    synthesis_constraint_spec: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_selection_receipt_digest": source_selection_receipt_digest,
            "synthesis_policy_digest": synthesis_policy_digest,
            "planos_recipient_digest": planos_recipient_digest,
            "request_owner_responsibility_digest": (
                request_owner_responsibility_digest
            ),
            "synthesis_request_id": synthesis_request_id,
            "requested_selected_candidate_id": requested_selected_candidate_id,
            "selected_candidate_plan_intent_digest": (
                selected_candidate_plan_intent_digest
            ),
            "synthesis_constraint_digest": synthesis_constraint_digest,
            "synthesis_constraint_spec": dict(synthesis_constraint_spec),
        }
    )


def build_decisionos_bounded_plan_synthesis_request_handoff_receipt(
    *,
    source_selection_receipt: Mapping[str, Any],
    synthesis_policy_digest: str,
    planos_recipient_digest: str,
    request_owner_responsibility_digest: str,
    synthesis_request_id: str,
    requested_selected_candidate_id: str,
    selected_candidate_plan_intent_digest: str,
    synthesis_constraint_spec: Mapping[str, Any],
    synthesis_constraint_digest: str,
    synthesis_handoff_bundle_digest: str,
) -> DecisionOSBoundedPlanSynthesisRequestHandoffResult:
    blockers: list[str] = []
    source = (
        dict(source_selection_receipt)
        if isinstance(source_selection_receipt, Mapping)
        else {}
    )
    spec = (
        dict(synthesis_constraint_spec)
        if isinstance(synthesis_constraint_spec, Mapping)
        else {}
    )

    if not source:
        blockers.append("source_selection_receipt_missing")
    for name, value in {
        "synthesis_policy_digest": synthesis_policy_digest,
        "planos_recipient_digest": planos_recipient_digest,
        "request_owner_responsibility_digest": request_owner_responsibility_digest,
        "synthesis_request_id": synthesis_request_id,
        "requested_selected_candidate_id": requested_selected_candidate_id,
        "selected_candidate_plan_intent_digest": selected_candidate_plan_intent_digest,
        "synthesis_constraint_digest": synthesis_constraint_digest,
        "synthesis_handoff_bundle_digest": synthesis_handoff_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    source_receipt_digest = ""
    source_selected_candidate_id = ""
    selected_source_record_digest = ""
    selected_support: list[str] = []
    selected_opposition: list[str] = []
    retained_alternatives: list[str] = []
    retained_nonadmissible: list[str] = []
    source_items: list[dict] = []

    if source:
        if source.get("decisionos_version") != SOURCE_DECISIONOS_VERSION:
            blockers.append("source_decisionos_version_invalid")
        if source.get("status") != SOURCE_STATUS:
            blockers.append("source_selection_receipt_not_issued")

        raw_digest = source.get("decisionos_selection_justification_receipt_digest")
        if not isinstance(raw_digest, str) or not raw_digest:
            blockers.append("source_selection_receipt_digest_missing")
        else:
            source_receipt_digest = raw_digest
            unsigned = dict(source)
            unsigned.pop("decisionos_selection_justification_receipt_digest", None)
            if raw_digest != canonical_digest(unsigned):
                blockers.append("source_selection_receipt_digest_mismatch")

        required_true = (
            "all_candidates_considered",
            "candidate_identity_preserved",
            "retained_alternatives_preserved",
            "nonselected_reasons_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "required_review_field_preserved",
            "source_probability_used_as_advisory_only",
            "source_action_used_as_advisory_only",
            "relational_partial_order_used",
            "single_scalar_utility_selection_forbidden",
            "selected_candidate_from_relational_frontier",
            "selection_authority_exercised_by_decision_os",
            "decision_selection_performed",
            "selected_candidate_present",
            "decision_receipt_issued",
            "selection_is_not_plan_synthesis",
            "selection_is_not_execution",
            "persistent_world_state_unchanged",
            "world_model_prediction_not_truth",
            "world_mutation_not_granted",
            "history_read_only",
            "qi_grants_no_authority",
            "future_only",
        )
        required_false = (
            "silent_substitution_detected",
            "selection_authority_inherited_from_planos",
            "selection_authority_inherited_from_world_model",
            "selection_authority_inherited_from_qi",
            "plan_synthesis_performed",
            "active_now",
            "execution_permission",
        )
        for name in required_true:
            if source.get(name) is not True:
                blockers.append(f"source_boundary_{name}_missing")
        for name in required_false:
            if source.get(name) is not False:
                blockers.append(f"source_boundary_{name}_promoted")

        for name in (
            "source_deliberation_receipt_digest",
            "source_intake_receipt_digest",
            "source_planos_handoff_certificate_digest",
            "source_world_binding_digest",
            "source_world_model_state_digest",
            "source_world_lineage_digest",
            "selection_policy_digest",
            "selector_responsibility_digest",
            "selection_bundle_digest",
        ):
            if not isinstance(source.get(name), str) or not source.get(name):
                blockers.append(f"source_{name}_missing")
        revision = source.get("source_world_model_revision")
        if not _is_int(revision) or revision < 0:
            blockers.append("source_world_model_revision_invalid")

        source_selected_candidate_id = source.get("selected_candidate_id", "")
        if (
            not isinstance(source_selected_candidate_id, str)
            or source_selected_candidate_id not in CANDIDATE_FIELD
        ):
            blockers.append("source_selected_candidate_invalid")
        if requested_selected_candidate_id != source_selected_candidate_id:
            blockers.append("selected_candidate_substitution_detected")

        frontier_valid, frontier = _string_list(
            source.get("relational_frontier_candidate_ids")
        )
        if not frontier_valid or source_selected_candidate_id not in frontier:
            blockers.append("source_selected_candidate_not_relational_frontier")

        alternatives_valid, alternatives = _string_list(
            source.get("retained_alternative_candidate_ids")
        )
        if (
            not alternatives_valid
            or any(item not in CANDIDATE_FIELD for item in alternatives)
            or source_selected_candidate_id in alternatives
        ):
            blockers.append("source_retained_alternatives_invalid")
        else:
            retained_alternatives = sorted(alternatives)

        nonadmissible_valid, nonadmissible = _string_list(
            source.get("retained_nonadmissible_candidate_ids")
        )
        if (
            not nonadmissible_valid
            or any(item not in CANDIDATE_FIELD for item in nonadmissible)
            or source_selected_candidate_id in nonadmissible
        ):
            blockers.append("source_retained_nonadmissible_invalid")
        else:
            retained_nonadmissible = sorted(nonadmissible)

        raw_items = source.get("candidate_selection_justification_items")
        item_map: dict[str, dict] = {}
        selected_flags: list[str] = []
        if not isinstance(raw_items, list) or not raw_items:
            blockers.append("source_candidate_selection_items_missing")
        else:
            for index, raw_item in enumerate(raw_items):
                if (
                    not isinstance(raw_item, dict)
                    or set(raw_item) != SOURCE_JUSTIFICATION_FIELDS
                ):
                    blockers.append(f"source_candidate_item_schema_invalid_{index}")
                    continue
                item = dict(raw_item)
                candidate_id = item.get("candidate_id")
                if (
                    not isinstance(candidate_id, str)
                    or candidate_id not in CANDIDATE_FIELD
                ):
                    blockers.append(f"source_candidate_item_id_invalid_{index}")
                    continue
                if candidate_id in item_map:
                    blockers.append("source_candidate_item_id_duplicate")
                item_map[candidate_id] = item
                if item.get("candidate_selection_justification_digest") != (
                    compute_source_candidate_selection_justification_digest(item)
                ):
                    blockers.append(
                        f"source_candidate_item_digest_mismatch_{candidate_id}"
                    )
                for field in (
                    "support_rationale_digests",
                    "opposition_rationale_digests",
                    "dissent_preservation_digests",
                    "minority_preservation_digests",
                    "review_resolution_digests",
                ):
                    valid, _ = _string_list(item.get(field))
                    if not valid:
                        blockers.append(
                            f"source_candidate_{field}_invalid_{candidate_id}"
                        )
                if not isinstance(item.get("selected"), bool):
                    blockers.append(f"source_candidate_selected_invalid_{candidate_id}")
                elif item["selected"]:
                    selected_flags.append(candidate_id)
                    if candidate_id != source_selected_candidate_id:
                        blockers.append("source_selected_flag_candidate_mismatch")
                    support_valid, support = _string_list(
                        item.get("support_rationale_digests")
                    )
                    opposition_valid, opposition = _string_list(
                        item.get("opposition_rationale_digests")
                    )
                    if not support_valid or not support:
                        blockers.append("source_selected_support_missing")
                    else:
                        selected_support = support
                    if opposition_valid:
                        selected_opposition = opposition
                    if item.get("nonselection_reason_digest") != "":
                        blockers.append("source_selected_nonselection_reason_forbidden")
                    selected_source_record_digest = item.get(
                        "source_deliberation_record_digest", ""
                    )
                else:
                    reason = item.get("nonselection_reason_digest")
                    if not isinstance(reason, str) or not reason:
                        blockers.append(
                            f"source_nonselected_reason_missing_{candidate_id}"
                        )
            source_items = [item_map[key] for key in sorted(item_map)]
            if selected_flags != [source_selected_candidate_id]:
                blockers.append("source_selected_candidate_flag_not_unique")

            nonselection_reason_map = source.get("nonselection_reason_map")
            expected_nonselection = {
                candidate_id: item_map[candidate_id]["nonselection_reason_digest"]
                for candidate_id in sorted(
                    set(item_map) - {source_selected_candidate_id}
                )
            }
            if nonselection_reason_map != expected_nonselection:
                blockers.append("source_nonselection_reason_map_mismatch")

        if source.get("selected_candidate_source_record_digest") != (
            selected_source_record_digest
        ):
            blockers.append("source_selected_record_digest_mismatch")
        if source.get("selected_candidate_support_rationale_digests") != (
            selected_support
        ):
            blockers.append("source_selected_support_map_mismatch")
        if source.get("selected_candidate_opposition_rationale_digests") != (
            selected_opposition
        ):
            blockers.append("source_selected_opposition_map_mismatch")
        if source.get("selection_bundle_digest") != (
            compute_source_selection_bundle_digest(source)
        ):
            blockers.append("source_selection_bundle_digest_mismatch")

        for field in (
            "dissent_preservation_map",
            "minority_preservation_map",
            "review_resolution_map",
        ):
            value = source.get(field)
            if not isinstance(value, dict):
                blockers.append(f"source_{field}_invalid")
            else:
                for candidate_id, digests in value.items():
                    valid, _ = _string_list(digests)
                    if candidate_id not in CANDIDATE_FIELD or not valid:
                        blockers.append(f"source_{field}_entry_invalid")

    if set(spec) != CONSTRAINT_FIELDS:
        blockers.append("synthesis_constraint_schema_invalid")

    horizon = spec.get("planning_horizon_steps")
    max_steps = spec.get("maximum_plan_steps")
    branching = spec.get("maximum_branching_factor")
    revisions = spec.get("maximum_revision_cycles")
    if not _is_int(horizon) or not 1 <= horizon <= 64:
        blockers.append("planning_horizon_steps_invalid")
    if (
        not _is_int(max_steps)
        or not 1 <= max_steps <= 32
        or (_is_int(horizon) and max_steps > horizon)
    ):
        blockers.append("maximum_plan_steps_invalid")
    if not _is_int(branching) or not 1 <= branching <= 8:
        blockers.append("maximum_branching_factor_invalid")
    if not _is_int(revisions) or not 0 <= revisions <= 8:
        blockers.append("maximum_revision_cycles_invalid")
    if spec.get("require_reversible_actions") is not True:
        blockers.append("reversible_actions_requirement_missing")
    if spec.get("require_checkpoint_before_irreversible_step") is not True:
        blockers.append("irreversible_step_checkpoint_requirement_missing")

    normalized_lists: dict[str, list[str]] = {}
    for field in (
        "required_checkpoint_digests",
        "stop_condition_digests",
        "preserved_evidence_digests",
        "forbidden_effects",
    ):
        valid, values = _string_list(spec.get(field))
        if not valid or not values:
            blockers.append(f"{field}_invalid")
        elif values != sorted(values):
            blockers.append(f"{field}_not_canonical")
        normalized_lists[field] = values

    if set(normalized_lists.get("forbidden_effects", [])) != FORBIDDEN_EFFECTS:
        blockers.append("forbidden_effects_field_mismatch")

    required_evidence = {
        source_receipt_digest,
        selected_source_record_digest,
        source.get("source_planos_handoff_certificate_digest", ""),
        source.get("source_world_binding_digest", ""),
        source.get("source_world_model_state_digest", ""),
        source.get("source_world_lineage_digest", ""),
        *selected_support,
        *selected_opposition,
    }
    required_evidence.discard("")
    if not required_evidence.issubset(
        set(normalized_lists.get("preserved_evidence_digests", []))
    ):
        blockers.append("preserved_evidence_lineage_incomplete")

    if spec and synthesis_constraint_digest != compute_synthesis_constraint_digest(spec):
        blockers.append("synthesis_constraint_digest_mismatch")

    if not blockers:
        expected_bundle = compute_synthesis_handoff_bundle_digest(
            source_selection_receipt_digest=source_receipt_digest,
            synthesis_policy_digest=synthesis_policy_digest,
            planos_recipient_digest=planos_recipient_digest,
            request_owner_responsibility_digest=request_owner_responsibility_digest,
            synthesis_request_id=synthesis_request_id,
            requested_selected_candidate_id=requested_selected_candidate_id,
            selected_candidate_plan_intent_digest=(
                selected_candidate_plan_intent_digest
            ),
            synthesis_constraint_digest=synthesis_constraint_digest,
            synthesis_constraint_spec=spec,
        )
        if synthesis_handoff_bundle_digest != expected_bundle:
            blockers.append("synthesis_handoff_bundle_digest_mismatch")

    if blockers:
        return DecisionOSBoundedPlanSynthesisRequestHandoffResult(
            STATUS_BLOCKED,
            sorted(set(blockers)),
            None,
        )

    receipt = {
        "kernel": "DecisionOS Bounded Plan Synthesis Request Handoff Kernel",
        "kernel_version": "v0.1",
        "decisionos_version": "v0.8",
        "status": "DECISIONOS_BOUNDED_PLAN_SYNTHESIS_REQUEST_HANDOFF_ISSUED",
        "source_decisionos_version": source["decisionos_version"],
        "source_selection_receipt_digest": source_receipt_digest,
        "source_deliberation_receipt_digest": source[
            "source_deliberation_receipt_digest"
        ],
        "source_intake_receipt_digest": source["source_intake_receipt_digest"],
        "source_planos_handoff_certificate_digest": source[
            "source_planos_handoff_certificate_digest"
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "source_selection_policy_digest": source["selection_policy_digest"],
        "source_selector_responsibility_digest": source[
            "selector_responsibility_digest"
        ],
        "synthesis_policy_digest": synthesis_policy_digest,
        "planos_recipient_digest": planos_recipient_digest,
        "request_owner_responsibility_digest": (
            request_owner_responsibility_digest
        ),
        "synthesis_request_id": synthesis_request_id,
        "selected_candidate_id": source_selected_candidate_id,
        "selected_candidate_source_record_digest": (
            selected_source_record_digest
        ),
        "selected_candidate_plan_intent_digest": (
            selected_candidate_plan_intent_digest
        ),
        "selected_candidate_support_rationale_digests": selected_support,
        "selected_candidate_opposition_rationale_digests": selected_opposition,
        "retained_alternative_candidate_ids": retained_alternatives,
        "retained_nonadmissible_candidate_ids": retained_nonadmissible,
        "candidate_selection_justification_items": source_items,
        "nonselection_reason_map": source["nonselection_reason_map"],
        "dissent_preservation_map": source["dissent_preservation_map"],
        "minority_preservation_map": source["minority_preservation_map"],
        "review_resolution_map": source["review_resolution_map"],
        "synthesis_constraint_spec": spec,
        "synthesis_constraint_digest": synthesis_constraint_digest,
        "synthesis_handoff_bundle_digest": synthesis_handoff_bundle_digest,
        "selected_candidate_not_substituted": True,
        "selection_remains_decisionos_owned": True,
        "candidate_evidence_lineage_preserved": True,
        "retained_alternatives_visible_to_synthesis": True,
        "retained_nonadmissible_candidates_visible": True,
        "nonselection_reasons_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "required_review_field_preserved": True,
        "planning_horizon_bounded": True,
        "plan_step_count_bounded": True,
        "branching_factor_bounded": True,
        "revision_cycles_bounded": True,
        "reversible_actions_required": True,
        "irreversible_step_requires_checkpoint": True,
        "stop_conditions_present": True,
        "forbidden_effects_fixed": True,
        "plan_synthesis_request_issued": True,
        "planos_synthesis_scope_bounded": True,
        "planos_receives_request_not_selection_authority": True,
        "selection_authority_transferred_to_planos": False,
        "execution_authority_granted_to_planos": False,
        "planos_plan_receipt_required": True,
        "plan_synthesis_result_not_accepted_without_receipt": True,
        "plan_synthesis_performed": False,
        "concrete_plan_issued": False,
        "plan_receipt_issued": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    receipt["decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"] = (
        canonical_digest(receipt)
    )
    return DecisionOSBoundedPlanSynthesisRequestHandoffResult(
        STATUS_READY,
        [],
        receipt,
    )
