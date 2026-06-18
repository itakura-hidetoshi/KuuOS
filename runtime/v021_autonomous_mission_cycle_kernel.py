from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_autonomous_mission_cycle_kernel_v0_21 import (
    apply_mission_cycle_event,
    build_initial_mission_cycle_state,
    build_mission_cycle_event,
)
from runtime.kuuos_autonomous_mission_cycle_store_v0_21 import (
    apply_mission_cycle_event_persisted,
    initialize_mission_cycle_store,
    recover_mission_cycle_store,
)
from runtime.kuuos_mission_contract_types_v0_20 import (
    build_authority_scope,
    build_evidence_policy,
    build_goal_policy,
    build_mission_contract,
    build_override_policy,
    build_renewal_policy,
    build_resource_envelope,
)
from runtime.kuuos_mission_state_v0_20 import (
    build_initial_mission_state,
    record_mission_usage,
)


def _fixture() -> tuple[dict, dict]:
    contract = build_mission_contract(
        mission_id="mission-v021",
        lineage_id="lineage-v021",
        revision=0,
        parent_contract_digest="",
        issuer_id="owner-1",
        issuer_role="owner",
        governance_root_digest="governance-root-v021",
        purpose="Persist the autonomous mission learning cycle",
        success_criteria=["cycle_receipts_are_durable"],
        failure_criteria=["phase_order_is_broken"],
        invariants=["append_only", "lower_authority_preserved"],
        prohibited_outcomes=["unlicensed_effect", "memory_overwrite"],
        resource_envelope=build_resource_envelope(
            max_total_cost=100.0,
            max_cycle_cost=10.0,
            max_cycles_before_renewal=10,
            max_active_goals=3,
            max_goal_count=6,
            reserve_floor=5.0,
        ),
        authority_scope=build_authority_scope(
            domain_scope=["software_runtime"],
            requested_capabilities=["host.invoke"],
        ),
        renewal_policy=build_renewal_policy(
            max_renewals=2,
            renewal_window_ms=1_000,
            authorized_roles=["owner"],
        ),
        override_policy=build_override_policy(
            {
                "owner": [
                    "pause",
                    "resume",
                    "terminate",
                    "handover",
                    "request_renewal",
                    "renew",
                ]
            }
        ),
        evidence_policy=build_evidence_policy(
            completion_roles=["verifier"],
            failure_roles=["verifier"],
            invariant_roles=["verifier"],
            minimum_confidence=0.8,
        ),
        goal_policy=build_goal_policy(plurality_floor=0.05),
        created_at_ms=0,
        valid_from_ms=0,
        expires_at_ms=100_000,
    )
    mission_state = build_initial_mission_state(contract, now_ms=1)
    return contract, mission_state


def _phase_metadata(phase: str) -> dict:
    if phase == "act":
        return {
            "action_receipt_digest": "action-receipt-001",
            "lower_authority_receipt_digest": "v017-host-license-receipt-001",
            "licensed_effect_applied": True,
        }
    if phase == "verify":
        return {
            "verdict": "failed",
            "verification_evidence_digest": "verification-evidence-001",
        }
    if phase == "learn":
        return {"future_only": True, "memory_overwrite": False}
    if phase == "replan":
        return {"next_plan_basis_digest": "next-plan-basis-001"}
    return {}


def run_kernel() -> dict:
    contract, mission_state = _fixture()
    initial = build_initial_mission_cycle_state(
        contract=contract, mission_state=mission_state, now_ms=2
    )
    phases = ["plan", "act", "observe", "verify", "learn", "replan"]
    events: list[dict] = []

    with TemporaryDirectory() as directory:
        initialize_mission_cycle_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            initial_cycle_state=initial,
        )
        state = initial
        for index, phase in enumerate(phases, start=3):
            if phase == "observe":
                mission_state = record_mission_usage(
                    mission_state,
                    contract,
                    cost=0.25,
                    completed_cycles=0,
                    now_ms=index,
                )
            event = build_mission_cycle_event(
                contract=contract,
                mission_state=mission_state,
                cycle_state=state,
                artifact_digest=f"artifact-{phase}-001",
                artifact_refs=[f"ref-{phase}-001"],
                actor_id="agent-1",
                actor_role="worker",
                issued_at_ms=index,
                cost=1.0 if phase == "act" else 0.0,
                metadata=_phase_metadata(phase),
            )
            events.append(event)
            result = apply_mission_cycle_event_persisted(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                event=event,
            )
            assert result["status"] == "APPLIED"
            state = result["result_state"]

        assert state["current_phase"] == "replan"
        assert state["cycle_index"] == 1
        assert state["completed_cycles"] == 1
        assert state["cycle_summaries"][0]["verification_verdict"] == "failed"
        assert state["cycle_summaries"][0]["cycle_cost"] == 1.0

        recovered = recover_mission_cycle_store(
            store_dir=directory, contract=contract
        )
        assert recovered == state
        replay = apply_mission_cycle_event_persisted(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            event=events[-1],
        )
        assert replay["status"] == "REPLAYED"

        snapshot_path = Path(directory) / "snapshot.json"
        snapshot_path.write_text("{}\n", encoding="utf-8")
        try:
            recover_mission_cycle_store(store_dir=directory, contract=contract)
            raise AssertionError("snapshot mismatch must fail closed")
        except ValueError as exc:
            assert "snapshot_ledger_mismatch" in str(exc)
        repaired = recover_mission_cycle_store(
            store_dir=directory, contract=contract, repair_snapshot=True
        )
        assert repaired == state

        next_plan = build_mission_cycle_event(
            contract=contract,
            mission_state=mission_state,
            cycle_state=state,
            artifact_digest="artifact-plan-002",
            actor_id="agent-1",
            actor_role="worker",
            issued_at_ms=20,
        )
        next_result = apply_mission_cycle_event(
            contract=contract,
            mission_state=mission_state,
            cycle_state=state,
            event=next_plan,
        )
        assert next_result["result_state"]["current_phase"] == "plan"
        assert next_result["result_state"]["cycle_index"] == 1

        budget_state = next_result["result_state"]
        oversized = build_mission_cycle_event(
            contract=contract,
            mission_state=mission_state,
            cycle_state=budget_state,
            artifact_digest="oversized-action",
            actor_id="agent-1",
            actor_role="worker",
            issued_at_ms=22,
            cost=11.0,
            metadata=_phase_metadata("act"),
        )
        try:
            apply_mission_cycle_event(
                contract=contract,
                mission_state=mission_state,
                cycle_state=budget_state,
                event=oversized,
            )
            raise AssertionError("cycle budget overflow must fail")
        except ValueError as exc:
            assert "mission_cycle_budget_exceeded" in str(exc)

        ledger_lines = (Path(directory) / "cycle-ledger.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        assert len(ledger_lines) == 6
        for line in ledger_lines:
            assert isinstance(json.loads(line), dict)

    return {
        "status": "V021_AUTONOMOUS_MISSION_CYCLE_OK",
        "completed_cycles": state["completed_cycles"],
        "event_count": state["event_count"],
        "final_phase": state["current_phase"],
        "state_digest": state["mission_cycle_state_digest"],
    }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
