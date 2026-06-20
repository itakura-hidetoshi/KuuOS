from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_successor_cycle_materialization_public_v2_0 import (
    build_successor_cycle_materialization_receipt,
    execution_authority_digest,
    materialization_receipt_digest,
    second_cycle_receipt_digest,
    successor_closure_digest,
    successor_handoff_digest,
    validate_second_cycle_receipt,
    validate_successor_cycle_materialization_receipt,
    validate_successor_effect_evidence_closure,
    validate_successor_execution_authority,
    validate_successor_licensed_act_handoff,
)


def _retag_materialization(receipt: dict) -> dict:
    receipt["successor_cycle_materialization_receipt_digest"] = ""
    receipt["successor_cycle_materialization_receipt_digest"] = (
        materialization_receipt_digest(receipt)
    )
    return receipt


def _retag_execution_authority(packet: dict) -> dict:
    packet["successor_execution_authority_digest"] = ""
    packet["successor_execution_authority_digest"] = execution_authority_digest(
        packet
    )
    return packet


def _retag_handoff(receipt: dict) -> dict:
    receipt["licensed_act_handoff_receipt_digest"] = ""
    receipt["licensed_act_handoff_receipt_digest"] = successor_handoff_digest(
        receipt
    )
    return receipt


def _retag_closure(receipt: dict) -> dict:
    receipt["successor_effect_evidence_closure_receipt_digest"] = ""
    receipt["successor_effect_evidence_closure_receipt_digest"] = (
        successor_closure_digest(receipt)
    )
    return receipt


def _retag_second_cycle(receipt: dict) -> dict:
    receipt["second_cycle_receipt_digest"] = ""
    receipt["second_cycle_receipt_digest"] = second_cycle_receipt_digest(receipt)
    return receipt


def _expect(errors: list[str], expected: str) -> None:
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_successor_cycle_materialization_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-successor-cycle-materialization-v20-"
    ) as temporary:
        receipt = build_successor_cycle_materialization_receipt(Path(temporary))
        assert validate_successor_cycle_materialization_receipt(receipt) == []

        first = receipt["first_cycle_receipt"]
        requirement = receipt["successor_authority_requirement"]
        candidate = receipt["freshness_candidate"]
        intake = receipt["successor_authority_intake"]
        execution_authority = receipt["successor_execution_authority"]
        handoff = receipt["second_cycle_handoff"]
        closure = receipt["second_cycle_closure"]
        second = receipt["second_cycle_receipt"]
        plan = first["source_v18_closure_receipt"]["next_cycle_artifacts"][
            "PlanOS"
        ]
        host_license = handoff["target_act_state"]["host_license"]

        assert receipt["closed_cycle_count"] == 2
        assert receipt["cycle_ordinals"] == [1, 2]
        assert first["cycle_ordinal"] == 1
        assert second["cycle_ordinal"] == 2
        assert second["predecessor_cycle_receipt_digest"] == first[
            "licensed_cycle_receipt_digest"
        ]
        assert handoff["release_consumption_count"] == 1
        assert handoff["effect_recorded"] is True
        assert closure["observation_debt_discharged"] is True
        assert closure["verification_debt_discharged"] is True
        assert closure["next_act_not_started"] is True
        assert second["cycle_closed"] is True
        assert second["next_act_started"] is False
        assert receipt["all_second_post_effect_blockers_active"] is True
        assert execution_authority["source_plan_basis_digest"] == plan[
            "plan_basis_digest"
        ]
        assert execution_authority["source_next_plan_basis_digest"] == plan[
            "next_plan_basis_digest"
        ]
        assert execution_authority["source_plan_basis_digest"] != execution_authority[
            "source_next_plan_basis_digest"
        ]

        bad_count = deepcopy(receipt)
        bad_count["closed_cycle_count"] = 3
        errors = validate_successor_cycle_materialization_receipt(
            _retag_materialization(bad_count)
        )
        _expect(errors, "materialization_closed_cycle_count_invalid")

        bad_ordinals = deepcopy(receipt)
        bad_ordinals["cycle_ordinals"] = [1, 3]
        errors = validate_successor_cycle_materialization_receipt(
            _retag_materialization(bad_ordinals)
        )
        _expect(errors, "materialization_cycle_ordinals_invalid")

        authority_reuse = deepcopy(execution_authority)
        authority_reuse["successor_execution_authority_digest"] = first[
            "consumed_external_authority_packet_digest"
        ]
        errors = validate_successor_execution_authority(
            authority_reuse,
            predecessor=first,
            requirement=requirement,
            intake=intake,
            freshness_candidate=candidate,
            plan_state=plan,
            host_license=host_license,
        )
        _expect(errors, "execution_authority_digest_invalid")
        _expect(errors, "execution_authority_predecessor_authority_reuse")

        approval_reuse = deepcopy(execution_authority)
        approval_reuse["human_approval_receipt_digest"] = first[
            "consumed_human_approval_receipt_digest"
        ]
        _retag_execution_authority(approval_reuse)
        errors = validate_successor_execution_authority(
            approval_reuse,
            predecessor=first,
            requirement=requirement,
            intake=intake,
            freshness_candidate=candidate,
            plan_state=plan,
            host_license=host_license,
        )
        _expect(errors, "execution_authority_human_approval_receipt_digest_invalid")
        _expect(errors, "execution_authority_predecessor_approval_reuse")

        host_reuse = deepcopy(execution_authority)
        host_reuse["host_license_digest"] = first[
            "consumed_host_license_digest"
        ]
        _retag_execution_authority(host_reuse)
        errors = validate_successor_execution_authority(
            host_reuse,
            predecessor=first,
            requirement=requirement,
            intake=intake,
            freshness_candidate=candidate,
            plan_state=plan,
            host_license=host_license,
        )
        _expect(errors, "execution_authority_host_license_digest_invalid")
        _expect(errors, "execution_authority_predecessor_host_reuse")

        basis_collapse = deepcopy(execution_authority)
        basis_collapse["source_plan_basis_digest"] = basis_collapse[
            "source_next_plan_basis_digest"
        ]
        _retag_execution_authority(basis_collapse)
        errors = validate_successor_execution_authority(
            basis_collapse,
            predecessor=first,
            requirement=requirement,
            intake=intake,
            freshness_candidate=candidate,
            plan_state=plan,
            host_license=host_license,
        )
        _expect(errors, "execution_authority_source_plan_basis_digest_invalid")
        _expect(errors, "execution_authority_plan_basis_layers_collapsed")

        multiuse = deepcopy(handoff)
        multiuse["release_consumption_count"] = 2
        errors = validate_successor_licensed_act_handoff(_retag_handoff(multiuse))
        _expect(errors, "second_handoff_replay_or_multiuse")

        recursive = deepcopy(handoff)
        recursive["same_cycle_recursive_invocation"] = True
        errors = validate_successor_licensed_act_handoff(_retag_handoff(recursive))
        _expect(errors, "second_handoff_same_cycle_recursive_invocation_invalid")

        world_substitution = deepcopy(closure)
        world_substitution["post_effect_world_projection"][
            "predecessor_world_projection_digest"
        ] = "substituted-predecessor-world"
        world = world_substitution["post_effect_world_projection"]
        world["world_projection_digest"] = ""
        from runtime.kuuos_belief_os_types_v0_1 import sha

        world["world_projection_digest"] = sha(
            {
                key: value
                for key, value in world.items()
                if key != "world_projection_digest"
            }
        )
        world_substitution["post_effect_world_projection_digest"] = world[
            "world_projection_digest"
        ]
        errors = validate_successor_effect_evidence_closure(
            _retag_closure(world_substitution)
        )
        _expect(errors, "second_closure_world_predecessor_mismatch")

        second_ordinal = deepcopy(second)
        second_ordinal["cycle_ordinal"] = 3
        errors = validate_second_cycle_receipt(
            _retag_second_cycle(second_ordinal),
            predecessor=first,
        )
        _expect(errors, "second_cycle_ordinal_invalid")

        second_replay = deepcopy(second)
        second_replay["receipt_consumption_count"] = 1
        errors = validate_second_cycle_receipt(
            _retag_second_cycle(second_replay),
            predecessor=first,
        )
        _expect(errors, "second_cycle_receipt_replay_or_consumption_forbidden")

        third_act = deepcopy(second)
        third_act["next_act_started"] = True
        errors = validate_second_cycle_receipt(
            _retag_second_cycle(third_act),
            predecessor=first,
        )
        _expect(errors, "second_cycle_next_act_started_invalid")

        chain_tamper = deepcopy(receipt)
        chain_tamper["two_cycle_chain_digest"] = "substituted-chain"
        errors = validate_successor_cycle_materialization_receipt(
            _retag_materialization(chain_tamper)
        )
        _expect(errors, "materialization_chain_digest_invalid")

        escalation = deepcopy(receipt)
        escalation["non_authority"][
            "materialization_grants_third_cycle_execution"
        ] = True
        errors = validate_successor_cycle_materialization_receipt(
            _retag_materialization(escalation)
        )
        _expect(errors, "materialization_non_authority_invalid")

        return {
            "status": "KUUOS_QI_WORLD_SUCCESSOR_CYCLE_MATERIALIZATION_V2_0_OK",
            "first_cycle_receipt_digest": receipt["first_cycle_receipt_digest"],
            "freshness_candidate_digest": receipt["freshness_candidate_digest"],
            "successor_execution_authority_digest": receipt[
                "successor_execution_authority_digest"
            ],
            "second_cycle_handoff_digest": receipt[
                "second_cycle_handoff_digest"
            ],
            "second_cycle_closure_digest": receipt[
                "second_cycle_closure_digest"
            ],
            "second_cycle_receipt_digest": receipt[
                "second_cycle_receipt_digest"
            ],
            "two_cycle_chain_digest": receipt["two_cycle_chain_digest"],
            "closed_cycle_count": receipt["closed_cycle_count"],
            "cycle_ordinals": receipt["cycle_ordinals"],
            "authority_digests_distinct": receipt[
                "authority_digests_distinct"
            ],
            "second_cycle_closed": receipt["second_cycle_closed"],
            "second_next_act_started": receipt["second_next_act_started"],
            "all_second_post_effect_blockers_active": receipt[
                "all_second_post_effect_blockers_active"
            ],
        }
