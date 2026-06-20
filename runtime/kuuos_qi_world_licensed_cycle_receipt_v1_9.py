from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    AUTHORITY_VERSION,
    authority_packet_digest,
    validate_licensed_act_handoff_receipt,
)
from runtime.kuuos_qi_world_licensed_effect_evidence_closure_public_v1_8 import (
    BLOCKER_ORDER,
    build_licensed_effect_evidence_closure_receipt,
    validate_licensed_effect_evidence_closure_receipt,
)

VERSION = "kuuos_qi_world_licensed_cycle_receipt_v1_9"
RECEIPT_VERSION = "kuuos_qi_world_closed_licensed_cycle_receipt_v1_9"
REQUIREMENT_VERSION = "kuuos_qi_world_successor_authority_requirement_v1_9"
INTAKE_VERSION = "kuuos_qi_world_successor_authority_intake_v1_9"
CYCLE_ID = "qi-world-licensed-cycle-receipt-v19"

CYCLE_NON_AUTHORITY = {
    "receipt_grants_execution": False,
    "receipt_grants_truth": False,
    "receipt_grants_world_identity": False,
    "receipt_grants_memory_overwrite": False,
    "receipt_issues_successor_authority": False,
    "receipt_renews_consumed_authority": False,
}

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


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def licensed_cycle_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "licensed_cycle_receipt_digest")


def successor_authority_requirement_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_authority_requirement_digest")


def successor_authority_intake_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_authority_intake_digest")


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
            "post_effect_world_projection_digest": world["world_projection_digest"],
        }
    )


def _authority_consumption_digest(handoff: Mapping[str, Any]) -> str:
    authority = dict(handoff["external_authority_packet"])
    discharge = dict(handoff["blocker_discharge_certificate"])
    return sha(
        {
            "external_authority_packet_digest": authority[
                "external_authority_packet_digest"
            ],
            "blocker_discharge_certificate_digest": discharge[
                "blocker_discharge_certificate_digest"
            ],
            "released_act_state_digest": discharge["released_act_state_digest"],
            "release_consumption_count": discharge["release_consumption_count"],
            "single_use_release": discharge["single_use_release"],
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
        "post_effect_world_projection_digest": world["world_projection_digest"],
        "all_required_blockers_active": blocker["all_required_blockers_active"],
        "next_act_not_started": blocker["next_act_not_started"],
    }


def build_licensed_cycle_receipt(root: Path) -> dict[str, Any]:
    closure = build_licensed_effect_evidence_closure_receipt(root / "closure-v18")
    closure_errors = validate_licensed_effect_evidence_closure_receipt(closure)
    if closure_errors:
        raise ValueError("source_v18_invalid:" + ";".join(closure_errors))

    handoff = dict(closure["source_licensed_handoff_receipt"])
    handoff_errors = validate_licensed_act_handoff_receipt(handoff)
    if handoff_errors:
        raise ValueError("source_v17_invalid:" + ";".join(handoff_errors))

    authority = dict(handoff["external_authority_packet"])
    blocker = dict(closure["post_effect_blocker_certificate"])
    successor_basis = _successor_basis(closure)
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 1,
        "predecessor_cycle_receipt_digest": "",
        "source_v17_handoff_receipt": deepcopy(handoff),
        "source_v17_handoff_receipt_digest": handoff[
            "licensed_act_handoff_receipt_digest"
        ],
        "source_v18_closure_receipt": deepcopy(closure),
        "source_v18_closure_receipt_digest": closure[
            "licensed_effect_evidence_closure_receipt_digest"
        ],
        "consumed_external_authority_packet_digest": authority[
            "external_authority_packet_digest"
        ],
        "consumed_human_approval_receipt_digest": authority[
            "human_approval_receipt_digest"
        ],
        "consumed_host_license_digest": authority["host_license_digest"],
        "authority_consumption_digest": _authority_consumption_digest(handoff),
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
        "all_post_effect_blockers_active": blocker[
            "all_required_blockers_active"
        ],
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CYCLE_NON_AUTHORITY),
        "licensed_cycle_receipt_digest": "",
    }
    receipt["licensed_cycle_receipt_digest"] = licensed_cycle_receipt_digest(
        receipt
    )
    errors = validate_licensed_cycle_receipt(receipt)
    if errors:
        raise ValueError("licensed_cycle_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_licensed_cycle_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == RECEIPT_VERSION, "cycle_receipt_version_invalid")
        require(
            receipt.get("licensed_cycle_receipt_digest")
            == licensed_cycle_receipt_digest(receipt),
            "cycle_receipt_digest_invalid",
        )
        require(receipt.get("cycle_ordinal") == 1, "cycle_receipt_ordinal_invalid")
        require(
            receipt.get("predecessor_cycle_receipt_digest") == "",
            "cycle_receipt_genesis_predecessor_invalid",
        )

        handoff = dict(receipt.get("source_v17_handoff_receipt", {}))
        errors.extend(
            "cycle_receipt_v17_" + error
            for error in validate_licensed_act_handoff_receipt(handoff)
        )
        require(
            receipt.get("source_v17_handoff_receipt_digest")
            == handoff.get("licensed_act_handoff_receipt_digest"),
            "cycle_receipt_v17_digest_mismatch",
        )

        closure = dict(receipt.get("source_v18_closure_receipt", {}))
        errors.extend(
            "cycle_receipt_v18_" + error
            for error in validate_licensed_effect_evidence_closure_receipt(closure)
        )
        require(
            receipt.get("source_v18_closure_receipt_digest")
            == closure.get("licensed_effect_evidence_closure_receipt_digest"),
            "cycle_receipt_v18_digest_mismatch",
        )
        require(
            dict(closure.get("source_licensed_handoff_receipt", {})) == handoff,
            "cycle_receipt_v17_v18_handoff_substitution",
        )

        authority = dict(handoff.get("external_authority_packet", {}))
        require(
            receipt.get("consumed_external_authority_packet_digest")
            == authority.get("external_authority_packet_digest"),
            "cycle_receipt_consumed_authority_digest_mismatch",
        )
        require(
            receipt.get("consumed_human_approval_receipt_digest")
            == authority.get("human_approval_receipt_digest"),
            "cycle_receipt_consumed_human_approval_mismatch",
        )
        require(
            receipt.get("consumed_host_license_digest")
            == authority.get("host_license_digest"),
            "cycle_receipt_consumed_host_license_mismatch",
        )
        require(
            receipt.get("authority_consumption_digest")
            == _authority_consumption_digest(handoff),
            "cycle_receipt_authority_consumption_digest_mismatch",
        )
        require(
            handoff.get("release_consumed") is True
            and handoff.get("release_consumption_count") == 1,
            "cycle_receipt_authority_not_consumed_once",
        )
        require(
            dict(handoff.get("blocker_discharge_certificate", {})).get(
                "single_use_release"
            )
            is True,
            "cycle_receipt_authority_not_single_use",
        )

        require(
            receipt.get("terminal_state_digest") == _terminal_state_digest(closure),
            "cycle_receipt_terminal_state_digest_mismatch",
        )
        successor_basis = dict(receipt.get("successor_basis", {}))
        require(
            successor_basis == _successor_basis(closure),
            "cycle_receipt_successor_basis_substitution",
        )
        require(
            receipt.get("successor_basis_digest") == sha(successor_basis),
            "cycle_receipt_successor_basis_digest_invalid",
        )
        blocker = dict(closure.get("post_effect_blocker_certificate", {}))
        require(
            blocker.get("missing_blockers") == []
            and blocker.get("all_required_blockers_active") is True
            and all(
                dict(blocker.get("composed_blocker_vector", {})).get(name) is True
                for name in BLOCKER_ORDER
            ),
            "cycle_receipt_terminal_blockers_not_all_active",
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
        for field, expected in expected_flags.items():
            require(receipt.get(field) == expected, f"cycle_receipt_{field}_invalid")
        require(
            receipt.get("receipt_consumption_count") == 0,
            "cycle_receipt_replay_or_consumption_forbidden",
        )
        require(
            dict(receipt.get("non_authority", {})) == CYCLE_NON_AUTHORITY,
            "cycle_receipt_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_successor_authority_requirement(
    closed_cycle_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_licensed_cycle_receipt(closed_cycle_receipt)
    if errors:
        raise ValueError("closed_cycle_invalid:" + ";".join(errors))
    basis = dict(closed_cycle_receipt["successor_basis"])
    requirement = {
        "version": REQUIREMENT_VERSION,
        "predecessor_cycle_receipt_digest": closed_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "predecessor_cycle_ordinal": closed_cycle_receipt["cycle_ordinal"],
        "target_cycle_ordinal": int(closed_cycle_receipt["cycle_ordinal"]) + 1,
        "source_successor_basis_digest": closed_cycle_receipt[
            "successor_basis_digest"
        ],
        "source_next_plan_state_digest": basis["next_plan_state_digest"],
        "source_next_plan_basis_digest": basis["next_plan_basis_digest"],
        "source_next_committed_plan_digest": basis[
            "next_committed_plan_digest"
        ],
        "source_post_effect_blocker_certificate_digest": basis[
            "post_effect_blocker_certificate_digest"
        ],
        "forbidden_external_authority_packet_digest": closed_cycle_receipt[
            "consumed_external_authority_packet_digest"
        ],
        "forbidden_human_approval_receipt_digest": closed_cycle_receipt[
            "consumed_human_approval_receipt_digest"
        ],
        "forbidden_host_license_digest": closed_cycle_receipt[
            "consumed_host_license_digest"
        ],
        "fresh_external_authority_required": True,
        "distinct_external_authority_digest_required": True,
        "new_human_approval_required": True,
        "new_host_license_required": True,
        "external_issuer_required": True,
        "self_issue_forbidden": True,
        "single_use_required": True,
        "all_source_blockers_active": True,
        "predecessor_receipt_read_only": True,
        "successor_act_started": False,
        "explicit_v1_7_discharge_still_required": True,
        "non_authority": deepcopy(REQUIREMENT_NON_AUTHORITY),
        "successor_authority_requirement_digest": "",
    }
    requirement["successor_authority_requirement_digest"] = (
        successor_authority_requirement_digest(requirement)
    )
    validation = validate_successor_authority_requirement(
        requirement,
        closed_cycle_receipt=closed_cycle_receipt,
    )
    if validation:
        raise ValueError("successor_requirement_invalid:" + ";".join(validation))
    return requirement


def validate_successor_authority_requirement(
    requirement: Mapping[str, Any],
    *,
    closed_cycle_receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        errors.extend(
            "successor_requirement_source_" + error
            for error in validate_licensed_cycle_receipt(closed_cycle_receipt)
        )
        require(
            requirement.get("version") == REQUIREMENT_VERSION,
            "successor_requirement_version_invalid",
        )
        require(
            requirement.get("successor_authority_requirement_digest")
            == successor_authority_requirement_digest(requirement),
            "successor_requirement_digest_invalid",
        )
        require(
            requirement.get("predecessor_cycle_receipt_digest")
            == closed_cycle_receipt.get("licensed_cycle_receipt_digest"),
            "successor_requirement_predecessor_mismatch",
        )
        require(
            requirement.get("target_cycle_ordinal")
            == int(closed_cycle_receipt.get("cycle_ordinal", -1)) + 1,
            "successor_requirement_target_ordinal_invalid",
        )
        basis = dict(closed_cycle_receipt.get("successor_basis", {}))
        expected = {
            "source_successor_basis_digest": closed_cycle_receipt.get(
                "successor_basis_digest"
            ),
            "source_next_plan_state_digest": basis.get("next_plan_state_digest"),
            "source_next_plan_basis_digest": basis.get("next_plan_basis_digest"),
            "source_next_committed_plan_digest": basis.get(
                "next_committed_plan_digest"
            ),
            "source_post_effect_blocker_certificate_digest": basis.get(
                "post_effect_blocker_certificate_digest"
            ),
            "forbidden_external_authority_packet_digest": closed_cycle_receipt.get(
                "consumed_external_authority_packet_digest"
            ),
            "forbidden_human_approval_receipt_digest": closed_cycle_receipt.get(
                "consumed_human_approval_receipt_digest"
            ),
            "forbidden_host_license_digest": closed_cycle_receipt.get(
                "consumed_host_license_digest"
            ),
        }
        for field, value in expected.items():
            require(requirement.get(field) == value, f"successor_requirement_{field}_invalid")
        for field in (
            "fresh_external_authority_required",
            "distinct_external_authority_digest_required",
            "new_human_approval_required",
            "new_host_license_required",
            "external_issuer_required",
            "self_issue_forbidden",
            "single_use_required",
            "all_source_blockers_active",
            "predecessor_receipt_read_only",
            "explicit_v1_7_discharge_still_required",
        ):
            require(requirement.get(field) is True, f"successor_requirement_{field}_invalid")
        require(
            requirement.get("successor_act_started") is False,
            "successor_requirement_act_started",
        )
        require(
            dict(requirement.get("non_authority", {}))
            == REQUIREMENT_NON_AUTHORITY,
            "successor_requirement_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_successor_authority_intake(
    *,
    requirement: Mapping[str, Any],
    closed_cycle_receipt: Mapping[str, Any],
    candidate_external_authority_packet: Mapping[str, Any],
) -> dict[str, Any]:
    requirement_errors = validate_successor_authority_requirement(
        requirement,
        closed_cycle_receipt=closed_cycle_receipt,
    )
    if requirement_errors:
        raise ValueError("successor_requirement_invalid:" + ";".join(requirement_errors))

    candidate = dict(candidate_external_authority_packet)
    old_authority_digest = requirement[
        "forbidden_external_authority_packet_digest"
    ]
    old_approval_digest = requirement[
        "forbidden_human_approval_receipt_digest"
    ]
    old_host_digest = requirement["forbidden_host_license_digest"]

    candidate_digest = candidate.get("external_authority_packet_digest")
    if candidate.get("version") != AUTHORITY_VERSION:
        raise ValueError("successor_candidate_authority_version_invalid")
    if candidate_digest != authority_packet_digest(candidate):
        raise ValueError("successor_candidate_authority_digest_invalid")
    if candidate_digest == old_authority_digest:
        raise ValueError("successor_authority_digest_reuse_forbidden")
    if candidate.get("human_approval_receipt_digest") == old_approval_digest:
        raise ValueError("successor_human_approval_reuse_forbidden")
    if candidate.get("host_license_digest") == old_host_digest:
        raise ValueError("successor_host_license_reuse_forbidden")
    if candidate.get("source_plan_state_digest") != requirement.get(
        "source_next_plan_state_digest"
    ):
        raise ValueError("successor_candidate_plan_state_mismatch")
    if candidate.get("source_plan_basis_digest") != requirement.get(
        "source_next_plan_basis_digest"
    ):
        raise ValueError("successor_candidate_plan_basis_mismatch")
    if candidate.get("source_committed_plan_digest") != requirement.get(
        "source_next_committed_plan_digest"
    ):
        raise ValueError("successor_candidate_committed_plan_mismatch")
    if candidate.get("external_issuer") is not True:
        raise ValueError("successor_candidate_external_issuer_required")
    if candidate.get("self_issued") is not False:
        raise ValueError("successor_candidate_self_issue_forbidden")
    if candidate.get("single_use") is not True:
        raise ValueError("successor_candidate_single_use_required")

    intake = {
        "version": INTAKE_VERSION,
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "predecessor_cycle_receipt_digest": closed_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "target_cycle_ordinal": requirement["target_cycle_ordinal"],
        "candidate_external_authority_packet_digest": candidate_digest,
        "previous_external_authority_packet_digest": old_authority_digest,
        "candidate_human_approval_receipt_digest": candidate[
            "human_approval_receipt_digest"
        ],
        "previous_human_approval_receipt_digest": old_approval_digest,
        "candidate_host_license_digest": candidate["host_license_digest"],
        "previous_host_license_digest": old_host_digest,
        "authority_digest_distinct": True,
        "human_approval_distinct": True,
        "host_license_distinct": True,
        "candidate_external_issuer": True,
        "candidate_self_issued": False,
        "candidate_single_use": True,
        "candidate_bound_to_next_plan": True,
        "freshness_qualified": True,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
        "successor_act_started": False,
        "explicit_v1_7_discharge_still_required": True,
        "non_authority": deepcopy(INTAKE_NON_AUTHORITY),
        "successor_authority_intake_digest": "",
    }
    intake["successor_authority_intake_digest"] = successor_authority_intake_digest(
        intake
    )
    errors = validate_successor_authority_intake(
        intake,
        requirement=requirement,
        closed_cycle_receipt=closed_cycle_receipt,
        candidate_external_authority_packet=candidate,
    )
    if errors:
        raise ValueError("successor_intake_invalid:" + ";".join(errors))
    return intake


def validate_successor_authority_intake(
    intake: Mapping[str, Any],
    *,
    requirement: Mapping[str, Any],
    closed_cycle_receipt: Mapping[str, Any],
    candidate_external_authority_packet: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        errors.extend(
            "successor_intake_requirement_" + error
            for error in validate_successor_authority_requirement(
                requirement,
                closed_cycle_receipt=closed_cycle_receipt,
            )
        )
        candidate = dict(candidate_external_authority_packet)
        require(intake.get("version") == INTAKE_VERSION, "successor_intake_version_invalid")
        require(
            intake.get("successor_authority_intake_digest")
            == successor_authority_intake_digest(intake),
            "successor_intake_digest_invalid",
        )
        expected = {
            "successor_authority_requirement_digest": requirement.get(
                "successor_authority_requirement_digest"
            ),
            "predecessor_cycle_receipt_digest": closed_cycle_receipt.get(
                "licensed_cycle_receipt_digest"
            ),
            "target_cycle_ordinal": requirement.get("target_cycle_ordinal"),
            "candidate_external_authority_packet_digest": candidate.get(
                "external_authority_packet_digest"
            ),
            "previous_external_authority_packet_digest": requirement.get(
                "forbidden_external_authority_packet_digest"
            ),
            "candidate_human_approval_receipt_digest": candidate.get(
                "human_approval_receipt_digest"
            ),
            "previous_human_approval_receipt_digest": requirement.get(
                "forbidden_human_approval_receipt_digest"
            ),
            "candidate_host_license_digest": candidate.get("host_license_digest"),
            "previous_host_license_digest": requirement.get(
                "forbidden_host_license_digest"
            ),
        }
        for field, value in expected.items():
            require(intake.get(field) == value, f"successor_intake_{field}_invalid")
        require(
            candidate.get("external_authority_packet_digest")
            != requirement.get("forbidden_external_authority_packet_digest"),
            "successor_authority_digest_reuse_forbidden",
        )
        require(
            candidate.get("human_approval_receipt_digest")
            != requirement.get("forbidden_human_approval_receipt_digest"),
            "successor_human_approval_reuse_forbidden",
        )
        require(
            candidate.get("host_license_digest")
            != requirement.get("forbidden_host_license_digest"),
            "successor_host_license_reuse_forbidden",
        )
        for field in (
            "authority_digest_distinct",
            "human_approval_distinct",
            "host_license_distinct",
            "candidate_external_issuer",
            "candidate_single_use",
            "candidate_bound_to_next_plan",
            "freshness_qualified",
            "explicit_v1_7_discharge_still_required",
        ):
            require(intake.get(field) is True, f"successor_intake_{field}_invalid")
        for field in (
            "candidate_self_issued",
            "predecessor_authority_inherited",
            "predecessor_authority_renewed",
            "successor_act_started",
        ):
            require(intake.get(field) is False, f"successor_intake_{field}_invalid")
        require(
            dict(intake.get("non_authority", {})) == INTAKE_NON_AUTHORITY,
            "successor_intake_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
