"""Bind Wa profile digests and source projections to a supplied committed Plural witness.

A finite JSON copy of the committed Plural state is checked locally and its
19 projected fields are compared with the Wa state before and after exactly
one unchanged v0.15 adapter call. Stored normalized profile digest and exact
schema are checked without invoking the native profile normalizer.

A supplied source snapshot is NOT an external signature; the selected native
fixture obtains it from the local Plural store recovery. This is not proof of
the source's truth, external issuer, global history or Lean/Python refinement.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any, NoReturn

from runtime import kuuos_lean_python_wa_evaluation_guard_v0_15 as prior
from runtime.kuuos_decision_os_plural_kernel_v0_2 import validate_plural_state
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint

VERSION = "kuuos_lean_python_wa_profile_source_guard_v0_16"
SOURCE_MAIN = "9bbd82a95a579a8091a1cb5d7e7f7b92eb254924"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"

_PHASES = ("bind", "profile", "evaluate", "false_harmony_check",
           "plurality_check", "gate", "commit")
_PROFILE_FIELDS = (
    "option_id", "option_digest", "positive_intervals", "alert_intervals",
    "dissent_considered", "minority_preserved",
    "dissent_evidence_digests", "minority_stakeholder_digests",
    "dialogue_receipt_digest", "indra_network_receipt_digest",
    "wa_profile_digest",
)
_DIRECT_SOURCE = {
    "lineage_id": "lineage_id",
    "source_plural_id": "plural_id",
    "source_plural_state_digest": "plural_state_digest",
    "source_committed_plural_digest": "latest_committed_plural_digest",
    "source_plural_decision_basis_digest": "plural_decision_basis_digest",
    "source_decision_basis_digest": "source_decision_basis_digest",
    "source_committed_decision_digest": "source_committed_decision_digest",
    "mission_contract_digest": "mission_contract_digest",
    "source_route": "route",
    "source_selected_option_id": "selected_option_id",
    "source_option_ids": "source_option_ids",
    "source_retained_alternative_ids": "retained_alternative_ids",
    "source_options_digest": "source_options_digest",
    "source_stakeholder_registry_digest": "stakeholder_registry_digest",
}
_HASHED_SOURCE = {
    "source_utility_records_digest": "utility_records",
    "source_veto_records_digest": "veto_records",
    "source_aggregate_records_digest": "aggregate_records",
    "source_appeal_history_digest": "appeal_history",
}


class WaProfileSourceBoundaryError(RuntimeError):
    """Missing witness/profile input, or a locally incompatible typed projection."""

    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise WaProfileSourceBoundaryError(status, (issue,))


def _required(value: dict[str, Any], key: str, label: str) -> Any:
    if key not in value:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return value[key]


def _obj(value: Any, label: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail(label + ":exact_object_required")
    return value


def _lst(value: Any, label: str) -> list[Any]:
    if type(value) is not list:
        _fail(label + ":exact_list_required")
    return value


def _txt(value: Any, label: str) -> str:
    if type(value) is not str or not value:
        _fail(label + ":nonempty_string_required")
    return value


def _flag(value: Any, label: str) -> bool:
    if type(value) is not bool:
        _fail(label + ":exact_bool_required")
    return value


def _copy(value: Any, label: str, *, object_required: bool = False) -> Any:
    if value is None and object_required:
        _fail(label + ":missing", status=NO_DATA)
    try:
        copied = _finite_json(value)
    except Exception as exc:
        _fail(label + ":invalid_finite_json:" + type(exc).__name__)
    if object_required:
        _obj(copied, label)
    return copied


def _same(left: Any, right: Any) -> bool:
    return _fingerprint(left) == _fingerprint(right)


def _validate_source(source: dict[str, Any]) -> None:
    if _required(source, "current_phase", "source_plural") != "commit":
        _fail("source_plural:not_committed")
    supplied_digest = _required(source, "plural_state_digest", "source_plural")
    if type(supplied_digest) is not str:
        _fail("source_plural:state_digest_type_invalid")
    content = {key: value for key, value in source.items() if key != "plural_state_digest"}
    if supplied_digest != _fingerprint(content):
        _fail("source_plural:state_digest_not_canonical")
    frozen = _fingerprint(source)
    try:
        problems = validate_plural_state(source)
    except Exception as exc:
        _fail("source_plural:validator_raised:" + type(exc).__name__)
    if _fingerprint(source) != frozen:
        _fail("source_plural:validator_mutated")
    if type(problems) is not list or problems:
        _fail("source_plural:original_validator_rejected")


def _source_projection(source: dict[str, Any]) -> dict[str, Any]:
    expected = {target: _required(source, field, "source_plural")
                for target, field in _DIRECT_SOURCE.items()}
    opts = _lst(_required(source, "source_options", "source_plural"),
                "source_plural:source_options")
    inventory: dict[str, str] = {}
    for index, raw in enumerate(opts):
        label = f"source_plural:source_options[{index}]"
        option = _obj(raw, label)
        option_id = _txt(_required(option, "option_id", label), label + ":option_id")
        digest = _txt(_required(option, "option_digest", label), label + ":option_digest")
        if option_id in inventory:
            _fail(label + ":duplicate_option_id")
        inventory[option_id] = digest
    expected["source_option_digest_by_id"] = inventory
    for target, field in _HASHED_SOURCE.items():
        expected[target] = _fingerprint(_lst(_required(source, field, "source_plural"),
                                            "source_plural:" + field))
    return expected


def _profile_semantics(state: dict[str, Any], label: str) -> None:
    phase = _required(state, "current_phase", label)
    if type(phase) is not str or phase not in _PHASES:
        _fail(label + ":phase_invalid")
    profiles = _lst(_required(state, "profiles", label), label + ":profiles")
    if phase == "bind":
        if profiles:
            _fail(label + ":premature_profiles")
        return
    source_map = _obj(_required(state, "source_option_digest_by_id", label),
                      label + ":source_option_digest_by_id")
    if len(profiles) != len(source_map):
        _fail(label + ":profile_count_mismatch")
    seen: set[str] = set()
    for index, item in enumerate(profiles):
        path = f"{label}:profiles[{index}]"
        profile = _obj(item, path)
        if set(profile) != set(_PROFILE_FIELDS):
            missing = set(_PROFILE_FIELDS) - set(profile)
            if missing:
                _fail(path + ":profile_fields_missing:" + ",".join(sorted(missing)), status=NO_DATA)
            _fail(path + ":profile_fields_unexpected")
        option = _txt(profile["option_id"], path + ":option_id")
        if option in seen or option not in source_map:
            _fail(path + ":profile_option_source_mismatch")
        seen.add(option)
        if not _same(profile["option_digest"], source_map[option]):
            _fail(path + ":source_option_digest_mismatch")
        for name in ("dissent_considered", "minority_preserved"):
            _flag(profile[name], path + ":" + name)
        for name in ("dialogue_receipt_digest", "indra_network_receipt_digest"):
            _txt(profile[name], path + ":" + name)
        for name in ("dissent_evidence_digests", "minority_stakeholder_digests"):
            values = _lst(profile[name], path + ":" + name)
            entries = [_txt(value, path + ":" + name + ":item") for value in values]
            if len(entries) != len(set(entries)):
                _fail(path + ":" + name + ":duplicate")
        stored = _txt(profile["wa_profile_digest"], path + ":wa_profile_digest")
        preimage = {key: profile[key] for key in _PROFILE_FIELDS if key != "wa_profile_digest"}
        if stored != _fingerprint(preimage):
            _fail(path + ":profile_digest_binding_mismatch")
    if seen != set(source_map):
        _fail(label + ":profile_inventory_mismatch")


def _check_locally(state: dict[str, Any], source: dict[str, Any], label: str) -> None:
    _validate_source(source)
    expected = _source_projection(source)
    for field, value in expected.items():
        if not _same(_required(state, field, label), value):
            _fail(label + ":" + field + ":committed_plural_projection_mismatch")
    _profile_semantics(state, label)


def checked_apply_wa_profile_source_event(
    state: Any, event: Any, source_plural_state: Any,
) -> dict[str, Any]:
    """Exactly one unchanged v0.15 Wa transition with explicit local Plural witness.

    The source is supplied, not externally authenticated. In the selected
    native fixture it is obtained from actual local Plural ledger recovery.
    Invalid source/prestate blocks before prior Wa kernel/store work; an
    invalid poststate blocks before a guarded caller can append it.
    """
    for name, item in (("_finite_json", _finite_json), ("_fingerprint", _fingerprint),
                       ("validate_plural_state", validate_plural_state),
                       ("v015_adapter", prior.checked_apply_wa_evaluation_event)):
        if not callable(item):
            _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
    original = _copy(state, "state", object_required=True)
    observed = _copy(event, "event", object_required=True)
    witness = _copy(source_plural_state, "source_plural", object_required=True)
    _check_locally(original, witness, "pre_state")
    state_arg, event_arg = _copy(original, "state"), _copy(observed, "event")
    try:
        native = prior.checked_apply_wa_evaluation_event(state_arg, event_arg)
    except prior.WaEvaluationBoundaryError as exc:
        status = exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED
        raise WaProfileSourceBoundaryError(
            status, tuple("evaluation:" + issue for issue in exc.issues)
        ) from exc
    except Exception as exc:
        _fail("evaluation_adapter_raised:" + type(exc).__name__)
    if not _same(state_arg, original) or not _same(event_arg, observed):
        _fail("evaluation_adapter_arguments_mutated")
    result = _copy(native, "result", object_required=True)
    status = _required(result, "status", "result")
    if type(status) is not str or status not in ("APPLIED", "REPLAYED", "REJECTED"):
        _fail("result:status_invalid")
    _check_locally(_obj(_required(result, "state", "result"), "post_state"),
                   witness, "post_state")
    return result


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA",
    "WaProfileSourceBoundaryError", "checked_apply_wa_profile_source_event",
)
