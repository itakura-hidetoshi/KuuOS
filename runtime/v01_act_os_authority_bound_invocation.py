from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import BLOCKED, READY
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_act_os_fixture_v0_1 import (
    apply,
    event,
    host_inputs,
    prepared_project_state,
    source_plan,
)
from runtime.kuuos_act_os_kernel_v0_1 import (
    build_authorized_invoke_event,
    build_initial_act_state,
    build_step_authorization,
)
from runtime.kuuos_act_os_store_v0_1 import ActStore, ActStoreError
from runtime.kuuos_act_os_types_v0_1 import copy_non_authority
from runtime.v017_host_adapter_fixtures import registry


def _finish(
    *,
    store: ActStore,
    state: dict,
    bundle: dict,
    policy: dict,
    invoke_ms: int,
) -> tuple[dict, dict]:
    invoke_event, tick = build_authorized_invoke_event(
        state=state,
        supervisor_bundle=bundle,
        worker_id="act-worker",
        now_ms=invoke_ms,
        supervisor_policy=policy,
        registry=registry(),
    )
    result = store.apply(invoke_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    state = result["state"]
    state = apply(
        store,
        state,
        "verify",
        {"verification_receipt_digest": sha("act-verification")},
        invoke_ms - 90_000 + 1,
    )
    commit_event = event(
        state,
        "commit",
        {
            "memory_overwrite": False,
            "automatic_truth_promotion": False,
            "automatic_plan_completion": False,
            "automatic_rollback": False,
            "lower_host_receipt_canonical": True,
            "source_lineage_preserved": True,
            "non_authority": copy_non_authority(),
        },
        invoke_ms - 90_000 + 2,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _missing_human_is_blocked(root: Path, plan_state: dict, activation: dict) -> None:
    _, bundle, license_packet, _ = host_inputs(job_id="missing-human-job")
    store = ActStore(root)
    state = store.initialize(
        build_initial_act_state(
            act_id="missing-human",
            plan_state=plan_state,
            plan_activation_receipt=activation,
            now_ms=90_000,
        )
    )
    state = apply(
        store,
        state,
        "select",
        {
            "plan_state": plan_state,
            "selected_step_id": "act-candidate",
            "operation_id": "fixture.success",
            "operation_input_digest": sha({"value": 1}),
        },
        20,
    )
    try:
        build_step_authorization(
            state=state,
            authorization_id="missing-human-auth",
            operation_id="fixture.success",
            operation_input_digest=sha({"value": 1}),
            act_phase_receipt_digest=sha("missing-human-act-phase"),
            invocation_id="missing-human-invocation",
            source_supervisor_bundle_digest=bundle["supervisor_bundle_digest"],
            host_job_id="missing-human-job",
            host_step_id="step-1",
            host_license=license_packet,
            issued_at_ms=90_000,
            expires_at_ms=100_000,
        )
    except ValueError as exc:
        if str(exc) != "human_approval_receipt_digest_required":
            raise
    else:
        raise AssertionError("human approval was not required")


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-act-os-v01-") as temporary:
        root = Path(temporary)
        plan_state, activation = source_plan(root)

        policy, bundle, license_packet, projection = host_inputs(job_id="ready-job")
        store, state = prepared_project_state(
            root=root / "ready",
            act_id="act-ready",
            plan_state=plan_state,
            plan_activation=activation,
            job_id="ready-job",
            host_license=license_packet,
            projection=projection,
        )
        ready, commit_event = _finish(
            store=store,
            state=state,
            bundle=bundle,
            policy=policy,
            invoke_ms=90_004,
        )
        assert ready["route"] == "EFFECT_RECORDED"
        assert ready["host_receipt"]["status"] == READY
        assert ready["effect_recorded"] is True
        assert ready["observation_required"] is True
        assert ready["verification_required"] is True
        assert ready["automatic_truth_promotion"] is False
        assert ready["automatic_plan_completion"] is False
        assert ready["automatic_rollback"] is False

        before_replay = store.ledger_commit_count()
        replay = store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_replay

        snapshot_path = root / "ready" / "act-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except ActStoreError as exc:
            assert str(exc) == "act_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt snapshot accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["act_state_digest"] == recovered["act_state_digest"]

        _missing_human_is_blocked(root / "missing-human", plan_state, activation)

        exp_policy, exp_bundle, exp_license, exp_projection = host_inputs(
            job_id="expired-job", expires_at_ms=90_050
        )
        exp_store, exp_state = prepared_project_state(
            root=root / "expired",
            act_id="act-expired",
            plan_state=plan_state,
            plan_activation=activation,
            job_id="expired-job",
            host_license=exp_license,
            projection=exp_projection,
        )
        blocked, _ = _finish(
            store=exp_store,
            state=exp_state,
            bundle=exp_bundle,
            policy=exp_policy,
            invoke_ms=90_100,
        )
        assert blocked["route"] == "BLOCKED"
        assert blocked["host_receipt"]["status"] == BLOCKED
        assert "host_license_expired" in blocked["blockers"]
        assert blocked["effect_recorded"] is False

        return {
            "status": "ACT_OS_AUTHORITY_BOUND_INVOCATION_V0_1_OK",
            "ready_route": ready["route"],
            "ready_host_receipt_digest": ready["host_receipt_digest"],
            "observation_required": ready["observation_required"],
            "verification_required": ready["verification_required"],
            "blocked_route": blocked["route"],
            "blocked_reason": blocked["blockers"],
            "ledger_commits": store.ledger_commit_count(),
            "recovered_act_state_digest": recovered["act_state_digest"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
