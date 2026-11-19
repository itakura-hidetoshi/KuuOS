"""Native Wa finite-extrema reference stability, exact rational v0.26.

This additive auditor reuses the original v0.19-v0.25 source-linked
observations. An explicitly identified counterfactual reference is
taken from the *opposite endpoint of the same original option*.
The original score is NOT recomputed, rewritten, or used as proof of
an actual native counterfactual execution.

Local observed errors and finite rational algebra establish a
conditional score bound. There is no universal CPython min/max/sum
semantics, IEEE 754 interpreter proof, external issuer authenticity,
full Lean-to-Python refinement or host authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from runtime import kuuos_lean_python_wa_finite_extrema_v0_25 as previous
from runtime import kuuos_lean_python_wa_normalized_score_v0_23 as v23
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint

VERSION = "kuuos_lean_python_wa_extrema_stability_v0_26"
SOURCE_MAIN = "9dc7e05a8deb2852698abdaa260ce143f45f8c35"
BLOCKED, NO_DATA = "BLOCKED", "NO_DATA"


class WaExtremaStabilityError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(message: str, status: str = BLOCKED) -> None:
    raise WaExtremaStabilityError(status, (message,))


def _copy(value: Any, label: str, kind: type) -> Any:
    try:
        return previous._copy(value, label, kind)
    except previous.WaFiniteExtremaError as exc:
        raise WaExtremaStabilityError(exc.status, exc.issues) from exc


def _need(data: dict, key: str, label: str) -> Any:
    if key not in data:
        _fail(label + ":" + key + ":missing", NO_DATA)
    return data[key]


def _q(value: Any, label: str) -> Fraction:
    try:
        return previous._q(value, label)
    except previous.WaFiniteExtremaError as exc:
        raise WaExtremaStabilityError(exc.status, exc.issues) from exc


def _f(value: Any, label: str) -> Fraction:
    try:
        return previous._f(value, label)
    except previous.WaFiniteExtremaError as exc:
        raise WaExtremaStabilityError(exc.status, exc.issues) from exc


def _pair(v: Fraction) -> list[int]:
    return [v.numerator, v.denominator]


def certify_exact_extrema_score_reference(
    beta: Any, observed_weighted: Any, normalized_weighted: Any,
    observed_weakest: Any, reference_weakest: Any,
    observed_alert: Any, reference_alert: Any, observed_score: Any,
    wa_error_budget: Any, normalized_weight_budget: Any,
    weakest_error_budget: Any, alert_error_budget: Any,
) -> dict[str, Any]:
    """Check a finite rational conditional witness, not an issuer signature.

    Values are canonical [numerator, denominator] pairs, including the
    reference values. An arbitrary caller cannot establish source identity
    by obtaining a successful pure mathematical certificate.
    """
    vals = {
        "beta": beta,
        "observed_weighted": observed_weighted,
        "normalized_weighted": normalized_weighted,
        "observed_weakest": observed_weakest,
        "reference_weakest": reference_weakest,
        "observed_alert": observed_alert,
        "reference_alert": reference_alert,
        "observed_score": observed_score,
        "wa_error_budget": wa_error_budget,
        "normalized_weight_budget": normalized_weight_budget,
        "weakest_error_budget": weakest_error_budget,
        "alert_error_budget": alert_error_budget,
    }
    q = {k: _q(v, k) for k, v in vals.items()}
    for key in ("beta", "normalized_weighted", "reference_weakest",
                "observed_alert", "reference_alert"):
        if not 0 <= q[key] <= 1:
            _fail(key + ":unit_interval_required")
    for key in ("wa_error_budget", "normalized_weight_budget",
                "weakest_error_budget", "alert_error_budget"):
        if q[key] < 0:
            _fail(key + ":nonnegative_budget_required")

    raw_ideal = v23._rational_ideal(
        q["beta"], q["observed_weighted"],
        q["observed_weakest"], q["observed_alert"])
    original_normalized_ideal = v23._rational_ideal(
        q["beta"], q["normalized_weighted"],
        q["observed_weakest"], q["observed_alert"])
    reference_ideal = v23._rational_ideal(
        q["beta"], q["normalized_weighted"],
        q["reference_weakest"], q["reference_alert"])
    measured_wa_error = abs(q["observed_score"] - raw_ideal)
    measured_weight_error = abs(q["observed_weighted"] - q["normalized_weighted"])
    measured_weak_error = abs(q["observed_weakest"] - q["reference_weakest"])
    measured_alert_error = abs(q["observed_alert"] - q["reference_alert"])
    if measured_wa_error > q["wa_error_budget"]:
        _fail("score:original_wa_error_exceeds_certificate")
    if measured_weight_error > q["normalized_weight_budget"]:
        _fail("weighted:normalized_error_exceeds_certificate")
    if measured_weak_error > q["weakest_error_budget"]:
        _fail("weakest:reference_error_exceeds_certificate")
    if measured_alert_error > q["alert_error_budget"]:
        _fail("alert:reference_error_exceeds_certificate")

    normalized_shift = abs(raw_ideal - original_normalized_ideal)
    weakest_shift = abs(
        original_normalized_ideal -
        v23._rational_ideal(q["beta"], q["normalized_weighted"],
                           q["reference_weakest"], q["observed_alert"]))
    alert_shift = abs(
        v23._rational_ideal(q["beta"], q["normalized_weighted"],
                           q["reference_weakest"], q["observed_alert"]) -
        reference_ideal)
    if normalized_shift > measured_weight_error:
        _fail("weighted:ideal_nonexpansivity_failed")
    if weakest_shift > measured_weak_error:
        _fail("weakest:ideal_nonexpansivity_failed")
    if alert_shift > measured_alert_error:
        _fail("alert:ideal_nonexpansivity_failed")

    final_error = abs(q["observed_score"] - reference_ideal)
    bound = (q["wa_error_budget"] + q["normalized_weight_budget"] +
             q["weakest_error_budget"] + q["alert_error_budget"])
    if final_error > bound:
        _fail("score:reference_error_composition_failed")
    return {
        "original_raw_ideal": _pair(raw_ideal),
        "normalized_original_extrema_ideal": _pair(original_normalized_ideal),
        "normalized_reference_extrema_ideal": _pair(reference_ideal),
        "observed_native_score": _pair(q["observed_score"]),
        "measured_wa_error": _pair(measured_wa_error),
        "measured_weight_error": _pair(measured_weight_error),
        "measured_weakest_error": _pair(measured_weak_error),
        "measured_alert_error": _pair(measured_alert_error),
        "normalized_ideal_shift": _pair(normalized_shift),
        "weakest_ideal_shift": _pair(weakest_shift),
        "alert_ideal_shift": _pair(alert_shift),
        "observed_reference_score_error": _pair(final_error),
        "conditional_composed_upper_bound": _pair(bound),
        "conditional_rational_inequality_checked": True,
        "counterfactual_reference_only": True,
        "external_reference_authenticated": False,
        "python_min_max_sum_semantics_proved": False,
        "host_authority_granted": False,
    }


def certify_original_wa_extrema_stability_trace(
    profile: Any, weights: Any, beta: Any,
) -> dict[str, Any]:
    """Use only the opposite *actual source endpoint* as comparison input."""
    p, w = _copy(profile, "profile", dict), _copy(weights, "weights", dict)
    try:
        extrema = previous.certify_original_wa_extrema_trace(p, w, beta)
        score = v23.certify_normalized_final_trace(p, w, beta)
    except previous.WaFiniteExtremaError as exc:
        raise WaExtremaStabilityError(
            exc.status, ("v025:" + ";".join(exc.issues),)) from exc
    except v23.WaNormalizedScoreError as exc:
        raise WaExtremaStabilityError(
            exc.status, ("v023:" + ";".join(exc.issues),)) from exc
    ext = _copy(_need(extrema, "endpoint_certificates", "extrema"),
                "extrema_endpoints", list)
    raw = _copy(_need(score, "endpoints", "score"), "score_endpoints", list)
    if len(ext) != 2 or len(raw) != 2:
        _fail("source:two_original_endpoints_required")
    if extrema.get("option_id") != score.get("option_id"):
        _fail("source:original_option_identity_mismatch")
    b = _f(beta, "beta")
    output = []
    for i, bound in enumerate(("lower", "upper")):
        this = _copy(ext[i], "source:" + bound, dict)
        opposite = _copy(ext[1 - i], "source:opposite:" + bound, dict)
        original = _copy(raw[i], "source:score:" + bound, dict)
        if (this.get("endpoint") != bound or
                opposite.get("endpoint") != ("upper" if i == 0 else "lower") or
                original.get("endpoint") != bound):
            _fail("source:original_endpoint_order_mismatch")
        if this.get("normalized_ideal_score") != original.get("normalized_ideal_score"):
            _fail("source:normalized_ideal_identity_failed")
        this_weak = _q(_need(this, "observed_weakest_positive", bound), "weakest")
        other_weak = _q(_need(opposite, "observed_weakest_positive", "reference"),
                        "reference_weakest")
        this_alert = _q(_need(this, "observed_strongest_alert", bound), "alert")
        other_alert = _q(_need(opposite, "observed_strongest_alert", "reference"),
                         "reference_alert")
        comparison = certify_exact_extrema_score_reference(
            _pair(b),
            _need(original, "observed_native_weighted", bound),
            _need(original, "exact_normalized_weighted", bound),
            _pair(this_weak), _pair(other_weak),
            _pair(this_alert), _pair(other_alert),
            _need(original, "observed_native_wa_score", bound),
            _need(original, "measured_raw_wa_error", bound),
            _need(original, "normalized_weighted_budget", bound),
            _pair(abs(this_weak - other_weak)),
            _pair(abs(this_alert - other_alert)),
        )
        if comparison["original_raw_ideal"] != original["original_raw_ideal_score"]:
            _fail("source:original_raw_ideal_identity_failed")
        if (comparison["normalized_original_extrema_ideal"] !=
                original["normalized_ideal_score"]):
            _fail("source:source_normalized_score_identity_failed")
        output.append({
            "endpoint": bound,
            "reference_endpoint": opposite["endpoint"],
            "source_positive_axis_order": this["positive_axis_names"],
            "source_alert_axis_order": this["alert_axis_names"],
            "observed_weakest_positive": _pair(this_weak),
            "reference_weakest_positive": _pair(other_weak),
            "observed_strongest_alert": _pair(this_alert),
            "reference_strongest_alert": _pair(other_alert),
            "comparison": comparison,
            "reference_comes_from_same_source_option": True,
            "reference_is_counterfactual_not_native_score": True,
            "python_generic_order_statistics_proved": False,
        })
    return {
        "version": VERSION,
        "option_id": extrema["option_id"],
        "endpoints": output,
        "original_state_modified": False,
        "global_python_lean_refinement_proved": False,
        "external_issuer_authenticated": False,
        "host_authority_granted": False,
    }


def audit_wa_extrema_stability_state(state: Any) -> dict[str, Any]:
    """Run the v0.25 source/state audit before the new comparison witness."""
    try:
        old = previous.audit_wa_finite_extrema_state(state)
    except previous.WaFiniteExtremaError as exc:
        raise WaExtremaStabilityError(
            exc.status, ("v025:" + ";".join(exc.issues),)) from exc
    s = _copy(state, "state", dict)
    result = {
        "version": VERSION,
        "source_main": SOURCE_MAIN,
        "state_digest": _fingerprint(s),
        "certificates": [],
        "all_conditional_extrema_reference_checks_passed": False,
        "original_state_modified": False,
        "global_python_lean_refinement_proved": False,
        "python_min_max_sum_semantics_proved": False,
        "external_issuer_authenticated": False,
        "host_authority_granted": False,
    }
    phase = _need(s, "current_phase", "state")
    if v20.native._PHASES.index(phase) < v20.native._PHASES.index("evaluate"):
        return result
    profiles = _copy(_need(s, "profiles", "state"), "profiles", list)
    weights = _copy(_need(s, "weights", "state"), "weights", dict)
    thresholds = _copy(_need(s, "thresholds", "state"), "thresholds", dict)
    beta = _need(thresholds, "bottleneck_weight", "thresholds")
    old_certs = _copy(_need(old, "certificates", "old"), "old_certificates", list)
    if len(profiles) != len(old_certs):
        _fail("source:prior_certificates_count_mismatch")
    for p, old_cert in zip(profiles, old_certs):
        cert = certify_original_wa_extrema_stability_trace(p, weights, beta)
        if cert["option_id"] != old_cert.get("option_id"):
            _fail("source:prior_option_identity_mismatch")
        result["certificates"].append(cert)
    result["all_conditional_extrema_reference_checks_passed"] = True
    return result


def checked_apply_wa_extrema_stability_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """At most one unchanged native event path, no new host effect."""
    args = [_copy(v, label, dict) for v, label in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief")
    )]
    audit_wa_extrema_stability_state(args[0])
    old = _fingerprint(args)
    try:
        value = previous.checked_apply_wa_finite_extrema_event(*args)
    except previous.WaFiniteExtremaError as exc:
        raise WaExtremaStabilityError(
            exc.status, ("v025:" + ";".join(exc.issues),)) from exc
    except Exception as exc:
        _fail("prior_adapter_exception:" + type(exc).__name__)
    if _fingerprint(args) != old:
        _fail("native_adapter_mutated_caller_arguments")
    result = _copy(value, "result", dict)
    audit_wa_extrema_stability_state(_need(result, "state", "result"))
    return result


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "WaExtremaStabilityError",
    "certify_exact_extrema_score_reference",
    "certify_original_wa_extrema_stability_trace",
    "audit_wa_extrema_stability_state",
    "checked_apply_wa_extrema_stability_event",
)
