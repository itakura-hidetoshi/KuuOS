from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime import kuuos_qi_world_licensed_effect_evidence_closure_v1_8 as _closure_core
from runtime import kuuos_qi_world_cross_cycle_reentry_v1_4_new as _reentry
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
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_plan_phase_activation_receipt,
    validate_plan_state,
)
from runtime.kuuos_qi_world_cross_cycle_blocker_v1_5 import (
    BLOCKED_CAPABILITY_BY_BLOCKER,
    BLOCKER_ORDER,
)
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    AUTHORITY_VERSION,
    INVARIANT_BLOCKERS,
    RELEASE_NON_AUTHORITY,
    RELEASE_SCOPE,
    RELEASABLE_BLOCKERS,
    authority_packet_digest,
    build_blocker_discharge_certificate,
    validate_blocker_discharge_certificate,
)
from runtime.kuuos_qi_world_licensed_cycle_receipt_public_v1_9 import (
    build_licensed_cycle_receipt,
    build_successor_authority_intake,
    build_successor_authority_requirement,
    validate_licensed_cycle_receipt,
    validate_successor_authority_intake,
    validate_successor_authority_requirement,
)
from runtime.kuuos_qi_world_licensed_effect_evidence_closure_public_v1_8 import (
    CLOSURE_NON_AUTHORITY,
    build_post_effect_blocker_certificate,
    validate_post_effect_blocker_certificate,
)
from runtime.v017_host_adapter_fixtures import registry

VERSION = "kuuos_qi_world_successor_licensed_cycle_materialization_v2_0"
SUCCESSOR_BLOCKER_CERTIFICATE_VERSION = (
    "kuuos_qi_world_successor_blocker_certificate_v2_0"
)
SUCCESSOR_BLOCKER_RECEIPT_VERSION = (
    "kuuos_qi_world_successor_blocker_receipt_v2_0"
)
SUCCESSOR_HANDOFF_VERSION = (
    "kuuos_qi_world_successor_licensed_act_handoff_receipt_v2_0"
)
SUCCESSOR_CLOSURE_VERSION = (
    "kuuos_qi_world_successor_effect_evidence_closure_receipt_v2_0"
)
SECOND_CYCLE_VERSION = "kuuos_qi_world_second_closed_cycle_receipt_v2_0"
MATERIALIZATION_VERSION = (
    "kuuos_qi_world_successor_cycle_materialization_receipt_v2_0"
)
CYCLE_ID = "qi-world-successor-cycle-materialization-v20"

SUCCESSOR_BLOCKER_NON_AUTHORITY = {
    "blocker_grants_execution": False,
    "blocker_grants_truth": False,
    "blocker_issues_authority": False,
    "blocker_starts_act": False,
    "blocker_updates_exact_world": False,
    "blocker_overwrites_predecessor": False,
}

MATERIALIZATION_NON_AUTHORITY = {
    "materialization_self_issues_authority": False,
    "materialization_reuses_predecessor_authority": False,
    "materialization_grants_truth": False,
    "materialization_updates_exact_world": False,
    "materialization_overwrites_predecessor": False,
    "materialization_collapses_worlds": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def successor_blocker_certificate_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_blocker_certificate_digest")


def successor_blocker_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_blocker_receipt_digest")


def successor_handoff_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "licensed_act_handoff_receipt_digest")


def successor_closure_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(
        value, "licensed_effect_evidence_closure_receipt_digest"
    )


def second_cycle_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "second_cycle_receipt_digest")


def materialization_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_cycle_materialization_receipt_digest")


def _require_all_blockers(vector: Mapping[str, Any]) -> bool:
    return all(vector.get(name) is True for name in BLOCKER_ORDER)


def build_successor_blocker_receipt(
    predecessor_cycle_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    predecessor_errors = validate_licensed_cycle_receipt(
        predecessor_cycle_receipt
    )
    if predecessor_errors:
        raise ValueError(
            "predecessor_cycle_invalid:" + ";".join(predecessor_errors)
        )
    closure = dict(predecessor_cycle_receipt["source_v18_closure_receipt"])
    post = dict(closure["post_effect_blocker_certificate"])
    plan = dict(closure["next_cycle_artifacts"]["PlanOS"])
    plan_errors = validate_plan_state(plan)
    if plan_errors:
        raise ValueError("successor_plan_invalid:" + ";".join(plan_errors))
    vector = dict(post["composed_blocker_vector"])
    if not _require_all_blockers(vector):
        raise ValueError("successor_source_blockers_not_all_active")

    certificate = {
        "version": SUCCESSOR_BLOCKER_CERTIFICATE_VERSION,
        "cycle_id": CYCLE_ID,
        "target_cycle_ordinal": 2,
        "predecessor_cycle_receipt_digest": predecessor_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "source_v18_closure_receipt_digest": closure[
            "licensed_effect_evidence_closure_receipt_digest"
        ],
        "source_post_effect_blocker_certificate_digest": post[
            "post_effect_blocker_certificate_digest"
        ],
        "source_plan_state_digest": plan["plan_state_digest"],
        "source_plan_basis_digest": plan["plan_basis_digest"],
        "source_next_plan_basis_digest": plan["next_plan_basis_digest"],
        "source_committed_plan_digest": plan["latest_committed_plan_digest"],
        "blocker_order": list(BLOCKER_ORDER),
        "composed_blocker_vector": deepcopy(vector),
        "active_blockers": list(BLOCKER_ORDER),
        "missing_blockers": [],
        "all_required_blockers_active": True,
        "blocked_capabilities": [
            BLOCKED_CAPABILITY_BY_BLOCKER[name] for name in BLOCKER_ORDER
        ],
        "disposition": "BLOCKED_PENDING_FRESH_SUCCESSOR_AUTHORITY",
        "predecessor_cycle_immutable": True,
        "next_act_not_started": True,
        "non_authority": deepcopy(SUCCESSOR_BLOCKER_NON_AUTHORITY),
        "successor_blocker_certificate_digest": "",
    }
    certificate["successor_blocker_certificate_digest"] = (
        successor_blocker_certificate_digest(certificate)
    )
    receipt = {
        "version": SUCCESSOR_BLOCKER_RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "target_cycle_ordinal": 2,
        "predecessor_cycle_receipt": deepcopy(
            dict(predecessor_cycle_receipt)
        ),
        "predecessor_cycle_receipt_digest": predecessor_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "source_v18_closure_receipt_digest": closure[
            "licensed_effect_evidence_closure_receipt_digest"
        ],
        "source_post_effect_blocker_certificate_digest": post[
            "post_effect_blocker_certificate_digest"
        ],
        "source_next_plan_state": deepcopy(plan),
        "blocker_certificate": certificate,
        "all_required_blockers_active": True,
        "unlicensed_transition_blocked": True,
        "next_act_started": False,
        "exact_world_updated": False,
        "predecessor_cycle_overwritten": False,
        "recursive_self_invocation_started": False,
        "non_authority": deepcopy(SUCCESSOR_BLOCKER_NON_AUTHORITY),
        "successor_blocker_receipt_digest": "",
    }
    receipt["successor_blocker_receipt_digest"] = (
        successor_blocker_receipt_digest(receipt)
    )
    errors = validate_successor_blocker_receipt(receipt)
    if errors:
        raise ValueError("successor_blocker_invalid:" + ";".join(errors))
    return receipt


def validate_successor_blocker_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(
            receipt.get("version") == SUCCESSOR_BLOCKER_RECEIPT_VERSION,
            "successor_blocker_receipt_version_invalid",
        )
        require(
            receipt.get("successor_blocker_receipt_digest")
            == successor_blocker_receipt_digest(receipt),
            "successor_blocker_receipt_digest_invalid",
        )
        predecessor = dict(receipt.get("predecessor_cycle_receipt", {}))
        errors.extend(
            "successor_blocker_predecessor_" + error
            for error in validate_licensed_cycle_receipt(predecessor)
        )
        require(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "successor_blocker_predecessor_digest_mismatch",
        )
        closure = dict(predecessor.get("source_v18_closure_receipt", {}))
        post = dict(closure.get("post_effect_blocker_certificate", {}))
        plan = dict(closure.get("next_cycle_artifacts", {}).get("PlanOS", {}))
        errors.extend(
            "successor_blocker_plan_" + error
            for error in validate_plan_state(plan)
        )
        require(
            receipt.get("source_v18_closure_receipt_digest")
            == closure.get("licensed_effect_evidence_closure_receipt_digest"),
            "successor_blocker_closure_digest_mismatch",
        )
        require(
            receipt.get("source_post_effect_blocker_certificate_digest")
            == post.get("post_effect_blocker_certificate_digest"),
            "successor_blocker_post_effect_digest_mismatch",
        )
        require(
            dict(receipt.get("source_next_plan_state", {})) == plan,
            "successor_blocker_plan_substitution",
        )
        certificate = dict(receipt.get("blocker_certificate", {}))
        require(
            certificate.get("version")
            == SUCCESSOR_BLOCKER_CERTIFICATE_VERSION,
            "successor_blocker_certificate_version_invalid",
        )
        require(
            certificate.get("successor_blocker_certificate_digest")
            == successor_blocker_certificate_digest(certificate),
            "successor_blocker_certificate_digest_invalid",
        )
        expected = {
            "predecessor_cycle_receipt_digest": predecessor.get(
                "licensed_cycle_receipt_digest"
            ),
            "source_v18_closure_receipt_digest": closure.get(
                "licensed_effect_evidence_closure_receipt_digest"
            ),
            "source_post_effect_blocker_certificate_digest": post.get(
                "post_effect_blocker_certificate_digest"
            ),
            "source_plan_state_digest": plan.get("plan_state_digest"),
            "source_plan_basis_digest": plan.get("plan_basis_digest"),
            "source_next_plan_basis_digest": plan.get(
                "next_plan_basis_digest"
            ),
            "source_committed_plan_digest": plan.get(
                "latest_committed_plan_digest"
            ),
        }
        for field, value in expected.items():
            require(
                certificate.get(field) == value,
                f"successor_blocker_certificate_{field}_invalid",
            )
        source_vector = dict(post.get("composed_blocker_vector", {}))
        require(
            _require_all_blockers(source_vector),
            "successor_blocker_source_vector_not_all_active",
        )
        require(
            dict(certificate.get("composed_blocker_vector", {}))
            == source_vector,
            "successor_blocker_vector_substitution",
        )
        require(
            certificate.get("blocker_order") == list(BLOCKER_ORDER),
            "successor_blocker_order_invalid",
        )
        require(
            certificate.get("active_blockers") == list(BLOCKER_ORDER),
            "successor_blocker_active_inventory_invalid",
        )
        require(
            certificate.get("missing_blockers") == [],
            "successor_blocker_missing_inventory_invalid",
        )
        require(
            certificate.get("all_required_blockers_active") is True,
            "successor_blocker_not_all_active",
        )
        require(
            certificate.get("blocked_capabilities")
            == [BLOCKED_CAPABILITY_BY_BLOCKER[name] for name in BLOCKER_ORDER],
            "successor_blocker_capability_inventory_invalid",
        )
        require(
            certificate.get("disposition")
            == "BLOCKED_PENDING_FRESH_SUCCESSOR_AUTHORITY",
            "successor_blocker_disposition_invalid",
        )
        require(
            dict(certificate.get("non_authority", {}))
            == SUCCESSOR_BLOCKER_NON_AUTHORITY,
            "successor_blocker_certificate_non_authority_invalid",
        )
        for field, expected_value in {
            "all_required_blockers_active": True,
            "unlicensed_transition_blocked": True,
            "next_act_started": False,
            "exact_world_updated": False,
            "predecessor_cycle_overwritten": False,
            "recursive_self_invocation_started": False,
        }.items():
            require(
                receipt.get(field) is expected_value,
                f"successor_blocker_{field}_invalid",
            )
        require(
            dict(receipt.get("non_authority", {}))
            == SUCCESSOR_BLOCKER_NON_AUTHORITY,
            "successor_blocker_receipt_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _build_fresh_authority(
    *,
    predecessor_cycle_receipt: Mapping[str, Any],
    successor_blocker_receipt: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> dict[str, Any]:
    plan = dict(successor_blocker_receipt["source_next_plan_state"])
    previous = dict(
        predecessor_cycle_receipt["source_v17_handoff_receipt"][
            "external_authority_packet"
        ]
    )
    packet = {
        "version": AUTHORITY_VERSION,
        "authority_id": "qi-world-v20-successor-external-authority",
        "external_issuer": True,
        "self_issued": False,
        "source_blocker_receipt_digest": successor_blocker_receipt[
            "successor_blocker_receipt_digest"
        ],
        "source_blocker_certificate_digest": successor_blocker_receipt[
            "blocker_certificate"
        ]["successor_blocker_certificate_digest"],
        "source_plan_state_digest": plan["plan_state_digest"],
        "source_plan_basis_digest": plan["plan_basis_digest"],
        "source_committed_plan_digest": plan["latest_committed_plan_digest"],
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
        "issued_at_ms": 290_000,
        "expires_at_ms": 480_000,
        "non_authority": deepcopy(RELEASE_NON_AUTHORITY),
        "external_authority_packet_digest": "",
    }
    packet["external_authority_packet_digest"] = authority_packet_digest(
        packet
    )
    if (
        packet["external_authority_packet_digest"]
        == previous["external_authority_packet_digest"]
    ):
        raise ValueError("successor_authority_digest_reuse_forbidden")
    if (
        packet["human_approval_receipt_digest"]
        == previous["human_approval_receipt_digest"]
    ):
        raise ValueError("successor_human_approval_reuse_forbidden")
    if packet["host_license_digest"] == previous["host_license_digest"]:
        raise ValueError("successor_host_license_reuse_forbidden")
    return packet


def validate_successor_external_authority(
    packet: Mapping[str, Any],
    *,
    predecessor_cycle_receipt: Mapping[str, Any],
    successor_blocker_receipt: Mapping[str, Any],
    host_license: Mapping[str, Any],
    now_ms: int,
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        errors.extend(
            "successor_authority_blocker_" + error
            for error in validate_successor_blocker_receipt(
                successor_blocker_receipt
            )
        )
        plan = dict(successor_blocker_receipt["source_next_plan_state"])
        previous = dict(
            predecessor_cycle_receipt["source_v17_handoff_receipt"][
                "external_authority_packet"
            ]
        )
        require(
            packet.get("version") == AUTHORITY_VERSION,
            "successor_authority_version_invalid",
        )
        require(
            packet.get("external_authority_packet_digest")
            == authority_packet_digest(packet),
            "successor_authority_digest_invalid",
        )
        require(
            packet.get("external_issuer") is True,
            "successor_authority_external_issuer_required",
        )
        require(
            packet.get("self_issued") is False,
            "successor_authority_self_issue_forbidden",
        )
        require(
            packet.get("single_use") is True,
            "successor_authority_single_use_required",
        )
        require(
            packet.get("authority_does_not_widen_host_license") is True,
            "successor_authority_license_widening_forbidden",
        )
        require(
            packet.get("target_cycle_strictly_later") is True,
            "successor_authority_target_cycle_not_later",
        )
        expected = {
            "source_blocker_receipt_digest": successor_blocker_receipt.get(
                "successor_blocker_receipt_digest"
            ),
            "source_blocker_certificate_digest": dict(
                successor_blocker_receipt.get("blocker_certificate", {})
            ).get("successor_blocker_certificate_digest"),
            "source_plan_state_digest": plan.get("plan_state_digest"),
            "source_plan_basis_digest": plan.get("plan_basis_digest"),
            "source_committed_plan_digest": plan.get(
                "latest_committed_plan_digest"
            ),
            "host_license_digest": host_license.get("host_license_digest"),
        }
        for field, value in expected.items():
            require(
                packet.get(field) == value,
                f"successor_authority_{field}_invalid",
            )
        require(
            packet.get("external_authority_packet_digest")
            != previous.get("external_authority_packet_digest"),
            "successor_authority_digest_reuse_forbidden",
        )
        require(
            packet.get("human_approval_receipt_digest")
            != previous.get("human_approval_receipt_digest"),
            "successor_human_approval_reuse_forbidden",
        )
        require(
            packet.get("host_license_digest")
            != previous.get("host_license_digest"),
            "successor_host_license_reuse_forbidden",
        )
        require(
            packet.get("released_blockers") == list(RELEASABLE_BLOCKERS),
            "successor_authority_released_inventory_invalid",
        )
        require(
            packet.get("retained_invariant_blockers")
            == list(INVARIANT_BLOCKERS),
            "successor_authority_invariant_inventory_invalid",
        )
        require(
            dict(packet.get("release_scope", {})) == RELEASE_SCOPE,
            "successor_authority_release_scope_invalid",
        )
        require(
            int(packet.get("issued_at_ms", -1)) <= now_ms,
            "successor_authority_not_yet_valid",
        )
        require(
            int(packet.get("expires_at_ms", 0)) > now_ms,
            "successor_authority_expired",
        )
        require(
            dict(packet.get("non_authority", {})) == RELEASE_NON_AUTHORITY,
            "successor_authority_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _build_second_act(
    root: Path,
    *,
    successor_blocker_receipt: Mapping[str, Any],
    external_authority: Mapping[str, Any],
    policy: Mapping[str, Any],
    bundle: Mapping[str, Any],
    host_license: Mapping[str, Any],
    projection: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = dict(successor_blocker_receipt["source_next_plan_state"])
    plan_activation = build_plan_phase_activation_receipt(
        state=plan,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=successor_blocker_receipt[
            "successor_blocker_receipt_digest"
        ],
        plan_phase_receipt_digest=sha("qi-world-v20-plan-phase"),
        now_ms=290_000,
    )
    store = ActStore(root)
    state = store.initialize(
        build_initial_act_state(
            act_id="qi-world-v20-second-act",
            plan_state=plan,
            plan_activation_receipt=plan_activation,
            now_ms=290_000,
        )
    )
    operation_input_digest = sha({"value": 2, "cycle_ordinal": 2})
    state = apply_act(
        store,
        state,
        "select",
        {
            "plan_state": deepcopy(plan),
            "selected_step_id": RELEASE_SCOPE["selected_step_id"],
            "operation_id": RELEASE_SCOPE["operation_id"],
            "operation_input_digest": operation_input_digest,
        },
        1,
    )
    authorization = build_step_authorization(
        state=state,
        authorization_id="qi-world-v20-step-authorization",
        operation_id=RELEASE_SCOPE["operation_id"],
        operation_input_digest=operation_input_digest,
        act_phase_receipt_digest=external_authority[
            "external_authority_packet_digest"
        ],
        invocation_id="qi-world-v20-single-invocation",
        source_supervisor_bundle_digest=projection[
            "source_supervisor_bundle_digest"
        ],
        host_job_id="qi-world-v20-job",
        host_step_id="step-2",
        host_license=host_license,
        human_approval_receipt_digest=external_authority[
            "human_approval_receipt_digest"
        ],
        human_approver_id=external_authority["human_approver_id"],
        issued_at_ms=290_000,
        expires_at_ms=480_000,
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
        {"host_projection": deepcopy(dict(projection))},
        3,
    )
    invoke_event, host_tick = build_authorized_invoke_event(
        state=state,
        supervisor_bundle=bundle,
        worker_id="qi-world-v20-worker",
        now_ms=290_004,
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
        {
            "verification_receipt_digest": sha(
                "qi-world-v20-act-verification"
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
        raise ValueError("successor_act_invalid:" + ";".join(errors))
    return state, plan_activation, host_tick


def _discharge_source(
    successor_blocker_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "cross_cycle_blocker_receipt_digest": successor_blocker_receipt[
            "successor_blocker_receipt_digest"
        ],
        "blocker_certificate": {
            "blocker_certificate_digest": successor_blocker_receipt[
                "blocker_certificate"
            ]["successor_blocker_certificate_digest"],
            "composed_blocker_vector": successor_blocker_receipt[
                "blocker_certificate"
            ]["composed_blocker_vector"],
        },
    }


def build_successor_handoff_receipt(
    root: Path,
    *,
    predecessor_cycle_receipt: Mapping[str, Any],
    successor_blocker_receipt: Mapping[str, Any],
    authority_requirement: Mapping[str, Any],
    authority_intake: Mapping[str, Any],
    external_authority: Mapping[str, Any],
    policy: Mapping[str, Any],
    bundle: Mapping[str, Any],
    host_license: Mapping[str, Any],
    projection: Mapping[str, Any],
) -> dict[str, Any]:
    act, activation, host_tick = _build_second_act(
        root / "act",
        successor_blocker_receipt=successor_blocker_receipt,
        external_authority=external_authority,
        policy=policy,
        bundle=bundle,
        host_license=host_license,
        projection=projection,
    )
    source_for_discharge = _discharge_source(successor_blocker_receipt)
    discharge = build_blocker_discharge_certificate(
        source_blocker_receipt=source_for_discharge,
        external_authority=external_authority,
        act_state=act,
    )
    discharge_errors = validate_blocker_discharge_certificate(
        discharge,
        source_blocker_receipt=source_for_discharge,
        external_authority=external_authority,
        act_state=act,
    )
    if discharge_errors:
        raise ValueError(
            "successor_discharge_invalid:" + ";".join(discharge_errors)
        )
    predecessor_handoff = dict(
        predecessor_cycle_receipt["source_v17_handoff_receipt"]
    )
    receipt = {
        "version": SUCCESSOR_HANDOFF_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_cycle_receipt_digest": predecessor_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "successor_authority_requirement_digest": authority_requirement[
            "successor_authority_requirement_digest"
        ],
        "successor_authority_intake_digest": authority_intake[
            "successor_authority_intake_digest"
        ],
        "source_blocker_receipt": deepcopy(
            dict(successor_blocker_receipt)
        ),
        "source_blocker_receipt_digest": successor_blocker_receipt[
            "successor_blocker_receipt_digest"
        ],
        "source_blocker_certificate_digest": successor_blocker_receipt[
            "blocker_certificate"
        ]["successor_blocker_certificate_digest"],
        "source_indra_transport_request_receipt": deepcopy(
            predecessor_handoff[
                "source_indra_transport_request_receipt"
            ]
        ),
        "source_indra_transport_request_receipt_digest": predecessor_handoff[
            "source_indra_transport_request_receipt_digest"
        ],
        "source_indra_transport_request_digest": predecessor_handoff[
            "source_indra_transport_request_digest"
        ],
        "indra_transport_disposition": predecessor_handoff[
            "indra_transport_disposition"
        ],
        "plan_activation_receipt": deepcopy(activation),
        "external_authority_packet": deepcopy(dict(external_authority)),
        "blocker_discharge_certificate": deepcopy(discharge),
        "target_act_state": deepcopy(act),
        "host_tick_digest": host_tick["host_tick_digest"],
        "host_license_digest": host_license["host_license_digest"],
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
        "external_authority_not_analytic_transport_receipt": True,
        "indra_transport_still_unrealized": True,
        "non_authority": deepcopy(RELEASE_NON_AUTHORITY),
        "licensed_act_handoff_receipt_digest": "",
    }
    receipt["licensed_act_handoff_receipt_digest"] = (
        successor_handoff_receipt_digest(receipt)
    )
    errors = validate_successor_handoff_receipt(
        receipt,
        predecessor_cycle_receipt=predecessor_cycle_receipt,
        authority_requirement=authority_requirement,
        authority_intake=authority_intake,
        host_license=host_license,
    )
    if errors:
        raise ValueError("successor_handoff_invalid:" + ";".join(errors))
    return receipt


def validate_successor_handoff_receipt(
    receipt: Mapping[str, Any],
    *,
    predecessor_cycle_receipt: Mapping[str, Any],
    authority_requirement: Mapping[str, Any],
    authority_intake: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        errors.extend(
            "successor_handoff_predecessor_" + error
            for error in validate_licensed_cycle_receipt(
                predecessor_cycle_receipt
            )
        )
        require(
            receipt.get("version") == SUCCESSOR_HANDOFF_VERSION,
            "successor_handoff_version_invalid",
        )
        require(
            receipt.get("licensed_act_handoff_receipt_digest")
            == successor_handoff_receipt_digest(receipt),
            "successor_handoff_digest_invalid",
        )
        require(
            receipt.get("cycle_ordinal") == 2,
            "successor_handoff_cycle_ordinal_invalid",
        )
        require(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor_cycle_receipt.get(
                "licensed_cycle_receipt_digest"
            ),
            "successor_handoff_predecessor_digest_mismatch",
        )
        require(
            receipt.get("successor_authority_requirement_digest")
            == authority_requirement.get(
                "successor_authority_requirement_digest"
            ),
            "successor_handoff_requirement_digest_mismatch",
        )
        require(
            receipt.get("successor_authority_intake_digest")
            == authority_intake.get("successor_authority_intake_digest"),
            "successor_handoff_intake_digest_mismatch",
        )
        blocker = dict(receipt.get("source_blocker_receipt", {}))
        errors.extend(
            "successor_handoff_blocker_" + error
            for error in validate_successor_blocker_receipt(blocker)
        )
        require(
            receipt.get("source_blocker_receipt_digest")
            == blocker.get("successor_blocker_receipt_digest"),
            "successor_handoff_blocker_digest_mismatch",
        )
        authority = dict(receipt.get("external_authority_packet", {}))
        errors.extend(
            "successor_handoff_authority_" + error
            for error in validate_successor_external_authority(
                authority,
                predecessor_cycle_receipt=predecessor_cycle_receipt,
                successor_blocker_receipt=blocker,
                host_license=host_license,
                now_ms=290_002,
            )
        )
        require(
            authority_intake.get(
                "candidate_external_authority_packet_digest"
            )
            == authority.get("external_authority_packet_digest"),
            "successor_handoff_intake_authority_mismatch",
        )
        act = dict(receipt.get("target_act_state", {}))
        errors.extend(
            "successor_handoff_act_" + error
            for error in validate_act_state(act)
        )
        plan = dict(blocker.get("source_next_plan_state", {}))
        require(
            act.get("source_plan_state_digest")
            == plan.get("plan_state_digest"),
            "successor_handoff_act_plan_state_mismatch",
        )
        authorization = dict(act.get("step_authorization", {}))
        require(
            authorization.get("act_phase_receipt_digest")
            == authority.get("external_authority_packet_digest"),
            "successor_handoff_step_authority_mismatch",
        )
        require(
            authorization.get("host_license_digest")
            == host_license.get("host_license_digest"),
            "successor_handoff_host_license_mismatch",
        )
        discharge = dict(
            receipt.get("blocker_discharge_certificate", {})
        )
        errors.extend(
            "successor_handoff_discharge_" + error
            for error in validate_blocker_discharge_certificate(
                discharge,
                source_blocker_receipt=_discharge_source(blocker),
                external_authority=authority,
                act_state=act,
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
            "external_authority_not_analytic_transport_receipt": True,
            "indra_transport_still_unrealized": True,
        }.items():
            require(
                receipt.get(field) == expected,
                f"successor_handoff_{field}_invalid",
            )
        require(
            dict(receipt.get("non_authority", {})) == RELEASE_NON_AUTHORITY,
            "successor_handoff_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_successor_closure_receipt(
    root: Path,
    *,
    successor_handoff_receipt: Mapping[str, Any],
    predecessor_cycle_receipt: Mapping[str, Any],
    authority_requirement: Mapping[str, Any],
    authority_intake: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> dict[str, Any]:
    handoff_errors = validate_successor_handoff_receipt(
        successor_handoff_receipt,
        predecessor_cycle_receipt=predecessor_cycle_receipt,
        authority_requirement=authority_requirement,
        authority_intake=authority_intake,
        host_license=host_license,
    )
    if handoff_errors:
        raise ValueError(
            "successor_handoff_invalid:" + ";".join(handoff_errors)
        )
    act = deepcopy(dict(successor_handoff_receipt["target_act_state"]))
    observe, verify, learn = _closure_core._build_downstream(
        root / "evidence", act
    )
    states = {
        "ActOS": act,
        "ObserveOS": observe,
        "VerifyOS": verify,
        "LearnOS": learn,
    }
    native_errors = _closure_core._native_validation_errors(states)
    if native_errors:
        raise ValueError(
            "successor_native_evidence_invalid:" + ";".join(native_errors)
        )
    lineage = _closure_core._evidence_lineage_digest(
        successor_handoff_receipt, states
    )
    next_artifacts = _closure_core._build_next_cycle(
        root / "next-cycle",
        source=successor_handoff_receipt,
        states=states,
        lineage_digest=lineage,
    )
    world = _closure_core._world_projection(
        successor_handoff_receipt, states, next_artifacts
    )
    qi = _closure_core._qi_receipt(states, next_artifacts)
    blocker = build_post_effect_blocker_certificate(
        source=successor_handoff_receipt,
        states=states,
        next_artifacts=next_artifacts,
        world=world,
    )
    receipt = {
        "version": SUCCESSOR_CLOSURE_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_cycle_receipt_digest": predecessor_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "source_licensed_handoff_receipt": deepcopy(
            dict(successor_handoff_receipt)
        ),
        "source_licensed_handoff_receipt_digest": successor_handoff_receipt[
            "licensed_act_handoff_receipt_digest"
        ],
        "native_evidence_states": deepcopy(states),
        "native_evidence_lineage_digest": lineage,
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
        "licensed_effect_evidence_closure_receipt_digest": "",
    }
    receipt["licensed_effect_evidence_closure_receipt_digest"] = (
        successor_closure_receipt_digest(receipt)
    )
    errors = validate_successor_closure_receipt(
        receipt,
        predecessor_cycle_receipt=predecessor_cycle_receipt,
        authority_requirement=authority_requirement,
        authority_intake=authority_intake,
        host_license=host_license,
    )
    if errors:
        raise ValueError("successor_closure_invalid:" + ";".join(errors))
    return receipt


def validate_successor_closure_receipt(
    receipt: Mapping[str, Any],
    *,
    predecessor_cycle_receipt: Mapping[str, Any],
    authority_requirement: Mapping[str, Any],
    authority_intake: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(
            receipt.get("version") == SUCCESSOR_CLOSURE_VERSION,
            "successor_closure_version_invalid",
        )
        require(
            receipt.get("licensed_effect_evidence_closure_receipt_digest")
            == successor_closure_receipt_digest(receipt),
            "successor_closure_digest_invalid",
        )
        require(
            receipt.get("cycle_ordinal") == 2,
            "successor_closure_cycle_ordinal_invalid",
        )
        require(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor_cycle_receipt.get(
                "licensed_cycle_receipt_digest"
            ),
            "successor_closure_predecessor_digest_mismatch",
        )
        handoff = dict(
            receipt.get("source_licensed_handoff_receipt", {})
        )
        errors.extend(
            "successor_closure_handoff_" + error
            for error in validate_successor_handoff_receipt(
                handoff,
                predecessor_cycle_receipt=predecessor_cycle_receipt,
                authority_requirement=authority_requirement,
                authority_intake=authority_intake,
                host_license=host_license,
            )
        )
        require(
            receipt.get("source_licensed_handoff_receipt_digest")
            == handoff.get("licensed_act_handoff_receipt_digest"),
            "successor_closure_handoff_digest_mismatch",
        )
        states = dict(receipt.get("native_evidence_states", {}))
        errors.extend(
            "successor_closure_" + error
            for error in _closure_core._native_validation_errors(states)
        )
        act = dict(states.get("ActOS", {}))
        observe = dict(states.get("ObserveOS", {}))
        verify = dict(states.get("VerifyOS", {}))
        learn = dict(states.get("LearnOS", {}))
        require(
            act == dict(handoff.get("target_act_state", {})),
            "successor_closure_act_substitution",
        )
        require(
            observe.get("source_act_state_digest")
            == act.get("act_state_digest"),
            "successor_closure_observe_act_mismatch",
        )
        require(
            verify.get("source_observe_state_digest")
            == observe.get("observe_state_digest"),
            "successor_closure_verify_observe_mismatch",
        )
        require(
            learn.get("source_verify_state_digest")
            == verify.get("verify_state_digest"),
            "successor_closure_learn_verify_mismatch",
        )
        delta = dict(learn.get("learning_delta", {}))
        require(
            delta.get("future_only") is True
            and delta.get("memory_overwrite") is False
            and learn.get("past_records_unchanged") is True,
            "successor_closure_learning_boundary_invalid",
        )
        require(
            receipt.get("native_evidence_lineage_digest")
            == _closure_core._evidence_lineage_digest(handoff, states),
            "successor_closure_lineage_digest_mismatch",
        )
        next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
        errors.extend(
            "successor_closure_next_" + error
            for error in _reentry._validate_next_artifacts(
                next_artifacts
            )
        )
        require(
            next_artifacts.get("PlanOS", {}).get(
                "next_plan_basis_digest"
            )
            == learn.get("learning_delta_digest"),
            "successor_closure_next_plan_basis_mismatch",
        )
        world = dict(receipt.get("post_effect_world_projection", {}))
        require(
            world.get("world_projection_digest")
            == _closure_core._digest_without(
                world, "world_projection_digest"
            ),
            "successor_closure_world_digest_invalid",
        )
        for field, expected in {
            "projection_read_only": True,
            "runtime_updates_world": False,
            "exact_world_identified": False,
            "indra_transport_still_unrealized": True,
            "multi_world_noncollapse": True,
            "two_truths_gap": True,
        }.items():
            require(
                world.get(field) == expected,
                f"successor_closure_world_{field}_invalid",
            )
        blocker = dict(
            receipt.get("post_effect_blocker_certificate", {})
        )
        errors.extend(
            validate_post_effect_blocker_certificate(
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
            "successor_closure_blocker_digest_mismatch",
        )
        require(
            blocker.get("all_required_blockers_active") is True
            and blocker.get("missing_blockers") == []
            and _require_all_blockers(
                dict(blocker.get("composed_blocker_vector", {}))
            ),
            "successor_closure_blockers_not_restored",
        )
        for field, expected in {
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
        }.items():
            require(
                receipt.get(field) == expected,
                f"successor_closure_{field}_invalid",
            )
        require(
            dict(receipt.get("non_authority", {}))
            == CLOSURE_NON_AUTHORITY,
            "successor_closure_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _terminal_digest(closure: Mapping[str, Any]) -> str:
    states = dict(closure["native_evidence_states"])
    plan = dict(closure["next_cycle_artifacts"]["PlanOS"])
    blocker = dict(closure["post_effect_blocker_certificate"])
    return sha(
        {
            "act_state_digest": states["ActOS"]["act_state_digest"],
            "observe_state_digest": states["ObserveOS"][
                "observe_state_digest"
            ],
            "verify_state_digest": states["VerifyOS"][
                "verify_state_digest"
            ],
            "learn_state_digest": states["LearnOS"]["learn_state_digest"],
            "learning_delta_digest": states["LearnOS"][
                "learning_delta_digest"
            ],
            "next_plan_state_digest": plan["plan_state_digest"],
            "post_effect_blocker_certificate_digest": blocker[
                "post_effect_blocker_certificate_digest"
            ],
        }
    )


def build_second_cycle_receipt(
    *,
    predecessor_cycle_receipt: Mapping[str, Any],
    successor_handoff_receipt: Mapping[str, Any],
    successor_closure_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    authority = dict(
        successor_handoff_receipt["external_authority_packet"]
    )
    plan = dict(
        successor_closure_receipt["next_cycle_artifacts"]["PlanOS"]
    )
    blocker = dict(
        successor_closure_receipt["post_effect_blocker_certificate"]
    )
    receipt = {
        "version": SECOND_CYCLE_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_cycle_receipt_digest": predecessor_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "source_successor_handoff_receipt_digest": successor_handoff_receipt[
            "licensed_act_handoff_receipt_digest"
        ],
        "source_successor_closure_receipt_digest": successor_closure_receipt[
            "licensed_effect_evidence_closure_receipt_digest"
        ],
        "consumed_external_authority_packet_digest": authority[
            "external_authority_packet_digest"
        ],
        "terminal_state_digest": _terminal_digest(
            successor_closure_receipt
        ),
        "successor_plan_state_digest": plan["plan_state_digest"],
        "successor_plan_basis_digest": plan["next_plan_basis_digest"],
        "post_effect_blocker_certificate_digest": blocker[
            "post_effect_blocker_certificate_digest"
        ],
        "cycle_closed": True,
        "closed_cycle_immutable": True,
        "closed_cycle_append_only": True,
        "receipt_replay_forbidden": True,
        "receipt_consumption_count": 0,
        "consumed_authority_single_use": True,
        "consumed_authority_renewable": False,
        "consumed_authority_inheritable": False,
        "all_post_effect_blockers_active": True,
        "next_act_started": False,
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "second_cycle_receipt_digest": "",
    }
    receipt["second_cycle_receipt_digest"] = second_cycle_receipt_digest(
        receipt
    )
    return receipt


def validate_second_cycle_receipt(
    receipt: Mapping[str, Any],
    *,
    predecessor_cycle_receipt: Mapping[str, Any],
    successor_handoff_receipt: Mapping[str, Any],
    successor_closure_receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(
            receipt.get("version") == SECOND_CYCLE_VERSION,
            "second_cycle_version_invalid",
        )
        require(
            receipt.get("second_cycle_receipt_digest")
            == second_cycle_receipt_digest(receipt),
            "second_cycle_digest_invalid",
        )
        expected = {
            "cycle_ordinal": 2,
            "predecessor_cycle_receipt_digest": predecessor_cycle_receipt.get(
                "licensed_cycle_receipt_digest"
            ),
            "source_successor_handoff_receipt_digest": successor_handoff_receipt.get(
                "licensed_act_handoff_receipt_digest"
            ),
            "source_successor_closure_receipt_digest": successor_closure_receipt.get(
                "licensed_effect_evidence_closure_receipt_digest"
            ),
            "consumed_external_authority_packet_digest": dict(
                successor_handoff_receipt.get(
                    "external_authority_packet", {}
                )
            ).get("external_authority_packet_digest"),
            "terminal_state_digest": _terminal_digest(
                successor_closure_receipt
            ),
            "successor_plan_state_digest": dict(
                successor_closure_receipt.get(
                    "next_cycle_artifacts", {}
                )
            )
            .get("PlanOS", {})
            .get("plan_state_digest"),
            "successor_plan_basis_digest": dict(
                successor_closure_receipt.get(
                    "next_cycle_artifacts", {}
                )
            )
            .get("PlanOS", {})
            .get("next_plan_basis_digest"),
            "post_effect_blocker_certificate_digest": dict(
                successor_closure_receipt.get(
                    "post_effect_blocker_certificate", {}
                )
            ).get("post_effect_blocker_certificate_digest"),
        }
        for field, value in expected.items():
            require(
                receipt.get(field) == value,
                f"second_cycle_{field}_invalid",
            )
        for field, expected_value in {
            "cycle_closed": True,
            "closed_cycle_immutable": True,
            "closed_cycle_append_only": True,
            "receipt_replay_forbidden": True,
            "receipt_consumption_count": 0,
            "consumed_authority_single_use": True,
            "consumed_authority_renewable": False,
            "consumed_authority_inheritable": False,
            "all_post_effect_blockers_active": True,
            "next_act_started": False,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }.items():
            require(
                receipt.get(field) == expected_value,
                f"second_cycle_{field}_invalid",
            )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_successor_cycle_materialization_receipt(
    root: Path,
) -> dict[str, Any]:
    predecessor = build_licensed_cycle_receipt(root / "predecessor-v19")
    predecessor_errors = validate_licensed_cycle_receipt(predecessor)
    if predecessor_errors:
        raise ValueError(
            "predecessor_cycle_invalid:" + ";".join(predecessor_errors)
        )
    blocker = build_successor_blocker_receipt(predecessor)
    requirement = build_successor_authority_requirement(predecessor)
    requirement_errors = validate_successor_authority_requirement(
        requirement,
        closed_cycle_receipt=predecessor,
    )
    if requirement_errors:
        raise ValueError(
            "successor_requirement_invalid:" + ";".join(requirement_errors)
        )
    policy, bundle, host_license, projection = host_inputs(
        job_id="qi-world-v20-job",
        expires_at_ms=480_000,
    )
    authority = _build_fresh_authority(
        predecessor_cycle_receipt=predecessor,
        successor_blocker_receipt=blocker,
        host_license=host_license,
    )
    authority_errors = validate_successor_external_authority(
        authority,
        predecessor_cycle_receipt=predecessor,
        successor_blocker_receipt=blocker,
        host_license=host_license,
        now_ms=290_002,
    )
    if authority_errors:
        raise ValueError(
            "successor_authority_invalid:" + ";".join(authority_errors)
        )
    if (
        authority["source_plan_basis_digest"]
        != requirement["source_next_plan_basis_digest"]
    ):
        raise ValueError("successor_materialization_plan_basis_mismatch")
    intake = build_successor_authority_intake(
        requirement=requirement,
        closed_cycle_receipt=predecessor,
        candidate_external_authority_packet=authority,
    )
    intake_errors = validate_successor_authority_intake(
        intake,
        requirement=requirement,
        closed_cycle_receipt=predecessor,
        candidate_external_authority_packet=authority,
    )
    if intake_errors:
        raise ValueError(
            "successor_intake_invalid:" + ";".join(intake_errors)
        )
    handoff = build_successor_handoff_receipt(
        root / "successor-handoff",
        predecessor_cycle_receipt=predecessor,
        successor_blocker_receipt=blocker,
        authority_requirement=requirement,
        authority_intake=intake,
        external_authority=authority,
        policy=policy,
        bundle=bundle,
        host_license=host_license,
        projection=projection,
    )
    closure = build_successor_closure_receipt(
        root / "successor-closure",
        successor_handoff_receipt=handoff,
        predecessor_cycle_receipt=predecessor,
        authority_requirement=requirement,
        authority_intake=intake,
        host_license=host_license,
    )
    second_cycle = build_second_cycle_receipt(
        predecessor_cycle_receipt=predecessor,
        successor_handoff_receipt=handoff,
        successor_closure_receipt=closure,
    )
    chain_digest = sha(
        {
            "first_cycle_receipt_digest": predecessor[
                "licensed_cycle_receipt_digest"
            ],
            "second_cycle_receipt_digest": second_cycle[
                "second_cycle_receipt_digest"
            ],
            "first_terminal_state_digest": predecessor[
                "terminal_state_digest"
            ],
            "second_terminal_state_digest": second_cycle[
                "terminal_state_digest"
            ],
        }
    )
    receipt = {
        "version": MATERIALIZATION_VERSION,
        "cycle_id": CYCLE_ID,
        "predecessor_cycle_receipt": deepcopy(predecessor),
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "successor_authority_requirement": deepcopy(requirement),
        "successor_authority_intake": deepcopy(intake),
        "successor_blocker_receipt": deepcopy(blocker),
        "successor_handoff_receipt": deepcopy(handoff),
        "successor_closure_receipt": deepcopy(closure),
        "second_cycle_receipt": deepcopy(second_cycle),
        "two_cycle_chain_digest": chain_digest,
        "first_cycle_ordinal": 1,
        "second_cycle_ordinal": 2,
        "cycle_ordinals_strictly_increasing": True,
        "fresh_authority_distinct": True,
        "fresh_human_approval_distinct": True,
        "fresh_host_license_distinct": True,
        "second_act_materialized": True,
        "second_effect_recorded": True,
        "second_observation_closed": True,
        "second_verification_closed": True,
        "second_learning_closed": True,
        "second_replan_closed": True,
        "second_cycle_closed": True,
        "predecessor_cycle_immutable": True,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
        "second_authority_consumed_once": True,
        "second_authority_inheritable": False,
        "all_second_post_effect_blockers_active": True,
        "third_act_started": False,
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
    errors = validate_successor_cycle_materialization_receipt(
        receipt,
        host_license=host_license,
    )
    if errors:
        raise ValueError(
            "successor_materialization_invalid:" + ";".join(errors)
        )
    return receipt


def validate_successor_cycle_materialization_receipt(
    receipt: Mapping[str, Any],
    *,
    host_license: Mapping[str, Any],
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
        predecessor = dict(
            receipt.get("predecessor_cycle_receipt", {})
        )
        errors.extend(
            "materialization_predecessor_" + error
            for error in validate_licensed_cycle_receipt(predecessor)
        )
        require(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "materialization_predecessor_digest_mismatch",
        )
        requirement = dict(
            receipt.get("successor_authority_requirement", {})
        )
        errors.extend(
            "materialization_requirement_" + error
            for error in validate_successor_authority_requirement(
                requirement,
                closed_cycle_receipt=predecessor,
            )
        )
        intake = dict(receipt.get("successor_authority_intake", {}))
        blocker = dict(receipt.get("successor_blocker_receipt", {}))
        errors.extend(
            "materialization_blocker_" + error
            for error in validate_successor_blocker_receipt(blocker)
        )
        handoff = dict(receipt.get("successor_handoff_receipt", {}))
        authority = dict(handoff.get("external_authority_packet", {}))
        errors.extend(
            "materialization_intake_" + error
            for error in validate_successor_authority_intake(
                intake,
                requirement=requirement,
                closed_cycle_receipt=predecessor,
                candidate_external_authority_packet=authority,
            )
        )
        errors.extend(
            "materialization_handoff_" + error
            for error in validate_successor_handoff_receipt(
                handoff,
                predecessor_cycle_receipt=predecessor,
                authority_requirement=requirement,
                authority_intake=intake,
                host_license=host_license,
            )
        )
        closure = dict(receipt.get("successor_closure_receipt", {}))
        errors.extend(
            "materialization_closure_" + error
            for error in validate_successor_closure_receipt(
                closure,
                predecessor_cycle_receipt=predecessor,
                authority_requirement=requirement,
                authority_intake=intake,
                host_license=host_license,
            )
        )
        second_cycle = dict(receipt.get("second_cycle_receipt", {}))
        errors.extend(
            "materialization_second_cycle_" + error
            for error in validate_second_cycle_receipt(
                second_cycle,
                predecessor_cycle_receipt=predecessor,
                successor_handoff_receipt=handoff,
                successor_closure_receipt=closure,
            )
        )
        expected_chain = sha(
            {
                "first_cycle_receipt_digest": predecessor.get(
                    "licensed_cycle_receipt_digest"
                ),
                "second_cycle_receipt_digest": second_cycle.get(
                    "second_cycle_receipt_digest"
                ),
                "first_terminal_state_digest": predecessor.get(
                    "terminal_state_digest"
                ),
                "second_terminal_state_digest": second_cycle.get(
                    "terminal_state_digest"
                ),
            }
        )
        require(
            receipt.get("two_cycle_chain_digest") == expected_chain,
            "materialization_chain_digest_mismatch",
        )
        require(
            authority.get("external_authority_packet_digest")
            != predecessor.get(
                "consumed_external_authority_packet_digest"
            ),
            "materialization_authority_reuse",
        )
        for field, expected in {
            "first_cycle_ordinal": 1,
            "second_cycle_ordinal": 2,
            "cycle_ordinals_strictly_increasing": True,
            "fresh_authority_distinct": True,
            "fresh_human_approval_distinct": True,
            "fresh_host_license_distinct": True,
            "second_act_materialized": True,
            "second_effect_recorded": True,
            "second_observation_closed": True,
            "second_verification_closed": True,
            "second_learning_closed": True,
            "second_replan_closed": True,
            "second_cycle_closed": True,
            "predecessor_cycle_immutable": True,
            "predecessor_authority_inherited": False,
            "predecessor_authority_renewed": False,
            "second_authority_consumed_once": True,
            "second_authority_inheritable": False,
            "all_second_post_effect_blockers_active": True,
            "third_act_started": False,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
            "multi_world_collapsed": False,
        }.items():
            require(
                receipt.get(field) == expected,
                f"materialization_{field}_invalid",
            )
        require(
            dict(receipt.get("non_authority", {}))
            == MATERIALIZATION_NON_AUTHORITY,
            "materialization_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
