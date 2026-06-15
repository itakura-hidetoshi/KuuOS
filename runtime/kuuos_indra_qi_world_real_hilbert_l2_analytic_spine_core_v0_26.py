#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_indra_qi_world_real_hilbert_l2_analytic_spine_packet_v0_26 import *

def validate_ledger(
    records: list[dict[str, Any]],
    spine_id: str,
    world_model_id: str,
    blockers: list[str],
) -> list[dict[str, Any]]:
    previous = "GENESIS"
    run_ids: set[str] = set()
    source_digests: set[str] = set()
    report_digests: set[str] = set()
    for index, record in enumerate(records):
        run_id = str(record.get("analysis_run_id", ""))
        source_digest = str(record.get("source_world_state_digest", ""))
        report_sha = str(record.get("world_l2_embedding_report_digest", ""))
        valid = (
            record.get("version") == LEDGER_VERSION
            and valid_digest(record, "record_digest")
            and record.get("prev_record_digest") == previous
            and record.get("spine_id") == spine_id
            and record.get("world_model_id") == world_model_id
            and bool(run_id)
            and run_id not in run_ids
            and bool(source_digest)
            and source_digest not in source_digests
            and bool(report_sha)
            and report_sha not in report_digests
        )
        if record.get("_invalid") or not valid:
            blockers.append(f"world_l2_ledger_record_{index}_invalid")
        run_ids.add(run_id)
        source_digests.add(source_digest)
        report_digests.add(report_sha)
        previous = str(record.get("record_digest", ""))
    return records

def build_world_real_hilbert_l2_analytic_spine(
    *,
    runtime_context: Mapping[str, Any],
    world_l2_spine_plan: Mapping[str, Any],
    world_l2_spine_license: Mapping[str, Any],
    world_l2_embedding_report: Mapping[str, Any],
) -> Result:
    context = mapping(runtime_context)
    plan = dict(mapping(world_l2_spine_plan))
    license_value = mapping(world_l2_spine_license)
    report = dict(mapping(world_l2_embedding_report))
    blockers: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_world_real_hilbert_l2_spine_v0_26_enabled") is not True:
        blockers.append("world_l2_spine_enabled_not_true")
    if context.get("apply_indra_qi_world_real_hilbert_l2_spine_v0_26") is not True:
        blockers.append("world_l2_spine_apply_not_true")

    validate_plan(plan, blockers)
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    source = validate_source_world(world, plan, blockers)
    coordinates, projections = validate_report(report, plan, source, blockers)
    validate_license(license_value, plan, report, source, blockers)

    spine_id = str(plan.get("spine_id", ""))
    run_id = str(plan.get("analysis_run_id", ""))
    world_model_id = str(plan.get("world_model_id", ""))
    ledger_path = root / "indra_qi_world_real_hilbert_l2_analytic_spine_ledger_v0_26.jsonl"
    prior = validate_ledger(read_jsonl(ledger_path), spine_id, world_model_id, blockers)
    report_sha = str(report.get("world_l2_embedding_report_digest", ""))
    source_digest = str(source.get("world_digest", ""))
    if any(
        record.get("analysis_run_id") == run_id
        or record.get("source_world_state_digest") == source_digest
        or record.get("world_l2_embedding_report_digest") == report_sha
        for record in prior
    ):
        blockers.append("world_l2_spine_replay_detected")

    prior_state = read_json(root / "indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json")
    if prior_state and not valid_digest(prior_state, "world_l2_spine_state_digest"):
        blockers.append("world_l2_prior_state_digest_invalid")

    analysis = analyze_embedding(coordinates, projections, report, plan, source)
    decision, reason = evaluate_analysis(analysis, blockers)
    if decision not in DECISIONS:
        blockers.append("world_l2_decision_invalid")
        decision = "quarantine_recommended"
        reason = "decision_outside_closed_set"
    if blockers:
        decision = "quarantine_recommended"
        reason = "fail_closed_on_validation_or_integrity_loss"

    return finalize_world_l2_spine(
        root=root,
        plan=plan,
        license_value=license_value,
        report=report,
        source=source,
        coordinates=coordinates,
        projections=projections,
        analysis=analysis,
        decision=decision,
        reason=reason,
        blockers=blockers,
        prior=prior,
        prior_state=prior_state,
        report_sha=report_sha,
        source_digest=source_digest,
    )
