#!/usr/bin/env python3
from __future__ import annotations

import pathlib

from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import read_json, write_json
from scripts.qi_bounded_cycle_v0_12_test_support import build_plan, prepare_source, run_cycle


def check_source_digest(base: pathlib.Path) -> None:
    root = base / "source-digest"
    source = prepare_source(root, "source-digest")
    plan = build_plan(
        root=root,
        source=source,
        runner_id="bounded-runner-source",
        generation=0,
        maximum=3,
        suffix="source",
    )
    path = root / "indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json"
    value = read_json(path)
    value["completed_generations"] = 999
    write_json(path, value)
    result = run_cycle(root, plan, source)
    assert result["status"].endswith("_BLOCKED")
    assert "bounded_cycle_source_v0_11_handoff_digest_invalid" in result["blockers"]
    assert result["v0_8_ready"] is False
