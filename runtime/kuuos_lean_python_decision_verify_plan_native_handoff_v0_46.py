"""Read-only original DecisionOS→VerifyOS→PlanOS six-route audit v0.46.

Call the actual unchanged DecisionOS v0.8 receipt builder, require its whole
output to be the input of each of the six unchanged VerifyOS v0.4 builders,
then delegate the complete native VerifyOS/PlanOS two-stage validation to
v0.45. All source envelopes are supplied, never synthesized here.

This finite operational reobservation does not prove Lean/CPython refinement,
external issuer identity, global atomic history, or host action authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import (
    kuuos_decisionos_bounded_plan_synthesis_request_handoff_v0_8 as decision,
)
from runtime import kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 as prior
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint

VERSION = "kuuos_lean_python_decision_verify_plan_native_handoff_v0_46"
SOURCE_PARENT = "959fad7db61f1f5a9f4a2ba219b04714e67c93f9"
SCOPED_COMPATIBLE = "SCOPED_DECISION_VERIFY_PLAN_NATIVE_HANDOFF_SIX_ROUTES_CHECKED"
BLOCKED = prior.BLOCKED
NO_DATA = prior.NO_DATA

DECISION_ARGS = frozenset((
    "source_selection_receipt",
    "synthesis_policy_digest",
    "planos_recipient_digest",
    "request_owner_responsibility_digest",
    "synthesis_request_id",
    "requested_selected_candidate_id",
    "selected_candidate_plan_intent_digest",
    "synthesis_constraint_spec",
    "synthesis_constraint_digest",
    "synthesis_handoff_bundle_digest",
))


@dataclass(frozen=True)
class DecisionVerifyPlanNativeAudit:
    status: str
    issues: tuple[str, ...] = ()
    original_decision_cases_run: int = 0
    original_verify_cases_run: int = 0
    original_plan_cases_run: int = 0
    full_decision_verify_packet_seams_checked: bool = False
    original_verify_plan_certificate_seams_checked: bool = False
    original_decision_source_unchanged: bool = False
    original_verify_plan_sources_unchanged: bool = False
    source_selection_receipt_digest: str | None = None
    original_decision_handoff_receipt_digest: str | None = None
    route_results: tuple[tuple[str, str, str, bool], ...] = ()
    unresolved: tuple[str, ...] = (
        "NATIVE_RECEIPT_GENERATION_IS_NOT_EXTERNAL_ISSUER_AUTHENTICATION",
        "FULL_LEAN_CPYTHON_SEMANTIC_REFINEMENT_NOT_PROVED",
        "SIX_ROUTE_CASES_NOT_ATOMIC_OR_CAUSALLY_ORDERED",
        "GLOBAL_DESCENT_NOT_CERTIFIED",
        "NO_PLAN_SYNTHESIS_OR_HOST_EXECUTION_AUTHORITY",
    )
    read_only: bool = True
    external_source_authenticated: bool = False
    global_descent_proved: bool = False
    plan_synthesis_performed: bool = False
    execution_permission_granted: bool = False
    git_or_memory_written: bool = False
    original_kernel_modified: bool = False


def _hold(status: str, *issues: str, decision_count: int = 0,
          verify_count: int = 0, plan_count: int = 0
          ) -> DecisionVerifyPlanNativeAudit:
    return DecisionVerifyPlanNativeAudit(
        status=status,
        issues=tuple(dict.fromkeys(issues)),
        original_decision_cases_run=decision_count,
        original_verify_cases_run=verify_count,
        original_plan_cases_run=plan_count,
    )


def audit_original_decision_verify_plan_native_handoff(
    supplied_decision_arguments: Any,
    supplied_verify_plan_cases: Any,
) -> DecisionVerifyPlanNativeAudit:
    """Verify a caller-supplied exact typed three-stage receipt chain.

    The original kernel constructs the DecisionOS handoff from a supplied
    selection receipt. The six VerifyOS/PlanOS envelopes must already exist.
    Neither historical issuance nor inter-case timing is manufactured.
    """
    if supplied_decision_arguments is None or supplied_verify_plan_cases is None:
        return _hold(NO_DATA, "original_decision_or_six_cases_missing")
    if type(supplied_decision_arguments) is not dict:
        return _hold(BLOCKED, "decision:plain_arguments_required")
    if type(supplied_verify_plan_cases) is not dict:
        return _hold(BLOCKED, "routes:plain_arguments_required")

    expected = set(prior.KIND_TO_STATUS)
    if set(supplied_verify_plan_cases) - expected:
        return _hold(BLOCKED, "routes:unknown_case")
    if set(supplied_verify_plan_cases) != expected:
        return _hold(NO_DATA, "routes:required_original_case_missing")
    if set(supplied_decision_arguments) != DECISION_ARGS:
        return _hold(BLOCKED, "decision:original_arguments_incomplete_or_extra")

    try:
        decision_data = prior._plain_copy(
            supplied_decision_arguments, "decision", dict,
        )
        route_data = prior._plain_copy(
            supplied_verify_plan_cases, "routes", dict,
        )
        decision_before = _fingerprint(decision_data)
        routes_before = _fingerprint(route_data)
    except (TypeError, ValueError, RecursionError, OverflowError) as exc:
        return _hold(BLOCKED, "sources:invalid_plain_finite_json:"
                     + type(exc).__name__)

    try:
        decision_result = decision.build_decisionos_bounded_plan_synthesis_request_handoff_receipt(
            **decision_data,
        )
    except (TypeError, ValueError, KeyError, RecursionError, OverflowError) as exc:
        return _hold(BLOCKED, "decision:original_builder_exception:"
                     + type(exc).__name__, decision_count=1)
    if (decision_result.status != decision.STATUS_READY
            or type(decision_result.receipt) is not dict
            or decision_result.blockers):
        return _hold(BLOCKED, "decision:original_handoff_not_ready",
                     decision_count=1)
    receipt = decision_result.receipt
    digest = receipt.get(
        "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
    )
    selection_digest = receipt.get("source_selection_receipt_digest")
    if (type(digest) is not str or not digest
            or type(selection_digest) is not str or not selection_digest):
        return _hold(BLOCKED, "decision:native_digest_missing",
                     decision_count=1)

    # Identity of the entire original native packet, including nested maps,
    # is stronger than agreement of one digest or selected-candidate label.
    # Fail before any downstream kernel runs if a seam is not exact.
    for kind in prior.KIND_TO_STATUS:
        envelope = route_data.get(kind)
        if type(envelope) is not dict:
            return _hold(BLOCKED, kind + ":original_envelope_invalid",
                         decision_count=1)
        verify_args = envelope.get("verify")
        if (type(verify_args) is not dict
                or type(verify_args.get("source_handoff_receipt")) is not dict
                or not prior._same(
                    verify_args["source_handoff_receipt"], receipt
                )):
            return _hold(
                BLOCKED, kind + ":original_decision_verify_full_receipt_mismatch",
                decision_count=1,
            )

    downstream = prior.audit_original_verify_plan_six_routes(route_data)
    if downstream.status != prior.SCOPED_COMPATIBLE:
        return _hold(
            downstream.status,
            *("verify_plan:" + item for item in downstream.issues),
            decision_count=1,
            verify_count=downstream.original_verify_cases_run,
            plan_count=downstream.original_plan_cases_run,
        )
    try:
        decision_unchanged = (
            decision_before == _fingerprint(decision_data)
            and decision_before == _fingerprint(supplied_decision_arguments)
        )
        routes_unchanged = (
            routes_before == _fingerprint(route_data)
            and routes_before == _fingerprint(supplied_verify_plan_cases)
        )
    except (TypeError, ValueError, RecursionError, OverflowError):
        return _hold(BLOCKED, "sources:reobservation_invalid",
                     decision_count=1,
                     verify_count=downstream.original_verify_cases_run,
                     plan_count=downstream.original_plan_cases_run)

    if not decision_unchanged or not routes_unchanged:
        return _hold(BLOCKED, "sources:original_inputs_mutated",
                     decision_count=1,
                     verify_count=downstream.original_verify_cases_run,
                     plan_count=downstream.original_plan_cases_run)

    if (downstream.source_handoff_receipt_digest != digest
            or downstream.original_verify_cases_run != 6
            or downstream.original_plan_cases_run != 6
            or not downstream.complete_original_certificate_seams_checked):
        return _hold(BLOCKED, "routes:original_native_seam_incomplete",
                     decision_count=1,
                     verify_count=downstream.original_verify_cases_run,
                     plan_count=downstream.original_plan_cases_run)

    return DecisionVerifyPlanNativeAudit(
        status=SCOPED_COMPATIBLE,
        original_decision_cases_run=1,
        original_verify_cases_run=downstream.original_verify_cases_run,
        original_plan_cases_run=downstream.original_plan_cases_run,
        full_decision_verify_packet_seams_checked=True,
        original_verify_plan_certificate_seams_checked=True,
        original_decision_source_unchanged=True,
        original_verify_plan_sources_unchanged=True,
        source_selection_receipt_digest=selection_digest,
        original_decision_handoff_receipt_digest=digest,
        route_results=downstream.route_results,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "BLOCKED", "NO_DATA",
    "DECISION_ARGS", "DecisionVerifyPlanNativeAudit",
    "audit_original_decision_verify_plan_native_handoff",
)
