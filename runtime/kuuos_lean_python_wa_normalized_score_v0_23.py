"""Native Wa final-score normalized comparison, bounded rational observation.

This additive, read-only v0.23 witness reruns the original v0.20 native
7-axis arithmetic trace, v0.21 weighted-product certificates, and v0.22
mathematical normalization certificate, then checks the original final
Wa interval's lower and upper endpoints against the exact rational
normalized-ideal comparison score.

It keeps the measured final native-score discrepancy separate from the
v0.20 two-stage relational/alert arithmetic discrepancy. It NEVER
asserts that arbitrary Python float evaluation satisfies IEEE-754
formal semantics, nor authenticates external issuer/history/authority.
No original Wa kernel, event, ledger, score, receipt or store is changed.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from runtime import kuuos_lean_python_wa_normalization_v0_22 as previous
from runtime import kuuos_lean_python_wa_weighted_sum_certificate_v0_21 as v21
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint

VERSION = "kuuos_lean_python_wa_normalized_score_v0_23"
SOURCE_MAIN = "d0d62b0bf15fda60900532b245f4e1b23b3222cc"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


class WaNormalizedScoreError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, status: str = BLOCKED) -> None:
    raise WaNormalizedScoreError(status, (issue,))


def _copy(value: Any, label: str, kind: type) -> Any:
    try:
        return previous._copy(value, label, kind)
    except previous.WaNormalizationError as exc:
        raise WaNormalizedScoreError(exc.status, exc.issues) from exc


def _required(mapping: dict, key: str, label: str) -> Any:
    if key not in mapping:
        _fail(label + ":" + key + ":missing", NO_DATA)
    return mapping[key]


def _q_pair(value: Any, label: str) -> Fraction:
    try:
        return previous._q_pair(value, label)
    except previous.WaNormalizationError as exc:
        raise WaNormalizedScoreError(exc.status, exc.issues) from exc


def _q_float(value: Any, label: str) -> Fraction:
    try:
        return previous._q_float(previous._native_float(value, label))
    except previous.WaNormalizationError as exc:
        raise WaNormalizedScoreError(exc.status, exc.issues) from exc


def _pair(q: Fraction) -> list[int]:
    return [q.numerator, q.denominator]


def _rational_ideal(
    beta: Fraction, weighted: Fraction, weakest: Fraction, alert: Fraction,
) -> Fraction:
    return ((1 - beta) * weighted + beta * weakest) * (1 - alert)


def certify_normalized_final_trace(
    profile: Any, weights: Any, beta: Any,
) -> dict[str, Any]:
    """Rerun original native observation and explicitly certify both Wa scores.

    This function by itself cannot authenticate a free-standing caller-supplied
    profile. The surrounding state audit validates the stored Wa state first.
    """
    p = _copy(profile, "profile", dict)
    w = _copy(weights, "weights", dict)
    b = _q_float(beta, "beta")
    if not 0 <= b <= 1:
        _fail("beta:unit_interval_required")
    try:
        trace = v20.trace_native_wa_score(p, w, beta)
        weighted = v21.certify_weighted_trace(trace)
        normalized = previous.certify_normalized_profile(p, w, weighted)
    except (v20.WaBinary64MidpointError, v21.WaWeightedSumError,
            previous.WaNormalizationError) as exc:
        raise WaNormalizedScoreError(exc.status, ("prior:" + ";".join(exc.issues),)) from exc
    items = _copy(_required(normalized, "endpoint_certificates", "normalization"),
                  "normalized_endpoints", list)
    weighted_rows = _copy(_required(weighted, "endpoints", "weighted"),
                          "weighted_endpoints", list)
    fields = _copy(_required(trace, "fields", "trace"), "fields", dict)
    if len(items) != 2 or len(weighted_rows) != 2:
        _fail("wa:two_endpoints_required")
    output: list[dict[str, Any]] = []
    for bound, alert_bound, cert, raw in zip(
        ("lower", "upper"), ("upper", "lower"), items, weighted_rows
    ):
        row = _copy(cert, "normalized:" + bound, dict)
        wr = _copy(raw, "weighted:" + bound, dict)
        if _required(row, "endpoint", bound) != bound:
            _fail("wa:" + bound + ":normalized_endpoint_order_mismatch")
        if _required(wr, "bound", bound) != bound:
            _fail("wa:" + bound + ":weighted_endpoint_order_mismatch")
        if _required(row, "conditional_lean_inequality_checked", bound) is not True:
            _fail("wa:" + bound + ":normalization_certificate_required")
        if _required(wr, "bound_checked", bound) is not True:
            _fail("wa:" + bound + ":product_certificates_required")
        obsWeighted = _q_pair(
            _required(row, "native_observed_weighted", bound), bound + ":observed_weighted")
        if obsWeighted != _q_pair(_required(wr, "native_weighted", bound),
                                  bound + ":original_weighted"):
            _fail("wa:" + bound + ":weighted_source_identity_failed")
        exactRaw = _q_pair(_required(row, "exact_raw_weighted", bound),
                           bound + ":exact_raw")
        if exactRaw != _q_pair(_required(wr, "exact_weighted", bound),
                               bound + ":exact_products"):
            _fail("wa:" + bound + ":seven_product_identity_failed")
        normWeighted = _q_pair(
            _required(row, "exact_normalized_weighted", bound),
            bound + ":normalized_weighted")
        normBudget = _q_pair(
            _required(row, "combined_error_bound", bound), bound + ":norm_budget")
        if normBudget < 0 or abs(obsWeighted - normWeighted) > normBudget:
            _fail("wa:" + bound + ":weighted_normalization_error_failed")
        weakest = _q_float(_required(fields, "weakest_interval." + bound, bound),
                           bound + ":weakest")
        alert = _q_float(_required(fields, "alert_interval." + alert_bound, bound),
                         bound + ":alert")
        rel = _q_float(_required(fields, "relational_interval." + bound, bound),
                       bound + ":relational")
        observedWa = _q_float(_required(fields, "wa_interval." + bound, bound),
                              bound + ":wa")
        if not 0 <= weakest <= 1 or not 0 <= alert <= 1:
            _fail("wa:" + bound + ":original_endpoint_not_unit")
        rawIdeal = _rational_ideal(b, obsWeighted, weakest, alert)
        normalizedIdeal = _rational_ideal(b, normWeighted, weakest, alert)
        observedRawError = abs(observedWa - rawIdeal)
        weightedIdealShift = abs(rawIdeal - normalizedIdeal)
        if weightedIdealShift > abs(obsWeighted - normWeighted):
            _fail("wa:" + bound + ":relational_weight_contraction_failed")
        mixExact = (1 - b) * obsWeighted + b * weakest
        epsRel = abs(rel - mixExact)
        epsOut = abs(observedWa - rel * (1 - alert))
        if observedRawError > epsOut + epsRel:
            _fail("wa:" + bound + ":two_stage_error_composition_failed")
        finalError = abs(observedWa - normalizedIdeal)
        composedBound = observedRawError + normBudget
        twoStageBound = epsOut + epsRel + normBudget
        if finalError > composedBound or finalError > twoStageBound:
            _fail("wa:" + bound + ":final_normalized_score_bound_failed")
        output.append({
            "endpoint": bound,
            "normalized_ideal_score": _pair(normalizedIdeal),
            "original_raw_ideal_score": _pair(rawIdeal),
            "observed_native_wa_score": _pair(observedWa),
            "observed_native_weighted": _pair(obsWeighted),
            "exact_normalized_weighted": _pair(normWeighted),
            "measured_raw_wa_error": _pair(observedRawError),
            "measured_wa_relational_stage_error": _pair(epsRel),
            "measured_wa_alert_stage_error": _pair(epsOut),
            "weighted_ideal_contraction_error": _pair(weightedIdealShift),
            "normalized_weighted_budget": _pair(normBudget),
            "observed_final_score_error": _pair(finalError),
            "composed_score_error_upper_bound": _pair(composedBound),
            "two_stage_composed_upper_bound": _pair(twoStageBound),
            "conditional_score_bound_checked": True,
            "python_builtin_sum_semantics_proved": False,
        })
    # The mathematical normalized ideal interval is a comparison construct.
    # The original native upper endpoint may have been clipped; never infer
    # an original-native interval type from this conditional comparison.
    return {
        "option_id": _required(p, "option_id", "profile"),
        "endpoints": output,
        "normalized_final_score_ideal_only": True,
        "original_score_modified": False,
        "global_ieee754_semantics_proved": False,
        "all_input_python_lean_refinement_proved": False,
        "external_issuer_authenticated": False,
        "host_authority_granted": False,
    }


def audit_wa_normalized_final_state(state: Any) -> dict[str, Any]:
    """Full original Wa state audit followed by local final score witnesses."""
    try:
        source = previous.audit_wa_normalization_state(state)
    except previous.WaNormalizationError as exc:
        raise WaNormalizedScoreError(exc.status, ("v022:" + ";".join(exc.issues),)) from exc
    s = _copy(state, "state", dict)
    result = {
        "version": VERSION,
        "source_main": SOURCE_MAIN,
        "state_digest": _fingerprint(s),
        "certificates": [],
        "all_local_final_score_checks_passed": False,
        "global_ieee754_semantics_proved": False,
        "python_lean_full_refinement_proved": False,
        "external_issuer_authenticated": False,
        "host_authority_granted": False,
        "original_state_modified": False,
    }
    phase = _required(s, "current_phase", "state")
    if v20.native._PHASES.index(phase) < v20.native._PHASES.index("evaluate"):
        return result
    profiles = _copy(_required(s, "profiles", "state"), "profiles", list)
    weights = _copy(_required(s, "weights", "state"), "weights", dict)
    thresholds = _copy(_required(s, "thresholds", "state"), "thresholds", dict)
    beta = _required(thresholds, "bottleneck_weight", "thresholds")
    if len(profiles) != len(source["certificates"]):
        _fail("state:normalization_certificate_count_mismatch")
    for p, cert in zip(profiles, source["certificates"]):
        score = certify_normalized_final_trace(p, weights, beta)
        if score["option_id"] != cert.get("option_id"):
            _fail("state:source_option_identity_mismatch")
        sourceRows = cert.get("endpoint_certificates")
        if type(sourceRows) is not list or len(sourceRows) != 2:
            _fail("state:source_endpoints_missing", NO_DATA)
        for scoreRow, priorRow in zip(score["endpoints"], sourceRows):
            if (scoreRow["endpoint"] != priorRow.get("endpoint") or
                    scoreRow["exact_normalized_weighted"] !=
                    priorRow.get("exact_normalized_weighted")):
                _fail("state:normalized_source_compatibility_failed")
        result["certificates"].append(score)
    result["all_local_final_score_checks_passed"] = True
    return result


def checked_apply_wa_normalized_final_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """One existing native event adapter; no extra host execution."""
    args = [_copy(x, label, dict) for x, label in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief"),
    )]
    audit_wa_normalized_final_state(args[0])
    old = _fingerprint(args)
    try:
        value = previous.checked_apply_wa_normalization_event(*args)
    except previous.WaNormalizationError as exc:
        raise WaNormalizedScoreError(exc.status, ("v022:" + ";".join(exc.issues),)) from exc
    except Exception as exc:
        _fail("prior_adapter_exception:" + type(exc).__name__)
    if _fingerprint(args) != old:
        _fail("native_adapter_mutated_caller_arguments")
    result = _copy(value, "result", dict)
    audit_wa_normalized_final_state(_required(result, "state", "result"))
    return result


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "WaNormalizedScoreError",
    "certify_normalized_final_trace", "audit_wa_normalized_final_state",
    "checked_apply_wa_normalized_final_event",
)
