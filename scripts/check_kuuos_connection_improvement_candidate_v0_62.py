#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        "runtime/kuuos_connection_candidate_receipt_v0_62.py",
        "runtime/kuuos_connection_candidate_search_v0_62.py",
        "tests/test_kuuos_connection_candidate_valid_v0_62.py",
        "tests/test_kuuos_connection_candidate_search_v0_62.py",
        "tests/test_kuuos_connection_candidate_receipt_v0_62.py",
        "formal/KUOS/WORLD/KuuOSConnectionCandidateCoreV0_62.lean",
        "formal/KUOS/WORLD/KuuOSConnectionCandidateGaugeInvarianceV0_62.lean",
        "formal/KuuOSFormalV0_62.lean",
        "docs/KUUOS_CONNECTION_IMPROVEMENT_CANDIDATE_v0_62.md",
        "manifests/kuuos_connection_improvement_candidate_v0_62.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        print(json.dumps({"status": "blocked", "missing": missing}, indent=2))
        return 1

    manifest = json.loads((ROOT / required[-1]).read_text(encoding="utf-8"))
    boundaries = manifest.get("boundaries", {})
    expected_true = (
        "source_bundle_digest_required",
        "source_connection_unchanged",
        "connection_domain_preserved",
        "gauge_group_preserved",
        "os_fields_preserved",
        "source_bindings_preserved",
        "change_budget_required",
        "curvature_nonincreasing_required",
        "memory_holonomy_observables_preserved",
        "rollback_bound_to_source_bundle",
        "finite_catalog_required",
        "catalog_product_bounded",
        "candidate_only",
        "no_admissible_candidate_preserves_source",
    )
    errors = [key for key in expected_true if boundaries.get(key) is not True]
    if boundaries.get("state_write_performed") is not False:
        errors.append("state_write_performed")
    if errors:
        print(json.dumps({"status": "blocked", "boundary_errors": errors}, indent=2))
        return 1

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_kuuos_connection_candidate_valid_v0_62",
            "tests.test_kuuos_connection_candidate_search_v0_62",
            "tests.test_kuuos_connection_candidate_receipt_v0_62",
        ],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        return result.returncode
    print(json.dumps({
        "status": "KUUOS_CONNECTION_IMPROVEMENT_CANDIDATE_V0_62_VALIDATED",
        "runtime_tests": "success",
        "manifest_boundaries": "success",
        "formal_status": "requires_lake_build",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
