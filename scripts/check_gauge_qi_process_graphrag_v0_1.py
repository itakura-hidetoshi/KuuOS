from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.v01_gauge_qi_process_graphrag import build_fixture, run_demo
from runtime.kuuos_gauge_qi_process_graphrag_v0_1 import evaluate_evidence_bundle


def run_checks() -> dict:
    result = run_demo()

    quarantined = build_fixture()
    quarantined["boundary"]["global_truth_granted"] = True
    quarantine_receipt = evaluate_evidence_bundle(quarantined)
    assert quarantine_receipt["route"] == "QUARANTINE"

    repair = build_fixture()
    repair["patches"][0]["provenance_completeness"] = 0.20
    repair_receipt = evaluate_evidence_bundle(repair)
    assert repair_receipt["route"] == "REPAIR"

    hold = build_fixture()
    hold["qi_process"]["observation_debt_pressure"] = 0.90
    hold_receipt = evaluate_evidence_bundle(hold)
    assert hold_receipt["route"] == "HOLD"

    malformed = build_fixture()
    malformed["declared_paths"][0]["connection_sequence"] = ["connection-ac"]
    try:
        evaluate_evidence_bundle(malformed)
        raise AssertionError("misaligned declared path must fail closed")
    except ValueError as exc:
        assert "path_path-mediated_connection_sequence_invalid" in str(exc)

    return {
        **result,
        "quarantine_boundary_checked": True,
        "repair_route_checked": True,
        "hold_route_checked": True,
        "malformed_path_fail_closed_checked": True,
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), ensure_ascii=False, sort_keys=True))
