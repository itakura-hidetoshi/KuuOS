#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

PLAN_STEP_FIELDS = {
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

ACTION_CLASS_TO_MATERIALIZATION_CLASS = {
    "evidence_collection": "evidence_collection_candidate",
    "review_checkpoint": "review_checkpoint_candidate",
    "prepare_reversible": "reversible_preparation_candidate",
    "analyze": "analysis_candidate",
    "condition_reassessment": "condition_reassessment_candidate",
    "hold": "bounded_hold_candidate",
    "request_revision": "revision_request_candidate",
    "terminate": "termination_candidate",
}

FIXED_FORBIDDEN_EFFECTS = frozenset(
    {
        "active_now",
        "candidate_substitution",
        "execution_permission",
        "external_side_effect",
        "persistent_world_mutation",
        "selection_authority_transfer",
        "tool_invocation",
        "unreviewed_scope_expansion",
    }
)


@dataclass
class ActOSDukkhaSupportedMaterializationIntakeResult:
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


def compute_materialization_intake_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def compute_concrete_plan_digest(receipt: Mapping[str, Any]) -> str:
    return canonical_digest(
        {
            "plan_id": receipt.get("plan_id"),
            "plan_revision": receipt.get("plan_revision"),
            "selected_candidate_id": receipt.get("selected_candidate_id"),
            "selected_candidate_plan_intent_digest": receipt.get(
                "selected_candidate_plan_intent_digest"
            ),
            "source_world_model_state_digest": receipt.get(
                "source_world_model_state_digest"
            ),
            "plan_steps": receipt.get("plan_steps"),
            "stop_condition_digests": receipt.get("stop_condition_digests"),
            "retained_alternative_records": receipt.get(
                "retained_alternative_records"
            ),
            "preserved_evidence_lineage_digests": receipt.get(
                "preserved_evidence_lineage_digests"
            ),
        }
    )


def _string_list(value: Any, *, allow_empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _verify_digest_bound_object(
    obj: dict,
    *,
    digest_field: str,
    expected_digest: str,
    prefix: str,
    blockers: list[str],
) -> str:
    digest = obj.get(digest_field)
    if not isinstance(digest, str) or not digest:
        blockers.append(f"{prefix}_digest_missing")
        return ""
    unsigned = dict(obj)
    unsigned.pop(digest_field, None)
    if digest != canonical_digest(unsigned):
        blockers.append(f"{prefix}_digest_mismatch")
    if digest != expected_digest:
        blockers.append(f"{prefix}_expected_binding_mismatch")
    return digest


def _verify_source_certificate(
    source: dict,
    expected_digest: str,
    blockers: list[str],
) -> tuple[str, list[str], list[str]]:
    if not source:
        blockers.append("source_verifyos_dukkha_certificate_missing")
        return "", [], []
    expected_headers = {
        "kernel": "VerifyOS Dukkha Reduction Claim Verification Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.6",
        "status": "VERIFYOS_DUKKHA_REDUCTION_CLAIM_VERIFIED",
        "dukkha_reduction_claim_status": "supported",
        "verification_disposition": (
            "dukkha_reduction_supported_for_materialization_intake"
        ),
    }
    for field, expected in expected_headers.items():
        if source.get(field) != expected:
            blockers.append(f"source_{field}_invalid")
    digest = _verify_digest_bound_object(
        source,
        digest_field=(
            "verifyos_dukkha_reduction_claim_verification_certificate_digest"
        ),
        expected_digest=expected_digest,
        prefix="source_verifyos_dukkha_certificate",
        blockers=blockers,
    )
    required_true = (
        "materialization_intake_admitted",
        "dukkha_vector_preserved",
        "single_scalar_utility_forbidden",
        "observation_integrity_preserved",
        "adverse_evidence_retained",
        "precision_collapse_not_used",
        "model_family_narrowing_not_used",
        "uncertainty_disclosed",
        "structural_suffering_acknowledged",
        "agency_preserved",
        "dissent_preserved",
        "minority_preserved",
        "future_burden_assessed",
        "causal_model_not_truth",
        "avoidable_dukkha_nonworsening_supported",
        "at_least_one_avoidable_dimension_improved",
        "attachment_rigidity_not_increased",
        "relational_curvature_not_hidden",
        "persistent_loop_gain_reduced",
        "model_revision_capacity_preserved",
        "protected_group_suffering_not_externalized",
        "future_suffering_not_externalized",
        "source_plan_preserved",
        "source_lineage_preserved",
        "source_responsibility_preserved",
        "selection_remains_decisionos_owned",
        "persistent_world_state_unchanged",
        "world_model_prediction_not_truth",
        "world_mutation_not_granted",
        "history_read_only",
        "qi_grants_no_authority",
        "future_only",
    )
    required_false = (
        "additional_evidence_required",
        "plan_revision_required",
        "selection_authority_granted_to_verifyos",
        "plan_revision_authority_granted_to_verifyos",
        "dukkha_minimization_authority_granted_to_verifyos",
        "plan_activated",
        "materialization_performed",
        "execution_authority_granted",
        "execution_permission",
        "active_now",
    )
    for field in required_true:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in required_false:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    lineage_ok, lineage = _string_list(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _string_list(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, lineage, responsibility


def _verify_plan_receipt(
    receipt: dict,
    expected_digest: str,
    source_certificate: dict,
    blockers: list[str],
) -> tuple[str, list[dict]]:
    if not receipt:
        blockers.append("source_plan_receipt_missing")
        return "", []
    expected_headers = {
        "kernel": "PlanOS Bounded Synthesis Receipt Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.04",
        "status": "PLANOS_BOUNDED_SYNTHESIS_RECEIPT_ISSUED",
    }
    for field, expected in expected_headers.items():
        if receipt.get(field) != expected:
            blockers.append(f"source_plan_{field}_invalid")
    digest = _verify_digest_bound_object(
        receipt,
        digest_field="planos_bounded_synthesis_receipt_digest",
        expected_digest=expected_digest,
        prefix="source_plan_receipt",
        blockers=blockers,
    )
    if source_certificate.get("source_plan_receipt_digest") != digest:
        blockers.append("source_certificate_plan_receipt_binding_mismatch")
    concrete_plan_digest = receipt.get("concrete_plan_digest")
    if not isinstance(concrete_plan_digest, str) or not concrete_plan_digest:
        blockers.append("source_concrete_plan_digest_missing")
    elif concrete_plan_digest != compute_concrete_plan_digest(receipt):
        blockers.append("source_concrete_plan_digest_mismatch")
    if source_certificate.get("source_concrete_plan_digest") != concrete_plan_digest:
        blockers.append("source_certificate_concrete_plan_binding_mismatch")
    required_true = (
        "finite_plan_constructed",
        "plan_synthesis_performed",
        "concrete_plan_issued",
        "plan_receipt_issued",
        "selected_candidate_not_substituted",
        "alternative_candidates_retained",
        "dissent_evidence_preserved",
        "minority_evidence_preserved",
        "irreversible_steps_checkpoint_guarded",
        "selection_remains_decisionos_owned",
        "persistent_world_state_unchanged",
        "world_model_prediction_not_truth",
        "world_mutation_not_granted",
        "history_read_only",
        "qi_grants_no_authority",
        "future_only",
    )
    required_false = (
        "selection_authority_granted_to_planos",
        "plan_activated",
        "materialization_performed",
        "execution_authority_granted",
        "execution_permission",
        "active_now",
    )
    for field in required_true:
        if receipt.get(field) is not True:
            blockers.append(f"source_plan_boundary_{field}_missing")
    for field in required_false:
        if receipt.get(field) is not False:
            blockers.append(f"source_plan_boundary_{field}_promoted")
    steps = receipt.get("plan_steps")
    if not isinstance(steps, list) or not steps:
        blockers.append("source_plan_steps_invalid")
        return digest, []
    if receipt.get("plan_step_count") != len(steps):
        blockers.append("source_plan_step_count_mismatch")
    step_ids: list[str] = []
    action_digests: list[str] = []
    for index, raw in enumerate(steps, start=1):
        if not isinstance(raw, Mapping) or set(raw) != PLAN_STEP_FIELDS:
            blockers.append(f"source_plan_step_schema_invalid_{index}")
            continue
        step = dict(raw)
        step_id = step.get("step_id")
        action_digest = step.get("action_spec_digest")
        if not isinstance(step_id, str) or not step_id:
            blockers.append(f"source_plan_step_id_invalid_{index}")
        if not isinstance(action_digest, str) or not action_digest:
            blockers.append(f"source_plan_action_digest_invalid_{index}")
        step_ids.append(str(step_id))
        action_digests.append(str(action_digest))
        if step.get("sequence_index") != index:
            blockers.append(f"source_plan_sequence_invalid_{index}")
        action_class = step.get("action_class")
        if action_class not in ACTION_CLASS_TO_MATERIALIZATION_CLASS:
            blockers.append(f"source_plan_action_class_unsupported_{index}")
        for field, allow_empty in (
            ("precondition_digests", False),
            ("expected_effect_digests", True),
            ("effect_tags", True),
            ("evidence_lineage_digests", False),
            ("stop_condition_digests", False),
            ("branch_ids", True),
        ):
            valid, _ = _string_list(step.get(field), allow_empty=allow_empty)
            if not valid:
                blockers.append(f"source_plan_{field}_invalid_{index}")
        effects = step.get("effect_tags")
        if isinstance(effects, list) and FIXED_FORBIDDEN_EFFECTS.intersection(effects):
            blockers.append(f"source_plan_forbidden_effect_{index}")
        reversible = step.get("reversible")
        irreversible = step.get("irreversible")
        if not isinstance(reversible, bool) or not isinstance(irreversible, bool):
            blockers.append(f"source_plan_reversibility_invalid_{index}")
        elif reversible == irreversible:
            blockers.append(f"source_plan_reversibility_not_exclusive_{index}")
        checkpoint = step.get("checkpoint_step_id")
        if irreversible:
            if (
                not isinstance(checkpoint, str)
                or not checkpoint
                or checkpoint not in step_ids[:-1]
            ):
                blockers.append(f"source_plan_checkpoint_invalid_{index}")
        elif checkpoint != "":
            blockers.append(f"source_plan_checkpoint_unexpected_{index}")
    if len(step_ids) != len(set(step_ids)):
        blockers.append("source_plan_step_ids_not_unique")
    if len(action_digests) != len(set(action_digests)):
        blockers.append("source_plan_action_digests_not_unique")
    return digest, [dict(step) for step in steps if isinstance(step, Mapping)]


def _materialization_candidate(step: Mapping[str, Any]) -> dict:
    payload = {
        "source_step_id": step["step_id"],
        "sequence_index": step["sequence_index"],
        "source_action_class": step["action_class"],
        "materialization_class": ACTION_CLASS_TO_MATERIALIZATION_CLASS[
            step["action_class"]
        ],
        "source_action_spec_digest": step["action_spec_digest"],
        "precondition_digests": list(step["precondition_digests"]),
        "expected_effect_digests": list(step["expected_effect_digests"]),
        "effect_tags": list(step["effect_tags"]),
        "evidence_lineage_digests": list(step["evidence_lineage_digests"]),
        "stop_condition_digests": list(step["stop_condition_digests"]),
        "reversible": step["reversible"],
        "irreversible": step["irreversible"],
        "checkpoint_step_id": step["checkpoint_step_id"],
        "branch_ids": list(step["branch_ids"]),
    }
    candidate = {
        "materialization_candidate_id": f"materialize-{step['step_id']}",
        **payload,
        "candidate_state": "prepared_not_activated",
        "adapter_binding_digest": "",
        "tool_invocation_requested": False,
        "external_side_effect_requested": False,
        "execution_permission_requested": False,
        "active_now_requested": False,
    }
    candidate["materialization_payload_digest"] = canonical_digest(payload)
    candidate["materialization_candidate_digest"] = canonical_digest(candidate)
    return candidate


def build_actos_dukkha_supported_bounded_plan_materialization_intake(
    *,
    source_verifyos_dukkha_certificate: Mapping[str, Any],
    expected_source_verifyos_dukkha_certificate_digest: str,
    source_plan_receipt: Mapping[str, Any],
    expected_source_plan_receipt_digest: str,
    materialization_policy_digest: str,
    actos_materialization_responsibility_digest: str,
    materialization_request_id: str,
    materialization_bundle_digest: str,
) -> ActOSDukkhaSupportedMaterializationIntakeResult:
    blockers: list[str] = []
    source = (
        dict(source_verifyos_dukkha_certificate)
        if isinstance(source_verifyos_dukkha_certificate, Mapping)
        else {}
    )
    plan_receipt = (
        dict(source_plan_receipt) if isinstance(source_plan_receipt, Mapping) else {}
    )
    for name, value in {
        "expected_source_verifyos_dukkha_certificate_digest": (
            expected_source_verifyos_dukkha_certificate_digest
        ),
        "expected_source_plan_receipt_digest": expected_source_plan_receipt_digest,
        "materialization_policy_digest": materialization_policy_digest,
        "actos_materialization_responsibility_digest": (
            actos_materialization_responsibility_digest
        ),
        "materialization_request_id": materialization_request_id,
        "materialization_bundle_digest": materialization_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    source_digest, source_lineage, source_responsibility = _verify_source_certificate(
        source, expected_source_verifyos_dukkha_certificate_digest, blockers
    )
    plan_digest, steps = _verify_plan_receipt(
        plan_receipt,
        expected_source_plan_receipt_digest,
        source,
        blockers,
    )
    if not blockers:
        expected_bundle = compute_materialization_intake_bundle_digest(
            source_verifyos_dukkha_certificate_digest=source_digest,
            expected_source_verifyos_dukkha_certificate_digest=(
                expected_source_verifyos_dukkha_certificate_digest
            ),
            source_plan_receipt_digest=plan_digest,
            expected_source_plan_receipt_digest=expected_source_plan_receipt_digest,
            source_concrete_plan_digest=plan_receipt["concrete_plan_digest"],
            materialization_policy_digest=materialization_policy_digest,
            actos_materialization_responsibility_digest=(
                actos_materialization_responsibility_digest
            ),
            materialization_request_id=materialization_request_id,
        )
        if materialization_bundle_digest != expected_bundle:
            blockers.append("materialization_bundle_digest_mismatch")
    if blockers:
        return ActOSDukkhaSupportedMaterializationIntakeResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )
    candidates = [_materialization_candidate(step) for step in steps]
    candidate_ids = [item["materialization_candidate_id"] for item in candidates]
    if len(candidate_ids) != len(set(candidate_ids)):
        return ActOSDukkhaSupportedMaterializationIntakeResult(
            STATUS_BLOCKED, ["materialization_candidate_ids_not_unique"], None
        )
    materialization_set_digest = canonical_digest(candidates)
    resulting_lineage = sorted(
        set(source_lineage)
        | {
            source_digest,
            plan_digest,
            plan_receipt["concrete_plan_digest"],
            materialization_set_digest,
            materialization_bundle_digest,
        }
    )
    resulting_responsibility = sorted(
        set(source_responsibility) | {actos_materialization_responsibility_digest}
    )
    receipt = {
        "kernel": "ActOS Dukkha-Supported Bounded Plan Materialization Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.5",
        "status": "ACTOS_DUKKHA_SUPPORTED_BOUNDED_PLAN_MATERIALIZATION_INTAKE_READY",
        "source_verifyos_dukkha_certificate_digest": source_digest,
        "source_plan_receipt_digest": plan_digest,
        "source_concrete_plan_digest": plan_receipt["concrete_plan_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": plan_receipt["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": plan_receipt[
            "selected_candidate_plan_intent_digest"
        ],
        "dukkha_assessment_digest": source["dukkha_assessment_digest"],
        "reference_plan_digest": source["reference_plan_digest"],
        "materialization_policy_digest": materialization_policy_digest,
        "actos_materialization_responsibility_digest": (
            actos_materialization_responsibility_digest
        ),
        "materialization_request_id": materialization_request_id,
        "materialization_bundle_digest": materialization_bundle_digest,
        "materialization_candidates": candidates,
        "materialization_candidate_count": len(candidates),
        "materialization_candidate_set_digest": materialization_set_digest,
        "materialization_intake_performed": True,
        "materialization_candidates_issued": True,
        "all_plan_steps_materialized": len(candidates) == len(steps),
        "one_to_one_step_mapping_preserved": True,
        "step_sequence_preserved": True,
        "checkpoint_guards_preserved": True,
        "stop_conditions_preserved": True,
        "evidence_lineage_preserved": True,
        "alternative_candidates_preserved": True,
        "dissent_preserved": True,
        "minority_preserved": True,
        "dukkha_reduction_support_preserved": True,
        "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True,
        "revision_capacity_preserved": True,
        "persistent_loop_reduction_preserved": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_actos": False,
        "plan_revision_authority_granted_to_actos": False,
        "dukkha_minimization_authority_granted_to_actos": False,
        "plan_activated": False,
        "adapter_binding_performed": False,
        "adapter_invocation_performed": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "execution_authority_granted": False,
        "execution_permission": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[
        "actos_dukkha_supported_bounded_plan_materialization_intake_receipt_digest"
    ] = canonical_digest(receipt)
    return ActOSDukkhaSupportedMaterializationIntakeResult(STATUS_READY, [], receipt)
