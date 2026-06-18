from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_context_transport_store_v0_2 import (
    BeliefTransportStore,
    BeliefTransportStoreError,
    build_initial_transport_state,
)
from runtime.kuuos_belief_os_context_transport_v0_2 import (
    build_atlas_transition,
    build_replan_transport_activation_receipt,
    build_transport_packet,
)
from runtime.kuuos_belief_os_kernel_v0_1 import (
    apply_belief_event,
    build_belief_event,
    build_initial_belief_state,
)
from runtime.kuuos_belief_os_types_v0_1 import copy_non_authority as belief_non_authority
from runtime.kuuos_belief_os_types_v0_1 import sha


def _advance(
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    event = build_belief_event(
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
    result = apply_belief_event(state, event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _committed_belief(
    *,
    belief_id: str,
    lineage_id: str,
    context_id: str,
    lower: float,
    upper: float,
    evidence_label: str,
    counterevidence_label: str,
    qi_label: str,
    tick_base: int,
) -> dict[str, Any]:
    state = build_initial_belief_state(
        belief_id=belief_id,
        lineage_id=lineage_id,
        claim="The observed trajectory is conditionally compatible with recovery.",
        claim_digest=sha({"belief_id": belief_id, "claim": "conditional-recovery"}),
        hypothesis_space_digest=sha(["recovery", "stable", "deterioration"]),
        source_memory_digest=sha({"belief_id": belief_id, "memory": "lineage"}),
        now_ms=1_000 + tick_base,
    )
    state = _advance(
        state,
        "contextualize",
        {
            "context": {
                "context_id": context_id,
                "observer_id": "observer-" + context_id,
                "observer_role": "responsible-reviewer",
                "temporal_scope": "current-cycle",
                "scale": "local",
                "task_scope": "conditional-belief-transport",
                "world_model_id": "plural-world-model",
            }
        },
        tick_base + 1,
    )
    state = _advance(
        state,
        "trace",
        {
            "evidence_digests": [sha(evidence_label)],
            "observation_digests": [sha("observation-" + evidence_label)],
            "verification_receipt_digests": [sha("verification-" + evidence_label)],
            "causal_support_digests": [],
        },
        tick_base + 2,
    )
    state = _advance(
        state,
        "weigh",
        {
            "credal_state": {
                "lower_probability": lower,
                "upper_probability": upper,
                "central_estimate": (lower + upper) / 2.0,
                "conflict_index": 0.1,
            },
            "uncertainty": {
                "epistemic": 0.22,
                "aleatory": 0.16,
                "contextual": 0.24,
                "temporal": 0.20,
                "model": 0.26,
                "observer": 0.18,
                "process_history": 0.21,
            },
        },
        tick_base + 3,
    )
    state = _advance(
        state,
        "challenge",
        {
            "counterevidence_digests": [sha(counterevidence_label)],
            "contradiction_digests": [],
            "alternative_hypothesis_digests": [
                sha("alternative-" + counterevidence_label)
            ],
            "unresolved_residual_digests": [
                sha("residual-" + counterevidence_label)
            ],
        },
        tick_base + 4,
    )
    state = _advance(
        state,
        "qi_condition",
        {
            "process_tensor_digest": sha("qi-process-" + qi_label),
            "history_window_digest": sha("qi-history-" + qi_label),
            "roles": [
                "likelihood_context_modifier",
                "context_transport_support",
            ],
            "flow_phase": "recovery-transition",
            "authority_source": False,
        },
        tick_base + 5,
    )
    state = _advance(
        state,
        "two_truths_check",
        {
            "two_truths": {
                "samvrti_operationally_usable": True,
                "paramartha_non_reified": True,
                "two_truths_separated": True,
            }
        },
        tick_base + 6,
    )
    state = _advance(
        state,
        "middle_way_gate",
        {
            "middle_way": {
                "reification_risk": 0.14,
                "nihilistic_erasure_risk": 0.10,
                "premature_closure_risk": 0.18,
                "responsibility_abandonment_risk": 0.08,
                "repairability": 0.94,
            },
            "route": "CANDIDATE",
            "reasoning_license": True,
            "planning_support_license": True,
        },
        tick_base + 7,
    )
    state = _advance(
        state,
        "commit",
        {
            "future_only": True,
            "memory_overwrite": False,
            "activation_boundary": "mission_replan_only",
            "non_authority": belief_non_authority(),
        },
        tick_base + 8,
    )
    return state


def run_kernel() -> dict[str, Any]:
    lineage_id = "belief-transport-lineage-001"
    source_a = _committed_belief(
        belief_id="belief-chart-a",
        lineage_id=lineage_id,
        context_id="context-a",
        lower=0.62,
        upper=0.78,
        evidence_label="evidence-a",
        counterevidence_label="counter-a",
        qi_label="a",
        tick_base=0,
    )
    source_b = _committed_belief(
        belief_id="belief-chart-b",
        lineage_id=lineage_id,
        context_id="context-b",
        lower=0.56,
        upper=0.74,
        evidence_label="evidence-b",
        counterevidence_label="counter-b",
        qi_label="b",
        tick_base=20,
    )

    transition_a = build_atlas_transition(
        source_context_id="context-a",
        target_context_id="context-target",
        declared_path=["context-a", "context-target"],
        overlap=0.92,
        curvature=0.04,
        cocycle_defect=0.03,
        holonomy_residual=0.02,
        qi_history_compatibility=0.95,
        atlas_receipt_digest=sha("atlas-transition-a"),
    )
    transition_b = build_atlas_transition(
        source_context_id="context-b",
        target_context_id="context-target",
        declared_path=["context-b", "context-bridge", "context-target"],
        overlap=0.88,
        curvature=0.05,
        cocycle_defect=0.02,
        holonomy_residual=0.03,
        qi_history_compatibility=0.90,
        atlas_receipt_digest=sha("atlas-transition-b"),
    )

    packet = build_transport_packet(
        packet_id="belief-transport-packet-001",
        lineage_id=lineage_id,
        target_context_id="context-target",
        target_context_signature_digest=sha("context-target-signature"),
        atlas_bundle_digest=sha("context-atlas-bundle"),
        source_belief_states=[source_a, source_b],
        transitions=[transition_a, transition_b],
        candidate_max_width=0.50,
        observe_max_width=0.80,
        candidate_max_conflict=0.12,
        created_at_ms=5_000,
    )

    with tempfile.TemporaryDirectory(prefix="kuuos-belief-transport-v02-") as tmp:
        store = BeliefTransportStore(Path(tmp))
        state = store.initialize(
            build_initial_transport_state(lineage_id=lineage_id, now_ms=4_000)
        )

        invalid_packet = dict(packet)
        invalid_packet["path_search_used"] = True
        invalid = store.apply(invalid_packet)
        assert invalid["status"] == "REJECTED"
        assert store.ledger_commit_count() == 0

        result = store.apply(packet)
        assert result["status"] == "APPLIED"
        receipt = result["receipt"]
        state = result["state"]
        assert receipt["route"] == "CANDIDATE"
        assert receipt["plurality_count"] == 2
        assert receipt["locality_preserved"] is True
        assert receipt["plurality_preserved"] is True
        assert len(receipt["counterevidence_digests"]) == 2
        assert receipt["path_search_used"] is False
        assert receipt["global_chart_ranking_used"] is False
        assert receipt["universal_winner_selected"] is False

        for section in receipt["transported_sections"]:
            source_interval = section["source_interval"]
            transported_interval = section["transported_interval"]
            assert (
                transported_interval["lower_probability"]
                <= source_interval["lower_probability"] + 1e-12
            )
            assert (
                transported_interval["upper_probability"] + 1e-12
                >= source_interval["upper_probability"]
            )

        direct_lower = min(
            section["transported_interval"]["lower_probability"]
            for section in receipt["transported_sections"]
        )
        direct_upper = max(
            section["transported_interval"]["upper_probability"]
            for section in receipt["transported_sections"]
        )
        assert abs(receipt["aggregate_interval"]["lower_probability"] - direct_lower) < 1e-12
        assert abs(receipt["aggregate_interval"]["upper_probability"] - direct_upper) < 1e-12

        before_replay = store.ledger_commit_count()
        replay = store.apply(packet)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_replay

        high_curvature_a = build_atlas_transition(
            source_context_id="context-a",
            target_context_id="context-target",
            declared_path=["context-a", "context-target"],
            overlap=0.92,
            curvature=0.90,
            cocycle_defect=0.20,
            holonomy_residual=0.10,
            qi_history_compatibility=0.80,
            atlas_receipt_digest=sha("atlas-high-curvature-a"),
        )
        high_curvature_b = build_atlas_transition(
            source_context_id="context-b",
            target_context_id="context-target",
            declared_path=["context-b", "context-target"],
            overlap=0.88,
            curvature=0.85,
            cocycle_defect=0.18,
            holonomy_residual=0.12,
            qi_history_compatibility=0.78,
            atlas_receipt_digest=sha("atlas-high-curvature-b"),
        )
        high_curvature_packet = build_transport_packet(
            packet_id="belief-transport-packet-002",
            lineage_id=lineage_id,
            target_context_id="context-target",
            target_context_signature_digest=sha("context-target-signature"),
            atlas_bundle_digest=sha("context-atlas-bundle-high-curvature"),
            source_belief_states=[source_a, source_b],
            transitions=[high_curvature_a, high_curvature_b],
            candidate_max_width=0.50,
            observe_max_width=0.80,
            candidate_max_conflict=0.12,
            created_at_ms=5_100,
        )
        high_curvature = store.apply(high_curvature_packet)
        assert high_curvature["status"] == "APPLIED"
        assert high_curvature["receipt"]["route"] in {"OBSERVE", "REPAIR"}
        assert high_curvature["receipt"]["route"] not in {"REJECT", "QUARANTINE"}
        assert high_curvature["receipt"]["curvature_is_not_veto"] is True

        try:
            build_replan_transport_activation_receipt(
                transport_receipt=receipt,
                mission_cycle_phase="learn",
                mission_cycle_state_digest=sha("mission-cycle-state"),
                replan_receipt_digest=sha("replan-receipt"),
                next_plan_basis_digest=sha("next-plan-basis"),
                now_ms=5_200,
            )
        except ValueError as exc:
            assert str(exc) == "mission_replan_required"
        else:
            raise AssertionError("transport_activation_without_replan_was_accepted")

        activation = build_replan_transport_activation_receipt(
            transport_receipt=receipt,
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("mission-cycle-state"),
            replan_receipt_digest=sha("replan-receipt"),
            next_plan_basis_digest=sha("next-plan-basis"),
            now_ms=5_201,
        )
        assert activation["future_only"] is True
        assert activation["memory_overwrite"] is False

        snapshot_path = Path(tmp) / "belief-transport-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except BeliefTransportStoreError as exc:
            assert str(exc) == "transport_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_transport_snapshot_was_accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["belief_transport_state_digest"] == recovered[
            "belief_transport_state_digest"
        ]
        assert recovered["event_count"] == 2
        assert recovered["run_count"] == 2

        return {
            "status": "BELIEF_OS_CONTEXT_GAUGE_TRANSPORT_V0_2_OK",
            "candidate_transport_receipt_digest": receipt[
                "belief_transport_receipt_digest"
            ],
            "activation_receipt_digest": activation[
                "belief_transport_activation_receipt_digest"
            ],
            "transport_state_digest": recovered[
                "belief_transport_state_digest"
            ],
            "holonomy_chain_digest": recovered["holonomy_chain_digest"],
            "ledger_commits": store.ledger_commit_count(),
            "candidate_route": receipt["route"],
            "high_curvature_route": high_curvature["receipt"]["route"],
            "aggregate_interval": receipt["aggregate_interval"],
            "counterevidence_count": len(receipt["counterevidence_digests"]),
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
