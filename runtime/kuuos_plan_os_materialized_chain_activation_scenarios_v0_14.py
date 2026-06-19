from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import state_digest as lease_state_digest
from runtime.kuuos_plan_os_materialized_chain_activation_kernel_v0_14 import (
    build_materialized_chain_activation_receipt,
)
from runtime.kuuos_plan_os_materialized_chain_activation_store_v0_14 import (
    MaterializedChainActivationStore,
    MaterializedChainActivationStoreError,
)
from runtime.kuuos_plan_os_materialized_chain_activation_types_v0_14 import (
    receipt_digest as activation_receipt_digest,
)
from runtime.kuuos_plan_os_rerotation_materialization_scenarios_v0_13 import (
    run_materialization,
)
from runtime.kuuos_plan_os_rerotation_materialization_types_v0_13 import (
    receipt_digest as materialization_receipt_digest,
)


def run_activation(root: Path) -> dict:
    materialization = run_materialization(root / "v13-source")
    owner = materialization["current_owner_id"]
    epoch = materialization["current_epoch_digest"]

    try:
        build_materialized_chain_activation_receipt(
            materialization_receipt=materialization,
            requested_owner_id=owner,
            requested_epoch_digest=epoch,
            current_cycle_index=12,
            mission_cycle_state_digest=sha("mission-cycle-12"),
            activation_authority_id="activation-board",
            activation_authority_receipt_digest=sha("activation-authority-early"),
            now_ms=81_000,
        )
    except ValueError as exc:
        assert str(exc).startswith("activation_lease_not_started:")
    else:
        raise AssertionError("materialized chain activated before lease start")

    try:
        build_materialized_chain_activation_receipt(
            materialization_receipt=materialization,
            requested_owner_id=owner,
            requested_epoch_digest=epoch,
            current_cycle_index=12,
            mission_cycle_state_digest=sha("mission-cycle-12"),
            activation_authority_id="activation-board",
            activation_authority_receipt_digest=sha("activation-authority-expired"),
            now_ms=90_000,
        )
    except ValueError as exc:
        assert str(exc).startswith("activation_lease_expired:")
    else:
        raise AssertionError("expired materialized chain activated")

    for field, value, expected in (
        ("requested_owner_id", "owner-substituted", "activation_requested_owner_mismatch"),
        ("requested_epoch_digest", sha("epoch-substituted"), "activation_requested_epoch_mismatch"),
    ):
        kwargs = {
            "materialization_receipt": materialization,
            "requested_owner_id": owner,
            "requested_epoch_digest": epoch,
            "current_cycle_index": 12,
            "mission_cycle_state_digest": sha("mission-cycle-12"),
            "activation_authority_id": "activation-board",
            "activation_authority_receipt_digest": sha("activation-authority"),
            "now_ms": 85_000,
        }
        kwargs[field] = value
        try:
            build_materialized_chain_activation_receipt(**kwargs)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError(expected + " was accepted")

    cross_link_tampered = deepcopy(materialization)
    first_kind = next(iter(cross_link_tampered["lease_state"]["leases"]))
    cross_link_tampered["lease_state"]["leases"][first_kind][
        "capability_digest"
    ] = sha("substituted-capability")
    cross_link_tampered["lease_state"]["capability_lease_state_digest"] = ""
    cross_link_tampered["lease_state"]["capability_lease_state_digest"] = (
        lease_state_digest(cross_link_tampered["lease_state"])
    )
    cross_link_tampered["rerotation_materialization_receipt_digest"] = ""
    cross_link_tampered["rerotation_materialization_receipt_digest"] = (
        materialization_receipt_digest(cross_link_tampered)
    )
    try:
        build_materialized_chain_activation_receipt(
            materialization_receipt=cross_link_tampered,
            requested_owner_id=owner,
            requested_epoch_digest=epoch,
            current_cycle_index=12,
            mission_cycle_state_digest=sha("mission-cycle-12"),
            activation_authority_id="activation-board",
            activation_authority_receipt_digest=sha("activation-authority-tamper"),
            now_ms=85_000,
        )
    except ValueError as exc:
        assert str(exc) == "activation_renewal_lease_state_mismatch"
    else:
        raise AssertionError("cross-linked lease substitution accepted")

    receipt = build_materialized_chain_activation_receipt(
        materialization_receipt=materialization,
        requested_owner_id=owner,
        requested_epoch_digest=epoch,
        current_cycle_index=12,
        mission_cycle_state_digest=sha("mission-cycle-12"),
        activation_authority_id="activation-board",
        activation_authority_receipt_digest=sha("activation-authority-valid"),
        now_ms=85_000,
    )
    assert receipt["active_from_cycle"] == 13
    assert receipt["mission_cycle_phase"] == "plan"
    assert receipt["next_plan_cycle_handoff_ready"] is True
    assert receipt["chain_activation_authorized"] is True
    assert len(receipt["scope_inventory"]) == 4
    assert receipt["execution_granted"] is False

    store = MaterializedChainActivationStore(root / "activation-store")
    store.initialize(materialization)
    applied = store.commit(receipt=receipt, now_ms=85_001)
    assert applied["status"] == "APPLIED"
    assert store.commit(receipt=receipt, now_ms=85_002)["status"] == "REPLAYED"

    conflicting = deepcopy(receipt)
    conflicting["activation_authority_receipt_digest"] = sha(
        "conflicting-activation-authority"
    )
    conflicting["materialized_chain_activation_receipt_digest"] = ""
    conflicting["materialized_chain_activation_receipt_digest"] = (
        activation_receipt_digest(conflicting)
    )
    rejected = store.commit(receipt=conflicting, now_ms=85_003)
    assert rejected["status"] == "REJECTED"
    assert "activation_already_committed" in rejected["errors"]

    snapshot = root / "activation-store" / "activation-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except MaterializedChainActivationStoreError as exc:
        assert str(exc) == "activation_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt activation snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["materialized_chain_activation_receipt_digest"] == recovered[
        "materialized_chain_activation_receipt_digest"
    ]
    return recovered
