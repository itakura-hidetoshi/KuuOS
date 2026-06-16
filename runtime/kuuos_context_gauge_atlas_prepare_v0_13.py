from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_adapter_capability_gauge_model_v0_6 import context_signature
from runtime.kuuos_context_gauge_atlas_basis_v0_13 import empty_bundle
from runtime.kuuos_context_gauge_atlas_license_check_v0_13 import check_license
from runtime.kuuos_context_gauge_atlas_paths_v0_13 import paths
from runtime.kuuos_context_gauge_atlas_plan_check_v0_13 import check_plan
from runtime.kuuos_context_gauge_atlas_result_v0_13 import replay_result
from runtime.kuuos_context_gauge_atlas_types_v0_13 import BUNDLE_VERSION, contains_graph_keys, integer, mapping, plan_digest, read_json, read_jsonl, safe_root, sha, valid_digest
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import normalize_sources
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_horizon_gauge_arbitration_upstream_v0_12 import load_upstream


def prepare_atlas(*, runtime_context: Mapping[str, Any], source_packets: list[Mapping[str, Any]], root_principles_packet: Mapping[str, Any], adapter_registry: Mapping[str, Any], atlas_plan: Mapping[str, Any], atlas_license: Mapping[str, Any]) -> dict[str, Any]:
    context = mapping(runtime_context)
    sources = [dict(mapping(item)) for item in source_packets]
    root_packet = mapping(root_principles_packet)
    registry = mapping(adapter_registry)
    plan = mapping(atlas_plan)
    license_packet = mapping(atlas_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    p = paths(root)
    current = load_upstream(p, str(plan.get("agent_id", "")))
    atlas_state = read_json(p["atlas_state"])
    atlas_bundle = read_json(p["atlas_bundle"]) or empty_bundle(str(plan.get("agent_id", "")))
    ledger = read_jsonl(p["atlas_ledger"])
    run_id = str(plan.get("atlas_run_id", ""))
    source_batch = batch_digest(sources)
    committed = next((row for row in reversed(ledger) if row.get("phase") == "committed" and row.get("atlas_run_id") == run_id), None)
    replay = None
    if committed is not None:
        if committed.get("atlas_plan_digest") == plan.get("atlas_plan_digest"):
            replay = replay_result(committed, root, p)
        else:
            blockers.append("atlas_run_id_reused_with_different_plan")
    pending = next((row for row in reversed(ledger) if row.get("phase") == "pending" and row.get("atlas_run_id") == run_id), None)
    if pending is not None:
        warnings.append("recovering_pending_atlas_run")
    if any(row.get("_invalid") for row in ledger):
        blockers.append("atlas_ledger_invalid")
    if context.get("context_gauge_atlas_enabled") is not True:
        blockers.append("context_gauge_atlas_enabled_not_true")
    if context.get("execute_one_atlas_cycle") is not True:
        blockers.append("execute_one_atlas_cycle_not_true")
    if contains_graph_keys(sources) or contains_graph_keys(registry):
        blockers.append("graph_semantics_present")
    if atlas_bundle.get("version") != BUNDLE_VERSION or not valid_digest(atlas_bundle, "atlas_bundle_digest"):
        blockers.append("atlas_bundle_invalid")
    if atlas_bundle.get("agent_id") != plan.get("agent_id"):
        blockers.append("atlas_bundle_agent_mismatch")
    if replay is None and not blockers and pending is None:
        check_plan(plan=plan, atlas_state=atlas_state, atlas_bundle=atlas_bundle, source_batch_digest=source_batch, root_digest=root_packet.get("root_principles_digest", ""), registry_digest=registry.get("adapter_registry_digest", ""), blockers=blockers)
        check_license(license_packet=license_packet, plan=plan, atlas_bundle=atlas_bundle, source_batch_digest=source_batch, root_digest=root_packet.get("root_principles_digest", ""), registry_digest=registry.get("adapter_registry_digest", ""), blockers=blockers)
    elif replay is None and not blockers:
        if plan.get("atlas_plan_digest") != plan_digest(plan):
            blockers.append("atlas_plan_digest_invalid")
        if pending.get("atlas_plan_digest") != plan.get("atlas_plan_digest"):
            blockers.append("pending_atlas_plan_digest_mismatch")
        if pending.get("source_batch_digest") != source_batch:
            blockers.append("pending_source_batch_digest_mismatch")
    normalized = normalize_sources(sources) if not blockers else {}
    context_key, signature = context_signature(sources, normalized) if not blockers else ("", {})
    cycle_index = integer(pending.get("cycle_index"), 0) if pending is not None else integer(atlas_state.get("cycle_index"), 0) + 1
    packet_id = "kuuos-context-atlas-" + sha({"run": run_id, "source_batch": source_batch, "cycle": cycle_index})[:18]
    return {"context": context, "sources": sources, "root_packet": root_packet, "registry": registry, "plan": plan, "license": license_packet, "blockers": blockers, "warnings": warnings, "root": root, "paths": p, "current": current, "atlas_state": atlas_state, "atlas_bundle": atlas_bundle, "ledger": ledger, "run_id": run_id, "source_batch": source_batch, "pending": pending, "recovered_pending": pending is not None, "replay": replay, "context_key": context_key, "context_signature": signature, "cycle_index": cycle_index, "packet_id": packet_id}
