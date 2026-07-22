from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from runtime.kuuos_codeai_bounded_official_harness_execution_schema_v0_1 import (
    canonical_digest,
    canonical_json_bytes,
    official_prediction,
    seal,
    OBSERVATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
)

def file_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def project_example(fixture: dict[str, Any]) -> dict[str, Any]:
    request = fixture["request"]
    plan = fixture["execution_plan"]
    prediction = fixture["prediction"]
    observation = fixture["observation"]
    pack = fixture["execution_pack"]
    receipt = fixture["receipt"]
    return {
        "schema_version": request["schema_version"],
        "profile_version": request["profile_version"],
        "controller_source_commit_sha": request["controller_source_commit_sha"],
        "predecessor_manifest_digest": request["predecessor_manifest_digest"],
        "predecessor_smoke_pack_digest": request["predecessor_smoke_pack_digest"],
        "predecessor_smoke_receipt_digest": request["predecessor_smoke_receipt_digest"],
        "predecessor_external_artifact_digest": request["predecessor_external_artifact_digest"],
        "dataset_name": request["dataset_name"],
        "dataset_revision": request["dataset_revision"],
        "dataset_artifact_sha256": request["dataset_artifact_sha256"],
        "harness_commit_sha": request["harness_commit_sha"],
        "instance_id": request["instance_id"],
        "base_commit_sha": request["base_commit_sha"],
        "prediction": official_prediction(prediction),
        "prediction_digest": prediction["bounded_prediction_digest"],
        "prediction_file_digest": plan["prediction_file_digest"],
        "sample_count": plan["sample_count"],
        "maximum_workers": plan["maximum_workers"],
        "timeout_seconds": plan["timeout_seconds"],
        "non_gold_prediction": plan["non_gold_prediction"],
        "reference_patch_applied": observation["patch_applied"],
        "reference_evaluation_completed": observation["evaluation_completed"],
        "reference_resolved": observation["resolved"],
        "decision": receipt["decision"],
        "execution_pack_digest": pack["bounded_execution_pack_digest"],
        "receipt_digest": receipt["bounded_execution_receipt_digest"],
        "gold_access_granted": receipt["gold_access_granted"],
        "correctness_claimed": receipt["correctness_claimed"],
    }

def project_manifest(receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "profile_version": receipt["profile_version"],
        "decision": receipt["decision"],
        "instance_id": receipt["instance_id"],
        "model_name_or_path": receipt["model_name_or_path"],
        "prediction_digest": receipt["prediction_digest"],
        "patch_applied": receipt["patch_applied"],
        "evaluation_completed": receipt["evaluation_completed"],
        "resolved": receipt["resolved"],
        "report_digest": receipt["report_digest"],
        "test_output_digest": receipt["test_output_digest"],
        "instance_log_digest": receipt["instance_log_digest"],
        "gold_access_granted": receipt["gold_access_granted"],
        "future_harness_execution_authority_granted": receipt["future_harness_execution_authority_granted"],
        "repository_mutation_authority_granted": receipt["repository_mutation_authority_granted"],
        "git_authority_granted": receipt["git_authority_granted"],
        "correctness_claimed": receipt["correctness_claimed"],
        "receipt_digest": receipt[RECEIPT_DIGEST_FIELD],
    }

def build_external_observation(
    *,
    template: dict[str, Any],
    report_path: str | Path,
    test_output_path: str | Path,
    instance_log_path: str | Path,
    instance_id: str,
) -> dict[str, Any]:
    report_path = Path(report_path)
    test_output_path = Path(test_output_path)
    instance_log_path = Path(instance_log_path)
    for path in (report_path, test_output_path, instance_log_path):
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"missing or empty evidence file: {path}")
    report = json.loads(report_path.read_text())
    if instance_id not in report or not isinstance(report[instance_id], dict):
        raise ValueError("report does not contain exact instance")
    instance_report = report[instance_id]
    log_text = instance_log_path.read_text(errors="replace")
    patch_applied = bool(instance_report.get("patch_successfully_applied"))
    if not patch_applied:
        patch_applied = "APPLY_PATCH_PASS" in log_text or "Patch applied successfully" in log_text
    observation = {
        key: value
        for key, value in template.items()
        if key != OBSERVATION_DIGEST_FIELD
    }
    observation.update(
        {
            "patch_applied": patch_applied,
            "evaluation_completed": True,
            "resolved": bool(instance_report.get("resolved", False)),
            "report_observed": True,
            "logs_observed": True,
            "report_digest": file_sha256(report_path),
            "test_output_digest": file_sha256(test_output_path),
            "instance_log_digest": file_sha256(instance_log_path),
        }
    )
    return seal(observation, OBSERVATION_DIGEST_FIELD)

def validate_official_prediction_jsonl(path: str | Path, prediction: dict[str, Any]) -> None:
    lines = Path(path).read_text().splitlines()
    if len(lines) != 1:
        raise ValueError("prediction JSONL must contain exactly one line")
    observed = json.loads(lines[0])
    expected = official_prediction(prediction)
    if observed != expected:
        raise ValueError("prediction JSONL mismatch")
    if canonical_digest(observed) != canonical_digest(expected):
        raise ValueError("prediction digest mismatch")
