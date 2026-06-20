from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_act_os_types_v0_1 import authorization_digest, state_digest
from runtime.kuuos_qi_world_indra_transport_request_v1_6 import (
    transport_receipt_digest,
)
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    INVARIANT_BLOCKERS,
    RELEASABLE_BLOCKERS,
    authority_packet_digest,
    build_licensed_act_handoff_receipt,
    discharge_certificate_digest,
    licensed_handoff_receipt_digest,
    validate_licensed_act_handoff_receipt,
)


def _retag(receipt: dict) -> dict:
    receipt["licensed_act_handoff_receipt_digest"] = ""
    receipt["licensed_act_handoff_receipt_digest"] = (
        licensed_handoff_receipt_digest(receipt)
    )
    return receipt


def _retag_authority(packet: dict) -> dict:
    packet["external_authority_packet_digest"] = ""
    packet["external_authority_packet_digest"] = authority_packet_digest(packet)
    return packet


def _retag_discharge(certificate: dict) -> dict:
    certificate["blocker_discharge_certificate_digest"] = ""
    certificate["blocker_discharge_certificate_digest"] = (
        discharge_certificate_digest(certificate)
    )
    return certificate


def _retag_act_state(state: dict) -> dict:
    state["act_state_digest"] = ""
    state["act_state_digest"] = state_digest(state)
    return state


def _retag_indra(receipt: dict) -> dict:
    receipt["indra_transport_request_receipt_digest"] = ""
    receipt["indra_transport_request_receipt_digest"] = transport_receipt_digest(
        receipt
    )
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_licensed_act_handoff_receipt(_retag(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_licensed_blocker_discharge_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-qi-world-licensed-discharge-v17-"
    ) as temporary:
        receipt = build_licensed_act_handoff_receipt(Path(temporary))
        assert validate_licensed_act_handoff_receipt(receipt) == []

        indra = receipt["source_indra_transport_request_receipt"]
        source = receipt["source_blocker_receipt"]
        source_digest = source["cross_cycle_blocker_receipt_digest"]
        source_certificate_digest = source["blocker_certificate"][
            "blocker_certificate_digest"
        ]
        authority = receipt["external_authority_packet"]
        discharge = receipt["blocker_discharge_certificate"]
        act = receipt["target_act_state"]
        authorization = act["step_authorization"]

        assert receipt["source_indra_transport_request_receipt_digest"] == indra[
            "indra_transport_request_receipt_digest"
        ]
        assert receipt["source_indra_transport_request_digest"] == indra[
            "transport_request"
        ]["transport_request_digest"]
        assert receipt["indra_transport_disposition"] == (
            "EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED"
        )
        assert receipt["external_authority_not_analytic_transport_receipt"] is True
        assert receipt["indra_transport_still_unrealized"] is True
        assert indra["runtime_transport_realized"] is False
        assert indra["exact_world_updated"] is False
        assert authority["released_blockers"] == list(RELEASABLE_BLOCKERS)
        assert authority["retained_invariant_blockers"] == list(
            INVARIANT_BLOCKERS
        )
        assert discharge["all_invariant_blockers_retained"] is True
        assert all(discharge["retained_invariant_blockers"].values())
        assert authority["self_issued"] is False
        assert authority["single_use"] is True
        assert receipt["release_consumption_count"] == 1
        assert receipt["target_cycle_strictly_later"] is True
        assert receipt["target_act_started"] is True
        assert receipt["effect_recorded"] is True
        assert receipt["observation_required"] is True
        assert receipt["verification_required"] is True
        assert receipt["memory_overwritten"] is False
        assert receipt["exact_world_updated"] is False
        assert receipt["truth_promoted"] is False
        assert receipt["same_cycle_recursive_invocation"] is False
        assert receipt["multi_world_collapsed"] is False
        assert authorization["act_phase_receipt_digest"] == authority[
            "external_authority_packet_digest"
        ]
        assert source == indra["source_cross_cycle_blocker_receipt"]
        assert source["cross_cycle_blocker_receipt_digest"] == source_digest
        assert source["blocker_certificate"][
            "blocker_certificate_digest"
        ] == source_certificate_digest

        indra_digest_substitution = deepcopy(receipt)
        indra_digest_substitution[
            "source_indra_transport_request_digest"
        ] = "substituted-indra-request-digest"
        _require_error(
            indra_digest_substitution,
            "handoff_indra_request_digest_mismatch",
        )

        realized_transport = deepcopy(receipt)
        changed_indra = realized_transport[
            "source_indra_transport_request_receipt"
        ]
        changed_indra["runtime_transport_realized"] = True
        _retag_indra(changed_indra)
        realized_transport[
            "source_indra_transport_request_receipt_digest"
        ] = changed_indra["indra_transport_request_receipt_digest"]
        _require_error(
            realized_transport,
            "handoff_indra_transport_must_remain_unrealized",
        )

        transport_conflation = deepcopy(receipt)
        transport_conflation[
            "external_authority_not_analytic_transport_receipt"
        ] = False
        _require_error(
            transport_conflation,
            "handoff_external_authority_transport_conflation",
        )

        indra_authority_escalation = deepcopy(receipt)
        changed_indra = indra_authority_escalation[
            "source_indra_transport_request_receipt"
        ]
        changed_indra["request_non_authority"][
            "request_grants_execution"
        ] = True
        _retag_indra(changed_indra)
        indra_authority_escalation[
            "source_indra_transport_request_receipt_digest"
        ] = changed_indra["indra_transport_request_receipt_digest"]
        _require_error(
            indra_authority_escalation,
            "handoff_indra_request_authority_escalation",
        )

        self_issued = deepcopy(receipt)
        packet = self_issued["external_authority_packet"]
        packet["self_issued"] = True
        _retag_authority(packet)
        _require_error(self_issued, "handoff_authority_self_issue_forbidden")

        expired = deepcopy(receipt)
        packet = expired["external_authority_packet"]
        packet["expires_at_ms"] = 90_002
        _retag_authority(packet)
        _require_error(expired, "handoff_authority_expired")

        widened_scope = deepcopy(receipt)
        packet = widened_scope["external_authority_packet"]
        packet["release_scope"]["maximum_invocations"] = 2
        _retag_authority(packet)
        _require_error(widened_scope, "handoff_authority_release_scope_invalid")

        released_memory = deepcopy(receipt)
        packet = released_memory["external_authority_packet"]
        packet["released_blockers"].append("memory_overwrite_blocker")
        _retag_authority(packet)
        _require_error(
            released_memory,
            "handoff_authority_released_blocker_inventory_invalid",
        )

        invariant_loss = deepcopy(receipt)
        certificate = invariant_loss["blocker_discharge_certificate"]
        certificate["retained_invariant_blockers"][
            "memory_overwrite_blocker"
        ] = False
        certificate["all_invariant_blockers_retained"] = False
        _retag_discharge(certificate)
        _require_error(invariant_loss, "handoff_discharge_invariant_loss")

        multi_use = deepcopy(receipt)
        multi_use["release_consumption_count"] = 2
        _require_error(multi_use, "handoff_release_consumption_count_invalid")

        authority_substitution = deepcopy(receipt)
        act_state = authority_substitution["target_act_state"]
        step_authorization = act_state["step_authorization"]
        step_authorization["act_phase_receipt_digest"] = (
            "substituted-external-authority-digest"
        )
        step_authorization["step_authorization_digest"] = ""
        step_authorization["step_authorization_digest"] = authorization_digest(
            step_authorization
        )
        act_state["step_authorization_digest"] = step_authorization[
            "step_authorization_digest"
        ]
        _retag_act_state(act_state)
        _require_error(
            authority_substitution,
            "handoff_step_authorization_external_authority_mismatch",
        )

        human_substitution = deepcopy(receipt)
        act_state = human_substitution["target_act_state"]
        step_authorization = act_state["step_authorization"]
        step_authorization["human_approver_id"] = "substituted-operator"
        step_authorization["step_authorization_digest"] = ""
        step_authorization["step_authorization_digest"] = authorization_digest(
            step_authorization
        )
        act_state["step_authorization_digest"] = step_authorization[
            "step_authorization_digest"
        ]
        _retag_act_state(act_state)
        _require_error(
            human_substitution,
            "handoff_step_authorization_human_approver_mismatch",
        )

        mutable_world = deepcopy(receipt)
        mutable_world["exact_world_updated"] = True
        _require_error(mutable_world, "handoff_exact_world_updated_invalid")

        truth_escalation = deepcopy(receipt)
        truth_escalation["truth_promoted"] = True
        _require_error(truth_escalation, "handoff_truth_promoted_invalid")

        recursive = deepcopy(receipt)
        recursive["same_cycle_recursive_invocation"] = True
        _require_error(
            recursive,
            "handoff_same_cycle_recursive_invocation_invalid",
        )

        return {
            "status": "KUUOS_QI_WORLD_LICENSED_BLOCKER_DISCHARGE_V1_7_OK",
            "source_indra_transport_request_receipt_digest": indra[
                "indra_transport_request_receipt_digest"
            ],
            "source_indra_transport_request_digest": indra[
                "transport_request"
            ]["transport_request_digest"],
            "indra_transport_disposition": receipt[
                "indra_transport_disposition"
            ],
            "source_blocker_receipt_digest": source_digest,
            "source_blocker_certificate_digest": source_certificate_digest,
            "external_authority_packet_digest": authority[
                "external_authority_packet_digest"
            ],
            "blocker_discharge_certificate_digest": discharge[
                "blocker_discharge_certificate_digest"
            ],
            "licensed_act_handoff_receipt_digest": receipt[
                "licensed_act_handoff_receipt_digest"
            ],
            "released_blockers": authority["released_blockers"],
            "retained_invariant_blockers": authority[
                "retained_invariant_blockers"
            ],
            "release_consumption_count": receipt[
                "release_consumption_count"
            ],
            "target_act_state_digest": act["act_state_digest"],
            "effect_recorded": receipt["effect_recorded"],
            "observation_required": receipt["observation_required"],
            "verification_required": receipt["verification_required"],
            "source_cycle_immutable": receipt["source_cycle_immutable"],
            "indra_transport_still_unrealized": receipt[
                "indra_transport_still_unrealized"
            ],
            "exact_world_updated": receipt["exact_world_updated"],
            "truth_promoted": receipt["truth_promoted"],
        }
