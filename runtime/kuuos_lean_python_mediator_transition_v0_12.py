"""Checked pure-event boundary for DecisionOSPlural and DecisionOSWa (v0.12).

One original kernel call is made on bounded finite built-in JSON copies. This
module checks native envelopes, local phase/index/history structure, immutable
source bindings, exact Boolean boundaries, and commit summary alignment before
returning the native result. It does not write a store or invoke a host.

The corresponding Lean phase/index and history theorems have explicit hypotheses
and Nat/structure models. These Python checks are not a refinement proof of those
models, an authentication of supplied source states, or truth/execution authority.
In particular numerical Plural/Wa evaluators and real-number/float correspondence
are outside this boundary. A self-consistent input history is not proof of its
external origin, and a checked transition is not a cross-process transaction.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from types import MappingProxyType
from typing import Any, NoReturn

try:
    from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
except ImportError:
    _finite_json = _fingerprint = None


VERSION = "kuuos_lean_python_mediator_transition_v0_12"
SOURCE_MAIN = "dacc6fb5ae3cd85b9afee48d53348e6cc0a8dcc7"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


class MediatorTransitionError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status = status
        self.issues = tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


@dataclass(frozen=True)
class _Binding:
    stem: str
    kernel: str
    types: str
    phases: tuple[str, ...]
    count: str
    required: tuple[str, ...]
    writes: tuple[tuple[str, tuple[str, ...]], ...]


# These are the original phase functions' top-level writes, excluding common
# event bookkeeping and commit fields. All other keys, including caller-added
# inert JSON fields, must remain canonically unchanged. Plural's source binding
# receipt is the one source_* field which register_stakeholders legitimately sets.
_BINDINGS = MappingProxyType({
    "DecisionOSPlural": _Binding(
        "plural", "runtime.kuuos_decision_os_plural_kernel_v0_2",
        "runtime.kuuos_decision_os_plural_types_v0_2",
        ("bind_v01", "register_stakeholders", "evaluate_plurality", "validate_vetoes",
         "aggregate", "explain", "appeal_window", "adjudicate", "commit"),
        "completed_plural_deliberations",
        ("source_decision_state_digest", "source_decision_basis_digest", "source_committed_decision_digest",
         "source_route", "source_selected_option_id", "source_option_ids", "source_options",
         "source_options_digest", "thresholds", "source_binding_receipt_digest", "stakeholders",
         "stakeholder_registry_digest", "utility_records", "veto_records", "validated_veto_records",
         "unvalidated_veto_records", "veto_excluded_option_ids", "aggregate_records", "ranked_aggregates",
         "broadly_acceptable_option_ids", "explanation", "appeal_history", "selected_option_id",
         "retained_alternative_ids", "plural_decision_basis_digest"),
        (("register_stakeholders", ("source_binding_receipt_digest", "stakeholders", "stakeholder_registry_digest")),
         ("evaluate_plurality", ("utility_records", "plural_evaluation_receipt_digest")),
         ("validate_vetoes", ("veto_records", "validated_veto_records", "unvalidated_veto_records",
                              "veto_excluded_option_ids", "veto_validation_receipt_digest")),
         ("aggregate", ("aggregate_records", "ranked_aggregates", "broadly_acceptable_option_ids", "aggregation_receipt_digest")),
         ("explain", ("explanation",)),
         ("appeal_window", ("appeal_history", "appeal_window_receipt_digest")),
         ("adjudicate", ("route", "selected_option_id", "retained_alternative_ids", "plural_decision_basis_digest",
                         "pending_replan_activation", "adjudication_rule_digest")),
         ("commit", ())),
    ),
    "DecisionOSWa": _Binding(
        "wa", "runtime.kuuos_decision_os_wa_kernel_v0_3",
        "runtime.kuuos_decision_os_wa_types_v0_3",
        ("bind", "profile", "evaluate", "false_harmony_check", "plurality_check", "gate", "commit"),
        "completed_wa_reviews",
        ("source_plural_id", "source_plural_state_digest", "source_committed_plural_digest",
         "source_plural_decision_basis_digest", "source_decision_basis_digest", "source_committed_decision_digest",
         "source_route", "source_selected_option_id", "source_option_ids", "source_retained_alternative_ids",
         "source_options_digest", "source_option_digest_by_id", "source_stakeholder_registry_digest",
         "source_utility_records_digest", "source_veto_records_digest", "source_aggregate_records_digest",
         "source_appeal_history_digest", "weights", "thresholds", "profiles", "wa_records",
         "false_harmony_records", "plurality", "endorsed_option_ids", "review_option_ids", "wa_basis_digest"),
        (("profile", ("profiles",)),
         ("evaluate", ("wa_records", "evaluation_receipt_digest")),
         ("false_harmony_check", ("false_harmony_records", "false_harmony_receipt_digest")),
         ("plurality_check", ("plurality", "plurality_receipt_digest")),
         ("gate", ("route", "endorsed_option_ids", "review_option_ids", "wa_gate_rule_digest",
                   "wa_basis_digest", "pending_replan_activation")),
         ("commit", ())),
    ),
})
MEDIATOR_OS_NAMES = tuple(_BINDINGS)


@dataclass(frozen=True)
class _Native:
    apply: Any
    validate: Any
    state_digest: Any
    event_digest: Any
    result_digest: Any
    sha: Any
    state_version: str
    event_version: str
    result_version: str
    non_authority: dict[str, bool]
    boundary: dict[str, bool]
    normalize_record: Any
    normalize_appeal: Any


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise MediatorTransitionError(status, (issue,))


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
    if object_required and type(copied) is not dict:
        _fail(label + ":object_required")
    return copied


def _same(left: Any, right: Any) -> bool:
    # Canonical JSON keeps bool/int/float distinctions hidden by Python ==.
    return _fingerprint(left) == _fingerprint(right)


def _string(value: Any, label: str, *, empty: bool = False) -> str:
    if type(value) is not str or (not empty and not value):
        _fail(label + ":exact_string_required")
    return value


def _natural(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        _fail(label + ":exact_natural_required")
    return value


def _bool(value: Any, label: str) -> None:
    if type(value) is not bool:
        _fail(label + ":exact_bool_required")


def _list(value: Any, label: str) -> list[Any]:
    if type(value) is not list:
        _fail(label + ":list_required")
    return value


def _strings(value: Any, label: str) -> list[str]:
    values = _list(value, label)
    for item in values:
        _string(item, label + ":item")
    if len(values) != len(set(values)):
        _fail(label + ":duplicate")
    return values


def _object(value: Any, label: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail(label + ":object_required")
    return value


def _flags(value: Any, expected: dict[str, bool], label: str) -> None:
    flags = _object(value, label)
    if not _same(flags, expected):
        _fail(label + ":exact_boolean_boundary_mismatch")


def _function(module: Any, name: str) -> Any:
    value = getattr(module, name, None)
    if not callable(value):
        _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
    return value


def _native(binding: _Binding) -> _Native:
    for name, function in (("_finite_json", _finite_json), ("_fingerprint", _fingerprint)):
        if not callable(function):
            _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
    try:
        kernel = import_module(binding.kernel)
        types = import_module(binding.types)
    except ImportError as exc:
        _fail("prerequisite:runtime_dependency_unavailable:" + type(exc).__name__, status=NO_DATA)
    except Exception as exc:
        _fail("prerequisite:runtime_dependency_raised:" + type(exc).__name__)
    if getattr(types, "PHASES", None) != binding.phases:
        _fail("prerequisite:phase_schema_mismatch")
    versions = []
    for name in ("STATE_VERSION", "EVENT_VERSION", "APPLY_RESULT_VERSION"):
        value = getattr(types, name, None)
        if value is None:
            _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
        versions.append(_string(value, "prerequisite:" + name))
    maps = []
    for name, expected in (("NON_AUTHORITY" if binding.stem == "plural" else "NON_AUTHORITY_FLAGS", False),
                           ("BOUNDARY" if binding.stem == "plural" else "REQUIRED_BOUNDARY", True)):
        value = _json(getattr(types, name, None), "prerequisite:" + name, object_required=True)
        if not value or any(type(flag) is not bool or flag is not expected for flag in value.values()):
            _fail("prerequisite:" + name + ":invalid_boolean_schema")
        maps.append(value)
    prefix = "wa_" if binding.stem == "wa" else ""
    return _Native(
        _function(kernel, "apply_" + binding.stem + "_event"),
        _function(kernel, "validate_" + binding.stem + "_state"),
        _function(types, prefix + "state_digest"), _function(types, prefix + "event_digest"),
        _function(types, prefix + "apply_result_digest"), _function(types, "sha"),
        *versions, *maps,
        _function(kernel, "_normalize_stakeholder" if binding.stem == "plural" else "_normalize_profile"),
        _function(kernel, "_normalize_appeal") if binding.stem == "plural" else None,
    )


def _digest(function: Any, value: Any, label: str) -> str:
    try:
        digest = function(value)
    except Exception as exc:
        _fail(label + ":native_digest_raised:" + type(exc).__name__)
    return _string(digest, label + ":native_digest")


def _validate_native(native: _Native, state: dict[str, Any], label: str) -> None:
    copy = _json(state, label)
    try:
        errors = native.validate(copy)
    except Exception as exc:
        _fail(label + ":native_validator_raised:" + type(exc).__name__)
    if not _same(_json(copy, label), state):
        _fail(label + ":native_validator_argument_mutated")
    if type(errors) is not list or any(type(error) is not str for error in errors):
        _fail(label + ":native_validator_contract_invalid")
    if errors:
        raise MediatorTransitionError(BLOCKED, tuple(label + ":native:" + error for error in errors))


def _normalized(function: Any, label: str, *values: Any) -> dict[str, Any]:
    """Bind normalized packets using original pure helpers, without reapplying."""
    copies = [_json(value, label) for value in values]
    try:
        normalized = function(*copies)
    except Exception as exc:
        _fail(label + ":normalizer_raised:" + type(exc).__name__)
    for copied, original in zip(copies, values):
        if not _same(_json(copied, label), original):
            _fail(label + ":normalizer_argument_mutated")
    return _json(normalized, label, object_required=True)


def _row(binding: _Binding, event: dict[str, Any]) -> dict[str, Any]:
    return {field: _required(event, field, "event") for field in (
        "event_index", "source_phase", "target_phase", "artifact_digest",
        binding.stem + "_event_digest", "created_at_ms",
    )}


def _commit_values(binding: _Binding, native: _Native, state: dict[str, Any],
                   event: dict[str, Any]) -> tuple[dict[str, Any], str]:
    stem = binding.stem
    event_id = event[stem + "_event_digest"]
    if stem == "plural":
        committed = {field: state[field] for field in (
            "plural_id", "plural_version", "source_decision_basis_digest",
            "plural_decision_basis_digest", "route", "selected_option_id",
        )}
        summary = {field: state[field] for field in (
            "plural_version", "route", "selected_option_id", "broadly_acceptable_option_ids",
            "retained_alternative_ids", "plural_decision_basis_digest",
        )}
        summary["appeal_count"] = len(state["appeal_history"])
    else:
        committed = {field: state[field] for field in (
            "wa_id", "wa_version", "source_committed_plural_digest", "source_plural_decision_basis_digest",
            "wa_basis_digest", "route", "endorsed_option_ids", "review_option_ids",
        )}
        summary = {field: state[field] for field in (
            "wa_version", "source_route", "route", "endorsed_option_ids", "review_option_ids", "wa_basis_digest",
        )}
        summary["commit_artifact_digest"] = event["artifact_digest"]
    committed["commit_event_digest"] = event_id
    summary["commit_event_digest"] = event_id
    return summary, _digest(native.sha, committed, "commit")


def _state_history(binding: _Binding, native: _Native, state: dict[str, Any], label: str) -> None:
    stem = binding.stem
    index = state["event_index"]
    history = _list(state["event_history"], label + ":event_history")
    processed = _strings(state["processed_event_digests"], label + ":processed_event_digests")
    if index >= len(binding.phases) or state["current_phase"] != binding.phases[index]:
        _fail(label + ":phase_index_mismatch")
    if len(history) != index or len(processed) != index:
        _fail(label + ":event_history_alignment_mismatch")
    previous_time = 0
    for position, row in enumerate(history, 1):
        row = _object(row, label + ":history_row")
        if set(row) != {"event_index", "source_phase", "target_phase", "artifact_digest",
                       stem + "_event_digest", "created_at_ms"}:
            _fail(label + ":history_row_schema_mismatch")
        if _natural(row["event_index"], label + ":history_row:event_index") != position:
            _fail(label + ":history_row_index_mismatch")
        if (row["source_phase"] != binding.phases[position - 1]
                or row["target_phase"] != binding.phases[position]):
            _fail(label + ":history_row_phase_mismatch")
        timestamp = _natural(row["created_at_ms"], label + ":history_row:created_at_ms")
        if timestamp < previous_time:
            _fail(label + ":history_time_regression")
        previous_time = timestamp
        _string(row["artifact_digest"], label + ":history_row:artifact_digest")
        if _string(row[stem + "_event_digest"], label + ":history_row:event_digest") != processed[position - 1]:
            _fail(label + ":history_processed_digest_mismatch")
    if history and previous_time != state["updated_at_ms"]:
        _fail(label + ":history_updated_at_mismatch")
    predecessor = _string(state["predecessor_" + stem + "_state_digest"], label + ":predecessor", empty=True)
    if bool(predecessor) != bool(index):
        _fail(label + ":predecessor_presence_mismatch")
    summaries = _list(state[stem + "_summaries"], label + ":summaries")
    version = state[stem + "_version"]
    if version != state[binding.count] or version != len(summaries):
        _fail(label + ":commit_summary_alignment_mismatch")
    # These original mediators have one terminal pass; commit has no successor
    # phase and their constructors start all three counters at zero.
    if version != int(state["current_phase"] == "commit"):
        _fail(label + ":terminal_commit_count_mismatch")
    latest = _string(state["latest_committed_" + stem + "_digest"], label + ":latest_committed_digest", empty=True)
    if version:
        summary, digest = _commit_values(binding, native, state, history[-1])
        if not _same(summaries[-1], summary) or latest != digest:
            _fail(label + ":commit_summary_or_digest_binding_mismatch")
    elif latest:
        _fail(label + ":premature_committed_digest")


def _state_flags_and_options(binding: _Binding, state: dict[str, Any], label: str) -> None:
    source = _strings(state["source_option_ids"], label + ":source_option_ids")
    selected = _string(state["source_selected_option_id"], label + ":source_selected_option_id", empty=True)
    if selected and selected not in source:
        _fail(label + ":source_selected_option_unknown")
    if binding.stem == "plural":
        for field in ("veto_excluded_option_ids", "broadly_acceptable_option_ids", "retained_alternative_ids"):
            if not set(_strings(state[field], label + ":" + field)).issubset(source):
                _fail(label + ":" + field + ":outside_source_options")
        _string(state["selected_option_id"], label + ":selected_option_id", empty=True)
        record_flags = {
            "stakeholders": ("appeal_right",),
            "veto_records": ("validated",), "validated_veto_records": ("validated",),
            "unvalidated_veto_records": ("validated",),
            "aggregate_records": ("validated_veto_present", "broadly_acceptable"),
            "ranked_aggregates": ("validated_veto_present", "broadly_acceptable"),
            "appeal_history": ("protected_boundary_claimed", "source_inconsistency_claimed", "material", "future_only", "rewrites_prior_decision"),
        }
        for appeal in _list(state["appeal_history"], label + ":appeal_history"):
            _object(appeal, label + ":appeal")
            if appeal.get("future_only") is not True or appeal.get("rewrites_prior_decision") is not False:
                _fail(label + ":appeal_boundary_invalid")
        for field in ("veto_records", "validated_veto_records", "unvalidated_veto_records"):
            for veto in _list(state[field], label + ":" + field):
                if _object(veto, label + ":veto").get("raw_veto_grants_authority") is not False:
                    _fail(label + ":raw_veto_authority_boundary_invalid")
        for stakeholder in _list(state["stakeholders"], label + ":stakeholders"):
            stakeholder = _object(stakeholder, label + ":stakeholder")
            for veto in _list(_required(stakeholder, "veto", label + ":stakeholder"), label + ":veto"):
                veto = _object(veto, label + ":veto")
                if veto.get("raw_veto_grants_authority") is not False or veto.get("validated") is not False:
                    _fail(label + ":raw_veto_boundary_invalid")
        explanation = _object(state["explanation"], label + ":explanation")
        if explanation:
            for flag in ("explanation_not_truth", "explanation_not_moral_worth"):
                if _required(explanation, flag, label + ":explanation") is not True:
                    _fail(label + ":explanation_boundary_invalid")
    else:
        for field in ("source_retained_alternative_ids", "endorsed_option_ids", "review_option_ids"):
            if not set(_strings(state[field], label + ":" + field)).issubset(source):
                _fail(label + ":" + field + ":outside_source_options")
        if state["route"] == "ENDORSE":
            if not selected or state["endorsed_option_ids"] != [selected]:
                _fail(label + ":endorsed_option_identity_mismatch")
        elif state["endorsed_option_ids"]:
            _fail(label + ":endorsement_route_mismatch")
        plurality = _object(state["plurality"], label + ":plurality")
        required = ("all_source_options_profiled", "retained_alternatives_preserved", "selected_identity_preserved",
                    "stakeholder_sections_preserved", "veto_and_appeal_history_preserved", "silent_substitution_detected")
        if set(plurality) != set(required):
            _fail(label + ":plurality_schema_mismatch")
        for field in required:
            _bool(plurality[field], label + ":plurality:" + field)
        for record in _list(state["false_harmony_records"], label + ":false_harmony_records"):
            if _object(record, label + ":false_harmony_record").get("smooth_surface_is_not_proof") is not True:
                _fail(label + ":false_harmony_boundary_invalid")
        record_flags = {
            "profiles": ("dissent_considered", "minority_preserved"),
            "wa_records": ("dissent_considered", "minority_preserved"),
            "false_harmony_records": ("confirmed_false_harmony", "suspected_false_harmony",
                                      "smooth_surface_is_not_proof", "minority_preserved", "dissent_considered"),
        }
    for field, flags in record_flags.items():
        for record in _list(state[field], label + ":" + field):
            record = _object(record, label + ":" + field + ":record")
            for flag in flags:
                _bool(_required(record, flag, label + ":" + field), label + ":" + field + ":" + flag)


def _record_bindings(binding: _Binding, native: _Native, state: dict[str, Any], label: str) -> None:
    position = binding.phases.index(state["current_phase"])
    if binding.stem == "plural":
        if position >= 1:
            if not state["stakeholders"]:
                _fail(label + ":registered_stakeholders_missing")
            if state["stakeholder_registry_digest"] != _digest(native.sha, state["stakeholders"], label + ":stakeholder_registry"):
                _fail(label + ":stakeholder_registry_digest_mismatch")
        return
    source_map = _object(state["source_option_digest_by_id"], label + ":source_option_digest_by_id")
    if set(source_map) != set(state["source_option_ids"]):
        _fail(label + ":source_option_digest_map_mismatch")
    for value in source_map.values():
        _string(value, label + ":source_option_digest")
    profiles = {}
    for profile in state["profiles"]:
        option_id = _string(_required(profile, "option_id", label + ":profile"), label + ":profile:option_id")
        if option_id not in source_map or profile.get("option_digest") != source_map[option_id]:
            _fail(label + ":profile_source_binding_mismatch")
        if option_id in profiles:
            _fail(label + ":profile_option_duplicate")
        supplied = _string(_required(profile, "wa_profile_digest", label + ":profile"), label + ":wa_profile_digest")
        expected = _digest(native.sha, {key: value for key, value in profile.items() if key != "wa_profile_digest"}, label + ":profile")
        if supplied != expected:
            _fail(label + ":profile_digest_mismatch")
        profiles[option_id] = profile
    if position >= 1 and set(profiles) != set(source_map):
        _fail(label + ":profiles_do_not_cover_source_options")
    for field, start in (("wa_records", 2), ("false_harmony_records", 3)):
        identifiers = []
        for record in state[field]:
            option_id = _string(_required(record, "option_id", label + ":" + field), label + ":record:option_id")
            if option_id not in profiles:
                _fail(label + ":record_option_not_profiled")
            identifiers.append(option_id)
            profile = profiles[option_id]
            fields = ("dissent_considered", "minority_preserved")
            if field == "wa_records":
                fields += ("option_digest", "wa_profile_digest")
            for key in fields:
                if not _same(_required(record, key, label + ":" + field), profile[key]):
                    _fail(label + ":" + field + ":profile_binding_mismatch:" + key)
        if len(identifiers) != len(set(identifiers)):
            _fail(label + ":record_option_duplicate")
        if position >= start and set(identifiers) != set(source_map):
            _fail(label + ":" + field + ":source_coverage_mismatch")


def _validate_state(binding: _Binding, native: _Native, state: dict[str, Any], label: str) -> str:
    stem = binding.stem
    common = ("version", stem + "_id", "lineage_id", "mission_contract_digest",
              "predecessor_" + stem + "_state_digest", stem + "_state_digest", "current_phase", "event_index",
              stem + "_version", binding.count, "updated_at_ms", "route", "pending_replan_activation",
              "latest_committed_" + stem + "_digest", "processed_event_digests", "event_history",
              stem + "_summaries", "non_authority", "boundary")
    for field in common + binding.required:
        _required(state, field, label)
    _validate_native(native, state, label)
    if state["version"] != native.state_version:
        _fail(label + ":version_mismatch")
    for field in (stem + "_id", "lineage_id", "mission_contract_digest", "current_phase", "route", "source_route"):
        _string(state[field], label + ":" + field)
    for field in ("event_index", stem + "_version", binding.count, "updated_at_ms"):
        _natural(state[field], label + ":" + field)
    _bool(state["pending_replan_activation"], label + ":pending_replan_activation")
    _flags(state["non_authority"], native.non_authority, label + ":non_authority")
    _flags(state["boundary"], native.boundary, label + ":boundary")
    for field in (("thresholds", "weights") if stem == "wa" else ("thresholds",)):
        for value in _object(state[field], label + ":" + field).values():
            if type(value) not in (int, float):
                _fail(label + ":" + field + ":exact_number_required")
    _state_flags_and_options(binding, state, label)
    _record_bindings(binding, native, state, label)
    _state_history(binding, native, state, label)
    digest = _digest(native.state_digest, state, label)
    if _string(state[stem + "_state_digest"], label + ":cached_state_digest") != digest:
        _fail(label + ":state_digest_mismatch")
    return digest


def _successful_event(binding: _Binding, native: _Native, before: dict[str, Any], event: dict[str, Any]) -> None:
    stem = binding.stem
    for field in ("event_index", "created_at_ms"):
        _natural(_required(event, field, "event"), "event:" + field)
    if _required(event, "version", "event") != native.event_version:
        _fail("event:version_mismatch")
    for field in (stem + "_id", "lineage_id"):
        if _string(_required(event, field, "event"), "event:" + field) != before[field]:
            _fail("event:" + field + ":identity_binding_mismatch")
    for field in ("artifact_digest", "expected_" + stem + "_state_digest", stem + "_event_digest"):
        _string(_required(event, field, "event"), "event:" + field)
    if event[stem + "_event_digest"] != _digest(native.event_digest, event, "event"):
        _fail("event:body_digest_mismatch")
    source = _string(_required(event, "source_phase", "event"), "event:source_phase")
    target = _string(_required(event, "target_phase", "event"), "event:target_phase")
    if source not in binding.phases[:-1] or target != binding.phases[binding.phases.index(source) + 1]:
        _fail("event:phase_order_invalid")
    if event["event_index"] != binding.phases.index(target):
        _fail("event:phase_index_mismatch")
    _flags(_required(event, "non_authority", "event"), native.non_authority, "event:non_authority")
    payload = _object(_required(event, "payload", "event"), "event:payload")
    if target == "adjudicate":
        _bool(payload.get("handover_required", False), "event:payload:handover_required")
    flag_records = {
        "register_stakeholders": ("stakeholders", ("appeal_right",)),
        "profile": ("profiles", ("dissent_considered", "minority_preserved")),
        "appeal_window": ("appeals", ("protected_boundary_claimed", "source_inconsistency_claimed")),
    }.get(target)
    if flag_records:
        field, flags = flag_records
        records = payload.get(field, []) if field == "appeals" else _required(payload, field, "event:payload")
        for record in _list(records, "event:payload:" + field):
            record = _object(record, "event:payload:" + field + ":record")
            for flag in flags:
                _bool(_required(record, flag, "event:payload:" + field), "event:payload:" + flag)
    if target == "commit":
        flags = {"future_only": True, "memory_overwrite": False}
        flags.update({"plural_decision_not_execution": True, "consensus_not_truth": True} if stem == "plural"
                     else {"wa_not_truth": True, "wa_not_execution": True, "wa_not_moral_veto": True})
        for field, expected in flags.items():
            if _required(payload, field, "event:payload") is not expected:
                _fail("event:payload:" + field + ":exact_boolean_boundary_mismatch")
        if _required(payload, "activation_boundary", "event:payload") != "mission_replan_only":
            _fail("event:payload:activation_boundary_mismatch")
        _flags(_required(payload, "non_authority", "event:payload"), native.non_authority, "event:payload:non_authority")


def _append(old: Any, new: Any, count: int, label: str) -> None:
    old, new = _list(old, label), _list(new, label)
    if len(new) != len(old) + count or not _same(new[:len(old)], old):
        _fail(label + ":not_exact_append")


def _phase_bindings(binding: _Binding, native: _Native, before: dict[str, Any],
                    event: dict[str, Any], after: dict[str, Any]) -> None:
    target, payload = event["target_phase"], event["payload"]
    receipt = {
        "register_stakeholders": ("source_binding_receipt_digest", "source_binding_receipt_digest"),
        "evaluate_plurality": ("plural_evaluation_receipt_digest", "evaluation_receipt_digest"),
        "validate_vetoes": ("veto_validation_receipt_digest", "veto_validation_receipt_digest"),
        "aggregate": ("aggregation_receipt_digest", "aggregation_receipt_digest"),
        "appeal_window": ("appeal_window_receipt_digest", "appeal_window_receipt_digest"),
        "adjudicate": ("adjudication_rule_digest", "adjudication_rule_digest"),
        "evaluate": ("evaluation_receipt_digest", "evaluation_receipt_digest"),
        "false_harmony_check": ("false_harmony_receipt_digest", "false_harmony_receipt_digest"),
        "plurality_check": ("plurality_receipt_digest", "plurality_receipt_digest"),
        "gate": ("wa_gate_rule_digest", "wa_gate_rule_digest"),
    }.get(target)
    if receipt:
        state_field, event_field = receipt
        value = _string(_required(payload, event_field, "event:payload"), "event:payload:" + event_field)
        if target in ("register_stakeholders", "validate_vetoes", "appeal_window"):
            value = _string(value.strip(), "event:payload:" + event_field)
        if _required(after, state_field, "post_state") != value:
            _fail("post_state:" + state_field + ":event_payload_binding_mismatch")
    if target == "register_stakeholders":
        for field in ("source_decision_state_digest", "source_decision_basis_digest"):
            if _required(payload, field, "event:payload") != before[field]:
                _fail("event:payload:" + field + ":source_binding_mismatch")
        if after["stakeholder_registry_digest"] != _digest(native.sha, after["stakeholders"], "stakeholder_registry"):
            _fail("post_state:stakeholder_registry_digest_mismatch")
        normalized = [_normalized(native.normalize_record, "stakeholder", record)
                      for record in _list(_required(payload, "stakeholders", "event:payload"), "event:payload:stakeholders")]
        if not _same(after["stakeholders"], normalized):
            _fail("transition:stakeholders:normalized_event_binding_mismatch")
    elif target == "profile":
        normalized = [_normalized(native.normalize_record, "profile", before, record)
                      for record in _list(_required(payload, "profiles", "event:payload"), "event:payload:profiles")]
        if not _same(after["profiles"], normalized):
            _fail("transition:profiles:normalized_event_binding_mismatch")
    elif target == "validate_vetoes":
        # The native validation phase copies raw claims without dropping them,
        # annotates these four binding conditions, then partitions the records.
        # This checks claim preservation and logical bindings, not utility math.
        mission_bound = [_string(value.strip(), "event:mission_bound_constraint_digest")
                         for value in _strings(payload.get("mission_bound_constraint_digests", []),
                                               "event:mission_bound_constraint_digests")]
        if len(mission_bound) != len(set(mission_bound)):
            _fail("event:mission_bound_constraint_digests:normalized_duplicate")
        records = []
        for stakeholder in before["stakeholders"]:
            for raw in stakeholder["veto"]:
                row = _json(raw, "veto")
                reasons = []
                if row["option_id"] not in before["source_option_ids"]:
                    reasons.append("veto_option_outside_source_field")
                if row["constraint_digest"] not in mission_bound:
                    reasons.append("veto_constraint_not_mission_bound")
                if row["constraint_digest"] not in stakeholder["protected_constraint_digests"]:
                    reasons.append("veto_constraint_not_stakeholder_protected")
                if not row["evidence_digest"]:
                    reasons.append("veto_evidence_missing")
                row["validation_reasons"] = reasons
                row["validated"] = not reasons
                records.append(row)
        validated = [row for row in records if row["validated"]]
        expected = {
            "veto_records": records,
            "validated_veto_records": validated,
            "unvalidated_veto_records": [row for row in records if not row["validated"]],
            "veto_excluded_option_ids": sorted({row["option_id"] for row in validated}),
        }
        for field, value in expected.items():
            if not _same(after[field], value):
                _fail("transition:" + field + ":source_claim_binding_mismatch")
    elif target == "explain":
        receipt_value = _string(_required(payload, "explanation_receipt_digest", "event:payload"), "event:payload:explanation_receipt_digest").strip()
        if after["explanation"].get("explanation_receipt_digest") != _string(receipt_value, "explanation_receipt_digest"):
            _fail("post_state:explanation_receipt_binding_mismatch")
    elif target == "appeal_window":
        incoming = _list(payload.get("appeals", []), "event:payload:appeals")
        _append(before["appeal_history"], after["appeal_history"], len(incoming), "transition:appeal_history")
        normalized = [_normalized(native.normalize_appeal, "appeal", raw, before) for raw in incoming]
        if not _same(after["appeal_history"][len(before["appeal_history"]):], normalized):
            _fail("transition:appeal_history:normalized_event_binding_mismatch")


def _applied(binding: _Binding, native: _Native, before: dict[str, Any],
             event: dict[str, Any], after: dict[str, Any]) -> None:
    stem = binding.stem
    state_key = stem + "_state_digest"
    if event["source_phase"] != before["current_phase"] or after["current_phase"] != event["target_phase"]:
        _fail("transition:phase_binding_mismatch")
    if event["event_index"] != before["event_index"] + 1 or after["event_index"] != event["event_index"]:
        _fail("transition:event_index_not_exact_successor")
    if event["created_at_ms"] < before["updated_at_ms"] or after["updated_at_ms"] != event["created_at_ms"]:
        _fail("transition:time_binding_mismatch")
    if event["expected_" + state_key] != before[state_key] or after["predecessor_" + state_key] != before[state_key]:
        _fail("transition:predecessor_state_binding_mismatch")
    writes = dict(binding.writes)[event["target_phase"]]
    mutable = set(writes) | {state_key, "predecessor_" + state_key, "current_phase", "event_index",
                             "updated_at_ms", "processed_event_digests", "event_history"}
    if event["target_phase"] == "commit":
        mutable.update((stem + "_version", binding.count, "latest_committed_" + stem + "_digest", stem + "_summaries"))
        for field in (stem + "_version", binding.count):
            if after[field] != before[field] + 1:
                _fail("transition:" + field + ":not_exact_successor")
        _append(before[stem + "_summaries"], after[stem + "_summaries"], 1, "transition:summaries")
    for field in (set(before) | set(after)) - mutable:
        if field not in before or field not in after or not _same(before[field], after[field]):
            _fail("post_state:" + field + ":outside_phase_write_set")
    for field in ("event_history", "processed_event_digests"):
        _append(before[field], after[field], 1, "transition:" + field)
    if not _same(after["event_history"][-1], _row(binding, event)):
        _fail("transition:event_history:appended_row_event_binding_mismatch")
    if after["processed_event_digests"][-1] != event[stem + "_event_digest"]:
        _fail("transition:processed_event_digests:appended_event_mismatch")
    if event[stem + "_event_digest"] in before["processed_event_digests"]:
        _fail("transition:applied_event_already_processed")
    _phase_bindings(binding, native, before, event, after)


def checked_apply_mediator_event(os_name: str, state: Any, event: Any) -> dict[str, Any]:
    """Return one native result only after this structural boundary passes.

    Native APPLIED/REPLAYED/REJECTED statuses are preserved. REPLAYED may refer
    to an old predecessor and phase; its original body must hash to an existing
    processed digest and matching history row. REJECTED and REPLAYED must leave
    state canonically unchanged. Missing prerequisites raise NO_DATA; violated
    or malformed data raise BLOCKED. Persist only after this function returns.
    """
    if type(os_name) is not str or os_name not in _BINDINGS:
        _fail("os_name:unsupported")
    binding = _BINDINGS[os_name]
    native = _native(binding)
    before = _json(state, "state", object_required=True)
    observed_event = _json(event, "event", object_required=True)
    before_digest = _validate_state(binding, native, before, "pre_state")
    state_copy, event_copy = _json(before, "state"), _json(observed_event, "event")
    try:
        raw_result = native.apply(state_copy, event_copy)
    except Exception as exc:
        raise MediatorTransitionError(BLOCKED, ("original_apply_raised:" + type(exc).__name__,)) from exc
    if not _same(_json(state_copy, "original_state_argument"), before):
        _fail("original_state_argument_mutated")
    if not _same(_json(event_copy, "original_event_argument"), observed_event):
        _fail("original_event_argument_mutated")
    result = _json(raw_result, "result", object_required=True)
    stem = binding.stem
    event_key, state_key = stem + "_event_digest", stem + "_state_digest"
    result_key = stem + "_apply_result_digest"
    required = {"version", "status", event_key, "predecessor_" + state_key,
                "result_" + state_key, "state", "errors", result_key}
    missing, extra = required - set(result), set(result) - required
    if extra:
        _fail("result:envelope_extra_fields:" + ",".join(sorted(extra)))
    if missing:
        _fail("result:envelope_missing_fields:" + ",".join(sorted(missing)), status=NO_DATA)
    if _string(result["version"], "result:version") != native.result_version:
        _fail("result:version_mismatch")
    status = result["status"]
    if type(status) is not str or status not in ("APPLIED", "REPLAYED", "REJECTED"):
        _fail("result:status_invalid")
    errors = result["errors"]
    if type(errors) is not list or any(type(error) is not str for error in errors):
        _fail("result:errors_string_list_required")
    if status in ("APPLIED", "REPLAYED") and errors:
        _fail("result:successful_status_has_errors")
    if status == "REJECTED" and not errors:
        _fail("result:rejected_status_missing_errors")
    after = _json(result["state"], "post_state", object_required=True)
    after_digest = _validate_state(binding, native, after, "post_state")
    for field, expected in {
        # Preserve original stringification even for malformed rejected input.
        event_key: str(observed_event.get(event_key, "")),
        "predecessor_" + state_key: before_digest,
        "result_" + state_key: after_digest,
        result_key: _digest(native.result_digest, result, "result"),
    }.items():
        if type(result[field]) is not str or result[field] != expected:
            _fail("result:" + field + ":binding_mismatch")
    if status in ("APPLIED", "REPLAYED"):
        _successful_event(binding, native, before, observed_event)
    if status == "APPLIED":
        _applied(binding, native, before, observed_event, after)
    else:
        if not _same(before, after):
            _fail("transition:non_applied_state_not_unchanged")
        if status == "REPLAYED":
            if observed_event[event_key] not in before["processed_event_digests"]:
                _fail("transition:replayed_event_not_previously_processed")
            position = before["processed_event_digests"].index(observed_event[event_key])
            if not _same(before["event_history"][position], _row(binding, observed_event)):
                _fail("transition:replayed_history_event_binding_mismatch")
    return result
