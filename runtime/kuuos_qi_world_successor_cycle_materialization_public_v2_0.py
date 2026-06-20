from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime import kuuos_qi_world_successor_cycle_materialization_v2_0 as _core


def _build_fresh_authority_candidate(
    *,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    plan_state: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> dict[str, Any]:
    packet = {
        "version": _core.AUTHORITY_VERSION,
        "authority_id": "qi-world-v20-fresh-successor-authority",
        "external_issuer": True,
        "self_issued": False,
        "source_blocker_receipt_digest": requirement[
            "source_successor_basis_digest"
        ],
        "source_blocker_certificate_digest": requirement[
            "source_post_effect_blocker_certificate_digest"
        ],
        "source_plan_state_digest": plan_state["plan_state_digest"],
        "source_plan_basis_digest": plan_state["next_plan_basis_digest"],
        "source_committed_plan_digest": plan_state[
            "latest_committed_plan_digest"
        ],
        "host_license_digest": host_license["host_license_digest"],
        "human_approval_receipt_digest": _core.sha(
            "qi-world-v20-fresh-human-approval"
        ),
        "human_approver_id": "external-human-operator-v20",
        "released_blockers": list(_core.RELEASABLE_BLOCKERS),
        "retained_invariant_blockers": list(_core.INVARIANT_BLOCKERS),
        "release_scope": deepcopy(_core.RELEASE_SCOPE),
        "single_use": True,
        "authority_does_not_widen_host_license": True,
        "target_cycle_strictly_later": True,
        "issued_at_ms": 90_000,
        "expires_at_ms": 180_000,
        "non_authority": deepcopy(_core.RELEASE_NON_AUTHORITY),
        "external_authority_packet_digest": "",
    }
    packet["external_authority_packet_digest"] = _core.authority_packet_digest(
        packet
    )
    return packet


def _build_second_act(
    root: Path,
    *,
    plan_state: Mapping[str, Any],
    execution_authority: Mapping[str, Any],
    host_license: Mapping[str, Any],
    supervisor_policy: Mapping[str, Any],
    supervisor_bundle: Mapping[str, Any],
    host_projection: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    activation = _core.build_plan_phase_activation_receipt(
        state=plan_state,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=execution_authority[
            "successor_authority_intake_digest"
        ],
        plan_phase_receipt_digest=execution_authority[
            "successor_execution_authority_digest"
        ],
        now_ms=90_000,
    )
    store = _core.ActStore(root)
    state = store.initialize(
        _core.build_initial_act_state(
            act_id="qi-world-v20-second-cycle-act",
            plan_state=plan_state,
            plan_activation_receipt=activation,
            now_ms=90_000,
        )
    )
    operation_input_digest = _core.sha({"value": 2, "cycle_ordinal": 2})
    state = _core.apply_act(
        store,
        state,
        "select",
        {
            "plan_state": deepcopy(dict(plan_state)),
            "selected_step_id": _core.RELEASE_SCOPE["selected_step_id"],
            "operation_id": _core.RELEASE_SCOPE["operation_id"],
            "operation_input_digest": operation_input_digest,
        },
        1,
    )
    authorization = _core.build_step_authorization(
        state=state,
        authorization_id="qi-world-v20-second-step-authorization",
        operation_id=_core.RELEASE_SCOPE["operation_id"],
        operation_input_digest=operation_input_digest,
        act_phase_receipt_digest=execution_authority[
            "successor_execution_authority_digest"
        ],
        invocation_id="qi-world-v20-second-single-invocation",
        source_supervisor_bundle_digest=host_projection[
            "source_supervisor_bundle_digest"
        ],
        host_job_id="qi-world-v20-job",
        host_step_id="step-1",
        host_license=host_license,
        human_approval_receipt_digest=execution_authority[
            "human_approval_receipt_digest"
        ],
        human_approver_id=execution_authority["human_approver_id"],
        issued_at_ms=90_000,
        expires_at_ms=180_000,
    )
    state = _core.apply_act(
        store,
        state,
        "authorize",
        {
            "step_authorization": authorization,
            "host_license": deepcopy(dict(host_license)),
        },
        2,
    )
    state = _core.apply_act(
        store,
        state,
        "project",
        {"host_projection": deepcopy(dict(host_projection))},
        3,
    )
    invoke_event, host_tick = _core.build_authorized_invoke_event(
        state=state,
        supervisor_bundle=supervisor_bundle,
        worker_id="qi-world-v20-worker",
        now_ms=90_004,
        supervisor_policy=supervisor_policy,
        registry=_core.registry(),
    )
    invoke_result = store.apply(invoke_event)
    if invoke_result.get("status") != "APPLIED":
        raise AssertionError(invoke_result)
    state = invoke_result["state"]
    state = _core.apply_act(
        store,
        state,
        "verify",
        {
            "verification_receipt_digest": _core.sha(
                "qi-world-v20-second-act-verification"
            )
        },
        5,
    )
    commit_event = _core.build_fixture_event(
        state,
        "commit",
        {
            "memory_overwrite": False,
            "automatic_truth_promotion": False,
            "automatic_plan_completion": False,
            "automatic_rollback": False,
            "lower_host_receipt_canonical": True,
            "source_lineage_preserved": True,
            "non_authority": _core.act_non_authority(),
        },
        6,
    )
    commit_result = store.apply(commit_event)
    if commit_result.get("status") != "APPLIED":
        raise AssertionError(commit_result)
    state = commit_result["state"]
    errors = _core.validate_act_state(state)
    if errors:
        raise ValueError("second_act_state_invalid:" + ";".join(errors))
    return state, activation, host_tick


_core._build_fresh_authority_candidate = _build_fresh_authority_candidate
_core._build_second_act = _build_second_act

VERSION = _core.VERSION
EXECUTION_AUTHORITY_VERSION = _core.EXECUTION_AUTHORITY_VERSION
DISCHARGE_VERSION = _core.DISCHARGE_VERSION
HANDOFF_VERSION = _core.HANDOFF_VERSION
CLOSURE_VERSION = _core.CLOSURE_VERSION
SECOND_CYCLE_VERSION = _core.SECOND_CYCLE_VERSION
MATERIALIZATION_VERSION = _core.MATERIALIZATION_VERSION
CYCLE_ID = _core.CYCLE_ID
execution_authority_digest = _core.execution_authority_digest
discharge_certificate_digest = _core.discharge_certificate_digest
successor_handoff_digest = _core.successor_handoff_digest
successor_closure_digest = _core.successor_closure_digest
second_cycle_receipt_digest = _core.second_cycle_receipt_digest
materialization_receipt_digest = _core.materialization_receipt_digest
build_successor_execution_authority = _core.build_successor_execution_authority
validate_successor_execution_authority = _core.validate_successor_execution_authority
build_successor_discharge_certificate = _core.build_successor_discharge_certificate
validate_successor_discharge_certificate = _core.validate_successor_discharge_certificate
build_successor_licensed_act_handoff = _core.build_successor_licensed_act_handoff
validate_successor_licensed_act_handoff = _core.validate_successor_licensed_act_handoff
build_successor_effect_evidence_closure = _core.build_successor_effect_evidence_closure
validate_successor_effect_evidence_closure = _core.validate_successor_effect_evidence_closure
build_second_cycle_receipt = _core.build_second_cycle_receipt
validate_second_cycle_receipt = _core.validate_second_cycle_receipt
build_successor_cycle_materialization_receipt = (
    _core.build_successor_cycle_materialization_receipt
)
validate_successor_cycle_materialization_receipt = (
    _core.validate_successor_cycle_materialization_receipt
)
