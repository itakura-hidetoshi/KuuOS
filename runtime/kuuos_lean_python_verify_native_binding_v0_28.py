"""VerifyOS: source-bind evidence adjudication and debt to real ObserveOS.

Only a typed original Observe→Verify handoff and native saved receipt
permit this local comparison; it does not assert external causality/truth.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any

from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, UnavailableSource, copied_state, copied_edge, fail,
    field, truth, string, require_match, finalize,
)
from runtime.kuuos_verify_os_types_v0_1 import (
    adjudication_receipt_digest as original_adjudication_digest,
    corroboration_report_digest as original_corroboration_digest,
)

OS_NAME = "VerifyOS"
ROUTES = {
    "PASSED": "VERIFICATION_PASSED",
    "FAILED": "VERIFICATION_FAILED",
    "INDETERMINATE": "VERIFICATION_INDETERMINATE",
}


def audit_native_verify_from_observe(observe_state: Any, verify_state: Any):
    try:
        observe = copied_state("ObserveOS", observe_state)
        verify = copied_state(OS_NAME, verify_state)
        copied_edge("ObserveOS", OS_NAME, observe, verify)
        adjudication = field(verify, "adjudication_receipt", "VerifyOS")
        receipt_id = string(adjudication, "adjudication_receipt_digest",
                            "VerifyOS.adjudication_receipt")
        require_match(receipt_id, original_adjudication_digest(adjudication),
                      "VerifyOS.adjudication.digest")
        require_match(string(verify, "adjudication_receipt_digest", "VerifyOS"),
                      receipt_id, "VerifyOS.adjudication.saved_digest")
        report = field(verify, "corroboration_report", "VerifyOS")
        report_id = string(report, "corroboration_report_digest",
                           "VerifyOS.corroboration_report")
        require_match(report_id, original_corroboration_digest(report),
                      "VerifyOS.corroboration.digest")
        require_match(string(verify, "corroboration_report_digest", "VerifyOS"),
                      report_id, "VerifyOS.corroboration.saved_digest")
        source_route = string(observe, "route", "ObserveOS")
        require_match(string(verify, "source_observation_route", "VerifyOS"),
                      source_route, "VerifyOS.source_observation_route")
        verdict = string(adjudication, "verdict", "VerifyOS.adjudication")
        if verdict not in ROUTES:
            raise UnavailableSource("VerifyOS:verdict_not_recognized", BLOCKED)
        require_match(string(verify, "route", "VerifyOS"), ROUTES[verdict],
                      "VerifyOS:verdict_route_mismatch")
        challenge = field(verify, "challenge_packet", "VerifyOS")
        falsifier = truth(adjudication, "falsifier_triggered",
                          "VerifyOS.adjudication")
        require_match(falsifier, truth(challenge, "falsifier_triggered",
                                      "VerifyOS.challenge"), "VerifyOS:falsifier_source")
        projection = {
            "verdict": verdict.lower(),
            "sourceMatched": source_route == "OBSERVATION_MATCHED",
            "sourceDivergent": source_route == "OBSERVATION_DIVERGENT",
            "corroborationAdmissible": truth(
                report, "admissible_for_conclusive_verdict",
                "VerifyOS.corroboration"),
            "criterionSatisfied": truth(
                adjudication, "criterion_satisfied", "VerifyOS.adjudication"),
            "falsifierTriggered": falsifier,
            "verificationIsTruth": truth(
                adjudication, "verification_is_absolute_truth", "VerifyOS.adjudication"),
            "causalAttributionGranted": truth(
                adjudication, "causal_attribution_granted", "VerifyOS.adjudication"),
            "verificationDebtDischarged": truth(
                verify, "verification_debt_discharged", "VerifyOS"),
            "verificationRequired": truth(verify, "verification_required", "VerifyOS"),
            "reobservationRequired": truth(verify, "reobservation_required", "VerifyOS"),
            "correctiveActionRequired": truth(
                verify, "corrective_action_required", "VerifyOS"),
            "learningRequired": truth(verify, "learning_required", "VerifyOS"),
        }
        paths = [
            "ObserveOS.route", "ObserveOS.observe_state_digest",
            "VerifyOS.source_observe_state_digest",
            "VerifyOS.source_observation_route", "VerifyOS.route",
            "VerifyOS.corroboration_report.corroboration_report_digest",
            "VerifyOS.corroboration_report.admissible_for_conclusive_verdict",
            "VerifyOS.adjudication_receipt.adjudication_receipt_digest",
            "VerifyOS.adjudication_receipt.verdict",
            "VerifyOS.adjudication_receipt.criterion_satisfied",
            "VerifyOS.adjudication_receipt.falsifier_triggered",
            "VerifyOS.challenge_packet.falsifier_triggered",
            "VerifyOS.adjudication_receipt.verification_is_absolute_truth",
            "VerifyOS.adjudication_receipt.causal_attribution_granted",
            "VerifyOS.verification_debt_discharged", "VerifyOS.verification_required",
            "VerifyOS.reobservation_required", "VerifyOS.corrective_action_required",
            "VerifyOS.learning_required",
        ]
        return finalize(OS_NAME, verify, [projection], paths, edge_validated=True)
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (TypeError, ValueError, KeyError, AttributeError) as exc:
        return fail(OS_NAME, "original_evidence_digest_check:" + type(exc).__name__,
                    status=BLOCKED)


__all__ = ("OS_NAME", "audit_native_verify_from_observe")
