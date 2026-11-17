"""Checked Wa classification, plurality witnesses, and route binding (v0.14).

The original v0.13 adapter is called once on defensive finite-JSON copies. This
module checks pre/post snapshots against the native classification priority,
actual local source/profile identifiers, phase-specific plurality values, and
the gate's ordered route rules. Numeric checks remain the v0.13 checks. Returned
native values, envelopes, digests, and rejection diagnostics are not repaired.

Classification uses the supplied bounded alert records and thresholds. This
does not establish that records were correctly calculated from profiles: an
in-range scoring forgery can remain accepted. No evaluator is rerun here.
The Lean WaEndorsementGate and WaPluralityBoundary contain explicit assumptions;
this local Python check is not a Lean/Python refinement proof or proof of source
authenticity. The native suspected-false-harmony restriction is an additional
Python condition. No truth, execution, host, merge, or institutional authority
is granted, and no store initialization, concurrency, or rollback is covered.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any, NoReturn

try:
    from runtime.kuuos_lean_python_wa_numeric_guard_v0_13 import (
        WaNumericBoundaryError as _PriorError, _state_numbers, checked_apply_wa_numeric_event,
    )
except ImportError:
    _PriorError = ()
    _state_numbers = checked_apply_wa_numeric_event = None

try:
    from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
except ImportError:
    _finite_json = _fingerprint = None


VERSION = "kuuos_lean_python_wa_gate_guard_v0_14"
SOURCE_MAIN = "05693ef17179ebddb974f23021be2e7d352b4fbb"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"

_PHASES = ("bind", "profile", "evaluate", "false_harmony_check", "plurality_check", "gate", "commit")
_PLURALITY_FLAGS = (
    "all_source_options_profiled", "retained_alternatives_preserved", "selected_identity_preserved",
    "stakeholder_sections_preserved", "veto_and_appeal_history_preserved", "silent_substitution_detected",
)
_SOURCE_RECEIPTS = (
    "source_stakeholder_registry_digest", "source_utility_records_digest", "source_aggregate_records_digest",
    "source_veto_records_digest", "source_appeal_history_digest",
)
_FALSE_FIELDS = (
    "option_id", "confirmed_false_harmony", "suspected_false_harmony", "reason_codes",
    "alert_interval", "smooth_surface_is_not_proof", "minority_preserved", "dissent_considered",
)
_BASIS_FIELDS = (
    "wa_id", "source_plural_state_digest", "source_committed_plural_digest",
    "source_plural_decision_basis_digest", "source_decision_basis_digest", "source_route",
    "source_selected_option_id", "source_stakeholder_registry_digest", "source_utility_records_digest",
    "source_veto_records_digest", "source_aggregate_records_digest", "source_appeal_history_digest",
    "wa_records", "false_harmony_records", "plurality", "route", "endorsed_option_ids", "review_option_ids",
)


class WaGateBoundaryError(RuntimeError):
    """Missing local prerequisites or a violated classification/gate boundary."""

    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status = status
        self.issues = tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise WaGateBoundaryError(status, (issue,))


def _required(value: dict[str, Any], key: str, label: str) -> Any:
    if key not in value:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return value[key]


def _object(value: Any, label: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail(label + ":exact_object_required")
    return value


def _list(value: Any, label: str) -> list[Any]:
    if type(value) is not list:
        _fail(label + ":exact_list_required")
    return value


def _string(value: Any, label: str, *, empty: bool = False) -> str:
    if type(value) is not str or (not empty and not value):
        _fail(label + ":exact_string_required")
    return value


def _strings(value: Any, label: str) -> list[str]:
    values = _list(value, label)
    for item in values:
        _string(item, label + ":item")
    if len(values) != len(set(values)):
        _fail(label + ":duplicate")
    return values


def _bool(value: Any, label: str) -> bool:
    if type(value) is not bool:
        _fail(label + ":exact_bool_required")
    return value


def _number(value: Any, label: str) -> float:
    # Finite JSON and the complete prior numeric check run first. This guard
    # repeats only the exact type/range boundary used in its own predicates.
    if type(value) not in (int, float) or value < 0 or value > 1:
        _fail(label + ":unit_int_or_float_required")
    return float(value)


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


def _same(left: Any, right: Any) -> bool:
    return _fingerprint(left) == _fingerprint(right)


def _prior_error(exc: Any, label: str) -> NoReturn:
    status = exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED
    raise WaGateBoundaryError(status, tuple(label + ":" + issue for issue in exc.issues)) from exc


def _numeric_state(state: dict[str, Any], label: str) -> None:
    copied = _json(state, label)
    try:
        outcome = _state_numbers(copied, label)
    except _PriorError as exc:
        _prior_error(exc, "numeric")
    except Exception as exc:
        _fail(label + ":numeric_state_check_raised:" + type(exc).__name__)
    if not _same(_json(copied, label), state):
        _fail(label + ":numeric_validator_argument_mutated")
    if outcome is not None:
        _fail(label + ":numeric_validator_contract_invalid")


def _source_and_records(state: dict[str, Any], position: int, label: str
                        ) -> tuple[list[dict[str, Any]], dict[str, Any], set[str]]:
    source_ids = _strings(_required(state, "source_option_ids", label), label + ":source_option_ids")
    source_set = set(source_ids)
    retained = _strings(_required(state, "source_retained_alternative_ids", label), label + ":source_retained_alternative_ids")
    if not set(retained).issubset(source_set):
        _fail(label + ":retained_option_outside_source")
    selected = _string(_required(state, "source_selected_option_id", label), label + ":source_selected_option_id", empty=True)
    if selected and selected not in source_set:
        _fail(label + ":selected_option_outside_source")
    source_route = _string(_required(state, "source_route", label), label + ":source_route")
    if source_route == "CONSENSUS_CANDIDATE" and not selected:
        _fail(label + ":consensus_selected_identity_missing")
    option_digests = _object(_required(state, "source_option_digest_by_id", label), label + ":source_option_digest_by_id")
    if set(option_digests) != source_set:
        _fail(label + ":source_option_digest_inventory_mismatch")
    for digest in option_digests.values():
        _string(digest, label + ":source_option_digest")
    for field in _SOURCE_RECEIPTS:
        _string(_required(state, field, label), label + ":" + field)

    profiles = _list(_required(state, "profiles", label), label + ":profiles")
    profile_map = {}
    for index, raw in enumerate(profiles):
        path = f"{label}:profiles[{index}]"
        profile = _object(raw, path)
        option_id = _string(_required(profile, "option_id", path), path + ":option_id")
        if option_id not in source_set or option_id in profile_map:
            _fail(path + ":source_identity_mismatch_or_duplicate")
        if _string(_required(profile, "option_digest", path), path + ":option_digest") != option_digests[option_id]:
            _fail(path + ":source_option_digest_mismatch")
        _string(_required(profile, "wa_profile_digest", path), path + ":wa_profile_digest")
        for flag in ("minority_preserved", "dissent_considered"):
            _bool(_required(profile, flag, path), path + ":" + flag)
        profile_map[option_id] = profile
    if position < 1:
        if profiles:
            _fail(label + ":premature_profiles")
    elif set(profile_map) != source_set:
        _fail(label + ":profiles_do_not_cover_actual_source_options")

    records = _list(_required(state, "wa_records", label), label + ":wa_records")
    record_map = {}
    for index, raw in enumerate(records):
        path = f"{label}:wa_records[{index}]"
        record = _object(raw, path)
        option_id = _string(_required(record, "option_id", path), path + ":option_id")
        if option_id not in profile_map or option_id in record_map:
            _fail(path + ":profile_identity_mismatch_or_duplicate")
        for field in ("option_digest", "wa_profile_digest", "minority_preserved", "dissent_considered"):
            if not _same(_required(record, field, path), profile_map[option_id][field]):
                _fail(path + ":profile_binding_mismatch:" + field)
        record_map[option_id] = record
    if position < 2:
        if records:
            _fail(label + ":premature_evaluation_records")
    elif set(record_map) != source_set:
        _fail(label + ":records_do_not_cover_actual_source_options")
    return profiles, record_map, source_set


def _classification(state: dict[str, Any], profiles: list[dict[str, Any]],
                    records: dict[str, Any], label: str) -> list[dict[str, Any]]:
    thresholds = state["thresholds"]
    confirmed_floor = _number(thresholds["confirmed_false_harmony_threshold"], label + ":confirmed_threshold")
    suspected_floor = _number(thresholds["suspected_false_harmony_threshold"], label + ":suspected_threshold")
    result = []
    for profile in profiles:
        record = records[profile["option_id"]]
        alert = record["alert_interval"]
        lower = _number(alert["lower"], label + ":alert_lower")
        upper = _number(alert["upper"], label + ":alert_upper")
        reasons = []
        confirmed = suspected = False
        if lower >= confirmed_floor:
            confirmed = True
            reasons.append("confirmed_alert_floor_reached")
        if profile["minority_preserved"] is not True:
            confirmed = True
            reasons.append("minority_not_preserved")
        if not confirmed and upper >= suspected_floor:
            suspected = True
            reasons.append("alert_upper_reaches_suspicion")
        if not confirmed and profile["dissent_considered"] is not True:
            suspected = True
            reasons.append("dissent_not_considered")
        result.append({
            "option_id": profile["option_id"], "confirmed_false_harmony": confirmed,
            "suspected_false_harmony": suspected, "reason_codes": reasons,
            "alert_interval": alert, "smooth_surface_is_not_proof": True,
            "minority_preserved": profile["minority_preserved"],
            "dissent_considered": profile["dissent_considered"],
        })
    return result


def _actual_plurality(state: dict[str, Any], profile_ids: set[str], source_ids: set[str]) -> dict[str, bool]:
    selected = state["source_selected_option_id"]
    return {
        "all_source_options_profiled": profile_ids == source_ids,
        "retained_alternatives_preserved": set(state["source_retained_alternative_ids"]).issubset(profile_ids),
        "selected_identity_preserved": not selected or selected in profile_ids,
        "stakeholder_sections_preserved": bool(state["source_stakeholder_registry_digest"]
                                              and state["source_utility_records_digest"]
                                              and state["source_aggregate_records_digest"]),
        "veto_and_appeal_history_preserved": bool(state["source_veto_records_digest"] and state["source_appeal_history_digest"]),
        "silent_substitution_detected": False,
    }


def _gate(state: dict[str, Any], records: dict[str, Any], classified: dict[str, Any],
          label: str) -> tuple[str, list[str], list[str]]:
    plurality = state["plurality"]
    if not all(plurality[field] is True for field in _PLURALITY_FLAGS[:-1]) or plurality["silent_substitution_detected"] is True:
        return "QUARANTINE", [], []
    direct = {"NEGOTIATE": "REOBSERVE", "APPEAL": "REOBSERVE", "HANDOVER": "ESCALATE",
              "HOLD": "HOLD", "REJECT": "REJECT", "QUARANTINE": "QUARANTINE"}
    source_route = state["source_route"]
    if source_route in direct:
        return direct[source_route], [], list(state["source_retained_alternative_ids"])
    if source_route != "CONSENSUS_CANDIDATE":
        return "QUARANTINE", [], []
    selected = state["source_selected_option_id"]
    if not selected:
        return "QUARANTINE", [], []
    if selected not in records or selected not in classified:
        return "QUARANTINE", [], [selected]
    false_record = classified[selected]
    if false_record["confirmed_false_harmony"]:
        return "ESCALATE", [], [selected]
    if false_record["suspected_false_harmony"]:
        return "REOBSERVE", [], [selected]
    record = records[selected]
    if (_number(record["wa_interval"]["lower"], label + ":wa_lower")
            < _number(state["thresholds"]["minimum_wa_floor"], label + ":minimum_wa_floor")
            or _number(record["weakest_interval"]["lower"], label + ":weakest_lower")
            < _number(state["thresholds"]["minimum_dimension_floor"], label + ":minimum_dimension_floor")):
        return "REPAIR", [], [selected]
    return "ENDORSE", [selected], []


def _state_semantics(state: dict[str, Any], label: str) -> None:
    phase = _string(_required(state, "current_phase", label), label + ":current_phase")
    if phase not in _PHASES:
        _fail(label + ":phase_invalid")
    position = _PHASES.index(phase)
    profiles, records, source_ids = _source_and_records(state, position, label)
    false_records = _list(_required(state, "false_harmony_records", label), label + ":false_harmony_records")
    if position < 3 and false_records:
        _fail(label + ":premature_false_harmony_records")
    false_ids = set()
    for index, raw in enumerate(false_records):
        path = f"{label}:false_harmony_records[{index}]"
        record = _object(raw, path)
        for field in _FALSE_FIELDS:
            _required(record, field, path)
        if set(record) != set(_FALSE_FIELDS):
            _fail(path + ":extra_fields")
        option_id = _string(record["option_id"], path + ":option_id")
        if option_id not in records or option_id in false_ids:
            _fail(path + ":record_identity_mismatch_or_duplicate")
        false_ids.add(option_id)
        _strings(record["reason_codes"], path + ":reason_codes")
        for flag in ("confirmed_false_harmony", "suspected_false_harmony", "smooth_surface_is_not_proof",
                     "minority_preserved", "dissent_considered"):
            _bool(record[flag], path + ":" + flag)
    _numeric_state(state, label)
    expected_false = _classification(state, profiles, records, label) if position >= 3 else []
    if not _same(false_records, expected_false):
        _fail(label + ":false_harmony_classification_binding_mismatch")
    plurality = _object(_required(state, "plurality", label), label + ":plurality")
    missing, extra = set(_PLURALITY_FLAGS) - set(plurality), set(plurality) - set(_PLURALITY_FLAGS)
    if extra:
        _fail(label + ":plurality_extra_fields")
    if missing:
        _fail(label + ":plurality_missing_fields:" + ",".join(sorted(missing)), status=NO_DATA)
    for field in _PLURALITY_FLAGS:
        _bool(plurality[field], label + ":plurality:" + field)
    expected_plurality = (_actual_plurality(state, {profile["option_id"] for profile in profiles}, source_ids)
                          if position >= 4 else {field: False for field in _PLURALITY_FLAGS})
    if not _same(plurality, expected_plurality):
        _fail(label + ":plurality_actual_binding_mismatch")
    for field in ("route", "endorsed_option_ids", "review_option_ids", "pending_replan_activation", "wa_basis_digest"):
        _required(state, field, label)
    if position < 5:
        expected_gate = {"route": "HOLD", "endorsed_option_ids": [], "review_option_ids": [],
                         "pending_replan_activation": False, "wa_basis_digest": ""}
    else:
        classified = {record["option_id"]: record for record in expected_false}
        route, endorsed, review = _gate(state, records, classified, label)
        expected_gate = {"route": route, "endorsed_option_ids": endorsed, "review_option_ids": review,
                         "pending_replan_activation": route not in {"REJECT", "QUARANTINE"}}
        if route == "ENDORSE":
            selected = state["source_selected_option_id"]
            chosen = classified[selected]
            if (chosen["confirmed_false_harmony"] is not False or chosen["suspected_false_harmony"] is not False
                    or chosen["minority_preserved"] is not True or chosen["dissent_considered"] is not True
                    or selected not in source_ids or endorsed != [selected]):
                _fail(label + ":endorsement_conditions_not_met")
        # v0.6's canonical JSON fingerprint is the same finite-JSON SHA256
        # construction used by the original native sha for this 18-field map.
        basis = {field: _required(state, field, label) for field in _BASIS_FIELDS}
        expected_gate["wa_basis_digest"] = _fingerprint(basis)
    for field, expected in expected_gate.items():
        if not _same(state[field], expected):
            _fail(label + ":" + field + ":gate_binding_mismatch")


def checked_apply_wa_gate_event(state: Any, event: Any) -> dict[str, Any]:
    """Check local Wa gate conditions around exactly one original prior call.

    Invalid pre-state conditions, including invalid replay snapshots, stop before
    the prior adapter. Post-state failures stop before a caller can persist the
    returned event result. Native REJECTED diagnostics are kept when the supplied
    unchanged state passes the boundaries. No host operation is performed here.
    """
    for name, function in (("_finite_json", _finite_json), ("_fingerprint", _fingerprint),
                           ("_state_numbers", _state_numbers), ("checked_apply_wa_numeric_event", checked_apply_wa_numeric_event)):
        if not callable(function):
            _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
    before = _json(state, "state", object_required=True)
    observed_event = _json(event, "event", object_required=True)
    _state_semantics(before, "pre_state")
    state_copy, event_copy = _json(before, "state"), _json(observed_event, "event")
    try:
        raw_result = checked_apply_wa_numeric_event(state_copy, event_copy)
    except _PriorError as exc:
        _prior_error(exc, "numeric_adapter")
    except Exception as exc:
        raise WaGateBoundaryError(BLOCKED, ("numeric_adapter_raised:" + type(exc).__name__,)) from exc
    if not _same(_json(state_copy, "numeric_state_argument"), before):
        _fail("numeric_state_argument_mutated")
    if not _same(_json(event_copy, "numeric_event_argument"), observed_event):
        _fail("numeric_event_argument_mutated")
    result = _json(raw_result, "result", object_required=True)
    status = _required(result, "status", "result")
    if type(status) is not str or status not in ("APPLIED", "REPLAYED", "REJECTED"):
        _fail("result:status_invalid")
    after = _object(_required(result, "state", "result"), "post_state")
    _state_semantics(after, "post_state")
    if status in ("APPLIED", "REPLAYED") and _required(observed_event, "target_phase", "event") == "gate":
        payload = _object(_required(observed_event, "payload", "event"), "event:payload")
        requested = payload.get("requested_route")
        if requested is not None and (type(requested) is not str or requested not in ("", after["route"])):
            _fail("event:requested_route:gate_binding_mismatch")
    return result


__all__ = ("VERSION", "SOURCE_MAIN", "WaGateBoundaryError", "checked_apply_wa_gate_event")
