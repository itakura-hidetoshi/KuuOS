#!/usr/bin/env python3
from typing import Any, Mapping
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_horizon_gauge_arbitration_paths_v0_12 import paths, replay_result
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import mapping, read_jsonl, safe_root
from runtime.kuuos_horizon_gauge_arbitration_upstream_v0_12 import child_upstream, load_upstream

def prepare_base(*, runtime_context: Mapping[str, Any], source_packets: list[Mapping[str, Any]], root_principles_packet: Mapping[str, Any], adapter_registry: Mapping[str, Any], arbitration_plan: Mapping[str, Any], arbitration_license: Mapping[str, Any]) -> dict[str, Any]:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(arbitration_plan)
    license_packet = mapping(arbitration_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    p = paths(root)
    values = load_upstream(p, str(plan.get("agent_id", "")))
    upstream = child_upstream(values)
    ledger = read_jsonl(p["ledger"])
    run_id = str(plan.get("arbitration_run_id", ""))
    source_batch = batch_digest(sources)
    if any(row.get("_invalid") for row in ledger):
        blockers.append("arbitration_ledger_invalid")
    committed = next((row for row in reversed(ledger) if row.get("phase") == "committed" and row.get("arbitration_run_id") == run_id), None)
    replay = None
    if committed is not None:
        if committed.get("arbitration_plan_digest") == plan.get("arbitration_plan_digest"):
            replay = replay_result(committed, root, p)
        else:
            blockers.append("arbitration_run_id_reused_with_different_plan")
    pending = next((row for row in reversed(ledger) if row.get("phase") == "pending" and row.get("arbitration_run_id") == run_id), None)
    if pending is not None:
        warnings.append("recovering_pending_arbitration_run")
    return {"context": context, "sources": sources, "root_packet": root_packet, "registry": registry, "plan": plan, "license": license_packet, "blockers": blockers, "warnings": warnings, "root": root, "paths": p, "values": values, "upstream": upstream, "state": values["state"], "bundle": values["bundle"], "run_id": run_id, "source_batch": source_batch, "pending": pending, "replay": replay, "recovered_pending": pending is not None}
