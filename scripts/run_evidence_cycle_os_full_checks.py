#!/usr/bin/env python3
"""Run cumulative evidence-cycle checks through ActOS v0.12 policy activation authorization."""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
from collections.abc import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]

COMMANDS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "-m", "runtime.v01_act_os_authority_bound_invocation"),
    (sys.executable, "scripts/check_act_os_authority_bound_invocation_v0_1.py"),
    (sys.executable, "-m", "runtime.v02_act_os_replan_lineage_authority_envelope"),
    (sys.executable, "scripts/check_act_os_replan_lineage_authority_envelope_v0_2.py"),
    (sys.executable, "-m", "runtime.v01_observe_os_effect_grounded_observation"),
    (sys.executable, "scripts/check_observe_os_effect_grounded_observation_v0_1.py"),
    (sys.executable, "-m", "runtime.v02_observe_os_replan_lineage_observation_envelope"),
    (sys.executable, "scripts/check_observe_os_replan_lineage_observation_envelope_v0_2.py"),
    (sys.executable, "-m", "runtime.v01_verify_os_evidence_bound_verification"),
    (sys.executable, "scripts/check_verify_os_evidence_bound_verification_v0_1.py"),
    (sys.executable, "-m", "runtime.v02_verify_os_replan_lineage_verification_envelope"),
    (sys.executable, "scripts/check_verify_os_replan_lineage_verification_envelope_v0_2.py"),
    (sys.executable, "-m", "runtime.v01_learn_os_future_only_evidence_learning"),
    (sys.executable, "scripts/check_learn_os_future_only_evidence_learning_v0_1.py"),
    (sys.executable, "-m", "runtime.v02_learn_os_replan_lineage_future_only_learning_envelope"),
    (sys.executable, "scripts/check_learn_os_replan_lineage_future_only_learning_envelope_v0_2.py"),
    (sys.executable, "scripts/check_actos_activation_authorization_intake_v0_3.py"),
    (sys.executable, "scripts/check_actos_bounded_adapter_invocation_v0_4.py"),
    (sys.executable, "scripts/check_observeos_vacuum_expectation_intake_commit_receipt_v0_3.py"),
    (sys.executable, "scripts/check_observeos_world_host_effect_observation_v0_4.py"),
    (sys.executable, "scripts/check_verifyos_vacuum_expectation_commit_verification_receipt_v0_3.py"),
    (
        sys.executable,
        "scripts/check_verifyos_middle_way_conditional_continuity_verification_v0_4.py",
    ),
    (
        sys.executable,
        "scripts/check_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_planos_bounded_synthesis_receipt_kernel_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_bounded_plan_middle_way_verification_kernel_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_dukkha_reduction_claim_verification_kernel_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_supported_bounded_plan_materialization_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_preserving_adapter_binding_authorization_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_preserving_frontier_plan_activation_receipt_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_preserving_bounded_adapter_invocation_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_preserving_effect_commit_authorization_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_preserving_single_use_effect_commit_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_preserving_atomic_external_host_effect_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_observeos_dukkha_preserving_external_host_effect_observation_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_dukkha_preserving_observed_host_effect_verification_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_world_dukkha_preserving_verified_host_effect_disposition_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_world_dukkha_preserving_single_use_world_mutation_application_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_dukkha_preserving_world_postcondition_verification_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_world_dukkha_preserving_world_fact_confirmation_disposition_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_dukkha_preserving_world_causal_attribution_verification_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_v0_1.py",
    ),
    (sys.executable, "scripts/check_learnos_vacuum_expectation_verification_future_only_delta_v0_3.py"),
    (
        sys.executable,
        "scripts/check_learnos_dukkha_preserving_future_only_learning_maintenance_disposition_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_learnos_dukkha_preserving_future_only_maintenance_disposition_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_verifyos_dukkha_preserving_future_only_policy_activation_review_intake_v0_1.py",
    ),
    (
        sys.executable,
        "scripts/check_actos_dukkha_preserving_bounded_policy_activation_authorization_intake_v0_1.py",
    ),
)


def run_command(command: Sequence[str], env: dict[str, str]) -> int:
    print("\n>>> " + " ".join(command), flush=True)
    return subprocess.run(list(command), cwd=ROOT, env=env, check=False).returncode


def main() -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        item for item in (str(ROOT), env.get("PYTHONPATH", "")) if item
    )
    env.setdefault("PYTHONUNBUFFERED", "1")

    failures: list[tuple[Sequence[str], int]] = []
    for command in COMMANDS:
        code = run_command(command, env)
        if code != 0:
            failures.append((command, code))

    if failures:
        for command, code in failures:
            print(f"FAIL: {' '.join(command)} exited with {code}")
        return 1

    print(
        "\nPASS: Evidence Cycle OS validation completed through "
        "ActOS v0.12 bounded policy activation authorization"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
