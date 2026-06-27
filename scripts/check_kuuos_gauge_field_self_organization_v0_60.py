#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        ROOT / "runtime/kuuos_gauge_field_self_organization_types_v0_60.py",
        ROOT / "runtime/kuuos_discrete_gauge_connection_v0_60.py",
        ROOT / "runtime/kuuos_gauge_field_self_organization_v0_60.py",
        ROOT / "tests/test_kuuos_gauge_field_self_organization_v0_60.py",
        ROOT / "docs/KUUOS_GAUGE_FIELD_SELF_ORGANIZATION_v0_60.md",
        ROOT / "formal/KUOS/WORLD/KuuOSGaugeFieldSelfOrganizationV0_60.lean",
        ROOT / "formal/KuuOSFormalV0_60.lean",
        ROOT / "manifests/kuuos_gauge_field_self_organization_v0_60.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({"status": "blocked", "missing": missing}, indent=2))
        return 1

    manifest = json.loads(required[-1].read_text(encoding="utf-8"))
    expected = {
        "graph_semantics_forbidden": True,
        "constitutional_coordinates_fixed": True,
        "gauge_change_does_not_grant_authority": True,
        "self_organization_produces_candidate_only": True,
        "production_mutation_not_performed": True,
        "rollback_required_before_promotion": True,
    }
    boundaries = manifest.get("boundaries", {})
    if any(boundaries.get(key) is not value for key, value in expected.items()):
        print(json.dumps({"status": "blocked", "reason": "manifest_boundary_mismatch"}, indent=2))
        return 1

    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "tests.test_kuuos_gauge_field_self_organization_v0_60"],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode != 0:
        return completed.returncode

    print(json.dumps({
        "status": "KUUOS_GAUGE_FIELD_SELF_ORGANIZATION_V0_60_VALIDATED",
        "runtime_tests": "success",
        "manifest_boundaries": "success",
        "formal_status": "requires_lake_build"
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
