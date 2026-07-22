from __future__ import annotations

import json
from pathlib import Path

from scripts.build_codeai_external_corpus_acquisition_freeze_receipt_fixture_v0_1 import build_fixture

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_external_corpus_acquisition_freeze_receipt_v0_1.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_external_corpus_acquisition_freeze_receipt_v0_1.json"


def manifest_projection(fixture: dict) -> dict:
    pack = fixture["freeze_pack"]
    receipt = fixture["receipt"]
    return {
        "profile_version": pack["profile_version"],
        "freeze_decision": pack["freeze_decision"],
        "freeze_pack_digest": pack["codeai_external_corpus_freeze_pack_digest"],
        "receipt_digest": receipt["codeai_external_corpus_freeze_receipt_digest"],
        "predecessor_manifest_digest": pack["predecessor_manifest_digest"],
        "benchmark_id": pack["benchmark_id"],
        "dataset_name": pack["dataset_name"],
        "dataset_revision": pack["dataset_revision"],
        "dataset_split": pack["dataset_split"],
        "artifact_path": pack["artifact_path"],
        "artifact_sha256": pack["artifact_sha256"],
        "artifact_size_bytes": pack["artifact_size_bytes"],
        "row_count": pack["row_count"],
        "corpus_frozen": pack["corpus_frozen"],
        "solver_visible_fields": pack["solver_visible_fields"],
        "restricted_evaluator_fields": pack["restricted_evaluator_fields"],
        "fetch_performed_by_kernel": pack["fetch_performed_by_kernel"],
        "artifact_copy_committed_to_repository": pack["artifact_copy_committed_to_repository"],
        "solver_label_access_granted": pack["solver_label_access_granted"],
        "gold_patch_access_granted": pack["gold_patch_access_granted"],
        "harness_execution_authority_granted": pack["harness_execution_authority_granted"],
        "repository_mutation_performed": pack["repository_mutation_performed"],
        "git_authority_granted": pack["git_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
    }


def main() -> None:
    fixture = build_fixture()
    EXAMPLE.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest_projection(fixture), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
