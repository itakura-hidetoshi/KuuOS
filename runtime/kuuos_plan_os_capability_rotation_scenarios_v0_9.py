from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_ownership_continuity_kernel_v0_8 import (
    apply_ownership_stage_receipt,
    build_ownership_stage_receipt,
)
from runtime.kuuos_plan_os_ownership_continuity_scenarios_v0_8 import _reentry
from runtime.kuuos_plan_os_ownership_continuity_types_v0_8 import PLAN
from runtime.kuuos_plan_os_capability_binding_kernel_v0_9 import (
    apply_capability_reissue_binding,
    build_capability_reissue_binding,
    validate_capability_reference,
)
from runtime.kuuos_plan_os_capability_rotation_kernel_v0_9 import (
    build_capability_rotation_receipt,
    build_initial_capability_epoch_state,
)
from runtime.kuuos_plan_os_capability_rotation_store_v0_9 import (
    CapabilityRotationStore,
    CapabilityRotationStoreError,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    BOUND,
    CAPABILITY_KINDS,
    HOST_LICENSE,
    binding_digest,
)


def previous_inventory(owner_id: str, epoch_digest: str) -> list[dict[str, str]]:
    return [
        {
            "kind": kind,
            "capability_digest": sha({"old": kind, "owner": owner_id}),
            "owner_id": owner_id,
            "epoch_digest": epoch_digest,
        }
        for kind in CAPABILITY_KINDS
    ]


def _rotation(kind: str) -> tuple[dict, dict, dict]:
    *_, ownership = _reentry(kind)
    old_epoch = sha({"epoch": 3, "owner": ownership["previous_owner_id"]})
    receipt = build_capability_rotation_receipt(
        ownership_state=ownership,
        previous_epoch_index=3,
        previous_epoch_digest=old_epoch,
        previous_capabilities=previous_inventory(
            ownership["previous_owner_id"], old_epoch
        ),
        now_ms=9_000,
    )
    state = build_initial_capability_epoch_state(
        rotation_receipt=receipt, now_ms=9_001
    )
    return ownership, receipt, state


def run_handover_rotation(root: Path) -> dict:
    ownership, receipt, state = _rotation("HANDOVER")
    assert state["previous_owner_id"] == "owner-alpha"
    assert state["current_owner_id"] == "owner-beta"
    assert state["current_epoch_index"] == 4
    assert len(state["revoked_capability_digests"]) == 4

    old_host = receipt["revoked_capabilities"][0]
    assert validate_capability_reference(
        state=state,
        kind=old_host["kind"],
        owner_id=old_host["owner_id"],
        epoch_digest=old_host["epoch_digest"],
        capability_digest=old_host["capability_digest"],
        source_authority_receipt_digest=sha("old-authority"),
        now_ms=9_100,
    ) == ["capability_reference_revoked"]

    try:
        build_capability_reissue_binding(
            state=state,
            kind=HOST_LICENSE,
            owner_id="owner-alpha",
            source_authority_receipt_digest=sha("old-owner-authority"),
            issued_capability_digest=sha("old-owner-new-license"),
            scope_digest=sha("old-owner-scope"),
            issued_at_ms=9_100,
            expires_at_ms=10_100,
        )
    except ValueError as exc:
        assert str(exc) == "capability_binding_current_owner_mismatch"
    else:
        raise AssertionError("previous owner received a new capability binding")

    advanced = build_ownership_stage_receipt(
        state=ownership,
        stage=PLAN,
        owner_id="owner-beta",
        handoff_receipt_digest=ownership["reentry_decision_digest"],
        completion_receipt_digest=ownership["target_active_state_digest"],
        stage_packet_digest=sha("advanced-plan"),
        now_ms=9_010,
    )
    advanced_state = apply_ownership_stage_receipt(ownership, advanced)["state"]
    try:
        build_capability_rotation_receipt(
            ownership_state=advanced_state,
            previous_epoch_index=3,
            previous_epoch_digest=receipt["previous_epoch_digest"],
            previous_capabilities=receipt["revoked_capabilities"],
            now_ms=9_020,
        )
    except ValueError as exc:
        assert str(exc) == "rotation_must_precede_plan_stage"
    else:
        raise AssertionError("late capability rotation accepted")

    store = CapabilityRotationStore(root / "capability-store")
    store.initialize(state)
    current = state
    issued: dict[str, dict] = {}
    for offset, capability_kind in enumerate(CAPABILITY_KINDS, start=1):
        authority_receipt = sha(
            {
                "authority": capability_kind,
                "owner": "owner-beta",
                "epoch": current["current_epoch_digest"],
            }
        )
        capability = sha(
            {
                "issued": capability_kind,
                "owner": "owner-beta",
                "epoch": current["current_epoch_digest"],
            }
        )
        binding = build_capability_reissue_binding(
            state=current,
            kind=capability_kind,
            owner_id="owner-beta",
            source_authority_receipt_digest=authority_receipt,
            issued_capability_digest=capability,
            scope_digest=sha({"scope": capability_kind}),
            issued_at_ms=10_000 + offset,
            expires_at_ms=20_000 + offset,
        )
        applied = store.commit(binding=binding, now_ms=11_000 + offset)
        assert applied["status"] == "APPLIED"
        current = applied["state"]
        issued[capability_kind] = binding
        replay = store.commit(binding=binding, now_ms=12_000 + offset)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == offset

    assert current["status"] == BOUND
    assert current["execution_granted"] is False
    assert current["host_license_granted"] is False
    for capability_kind, binding in issued.items():
        assert validate_capability_reference(
            state=current,
            kind=capability_kind,
            owner_id="owner-beta",
            epoch_digest=current["current_epoch_digest"],
            capability_digest=binding["issued_capability_digest"],
            source_authority_receipt_digest=binding[
                "source_authority_receipt_digest"
            ],
            now_ms=15_000,
        ) == []

    host_binding = issued[HOST_LICENSE]
    assert "capability_reference_epoch_mismatch" in validate_capability_reference(
        state=current,
        kind=HOST_LICENSE,
        owner_id="owner-beta",
        epoch_digest=current["previous_epoch_digest"],
        capability_digest=host_binding["issued_capability_digest"],
        source_authority_receipt_digest=host_binding[
            "source_authority_receipt_digest"
        ],
        now_ms=15_000,
    )
    assert "capability_reference_not_current" in validate_capability_reference(
        state=current,
        kind=HOST_LICENSE,
        owner_id="owner-beta",
        epoch_digest=current["current_epoch_digest"],
        capability_digest=host_binding["issued_capability_digest"],
        source_authority_receipt_digest=host_binding[
            "source_authority_receipt_digest"
        ],
        now_ms=host_binding["expires_at_ms"],
    )

    tampered = deepcopy(host_binding)
    tampered["predecessor_state_digest"] = sha("wrong-predecessor")
    tampered["capability_reissue_binding_digest"] = ""
    tampered["capability_reissue_binding_digest"] = binding_digest(tampered)
    rejected = apply_capability_reissue_binding(state, tampered)
    assert rejected["status"] == "REJECTED"
    assert "binding_predecessor_state_digest_mismatch" in rejected["errors"]

    snapshot = root / "capability-store" / "capability-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except CapabilityRotationStoreError as exc:
        assert str(exc) == "capability_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt capability snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["capability_epoch_state_digest"] == recovered[
        "capability_epoch_state_digest"
    ]
    return recovered


def run_hold_rotation() -> dict:
    _, receipt, state = _rotation("HOLD")
    assert state["previous_owner_id"] == "owner-alpha"
    assert state["current_owner_id"] == "owner-alpha"
    assert state["previous_epoch_digest"] != state["current_epoch_digest"]
    binding = build_capability_reissue_binding(
        state=state,
        kind=HOST_LICENSE,
        owner_id="owner-alpha",
        source_authority_receipt_digest=sha("hold-new-authority"),
        issued_capability_digest=sha("hold-new-license"),
        scope_digest=sha("hold-new-scope"),
        issued_at_ms=10_000,
        expires_at_ms=20_000,
    )
    result = apply_capability_reissue_binding(state, binding)
    assert result["status"] == "APPLIED"
    assert receipt["all_previous_capabilities_revoked"] is True
    return result["state"]
