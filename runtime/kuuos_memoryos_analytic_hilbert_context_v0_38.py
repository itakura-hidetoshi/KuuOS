from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime import kuuos_memoryos_predictive_shielded_memory_v0_37 as v037

VERSION = "kuuos_memoryos_analytic_hilbert_context_v0_38"
CONTEXT_VERSION = "memoryos_analytic_hilbert_context_v0_38"
ANALYTIC_BRIDGE_VERSION = "world_kuu_vacuum_os_hilbert_completion_v0_49"
CONTEXT_KIND = "READ_ONLY_OS_HILBERT_CONTEXT_CANDIDATE"
RECEIPT_KIND = "SUPPLIED_READ_ONLY_WORLD_V049_ANALYTIC_RECEIPT"

CONTEXT_ROUTES = {
    "QUARANTINE_SOURCE_CAPSULE",
    "REOBSERVE_BEFORE_ANALYTIC_CONTEXT",
    "REVIEW_BEFORE_ANALYTIC_CONTEXT",
    "RETURN_ANALYTIC_CONTEXT_WITH_RESIDUE",
    "RETURN_READ_ONLY_ANALYTIC_CONTEXT",
}
SOURCE_KINDS = {"memory_record", "predictive_state"}
VACUUM_RELATION = "REFERENCE_ONLY"

NON_AUTHORITY = {
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_execution_authority": False,
    "grants_plan_activation": False,
    "grants_actos_invocation": False,
    "grants_blocker_discharge_authority": False,
    "grants_world_commit_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_actual_hilbert_vector_status": False,
    "grants_inner_product_claim": False,
    "grants_norm_claim": False,
    "grants_probability_claim": False,
    "grants_vacuum_identity": False,
}

BOUNDARY = {
    "source_v037_capsule_exactly_bound": True,
    "source_predictive_state_exactly_bound": True,
    "source_world_fragment_exactly_bound": True,
    "source_v049_analytic_receipt_exactly_bound": True,
    "analytic_context_candidate_only": True,
    "runtime_constructs_no_os_completion": True,
    "runtime_computes_no_hilbert_vector": True,
    "runtime_computes_no_inner_product": True,
    "runtime_computes_no_norm": True,
    "runtime_evaluates_no_vacuum_state": True,
    "vacuum_is_reference_only": True,
    "memory_candidate_not_vacuum": True,
    "world_not_vacuum": True,
    "kuu_not_zero_vector": True,
    "modular_time_not_physical_time": True,
    "contradiction_residue_preserved": True,
    "blocker_shield_preserved": True,
    "append_only_context_lineage": True,
    "runtime_read_only": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def context_digest(value: Mapping[str, Any]) -> str:
    return v037.v035.world_v034.digest(_without(value, "analytic_context_digest"))


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _nat(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field}_invalid")
    return value


def _normalize_receipt(value: Mapping[str, Any]) -> dict[str, Any]:
    if value.get("receipt_kind") != RECEIPT_KIND:
        raise ValueError("analytic_receipt_kind_invalid")
    if value.get("bridge_version") != ANALYTIC_BRIDGE_VERSION:
        raise ValueError("analytic_bridge_version_invalid")
    if value.get("os_completion_claim_supplied") is not True:
        raise ValueError("os_completion_receipt_missing")
    if value.get("vacuum_nonzero_theorem_registered") is not True:
        raise ValueError("vacuum_nonzero_receipt_missing")
    for field in (
        "runtime_constructed_completion",
        "runtime_computed_hilbert_vectors",
        "runtime_computed_inner_products",
        "runtime_computed_norms",
        "runtime_evaluated_vacuum_state",
        "runtime_executed_modular_time",
        "runtime_executed_physical_time",
        "identifies_world_with_vacuum",
        "identifies_memory_candidate_with_vacuum",
        "identifies_kuu_with_zero",
        "truth_authority",
        "execution_authority",
    ):
        if value.get(field) is not False:
            raise ValueError(f"analytic_receipt_{field}_forbidden")
    return {
        "receipt_kind": RECEIPT_KIND,
        "bridge_version": ANALYTIC_BRIDGE_VERSION,
        "formal_module_digest": _text(
            value.get("formal_module_digest"), "formal_module_digest"
        ),
        "os_completion_claim_supplied": True,
        "vacuum_nonzero_theorem_registered": True,
        "runtime_constructed_completion": False,
        "runtime_computed_hilbert_vectors": False,
        "runtime_computed_inner_products": False,
        "runtime_computed_norms": False,
        "runtime_evaluated_vacuum_state": False,
        "runtime_executed_modular_time": False,
        "runtime_executed_physical_time": False,
        "identifies_world_with_vacuum": False,
        "identifies_memory_candidate_with_vacuum": False,
        "identifies_kuu_with_zero": False,
        "truth_authority": False,
        "execution_authority": False,
    }


def _source_digest_for_candidate(
    capsule: Mapping[str, Any], source_kind: str, source_id: str
) -> str:
    if source_kind == "predictive_state":
        if source_id != "predictive_state":
            raise ValueError("predictive_state_source_id_invalid")
        return _text(capsule.get("predictive_state_digest"), "predictive_state_digest")
    records = capsule.get("memory_records")
    if not isinstance(records, list):
        raise ValueError("source_memory_records_invalid")
    for record in records:
        if isinstance(record, Mapping) and record.get("record_id") == source_id:
            return _text(record.get("content_digest"), "source_content_digest")
    raise ValueError("analytic_candidate_source_record_missing")


def _normalize_candidate(
    value: Mapping[str, Any], capsule: Mapping[str, Any]
) -> dict[str, Any]:
    source_kind = _text(value.get("source_kind"), "source_kind")
    if source_kind not in SOURCE_KINDS:
        raise ValueError("analytic_candidate_source_kind_invalid")
    source_id = _text(value.get("source_id"), "source_id")
    expected_source_digest = _source_digest_for_candidate(
        capsule, source_kind, source_id
    )
    source_digest = _text(value.get("source_digest"), "source_digest")
    if source_digest != expected_source_digest:
        raise ValueError("analytic_candidate_source_digest_mismatch")
    if value.get("relation_to_vacuum") != VACUUM_RELATION:
        raise ValueError("analytic_candidate_vacuum_relation_invalid")
    for field in (
        "actual_hilbert_vector_claim",
        "inner_product_claim",
        "norm_claim",
        "probability_claim",
        "vacuum_identity_claim",
        "truth_claim",
        "execution_authority",
        "plan_activation",
    ):
        if value.get(field) is not False:
            raise ValueError(f"analytic_candidate_{field}_forbidden")
    if value.get("candidate_context_only") is not True:
        raise ValueError("analytic_candidate_context_only_required")
    return {
        "candidate_id": _text(value.get("candidate_id"), "candidate_id"),
        "context_kind": CONTEXT_KIND,
        "source_kind": source_kind,
        "source_id": source_id,
        "source_digest": source_digest,
        "observable_class_digest": _text(
            value.get("observable_class_digest"), "observable_class_digest"
        ),
        "hilbert_context_digest": _text(
            value.get("hilbert_context_digest"), "hilbert_context_digest"
        ),
        "relation_to_vacuum": VACUUM_RELATION,
        "candidate_context_only": True,
        "actual_hilbert_vector_claim": False,
        "inner_product_claim": False,
        "norm_claim": False,
        "probability_claim": False,
        "vacuum_identity_claim": False,
        "truth_claim": False,
        "execution_authority": False,
        "plan_activation": False,
    }


def _normalize_candidates(
    values: Sequence[Mapping[str, Any]], capsule: Mapping[str, Any]
) -> list[dict[str, Any]]:
    if isinstance(values, (str, bytes)):
        raise ValueError("analytic_context_candidates_invalid")
    result = [_normalize_candidate(value, capsule) for value in values]
    ids = [item["candidate_id"] for item in result]
    if len(ids) != len(set(ids)):
        raise ValueError("analytic_context_candidate_id_duplicate")
    return result


def _expected_route(source_capsule_route: str) -> str:
    if source_capsule_route == "QUARANTINE_SOURCE_BLOCKER_EVIDENCE":
        return "QUARANTINE_SOURCE_CAPSULE"
    if source_capsule_route == "REOBSERVE_PREDICTIVE_STATE":
        return "REOBSERVE_BEFORE_ANALYTIC_CONTEXT"
    if source_capsule_route == "REVIEW_CONTRADICTION_RESIDUE":
        return "REVIEW_BEFORE_ANALYTIC_CONTEXT"
    if source_capsule_route == "PRESERVE_RESIDUE_WITH_CONTEXT":
        return "RETURN_ANALYTIC_CONTEXT_WITH_RESIDUE"
    if source_capsule_route == "READY_FOR_SHIELDED_RETRIEVAL":
        return "RETURN_READ_ONLY_ANALYTIC_CONTEXT"
    raise ValueError("source_capsule_route_invalid")


def _validate_prior_context(
    prior_context: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if prior_context is None:
        return None
    errors = validate_memoryos_analytic_hilbert_context(prior_context)
    if errors:
        raise ValueError("prior_analytic_context_invalid:" + ";".join(errors))
    return deepcopy(dict(prior_context))


def build_memoryos_analytic_hilbert_context(
    *,
    source_capsule: Mapping[str, Any],
    analytic_receipt: Mapping[str, Any],
    analytic_context_candidates: Sequence[Mapping[str, Any]],
    created_at_ms: int,
    prior_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    source_errors = v037.validate_predictive_shielded_memory_capsule(source_capsule)
    if source_errors:
        raise ValueError("source_capsule_invalid:" + ";".join(source_errors))
    receipt = _normalize_receipt(analytic_receipt)
    candidates = _normalize_candidates(analytic_context_candidates, source_capsule)
    prior = _validate_prior_context(prior_context)

    source_sequence = _nat(source_capsule.get("sequence_index"), "source_sequence")
    source_digest = _text(
        source_capsule.get("memory_capsule_digest"), "source_memory_capsule_digest"
    )
    if prior is None:
        sequence_index = 0
        previous_digest = v037.v035.world_v034.ZERO_DIGEST
    else:
        if source_capsule.get("mission_id") != prior.get("mission_id"):
            raise ValueError("analytic_context_mission_changed")
        if source_capsule.get("lineage_id") != prior.get("lineage_id"):
            raise ValueError("analytic_context_lineage_changed")
        previous_source_sequence = prior["source_memory_capsule_sequence_index"]
        if source_sequence < previous_source_sequence:
            raise ValueError("source_memory_capsule_sequence_regressed")
        if (
            source_sequence == previous_source_sequence
            and source_digest != prior["source_memory_capsule_digest"]
        ):
            raise ValueError("source_memory_capsule_substituted_same_sequence")
        if receipt != prior["analytic_receipt"]:
            raise ValueError("analytic_receipt_changed_within_lineage")
        old_candidates = prior["analytic_context_candidates"]
        if candidates[: len(old_candidates)] != old_candidates:
            raise ValueError("analytic_context_candidates_append_only_violation")
        sequence_index = prior["sequence_index"] + 1
        previous_digest = prior["analytic_context_digest"]

    source_route = _text(source_capsule.get("capsule_route"), "source_capsule_route")
    route = _expected_route(source_route)
    context = {
        "version": CONTEXT_VERSION,
        "sequence_index": sequence_index,
        "previous_analytic_context_digest": previous_digest,
        "source_memory_capsule_digest": source_digest,
        "source_memory_capsule_sequence_index": source_sequence,
        "source_predictive_state_digest": _text(
            source_capsule.get("predictive_state_digest"),
            "source_predictive_state_digest",
        ),
        "source_world_fragment_digest": _text(
            source_capsule.get("source_world_fragment_digest"),
            "source_world_fragment_digest",
        ),
        "source_qi_process_tensor_trace_digest": _text(
            source_capsule.get("source_qi_process_tensor_trace_digest"),
            "source_qi_process_tensor_trace_digest",
        ),
        "source_capsule_route": source_route,
        "mission_id": _text(source_capsule.get("mission_id"), "mission_id"),
        "lineage_id": _text(source_capsule.get("lineage_id"), "lineage_id"),
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "route": route,
        "analytic_receipt": receipt,
        "analytic_context_candidates": candidates,
        "contradiction_residue": deepcopy(
            source_capsule.get("contradiction_residue", [])
        ),
        "blocker_projection": {
            "active_blockers": deepcopy(
                source_capsule.get("blocker_projection", {}).get(
                    "active_blockers", []
                )
            ),
            "blocked_capabilities": deepcopy(
                source_capsule.get("blocker_projection", {}).get(
                    "blocked_capabilities", []
                )
            ),
            "shield_gate_required": True,
            "analytic_context_may_discharge_blocker": False,
            "analytic_context_may_return_capability": False,
        },
        "append_candidate": {
            "target_stream": "memoryos/analytic_hilbert_context/append_only",
            "append_only_required": True,
            "durable_persistence_performed_by_this_kernel": False,
            "memory_overwrite_performed": False,
            "world_update_performed": False,
        },
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "analytic_context_digest": "",
    }
    context["analytic_context_digest"] = context_digest(context)
    errors = validate_memoryos_analytic_hilbert_context(context)
    if errors:
        raise ValueError(";".join(errors))
    return context


def validate_memoryos_analytic_hilbert_context(
    context: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if context.get("version") != CONTEXT_VERSION:
        errors.append("analytic_context_version_invalid")
    for field in (
        "sequence_index",
        "source_memory_capsule_sequence_index",
        "created_at_ms",
    ):
        try:
            _nat(context.get(field), field)
        except ValueError as exc:
            errors.append(str(exc))
    for field in (
        "previous_analytic_context_digest",
        "source_memory_capsule_digest",
        "source_predictive_state_digest",
        "source_world_fragment_digest",
        "source_qi_process_tensor_trace_digest",
        "source_capsule_route",
        "mission_id",
        "lineage_id",
    ):
        if not isinstance(context.get(field), str) or not context.get(field):
            errors.append(f"analytic_context_{field}_missing")
    if context.get("route") not in CONTEXT_ROUTES:
        errors.append("analytic_context_route_invalid")
    else:
        try:
            if context.get("route") != _expected_route(
                str(context.get("source_capsule_route"))
            ):
                errors.append("analytic_context_route_source_mismatch")
        except ValueError as exc:
            errors.append(str(exc))

    receipt = context.get("analytic_receipt")
    if not isinstance(receipt, Mapping):
        errors.append("analytic_context_receipt_invalid")
    else:
        try:
            if dict(receipt) != _normalize_receipt(receipt):
                errors.append("analytic_context_receipt_not_normalized")
        except ValueError as exc:
            errors.append(str(exc))

    candidates = context.get("analytic_context_candidates")
    if not isinstance(candidates, list):
        errors.append("analytic_context_candidates_invalid")
    else:
        ids: list[str] = []
        for candidate in candidates:
            if not isinstance(candidate, Mapping):
                errors.append("analytic_context_candidate_invalid")
                continue
            candidate_id = candidate.get("candidate_id")
            if not isinstance(candidate_id, str) or not candidate_id:
                errors.append("analytic_context_candidate_id_invalid")
            else:
                ids.append(candidate_id)
            if candidate.get("context_kind") != CONTEXT_KIND:
                errors.append("analytic_context_candidate_kind_invalid")
            if candidate.get("source_kind") not in SOURCE_KINDS:
                errors.append("analytic_context_candidate_source_kind_invalid")
            if candidate.get("relation_to_vacuum") != VACUUM_RELATION:
                errors.append("analytic_context_candidate_vacuum_relation_invalid")
            if candidate.get("candidate_context_only") is not True:
                errors.append("analytic_context_candidate_context_only_invalid")
            for field in (
                "actual_hilbert_vector_claim",
                "inner_product_claim",
                "norm_claim",
                "probability_claim",
                "vacuum_identity_claim",
                "truth_claim",
                "execution_authority",
                "plan_activation",
            ):
                if candidate.get(field) is not False:
                    errors.append(f"analytic_context_candidate_{field}_invalid")
        if len(ids) != len(set(ids)):
            errors.append("analytic_context_candidate_id_duplicate")

    residues = context.get("contradiction_residue")
    if not isinstance(residues, list):
        errors.append("analytic_context_residue_invalid")
    else:
        for residue in residues:
            if not isinstance(residue, Mapping):
                errors.append("analytic_context_residue_entry_invalid")
                continue
            if residue.get("resolved_by_consolidation") is not False:
                errors.append("analytic_context_residue_resolution_invalid")
            if residue.get("silent_collapse") is not False:
                errors.append("analytic_context_residue_silent_collapse_invalid")

    blocker = context.get("blocker_projection")
    if not isinstance(blocker, Mapping):
        errors.append("analytic_context_blocker_projection_invalid")
    else:
        if blocker.get("shield_gate_required") is not True:
            errors.append("analytic_context_shield_gate_invalid")
        if blocker.get("analytic_context_may_discharge_blocker") is not False:
            errors.append("analytic_context_blocker_discharge_invalid")
        if blocker.get("analytic_context_may_return_capability") is not False:
            errors.append("analytic_context_capability_return_invalid")

    append_candidate = context.get("append_candidate")
    if not isinstance(append_candidate, Mapping):
        errors.append("analytic_context_append_candidate_invalid")
    else:
        if append_candidate.get("append_only_required") is not True:
            errors.append("analytic_context_append_only_invalid")
        for field in (
            "durable_persistence_performed_by_this_kernel",
            "memory_overwrite_performed",
            "world_update_performed",
        ):
            if append_candidate.get(field) is not False:
                errors.append(f"analytic_context_append_{field}_invalid")

    if context.get("non_authority") != NON_AUTHORITY:
        errors.append("analytic_context_non_authority_invalid")
    if context.get("boundary") != BOUNDARY:
        errors.append("analytic_context_boundary_invalid")
    if context.get("analytic_context_digest") != context_digest(context):
        errors.append("analytic_context_digest_invalid")
    return errors
