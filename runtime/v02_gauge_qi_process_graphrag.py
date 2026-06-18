from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_gauge_qi_process_graphrag_bridge_v0_2 import (
    build_belief_evidence_packet,
    build_replan_adoption_receipt,
)
from runtime.kuuos_gauge_qi_process_graphrag_store_v0_2 import (
    GaugeQiGraphRAGStore,
    GaugeQiGraphRAGStoreError,
    build_initial_graph_rag_state,
)
from runtime.v01_gauge_qi_process_graphrag import build_fixture


def run_demo() -> dict:
    bundle = build_fixture()
    with TemporaryDirectory() as directory:
        store = GaugeQiGraphRAGStore(directory)
        initial = build_initial_graph_rag_state(
            lineage_id="gauge-qi-graphrag-lineage-v02",
            query_id=bundle["query_id"],
            now_ms=0,
        )
        store.initialize(initial)

        first = store.apply(bundle, now_ms=1)
        assert first["status"] == "APPLIED"
        assert first["receipt"]["route"] == "CANDIDATE"
        assert first["state"]["event_count"] == 1

        replay = store.apply(bundle, now_ms=2)
        assert replay["status"] == "REPLAYED"
        assert replay["state"] == first["state"]
        ledger_lines = (Path(directory) / "graph-rag-ledger.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        assert len(ledger_lines) == 1

        recovered = store.recover()
        assert recovered == first["state"]

        belief_packet = build_belief_evidence_packet(
            state=recovered, now_ms=3
        )
        assert belief_packet["candidate_for_belief_weighing"] is True
        assert belief_packet["belief_authority_granted"] is False
        assert belief_packet["truth_authority_granted"] is False

        try:
            build_replan_adoption_receipt(
                state=recovered,
                belief_state_digest="belief-state-001",
                belief_commit_receipt_digest="belief-commit-001",
                belief_route="CANDIDATE",
                mission_cycle_phase="learn",
                mission_cycle_state_digest="mission-cycle-state-001",
                replan_receipt_digest="replan-receipt-001",
                next_plan_basis_digest="next-plan-basis-001",
                now_ms=4,
            )
            raise AssertionError("non-Replan adoption must fail")
        except ValueError as exc:
            assert "mission_replan_required" in str(exc)

        adoption = build_replan_adoption_receipt(
            state=recovered,
            belief_state_digest="belief-state-001",
            belief_commit_receipt_digest="belief-commit-001",
            belief_route="CANDIDATE",
            mission_cycle_phase="replan",
            mission_cycle_state_digest="mission-cycle-state-001",
            replan_receipt_digest="replan-receipt-001",
            next_plan_basis_digest="next-plan-basis-001",
            now_ms=4,
        )
        assert adoption["future_only"] is True
        assert adoption["memory_overwrite"] is False
        assert adoption["decision_commit_granted"] is False
        assert adoption["execution_authority_granted"] is False

        snapshot_path = Path(directory) / "graph-rag-snapshot.json"
        snapshot_path.write_text("{}\n", encoding="utf-8")
        try:
            store.recover()
            raise AssertionError("snapshot mismatch must fail closed")
        except GaugeQiGraphRAGStoreError as exc:
            assert "graph_rag_snapshot_ledger_mismatch" in str(exc)
        repaired = store.recover(repair_snapshot=True)
        assert repaired == recovered

        hold_bundle = deepcopy(bundle)
        hold_bundle["qi_process"]["history_window_digest"] = (
            "qi-history-window-high-debt"
        )
        hold_bundle["qi_process"]["observation_debt_pressure"] = 0.90
        second = store.apply(hold_bundle, now_ms=5)
        assert second["status"] == "APPLIED"
        assert second["receipt"]["route"] == "HOLD"
        assert second["state"]["event_count"] == 2
        assert second["state"]["evidence_chain_digest"] != recovered[
            "evidence_chain_digest"
        ]
        assert second["state"]["holonomy_chain_digest"] != recovered[
            "holonomy_chain_digest"
        ]
        assert second["state"]["observation_debt_chain_digest"] != recovered[
            "observation_debt_chain_digest"
        ]

        final_state = store.recover()
        assert final_state == second["state"]

    return {
        "status": "GAUGE_QI_PROCESS_GRAPHRAG_V0_2_OK",
        "event_count": final_state["event_count"],
        "latest_route": final_state["latest_route"],
        "belief_evidence_packet_digest": belief_packet[
            "belief_evidence_packet_digest"
        ],
        "replan_adoption_receipt_digest": adoption[
            "replan_adoption_receipt_digest"
        ],
        "evidence_chain_digest": final_state["evidence_chain_digest"],
        "holonomy_chain_digest": final_state["holonomy_chain_digest"],
        "observation_debt_chain_digest": final_state[
            "observation_debt_chain_digest"
        ],
        "restart_recovery_checked": True,
        "idempotent_replay_checked": True,
        "snapshot_repair_checked": True,
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), ensure_ascii=False, sort_keys=True))
