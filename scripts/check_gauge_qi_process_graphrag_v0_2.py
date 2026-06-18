from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.kuuos_gauge_qi_process_graphrag_bridge_v0_2 import (
    build_belief_evidence_packet,
    build_replan_adoption_receipt,
)
from runtime.kuuos_gauge_qi_process_graphrag_store_v0_2 import (
    GaugeQiGraphRAGStore,
    GaugeQiGraphRAGStoreError,
    apply_evidence_bundle,
    build_initial_graph_rag_state,
)
from runtime.v01_gauge_qi_process_graphrag import build_fixture
from runtime.v02_gauge_qi_process_graphrag import run_demo


def run_checks() -> dict:
    demo = run_demo()
    bundle = build_fixture()
    initial = build_initial_graph_rag_state(
        lineage_id="checks-lineage",
        query_id=bundle["query_id"],
        now_ms=0,
    )

    wrong_query = deepcopy(bundle)
    wrong_query["query_id"] = "another-query"
    rejected = apply_evidence_bundle(initial, wrong_query, now_ms=1)
    assert rejected["status"] == "REJECTED"
    assert rejected["errors"] == ["graph_rag_query_lineage_mismatch"]

    applied = apply_evidence_bundle(initial, bundle, now_ms=1)
    assert applied["status"] == "APPLIED"
    packet = build_belief_evidence_packet(state=applied["state"], now_ms=2)
    assert packet["candidate_for_belief_weighing"] is True
    assert packet["belief_authority_granted"] is False
    assert packet["truth_authority_granted"] is False
    assert packet["future_only"] is True
    assert packet["memory_overwrite"] is False

    try:
        build_replan_adoption_receipt(
            state=applied["state"],
            belief_state_digest="belief-state-check",
            belief_commit_receipt_digest="belief-commit-check",
            belief_route="HOLD",
            mission_cycle_phase="replan",
            mission_cycle_state_digest="cycle-state-check",
            replan_receipt_digest="replan-check",
            next_plan_basis_digest="basis-check",
            now_ms=3,
        )
        raise AssertionError("non-candidate BeliefOS route must fail")
    except ValueError as exc:
        assert "belief_os_candidate_required" in str(exc)

    hold_bundle = deepcopy(bundle)
    hold_bundle["qi_process"]["history_window_digest"] = "hold-history-check"
    hold_bundle["qi_process"]["observation_debt_pressure"] = 0.95
    held = apply_evidence_bundle(applied["state"], hold_bundle, now_ms=4)
    assert held["status"] == "APPLIED"
    assert held["state"]["latest_route"] == "HOLD"
    try:
        build_replan_adoption_receipt(
            state=held["state"],
            belief_state_digest="belief-state-check",
            belief_commit_receipt_digest="belief-commit-check",
            belief_route="CANDIDATE",
            mission_cycle_phase="replan",
            mission_cycle_state_digest="cycle-state-check",
            replan_receipt_digest="replan-check",
            next_plan_basis_digest="basis-check",
            now_ms=5,
        )
        raise AssertionError("non-candidate GraphRAG route must fail")
    except ValueError as exc:
        assert "graph_rag_candidate_required" in str(exc)

    with TemporaryDirectory() as directory:
        store = GaugeQiGraphRAGStore(directory)
        store.initialize(initial)
        persisted = store.apply(bundle, now_ms=1)
        assert persisted["status"] == "APPLIED"
        ledger_path = Path(directory) / "graph-rag-ledger.jsonl"
        record = json.loads(ledger_path.read_text(encoding="utf-8"))
        record["persistent_receipt_digest"] = "tampered"
        ledger_path.write_text(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        try:
            store.recover()
            raise AssertionError("tampered ledger must fail closed")
        except GaugeQiGraphRAGStoreError as exc:
            assert "graph_rag_ledger_commit_digest_invalid" in str(exc)

    return {
        **demo,
        "query_lineage_rejection_checked": True,
        "belief_packet_non_authority_checked": True,
        "belief_candidate_gate_checked": True,
        "graph_candidate_gate_checked": True,
        "ledger_corruption_fail_closed_checked": True,
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), ensure_ascii=False, sort_keys=True))
