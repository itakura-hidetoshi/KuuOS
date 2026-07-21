from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime import kuuos_qi_world_successor_cycle_materialization_v2_0 as _core
from runtime import kuuos_qi_world_licensed_cycle_receipt_public_v1_9 as _v19

REQUIREMENT_VERSION = "kuuos_qi_world_dual_basis_successor_authority_requirement_v2_0"
INTAKE_VERSION = "kuuos_qi_world_dual_basis_successor_authority_intake_v2_0"


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return _core.sha(packet)


def requirement_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_authority_requirement_digest")


def intake_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_authority_intake_digest")


def build_successor_authority_requirement(
    predecessor: Mapping[str, Any],
) -> dict[str, Any]:
    errors = _v19.validate_licensed_cycle_receipt(predecessor)
    if errors:
        raise ValueError("predecessor_cycle_invalid:" + ";".join(errors))
    closure = dict(predecessor["source_v18_closure_receipt"])
    plan = dict(closure["next_cycle_artifacts"]["PlanOS"])
    basis = dict(predecessor["successor_basis"])
    requirement = {
        "version": REQUIREMENT_VERSION,
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "predecessor_cycle_ordinal": predecessor["cycle_ordinal"],
        "target_cycle_ordinal": int(predecessor["cycle_ordinal"]) + 1,
        "source_successor_basis_digest": predecessor["successor_basis_digest"],
        "source_next_plan_state_digest": plan["plan_state_digest"],
        "source_learning_plan_basis_digest": plan["next_plan_basis_digest"],
        "source_execution_plan_basis_digest": plan["plan_basis_digest"],
        "source_next_plan_basis_digest": plan["plan_basis_digest"],
        "source_next_committed_plan_digest": plan[
            "latest_committed_plan_digest"
        ],
        "source_post_effect_blocker_certificate_digest": basis[
            "post_effect_blocker_certificate_digest"
        ],
        "forbidden_external_authority_packet_digest": predecessor[
            "consumed_external_authority_packet_digest"
        ],
        "forbidden_human_approval_receipt_digest": predecessor[
            "consumed_human_approval_receipt_digest"
        ],
        "forbidden_host_license_digest": predecessor[
            "consumed_host_license_digest"
        ],
        "dual_basis_separation_preserved": True,
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
        "non_authority": deepcopy(_v19.REQUIREMENT_NON_AUTHORITY),
        "successor_authority_requirement_digest": "",
    }
    requirement["successor_authority_requirement_digest"] = requirement_digest(
        requirement
    )
    validation = validate_successor_authority_requirement(
        requirement,
        closed_cycle_receipt=predecessor,
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
            "successor_requirement_predecessor_" + error
            for error in _v19.validate_licensed_cycle_receipt(
                closed_cycle_receipt
            )
        )
        closure = dict(closed_cycle_receipt["source_v18_closure_receipt"])
        plan = dict(closure["next_cycle_artifacts"]["PlanOS"])
        basis = dict(closed_cycle_receipt["successor_basis"])
        require(
            requirement.get("version") == REQUIREMENT_VERSION,
            "successor_requirement_version_invalid",
        )
        require(
            requirement.get("successor_authority_requirement_digest")
            == requirement_digest(requirement),
            "successor_requirement_digest_invalid",
        )
        expected = {
            "predecessor_cycle_receipt_digest": closed_cycle_receipt.get(
                "licensed_cycle_receipt_digest"
            ),
            "predecessor_cycle_ordinal": closed_cycle_receipt.get(
                "cycle_ordinal"
            ),
            "target_cycle_ordinal": int(
                closed_cycle_receipt.get("cycle_ordinal", -1)
            )
            + 1,
            "source_successor_basis_digest": closed_cycle_receipt.get(
                "successor_basis_digest"
            ),
            "source_next_plan_state_digest": plan.get("plan_state_digest"),
            "source_learning_plan_basis_digest": plan.get(
                "next_plan_basis_digest"
            ),
            "source_execution_plan_basis_digest": plan.get(
                "plan_basis_digest"
            ),
            "source_next_plan_basis_digest": plan.get("plan_basis_digest"),
            "source_next_committed_plan_digest": plan.get(
                "latest_committed_plan_digest"
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
            require(
                requirement.get(field) == value,
                f"successor_requirement_{field}_invalid",
            )
        for field in (
            "dual_basis_separation_preserved",
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
            require(
                requirement.get(field) is True,
                f"successor_requirement_{field}_invalid",
            )
        require(
            requirement.get("successor_act_started") is False,
            "successor_requirement_act_started",
        )
        require(
            dict(requirement.get("non_authority", {}))
            == _v19.REQUIREMENT_NON_AUTHORITY,
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
    errors = validate_successor_authority_requirement(
        requirement,
        closed_cycle_receipt=closed_cycle_receipt,
    )
    if errors:
        raise ValueError("successor_requirement_invalid:" + ";".join(errors))
    candidate = dict(candidate_external_authority_packet)
    old_authority = requirement["forbidden_external_authority_packet_digest"]
    old_approval = requirement["forbidden_human_approval_receipt_digest"]
    old_host = requirement["forbidden_host_license_digest"]
    checks = {
        "successor_candidate_authority_version_invalid": (
            candidate.get("version") == _core.AUTHORITY_VERSION
        ),
        "successor_candidate_authority_digest_invalid": (
            candidate.get("external_authority_packet_digest")
            == _core.authority_packet_digest(candidate)
        ),
        "successor_authority_digest_reuse_forbidden": (
            candidate.get("external_authority_packet_digest") != old_authority
        ),
        "successor_human_approval_reuse_forbidden": (
            candidate.get("human_approval_receipt_digest") != old_approval
        ),
        "successor_host_license_reuse_forbidden": (
            candidate.get("host_license_digest") != old_host
        ),
        "successor_candidate_plan_state_mismatch": (
            candidate.get("source_plan_state_digest")
            == requirement.get("source_next_plan_state_digest")
        ),
        "successor_candidate_execution_plan_basis_mismatch": (
            candidate.get("source_plan_basis_digest")
            == requirement.get("source_execution_plan_basis_digest")
        ),
        "successor_candidate_committed_plan_mismatch": (
            candidate.get("source_committed_plan_digest")
            == requirement.get("source_next_committed_plan_digest")
        ),
        "successor_candidate_external_issuer_required": (
            candidate.get("external_issuer") is True
        ),
        "successor_candidate_self_issue_forbidden": (
            candidate.get("self_issued") is False
        ),
        "successor_candidate_single_use_required": (
            candidate.get("single_use") is True
        ),
    }
    for code, condition in checks.items():
        if not condition:
            raise ValueError(code)
    intake = {
        "version": INTAKE_VERSION,
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "predecessor_cycle_receipt_digest": closed_cycle_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "target_cycle_ordinal": requirement["target_cycle_ordinal"],
        "candidate_external_authority_packet_digest": candidate[
            "external_authority_packet_digest"
        ],
        "previous_external_authority_packet_digest": old_authority,
        "candidate_human_approval_receipt_digest": candidate[
            "human_approval_receipt_digest"
        ],
        "previous_human_approval_receipt_digest": old_approval,
        "candidate_host_license_digest": candidate["host_license_digest"],
        "previous_host_license_digest": old_host,
        "source_learning_plan_basis_digest": requirement[
            "source_learning_plan_basis_digest"
        ],
        "source_execution_plan_basis_digest": requirement[
            "source_execution_plan_basis_digest"
        ],
        "authority_digest_distinct": True,
        "human_approval_distinct": True,
        "host_license_distinct": True,
        "dual_basis_separation_preserved": True,
        "candidate_external_issuer": True,
        "candidate_self_issued": False,
        "candidate_single_use": True,
        "candidate_bound_to_next_plan": True,
        "freshness_qualified": True,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
        "successor_act_started": False,
        "explicit_v1_7_discharge_still_required": True,
        "non_authority": deepcopy(_v19.INTAKE_NON_AUTHORITY),
        "successor_authority_intake_digest": "",
    }
    intake["successor_authority_intake_digest"] = intake_digest(intake)
    validation = validate_successor_authority_intake(
        intake,
        requirement=requirement,
        closed_cycle_receipt=closed_cycle_receipt,
        candidate_external_authority_packet=candidate,
    )
    if validation:
        raise ValueError("successor_intake_invalid:" + ";".join(validation))
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
        require(
            intake.get("version") == INTAKE_VERSION,
            "successor_intake_version_invalid",
        )
        require(
            intake.get("successor_authority_intake_digest")
            == intake_digest(intake),
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
            "source_learning_plan_basis_digest": requirement.get(
                "source_learning_plan_basis_digest"
            ),
            "source_execution_plan_basis_digest": requirement.get(
                "source_execution_plan_basis_digest"
            ),
        }
        for field, value in expected.items():
            require(
                intake.get(field) == value,
                f"successor_intake_{field}_invalid",
            )
        require(
            candidate.get("external_authority_packet_digest")
            == _core.authority_packet_digest(candidate),
            "successor_candidate_authority_digest_invalid",
        )
        require(
            candidate.get("source_plan_state_digest")
            == requirement.get("source_next_plan_state_digest"),
            "successor_candidate_plan_state_mismatch",
        )
        require(
            candidate.get("source_plan_basis_digest")
            == requirement.get("source_execution_plan_basis_digest"),
            "successor_candidate_execution_plan_basis_mismatch",
        )
        require(
            candidate.get("source_committed_plan_digest")
            == requirement.get("source_next_committed_plan_digest"),
            "successor_candidate_committed_plan_mismatch",
        )
        for field in (
            "authority_digest_distinct",
            "human_approval_distinct",
            "host_license_distinct",
            "dual_basis_separation_preserved",
            "candidate_external_issuer",
            "candidate_single_use",
            "candidate_bound_to_next_plan",
            "freshness_qualified",
            "explicit_v1_7_discharge_still_required",
        ):
            require(
                intake.get(field) is True,
                f"successor_intake_{field}_invalid",
            )
        for field in (
            "candidate_self_issued",
            "predecessor_authority_inherited",
            "predecessor_authority_renewed",
            "successor_act_started",
        ):
            require(
                intake.get(field) is False,
                f"successor_intake_{field}_invalid",
            )
        require(
            dict(intake.get("non_authority", {}))
            == _v19.INTAKE_NON_AUTHORITY,
            "successor_intake_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


_core.build_successor_authority_requirement = build_successor_authority_requirement
_core.validate_successor_authority_requirement = validate_successor_authority_requirement
_core.build_successor_authority_intake = build_successor_authority_intake
_core.validate_successor_authority_intake = validate_successor_authority_intake

VERSION = _core.VERSION
build_successor_cycle_materialization_receipt = (
    _core.build_successor_cycle_materialization_receipt
)
validate_successor_cycle_materialization_receipt = (
    _core.validate_successor_cycle_materialization_receipt
)
materialization_receipt_digest = _core.materialization_receipt_digest
second_cycle_receipt_digest = _core.second_cycle_receipt_digest
successor_blocker_certificate_digest = _core.successor_blocker_certificate_digest
successor_blocker_receipt_digest = _core.successor_blocker_receipt_digest
successor_closure_receipt_digest = _core.successor_closure_receipt_digest
validate_second_cycle_receipt = _core.validate_second_cycle_receipt
validate_successor_blocker_receipt = _core.validate_successor_blocker_receipt
validate_successor_closure_receipt = _core.validate_successor_closure_receipt
validate_successor_external_authority = _core.validate_successor_external_authority
