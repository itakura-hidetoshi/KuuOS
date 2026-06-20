from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime import kuuos_qi_world_successor_licensed_cycle_materialization_v2_0 as _v20
from runtime import kuuos_qi_world_successor_native_evidence_clock_v2_0 as _clock
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
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_plan_phase_activation_receipt,
    validate_plan_state,
)
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    RELEASE_SCOPE,
    authority_packet_digest,
)
from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1 import (
    WITNESS_NON_AUTHORITY,
    WITNESS_VERSION,
    append_closed_cycle,
    build_inductive_licensed_cycle_chain,
    extension_witness_digest,
    validate_closed_cycle_extension_witness,
    validate_inductive_licensed_cycle_chain,
)
from runtime.kuuos_qi_world_successor_native_evidence_clock_v2_0 import (
    build_successor_native_evidence_downstream,
)
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.v017_host_adapter_fixtures import registry

VERSION = "kuuos_qi_world_concrete_third_licensed_cycle_materialization_v2_2"
REQUIREMENT_VERSION = "kuuos_qi_world_third_cycle_authority_requirement_v2_2"
INTAKE_VERSION = "kuuos_qi_world_third_cycle_authority_intake_v2_2"
HANDOFF_VERSION = "kuuos_qi_world_third_licensed_act_handoff_receipt_v2_2"
CLOSURE_VERSION = "kuuos_qi_world_third_native_evidence_closure_receipt_v2_2"
RECEIPT_VERSION = "kuuos_qi_world_third_closed_licensed_cycle_receipt_v2_2"
BUNDLE_VERSION = "kuuos_qi_world_concrete_three_cycle_bundle_v2_2"
CYCLE_ID = "qi-world-concrete-third-licensed-cycle-materialization-v22"

REQUIREMENT_NON_AUTHORITY = {
    "requirement_is_authority": False,
    "requirement_grants_execution": False,
    "requirement_starts_act": False,
    "requirement_self_issues_authority": False,
}
INTAKE_NON_AUTHORITY = {
    "intake_is_authority": False,
    "intake_grants_execution": False,
    "intake_starts_act": False,
    "intake_replaces_explicit_discharge": False,
}
HANDOFF_NON_AUTHORITY = {
    "materialization_grants_truth": False,
    "materialization_grants_world_identity": False,
    "materialization_grants_memory_overwrite": False,
    "materialization_issues_further_authority": False,
    "materialization_replays_predecessor_receipt": False,
    "materialization_inherits_predecessor_authority": False,
}
CLOSURE_NON_AUTHORITY = {
    "closure_grants_execution": False,
    "closure_grants_truth": False,
    "closure_issues_authority": False,
    "closure_starts_next_act": False,
    "closure_updates_exact_world": False,
    "closure_overwrites_history": False,
}
RECEIPT_NON_AUTHORITY = {
    "receipt_grants_execution": False,
    "receipt_grants_truth": False,
    "receipt_grants_world_identity": False,
    "receipt_grants_memory_overwrite": False,
    "receipt_issues_successor_authority": False,
    "receipt_renews_consumed_authority": False,
}
BUNDLE_NON_AUTHORITY = {
    "bundle_is_execution_capability": False,
    "bundle_issues_authority": False,
    "bundle_replays_receipts": False,
    "bundle_overwrites_history": False,
    "bundle_updates_exact_world": False,
    "bundle_promotes_truth": False,
}
BLOCKER_ORDER = [
    "fresh_external_authority_consumed_once",
    "predecessor_receipt_read_only",
    "observation_debt_discharged",
    "verification_debt_discharged",
    "learning_recorded_future_only",
    "replan_debt_discharged",
    "next_act_not_started",
    "world_projection_read_only",
    "history_immutable",
    "truth_not_promoted",
]


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def requirement_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "third_cycle_authority_requirement_digest")


def intake_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "third_cycle_authority_intake_digest")


def handoff_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "third_licensed_act_handoff_receipt_digest")


def closure_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "third_native_evidence_closure_receipt_digest")


def receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "licensed_cycle_receipt_digest")


def bundle_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "concrete_three_cycle_bundle_digest")


def blocker_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "post_effect_blocker_certificate_digest")


def world_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "world_projection_digest")


def _basis_bridge(plan: Mapping[str, Any]) -> dict[str, Any]:
    bridge = {
        "next_plan_basis_digest": plan["next_plan_basis_digest"],
        "materialized_plan_basis_digest": plan["plan_basis_digest"],
        "plan_state_digest": plan["plan_state_digest"],
        "committed_plan_digest": plan["latest_committed_plan_digest"],
        "bridge_read_only": True,
        "bridge_grants_execution": False,
        "basis_bridge_digest": "",
    }
    bridge["basis_bridge_digest"] = _digest_without(bridge, "basis_bridge_digest")
    return bridge


def _second_receipt(base_chain: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(
        dict(base_chain["root_two_cycle_chain"]["second_cycle_receipt"])
    )


def _source_plan(second: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(
        dict(
            second["source_successor_closure_receipt"]["next_cycle_artifacts"][
                "PlanOS"
            ]
        )
    )


def build_third_cycle_authority_requirement(
    base_chain: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_inductive_licensed_cycle_chain(base_chain)
    if errors:
        raise ValueError("base_chain_invalid:" + ";".join(errors))
    if base_chain["cycle_count"] != 2:
        raise ValueError("base_chain_must_end_at_cycle_2")
    second = _second_receipt(base_chain)
    plan = _source_plan(second)
    errors = validate_plan_state(plan)
    if errors:
        raise ValueError("third_source_plan_invalid:" + ";".join(errors))
    basis = dict(second["successor_basis"])
    requirement = {
        "version": REQUIREMENT_VERSION,
        "source_chain_digest": base_chain["inductive_chain_digest"],
        "source_prefix_digest": base_chain["prefix_digest"],
        "predecessor_cycle_receipt_digest": second[
            "licensed_cycle_receipt_digest"
        ],
        "predecessor_cycle_ordinal": 2,
        "target_cycle_ordinal": 3,
        "source_successor_basis_digest": second["successor_basis_digest"],
        "source_next_plan_state_digest": basis["next_plan_state_digest"],
        "source_next_plan_basis_digest": basis["next_plan_basis_digest"],
        "source_next_committed_plan_digest": basis[
            "next_committed_plan_digest"
        ],
        "materialized_plan_basis_digest": plan["plan_basis_digest"],
        "fresh_external_authority_required": True,
        "distinct_authority_packet_digest_required": True,
        "new_human_approval_required": True,
        "new_host_license_required": True,
        "external_issuer_required": True,
        "self_issued_forbidden": True,
        "single_use_required": True,
        "forbidden_external_authority_packet_digests": list(
            base_chain["authority_packet_digests"]
        ),
        "forbidden_human_approval_receipt_digests": list(
            base_chain["human_approval_receipt_digests"]
        ),
        "forbidden_host_license_digests": list(
            base_chain["host_license_digests"]
        ),
        "requirement_only": True,
        "non_authority": deepcopy(REQUIREMENT_NON_AUTHORITY),
        "third_cycle_authority_requirement_digest": "",
    }
    requirement["third_cycle_authority_requirement_digest"] = requirement_digest(
        requirement
    )
    errors = validate_third_cycle_authority_requirement(
        requirement, base_chain=base_chain
    )
    if errors:
        raise ValueError("third_requirement_invalid:" + ";".join(errors))
    return requirement


def validate_third_cycle_authority_requirement(
    requirement: Mapping[str, Any],
    *,
    base_chain: Mapping[str, Any],
) -> list[str]:
    errors = [
        "requirement_base_" + error
        for error in validate_inductive_licensed_cycle_chain(base_chain)
    ]
    if errors:
        return errors

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        second = _second_receipt(base_chain)
        plan = _source_plan(second)
        basis = dict(second["successor_basis"])
        req(requirement.get("version") == REQUIREMENT_VERSION, "requirement_version_invalid")
        req(
            requirement.get("third_cycle_authority_requirement_digest")
            == requirement_digest(requirement),
            "requirement_digest_invalid",
        )
        req(base_chain.get("cycle_count") == 2, "requirement_source_count_invalid")
        req(
            requirement.get("source_chain_digest")
            == base_chain.get("inductive_chain_digest"),
            "requirement_source_chain_digest_mismatch",
        )
        req(
            requirement.get("source_prefix_digest") == base_chain.get("prefix_digest"),
            "requirement_source_prefix_digest_mismatch",
        )
        req(
            requirement.get("predecessor_cycle_receipt_digest")
            == second.get("licensed_cycle_receipt_digest"),
            "requirement_predecessor_digest_mismatch",
        )
        req(requirement.get("predecessor_cycle_ordinal") == 2, "requirement_predecessor_ordinal_invalid")
        req(requirement.get("target_cycle_ordinal") == 3, "requirement_target_ordinal_invalid")
        req(
            requirement.get("source_successor_basis_digest")
            == second.get("successor_basis_digest"),
            "requirement_successor_basis_digest_mismatch",
        )
        req(
            requirement.get("source_next_plan_state_digest")
            == basis.get("next_plan_state_digest")
            == plan.get("plan_state_digest"),
            "requirement_plan_state_digest_mismatch",
        )
        req(
            requirement.get("source_next_plan_basis_digest")
            == basis.get("next_plan_basis_digest")
            == plan.get("next_plan_basis_digest"),
            "requirement_plan_basis_digest_mismatch",
        )
        req(
            requirement.get("source_next_committed_plan_digest")
            == basis.get("next_committed_plan_digest")
            == plan.get("latest_committed_plan_digest"),
            "requirement_committed_plan_digest_mismatch",
        )
        req(
            requirement.get("materialized_plan_basis_digest")
            == plan.get("plan_basis_digest"),
            "requirement_materialized_basis_mismatch",
        )
        expected = {
            "fresh_external_authority_required": True,
            "distinct_authority_packet_digest_required": True,
            "new_human_approval_required": True,
            "new_host_license_required": True,
            "external_issuer_required": True,
            "self_issued_forbidden": True,
            "single_use_required": True,
            "requirement_only": True,
        }
        for field, value in expected.items():
            req(requirement.get(field) == value, f"requirement_{field}_invalid")
        req(
            requirement.get("forbidden_external_authority_packet_digests")
            == base_chain.get("authority_packet_digests"),
            "requirement_authority_inventory_invalid",
        )
        req(
            requirement.get("forbidden_human_approval_receipt_digests")
            == base_chain.get("human_approval_receipt_digests"),
            "requirement_approval_inventory_invalid",
        )
        req(
            requirement.get("forbidden_host_license_digests")
            == base_chain.get("host_license_digests"),
            "requirement_host_license_inventory_invalid",
        )
        req(
            dict(requirement.get("non_authority", {}))
            == REQUIREMENT_NON_AUTHORITY,
            "requirement_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _fresh_authority(
    second: Mapping[str, Any],
    plan: Mapping[str, Any],
    host_license: Mapping[str, Any],
    requirement: Mapping[str, Any],
) -> dict[str, Any]:
    packet = deepcopy(
        dict(second["source_successor_handoff_receipt"]["external_authority_packet"])
    )
    bridge = _basis_bridge(plan)
    packet.update(
        {
            "authority_id": "qi-world-v22-third-cycle-external-authority",
            "source_blocker_receipt_digest": second["successor_basis_digest"],
            "source_blocker_certificate_digest": second["successor_basis"][
                "post_effect_blocker_certificate_digest"
            ],
            "source_plan_state_digest": plan["plan_state_digest"],
            "source_plan_basis_digest": plan["next_plan_basis_digest"],
            "source_committed_plan_digest": plan[
                "latest_committed_plan_digest"
            ],
            "materialized_plan_basis_digest": plan["plan_basis_digest"],
            "basis_bridge_digest": bridge["basis_bridge_digest"],
            "predecessor_cycle_receipt_digest": second[
                "licensed_cycle_receipt_digest"
            ],
            "predecessor_cycle_ordinal": 2,
            "target_cycle_ordinal": 3,
            "host_license_digest": host_license["host_license_digest"],
            "human_approval_receipt_digest": sha(
                "qi-world-v22-third-cycle-human-approval"
            ),
            "human_approver_id": "external-human-operator-v22",
            "issued_at_ms": 690_000,
            "expires_at_ms": 780_000,
            "source_requirement_digest": requirement[
                "third_cycle_authority_requirement_digest"
            ],
            "external_authority_packet_digest": "",
        }
    )
    packet["external_authority_packet_digest"] = authority_packet_digest(packet)
    return packet


def build_third_cycle_authority_intake(
    *,
    requirement: Mapping[str, Any],
    base_chain: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_third_cycle_authority_requirement(
        requirement, base_chain=base_chain
    )
    if errors:
        raise ValueError("third_requirement_invalid:" + ";".join(errors))
    intake = {
        "version": INTAKE_VERSION,
        "source_requirement_digest": requirement[
            "third_cycle_authority_requirement_digest"
        ],
        "source_chain_digest": base_chain["inductive_chain_digest"],
        "predecessor_cycle_receipt_digest": requirement[
            "predecessor_cycle_receipt_digest"
        ],
        "target_cycle_ordinal": 3,
        "candidate_external_authority_packet_digest": candidate[
            "external_authority_packet_digest"
        ],
        "candidate_human_approval_receipt_digest": candidate[
            "human_approval_receipt_digest"
        ],
        "candidate_host_license_digest": candidate["host_license_digest"],
        "candidate_source_plan_state_digest": candidate[
            "source_plan_state_digest"
        ],
        "candidate_source_plan_basis_digest": candidate[
            "source_plan_basis_digest"
        ],
        "candidate_committed_plan_digest": candidate[
            "source_committed_plan_digest"
        ],
        "candidate_materialized_plan_basis_digest": candidate[
            "materialized_plan_basis_digest"
        ],
        "freshness_qualified": True,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
        "successor_act_started": False,
        "explicit_discharge_still_required": True,
        "intake_only": True,
        "non_authority": deepcopy(INTAKE_NON_AUTHORITY),
        "third_cycle_authority_intake_digest": "",
    }
    intake["third_cycle_authority_intake_digest"] = intake_digest(intake)
    errors = validate_third_cycle_authority_intake(
        intake,
        requirement=requirement,
        base_chain=base_chain,
        candidate=candidate,
    )
    if errors:
        raise ValueError("third_intake_invalid:" + ";".join(errors))
    return intake


def validate_third_cycle_authority_intake(
    intake: Mapping[str, Any],
    *,
    requirement: Mapping[str, Any],
    base_chain: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> list[str]:
    errors = validate_third_cycle_authority_requirement(
        requirement, base_chain=base_chain
    )

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(intake.get("version") == INTAKE_VERSION, "intake_version_invalid")
        req(
            intake.get("third_cycle_authority_intake_digest")
            == intake_digest(intake),
            "intake_digest_invalid",
        )
        req(
            candidate.get("external_authority_packet_digest")
            == authority_packet_digest(candidate),
            "intake_candidate_authority_digest_invalid",
        )
        req(
            candidate.get("external_authority_packet_digest")
            not in base_chain.get("authority_packet_digests", []),
            "intake_candidate_authority_reuse",
        )
        req(
            candidate.get("human_approval_receipt_digest")
            not in base_chain.get("human_approval_receipt_digests", []),
            "intake_candidate_approval_reuse",
        )
        req(
            candidate.get("host_license_digest")
            not in base_chain.get("host_license_digests", []),
            "intake_candidate_host_license_reuse",
        )
        req(candidate.get("external_issuer") is True, "intake_external_issuer_required")
        req(candidate.get("self_issued") is False, "intake_self_issued_forbidden")
        req(candidate.get("single_use") is True, "intake_single_use_required")
        req(candidate.get("predecessor_cycle_ordinal") == 2, "intake_predecessor_ordinal_invalid")
        req(candidate.get("target_cycle_ordinal") == 3, "intake_target_ordinal_invalid")
        req(
            candidate.get("predecessor_cycle_receipt_digest")
            == requirement.get("predecessor_cycle_receipt_digest"),
            "intake_predecessor_digest_mismatch",
        )
        bindings = {
            "source_requirement_digest": requirement.get(
                "third_cycle_authority_requirement_digest"
            ),
            "source_chain_digest": base_chain.get("inductive_chain_digest"),
            "predecessor_cycle_receipt_digest": requirement.get(
                "predecessor_cycle_receipt_digest"
            ),
            "target_cycle_ordinal": 3,
            "candidate_external_authority_packet_digest": candidate.get(
                "external_authority_packet_digest"
            ),
            "candidate_human_approval_receipt_digest": candidate.get(
                "human_approval_receipt_digest"
            ),
            "candidate_host_license_digest": candidate.get("host_license_digest"),
            "candidate_source_plan_state_digest": candidate.get(
                "source_plan_state_digest"
            ),
            "candidate_source_plan_basis_digest": candidate.get(
                "source_plan_basis_digest"
            ),
            "candidate_committed_plan_digest": candidate.get(
                "source_committed_plan_digest"
            ),
            "candidate_materialized_plan_basis_digest": candidate.get(
                "materialized_plan_basis_digest"
            ),
        }
        for field, value in bindings.items():
            req(intake.get(field) == value, f"intake_{field}_mismatch")
        expected = {
            "freshness_qualified": True,
            "predecessor_authority_inherited": False,
            "predecessor_authority_renewed": False,
            "successor_act_started": False,
            "explicit_discharge_still_required": True,
            "intake_only": True,
        }
        for field, value in expected.items():
            req(intake.get(field) == value, f"intake_{field}_invalid")
        req(
            dict(intake.get("non_authority", {})) == INTAKE_NON_AUTHORITY,
            "intake_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _materialize_third_act(
    root: Path,
    *,
    plan: Mapping[str, Any],
    candidate: Mapping[str, Any],
    requirement: Mapping[str, Any],
    intake: Mapping[str, Any],
    policy: Mapping[str, Any],
    supervisor_bundle: Mapping[str, Any],
    host_license: Mapping[str, Any],
    projection: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    activation = build_plan_phase_activation_receipt(
        state=plan,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=requirement[
            "third_cycle_authority_requirement_digest"
        ],
        plan_phase_receipt_digest=sha("qi-world-v22-third-plan-phase"),
        now_ms=690_000,
    )
    store = ActStore(root)
    state = store.initialize(
        build_initial_act_state(
            act_id="qi-world-v22-third-act",
            plan_state=plan,
            plan_activation_receipt=activation,
            now_ms=690_000,
        )
    )
    operation_input_digest = sha({"value": 3})
    state = apply_act(
        store,
        state,
        "select",
        {
            "plan_state": deepcopy(dict(plan)),
            "selected_step_id": RELEASE_SCOPE["selected_step_id"],
            "operation_id": RELEASE_SCOPE["operation_id"],
            "operation_input_digest": operation_input_digest,
        },
        690_001,
    )
    authorization = build_step_authorization(
        state=state,
        authorization_id="qi-world-v22-third-step-authorization",
        operation_id=RELEASE_SCOPE["operation_id"],
        operation_input_digest=operation_input_digest,
        act_phase_receipt_digest=candidate["external_authority_packet_digest"],
        invocation_id="qi-world-v22-third-single-invocation",
        source_supervisor_bundle_digest=projection[
            "source_supervisor_bundle_digest"
        ],
        host_job_id="qi-world-v22-third-job",
        host_step_id="step-1",
        host_license=host_license,
        human_approval_receipt_digest=candidate[
            "human_approval_receipt_digest"
        ],
        human_approver_id=candidate["human_approver_id"],
        issued_at_ms=690_000,
        expires_at_ms=780_000,
    )
    state = apply_act(
        store,
        state,
        "authorize",
        {"step_authorization": authorization, "host_license": deepcopy(host_license)},
        690_002,
    )
    state = apply_act(
        store,
        state,
        "project",
        {"host_projection": deepcopy(projection)},
        690_003,
    )
    invoke_event, host_tick = build_authorized_invoke_event(
        state=state,
        supervisor_bundle=supervisor_bundle,
        worker_id="qi-world-v22-third-worker",
        now_ms=690_004,
        supervisor_policy=policy,
        registry=registry(),
    )
    result = store.apply(invoke_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    state = result["state"]
    state = apply_act(
        store,
        state,
        "verify",
        {"verification_receipt_digest": sha("qi-world-v22-third-act-verification")},
        690_005,
    )
    result = store.apply(
        build_fixture_event(
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
            690_006,
        )
    )
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    state = result["state"]
    errors = validate_act_state(state)
    if errors:
        raise ValueError("third_act_invalid:" + ";".join(errors))
    discharge = {
        "source_requirement_digest": requirement[
            "third_cycle_authority_requirement_digest"
        ],
        "source_intake_digest": intake["third_cycle_authority_intake_digest"],
        "external_authority_packet_digest": candidate[
            "external_authority_packet_digest"
        ],
        "basis_bridge_digest": candidate["basis_bridge_digest"],
        "single_use_release": True,
        "release_consumption_count": 1,
        "released_act_state_digest": state["act_state_digest"],
        "predecessor_receipt_consumed": False,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
        "blocker_discharge_certificate_digest": "",
    }
    discharge["blocker_discharge_certificate_digest"] = _digest_without(
        discharge, "blocker_discharge_certificate_digest"
    )
    return state, activation, {"host_tick": host_tick, "discharge": discharge}


def build_third_licensed_act_handoff_receipt(root: Path) -> dict[str, Any]:
    base_chain = build_inductive_licensed_cycle_chain(root / "base")
    requirement = build_third_cycle_authority_requirement(base_chain)
    second = _second_receipt(base_chain)
    plan = _source_plan(second)
    policy, supervisor_bundle, host_license, projection = host_inputs(
        job_id="qi-world-v22-third-job",
        expires_at_ms=780_000,
    )
    candidate = _fresh_authority(
        second, plan, host_license, requirement
    )
    intake = build_third_cycle_authority_intake(
        requirement=requirement,
        base_chain=base_chain,
        candidate=candidate,
    )
    act, activation, materialization = _materialize_third_act(
        root / "act",
        plan=plan,
        candidate=candidate,
        requirement=requirement,
        intake=intake,
        policy=policy,
        supervisor_bundle=supervisor_bundle,
        host_license=host_license,
        projection=projection,
    )
    bridge = _basis_bridge(plan)
    receipt = {
        "version": HANDOFF_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 3,
        "source_inductive_chain": deepcopy(base_chain),
        "source_inductive_chain_digest": base_chain["inductive_chain_digest"],
        "predecessor_closed_cycle_receipt": deepcopy(second),
        "predecessor_cycle_receipt_digest": second[
            "licensed_cycle_receipt_digest"
        ],
        "third_cycle_authority_requirement": deepcopy(requirement),
        "third_cycle_authority_requirement_digest": requirement[
            "third_cycle_authority_requirement_digest"
        ],
        "third_cycle_authority_intake": deepcopy(intake),
        "third_cycle_authority_intake_digest": intake[
            "third_cycle_authority_intake_digest"
        ],
        "basis_bridge": bridge,
        "basis_bridge_digest": bridge["basis_bridge_digest"],
        "source_plan_state": deepcopy(plan),
        "source_plan_state_digest": plan["plan_state_digest"],
        "source_plan_basis_digest": plan["next_plan_basis_digest"],
        "materialized_plan_basis_digest": plan["plan_basis_digest"],
        "source_committed_plan_digest": plan["latest_committed_plan_digest"],
        "plan_activation_receipt": deepcopy(activation),
        "external_authority_packet": deepcopy(candidate),
        "blocker_discharge_certificate": materialization["discharge"],
        "target_act_state": deepcopy(act),
        "host_tick_digest": materialization["host_tick"]["host_tick_digest"],
        "source_chain_immutable": True,
        "source_receipt_read_only": True,
        "source_receipt_consumed": False,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
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
        "non_authority": deepcopy(HANDOFF_NON_AUTHORITY),
        "third_licensed_act_handoff_receipt_digest": "",
    }
    receipt["third_licensed_act_handoff_receipt_digest"] = handoff_digest(receipt)
    errors = validate_third_licensed_act_handoff_receipt(receipt)
    if errors:
        raise ValueError("third_handoff_invalid:" + ";".join(errors))
    return receipt


def validate_third_licensed_act_handoff_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(receipt.get("version") == HANDOFF_VERSION, "handoff_version_invalid")
        req(
            receipt.get("third_licensed_act_handoff_receipt_digest")
            == handoff_digest(receipt),
            "handoff_digest_invalid",
        )
        req(receipt.get("cycle_ordinal") == 3, "handoff_cycle_ordinal_invalid")
        base = dict(receipt.get("source_inductive_chain", {}))
        errors += [
            "handoff_base_" + error
            for error in validate_inductive_licensed_cycle_chain(base)
        ]
        req(base.get("cycle_count") == 2, "handoff_base_cycle_count_invalid")
        req(
            receipt.get("source_inductive_chain_digest")
            == base.get("inductive_chain_digest"),
            "handoff_base_digest_mismatch",
        )
        second = _second_receipt(base)
        req(
            dict(receipt.get("predecessor_closed_cycle_receipt", {})) == second,
            "handoff_predecessor_substitution",
        )
        req(
            receipt.get("predecessor_cycle_receipt_digest")
            == second.get("licensed_cycle_receipt_digest"),
            "handoff_predecessor_digest_mismatch",
        )
        requirement = dict(receipt.get("third_cycle_authority_requirement", {}))
        errors += [
            "handoff_requirement_" + error
            for error in validate_third_cycle_authority_requirement(
                requirement, base_chain=base
            )
        ]
        candidate = dict(receipt.get("external_authority_packet", {}))
        intake = dict(receipt.get("third_cycle_authority_intake", {}))
        errors += [
            "handoff_intake_" + error
            for error in validate_third_cycle_authority_intake(
                intake,
                requirement=requirement,
                base_chain=base,
                candidate=candidate,
            )
        ]
        plan = dict(receipt.get("source_plan_state", {}))
        errors += ["handoff_plan_" + error for error in validate_plan_state(plan)]
        bridge = dict(receipt.get("basis_bridge", {}))
        req(bridge == _basis_bridge(plan), "handoff_basis_bridge_substitution")
        req(
            candidate.get("basis_bridge_digest") == bridge.get("basis_bridge_digest"),
            "handoff_authority_basis_bridge_mismatch",
        )
        act = dict(receipt.get("target_act_state", {}))
        errors += ["handoff_act_" + error for error in validate_act_state(act)]
        req(act.get("current_phase") == "commit", "handoff_act_not_committed")
        req(act.get("route") == "EFFECT_RECORDED", "handoff_act_route_invalid")
        req(
            act.get("source_plan_basis_digest") == plan.get("plan_basis_digest"),
            "handoff_act_materialized_basis_mismatch",
        )
        authorization = dict(act.get("step_authorization", {}))
        req(
            authorization.get("act_phase_receipt_digest")
            == candidate.get("external_authority_packet_digest"),
            "handoff_authorization_authority_mismatch",
        )
        req(
            authorization.get("host_license_digest")
            == candidate.get("host_license_digest"),
            "handoff_authorization_host_license_mismatch",
        )
        req(
            authorization.get("human_approval_receipt_digest")
            == candidate.get("human_approval_receipt_digest"),
            "handoff_authorization_approval_mismatch",
        )
        discharge = dict(receipt.get("blocker_discharge_certificate", {}))
        req(
            discharge.get("blocker_discharge_certificate_digest")
            == _digest_without(discharge, "blocker_discharge_certificate_digest"),
            "handoff_discharge_digest_invalid",
        )
        req(
            discharge.get("release_consumption_count") == 1
            and discharge.get("single_use_release") is True,
            "handoff_discharge_not_single_use",
        )
        expected = {
            "source_chain_immutable": True,
            "source_receipt_read_only": True,
            "source_receipt_consumed": False,
            "predecessor_authority_inherited": False,
            "predecessor_authority_renewed": False,
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
        }
        for field, value in expected.items():
            req(receipt.get(field) == value, f"handoff_{field}_invalid")
        req(
            dict(receipt.get("non_authority", {})) == HANDOFF_NON_AUTHORITY,
            "handoff_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _third_evidence(root: Path, act: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    names = (
        "OBSERVE_INITIAL_MS",
        "OBSERVE_WINDOW_START_MS",
        "OBSERVE_WINDOW_END_MS",
        "OBSERVE_EVENT_BASE_MS",
        "VERIFY_INITIAL_MS",
        "VERIFY_EVENT_BASE_MS",
        "LEARN_INITIAL_MS",
        "LEARN_EVENT_BASE_MS",
    )
    previous = {name: getattr(_clock, name) for name in names}
    shifted = {
        "OBSERVE_INITIAL_MS": 698_000,
        "OBSERVE_WINDOW_START_MS": 699_000,
        "OBSERVE_WINDOW_END_MS": 699_900,
        "OBSERVE_EVENT_BASE_MS": 700_000,
        "VERIFY_INITIAL_MS": 710_000,
        "VERIFY_EVENT_BASE_MS": 720_000,
        "LEARN_INITIAL_MS": 800_000,
        "LEARN_EVENT_BASE_MS": 810_000,
    }
    try:
        for name, value in shifted.items():
            setattr(_clock, name, value)
        return build_successor_native_evidence_downstream(root, act)
    finally:
        for name, value in previous.items():
            setattr(_clock, name, value)


def _native_errors(states: Mapping[str, Mapping[str, Any]]) -> list[str]:
    validators = {
        "ActOS": validate_act_state,
        "ObserveOS": validate_observe_state,
        "VerifyOS": validate_verify_state,
        "LearnOS": validate_learn_state,
    }
    errors: list[str] = []
    for name, validator in validators.items():
        state = states.get(name)
        if not isinstance(state, Mapping):
            errors.append(f"{name}_missing")
        else:
            errors += [f"{name}:{error}" for error in validator(state)]
    return errors


def _evidence_lineage(
    handoff: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
) -> str:
    return sha(
        {
            "predecessor_cycle_receipt_digest": handoff[
                "predecessor_cycle_receipt_digest"
            ],
            "third_handoff_receipt_digest": handoff[
                "third_licensed_act_handoff_receipt_digest"
            ],
            "act_state_digest": states["ActOS"]["act_state_digest"],
            "observe_state_digest": states["ObserveOS"]["observe_state_digest"],
            "verify_state_digest": states["VerifyOS"]["verify_state_digest"],
            "learn_state_digest": states["LearnOS"]["learn_state_digest"],
        }
    )


def _compat_handoff(handoff: Mapping[str, Any]) -> dict[str, Any]:
    adapted = deepcopy(dict(handoff))
    predecessor = deepcopy(dict(adapted["predecessor_closed_cycle_receipt"]))
    closure = deepcopy(dict(predecessor["source_successor_closure_receipt"]))
    predecessor["source_v18_closure_receipt"] = closure
    adapted["predecessor_closed_cycle_receipt"] = predecessor
    adapted["successor_licensed_act_handoff_receipt_digest"] = handoff[
        "third_licensed_act_handoff_receipt_digest"
    ]
    return adapted


def _world_projection(
    handoff: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    predecessor = handoff["predecessor_closed_cycle_receipt"]
    source_world = predecessor["source_successor_closure_receipt"][
        "post_effect_world_projection_digest"
    ]
    world = {
        "projection_kind": "concrete_third_licensed_cycle_projection_v2_2",
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "source_world_projection_digest": source_world,
        "third_handoff_receipt_digest": handoff[
            "third_licensed_act_handoff_receipt_digest"
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
    world["world_projection_digest"] = world_digest(world)
    return world


def _blocker_certificate(
    handoff: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
) -> dict[str, Any]:
    vector = {name: True for name in BLOCKER_ORDER}
    blocker = {
        "version": "kuuos_qi_world_third_post_effect_blocker_certificate_v2_2",
        "source_handoff_receipt_digest": handoff[
            "third_licensed_act_handoff_receipt_digest"
        ],
        "act_state_digest": states["ActOS"]["act_state_digest"],
        "observe_state_digest": states["ObserveOS"]["observe_state_digest"],
        "verify_state_digest": states["VerifyOS"]["verify_state_digest"],
        "learn_state_digest": states["LearnOS"]["learn_state_digest"],
        "next_plan_state_digest": next_artifacts["PlanOS"]["plan_state_digest"],
        "next_plan_basis_digest": next_artifacts["PlanOS"][
            "next_plan_basis_digest"
        ],
        "world_projection_digest": world["world_projection_digest"],
        "composed_blocker_vector": vector,
        "missing_blockers": [],
        "all_required_blockers_active": True,
        "next_act_not_started": True,
        "bounded_contextual_repairable": True,
        "certificate_grants_execution": False,
        "post_effect_blocker_certificate_digest": "",
    }
    blocker["post_effect_blocker_certificate_digest"] = blocker_digest(blocker)
    return blocker


def validate_third_post_effect_blocker_certificate(
    blocker: Mapping[str, Any],
    *,
    handoff: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(
            blocker.get("post_effect_blocker_certificate_digest")
            == blocker_digest(blocker),
            "blocker_digest_invalid",
        )
        bindings = {
            "source_handoff_receipt_digest": handoff.get(
                "third_licensed_act_handoff_receipt_digest"
            ),
            "act_state_digest": states.get("ActOS", {}).get("act_state_digest"),
            "observe_state_digest": states.get("ObserveOS", {}).get(
                "observe_state_digest"
            ),
            "verify_state_digest": states.get("VerifyOS", {}).get(
                "verify_state_digest"
            ),
            "learn_state_digest": states.get("LearnOS", {}).get("learn_state_digest"),
            "next_plan_state_digest": next_artifacts.get("PlanOS", {}).get(
                "plan_state_digest"
            ),
            "next_plan_basis_digest": next_artifacts.get("PlanOS", {}).get(
                "next_plan_basis_digest"
            ),
            "world_projection_digest": world.get("world_projection_digest"),
        }
        for field, value in bindings.items():
            req(blocker.get(field) == value, f"blocker_{field}_mismatch")
        vector = dict(blocker.get("composed_blocker_vector", {}))
        req(
            vector == {name: True for name in BLOCKER_ORDER},
            "blocker_vector_invalid",
        )
        req(blocker.get("missing_blockers") == [], "blocker_missing_not_empty")
        req(blocker.get("all_required_blockers_active") is True, "blocker_not_all_active")
        req(blocker.get("next_act_not_started") is True, "blocker_next_act_started")
        req(
            blocker.get("bounded_contextual_repairable") is True,
            "blocker_governance_boundary_invalid",
        )
        req(blocker.get("certificate_grants_execution") is False, "blocker_execution_escalation")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_third_native_evidence_closure_receipt(root: Path) -> dict[str, Any]:
    handoff = build_third_licensed_act_handoff_receipt(root / "handoff")
    act = deepcopy(dict(handoff["target_act_state"]))
    observe, verify, learn = _third_evidence(root / "evidence", act)
    states = {
        "ActOS": act,
        "ObserveOS": observe,
        "VerifyOS": verify,
        "LearnOS": learn,
    }
    errors = _native_errors(states)
    if errors:
        raise ValueError("third_native_evidence_invalid:" + ";".join(errors))
    lineage = _evidence_lineage(handoff, states)
    compat = _compat_handoff(handoff)
    next_artifacts = _v20._next_cycle(
        root / "next-cycle", compat, states, lineage
    )
    world = _world_projection(handoff, states, next_artifacts)
    blocker = _blocker_certificate(handoff, states, next_artifacts, world)
    errors = validate_third_post_effect_blocker_certificate(
        blocker,
        handoff=handoff,
        states=states,
        next_artifacts=next_artifacts,
        world=world,
    )
    if errors:
        raise ValueError("third_blocker_invalid:" + ";".join(errors))
    receipt = {
        "version": CLOSURE_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 3,
        "source_third_handoff_receipt": deepcopy(handoff),
        "source_third_handoff_receipt_digest": handoff[
            "third_licensed_act_handoff_receipt_digest"
        ],
        "predecessor_cycle_receipt_digest": handoff[
            "predecessor_cycle_receipt_digest"
        ],
        "native_evidence_states": deepcopy(states),
        "native_evidence_lineage_digest": lineage,
        "next_cycle_artifacts": deepcopy(next_artifacts),
        "post_effect_world_projection": world,
        "post_effect_world_projection_digest": world["world_projection_digest"],
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
        "all_post_effect_blockers_active": True,
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CLOSURE_NON_AUTHORITY),
        "third_native_evidence_closure_receipt_digest": "",
    }
    receipt["third_native_evidence_closure_receipt_digest"] = closure_digest(receipt)
    errors = validate_third_native_evidence_closure_receipt(receipt)
    if errors:
        raise ValueError("third_closure_invalid:" + ";".join(errors))
    return receipt


def validate_third_native_evidence_closure_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(receipt.get("version") == CLOSURE_VERSION, "closure_version_invalid")
        req(
            receipt.get("third_native_evidence_closure_receipt_digest")
            == closure_digest(receipt),
            "closure_digest_invalid",
        )
        req(receipt.get("cycle_ordinal") == 3, "closure_cycle_ordinal_invalid")
        handoff = dict(receipt.get("source_third_handoff_receipt", {}))
        errors += [
            "closure_source_" + error
            for error in validate_third_licensed_act_handoff_receipt(handoff)
        ]
        states = dict(receipt.get("native_evidence_states", {}))
        errors += ["closure_" + error for error in _native_errors(states)]
        act = dict(states.get("ActOS", {}))
        observe = dict(states.get("ObserveOS", {}))
        verify = dict(states.get("VerifyOS", {}))
        learn = dict(states.get("LearnOS", {}))
        req(act == handoff.get("target_act_state"), "closure_source_act_substitution")
        req(
            observe.get("source_act_state_digest") == act.get("act_state_digest"),
            "closure_observe_source_act_mismatch",
        )
        req(
            verify.get("source_observe_state_digest")
            == observe.get("observe_state_digest"),
            "closure_verify_source_observe_mismatch",
        )
        req(
            learn.get("source_verify_state_digest") == verify.get("verify_state_digest"),
            "closure_learn_source_verify_mismatch",
        )
        req(
            receipt.get("native_evidence_lineage_digest")
            == _evidence_lineage(handoff, states),
            "closure_evidence_lineage_mismatch",
        )
        next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
        errors += [
            "closure_next_" + error
            for error in _reentry._validate_next_artifacts(next_artifacts)
        ]
        req(
            next_artifacts.get("PlanOS", {}).get("next_plan_basis_digest")
            == learn.get("learning_delta_digest"),
            "closure_next_plan_learning_basis_mismatch",
        )
        world = dict(receipt.get("post_effect_world_projection", {}))
        req(
            world.get("world_projection_digest") == world_digest(world),
            "closure_world_digest_invalid",
        )
        req(
            world.get("projection_read_only") is True
            and world.get("runtime_updates_world") is False
            and world.get("exact_world_identified") is False,
            "closure_world_boundary_invalid",
        )
        blocker = dict(receipt.get("post_effect_blocker_certificate", {}))
        errors += validate_third_post_effect_blocker_certificate(
            blocker,
            handoff=handoff,
            states=states,
            next_artifacts=next_artifacts,
            world=world,
        )
        req(
            receipt.get("source_third_handoff_receipt_digest")
            == handoff.get("third_licensed_act_handoff_receipt_digest"),
            "closure_source_handoff_digest_mismatch",
        )
        req(
            receipt.get("post_effect_world_projection_digest")
            == world.get("world_projection_digest"),
            "closure_world_binding_mismatch",
        )
        req(
            receipt.get("post_effect_blocker_certificate_digest")
            == blocker.get("post_effect_blocker_certificate_digest"),
            "closure_blocker_binding_mismatch",
        )
        expected = {
            "source_effect_immutable": True,
            "source_authority_consumed_once": True,
            "observation_debt_discharged": True,
            "verification_debt_discharged": True,
            "learning_recorded": True,
            "replan_debt_discharged": True,
            "next_act_not_started": True,
            "all_post_effect_blockers_active": True,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(receipt.get(field) == value, f"closure_{field}_invalid")
        req(
            dict(receipt.get("non_authority", {})) == CLOSURE_NON_AUTHORITY,
            "closure_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _terminal_digest(closure: Mapping[str, Any]) -> str:
    states = closure["native_evidence_states"]
    plan = closure["next_cycle_artifacts"]["PlanOS"]
    return sha(
        {
            "act": states["ActOS"]["act_state_digest"],
            "observe": states["ObserveOS"]["observe_state_digest"],
            "verify": states["VerifyOS"]["verify_state_digest"],
            "learn": states["LearnOS"]["learn_state_digest"],
            "next_plan": plan["plan_state_digest"],
            "blockers": closure["post_effect_blocker_certificate_digest"],
            "world": closure["post_effect_world_projection_digest"],
        }
    )


def _successor_basis(closure: Mapping[str, Any]) -> dict[str, Any]:
    plan = closure["next_cycle_artifacts"]["PlanOS"]
    blocker = closure["post_effect_blocker_certificate"]
    return {
        "next_plan_state_digest": plan["plan_state_digest"],
        "next_plan_basis_digest": plan["next_plan_basis_digest"],
        "next_committed_plan_digest": plan["latest_committed_plan_digest"],
        "materialized_plan_basis_digest": plan["plan_basis_digest"],
        "post_effect_blocker_certificate_digest": closure[
            "post_effect_blocker_certificate_digest"
        ],
        "post_effect_world_projection_digest": closure[
            "post_effect_world_projection_digest"
        ],
        "all_required_blockers_active": blocker["all_required_blockers_active"],
        "next_act_not_started": blocker["next_act_not_started"],
    }


def build_third_closed_cycle_receipt(root: Path) -> dict[str, Any]:
    closure = build_third_native_evidence_closure_receipt(root / "closure")
    handoff = closure["source_third_handoff_receipt"]
    predecessor = handoff["predecessor_closed_cycle_receipt"]
    authority = handoff["external_authority_packet"]
    basis = _successor_basis(closure)
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 3,
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "source_third_handoff_receipt": deepcopy(handoff),
        "source_third_closure_receipt": deepcopy(closure),
        "consumed_external_authority_packet_digest": authority[
            "external_authority_packet_digest"
        ],
        "consumed_human_approval_receipt_digest": authority[
            "human_approval_receipt_digest"
        ],
        "consumed_host_license_digest": authority["host_license_digest"],
        "terminal_state_digest": _terminal_digest(closure),
        "successor_basis": basis,
        "successor_basis_digest": sha(basis),
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
        "next_act_started": False,
        "all_post_effect_blockers_active": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(RECEIPT_NON_AUTHORITY),
        "licensed_cycle_receipt_digest": "",
    }
    receipt["licensed_cycle_receipt_digest"] = receipt_digest(receipt)
    errors = validate_third_closed_cycle_receipt(receipt)
    if errors:
        raise ValueError("third_cycle_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_third_closed_cycle_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(receipt.get("version") == RECEIPT_VERSION, "receipt_version_invalid")
        req(receipt.get("licensed_cycle_receipt_digest") == receipt_digest(receipt), "receipt_digest_invalid")
        req(receipt.get("cycle_ordinal") == 3, "receipt_cycle_ordinal_invalid")
        handoff = dict(receipt.get("source_third_handoff_receipt", {}))
        closure = dict(receipt.get("source_third_closure_receipt", {}))
        errors += ["receipt_handoff_" + error for error in validate_third_licensed_act_handoff_receipt(handoff)]
        errors += ["receipt_closure_" + error for error in validate_third_native_evidence_closure_receipt(closure)]
        req(closure.get("source_third_handoff_receipt") == handoff, "receipt_handoff_closure_substitution")
        predecessor = handoff.get("predecessor_closed_cycle_receipt", {})
        req(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "receipt_predecessor_link_mismatch",
        )
        authority = handoff.get("external_authority_packet", {})
        req(
            receipt.get("consumed_external_authority_packet_digest")
            == authority.get("external_authority_packet_digest"),
            "receipt_authority_digest_mismatch",
        )
        req(
            receipt.get("consumed_human_approval_receipt_digest")
            == authority.get("human_approval_receipt_digest"),
            "receipt_approval_digest_mismatch",
        )
        req(
            receipt.get("consumed_host_license_digest")
            == authority.get("host_license_digest"),
            "receipt_host_license_digest_mismatch",
        )
        req(receipt.get("terminal_state_digest") == _terminal_digest(closure), "receipt_terminal_digest_mismatch")
        basis = dict(receipt.get("successor_basis", {}))
        req(basis == _successor_basis(closure), "receipt_successor_basis_substitution")
        req(receipt.get("successor_basis_digest") == sha(basis), "receipt_successor_basis_digest_invalid")
        expected = {
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
            "next_act_started": False,
            "all_post_effect_blockers_active": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(receipt.get(field) == value, f"receipt_{field}_invalid")
        req(receipt.get("receipt_consumption_count") == 0, "receipt_consumption_forbidden")
        req(dict(receipt.get("non_authority", {})) == RECEIPT_NON_AUTHORITY, "receipt_non_authority_invalid")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_materialized_third_cycle_extension_witness(
    base_chain: Mapping[str, Any],
    third_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_inductive_licensed_cycle_chain(base_chain)
    errors += validate_third_closed_cycle_receipt(third_receipt)
    if errors:
        raise ValueError("third_witness_source_invalid:" + ";".join(errors))
    closure = third_receipt["source_third_closure_receipt"]
    handoff = third_receipt["source_third_handoff_receipt"]
    authority = handoff["external_authority_packet"]
    witness = {
        "version": WITNESS_VERSION,
        "source_chain_digest": base_chain["inductive_chain_digest"],
        "source_prefix_digest": base_chain["prefix_digest"],
        "source_cycle_count": base_chain["cycle_count"],
        "target_cycle_ordinal": 3,
        "predecessor_cycle_receipt_digest": third_receipt[
            "predecessor_cycle_receipt_digest"
        ],
        "source_materialization_receipt_digest": handoff[
            "third_licensed_act_handoff_receipt_digest"
        ],
        "source_native_closure_receipt_digest": closure[
            "third_native_evidence_closure_receipt_digest"
        ],
        "source_blocker_certificate_digest": closure[
            "post_effect_blocker_certificate_digest"
        ],
        "source_world_projection_digest": closure[
            "post_effect_world_projection_digest"
        ],
        "fresh_external_authority_packet_digest": authority[
            "external_authority_packet_digest"
        ],
        "new_human_approval_receipt_digest": authority[
            "human_approval_receipt_digest"
        ],
        "new_host_license_digest": authority["host_license_digest"],
        "closed_cycle_receipt_digest": third_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "cycle_materialized": True,
        "native_closure_completed": True,
        "cycle_closed": True,
        "closed_cycle_immutable": True,
        "closed_cycle_append_only": True,
        "receipt_replay_forbidden": True,
        "receipt_consumption_count": 0,
        "authority_consumption_count": 1,
        "authority_single_use": True,
        "authority_renewable": False,
        "authority_inheritable": False,
        "next_act_started": False,
        "all_blockers_active": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "witness_only": True,
        "non_authority": deepcopy(WITNESS_NON_AUTHORITY),
        "extension_witness_digest": "",
    }
    witness["extension_witness_digest"] = extension_witness_digest(witness)
    errors = validate_closed_cycle_extension_witness(
        witness, source_chain=base_chain
    )
    if errors:
        raise ValueError("materialized_witness_invalid:" + ";".join(errors))
    return witness


def build_concrete_three_cycle_bundle(root: Path) -> dict[str, Any]:
    third = build_third_closed_cycle_receipt(root / "third")
    base = deepcopy(dict(third["source_third_handoff_receipt"]["source_inductive_chain"]))
    witness = build_materialized_third_cycle_extension_witness(base, third)
    chain = append_closed_cycle(base, witness)
    bundle = {
        "version": BUNDLE_VERSION,
        "cycle_id": CYCLE_ID,
        "source_two_cycle_chain": deepcopy(base),
        "source_two_cycle_chain_digest": base["inductive_chain_digest"],
        "third_cycle_receipt": deepcopy(third),
        "third_cycle_receipt_digest": third["licensed_cycle_receipt_digest"],
        "materialized_extension_witness": deepcopy(witness),
        "materialized_extension_witness_digest": witness[
            "extension_witness_digest"
        ],
        "three_cycle_chain": deepcopy(chain),
        "three_cycle_chain_digest": chain["inductive_chain_digest"],
        "cycle_count": 3,
        "cycle_ordinals": [1, 2, 3],
        "third_cycle_concrete": True,
        "third_act_effect_recorded": True,
        "third_native_closure_completed": True,
        "third_receipt_immutable": True,
        "v2_1_induction_witness_realized": True,
        "all_cycles_closed": True,
        "all_blockers_active": True,
        "next_act_started": False,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(BUNDLE_NON_AUTHORITY),
        "concrete_three_cycle_bundle_digest": "",
    }
    bundle["concrete_three_cycle_bundle_digest"] = bundle_digest(bundle)
    errors = validate_concrete_three_cycle_bundle(bundle)
    if errors:
        raise ValueError("concrete_three_cycle_bundle_invalid:" + ";".join(errors))
    return bundle


def validate_concrete_three_cycle_bundle(bundle: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(bundle.get("version") == BUNDLE_VERSION, "bundle_version_invalid")
        req(
            bundle.get("concrete_three_cycle_bundle_digest")
            == bundle_digest(bundle),
            "bundle_digest_invalid",
        )
        base = dict(bundle.get("source_two_cycle_chain", {}))
        errors += ["bundle_base_" + error for error in validate_inductive_licensed_cycle_chain(base)]
        third = dict(bundle.get("third_cycle_receipt", {}))
        errors += ["bundle_third_" + error for error in validate_third_closed_cycle_receipt(third)]
        witness = dict(bundle.get("materialized_extension_witness", {}))
        errors += [
            "bundle_witness_" + error
            for error in validate_closed_cycle_extension_witness(
                witness, source_chain=base
            )
        ]
        chain = dict(bundle.get("three_cycle_chain", {}))
        errors += ["bundle_chain_" + error for error in validate_inductive_licensed_cycle_chain(chain)]
        req(chain == append_closed_cycle(base, witness), "bundle_appended_chain_substitution")
        req(
            witness.get("closed_cycle_receipt_digest")
            == third.get("licensed_cycle_receipt_digest"),
            "bundle_witness_receipt_digest_mismatch",
        )
        req(
            bundle.get("source_two_cycle_chain_digest")
            == base.get("inductive_chain_digest"),
            "bundle_base_digest_mismatch",
        )
        req(
            bundle.get("third_cycle_receipt_digest")
            == third.get("licensed_cycle_receipt_digest"),
            "bundle_third_digest_mismatch",
        )
        req(
            bundle.get("materialized_extension_witness_digest")
            == witness.get("extension_witness_digest"),
            "bundle_witness_digest_mismatch",
        )
        req(
            bundle.get("three_cycle_chain_digest")
            == chain.get("inductive_chain_digest"),
            "bundle_chain_digest_mismatch",
        )
        req(bundle.get("cycle_count") == 3, "bundle_cycle_count_invalid")
        req(bundle.get("cycle_ordinals") == [1, 2, 3], "bundle_cycle_sequence_invalid")
        expected = {
            "third_cycle_concrete": True,
            "third_act_effect_recorded": True,
            "third_native_closure_completed": True,
            "third_receipt_immutable": True,
            "v2_1_induction_witness_realized": True,
            "all_cycles_closed": True,
            "all_blockers_active": True,
            "next_act_started": False,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(bundle.get(field) == value, f"bundle_{field}_invalid")
        req(dict(bundle.get("non_authority", {})) == BUNDLE_NON_AUTHORITY, "bundle_non_authority_invalid")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
