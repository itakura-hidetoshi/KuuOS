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
from runtime.kuuos_qi_world_cross_cycle_blocker_v1_5 import (
    BLOCKER_ORDER,
    blocker_receipt_digest,
    build_cross_cycle_blocker_receipt,
    validate_cross_cycle_blocker_receipt,
)
from runtime.v017_host_adapter_fixtures import registry

VERSION = "kuuos_qi_world_licensed_blocker_discharge_v1_6"
AUTHORITY_VERSION = "kuuos_qi_world_external_authority_packet_v1_6"
DISCHARGE_VERSION = "kuuos_qi_world_blocker_discharge_certificate_v1_6"
RECEIPT_VERSION = "kuuos_qi_world_licensed_act_handoff_receipt_v1_6"
CYCLE_ID = "qi-world-licensed-blocker-discharge-v16"

RELEASABLE_BLOCKERS = (
    "present_activation_blocker",
    "execution_authority_blocker",
)

INVARIANT_BLOCKERS = tuple(
    name for name in BLOCKER_ORDER if name not in set(RELEASABLE_BLOCKERS)
)

RELEASE_SCOPE = {
    "operation_id": "fixture.success",
    "selected_step_id": "act-candidate",
    "maximum_invocations": 1,
    "maximum_effectful_steps": 1,
    "target_cycle_only": True,
}

RELEASE_NON_AUTHORITY = {
    "release_grants_truth": False,
    "release_grants_world_identity": False,
    "release_grants_memory_overwrite": False,
    "release_grants_plan_completion": False,
    "release_grants_automatic_rollback": False,
    "release_issues_further_authority": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def authority_packet_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "external_authority_packet_digest")


def discharge_certificate_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "blocker_discharge_certificate_digest")


def licensed_handoff_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "licensed_act_handoff_receipt_digest")


def build_external_authority_packet(
    *,
    source_blocker_receipt: Mapping[str, Any],
    plan_state: Mapping[str, Any],
    host_license: Mapping[str, Any],
    human_approval_receipt_digest: str,
    human_approver_id: str,
    issued_at_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    if validate_cross_cycle_blocker_receipt(source_blocker_receipt):
        raise ValueError("source_blocker_receipt_invalid")
    if expires_at_ms <= issued_at_ms:
        raise ValueError("external_authority_expiry_invalid")
    packet = {
        "version": AUTHORITY_VERSION,
        "authority_id": "qi-world-v16-external-authority",
        "external_issuer": True,
        "self_issued": False,
        "source_blocker_receipt_digest": source_blocker_receipt[
            "cross_cycle_blocker_receipt_digest"
        ],
        "source_blocker_certificate_digest": source_blocker_receipt[
            "blocker_certificate"
        ]["blocker_certificate_digest"],
        "source_plan_state_digest": plan_state["plan_state_digest"],
        "source_plan_basis_digest": plan_state["plan_basis_digest"],
        "source_committed_plan_digest": plan_state[
            "latest_committed_plan_digest"
        ],
        "host_license_digest": host_license["host_license_digest"],
        "human_approval_receipt_digest": human_approval_receipt_digest,
        "human_approver_id": human_approver_id,
        "released_blockers": list(RELEASABLE_BLOCKERS),
        "retained_invariant_blockers": list(INVARIANT_BLOCKERS),
        "release_scope": deepcopy(RELEASE_SCOPE),
        "single_use": True,
        "authority_does_not_widen_host_license": True,
        "target_cycle_strictly_later": True,
        "issued_at_ms": issued_at_ms,
        "expires_at_ms": expires_at_ms,
        "non_authority": deepcopy(RELEASE_NON_AUTHORITY),
        "external_authority_packet_digest": "",
    }
    packet["external_authority_packet_digest"] = authority_packet_digest(packet)
    return packet


def validate_external_authority_packet(
    packet: Mapping[str, Any],
    *,
    source_blocker_receipt: Mapping[str, Any],
    plan_state: Mapping[str, Any],
    host_license: Mapping[str, Any],
    now_ms: int,
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(packet.get("version") == AUTHORITY_VERSION, "authority_version_invalid")
        require(
            packet.get("external_authority_packet_digest")
            == authority_packet_digest(packet),
            "authority_digest_invalid",
        )
        require(packet.get("external_issuer") is True, "authority_external_issuer_required")
        require(packet.get("self_issued") is False, "authority_self_issue_forbidden")
        require(packet.get("single_use") is True, "authority_single_use_required")
        require(
            packet.get("authority_does_not_widen_host_license") is True,
            "authority_license_widening_forbidden",
        )
        require(
            packet.get("target_cycle_strictly_later") is True,
            "authority_target_cycle_not_later",
        )
        require(
            packet.get("source_blocker_receipt_digest")
            == source_blocker_receipt.get("cross_cycle_blocker_receipt_digest"),
            "authority_source_blocker_receipt_mismatch",
        )
        require(
            packet.get("source_blocker_certificate_digest")
            == dict(source_blocker_receipt.get("blocker_certificate", {})).get(
                "blocker_certificate_digest"
            ),
            "authority_source_blocker_certificate_mismatch",
        )
        require(
            packet.get("source_plan_state_digest") == plan_state.get("plan_state_digest"),
            "authority_source_plan_state_mismatch",
        )
        require(
            packet.get("source_plan_basis_digest") == plan_state.get("plan_basis_digest"),
            "authority_source_plan_basis_mismatch",
        )
        require(
            packet.get("source_committed_plan_digest")
            == plan_state.get("latest_committed_plan_digest"),
            "authority_source_committed_plan_mismatch",
        )
        require(
            packet.get("host_license_digest") == host_license.get("host_license_digest"),
            "authority_host_license_mismatch",
        )
        require(
            bool(str(packet.get("human_approval_receipt_digest", ""))),
            "authority_human_approval_required",
        )
        require(
            bool(str(packet.get("human_approver_id", ""))),
            "authority_human_approver_required",
        )
        require(
            list(packet.get("released_blockers", [])) == list(RELEASABLE_BLOCKERS),
            "authority_released_blocker_inventory_invalid",
        )
        require(
            list(packet.get("retained_invariant_blockers", []))
            == list(INVARIANT_BLOCKERS),
            "authority_invariant_blocker_inventory_invalid",
        )
        require(
            dict(packet.get("release_scope", {})) == RELEASE_SCOPE,
            "authority_release_scope_invalid",
        )
        require(
            int(packet.get("issued_at_ms", -1)) <= now_ms,
            "authority_not_yet_valid",
        )
        require(
            int(packet.get("expires_at_ms", 0)) > now_ms,
            "authority_expired",
        )
        require(
            dict(packet.get("non_authority", {})) == RELEASE_NON_AUTHORITY,
            "authority_non_authority_invalid",
        )
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _build_act_handoff(
    root: Path,
    *,
    source_blocker_receipt: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    cross_cycle = source_blocker_receipt["source_cross_cycle_receipt"]
    plan_state = cross_cycle["next_cycle_artifacts"]["PlanOS"]
    plan_activation = build_plan_phase_activation_receipt(
        state=plan_state,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=source_blocker_receipt[
            "cross_cycle_blocker_receipt_digest"
        ],
        plan_phase_receipt_digest=sha("qi-world-v16-plan-phase"),
        now_ms=90_000,
    )

    policy, bundle, host_license, projection = host_inputs(
        job_id="qi-world-v16-job",
        expires_at_ms=180_000,
    )
    human_approval = sha("qi-world-v16-human-approval")
    human_approver = "external-human-operator"
    external_authority = build_external_authority_packet(
        source_blocker_receipt=source_blocker_receipt,
        plan_state=plan_state,
        host_license=host_license,
        human_approval_receipt_digest=human_approval,
        human_approver_id=human_approver,
        issued_at_ms=90_000,
        expires_at_ms=180_000,
    )
    authority_errors = validate_external_authority_packet(
        external_authority,
        source_blocker_receipt=source_blocker_receipt,
        plan_state=plan_state,
        host_license=host_license,
        now_ms=90_002,
    )
    if authority_errors:
        raise ValueError("external_authority_invalid:" + ";".join(authority_errors))

    store = ActStore(root)
    state = store.initialize(
        build_initial_act_state(
            act_id="qi-world-v16-act",
            plan_state=plan_state,
            plan_activation_receipt=plan_activation,
            now_ms=90_000,
        )
    )
    operation_input_digest = sha({"value": 1})
    state = apply_act(
        store,
        state,
        "select",
        {
            "plan_state": deepcopy(plan_state),
            "selected_step_id": RELEASE_SCOPE["selected_step_id"],
            "operation_id": RELEASE_SCOPE["operation_id"],
            "operation_input_digest": operation_input_digest,
        },
        1,
    )
    authorization = build_step_authorization(
        state=state,
        authorization_id="qi-world-v16-step-authorization",
        operation_id=RELEASE_SCOPE["operation_id"],
        operation_input_digest=operation_input_digest,
        act_phase_receipt_digest=external_authority[
            "external_authority_packet_digest"
        ],
        invocation_id="qi-world-v16-single-invocation",
        source_supervisor_bundle_digest=projection[
            "source_supervisor_bundle_digest"
        ],
        host_job_id="qi-world-v16-job",
        host_step_id="step-1",
        host_license=host_license,
        human_approval_receipt_digest=human_approval,
        human_approver_id=human_approver,
        issued_at_ms=90_000,
        expires_at_ms=180_000,
    )
    state = apply_act(
        store,
        state,
        "authorize",
        {
            "step_authorization": authorization,
            "host_license": deepcopy(host_license),
        },
        2,
    )
    state = apply_act(
        store,
        state,
        "project",
        {"host_projection": deepcopy(projection)},
        3,
    )
    invoke_event, host_tick = build_authorized_invoke_event(
        state=state,
        supervisor_bundle=bundle,
        worker_id="qi-world-v16-worker",
        now_ms=90_004,
        supervisor_policy=policy,
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
        {"verification_receipt_digest": sha("qi-world-v16-act-verification")},
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
    return state, plan_activation, external_authority, host_tick


def build_blocker_discharge_certificate(
    *,
    source_blocker_receipt: Mapping[str, Any],
    external_authority: Mapping[str, Any],
    act_state: Mapping[str, Any],
) -> dict[str, Any]:
    source_certificate = source_blocker_receipt["blocker_certificate"]
    vector = source_certificate["composed_blocker_vector"]
    retained = {
        name: vector.get(name) is True for name in INVARIANT_BLOCKERS
    }
    certificate = {
        "version": DISCHARGE_VERSION,
        "source_blocker_receipt_digest": source_blocker_receipt[
            "cross_cycle_blocker_receipt_digest"
        ],
        "source_blocker_certificate_digest": source_certificate[
            "blocker_certificate_digest"
        ],
        "external_authority_packet_digest": external_authority[
            "external_authority_packet_digest"
        ],
        "released_blockers": list(RELEASABLE_BLOCKERS),
        "retained_invariant_blockers": retained,
        "all_invariant_blockers_retained": all(retained.values()),
        "source_blocker_certificate_immutable": True,
        "target_cycle_strictly_later": True,
        "single_use_release": True,
        "release_consumption_count": 1,
        "released_operation_id": act_state["operation_id"],
        "released_step_id": act_state["selected_step_id"],
        "released_act_state_digest": act_state["act_state_digest"],
        "effect_recorded": act_state["effect_recorded"],
        "observation_required": act_state["observation_required"],
        "verification_required": act_state["verification_required"],
        "memory_overwritten": False,
        "exact_world_updated": False,
        "truth_promoted": False,
        "same_cycle_recursive_invocation": False,
        "multi_world_collapsed": False,
        "non_authority": deepcopy(RELEASE_NON_AUTHORITY),
        "blocker_discharge_certificate_digest": "",
    }
    certificate["blocker_discharge_certificate_digest"] = (
        discharge_certificate_digest(certificate)
    )
    return certificate


def validate_blocker_discharge_certificate(
    certificate: Mapping[str, Any],
    *,
    source_blocker_receipt: Mapping[str, Any],
    external_authority: Mapping[str, Any],
    act_state: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        expected = build_blocker_discharge_certificate(
            source_blocker_receipt=source_blocker_receipt,
            external_authority=external_authority,
            act_state=act_state,
        )
        require(certificate.get("version") == DISCHARGE_VERSION, "discharge_version_invalid")
        require(
            certificate.get("blocker_discharge_certificate_digest")
            == discharge_certificate_digest(certificate),
            "discharge_digest_invalid",
        )
        for field in (
            "source_blocker_receipt_digest",
            "source_blocker_certificate_digest",
            "external_authority_packet_digest",
            "released_blockers",
            "retained_invariant_blockers",
            "all_invariant_blockers_retained",
            "source_blocker_certificate_immutable",
            "target_cycle_strictly_later",
            "single_use_release",
            "release_consumption_count",
            "released_operation_id",
            "released_step_id",
            "released_act_state_digest",
            "effect_recorded",
            "observation_required",
            "verification_required",
            "memory_overwritten",
            "exact_world_updated",
            "truth_promoted",
            "same_cycle_recursive_invocation",
            "multi_world_collapsed",
            "non_authority",
        ):
            require(certificate.get(field) == expected.get(field), f"discharge_{field}_invalid")
        require(certificate.get("release_consumption_count") == 1, "discharge_replay_or_multiuse")
        require(certificate.get("all_invariant_blockers_retained") is True, "discharge_invariant_loss")
        require(certificate.get("effect_recorded") is True, "discharge_effect_not_recorded")
        require(certificate.get("observation_required") is True, "discharge_observation_debt_missing")
        require(certificate.get("verification_required") is True, "discharge_verification_debt_missing")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_licensed_act_handoff_receipt(root: Path) -> dict[str, Any]:
    source = build_cross_cycle_blocker_receipt(root / "source-v15")
    source_errors = validate_cross_cycle_blocker_receipt(source)
    if source_errors:
        raise ValueError("source_v15_invalid:" + ";".join(source_errors))
    act_state, plan_activation, external_authority, host_tick = _build_act_handoff(
        root / "act-v16",
        source_blocker_receipt=source,
    )
    act_errors = validate_act_state(act_state)
    if act_errors:
        raise ValueError("act_state_invalid:" + ";".join(act_errors))
    discharge = build_blocker_discharge_certificate(
        source_blocker_receipt=source,
        external_authority=external_authority,
        act_state=act_state,
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "source_blocker_receipt": deepcopy(source),
        "source_blocker_receipt_digest": source[
            "cross_cycle_blocker_receipt_digest"
        ],
        "source_blocker_certificate_digest": source["blocker_certificate"][
            "blocker_certificate_digest"
        ],
        "plan_activation_receipt": deepcopy(plan_activation),
        "external_authority_packet": deepcopy(external_authority),
        "blocker_discharge_certificate": deepcopy(discharge),
        "target_act_state": deepcopy(act_state),
        "host_tick_digest": host_tick["host_tick_digest"],
        "source_cycle_immutable": True,
        "source_blocker_certificate_immutable": True,
        "target_cycle_strictly_later": True,
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
        "non_authority": deepcopy(RELEASE_NON_AUTHORITY),
        "licensed_act_handoff_receipt_digest": "",
    }
    receipt["licensed_act_handoff_receipt_digest"] = licensed_handoff_receipt_digest(
        receipt
    )
    errors = validate_licensed_act_handoff_receipt(receipt)
    if errors:
        raise ValueError("licensed_handoff_invalid:" + ";".join(errors))
    return receipt


def validate_licensed_act_handoff_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == RECEIPT_VERSION, "handoff_version_invalid")
        require(
            receipt.get("licensed_act_handoff_receipt_digest")
            == licensed_handoff_receipt_digest(receipt),
            "handoff_digest_invalid",
        )
        source = dict(receipt.get("source_blocker_receipt", {}))
        errors.extend("handoff_source_" + error for error in validate_cross_cycle_blocker_receipt(source))
        require(
            receipt.get("source_blocker_receipt_digest")
            == source.get("cross_cycle_blocker_receipt_digest"),
            "handoff_source_blocker_receipt_mismatch",
        )
        require(
            receipt.get("source_blocker_certificate_digest")
            == dict(source.get("blocker_certificate", {})).get(
                "blocker_certificate_digest"
            ),
            "handoff_source_blocker_certificate_mismatch",
        )
        cross_cycle = source["source_cross_cycle_receipt"]
        plan_state = cross_cycle["next_cycle_artifacts"]["PlanOS"]
        plan_activation = dict(receipt.get("plan_activation_receipt", {}))
        require(
            plan_activation.get("plan_state_digest") == plan_state.get("plan_state_digest"),
            "handoff_plan_activation_state_mismatch",
        )
        require(
            plan_activation.get("plan_not_execution") is True,
            "handoff_plan_activation_nonexecution_missing",
        )
        require(
            plan_activation.get("host_license_granted") is False,
            "handoff_plan_activation_license_escalation",
        )
        act_state = dict(receipt.get("target_act_state", {}))
        errors.extend("handoff_act_" + error for error in validate_act_state(act_state))
        require(act_state.get("current_phase") == "commit", "handoff_act_not_committed")
        require(act_state.get("route") == "EFFECT_RECORDED", "handoff_act_route_invalid")
        require(act_state.get("effect_recorded") is True, "handoff_effect_not_recorded")
        require(act_state.get("observation_required") is True, "handoff_observation_debt_missing")
        require(act_state.get("verification_required") is True, "handoff_verification_debt_missing")
        host_license = dict(act_state.get("host_license", {}))
        external_authority = dict(receipt.get("external_authority_packet", {}))
        errors.extend(
            "handoff_" + error
            for error in validate_external_authority_packet(
                external_authority,
                source_blocker_receipt=source,
                plan_state=plan_state,
                host_license=host_license,
                now_ms=90_002,
            )
        )
        discharge = dict(receipt.get("blocker_discharge_certificate", {}))
        errors.extend(
            "handoff_" + error
            for error in validate_blocker_discharge_certificate(
                discharge,
                source_blocker_receipt=source,
                external_authority=external_authority,
                act_state=act_state,
            )
        )
        for field, expected in {
            "source_cycle_immutable": True,
            "source_blocker_certificate_immutable": True,
            "target_cycle_strictly_later": True,
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
        }.items():
            require(receipt.get(field) == expected, f"handoff_{field}_invalid")
        require(
            dict(receipt.get("non_authority", {})) == RELEASE_NON_AUTHORITY,
            "handoff_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
