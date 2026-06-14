#!/usr/bin/env python3
from __future__ import annotations

import pathlib

from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import cycle_plan_digest
from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import snapshot_root_files, snapshot_tree
from scripts.qi_bounded_cycle_v0_12_test_support import build_plan, prepare_source, run_cycle


def check_compensation(base: pathlib.Path) -> None:
    root = base / "compensation"
    source = prepare_source(root, "compensation")
    plan = build_plan(
        root=root,
        source=source,
        runner_id="bounded-runner-compensation",
        generation=0,
        maximum=3,
        suffix="compensation",
    )
    plan["projection_policy"]["minimum_seed_count"] = 99
    plan["cycle_plan_digest"] = cycle_plan_digest(plan)
    root_before = snapshot_root_files(root)
    child_before = snapshot_tree(source["child"])
    target = root / "indra_qi_causal_reentry_cycles_v0_7" / plan["reentry_id"]
    result = run_cycle(root, plan, source)
    assert result["status"].endswith("_BLOCKED"), result
    assert result["transaction_rolled_back"] is True
    assert result["v0_8_ready"] is True
    assert result["v0_9_ready"] is True
    assert result["v0_10_ready"] is True
    assert result["v0_11_ready"] is False
    assert snapshot_root_files(root) == root_before
    assert snapshot_tree(source["child"]) == child_before
    assert not target.exists()
