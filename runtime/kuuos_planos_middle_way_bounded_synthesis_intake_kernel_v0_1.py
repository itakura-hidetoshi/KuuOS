#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_KERNEL = "VerifyOS Middle-Way Conditional Continuity Verification Kernel"
SOURCE_KERNEL_VERSION = "v0.1"
SOURCE_VERIFYOS_VERSION = "v0.4"
SOURCE_STATUS = "VERIFYOS_MIDDLE_WAY_CONDITIONAL_CONTINUITY_VERIFIED"
TRANSITION_TO_STATUS = {
    "retain": "valid",
    "suspend": "suspended",
    "request_revision": "revision_required",
    "supersede_with_lineage": "superseded",
    "complete": "completed",
    "terminate": "terminated",
}
STATUS_TO_DISPOSITION = {
    "valid": "bounded_synthesis_intake_ready",
    "suspended": "await_condition_change",
    "revision_required": "return_to_decisionos_revision",
    "superseded": "successor_lineage_reverification_required",
    "completed": "close_without_synthesis",
    "terminated": "terminate_without_synthesis",
}


@dataclass
class PlanOSMiddleWayBoundedSynthesisIntakeResult:
    status: str
    blockers: list[str]
    certificate: dict | None


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


def compute_planos_middle_way_intake_bundle_digest(
    *,
    source_verifyos_certificate_digest: str,
    expected_source_verifyos_certificate_digest: str,
    expected_source_handoff_receipt_digest: str,
    expected_world_binding_digest: str,
    expected_world_model_state_digest: str,
    expected_world_model_revision: int,
    expected_world_lineage_digest: str,
    expected_selected_candidate_id: str,
    expected_selected_candidate_plan_intent_digest: str,
    expected_synthesis_constraint_digest: str,
    intake_policy_digest: str,
    planos_intake_responsibility_digest: str,
    intake_request_id: str,
) -> str:
    return canonical_digest(
        {
            "source_verifyos_certificate_digest": source_verifyos_certificate_digest,
            "expected_source_verifyos_certificate_digest": (
                expected_source_verifyos_certificate_digest
            ),
            "expected_source_handoff_receipt_digest": (
                expected_source_handoff_receipt_digest
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
            "intake_policy_digest": intake_policy_digest,
            "planos_intake_responsibility_digest": (
                planos_intake_responsibility_digest
            ),
            "intake_request_id": intake_request_id,
        }
    )


def build_planos_middle_way_bounded_synthesis_intake_certificate(
    *,
    source_verifyos_certificate: Mapping[str, Any],
    expected_source_verifyos_certificate_digest: str,
    expected_source_handoff_receipt_digest: str,
    expected_world_binding_digest: str,
    expected_world_model_state_digest: str,
    expected_world_model_revision: int,
    expected_world_lineage_digest: str,
    expected_selected_candidate_id: str,
    expected_selected_candidate_plan_intent_digest: str,
    expected_synthesis_constraint_digest: str,
    intake_policy_digest: str,
    planos_intake_responsibility_digest: str,
    intake_request_id: str,
    intake_bundle_digest: str,
) -> PlanOSMiddleWayBoundedSynthesisIntakeResult:
    blockers: list[str] = []
    source = dict(source_verifyos_certificate) if isinstance(
        source_verifyos_certificate, Mapping
    ) else {}

    text_inputs = {
        "expected_source_verifyos_certificate_digest": (
            expected_source_verifyos_certificate_digest
        ),
        "expected_source_handoff_receipt_digest": (
            expected_source_handoff_receipt_digest
        ),
        "expected_world_binding_digest": expected_world_binding_digest,
        "expected_world_model_state_digest": expected_world_model_state_digest,
        "expected_world_lineage_digest": expected_world_lineage_digest,
        "expected_selected_candidate_id": expected_selected_candidate_id,
        "expected_selected_candidate_plan_intent_digest": (
            expected_selected_candidate_plan_intent_digest
        ),
        "expected_synthesis_constraint_digest": expected_synthesis_constraint_digest,
        "intake_policy_digest": intake_policy_digest,
        "planos_intake_responsibility_digest": (
            planos_intake_responsibility_digest
        ),
        "intake_request_id": intake_request_id,
        "intake_bundle_digest": intake_bundle_digest,
    }
    for name, value in text_inputs.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    if not isinstance(expected_world_model_revision, int) or isinstance(
        expected_world_model_revision, bool
    ) or expected_world_model_revision < 0:
        blockers.append("expected_world_model_revision_invalid")

    source_digest = ""
    spec: dict[str, Any] = {}
    source_resp_result: list[str] = []
    if not source:
        blockers.append("source_verifyos_certificate_missing")
    else:
        exact_source_headers = {
            "kernel": SOURCE_KERNEL,
            "kernel_version": SOURCE_KERNEL_VERSION,
            "verifyos_version": SOURCE_VERIFYOS_VERSION,
            "status": SOURCE_STATUS,
            "source_decisionos_version": "v0.8",
        }
        for name, expected in exact_source_headers.items():
            if source.get(name) != expected:
                blockers.append(f"source_{name}_invalid")

        raw_digest = source.get(
            "verifyos_middle_way_conditional_continuity_certificate_digest"
        )
        if not isinstance(raw_digest, str) or not raw_digest:
            blockers.append("source_verifyos_certificate_digest_missing")
        else:
            source_digest = raw_digest
            unsigned = dict(source)
            unsigned.pop(
                "verifyos_middle_way_conditional_continuity_certificate_digest",
                None,
            )
            if raw_digest != canonical_digest(unsigned):
                blockers.append("source_verifyos_certificate_digest_mismatch")
            if raw_digest != expected_source_verifyos_certificate_digest:
                blockers.append("source_verifyos_certificate_expected_binding_mismatch")

        required_text = (
            "source_handoff_receipt_digest",
            "source_selection_receipt_digest",
            "source_world_binding_digest",
            "source_world_model_state_digest",
            "source_world_lineage_digest",
            "source_synthesis_constraint_digest",
            "source_synthesis_handoff_bundle_digest",
            "selected_candidate_id",
            "selected_candidate_plan_intent_digest",
            "verification_policy_digest",
            "verification_owner_responsibility_digest",
            "verification_request_id",
            "transition_spec_digest",
            "verification_bundle_digest",
            "conditional_validity_status",
            "transition_kind",
            "transition_reason_digest",
        )
        for name in required_text:
            if not isinstance(source.get(name), str) or not source.get(name):
                blockers.append(f"source_{name}_missing")

        revision = source.get("source_world_model_revision")
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
            blockers.append("source_world_model_revision_invalid")

        expected_bindings = {
            "source_handoff_receipt_digest": expected_source_handoff_receipt_digest,
            "source_world_binding_digest": expected_world_binding_digest,
            "source_world_model_state_digest": expected_world_model_state_digest,
            "source_world_lineage_digest": expected_world_lineage_digest,
            "selected_candidate_id": expected_selected_candidate_id,
            "selected_candidate_plan_intent_digest": (
                expected_selected_candidate_plan_intent_digest
            ),
            "source_synthesis_constraint_digest": expected_synthesis_constraint_digest,
        }
        for name, expected in expected_bindings.items():
            if source.get(name) != expected:
                blockers.append(f"{name}_expected_binding_mismatch")
        if revision != expected_world_model_revision:
            blockers.append("source_world_model_revision_expected_binding_mismatch")

        true_boundaries = (
            "conditions_explicit",
            "changed_conditions_explicit",
            "predecessor_preserved",
            "lineage_monotone",
            "responsibility_preserved",
            "dissent_preserved",
            "minority_evidence_preserved",
            "object_not_reified",
            "object_not_erased",
            "commitment_not_absolutized",
            "revision_preserves_lineage",
            "supersession_preserves_predecessor",
            "termination_does_not_erase_history",
            "condition_change_may_trigger_revision",
            "condition_change_does_not_silently_rewrite",
            "emptiness_does_not_imply_irresponsibility",
            "commitment_does_not_imply_reification",
            "selection_remains_decisionos_owned",
            "planos_receives_verified_request_not_selection_authority",
            "authority_unchanged",
            "execution_permission_not_granted",
            "persistent_world_state_unchanged",
            "world_model_prediction_not_truth",
            "world_mutation_not_granted",
            "verification_passed",
            "future_only",
        )
        false_boundaries = (
            "plan_synthesis_performed",
            "concrete_plan_issued",
            "plan_receipt_issued",
            "active_now",
            "execution_permission",
        )
        for name in true_boundaries:
            if source.get(name) is not True:
                blockers.append(f"source_boundary_{name}_missing")
        for name in false_boundaries:
            if source.get(name) is not False:
                blockers.append(f"source_boundary_{name}_promoted")

        raw_spec = source.get("transition_spec")
        if not isinstance(raw_spec, dict) or not raw_spec:
            blockers.append("source_transition_spec_invalid")
        else:
            spec = dict(raw_spec)
            if source.get("transition_spec_digest") != canonical_digest(spec):
                blockers.append("source_transition_spec_digest_mismatch")
            kind = spec.get("transition_kind")
            expected_status = TRANSITION_TO_STATUS.get(kind)
            if expected_status is None:
                blockers.append("source_transition_kind_invalid")
            if spec.get("conditional_validity_status") != expected_status:
                blockers.append("source_transition_status_mismatch")
            if source.get("transition_kind") != kind:
                blockers.append("source_top_level_transition_kind_mismatch")
            if source.get("conditional_validity_status") != expected_status:
                blockers.append("source_top_level_conditional_status_mismatch")
            if source.get("transition_reason_digest") != spec.get(
                "transition_reason_digest"
            ):
                blockers.append("source_transition_reason_mismatch")

            normalized: dict[str, list[str]] = {}
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
                    blockers.append(f"source_{name}_invalid")
                normalized[name] = values

            source_conditions = set(normalized["source_condition_digests"])
            current_conditions = set(normalized["current_condition_digests"])
            changed_conditions = set(normalized["changed_condition_digests"])
            if changed_conditions != source_conditions.symmetric_difference(
                current_conditions
            ):
                blockers.append("source_changed_condition_set_mismatch")

            source_lineage = set(normalized["source_lineage_digests"])
            resulting_lineage = set(normalized["resulting_lineage_digests"])
            if not source_lineage.issubset(resulting_lineage):
                blockers.append("source_lineage_not_monotone")
            if spec.get("predecessor_reference_digest") not in resulting_lineage:
                blockers.append("source_predecessor_reference_not_preserved")
            if spec.get("source_object_digest") not in resulting_lineage:
                blockers.append("source_object_not_preserved_in_lineage")
            if spec.get("source_object_digest") != source.get(
                "source_handoff_receipt_digest"
            ):
                blockers.append("source_object_handoff_digest_mismatch")

            source_resp = set(
                normalized["source_responsibility_lineage_digests"]
            )
            resulting_resp = set(
                normalized["resulting_responsibility_lineage_digests"]
            )
            source_resp_result = sorted(resulting_resp)
            if not source_resp.issubset(resulting_resp):
                blockers.append("source_responsibility_lineage_not_monotone")
            if source.get(
                "verification_owner_responsibility_digest"
            ) not in resulting_resp:
                blockers.append("source_verification_owner_not_retained")

            forbidden = (
                "object_eternal_truth_claimed",
                "object_disposable_null_claimed",
                "silent_rewrite_requested",
                "history_erasure_requested",
                "authority_expansion_requested",
                "execution_permission_requested",
                "persistent_world_mutation_requested",
            )
            for name in forbidden:
                if spec.get(name) is not False:
                    blockers.append(f"source_transition_boundary_{name}_promoted")

    if not blockers:
        expected_bundle = compute_planos_middle_way_intake_bundle_digest(
            source_verifyos_certificate_digest=source_digest,
            expected_source_verifyos_certificate_digest=(
                expected_source_verifyos_certificate_digest
            ),
            expected_source_handoff_receipt_digest=(
                expected_source_handoff_receipt_digest
            ),
            expected_world_binding_digest=expected_world_binding_digest,
            expected_world_model_state_digest=expected_world_model_state_digest,
            expected_world_model_revision=expected_world_model_revision,
            expected_world_lineage_digest=expected_world_lineage_digest,
            expected_selected_candidate_id=expected_selected_candidate_id,
            expected_selected_candidate_plan_intent_digest=(
                expected_selected_candidate_plan_intent_digest
            ),
            expected_synthesis_constraint_digest=expected_synthesis_constraint_digest,
            intake_policy_digest=intake_policy_digest,
            planos_intake_responsibility_digest=(
                planos_intake_responsibility_digest
            ),
            intake_request_id=intake_request_id,
        )
        if intake_bundle_digest != expected_bundle:
            blockers.append("intake_bundle_digest_mismatch")

    if blockers:
        return PlanOSMiddleWayBoundedSynthesisIntakeResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    conditional_status = source["conditional_validity_status"]
    disposition = STATUS_TO_DISPOSITION[conditional_status]
    admitted = conditional_status == "valid"
    resulting_responsibility = sorted(
        set(source_resp_result) | {planos_intake_responsibility_digest}
    )
    certificate = {
        "kernel": "PlanOS Middle-Way Bounded Synthesis Intake Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.03",
        "status": "PLANOS_MIDDLE_WAY_BOUNDED_SYNTHESIS_INTAKE_ROUTED",
        "source_verifyos_version": source["verifyos_version"],
        "source_verifyos_certificate_digest": source_digest,
        "expected_source_verifyos_certificate_digest": (
            expected_source_verifyos_certificate_digest
        ),
        "source_decisionos_handoff_receipt_digest": source[
            "source_handoff_receipt_digest"
        ],
        "source_selection_receipt_digest": source["source_selection_receipt_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "source_synthesis_constraint_digest": source[
            "source_synthesis_constraint_digest"
        ],
        "source_synthesis_handoff_bundle_digest": source[
            "source_synthesis_handoff_bundle_digest"
        ],
        "selected_candidate_id": source["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": source[
            "selected_candidate_plan_intent_digest"
        ],
        "source_transition_spec": spec,
        "source_transition_spec_digest": source["transition_spec_digest"],
        "conditional_validity_status": conditional_status,
        "transition_kind": source["transition_kind"],
        "transition_reason_digest": source["transition_reason_digest"],
        "intake_disposition": disposition,
        "intake_policy_digest": intake_policy_digest,
        "planos_intake_responsibility_digest": planos_intake_responsibility_digest,
        "intake_request_id": intake_request_id,
        "intake_bundle_digest": intake_bundle_digest,
        "bounded_synthesis_request_admitted": admitted,
        "bounded_synthesis_intake_ready": admitted,
        "awaiting_condition_change": conditional_status == "suspended",
        "decisionos_revision_required": conditional_status == "revision_required",
        "successor_lineage_reverification_required": (
            conditional_status == "superseded"
        ),
        "close_without_synthesis": conditional_status == "completed",
        "terminate_without_synthesis": conditional_status == "terminated",
        "conditional_validity_enforced": True,
        "only_valid_status_admitted": True,
        "nonvalid_status_not_synthesized": True,
        "source_conditions_preserved": True,
        "source_changed_conditions_preserved": True,
        "source_lineage_preserved": True,
        "source_predecessor_preserved": True,
        "source_responsibility_preserved": True,
        "source_dissent_preserved": True,
        "source_minority_evidence_preserved": True,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
        "responsibility_extended_not_replaced": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_planos": False,
        "plan_synthesis_performed": False,
        "concrete_plan_issued": False,
        "plan_receipt_issued": False,
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
    certificate[
        "planos_middle_way_bounded_synthesis_intake_certificate_digest"
    ] = canonical_digest(certificate)
    return PlanOSMiddleWayBoundedSynthesisIntakeResult(
        STATUS_READY, [], certificate
    )
