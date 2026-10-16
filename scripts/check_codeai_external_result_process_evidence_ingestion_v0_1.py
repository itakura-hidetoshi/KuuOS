from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_schema_v0_1 import (
    canonical_digest, seal, REQUEST_DIGEST_FIELD, POLICY_DIGEST_FIELD,
    PLAN_DIGEST_FIELD, RESULT_DIGEST_FIELD, PROCESS_DIGEST_FIELD,
)
from runtime.kuuos_codeai_external_result_process_evidence_ingestion_v0_1 import build_codeai_external_result_process_evidence_ingestion
from scripts.build_codeai_external_result_process_evidence_ingestion_fixture_v0_1 import (
    build_fixture, EXTERNAL_OBSERVATION_DIGEST, REPORT_DIGEST, TEST_OUTPUT_DIGEST,
    INSTANCE_LOG_DIGEST, PREDECESSOR_ARTIFACT_DIGEST, PREDECESSOR_ARTIFACT_ID,
    PREDECESSOR_WORKFLOW_RUN_ID, PREDECESSOR_WORKFLOW_HEAD_SHA,
)
from scripts.project_codeai_external_result_process_evidence_ingestion_fixture_v0_1 import project_fixture
from scripts.build_codeai_bounded_official_harness_execution_fixture_v0_1 import build_fixture as build_bounded_fixture

ROOT = Path(__file__).resolve().parents[1]
LIVE_BINDING_FIELDS = frozenset({
    "schema_version", "predecessor_workflow_run_id", "predecessor_workflow_run_attempt",
    "predecessor_workflow_head_sha", "predecessor_artifact_id", "predecessor_artifact_name",
    "predecessor_artifact_digest", "external_observation_digest", "prediction_digest",
    "report_digest", "test_output_digest", "instance_log_digest",
})


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_live_binding(binding: dict[str, Any]) -> None:
    """Accept only one named, immutable and independently observed replacement run."""
    if not isinstance(binding, dict) or set(binding) != LIVE_BINDING_FIELDS:
        raise SystemExit("live binding has missing or unexpected fields")
    if binding["schema_version"] != "kuuos.external-evidence.reobservation.v1":
        raise SystemExit("unknown live binding schema")
    for key in ("predecessor_workflow_run_id", "predecessor_artifact_id"):
        if type(binding[key]) is not int or binding[key] <= 0:
            raise SystemExit(f"invalid {key}")
    if type(binding["predecessor_workflow_run_attempt"]) is not int or binding["predecessor_workflow_run_attempt"] <= 0:
        raise SystemExit("invalid predecessor run attempt")
    if not isinstance(binding["predecessor_workflow_head_sha"], str) or not re.fullmatch(r"[0-9a-f]{40}",binding["predecessor_workflow_head_sha"]):
        raise SystemExit("invalid predecessor commit SHA")
    for key in ("predecessor_artifact_digest", "external_observation_digest", "prediction_digest",
                "report_digest", "test_output_digest", "instance_log_digest"):
        if not isinstance(binding[key], str) or not re.fullmatch(r"[0-9a-f]{64}", binding[key]):
            raise SystemExit(f"invalid {key}")
    expected_name = ("codeai-bounded-official-external-v0-1-"
                     f"{binding['predecessor_workflow_run_id']}-{binding['predecessor_workflow_run_attempt']}")
    if binding["predecessor_artifact_name"] != expected_name:
        raise SystemExit("predecessor artifact name does not match the exact run attempt")
    if binding["prediction_digest"] != build_fixture()["request"]["prediction_digest"]:
        raise SystemExit("predecessor prediction changed: new authorization required")


def build_reobserved_fixture(binding: dict[str, Any]) -> dict[str, Any]:
    """New sealed ingestion receipt; leave original v0.1 reference fixture unchanged."""
    validate_live_binding(binding)
    fixture = build_fixture()
    updates = {
        "predecessor_workflow_run_id": binding["predecessor_workflow_run_id"],
        "predecessor_artifact_id": binding["predecessor_artifact_id"],
        "predecessor_artifact_digest": binding["predecessor_artifact_digest"],
        "external_observation_digest": binding["external_observation_digest"],
    }
    for component, digest_key in (
        ("request", REQUEST_DIGEST_FIELD), ("plan", PLAN_DIGEST_FIELD),
        ("result_evidence", RESULT_DIGEST_FIELD), ("process_evidence", PROCESS_DIGEST_FIELD),
    ):
        value = {k: v for k, v in fixture[component].items() if k != digest_key}
        value.update(updates)
        if component == "request":
            value["request_id"] = "external-result-ingestion-request-reobserved-20261016"
            value["request_revision"] = "external-result-ingestion-rev-002"
        if component == "plan":
            value["ingestion_id"] = "kuuos-external-result-ingestion-reobserved-20261016"
        if component == "result_evidence":
            value["report_digest"] = binding["report_digest"]
        if component == "process_evidence":
            value["test_output_digest"] = binding["test_output_digest"]
            value["instance_log_digest"] = binding["instance_log_digest"]
        fixture[component] = seal(value, digest_key)
    policy = {k: v for k, v in fixture["policy"].items() if k != POLICY_DIGEST_FIELD}
    policy.update({"expected_" + k: v for k, v in updates.items()})
    fixture["policy"] = seal(policy, POLICY_DIGEST_FIELD)
    rebuilt = build_codeai_external_result_process_evidence_ingestion(
        request=fixture["request"], policy=fixture["policy"],
        predecessor_manifest=fixture["predecessor_manifest"], plan=fixture["plan"],
        result_evidence=fixture["result_evidence"], process_evidence=fixture["process_evidence"],
    )
    if rebuilt.status != "admitted" or rebuilt.ingestion_pack is None or rebuilt.receipt is None:
        raise SystemExit("fresh run failed original ingestion policy")
    fixture["ingestion_pack"] = rebuilt.ingestion_pack
    fixture["receipt"] = rebuilt.receipt
    return fixture


def verify_artifact(root: Path, metadata: Path | None = None, *,
                    live_binding: dict[str, Any] | None = None,
                    workflow_metadata: Path | None = None) -> dict[str, Any]:
    """Verify raw files off-repository; emit only aggregate counts and digests."""
    if live_binding is not None:
        validate_live_binding(live_binding)
        if metadata is None or workflow_metadata is None:
            raise SystemExit("live evidence needs both artifact and workflow metadata")
    report_path = root / "codeai-bounded-official-external-artifacts" / "report.json"
    output_path = root / "codeai-bounded-official-external-artifacts" / "test_output.txt"
    log_path = root / "codeai-bounded-official-external-artifacts" / "run_instance.log"
    obs_path = root / "codeai-bounded-official-external-observation-v0-1.json"
    for path in (report_path, output_path, log_path, obs_path):
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"missing or empty artifact file: {path.name}")
    observed = {
        "report_digest": sha256_file(report_path),
        "test_output_digest": sha256_file(output_path),
        "instance_log_digest": sha256_file(log_path),
    }
    expected = {key: (live_binding[key] if live_binding else value) for key, value in {
        "report_digest": REPORT_DIGEST,
        "test_output_digest": TEST_OUTPUT_DIGEST,
        "instance_log_digest": INSTANCE_LOG_DIGEST,
    }.items()}
    if observed != expected:
        raise SystemExit("evidence file digest mismatch")
    observation = load_json(obs_path)
    if not isinstance(observation, dict):
        raise SystemExit("observation not an object")
    sealed = observation.pop("bounded_execution_observation_digest", None)
    observation_digest = live_binding["external_observation_digest"] if live_binding else EXTERNAL_OBSERVATION_DIGEST
    if sealed != observation_digest or canonical_digest(observation) != sealed:
        raise SystemExit("external observation seal mismatch")
    if live_binding is not None:
        bounded = build_bounded_fixture()
        for key, value in {
            **observed,
            "instance_id": bounded["request"]["instance_id"],
            "prediction_digest": live_binding["prediction_digest"],
            "controller_repository": bounded["request"]["controller_repository"],
            "controller_source_commit_sha": bounded["request"]["controller_source_commit_sha"],
            "predecessor_manifest_digest": bounded["request"]["predecessor_manifest_digest"],
            "execution_contract_digest": bounded["request"]["execution_contract_digest"],
            "dataset_artifact_sha256": bounded["request"]["dataset_artifact_sha256"],
            "harness_commit_sha": bounded["request"]["harness_commit_sha"],
        }.items():
            if observation.get(key) != value:
                raise SystemExit(f"external observation mismatch: {key}")
        for key in ("evaluation_completed", "patch_applied", "docker_used", "container_started",
                    "image_available", "report_observed", "logs_observed", "external_harness_execution_observed"):
            if observation.get(key) is not True:
                raise SystemExit(f"external observation incomplete: {key}")
        for key in ("resolved", "gold_exposed_to_solver", "gold_used_for_candidate_generation",
                    "gold_used_for_repair_memory", "repository_mutated", "git_authority",
                    "correctness_claimed", "harness_execution_performed_by_kernel"):
            if observation.get(key) is not False:
                raise SystemExit(f"external observation overclaim: {key}")
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
        expected_id = live_binding["predecessor_artifact_id"] if live_binding else PREDECESSOR_ARTIFACT_ID
        expected_digest = live_binding["predecessor_artifact_digest"] if live_binding else PREDECESSOR_ARTIFACT_DIGEST
        expected_run = live_binding["predecessor_workflow_run_id"] if live_binding else PREDECESSOR_WORKFLOW_RUN_ID
        expected_head = live_binding["predecessor_workflow_head_sha"] if live_binding else PREDECESSOR_WORKFLOW_HEAD_SHA
        if meta.get("id") != expected_id or meta.get("expired") is not False:
            raise SystemExit("artifact id mismatch or artifact expired")
        if meta.get("digest") != "sha256:" + expected_digest:
            raise SystemExit("artifact metadata digest mismatch")
        if live_binding and meta.get("name") != live_binding["predecessor_artifact_name"]:
            raise SystemExit("artifact name mismatch")
        run = meta.get("workflow_run", {})
        if run.get("id") != expected_run or run.get("head_sha") != expected_head:
            raise SystemExit("artifact workflow identity mismatch")
    if live_binding is not None:
        run = load_json(workflow_metadata)
        if (run.get("id") != live_binding["predecessor_workflow_run_id"] or
            run.get("run_attempt") != live_binding["predecessor_workflow_run_attempt"] or
            run.get("head_sha") != live_binding["predecessor_workflow_head_sha"] or
            run.get("status") != "completed" or run.get("conclusion") != "success" or
            run.get("event") != "pull_request" or
            run.get("repository", {}).get("full_name") != "itakura-hidetoshi/KuuOS"):
            raise SystemExit("external workflow not verified as exact successful run")
    return {**observed, **counts, "resolved": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--artifact-metadata", type=Path)
    parser.add_argument("--live-binding", type=Path)
    parser.add_argument("--workflow-metadata", type=Path)
    parser.add_argument("--receipt-output", type=Path)
    args = parser.parse_args()
    if args.live_binding and not args.artifact_root:
        raise SystemExit("live binding requires an artifact root")
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
    if args.live_binding:
        binding = load_json(args.live_binding)
        fresh = build_reobserved_fixture(binding)
        verified = verify_artifact(args.artifact_root, args.artifact_metadata,
                                   live_binding=binding, workflow_metadata=args.workflow_metadata)
        result = {**verified, **project_fixture(fresh),
                  "evidence_lineage": "independent_reobservation",
                  "predecessor_workflow_run_attempt": binding["predecessor_workflow_run_attempt"],
                  "predecessor_workflow_head_sha": binding["predecessor_workflow_head_sha"],
                  "predecessor_artifact_name": binding["predecessor_artifact_name"]}
        if args.receipt_output:
            args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
            args.receipt_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, sort_keys=True))
    else:
        if args.receipt_output or args.workflow_metadata:
            raise SystemExit("live receipt options require an explicit live binding")
        if args.artifact_root:
            print(json.dumps(verify_artifact(args.artifact_root, args.artifact_metadata), sort_keys=True))
        else:
            print(json.dumps(projected, sort_keys=True))

if __name__ == "__main__":
    main()
