"""A bounded pre-host gate for the original Act invocation builder.

This checks supplied snapshots before entering the original builder. It then
checks the returned event with v0.10, after a host call may already have had an
effect. It cannot roll effects back, authenticate issuers/executors, establish
the current state of an external store, or provide global exactly-once execution.
The registry is trusted code, separate from copied JSON. Passing this gate is
not a Lean proof, a new license, or execution/truth authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any, NoReturn

from runtime import kuuos_act_os_kernel_v0_1 as act
from runtime import kuuos_act_os_types_v0_1 as act_types
from runtime import kuuos_cooperative_execution_supervisor_types_v0_16 as supervisor
from runtime import kuuos_cooperative_host_adapter_types_v0_17 as host
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import next_step, validate_job
from runtime.kuuos_cooperative_execution_supervisor_step_precheck_v0_16 import precheck_step
from runtime.kuuos_cooperative_host_adapter_license_v0_17 import REQUIRED_PERMISSIONS, validate_host_license
from runtime.kuuos_cooperative_host_adapter_projection_v0_17 import project_host_work
from runtime.kuuos_cooperative_host_adapter_tick_v0_17 import _effective_policy, _projection_blockers
from runtime.kuuos_lean_python_checked_transition_v0_10 import CheckedTransitionError, checked_apply_event
from runtime.kuuos_lean_python_contract_bridge_v0_1 import audit_core_state
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
from runtime.kuuos_plan_os_kernel_v0_1 import _step_digest
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import TICKET_VERSION, ticket_digest

VERSION = "kuuos_lean_python_pre_host_guard_v0_11"
SOURCE_MAIN = "3da68503b6be1f6ef02d6100b730fa5ab9b92498"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"
_NO_CACHED_DIGEST = object()


class PreHostCheckError(ValueError):
    """Failure before or after dispatch to a possibly effectful original builder.

    ``host_call_attempted`` becomes true on dispatch into that builder. It is
    conservative: true does not prove an effect, and no rollback is promised.
    """

    def __init__(self, status: str, issues: tuple[str, ...], *, host_call_attempted: bool = False) -> None:
        self.status = status
        self.issues = tuple(issues)
        self.host_call_attempted = host_call_attempted
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise PreHostCheckError(status, (issue,))


def _required(packet: dict[str, Any], key: str, label: str) -> Any:
    if key not in packet:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return packet[key]


def _object(value: Any, label: str) -> dict[str, Any]:
    if value is None:
        _fail(label + ":missing", status=NO_DATA)
    if type(value) is not dict:
        _fail(label + ":exact_object_required")
    return value


def _string(value: Any, label: str, *, empty: bool = False) -> str:
    if type(value) is not str or (not empty and not value.strip()):
        _fail(label + ":exact_string_required")
    return value


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        _fail(label + ":exact_integer_required")
    return value


def _number(value: Any, label: str, *, unit: bool = False) -> Any:
    # The encompassing finite-JSON copy has already excluded NaN/infinities.
    if type(value) not in (int, float) or value < 0 or (unit and value > 1):
        _fail(label + ":finite_nonnegative_number_required")
    return value


def _boolean(value: Any, label: str) -> bool:
    if type(value) is not bool:
        _fail(label + ":exact_boolean_required")
    return value


def _strings(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    if type(value) is not list or (nonempty and not value):
        _fail(label + ":string_list_required")
    for item in value:
        _string(item, label)
    if len(value) != len(set(value)):
        _fail(label + ":duplicate_string")
    return value


def _flags(actual: Any, expected: dict[str, bool], label: str) -> None:
    actual = _object(actual, label)
    if set(actual) != set(expected):
        _fail(label + ":flag_inventory_mismatch")
    for key, expected_value in expected.items():
        if type(actual[key]) is not bool or actual[key] is not expected_value:
            _fail(label + ":" + key + ":flag_mismatch")


def _digest(packet: dict[str, Any], key: str, function: Any, label: str,
            cached: Any = _NO_CACHED_DIGEST, *, cached_key: str | None = None) -> str:
    value = _string(_required(packet, key, label), label + ":" + key)
    if value != function(packet):
        _fail(label + ":" + key + ":binding_mismatch")
    if cached is not _NO_CACHED_DIGEST:
        _string(cached, label + ":" + (cached_key or key))
        if value != cached:
            _fail(label + ":" + (cached_key or key) + ":cached_binding_mismatch")
    return value


def _same(left: Any, right: Any) -> bool:
    return _fingerprint(left) == _fingerprint(right)


def _selected_step(state: dict[str, Any]) -> None:
    step = _object(_required(state, "selected_step", "state"), "selected_step")
    _digest(step, "step_digest", _step_digest, "selected_step",
            _required(state, "selected_step_digest", "state"), cached_key="selected_step_digest")
    for name in ("step_id", "expected_observation_digest", "verification_criterion_digest"):
        value = _string(_required(step, name, "selected_step"), "selected_step:" + name)
        state_key = "selected_step_id" if name == "step_id" else name
        if value != _required(state, state_key, "state"):
            _fail("selected_step:" + name + ":state_binding_mismatch")
    if step.get("step_class") != "act_candidate":
        _fail("selected_step:act_candidate_required")
    for field in ("effectful", "requires_external_license", "requires_human_review"):
        _boolean(_required(step, field, "selected_step"), "selected_step:" + field)
    if step["effectful"] is not True:
        _fail("selected_step:effectful_required")
    _integer(_required(step, "rank", "selected_step"), "selected_step:rank")
    for field in ("estimated_cost", "estimated_risk", "reversibility"):
        _number(_required(step, field, "selected_step"), "selected_step:" + field,
                unit=field != "estimated_cost")
    for field in ("depends_on", "precondition_digests", "stop_condition_digests", "stakeholder_scope_digests"):
        _strings(_required(step, field, "selected_step"), "selected_step:" + field,
                 nonempty=field == "stop_condition_digests")


def _authorization_and_license(state: dict[str, Any], now: int) -> tuple[dict[str, Any], dict[str, Any]]:
    authorization = _object(_required(state, "step_authorization", "state"), "authorization")
    license_packet = _object(_required(state, "host_license", "state"), "license")
    _digest(authorization, "step_authorization_digest", act_types.authorization_digest,
            "authorization", _required(state, "step_authorization_digest", "state"))
    _digest(license_packet, "host_license_digest", host.license_digest,
            "license", _required(state, "host_license_digest", "state"))
    _flags(authorization.get("non_authority"), act_types.NON_AUTHORITY_FLAGS, "authorization:non_authority")
    for field in ("authorization_id", "act_phase_receipt_digest", "invocation_id", "host_job_id",
                  "host_step_id", "source_supervisor_bundle_digest", "host_license_digest"):
        _string(_required(authorization, field, "authorization"), "authorization:" + field)
    for field in ("human_approval_receipt_digest", "human_approver_id"):
        _string(_required(authorization, field, "authorization"), "authorization:" + field,
                empty=state["selected_step"]["requires_human_review"] is False)
    for field in ("issued_at_ms", "expires_at_ms"):
        _integer(_required(authorization, field, "authorization"), "authorization:" + field)
        _integer(_required(license_packet, field, "license"), "license:" + field)
    if authorization["expires_at_ms"] <= authorization["issued_at_ms"]:
        _fail("authorization:invalid_validity_interval")
    for field in ("single_use", "authorization_does_not_widen_license"):
        if _required(authorization, field, "authorization") is not True:
            _fail("authorization:" + field + ":true_required")
    _string(_required(license_packet, "license_id", "license"), "license:license_id")
    _strings(_required(license_packet, "operation_allowlist", "license"), "license:operation_allowlist", nonempty=True)
    for field in ("max_jobs_per_invocation", "max_steps_per_slice", "lease_duration_ms"):
        _integer(_required(license_packet, field, "license"), "license:" + field, minimum=1)
    if license_packet["max_jobs_per_invocation"] != 1:
        _fail("license:one_job_required")
    if license_packet["max_steps_per_slice"] > 25 or license_packet["lease_duration_ms"] > 86_400_000:
        _fail("license:constructor_bounds_exceeded")
    _number(_required(license_packet, "max_cost_per_slice", "license"), "license:max_cost_per_slice")
    _boolean(_required(license_packet, "in_place_bundle_write_allowed", "license"), "license:in_place_bundle_write_allowed")
    for field in REQUIRED_PERMISSIONS:
        if _required(license_packet, field, "license") is not True:
            _fail("license:" + field + ":true_required")
    if license_packet["expires_at_ms"] <= license_packet["issued_at_ms"]:
        _fail("license:invalid_validity_interval")
    # Native authorization validation is repeated at INVOCATION time, not only
    # at the earlier authorize event. It binds Plan/step/operation/license too.
    try:
        act._validate_authorization(state, authorization, license_packet, now)
    except Exception as exc:
        _fail("authorization:" + type(exc).__name__ + ":" + str(exc))
    if validate_host_license(license_packet, now_ms=now):
        _fail("license:native_validation_failed")
    if authorization["source_supervisor_bundle_digest"] != state.get("source_supervisor_bundle_digest"):
        _fail("authorization:source_supervisor_bundle_digest:state_binding_mismatch")
    return authorization, license_packet


_POLICY_BOOLEANS = frozenset((
    "background_worker_available", "background_handoff_enabled", "auto_background_on_budget_pause",
    "auto_background_on_external_wait", "auto_background_on_transient_error",
))
_POLICY_INTEGERS = frozenset((
    "max_steps_per_slice", "foreground_wait_threshold_ms", "external_recheck_after_ms",
    "retry_backoff_base_ms", "max_retry_backoff_ms", "max_retries",
))
_POLICY_NUMBERS = frozenset(("max_cost_per_slice", "cost_reserve_units"))


def _policy(policy: dict[str, Any], license_packet: dict[str, Any]) -> dict[str, Any]:
    if set(policy) - (_POLICY_BOOLEANS | _POLICY_INTEGERS | _POLICY_NUMBERS):
        _fail("policy:unknown_field")
    for field in policy:
        if field in _POLICY_BOOLEANS:
            _boolean(policy[field], "policy:" + field)
        elif field in _POLICY_INTEGERS:
            _integer(policy[field], "policy:" + field, minimum=1 if field == "max_steps_per_slice" else 0)
        elif not (field == "max_cost_per_slice" and policy[field] is None):
            _number(policy[field], "policy:" + field)
    effective = _effective_policy(policy, license_packet)
    if type(effective["max_steps_per_slice"]) is not int or effective["max_steps_per_slice"] != 1:
        _fail("policy:single_step_effective_slice_required")
    return effective


def _bundle_jobs(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    if bundle.get("version") != supervisor.BUNDLE_VERSION:
        _fail("bundle:version_mismatch")
    _string(_required(bundle, "agent_id", "bundle"), "bundle:agent_id")
    _integer(_required(bundle, "generation", "bundle"), "bundle:generation")
    _digest(bundle, "supervisor_bundle_digest", supervisor.bundle_digest, "bundle")
    jobs = _required(bundle, "jobs", "bundle")
    if type(jobs) is not list or not jobs:
        _fail("bundle:nonempty_jobs_required")
    identifiers = []
    for raw in jobs:
        job = _object(raw, "job")
        identifiers.append(_string(_required(job, "job_id", "job"), "job:job_id"))
        for field in ("manifest_revision", "generation", "current_step_index"):
            _integer(_required(job, field, "job"), "job:" + field)
        _number(_required(job, "remaining_budget_units", "job"), "job:remaining_budget_units")
        _strings(_required(job, "granted_permissions", "job"), "job:granted_permissions")
        _strings(_required(job, "completed_step_ids", "job"), "job:completed_step_ids")
        attempts = _object(_required(job, "step_attempts", "job"), "job:step_attempts")
        for key, value in attempts.items():
            _string(key, "job:step_attempts:key")
            _integer(value, "job:step_attempts:value")
        steps = _required(job, "steps", "job")
        if type(steps) is not list or not steps:
            _fail("job:steps_required")
        step_ids = []
        for raw_step in steps:
            step = _object(raw_step, "job:step")
            step_ids.append(_string(_required(step, "step_id", "job:step"), "job:step:step_id"))
            _string(_required(step, "operation_id", "job:step"), "job:step:operation_id")
            operation_input = _object(_required(step, "operation_input", "job:step"), "job:step:operation_input")
            if _required(step, "operation_input_digest", "job:step") != supervisor.sha(operation_input):
                _fail("job:step:operation_input_digest:body_mismatch")
            _number(_required(step, "estimated_cost_units", "job:step"), "job:step:estimated_cost_units")
            _integer(_required(step, "max_attempts", "job:step"), "job:step:max_attempts", minimum=1)
            _string(_required(step, "required_permission", "job:step"), "job:step:required_permission", empty=True)
        if len(step_ids) != len(set(step_ids)):
            _fail("job:duplicate_step_id")
        validate_job(job)
    if len(identifiers) != len(set(identifiers)):
        _fail("bundle:duplicate_job_id")
    _strings(bundle.get("processed_host_invocation_digests", []), "bundle:processed_host_invocation_digests")
    return jobs


def _projection(state: dict[str, Any], bundle: dict[str, Any], authorization: dict[str, Any],
                license_packet: dict[str, Any], now: int, registry: dict[str, Any],
                policy: dict[str, Any], worker: str) -> None:
    projection = _object(_required(state, "host_projection", "state"), "projection")
    _digest(projection, "projection_digest", host.projection_digest, "projection",
            _required(state, "host_projection_digest", "state"), cached_key="host_projection_digest")
    projected_at = _integer(_required(projection, "projected_at_ms", "projection"), "projection:projected_at_ms")
    if projected_at > state["updated_at_ms"] or projected_at > now:
        _fail("projection:future_timestamp")
    _flags(projection.get("boundary"), host.REQUIRED_BOUNDARY, "projection:boundary")
    _flags({key: _required(projection, key, "projection") for key in host.NON_AUTHORITY_FLAGS},
           host.NON_AUTHORITY_FLAGS, "projection:non_authority")
    expected = project_host_work(supervisor_bundle=bundle, now_ms=projected_at,
                                 operation_allowlist=license_packet["operation_allowlist"])
    if not _same(projection, expected):
        _fail("projection:native_reconstruction_mismatch")
    if projection.get("status") != host.READY or projection.get("adapter_state") != "work_ready":
        _fail("projection:work_not_ready")
    bindings = {
        "source_supervisor_bundle_digest": authorization["source_supervisor_bundle_digest"],
        "selected_job_id": authorization["host_job_id"],
        "selected_step_id": authorization["host_step_id"],
        "selected_operation_id": state["operation_id"],
    }
    for field, expected_value in bindings.items():
        if projection.get(field) != expected_value:
            _fail("projection:" + field + ":authorization_binding_mismatch")
    fresh = project_host_work(supervisor_bundle=bundle, now_ms=now,
                              operation_allowlist=license_packet["operation_allowlist"])
    for field in ("status", "adapter_state", "selected_job_id", "selected_job_state_digest",
                  "selected_ticket_id", "selected_ticket_digest", "selected_checkpoint_digest",
                  "selected_step_id", "selected_operation_id"):
        if not _same(projection[field], fresh[field]):
            _fail("projection:current_selection_mismatch:" + field)
    blockers = _projection_blockers(bundle, projection, license_packet, registry)
    if blockers:
        _fail("projection:native_precheck:" + ";".join(blockers))
    job = next(item for item in bundle["jobs"] if item["job_id"] == authorization["host_job_id"])
    ticket = _object(_required(job, "active_continuation_ticket", "job"), "ticket")
    if ticket.get("version") != TICKET_VERSION:
        _fail("ticket:version_mismatch")
    _digest(ticket, "background_ticket_digest", ticket_digest, "ticket")
    for field in ("ticket_id", "job_id", "checkpoint_digest"):
        _string(_required(ticket, field, "ticket"), "ticket:" + field)
    checkpoint = _string(_required(job, "latest_checkpoint_digest", "job"), "job:latest_checkpoint_digest")
    if ticket["job_id"] != job["job_id"] or ticket["checkpoint_digest"] != checkpoint:
        _fail("ticket:job_checkpoint_binding_mismatch")
    for field in ("retry_after_ms", "lease_started_at_ms", "lease_expires_at_ms", "heartbeat_at_ms"):
        _integer(_required(ticket, field, "ticket"), "ticket:" + field)
    _string(_required(ticket, "lease_owner", "ticket"), "ticket:lease_owner",
            empty=ticket.get("queue_status") == "queued")
    step = next_step(job)
    if type(step) is not dict:
        _fail("job:next_step_missing", status=NO_DATA)
    if (step["step_id"] != authorization["host_step_id"]
            or step["operation_id"] != state["operation_id"]):
        _fail("job:next_step_authorization_mismatch")
    if not (supervisor.sha(step["operation_input"]) == step["operation_input_digest"]
            == state["operation_input_digest"] == authorization["operation_input_digest"]):
        _fail("job:operation_input_digest:authorization_binding_mismatch")
    ready = precheck_step(job=job, policy=policy, spent_cost=0.0,
                          maximum_cost=policy["max_cost_per_slice"])
    if ready.get("kind") != "ready":
        _fail("job:step_unavailable:" + str(ready.get("phase", ready.get("kind"))))
    invocation = host.invocation_digest(
        invocation_id=authorization["invocation_id"], source_bundle_digest=bundle["supervisor_bundle_digest"],
        projection=projection["projection_digest"], worker_id=worker,
    )
    if invocation in bundle.get("processed_host_invocation_digests", []):
        _fail("invocation:already_processed_no_new_host_dispatch")


def _preflight(data: dict[str, Any]) -> None:
    state, bundle, policy = data["state"], data["supervisor_bundle"], data["supervisor_policy"]
    now = _integer(data["now_ms"], "now_ms")
    worker = _string(data["worker_id"], "worker_id")
    audit = audit_core_state("ActOS", state)
    if audit.status != "RUNTIME_CHECK_PASSED":
        raise PreHostCheckError(NO_DATA if audit.status == NO_DATA else BLOCKED,
                               tuple("state:" + issue for issue in audit.issues) or ("state:audit_failed",))
    if state.get("current_phase") != "project" or state.get("route") != "PENDING":
        _fail("state:uninvoked_project_phase_required")
    if now < state["updated_at_ms"]:
        _fail("state:time_regression")
    for field in ("effect_recorded", "observation_required", "verification_required"):
        if _required(state, field, "state") is not False:
            _fail("state:" + field + ":uninvoked_false_required")
    for field in ("host_tick", "host_receipt"):
        if not _same(_required(state, field, "state"), {}):
            _fail("state:" + field + ":already_present")
    for field in ("host_tick_digest", "host_receipt_digest", "host_invocation_digest"):
        if _required(state, field, "state") != "":
            _fail("state:" + field + ":already_present")
    _selected_step(state)
    authorization, license_packet = _authorization_and_license(state, now)
    _bundle_jobs(bundle)
    if bundle["supervisor_bundle_digest"] != state.get("source_supervisor_bundle_digest"):
        _fail("bundle:authorization_binding_mismatch")
    effective = _policy(policy, license_packet)
    _projection(state, bundle, authorization, license_packet, now, data["registry"], effective, worker)


def checked_build_authorized_invoke_event(
    *, state: Any, supervisor_bundle: Any, worker_id: Any, now_ms: Any,
    supervisor_policy: Any, registry: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Check one fresh Act invocation before the original builder may call host.

    Supplied JSON is copied without custom hooks. Registry values remain trusted
    callables and are shallow-copied separately. The added single-step cap is a
    Python restriction; Lean's one-slice bound does not itself imply one step.
    """
    try:
        if registry is None:
            _fail("registry:missing", status=NO_DATA)
        if type(registry) is not dict:
            _fail("registry:exact_dict_required")
        _finite_json(list(registry))
        for key, value in registry.items():
            _string(key, "registry:key")
            if not callable(value):
                _fail("registry:callable_required:" + key)
        copied_registry = dict(registry)
        data = {
            "state": _object(_finite_json(state), "state"),
            "supervisor_bundle": _object(_finite_json(supervisor_bundle), "supervisor_bundle"),
            "supervisor_policy": _object(_finite_json(supervisor_policy), "supervisor_policy"),
            "worker_id": _finite_json(worker_id), "now_ms": _finite_json(now_ms),
            "registry": copied_registry,
        }
        for label, function in (("original_builder", act.build_authorized_invoke_event),
                                ("original_authorization_validator", act._validate_authorization),
                                ("checked_apply_event", checked_apply_event)):
            if not callable(function):
                _fail("prerequisite:" + label + ":unavailable", status=NO_DATA)
        snapshots = {key: _fingerprint(value) for key, value in data.items() if key != "registry"}
        _preflight(data)
        if any(_fingerprint(data[key]) != value for key, value in snapshots.items()):
            _fail("preflight:input_mutated")
    except PreHostCheckError:
        raise
    except Exception as exc:
        raise PreHostCheckError(BLOCKED, ("preflight:" + type(exc).__name__ + ":" + str(exc),)) from exc

    # From here failures must never imply that no host effect occurred.
    try:
        result = act.build_authorized_invoke_event(**data)
        if any(_fingerprint(_finite_json(data[key])) != value for key, value in snapshots.items()):
            _fail("original_builder:input_mutated")
        if (type(data["registry"]) is not dict or set(data["registry"]) != set(registry)
                or any(data["registry"][key] is not registry[key] for key in registry)):
            _fail("original_builder:registry_mutated")
        if type(result) is not tuple or len(result) != 2:
            _fail("original_builder:return_pair_required")
        event = _object(_finite_json(result[0]), "event")
        tick = _object(_finite_json(result[1]), "tick")
        if not _same(_object(event.get("payload"), "event:payload").get("host_tick"), tick):
            _fail("event:host_tick_return_binding_mismatch")
        checked = checked_apply_event("ActOS", data["state"], event)
        if checked["status"] != "APPLIED":
            _fail("post_host:invoke_event_not_applied:" + checked["status"])
        return event, tick
    except (PreHostCheckError, CheckedTransitionError) as exc:
        raise PreHostCheckError(exc.status, exc.issues, host_call_attempted=True) from exc
    except Exception as exc:
        raise PreHostCheckError(BLOCKED, ("post_host:" + type(exc).__name__ + ":" + str(exc),),
                               host_call_attempted=True) from exc
