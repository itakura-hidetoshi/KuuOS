from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_event_wakeup_control_resource_scenarios_v0_25 import (
    _admitted_and_replay,
)
from runtime.kuuos_governed_self_modification_kernel_v0_26 import (
    apply_event,
    build_decision,
    build_event,
    build_external_approval,
    build_initial_state,
    build_limited_deployment_authorization,
    build_rollback_receipt,
    build_self_modification_proposal,
    build_stage_evidence,
    validate_state,
)
from runtime.kuuos_governed_self_modification_store_v0_26 import (
    SelfModificationStore,
    SelfModificationStoreError,
)


def _initial(
    root: Path,
    *,
    proposal_id: str,
    requested_actions: list[str] | None = None,
    approval_required: bool = True,
) -> tuple[dict[str, Any], SelfModificationStore]:
    source = _admitted_and_replay(root / "source-v025")
    proposal = build_self_modification_proposal(
        proposal_id=proposal_id,
        source_v025_state=source,
        base_artifact_digest=sha(proposal_id + "-base"),
        candidate_artifact_digest=sha(proposal_id + "-candidate"),
        rollback_artifact_digest=sha(proposal_id + "-rollback"),
        changed_paths=["runtime/example.py", "tests/test_example.py"],
        intended_improvement_digest=sha(proposal_id + "-improvement"),
        success_criteria_digest=sha(proposal_id + "-success-criteria"),
        requested_actions=list(requested_actions or []),
        external_approval_required=approval_required,
        max_canary_percent=5,
        max_deployment_cycles=3,
        rollback_window_ms=10_000,
        proposed_at_ms=300_000,
    )
    state = build_initial_state(
        proposal=proposal, source_v025_state=source, now_ms=300_000
    )
    store = SelfModificationStore(root / "self-modification-store")
    return store.initialize(state), store


def _apply(
    store: SelfModificationStore,
    state: Mapping[str, Any],
    kind: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    event = build_event(
        state=state, event_kind=kind, payload=payload, now_ms=now_ms
    )
    result = store.apply(event)
    if result["status"] != "APPLIED":
        raise AssertionError(result)
    return result["state"], event


def _stage(
    store: SelfModificationStore,
    state: Mapping[str, Any],
    *,
    stage: str,
    passed: bool,
    findings: list[str] | None = None,
    now_ms: int,
) -> dict[str, Any]:
    evidence = build_stage_evidence(
        state=state,
        stage=stage,
        passed=passed,
        evidence_digests=[sha(f"{state['proposal_digest']}:{stage}:evidence")],
        finding_codes=list(findings or []),
        isolated_environment_digest=sha(f"{stage}:isolated-environment"),
        evaluator_id=f"{stage}-external-evaluator",
        evaluated_at_ms=now_ms,
    )
    return _apply(store, state, "stage_evidence", evidence, now_ms + 1)[0]


def _pass_all_stages(
    store: SelfModificationStore, state: Mapping[str, Any]
) -> dict[str, Any]:
    now = 300_010
    for stage in (
        "static_analysis",
        "sandbox",
        "regression",
        "formal_property",
        "canary",
    ):
        state = _stage(store, state, stage=stage, passed=True, now_ms=now)
        now += 10
    return dict(state)


def _approve(
    store: SelfModificationStore, state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    approval = build_external_approval(
        state=state,
        approver_id="external-governance-board",
        approver_authority_digest=sha("external-governance-authority"),
        approved=True,
        approval_scope_digest=sha("limited-canary-deployment-scope"),
        expires_at_ms=now_ms + 20_000,
        approved_at_ms=now_ms,
    )
    return _apply(store, state, "external_approval", approval, now_ms + 1)[0]


def _decide(
    store: SelfModificationStore, state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    decision = build_decision(
        state=state,
        rationale_digest=sha(state["proposal_digest"] + ":decision"),
        decided_at_ms=now_ms,
    )
    return _apply(store, state, "decision", decision, now_ms + 1)[0]


def _deploy(
    store: SelfModificationStore, state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    authorization = build_limited_deployment_authorization(
        state=state,
        deployment_id=state["proposal"]["proposal_id"] + "-limited-deployment",
        scope_digest=sha("five-percent-three-cycle-canary"),
        canary_percent=5,
        deployment_cycles=3,
        deployment_expires_at_ms=now_ms + 9_000,
        rollback_deadline_ms=now_ms + 10_000,
        authorized_at_ms=now_ms,
    )
    return _apply(
        store, state, "limited_deployment", authorization, now_ms + 1
    )[0]


def _successful_close(root: Path) -> tuple[dict[str, Any], SelfModificationStore, dict[str, Any]]:
    state, store = _initial(root, proposal_id="safe-success-proposal")
    state = _pass_all_stages(store, state)
    state = _approve(store, state, 300_100)
    state = _decide(store, state, 300_110)
    assert state["route"] == "LIMITED_DEPLOYMENT_AUTHORIZED"
    state = _deploy(store, state, 300_120)
    close_payload = {
        "independent_post_deployment_evidence_digest": sha("post-deployment-evidence"),
        "verification_receipt_digest": sha("post-deployment-verification"),
        "rollback_window_observation_digest": sha("rollback-window-observation"),
        "external_verification_passed": True,
        "canary_success_is_truth": False,
        "permanent_renewal_granted": False,
        "closed_at_ms": 310_120,
    }
    state, close_event = _apply(
        store, state, "close_success", close_payload, 310_121
    )
    assert state["route"] == "DEPLOYMENT_CLOSED_SUCCESS"
    assert state["deployment_closed"] is True
    return state, store, close_event


def _rollback(root: Path) -> dict[str, Any]:
    state, store = _initial(root, proposal_id="safe-rollback-proposal")
    state = _pass_all_stages(store, state)
    state = _approve(store, state, 300_100)
    state = _decide(store, state, 300_110)
    state = _deploy(store, state, 300_120)
    receipt = build_rollback_receipt(
        state=state,
        rollback_id="safe-rollback-receipt",
        trigger_digest=sha("canary-regression-trigger"),
        observed_failure_digest=sha("canary-regression-observation"),
        external_actos_receipt_digest=sha("external-actos-rollback-receipt"),
        rolled_back_at_ms=305_000,
    )
    state, _ = _apply(store, state, "rollback", receipt, 305_001)
    assert state["route"] == "ROLLED_BACK"
    assert state["automatic_rollback_performed"] is False
    return state


def _forbidden(root: Path) -> dict[str, Any]:
    forbidden = [
        "widen_own_authority",
        "disable_audit",
        "remove_rollback",
    ]
    state, store = _initial(
        root,
        proposal_id="forbidden-proposal",
        requested_actions=forbidden,
    )
    state = _stage(
        store,
        state,
        stage="static_analysis",
        passed=False,
        findings=forbidden,
        now_ms=300_010,
    )
    state = _decide(store, state, 300_020)
    assert state["route"] == "REJECTED_PERMANENT_FORBIDDEN_ACTION"
    assert state["current_stage"] == "decision"
    return state


def _regression_failure(root: Path) -> dict[str, Any]:
    state, store = _initial(
        root,
        proposal_id="regression-failure-proposal",
        approval_required=False,
    )
    state = _stage(store, state, stage="static_analysis", passed=True, now_ms=300_010)
    state = _stage(store, state, stage="sandbox", passed=True, now_ms=300_020)
    state = _stage(
        store,
        state,
        stage="regression",
        passed=False,
        findings=["existing_behavior_regressed"],
        now_ms=300_030,
    )
    state = _decide(store, state, 300_040)
    assert state["route"] == "REJECTED_VALIDATION_FAILURE"
    return state


def _approval_missing(root: Path) -> dict[str, Any]:
    state, store = _initial(root, proposal_id="approval-missing-proposal")
    state = _pass_all_stages(store, state)
    state = _decide(store, state, 300_100)
    assert state["route"] == "EXTERNAL_APPROVAL_REQUIRED"
    return state


def run_governed_self_modification_scenarios() -> dict[str, Any]:
    with TemporaryDirectory(prefix="kuuos-self-mod-v026-") as temporary:
        root = Path(temporary)
        successful, store, close_event = _successful_close(root / "success")
        rolled_back = _rollback(root / "rollback")
        forbidden = _forbidden(root / "forbidden")
        regression = _regression_failure(root / "regression")
        approval_missing = _approval_missing(root / "approval-missing")

        before = store.ledger_event_count()
        replay = store.apply(close_event)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_event_count() == before

        stale = deepcopy(close_event)
        stale["self_modification_event_digest"] = sha("stale-self-modification-event")
        stale_result = apply_event(successful, stale)
        assert stale_result["status"] == "REJECTED"
        assert "event_state_stale" in stale_result["errors"]

        store.snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except SelfModificationStoreError as exc:
            assert str(exc) == "self_modification_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt self-modification snapshot accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["self_modification_state_digest"] == recovered[
            "self_modification_state_digest"
        ]

        assert validate_state(successful) == []
        assert successful["running_system_modified_by_gate"] is False
        assert successful["direct_production_deployment_performed"] is False
        assert successful["authority_widened"] is False
        assert successful["audit_disabled"] is False
        assert successful["provenance_erased"] is False
        assert successful["rollback_removed"] is False

        return {
            "status": "KUUOS_GOVERNED_SELF_MODIFICATION_V0_26_OK",
            "success_route": successful["route"],
            "rollback_route": rolled_back["route"],
            "forbidden_route": forbidden["route"],
            "regression_route": regression["route"],
            "approval_missing_route": approval_missing["route"],
            "replay_status": replay["status"],
            "stale_status": stale_result["status"],
            "gate_modified_running_system": successful[
                "running_system_modified_by_gate"
            ],
            "authority_widened": successful["authority_widened"],
            "automatic_rollback": successful["automatic_rollback_performed"],
            "execution_authority_granted": False,
            "recovered_state_digest": recovered[
                "self_modification_state_digest"
            ],
        }


__all__ = ["run_governed_self_modification_scenarios"]
