#!/usr/bin/env python3
from __future__ import annotations

import pathlib

from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import valid_digest
from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import read_json, records
from scripts.qi_bounded_cycle_v0_12_test_support import (
    build_plan,
    prepare_source,
    run_cycle,
)


def current_source(root: pathlib.Path) -> dict:
    reentry = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
    child = pathlib.Path(reentry["child_runtime_root"])
    values = records(root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl")
    return {
        "world": read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json"),
        "handoff": read_json(root / "indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json"),
        "record": read_json(root / "indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json"),
        "ledger": values[-1],
        "reentry": reentry,
        "child": child,
        "causal": read_json(child / "kuuos_causal_world_model_state_v14_0.json"),
    }


def check_two_generations(base: pathlib.Path) -> None:
    root = base / "two-generations"
    source0 = prepare_source(root, "two-generations")
    plan0 = build_plan(
        root=root,
        source=source0,
        runner_id="bounded-runner-two",
        generation=0,
        maximum=2,
        suffix="g0",
    )
    result0 = run_cycle(root, plan0, source0)
    assert result0["status"].endswith("_READY"), result0
    assert result0["completed_generations"] == 1
    assert result0["runner_status"] == "bounded_cycle_ready_for_next_generation"
    assert result0["v0_8_ready"] and result0["v0_9_ready"]
    assert result0["v0_10_ready"] and result0["v0_11_ready"]
    state0 = read_json(root / "indra_qi_bounded_cycle_state_v0_12.json")
    handoff0 = read_json(root / "indra_qi_bounded_cycle_handoff_v0_12.json")
    record0 = read_json(root / "indra_qi_bounded_cycle_record_v0_12.json")
    ledger0 = records(root / "indra_qi_bounded_cycle_ledger_v0_12.jsonl")
    assert valid_digest(state0, "runner_state_digest")
    assert valid_digest(handoff0, "generation_handoff_digest")
    assert valid_digest(record0, "generation_record_digest")
    assert valid_digest(ledger0[-1], "record_digest")
    assert pathlib.Path(state0["latest_child_runtime_root"]).is_dir()

    source1 = current_source(root)
    plan1 = build_plan(
        root=root,
        source=source1,
        runner_id="bounded-runner-two",
        generation=1,
        maximum=2,
        suffix="g1",
    )
    result1 = run_cycle(root, plan1, source1)
    assert result1["status"].endswith("_READY"), result1
    assert result1["completed_generations"] == 2
    assert result1["runner_status"] == "bounded_cycle_stopped"
    assert result1["stop_reason"] == "maximum_generations_reached"
    state1 = read_json(root / "indra_qi_bounded_cycle_state_v0_12.json")
    ledger1 = records(root / "indra_qi_bounded_cycle_ledger_v0_12.jsonl")
    assert state1["completed_generations"] == 2
    assert len(ledger1) == 2
    assert ledger1[-1]["prev_record_digest"] == ledger1[-2]["record_digest"]

    source2 = current_source(root)
    plan2 = build_plan(
        root=root,
        source=source2,
        runner_id="bounded-runner-two",
        generation=2,
        maximum=2,
        suffix="g2",
    )
    blocked = run_cycle(root, plan2, source2)
    assert blocked["status"].endswith("_BLOCKED")
    assert "bounded_cycle_generation_index_at_or_above_maximum" in blocked["blockers"]
    assert blocked["v0_8_ready"] is False
    assert len(records(root / "indra_qi_bounded_cycle_ledger_v0_12.jsonl")) == 2


def check_convergence(base: pathlib.Path) -> None:
    root = base / "convergence"
    source = prepare_source(root, "convergence")
    plan = build_plan(
        root=root,
        source=source,
        runner_id="bounded-runner-converge",
        generation=0,
        maximum=3,
        suffix="converge",
        convergence_policy={
            "maximum_observation_debt": 1.0,
            "minimum_recoverability_reserve": 0.0,
            "maximum_intervention_residue": 1.0,
        },
    )
    result = run_cycle(root, plan, source)
    assert result["status"].endswith("_READY"), result
    assert result["runner_status"] == "bounded_cycle_stopped"
    assert result["stop_reason"] == "dynamic_world_convergence_reached"
