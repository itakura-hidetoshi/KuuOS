from __future__ import annotations

import json

from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_schema_v0_1 import (
    DECISION_ADMIT,
    OFFICIAL_PREDICTION_FIELDS,
    STATUS_READY,
    canonical_json,
)
from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1 import (
    build_codeai_external_general_benchmark_swebench_verified_adapter,
)
from scripts.build_codeai_external_general_benchmark_swebench_verified_adapter_fixture_v0_1 import (
    build_fixture,
)
from scripts.project_codeai_external_general_benchmark_swebench_verified_adapter_fixture_v0_1 import (
    EXAMPLE_PATH,
    MANIFEST_PATH,
    compact_projection,
)


def main() -> int:
    fixture = build_fixture()
    committed_example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    committed_manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if canonical_json(committed_example) != canonical_json(fixture):
        raise SystemExit("example projection mismatch")
    expected_manifest = compact_projection(fixture)
    if canonical_json(committed_manifest) != canonical_json(expected_manifest):
        raise SystemExit("manifest projection mismatch")

    result = build_codeai_external_general_benchmark_swebench_verified_adapter(
        request=fixture["request"],
        policy=fixture["policy"],
        benchmark_contract=fixture["benchmark_contract"],
        run_plan=fixture["run_plan"],
        predictions=fixture["predictions"],
    )
    if result.status != STATUS_READY or result.adapter_pack is None or result.receipt is None:
        raise SystemExit("reference adapter did not produce a ready result")
    if result.adapter_pack["adapter_decision"] != DECISION_ADMIT:
        raise SystemExit("reference protocol was not admitted")
    if tuple(result.adapter_pack["official_prediction_fields"]) != OFFICIAL_PREDICTION_FIELDS:
        raise SystemExit("official prediction field projection mismatch")
    if result.adapter_pack["harness_execution_performed"]:
        raise SystemExit("protocol adapter performed harness execution")
    if result.adapter_pack["benchmark_result_ingested"]:
        raise SystemExit("protocol adapter ingested an unexecuted result")
    if result.adapter_pack["repository_mutation_performed"] or result.adapter_pack["git_authority_granted"]:
        raise SystemExit("protocol adapter crossed repository or Git authority boundary")
    print(
        json.dumps(
            {
                "status": result.status,
                "decision": result.adapter_pack["adapter_decision"],
                "sample_count": result.adapter_pack["sample_count"],
                "official_predictions_digest": result.adapter_pack["official_predictions_digest"],
                "adapter_pack_digest": result.adapter_pack["codeai_external_benchmark_adapter_pack_digest"],
                "receipt_digest": result.receipt[
                    "codeai_external_benchmark_adapter_receipt_digest"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
