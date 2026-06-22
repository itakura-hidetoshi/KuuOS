from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_adaptive_agent_reference_types_v1_0 import state_digest
from runtime.kuuos_adaptive_agent_runtime_megamodel_v1_0 import (
    MODEL_KINDS,
    build_runtime_megamodel,
)
from runtime.kuuos_adaptive_agent_transition_kernel_v1_0 import (
    apply_adaptive_event,
    build_adaptive_event,
    build_initial_adaptive_state,
)
from runtime.kuuos_operational_agent_adapter_contract_v1_1 import (
    DeterministicEvidenceVerifier,
    DeterministicFutureOnlyLearner,
    DeterministicIndependentObserver,
    DeterministicStagedAdapter,
)
from runtime.kuuos_operational_agent_capability_registry_v1_1 import CapabilityRegistry
from runtime.kuuos_operational_agent_controller_v1_1 import run_operational_cycle
from runtime.kuuos_operational_agent_lease_ledger_v1_1 import (
    ExecutionLeaseUsageLedger,
)
from runtime.kuuos_operational_agent_receipt_store_v1_1 import AppendOnlyReceiptStore
from runtime.kuuos_operational_agent_types_v1_1 import (
    build_action_intent,
    build_capability,
    build_execution_lease,
    sha,
)


def _emit(state: dict, kind: str, **payload: object) -> dict:
    return apply_adaptive_event(
        state,
        build_adaptive_event(
            kind=kind,
            event_index=state["sequence"] + 1,
            payload=payload,
        ),
    )


def build_fixture(
    *,
    label: str = "nominal",
    max_uses: int = 1,
    effect_class: str = "STAGED_WRITE",
) -> dict:
    megamodel = build_runtime_megamodel(
        model_digests={kind: sha({"model": kind}) for kind in MODEL_KINDS}
    )
    state = build_initial_adaptive_state(
        owner_id="owner-alpha",
        lineage_id=f"lineage-{label}-0",
        runtime_megamodel_digest=megamodel["runtime_megamodel_digest"],
    )
    state = _emit(state, "DECISION_COMMITTED")
    state = _emit(state, "PLAN_BOUND", plan_digest=sha(f"plan-{label}"))
    state = _emit(
        state,
        "AUTHORITY_BOUND",
        authority_receipt_digest=sha(f"authority-{label}"),
    )
    state = _emit(state, "LEASE_ACTIVATED")
    session_digest = sha(f"session-{label}-0")
    state = _emit(state, "SESSION_BOOTSTRAPPED", session_digest=session_digest)

    capability = build_capability(
        capability_id=f"capability-{label}",
        owner_id="owner-alpha",
        adapter_kind="DETERMINISTIC_STAGED",
        operation_allowlist=["STAGE_PATCH"],
        resource_scope=["repo:itakura-hidetoshi/KuuOS"],
        capability_epoch=state["epoch_index"],
        effect_ceiling="STAGED_WRITE",
    )
    lease = build_execution_lease(
        lease_id=f"lease-{label}",
        capability_id=capability["capability_id"],
        owner_id="owner-alpha",
        lineage_id=state["lineage_id"],
        session_digest=session_digest,
        capability_epoch=state["epoch_index"],
        allowed_operations=["STAGE_PATCH"],
        resource_scope=["repo:itakura-hidetoshi/KuuOS"],
        max_uses=max_uses,
        issued_at_sequence=state["sequence"],
        expires_at_sequence=state["sequence"] + 20,
        host_license_digest=sha(f"host-license-{label}"),
        effect_ceiling="STAGED_WRITE",
    )
    intent = build_action_intent(
        intent_id=f"intent-{label}-0",
        owner_id="owner-alpha",
        lineage_id=state["lineage_id"],
        session_digest=session_digest,
        capability_id=capability["capability_id"],
        capability_epoch=state["epoch_index"],
        adapter_kind="DETERMINISTIC_STAGED",
        operation="STAGE_PATCH",
        resource="repo:itakura-hidetoshi/KuuOS",
        effect_class=effect_class,
        payload={"patch": label},
        idempotency_key=f"idempotency-{label}-0",
    )
    registry = CapabilityRegistry()
    registry.register(capability)
    return {
        "state": state,
        "capability": capability,
        "lease": lease,
        "intent": intent,
        "registry": registry,
        "adapter": DeterministicStagedAdapter(),
        "observer": DeterministicIndependentObserver(),
        "verifier": DeterministicEvidenceVerifier(),
        "learner": DeterministicFutureOnlyLearner(),
        "lease_ledger": ExecutionLeaseUsageLedger(),
        "receipt_store": AppendOnlyReceiptStore(same_root_id="kuuos-main-root"),
    }


def _run(fixture: dict) -> dict:
    return run_operational_cycle(
        state=fixture["state"],
        registry=fixture["registry"],
        lease=fixture["lease"],
        intent=fixture["intent"],
        adapter=fixture["adapter"],
        observer=fixture["observer"],
        verifier=fixture["verifier"],
        learner=fixture["learner"],
        lease_ledger=fixture["lease_ledger"],
        receipt_store=fixture["receipt_store"],
    )


def run_nominal_scenario() -> dict:
    result = _run(build_fixture())
    assert result["status"] == "COMPLETED"
    assert result["state"]["task_stage"] == "PLAN"
    assert result["state"]["execution_allowed"] is False
    assert result["external_commit_performed"] is False
    assert result["observation"]["independent_from_adapter"] is True
    assert result["learning"]["future_only"] is True
    return result


def run_external_commit_hold() -> dict:
    fixture = build_fixture(label="external", effect_class="EXTERNAL_COMMIT")
    result = _run(fixture)
    assert result["status"] == "HOLD"
    assert result["recovery_decision"] == "REQUEST_HUMAN"
    assert result["adapter_invoked"] is False
    assert result["external_commit_performed"] is False
    return result


def run_stale_epoch_hold() -> dict:
    fixture = build_fixture(label="stale")
    fixture["state"] = deepcopy(fixture["state"])
    fixture["state"]["epoch_index"] += 1
    fixture["state"]["adaptive_control_state_digest"] = state_digest(fixture["state"])
    result = _run(fixture)
    assert result["status"] == "HOLD"
    assert result["recovery_decision"] == "REROTATE"
    assert result["adapter_invoked"] is False
    return result


def run_replay_hold() -> dict:
    fixture = build_fixture(label="replay", max_uses=2)
    first = _run(fixture)
    assert first["status"] == "COMPLETED"
    fixture["state"] = first["state"]
    second = _run(fixture)
    assert second["status"] == "HOLD"
    assert second["recovery_decision"] == "REVALIDATE"
    assert second["adapter_invoked"] is False
    return second


def run_reference_scenarios() -> dict:
    nominal = run_nominal_scenario()
    external = run_external_commit_hold()
    stale = run_stale_epoch_hold()
    replay = run_replay_hold()
    return {
        "status": "KUUOS_OPERATIONAL_AGENT_CONTROLLER_V1_1_OK",
        "nominal_status": nominal["status"],
        "nominal_final_stage": nominal["state"]["task_stage"],
        "independent_observation": nominal["observation"]["independent_from_adapter"],
        "future_only_learning": nominal["learning"]["future_only"],
        "external_commit_status": external["status"],
        "external_commit_recovery": external["recovery_decision"],
        "external_commit_performed": external["external_commit_performed"],
        "stale_epoch_recovery": stale["recovery_decision"],
        "replay_recovery": replay["recovery_decision"],
    }
