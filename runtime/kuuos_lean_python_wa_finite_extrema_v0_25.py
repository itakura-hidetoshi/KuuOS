"""Read-only original Wa finite min/max observation identity, v0.25.

The original Wa v0.3 evaluator uses native min() for seven positive-axis
samples and native max() for alert-axis samples. This observer validates
that each finite recorded float and each original observed extremum have
matching exact-rational representations. It does not assert global
Python/IEEE754 min()/max() semantics, issuer authenticity or action
authority. Nothing in the original kernel, scores, ledger or stores
is changed.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from runtime import kuuos_lean_python_wa_upper_clip_v0_24 as previous
from runtime import kuuos_lean_python_wa_normalized_score_v0_23 as v23
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint

VERSION = "kuuos_lean_python_wa_finite_extrema_v0_25"
SOURCE_MAIN = "6a9ec01adfd67ea17822612ad1cb9fa50c4f82bc"
BLOCKED, NO_DATA = "BLOCKED", "NO_DATA"


class WaFiniteExtremaError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(reason: str, status: str = BLOCKED) -> None:
    raise WaFiniteExtremaError(status, (reason,))


def _copy(obj: Any, label: str, kind: type) -> Any:
    try:
        return previous._copy(obj, label, kind)
    except previous.WaUpperClipError as exc:
        raise WaFiniteExtremaError(exc.status, exc.issues) from exc


def _need(data: dict, key: str, label: str) -> Any:
    if key not in data:
        _fail(label + ":" + key + ":missing", NO_DATA)
    return data[key]


def _f(value: Any, label: str) -> Fraction:
    try:
        return previous._f(value, label)
    except previous.WaUpperClipError as exc:
        raise WaFiniteExtremaError(exc.status, exc.issues) from exc


def _q(pair: Any, label: str) -> Fraction:
    try:
        return previous._q(pair, label)
    except previous.WaUpperClipError as exc:
        raise WaFiniteExtremaError(exc.status, exc.issues) from exc


def _pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def certify_finite_extrema(
    samples: Any, observed_min: Any, observed_max: Any,
) -> dict[str, Any]:
    """Pure finite rational witness; caller's source remains unauthenticated."""
    if type(samples) is not list or not samples:
        _fail("finite_extrema:nonempty_rational_list_required")
    items = [_q(item, "sample:" + str(i)) for i, item in enumerate(samples)]
    if any(x < 0 or x > 1 for x in items):
        _fail("finite_extrema:unit_samples_required")
    minimum, maximum = _q(observed_min, "min"), _q(observed_max, "max")
    # The endpoints 1/0 are mathematical fold sentinels, NOT observed
    # native inputs or a claim about an interpreter's internal algorithm.
    min_fold = min([Fraction(1)] + items)
    max_fold = max([Fraction(0)] + items)
    if minimum != min_fold:
        _fail("finite_extrema:observed_min_identity_failed")
    if maximum != max_fold:
        _fail("finite_extrema:observed_max_identity_failed")
    if not all(minimum <= item <= maximum for item in items):
        _fail("finite_extrema:member_bounds_failed")
    return {
        "count": len(items),
        "sample_rationals": [_pair(item) for item in items],
        "observed_min": _pair(minimum),
        "observed_max": _pair(maximum),
        "min_member_indices": [i for i, x in enumerate(items) if x == minimum],
        "max_member_indices": [i for i, x in enumerate(items) if x == maximum],
        "rational_finite_extrema_checked": True,
        "caller_source_authenticated": False,
        "python_min_max_semantics_proved": False,
    }


def certify_original_wa_extrema_trace(
    profile: Any, weights: Any, beta: Any,
) -> dict[str, Any]:
    """Bind selected min/max to each original positive/alert axis and Wa score."""
    p, w = _copy(profile, "profile", dict), _copy(weights, "weights", dict)
    try:
        prior = v23.certify_normalized_final_trace(p, w, beta)
        upper_clip = previous.certify_original_upper_clip_trace(p, w, beta)
        trace = v20.trace_native_wa_score(p, w, beta)
    except v23.WaNormalizedScoreError as exc:
        raise WaFiniteExtremaError(exc.status, ("v023:" + ";".join(exc.issues),)) from exc
    except previous.WaUpperClipError as exc:
        raise WaFiniteExtremaError(exc.status, ("v024:" + ";".join(exc.issues),)) from exc
    except v20.WaBinary64MidpointError as exc:
        raise WaFiniteExtremaError(exc.status, ("v020:" + ";".join(exc.issues),)) from exc

    pos = _copy(_need(p, "positive_intervals", "profile"), "positive_intervals", dict)
    alert = _copy(_need(p, "alert_intervals", "profile"), "alert_intervals", dict)
    pos_axes = tuple(v20.native._POSITIVE)
    alert_axes = tuple(v20.native._ALERT)
    if not pos_axes or len(pos) != len(pos_axes) or set(pos) != set(pos_axes):
        _fail("positive_axes:original_native_axis_set_required")
    if not alert_axes or len(alert) != len(alert_axes) or set(alert) != set(alert_axes):
        _fail("alert_axes:original_native_axis_set_required")
    fields = _copy(_need(trace, "fields", "trace"), "trace_fields", dict)
    endpoints = _copy(_need(prior, "endpoints", "prior"), "prior_endpoints", list)
    if len(endpoints) != 2:
        _fail("prior:two_wa_endpoints_required")
    b = _f(beta, "beta")
    outputs: list[dict[str, Any]] = []
    for endpoint, opposite_alert, row in zip(
        ("lower", "upper"), ("upper", "lower"), endpoints
    ):
        old = _copy(row, "prior:" + endpoint, dict)
        if _need(old, "endpoint", "prior") != endpoint:
            _fail("prior:wa_endpoint_order_mismatch")
        positives: list[Fraction] = []
        alerts: list[Fraction] = []
        for axis in pos_axes:
            values = _copy(_need(pos, axis, "positive"), "positive:" + axis, dict)
            positives.append(_f(_need(values, endpoint, axis), axis + ":" + endpoint))
        for axis in alert_axes:
            values = _copy(_need(alert, axis, "alert"), "alert:" + axis, dict)
            alerts.append(_f(_need(values, opposite_alert, axis),
                             axis + ":" + opposite_alert))
        weakest = _f(_need(fields, "weakest_interval." + endpoint, "fields"),
                     "weakest:" + endpoint)
        strongest_alert = _f(
            _need(fields, "alert_interval." + opposite_alert, "fields"),
            "alert:" + opposite_alert)
        if any(x < 0 or x > 1 for x in positives + alerts):
            _fail("wa:" + endpoint + ":axis_samples_out_of_unit")
        pos_witness = certify_finite_extrema(
            [_pair(x) for x in positives], _pair(weakest),
            _pair(max(positives)))
        alert_witness = certify_finite_extrema(
            [_pair(x) for x in alerts], _pair(min(alerts)),
            _pair(strongest_alert))
        if weakest != min(positives) or strongest_alert != max(alerts):
            _fail("wa:" + endpoint + ":native_extremum_identity_failed")
        normalized = _q(
            _need(old, "exact_normalized_weighted", "prior"),
            "normalized:" + endpoint)
        ideal = v23._rational_ideal(b, normalized, weakest, strongest_alert)
        if ideal != _q(_need(old, "normalized_ideal_score", "prior"),
                       "prior_normalized_ideal:" + endpoint):
            _fail("wa:" + endpoint + ":finite_extremum_score_identity_failed")
        if endpoint == "upper" and (
                upper_clip["upper"]["normalized_ideal"] != _pair(ideal) or
                upper_clip["upper"]["clipped_upper"] !=
                _need(old, "observed_native_wa_score", "prior")):
            _fail("wa:upper_clipping_source_compatibility_failed")
        outputs.append({
            "endpoint": endpoint,
            "alert_source_endpoint": opposite_alert,
            "positive_axis_names": list(pos_axes),
            "alert_axis_names": list(alert_axes),
            "positive_sample_rationals": [_pair(x) for x in positives],
            "alert_sample_rationals": [_pair(x) for x in alerts],
            "observed_weakest_positive": _pair(weakest),
            "observed_strongest_alert": _pair(strongest_alert),
            "positive_min_member_indices": pos_witness["min_member_indices"],
            "alert_max_member_indices": alert_witness["max_member_indices"],
            "normalized_ideal_score": _pair(ideal),
            "original_extremum_identities_checked": True,
            "finite_membership_bounds_checked": True,
            "observed_min_max_gluing_checked": True,
            "python_min_max_semantics_proved": False,
        })
    return {
        "version": VERSION,
        "option_id": _need(p, "option_id", "profile"),
        "endpoint_certificates": outputs,
        "original_wa_source_modified": False,
        "global_python_min_max_semantics_proved": False,
        "external_issuer_authenticated": False,
        "host_authority_granted": False,
    }


def audit_wa_finite_extrema_state(state: Any) -> dict[str, Any]:
    """Retain v0.24 source/state checks before new finite-list claims."""
    try:
        previous_audit = previous.audit_wa_upper_clip_state(state)
    except previous.WaUpperClipError as exc:
        raise WaFiniteExtremaError(exc.status, ("v024:" + ";".join(exc.issues),)) from exc
    s = _copy(state, "state", dict)
    result = {
        "version": VERSION,
        "source_main": SOURCE_MAIN,
        "state_digest": _fingerprint(s),
        "certificates": [],
        "all_original_finite_extrema_checked": False,
        "original_state_modified": False,
        "global_ieee754_semantics_proved": False,
        "python_min_max_semantics_proved": False,
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
    previous_certs = _copy(_need(previous_audit, "certificates", "prior"),
                           "prior_certificates", list)
    if len(profiles) != len(previous_certs):
        _fail("wa:prior_certificate_count_mismatch")
    for p, old in zip(profiles, previous_certs):
        witness = certify_original_wa_extrema_trace(p, weights, beta)
        if witness["option_id"] != old.get("option_id"):
            _fail("wa:prior_option_id_mismatch")
        result["certificates"].append(witness)
    result["all_original_finite_extrema_checked"] = True
    return result


def checked_apply_wa_finite_extrema_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """Reuse the one native adapter without extra host effects."""
    args = [_copy(v, label, dict) for v, label in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief")
    )]
    audit_wa_finite_extrema_state(args[0])
    before = _fingerprint(args)
    try:
        output = previous.checked_apply_wa_upper_clip_event(*args)
    except previous.WaUpperClipError as exc:
        raise WaFiniteExtremaError(exc.status, ("v024:" + ";".join(exc.issues),)) from exc
    except Exception as exc:
        _fail("prior_adapter_exception:" + type(exc).__name__)
    if _fingerprint(args) != before:
        _fail("native_adapter_mutated_caller_arguments")
    copied = _copy(output, "result", dict)
    audit_wa_finite_extrema_state(_need(copied, "state", "result"))
    return copied


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "WaFiniteExtremaError",
    "certify_finite_extrema", "certify_original_wa_extrema_trace",
    "audit_wa_finite_extrema_state", "checked_apply_wa_finite_extrema_event",
)
