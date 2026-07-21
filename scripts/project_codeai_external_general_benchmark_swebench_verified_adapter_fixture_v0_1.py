from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.build_codeai_external_general_benchmark_swebench_verified_adapter_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "examples" / "codeai_external_general_benchmark_swebench_verified_adapter_v0_1.json"
MANIFEST_PATH = ROOT / "manifests" / "kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1.json"


def compact_projection(fixture: dict[str, Any]) -> dict[str, Any]:
    pack = fixture["adapter_pack"]
    receipt = fixture["receipt"]
    return {
        "profile_version": pack["profile_version"],
        "controller_source_commit_sha": pack["controller_source_commit_sha"],
        "benchmark_id": pack["benchmark_id"],
        "dataset_name": pack["dataset_name"],
        "split": pack["split"],
        "expected_instance_count": pack["expected_instance_count"],
        "harness_repository": pack["harness_repository"],
        "harness_commit_sha": pack["harness_commit_sha"],
        "evaluation_mode": pack["evaluation_mode"],
        "sample_count": pack["sample_count"],
        "prediction_count": pack["prediction_count"],
        "official_prediction_fields": pack["official_prediction_fields"],
        "official_predictions_digest": pack["official_predictions_digest"],
        "adapter_decision": pack["adapter_decision"],
        "hold_reasons": pack["hold_reasons"],
        "protocol_projection_only": pack["protocol_projection_only"],
        "harness_execution_performed": pack["harness_execution_performed"],
        "benchmark_result_ingested": pack["benchmark_result_ingested"],
        "network_access_performed": pack["network_access_performed"],
        "secret_access_performed": pack["secret_access_performed"],
        "repository_mutation_performed": pack["repository_mutation_performed"],
        "git_authority_granted": pack["git_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
        "adapter_pack_digest": pack["codeai_external_benchmark_adapter_pack_digest"],
        "receipt_digest": receipt["codeai_external_benchmark_adapter_receipt_digest"],
    }


def project() -> tuple[dict[str, Any], dict[str, Any]]:
    fixture = build_fixture()
    example = fixture
    manifest = compact_projection(fixture)
    EXAMPLE_PATH.write_text(json.dumps(example, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return example, manifest


if __name__ == "__main__":
    project()
