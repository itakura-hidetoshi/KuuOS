"""ObserveOS: source-bind comparison/debt claims to real Act→Observe state.

Requires both original committed states and the exact typed handoff.
It performs NO observation collection and grants NO verification/truth authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, UnavailableSource, copied_state, copied_edge, fail,
    field, truth, string, require_match, finalize,
)
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    READY as HOST_READY, receipt_digest as original_host_receipt_digest,
)
from runtime.kuuos_observe_os_types_v0_1 import (
    comparison_receipt_digest as original_comparison_digest,
)

OS_NAME = "ObserveOS"
ROUTES = {
    "MATCHED": "OBSERVATION_MATCHED",
    "DIVERGENT": "OBSERVATION_DIVERGENT",
    "INCONCLUSIVE": "OBSERVATION_INCONCLUSIVE",
    "CONFLICTED": "OBSERVATION_CONFLICTED",
}


def audit_native_observe_from_act(act_state: Any, observe_state: Any):
    try:
        act = copied_state("ActOS", act_state)
        observe = copied_state(OS_NAME, observe_state)
        copied_edge("ActOS", OS_NAME, act, observe)
        host = field(act, "host_receipt", "ActOS")
        host_digest = string(host, "host_receipt_digest", "ActOS.host_receipt")
        require_match(host_digest, original_host_receipt_digest(host),
                      "ActOS.host_receipt.digest")
        require_match(string(act, "host_receipt_digest", "ActOS"), host_digest,
                      "ActOS.host_receipt.source_binding")
        comparison = field(observe, "comparison_receipt", OS_NAME)
        comp_digest = string(comparison, "comparison_receipt_digest", "ObserveOS.comparison")
        require_match(comp_digest, original_comparison_digest(comparison),
                      "ObserveOS.comparison_receipt.digest")
        require_match(string(observe, "comparison_receipt_digest", OS_NAME), comp_digest,
                      "ObserveOS.comparison_receipt.source_binding")
        verdict = string(comparison, "verdict", "ObserveOS.comparison")
        if verdict not in ROUTES:
            raise UnavailableSource("ObserveOS:comparison_verdict_invalid", BLOCKED)
        require_match(string(observe, "route", "ObserveOS"), ROUTES[verdict],
                      "ObserveOS:original_route_mismatch")
        projection = {
            "committedActState": act["current_phase"] == "commit",
            "effectRecorded": truth(act, "effect_recorded", "ActOS"),
            "canonicalReadyReceipt": string(host, "status", "ActOS.host_receipt") == HOST_READY,
            "comparisonIsVerification": truth(
                comparison, "comparison_is_verification", "ObserveOS.comparison"),
            "verdict": verdict.lower(),
            "observationDebtDischarged": truth(
                observe, "observation_debt_discharged", "ObserveOS"),
            "reobservationRequired": truth(observe, "reobservation_required", "ObserveOS"),
            "verificationRequired": truth(observe, "verification_required", "ObserveOS"),
        }
        paths = [
            "ActOS.current_phase", "ActOS.effect_recorded",
            "ActOS.host_receipt.host_receipt_digest",
            "ActOS.host_receipt.status",
            "ObserveOS.source_act_state_digest",
            "ObserveOS.comparison_receipt.comparison_receipt_digest",
            "ObserveOS.comparison_receipt.comparison_is_verification",
            "ObserveOS.comparison_receipt.verdict",
            "ObserveOS.route",
            "ObserveOS.observation_debt_discharged",
            "ObserveOS.reobservation_required",
            "ObserveOS.verification_required",
        ]
        return finalize(OS_NAME, observe, [projection], paths, edge_validated=True)
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (TypeError, ValueError, KeyError, AttributeError) as exc:
        return fail(OS_NAME, "original_receipt_digest_check:" + type(exc).__name__,
                    status=BLOCKED)


__all__ = ("OS_NAME", "audit_native_observe_from_act")
