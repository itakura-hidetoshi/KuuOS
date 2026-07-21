from __future__ import annotations

import json
from pathlib import Path

from scripts.build_codeai_subtask_level_version_bound_memory_fixture_v0_1 import build_reference_fixture
from scripts.project_codeai_subtask_level_version_bound_memory_fixture_v0_1 import project_fixture

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/codeai_subtask_level_version_bound_memory_v0_1.json"


def main() -> int:
    expected = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    actual = project_fixture(build_reference_fixture())
    if actual != expected:
        print("compact projection mismatch")
        print(json.dumps({"expected": expected, "actual": actual}, indent=2, sort_keys=True))
        return 1
    assert actual["matched_entry_count"] == 1
    assert actual["matched_entry_ids"] == ["memory-verify-current-001"]
    assert actual["excluded_entry_count"] == 8
    assert actual["recommendation"] == "exact_subtask_version_bound_memory_available"
    assert actual["holdout_protection_verified"] is True
    assert actual["repository_mutation_performed"] is False
    assert actual["candidate_selected"] is False
    assert actual["execution_authority_granted"] is False
    assert actual["git_authority_granted"] is False
    print("CodeAI Subtask-Level Version-Bound Memory v0.1: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
