from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_v0_1 import (
    evaluate_gold_patch_environment_smoke,
)
from scripts.build_codeai_gold_patch_environment_smoke_validation_fixture_v0_1 import (
    build_reference_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/codeai_gold_patch_environment_smoke_validation_v0_1.json"
MANIFEST = ROOT / "manifests/kuuos_codeai_gold_patch_environment_smoke_validation_v0_1.json"

def build_projection() -> tuple[dict, dict]:
    fixture = build_reference_fixture()
    result = evaluate_gold_patch_environment_smoke(
        fixture["request"], fixture["policy"], fixture["predecessor_manifest"],
        fixture["smoke_plan"], fixture["observation"],
    )
    if result.smoke_pack is None or result.receipt is None:
        raise RuntimeError(result.issues)
    example = {**fixture, "smoke_pack": result.smoke_pack, "receipt": result.receipt}
    manifest = {
        "profile_version": result.receipt["profile_version"],
        "predecessor_manifest_digest": fixture["request"]["predecessor_manifest_digest"],
        "dataset_name": fixture["request"]["dataset_name"],
        "dataset_revision": fixture["request"]["dataset_revision"],
        "dataset_artifact_sha256": fixture["request"]["dataset_artifact_sha256"],
        "harness_repository": fixture["request"]["harness_repository"],
        "harness_commit_sha": fixture["request"]["harness_commit_sha"],
        "instance_id": fixture["request"]["instance_id"],
        "predictions_path": fixture["smoke_plan"]["predictions_path"],
        "maximum_workers": fixture["smoke_plan"]["maximum_workers"],
        "timeout_seconds": fixture["smoke_plan"]["timeout_seconds"],
        "decision": result.receipt["decision"],
        "resolved": result.receipt["resolved"],
        "gold_patch_available_to_solver": result.receipt["gold_patch_available_to_solver"],
        "future_harness_execution_authority_granted": result.receipt["future_harness_execution_authority_granted"],
        "repository_mutation_authority_granted": result.receipt["repository_mutation_authority_granted"],
        "git_authority_granted": result.receipt["git_authority_granted"],
        "correctness_claimed": result.receipt["correctness_claimed"],
        "smoke_pack_digest": result.smoke_pack["gold_patch_smoke_pack_digest"],
        "receipt_digest": result.receipt["gold_patch_smoke_receipt_digest"],
    }
    return example, manifest

def write_projection() -> None:
    example, manifest = build_projection()
    EXAMPLE.write_text(json.dumps(example, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

if __name__ == "__main__":
    write_projection()
