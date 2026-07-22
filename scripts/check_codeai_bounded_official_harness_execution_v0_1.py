from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from scripts.build_codeai_bounded_official_harness_execution_fixture_v0_1 import build_fixture
from runtime.kuuos_codeai_bounded_official_harness_execution_checks_v0_1 import (
    build_external_observation,
    project_example,
    project_manifest,
    validate_official_prediction_jsonl,
)
from runtime.kuuos_codeai_bounded_official_harness_execution_schema_v0_1 import (
    PACK_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    official_prediction,
)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", default="examples/codeai_bounded_official_harness_execution_v0_1.json")
    parser.add_argument("--manifest", default="manifests/kuuos_codeai_bounded_official_harness_execution_v0_1.json")
    parser.add_argument("--predictions")
    parser.add_argument("--report")
    parser.add_argument("--test-output")
    parser.add_argument("--instance-log")
    parser.add_argument("--instance-id")
    parser.add_argument("--write-observation")
    args = parser.parse_args()

    fixture = build_fixture()
    expected_example = json.dumps(project_example(fixture), indent=2, sort_keys=True) + "\n"
    expected_manifest = json.dumps(project_manifest(fixture["receipt"]), indent=2, sort_keys=True) + "\n"
    if Path(args.example).read_text() != expected_example:
        raise SystemExit("example projection mismatch")
    if Path(args.manifest).read_text() != expected_manifest:
        raise SystemExit("manifest projection mismatch")

    if args.predictions:
        validate_official_prediction_jsonl(args.predictions, fixture["prediction"])

    external = (args.report, args.test_output, args.instance_log, args.instance_id)
    if any(external):
        if not all(external):
            raise SystemExit("all external evidence arguments are required")
        observation = build_external_observation(
            template=fixture["observation"],
            report_path=args.report,
            test_output_path=args.test_output,
            instance_log_path=args.instance_log,
            instance_id=args.instance_id,
        )
        if not observation["patch_applied"]:
            raise SystemExit("external prediction patch was not applied")
        if not observation["evaluation_completed"]:
            raise SystemExit("external evaluation did not complete")
        if args.write_observation:
            Path(args.write_observation).write_text(
                json.dumps(observation, indent=2, sort_keys=True) + "\n"
            )
        print(json.dumps({
            "instance_id": args.instance_id,
            "resolved": observation["resolved"],
            "report_digest": observation["report_digest"],
            "test_output_digest": observation["test_output_digest"],
            "instance_log_digest": observation["instance_log_digest"],
        }, sort_keys=True))
    else:
        print(json.dumps({
            "decision": fixture["receipt"]["decision"],
            "resolved": fixture["receipt"]["resolved"],
            "execution_pack_digest": fixture["execution_pack"][PACK_DIGEST_FIELD],
            "receipt_digest": fixture["receipt"][RECEIPT_DIGEST_FIELD],
        }, sort_keys=True))

if __name__ == "__main__":
    main()
