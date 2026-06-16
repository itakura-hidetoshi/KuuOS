from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import PLAN_VERSION, REQUIRED_BOUNDARY, clamp, integer, mapping, plan_digest


def check_plan(*, plan: Mapping[str, Any], atlas_state: Mapping[str, Any], atlas_bundle: Mapping[str, Any], source_batch_digest: str, root_digest: str, registry_digest: str, blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("atlas_plan_version_invalid")
    if plan.get("atlas_plan_digest") != plan_digest(plan):
        blockers.append("atlas_plan_digest_invalid")
    for field in ("atlas_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"atlas_plan_{field}_missing")
    expected = {
        "expected_source_batch_digest": source_batch_digest,
        "expected_root_principles_digest": root_digest,
        "expected_adapter_registry_digest": registry_digest,
        "expected_previous_atlas_state_digest": atlas_state.get("atlas_state_digest", ""),
        "expected_previous_atlas_bundle_digest": atlas_bundle.get("atlas_bundle_digest", ""),
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"atlas_plan_{field}_mismatch")
    for field, value in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not value:
            blockers.append(f"atlas_boundary_{field}_invalid")
    for field in ("minimum_chart_overlap", "target_chart_retention", "transition_phase_gain", "plural_atlas_curvature_threshold", "minimum_horizon_weight"):
        raw = plan.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0.0 <= float(raw) <= 1.0:
            blockers.append(f"atlas_plan_{field}_invalid")
    if clamp(plan.get("minimum_horizon_weight")) > 1.0 / 3.0:
        blockers.append("atlas_minimum_horizon_weight_too_large")
    for field in ("max_atlas_holonomy", "max_atlas_outcomes"):
        if integer(plan.get(field), 0) <= 0:
            blockers.append(f"atlas_plan_{field}_invalid")
