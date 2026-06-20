from __future__ import annotations

from typing import Any, Mapping

from runtime import kuuos_qi_world_licensed_blocker_discharge_core_v1_6 as _core

_ORIGINAL_VALIDATE_HANDOFF = _core.validate_licensed_act_handoff_receipt


def validate_licensed_act_handoff_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors = list(_ORIGINAL_VALIDATE_HANDOFF(receipt))

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        source = dict(receipt.get("source_blocker_receipt", {}))
        source_certificate = dict(source.get("blocker_certificate", {}))
        source_vector = dict(source_certificate.get("composed_blocker_vector", {}))
        act_state = dict(receipt.get("target_act_state", {}))
        authorization = dict(act_state.get("step_authorization", {}))
        external_authority = dict(receipt.get("external_authority_packet", {}))
        plan_activation = dict(receipt.get("plan_activation_receipt", {}))

        require(
            all(source_vector.get(name) is True for name in _core.BLOCKER_ORDER),
            "handoff_source_blocker_vector_not_all_active",
        )
        require(
            authorization.get("act_phase_receipt_digest")
            == external_authority.get("external_authority_packet_digest"),
            "handoff_step_authorization_external_authority_mismatch",
        )
        require(
            authorization.get("host_license_digest")
            == external_authority.get("host_license_digest"),
            "handoff_step_authorization_host_license_mismatch",
        )
        require(
            authorization.get("human_approval_receipt_digest")
            == external_authority.get("human_approval_receipt_digest"),
            "handoff_step_authorization_human_approval_mismatch",
        )
        require(
            authorization.get("human_approver_id")
            == external_authority.get("human_approver_id"),
            "handoff_step_authorization_human_approver_mismatch",
        )
        require(
            authorization.get("source_plan_state_digest")
            == external_authority.get("source_plan_state_digest"),
            "handoff_step_authorization_plan_state_mismatch",
        )
        require(
            authorization.get("source_plan_basis_digest")
            == external_authority.get("source_plan_basis_digest"),
            "handoff_step_authorization_plan_basis_mismatch",
        )
        require(
            authorization.get("source_committed_plan_digest")
            == external_authority.get("source_committed_plan_digest"),
            "handoff_step_authorization_committed_plan_mismatch",
        )
        require(
            authorization.get("plan_activation_receipt_digest")
            == plan_activation.get("plan_activation_receipt_digest"),
            "handoff_step_authorization_plan_activation_mismatch",
        )
        release_scope = dict(external_authority.get("release_scope", {}))
        require(
            act_state.get("operation_id") == release_scope.get("operation_id"),
            "handoff_released_operation_scope_mismatch",
        )
        require(
            act_state.get("selected_step_id")
            == release_scope.get("selected_step_id"),
            "handoff_released_step_scope_mismatch",
        )
        require(
            int(act_state.get("act_version", -1)) == 1
            and int(act_state.get("committed_records", -1)) == 1,
            "handoff_release_not_single_commit",
        )
        require(
            [item.get("target_phase") for item in act_state.get("event_history", [])]
            == ["select", "authorize", "project", "invoke", "verify", "commit"],
            "handoff_act_phase_history_invalid",
        )
        require(
            receipt.get("host_tick_digest") == act_state.get("host_tick_digest"),
            "handoff_host_tick_mismatch",
        )
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


_core.validate_licensed_act_handoff_receipt = validate_licensed_act_handoff_receipt

VERSION = _core.VERSION
AUTHORITY_VERSION = _core.AUTHORITY_VERSION
DISCHARGE_VERSION = _core.DISCHARGE_VERSION
RECEIPT_VERSION = _core.RECEIPT_VERSION
CYCLE_ID = _core.CYCLE_ID
RELEASABLE_BLOCKERS = _core.RELEASABLE_BLOCKERS
INVARIANT_BLOCKERS = _core.INVARIANT_BLOCKERS
RELEASE_SCOPE = _core.RELEASE_SCOPE
RELEASE_NON_AUTHORITY = _core.RELEASE_NON_AUTHORITY
authority_packet_digest = _core.authority_packet_digest
discharge_certificate_digest = _core.discharge_certificate_digest
licensed_handoff_receipt_digest = _core.licensed_handoff_receipt_digest
build_external_authority_packet = _core.build_external_authority_packet
validate_external_authority_packet = _core.validate_external_authority_packet
build_blocker_discharge_certificate = _core.build_blocker_discharge_certificate
validate_blocker_discharge_certificate = _core.validate_blocker_discharge_certificate
build_licensed_act_handoff_receipt = _core.build_licensed_act_handoff_receipt
