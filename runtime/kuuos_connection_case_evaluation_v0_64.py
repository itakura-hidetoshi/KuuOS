#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_connection_admission_types_v0_63 import (
    READY,
    ConnectionAdmissionReceipt,
)
from runtime.kuuos_connection_candidate_search_v0_62 import ConnectionCandidateProposal
from runtime.kuuos_connection_evaluation_types_v0_64 import (
    BLOCKED_STATUS,
    READY_STATUS,
    VERSION,
    ConnectionEvaluationCaseReceipt,
    ConnectionEvaluationPolicy,
    ConnectionEvaluationReceipt,
)
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_os_curvature_holonomy_v0_61 import (
    OSGaugeBundle,
    decompose_os_curvature,
    memory_holonomy,
)


def connection_domain(bundle: OSGaugeBundle) -> tuple[tuple[str, str], ...]:
    return tuple(sorted(bundle.connection.transports))


def field_signature(bundle: OSGaugeBundle) -> dict[str, Any]:
    return {role: field.to_dict() for role, field in sorted(bundle.fields.items())}


def source_signature(bundle: OSGaugeBundle) -> dict[str, str]:
    return {role: field.source_digest for role, field in sorted(bundle.fields.items())}


def close_value(left: float, right: float, tolerance: float) -> bool:
    return abs(float(left) - float(right)) <= tolerance


def memory_observables_preserved(source, candidate, tolerance: float) -> bool:
    return (
        source.path == candidate.path
        and close_value(source.wilson_observable, candidate.wilson_observable, tolerance)
        and close_value(source.holonomy_defect, candidate.holonomy_defect, tolerance)
        and close_value(
            source.memory_channel_return_energy,
            candidate.memory_channel_return_energy,
            tolerance,
        )
    )


def evaluate_connection_case(
    case_id: str,
    source_bundle: OSGaugeBundle,
    candidate_connection,
    reference_bundle: OSGaugeBundle,
    policy: ConnectionEvaluationPolicy,
) -> ConnectionEvaluationCaseReceipt:
    blockers: list[str] = []
    source_digest = canonical_digest(source_bundle.to_dict())
    group_ok = (
        source_bundle.group == reference_bundle.group
        and candidate_connection.group == source_bundle.group
    )
    domain_ok = (
        connection_domain(source_bundle) == connection_domain(reference_bundle)
        and tuple(sorted(candidate_connection.transports)) == connection_domain(source_bundle)
    )
    if not group_ok:
        blockers.append("evaluation_case_group_mismatch")
    if not domain_ok:
        blockers.append("evaluation_case_connection_domain_mismatch")

    if blockers:
        payload = {
            "case_id": case_id,
            "source_bundle_digest": source_digest,
            "source_curvature": None,
            "candidate_curvature": None,
            "curvature_nonincreasing": False,
            "curvature_strictly_decreased": False,
            "memory_holonomy_preserved": False,
            "fields_preserved": False,
            "source_bindings_preserved": False,
            "admissible": False,
            "blockers": blockers,
        }
        return ConnectionEvaluationCaseReceipt(
            case_id=case_id,
            source_bundle_digest=source_digest,
            source_curvature=None,
            candidate_curvature=None,
            curvature_nonincreasing=False,
            curvature_strictly_decreased=False,
            memory_holonomy_preserved=False,
            fields_preserved=False,
            source_bindings_preserved=False,
            admissible=False,
            blockers=tuple(blockers),
            receipt_digest=canonical_digest(payload),
        )

    candidate_bundle = OSGaugeBundle(
        source_bundle.group,
        candidate_connection,
        source_bundle.fields,
    )
    fields_ok = field_signature(candidate_bundle) == field_signature(source_bundle)
    sources_ok = source_signature(candidate_bundle) == source_signature(source_bundle)
    source_curvature = decompose_os_curvature(source_bundle)
    candidate_curvature = decompose_os_curvature(candidate_bundle)
    source_memory = memory_holonomy(source_bundle)
    candidate_memory = memory_holonomy(candidate_bundle)

    nonincreasing = (
        candidate_curvature.total_curvature
        <= source_curvature.total_curvature + policy.tolerance
    )
    strict = (
        candidate_curvature.total_curvature
        < source_curvature.total_curvature - policy.tolerance
    )
    holonomy_ok = memory_observables_preserved(
        source_memory,
        candidate_memory,
        policy.tolerance,
    )
    if not nonincreasing:
        blockers.append("evaluation_case_curvature_increased")
    if not holonomy_ok:
        blockers.append("evaluation_case_memory_holonomy_changed")
    if not fields_ok:
        blockers.append("evaluation_case_fields_changed")
    if not sources_ok:
        blockers.append("evaluation_case_source_bindings_changed")

    payload = {
        "case_id": case_id,
        "source_bundle_digest": source_digest,
        "source_curvature": source_curvature.total_curvature,
        "candidate_curvature": candidate_curvature.total_curvature,
        "curvature_nonincreasing": nonincreasing,
        "curvature_strictly_decreased": strict,
        "memory_holonomy_preserved": holonomy_ok,
        "fields_preserved": fields_ok,
        "source_bindings_preserved": sources_ok,
        "admissible": not blockers,
        "blockers": blockers,
    }
    return ConnectionEvaluationCaseReceipt(
        case_id=case_id,
        source_bundle_digest=source_digest,
        source_curvature=source_curvature.total_curvature,
        candidate_curvature=candidate_curvature.total_curvature,
        curvature_nonincreasing=nonincreasing,
        curvature_strictly_decreased=strict,
        memory_holonomy_preserved=holonomy_ok,
        fields_preserved=fields_ok,
        source_bindings_preserved=sources_ok,
        admissible=not blockers,
        blockers=tuple(blockers),
        receipt_digest=canonical_digest(payload),
    )


def evaluation_binding_blockers(
    source_bundle: OSGaugeBundle,
    proposal: ConnectionCandidateProposal,
    admission: ConnectionAdmissionReceipt,
) -> tuple[str, ...]:
    blockers: list[str] = []
    source_digest = canonical_digest(source_bundle.to_dict())
    proposal_digest = canonical_digest(proposal.to_dict())
    selected = proposal.selected_receipt

    if proposal.route != "PROPOSE_CONNECTION_UPDATE":
        blockers.append("evaluation_proposal_route_invalid")
    if selected is None or proposal.selected_connection is None:
        blockers.append("evaluation_selected_candidate_missing")
    elif not selected.admissible:
        blockers.append("evaluation_selected_receipt_not_admissible")

    admission_payload = admission.to_dict()
    recorded_admission_digest = admission_payload.pop("receipt_digest", "")
    if recorded_admission_digest != canonical_digest(admission_payload):
        blockers.append("evaluation_admission_receipt_digest_invalid")
    if admission.status != READY or not admission.staging_ready:
        blockers.append("evaluation_admission_not_ready")
    if admission.production_apply_ready:
        blockers.append("evaluation_admission_scope_invalid")
    if not admission.candidate_only:
        blockers.append("evaluation_admission_not_candidate_only")
    if admission.state_write_performed:
        blockers.append("evaluation_admission_state_write_detected")
    if admission.authority_widened:
        blockers.append("evaluation_admission_authority_widened")
    if admission.blockers:
        blockers.append("evaluation_admission_has_blockers")

    expected_receipt = "" if selected is None else selected.receipt_digest
    expected_connection = "" if selected is None else selected.candidate_connection_digest
    expected_rollback = "" if selected is None else selected.rollback_digest
    bindings = (
        (admission.source_bundle_digest, source_digest, "source_bundle"),
        (proposal.source_bundle_digest, source_digest, "proposal_source_bundle"),
        (admission.proposal_digest, proposal_digest, "proposal"),
        (admission.selected_receipt_digest, expected_receipt, "selected_receipt"),
        (admission.candidate_connection_digest, expected_connection, "candidate_connection"),
        (admission.rollback_digest, expected_rollback, "rollback"),
    )
    for actual, expected, name in bindings:
        if actual != expected:
            blockers.append(f"evaluation_{name}_binding_mismatch")
    if expected_rollback != source_digest:
        blockers.append("evaluation_rollback_not_source_bundle")
    return tuple(blockers)


def evaluate_connection_candidate_cases(
    source_bundle: OSGaugeBundle,
    proposal: ConnectionCandidateProposal,
    admission: ConnectionAdmissionReceipt,
    cases: Mapping[str, OSGaugeBundle],
    *,
    policy: ConnectionEvaluationPolicy = ConnectionEvaluationPolicy(),
) -> ConnectionEvaluationReceipt:
    blockers = list(evaluation_binding_blockers(source_bundle, proposal, admission))
    source_digest = canonical_digest(source_bundle.to_dict())
    proposal_digest = canonical_digest(proposal.to_dict())
    selected = proposal.selected_receipt
    candidate_connection = proposal.selected_connection
    expected_receipt = "" if selected is None else selected.receipt_digest
    expected_connection = "" if selected is None else selected.candidate_connection_digest
    expected_rollback = "" if selected is None else selected.rollback_digest

    normalized = tuple(sorted((str(case_id), bundle) for case_id, bundle in cases.items()))
    if not normalized:
        blockers.append("evaluation_cases_empty")
    if len(normalized) > policy.max_cases:
        blockers.append("evaluation_case_limit_exceeded")
    if any(not case_id for case_id, _ in normalized):
        blockers.append("evaluation_case_id_missing")

    case_receipts = []
    if candidate_connection is not None:
        for case_id, bundle in normalized[: policy.max_cases]:
            case_receipts.append(
                evaluate_connection_case(
                    case_id,
                    bundle,
                    candidate_connection,
                    source_bundle,
                    policy,
                )
            )

    all_cases = bool(case_receipts) and all(case.admissible for case in case_receipts)
    strict_observed = any(case.curvature_strictly_decreased for case in case_receipts)
    if not all_cases:
        blockers.append("evaluation_cases_not_all_admissible")
    if policy.require_strict_improvement_in_one_case and not strict_observed:
        blockers.append("evaluation_strict_improvement_missing")

    ready = not blockers
    status = READY_STATUS if ready else BLOCKED_STATUS
    payload = {
        "version": VERSION,
        "status": status,
        "source_bundle_digest": source_digest,
        "proposal_digest": proposal_digest,
        "admission_receipt_digest": admission.receipt_digest,
        "selected_receipt_digest": expected_receipt,
        "candidate_connection_digest": expected_connection,
        "rollback_digest": expected_rollback,
        "case_receipts": [case.to_dict() for case in case_receipts],
        "evaluated_case_count": len(case_receipts),
        "all_cases_admissible": all_cases,
        "strict_improvement_observed": strict_observed,
        "staging_review_ready": ready,
        "production_apply_ready": False,
        "state_write_performed": False,
        "authority_widened": False,
        "blockers": blockers,
    }
    return ConnectionEvaluationReceipt(
        status=status,
        source_bundle_digest=source_digest,
        proposal_digest=proposal_digest,
        admission_receipt_digest=admission.receipt_digest,
        selected_receipt_digest=expected_receipt,
        candidate_connection_digest=expected_connection,
        rollback_digest=expected_rollback,
        case_receipts=tuple(case_receipts),
        evaluated_case_count=len(case_receipts),
        all_cases_admissible=all_cases,
        strict_improvement_observed=strict_observed,
        staging_review_ready=ready,
        production_apply_ready=False,
        state_write_performed=False,
        authority_widened=False,
        blockers=tuple(blockers),
        receipt_digest=canonical_digest(payload),
    )
