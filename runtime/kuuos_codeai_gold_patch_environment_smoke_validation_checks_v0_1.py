from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any, Mapping

from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_schema_v0_1 import (
    PACK_DIGEST_FIELD, RECEIPT_DIGEST_FIELD, digest_ok,
)
from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_v0_1 import (
    evaluate_gold_patch_environment_smoke,
)

def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def file_digest(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_reference(example: Mapping[str, Any], manifest: Mapping[str, Any]) -> list[str]:
    result = evaluate_gold_patch_environment_smoke(
        example["request"], example["policy"], example["predecessor_manifest"],
        example["smoke_plan"], example["observation"],
    )
    issues: list[str] = []
    if result.status != "ready": issues.append("reference_not_ready")
    if result.smoke_pack is None or not digest_ok(result.smoke_pack, PACK_DIGEST_FIELD):
        issues.append("pack_invalid")
    if result.receipt is None or not digest_ok(result.receipt, RECEIPT_DIGEST_FIELD):
        issues.append("receipt_invalid")
    if result.smoke_pack and result.smoke_pack[PACK_DIGEST_FIELD] != manifest.get("smoke_pack_digest"):
        issues.append("manifest_pack_mismatch")
    if result.receipt and result.receipt[RECEIPT_DIGEST_FIELD] != manifest.get("receipt_digest"):
        issues.append("manifest_receipt_mismatch")
    if result.smoke_pack and result.smoke_pack.get("decision") != "gold_patch_environment_smoke_admitted":
        issues.append("reference_not_admitted")
    return sorted(set(issues))

def validate_harness_outputs(report_path: str | Path, test_output_path: str | Path,
                             instance_log_path: str | Path, instance_id: str) -> dict[str, Any]:
    report = load_json(report_path)
    if instance_id not in report:
        raise ValueError("instance missing from report")
    resolved = report[instance_id].get("resolved")
    if resolved is not True:
        raise ValueError("gold smoke instance unresolved")
    test_path, log_path = Path(test_output_path), Path(instance_log_path)
    if not test_path.is_file() or test_path.stat().st_size == 0:
        raise ValueError("test output missing")
    if not log_path.is_file() or log_path.stat().st_size == 0:
        raise ValueError("instance log missing")
    return {
        "instance_id": instance_id,
        "resolved": True,
        "report_digest": file_digest(report_path),
        "test_output_digest": file_digest(test_path),
        "instance_log_digest": file_digest(log_path),
        "external_harness_execution_observed": True,
        "harness_execution_performed_by_kernel": False,
    }
