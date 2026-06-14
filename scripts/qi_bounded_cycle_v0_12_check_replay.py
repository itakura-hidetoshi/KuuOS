#!/usr/bin/env python3
from __future__ import annotations

import pathlib

from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import read_json, records
from scripts.qi_bounded_cycle_v0_12_test_support import build_plan, prepare_source, run_cycle


def check_replay(base: pathlib.Path) -> None:
    root = base / "replay"
    source = prepare_source(root, "replay")
    plan = build_plan(
        root=root,
        source=source,
        runner_id="bounded-runner-replay",
        generation=0,
        maximum=3,
        suffix="same",
    )
    first = run_cycle(root, plan, source)
    assert first["status"].endswith("_READY"), first
    state = read_json(root / "indra_qi_bounded_cycle_state_v0_12.json")
    count = len(records(root / "indra_qi_bounded_cycle_ledger_v0_12.jsonl"))
    replay = run_cycle(root, plan, source)
    assert replay["status"].endswith("_BLOCKED")
    assert replay["v0_8_ready"] is False
    assert read_json(root / "indra_qi_bounded_cycle_state_v0_12.json") == state
    assert len(records(root / "indra_qi_bounded_cycle_ledger_v0_12.jsonl")) == count
