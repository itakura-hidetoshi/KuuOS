from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime import kuuos_qi_world_licensed_blocker_discharge_core_v1_7 as _core
from runtime.kuuos_qi_world_indra_transport_request_v1_6 import (
    build_indra_transport_request_receipt,
    validate_indra_transport_request_receipt,
)

_core.VERSION = "kuuos_qi_world_licensed_blocker_discharge_v1_7"
_core.AUTHORITY_VERSION = "kuuos_qi_world_external_authority_packet_v1_7"
_core.DISCHARGE_VERSION = "kuuos_qi_world_blocker_discharge_certificate_v1_7"
_core.RECEIPT_VERSION = "kuuos_qi_world_licensed_act_handoff_receipt_v1_7"
_core.CYCLE_ID = "qi-world-licensed-blocker-discharge-v17"

_ORIGINAL_VALIDATE_HANDOFF = _core.validate_licensed_act_handoff_receipt
_ORIGINAL_BUILD_BLOCKER_RECEIPT = _core.build_cross_cycle_blocker_receipt


def _indra_source(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = build_indra_transport_request_receipt(root)
    errors = validate_indra_transport_request_receipt(receipt)
    if errors:
        raise ValueError("source_indra_request_invalid:" + ";".join(errors))
    blocker = receipt["source_cross_cycle_blocker_receipt"]
    return receipt, deepcopy(dict(blocker))


def validate_licensed_act_handoff_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors = list(_ORIGINAL_VALIDATE_HANDOFF(receipt))

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        indra = dict(receipt.get("source_indra_transport_request_receipt", {}))
        errors.extend(
            "handoff_indra_" + error
            for error in validate_indra_transport_request_receipt(indra)
        )
        require(
            receipt.get("source_indra_transport_request_receipt_digest")
            == indra.get("indra_transport_request_receipt_digest"),
            "handoff_indra_receipt_digest_mismatch",
        )
        request = dict(indra.get("transport_request", {}))
        require(
            receipt.get("source_indra_transport_request_digest")
            == request.get("transport_request_digest"),
            "handoff_indra_request_digest_mismatch",
        )
        require(
            receipt.get("indra_transport_disposition")
            == "EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED",
            "handoff_indra_disposition_invalid",
        )
        require(
            indra.get("runtime_transport_realized") is False,
            "handoff_indra_transport_must_remain_unrealized",
        )
        require(
            indra.get("exact_world_updated") is False,
            "handoff_indra_exact_world_update_forbidden",
        )
        request_non_authority = dict(indra.get("request_non_authority", {}))
        require(
            bool(request_non_authority)
            and all(value is False for value in request_non_authority.values()),
            "handoff_indra_request_authority_escalation",
        )

        source = dict(receipt.get("source_blocker_receipt", {}))
        indra_blocker = dict(indra.get("source_cross_cycle_blocker_receipt", {}))
        require(
            source == indra_blocker,
            "handoff_indra_blocker_receipt_substitution",
        )
        source_certificate = dict(source.get("blocker_certificate", {}))
        source_vector = dict(source_certificate.get("composed_blocker_vector", {}))
        require(
            all(source_vector.get(name) is True for name in _core.BLOCKER_ORDER),
            "handoff_source_blocker_vector_not_all_active",
        )

        act_state = dict(receipt.get("target_act_state", {}))
        authorization = dict(act_state.get("step_authorization", {}))
        external_authority = dict(receipt.get("external_authority_packet", {}))
        plan_activation = dict(receipt.get("plan_activation_receipt", {}))

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
        require(
            receipt.get("external_authority_not_analytic_transport_receipt") is True,
            "handoff_external_authority_transport_conflation",
        )
        require(
            receipt.get("indra_transport_still_unrealized") is True,
            "handoff_indra_transport_realization_claim",
        )
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_licensed_act_handoff_receipt(root: Path) -> dict[str, Any]:
    indra, blocker = _indra_source(root / "indra-v16")
    original_builder = _core.build_cross_cycle_blocker_receipt
    _core.build_cross_cycle_blocker_receipt = lambda _: deepcopy(blocker)
    try:
        receipt = _core.build_licensed_act_handoff_receipt(root / "licensed-v17")
    finally:
        _core.build_cross_cycle_blocker_receipt = original_builder

    receipt["source_indra_transport_request_receipt"] = deepcopy(indra)
    receipt["source_indra_transport_request_receipt_digest"] = indra[
        "indra_transport_request_receipt_digest"
    ]
    receipt["source_indra_transport_request_digest"] = indra[
        "transport_request"
    ]["transport_request_digest"]
    receipt["indra_transport_disposition"] = indra["disposition"]
    receipt["external_authority_not_analytic_transport_receipt"] = True
    receipt["indra_transport_still_unrealized"] = True
    receipt["licensed_act_handoff_receipt_digest"] = ""
    receipt["licensed_act_handoff_receipt_digest"] = (
        _core.licensed_handoff_receipt_digest(receipt)
    )
    errors = validate_licensed_act_handoff_receipt(receipt)
    if errors:
        raise ValueError("licensed_handoff_invalid:" + ";".join(errors))
    return receipt


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
