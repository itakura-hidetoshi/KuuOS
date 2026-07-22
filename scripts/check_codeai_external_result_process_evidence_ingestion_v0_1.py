from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_schema_v0_1 import canonical_digest
from runtime.kuuos_codeai_external_result_process_evidence_ingestion_v0_1 import build_codeai_external_result_process_evidence_ingestion
from scripts.build_codeai_external_result_process_evidence_ingestion_fixture_v0_1 import (
    build_fixture, EXTERNAL_OBSERVATION_DIGEST, REPORT_DIGEST, TEST_OUTPUT_DIGEST,
    INSTANCE_LOG_DIGEST, PREDECESSOR_ARTIFACT_DIGEST, PREDECESSOR_ARTIFACT_ID,
    PREDECESSOR_WORKFLOW_RUN_ID, PREDECESSOR_WORKFLOW_HEAD_SHA,
)
from scripts.project_codeai_external_result_process_evidence_ingestion_fixture_v0_1 import project_fixture

ROOT = Path(__file__).resolve().parents[1]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def verify_artifact(root: Path, metadata: Path | None = None) -> dict[str, Any]:
    report_path = root / "codeai-bounded-official-external-artifacts" / "report.json"
    output_path = root / "codeai-bounded-official-external-artifacts" / "test_output.txt"
    log_path = root / "codeai-bounded-official-external-artifacts" / "run_instance.log"
    obs_path = root / "codeai-bounded-official-external-observation-v0-1.json"
    for path in (report_path, output_path, log_path, obs_path):
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"missing or empty artifact file: {path}")
    observed = {
        "report_digest": sha256_file(report_path),
        "test_output_digest": sha256_file(output_path),
        "instance_log_digest": sha256_file(log_path),
    }
    expected = {
        "report_digest": REPORT_DIGEST,
        "test_output_digest": TEST_OUTPUT_DIGEST,
        "instance_log_digest": INSTANCE_LOG_DIGEST,
    }
    if observed != expected:
        raise SystemExit(f"evidence file digest mismatch: {observed}")
    observation = load_json(obs_path)
    sealed = observation.pop("bounded_execution_observation_digest", None)
    if sealed != EXTERNAL_OBSERVATION_DIGEST or canonical_digest(observation) != sealed:
        raise SystemExit("external observation seal mismatch")
    report = load_json(report_path)
    item = report.get("sympy__sympy-20590")
    if not isinstance(item, dict):
        raise SystemExit("missing expected report instance")
    if item.get("patch_successfully_applied") is not True or item.get("resolved") is not False:
        raise SystemExit("unexpected bounded report outcome")
    status = item.get("tests_status", {})
    counts = {
        "fail_to_pass_success_count": len(status.get("FAIL_TO_PASS", {}).get("success", [])),
        "fail_to_pass_failure_count": len(status.get("FAIL_TO_PASS", {}).get("failure", [])),
        "pass_to_pass_success_count": len(status.get("PASS_TO_PASS", {}).get("success", [])),
        "pass_to_pass_failure_count": len(status.get("PASS_TO_PASS", {}).get("failure", [])),
    }
    if counts != {
        "fail_to_pass_success_count": 0,
        "fail_to_pass_failure_count": 1,
        "pass_to_pass_success_count": 21,
        "pass_to_pass_failure_count": 0,
    }:
        raise SystemExit(f"unexpected aggregate counts: {counts}")
    if metadata is not None:
        meta = load_json(metadata)
        if meta.get("id") != PREDECESSOR_ARTIFACT_ID:
            raise SystemExit("artifact id mismatch")
        if meta.get("expired") is not False:
            raise SystemExit("artifact expired")
        if meta.get("digest") != "sha256:" + PREDECESSOR_ARTIFACT_DIGEST:
            raise SystemExit("artifact metadata digest mismatch")
        run = meta.get("workflow_run", {})
        if run.get("id") != PREDECESSOR_WORKFLOW_RUN_ID:
            raise SystemExit("workflow run mismatch")
        if run.get("head_sha") != PREDECESSOR_WORKFLOW_HEAD_SHA:
            raise SystemExit("workflow head mismatch")
    return {**observed, **counts, "resolved": False}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--artifact-metadata", type=Path)
    args = parser.parse_args()
    fixture = build_fixture()
    projected = project_fixture(fixture)
    for relative in (
        "examples/codeai_external_result_process_evidence_ingestion_v0_1.json",
        "manifests/kuuos_codeai_external_result_process_evidence_ingestion_v0_1.json",
    ):
        path = ROOT / relative
        if load_json(path) != projected:
            raise SystemExit(f"projection mismatch: {relative}")
    rebuilt = build_codeai_external_result_process_evidence_ingestion(
        request=fixture["request"], policy=fixture["policy"],
        predecessor_manifest=fixture["predecessor_manifest"], plan=fixture["plan"],
        result_evidence=fixture["result_evidence"], process_evidence=fixture["process_evidence"],
    )
    if rebuilt.status != "admitted":
        raise SystemExit("reference ingestion not admitted")
    if args.artifact_root:
        verified = verify_artifact(args.artifact_root, args.artifact_metadata)
        print(json.dumps(verified, sort_keys=True))
    else:
        print(json.dumps(projected, sort_keys=True))

if __name__ == "__main__":
    main()
