#!/usr/bin/env python3
from __future__ import annotations

import pathlib

from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import snapshot_root_files
from scripts.qi_bounded_cycle_v0_12_test_support import (
    build_plan,
    cycle_license,
    prepare_source,
    run_cycle,
)


def check_gate(base: pathlib.Path) -> None:
    root = base / "license-gate"
    source = prepare_source(root, "license-gate")
    plan = build_plan(
        root=root,
        source=source,
        runner_id="bounded-runner-license",
        generation=0,
        maximum=3,
        suffix="license",
    )
    license_value = cycle_license(plan, source)
    license_value["v0_10_invoke_allowed"] = False
    before = snapshot_root_files(root)
    result = run_cycle(root, plan, source, license_value)
    assert result["status"].endswith("_BLOCKED")
    assert "bounded_cycle_license_v0_10_invoke_allowed_not_true" in result["blockers"]
    assert result["v0_8_ready"] is False
    assert snapshot_root_files(root) == before
