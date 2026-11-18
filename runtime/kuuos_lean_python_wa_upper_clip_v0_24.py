"""Observed original Wa upper clipping and exact rational comparison v0.24.

The native v0.3 evaluator computes a float upper multiplication and only
then uses min(1.0, high). This additive observer binds the actual v0.20
arithmetic trace to the stored native upper endpoint, and checks the
conditional rational nonexpansive clipping inequality.

Only local observed inputs are certified. The observer NEVER asserts
universal Python min() / CPython / IEEE754 operational semantics, external
issuer authentication or execution authority; it never changes Wa state,
ledger, native evaluator or score.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any

from runtime import kuuos_lean_python_wa_normalized_score_v0_23 as previous
from runtime import kuuos_lean_python_wa_binary64_midpoint_v0_20 as v20
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint

VERSION = "kuuos_lean_python_wa_upper_clip_v0_24"
SOURCE_MAIN = "3f754ac305366a2c69627512a44d8fb86a788fff"
BLOCKED, NO_DATA = "BLOCKED", "NO_DATA"


class WaUpperClipError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, status: str = BLOCKED) -> None:
    raise WaUpperClipError(status, (issue,))


def _copy(value: Any, label: str, kind: type) -> Any:
    try:
        return previous._copy(value, label, kind)
    except previous.WaNormalizedScoreError as exc:
        raise WaUpperClipError(exc.status, exc.issues) from exc


def _need(obj: dict, field: str, label: str) -> Any:
    if field not in obj:
        _fail(label + ":" + field + ":missing", NO_DATA)
    return obj[field]


def _q(value: Any, label: str) -> Fraction:
    try:
        return previous._q_pair(value, label)
    except previous.WaNormalizedScoreError as exc:
        raise WaUpperClipError(exc.status, exc.issues) from exc


def _f(value: Any, label: str) -> Fraction:
    try:
        return previous._q_float(value, label)
    except previous.WaNormalizedScoreError as exc:
        raise WaUpperClipError(exc.status, exc.issues) from exc


def _pair(q: Fraction) -> list[int]:
    return [q.numerator, q.denominator]


def certify_exact_upper_clip(raw: Any, clipped: Any, ideal: Any) -> dict[str, Any]:
    """Pure exact-rational local witness; caller-supplied source NOT authentic."""
    r, c, i = _q(raw, "raw"), _q(clipped, "clipped"), _q(ideal, "ideal")
    if not 0 <= i <= 1:
        _fail("ideal:unit_interval_required")
    if c != min(Fraction(1), r):
        _fail("upper_clip:observed_min_identity_failed")
    raw_error, clipped_error = abs(r - i), abs(c - i)
    if clipped_error > raw_error:
        _fail("upper_clip:nonexpansive_inequality_failed")
    return {
        "unclipped_upper": _pair(r),
        "clipped_upper": _pair(c),
        "normalized_ideal": _pair(i),
        "raw_ideal_error": _pair(raw_error),
        "clipped_ideal_error": _pair(clipped_error),
        "clipping_nonexpansive_checked": True,
        "caller_source_authenticated": False,
        "python_builtin_min_semantics_proved": False,
    }


def certify_original_upper_clip_trace(
    profile: Any, weights: Any, beta: Any,
) -> dict[str, Any]:
    """Bind measured original upper-step to the original stored endpoint."""
    p, w = _copy(profile, "profile", dict), _copy(weights, "weights", dict)
    try:
        prior = previous.certify_normalized_final_trace(p, w, beta)
        trace = v20.trace_native_wa_score(p, w, beta)
    except previous.WaNormalizedScoreError as exc:
        raise WaUpperClipError(exc.status, ("v023:" + ";".join(exc.issues),)) from exc
    except v20.WaBinary64MidpointError as exc:
        raise WaUpperClipError(exc.status, ("v020:" + ";".join(exc.issues),)) from exc
    endpoints = _copy(_need(prior, "endpoints", "prior"), "endpoints", list)
    if len(endpoints) != 2:
        _fail("prior:exactly_two_endpoints_required")
    upper = _copy(endpoints[1], "upper", dict)
    if _need(upper, "endpoint", "upper") != "upper":
        _fail("prior:upper_order_mismatch")
    fields = _copy(_need(trace, "fields", "trace"), "fields", dict)
    steps = _copy(_need(trace, "steps", "trace"), "steps", list)
    matches = [x for x in steps if type(x) is dict and x.get("label") == "wa:upper"]
    factors = [x for x in steps if type(x) is dict and x.get("label") == "wa:upper_factor"]
    if len(matches) != 1 or len(factors) != 1:
        _fail("trace:unique_original_upper_steps_required")
    step = _copy(matches[0], "upper_step", dict)
    factor = _copy(factors[0], "upper_factor", dict)
    if (step.get("operator") != "mul" or
            step.get("exact_midpoint_certificate_checked") is not True or
            factor.get("operator") != "sub" or
            factor.get("exact_midpoint_certificate_checked") is not True):
        _fail("trace:original_midpoint_certificates_required")
    if _q(_need(step, "left", "upper_step"), "upper_step:left") != _f(
            _need(fields, "relational_interval.upper", "fields"), "relational"):
        _fail("trace:upper_relational_operand_identity_failed")
    if _q(_need(step, "right", "upper_step"), "upper_step:right") != _q(
            _need(factor, "observed", "upper_factor"), "factor"):
        _fail("trace:upper_factor_operand_identity_failed")
    normalized = _q(_need(upper, "exact_normalized_weighted", "upper"), "normalized")
    weakest = _f(_need(fields, "weakest_interval.upper", "fields"), "weakest")
    alert = _f(_need(fields, "alert_interval.lower", "fields"), "alert")
    mix = _f(beta, "beta")
    if not all(0 <= q <= 1 for q in (normalized, weakest, alert, mix)):
        _fail("ideal:normalized_scalar_conditions_failed")
    ideal = previous._rational_ideal(mix, normalized, weakest, alert)
    if ideal != _q(_need(upper, "normalized_ideal_score", "upper"), "prior:ideal"):
        _fail("prior:normalized_final_identity_failed")
    raw = _q(_need(step, "observed", "upper_step"), "upper_step:observed")
    clipped = _f(_need(fields, "wa_interval.upper", "fields"), "upper:stored")
    if clipped != _q(_need(upper, "observed_native_wa_score", "upper"), "prior:stored"):
        _fail("prior:original_upper_score_identity_failed")
    clip = certify_exact_upper_clip(_pair(raw), _pair(clipped), _pair(ideal))
    raw_ideal = _q(_need(upper, "original_raw_ideal_score", "upper"),
                   "upper:original_ideal")
    weighted_budget = _q(_need(upper, "normalized_weighted_budget", "upper"),
                         "upper:weight_budget")
    raw_wa_error = abs(raw - raw_ideal)
    raw_normalized_error = abs(raw - ideal)
    bound = raw_wa_error + weighted_budget
    if weighted_budget < 0 or raw_normalized_error > bound:
        _fail("upper_clip:preclip_normalized_composition_failed")
    if _q(clip["clipped_ideal_error"], "clip:error") > bound:
        _fail("upper_clip:clipped_final_budget_failed")
    return {
        "option_id": _need(prior, "option_id", "prior"),
        "version": VERSION,
        "upper": clip,
        "native_raw_upper_midpoint_checked": True,
        "original_native_upper_clipping_identity_checked": True,
        "observed_preclip_raw_wa_error": _pair(raw_wa_error),
        "normalized_weighted_budget": _pair(weighted_budget),
        "preclip_normalized_error": _pair(raw_normalized_error),
        "clipped_normalized_error": clip["clipped_ideal_error"],
        "composed_upper_bound": _pair(bound),
        "conditional_lean_inequality_checked": True,
        "original_state_modified": False,
        "global_ieee754_semantics_proved": False,
        "python_min_max_sum_semantics_proved": False,
        "external_issuer_authenticated": False,
        "host_authority_granted": False,
    }


def audit_wa_upper_clip_state(state: Any) -> dict[str, Any]:
    """Full old audit first; preserve NO_DATA on unevaluated states."""
    try:
        old = previous.audit_wa_normalized_final_state(state)
    except previous.WaNormalizedScoreError as exc:
        raise WaUpperClipError(exc.status, ("v023:" + ";".join(exc.issues),)) from exc
    s = _copy(state, "state", dict)
    result: dict[str, Any] = {
        "version": VERSION,
        "source_main": SOURCE_MAIN,
        "state_digest": _fingerprint(s),
        "certificates": [],
        "all_local_upper_clips_checked": False,
        "original_state_modified": False,
        "global_ieee754_semantics_proved": False,
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
    prior_certs = _copy(_need(old, "certificates", "prior"), "prior_certs", list)
    if len(profiles) != len(prior_certs):
        _fail("state:prior_certificate_count_mismatch")
    for p, old_cert in zip(profiles, prior_certs):
        cert = certify_original_upper_clip_trace(p, weights, beta)
        if cert["option_id"] != old_cert.get("option_id"):
            _fail("state:prior_option_identity_mismatch")
        result["certificates"].append(cert)
    result["all_local_upper_clips_checked"] = True
    return result


def checked_apply_wa_upper_clip_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """Reuse the original single native adapter, never invoke a second host."""
    args = [_copy(value, label, dict) for value, label in (
        (state, "state"), (event, "event"), (plural, "plural"),
        (decision, "decision"), (belief, "belief")
    )]
    audit_wa_upper_clip_state(args[0])
    original = _fingerprint(args)
    try:
        produced = previous.checked_apply_wa_normalized_final_event(*args)
    except previous.WaNormalizedScoreError as exc:
        raise WaUpperClipError(exc.status, ("v023:" + ";".join(exc.issues),)) from exc
    except Exception as exc:
        _fail("prior_adapter_exception:" + type(exc).__name__)
    if _fingerprint(args) != original:
        _fail("native_adapter_mutated_caller_arguments")
    output = _copy(produced, "result", dict)
    audit_wa_upper_clip_state(_need(output, "state", "result"))
    return output


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "WaUpperClipError",
    "certify_exact_upper_clip", "certify_original_upper_clip_trace",
    "audit_wa_upper_clip_state", "checked_apply_wa_upper_clip_event",
)
