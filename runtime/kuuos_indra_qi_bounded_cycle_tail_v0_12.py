#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import mapping, valid_digest
from runtime.kuuos_indra_qi_bounded_cycle_link_v0_12 import compose, run
from runtime.kuuos_indra_qi_bounded_cycle_plans_v0_12 import build_loop_plan, dynamic_metrics
from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import latest_matching, read_json, records
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import dynamic_world_state_digest
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import compute_indra_qi_world_state_digest


def _prepare(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    license_value: Mapping[str, Any],
    source: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    loop_plan = build_loop_plan(
        plan=plan,
        world=read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json"),
        handoff=mapping(source.get("bridge_handoff")),
        bridge_record=mapping(source.get("bridge_record")),
        bridge_ledger=mapping(source.get("bridge_ledger")),
        cycle=mapping(source.get("cycle_state")),
        seed=mapping(source.get("cycle_seed")),
    )
    nested = dict(mapping(license_value.get("v0_11_license_template")))
    nested["bound_loop_plan_digest"] = loop_plan["loop_plan_digest"]
    return loop_plan, nested


def build_tail(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    license_value: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    output: dict[str, Any] = {
        "invoked": False,
        "ready": False,
        "target_child_runtime_root": "",
    }
    if blockers:
        return output
    loop_plan, nested = _prepare(
        root=root,
        plan=plan,
        license_value=license_value,
        source=source,
    )
    output["invoked"] = True
    result = run(
        compose(
            runtime_root=str(root),
            loop_plan=loop_plan,
            loop_license=nested,
        )
    )
    output["target_child_runtime_root"] = str(result.get("child_runtime_root", ""))
    if not str(result.get("status", "")).endswith("_READY"):
        blockers.append("bounded_cycle_tail_not_ready")
        blockers.extend(
            f"bounded_cycle_tail:{value}"
            for value in result.get("blockers", [])
            if isinstance(value, str)
        )
        return output
    output["ready"] = True
    return output
