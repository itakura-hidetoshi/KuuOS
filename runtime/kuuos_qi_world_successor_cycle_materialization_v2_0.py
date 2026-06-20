from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_act_os_fixture_v0_1 import apply as apply_act
from runtime.kuuos_act_os_fixture_v0_1 import event as build_fixture_event
from runtime.kuuos_act_os_fixture_v0_1 import host_inputs
from runtime.kuuos_act_os_kernel_v0_1 import (
    build_authorized_invoke_event,
    build_initial_act_state,
    build_step_authorization,
    validate_act_state,
)
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_act_os_types_v0_1 import copy_non_authority as act_non_authority
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    AUTHORITY_VERSION,
    INVARIANT_BLOCKERS,
    RELEASE_NON_AUTHORITY,
    RELEASE_SCOPE,
    RELEASABLE_BLOCKERS,
    authority_packet_digest,
)
from runtime import kuuos_qi_world_licensed_effect_evidence_closure_v1_8 as _closure
from runtime.kuuos_qi_world_licensed_cycle_receipt_public_v1_9 import (
    build_licensed_cycle_receipt,
    build_successor_authority_intake,
    build_successor_authority_requirement,
    validate_licensed_cycle_receipt,
    validate_successor_authority_intake,
    validate_successor_authority_requirement,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import _build_downstream
from runtime.v017_host_adapter_fixtures import registry

VERSION = "kuuos_qi_world_successor_cycle_materialization_v2_0"
EXECUTION_AUTHORITY_VERSION = (
    "kuuos_qi_world_successor_execution_authority_packet_v2_0"
)
DISCHARGE_VERSION = "kuuos_qi_world_successor_discharge_certificate_v2_0"
HANDOFF_VERSION = "kuuos_qi_world_successor_licensed_act_handoff_v2_0"
CLOSURE_VERSION = "kuuos_qi_world_successor_effect_evidence_closure_v2_0"
SECOND_CYCLE_VERSION = "kuuos_qi_world_second_closed_cycle_receipt_v2_0"
MATERIALIZATION_VERSION = "kuuos_qi_world_two_cycle_materialization_receipt_v2_0"
CYCLE_ID = "qi-world-successor-cycle-materialization-v20"

EXECUTION_AUTHORITY_NON_AUTHORITY = {
    "authority_grants_truth": False,
    "authority_grants_world_identity": False,
    "authority_grants_memory_overwrite": False,
    "authority_grants_plan_completion": False,
    "authority_grants_automatic_rollback": False,
    "authority_issues_further_authority": False,
}

HANDOFF_NON_AUTHORITY = {
    "handoff_grants_truth": False,
    "handoff_updates_exact_world": False,
    "handoff_overwrites_history": False,
    "handoff_issues_further_authority": False,
    "handoff_starts_third_cycle": False,
}

CLOSURE_NON_AUTHORITY = {
    "closure_grants_execution": False,
    "closure_grants_truth": False,
    "closure_issues_authority": False,
    "closure_starts_next_act": False,
    "closure_updates_exact_world": False,
    "closure_overwrites_history": False,
    "closure_renews_external_authority": False,
}

SECOND_CYCLE_NON_AUTHORITY = {
    "receipt_grants_execution": False,
    "receipt_grants_truth": False,
    "receipt_grants_world_identity": False,
    "receipt_grants_memory_overwrite": False,
    "receipt_issues_successor_authority": False,
    "receipt_renews_consumed_authority": False,
}

MATERIALIZATION_NON_AUTHORITY = {
    "materialization_grants_third_cycle_execution": False,
    "materialization_grants_truth": False,
    "materialization_updates_exact_world": False,
    "materialization_overwrites_history": False,
    "materialization_collapses_worlds": False,
    "materialization_issues_further_authority": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def execution_authority_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_execution_authority_digest")


def discharge_certificate_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_discharge_certificate_digest")


def successor_handoff_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "licensed_act_handoff_receipt_digest")


def successor_closure_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(
        value, "successor_effect_evidence_closure_receipt_digest"
    )


def second_cycle_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "second_cycle_receipt_digest")


def materialization_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_cycle_materialization_receipt_digest")


def _predecessor_closure(predecessor: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(predecessor["source_v18_closure_receipt"]))


def _predecessor_plan(predecessor: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(_predecessor_closure(predecessor)["next_cycle_artifacts"]["PlanOS"]))


def _build_fresh_authority_candidate(
    *,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    plan_state: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> dict[str, Any]:
    packet = {
        "version": AUTHORITY_VERSION,
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
        "human_approval_receipt_digest": sha(
            "qi-world-v20-fresh-human-approval"
        ),
        "human_approver_id": "external-human-operator-v20",
        "released_blockers": list(RELEASABLE_BLOCKERS),
        "retained_invariant_blockers": list(INVARIANT_BLOCKERS),
        "release_scope": deepcopy(RELEASE_SCOPE),
        "single_use": True,
        "authority_does_not_widen_host_license": True,
        "target_cycle_strictly_later": True,
        "issued_at_ms": 190_000,
        "expires_at_ms": 280_000,
        "non_authority": deepcopy(RELEASE_NON_AUTHORITY),
        "external_authority_packet_digest": "",
    }
    packet["external_authority_packet_digest"] = authority_packet_digest(packet)
    return packet


def build_successor_execution_authority(
    *,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    intake: Mapping[str, Any],
    freshness_candidate: Mapping[str, Any],
    plan_state: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> dict[str, Any]:
    packet = {
        "version": EXECUTION_AUTHORITY_VERSION,
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "target_cycle_ordinal": 2,
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "successor_authority_intake_digest": intake[
            "successor_authority_intake_digest"
        ],
        "freshness_candidate_digest": freshness_candidate[
            "external_authority_packet_digest"
        ],
        "source_post_effect_blocker_certificate_digest": requirement[
            "source_post_effect_blocker_certificate_digest"
        ],
        "source_plan_state_digest": plan_state["plan_state_digest"],
        "source_committed_plan_digest": plan_state[
            "latest_committed_plan_digest"
        ],
        "source_plan_basis_digest": plan_state["plan_basis_digest"],
        "source_next_plan_basis_digest": plan_state[
            "next_plan_basis_digest"
        ],
        "host_license_digest": host_license["host_license_digest"],
        "human_approval_receipt_digest": freshness_candidate[
            "human_approval_receipt_digest"
        ],
        "human_approver_id": freshness_candidate["human_approver_id"],
        "released_blockers": list(RELEASABLE_BLOCKERS),
        "retained_invariant_blockers": list(INVARIANT_BLOCKERS),
        "release_scope": deepcopy(RELEASE_SCOPE),
        "external_materialization": True,
        "self_issued": False,
        "single_use": True,
        "authority_does_not_widen_host_license": True,
        "target_cycle_strictly_later": True,
        "freshness_candidate_not_execution_authority": True,
        "issued_at_ms": freshness_candidate["issued_at_ms"],
        "expires_at_ms": freshness_candidate["expires_at_ms"],
        "non_authority": deepcopy(EXECUTION_AUTHORITY_NON_AUTHORITY),
        "successor_execution_authority_digest": "",
    }
    packet["successor_execution_authority_digest"] = execution_authority_digest(
        packet
    )
    errors = validate_successor_execution_authority(
        packet,
        predecessor=predecessor,
        requirement=requirement,
        intake=intake,
        freshness_candidate=freshness_candidate,
        plan_state=plan_state,
        host_license=host_license,
    )
    if errors:
        raise ValueError("successor_execution_authority_invalid:" + ";".join(errors))
    return packet


def validate_successor_execution_authority(
    packet: Mapping[str, Any],
    *,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    intake: Mapping[str, Any],
    freshness_candidate: Mapping[str, Any],
    plan_state: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        errors.extend(
            "execution_authority_predecessor_" + error
            for error in validate_licensed_cycle_receipt(predecessor)
        )
        errors.extend(
            "execution_authority_requirement_" + error
            for error in validate_successor_authority_requirement(
                requirement,
                closed_cycle_receipt=predecessor,
            )
        )
        errors.extend(
            "execution_authority_intake_" + error
            for error in validate_successor_authority_intake(
                intake,
                requirement=requirement,
                closed_cycle_receipt=predecessor,
                candidate_external_authority_packet=freshness_candidate,
            )
        )
        require(
            packet.get("version") == EXECUTION_AUTHORITY_VERSION,
            "execution_authority_version_invalid",
        )
        require(
            packet.get("successor_execution_authority_digest")
            == execution_authority_digest(packet),
            "execution_authority_digest_invalid",
        )
        expected = {
            "predecessor_cycle_receipt_digest": predecessor.get(
                "licensed_cycle_receipt_digest"
            ),
            "target_cycle_ordinal": 2,
            "successor_authority_requirement_digest": requirement.get(
                "successor_authority_requirement_digest"
            ),
            "successor_authority_intake_digest": intake.get(
                "successor_authority_intake_digest"
            ),
            "freshness_candidate_digest": freshness_candidate.get(
                "external_authority_packet_digest"
            ),
            "source_post_effect_blocker_certificate_digest": requirement.get(
                "source_post_effect_blocker_certificate_digest"
            ),
            "source_plan_state_digest": plan_state.get("plan_state_digest"),
            "source_committed_plan_digest": plan_state.get(
                "latest_committed_plan_digest"
            ),
            "source_plan_basis_digest": plan_state.get("plan_basis_digest"),
            "source_next_plan_basis_digest": plan_state.get(
                "next_plan_basis_digest"
            ),
            "host_license_digest": host_license.get("host_license_digest"),
            "human_approval_receipt_digest": freshness_candidate.get(
                "human_approval_receipt_digest"
            ),
            "human_approver_id": freshness_candidate.get("human_approver_id"),
            "released_blockers": list(RELEASABLE_BLOCKERS),
            "retained_invariant_blockers": list(INVARIANT_BLOCKERS),
            "release_scope": RELEASE_SCOPE,
        }
        for field, value in expected.items():
            require(
                packet.get(field) == value,
                f"execution_authority_{field}_invalid",
            )
        require(
            freshness_candidate.get("source_plan_state_digest")
            == plan_state.get("plan_state_digest"),
            "execution_authority_freshness_plan_state_mismatch",
        )
        require(
            freshness_candidate.get("source_plan_basis_digest")
            == plan_state.get("next_plan_basis_digest"),
            "execution_authority_freshness_next_basis_mismatch",
        )
        require(
            packet.get("source_plan_basis_digest")
            != packet.get("source_next_plan_basis_digest"),
            "execution_authority_plan_basis_layers_collapsed",
        )
        old_authority = predecessor.get(
            "consumed_external_authority_packet_digest"
        )
        old_approval = predecessor.get("consumed_human_approval_receipt_digest")
        old_host = predecessor.get("consumed_host_license_digest")
        require(
            packet.get("successor_execution_authority_digest") != old_authority,
            "execution_authority_predecessor_authority_reuse",
        )
        require(
            packet.get("human_approval_receipt_digest") != old_approval,
            "execution_authority_predecessor_approval_reuse",
        )
        require(
            packet.get("host_license_digest") != old_host,
            "execution_authority_predecessor_host_reuse",
        )
        for field in (
            "external_materialization",
            "single_use",
            "authority_does_not_widen_host_license",
            "target_cycle_strictly_later",
            "freshness_candidate_not_execution_authority",
        ):
            require(packet.get(field) is True, f"execution_authority_{field}_invalid")
        require(
            packet.get("self_issued") is False,
            "execution_authority_self_issue_forbidden",
        )
        require(
            int(packet.get("issued_at_ms", -1))
            == int(freshness_candidate.get("issued_at_ms", -2)),
            "execution_authority_issued_at_mismatch",
        )
        require(
            int(packet.get("expires_at_ms", -1))
            == int(freshness_candidate.get("expires_at_ms", -2)),
            "execution_authority_expires_at_mismatch",
        )
        require(
            dict(packet.get("non_authority", {}))
            == EXECUTION_AUTHORITY_NON_AUTHORITY,
            "execution_authority_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


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
    activation = build_plan_phase_activation_receipt(
        state=plan_state,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=execution_authority[
            "successor_authority_intake_digest"
        ],
        plan_phase_receipt_digest=execution_authority[
            "successor_execution_authority_digest"
        ],
        now_ms=190_000,
    )
    store = ActStore(root)
    state = store.initialize(
        build_initial_act_state(
            act_id="qi-world-v20-second-cycle-act",
            plan_state=plan_state,
            plan_activation_receipt=activation,
            now_ms=190_000,
        )
    )
    operation_input_digest = sha({"value": 2, "cycle_ordinal": 2})
    state = apply_act(
        store,
        state,
        "select",
        {
            "plan_state": deepcopy(dict(plan_state)),
            "selected_step_id": RELEASE_SCOPE["selected_step_id"],
            "operation_id": RELEASE_SCOPE["operation_id"],
            "operation_input_digest": operation_input_digest,
        },
        1,
    )
    authorization = build_step_authorization(
        state=state,
        authorization_id="qi-world-v20-second-step-authorization",
        operation_id=RELEASE_SCOPE["operation_id"],
        operation_input_digest=operation_input_digest,
        act_phase_receipt_digest=execution_authority[
            "successor_execution_authority_digest"
        ],
        invocation_id="qi-world-v20-second-single-invocation",
        source_supervisor_bundle_digest=host_projection[
            "source_supervisor_bundle_digest"
        ],
        host_job_id="qi-world-v20-job",
        host_step_id="step-2",
        host_license=host_license,
        human_approval_receipt_digest=execution_authority[
            "human_approval_receipt_digest"
        ],
        human_approver_id=execution_authority["human_approver_id"],
        issued_at_ms=190_000,
        expires_at_ms=280_000,
    )
    state = apply_act(
        store,
        state,
        "authorize",
        {
            "step_authorization": authorization,
            "host_license": deepcopy(dict(host_license)),
        },
        2,
    )
    state = apply_act(
        store,
        state,
        "project",
        {"host_projection": deepcopy(dict(host_projection))},
        3,
    )
    invoke_event, host_tick = build_authorized_invoke_event(
        state=state,
        supervisor_bundle=supervisor_bundle,
        worker_id="qi-world-v20-worker",
        now_ms=190_004,
        supervisor_policy=supervisor_policy,
        registry=registry(),
    )
    invoke_result = store.apply(invoke_event)
    if invoke_result.get("status") != "APPLIED":
        raise AssertionError(invoke_result)
    state = invoke_result["state"]
    state = apply_act(
        store,
        state,
        "verify",
        {
            "verification_receipt_digest": sha(
                "qi-world-v20-second-act-verification"
            )
        },
        5,
    )
    commit_event = build_fixture_event(
        state,
        "commit",
        {
            "memory_overwrite": False,
            "automatic_truth_promotion": False,
            "automatic_plan_completion": False,
            "automatic_rollback": False,
            "lower_host_receipt_canonical": True,
            "source_lineage_preserved": True,
            "non_authority": act_non_authority(),
        },
        6,
    )
    commit_result = store.apply(commit_event)
    if commit_result.get("status") != "APPLIED":
        raise AssertionError(commit_result)
    state = commit_result["state"]
    errors = validate_act_state(state)
    if errors:
        raise ValueError("second_act_state_invalid:" + ";".join(errors))
    return state, activation, host_tick


def build_successor_discharge_certificate(
    *,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    intake: Mapping[str, Any],
    freshness_candidate: Mapping[str, Any],
    execution_authority: Mapping[str, Any],
    act_state: Mapping[str, Any],
) -> dict[str, Any]:
    blocker = _predecessor_closure(predecessor)[
        "post_effect_blocker_certificate"
    ]
    vector = dict(blocker["composed_blocker_vector"])
    retained = {name: vector.get(name) is True for name in INVARIANT_BLOCKERS}
    certificate = {
        "version": DISCHARGE_VERSION,
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "target_cycle_ordinal": 2,
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "successor_authority_intake_digest": intake[
            "successor_authority_intake_digest"
        ],
        "freshness_candidate_digest": freshness_candidate[
            "external_authority_packet_digest"
        ],
        "successor_execution_authority_digest": execution_authority[
            "successor_execution_authority_digest"
        ],
        "source_post_effect_blocker_certificate_digest": blocker[
            "post_effect_blocker_certificate_digest"
        ],
        "released_blockers": list(RELEASABLE_BLOCKERS),
        "retained_invariant_blockers": retained,
        "all_invariant_blockers_retained": all(retained.values()),
        "predecessor_cycle_immutable": True,
        "freshness_candidate_read_only": True,
        "target_cycle_strictly_later": True,
        "single_use_release": True,
        "release_consumption_count": 1,
        "released_operation_id": act_state["operation_id"],
        "released_step_id": act_state["selected_step_id"],
        "released_act_state_digest": act_state["act_state_digest"],
        "effect_recorded": act_state["effect_recorded"],
        "observation_required": act_state["observation_required"],
        "verification_required": act_state["verification_required"],
        "explicit_discharge_completed": True,
        "memory_overwritten": False,
        "exact_world_updated": False,
        "truth_promoted": False,
        "same_cycle_recursive_invocation": False,
        "multi_world_collapsed": False,
        "non_authority": deepcopy(HANDOFF_NON_AUTHORITY),
        "successor_discharge_certificate_digest": "",
    }
    certificate["successor_discharge_certificate_digest"] = (
        discharge_certificate_digest(certificate)
    )
    return certificate


def validate_successor_discharge_certificate(
    certificate: Mapping[str, Any],
    *,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    intake: Mapping[str, Any],
    freshness_candidate: Mapping[str, Any],
    execution_authority: Mapping[str, Any],
    act_state: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        expected = build_successor_discharge_certificate(
            predecessor=predecessor,
            requirement=requirement,
            intake=intake,
            freshness_candidate=freshness_candidate,
            execution_authority=execution_authority,
            act_state=act_state,
        )
        require(
            certificate.get("version") == DISCHARGE_VERSION,
            "second_discharge_version_invalid",
        )
        require(
            certificate.get("successor_discharge_certificate_digest")
            == discharge_certificate_digest(certificate),
            "second_discharge_digest_invalid",
        )
        for field, value in expected.items():
            if field == "successor_discharge_certificate_digest":
                continue
            require(
                certificate.get(field) == value,
                f"second_discharge_{field}_invalid",
            )
        require(
            certificate.get("release_consumption_count") == 1,
            "second_discharge_replay_or_multiuse",
        )
        require(
            certificate.get("all_invariant_blockers_retained") is True,
            "second_discharge_invariant_loss",
        )
        require(
            certificate.get("explicit_discharge_completed") is True,
            "second_discharge_not_completed",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_successor_licensed_act_handoff(
    root: Path,
    *,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    intake: Mapping[str, Any],
    freshness_candidate: Mapping[str, Any],
    execution_authority: Mapping[str, Any],
    plan_state: Mapping[str, Any],
    host_license: Mapping[str, Any],
    supervisor_policy: Mapping[str, Any],
    supervisor_bundle: Mapping[str, Any],
    host_projection: Mapping[str, Any],
) -> dict[str, Any]:
    act_state, activation, host_tick = _build_second_act(
        root / "act-v20",
        plan_state=plan_state,
        execution_authority=execution_authority,
        host_license=host_license,
        supervisor_policy=supervisor_policy,
        supervisor_bundle=supervisor_bundle,
        host_projection=host_projection,
    )
    discharge = build_successor_discharge_certificate(
        predecessor=predecessor,
        requirement=requirement,
        intake=intake,
        freshness_candidate=freshness_candidate,
        execution_authority=execution_authority,
        act_state=act_state,
    )
    first_handoff = predecessor["source_v17_handoff_receipt"]
    receipt = {
        "version": HANDOFF_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_cycle_receipt": deepcopy(dict(predecessor)),
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "successor_authority_requirement": deepcopy(dict(requirement)),
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "successor_authority_intake": deepcopy(dict(intake)),
        "successor_authority_intake_digest": intake[
            "successor_authority_intake_digest"
        ],
        "freshness_candidate": deepcopy(dict(freshness_candidate)),
        "freshness_candidate_digest": freshness_candidate[
            "external_authority_packet_digest"
        ],
        "successor_execution_authority": deepcopy(dict(execution_authority)),
        "successor_execution_authority_digest": execution_authority[
            "successor_execution_authority_digest"
        ],
        "plan_activation_receipt": deepcopy(activation),
        "successor_discharge_certificate": deepcopy(discharge),
        "successor_discharge_certificate_digest": discharge[
            "successor_discharge_certificate_digest"
        ],
        "target_act_state": deepcopy(act_state),
        "host_tick_digest": host_tick["host_tick_digest"],
        "source_indra_transport_request_receipt": deepcopy(
            dict(first_handoff["source_indra_transport_request_receipt"])
        ),
        "source_indra_transport_request_receipt_digest": first_handoff[
            "source_indra_transport_request_receipt_digest"
        ],
        "predecessor_cycle_immutable": True,
        "freshness_candidate_read_only": True,
        "execution_authority_materialized": True,
        "release_consumed": True,
        "release_consumption_count": 1,
        "target_act_started": True,
        "effect_recorded": True,
        "observation_required": True,
        "verification_required": True,
        "memory_overwritten": False,
        "exact_world_updated": False,
        "truth_promoted": False,
        "same_cycle_recursive_invocation": False,
        "multi_world_collapsed": False,
        "indra_transport_still_unrealized": True,
        "non_authority": deepcopy(HANDOFF_NON_AUTHORITY),
        "licensed_act_handoff_receipt_digest": "",
    }
    receipt["licensed_act_handoff_receipt_digest"] = successor_handoff_digest(
        receipt
    )
    errors = validate_successor_licensed_act_handoff(receipt)
    if errors:
        raise ValueError("successor_handoff_invalid:" + ";".join(errors))
    return receipt


def validate_successor_licensed_act_handoff(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == HANDOFF_VERSION, "second_handoff_version_invalid")
        require(
            receipt.get("licensed_act_handoff_receipt_digest")
            == successor_handoff_digest(receipt),
            "second_handoff_digest_invalid",
        )
        predecessor = dict(receipt.get("predecessor_cycle_receipt", {}))
        errors.extend(
            "second_handoff_predecessor_" + error
            for error in validate_licensed_cycle_receipt(predecessor)
        )
        require(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "second_handoff_predecessor_digest_mismatch",
        )
        requirement = dict(receipt.get("successor_authority_requirement", {}))
        errors.extend(
            "second_handoff_requirement_" + error
            for error in validate_successor_authority_requirement(
                requirement,
                closed_cycle_receipt=predecessor,
            )
        )
        intake = dict(receipt.get("successor_authority_intake", {}))
        candidate = dict(receipt.get("freshness_candidate", {}))
        errors.extend(
            "second_handoff_intake_" + error
            for error in validate_successor_authority_intake(
                intake,
                requirement=requirement,
                closed_cycle_receipt=predecessor,
                candidate_external_authority_packet=candidate,
            )
        )
        require(
            receipt.get("successor_authority_requirement_digest")
            == requirement.get("successor_authority_requirement_digest"),
            "second_handoff_requirement_digest_mismatch",
        )
        require(
            receipt.get("successor_authority_intake_digest")
            == intake.get("successor_authority_intake_digest"),
            "second_handoff_intake_digest_mismatch",
        )
        require(
            receipt.get("freshness_candidate_digest")
            == candidate.get("external_authority_packet_digest"),
            "second_handoff_candidate_digest_mismatch",
        )
        execution_authority = dict(
            receipt.get("successor_execution_authority", {})
        )
        plan_state = _predecessor_plan(predecessor)
        act_state = dict(receipt.get("target_act_state", {}))
        host_license = dict(act_state.get("host_license", {}))
        errors.extend(
            "second_handoff_execution_authority_" + error
            for error in validate_successor_execution_authority(
                execution_authority,
                predecessor=predecessor,
                requirement=requirement,
                intake=intake,
                freshness_candidate=candidate,
                plan_state=plan_state,
                host_license=host_license,
            )
        )
        require(
            receipt.get("successor_execution_authority_digest")
            == execution_authority.get("successor_execution_authority_digest"),
            "second_handoff_execution_authority_digest_mismatch",
        )
        errors.extend("second_handoff_act_" + error for error in validate_act_state(act_state))
        require(
            act_state.get("source_plan_state_digest")
            == plan_state.get("plan_state_digest"),
            "second_handoff_act_plan_state_mismatch",
        )
        require(
            act_state.get("source_plan_basis_digest")
            == plan_state.get("plan_basis_digest"),
            "second_handoff_act_plan_basis_mismatch",
        )
        authorization = dict(act_state.get("step_authorization", {}))
        activation = dict(receipt.get("plan_activation_receipt", {}))
        require(
            authorization.get("act_phase_receipt_digest")
            == execution_authority.get("successor_execution_authority_digest"),
            "second_handoff_authorization_execution_authority_mismatch",
        )
        require(
            authorization.get("plan_activation_receipt_digest")
            == activation.get("plan_activation_receipt_digest"),
            "second_handoff_authorization_activation_mismatch",
        )
        require(
            authorization.get("host_license_digest")
            == execution_authority.get("host_license_digest"),
            "second_handoff_authorization_host_mismatch",
        )
        require(
            authorization.get("human_approval_receipt_digest")
            == execution_authority.get("human_approval_receipt_digest"),
            "second_handoff_authorization_approval_mismatch",
        )
        require(
            [item.get("target_phase") for item in act_state.get("event_history", [])]
            == ["select", "authorize", "project", "invoke", "verify", "commit"],
            "second_handoff_act_phase_history_invalid",
        )
        discharge = dict(receipt.get("successor_discharge_certificate", {}))
        errors.extend(
            validate_successor_discharge_certificate(
                discharge,
                predecessor=predecessor,
                requirement=requirement,
                intake=intake,
                freshness_candidate=candidate,
                execution_authority=execution_authority,
                act_state=act_state,
            )
        )
        require(
            receipt.get("successor_discharge_certificate_digest")
            == discharge.get("successor_discharge_certificate_digest"),
            "second_handoff_discharge_digest_mismatch",
        )
        require(
            receipt.get("host_tick_digest") == act_state.get("host_tick_digest"),
            "second_handoff_host_tick_mismatch",
        )
        first_handoff = predecessor["source_v17_handoff_receipt"]
        require(
            dict(receipt.get("source_indra_transport_request_receipt", {}))
            == dict(first_handoff["source_indra_transport_request_receipt"]),
            "second_handoff_indra_receipt_substitution",
        )
        require(receipt.get("cycle_ordinal") == 2, "second_handoff_ordinal_invalid")
        expected_flags = {
            "predecessor_cycle_immutable": True,
            "freshness_candidate_read_only": True,
            "execution_authority_materialized": True,
            "release_consumed": True,
            "target_act_started": True,
            "effect_recorded": True,
            "observation_required": True,
            "verification_required": True,
            "memory_overwritten": False,
            "exact_world_updated": False,
            "truth_promoted": False,
            "same_cycle_recursive_invocation": False,
            "multi_world_collapsed": False,
            "indra_transport_still_unrealized": True,
        }
        for field, value in expected_flags.items():
            require(receipt.get(field) == value, f"second_handoff_{field}_invalid")
        require(
            receipt.get("release_consumption_count") == 1,
            "second_handoff_replay_or_multiuse",
        )
        require(
            dict(receipt.get("non_authority", {})) == HANDOFF_NON_AUTHORITY,
            "second_handoff_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _second_world_projection(
    *,
    predecessor: Mapping[str, Any],
    handoff: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    first_closure = _predecessor_closure(predecessor)
    indra = dict(handoff["source_indra_transport_request_receipt"])
    request = dict(indra["transport_request"])
    packet = {
        "projection_kind": "successor_licensed_effect_evidence_projection",
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "predecessor_world_projection_digest": first_closure[
            "post_effect_world_projection_digest"
        ],
        "source_indra_transport_request_digest": request[
            "transport_request_digest"
        ],
        "act_state_digest": states["ActOS"]["act_state_digest"],
        "observe_state_digest": states["ObserveOS"]["observe_state_digest"],
        "verify_state_digest": states["VerifyOS"]["verify_state_digest"],
        "learn_state_digest": states["LearnOS"]["learn_state_digest"],
        "next_plan_state_digest": next_artifacts["PlanOS"]["plan_state_digest"],
        "projection_read_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "exact_world_identified": False,
        "runtime_updates_world": False,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
        "indra_transport_still_unrealized": True,
        "world_projection_digest": "",
    }
    packet["world_projection_digest"] = _digest_without(
        packet, "world_projection_digest"
    )
    return packet


def build_successor_effect_evidence_closure(
    root: Path,
    *,
    handoff: Mapping[str, Any],
) -> dict[str, Any]:
    handoff_errors = validate_successor_licensed_act_handoff(handoff)
    if handoff_errors:
        raise ValueError("second_handoff_invalid:" + ";".join(handoff_errors))
    predecessor = dict(handoff["predecessor_cycle_receipt"])
    act = deepcopy(dict(handoff["target_act_state"]))
    observe, verify, learn = _build_downstream(root / "evidence", act)
    states = {
        "ActOS": act,
        "ObserveOS": observe,
        "VerifyOS": verify,
        "LearnOS": learn,
    }
    native_errors = _closure._native_validation_errors(states)
    if native_errors:
        raise ValueError("second_native_evidence_invalid:" + ";".join(native_errors))
    lineage_digest = _closure._evidence_lineage_digest(handoff, states)
    next_artifacts = _closure._build_next_cycle(
        root / "next-cycle",
        source=handoff,
        states=states,
        lineage_digest=lineage_digest,
    )
    world = _second_world_projection(
        predecessor=predecessor,
        handoff=handoff,
        states=states,
        next_artifacts=next_artifacts,
    )
    qi = _closure._qi_receipt(states, next_artifacts)
    blocker = _closure.build_post_effect_blocker_certificate(
        source=handoff,
        states=states,
        next_artifacts=next_artifacts,
        world=world,
    )
    receipt = {
        "version": CLOSURE_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "source_successor_handoff": deepcopy(dict(handoff)),
        "source_successor_handoff_digest": handoff[
            "licensed_act_handoff_receipt_digest"
        ],
        "native_evidence_states": deepcopy(states),
        "native_evidence_lineage_digest": lineage_digest,
        "next_cycle_artifacts": deepcopy(next_artifacts),
        "post_effect_qi_receipt": qi,
        "post_effect_world_projection": world,
        "post_effect_world_projection_digest": world[
            "world_projection_digest"
        ],
        "post_effect_blocker_certificate": blocker,
        "post_effect_blocker_certificate_digest": blocker[
            "post_effect_blocker_certificate_digest"
        ],
        "source_effect_immutable": True,
        "source_authority_consumed_once": True,
        "observation_debt_discharged": True,
        "verification_debt_discharged": True,
        "learning_recorded": True,
        "replan_debt_discharged": True,
        "next_act_not_started": True,
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CLOSURE_NON_AUTHORITY),
        "successor_effect_evidence_closure_receipt_digest": "",
    }
    receipt["successor_effect_evidence_closure_receipt_digest"] = (
        successor_closure_digest(receipt)
    )
    errors = validate_successor_effect_evidence_closure(receipt)
    if errors:
        raise ValueError("second_evidence_closure_invalid:" + ";".join(errors))
    return receipt


def validate_successor_effect_evidence_closure(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == CLOSURE_VERSION, "second_closure_version_invalid")
        require(
            receipt.get("successor_effect_evidence_closure_receipt_digest")
            == successor_closure_digest(receipt),
            "second_closure_digest_invalid",
        )
        handoff = dict(receipt.get("source_successor_handoff", {}))
        errors.extend(
            "second_closure_source_" + error
            for error in validate_successor_licensed_act_handoff(handoff)
        )
        require(
            receipt.get("source_successor_handoff_digest")
            == handoff.get("licensed_act_handoff_receipt_digest"),
            "second_closure_handoff_digest_mismatch",
        )
        predecessor = dict(handoff.get("predecessor_cycle_receipt", {}))
        require(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "second_closure_predecessor_digest_mismatch",
        )
        states = dict(receipt.get("native_evidence_states", {}))
        errors.extend("second_closure_" + error for error in _closure._native_validation_errors(states))
        act = dict(states.get("ActOS", {}))
        observe = dict(states.get("ObserveOS", {}))
        verify = dict(states.get("VerifyOS", {}))
        learn = dict(states.get("LearnOS", {}))
        require(
            act == dict(handoff.get("target_act_state", {})),
            "second_closure_source_act_substitution",
        )
        require(
            observe.get("source_act_state_digest") == act.get("act_state_digest"),
            "second_closure_observe_source_mismatch",
        )
        require(
            verify.get("source_observe_state_digest")
            == observe.get("observe_state_digest"),
            "second_closure_verify_source_mismatch",
        )
        require(
            learn.get("source_verify_state_digest")
            == verify.get("verify_state_digest"),
            "second_closure_learn_source_mismatch",
        )
        require(
            receipt.get("native_evidence_lineage_digest")
            == _closure._evidence_lineage_digest(handoff, states),
            "second_closure_lineage_digest_mismatch",
        )
        next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
        errors.extend(
            "second_closure_next_" + error
            for error in _closure._reentry._validate_next_artifacts(next_artifacts)
        )
        plan = dict(next_artifacts.get("PlanOS", {}))
        require(
            plan.get("next_plan_basis_digest")
            == learn.get("learning_delta_digest"),
            "second_closure_next_plan_learning_basis_mismatch",
        )
        require(
            plan.get("current_phase") == "commit",
            "second_closure_next_plan_not_committed",
        )
        world = dict(receipt.get("post_effect_world_projection", {}))
        require(
            receipt.get("post_effect_world_projection_digest")
            == world.get("world_projection_digest"),
            "second_closure_world_digest_mismatch",
        )
        require(
            world.get("world_projection_digest")
            == _digest_without(world, "world_projection_digest"),
            "second_closure_world_digest_invalid",
        )
        first_closure = _predecessor_closure(predecessor)
        require(
            world.get("predecessor_world_projection_digest")
            == first_closure.get("post_effect_world_projection_digest"),
            "second_closure_world_predecessor_mismatch",
        )
        blocker = dict(receipt.get("post_effect_blocker_certificate", {}))
        errors.extend(
            _closure.validate_post_effect_blocker_certificate(
                blocker,
                source=handoff,
                states=states,
                next_artifacts=next_artifacts,
                world=world,
            )
        )
        require(
            receipt.get("post_effect_blocker_certificate_digest")
            == blocker.get("post_effect_blocker_certificate_digest"),
            "second_closure_blocker_digest_mismatch",
        )
        require(
            blocker.get("all_required_blockers_active") is True
            and blocker.get("missing_blockers") == []
            and all(
                dict(blocker.get("composed_blocker_vector", {})).get(name) is True
                for name in _closure.BLOCKER_ORDER
            ),
            "second_closure_blockers_not_all_active",
        )
        expected_flags = {
            "source_effect_immutable": True,
            "source_authority_consumed_once": True,
            "observation_debt_discharged": True,
            "verification_debt_discharged": True,
            "learning_recorded": True,
            "replan_debt_discharged": True,
            "next_act_not_started": True,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected_flags.items():
            require(receipt.get(field) == value, f"second_closure_{field}_invalid")
        require(receipt.get("cycle_ordinal") == 2, "second_closure_ordinal_invalid")
        require(
            dict(receipt.get("non_authority", {})) == CLOSURE_NON_AUTHORITY,
            "second_closure_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _terminal_state_digest(closure: Mapping[str, Any]) -> str:
    states = dict(closure["native_evidence_states"])
    next_artifacts = dict(closure["next_cycle_artifacts"])
    blocker = dict(closure["post_effect_blocker_certificate"])
    world = dict(closure["post_effect_world_projection"])
    return sha(
        {
            "act_state_digest": states["ActOS"]["act_state_digest"],
            "observe_state_digest": states["ObserveOS"]["observe_state_digest"],
            "verify_state_digest": states["VerifyOS"]["verify_state_digest"],
            "learn_state_digest": states["LearnOS"]["learn_state_digest"],
            "learning_delta_digest": states["LearnOS"]["learning_delta_digest"],
            "next_plan_state_digest": next_artifacts["PlanOS"]["plan_state_digest"],
            "next_plan_basis_digest": next_artifacts["PlanOS"][
                "next_plan_basis_digest"
            ],
            "post_effect_blocker_certificate_digest": blocker[
                "post_effect_blocker_certificate_digest"
            ],
            "post_effect_world_projection_digest": world[
                "world_projection_digest"
            ],
        }
    )


def _successor_basis(closure: Mapping[str, Any]) -> dict[str, Any]:
    plan = dict(closure["next_cycle_artifacts"]["PlanOS"])
    blocker = dict(closure["post_effect_blocker_certificate"])
    world = dict(closure["post_effect_world_projection"])
    return {
        "next_plan_state_digest": plan["plan_state_digest"],
        "next_plan_basis_digest": plan["next_plan_basis_digest"],
        "next_committed_plan_digest": plan["latest_committed_plan_digest"],
        "post_effect_blocker_certificate_digest": blocker[
            "post_effect_blocker_certificate_digest"
        ],
        "post_effect_world_projection_digest": world[
            "world_projection_digest"
        ],
        "all_required_blockers_active": blocker[
            "all_required_blockers_active"
        ],
        "next_act_not_started": blocker["next_act_not_started"],
    }


def build_second_cycle_receipt(
    *,
    predecessor: Mapping[str, Any],
    handoff: Mapping[str, Any],
    closure: Mapping[str, Any],
) -> dict[str, Any]:
    execution_authority = dict(handoff["successor_execution_authority"])
    candidate = dict(handoff["freshness_candidate"])
    successor_basis = _successor_basis(closure)
    receipt = {
        "version": SECOND_CYCLE_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "source_successor_handoff": deepcopy(dict(handoff)),
        "source_successor_handoff_digest": handoff[
            "licensed_act_handoff_receipt_digest"
        ],
        "source_successor_closure": deepcopy(dict(closure)),
        "source_successor_closure_digest": closure[
            "successor_effect_evidence_closure_receipt_digest"
        ],
        "consumed_freshness_candidate_digest": candidate[
            "external_authority_packet_digest"
        ],
        "consumed_execution_authority_digest": execution_authority[
            "successor_execution_authority_digest"
        ],
        "consumed_human_approval_receipt_digest": execution_authority[
            "human_approval_receipt_digest"
        ],
        "consumed_host_license_digest": execution_authority[
            "host_license_digest"
        ],
        "terminal_state_digest": _terminal_state_digest(closure),
        "successor_basis": successor_basis,
        "successor_basis_digest": sha(successor_basis),
        "cycle_started": True,
        "effect_recorded": True,
        "observation_closed": True,
        "verification_closed": True,
        "learning_closed": True,
        "replan_closed": True,
        "cycle_closed": True,
        "closed_cycle_immutable": True,
        "closed_cycle_append_only": True,
        "receipt_replay_forbidden": True,
        "receipt_consumption_count": 0,
        "consumed_authority_single_use": True,
        "consumed_authority_renewable": False,
        "consumed_authority_inheritable": False,
        "successor_requires_fresh_external_authority": True,
        "successor_requires_distinct_authority_digest": True,
        "successor_requires_new_human_approval": True,
        "successor_requires_new_host_license": True,
        "next_act_started": False,
        "all_post_effect_blockers_active": True,
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(SECOND_CYCLE_NON_AUTHORITY),
        "second_cycle_receipt_digest": "",
    }
    receipt["second_cycle_receipt_digest"] = second_cycle_receipt_digest(receipt)
    errors = validate_second_cycle_receipt(receipt, predecessor=predecessor)
    if errors:
        raise ValueError("second_cycle_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_second_cycle_receipt(
    receipt: Mapping[str, Any],
    *,
    predecessor: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        errors.extend(
            "second_cycle_predecessor_" + error
            for error in validate_licensed_cycle_receipt(predecessor)
        )
        require(receipt.get("version") == SECOND_CYCLE_VERSION, "second_cycle_version_invalid")
        require(
            receipt.get("second_cycle_receipt_digest")
            == second_cycle_receipt_digest(receipt),
            "second_cycle_digest_invalid",
        )
        require(receipt.get("cycle_ordinal") == 2, "second_cycle_ordinal_invalid")
        require(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "second_cycle_predecessor_digest_mismatch",
        )
        handoff = dict(receipt.get("source_successor_handoff", {}))
        errors.extend(
            "second_cycle_handoff_" + error
            for error in validate_successor_licensed_act_handoff(handoff)
        )
        closure = dict(receipt.get("source_successor_closure", {}))
        errors.extend(
            "second_cycle_closure_" + error
            for error in validate_successor_effect_evidence_closure(closure)
        )
        require(
            receipt.get("source_successor_handoff_digest")
            == handoff.get("licensed_act_handoff_receipt_digest"),
            "second_cycle_handoff_digest_mismatch",
        )
        require(
            receipt.get("source_successor_closure_digest")
            == closure.get("successor_effect_evidence_closure_receipt_digest"),
            "second_cycle_closure_digest_mismatch",
        )
        require(
            dict(closure.get("source_successor_handoff", {})) == handoff,
            "second_cycle_handoff_closure_substitution",
        )
        execution_authority = dict(handoff.get("successor_execution_authority", {}))
        candidate = dict(handoff.get("freshness_candidate", {}))
        require(
            receipt.get("consumed_freshness_candidate_digest")
            == candidate.get("external_authority_packet_digest"),
            "second_cycle_candidate_digest_mismatch",
        )
        require(
            receipt.get("consumed_execution_authority_digest")
            == execution_authority.get("successor_execution_authority_digest"),
            "second_cycle_execution_authority_digest_mismatch",
        )
        require(
            receipt.get("consumed_human_approval_receipt_digest")
            == execution_authority.get("human_approval_receipt_digest"),
            "second_cycle_approval_digest_mismatch",
        )
        require(
            receipt.get("consumed_host_license_digest")
            == execution_authority.get("host_license_digest"),
            "second_cycle_host_digest_mismatch",
        )
        require(
            receipt.get("terminal_state_digest") == _terminal_state_digest(closure),
            "second_cycle_terminal_state_digest_mismatch",
        )
        basis = dict(receipt.get("successor_basis", {}))
        require(
            basis == _successor_basis(closure),
            "second_cycle_successor_basis_substitution",
        )
        require(
            receipt.get("successor_basis_digest") == sha(basis),
            "second_cycle_successor_basis_digest_invalid",
        )
        blocker = dict(closure.get("post_effect_blocker_certificate", {}))
        require(
            blocker.get("all_required_blockers_active") is True
            and blocker.get("missing_blockers") == [],
            "second_cycle_terminal_blockers_not_all_active",
        )
        expected_flags = {
            "cycle_started": True,
            "effect_recorded": True,
            "observation_closed": True,
            "verification_closed": True,
            "learning_closed": True,
            "replan_closed": True,
            "cycle_closed": True,
            "closed_cycle_immutable": True,
            "closed_cycle_append_only": True,
            "receipt_replay_forbidden": True,
            "consumed_authority_single_use": True,
            "consumed_authority_renewable": False,
            "consumed_authority_inheritable": False,
            "successor_requires_fresh_external_authority": True,
            "successor_requires_distinct_authority_digest": True,
            "successor_requires_new_human_approval": True,
            "successor_requires_new_host_license": True,
            "next_act_started": False,
            "all_post_effect_blockers_active": True,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected_flags.items():
            require(receipt.get(field) == value, f"second_cycle_{field}_invalid")
        require(
            receipt.get("receipt_consumption_count") == 0,
            "second_cycle_receipt_replay_or_consumption_forbidden",
        )
        require(
            dict(receipt.get("non_authority", {}))
            == SECOND_CYCLE_NON_AUTHORITY,
            "second_cycle_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _two_cycle_chain_digest(
    predecessor: Mapping[str, Any], second_cycle: Mapping[str, Any]
) -> str:
    return sha(
        {
            "first_cycle_ordinal": predecessor["cycle_ordinal"],
            "first_cycle_receipt_digest": predecessor[
                "licensed_cycle_receipt_digest"
            ],
            "second_cycle_ordinal": second_cycle["cycle_ordinal"],
            "second_cycle_receipt_digest": second_cycle[
                "second_cycle_receipt_digest"
            ],
            "second_cycle_predecessor_digest": second_cycle[
                "predecessor_cycle_receipt_digest"
            ],
            "first_terminal_state_digest": predecessor["terminal_state_digest"],
            "second_terminal_state_digest": second_cycle["terminal_state_digest"],
        }
    )


def build_successor_cycle_materialization_receipt(root: Path) -> dict[str, Any]:
    predecessor = build_licensed_cycle_receipt(root / "predecessor-v19")
    predecessor_errors = validate_licensed_cycle_receipt(predecessor)
    if predecessor_errors:
        raise ValueError("predecessor_v19_invalid:" + ";".join(predecessor_errors))
    requirement = build_successor_authority_requirement(predecessor)
    plan_state = _predecessor_plan(predecessor)
    policy, bundle, host_license, projection = host_inputs(
        job_id="qi-world-v20-job",
        expires_at_ms=280_000,
    )
    candidate = _build_fresh_authority_candidate(
        predecessor=predecessor,
        requirement=requirement,
        plan_state=plan_state,
        host_license=host_license,
    )
    intake = build_successor_authority_intake(
        requirement=requirement,
        closed_cycle_receipt=predecessor,
        candidate_external_authority_packet=candidate,
    )
    execution_authority = build_successor_execution_authority(
        predecessor=predecessor,
        requirement=requirement,
        intake=intake,
        freshness_candidate=candidate,
        plan_state=plan_state,
        host_license=host_license,
    )
    handoff = build_successor_licensed_act_handoff(
        root / "second-handoff",
        predecessor=predecessor,
        requirement=requirement,
        intake=intake,
        freshness_candidate=candidate,
        execution_authority=execution_authority,
        plan_state=plan_state,
        host_license=host_license,
        supervisor_policy=policy,
        supervisor_bundle=bundle,
        host_projection=projection,
    )
    closure = build_successor_effect_evidence_closure(
        root / "second-closure",
        handoff=handoff,
    )
    second_cycle = build_second_cycle_receipt(
        predecessor=predecessor,
        handoff=handoff,
        closure=closure,
    )
    chain_digest = _two_cycle_chain_digest(predecessor, second_cycle)
    receipt = {
        "version": MATERIALIZATION_VERSION,
        "cycle_id": CYCLE_ID,
        "first_cycle_receipt": deepcopy(predecessor),
        "first_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "successor_authority_requirement": deepcopy(requirement),
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "freshness_candidate": deepcopy(candidate),
        "freshness_candidate_digest": candidate[
            "external_authority_packet_digest"
        ],
        "successor_authority_intake": deepcopy(intake),
        "successor_authority_intake_digest": intake[
            "successor_authority_intake_digest"
        ],
        "successor_execution_authority": deepcopy(execution_authority),
        "successor_execution_authority_digest": execution_authority[
            "successor_execution_authority_digest"
        ],
        "second_cycle_handoff": deepcopy(handoff),
        "second_cycle_handoff_digest": handoff[
            "licensed_act_handoff_receipt_digest"
        ],
        "second_cycle_closure": deepcopy(closure),
        "second_cycle_closure_digest": closure[
            "successor_effect_evidence_closure_receipt_digest"
        ],
        "second_cycle_receipt": deepcopy(second_cycle),
        "second_cycle_receipt_digest": second_cycle[
            "second_cycle_receipt_digest"
        ],
        "two_cycle_chain_digest": chain_digest,
        "closed_cycle_count": 2,
        "cycle_ordinals": [1, 2],
        "authority_digests_distinct": True,
        "human_approval_digests_distinct": True,
        "host_license_digests_distinct": True,
        "first_cycle_receipt_read_only": True,
        "freshness_candidate_read_only": True,
        "successor_execution_authority_single_use": True,
        "second_cycle_materialized": True,
        "second_effect_recorded": True,
        "second_evidence_closed": True,
        "second_cycle_closed": True,
        "second_next_act_started": False,
        "all_second_post_effect_blockers_active": True,
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "multi_world_collapsed": False,
        "non_authority": deepcopy(MATERIALIZATION_NON_AUTHORITY),
        "successor_cycle_materialization_receipt_digest": "",
    }
    receipt["successor_cycle_materialization_receipt_digest"] = (
        materialization_receipt_digest(receipt)
    )
    errors = validate_successor_cycle_materialization_receipt(receipt)
    if errors:
        raise ValueError("successor_materialization_invalid:" + ";".join(errors))
    return receipt


def validate_successor_cycle_materialization_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(
            receipt.get("version") == MATERIALIZATION_VERSION,
            "materialization_version_invalid",
        )
        require(
            receipt.get("successor_cycle_materialization_receipt_digest")
            == materialization_receipt_digest(receipt),
            "materialization_digest_invalid",
        )
        predecessor = dict(receipt.get("first_cycle_receipt", {}))
        errors.extend(
            "materialization_first_" + error
            for error in validate_licensed_cycle_receipt(predecessor)
        )
        require(
            receipt.get("first_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "materialization_first_digest_mismatch",
        )
        requirement = dict(receipt.get("successor_authority_requirement", {}))
        errors.extend(
            "materialization_requirement_" + error
            for error in validate_successor_authority_requirement(
                requirement,
                closed_cycle_receipt=predecessor,
            )
        )
        candidate = dict(receipt.get("freshness_candidate", {}))
        intake = dict(receipt.get("successor_authority_intake", {}))
        errors.extend(
            "materialization_intake_" + error
            for error in validate_successor_authority_intake(
                intake,
                requirement=requirement,
                closed_cycle_receipt=predecessor,
                candidate_external_authority_packet=candidate,
            )
        )
        handoff = dict(receipt.get("second_cycle_handoff", {}))
        errors.extend(
            "materialization_handoff_" + error
            for error in validate_successor_licensed_act_handoff(handoff)
        )
        closure = dict(receipt.get("second_cycle_closure", {}))
        errors.extend(
            "materialization_closure_" + error
            for error in validate_successor_effect_evidence_closure(closure)
        )
        second_cycle = dict(receipt.get("second_cycle_receipt", {}))
        errors.extend(
            "materialization_second_" + error
            for error in validate_second_cycle_receipt(
                second_cycle,
                predecessor=predecessor,
            )
        )
        expected_digests = {
            "successor_authority_requirement_digest": requirement.get(
                "successor_authority_requirement_digest"
            ),
            "freshness_candidate_digest": candidate.get(
                "external_authority_packet_digest"
            ),
            "successor_authority_intake_digest": intake.get(
                "successor_authority_intake_digest"
            ),
            "successor_execution_authority_digest": dict(
                receipt.get("successor_execution_authority", {})
            ).get("successor_execution_authority_digest"),
            "second_cycle_handoff_digest": handoff.get(
                "licensed_act_handoff_receipt_digest"
            ),
            "second_cycle_closure_digest": closure.get(
                "successor_effect_evidence_closure_receipt_digest"
            ),
            "second_cycle_receipt_digest": second_cycle.get(
                "second_cycle_receipt_digest"
            ),
        }
        for field, value in expected_digests.items():
            require(receipt.get(field) == value, f"materialization_{field}_invalid")
        execution_authority = dict(
            receipt.get("successor_execution_authority", {})
        )
        require(
            dict(handoff.get("successor_execution_authority", {}))
            == execution_authority,
            "materialization_execution_authority_substitution",
        )
        require(
            dict(closure.get("source_successor_handoff", {})) == handoff,
            "materialization_handoff_closure_substitution",
        )
        require(
            dict(second_cycle.get("source_successor_closure", {})) == closure,
            "materialization_closure_cycle_substitution",
        )
        require(
            second_cycle.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "materialization_chain_predecessor_mismatch",
        )
        require(
            receipt.get("two_cycle_chain_digest")
            == _two_cycle_chain_digest(predecessor, second_cycle),
            "materialization_chain_digest_invalid",
        )
        require(
            predecessor.get("consumed_external_authority_packet_digest")
            != execution_authority.get("successor_execution_authority_digest"),
            "materialization_authority_reuse",
        )
        require(
            predecessor.get("consumed_human_approval_receipt_digest")
            != execution_authority.get("human_approval_receipt_digest"),
            "materialization_approval_reuse",
        )
        require(
            predecessor.get("consumed_host_license_digest")
            != execution_authority.get("host_license_digest"),
            "materialization_host_reuse",
        )
        require(
            receipt.get("closed_cycle_count") == 2,
            "materialization_closed_cycle_count_invalid",
        )
        require(
            receipt.get("cycle_ordinals") == [1, 2],
            "materialization_cycle_ordinals_invalid",
        )
        expected_flags = {
            "authority_digests_distinct": True,
            "human_approval_digests_distinct": True,
            "host_license_digests_distinct": True,
            "first_cycle_receipt_read_only": True,
            "freshness_candidate_read_only": True,
            "successor_execution_authority_single_use": True,
            "second_cycle_materialized": True,
            "second_effect_recorded": True,
            "second_evidence_closed": True,
            "second_cycle_closed": True,
            "second_next_act_started": False,
            "all_second_post_effect_blockers_active": True,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
            "multi_world_collapsed": False,
        }
        for field, value in expected_flags.items():
            require(receipt.get(field) == value, f"materialization_{field}_invalid")
        require(
            dict(receipt.get("non_authority", {}))
            == MATERIALIZATION_NON_AUTHORITY,
            "materialization_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
