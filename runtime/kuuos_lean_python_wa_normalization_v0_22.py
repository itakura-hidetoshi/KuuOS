"""Selected native Wa weight-tolerance to exact-normalized rational comparison.

The original Wa kernel accepts a Python float sum of the seven weights
within 1e-9. This module separately measures the exact sum of their
represented rational values and the CPython built-in sum discrepancy.
A normalized rational score is constructed for *comparison only*.

The bound is exactly the v0.22 Lean conditional mathematical implication:
observed-weighted error + observed native-acceptance tolerance + measured
weight-sum error. No IEEE-754/CPython operational semantics is proved.
No original kernel, weight, score, state, store, ledger, receipt or digest
is modified. No external source/host authority is created.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from runtime import kuuos_lean_python_wa_weighted_sum_certificate_v0_21 as prior
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime import kuuos_lean_python_wa_rational_shadow_v0_19 as v19
from runtime.kuuos_decision_os_wa_types_v0_3 import POSITIVE_DIMENSIONS

VERSION = "kuuos_lean_python_wa_normalization_v0_22"
SOURCE_MAIN = "9304e28e8f8391f49a7989f3f04a84ed56231ef6"
NATIVE_WEIGHT_TOLERANCE = 1e-9
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


class WaNormalizationError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, status: str = BLOCKED) -> None:
    raise WaNormalizationError(status, (issue,))


def _copy(value: Any, label: str, kind: type) -> Any:
    try:
        return prior._copy(value, label, kind)
    except prior.WaWeightedSumError as exc:
        raise WaNormalizationError(exc.status, tuple(label + ":" + x for x in exc.issues)) from exc


def _required(source: dict, key: str, label: str) -> Any:
    if key not in source:
        _fail(label + ":" + key + ":missing", NO_DATA)
    return source[key]


def _native_float(value: Any, label: str) -> float:
    try:
        return v20._unit(value, label)
    except v20.WaBinary64MidpointError as exc:
        raise WaNormalizationError(exc.status, tuple(label + ":" + x for x in exc.issues)) from exc


def _q_float(value: float) -> Fraction:
    return Fraction(*value.as_integer_ratio())


def _q_pair(value: Any, label: str) -> Fraction:
    try:
        return prior._ratio(value, label)
    except prior.WaWeightedSumError as exc:
        raise WaNormalizationError(exc.status, exc.issues) from exc


def _pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def certify_native_weight_tolerance(weights: Any) -> dict[str, Any]:
    """Read-only native seven-axis sum observation, without exact-sum fiction."""
    w = _copy(weights, "weights", dict)
    axes = tuple(POSITIVE_DIMENSIONS)
    if axes != tuple(v20.native._POSITIVE):
        _fail("weights:original_axis_order_mismatch")
    if len(w) != len(axes) or set(w) != set(axes):
        _fail("weights:exact_native_seven_axis_keys_required")
    floating = [_native_float(w[name], "weight:" + name) for name in axes]
    rational = [_q_float(value) for value in floating]
    exact_total = sum(rational, Fraction(0))
    native_sum = sum(floating)
    # The original validator uses the native Python float tolerance test.
    native_accepted = abs(native_sum - 1.0) <= NATIVE_WEIGHT_TOLERANCE
    if not native_accepted:
        _fail("weights:original_native_tolerance_failed")
    native_ratio = _q_float(native_sum)
    tolerance_ratio = _q_float(NATIVE_WEIGHT_TOLERANCE)
    observed_native_defect = abs(native_ratio - 1)
    # A conservative additional exact certificate; acceptance by the
    # original Python float comparison alone does not prove this inequality.
    if observed_native_defect > tolerance_ratio:
        _fail("weights:exact_native_tolerance_certificate_failed")
    if exact_total <= 0:
        _fail("weights:exact_rational_total_must_be_positive")
    builtin_sum_error = abs(native_ratio - exact_total)
    exact_defect = abs(exact_total - 1)
    defect_bound = tolerance_ratio + builtin_sum_error
    if exact_defect > defect_bound:
        _fail("weights:exact_defect_triangle_inequality_failed")
    normalized_weights = [weight / exact_total for weight in rational]
    if sum(normalized_weights, Fraction(0)) != 1:
        _fail("weights:normalized_rational_sum_not_one")
    if any(not 0 <= x <= 1 for x in normalized_weights):
        _fail("weights:normalized_rational_axis_outside_unit")
    return {
        "axes": list(axes),
        "native_floats_rational": [_pair(x) for x in rational],
        "native_builtin_weight_sum": _pair(native_ratio),
        "exact_rational_weight_total": _pair(exact_total),
        "native_float_tolerance": _pair(tolerance_ratio),
        "observed_native_sum_defect": _pair(observed_native_defect),
        "observed_builtin_sum_error": _pair(builtin_sum_error),
        "observed_exact_weight_defect": _pair(exact_defect),
        "exact_weight_defect_upper_bound": _pair(defect_bound),
        "normalized_rational_weights": [_pair(x) for x in normalized_weights],
        "sum_of_normalized_rational_weights_is_one": True,
        "exact_native_tolerance_observed": True,
        "native_sum_semantics_formally_proved": False,
        "native_weights_modified": False,
    }


def certify_normalized_profile(
    profile: Any,
    weights: Any,
    weighted_certificate: Any,
    weight_certificate: Any = None,
) -> dict[str, Any]:
    """Bridge one v0.21 measured native score to normalized *rational* Wa."""
    p = _copy(profile, "profile", dict)
    previous = _copy(weighted_certificate, "weighted_certificate", dict)
    wc = certify_native_weight_tolerance(weights) if weight_certificate is None else (
        _copy(weight_certificate, "weight_certificate", dict)
    )
    # A caller-provided precomputed certificate is never trusted on flags
    # or hashes; require byte-equivalent reconstructed typed evidence.
    computed = certify_native_weight_tolerance(weights)
    if wc != computed:
        _fail("weight_certificate:reconstructed_evidence_mismatch")
    endpoints = _copy(_required(previous, "endpoints", "weighted_certificate"),
                      "endpoints", list)
    if len(endpoints) != 2:
        _fail("weighted_certificate:two_endpoints_required")
    positive = _copy(_required(p, "positive_intervals", "profile"),
                     "positive", dict)
    wvals = [_q_pair(value, "weight") for value in computed["native_floats_rational"]]
    total = _q_pair(computed["exact_rational_weight_total"], "total")
    tol = _q_pair(computed["native_float_tolerance"], "tolerance")
    native_sum_error = _q_pair(computed["observed_builtin_sum_error"], "sum_error")
    exact_defect = _q_pair(computed["observed_exact_weight_defect"], "exact_defect")
    results: list[dict[str, Any]] = []
    for expected_bound, value in zip(("lower", "upper"), endpoints):
        item = _copy(value, "weighted:" + expected_bound, dict)
        if _required(item, "bound", expected_bound) != expected_bound:
            _fail("weighted:" + expected_bound + ":endpoint_order_changed")
        if _required(item, "bound_checked", expected_bound) is not True:
            _fail("weighted:" + expected_bound + ":original_bound_missing")
        samples: list[Fraction] = []
        for name in computed["axes"]:
            interval = _copy(_required(positive, name, "positive"),
                             "positive:" + name, dict)
            s = _native_float(_required(interval, expected_bound, name),
                              "positive:" + name + ":" + expected_bound)
            samples.append(_q_float(s))
        exact_weighted = sum((w * x for w, x in zip(wvals, samples)), Fraction(0))
        if _q_pair(_required(item, "exact_weighted", expected_bound),
                   expected_bound + ":exact_weighted") != exact_weighted:
            _fail("weighted:" + expected_bound + ":source_weighted_mismatch")
        observed = _q_pair(_required(item, "native_weighted", expected_bound),
                           expected_bound + ":native_weighted")
        weighted_error = _q_pair(
            _required(item, "composed_upper_bound", expected_bound),
            expected_bound + ":composed_upper_bound")
        if weighted_error < 0 or abs(observed - exact_weighted) > weighted_error:
            _fail("weighted:" + expected_bound + ":v021_weighted_bound_failed")
        normalized = exact_weighted / total
        if not (0 <= normalized <= 1):
            _fail("weighted:" + expected_bound + ":normalized_outside_unit")
        shift = abs(exact_weighted - normalized)
        if shift > exact_defect:
            _fail("weighted:" + expected_bound + ":normalization_shift_bound_failed")
        bound = weighted_error + (tol + native_sum_error)
        observed_error = abs(observed - normalized)
        if observed_error > bound:
            _fail("weighted:" + expected_bound + ":normalization_error_bound_failed")
        results.append({
            "endpoint": expected_bound,
            "exact_raw_weighted": _pair(exact_weighted),
            "native_observed_weighted": _pair(observed),
            "exact_normalized_weighted": _pair(normalized),
            "actual_normalization_shift": _pair(shift),
            "actual_native_vs_normalized_error": _pair(observed_error),
            "input_weighted_error_budget": _pair(weighted_error),
            "weight_tolerance_budget": _pair(tol),
            "observed_builtin_weight_sum_error": _pair(native_sum_error),
            "combined_error_bound": _pair(bound),
            "conditional_lean_inequality_checked": True,
        })
    if _q_pair(results[0]["exact_normalized_weighted"], "lower") > _q_pair(results[1]["exact_normalized_weighted"], "upper"):
        # Fractions are compared exactly, not lexicographically as pairs.
        _fail("weighted:normalization_interval_order_invalid")
    return {
        "option_id": _required(p, "option_id", "profile"),
        "endpoint_certificates": results,
        "exact_rational_normalized_interval_only": True,
        "python_builtin_sum_semantics_proved": False,
        "python_lean_full_refinement_proved": False,
        "authority_granted": False,
    }


def audit_wa_normalization_state(state: Any) -> dict[str, Any]:
    """Original native v0.21 checks, then exact-rational normalization witness."""
    try:
        predecessor = prior.audit_wa_weighted_state(state)
    except prior.WaWeightedSumError as exc:
        raise WaNormalizationError(exc.status, tuple("v021:" + x for x in exc.issues)) from exc
    s = _copy(state, "state", dict)
    result = {
        "version": VERSION,
        "source_main": SOURCE_MAIN,
        "state_digest": prior.prior._fingerprint(s),
        "weight_tolerance": None,
        "certificates": [],
        "all_input_observations_certified": False,
        "ieee754_global_semantics_proved": False,
        "python_lean_full_refinement_proved": False,
        "original_weights_normalized_or_modified": False,
        "external_issuer_authenticated": False,
        "authority_granted": False,
    }
    phase = _required(s, "current_phase", "state")
    if v20.native._PHASES.index(phase) < v20.native._PHASES.index("evaluate"):
        return result
    profiles = _copy(_required(s, "profiles", "state"), "profiles", list)
    weights = _copy(_required(s, "weights", "state"), "weights", dict)
    if len(profiles) != len(predecessor["certificates"]):
        _fail("state:profile_certificate_count_mismatch")
    wc = certify_native_weight_tolerance(weights)
    result["weight_tolerance"] = wc
    for p, c in zip(profiles, predecessor["certificates"]):
        checked = certify_normalized_profile(p, weights, c, wc)
        if checked["option_id"] != c.get("option_id"):
            _fail("state:original_option_identity_mismatch")
        result["certificates"].append(checked)
    result["all_input_observations_certified"] = True
    return result


def checked_apply_wa_normalization_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """One original v0.21 adapter, pure read-only pre/post checks."""
    values = [_copy(v, label, dict) for v, label in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief"),
    )]
    audit_wa_normalization_state(values[0])
    digest = prior.prior._fingerprint(values)
    try:
        outcome = prior.checked_apply_wa_weighted_event(*values)
    except prior.WaWeightedSumError as exc:
        raise WaNormalizationError(exc.status, tuple("v021:" + x for x in exc.issues)) from exc
    except Exception as exc:
        _fail("prior_adapter_exception:" + type(exc).__name__)
    if prior.prior._fingerprint(values) != digest:
        _fail("prior_adapter_mutated_arguments")
    result = _copy(outcome, "result", dict)
    audit_wa_normalization_state(_required(result, "state", "result"))
    return result


__all__ = (
    "VERSION", "SOURCE_MAIN", "NATIVE_WEIGHT_TOLERANCE", "BLOCKED", "NO_DATA",
    "WaNormalizationError", "certify_native_weight_tolerance",
    "certify_normalized_profile", "audit_wa_normalization_state",
    "checked_apply_wa_normalization_event",
)
