#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

EARLY = [
    (
        "runtime.v01_plan_os_replan_bound_synthesis",
        "scripts/check_plan_os_replan_bound_synthesis_v0_1.py",
        "plan-os-v01.log",
    ),
    (
        "runtime.v02_plan_os_qi_conditioned_nonmarkov_replan",
        "scripts/check_plan_os_qi_conditioned_nonmarkov_replan_v0_2.py",
        "plan-os-v02.log",
    ),
    (
        "runtime.v03_plan_os_next_cycle_basis_compiler_adapter",
        "scripts/check_plan_os_next_cycle_basis_compiler_adapter_v0_3.py",
        "plan-os-v03.log",
    ),
]

CHECKS = [
    "scripts/check_plan_os_closed_loop_replan_intake_adapter_v0_4.py",
    "scripts/check_plan_os_generational_replan_cycle_driver_v0_5.py",
    "scripts/check_plan_os_bounded_multi_generation_supervisor_v0_6.py",
    "scripts/check_plan_os_external_resume_handover_reentry_v0_7.py",
    "scripts/check_plan_os_reentry_ownership_continuity_v0_8.py",
    "scripts/check_plan_os_v0_9.py",
    "scripts/check_plan_os_v0_10.py",
    "scripts/check_plan_os_v0_11.py",
    "scripts/check_plan_os_v0_12.py",
    "scripts/check_plan_os_v0_13.py",
    "scripts/check_plan_os_v0_14.py",
    "scripts/check_plan_os_v0_15.py",
    "scripts/check_plan_os_v0_16.py",
    "scripts/check_plan_os_v0_17.py",
    "scripts/check_planos_vacuum_expectation_learning_replan_intake_v0_18.py",
    "scripts/check_planos_history_qi_candidate_generation_v0_19.py",
    "scripts/check_planos_hysteresis_constraint_decision_handoff_v0_20.py",
    "scripts/check_planos_selected_candidate_next_cycle_synthesis_v0_21.py",
    "scripts/check_planos_compiler_materialization_v0_22.py",
    "scripts/check_planos_activation_admission_actos_handoff_v0_23.py",
]


def run_logged(module: str, check: str, log_name: str) -> int:
    log_path = ROOT / log_name
    with log_path.open("w", encoding="utf-8") as log:
        runtime_result = subprocess.run(
            [sys.executable, "-m", module],
            cwd=ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        if runtime_result.returncode != 0:
            return runtime_result.returncode
        check_result = subprocess.run(
            [sys.executable, check],
            cwd=ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        return check_result.returncode


def main() -> int:
    failures: list[str] = []

    for module, check, log_name in EARLY:
        if run_logged(module, check, log_name) != 0:
            failures.append(check)

    for check in CHECKS:
        result = subprocess.run([sys.executable, check], cwd=ROOT)
        if result.returncode != 0:
            failures.append(check)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: PlanOS v0.1-v0.23 validation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
