#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DECISIONOS_VERSION = "v0.8"
SOURCE_STATUS = "DECISIONOS_BOUNDED_PLAN_SYNTHESIS_REQUEST_HANDOFF_ISSUED"
TRANSITION_TO_STATUS = {
    "retain": "valid",
    "suspend": "suspended",
    "request_revision": "revision_required",
    "supersede_with_lineage": "superseded",
    "complete": "completed",
    "terminate": "terminated",
}
TRANSITION_FIELDS = {
    "source_object_digest",
    "predecessor_state_digest",
    "proposed_state_digest",
    "source_condition_digests",
    "current_condition_digests",
    "changed_condition_digests",
    "source_lineage_digests",
    "resulting_lineage_digests",
    "predecessor_reference_digest",
    "source_responsibility_lineage_digests",
    "resulting_responsibility_lineage_digests",
    "transition_kind",
    "transition_reason_digest",
    "conditional_validity_status",
    "preserved_dissent_evidence_digests",
    "preserved_minority_evidence_digests",
    "object_eternal_truth_claimed",
    "object_disposable_null_claimed",
    "silent_rewrite_requested",
    "history_erasure_requested",
    "authority_expansion_requested",
    "execution_permission_requested",
    "persistent_world_mutation_requested",
}


@dataclass
class VerifyOSMiddleWayConditionalContinuityResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def _canonical_string_list(
    value: Any, *, allow_empty: bool = False
) -> tuple[bool, list[str]]:
    if not isinstance(value, list):
        return False, []
    if not allow_empty and not value:
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if len(value) != len(set(value)) or value != sorted(value):
        return False, []
    return True, list(value)


def _flatten_digest_map(value: Any) -> tuple[bool, list[str]]:
    if not isinstance(value, dict):
        return False, []
    flattened: list[str] = []
    for key in sorted(value):
        if not isinstance(key, str) or not key:
            return False, []
        valid, digests = _canonical_string_list(value[key], allow_empty=True)
        if not valid:
            return False, []
        flattened.extend(digests)
    return True, sorted(set(flattened))


def compute_transition_spec_digest(spec: Mapping[str, Any]) -> str:
    return canonical_digest(dict(spec))


def compute_verification_bundle_digest(
    *,
    source_handoff_receipt_digest: str,
    verification_policy_digest: str,
    verification_owner_responsibility_digest: str,
    verification_request_id: str,
    transition_spec_digest: str,
    transition_spec: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_handoff_receipt_digest": source_handoff_receipt_digest,
            "verification_policy_digest": verification_policy_digest,
            "verification_owner_responsibility_digest": (
                verification_owner_responsibility_digest
            ),
            "verification_request_id": verification_request_id,
            "transition_spec_digest": transition_spec_digest,
            "transition_spec": dict(transition_spec),
        }
    )


def build_verifyos_middle_way_conditional_continuity_certificate(
    *,
    source_handoff_receipt: Mapping[str, Any],
    verification_policy_digest: str,
    verification_owner_responsibility_digest: str,
    verification_request_id: str,
    transition_spec: Mapping[str, Any],
    transition_spec_digest: str,
    verification_bundle_digest: str,
) -> VerifyOSMiddleWayConditionalContinuityResult:
    blockers: list[str] = []
    source = (
        dict(source_handoff_receipt)
        if isinstance(source_handoff_receipt, Mapping)
        else {}
    )
    spec = dict(transition_spec) if isinstance(transition_spec, Mapping) else {}

    if not source:
        blockers.append("source_handoff_receipt_missing")
    for name, value in {
        "verification_policy_digest": verification_policy_digest,
        "verification_owner_responsibility_digest": (
            verification_owner_responsibility_digest
        ),
        "verification_request_id": verification_request_id,
        "transition_spec_digest": transition_spec_digest,
        "verification_bundle_digest": verification_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    source_receipt_digest = ""
    source_dissent: list[str] = []
    source_minority: list[str] = []
    if source:
        if source.get("decisionos_version") != SOURCE_DECISIONOS_VERSION:
            blockers.append("source_decisionos_version_invalid")
        if source.get("status") != SOURCE_STATUS:
            blockers.append("source_handoff_not_issued")
        raw_digest = source.get(
            "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
        )
        if not isinstance(raw_digest, str) or not raw_digest:
            blockers.append("source_handoff_receipt_digest_missing")
        else:
            source_receipt_digest = raw_digest
            unsigned = dict(source)
            unsigned.pop(
                "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest",
                None,
            )
            if raw_digest != canonical_digest(unsigned):
                blockers.append("source_handoff_receipt_digest_mismatch")
        for name in (
            "source_selection_receipt_digest",
            "source_world_binding_digest",
            "source_world_model_state_digest",
            "source_world_lineage_digest",
            "synthesis_constraint_digest",
            "synthesis_handoff_bundle_digest",
            "selected_candidate_id",
            "selected_candidate_plan_intent_digest",
        ):
            if not isinstance(source.get(name), str) or not source.get(name):
                blockers.append(f"source_{name}_missing")
        required_true = (
            "selected_candidate_not_substituted",
            "selection_remains_decisionos_owned",
            "candidate_evidence_lineage_preserved",
            "retained_alternatives_visible_to_synthesis",
            "retained_nonadmissible_candidates_visible",
            "nonselection_reasons_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "required_review_field_preserved",
            "planning_horizon_bounded",
            "plan_step_count_bounded",
            "branching_factor_bounded",
            "revision_cycles_bounded",
            "reversible_actions_required",
            "irreversible_step_requires_checkpoint",
            "stop_conditions_present",
            "forbidden_effects_fixed",
            "plan_synthesis_request_issued",
            "planos_synthesis_scope_bounded",
            "planos_receives_request_not_selection_authority",
            "planos_plan_receipt_required",
            "plan_synthesis_result_not_accepted_without_receipt",
            "persistent_world_state_unchanged",
            "world_model_prediction_not_truth",
            "world_mutation_not_granted",
            "history_read_only",
            "qi_grants_no_authority",
            "future_only",
        )
        required_false = (
            "selection_authority_transferred_to_planos",
            "execution_authority_granted_to_planos",
            "plan_synthesis_performed",
            "concrete_plan_issued",
            "plan_receipt_issued",
            "active_now",
            "execution_permission",
        )
        for name in required_true:
            if source.get(name) is not True:
                blockers.append(f"source_boundary_{name}_missing")
        for name in required_false:
            if source.get(name) is not False:
                blockers.append(f"source_boundary_{name}_promoted")
        dissent_valid, source_dissent = _flatten_digest_map(
            source.get("dissent_preservation_map")
        )
        minority_valid, source_minority = _flatten_digest_map(
            source.get("minority_preservation_map")
        )
        if not dissent_valid:
            blockers.append("source_dissent_preservation_map_invalid")
        if not minority_valid:
            blockers.append("source_minority_preservation_map_invalid")

    if set(spec) != TRANSITION_FIELDS:
        blockers.append("transition_spec_schema_invalid")

    string_fields = (
        "source_object_digest",
        "predecessor_state_digest",
        "proposed_state_digest",
        "predecessor_reference_digest",
        "transition_kind",
        "transition_reason_digest",
        "conditional_validity_status",
    )
    for name in string_fields:
        if not isinstance(spec.get(name), str) or not spec.get(name):
            blockers.append(f"{name}_missing")

    transition_kind = spec.get("transition_kind")
    expected_status = TRANSITION_TO_STATUS.get(transition_kind)
    if expected_status is None:
        blockers.append("transition_kind_invalid")
    elif spec.get("conditional_validity_status") != expected_status:
        blockers.append("transition_status_mismatch")

    normalized_lists: dict[str, list[str]] = {}
    for name, allow_empty in (
        ("source_condition_digests", False),
        ("current_condition_digests", False),
        ("changed_condition_digests", True),
        ("source_lineage_digests", False),
        ("resulting_lineage_digests", False),
        ("source_responsibility_lineage_digests", False),
        ("resulting_responsibility_lineage_digests", False),
        ("preserved_dissent_evidence_digests", True),
        ("preserved_minority_evidence_digests", True),
    ):
        valid, values = _canonical_string_list(
            spec.get(name), allow_empty=allow_empty
        )
        if not valid:
            blockers.append(f"{name}_invalid")
        normalized_lists[name] = values

    source_conditions = set(normalized_lists["source_condition_digests"])
    current_conditions = set(normalized_lists["current_condition_digests"])
    changed_conditions = set(normalized_lists["changed_condition_digests"])
    expected_changed = source_conditions.symmetric_difference(current_conditions)
    if changed_conditions != expected_changed:
        blockers.append("changed_condition_set_mismatch")
    if transition_kind == "retain" and expected_changed:
        blockers.append("retain_with_changed_conditions_forbidden")
    if transition_kind != "retain" and not expected_changed:
        blockers.append("nonretain_requires_condition_change")

    source_lineage = set(normalized_lists["source_lineage_digests"])
    resulting_lineage = set(normalized_lists["resulting_lineage_digests"])
    if not source_lineage.issubset(resulting_lineage):
        blockers.append("lineage_not_monotone")
    if spec.get("predecessor_reference_digest") not in resulting_lineage:
        blockers.append("predecessor_reference_not_preserved")
    if spec.get("source_object_digest") not in resulting_lineage:
        blockers.append("source_object_not_preserved_in_lineage")
    if (
        source_receipt_digest
        and spec.get("source_object_digest") != source_receipt_digest
    ):
        blockers.append("source_object_digest_mismatch")

    source_resp = set(
        normalized_lists["source_responsibility_lineage_digests"]
    )
    resulting_resp = set(
        normalized_lists["resulting_responsibility_lineage_digests"]
    )
    if not source_resp.issubset(resulting_resp):
        blockers.append("responsibility_lineage_not_monotone")
    if verification_owner_responsibility_digest not in resulting_resp:
        blockers.append("verification_owner_not_retained")

    if not set(source_dissent).issubset(
        set(normalized_lists["preserved_dissent_evidence_digests"])
    ):
        blockers.append("dissent_evidence_erased")
    if not set(source_minority).issubset(
        set(normalized_lists["preserved_minority_evidence_digests"])
    ):
        blockers.append("minority_evidence_erased")

    for name in (
        "object_eternal_truth_claimed",
        "object_disposable_null_claimed",
        "silent_rewrite_requested",
        "history_erasure_requested",
        "authority_expansion_requested",
        "execution_permission_requested",
        "persistent_world_mutation_requested",
    ):
        value = spec.get(name)
        if not isinstance(value, bool):
            blockers.append(f"{name}_invalid")
        elif value:
            blockers.append(f"{name}_forbidden")

    if spec and transition_spec_digest != compute_transition_spec_digest(spec):
        blockers.append("transition_spec_digest_mismatch")
    if not blockers:
        expected_bundle = compute_verification_bundle_digest(
            source_handoff_receipt_digest=source_receipt_digest,
            verification_policy_digest=verification_policy_digest,
            verification_owner_responsibility_digest=(
                verification_owner_responsibility_digest
            ),
            verification_request_id=verification_request_id,
            transition_spec_digest=transition_spec_digest,
            transition_spec=spec,
        )
        if verification_bundle_digest != expected_bundle:
            blockers.append("verification_bundle_digest_mismatch")

    if blockers:
        return VerifyOSMiddleWayConditionalContinuityResult(
            STATUS_BLOCKED,
            sorted(set(blockers)),
            None,
        )

    certificate = {
        "kernel": "VerifyOS Middle-Way Conditional Continuity Verification Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.4",
        "status": "VERIFYOS_MIDDLE_WAY_CONDITIONAL_CONTINUITY_VERIFIED",
        "source_decisionos_version": source["decisionos_version"],
        "source_handoff_receipt_digest": source_receipt_digest,
        "source_selection_receipt_digest": source[
            "source_selection_receipt_digest"
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "source_synthesis_constraint_digest": source[
            "synthesis_constraint_digest"
        ],
        "source_synthesis_handoff_bundle_digest": source[
            "synthesis_handoff_bundle_digest"
        ],
        "selected_candidate_id": source["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": source[
            "selected_candidate_plan_intent_digest"
        ],
        "verification_policy_digest": verification_policy_digest,
        "verification_owner_responsibility_digest": (
            verification_owner_responsibility_digest
        ),
        "verification_request_id": verification_request_id,
        "transition_spec": spec,
        "transition_spec_digest": transition_spec_digest,
        "verification_bundle_digest": verification_bundle_digest,
        "conditional_validity_status": spec["conditional_validity_status"],
        "transition_kind": spec["transition_kind"],
        "transition_reason_digest": spec["transition_reason_digest"],
        "conditions_explicit": True,
        "changed_conditions_explicit": True,
        "predecessor_preserved": True,
        "lineage_monotone": True,
        "responsibility_preserved": True,
        "dissent_preserved": True,
        "minority_evidence_preserved": True,
        "object_not_reified": True,
        "object_not_erased": True,
        "commitment_not_absolutized": True,
        "revision_preserves_lineage": True,
        "supersession_preserves_predecessor": True,
        "termination_does_not_erase_history": True,
        "condition_change_may_trigger_revision": True,
        "condition_change_does_not_silently_rewrite": True,
        "emptiness_does_not_imply_irresponsibility": True,
        "commitment_does_not_imply_reification": True,
        "selection_remains_decisionos_owned": True,
        "planos_receives_verified_request_not_selection_authority": True,
        "authority_unchanged": True,
        "execution_permission_not_granted": True,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "plan_synthesis_performed": False,
        "concrete_plan_issued": False,
        "plan_receipt_issued": False,
        "verification_passed": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate[
        "verifyos_middle_way_conditional_continuity_certificate_digest"
    ] = canonical_digest(certificate)
    return VerifyOSMiddleWayConditionalContinuityResult(
        STATUS_READY,
        [],
        certificate,
    )
