from __future__ import annotations

import json
from math import cos, sin

from runtime.kuuos_gauge_qi_process_graphrag_v0_1 import (
    build_evidence_bundle,
    evaluate_evidence_bundle,
    gauge_transform_bundle,
)


def rotation(theta: float) -> list[list[float]]:
    return [[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]


def build_fixture() -> dict:
    x_a = [1.0, 0.0]
    x_b = [cos(0.20), sin(0.20)]
    x_c = [cos(0.50), sin(0.50)]
    patches = [
        {
            "patch_id": "patch-a",
            "context_id": "clinical-source-chart",
            "evidence_digest": "evidence-a",
            "source_digest": "source-a",
            "local_vector": x_a,
            "relevance": 0.94,
            "source_confidence": 0.92,
            "provenance_completeness": 0.95,
            "uncertainty": 0.12,
            "observed_at": 1,
            "rollback_ref": "rollback-a",
        },
        {
            "patch_id": "patch-b",
            "context_id": "ontology-bridge-chart",
            "evidence_digest": "evidence-b",
            "source_digest": "source-b",
            "local_vector": x_b,
            "relevance": 0.90,
            "source_confidence": 0.90,
            "provenance_completeness": 0.91,
            "uncertainty": 0.16,
            "observed_at": 2,
            "rollback_ref": "rollback-b",
        },
        {
            "patch_id": "patch-c",
            "context_id": "query-answer-chart",
            "evidence_digest": "evidence-c",
            "source_digest": "source-c",
            "local_vector": x_c,
            "relevance": 0.93,
            "source_confidence": 0.89,
            "provenance_completeness": 0.93,
            "uncertainty": 0.15,
            "observed_at": 3,
            "rollback_ref": "rollback-c",
        },
    ]
    connections = [
        {
            "connection_id": "connection-ab",
            "source_patch": "patch-a",
            "target_patch": "patch-b",
            "transport": rotation(0.20),
            "overlap": 0.95,
            "confidence": 0.94,
            "provenance_digest": "connection-evidence-ab",
        },
        {
            "connection_id": "connection-bc",
            "source_patch": "patch-b",
            "target_patch": "patch-c",
            "transport": rotation(0.30),
            "overlap": 0.94,
            "confidence": 0.93,
            "provenance_digest": "connection-evidence-bc",
        },
        {
            "connection_id": "connection-ac",
            "source_patch": "patch-a",
            "target_patch": "patch-c",
            "transport": rotation(0.52),
            "overlap": 0.92,
            "confidence": 0.91,
            "provenance_digest": "connection-evidence-ac",
        },
        {
            "connection_id": "connection-ca",
            "source_patch": "patch-c",
            "target_patch": "patch-a",
            "transport": rotation(-0.47),
            "overlap": 0.90,
            "confidence": 0.90,
            "provenance_digest": "connection-evidence-ca",
        },
    ]
    paths = [
        {
            "path_id": "path-mediated",
            "patch_sequence": ["patch-a", "patch-b", "patch-c"],
            "connection_sequence": ["connection-ab", "connection-bc"],
            "declared_by": "query-planner",
        },
        {
            "path_id": "path-direct",
            "patch_sequence": ["patch-a", "patch-c"],
            "connection_sequence": ["connection-ac"],
            "declared_by": "query-planner",
        },
    ]
    cycles = [
        {
            "cycle_id": "cycle-abc",
            "patch_sequence": ["patch-a", "patch-b", "patch-c", "patch-a"],
            "connection_sequence": ["connection-ab", "connection-bc", "connection-ca"],
        }
    ]
    qi_process = {
        "process_tensor_digest": "qi-process-tensor-fixture",
        "history_window_digest": "qi-history-window-fixture",
        "history_depth": 8,
        "transition_continuity": 0.94,
        "memory_continuity": 0.92,
        "nonmarkov_link_density": 0.84,
        "recoverability_branching_capacity": 0.90,
        "observation_debt_pressure": 0.12,
        "intervention_residue": 0.10,
    }
    return build_evidence_bundle(
        query_id="query-gauge-qi-001",
        query_text="Can two declared evidence paths support the same local answer without erasing path dependence?",
        patches=patches,
        connections=connections,
        declared_paths=paths,
        declared_cycles=cycles,
        qi_process=qi_process,
    )


def run_demo() -> dict:
    bundle = build_fixture()
    receipt = evaluate_evidence_bundle(bundle)
    gauges = {
        "patch-a": rotation(0.37),
        "patch-b": rotation(-0.23),
        "patch-c": rotation(0.61),
    }
    transformed_receipt = evaluate_evidence_bundle(gauge_transform_bundle(bundle, gauges))
    for original, transformed in zip(receipt["path_results"], transformed_receipt["path_results"], strict=True):
        assert abs(original["path_action"] - transformed["path_action"]) < 1e-12
        assert abs(original["alignment_residual"] - transformed["alignment_residual"]) < 1e-12
    assert abs(
        receipt["max_curvature_residual"] - transformed_receipt["max_curvature_residual"]
    ) < 1e-12
    assert receipt["route"] == "CANDIDATE"
    assert receipt["plurality_preserved"] is True
    assert set(receipt["admissible_paths"]) == {"path-mediated", "path-direct"}
    return {
        "status": "GAUGE_QI_PROCESS_GRAPHRAG_V0_1_OK",
        "route": receipt["route"],
        "admissible_paths": receipt["admissible_paths"],
        "max_curvature_residual": receipt["max_curvature_residual"],
        "next_observation_target": receipt["next_observation_target"],
        "receipt_digest": receipt["receipt_digest"],
        "gauge_invariance_checked": True,
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), ensure_ascii=False, sort_keys=True))
