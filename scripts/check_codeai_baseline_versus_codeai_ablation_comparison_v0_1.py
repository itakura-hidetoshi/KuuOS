from __future__ import annotations

import json
from pathlib import Path

from scripts.build_codeai_baseline_versus_codeai_ablation_comparison_fixture_v0_1 import build_fixture
from scripts.project_codeai_baseline_versus_codeai_ablation_comparison_fixture_v0_1 import (
    project_example,
    project_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_baseline_versus_codeai_ablation_comparison_v0_1.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_baseline_versus_codeai_ablation_comparison_v0_1.json"


def main() -> None:
    fixture = build_fixture()
    expected_example = project_example(fixture)
    expected_manifest = project_fixture(fixture)
    observed_example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    observed_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if observed_example != expected_example:
        raise SystemExit("example projection is not deterministic")
    if observed_manifest != expected_manifest:
        raise SystemExit("compact manifest is not deterministic")
    print(json.dumps({
        "status": "ok",
        "decision": expected_manifest["decision"],
        "comparison_phase": expected_manifest["comparison_phase"],
        "pending_cohort_count": len(expected_manifest["pending_cohort_ids"]),
        "performance_comparison_completed": expected_manifest[
            "performance_comparison_completed"
        ],
        "comparison_pack_digest": expected_manifest["comparison_pack_digest"],
        "receipt_digest": expected_manifest["receipt_digest"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
