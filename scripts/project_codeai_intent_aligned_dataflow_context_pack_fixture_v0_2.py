#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from scripts.build_codeai_intent_aligned_dataflow_context_pack_fixture_v0_2 import build_reference_result


def project_reference_result(result: Mapping[str, Any]) -> dict[str, Any]:
    pack = result["context_pack"]
    receipt = result["receipt"]
    selected = pack["selected_files"]
    return {
        "schema_version": pack["schema_version"],
        "profile_version": pack["profile_version"],
        "codeai_disposition": pack["codeai_disposition"],
        "operating_mode": pack["operating_mode"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "context_pack_digest": pack["codeai_intent_aligned_dataflow_context_pack_digest"],
        "receipt_digest": receipt["codeai_intent_aligned_dataflow_context_receipt_digest"],
        "query_stages": [node["stage"] for node in pack["query_lineage"]],
        "query_lineage_node_count": len(pack["query_lineage"]),
        "selected_paths": [item["path"] for item in selected],
        "selected_file_count": len(selected),
        "symbol_digest_count": sum(bool(item["symbol_digest"]) for item in selected),
        "resolved_dependency_path_count": sum(len(item["resolved_dependency_paths"]) for item in selected),
        "dataflow_edge_count": sum(len(item["dataflow_edges"]) for item in selected),
        "repository_snapshot_bytes": pack["budget_evidence"]["repository_snapshot_bytes"],
        "total_context_bytes": pack["budget_evidence"]["total_context_bytes"],
        "repository_observation_read_only": pack["repository_observation_read_only"],
        "repository_mutation_performed": pack["repository_mutation_performed"],
        "network_access_performed": pack["network_access_performed"],
        "secret_material_read": pack["secret_material_read"],
        "candidate_selection_authority_granted": pack["candidate_selection_authority_granted"],
        "execution_authority_granted": pack["execution_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
        "completeness_claimed": pack["completeness_claimed"],
        "representativeness_claimed": pack["representativeness_claimed"],
    }


def build_projection() -> dict[str, Any]:
    return project_reference_result(build_reference_result())


if __name__ == "__main__":
    output_path = Path("examples/codeai_intent_aligned_dataflow_context_pack_v0_2.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_projection(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
