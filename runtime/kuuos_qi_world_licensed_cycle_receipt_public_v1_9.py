from __future__ import annotations

from typing import Any, Mapping

from runtime import kuuos_qi_world_licensed_cycle_receipt_v1_9 as _core

_ORIGINAL_VALIDATE_REQUIREMENT = _core.validate_successor_authority_requirement
_ORIGINAL_VALIDATE_INTAKE = _core.validate_successor_authority_intake


def validate_successor_authority_requirement(
    requirement: Mapping[str, Any],
    *,
    closed_cycle_receipt: Mapping[str, Any],
) -> list[str]:
    errors = list(
        _ORIGINAL_VALIDATE_REQUIREMENT(
            requirement,
            closed_cycle_receipt=closed_cycle_receipt,
        )
    )

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(
            requirement.get("predecessor_cycle_ordinal")
            == closed_cycle_receipt.get("cycle_ordinal"),
            "successor_requirement_predecessor_ordinal_mismatch",
        )
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def validate_successor_authority_intake(
    intake: Mapping[str, Any],
    *,
    requirement: Mapping[str, Any],
    closed_cycle_receipt: Mapping[str, Any],
    candidate_external_authority_packet: Mapping[str, Any],
) -> list[str]:
    errors = list(
        _ORIGINAL_VALIDATE_INTAKE(
            intake,
            requirement=requirement,
            closed_cycle_receipt=closed_cycle_receipt,
            candidate_external_authority_packet=candidate_external_authority_packet,
        )
    )

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        candidate = dict(candidate_external_authority_packet)
        require(
            candidate.get("version") == _core.AUTHORITY_VERSION,
            "successor_candidate_authority_version_invalid",
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
            == requirement.get("source_next_plan_basis_digest"),
            "successor_candidate_plan_basis_mismatch",
        )
        require(
            candidate.get("source_committed_plan_digest")
            == requirement.get("source_next_committed_plan_digest"),
            "successor_candidate_committed_plan_mismatch",
        )
        require(
            candidate.get("external_issuer") is True,
            "successor_candidate_external_issuer_required",
        )
        require(
            candidate.get("self_issued") is False,
            "successor_candidate_self_issue_forbidden",
        )
        require(
            candidate.get("single_use") is True,
            "successor_candidate_single_use_required",
        )
        require(
            candidate.get("authority_does_not_widen_host_license") is True,
            "successor_candidate_host_license_widening_forbidden",
        )
        require(
            candidate.get("target_cycle_strictly_later") is True,
            "successor_candidate_target_cycle_not_later",
        )
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


_core.validate_successor_authority_requirement = (
    validate_successor_authority_requirement
)
_core.validate_successor_authority_intake = validate_successor_authority_intake

VERSION = _core.VERSION
RECEIPT_VERSION = _core.RECEIPT_VERSION
REQUIREMENT_VERSION = _core.REQUIREMENT_VERSION
INTAKE_VERSION = _core.INTAKE_VERSION
CYCLE_ID = _core.CYCLE_ID
CYCLE_NON_AUTHORITY = _core.CYCLE_NON_AUTHORITY
REQUIREMENT_NON_AUTHORITY = _core.REQUIREMENT_NON_AUTHORITY
INTAKE_NON_AUTHORITY = _core.INTAKE_NON_AUTHORITY
licensed_cycle_receipt_digest = _core.licensed_cycle_receipt_digest
successor_authority_requirement_digest = (
    _core.successor_authority_requirement_digest
)
successor_authority_intake_digest = _core.successor_authority_intake_digest
build_licensed_cycle_receipt = _core.build_licensed_cycle_receipt
validate_licensed_cycle_receipt = _core.validate_licensed_cycle_receipt
build_successor_authority_requirement = _core.build_successor_authority_requirement
build_successor_authority_intake = _core.build_successor_authority_intake
