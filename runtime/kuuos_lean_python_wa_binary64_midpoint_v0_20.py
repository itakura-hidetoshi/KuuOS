"""Finite Python binary64 step observations and exact-rational Wa midpoint checks.

The nearest-neighbor check is performed on *observed* native Python results.
It supplies conditional midpoint inequalities that match the Lean v0.20
neighbor theorem. It does not prove CPython / IEEE-754 semantics, arbitrary
native execution, faithful hardware operation ordering or external authority.

No existing native kernel, store, ledger, score, receipt or digest is mutated.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
import math
from typing import Any

from runtime import kuuos_lean_python_wa_rational_shadow_v0_19 as prior
from runtime import kuuos_lean_python_wa_evaluation_guard_v0_15 as native
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint

VERSION = "kuuos_lean_python_wa_binary64_midpoint_v0_20"
SOURCE_MAIN = "73bba9d114c8f4fcdfe636ba46360f9e18b9977e"
BLOCKED, NO_DATA = "BLOCKED", "NO_DATA"


class WaBinary64MidpointError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, status: str = BLOCKED) -> None:
    raise WaBinary64MidpointError(status, (issue,))


def _copy(value: Any, label: str, kind: type) -> Any:
    try:
        return prior._copy(value, label, kind)
    except prior.WaRationalShadowError as exc:
        raise WaBinary64MidpointError(exc.status, tuple(label + ":" + i for i in exc.issues)) from exc


def _need(mapping: dict, key: str, label: str) -> Any:
    if key not in mapping:
        _fail(label + ":" + key + ":missing", NO_DATA)
    return mapping[key]


def _unit(value: Any, label: str) -> float:
    try:
        return native._number(value, label)
    except native.WaEvaluationBoundaryError as exc:
        raise WaBinary64MidpointError(
            exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED,
            tuple(label + ":" + i for i in exc.issues),
        ) from exc


def _fraction(value: Any, label: str) -> Fraction:
    if type(value) is not float or not math.isfinite(value):
        _fail(label + ":finite_native_float_required")
    return Fraction(*value.as_integer_ratio())


def _pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def observed_binary64_operation(
    left: float, right: float, operator: str, label: str = "operation",
) -> tuple[float, dict[str, Any]]:
    """Check the *observed* operation against exact-rational neighbor midpoints.

    Not a proof of an interpreter or of all IEEE-754 executions. Both
    neighbors must be finite and strictly ordered (fail closed at extremes).
    """
    a, b = _fraction(left, label + ":left"), _fraction(right, label + ":right")
    if operator == "add":
        observed, ideal = left + right, a + b
    elif operator == "sub":
        observed, ideal = left - right, a - b
    elif operator == "mul":
        observed, ideal = left * right, a * b
    else:
        _fail(label + ":unknown_operation")
    z = _fraction(observed, label + ":result")
    below = math.nextafter(observed, -math.inf)
    above = math.nextafter(observed, math.inf)
    lower = _fraction(below, label + ":previous")
    upper = _fraction(above, label + ":next")
    if not (lower < z < upper):
        _fail(label + ":strict_finite_neighbors_required")
    quantum = max(z - lower, upper - z)
    if not ((lower + z) / 2 <= ideal <= (z + upper) / 2):
        _fail(label + ":exact_midpoint_certificate_failed")
    error = abs(z - ideal)
    if error > quantum / 2:
        _fail(label + ":half_quantum_bound_failed")
    return observed, {
        "label": label,
        "operator": operator,
        "left": _pair(a),
        "right": _pair(b),
        "observed": _pair(z),
        "exact": _pair(ideal),
        "previous": _pair(lower),
        "next": _pair(upper),
        "maximum_neighbor_gap": _pair(quantum),
        "absolute_error": _pair(error),
        "exact_midpoint_certificate_checked": True,
    }


def trace_native_wa_score(
    profile: Any, weights: Any, beta: Any,
) -> dict[str, Any]:
    """Trace the original v0.3 score arithmetic without writing any stores."""
    p, w = _copy(profile, "profile", dict), _copy(weights, "weights", dict)
    b = _unit(beta, "beta")
    positive = _copy(_need(p, "positive_intervals", "profile"), "positive", dict)
    alerts = _copy(_need(p, "alert_intervals", "profile"), "alerts", dict)
    steps: list[dict[str, Any]] = []
    builtin_summations: list[dict[str, Any]] = []

    def value(source: dict, name: str, bound: str, label: str) -> float:
        item = _copy(_need(source, name, label), label + ":" + name, dict)
        return _unit(_need(item, bound, label + ":" + name), label + ":" + name + ":" + bound)

    def execute(a: float, c: float, op: str, label: str) -> float:
        result, certificate = observed_binary64_operation(a, c, op, label)
        steps.append(certificate)
        return result

    terms: dict[str, float] = {}
    for bound in ("lower", "upper"):
        samples = [value(positive, axis, bound, "positive") for axis in native._POSITIVE]
        products: list[float] = []
        for axis, sample in zip(native._POSITIVE, samples):
            weight = _unit(_need(w, axis, "weights"), "weights:" + axis)
            products.append(execute(weight, sample, "mul", bound + ":weight:" + axis))
        # Preserve CPython's original built-in sum(), which may use a
        # compensated float algorithm instead of seven naive additions.
        # The true algorithm is NOT formalized here: retain its exact
        # observed rational discrepancy as a separate obstruction.
        weighted = sum(products)
        expected_sum = sum((_fraction(term, bound + ":sum_term")
                            for term in products), Fraction(0))
        observed_sum = _fraction(weighted, bound + ":native_builtin_sum")
        builtin_summations.append({
            "bound": bound,
            "terms": len(products),
            "exact_sum": _pair(expected_sum),
            "observed_sum": _pair(observed_sum),
            "absolute_error": _pair(abs(observed_sum - expected_sum)),
            "builtin_sum_semantics_proved": False,
        })
        weakest = min(samples)
        left_weight = execute(1.0, b, "sub", bound + ":one_minus_beta")
        left = execute(left_weight, weighted, "mul", bound + ":weighted_mix")
        right = execute(b, weakest, "mul", bound + ":weakest_mix")
        relational = execute(left, right, "add", bound + ":relational")
        alert_samples = [value(alerts, axis, bound, "alerts") for axis in native._ALERT]
        terms["weighted_interval." + bound] = weighted
        terms["weakest_interval." + bound] = weakest
        terms["relational_interval." + bound] = relational
        terms["alert_interval." + bound] = max(alert_samples)

    lower_factor = execute(1.0, terms["alert_interval.upper"], "sub", "wa:lower_factor")
    upper_factor = execute(1.0, terms["alert_interval.lower"], "sub", "wa:upper_factor")
    low = execute(terms["relational_interval.lower"], lower_factor, "mul", "wa:lower")
    high = execute(terms["relational_interval.upper"], upper_factor, "mul", "wa:upper")
    if not (0.0 <= low <= high <= 1.0 + 1e-12):
        _fail("wa:original_native_score_range_failed")
    high_clipped = min(1.0, high)
    width = execute(high_clipped, low, "sub", "wa:width")
    terms["wa_interval.lower"] = low
    terms["wa_interval.upper"] = high_clipped
    terms["wa_interval.width"] = width
    return {"fields": terms, "steps": steps,
            "builtin_summations": builtin_summations}


def audit_wa_binary64_state(state: Any) -> dict[str, Any]:
    """Read-only operational witness on selected committed Wa score records."""
    try:
        earlier = prior.audit_wa_rational_state(state)
    except prior.WaRationalShadowError as exc:
        raise WaBinary64MidpointError(
            exc.status, tuple("v019:" + issue for issue in exc.issues),
        ) from exc
    s = _copy(state, "state", dict)
    result: dict[str, Any] = {
        "version": VERSION,
        "source_main": SOURCE_MAIN,
        "state_digest": _fingerprint(s),
        "v019_certificates": len(earlier["certificates"]),
        "local_step_certificates": [],
        "all_local_midpoints_checked": True,
        "builtin_sum_semantics_proved": False,
        "ieee754_global_semantics_proved": False,
        "python_lean_full_refinement_proved": False,
        "external_issuer_authenticated": False,
        "history_complete_proved": False,
        "host_authority_granted": False,
    }
    phase = _need(s, "current_phase", "state")
    if native._PHASES.index(phase) < native._PHASES.index("evaluate"):
        return result
    profiles = _copy(_need(s, "profiles", "state"), "profiles", list)
    records = _copy(_need(s, "wa_records", "state"), "records", list)
    weights = _copy(_need(s, "weights", "state"), "weights", dict)
    thresholds = _copy(_need(s, "thresholds", "state"), "thresholds", dict)
    beta = _need(thresholds, "bottleneck_weight", "thresholds")
    for index, (profile, record) in enumerate(zip(profiles, records)):
        label = "wa_record[" + str(index) + "]"
        p, r = _copy(profile, label + ":profile", dict), _copy(record, label, dict)
        if _need(p, "option_id", label) != _need(r, "option_id", label):
            _fail(label + ":option_id_mismatch")
        trace = trace_native_wa_score(p, weights, beta)
        for field, calculated in trace["fields"].items():
            group, key = field.split(".", 1)
            stored_group = _copy(_need(r, group, label), label + ":" + group, dict)
            stored = _fraction(_need(stored_group, key, label + ":" + group), label + ":" + field)
            if stored != _fraction(calculated, label + ":" + field + ":trace"):
                _fail(label + ":" + field + ":native_float_trace_mismatch")
        result["local_step_certificates"].append({
            "option_id": _need(p, "option_id", label),
            "stored_scores_exact": True,
            "score_field_count": len(trace["fields"]),
            "step_count": len(trace["steps"]),
            "step_certificates": trace["steps"],
            "builtin_summations": trace["builtin_summations"],
        })
    return result


def checked_apply_wa_binary64_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """Exactly one original v0.19 adapter and read-only pre/post checks."""
    args = [_copy(v, name, dict) for v, name in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief"),
    )]
    audit_wa_binary64_state(args[0])
    before = _fingerprint(args)
    try:
        outcome = prior.checked_apply_wa_rational_event(*args)
    except prior.WaRationalShadowError as exc:
        raise WaBinary64MidpointError(
            exc.status, tuple("prior:" + issue for issue in exc.issues),
        ) from exc
    except Exception as exc:
        _fail("prior_adapter_exception:" + type(exc).__name__)
    if _fingerprint(args) != before:
        _fail("prior_adapter_mutated_inputs")
    copied = _copy(outcome, "outcome", dict)
    audit_wa_binary64_state(_need(copied, "state", "outcome"))
    return copied


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "WaBinary64MidpointError",
    "observed_binary64_operation", "trace_native_wa_score",
    "audit_wa_binary64_state", "checked_apply_wa_binary64_event",
)
