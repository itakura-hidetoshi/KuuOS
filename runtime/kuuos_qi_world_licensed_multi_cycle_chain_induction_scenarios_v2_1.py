from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1 import (
    append_closed_cycle,
    build_closed_cycle_extension_witness,
    build_inductive_licensed_cycle_chain,
    build_three_cycle_inductive_chain,
    cycle_node_digest,
    extension_witness_digest,
    inductive_chain_digest,
    validate_closed_cycle_extension_witness,
    validate_inductive_licensed_cycle_chain,
)


def _retag_witness(value: dict) -> dict:
    value["extension_witness_digest"] = ""
    value["extension_witness_digest"] = extension_witness_digest(value)
    return value


def _retag_node(value: dict) -> dict:
    value["cycle_node_digest"] = ""
    value["cycle_node_digest"] = cycle_node_digest(value)
    return value


def _retag_chain(value: dict) -> dict:
    value["inductive_chain_digest"] = ""
    value["inductive_chain_digest"] = inductive_chain_digest(value)
    return value


def _expect(errors: list[str], expected: str) -> None:
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_licensed_multi_cycle_chain_induction_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-multi-cycle-induction-v21-") as temporary:
        root = Path(temporary)
        base = build_inductive_licensed_cycle_chain(root / "base")
        assert validate_inductive_licensed_cycle_chain(base) == []
        witness = build_closed_cycle_extension_witness(
            base,
            nonce="scenario-cycle-3",
        )
        assert validate_closed_cycle_extension_witness(witness, source_chain=base) == []
        chain = append_closed_cycle(base, witness)
        assert validate_inductive_licensed_cycle_chain(chain) == []

        rebuilt = build_three_cycle_inductive_chain(root / "rebuilt")
        assert validate_inductive_licensed_cycle_chain(rebuilt) == []

        assert base["cycle_count"] == 2
        assert chain["cycle_count"] == 3
        assert chain["cycle_ordinals"] == [1, 2, 3]
        assert chain["cycle_nodes"][:2] == base["cycle_nodes"]
        assert chain["cycle_nodes"][2]["predecessor_cycle_receipt_digest"] == base[
            "cycle_nodes"
        ][1]["closed_cycle_receipt_digest"]
        assert len(set(chain["authority_packet_digests"])) == 3
        assert len(set(chain["human_approval_receipt_digests"])) == 3
        assert len(set(chain["host_license_digests"])) == 3
        assert chain["all_cycles_closed"] is True
        assert chain["all_receipts_non_consumable"] is True
        assert chain["next_act_started"] is False

        wrong_ordinal = deepcopy(witness)
        wrong_ordinal["target_cycle_ordinal"] = 4
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(wrong_ordinal), source_chain=base
            ),
            "witness_target_ordinal_invalid",
        )

        broken_predecessor = deepcopy(witness)
        broken_predecessor["predecessor_cycle_receipt_digest"] = "broken-predecessor"
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(broken_predecessor), source_chain=base
            ),
            "witness_predecessor_digest_mismatch",
        )

        authority_reuse = deepcopy(witness)
        authority_reuse["fresh_external_authority_packet_digest"] = base[
            "authority_packet_digests"
        ][0]
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(authority_reuse), source_chain=base
            ),
            "witness_authority_reuse",
        )

        approval_reuse = deepcopy(witness)
        approval_reuse["new_human_approval_receipt_digest"] = base[
            "human_approval_receipt_digests"
        ][0]
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(approval_reuse), source_chain=base
            ),
            "witness_human_approval_reuse",
        )

        license_reuse = deepcopy(witness)
        license_reuse["new_host_license_digest"] = base["host_license_digests"][0]
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(license_reuse), source_chain=base
            ),
            "witness_host_license_reuse",
        )

        consumed_receipt = deepcopy(witness)
        consumed_receipt["receipt_consumption_count"] = 1
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(consumed_receipt), source_chain=base
            ),
            "witness_receipt_consumption_forbidden",
        )

        next_act = deepcopy(witness)
        next_act["next_act_started"] = True
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(next_act), source_chain=base
            ),
            "witness_next_act_started_invalid",
        )

        missing_blocker = deepcopy(witness)
        missing_blocker["all_blockers_active"] = False
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(missing_blocker), source_chain=base
            ),
            "witness_all_blockers_active_invalid",
        )

        execution_escalation = deepcopy(witness)
        execution_escalation["non_authority"]["witness_is_execution_capability"] = True
        _expect(
            validate_closed_cycle_extension_witness(
                _retag_witness(execution_escalation), source_chain=base
            ),
            "witness_non_authority_invalid",
        )

        prefix_mutation = deepcopy(chain)
        prefix_mutation["cycle_nodes"][0]["closed_cycle_receipt_digest"] = "mutated-prefix"
        prefix_mutation["cycle_nodes"][0] = _retag_node(prefix_mutation["cycle_nodes"][0])
        _expect(
            validate_inductive_licensed_cycle_chain(_retag_chain(prefix_mutation)),
            "chain_cycle_node_inventory_invalid",
        )

        broken_link = deepcopy(chain)
        broken_link["cycle_nodes"][2]["predecessor_cycle_receipt_digest"] = "broken-link"
        broken_link["cycle_nodes"][2] = _retag_node(broken_link["cycle_nodes"][2])
        _expect(
            validate_inductive_licensed_cycle_chain(_retag_chain(broken_link)),
            "chain_digest_link_3_invalid",
        )

        chain_escalation = deepcopy(chain)
        chain_escalation["non_authority"]["chain_is_execution_capability"] = True
        _expect(
            validate_inductive_licensed_cycle_chain(_retag_chain(chain_escalation)),
            "chain_non_authority_invalid",
        )

        digest_break = deepcopy(chain)
        digest_break["inductive_chain_digest"] = "broken-chain-digest"
        _expect(
            validate_inductive_licensed_cycle_chain(digest_break),
            "chain_digest_invalid",
        )

        return {
            "status": "KUUOS_QI_WORLD_LICENSED_MULTI_CYCLE_CHAIN_INDUCTION_V2_1_OK",
            "base_chain_digest": base["inductive_chain_digest"],
            "extension_witness_digest": witness["extension_witness_digest"],
            "three_cycle_chain_digest": chain["inductive_chain_digest"],
            "prefix_digest": chain["prefix_digest"],
            "cycle_count": chain["cycle_count"],
            "cycle_ordinals": chain["cycle_ordinals"],
            "all_digest_links_exact": chain["all_digest_links_exact"],
            "all_authority_packets_distinct": chain[
                "all_authority_packets_distinct"
            ],
            "all_cycles_closed": chain["all_cycles_closed"],
            "all_receipts_non_consumable": chain[
                "all_receipts_non_consumable"
            ],
            "next_act_started": chain["next_act_started"],
        }
