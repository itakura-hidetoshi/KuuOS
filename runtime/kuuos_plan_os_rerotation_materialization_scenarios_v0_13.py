from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_bounded_renewal_scenarios_v0_11 import (
    run_bounded_renewal,
)
from runtime.kuuos_plan_os_capability_binding_kernel_v0_9 import (
    validate_capability_reference,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    BOUND,
    CAPABILITY_KINDS,
    HOST_LICENSE,
)
from runtime.kuuos_plan_os_renewal_escalation_decision_v0_12 import (
    apply_escalation_decision,
    build_escalation_decision,
)
from runtime.kuuos_plan_os_renewal_escalation_state_v0_12 import (
    build_renewal_escalation_state,
)
from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import RE_ROTATE
from runtime.kuuos_plan_os_rerotation_materialization_adapter_v0_13 import (
    materialize_authorized_rerotation_chain,
)
from runtime.kuuos_plan_os_rerotation_materialization_store_v0_13 import (
    RerotationMaterializationStore,
    RerotationMaterializationStoreError,
)
from runtime.kuuos_plan_os_rerotation_materialization_types_v0_13 import (
    receipt_digest,
)


def _source(root: Path) -> tuple[dict, dict, dict]:
    bounded = run_bounded_renewal(root / "bounded-source")
    open_state = build_renewal_escalation_state(
        bounded_renewal_state=bounded,
        capability_kind=HOST_LICENSE,
        now_ms=80_000,
    )
    decision = build_escalation_decision(
        state=open_state,
        route=RE_ROTATE,
        governance_authority_id="governance-board-v13",
        governance_receipt_digest=sha("governance-v13-rerotation"),
        target_owner_id=open_state["current_owner_id"],
        rerotation_scope_digest=sha("v13-rerotation-scope"),
        now_ms=80_100,
    )
    applied = apply_escalation_decision(open_state, decision)
    assert applied["status"] == "APPLIED"
    return bounded, decision, applied["state"]


def _binding_specs(state: dict) -> dict[str, dict]:
    return {
        kind: {
            "source_authority_receipt_digest": sha(
                {
                    "authority": kind,
                    "seed": state["next_epoch_seed_digest"],
                }
            ),
            "issued_capability_digest": sha(
                {
                    "capability": kind,
                    "seed": state["next_epoch_seed_digest"],
                }
            ),
            "scope_digest": sha(
                {"scope": kind, "seed": state["next_epoch_seed_digest"]}
            ),
            "issued_at_ms": 81_000 + index,
            "expires_at_ms": 100_000 + index,
        }
        for index, kind in enumerate(CAPABILITY_KINDS, start=1)
    }


def _lease_specs(state: dict) -> dict[str, dict]:
    return {
        kind: {
            "allowed_stages": ["ACT"],
            "operation_allowlist": [f"rerotation.{kind.lower()}"],
            "scope_digest": sha(
                {
                    "lease-scope": kind,
                    "seed": state["next_epoch_seed_digest"],
                }
            ),
            "max_uses": 3,
            "max_cost_units": 12,
            "not_before_ms": 82_000,
            "expires_at_ms": 90_000,
        }
        for kind in CAPABILITY_KINDS
    }


def _renewal_policies() -> dict[str, dict]:
    return {
        kind: {
            "renewal_authority_id": "renewal-board-v13",
            "max_renewals": 2,
            "max_cumulative_added_uses": 4,
            "max_cumulative_added_cost_units": 8,
            "absolute_expires_at_ms": 120_000,
            "cooldown_ms": 2_000,
        }
        for kind in CAPABILITY_KINDS
    }


def run_materialization(root: Path) -> dict:
    bounded, decision, escalation = _source(root)
    specs = _binding_specs(escalation)
    old_digests = {
        lease["capability_digest"]
        for lease in bounded["current_lease_state"]["leases"].values()
    }

    substituted = deepcopy(decision)
    substituted["next_epoch_seed_digest"] = sha("substituted-seed")
    from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import (
        decision_digest,
    )

    substituted["renewal_escalation_decision_digest"] = ""
    substituted["renewal_escalation_decision_digest"] = decision_digest(
        substituted
    )
    try:
        materialize_authorized_rerotation_chain(
            escalation_state=escalation,
            escalation_decision=substituted,
            source_bounded_renewal_state=bounded,
            binding_specs=specs,
            lease_specs=_lease_specs(escalation),
            renewal_policies=_renewal_policies(),
            now_ms=81_000,
        )
    except ValueError as exc:
        assert str(exc) == (
            "materialization_decision_"
            "renewal_escalation_decision_digest_mismatch"
        )
    else:
        raise AssertionError("substituted rerotation decision accepted")

    reused = deepcopy(specs)
    reused[HOST_LICENSE]["issued_capability_digest"] = next(iter(old_digests))
    try:
        materialize_authorized_rerotation_chain(
            escalation_state=escalation,
            escalation_decision=decision,
            source_bounded_renewal_state=bounded,
            binding_specs=reused,
            lease_specs=_lease_specs(escalation),
            renewal_policies=_renewal_policies(),
            now_ms=81_000,
        )
    except ValueError as exc:
        assert str(exc) == "materialization_old_capability_reuse_forbidden"
    else:
        raise AssertionError("old capability digest reused in new epoch")

    receipt = materialize_authorized_rerotation_chain(
        escalation_state=escalation,
        escalation_decision=decision,
        source_bounded_renewal_state=bounded,
        binding_specs=specs,
        lease_specs=_lease_specs(escalation),
        renewal_policies=_renewal_policies(),
        now_ms=81_000,
    )
    capability_state = receipt["capability_state"]
    lease_state = receipt["lease_state"]
    renewal_state = receipt["renewal_state"]
    assert capability_state["status"] == BOUND
    assert capability_state["current_epoch_index"] == escalation[
        "next_epoch_index"
    ]
    assert capability_state["current_epoch_digest"] == escalation[
        "next_epoch_seed_digest"
    ]
    assert set(receipt["revoked_capability_digests"]) == old_digests
    new_digests = {
        item["issued_capability_digest"]
        for item in capability_state["capability_bindings"].values()
    }
    assert old_digests.isdisjoint(new_digests)
    assert lease_state["processed_consumption_digests"] == []
    assert lease_state["processed_renewal_digests"] == []
    assert all(
        policy["renewal_count"] == 0
        and policy["cumulative_added_uses"] == 0
        and policy["cumulative_added_cost_units"] == 0
        for policy in renewal_state["policies"].values()
    )
    old_host = bounded["current_lease_state"]["leases"][HOST_LICENSE]
    assert validate_capability_reference(
        state=capability_state,
        kind=HOST_LICENSE,
        owner_id=capability_state["current_owner_id"],
        epoch_digest=old_host["epoch_digest"],
        capability_digest=old_host["capability_digest"],
        source_authority_receipt_digest=sha("old-authority"),
        now_ms=85_000,
    ) == ["capability_reference_revoked"]

    store = RerotationMaterializationStore(root / "materialization-store")
    store.initialize(escalation)
    applied = store.commit(receipt=receipt, now_ms=82_000)
    assert applied["status"] == "APPLIED"
    assert store.commit(receipt=receipt, now_ms=82_001)["status"] == "REPLAYED"
    conflicting = deepcopy(receipt)
    conflicting["materialized_at_ms"] += 1
    conflicting["rerotation_materialization_receipt_digest"] = ""
    conflicting["rerotation_materialization_receipt_digest"] = receipt_digest(
        conflicting
    )
    assert store.commit(receipt=conflicting, now_ms=82_002)[
        "status"
    ] == "REJECTED"

    snapshot = root / "materialization-store" / "materialization-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except RerotationMaterializationStoreError as exc:
        assert str(exc) == "materialization_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt materialization snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["rerotation_materialization_receipt_digest"] == recovered[
        "rerotation_materialization_receipt_digest"
    ]
    return recovered
