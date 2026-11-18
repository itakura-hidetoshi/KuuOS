"""Exact-rational shadow of selected original Wa float score records.

Finite Python floats are interpreted by their exact as_integer_ratio() values.
Rational discrepancies are checked against an explicit fixed small budget.
No IEEE-754 semantics proof, external issuer certification, full Lean/Python
refinement, state repair, store mutation or host authority is asserted.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
import math
from typing import Any

from runtime import kuuos_lean_python_belief_receipt_guard_v0_18 as prior
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
from runtime.kuuos_lean_python_wa_evaluation_guard_v0_15 import _POSITIVE, _ALERT, _PHASES

VERSION = "kuuos_lean_python_wa_rational_shadow_v0_19"
SOURCE_MAIN = "af8b47cc20d35e1a44b25df4917505a90a4a9709"
ERROR_BUDGET = Fraction(1, 2**40)
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


class WaRationalShadowError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, *, status: str = BLOCKED) -> None:
    raise WaRationalShadowError(status, (issue,))


def _copy(value: Any, label: str, kind: type) -> Any:
    if value is None:
        _fail(label + ":missing", status=NO_DATA)
    try:
        copy = _finite_json(value)
    except Exception as exc:
        _fail(label + ":invalid_json:" + type(exc).__name__)
    if type(copy) is not kind:
        _fail(label + ":exact_" + kind.__name__ + "_required")
    return copy


def _require(value: dict, key: str, label: str) -> Any:
    if key not in value:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return value[key]


def _q(value: Any, label: str) -> Fraction:
    if type(value) is int:
        return Fraction(value)
    if type(value) is not float or not math.isfinite(value):
        _fail(label + ":finite_native_int_or_float_required")
    return Fraction(*value.as_integer_ratio())


def _interval_value(mapping: dict, axis: str, bound: str, label: str) -> Fraction:
    item = _copy(_require(mapping, axis, label), label + ":" + axis, dict)
    return _q(_require(item, bound, label + ":" + axis), label + ":" + axis + ":" + bound)


def rational_ideal_record(profile: Any, weights: Any, beta: Any) -> dict[str, Fraction]:
    """Exact rational operations on represented input values, NOT float arithmetic."""
    p = _copy(profile, "profile", dict)
    w = _copy(weights, "weights", dict)
    b = _q(beta, "beta")
    positive = _copy(_require(p, "positive_intervals", "profile"), "positive", dict)
    alerts = _copy(_require(p, "alert_intervals", "profile"), "alert", dict)
    terms = {}
    for bound in ("lower", "upper"):
        samples = [_interval_value(positive, name, bound, "positive") for name in _POSITIVE]
        terms["weighted_interval." + bound] = sum(
            (_q(_require(w, name, "weights"), "weights:" + name) * v
             for name, v in zip(_POSITIVE, samples)), Fraction(0)
        )
        terms["weakest_interval." + bound] = min(samples)
        terms["relational_interval." + bound] = (
            (1 - b) * terms["weighted_interval." + bound]
            + b * terms["weakest_interval." + bound]
        )
        alert_samples = [_interval_value(alerts, name, bound, "alert") for name in _ALERT]
        terms["alert_interval." + bound] = max(alert_samples)
    raw_lower = terms["relational_interval.lower"] * (1 - terms["alert_interval.upper"])
    raw_upper = terms["relational_interval.upper"] * (1 - terms["alert_interval.lower"])
    terms["wa_interval.lower"] = raw_lower
    terms["wa_interval.upper"] = min(Fraction(1), raw_upper)
    terms["wa_interval.width"] = terms["wa_interval.upper"] - raw_lower
    return terms


def audit_wa_rational_state(state: Any) -> dict[str, Any]:
    """Finite observation certificate from *stored* native scores.

    The Lean theorem proves the implication of an exact rational inequality,
    not that Python always satisfies the declared budget for all inputs.
    """
    s = _copy(state, "state", dict)
    phase = _require(s, "current_phase", "state")
    if type(phase) is not str or phase not in _PHASES:
        _fail("state:unknown_phase")
    profiles = _copy(_require(s, "profiles", "state"), "profiles", list)
    records = _copy(_require(s, "wa_records", "state"), "records", list)
    result = {
        "version": VERSION, "source_main": SOURCE_MAIN,
        "state_digest": _fingerprint(s), "error_budget": [1, 2**40],
        "certificates": [], "real_from_rational_condition_checked": True,
        "ieee754_global_rounding_proved": False,
        "lean_python_full_refinement_proved": False,
        "external_issuer_authenticated": False,
        "authority_granted": False,
    }
    if _PHASES.index(phase) < _PHASES.index("evaluate"):
        if records:
            _fail("state:premature_score_records")
        return result
    if len(profiles) != len(records):
        _fail("state:profile_record_count_mismatch")
    weights = _copy(_require(s, "weights", "state"), "weights", dict)
    thresholds = _copy(_require(s, "thresholds", "state"), "thresholds", dict)
    beta = _require(thresholds, "bottleneck_weight", "thresholds")
    for index, (profile, record) in enumerate(zip(profiles, records)):
        label = "wa_record[" + str(index) + "]"
        profile = _copy(profile, label + ":profile", dict)
        record = _copy(record, label, dict)
        option_id = _require(profile, "option_id", label)
        if type(option_id) is not str or record.get("option_id") != option_id:
            _fail(label + ":option_id_mismatch")
        ideals = rational_ideal_record(profile, weights, beta)
        largest = Fraction(0)
        fields = {}
        for field, exact in ideals.items():
            name, key = field.split(".", 1)
            observed = _copy(_require(record, name, label), label + ":" + name, dict)
            actual = _q(_require(observed, key, label + ":" + name), label + ":" + field)
            error = abs(actual - exact)
            if error > ERROR_BUDGET:
                _fail(label + ":" + field + ":exact_rational_error_exceeds_budget")
            largest = max(largest, error)
            fields[field] = [error.numerator, error.denominator]
        result["certificates"].append({
            "option_id": option_id,
            "exact_error_by_field": fields,
            "maximum_absolute_error": [largest.numerator, largest.denominator],
        })
    return result


def checked_apply_wa_rational_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """Exactly one original v0.18 adapter, rational checks before and after."""
    args = [_copy(x, name, dict) for x, name in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief"))]
    audit_wa_rational_state(args[0])
    frozen = _fingerprint(args)
    try:
        result = prior.checked_apply_wa_belief_receipt_event(*args)
    except prior.BeliefReceiptBoundaryError as exc:
        raise WaRationalShadowError(
            exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED,
            tuple("belief_receipt:" + issue for issue in exc.issues),
        ) from exc
    except Exception as exc:
        _fail("prior_adapter_raised:" + type(exc).__name__)
    if _fingerprint(args) != frozen:
        _fail("prior_adapter_mutated_arguments")
    copied = _copy(result, "result", dict)
    audit_wa_rational_state(_require(copied, "state", "result"))
    return copied


__all__ = (
    "VERSION", "SOURCE_MAIN", "ERROR_BUDGET", "BLOCKED", "NO_DATA",
    "WaRationalShadowError", "rational_ideal_record", "audit_wa_rational_state",
    "checked_apply_wa_rational_event",
)
