"""ActOS: original authorization and host evidence, without fake job counts.

The real source has Boolean host *claims* that at most one job/slice ran,
and a license maximum, but does NOT furnish a Lean-certified numeric
jobsClaimed/slicesRun value. Preserve that obstruction as NO_DATA.
No new host job, invocation, approval, license or receipt is issued.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, NO_DATA, UnavailableSource, NativeOSBindingAudit,
    copied_state, fail, field, truth, string, natural, plain_list, require_match,
)
from runtime.kuuos_act_os_kernel_v0_1 import _validate_authorization
from runtime.kuuos_act_os_types_v0_1 import authorization_digest
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    license_digest, projection_digest, receipt_digest,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint

OS_NAME = "ActOS"


def audit_native_act_authorization(plan_state: Any, act_state: Any):
    try:
        plan = copied_state("PlanOS", plan_state)
        act = copied_state(OS_NAME, act_state)
        require_match(string(act, "source_plan_state_digest", "ActOS"),
                      string(plan, "plan_state_digest", "PlanOS"),
                      "ActOS:original_plan_state_identity")
        selected = field(act, "selected_step", "ActOS")
        step_id = string(act, "selected_step_id", "ActOS")
        matches = [step for step in plain_list(plan, "steps", "PlanOS")
                   if type(step) is dict and step.get("step_id") == step_id]
        if len(matches) != 1:
            raise UnavailableSource("ActOS:exact_selected_plan_step_missing", BLOCKED)
        require_match(selected, matches[0], "ActOS:original_selected_step")
        authorization = field(act, "step_authorization", "ActOS")
        license_packet = field(act, "host_license", "ActOS")
        projection = field(act, "host_projection", "ActOS")
        receipt = field(act, "host_receipt", "ActOS")
        require_match(string(authorization, "step_authorization_digest", "ActOS"),
                      authorization_digest(authorization), "ActOS:auth_digest")
        require_match(string(act, "step_authorization_digest", "ActOS"),
                      string(authorization, "step_authorization_digest", "ActOS"),
                      "ActOS:auth_binding")
        require_match(string(license_packet, "host_license_digest", "ActOS"),
                      license_digest(license_packet), "ActOS:license_digest")
        require_match(string(act, "host_license_digest", "ActOS"),
                      string(license_packet, "host_license_digest", "ActOS"),
                      "ActOS:license_binding")
        require_match(string(projection, "projection_digest", "ActOS"),
                      projection_digest(projection), "ActOS:projection_digest")
        require_match(string(act, "host_projection_digest", "ActOS"),
                      string(projection, "projection_digest", "ActOS"),
                      "ActOS:projection_binding")
        require_match(string(receipt, "host_receipt_digest", "ActOS"),
                      receipt_digest(receipt), "ActOS:receipt_digest")
        require_match(string(act, "host_receipt_digest", "ActOS"),
                      string(receipt, "host_receipt_digest", "ActOS"),
                      "ActOS:receipt_binding")
        if not truth(authorization, "single_use", "ActOS.authorization"):
            raise UnavailableSource("ActOS:authorization_not_single_use", BLOCKED)
        if not truth(authorization, "authorization_does_not_widen_license",
                     "ActOS.authorization"):
            raise UnavailableSource("ActOS:license_widening_claim", BLOCKED)
        if natural(license_packet, "max_jobs_per_invocation", "ActOS.license") != 1:
            raise UnavailableSource("ActOS:host_license_job_bound_invalid", BLOCKED)
        if not truth(receipt, "one_job_claimed_at_most", "ActOS.host_receipt"):
            raise UnavailableSource("ActOS:host_receipt_job_claim_not_bounded", BLOCKED)
        if not truth(receipt, "one_bounded_slice_run_at_most", "ActOS.host_receipt"):
            raise UnavailableSource("ActOS:host_receipt_slice_claim_not_bounded", BLOCKED)
        # Recheck native authorization at its historical phase event time.
        # This is a local replay check, never a current host permission grant.
        history = plain_list(act, "event_history", "ActOS")
        authorizations = [e for e in history if type(e) is dict
                          and e.get("target_phase") == "authorize"]
        if len(authorizations) != 1:
            raise UnavailableSource("ActOS:unique_original_authorization_event_required")
        at = natural(authorizations[0], "created_at_ms", "ActOS.event")
        try:
            _validate_authorization(act, authorization, license_packet, at)
        except (ValueError, TypeError, KeyError) as exc:
            raise UnavailableSource(
                "ActOS:original_authorization_replay:" + type(exc).__name__, BLOCKED
            ) from exc
        paths = (
            "PlanOS.plan_state_digest", "PlanOS.steps[*].step_digest",
            "ActOS.source_plan_state_digest", "ActOS.selected_step",
            "ActOS.step_authorization.single_use",
            "ActOS.step_authorization.authorization_does_not_widen_license",
            "ActOS.step_authorization.step_authorization_digest",
            "ActOS.host_license.host_license_digest",
            "ActOS.host_license.max_jobs_per_invocation",
            "ActOS.host_projection.projection_digest",
            "ActOS.host_receipt.host_receipt_digest",
            "ActOS.host_receipt.one_job_claimed_at_most",
            "ActOS.host_receipt.one_bounded_slice_run_at_most",
            "ActOS.event_history[target_phase=authorize].created_at_ms",
        )
        return NativeOSBindingAudit(
            os_name=OS_NAME, status=NO_DATA, source_digest=_fingerprint(act),
            source_field_paths=paths,
            checked_witnesses=0,
            issues=("ActOS:actual_jobsClaimed_numeric_witness_unavailable",
                    "ActOS:actual_slicesRun_numeric_witness_unavailable",
                    "ActOS:original_activation_receipt_issuer_unverified"),
            original_state_validated=True,
            source_bound_python_conditions_checked=False,
        )
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return fail(OS_NAME, "ActOS:native_source_exception:" + type(exc).__name__,
                    status=BLOCKED)


__all__ = ("OS_NAME", "audit_native_act_authorization")
