"""PlanOS: bind v0.27 EffectGuard obligations to original committed steps.

The final PlanOS snapshot is validated by its original state validator
first. No change to the plan, step graph, license or actuator is performed.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, UnavailableSource, copied_state, fail, field, truth, natural,
    string, plain_list, finalize,
)

OS_NAME = "PlanOS"


def audit_native_plan_effect_guards(state: Any):
    """Local source-linked checks; does not grant execution authority."""
    try:
        plan = copied_state(OS_NAME, state)
        steps = plain_list(plan, "steps", "PlanOS")
        if not steps:
            raise UnavailableSource("PlanOS:steps_not_observed")
        if truth(field(plan, "guard_summary", "PlanOS"),
                 "all_effects_guarded", "PlanOS.guard_summary") is not True:
            raise UnavailableSource("PlanOS:source_guard_summary_failed", BLOCKED)
        if truth(field(plan, "checkpoint_summary", "PlanOS"),
                 "all_effects_have_checkpoint", "PlanOS.checkpoint_summary") is not True:
            raise UnavailableSource("PlanOS:source_checkpoint_summary_failed", BLOCKED)
        if truth(field(plan, "verification_summary", "PlanOS"),
                 "plan_verified", "PlanOS.verification_summary") is not True:
            raise UnavailableSource("PlanOS:plan_not_verified", BLOCKED)
        boundary = field(plan, "boundary", "PlanOS")
        not_execution = truth(boundary, "plan_is_not_execution", "PlanOS.boundary")
        by_id: dict[str, dict] = {}
        for item in steps:
            if type(item) is not dict:
                raise UnavailableSource("PlanOS:step_plain_object_required", BLOCKED)
            ident = string(item, "step_id", "PlanOS.step")
            if ident in by_id:
                raise UnavailableSource("PlanOS:duplicate_step_id", BLOCKED)
            by_id[ident] = item
        projections: list[dict] = []
        paths = [
            "PlanOS.current_phase", "PlanOS.plan_state_digest",
            "PlanOS.guard_summary.all_effects_guarded",
            "PlanOS.checkpoint_summary.all_effects_have_checkpoint",
            "PlanOS.verification_summary.plan_verified",
            "PlanOS.boundary.plan_is_not_execution",
        ]
        for step in steps:
            if not truth(step, "effectful", "PlanOS.step"):
                continue
            ident = string(step, "step_id", "PlanOS.step")
            string(step, "step_digest", "PlanOS.step")
            rank = natural(step, "rank", "PlanOS.step")
            stop = plain_list(step, "stop_condition_digests", "PlanOS.step")
            rollback_id = string(step, "rollback_step_id", "PlanOS.step",
                                 empty_allowed=True)
            rollback_step = by_id.get(rollback_id)
            rollback = False
            if rollback_step is not None:
                rollback = (string(rollback_step, "step_class", "PlanOS.step")
                            == "repair"
                            and natural(rollback_step, "rank", "PlanOS.step") > rank)
            checkpoint = False
            for later in steps:
                cls = string(later, "step_class", "PlanOS.step")
                depends_on = plain_list(later, "depends_on", "PlanOS.step")
                later_rank = natural(later, "rank", "PlanOS.step")
                if (cls in ("observe", "verify") and ident in depends_on
                        and later_rank > rank):
                    checkpoint = True
            projections.append({
                "effectful": True, "rollbackPresent": rollback,
                "humanReviewRequired": truth(step, "requires_human_review", "PlanOS.step"),
                "externalLicenseRequired": truth(step, "requires_external_license", "PlanOS.step"),
                "stopConditionPresent": bool(stop),
                "checkpointPresent": checkpoint,
                "planIsExecution": not not_execution,
            })
            paths.extend([
                "PlanOS.steps[" + ident + "].step_digest",
                "PlanOS.steps[" + ident + "].rank",
                "PlanOS.steps[" + ident + "].rollback_step_id",
                "PlanOS.steps[" + ident + "].stop_condition_digests",
                "PlanOS.steps[" + ident + "].requires_human_review",
                "PlanOS.steps[" + ident + "].requires_external_license",
                "PlanOS.steps[*].depends_on",
            ])
        if not projections:
            raise UnavailableSource("PlanOS:no_effectful_steps")
        return finalize(OS_NAME, plan, projections, paths)
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)


__all__ = ("OS_NAME", "audit_native_plan_effect_guards")
