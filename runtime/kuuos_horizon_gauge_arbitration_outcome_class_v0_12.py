#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import clamp

def classify_commitment_outcome(*, child_horizon_outcome: Mapping[str, Any], decision: Mapping[str, Any], plan: Mapping[str, Any]) -> str:
    progress = clamp(child_horizon_outcome.get("commitment_progress_score"))
    recovery = clamp(child_horizon_outcome.get("recovery_cost"))
    terminal = clamp(child_horizon_outcome.get("terminal_section_ratio"))
    mode = str(child_horizon_outcome.get("child_policy_mode", ""))
    curvature = clamp(decision.get("arbitration_curvature"))
    if recovery >= clamp(plan.get("repair_outcome_threshold"), 0.25) and recovery > progress:
        return "repairing"
    if terminal >= clamp(plan.get("stabilizing_terminal_threshold"), 0.5) and mode == "exploit":
        return "stabilizing"
    if progress >= clamp(plan.get("progressing_outcome_threshold"), 0.25):
        return "progressing"
    if curvature >= clamp(plan.get("plural_conflict_curvature_threshold"), 0.25):
        return "plural_conflict"
    if mode == "experiment":
        return "exploring"
    return "holding"
