from __future__ import annotations

import json
import math
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_mission_kernel_v0_20 import (
    NON_AUTHORITY_FLAGS,
    append_jsonl,
    apply_mission_decision,
    build_authority_scope,
    build_evidence_policy,
    build_goal_policy,
    build_goal_portfolio,
    build_goal_proposal,
    build_initial_mission_state,
    build_mission_command,
    build_mission_contract,
    build_mission_evidence,
    build_override_policy,
    build_renewal_policy,
    build_resource_envelope,
    build_successor_mission_contract,
    build_successor_mission_state,
    evaluate_mission_lifecycle,
    read_json,
    record_mission_usage,
    validate_goal_portfolio,
    validate_mission_contract,
    validate_mission_state,
    write_json_atomic,
)


def fixture_contract(
    *, allow_resource_increase: bool = False, max_cycles: int = 3
) -> dict:
    return build_mission_contract(
        mission_id="mission-alpha",
        lineage_id="lineage-alpha",
        revision=0,
        parent_contract_digest="",
        issuer_id="user-a",
        issuer_role="user",
        governance_root_digest="governance-root-v1",
        purpose="Produce a verified, bounded, user-steerable research artifact.",
        success_criteria=["artifact_verified", "user_acceptance_recorded"],
        failure_criteria=["invariant_breach", "evidence_unrecoverable"],
        invariants=[
            "bounded_cycle",
            "foreground_user_control_available",
            "plan_not_permission",
        ],
        prohibited_outcomes=["hidden_background_execution", "unbounded_authority"],
        resource_envelope=build_resource_envelope(
            max_total_cost=10.0,
            max_cycle_cost=3.0,
            max_cycles_before_renewal=max_cycles,
            max_active_goals=2,
            max_goal_count=5,
            reserve_floor=1.0,
        ),
        authority_scope=build_authority_scope(
            domain_scope=["research", "documentation"],
            requested_capabilities=[
                "read_sources",
                "write_artifact",
                "run_validator",
            ],
        ),
        renewal_policy=build_renewal_policy(
            max_renewals=2,
            renewal_window_ms=1000,
            authorized_roles=["user", "governance"],
            allow_resource_increase=allow_resource_increase,
        ),
        override_policy=build_override_policy(
            {
                "user": [
                    "pause",
                    "resume",
                    "terminate",
                    "handover",
                    "request_renewal",
                    "renew",
                ],
                "governance": [
                    "pause",
                    "terminate",
                    "handover",
                    "request_renewal",
                    "renew",
                ],
                "operator": ["pause", "request_renewal"],
            }
        ),
        evidence_policy=build_evidence_policy(
            completion_roles=["user", "verifier"],
            failure_roles=["user", "verifier", "governance"],
            invariant_roles=["governance", "verifier"],
            minimum_confidence=0.8,
        ),
        goal_policy=build_goal_policy(plurality_floor=0.1),
        created_at_ms=1000,
        valid_from_ms=1000,
        expires_at_ms=10000,
    )


def _main_flow() -> None:
    contract = fixture_contract()
    assert validate_mission_contract(contract) == []
    assert contract["non_authority"] == NON_AUTHORITY_FLAGS
    state = build_initial_mission_state(contract, now_ms=1000)
    assert state["lifecycle_state"] == "active"
    assert validate_mission_state(state, contract) == []

    goal_a = build_goal_proposal(
        contract=contract,
        goal_id="goal-a",
        objective="Collect source evidence",
        priority_weight=0.6,
        horizon="short",
        expected_outcomes=["source_packet_ready"],
        required_capabilities=["read_sources"],
        dependencies=[],
        requested_cost=1.0,
        requested_cycles=1,
        created_at_ms=1000,
    )
    goal_b = build_goal_proposal(
        contract=contract,
        goal_id="goal-b",
        objective="Draft the artifact",
        priority_weight=0.4,
        horizon="medium",
        expected_outcomes=["draft_ready"],
        required_capabilities=["write_artifact"],
        dependencies=["goal-a"],
        requested_cost=2.0,
        requested_cycles=1,
        created_at_ms=1001,
    )
    goal_c = build_goal_proposal(
        contract=contract,
        goal_id="goal-c",
        objective="Open unrestricted authority",
        priority_weight=0.2,
        horizon="long",
        expected_outcomes=["unbounded_authority"],
        required_capabilities=[],
        dependencies=[],
        requested_cost=1.0,
        requested_cycles=1,
        created_at_ms=1002,
    )
    portfolio = build_goal_portfolio(
        contract=contract, goals=[goal_a, goal_b, goal_c], now_ms=1100
    )
    assert validate_goal_portfolio(portfolio, contract) == []
    assert portfolio["active_goal_ids"] == ["goal-a", "goal-b"]
    assert portfolio["recommended_goal_id"] == "goal-a"
    assert portfolio["recommendation_grants_effect_authority"] is False
    assert portfolio["rejected_goals"] == [
        {"goal_id": "goal-c", "reason": "prohibited_outcome_collision"}
    ]
    assert abs(sum(portfolio["normalized_weights"].values()) - 1.0) < 1e-12
    assert all(value >= 0.1 for value in portfolio["normalized_weights"].values())

    continued = evaluate_mission_lifecycle(
        contract=contract, state=state, now_ms=1200
    )
    assert continued["decision"] == "continue"
    applied_continue = apply_mission_decision(
        contract=contract, state=state, decision=continued
    )
    state = applied_continue["result_state"]
    assert state["lifecycle_state"] == "active"

    pause_command = build_mission_command(
        contract=contract,
        state=state,
        actor_id="user-a",
        actor_role="user",
        command="pause",
        reason="Review intermediate evidence",
        issued_at_ms=1300,
    )
    pause_decision = evaluate_mission_lifecycle(
        contract=contract, state=state, now_ms=1300, command=pause_command
    )
    paused_result = apply_mission_decision(
        contract=contract, state=state, decision=pause_decision
    )
    paused_state = paused_result["result_state"]
    assert paused_state["lifecycle_state"] == "paused"
    replay = apply_mission_decision(
        contract=contract, state=paused_state, decision=pause_decision
    )
    assert replay["status"] == "REPLAYED"
    assert replay["result_state_digest"] == paused_state["mission_state_digest"]

    resume_command = build_mission_command(
        contract=contract,
        state=paused_state,
        actor_id="user-a",
        actor_role="user",
        command="resume",
        reason="Review complete",
        issued_at_ms=1400,
    )
    resume_decision = evaluate_mission_lifecycle(
        contract=contract,
        state=paused_state,
        now_ms=1400,
        command=resume_command,
    )
    resumed_result = apply_mission_decision(
        contract=contract, state=paused_state, decision=resume_decision
    )
    state = resumed_result["result_state"]
    assert state["lifecycle_state"] == "active"

    state = record_mission_usage(
        state, contract, cost=2.0, completed_cycles=3, now_ms=1500
    )
    renewal_decision = evaluate_mission_lifecycle(
        contract=contract, state=state, now_ms=1500
    )
    assert renewal_decision["decision"] == "renewal_required"
    renewal_result = apply_mission_decision(
        contract=contract, state=state, decision=renewal_decision
    )
    renewal_state = renewal_result["result_state"]
    assert renewal_state["lifecycle_state"] == "renewal_required"

    renewal_command = build_mission_command(
        contract=contract,
        state=renewal_state,
        actor_id="user-a",
        actor_role="user",
        command="renew",
        reason="Continue under the same bounded envelope",
        issued_at_ms=1600,
    )
    successor = build_successor_mission_contract(
        parent_contract=contract,
        parent_state=renewal_state,
        renewal_command=renewal_command,
        created_at_ms=1600,
        valid_from_ms=1600,
        expires_at_ms=20000,
    )
    assert successor["revision"] == 1
    assert successor["parent_contract_digest"] == contract["mission_contract_digest"]
    successor_state = build_successor_mission_state(
        parent_state=renewal_state,
        successor_contract=successor,
        now_ms=1600,
    )
    assert (
        successor_state["predecessor_state_digest"]
        == renewal_state["mission_state_digest"]
    )
    assert successor_state["lifecycle_state"] == "active"

    success_evidence = build_mission_evidence(
        contract=successor,
        state=successor_state,
        source_id="verifier-a",
        source_role="verifier",
        evidence_level="authorized_verification",
        observed_at_ms=1700,
        confidence=0.95,
        success_verified=True,
        evidence_refs=["receipt-1", "independent-check-1"],
    )
    completion_decision = evaluate_mission_lifecycle(
        contract=successor,
        state=successor_state,
        now_ms=1700,
        evidence=success_evidence,
    )
    assert completion_decision["decision"] == "complete"
    completed = apply_mission_decision(
        contract=successor,
        state=successor_state,
        decision=completion_decision,
    )["result_state"]
    assert completed["lifecycle_state"] == "completed"


def _edge_cases() -> None:
    contract = fixture_contract()
    state = build_initial_mission_state(contract, now_ms=1000)

    try:
        build_resource_envelope(
            max_total_cost=math.inf,
            max_cycle_cost=1.0,
            max_cycles_before_renewal=1,
            max_active_goals=1,
            max_goal_count=1,
        )
        raise AssertionError("infinite resource envelope accepted")
    except ValueError as exc:
        assert "not_finite" in str(exc)

    tampered_contract = deepcopy(contract)
    tampered_contract["authority_scope"]["network_authority_granted"] = True
    tampered_contract["mission_contract_digest"] = ""
    from runtime.kuuos_mission_contract_kernel_v0_20 import contract_digest

    tampered_contract["mission_contract_digest"] = contract_digest(tampered_contract)
    assert "authority_scope_forbidden:network_authority_granted" in validate_mission_contract(
        tampered_contract
    )

    try:
        build_mission_command(
            contract=contract,
            state=state,
            actor_id="operator-a",
            actor_role="operator",
            command="terminate",
            reason="Unauthorized termination",
            issued_at_ms=1100,
        )
        raise AssertionError("unauthorized mission command accepted")
    except ValueError as exc:
        assert "not_authorized" in str(exc)

    stale_state = record_mission_usage(
        state, contract, cost=0.1, completed_cycles=0, now_ms=1100
    )
    command = build_mission_command(
        contract=contract,
        state=state,
        actor_id="user-a",
        actor_role="user",
        command="pause",
        reason="Pause",
        issued_at_ms=1100,
    )
    try:
        evaluate_mission_lifecycle(
            contract=contract, state=stale_state, now_ms=1100, command=command
        )
        raise AssertionError("stale command accepted")
    except ValueError as exc:
        assert "stale" in str(exc)

    try:
        build_mission_evidence(
            contract=contract,
            state=state,
            source_id="verifier-a",
            source_role="verifier",
            evidence_level="authorized_verification",
            observed_at_ms=1100,
            confidence=0.9,
            success_verified=True,
            failure_verified=True,
        )
        raise AssertionError("conflicting evidence accepted")
    except ValueError as exc:
        assert "success_failure_conflict" in str(exc)

    weak_success = build_mission_evidence(
        contract=contract,
        state=state,
        source_id="observer-a",
        source_role="observer",
        evidence_level="observation",
        observed_at_ms=1100,
        confidence=0.99,
        success_verified=True,
    )
    weak_decision = evaluate_mission_lifecycle(
        contract=contract,
        state=state,
        now_ms=1100,
        evidence=weak_success,
    )
    assert weak_decision["decision"] == "pause"
    assert weak_decision["reason"] == "success_evidence_not_authorized"

    goal_x = build_goal_proposal(
        contract=contract,
        goal_id="goal-x",
        objective="Choose path X",
        priority_weight=0.5,
        horizon="short",
        expected_outcomes=["path-x"],
        required_capabilities=[],
        dependencies=[],
        requested_cost=1.0,
        requested_cycles=1,
        created_at_ms=1000,
        exclusive_group="path-choice",
    )
    goal_y = build_goal_proposal(
        contract=contract,
        goal_id="goal-y",
        objective="Choose path Y",
        priority_weight=0.5,
        horizon="short",
        expected_outcomes=["path-y"],
        required_capabilities=[],
        dependencies=[],
        requested_cost=1.0,
        requested_cycles=1,
        created_at_ms=1001,
        exclusive_group="path-choice",
    )
    tied = build_goal_portfolio(
        contract=contract, goals=[goal_x, goal_y], now_ms=1200
    )
    assert tied["active_goal_ids"] == []
    assert {item["reason"] for item in tied["held_goals"]} == {
        "human_arbitration_required"
    }

    too_large_goal = build_goal_proposal(
        contract=contract,
        goal_id="goal-large",
        objective="Exceed one-cycle resource envelope",
        priority_weight=0.4,
        horizon="medium",
        expected_outcomes=["large-output"],
        required_capabilities=[],
        dependencies=[],
        requested_cost=4.0,
        requested_cycles=1,
        created_at_ms=1200,
    )
    resource_held = build_goal_portfolio(
        contract=contract, goals=[too_large_goal], now_ms=1200
    )
    assert resource_held["held_goals"] == [
        {
            "goal_id": "goal-large",
            "reason": "resource_request_exceeds_envelope",
        }
    ]

    terminal_evidence = build_mission_evidence(
        contract=contract,
        state=state,
        source_id="verifier-a",
        source_role="verifier",
        evidence_level="authorized_verification",
        observed_at_ms=1200,
        confidence=0.9,
        success_verified=True,
    )
    terminal_decision = evaluate_mission_lifecycle(
        contract=contract,
        state=state,
        now_ms=1200,
        evidence=terminal_evidence,
    )
    completed = apply_mission_decision(
        contract=contract, state=state, decision=terminal_decision
    )["result_state"]
    terminal_check = evaluate_mission_lifecycle(
        contract=contract, state=completed, now_ms=1300
    )
    assert terminal_check["decision"] == "no_change"
    assert terminal_check["reason"] == "mission_terminal"

    renewal_state = record_mission_usage(
        state, contract, cost=0.0, completed_cycles=3, now_ms=1300
    )
    renewal_decision = evaluate_mission_lifecycle(
        contract=contract, state=renewal_state, now_ms=1300
    )
    renewal_state = apply_mission_decision(
        contract=contract, state=renewal_state, decision=renewal_decision
    )["result_state"]
    renewal_command = build_mission_command(
        contract=contract,
        state=renewal_state,
        actor_id="user-a",
        actor_role="user",
        command="renew",
        reason="Attempt resource increase",
        issued_at_ms=1400,
    )
    increased = build_resource_envelope(
        max_total_cost=20.0,
        max_cycle_cost=3.0,
        max_cycles_before_renewal=3,
        max_active_goals=2,
        max_goal_count=5,
        reserve_floor=1.0,
    )
    try:
        build_successor_mission_contract(
            parent_contract=contract,
            parent_state=renewal_state,
            renewal_command=renewal_command,
            created_at_ms=1400,
            valid_from_ms=1400,
            expires_at_ms=20000,
            resource_envelope=increased,
        )
        raise AssertionError("forbidden resource increase accepted")
    except ValueError as exc:
        assert "resource_increase_forbidden" in str(exc)

    tampered_state = deepcopy(state)
    tampered_state["used_cost"] = 99.0
    assert "mission_state_digest_invalid" in validate_mission_state(
        tampered_state, contract
    )


def _io_cases() -> None:
    contract = fixture_contract()
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        contract_path = root / "contract.json"
        audit_path = root / "audit.jsonl"
        write_json_atomic(contract_path, contract)
        assert read_json(contract_path) == contract
        try:
            write_json_atomic(contract_path, contract)
            raise AssertionError("overwrite without permission accepted")
        except FileExistsError:
            pass
        write_json_atomic(contract_path, contract, allow_overwrite=True)
        append_jsonl(
            audit_path,
            {
                "event": "contract_persisted",
                "digest": contract["mission_contract_digest"],
            },
        )
        append_jsonl(audit_path, {"event": "contract_validated", "valid": True})
        rows = [
            json.loads(line)
            for line in audit_path.read_text(encoding="utf-8").splitlines()
        ]
        assert [row["event"] for row in rows] == [
            "contract_persisted",
            "contract_validated",
        ]


def _readiness_overlay_case() -> None:
    base_path = Path(
        "manifests/kuuos_autonomous_agent_completion_architecture_v0_19.json"
    )
    overlay_path = Path(
        "manifests/kuuos_autonomous_agent_completion_status_v0_20.json"
    )
    if not base_path.exists() or not overlay_path.exists():
        print("SKIP: v0.19 readiness files unavailable in local prototype")
        return
    from runtime.kuuos_autonomous_agent_readiness_v0_20 import (
        load_and_resolve,
        validate_status_overlay,
    )

    resolved = load_and_resolve(
        base_manifest_path=base_path,
        status_overlay_path=overlay_path,
    )
    report = resolved["readiness_report"]
    assert report["status_counts"] == {
        "implemented": 4,
        "open_gap": 10,
        "partial_gap": 2,
    }
    assert report["open_component_count"] == 12
    assert report["next_dependency_rank"] == 2
    assert report["next_release"] == "v0.21"
    assert resolved["execution_authority_opened"] is False

    base = json.loads(base_path.read_text(encoding="utf-8"))
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    tampered = deepcopy(overlay)
    tampered["component_updates"][0]["evidence"].pop(
        "non_authority_boundary"
    )
    assert any(
        error.startswith(
            "component_update_evidence_incomplete:mission_contract_kernel"
        )
        for error in validate_status_overlay(base, tampered)
    )


def main() -> bool:
    _main_flow()
    _edge_cases()
    _io_cases()
    _readiness_overlay_case()
    print("PASS: mission contract kernel v0.20")
    return True


if __name__ == "__main__":
    main()
