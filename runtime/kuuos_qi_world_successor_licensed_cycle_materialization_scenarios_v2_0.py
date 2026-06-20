from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_successor_licensed_cycle_materialization_v2_0 import (
    build_digest_linked_multi_cycle_chain,
    multi_cycle_chain_digest,
    second_cycle_receipt_digest,
    successor_closure_digest,
    successor_handoff_digest,
    validate_digest_linked_multi_cycle_chain,
    validate_second_closed_cycle_receipt,
    validate_successor_evidence_closure_receipt,
    validate_successor_licensed_act_handoff_receipt,
)


def _retag_handoff(value: dict) -> dict:
    value["successor_licensed_act_handoff_receipt_digest"] = ""
    value["successor_licensed_act_handoff_receipt_digest"] = successor_handoff_digest(value)
    return value


def _retag_closure(value: dict) -> dict:
    value["successor_evidence_closure_receipt_digest"] = ""
    value["successor_evidence_closure_receipt_digest"] = successor_closure_digest(value)
    return value


def _retag_second(value: dict) -> dict:
    value["licensed_cycle_receipt_digest"] = ""
    value["licensed_cycle_receipt_digest"] = second_cycle_receipt_digest(value)
    return value


def _retag_chain(value: dict) -> dict:
    value["multi_cycle_chain_digest"] = ""
    value["multi_cycle_chain_digest"] = multi_cycle_chain_digest(value)
    return value


def _expect(errors: list[str], expected: str) -> None:
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_successor_licensed_cycle_materialization_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-successor-licensed-cycle-v20-") as temporary:
        chain = build_digest_linked_multi_cycle_chain(Path(temporary))
        assert validate_digest_linked_multi_cycle_chain(chain) == []

        first = chain["first_cycle_receipt"]
        second = chain["second_cycle_receipt"]
        closure = second["source_successor_closure_receipt"]
        handoff = second["source_successor_handoff_receipt"]
        candidate = handoff["external_authority_packet"]
        act = handoff["target_act_state"]

        assert chain["cycle_count"] == 2
        assert chain["cycle_ordinals"] == [1, 2]
        assert second["predecessor_cycle_receipt_digest"] == first["licensed_cycle_receipt_digest"]
        assert candidate["external_authority_packet_digest"] != first["consumed_external_authority_packet_digest"]
        assert candidate["human_approval_receipt_digest"] != first["consumed_human_approval_receipt_digest"]
        assert candidate["host_license_digest"] != first["consumed_host_license_digest"]
        assert handoff["source_receipt_consumed"] is False
        assert handoff["predecessor_authority_inherited"] is False
        assert handoff["predecessor_authority_renewed"] is False
        assert handoff["release_consumption_count"] == 1
        assert act["effect_recorded"] is True
        assert closure["observation_debt_discharged"] is True
        assert closure["verification_debt_discharged"] is True
        assert closure["learning_recorded"] is True
        assert closure["replan_debt_discharged"] is True
        assert closure["all_post_effect_blockers_active"] is True
        assert second["cycle_closed"] is True
        assert second["receipt_consumption_count"] == 0
        assert chain["next_act_started"] is False

        basis_substitution = deepcopy(handoff)
        basis_substitution["basis_bridge"]["materialized_plan_basis_digest"] = "substituted-materialized-basis"
        _expect(
            validate_successor_licensed_act_handoff_receipt(_retag_handoff(basis_substitution)),
            "handoff_basis_bridge_substitution",
        )

        predecessor_receipt_consumption = deepcopy(handoff)
        predecessor_receipt_consumption["source_receipt_consumed"] = True
        _expect(
            validate_successor_licensed_act_handoff_receipt(_retag_handoff(predecessor_receipt_consumption)),
            "handoff_source_receipt_consumed_invalid",
        )

        inherited_authority = deepcopy(handoff)
        inherited_authority["predecessor_authority_inherited"] = True
        _expect(
            validate_successor_licensed_act_handoff_receipt(_retag_handoff(inherited_authority)),
            "handoff_predecessor_authority_inherited_invalid",
        )

        multiuse = deepcopy(handoff)
        multiuse["release_consumption_count"] = 2
        _expect(
            validate_successor_licensed_act_handoff_receipt(_retag_handoff(multiuse)),
            "handoff_release_consumption_count_invalid",
        )

        closure_activation = deepcopy(closure)
        closure_activation["next_act_not_started"] = False
        _expect(
            validate_successor_evidence_closure_receipt(_retag_closure(closure_activation)),
            "closure_next_act_not_started_invalid",
        )

        closure_world_mutation = deepcopy(closure)
        closure_world_mutation["post_effect_world_projection"]["runtime_updates_world"] = True
        closure_world_mutation["post_effect_world_projection"]["world_projection_digest"] = ""
        _expect(
            validate_successor_evidence_closure_receipt(_retag_closure(closure_world_mutation)),
            "closure_world_digest_invalid",
        )

        replay = deepcopy(second)
        replay["receipt_consumption_count"] = 1
        _expect(
            validate_second_closed_cycle_receipt(_retag_second(replay)),
            "cycle_receipt_consumption_forbidden",
        )

        renewable = deepcopy(second)
        renewable["consumed_authority_renewable"] = True
        _expect(
            validate_second_closed_cycle_receipt(_retag_second(renewable)),
            "cycle_receipt_consumed_authority_renewable_invalid",
        )

        broken_link = deepcopy(chain)
        broken_link["second_cycle_receipt"]["predecessor_cycle_receipt_digest"] = "substituted-predecessor-receipt"
        broken_link["second_cycle_receipt"] = _retag_second(broken_link["second_cycle_receipt"])
        broken_link["second_cycle_receipt_digest"] = broken_link["second_cycle_receipt"]["licensed_cycle_receipt_digest"]
        _expect(
            validate_digest_linked_multi_cycle_chain(_retag_chain(broken_link)),
            "chain_predecessor_link_mismatch",
        )

        authority_reuse = deepcopy(chain)
        authority_reuse["authority_packet_digests"][1] = authority_reuse["authority_packet_digests"][0]
        _expect(
            validate_digest_linked_multi_cycle_chain(_retag_chain(authority_reuse)),
            "chain_authority_distinctness_invalid",
        )

        chain_escalation = deepcopy(chain)
        chain_escalation["non_authority"]["chain_is_execution_capability"] = True
        _expect(
            validate_digest_linked_multi_cycle_chain(_retag_chain(chain_escalation)),
            "chain_non_authority_invalid",
        )

        return {
            "status": "KUUOS_QI_WORLD_SUCCESSOR_LICENSED_CYCLE_MATERIALIZATION_V2_0_OK",
            "multi_cycle_chain_digest": chain["multi_cycle_chain_digest"],
            "first_cycle_receipt_digest": chain["first_cycle_receipt_digest"],
            "second_cycle_receipt_digest": chain["second_cycle_receipt_digest"],
            "successor_handoff_receipt_digest": handoff["successor_licensed_act_handoff_receipt_digest"],
            "successor_closure_receipt_digest": closure["successor_evidence_closure_receipt_digest"],
            "basis_bridge_digest": handoff["basis_bridge_digest"],
            "authority_packets_distinct": chain["authority_packets_distinct"],
            "human_approvals_distinct": chain["human_approvals_distinct"],
            "host_licenses_distinct": chain["host_licenses_distinct"],
            "cycle_count": chain["cycle_count"],
            "all_cycles_closed": chain["all_cycles_closed"],
            "all_blockers_active": chain["all_blockers_active"],
            "next_act_started": chain["next_act_started"],
        }
