#!/usr/bin/env python3
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON_ENV = os.environ.copy()
PYTHON_ENV["PYTHONPATH"] = os.pathsep.join(
    part for part in (str(ROOT), PYTHON_ENV.get("PYTHONPATH", "")) if part
)

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
    "scripts/check_planos_qi_blocker_foresight_plan_gate_v0_24.py",
    "scripts/check_planos_path_integral_candidate_weighting_v0_25.py",
    "scripts/check_planos_weighted_decision_evidence_handoff_v0_26.py",
    "scripts/check_planos_decision_review_intake_v0_27.py",
    "scripts/check_planos_decisionos_selection_request_v0_28.py",
    "scripts/check_planos_decisionos_selection_receipt_intake_v0_29.py",
    "scripts/check_planos_selected_candidate_synthesis_request_v0_30.py",
    "scripts/check_planos_selected_candidate_synthesis_receipt_v0_31.py",
    "scripts/check_planos_selected_candidate_materialization_preflight_v0_32.py",
    "scripts/check_planos_materialization_authorization_request_v0_33.py",
    "scripts/check_planos_materialization_authorization_request_receipt_v0_34.py",
    "scripts/check_planos_materialization_authorization_grant_v0_35.py",
    "scripts/check_planos_materialization_execution_receipt_v0_36.py",
    "scripts/check_planos_activation_authorization_request_v0_37.py",
    "scripts/check_planos_activation_authorization_grant_v0_38.py",
    "scripts/check_planos_actos_invocation_receipt_v0_39.py",
    "scripts/check_planos_literature_grounded_selective_foresight_gate_v0_40.py",
    "scripts/check_planos_execution_authorization_request_v0_41.py",
    "scripts/check_planos_execution_authorization_grant_v0_42.py",
    "scripts/check_planos_execution_receipt_v0_43.py",
    "scripts/check_planos_external_commit_authorization_request_v0_44.py",
    "scripts/check_planos_external_commit_authorization_grant_v0_45.py",
    "scripts/check_planos_external_commit_receipt_v0_46.py",
    "scripts/check_planos_external_commit_closeout_receipt_v0_47.py",
    "scripts/check_planos_memory_overwrite_authorization_request_v0_48.py",
    "scripts/check_planos_memory_overwrite_authorization_grant_v0_49.py",
    "scripts/check_planos_memory_overwrite_receipt_v0_50.py",
    "scripts/check_planos_memory_overwrite_closeout_receipt_v0_51.py",
    "scripts/check_planos_truth_authority_authorization_request_v0_52.py",
    "scripts/check_planos_truth_authority_authorization_grant_v0_53.py",
    "scripts/check_planos_truth_authority_receipt_v0_54.py",
    "scripts/check_planos_truth_authority_closeout_receipt_v0_55.py",
    "scripts/check_planos_blocker_release_authorization_request_v0_56.py",
    "scripts/check_planos_blocker_release_authorization_grant_v0_57.py",
    "scripts/check_planos_blocker_release_receipt_v0_58.py",
    "scripts/check_planos_blocker_release_closeout_receipt_v0_59.py",
    "scripts/check_planos_next_cycle_admission_request_v0_60.py",
    "scripts/check_planos_next_cycle_admission_grant_v0_61.py",
    "scripts/check_planos_next_cycle_start_receipt_v0_62.py",
    "scripts/check_planos_next_cycle_closeout_receipt_v0_63.py",
    "scripts/check_planos_subsequent_cycle_replan_request_v0_64.py",
    "scripts/check_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65.py",
    "scripts/check_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66.py",
    "scripts/check_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67.py",
    "scripts/check_planos_subsequent_cycle_candidate_review_request_v0_68.py",
]

SUPPORTED_PLANOS_VALIDATION_RANGES = (
    "v0.1-v0.33",
    "v0.1-v0.34",
    "v0.1-v0.35",
    "v0.1-v0.36",
    "v0.1-v0.37",
    "v0.1-v0.38",
    "v0.1-v0.39",
    "v0.1-v0.40",
    "v0.1-v0.41",
    "v0.1-v0.42",
    "v0.1-v0.43",
    "v0.1-v0.44",
    "v0.1-v0.45",
    "v0.1-v0.46",
    "v0.1-v0.47",
    "v0.1-v0.48",
    "v0.1-v0.49",
    "v0.1-v0.50",
    "v0.1-v0.51",
    "v0.1-v0.52",
    "v0.1-v0.53",
    "v0.1-v0.54",
    "v0.1-v0.55",
    "v0.1-v0.56",
    "v0.1-v0.57",
    "v0.1-v0.58",
    "v0.1-v0.59",
    "v0.1-v0.60",
    "v0.1-v0.61",
    "v0.1-v0.62",
    "v0.1-v0.63",
    "v0.1-v0.64",
    "v0.1-v0.65",
    "v0.1-v0.66",
    "v0.1-v0.67",
    "v0.1-v0.68",
)


def run_logged(module: str, check: str, log_name: str) -> int:
    log_path = ROOT / log_name
    with log_path.open("w", encoding="utf-8") as log:
        runtime_result = subprocess.run(
            [sys.executable, "-m", module],
            cwd=ROOT,
            env=PYTHON_ENV,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        if runtime_result.returncode != 0:
            return runtime_result.returncode
        check_result = subprocess.run(
            [sys.executable, check],
            cwd=ROOT,
            env=PYTHON_ENV,
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
        result = subprocess.run([sys.executable, check], cwd=ROOT, env=PYTHON_ENV)
        if result.returncode != 0:
            failures.append(check)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: PlanOS v0.1-v0.68 validation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
