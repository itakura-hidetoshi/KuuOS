from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    authority_packet_digest,
)
from runtime.kuuos_qi_world_licensed_cycle_receipt_v1_9 import (
    build_licensed_cycle_receipt,
    build_successor_authority_intake,
    build_successor_authority_requirement,
    licensed_cycle_receipt_digest,
    successor_authority_intake_digest,
    successor_authority_requirement_digest,
    validate_licensed_cycle_receipt,
    validate_successor_authority_intake,
    validate_successor_authority_requirement,
)


def _retag_cycle(receipt: dict) -> dict:
    receipt["licensed_cycle_receipt_digest"] = ""
    receipt["licensed_cycle_receipt_digest"] = licensed_cycle_receipt_digest(receipt)
    return receipt


def _retag_requirement(requirement: dict) -> dict:
    requirement["successor_authority_requirement_digest"] = ""
    requirement["successor_authority_requirement_digest"] = (
        successor_authority_requirement_digest(requirement)
    )
    return requirement


def _retag_intake(intake: dict) -> dict:
    intake["successor_authority_intake_digest"] = ""
    intake["successor_authority_intake_digest"] = successor_authority_intake_digest(
        intake
    )
    return intake


def _fresh_candidate(receipt: dict) -> dict:
    old = deepcopy(receipt["source_v17_handoff_receipt"]["external_authority_packet"])
    basis = receipt["successor_basis"]
    old["authority_id"] = "qi-world-v19-successor-authority-candidate"
    old["source_blocker_receipt_digest"] = receipt["successor_basis_digest"]
    old["source_blocker_certificate_digest"] = basis[
        "post_effect_blocker_certificate_digest"
    ]
    old["source_plan_state_digest"] = basis["next_plan_state_digest"]
    old["source_plan_basis_digest"] = basis["next_plan_basis_digest"]
    old["source_committed_plan_digest"] = basis["next_committed_plan_digest"]
    old["host_license_digest"] = "fresh-host-license-digest-v19"
    old["human_approval_receipt_digest"] = "fresh-human-approval-digest-v19"
    old["human_approver_id"] = "external-human-operator-v19"
    old["issued_at_ms"] = 190_000
    old["expires_at_ms"] = 280_000
    old["external_authority_packet_digest"] = ""
    old["external_authority_packet_digest"] = authority_packet_digest(old)
    return old


def _expect_cycle_error(receipt: dict, expected: str) -> None:
    errors = validate_licensed_cycle_receipt(_retag_cycle(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def _expect_requirement_error(
    requirement: dict, receipt: dict, expected: str
) -> None:
    errors = validate_successor_authority_requirement(
        _retag_requirement(requirement),
        closed_cycle_receipt=receipt,
    )
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def _expect_intake_error(
    intake: dict,
    requirement: dict,
    receipt: dict,
    candidate: dict,
    expected: str,
) -> None:
    errors = validate_successor_authority_intake(
        _retag_intake(intake),
        requirement=requirement,
        closed_cycle_receipt=receipt,
        candidate_external_authority_packet=candidate,
    )
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def _expect_value_error(call, expected: str) -> None:
    try:
        call()
    except ValueError as exc:
        if expected not in str(exc):
            raise AssertionError({"expected": expected, "error": str(exc)}) from exc
    else:
        raise AssertionError({"expected": expected, "error": "no_error"})


def run_licensed_cycle_receipt_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-licensed-cycle-receipt-v19-"
    ) as temporary:
        receipt = build_licensed_cycle_receipt(Path(temporary))
        assert validate_licensed_cycle_receipt(receipt) == []

        closure = receipt["source_v18_closure_receipt"]
        handoff = receipt["source_v17_handoff_receipt"]
        requirement = build_successor_authority_requirement(receipt)
        assert (
            validate_successor_authority_requirement(
                requirement,
                closed_cycle_receipt=receipt,
            )
            == []
        )
        candidate = _fresh_candidate(receipt)
        intake = build_successor_authority_intake(
            requirement=requirement,
            closed_cycle_receipt=receipt,
            candidate_external_authority_packet=candidate,
        )
        assert (
            validate_successor_authority_intake(
                intake,
                requirement=requirement,
                closed_cycle_receipt=receipt,
                candidate_external_authority_packet=candidate,
            )
            == []
        )

        assert receipt["cycle_closed"] is True
        assert receipt["receipt_consumption_count"] == 0
        assert receipt["receipt_replay_forbidden"] is True
        assert receipt["consumed_authority_inheritable"] is False
        assert receipt["consumed_authority_renewable"] is False
        assert receipt["next_act_started"] is False
        assert receipt["all_post_effect_blockers_active"] is True
        assert closure["next_act_not_started"] is True
        assert handoff["release_consumption_count"] == 1
        assert requirement["explicit_v1_7_discharge_still_required"] is True
        assert intake["freshness_qualified"] is True
        assert intake["successor_act_started"] is False
        assert intake["predecessor_authority_inherited"] is False

        replay = deepcopy(receipt)
        replay["receipt_consumption_count"] = 1
        _expect_cycle_error(
            replay,
            "cycle_receipt_replay_or_consumption_forbidden",
        )

        authority_inheritance = deepcopy(receipt)
        authority_inheritance["consumed_authority_inheritable"] = True
        _expect_cycle_error(
            authority_inheritance,
            "cycle_receipt_consumed_authority_inheritable_invalid",
        )

        authority_renewal = deepcopy(receipt)
        authority_renewal["consumed_authority_renewable"] = True
        _expect_cycle_error(
            authority_renewal,
            "cycle_receipt_consumed_authority_renewable_invalid",
        )

        next_act_started = deepcopy(receipt)
        next_act_started["next_act_started"] = True
        _expect_cycle_error(
            next_act_started,
            "cycle_receipt_next_act_started_invalid",
        )

        successor_basis_substitution = deepcopy(receipt)
        successor_basis_substitution["successor_basis"][
            "next_plan_state_digest"
        ] = "substituted-next-plan-state"
        successor_basis_substitution["successor_basis_digest"] = ""
        _expect_cycle_error(
            successor_basis_substitution,
            "cycle_receipt_successor_basis_substitution",
        )

        terminal_substitution = deepcopy(receipt)
        terminal_substitution["terminal_state_digest"] = "substituted-terminal"
        _expect_cycle_error(
            terminal_substitution,
            "cycle_receipt_terminal_state_digest_mismatch",
        )

        requirement_act_start = deepcopy(requirement)
        requirement_act_start["successor_act_started"] = True
        _expect_requirement_error(
            requirement_act_start,
            receipt,
            "successor_requirement_act_started",
        )

        requirement_authority = deepcopy(requirement)
        requirement_authority["non_authority"]["requirement_is_authority"] = True
        _expect_requirement_error(
            requirement_authority,
            receipt,
            "successor_requirement_non_authority_invalid",
        )

        reused_authority = deepcopy(
            handoff["external_authority_packet"]
        )
        _expect_value_error(
            lambda: build_successor_authority_intake(
                requirement=requirement,
                closed_cycle_receipt=receipt,
                candidate_external_authority_packet=reused_authority,
            ),
            "successor_authority_digest_reuse_forbidden",
        )

        reused_approval = deepcopy(candidate)
        reused_approval["human_approval_receipt_digest"] = receipt[
            "consumed_human_approval_receipt_digest"
        ]
        reused_approval["external_authority_packet_digest"] = ""
        reused_approval["external_authority_packet_digest"] = authority_packet_digest(
            reused_approval
        )
        _expect_value_error(
            lambda: build_successor_authority_intake(
                requirement=requirement,
                closed_cycle_receipt=receipt,
                candidate_external_authority_packet=reused_approval,
            ),
            "successor_human_approval_reuse_forbidden",
        )

        reused_host = deepcopy(candidate)
        reused_host["host_license_digest"] = receipt[
            "consumed_host_license_digest"
        ]
        reused_host["external_authority_packet_digest"] = ""
        reused_host["external_authority_packet_digest"] = authority_packet_digest(
            reused_host
        )
        _expect_value_error(
            lambda: build_successor_authority_intake(
                requirement=requirement,
                closed_cycle_receipt=receipt,
                candidate_external_authority_packet=reused_host,
            ),
            "successor_host_license_reuse_forbidden",
        )

        wrong_plan = deepcopy(candidate)
        wrong_plan["source_plan_state_digest"] = "wrong-next-plan-state"
        wrong_plan["external_authority_packet_digest"] = ""
        wrong_plan["external_authority_packet_digest"] = authority_packet_digest(
            wrong_plan
        )
        _expect_value_error(
            lambda: build_successor_authority_intake(
                requirement=requirement,
                closed_cycle_receipt=receipt,
                candidate_external_authority_packet=wrong_plan,
            ),
            "successor_candidate_plan_state_mismatch",
        )

        self_issued = deepcopy(candidate)
        self_issued["self_issued"] = True
        self_issued["external_authority_packet_digest"] = ""
        self_issued["external_authority_packet_digest"] = authority_packet_digest(
            self_issued
        )
        _expect_value_error(
            lambda: build_successor_authority_intake(
                requirement=requirement,
                closed_cycle_receipt=receipt,
                candidate_external_authority_packet=self_issued,
            ),
            "successor_candidate_self_issue_forbidden",
        )

        intake_escalation = deepcopy(intake)
        intake_escalation["successor_act_started"] = True
        _expect_intake_error(
            intake_escalation,
            requirement,
            receipt,
            candidate,
            "successor_intake_successor_act_started_invalid",
        )

        return {
            "status": "KUUOS_QI_WORLD_LICENSED_CYCLE_RECEIPT_V1_9_OK",
            "licensed_cycle_receipt_digest": receipt[
                "licensed_cycle_receipt_digest"
            ],
            "source_v17_handoff_receipt_digest": receipt[
                "source_v17_handoff_receipt_digest"
            ],
            "source_v18_closure_receipt_digest": receipt[
                "source_v18_closure_receipt_digest"
            ],
            "authority_consumption_digest": receipt[
                "authority_consumption_digest"
            ],
            "terminal_state_digest": receipt["terminal_state_digest"],
            "successor_basis_digest": receipt["successor_basis_digest"],
            "successor_authority_requirement_digest": requirement[
                "successor_authority_requirement_digest"
            ],
            "successor_authority_intake_digest": intake[
                "successor_authority_intake_digest"
            ],
            "cycle_closed": receipt["cycle_closed"],
            "receipt_replay_forbidden": receipt[
                "receipt_replay_forbidden"
            ],
            "consumed_authority_inheritable": receipt[
                "consumed_authority_inheritable"
            ],
            "freshness_qualified": intake["freshness_qualified"],
            "successor_act_started": intake["successor_act_started"],
            "explicit_v1_7_discharge_still_required": intake[
                "explicit_v1_7_discharge_still_required"
            ],
        }
