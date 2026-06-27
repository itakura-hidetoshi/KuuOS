#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        ROOT / "runtime/kuuos_os_gauge_field_types_v0_61.py",
        ROOT / "runtime/kuuos_os_associated_fields_v0_61.py",
        ROOT / "runtime/kuuos_os_curvature_holonomy_v0_61.py",
        ROOT / "tests/test_kuuos_os_associated_fields_v0_61.py",
        ROOT / "tests/test_kuuos_os_curvature_holonomy_v0_61.py",
        ROOT / "docs/KUUOS_OS_ASSOCIATED_GAUGE_FIELDS_v0_61.md",
        ROOT / "formal/KUOS/WORLD/KuuOSOSAssociatedGaugeFieldsV0_61.lean",
        ROOT / "formal/KuuOSFormalV0_61.lean",
        ROOT / "manifests/kuuos_os_associated_gauge_fields_v0_61.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({"status": "blocked", "missing": missing}, indent=2))
        return 1

    manifest = json.loads(required[-1].read_text(encoding="utf-8"))
    expected = {
        "source_os_validators_required": True,
        "committed_observe_state_required": True,
        "committed_verify_state_required": True,
        "valid_memory_capsule_required": True,
        "verify_observe_exact_binding_required": True,
        "memory_verify_exact_source_binding_required": True,
        "projection_is_read_only": True,
        "source_digest_preserved": True,
        "channel_decomposition_fixed": True,
        "cross_channel_gauge_transform_forbidden": True,
        "verification_is_not_truth": True,
        "memory_projection_does_not_overwrite": True,
        "curvature_channels_not_collapsed": True,
        "memory_holonomy_not_erased": True,
        "production_mutation_not_performed": True,
    }
    boundaries = manifest.get("boundaries", {})
    mismatches = {
        key: {"expected": value, "actual": boundaries.get(key)}
        for key, value in expected.items()
        if boundaries.get(key) is not value
    }
    if mismatches:
        print(json.dumps({
            "status": "blocked",
            "reason": "manifest_boundary_mismatch",
            "mismatches": mismatches,
        }, indent=2))
        return 1

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_kuuos_os_associated_fields_v0_61",
            "tests.test_kuuos_os_curvature_holonomy_v0_61",
        ],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode != 0:
        return completed.returncode

    print(json.dumps({
        "status": "KUUOS_OS_ASSOCIATED_GAUGE_FIELDS_V0_61_VALIDATED",
        "runtime_tests": "success",
        "manifest_boundaries": "success",
        "formal_status": "requires_lake_build",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
