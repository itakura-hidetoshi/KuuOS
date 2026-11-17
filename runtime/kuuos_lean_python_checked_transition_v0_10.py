"""Fail-closed adapter around six original pure event kernels (v0.10).

The original kernel is called once, on defensive finite-JSON copies. Its
unchanged result is returned only after native schema/digest checks and the
existing structural Lean/Python projection both pass. These are Python checks,
not a Lean refinement proof, authenticated evidence, or execution authority.

The Lean ``*Phase_next_deterministic`` theorems concern their explicit ``next``
hypotheses, and ``*EventIndex_strict`` concerns the defined Nat append. Neither
proves these Python functions. In particular ActOS host work can already have
happened in ``build_authorized_invoke_event`` before this adapter is called.
This boundary neither invokes a host nor grants permission for that earlier work.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from types import MappingProxyType
from typing import Any, NoReturn

try:
    from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
        audit_core_state, audit_core_transition,
    )
except ImportError:
    audit_core_state = audit_core_transition = None

try:
    from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
        _finite_json, _fingerprint,
    )
except ImportError:
    _finite_json = _fingerprint = None


VERSION = "kuuos_lean_python_checked_transition_v0_10"
SOURCE_MAIN = "8b855cf1f1c2296dbe0d8d3057cd391729d572d1"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"


class CheckedTransitionError(RuntimeError):
    """A missing prerequisite or a violated Python boundary; never a success."""

    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status = status
        self.issues = tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


@dataclass(frozen=True)
class _Binding:
    stem: str
    kernel: str
    types: str
    immutable: tuple[str, ...]


# Literal module names are selected only by this fixed map. No callable or
# import name is accepted from the caller. Lists below record fields which the
# existing initial constructors bind and the original phase functions preserve.
# Act's source_supervisor_bundle_digest is deliberately absent: authorize sets it.
_BINDINGS = MappingProxyType({
    "DecisionOS": _Binding(
        "decision", "runtime.kuuos_decision_os_kernel_v0_1",
        "runtime.kuuos_decision_os_types_v0_1",
        ("mission_state_digest", "source_belief_receipt_digest", "decision_context_digest",
         "decision_budget", "weights", "thresholds"),
    ),
    "PlanOS": _Binding(
        "plan", "runtime.kuuos_plan_os_kernel_v0_1",
        "runtime.kuuos_plan_os_types_v0_1",
        ("source_wa_id", "source_wa_state_digest", "source_committed_wa_digest",
         "source_wa_basis_digest", "source_plural_decision_basis_digest",
         "source_decision_basis_digest", "source_wa_route", "source_endorsed_option_ids",
         "source_review_option_ids", "source_selected_option_id", "source_option_ids",
         "source_retained_alternative_ids", "source_stakeholder_registry_digest",
         "source_utility_records_digest", "source_veto_records_digest", "source_appeal_history_digest",
         "replan_activation_receipt_digest", "replan_receipt_digest", "mission_cycle_state_digest",
         "next_plan_basis_digest", "plan_budget", "maximum_step_risk", "route"),
    ),
    "ActOS": _Binding(
        "act", "runtime.kuuos_act_os_kernel_v0_1", "runtime.kuuos_act_os_types_v0_1",
        ("source_plan_id", "source_plan_state_digest", "source_committed_plan_digest",
         "source_plan_basis_digest", "plan_activation_receipt_digest", "source_wa_basis_digest"),
    ),
    "ObserveOS": _Binding(
        "observe", "runtime.kuuos_observe_os_kernel_v0_1",
        "runtime.kuuos_observe_os_types_v0_1",
        ("source_act_id", "source_act_state_digest", "source_act_version", "source_act_updated_at_ms",
         "host_receipt_digest", "host_invocation_digest", "selected_step_id", "selected_step_digest",
         "operation_id", "expected_observation_digest", "verification_criterion_digest"),
    ),
    "VerifyOS": _Binding(
        "verify", "runtime.kuuos_verify_os_kernel_v0_1", "runtime.kuuos_verify_os_types_v0_1",
        ("source_observe_id", "source_observe_state_digest", "source_observe_version",
         "source_observe_updated_at_ms", "source_observation_route",
         "source_observation_debt_discharged", "source_reobservation_required", "source_act_state_digest",
         "host_receipt_digest", "host_invocation_digest", "expected_observation_digest",
         "verification_criterion_digest", "evidence_packet_digest", "quality_report_digest",
         "comparison_receipt_digest"),
    ),
    "LearnOS": _Binding(
        "learn", "runtime.kuuos_learn_os_kernel_v0_1", "runtime.kuuos_learn_os_types_v0_1",
        ("source_verify_id", "source_verify_state_digest", "source_verify_version",
         "source_verify_updated_at_ms", "source_verification_route", "source_verification_evidence_digest",
         "source_observe_state_digest", "source_act_state_digest", "source_challenge_packet_digest",
         "source_counterevidence_digests", "source_counterevidence_digest", "source_unresolved_conflict",
         "source_reobservation_required", "source_corrective_action_required", "verification_criterion_digest",
         "criterion_packet_digest", "corroboration_report_digest", "adjudication_receipt_digest"),
    ),
})
CHECKED_OS_NAMES = tuple(_BINDINGS)


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise CheckedTransitionError(status, (issue,))


def _json(value: Any, label: str, *, object_required: bool = False) -> Any:
    if object_required and value is None:
        _fail(label + ":missing", status=NO_DATA)
    try:
        copied = _finite_json(value)
    except Exception as exc:
        _fail(f"{label}:invalid_json:{type(exc).__name__}:{exc}")
    if object_required and type(copied) is not dict:
        _fail(label + ":json_object_required")
    return copied


def _required(value: dict[str, Any], key: str, label: str) -> Any:
    if key not in value:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return value[key]


def _same(left: Any, right: Any) -> bool:
    # Python equality equates True, 1, and 1.0; canonical JSON preserves types.
    return _fingerprint(left) == _fingerprint(right)


def _function(module: Any, name: str) -> Any:
    function = getattr(module, name, None)
    if not callable(function):
        _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
    return function


def _native(binding: _Binding) -> tuple[Any, str, Any, Any, Any]:
    for name, function in (
        ("audit_core_state", audit_core_state), ("audit_core_transition", audit_core_transition),
        ("_finite_json", _finite_json), ("_fingerprint", _fingerprint),
    ):
        if not callable(function):
            _fail("prerequisite:" + name + ":unavailable", status=NO_DATA)
    try:
        kernel = import_module(binding.kernel)
        types = import_module(binding.types)
    except ImportError as exc:
        _fail("prerequisite:runtime_dependency_unavailable:" + type(exc).__name__, status=NO_DATA)
    except Exception as exc:
        _fail("prerequisite:runtime_dependency_raised:" + type(exc).__name__)
    apply = _function(kernel, f"apply_{binding.stem}_event")
    _function(kernel, f"validate_{binding.stem}_state")
    version = getattr(types, "APPLY_RESULT_VERSION", None)
    if version is None:
        _fail("prerequisite:APPLY_RESULT_VERSION:unavailable", status=NO_DATA)
    if type(version) is not str or not version:
        _fail("prerequisite:APPLY_RESULT_VERSION:invalid")
    prefix = "plan_" if binding.stem == "plan" else ""
    return (apply, version, _function(types, prefix + "state_digest"),
            _function(types, prefix + "event_digest"), _function(types, prefix + "apply_result_digest"))


def _digest(function: Any, value: dict[str, Any], label: str) -> str:
    try:
        digest = function(value)
    except Exception as exc:
        _fail(label + ":native_digest_raised:" + type(exc).__name__)
    if type(digest) is not str or not digest:
        _fail(label + ":native_digest_invalid")
    return digest


def _audit(label: str, function: Any, *arguments: Any) -> None:
    # Auditors receive their own copies too; an accidental mutating validator
    # cannot change the baseline subsequently given to the pure event kernel.
    copied = [_json(value, label) for value in arguments]
    fingerprints = [_fingerprint(value) for value in copied]
    try:
        audit = function(*copied)
    except Exception as exc:
        _fail(label + ":audit_raised:" + type(exc).__name__)
    for value, fingerprint in zip(copied, fingerprints):
        if _fingerprint(_json(value, label)) != fingerprint:
            _fail(label + ":audit_argument_mutated")
    status = getattr(audit, "status", None)
    issues = getattr(audit, "issues", None)
    if type(status) is not str or type(issues) is not tuple or any(type(item) is not str for item in issues):
        _fail(label + ":audit_contract_invalid")
    if status == "RUNTIME_CHECK_PASSED" and not issues:
        return
    outcome = NO_DATA if status == NO_DATA else BLOCKED
    raise CheckedTransitionError(outcome, tuple(label + ":" + issue for issue in issues)
                                 or (label + ":audit_did_not_pass:" + status,))


def _successful_event(binding: _Binding, before: dict[str, Any], event: dict[str, Any],
                      event_digest: Any) -> None:
    for field in ("event_index", "created_at_ms"):
        value = _required(event, field, "event")
        if type(value) is not int or value < 0:
            _fail("event:" + field + ":exact_natural_required")
    key = binding.stem + "_event_digest"
    if _required(event, key, "event") != _digest(event_digest, event, key):
        _fail("event:" + key + ":body_digest_mismatch")
    for field in (binding.stem + "_id", "lineage_id"):
        if not _same(_required(event, field, "event"), _required(before, field, "state")):
            _fail("event:" + field + ":binding_mismatch")


def _applied(binding: _Binding, before: dict[str, Any], event: dict[str, Any],
             after: dict[str, Any]) -> None:
    stem = binding.stem
    for field in ("version", stem + "_id", "lineage_id", "mission_contract_digest") + binding.immutable:
        if not _same(_required(before, field, "pre_state"), _required(after, field, "post_state")):
            _fail("post_state:" + field + ":immutable_binding_changed")
    expected_key = "expected_" + stem + "_state_digest"
    if _required(event, expected_key, "event") != before[stem + "_state_digest"]:
        _fail("event:" + expected_key + ":binding_mismatch")
    if not _same(_required(after, "updated_at_ms", "post_state"), event["created_at_ms"]):
        _fail("post_state:updated_at_ms:event_binding_mismatch")
    for field in ("event_history", "processed_event_digests"):
        old = _required(before, field, "pre_state")
        new = _required(after, field, "post_state")
        if type(old) is not list or type(new) is not list:
            _fail("transition:" + field + ":list_required")
        if len(new) != len(old) + 1 or not _same(new[:-1], old):
            _fail("transition:" + field + ":not_exact_append")
    row = {field: _required(event, field, "event") for field in (
        "event_index", "source_phase", "target_phase", "artifact_digest",
        stem + "_event_digest", "created_at_ms",
    )}
    if not _same(after["event_history"][-1], row):
        _fail("transition:event_history:appended_row_event_binding_mismatch")
    if not _same(after["processed_event_digests"][-1], event[stem + "_event_digest"]):
        _fail("transition:processed_event_digests:appended_event_binding_mismatch")


def checked_apply_event(os_name: str, state: Any, event: Any) -> dict[str, Any]:
    """Apply one original event and return its native envelope after all checks.

    ``REJECTED`` and ``REPLAYED`` remain their original statuses and must preserve
    the exact input state. Missing prerequisites raise ``NO_DATA``; malformed or
    violating data raise ``BLOCKED``. No store write, host invocation, certificate,
    or permission is produced here. Callers must perform any persistence only
    after this function returns successfully.
    """
    if type(os_name) is not str or os_name not in _BINDINGS:
        _fail("os_name:unsupported")
    binding = _BINDINGS[os_name]
    apply, version, state_digest, event_digest, result_digest = _native(binding)
    before = _json(state, "state", object_required=True)
    observed_event = _json(event, "event", object_required=True)
    _audit("pre_state", audit_core_state, os_name, before)
    state_key = binding.stem + "_state_digest"
    before_digest = _digest(state_digest, before, "pre_state:" + state_key)
    if _required(before, state_key, "pre_state") != before_digest:
        _fail("pre_state:" + state_key + ":digest_mismatch")

    kernel_state = _json(before, "state")
    kernel_event = _json(observed_event, "event")
    try:
        raw_result = apply(kernel_state, kernel_event)
    except Exception as exc:
        raise CheckedTransitionError(BLOCKED, ("original_apply_raised:" + type(exc).__name__,)) from exc
    if not _same(_json(kernel_state, "original_state_argument"), before):
        _fail("original_state_argument_mutated")
    if not _same(_json(kernel_event, "original_event_argument"), observed_event):
        _fail("original_event_argument_mutated")
    result = _json(raw_result, "result", object_required=True)
    event_key = binding.stem + "_event_digest"
    predecessor_key = "predecessor_" + state_key
    result_state_key = "result_" + state_key
    result_key = binding.stem + "_apply_result_digest"
    required_keys = {"version", "status", event_key, predecessor_key,
                     result_state_key, "state", "errors", result_key}
    extra = set(result) - required_keys
    missing = required_keys - set(result)
    if extra:
        _fail("result:envelope_extra_fields:" + ",".join(sorted(extra)))
    if missing:
        _fail("result:envelope_missing_fields:" + ",".join(sorted(missing)), status=NO_DATA)
    if type(result["version"]) is not str or result["version"] != version:
        _fail("result:version_mismatch")
    status = result["status"]
    # v0.1's transition audit does not reject a present null status. The exact
    # enum check is therefore mandatory before using that structural audit.
    if type(status) is not str or status not in ("APPLIED", "REPLAYED", "REJECTED"):
        _fail("result:status_invalid")
    errors = result["errors"]
    if type(errors) is not list or any(type(error) is not str for error in errors):
        _fail("result:errors_string_list_required")
    if status in ("APPLIED", "REPLAYED") and errors:
        _fail("result:successful_status_has_errors")
    after = _json(result["state"], "post_state", object_required=True)
    after_digest = _digest(state_digest, after, "post_state:" + state_key)
    if _required(after, state_key, "post_state") != after_digest:
        _fail("post_state:" + state_key + ":digest_mismatch")
    expected_digests = {
        # Native kernels stringify this field even for malformed rejected
        # events. Preserve that rejection convention without accepting its
        # digest as a claim about the event body on a successful status.
        event_key: str(observed_event.get(event_key, "")),
        predecessor_key: before_digest,
        result_state_key: after_digest,
        result_key: _digest(result_digest, result, result_key),
    }
    for field, expected in expected_digests.items():
        if type(result[field]) is not str or result[field] != expected:
            _fail("result:" + field + ":binding_mismatch")
    if status in ("APPLIED", "REPLAYED"):
        _successful_event(binding, before, observed_event, event_digest)
    if status == "APPLIED":
        _applied(binding, before, observed_event, after)
    else:
        if not _same(after, before):
            _fail("transition:non_applied_state_not_unchanged")
        if status == "REPLAYED":
            processed = _required(before, "processed_event_digests", "pre_state")
            if type(processed) is not list or observed_event[event_key] not in processed:
                _fail("transition:replayed_event_not_previously_processed")
    # This invokes the native validator as well as the original authority and
    # boundary projection, independently of the apply result's own checksum.
    _audit("post_state", audit_core_state, os_name, after)
    _audit("transition", audit_core_transition, os_name, before, observed_event, result)
    return result
