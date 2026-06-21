from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from runtime.kuuos_act_os_fixture_v0_1 import (
    host_inputs,
    prepared_project_state,
    source_plan,
)
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_observe_os_fixture_v0_1 import prepared_assessed_state
from runtime.kuuos_transactional_effect_commit_v0_24 import (
    build_transaction_final_receipt_v0_24,
)
from runtime.kuuos_transactional_effect_reconciliation_kernel_v0_24 import (
    apply_transaction_event,
    build_compensation_request,
    build_connector_contract,
    build_initial_transaction_state,
    build_transaction_decision,
    build_transaction_event,
    build_transaction_intent,
    build_world_effect_reconciliation_receipt,
    validate_transaction_state,
)
from runtime.kuuos_transactional_effect_store_v0_24 import (
    TransactionStore,
    TransactionStoreError,
)
from runtime.kuuos_transactional_effect_types_v0_24 import copy_non_authority
from runtime.kuuos_verify_os_fixture_v0_1 import prepared_corroborated_state
from runtime.v01_act_os_authority_bound_invocation import _finish as finish_act
from runtime.v01_observe_os_effect_grounded_observation import (
    _finish as finish_observe,
)
from runtime.v01_verify_os_evidence_bound_verification import (
    _finish as finish_verify,
)
from runtime.v017_host_adapter_fixtures import registry


def _connector_contract(*, compensation_mode: str) -> dict[str, Any]:
    compensation_operations = (
        ["fixture.success"] if compensation_mode == "explicit_operation" else []
    )
    return build_connector_contract(
        connector_id="fixture-transactional-connector",
        adapter_kind="fixture",
        trusted_registry_entry_digest=sha("fixture-transactional-registry-entry"),
        operation_allowlist=["fixture.success"],
        compensation_mode=compensation_mode,
        compensation_operation_allowlist=compensation_operations,
        observation_channel_ids=["system-output", "independent-check"],
    )


def _prepared_transaction(
    root: Path,
    *,
    transaction_id: str,
    compensation_mode: str,
    expires_at_ms: int = 600_000,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    TransactionStore,
]:
    plan_state, activation = source_plan(root / "plan")
    policy, bundle, host_license, projection = host_inputs(
        job_id=transaction_id + "-job", expires_at_ms=expires_at_ms
    )
    act_store, prepared_act = prepared_project_state(
        root=root / "act",
        act_id=transaction_id + "-act",
        plan_state=plan_state,
        plan_activation=activation,
        job_id=transaction_id + "-job",
        host_license=host_license,
        projection=projection,
    )
    connector = _connector_contract(compensation_mode=compensation_mode)
    kwargs: dict[str, Any] = {}
    if compensation_mode == "explicit_operation":
        kwargs = {
            "compensation_operation_id": "fixture.success",
            "compensation_input_digest": sha(
                {"transaction_id": transaction_id, "compensation": True}
            ),
        }
    else:
        kwargs = {
            "noncompensability_reason_digest": sha(
                {"transaction_id": transaction_id, "mode": compensation_mode}
            )
        }
    intent = build_transaction_intent(
        transaction_id=transaction_id,
        prepared_act_state=prepared_act,
        connector_contract=connector,
        intended_effect_digest=sha(
            {"transaction_id": transaction_id, "intended_effect": True}
        ),
        idempotency_key=prepared_act["step_authorization"]["invocation_id"],
        timeout_ms=30_000,
        max_retries=2,
        prepared_at_ms=90_003,
        **kwargs,
    )
    state = build_initial_transaction_state(
        intent=intent,
        connector_contract=connector,
        prepared_act_state=prepared_act,
        now_ms=90_003,
    )
    transaction_store = TransactionStore(root / "transaction")
    state = transaction_store.initialize(state)
    return (
        policy,
        bundle,
        host_license,
        prepared_act,
        act_store,
        connector,
        intent,
        transaction_store,
    )


def _event(
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    return build_transaction_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha(
            {
                "transaction_id": state["transaction_id"],
                "phase": phase,
                "payload": dict(payload),
                "now_ms": now_ms,
            }
        ),
        payload=payload,
        now_ms=now_ms,
    )


def _apply(
    store: TransactionStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    event = _event(state, phase, payload, now_ms)
    result = store.apply(event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], event


def _effect_bound(
    *,
    store: TransactionStore,
    transaction_state: Mapping[str, Any],
    act_store: Any,
    prepared_act: dict[str, Any],
    bundle: dict[str, Any],
    policy: dict[str, Any],
    invoke_ms: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    final_act, _ = finish_act(
        store=act_store,
        state=prepared_act,
        bundle=bundle,
        policy=policy,
        invoke_ms=invoke_ms,
    )
    state, event = _apply(
        store,
        transaction_state,
        "effect_bound",
        {"final_act_state": final_act},
        invoke_ms + 10,
    )
    return state, event


def _observed(
    *,
    root: Path,
    store: TransactionStore,
    transaction_state: Mapping[str, Any],
    verdict: str,
    conflict: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    quality: dict[str, Any] | None = None
    if conflict:
        quality = {
            "coverage": 0.9,
            "freshness": 0.9,
            "provenance": 0.9,
            "calibration": 0.9,
            "completeness": 0.9,
            "conflict": 0.9,
            "assessment_method_digest": sha("v024-conflicted-quality"),
        }
    observe_store, observe_state = prepared_assessed_state(
        root=root / "observe",
        observe_id=transaction_state["transaction_id"] + "-observe",
        act_state=transaction_state["final_act_state"],
        quality=quality,
        conflict=conflict,
    )
    observe_state, _ = finish_observe(
        store=observe_store,
        state=observe_state,
        verdict=verdict,
        tick=50,
    )
    return _apply(
        store,
        transaction_state,
        "observed",
        {"observe_state": observe_state},
        100_100,
    )[0], observe_state


def _reconciled(
    *,
    store: TransactionStore,
    transaction_state: Mapping[str, Any],
    verdict: str,
) -> dict[str, Any]:
    intended = transaction_state["transaction_intent"]["intended_effect_digest"]
    observed_effect = intended if verdict == "EFFECT_CONFIRMED" else sha(
        {
            "transaction_id": transaction_state["transaction_id"],
            "observed_effect": verdict,
        }
    )
    receipt = build_world_effect_reconciliation_receipt(
        state=transaction_state,
        reconciliation_id=transaction_state["transaction_id"] + "-reconciliation",
        verdict=verdict,
        prior_world_state_digest=sha(
            {"transaction_id": transaction_state["transaction_id"], "world": "prior"}
        ),
        observed_world_state_digest=sha(
            {
                "transaction_id": transaction_state["transaction_id"],
                "world": "observed",
                "verdict": verdict,
            }
        ),
        observed_effect_digest=observed_effect,
        independent_world_evidence_digests=[
            sha(transaction_state["transaction_id"] + "-world-evidence-a"),
            sha(transaction_state["transaction_id"] + "-world-evidence-b"),
        ],
        independent_source_ids=["world-observer-a", "world-observer-b"],
        reconciliation_method_digest=sha("v024-reconciliation-method"),
        rationale_digest=sha(
            transaction_state["transaction_id"] + "-reconciliation-" + verdict
        ),
        reconciled_at_ms=110_000,
    )
    return _apply(
        store,
        transaction_state,
        "reconciled",
        {"reconciliation_receipt": receipt},
        110_001,
    )[0]


def _verified(
    *,
    root: Path,
    store: TransactionStore,
    transaction_state: Mapping[str, Any],
    verdict: str,
    admissible: bool = True,
) -> tuple[dict[str, Any], dict[str, Any]]:
    verify_store, verify_state = prepared_corroborated_state(
        root=root / "verify",
        verify_id=transaction_state["transaction_id"] + "-verify",
        observe_state=transaction_state["observe_state"],
        admissible=admissible,
    )
    verify_state, _ = finish_verify(
        store=verify_store,
        state=verify_state,
        verdict=verdict,
        criterion_satisfied=verdict == "PASSED",
        tick=60,
    )
    state, _ = _apply(
        store,
        transaction_state,
        "verified",
        {"verify_state": verify_state},
        120_100,
    )
    return state, verify_state


def _decide_and_commit(
    *,
    store: TransactionStore,
    transaction_state: Mapping[str, Any],
    compensation_request: Mapping[str, Any] | None = None,
    handover_reason_digest: str = "",
    reobservation_reason_digest: str = "",
) -> tuple[dict[str, Any], dict[str, Any]]:
    decision = build_transaction_decision(
        state=transaction_state,
        compensation_request=compensation_request,
        handover_reason_digest=handover_reason_digest,
        reobservation_reason_digest=reobservation_reason_digest,
        decided_at_ms=130_000,
    )
    decided, _ = _apply(
        store,
        transaction_state,
        "decided",
        {"transaction_decision": decision},
        130_001,
    )
    final_receipt = build_transaction_final_receipt_v0_24(
        state=decided, committed_at_ms=130_100
    )
    committed, commit_event = _apply(
        store,
        decided,
        "committed",
        {
            "transaction_final_receipt": final_receipt,
            "append_only_commit": True,
            "memory_overwrite": False,
            "automatic_compensation": False,
            "automatic_rollback": False,
            "non_authority": copy_non_authority(),
        },
        130_101,
    )
    return committed, commit_event


def _confirmed(root: Path) -> tuple[dict[str, Any], TransactionStore, dict[str, Any]]:
    policy, bundle, _, prepared_act, act_store, _, _, store = _prepared_transaction(
        root,
        transaction_id="transaction-confirmed",
        compensation_mode="explicit_operation",
    )
    state = store.recover()
    state, _ = _effect_bound(
        store=store,
        transaction_state=state,
        act_store=act_store,
        prepared_act=prepared_act,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )
    state, _ = _observed(
        root=root, store=store, transaction_state=state, verdict="MATCHED"
    )
    state = _reconciled(store=store, transaction_state=state, verdict="EFFECT_CONFIRMED")
    state, _ = _verified(
        root=root, store=store, transaction_state=state, verdict="PASSED"
    )
    committed, commit_event = _decide_and_commit(
        store=store, transaction_state=state
    )
    assert committed["route"] == "EFFECT_CONFIRMED"
    assert committed["reconciliation_verdict"] == "EFFECT_CONFIRMED"
    assert committed["verification_route"] == "VERIFICATION_PASSED"
    return committed, store, commit_event


def _compensable(root: Path) -> dict[str, Any]:
    policy, bundle, _, prepared_act, act_store, _, _, store = _prepared_transaction(
        root,
        transaction_id="transaction-compensable",
        compensation_mode="explicit_operation",
    )
    state, _ = _effect_bound(
        store=store,
        transaction_state=store.recover(),
        act_store=act_store,
        prepared_act=prepared_act,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )
    state, _ = _observed(
        root=root, store=store, transaction_state=state, verdict="DIVERGENT"
    )
    state = _reconciled(
        store=store,
        transaction_state=state,
        verdict="COMPENSATION_REQUIRED",
    )
    state, _ = _verified(
        root=root, store=store, transaction_state=state, verdict="FAILED"
    )
    request = build_compensation_request(
        state=state,
        request_id="transaction-compensable-request",
        new_idempotency_key="transaction-compensable-compensation-invocation",
        proposed_plan_lineage_id="transaction-compensable-new-plan-lineage",
        rationale_digest=sha("transaction-compensable-rationale"),
        requested_at_ms=125_000,
    )
    committed, _ = _decide_and_commit(
        store=store,
        transaction_state=state,
        compensation_request=request,
    )
    assert committed["route"] == "COMPENSATION_PROPOSED"
    assert committed["automatic_compensation"] is False
    assert request["requires_new_actos_authorization"] is True
    assert request["same_transaction_execution_forbidden"] is True
    return committed


def _handover(root: Path) -> dict[str, Any]:
    policy, bundle, _, prepared_act, act_store, _, _, store = _prepared_transaction(
        root,
        transaction_id="transaction-handover",
        compensation_mode="noncompensable",
    )
    state, _ = _effect_bound(
        store=store,
        transaction_state=store.recover(),
        act_store=act_store,
        prepared_act=prepared_act,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )
    state, _ = _observed(
        root=root, store=store, transaction_state=state, verdict="DIVERGENT"
    )
    state = _reconciled(
        store=store, transaction_state=state, verdict="EFFECT_PARTIAL"
    )
    state, _ = _verified(
        root=root, store=store, transaction_state=state, verdict="FAILED"
    )
    committed, _ = _decide_and_commit(
        store=store,
        transaction_state=state,
        handover_reason_digest=sha("transaction-handover-required"),
    )
    assert committed["route"] == "HANDOVER_REQUIRED"
    return committed


def _reobserve(root: Path) -> dict[str, Any]:
    policy, bundle, _, prepared_act, act_store, _, _, store = _prepared_transaction(
        root,
        transaction_id="transaction-reobserve",
        compensation_mode="manual_handover",
    )
    state, _ = _effect_bound(
        store=store,
        transaction_state=store.recover(),
        act_store=act_store,
        prepared_act=prepared_act,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )
    state, _ = _observed(
        root=root,
        store=store,
        transaction_state=state,
        verdict="CONFLICTED",
        conflict=True,
    )
    state = _reconciled(
        store=store, transaction_state=state, verdict="EFFECT_CONFLICTED"
    )
    state, _ = _verified(
        root=root,
        store=store,
        transaction_state=state,
        verdict="INDETERMINATE",
        admissible=False,
    )
    committed, _ = _decide_and_commit(
        store=store,
        transaction_state=state,
        reobservation_reason_digest=sha("transaction-reobservation-required"),
    )
    assert committed["route"] == "REOBSERVATION_REQUIRED"
    return committed


def _blocked_no_effect(root: Path) -> dict[str, Any]:
    policy, bundle, _, prepared_act, act_store, _, _, store = _prepared_transaction(
        root,
        transaction_id="transaction-no-effect",
        compensation_mode="manual_handover",
        expires_at_ms=90_050,
    )
    state, _ = _effect_bound(
        store=store,
        transaction_state=store.recover(),
        act_store=act_store,
        prepared_act=prepared_act,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_100,
    )
    assert state["effect_recorded"] is False
    assert state["current_phase"] == "effect_bound"
    committed, _ = _decide_and_commit(
        store=store, transaction_state=state
    )
    assert committed["route"] == "NO_EFFECT_RECORDED"
    assert committed["observe_state_digest"] == ""
    assert committed["verify_state_digest"] == ""
    return committed


def _invalid_confirmed_digest_rejected(root: Path) -> None:
    policy, bundle, _, prepared_act, act_store, _, _, store = _prepared_transaction(
        root,
        transaction_id="transaction-invalid-confirmed",
        compensation_mode="explicit_operation",
    )
    state, _ = _effect_bound(
        store=store,
        transaction_state=store.recover(),
        act_store=act_store,
        prepared_act=prepared_act,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )
    state, _ = _observed(
        root=root, store=store, transaction_state=state, verdict="MATCHED"
    )
    try:
        build_world_effect_reconciliation_receipt(
            state=state,
            reconciliation_id="invalid-confirmed-reconciliation",
            verdict="EFFECT_CONFIRMED",
            prior_world_state_digest=sha("invalid-prior"),
            observed_world_state_digest=sha("invalid-observed-world"),
            observed_effect_digest=sha("substituted-effect"),
            independent_world_evidence_digests=[sha("a"), sha("b")],
            independent_source_ids=["source-a", "source-b"],
            reconciliation_method_digest=sha("method"),
            rationale_digest=sha("rationale"),
            reconciled_at_ms=110_000,
        )
    except ValueError as exc:
        assert str(exc) == "confirmed_effect_digest_mismatch"
    else:
        raise AssertionError("substituted confirmed effect accepted")


def run_transactional_effect_scenarios() -> dict[str, Any]:
    with TemporaryDirectory(prefix="kuuos-transaction-v024-") as temporary:
        root = Path(temporary)
        confirmed, confirmed_store, commit_event = _confirmed(root / "confirmed")
        before_replay = confirmed_store.ledger_commit_count()
        replay = confirmed_store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert confirmed_store.ledger_commit_count() == before_replay

        snapshot = confirmed_store.snapshot_path
        snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            confirmed_store.recover(require_snapshot_match=True)
        except TransactionStoreError as exc:
            assert str(exc) == "transaction_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt transaction snapshot accepted")
        repaired = confirmed_store.repair_snapshot()
        recovered = confirmed_store.recover(require_snapshot_match=True)
        assert repaired["transaction_state_digest"] == recovered[
            "transaction_state_digest"
        ]

        compensable = _compensable(root / "compensable")
        handover = _handover(root / "handover")
        reobserve = _reobserve(root / "reobserve")
        no_effect = _blocked_no_effect(root / "no-effect")
        _invalid_confirmed_digest_rejected(root / "invalid-confirmed")

        stale = deepcopy(commit_event)
        stale["transaction_event_digest"] = sha("stale-unprocessed-event")
        stale_result = apply_transaction_event(confirmed, stale)
        assert stale_result["status"] == "REJECTED"
        assert "transaction_event_state_digest_stale" in stale_result["errors"]

        assert validate_transaction_state(confirmed) == []
        assert confirmed["automatic_compensation"] is False
        assert confirmed["automatic_rollback"] is False
        assert confirmed["hidden_connector_call_performed"] is False
        assert confirmed["memory_overwrite"] is False

        return {
            "status": "KUUOS_TRANSACTIONAL_EFFECT_RECONCILIATION_V0_24_OK",
            "confirmed_route": confirmed["route"],
            "compensation_route": compensable["route"],
            "handover_route": handover["route"],
            "reobservation_route": reobserve["route"],
            "no_effect_route": no_effect["route"],
            "replay_status": replay["status"],
            "ledger_commits": confirmed_store.ledger_commit_count(),
            "recovered_transaction_state_digest": recovered[
                "transaction_state_digest"
            ],
            "tool_response_success_not_world_confirmation": confirmed[
                "final_receipt"
            ]["tool_response_success_not_world_confirmation"],
            "automatic_compensation": confirmed["automatic_compensation"],
            "automatic_rollback": confirmed["automatic_rollback"],
            "execution_authority_granted": False,
        }


__all__ = ["run_transactional_effect_scenarios"]
