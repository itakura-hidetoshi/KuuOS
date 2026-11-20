"""v0.45 original VerifyOS→PlanOS six-route conditional semantic witness.

Execute the UNCHANGED original Python VerifyOS v0.4 and PlanOS v1.03
middle-way certificate kernels over six separately supplied original
input envelopes. Bind each PlanOS intake to its corresponding ACTUAL
VerifyOS output (entire certificate, not just a plausible summary).
Test all finite routes against the independent Lean string-model table.

This is selected, read-only runtime evidence. The corresponding Lean
proof describes the finite source tables, not the CPython interpreter.
No plan synthesis, host action, source issuer, or Git authority follows.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import (
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
)
from runtime import (
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45"
SOURCE_PARENT = "0be0755998af0d07ad7c66514293f15731d9f5e3"
SCOPED_COMPATIBLE = "SCOPED_VERIFY_PLAN_SIX_NATIVE_MIDDLE_WAY_ROUTES_CHECKED"
ROUTES = (
    ("retain", "valid", "bounded_synthesis_intake_ready", True),
    ("suspend", "suspended", "await_condition_change", False),
    ("request_revision", "revision_required", "return_to_decisionos_revision", False),
    ("supersede_with_lineage", "superseded",
     "successor_lineage_reverification_required", False),
    ("complete", "completed", "close_without_synthesis", False),
    ("terminate", "terminated", "terminate_without_synthesis", False),
)
KIND_TO_STATUS = {kind: status for kind, status, _, _ in ROUTES}
STATUS_TO_DISPOSITION = {
    status: disposition for _, status, disposition, _ in ROUTES
}
VERIFY_ARGS = frozenset((
    "source_handoff_receipt",
    "verification_policy_digest",
    "verification_owner_responsibility_digest",
    "verification_request_id",
    "transition_spec",
    "transition_spec_digest",
    "verification_bundle_digest",
))
PLAN_ARGS = frozenset((
    "source_verifyos_certificate",
    "expected_source_verifyos_certificate_digest",
    "expected_source_handoff_receipt_digest",
    "expected_world_binding_digest",
    "expected_world_model_state_digest",
    "expected_world_model_revision",
    "expected_world_lineage_digest",
    "expected_selected_candidate_id",
    "expected_selected_candidate_plan_intent_digest",
    "expected_synthesis_constraint_digest",
    "intake_policy_digest",
    "planos_intake_responsibility_digest",
    "intake_request_id",
    "intake_bundle_digest",
))
VERIFY_TRUE = (
    "verification_passed", "conditions_explicit", "changed_conditions_explicit",
    "predecessor_preserved", "lineage_monotone",
    "responsibility_preserved", "dissent_preserved",
    "minority_evidence_preserved", "object_not_reified", "object_not_erased",
    "commitment_not_absolutized", "termination_does_not_erase_history",
    "selection_remains_decisionos_owned", "authority_unchanged",
    "execution_permission_not_granted", "persistent_world_state_unchanged",
    "future_only",
)
VERIFY_FALSE = (
    "plan_synthesis_performed", "concrete_plan_issued", "plan_receipt_issued",
    "active_now", "execution_permission",
)
PLAN_TRUE = (
    "conditional_validity_enforced", "only_valid_status_admitted",
    "nonvalid_status_not_synthesized", "source_conditions_preserved",
    "source_lineage_preserved", "source_predecessor_preserved",
    "source_responsibility_preserved", "source_dissent_preserved",
    "source_minority_evidence_preserved",
    "responsibility_extended_not_replaced",
    "selection_remains_decisionos_owned",
    "persistent_world_state_unchanged", "future_only",
)
PLAN_FALSE = (
    "selection_authority_granted_to_planos",
    "plan_synthesis_performed", "concrete_plan_issued", "plan_receipt_issued",
    "execution_authority_granted", "execution_permission", "active_now",
)
UNRESOLVED = (
    "LEAN_TO_CPYTHON_EVALUATION_REFINEMENT_NOT_FORMALLY_PROVED",
    "LEAN_FORMAL_MODEL_IS_NOT_ORIGINAL_KERNEL_PROOF",
    "EXTERNAL_DECISIONOS_ISSUER_NOT_AUTHENTICATED",
    "SIX_CASES_ARE_NOT_ONE_ATOMIC_OR_CAUSAL_HISTORY",
    "ACTUAL_HOST_EXECUTION_PERMISSION_UNAVAILABLE",
    "GLOBAL_DESCENT_AND_WORLD_TRUTH_NOT_CERTIFIED",
)
HOLD_ADVICE = (
    ("CodeAI", "HOLD_EXACT_SOURCE_REOBSERVATION_REQUIRED"),
    ("MemoryOS", "PRESERVE_EVIDENCE_NO_WRITE"),
    ("DecisionOS", "HOLD_NOT_TRUTH"),
    ("PlanOS", "HOLD_NOT_SYNTHESIS"),
)
CHECKED_ADVICE = (
    ("CodeAI", "TEST_REQUIRED_NO_AUTO_MERGE"),
    ("MemoryOS", "APPEND_ONLY_PROPOSAL_NOT_WRITTEN"),
    ("DecisionOS", "CONDITIONAL_SOURCE_ADVISORY_NOT_TRUTH"),
    ("PlanOS", "BOUNDED_INTAKE_ROUTING_NOT_SYNTHESIS"),
)


@dataclass(frozen=True)
class VerifyPlanSixRoutesAudit:
    status: str
    issues: tuple[str, ...] = ()
    original_verify_cases_run: int = 0
    original_plan_cases_run: int = 0
    route_results: tuple[tuple[str, str, str, bool], ...] = ()
    original_certificate_digest_pairs: tuple[tuple[str, str, str], ...] = ()
    source_handoff_receipt_digest: str | None = None
    original_python_source_tables_checked: bool = False
    complete_original_certificate_seams_checked: bool = False
    original_source_inputs_unchanged: bool = False
    read_only_consumer_advice: tuple[tuple[str, str], ...] = HOLD_ADVICE
    unresolved: tuple[str, ...] = UNRESOLVED
    lean_model_witness_constructed_by_this_python_process: bool = False
    lean_cpython_refinement_proved: bool = False
    globally_atomic_six_case_history_proved: bool = False
    external_source_authenticated: bool = False
    common_causal_clock_proved: bool = False
    global_descent_proved: bool = False
    verification_grants_truth_authority: bool = False
    selection_authority_granted_to_planos: bool = False
    plan_synthesis_performed: bool = False
    execution_permission_granted: bool = False
    host_action_performed: bool = False
    memoryos_write_performed: bool = False
    git_authority_granted: bool = False
    original_kernel_modified: bool = False


def _hold(status: str, *issues: str) -> VerifyPlanSixRoutesAudit:
    return VerifyPlanSixRoutesAudit(
        status=status, issues=tuple(dict.fromkeys(issues)),
    )


def _same(a: Any, b: Any) -> bool:
    return _fingerprint(a) == _fingerprint(b)


def _plain_copy(value: Any, label: str, expected_type: type) -> Any:
    if type(value) is not expected_type:
        raise ValueError(label + ":plain_" + expected_type.__name__ + "_required")
    result = _finite_json(value)
    if type(result) is not expected_type:
        raise ValueError(label + ":exact_json_type_required")
    return result


def _route_flags(cert: dict, required_true: tuple[str, ...],
                 required_false: tuple[str, ...], label: str) -> tuple[str, ...]:
    return tuple(
        label + ":required_true:" + name
        for name in required_true if cert.get(name) is not True
    ) + tuple(
        label + ":required_false:" + name
        for name in required_false if cert.get(name) is not False
    )


def audit_original_verify_plan_six_routes(
    supplied_cases: Any,
) -> VerifyPlanSixRoutesAudit:
    """Run both original full certificate builders, never synthesize inputs.

    Each case is an independent supplied DecisionOS source / VerifyOS
    transition request / PlanOS intake request, NOT a global state sequence.
    """
    if supplied_cases is None:
        return _hold(NO_DATA, "cases:original_envelopes_missing")
    if type(supplied_cases) is not dict:
        return _hold(BLOCKED, "cases:plain_named_dictionary_required")
    expected_kinds = set(KIND_TO_STATUS)
    if set(supplied_cases) - expected_kinds:
        return _hold(BLOCKED, "cases:unknown_transition_kind")
    absent = tuple(kind + ":original_case_missing" for kind in KIND_TO_STATUS
                   if supplied_cases.get(kind) is None)
    if absent:
        return _hold(NO_DATA, *absent)

    try:
        data = _plain_copy(supplied_cases, "cases", dict)
        original_digest = _fingerprint(data)
    except (TypeError, ValueError, RecursionError, OverflowError) as exc:
        return _hold(BLOCKED, "cases:original_source_invalid:"
                     + type(exc).__name__)

    if (type(verify.TRANSITION_TO_STATUS) is not dict
            or type(plan.TRANSITION_TO_STATUS) is not dict
            or type(plan.STATUS_TO_DISPOSITION) is not dict
            or not _same(verify.TRANSITION_TO_STATUS, KIND_TO_STATUS)
            or not _same(plan.TRANSITION_TO_STATUS, KIND_TO_STATUS)
            or not _same(plan.STATUS_TO_DISPOSITION, STATUS_TO_DISPOSITION)):
        return _hold(BLOCKED, "original_kernels:finite_routing_tables_changed")

    issues: list[str] = []
    rows: list[tuple[str, str, str, bool]] = []
    digests: list[tuple[str, str, str]] = []
    verify_count = 0
    plan_count = 0
    source_receipt_digest: str | None = None

    for kind, status, disposition, admitted in ROUTES:
        envelope = data[kind]
        if type(envelope) is not dict or set(envelope) != {"verify", "plan"}:
            issues.append(kind + ":original_case_envelope_invalid")
            continue
        ver_args, intake_args = envelope.get("verify"), envelope.get("plan")
        if type(ver_args) is not dict or type(intake_args) is not dict:
            issues.append(kind + ":plain_original_arguments_required")
            continue
        if set(ver_args) != VERIFY_ARGS or set(intake_args) != PLAN_ARGS:
            issues.append(kind + ":original_kernel_arguments_incomplete_or_extra")
            continue
        if (type(ver_args["transition_spec"]) is not dict
                or ver_args["transition_spec"].get("transition_kind") != kind):
            issues.append(kind + ":original_transition_spec_mismatch")
            continue
        try:
            verify_outcome = verify.build_verifyos_middle_way_conditional_continuity_certificate(
                **ver_args,
            )
            verify_count += 1
        except (TypeError, ValueError, KeyError, RecursionError, OverflowError) as exc:
            issues.append(kind + ":original_verify_exception:" + type(exc).__name__)
            continue
        if (verify_outcome.status != verify.STATUS_READY
                or type(verify_outcome.certificate) is not dict
                or verify_outcome.blockers):
            issues.append(kind + ":original_verify_not_ready")
            continue
        vcert = verify_outcome.certificate
        issues.extend(_route_flags(vcert, VERIFY_TRUE, VERIFY_FALSE,
                                   kind + ":verify"))
        if (vcert.get("transition_kind") != kind
                or vcert.get("conditional_validity_status") != status):
            issues.append(kind + ":original_verify_route_mismatch")
        if (not _same(intake_args.get("source_verifyos_certificate"), vcert)):
            issues.append(kind + ":original_full_certificate_seam_mismatch")
            continue

        try:
            intake_outcome = plan.build_planos_middle_way_bounded_synthesis_intake_certificate(
                **intake_args,
            )
            plan_count += 1
        except (TypeError, ValueError, KeyError, RecursionError, OverflowError) as exc:
            issues.append(kind + ":original_intake_exception:" + type(exc).__name__)
            continue
        if (intake_outcome.status != plan.STATUS_READY
                or type(intake_outcome.certificate) is not dict
                or intake_outcome.blockers):
            issues.append(kind + ":original_intake_not_ready")
            continue
        pcert = intake_outcome.certificate
        issues.extend(_route_flags(pcert, PLAN_TRUE, PLAN_FALSE,
                                   kind + ":plan"))
        if (pcert.get("conditional_validity_status") != status
                or pcert.get("transition_kind") != kind
                or pcert.get("intake_disposition") != disposition
                or pcert.get("bounded_synthesis_request_admitted") is not admitted
                or pcert.get("bounded_synthesis_intake_ready") is not admitted):
            issues.append(kind + ":original_plan_route_mismatch")
        source_id = vcert.get("source_handoff_receipt_digest")
        if type(source_id) is not str or not source_id:
            issues.append(kind + ":original_handoff_digest_missing")
        elif source_receipt_digest is None:
            source_receipt_digest = source_id
        elif source_id != source_receipt_digest:
            issues.append(kind + ":cross_case_original_handoff_source_mismatch")
        if not _same(pcert.get("source_verifyos_certificate_digest"),
                     vcert.get("verifyos_middle_way_conditional_continuity_certificate_digest")):
            issues.append(kind + ":intake_source_verify_digest_mismatch")
        rows.append((kind, status, disposition, admitted))
        digests.append((
            kind,
            str(vcert.get(
                "verifyos_middle_way_conditional_continuity_certificate_digest", ""
            )),
            str(pcert.get("planos_middle_way_bounded_synthesis_intake_certificate_digest", "")),
        ))

    unchanged = False
    try:
        unchanged = original_digest == _fingerprint(data)
        # Also compare caller data after native kernel calls, not only copied data.
        unchanged = unchanged and original_digest == _fingerprint(supplied_cases)
    except (TypeError, ValueError, RecursionError, OverflowError):
        issues.append("cases:original_input_reobservation_invalid")
    if not unchanged:
        issues.append("cases:original_inputs_mutated_during_audit")

    if verify_count != len(ROUTES) or plan_count != len(ROUTES):
        issues.append("cases:not_all_original_kernels_executed")
    passed = not issues
    return VerifyPlanSixRoutesAudit(
        status=SCOPED_COMPATIBLE if passed else BLOCKED,
        issues=tuple(dict.fromkeys(issues)),
        original_verify_cases_run=verify_count,
        original_plan_cases_run=plan_count,
        route_results=tuple(rows),
        original_certificate_digest_pairs=tuple(digests),
        source_handoff_receipt_digest=source_receipt_digest,
        original_python_source_tables_checked=passed,
        complete_original_certificate_seams_checked=passed,
        original_source_inputs_unchanged=unchanged,
        read_only_consumer_advice=CHECKED_ADVICE if passed else HOLD_ADVICE,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "BLOCKED", "NO_DATA",
    "ROUTES", "KIND_TO_STATUS", "STATUS_TO_DISPOSITION", "VERIFY_ARGS",
    "PLAN_ARGS", "VerifyPlanSixRoutesAudit",
    "audit_original_verify_plan_six_routes",
)
