"""Exact finite rational propagation for selected native seven-axis Wa weighted sums.

A v0.21 observation composes the individually checked v0.20 multiplication
midpoint certificates with the independently measured error of Python's
built-in sum() relative to the exact sum of *observed rounded products*.

This is a read-only, local certificate of finite observations. It does not
specify CPython's sum algorithm, prove arbitrary IEEE 754 operations, or
grant external provenance or action authority. The original Wa OS kernel,
store, ledger, receipts and input state remain untouched.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as prior
from runtime import kuuos_lean_python_wa_rational_shadow_v0_19 as rational

VERSION = "kuuos_lean_python_wa_weighted_sum_certificate_v0_21"
SOURCE_MAIN = "3cad1cb96210ce88e9b7f1921c8dc7b9df198350"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


class WaWeightedSumError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(reason: str, status: str = BLOCKED) -> None:
    raise WaWeightedSumError(status, (reason,))


def _copy(value: Any, label: str, kind: type) -> Any:
    try:
        return prior._copy(value, label, kind)
    except prior.WaBinary64MidpointError as exc:
        raise WaWeightedSumError(exc.status, exc.issues) from exc


def _ratio(value: Any, label: str) -> Fraction:
    if type(value) is not list or len(value) != 2:
        _fail(label + ":rational_pair_required")
    num, den = value
    if type(num) is not int or type(den) is not int or den <= 0:
        _fail(label + ":canonical_rational_types_required")
    fraction = Fraction(num, den)
    if [fraction.numerator, fraction.denominator] != value:
        _fail(label + ":noncanonical_rational_pair")
    return fraction


def _pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def _require(mapping: dict, key: str, label: str) -> Any:
    if key not in mapping:
        _fail(label + ":" + key + ":missing", NO_DATA)
    return mapping[key]


def _certify_product(record: dict, label: str) -> dict[str, Any]:
    if _require(record, "operator", label) != "mul":
        _fail(label + ":product_operator_required")
    if _require(record, "label", label) != label:
        _fail(label + ":product_label_mismatch")
    if _require(record, "exact_midpoint_certificate_checked", label) is not True:
        _fail(label + ":midpoint_flag_missing")
    left = _ratio(_require(record, "left", label), label + ":left")
    right = _ratio(_require(record, "right", label), label + ":right")
    rounded = _ratio(_require(record, "observed", label), label + ":observed")
    previous = _ratio(_require(record, "previous", label), label + ":previous")
    following = _ratio(_require(record, "next", label), label + ":next")
    quantum = _ratio(_require(record, "maximum_neighbor_gap", label), label + ":quantum")
    exact = left * right
    if _ratio(_require(record, "exact", label), label + ":exact") != exact:
        _fail(label + ":product_ideal_mismatch")
    if not (previous < rounded < following):
        _fail(label + ":strict_neighbor_order_required")
    if quantum != max(rounded - previous, following - rounded):
        _fail(label + ":neighbor_gap_mismatch")
    if not ((previous + rounded) / 2 <= exact <= (rounded + following) / 2):
        _fail(label + ":midpoint_inequality_invalid")
    error = rounded - exact
    if _ratio(_require(record, "absolute_error", label), label + ":error") != abs(error):
        _fail(label + ":signed_product_error_mismatch")
    if abs(error) > quantum / 2:
        _fail(label + ":local_half_quantum_bound_failed")
    return {
        "label": label,
        "exact_product": _pair(exact),
        "rounded_product": _pair(rounded),
        "signed_error": _pair(error),
        "half_quantum": _pair(quantum / 2),
    }


def certify_weighted_trace(trace: Any) -> dict[str, Any]:
    """Finite signed-error list and original built-in sum, exact ℚ arithmetic.

    The trace comes from the existing v0.20 independent native-Wa replay.
    This second checker validates all rational relations itself. Passing an
    arbitrary caller-declared trace alone is not proof of native provenance.
    """
    t = _copy(trace, "trace", dict)
    steps = _copy(_require(t, "steps", "trace"), "steps", list)
    summaries = _copy(_require(t, "builtin_summations", "trace"), "sums", list)
    fields = _copy(_require(t, "fields", "trace"), "fields", dict)
    if len(summaries) != 2:
        _fail("trace:two_native_summations_required")
    if len(steps) != 27:
        _fail("trace:original_27_rounding_steps_required")
    names = prior.native._POSITIVE
    outcomes: list[dict[str, Any]] = []
    for bound, summary in zip(("lower", "upper"), summaries):
        row = _copy(summary, "sum:" + bound, dict)
        if _require(row, "bound", bound) != bound or _require(row, "terms", bound) != 7:
            _fail("sum:" + bound + ":seven_terms_or_bound_mismatch")
        if _require(row, "builtin_sum_semantics_proved", bound) is not False:
            _fail("sum:" + bound + ":unproved_semantics_flag_required")
        records = []
        for axis in names:
            label = bound + ":weight:" + axis
            matching = [x for x in steps if
                        type(x) is dict and x.get("label") == label]
            if len(matching) != 1:
                _fail(label + ":exactly_one_source_step_required")
            records.append(_certify_product(matching[0], label))
        observed_products = [_ratio(p["rounded_product"], "rounded")
                             for p in records]
        exact_products = [_ratio(p["exact_product"], "exact")
                          for p in records]
        signed_errors = [_ratio(p["signed_error"], "signed")
                         for p in records]
        half_quantums = [_ratio(p["half_quantum"], "quantum")
                         for p in records]
        rounded_sum = sum(observed_products, Fraction(0))
        exact_sum = sum(exact_products, Fraction(0))
        summed_errors = sum(signed_errors, Fraction(0))
        observed_sum = _ratio(_require(row, "observed_sum", bound), bound + ":observed")
        if _ratio(_require(row, "exact_sum", bound), bound + ":sum") != rounded_sum:
            _fail("sum:" + bound + ":rounded_product_sum_mismatch")
        if _ratio(_require(row, "absolute_error", bound), bound + ":error") != abs(
                observed_sum - rounded_sum):
            _fail("sum:" + bound + ":builtin_sum_error_mismatch")
        if observed_sum != prior._fraction(
                _require(fields, "weighted_interval." + bound, "fields"),
                bound + ":original_weighted"):
            _fail("sum:" + bound + ":original_native_weighted_mismatch")
        if rounded_sum - exact_sum != summed_errors:
            _fail("sum:" + bound + ":signed_error_sum_identity_failed")
        half_quantum_budget = sum(half_quantums, Fraction(0))
        total_abs_product_error = sum(map(abs, signed_errors), Fraction(0))
        builtin_sum_error = abs(observed_sum - rounded_sum)
        weighted_error = abs(observed_sum - exact_sum)
        final_budget = half_quantum_budget + builtin_sum_error
        if total_abs_product_error > half_quantum_budget:
            _fail("sum:" + bound + ":total_local_quantum_budget_failed")
        if weighted_error > final_budget:
            _fail("sum:" + bound + ":composed_weighted_error_budget_failed")
        outcomes.append({
            "bound": bound,
            "products": records,
            "product_count": len(records),
            "exact_weighted": _pair(exact_sum),
            "rounded_product_sum": _pair(rounded_sum),
            "native_weighted": _pair(observed_sum),
            "signed_product_error_sum": _pair(summed_errors),
            "sum_absolute_product_errors": _pair(total_abs_product_error),
            "half_quantum_budget": _pair(half_quantum_budget),
            "observed_builtin_sum_error": _pair(builtin_sum_error),
            "observed_weighted_error": _pair(weighted_error),
            "composed_upper_bound": _pair(final_budget),
            "bound_checked": True,
            "builtin_sum_semantics_proved": False,
        })
    return {
        "version": VERSION,
        "endpoints": outcomes,
        "certified_endpoint_count": 2,
        "rational_finite_sum_inequalities_checked": True,
        "builtin_sum_semantics_proved": False,
        "ieee754_global_semantics_proved": False,
        "lean_python_full_refinement_proved": False,
        "external_issuer_authenticated": False,
        "action_authority_granted": False,
    }


def audit_wa_weighted_state(state: Any) -> dict[str, Any]:
    """Rerun v0.20 native-store audit; additionally certify 7-axis sums."""
    try:
        original = prior.audit_wa_binary64_state(state)
    except prior.WaBinary64MidpointError as exc:
        raise WaWeightedSumError(exc.status, ("prior:" + ";".join(exc.issues),)) from exc
    s = _copy(state, "state", dict)
    result = {
        "version": VERSION, "source_main": SOURCE_MAIN,
        "state_digest": prior._fingerprint(s),
        "wa_v020_record_count": len(original["local_step_certificates"]),
        "certificates": [],
        "python_builtin_sum_semantics_proved": False,
        "ieee754_global_semantics_proved": False,
        "full_refinement_proved": False,
        "external_issuer_authenticated": False,
        "action_authority_granted": False,
    }
    phase = _require(s, "current_phase", "state")
    if prior.native._PHASES.index(phase) < prior.native._PHASES.index("evaluate"):
        return result
    profiles = _copy(_require(s, "profiles", "state"), "profiles", list)
    weights = _copy(_require(s, "weights", "state"), "weights", dict)
    thresholds = _copy(_require(s, "thresholds", "state"), "thresholds", dict)
    beta = _require(thresholds, "bottleneck_weight", "thresholds")
    for profile in profiles:
        p = _copy(profile, "profile", dict)
        trace = prior.trace_native_wa_score(p, weights, beta)
        cert = certify_weighted_trace(trace)
        ideals = rational.rational_ideal_record(p, weights, beta)
        for endpoint in cert["endpoints"]:
            name = "weighted_interval." + endpoint["bound"]
            if _ratio(endpoint["exact_weighted"], name) != ideals[name]:
                _fail("state:" + name + ":v019_exact_rational_shadow_mismatch")
        cert["option_id"] = _require(p, "option_id", "profile")
        result["certificates"].append(cert)
    if len(result["certificates"]) != len(original["local_step_certificates"]):
        _fail("state:v020_record_count_mismatch")
    return result


def checked_apply_wa_weighted_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """One original v0.20 native adapter, read-only pre/post certificate."""
    args = [_copy(v, label, dict) for v, label in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief"),
    )]
    audit_wa_weighted_state(args[0])
    digest = prior._fingerprint(args)
    try:
        observed = prior.checked_apply_wa_binary64_event(*args)
    except prior.WaBinary64MidpointError as exc:
        raise WaWeightedSumError(exc.status, ("prior:" + ";".join(exc.issues),)) from exc
    except Exception as exc:
        _fail("prior_adapter_exception:" + type(exc).__name__)
    if prior._fingerprint(args) != digest:
        _fail("prior_adapter_mutated_arguments")
    output = _copy(observed, "output", dict)
    audit_wa_weighted_state(_require(output, "state", "output"))
    return output


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "WaWeightedSumError",
    "certify_weighted_trace", "audit_wa_weighted_state",
    "checked_apply_wa_weighted_event",
)
