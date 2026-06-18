from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_context_transport_types_v0_2 import (
    RECEIPT_VERSION as TRANSPORT_RECEIPT_VERSION,
    copy_non_authority as transport_non_authority,
    receipt_digest as transport_receipt_digest,
)
from runtime.kuuos_belief_os_gerbe_coherence_v0_3 import (
    build_gerbe_packet,
    build_replan_gerbe_activation_receipt,
)
from runtime.kuuos_belief_os_gerbe_store_v0_3 import (
    BeliefGerbeStore,
    BeliefGerbeStoreError,
    build_initial_gerbe_state,
)
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_context_gerbe_coherence_types_v0_14 import (
    DECISION_VERSION as GERBE_DECISION_VERSION,
    decision_digest as gerbe_decision_digest,
)


def _transport_receipt(
    *,
    packet_id: str,
    lineage_id: str,
    source_context_id: str,
    target_context_id: str,
    source_state_digest: str,
    declared_path: Sequence[str],
    lower: float,
    upper: float,
    overlap: float,
    reliability: float,
    qi_history_compatibility: float,
    evidence_label: str,
    counterevidence_label: str,
    created_at_ms: int,
) -> dict[str, Any]:
    transition_digest = sha(
        {
            "source_context_id": source_context_id,
            "target_context_id": target_context_id,
            "declared_path": list(declared_path),
            "packet_id": packet_id,
        }
    )
    evidence_digest = sha(evidence_label)
    counterevidence_digest = sha(counterevidence_label)
    section = {
        "source_belief_id": "belief-" + source_context_id,
        "source_context_id": source_context_id,
        "source_belief_state_digest": source_state_digest,
        "source_committed_belief_digest": sha(
            {"source_state_digest": source_state_digest, "committed": True}
        ),
        "source_route": "CANDIDATE",
        "source_interval": {
            "lower_probability": min(1.0, lower + 0.02),
            "upper_probability": max(0.0, upper - 0.02),
        },
        "transport_reliability": reliability,
        "transported_interval": {
            "lower_probability": lower,
            "upper_probability": upper,
            "ignorance_width": upper - lower,
        },
        "declared_path": list(declared_path),
        "overlap": overlap,
        "curvature": 0.02,
        "cocycle_defect": 0.01,
        "holonomy_residual": 0.01,
        "qi_history_compatibility": qi_history_compatibility,
        "atlas_transition_digest": transition_digest,
        "atlas_receipt_digest": sha("atlas-receipt-" + packet_id),
        "evidence_digests": [evidence_digest],
        "counterevidence_digests": [counterevidence_digest],
    }
    receipt = {
        "version": TRANSPORT_RECEIPT_VERSION,
        "packet_id": packet_id,
        "lineage_id": lineage_id,
        "belief_transport_packet_digest": sha("transport-packet-" + packet_id),
        "target_context_id": target_context_id,
        "target_context_signature_digest": sha(
            "target-signature-" + target_context_id
        ),
        "atlas_bundle_digest": sha("atlas-bundle-" + target_context_id),
        "transported_sections": [section],
        "plurality_count": 1,
        "aggregate_interval": {
            "lower_probability": lower,
            "upper_probability": upper,
            "ignorance_width": upper - lower,
        },
        "conflict_index": 0.0,
        "aggregate_curvature": 0.02,
        "aggregate_cocycle_defect": 0.01,
        "aggregate_holonomy_residual": 0.01,
        "qi_history_residual": 1.0 - qi_history_compatibility,
        "evidence_digests": [evidence_digest],
        "counterevidence_digests": [counterevidence_digest],
        "route": "CANDIDATE",
        "reasoning_license": True,
        "planning_support_license": True,
        "next_revision_basis_digest": sha("basis-" + packet_id),
        "pending_replan_activation": True,
        "locality_preserved": True,
        "plurality_preserved": True,
        "paramartha_non_reified": True,
        "two_truths_separated": True,
        "curvature_is_not_veto": True,
        "cocycle_defect_is_not_prohibition": True,
        "holonomy_is_not_authority": True,
        "path_search_used": False,
        "global_chart_ranking_used": False,
        "universal_winner_selected": False,
        "future_only": True,
        "memory_overwrite": False,
        "non_authority": transport_non_authority(),
        "created_at_ms": created_at_ms,
        "belief_transport_receipt_digest": "",
    }
    receipt["belief_transport_receipt_digest"] = transport_receipt_digest(receipt)
    return receipt


def _gerbe_decision(
    *,
    target_context_id: str,
    two_curvature: float,
    higher_defect: float,
    suffix: str,
) -> dict[str, Any]:
    decision = {
        "version": GERBE_DECISION_VERSION,
        "gerbe_run_id": "gerbe-run-" + suffix,
        "cycle_index": 1,
        "target_context_key": target_context_id,
        "target_context_signature": {"digest": sha(target_context_id)},
        "source_atlas_bundle_digest": sha("source-atlas-bundle-" + suffix),
        "source_atlas_decision_digest": sha(
            "source-atlas-decision-" + suffix
        ),
        "source_atlas_class": "plural_atlas",
        "gerbe_class": (
            "coherent_gerbe_transport"
            if max(two_curvature, higher_defect) < 0.1
            else "plural_gerbe_transport"
        ),
        "compatible_chart_count": 4,
        "two_cell_count": 3,
        "quadruple_witness_count": 1,
        "two_cells": [],
        "quadruple_witnesses": [],
        "gerbe_two_curvature": two_curvature,
        "higher_cocycle_defect": higher_defect,
        "lifted_base_short_horizon_weight": 0.4,
        "lifted_base_medium_horizon_weight": 0.35,
        "lifted_base_long_horizon_weight": 0.25,
        "lifted_weight_sum": 1.0,
        "v0_13_decision_is_the_only_pairwise_transport_source": True,
        "two_cell_residue_is_not_a_veto": True,
        "higher_cocycle_defect_is_not_a_veto": True,
        "global_trivialization_forbidden": True,
        "v0_13_authority_preserved": True,
        "surface_holonomy_append_only": True,
        "gerbe_decision_digest": "",
    }
    decision["gerbe_decision_digest"] = gerbe_decision_digest(decision)
    return decision


def _packet(
    *,
    packet_id: str,
    lineage_id: str,
    target_context_id: str,
    receipts: Sequence[Mapping[str, Any]],
    gerbe_decision: Mapping[str, Any],
    created_at_ms: int,
) -> dict[str, Any]:
    return build_gerbe_packet(
        packet_id=packet_id,
        lineage_id=lineage_id,
        target_context_id=target_context_id,
        source_transport_receipts=receipts,
        source_gerbe_decision=gerbe_decision,
        candidate_max_width=0.40,
        observe_max_width=0.75,
        candidate_max_two_cell_residue=0.05,
        candidate_max_higher_defect=0.06,
        hold_min_defect=0.40,
        minimum_triple_overlap=0.50,
        minimum_quadruple_overlap=0.50,
        created_at_ms=created_at_ms,
    )


def run_kernel() -> dict[str, Any]:
    lineage_id = "belief-gerbe-lineage-001"
    target_context_id = "context-target"
    source_state_a = sha("belief-source-state-a")
    source_state_d = sha("belief-source-state-d")

    receipts = [
        _transport_receipt(
            packet_id="transport-direct-a",
            lineage_id=lineage_id,
            source_context_id="context-a",
            target_context_id=target_context_id,
            source_state_digest=source_state_a,
            declared_path=["context-a", target_context_id],
            lower=0.58,
            upper=0.78,
            overlap=0.94,
            reliability=0.88,
            qi_history_compatibility=0.95,
            evidence_label="evidence-direct-a",
            counterevidence_label="counter-direct-a",
            created_at_ms=4_100,
        ),
        _transport_receipt(
            packet_id="transport-via-b",
            lineage_id=lineage_id,
            source_context_id="context-a",
            target_context_id=target_context_id,
            source_state_digest=source_state_a,
            declared_path=["context-a", "context-b", target_context_id],
            lower=0.56,
            upper=0.80,
            overlap=0.91,
            reliability=0.85,
            qi_history_compatibility=0.92,
            evidence_label="evidence-via-b",
            counterevidence_label="counter-via-b",
            created_at_ms=4_110,
        ),
        _transport_receipt(
            packet_id="transport-via-c",
            lineage_id=lineage_id,
            source_context_id="context-a",
            target_context_id=target_context_id,
            source_state_digest=source_state_a,
            declared_path=["context-a", "context-c", target_context_id],
            lower=0.57,
            upper=0.79,
            overlap=0.90,
            reliability=0.84,
            qi_history_compatibility=0.91,
            evidence_label="evidence-via-c",
            counterevidence_label="counter-via-c",
            created_at_ms=4_120,
        ),
        _transport_receipt(
            packet_id="transport-direct-d",
            lineage_id=lineage_id,
            source_context_id="context-d",
            target_context_id=target_context_id,
            source_state_digest=source_state_d,
            declared_path=["context-d", target_context_id],
            lower=0.54,
            upper=0.77,
            overlap=0.89,
            reliability=0.83,
            qi_history_compatibility=0.90,
            evidence_label="evidence-direct-d",
            counterevidence_label="counter-direct-d",
            created_at_ms=4_130,
        ),
    ]

    candidate_packet = _packet(
        packet_id="belief-gerbe-packet-001",
        lineage_id=lineage_id,
        target_context_id=target_context_id,
        receipts=receipts,
        gerbe_decision=_gerbe_decision(
            target_context_id=target_context_id,
            two_curvature=0.03,
            higher_defect=0.02,
            suffix="candidate",
        ),
        created_at_ms=5_000,
    )

    with tempfile.TemporaryDirectory(prefix="kuuos-belief-gerbe-v03-") as tmp:
        store = BeliefGerbeStore(Path(tmp))
        store.initialize(
            build_initial_gerbe_state(lineage_id=lineage_id, now_ms=4_000)
        )

        invalid_packet = deepcopy(candidate_packet)
        invalid_packet["global_trivialization_used"] = True
        invalid_result = store.apply(invalid_packet)
        assert invalid_result["status"] == "REJECTED"
        assert store.ledger_commit_count() == 0

        tampered_packet = deepcopy(candidate_packet)
        tampered_packet["source_transport_receipts"][0][
            "belief_transport_receipt_digest"
        ] = "tampered"
        tampered_result = store.apply(tampered_packet)
        assert tampered_result["status"] == "REJECTED"
        assert store.ledger_commit_count() == 0

        applied = store.apply(candidate_packet)
        assert applied["status"] == "APPLIED"
        receipt = applied["receipt"]
        assert receipt["route"] == "CANDIDATE"
        assert receipt["path_count"] == 4
        assert receipt["two_cell_count"] == 3
        assert receipt["higher_witness_count"] == 1
        assert len(receipt["counterevidence_digests"]) == 4
        assert receipt["global_trivialization_used"] is False
        assert receipt["two_cell_residue_is_not_veto"] is True
        assert receipt["higher_defect_is_not_prohibition"] is True
        assert (
            receipt["coherent_interval"]["lower_probability"]
            <= receipt["path_hull_interval"]["lower_probability"] + 1e-12
        )
        assert (
            receipt["coherent_interval"]["upper_probability"] + 1e-12
            >= receipt["path_hull_interval"]["upper_probability"]
        )

        before_replay = store.ledger_commit_count()
        replay = store.apply(candidate_packet)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_replay

        stale_packet = _packet(
            packet_id="belief-gerbe-packet-stale",
            lineage_id=lineage_id,
            target_context_id=target_context_id,
            receipts=receipts,
            gerbe_decision=_gerbe_decision(
                target_context_id=target_context_id,
                two_curvature=0.02,
                higher_defect=0.01,
                suffix="stale",
            ),
            created_at_ms=4_900,
        )
        stale = store.apply(stale_packet)
        assert stale["status"] == "REJECTED"
        assert "gerbe_packet_time_regression" in stale["errors"]

        high_defect_packet = _packet(
            packet_id="belief-gerbe-packet-002",
            lineage_id=lineage_id,
            target_context_id=target_context_id,
            receipts=receipts,
            gerbe_decision=_gerbe_decision(
                target_context_id=target_context_id,
                two_curvature=0.65,
                higher_defect=0.55,
                suffix="high-defect",
            ),
            created_at_ms=5_100,
        )
        high_defect = store.apply(high_defect_packet)
        assert high_defect["status"] == "APPLIED"
        assert high_defect["receipt"]["route"] == "HOLD"
        assert high_defect["receipt"]["route"] not in {"REJECT", "QUARANTINE"}
        assert high_defect["receipt"]["two_cell_residue_is_not_veto"] is True
        assert high_defect["receipt"]["higher_defect_is_not_prohibition"] is True

        try:
            build_replan_gerbe_activation_receipt(
                gerbe_receipt=receipt,
                mission_cycle_phase="learn",
                mission_cycle_state_digest=sha("mission-state"),
                replan_receipt_digest=sha("replan-receipt"),
                next_plan_basis_digest=sha("next-plan-basis"),
                now_ms=5_200,
            )
        except ValueError as exc:
            assert str(exc) == "mission_replan_required"
        else:
            raise AssertionError("gerbe_activation_without_replan_was_accepted")

        activation = build_replan_gerbe_activation_receipt(
            gerbe_receipt=receipt,
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("mission-state"),
            replan_receipt_digest=sha("replan-receipt"),
            next_plan_basis_digest=sha("next-plan-basis"),
            now_ms=5_201,
        )
        assert activation["future_only"] is True
        assert activation["memory_overwrite"] is False

        snapshot_path = Path(tmp) / "belief-gerbe-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except BeliefGerbeStoreError as exc:
            assert str(exc) == "gerbe_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_gerbe_snapshot_was_accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["belief_gerbe_state_digest"] == recovered[
            "belief_gerbe_state_digest"
        ]
        assert recovered["event_count"] == 2
        assert recovered["run_count"] == 2

        return {
            "status": "BELIEF_OS_CONTEXT_GERBE_COHERENCE_V0_3_OK",
            "candidate_receipt_digest": receipt["belief_gerbe_receipt_digest"],
            "activation_receipt_digest": activation[
                "belief_gerbe_activation_receipt_digest"
            ],
            "gerbe_state_digest": recovered["belief_gerbe_state_digest"],
            "surface_holonomy_chain_digest": recovered[
                "surface_holonomy_chain_digest"
            ],
            "ledger_commits": store.ledger_commit_count(),
            "candidate_route": receipt["route"],
            "high_defect_route": high_defect["receipt"]["route"],
            "path_count": receipt["path_count"],
            "two_cell_count": receipt["two_cell_count"],
            "higher_witness_count": receipt["higher_witness_count"],
            "counterevidence_count": len(receipt["counterevidence_digests"]),
            "coherent_interval": receipt["coherent_interval"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
