from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_successor_licensed_cycle_materialization_public_v2_0 import (
    build_digest_linked_multi_cycle_chain,
    validate_digest_linked_multi_cycle_chain,
)

VERSION = "kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1"
NODE_VERSION = "kuuos_qi_world_closed_cycle_node_v2_1"
WITNESS_VERSION = "kuuos_qi_world_closed_cycle_extension_witness_v2_1"
CHAIN_VERSION = "kuuos_qi_world_inductive_licensed_cycle_chain_v2_1"
CYCLE_ID = "qi-world-licensed-multi-cycle-chain-induction-v21"

NODE_NON_AUTHORITY = {
    "node_is_execution_capability": False,
    "node_issues_authority": False,
    "node_replays_receipt": False,
    "node_overwrites_history": False,
    "node_promotes_truth": False,
}
WITNESS_NON_AUTHORITY = {
    "witness_is_execution_capability": False,
    "witness_materializes_act": False,
    "witness_issues_authority": False,
    "witness_consumes_predecessor_receipt": False,
    "witness_inherits_predecessor_authority": False,
}
CHAIN_NON_AUTHORITY = {
    "chain_is_execution_capability": False,
    "chain_issues_authority": False,
    "chain_replays_closed_receipts": False,
    "chain_overwrites_history": False,
    "chain_collapses_worlds": False,
    "chain_promotes_truth": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def cycle_node_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "cycle_node_digest")


def extension_witness_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "extension_witness_digest")


def inductive_chain_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "inductive_chain_digest")


def _prefix_digest(
    root_chain_digest: str,
    nodes: list[Mapping[str, Any]],
    witnesses: list[Mapping[str, Any]],
) -> str:
    return sha(
        {
            "root_two_cycle_chain_digest": root_chain_digest,
            "cycle_node_digests": [node["cycle_node_digest"] for node in nodes],
            "extension_witness_digests": [
                witness["extension_witness_digest"] for witness in witnesses
            ],
            "cycle_count": len(nodes),
        }
    )


def _node_from_materialized_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    node = {
        "version": NODE_VERSION,
        "cycle_ordinal": int(receipt["cycle_ordinal"]),
        "predecessor_cycle_receipt_digest": str(
            receipt.get("predecessor_cycle_receipt_digest", "")
        ),
        "closed_cycle_receipt_digest": str(receipt["licensed_cycle_receipt_digest"]),
        "consumed_external_authority_packet_digest": str(
            receipt["consumed_external_authority_packet_digest"]
        ),
        "consumed_human_approval_receipt_digest": str(
            receipt["consumed_human_approval_receipt_digest"]
        ),
        "consumed_host_license_digest": str(receipt["consumed_host_license_digest"]),
        "source_kind": "materialized_closed_cycle_receipt",
        "source_artifact_digest": str(receipt["licensed_cycle_receipt_digest"]),
        "cycle_materialized": True,
        "native_closure_completed": True,
        "cycle_closed": bool(receipt["cycle_closed"]),
        "closed_cycle_immutable": bool(receipt["closed_cycle_immutable"]),
        "closed_cycle_append_only": bool(receipt["closed_cycle_append_only"]),
        "receipt_replay_forbidden": bool(receipt["receipt_replay_forbidden"]),
        "receipt_consumption_count": int(receipt["receipt_consumption_count"]),
        "consumed_authority_single_use": bool(receipt["consumed_authority_single_use"]),
        "consumed_authority_renewable": bool(receipt["consumed_authority_renewable"]),
        "consumed_authority_inheritable": bool(receipt["consumed_authority_inheritable"]),
        "next_act_started": bool(receipt["next_act_started"]),
        "all_post_effect_blockers_active": bool(
            receipt["all_post_effect_blockers_active"]
        ),
        "exact_world_updated": bool(receipt["exact_world_updated"]),
        "history_overwritten": bool(receipt["history_overwritten"]),
        "truth_promoted": bool(receipt["truth_promoted"]),
        "non_authority": deepcopy(NODE_NON_AUTHORITY),
        "cycle_node_digest": "",
    }
    node["cycle_node_digest"] = cycle_node_digest(node)
    return node


def _node_from_witness(witness: Mapping[str, Any]) -> dict[str, Any]:
    node = {
        "version": NODE_VERSION,
        "cycle_ordinal": int(witness["target_cycle_ordinal"]),
        "predecessor_cycle_receipt_digest": str(
            witness["predecessor_cycle_receipt_digest"]
        ),
        "closed_cycle_receipt_digest": str(witness["closed_cycle_receipt_digest"]),
        "consumed_external_authority_packet_digest": str(
            witness["fresh_external_authority_packet_digest"]
        ),
        "consumed_human_approval_receipt_digest": str(
            witness["new_human_approval_receipt_digest"]
        ),
        "consumed_host_license_digest": str(witness["new_host_license_digest"]),
        "source_kind": "closed_cycle_extension_witness",
        "source_artifact_digest": str(witness["extension_witness_digest"]),
        "cycle_materialized": bool(witness["cycle_materialized"]),
        "native_closure_completed": bool(witness["native_closure_completed"]),
        "cycle_closed": bool(witness["cycle_closed"]),
        "closed_cycle_immutable": bool(witness["closed_cycle_immutable"]),
        "closed_cycle_append_only": bool(witness["closed_cycle_append_only"]),
        "receipt_replay_forbidden": bool(witness["receipt_replay_forbidden"]),
        "receipt_consumption_count": int(witness["receipt_consumption_count"]),
        "consumed_authority_single_use": bool(witness["authority_single_use"]),
        "consumed_authority_renewable": bool(witness["authority_renewable"]),
        "consumed_authority_inheritable": bool(witness["authority_inheritable"]),
        "next_act_started": bool(witness["next_act_started"]),
        "all_post_effect_blockers_active": bool(witness["all_blockers_active"]),
        "exact_world_updated": bool(witness["exact_world_updated"]),
        "history_overwritten": bool(witness["history_overwritten"]),
        "truth_promoted": bool(witness["truth_promoted"]),
        "non_authority": deepcopy(NODE_NON_AUTHORITY),
        "cycle_node_digest": "",
    }
    node["cycle_node_digest"] = cycle_node_digest(node)
    return node


def validate_cycle_node(node: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(node.get("version") == NODE_VERSION, "node_version_invalid")
        req(node.get("cycle_node_digest") == cycle_node_digest(node), "node_digest_invalid")
        ordinal = int(node.get("cycle_ordinal", 0))
        req(ordinal >= 1, "node_ordinal_invalid")
        predecessor = node.get("predecessor_cycle_receipt_digest")
        req(
            predecessor == "" if ordinal == 1 else isinstance(predecessor, str) and bool(predecessor),
            "node_predecessor_invalid",
        )
        for field in (
            "closed_cycle_receipt_digest",
            "consumed_external_authority_packet_digest",
            "consumed_human_approval_receipt_digest",
            "consumed_host_license_digest",
            "source_artifact_digest",
        ):
            req(isinstance(node.get(field), str) and bool(node.get(field)), f"node_{field}_invalid")
        expected = {
            "cycle_materialized": True,
            "native_closure_completed": True,
            "cycle_closed": True,
            "closed_cycle_immutable": True,
            "closed_cycle_append_only": True,
            "receipt_replay_forbidden": True,
            "consumed_authority_single_use": True,
            "consumed_authority_renewable": False,
            "consumed_authority_inheritable": False,
            "next_act_started": False,
            "all_post_effect_blockers_active": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(node.get(field) == value, f"node_{field}_invalid")
        req(node.get("receipt_consumption_count") == 0, "node_receipt_consumption_forbidden")
        req(dict(node.get("non_authority", {})) == NODE_NON_AUTHORITY, "node_non_authority_invalid")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _inventories(nodes: list[Mapping[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    return (
        [str(node["consumed_external_authority_packet_digest"]) for node in nodes],
        [str(node["consumed_human_approval_receipt_digest"]) for node in nodes],
        [str(node["consumed_host_license_digest"]) for node in nodes],
    )


def _assemble_chain(
    root_chain: Mapping[str, Any],
    nodes: list[Mapping[str, Any]],
    witnesses: list[Mapping[str, Any]],
) -> dict[str, Any]:
    authorities, approvals, licenses = _inventories(nodes)
    root_digest = str(root_chain["multi_cycle_chain_digest"])
    chain = {
        "version": CHAIN_VERSION,
        "cycle_id": CYCLE_ID,
        "root_two_cycle_chain": deepcopy(dict(root_chain)),
        "root_two_cycle_chain_digest": root_digest,
        "cycle_nodes": deepcopy(nodes),
        "extension_witnesses": deepcopy(witnesses),
        "cycle_count": len(nodes),
        "cycle_ordinals": [int(node["cycle_ordinal"]) for node in nodes],
        "authority_packet_digests": authorities,
        "human_approval_receipt_digests": approvals,
        "host_license_digests": licenses,
        "prefix_digest": _prefix_digest(root_digest, nodes, witnesses),
        "all_digest_links_exact": True,
        "all_authority_packets_distinct": True,
        "all_human_approvals_distinct": True,
        "all_host_licenses_distinct": True,
        "all_cycles_materialized": True,
        "all_native_closures_completed": True,
        "all_cycles_closed": True,
        "all_receipts_immutable": True,
        "all_receipts_append_only": True,
        "all_receipts_non_consumable": True,
        "all_authorities_single_use": True,
        "no_authority_inheritance": True,
        "no_authority_renewal": True,
        "prefix_immutable": True,
        "append_only_extension": True,
        "next_act_started": False,
        "all_blockers_active": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CHAIN_NON_AUTHORITY),
        "inductive_chain_digest": "",
    }
    chain["inductive_chain_digest"] = inductive_chain_digest(chain)
    return chain


def build_inductive_licensed_cycle_chain(root: Path) -> dict[str, Any]:
    root_chain = build_digest_linked_multi_cycle_chain(root / "root-two-cycle-chain")
    errors = validate_digest_linked_multi_cycle_chain(root_chain)
    if errors:
        raise ValueError("root_two_cycle_chain_invalid:" + ";".join(errors))
    nodes = [
        _node_from_materialized_receipt(root_chain["first_cycle_receipt"]),
        _node_from_materialized_receipt(root_chain["second_cycle_receipt"]),
    ]
    chain = _assemble_chain(root_chain, nodes, [])
    errors = validate_inductive_licensed_cycle_chain(chain)
    if errors:
        raise ValueError("inductive_chain_invalid:" + ";".join(errors))
    return chain


def build_closed_cycle_extension_witness(
    source_chain: Mapping[str, Any],
    *,
    nonce: str,
) -> dict[str, Any]:
    errors = validate_inductive_licensed_cycle_chain(source_chain)
    if errors:
        raise ValueError("source_chain_invalid:" + ";".join(errors))
    last = source_chain["cycle_nodes"][-1]
    target = int(source_chain["cycle_count"]) + 1
    seed = {
        "source_chain_digest": source_chain["inductive_chain_digest"],
        "source_prefix_digest": source_chain["prefix_digest"],
        "predecessor_cycle_receipt_digest": last["closed_cycle_receipt_digest"],
        "target_cycle_ordinal": target,
        "nonce": nonce,
    }
    materialization = sha({"kind": "cycle_materialization", **seed})
    closure = sha({"kind": "native_closure", **seed})
    blocker = sha({"kind": "blocker_restoration", **seed})
    world = sha({"kind": "world_projection", **seed})
    authority = sha({"kind": "fresh_external_authority", **seed})
    approval = sha({"kind": "new_human_approval", **seed})
    license_digest = sha({"kind": "new_host_license", **seed})
    receipt_digest = sha(
        {
            "target_cycle_ordinal": target,
            "predecessor_cycle_receipt_digest": last["closed_cycle_receipt_digest"],
            "source_materialization_receipt_digest": materialization,
            "source_native_closure_receipt_digest": closure,
            "source_blocker_certificate_digest": blocker,
            "source_world_projection_digest": world,
            "fresh_external_authority_packet_digest": authority,
            "new_human_approval_receipt_digest": approval,
            "new_host_license_digest": license_digest,
        }
    )
    witness = {
        "version": WITNESS_VERSION,
        "source_chain_digest": source_chain["inductive_chain_digest"],
        "source_prefix_digest": source_chain["prefix_digest"],
        "source_cycle_count": source_chain["cycle_count"],
        "target_cycle_ordinal": target,
        "predecessor_cycle_receipt_digest": last["closed_cycle_receipt_digest"],
        "source_materialization_receipt_digest": materialization,
        "source_native_closure_receipt_digest": closure,
        "source_blocker_certificate_digest": blocker,
        "source_world_projection_digest": world,
        "fresh_external_authority_packet_digest": authority,
        "new_human_approval_receipt_digest": approval,
        "new_host_license_digest": license_digest,
        "closed_cycle_receipt_digest": receipt_digest,
        "cycle_materialized": True,
        "native_closure_completed": True,
        "cycle_closed": True,
        "closed_cycle_immutable": True,
        "closed_cycle_append_only": True,
        "receipt_replay_forbidden": True,
        "receipt_consumption_count": 0,
        "authority_consumption_count": 1,
        "authority_single_use": True,
        "authority_renewable": False,
        "authority_inheritable": False,
        "next_act_started": False,
        "all_blockers_active": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "witness_only": True,
        "non_authority": deepcopy(WITNESS_NON_AUTHORITY),
        "extension_witness_digest": "",
    }
    witness["extension_witness_digest"] = extension_witness_digest(witness)
    errors = validate_closed_cycle_extension_witness(witness, source_chain=source_chain)
    if errors:
        raise ValueError("extension_witness_invalid:" + ";".join(errors))
    return witness


def _validate_witness_against_prefix(
    witness: Mapping[str, Any],
    prefix_chain: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(witness.get("version") == WITNESS_VERSION, "witness_version_invalid")
        req(
            witness.get("extension_witness_digest") == extension_witness_digest(witness),
            "witness_digest_invalid",
        )
        req(
            witness.get("source_chain_digest") == prefix_chain.get("inductive_chain_digest"),
            "witness_source_chain_digest_mismatch",
        )
        req(
            witness.get("source_prefix_digest") == prefix_chain.get("prefix_digest"),
            "witness_source_prefix_digest_mismatch",
        )
        req(
            witness.get("source_cycle_count") == prefix_chain.get("cycle_count"),
            "witness_source_cycle_count_mismatch",
        )
        target = int(prefix_chain["cycle_count"]) + 1
        req(witness.get("target_cycle_ordinal") == target, "witness_target_ordinal_invalid")
        last = prefix_chain["cycle_nodes"][-1]
        req(
            witness.get("predecessor_cycle_receipt_digest")
            == last.get("closed_cycle_receipt_digest"),
            "witness_predecessor_digest_mismatch",
        )
        for field in (
            "source_materialization_receipt_digest",
            "source_native_closure_receipt_digest",
            "source_blocker_certificate_digest",
            "source_world_projection_digest",
            "fresh_external_authority_packet_digest",
            "new_human_approval_receipt_digest",
            "new_host_license_digest",
            "closed_cycle_receipt_digest",
        ):
            req(isinstance(witness.get(field), str) and bool(witness.get(field)), f"witness_{field}_invalid")
        req(
            witness.get("fresh_external_authority_packet_digest")
            not in prefix_chain.get("authority_packet_digests", []),
            "witness_authority_reuse",
        )
        req(
            witness.get("new_human_approval_receipt_digest")
            not in prefix_chain.get("human_approval_receipt_digests", []),
            "witness_human_approval_reuse",
        )
        req(
            witness.get("new_host_license_digest")
            not in prefix_chain.get("host_license_digests", []),
            "witness_host_license_reuse",
        )
        expected = {
            "cycle_materialized": True,
            "native_closure_completed": True,
            "cycle_closed": True,
            "closed_cycle_immutable": True,
            "closed_cycle_append_only": True,
            "receipt_replay_forbidden": True,
            "authority_consumption_count": 1,
            "authority_single_use": True,
            "authority_renewable": False,
            "authority_inheritable": False,
            "next_act_started": False,
            "all_blockers_active": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
            "witness_only": True,
        }
        for field, value in expected.items():
            req(witness.get(field) == value, f"witness_{field}_invalid")
        req(witness.get("receipt_consumption_count") == 0, "witness_receipt_consumption_forbidden")
        req(dict(witness.get("non_authority", {})) == WITNESS_NON_AUTHORITY, "witness_non_authority_invalid")
        errors += ["witness_node_" + e for e in validate_cycle_node(_node_from_witness(witness))]
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def validate_closed_cycle_extension_witness(
    witness: Mapping[str, Any],
    *,
    source_chain: Mapping[str, Any],
) -> list[str]:
    errors = ["source_chain_" + e for e in validate_inductive_licensed_cycle_chain(source_chain)]
    if errors:
        return errors
    return _validate_witness_against_prefix(witness, source_chain)


def append_closed_cycle(
    source_chain: Mapping[str, Any],
    witness: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_closed_cycle_extension_witness(witness, source_chain=source_chain)
    if errors:
        raise ValueError("extension_witness_invalid:" + ";".join(errors))
    nodes = deepcopy(list(source_chain["cycle_nodes"]))
    witnesses = deepcopy(list(source_chain["extension_witnesses"]))
    nodes.append(_node_from_witness(witness))
    witnesses.append(deepcopy(dict(witness)))
    chain = _assemble_chain(source_chain["root_two_cycle_chain"], nodes, witnesses)
    errors = validate_inductive_licensed_cycle_chain(chain)
    if errors:
        raise ValueError("extended_chain_invalid:" + ";".join(errors))
    return chain


def build_three_cycle_inductive_chain(root: Path) -> dict[str, Any]:
    base = build_inductive_licensed_cycle_chain(root / "base")
    witness = build_closed_cycle_extension_witness(base, nonce="concrete-cycle-3")
    return append_closed_cycle(base, witness)


def validate_inductive_licensed_cycle_chain(chain: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(chain.get("version") == CHAIN_VERSION, "chain_version_invalid")
        root_chain = dict(chain.get("root_two_cycle_chain", {}))
        errors += ["chain_root_" + e for e in validate_digest_linked_multi_cycle_chain(root_chain)]
        req(
            chain.get("root_two_cycle_chain_digest") == root_chain.get("multi_cycle_chain_digest"),
            "chain_root_digest_mismatch",
        )
        expected_nodes = [
            _node_from_materialized_receipt(root_chain["first_cycle_receipt"]),
            _node_from_materialized_receipt(root_chain["second_cycle_receipt"]),
        ]
        accepted_witnesses: list[Mapping[str, Any]] = []
        for index, raw_witness in enumerate(chain.get("extension_witnesses", []), start=3):
            prefix = _assemble_chain(root_chain, expected_nodes, accepted_witnesses)
            witness = dict(raw_witness)
            errors += [
                f"chain_extension_{index}_" + e
                for e in _validate_witness_against_prefix(witness, prefix)
            ]
            expected_nodes.append(_node_from_witness(witness))
            accepted_witnesses.append(witness)
        nodes = list(chain.get("cycle_nodes", []))
        req(nodes == expected_nodes, "chain_cycle_node_inventory_invalid")
        for index, node in enumerate(nodes, start=1):
            errors += [f"chain_node_{index}_" + e for e in validate_cycle_node(node)]
        count = len(nodes)
        req(chain.get("cycle_count") == count, "chain_cycle_count_invalid")
        req(chain.get("cycle_ordinals") == list(range(1, count + 1)), "chain_cycle_sequence_invalid")
        for index in range(1, count):
            req(
                nodes[index].get("predecessor_cycle_receipt_digest")
                == nodes[index - 1].get("closed_cycle_receipt_digest"),
                f"chain_digest_link_{index + 1}_invalid",
            )
        authorities, approvals, licenses = _inventories(nodes)
        req(chain.get("authority_packet_digests") == authorities, "chain_authority_inventory_invalid")
        req(chain.get("human_approval_receipt_digests") == approvals, "chain_approval_inventory_invalid")
        req(chain.get("host_license_digests") == licenses, "chain_host_license_inventory_invalid")
        req(len(set(authorities)) == count, "chain_authority_distinctness_invalid")
        req(len(set(approvals)) == count, "chain_approval_distinctness_invalid")
        req(len(set(licenses)) == count, "chain_host_license_distinctness_invalid")
        expected_prefix = _prefix_digest(
            str(root_chain["multi_cycle_chain_digest"]),
            expected_nodes,
            accepted_witnesses,
        )
        req(chain.get("prefix_digest") == expected_prefix, "chain_prefix_digest_invalid")
        expected = {
            "all_digest_links_exact": True,
            "all_authority_packets_distinct": True,
            "all_human_approvals_distinct": True,
            "all_host_licenses_distinct": True,
            "all_cycles_materialized": True,
            "all_native_closures_completed": True,
            "all_cycles_closed": True,
            "all_receipts_immutable": True,
            "all_receipts_append_only": True,
            "all_receipts_non_consumable": True,
            "all_authorities_single_use": True,
            "no_authority_inheritance": True,
            "no_authority_renewal": True,
            "prefix_immutable": True,
            "append_only_extension": True,
            "next_act_started": False,
            "all_blockers_active": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(chain.get(field) == value, f"chain_{field}_invalid")
        req(dict(chain.get("non_authority", {})) == CHAIN_NON_AUTHORITY, "chain_non_authority_invalid")
        req(
            chain.get("inductive_chain_digest") == inductive_chain_digest(chain),
            "chain_digest_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
