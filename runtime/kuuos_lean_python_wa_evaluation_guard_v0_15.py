"""Independent local v0.3 Wa float-score check around the unchanged v0.14 gate.

Reproduces stored Python float operations from already supplied normalized
profiles, weights and thresholds without invoking the native evaluator.
External provenance, Lean-real refinement, arbitrary writes or host effects
are NOT proved. No score, digest or original state is repaired.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
import math
from typing import Any, NoReturn
from runtime import kuuos_lean_python_wa_gate_guard_v0_14 as prior
from runtime.kuuos_lean_python_wa_numeric_guard_v0_13 import (
    WaNumericBoundaryError, _state_numbers,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint

VERSION = "kuuos_lean_python_wa_evaluation_guard_v0_15"
SOURCE_MAIN = "69bd75f4ae14e912b45f520636ffd8a400067d36"
BLOCKED, NO_DATA = "BLOCKED", "NO_DATA"
_POSITIVE = ("inclusion", "dialogue", "mutual_reflection", "emergence",
             "dynamic_adaptation", "non_hierarchy", "recursive_feedback")
_ALERT = ("coercive_conformity", "exclusion", "oppression", "hierarchy_concentration",
          "minority_erasure", "false_stability", "complacency_in_safe_conditions")
_PHASES = ("bind", "profile", "evaluate", "false_harmony_check",
           "plurality_check", "gate", "commit")


class WaEvaluationBoundaryError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, status: str = BLOCKED) -> NoReturn:
    raise WaEvaluationBoundaryError(status, (issue,))


def _required(value: dict, key: str, label: str) -> Any:
    if key not in value:
        _fail(label + ":" + key + ":missing", NO_DATA)
    return value[key]


def _dict(value: Any, label: str) -> dict:
    if type(value) is not dict:
        _fail(label + ":exact_object_required")
    return value


def _list(value: Any, label: str) -> list:
    if type(value) is not list:
        _fail(label + ":exact_list_required")
    return value


def _copy(value: Any, label: str, object_required: bool = False) -> Any:
    if object_required and value is None:
        _fail(label + ":missing", NO_DATA)
    try:
        result = _finite_json(value)
    except Exception as exc:
        _fail(label + ":invalid_json:" + type(exc).__name__)
    if object_required:
        _dict(result, label)
    return result


def _same(left: Any, right: Any) -> bool:
    return _fingerprint(left) == _fingerprint(right)


def _number(value: Any, label: str) -> float:
    if type(value) not in (int, float):
        _fail(label + ":numeric_type_invalid")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        _fail(label + ":float_conversion:" + type(exc).__name__)
    if not math.isfinite(number) or not 0 <= number <= 1:
        _fail(label + ":finite_unit_invalid")
    return number


def _calculate(profile: dict, weights: dict, beta: float, label: str) -> dict:
    positive = _dict(_required(profile, "positive_intervals", label), label + ":positive")
    alerts = _dict(_required(profile, "alert_intervals", label), label + ":alerts")
    def axis(source: dict, name: str, bound: str) -> float:
        item = _dict(_required(source, name, label), label + ":" + name)
        return _number(_required(item, bound, label), label + ":" + name + ":" + bound)
    wl = sum(_number(_required(weights, name, label), label + ":weight:" + name)
             * axis(positive, name, "lower") for name in _POSITIVE)
    wu = sum(_number(_required(weights, name, label), label + ":weight:" + name)
             * axis(positive, name, "upper") for name in _POSITIVE)
    ml = min(axis(positive, name, "lower") for name in _POSITIVE)
    mu = min(axis(positive, name, "upper") for name in _POSITIVE)
    rl = (1.0 - beta) * wl + beta * ml
    ru = (1.0 - beta) * wu + beta * mu
    al = max(axis(alerts, name, "lower") for name in _ALERT)
    au = max(axis(alerts, name, "upper") for name in _ALERT)
    low, high = rl * (1.0 - au), ru * (1.0 - al)
    if not (0.0 <= low <= high <= 1.0 + 1e-12):
        _fail(label + ":native_wa_interval_invalid")
    high_clipped = min(1.0, high)
    return {
        "option_id": _required(profile, "option_id", label),
        "option_digest": _required(profile, "option_digest", label),
        "wa_profile_digest": _required(profile, "wa_profile_digest", label),
        "weighted_interval": {"lower": wl, "upper": wu},
        "weakest_interval": {"lower": ml, "upper": mu},
        "relational_interval": {"lower": rl, "upper": ru},
        "alert_interval": {"lower": al, "upper": au},
        "wa_interval": {"lower": low, "upper": high_clipped, "width": high_clipped - low},
        "dissent_considered": _required(profile, "dissent_considered", label),
        "minority_preserved": _required(profile, "minority_preserved", label),
    }


def _check_scores(state: dict, label: str) -> None:
    phase = _required(state, "current_phase", label)
    if type(phase) is not str or phase not in _PHASES:
        _fail(label + ":phase_invalid")
    if _PHASES.index(phase) < 2:
        return  # prior guard still checks that records are absent before evaluate
    try:
        _state_numbers(state, label)
    except WaNumericBoundaryError as exc:
        raise WaEvaluationBoundaryError(exc.status, tuple("numeric:" + x for x in exc.issues)) from exc
    except Exception as exc:
        _fail(label + ":numeric_validator_raised:" + type(exc).__name__)
    weights = _dict(_required(state, "weights", label), label + ":weights")
    thresholds = _dict(_required(state, "thresholds", label), label + ":thresholds")
    beta = _number(_required(thresholds, "bottleneck_weight", label), label + ":beta")
    profiles = _list(_required(state, "profiles", label), label + ":profiles")
    records = _list(_required(state, "wa_records", label), label + ":wa_records")
    if len(profiles) != len(records):
        _fail(label + ":record_count_or_order_mismatch")
    for index, (raw_profile, raw_record) in enumerate(zip(profiles, records)):
        path = label + ":wa_records[" + str(index) + "]"
        expected = _calculate(_dict(raw_profile, path + ":profile"), weights, beta, path)
        observed = _dict(raw_record, path)
        for field, value in expected.items():
            if not _same(_required(observed, field, path), value):
                _fail(path + ":" + field + ":derived_value_mismatch")
        if set(observed) != set(expected):
            _fail(path + ":unexpected_record_fields")


def checked_apply_wa_evaluation_event(state: Any, event: Any) -> dict:
    for name, dependency in (("_finite_json", _finite_json), ("_fingerprint", _fingerprint),
                             ("_state_numbers", _state_numbers),
                             ("gate_adapter", prior.checked_apply_wa_gate_event)):
        if not callable(dependency):
            _fail("prerequisite:" + name + ":unavailable", NO_DATA)
    before = _copy(state, "state", True)
    given_event = _copy(event, "event", True)
    _check_scores(before, "pre_state")
    state_copy, event_copy = _copy(before, "state"), _copy(given_event, "event")
    try:
        raw = prior.checked_apply_wa_gate_event(state_copy, event_copy)
    except prior.WaGateBoundaryError as exc:
        raise WaEvaluationBoundaryError(exc.status, tuple("gate:" + x for x in exc.issues)) from exc
    except Exception as exc:
        _fail("gate_adapter_raised:" + type(exc).__name__)
    if not _same(state_copy, before) or not _same(event_copy, given_event):
        _fail("gate_adapter_argument_mutated")
    result = _copy(raw, "result", True)
    if _required(result, "status", "result") not in ("APPLIED", "REPLAYED", "REJECTED") or type(result["status"]) is not str:
        _fail("result:status_invalid")
    _check_scores(_dict(_required(result, "state", "result"), "post_state"), "post_state")
    return result


__all__ = ("VERSION", "SOURCE_MAIN", "WaEvaluationBoundaryError",
           "checked_apply_wa_evaluation_event")
