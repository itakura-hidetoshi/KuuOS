from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime.kuuos_codeai_gold_patch_environment_smoke_validation_checks_v0_1 import (
    load_json, validate_harness_outputs, validate_reference,
)
from scripts.project_codeai_gold_patch_environment_smoke_validation_fixture_v0_1 import (
    EXAMPLE, MANIFEST, build_projection,
)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report")
    parser.add_argument("--test-output")
    parser.add_argument("--instance-log")
    parser.add_argument("--instance-id", default="sympy__sympy-20590")
    parser.add_argument("--write-observation")
    args = parser.parse_args()

    expected_example, expected_manifest = build_projection()
    actual_example, actual_manifest = load_json(EXAMPLE), load_json(MANIFEST)
    if actual_example != expected_example:
        raise SystemExit("example projection mismatch")
    if actual_manifest != expected_manifest:
        raise SystemExit("manifest projection mismatch")
    issues = validate_reference(actual_example, actual_manifest)
    if issues:
        raise SystemExit("reference validation failed: " + ",".join(issues))

    if any((args.report, args.test_output, args.instance_log)):
        if not all((args.report, args.test_output, args.instance_log)):
            raise SystemExit("all harness output paths are required")
        evidence = validate_harness_outputs(
            args.report, args.test_output, args.instance_log, args.instance_id
        )
        if args.write_observation:
            Path(args.write_observation).write_text(
                json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        print(json.dumps(evidence, sort_keys=True))
    else:
        print(json.dumps({
            "decision": actual_manifest["decision"],
            "instance_id": actual_manifest["instance_id"],
            "smoke_pack_digest": actual_manifest["smoke_pack_digest"],
            "receipt_digest": actual_manifest["receipt_digest"],
        }, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
