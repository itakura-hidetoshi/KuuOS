from __future__ import annotations

import runtime.v05_plan_os_generational_replan_cycle_driver as driver

_original_initial_plan = driver.build_next_cycle_initial_plan_state
_original_generation_receipt = driver.build_generational_cycle_receipt
_installed = False


def install_generational_entry_adapter() -> None:
    global _installed
    if _installed:
        return

    def monotone_initial_plan(**kwargs):
        kwargs["now_ms"] = min(int(kwargs.get("now_ms", 500_000)), 500_000)
        return _original_initial_plan(**kwargs)

    def canonical_activation_projection(**kwargs):
        activation = dict(kwargs["plan_activation_receipt"])
        activation["plan_phase_activation_receipt_digest"] = activation[
            "plan_activation_receipt_digest"
        ]
        kwargs["plan_activation_receipt"] = activation
        return _original_generation_receipt(**kwargs)

    driver.build_next_cycle_initial_plan_state = monotone_initial_plan
    driver.build_generational_cycle_receipt = canonical_activation_projection
    _installed = True


def run_kernel() -> dict:
    install_generational_entry_adapter()
    result = driver.run_kernel()
    from runtime.v06_plan_os_bounded_multi_generation_supervisor import (
        run_kernel as run_next,
    )

    next_result = run_next()
    if next_result.get("status") != "PLAN_OS_BOUNDED_MULTI_GENERATION_SUPERVISOR_V0_6_OK":
        raise AssertionError(next_result)
    return result
