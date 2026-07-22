from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.build_codeai_bounded_official_harness_execution_fixture_v0_1 import build_fixture
from runtime.kuuos_codeai_bounded_official_harness_execution_checks_v0_1 import project_example, project_manifest
from runtime.kuuos_codeai_bounded_official_harness_execution_schema_v0_1 import official_prediction

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--example-output")
    parser.add_argument("--manifest-output")
    parser.add_argument("--predictions-output")
    args = parser.parse_args()
    fixture = build_fixture()
    if args.example_output:
        Path(args.example_output).write_text(json.dumps(project_example(fixture), indent=2, sort_keys=True) + "\n")
    if args.manifest_output:
        Path(args.manifest_output).write_text(
            json.dumps(project_manifest(fixture["receipt"]), indent=2, sort_keys=True) + "\n"
        )
    if args.predictions_output:
        Path(args.predictions_output).write_text(
            json.dumps(official_prediction(fixture["prediction"]), sort_keys=True) + "\n"
        )
    if not any((args.example_output, args.manifest_output, args.predictions_output)):
        print(json.dumps(fixture, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
