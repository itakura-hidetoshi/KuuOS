from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_kernel_v0_1 import (
    build_belief_event,
    build_initial_belief_state,
    build_replan_activation_receipt,
)
from runtime.kuuos_belief_os_store_v0_1 import BeliefStore, BeliefStoreError
from runtime.kuuos_belief_os_types_v0_1 import copy_non_authority, sha


def _event(
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_belief_event(
        state=state,
        target_phase=target_phase,
        artifact_digest=sha(
            {
                "target_phase": target_phase,
                "payload": dict(payload),
                "tick": tick,
            }
        ),
        payload=payload,
        now_ms=1_000 + tick,
    )


def _apply(
    store: BeliefStore,
    state: Mapping[str, Any],
    target: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(_event(state, target, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def run_kernel() -> dict[str, Any]:
    initial = build_initial_belief_state(
        belief_id="belief-demo-001",
        lineage_id="lineage-demo-001",
        claim="The observed change is conditionally compatible with recovery.",
        claim_digest=sha("demo-claim"),
        hypothesis_space_digest=sha(["recovery", "stable", "deterioration"]),
        source_memory_digest=sha("memory-lineage-demo"),
        now_ms=1_000,
    )

    with tempfile.TemporaryDirectory(prefix="kuuos-belief-v01-") as tmp:
        store = BeliefStore(Path(tmp))
        state = store.initialize(initial)

        skip_event = _event(
            state,
            "trace",
            {"evidence_digests": [sha("invalid-skip")]},
            1,
        )
        skipped = store.apply(skip_event)
        assert skipped["status"] == "REJECTED"
        assert "event_phase_order_invalid" in skipped["errors"]
        assert store.ledger_commit_count() == 0

        state = _apply(
            store,
            state,
            "contextualize",
            {
                "context": {
                    "context_id": "clinical-observation-chart",
                    "observer_id": "observer-demo",
                    "observer_role": "responsible-reviewer",
                    "temporal_scope": "current-cycle",
                    "scale": "individual-local",
                    "task_scope": "conditional-reasoning",
                    "world_model_id": "plural-world-demo",
                }
            },
            2,
        )
        first_applied_event = state["event_history"][-1]["belief_event_digest"]

        state = _apply(
            store,
            state,
            "trace",
            {
                "evidence_digests": [sha("evidence-1")],
                "observation_digests": [sha("observation-1")],
                "verification_receipt_digests": [sha("verification-1")],
                "causal_support_digests": [],
            },
            3,
        )
        state = _apply(
            store,
            state,
            "weigh",
            {
                "credal_state": {
                    "lower_probability": 0.58,
                    "upper_probability": 0.84,
                    "central_estimate": 0.71,
                    "conflict_index": 0.14,
                },
                "uncertainty": {
                    "epistemic": 0.24,
                    "aleatory": 0.18,
                    "contextual": 0.22,
                    "temporal": 0.28,
                    "model": 0.31,
                    "observer": 0.20,
                    "process_history": 0.26,
                },
            },
            4,
        )
        state = _apply(
            store,
            state,
            "challenge",
            {
                "counterevidence_digests": [sha("counterevidence-1")],
                "contradiction_digests": [],
                "alternative_hypothesis_digests": [sha("alternative-stable")],
                "unresolved_residual_digests": [sha("context-residual-1")],
            },
            5,
        )

        forbidden_qi_event = _event(
            state,
            "qi_condition",
            {
                "process_tensor_digest": sha("qi-process"),
                "history_window_digest": sha("qi-history"),
                "roles": ["direct_execution_license"],
                "flow_phase": "recovery-transition",
                "authority_source": False,
            },
            6,
        )
        forbidden_qi = store.apply(forbidden_qi_event)
        assert forbidden_qi["status"] == "REJECTED"
        assert "qi_forbidden_role" in forbidden_qi["errors"]

        state = _apply(
            store,
            state,
            "qi_condition",
            {
                "process_tensor_digest": sha("qi-process"),
                "history_window_digest": sha("qi-history"),
                "roles": [
                    "likelihood_context_modifier",
                    "recovery_trajectory_signal",
                ],
                "flow_phase": "recovery-transition",
                "authority_source": False,
            },
            7,
        )
        state = _apply(
            store,
            state,
            "two_truths_check",
            {
                "two_truths": {
                    "samvrti_operationally_usable": True,
                    "paramartha_non_reified": True,
                    "two_truths_separated": True,
                }
            },
            8,
        )
        state = _apply(
            store,
            state,
            "middle_way_gate",
            {
                "middle_way": {
                    "reification_risk": 0.18,
                    "nihilistic_erasure_risk": 0.12,
                    "premature_closure_risk": 0.24,
                    "responsibility_abandonment_risk": 0.08,
                    "repairability": 0.92,
                },
                "route": "CANDIDATE",
                "reasoning_license": True,
                "planning_support_license": True,
            },
            9,
        )
        commit_event = _event(
            state,
            "commit",
            {
                "future_only": True,
                "memory_overwrite": False,
                "activation_boundary": "mission_replan_only",
                "non_authority": copy_non_authority(),
            },
            10,
        )
        commit_result = store.apply(commit_event)
        assert commit_result["status"] == "APPLIED"
        state = commit_result["state"]
        assert state["belief_version"] == 1
        assert state["completed_revisions"] == 1
        assert state["pending_replan_activation"] is True
        assert state["counterevidence_digests"] == [sha("counterevidence-1")]

        commits_before_replay = store.ledger_commit_count()
        replay = store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == commits_before_replay

        stale_event = dict(commit_event)
        stale_event["belief_event_digest"] = "stale-nonmatching-digest"
        stale = store.apply(stale_event)
        assert stale["status"] == "REJECTED"

        try:
            build_replan_activation_receipt(
                state=state,
                mission_cycle_phase="learn",
                mission_cycle_state_digest=sha("mission-state"),
                replan_receipt_digest=sha("replan-receipt"),
                next_plan_basis_digest=sha("next-plan-basis"),
                now_ms=2_000,
            )
        except ValueError as exc:
            assert str(exc) == "mission_replan_required"
        else:
            raise AssertionError("activation_without_replan_was_accepted")

        activation = build_replan_activation_receipt(
            state=state,
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("mission-state"),
            replan_receipt_digest=sha("replan-receipt"),
            next_plan_basis_digest=sha("next-plan-basis"),
            now_ms=2_001,
        )
        assert activation["future_only"] is True
        assert activation["memory_overwrite"] is False
        assert activation["non_authority"] == copy_non_authority()

        snapshot_path = Path(tmp) / "belief-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except BeliefStoreError as exc:
            assert str(exc) == "snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_snapshot_was_accepted")
        repaired = store.repair_snapshot()
        assert repaired["belief_state_digest"] == state["belief_state_digest"]
        recovered = store.recover(require_snapshot_match=True)
        assert recovered["belief_state_digest"] == state["belief_state_digest"]

        return {
            "status": "BELIEF_OS_V0_1_OK",
            "belief_state_digest": state["belief_state_digest"],
            "activation_receipt_digest": activation[
                "belief_activation_receipt_digest"
            ],
            "committed_versions": state["belief_version"],
            "ledger_commits": store.ledger_commit_count(),
            "first_applied_event_digest": first_applied_event,
            "route": state["route"],
            "credal_interval": [
                state["credal_state"]["lower_probability"],
                state["credal_state"]["upper_probability"],
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
