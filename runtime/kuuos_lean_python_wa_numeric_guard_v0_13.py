"""Finite, ordered unit intervals around the original Wa transition (v0.13).

This additive pure boundary calls the v0.12 checked mediator adapter once. It
checks numeric fields in the supplied and returned states, plus raw profile
numbers on APPLIED/REPLAYED events. No value is clamped, corrected, normalized,
or resealed here. No evaluator is rerun. The native result is returned unchanged
when these extra checks pass; native REJECTED diagnostics remain native.

Integers and finite floats are interpreted as their represented rational values
for bounds and order. Wa width instead must match Python's subtraction of the
stored endpoints, preserving the original rounded arithmetic. An exact rational
weight sum of one, or exact rational endpoint subtraction, is not required.
The original weight-sum tolerance remains in the original state validator.

The Lean UnitInterval inequalities are explicit real-number hypotheses. These
checks do not prove a Python/Lean refinement, evaluator correctness, monotonicity,
source authenticity, or truth/execution authority. Store initialization, host
effects, cross-process concurrency, and rollback are outside this pure function.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import math
from typing import Any, NoReturn

try:
    from runtime.kuuos_lean_python_mediator_transition_v0_12 import (
        MediatorTransitionError as _PriorError, checked_apply_mediator_event,
    )
except ImportError:
    _PriorError = ()
    checked_apply_mediator_event = None

try:
    from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
except ImportError:
    _finite_json = _fingerprint = None


VERSION = "kuuos_lean_python_wa_numeric_guard_v0_13"
SOURCE_MAIN = "a866f5841e8f324133928eed101cec405d67ac76"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"

_POSITIVE_AXES = (
    "inclusion", "dialogue", "mutual_reflection", "emergence",
    "dynamic_adaptation", "non_hierarchy", "recursive_feedback",
)
_ALERT_AXES = (
    "coercive_conformity", "exclusion", "oppression", "hierarchy_concentration",
    "minority_erasure", "false_stability", "complacency_in_safe_conditions",
)
_THRESHOLDS = (
    "bottleneck_weight", "minimum_wa_floor", "minimum_dimension_floor",
    "suspected_false_harmony_threshold", "confirmed_false_harmony_threshold",
)
_RECORD_INTERVALS = (
    "weighted_interval", "weakest_interval", "relational_interval", "alert_interval", "wa_interval",
)


class WaNumericBoundaryError(RuntimeError):
    """Missing numeric prerequisites or an explicitly violated local boundary."""

    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status = status
        self.issues = tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise WaNumericBoundaryError(status, (issue,))


def _required(value: dict[str, Any], key: str, label: str) -> Any:
    if key not in value:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return value[key]


def _json(value: Any, label: str, *, object_required: bool = False) -> Any:
    if object_required and value is None:
        _fail(label + ":missing", status=NO_DATA)
    try:
        copied = _finite_json(value)
    except Exception as exc:
        _fail(label + ":invalid_json:" + type(exc).__name__)
    if object_required:
        _object(copied, label)
    return copied


def _object(value: Any, label: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail(label + ":exact_object_required")
    return value


def _list(value: Any, label: str) -> list[Any]:
    if type(value) is not list:
        _fail(label + ":exact_list_required")
    return value


def _keys(value: Any, required: tuple[str, ...], label: str) -> dict[str, Any]:
    value = _object(value, label)
    extra, missing = set(value) - set(required), set(required) - set(value)
    if extra:
        _fail(label + ":unexpected_fields:" + ",".join(sorted(extra)))
    if missing:
        _fail(label + ":missing_fields:" + ",".join(sorted(missing)), status=NO_DATA)
    return value


def _ratio(value: Any, label: str) -> tuple[int, int]:
    """Exact represented value; no bool, numeric string, or float conversion."""
    if type(value) is int:
        return value, 1
    if type(value) is not float or not math.isfinite(value):
        _fail(label + ":finite_exact_int_or_float_required")
    return value.as_integer_ratio()


def _unit(value: Any, label: str) -> tuple[int, int]:
    numerator, denominator = _ratio(value, label)
    if numerator < 0 or numerator > denominator:
        _fail(label + ":outside_unit_range")
    return numerator, denominator


def _interval(value: Any, label: str, *, width: bool = False) -> dict[str, Any]:
    interval = _keys(value, ("lower", "upper", "width") if width else ("lower", "upper"), label)
    lower_n, lower_d = _unit(interval["lower"], label + ":lower")
    upper_n, upper_d = _unit(interval["upper"], label + ":upper")
    if lower_n * upper_d > upper_n * lower_d:
        _fail(label + ":lower_exceeds_upper")
    if width:
        width_n, width_d = _ratio(interval["width"], label + ":width")
        if width_n < 0:
            _fail(label + ":negative_width")
        # This checks native rounded subtraction, not equality to the rational
        # difference of endpoints. In-range integer endpoints are only 0 or 1.
        expected = interval["upper"] - interval["lower"]
        expected_n, expected_d = _ratio(expected, label + ":native_width")
        if width_n * expected_d != expected_n * width_d:
            _fail(label + ":width_not_native_endpoint_subtraction")
    return interval


def _profiles(value: Any, label: str) -> None:
    for index, raw in enumerate(_list(value, label)):
        path = f"{label}[{index}]"
        profile = _object(raw, path)
        for field, axes in (("positive_intervals", _POSITIVE_AXES), ("alert_intervals", _ALERT_AXES)):
            axis_map = _keys(_required(profile, field, path), axes, path + ":" + field)
            for axis in axes:
                _interval(axis_map[axis], path + ":" + field + ":" + axis)


def _option_id(record: dict[str, Any], label: str) -> str:
    value = _required(record, "option_id", label)
    if type(value) is not str or not value:
        _fail(label + ":option_id:exact_nonempty_string_required")
    return value


def _state_numbers(state: dict[str, Any], label: str) -> None:
    for field, keys in (("weights", _POSITIVE_AXES), ("thresholds", _THRESHOLDS)):
        values = _keys(_required(state, field, label), keys, label + ":" + field)
        for key in keys:
            _unit(values[key], label + ":" + field + ":" + key)
    _profiles(_required(state, "profiles", label), label + ":profiles")
    records = {}
    for index, raw in enumerate(_list(_required(state, "wa_records", label), label + ":wa_records")):
        path = f"{label}:wa_records[{index}]"
        record = _object(raw, path)
        option_id = _option_id(record, path)
        if option_id in records:
            _fail(label + ":wa_records:duplicate_option")
        for field in _RECORD_INTERVALS:
            _interval(_required(record, field, path), path + ":" + field, width=field == "wa_interval")
        records[option_id] = record
    for index, raw in enumerate(_list(_required(state, "false_harmony_records", label),
                                     label + ":false_harmony_records")):
        path = f"{label}:false_harmony_records[{index}]"
        record = _object(raw, path)
        option_id = _option_id(record, path)
        alert = _interval(_required(record, "alert_interval", path), path + ":alert_interval")
        if option_id not in records:
            _fail(path + ":matching_wa_record_missing", status=NO_DATA)
        if _fingerprint(alert) != _fingerprint(records[option_id]["alert_interval"]):
            _fail(path + ":alert_interval_not_exact_wa_record_copy")


def checked_apply_wa_numeric_event(state: Any, event: Any) -> dict[str, Any]:
    """Call the v0.12 Wa adapter once and return its unmodified native result.

    Supplied and returned states must satisfy the numeric boundary even when the
    native result is REJECTED or REPLAYED. Raw profile event numbers are checked
    only for APPLIED/REPLAYED, so native rejection diagnostics remain intact.
    A post-check failure occurs after a pure transition, before callers persist
    its result. This function neither starts host work nor promises rollback.
    """
    for name, function in (("_finite_json", _finite_json), ("_fingerprint", _fingerprint),
                           ("checked_apply_mediator_event", checked_apply_mediator_event)):
        if not callable(function):
            _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
    before = _json(state, "state", object_required=True)
    observed_event = _json(event, "event", object_required=True)
    _state_numbers(before, "pre_state")
    state_copy, event_copy = _json(before, "state"), _json(observed_event, "event")
    try:
        raw_result = checked_apply_mediator_event("DecisionOSWa", state_copy, event_copy)
    except _PriorError as exc:
        status = exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED
        raise WaNumericBoundaryError(status, tuple("mediator:" + issue for issue in exc.issues)) from exc
    except Exception as exc:
        raise WaNumericBoundaryError(BLOCKED, ("mediator_adapter_raised:" + type(exc).__name__,)) from exc
    if _fingerprint(_json(state_copy, "mediator_state_argument")) != _fingerprint(before):
        _fail("mediator_state_argument_mutated")
    if _fingerprint(_json(event_copy, "mediator_event_argument")) != _fingerprint(observed_event):
        _fail("mediator_event_argument_mutated")
    result = _json(raw_result, "result", object_required=True)
    status = _required(result, "status", "result")
    if type(status) is not str or status not in ("APPLIED", "REPLAYED", "REJECTED"):
        _fail("result:status_invalid")
    after = _object(_required(result, "state", "result"), "post_state")
    _state_numbers(after, "post_state")
    if status in ("APPLIED", "REPLAYED"):
        target = _required(observed_event, "target_phase", "event")
        if target == "profile":
            payload = _object(_required(observed_event, "payload", "event"), "event:payload")
            _profiles(_required(payload, "profiles", "event:payload"), "event:payload:profiles")
    return result


__all__ = ("VERSION", "SOURCE_MAIN", "WaNumericBoundaryError", "checked_apply_wa_numeric_event")
