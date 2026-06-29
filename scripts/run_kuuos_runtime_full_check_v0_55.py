#!/usr/bin/env python3
from __future__ import annotations

"""Cumulative KuuOS runtime validation root.

The filename is retained for compatibility with existing workflows and external
callers. The actual validation frontier follows the integrated `main` branch
through KuuOS Repository Atomic Checkpoint Creation v1.02.

The runner executes validators and focused unit-test modules in dependency order
and stops at the first failure. A successful run is an integrity receipt for the
checked repository surfaces. It is not truth, external theorem acceptance,
institutional approval, evidence of a live Git mutation, or unrestricted
execution authority.
"""

import os
import pathlib
import subprocess
import sys
from collections.abc import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_modular_evolution_mesh_v0_1 import (
    main as check_modular_evolution_mesh_v0_1,
)
from scripts.check_world_kuu_vacuum_information_geometry_v0_55 import (
    main as check_v055,
)
from scripts.run_kuuos_runtime_full_check_v0_54 import main as run_v054_full_check


CURRENT_RUNTIME_FRONTIER = "v1.02"

VALIDATORS_AFTER_V055: tuple[str, ...] = (
    "scripts/check_world_kuu_vacuum_araki_hessian_physical_realization_v0_56.py",
    "scripts/check_world_four_great_phase_dynamics_v0_59.py",
    "scripts/check_kuuos_gauge_field_self_organization_v0_60.py",
    "scripts/check_kuuos_os_associated_gauge_fields_v0_61.py",
    "scripts/check_kuuos_connection_improvement_candidate_v0_62.py",
    "scripts/check_kuuos_v063.py",
    "scripts/check_kuuos_evaluation_v064.py",
    "scripts/check_kuuos_staging_v065.py",
    "scripts/check_kuuos_shadow_v066.py",
    "scripts/check_kuuos_orbit_v067.py",
    "scripts/check_kuuos_evidence_v068.py",
    "scripts/check_kuuos_evidence_review_v069.py",
    "scripts/check_kuuos_module_bundle_v070.py",
    "scripts/check_kuuos_noncommutative_leibniz_v071.py",
    "scripts/check_kuuos_nonmarkov_memory_v072.py",
    "scripts/check_kuuos_memory_evaluation_v073.py",
    "scripts/check_kuuos_memory_review_v074.py",
    "scripts/check_kuuos_memory_application_v075.py",
    "scripts/check_kuuos_memory_rollback_v076.py",
    "scripts/check_kuuos_self_organization_v078.py",
    "scripts/check_kuuos_repository_alignment_v079.py",
    "scripts/check_kuuos_repository_normal_form_v080.py",
    "scripts/check_kuuos_repository_incremental_preservation_v081.py",
    "scripts/check_kuuos_repository_certificate_chain_v082.py",
    "scripts/check_kuuos_repository_git_revision_adapter_v083.py",
    "scripts/check_kuuos_repository_merge_certificate_v084.py",
    "scripts/check_kuuos_repository_revision_dag_v085.py",
    "scripts/check_kuuos_repository_frontier_certificate_v086.py",
    "scripts/check_kuuos_repository_self_evolution_v087.py",
    "scripts/check_kuuos_repository_self_evolution_shadow_v088.py",
    "scripts/check_kuuos_repository_evolution_admission_v089.py",
    "scripts/check_kuuos_repository_external_approval_v090.py",
    "scripts/check_kuuos_repository_application_authorization_v091.py",
    "scripts/check_kuuos_repository_atomic_application_v092.py",
    "scripts/check_kuuos_repository_commit_candidate_v093.py",
    "scripts/check_kuuos_repository_object_materialization_authorization_v094.py",
    "scripts/check_kuuos_repository_object_materialization_receipt_v095.py",
)

FRONTIER_STEPS_AFTER_V095: tuple[tuple[str, str], ...] = (
    (
        "scripts/check_kuuos_live_v096.py",
        "tests.test_kuuos_repository_reference_update_authorization_v0_96",
    ),
    (
        "scripts/check_kuuos_live_v097.py",
        "tests.test_kuuos_repository_atomic_reference_update_v0_97",
    ),
    (
        "scripts/check_kuuos_live_v098.py",
        "tests.test_kuuos_repository_reference_update_receipt_v0_98",
    ),
    (
        "scripts/check_kuuos_live_v099.py",
        "tests.test_kuuos_repository_reference_stability_v0_99",
    ),
    (
        "scripts/check_kuuos_live_v100.py",
        "tests.test_kuuos_repository_local_frontier_finality_v1_00",
    ),
    (
        "scripts/check_kuuos_live_v101.py",
        "tests.test_kuuos_repository_local_frontier_checkpoint_authorization_v1_01",
    ),
    (
        "scripts/check_kuuos_live_v102.py",
        "tests.test_kuuos_repository_atomic_checkpoint_creation_v1_02",
    ),
)


def _runtime_environment() -> dict[str, str]:
    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    root_text = str(ROOT)
    env["PYTHONPATH"] = (
        root_text
        if not current_pythonpath
        else os.pathsep.join((root_text, current_pythonpath))
    )
    env.setdefault("PYTHONUNBUFFERED", "1")
    return env


def _run_command(label: str, command: Sequence[str], env: dict[str, str]) -> int:
    print(f"[KuuOS runtime root] running {label}", flush=True)
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        env=env,
        check=False,
    )
    if completed.returncode != 0:
        print(
            "[KuuOS runtime root] failed "
            f"{label} with exit code {completed.returncode}",
            file=sys.stderr,
            flush=True,
        )
        return completed.returncode or 1
    return 0


def _run_validator(relative_path: str, env: dict[str, str]) -> int:
    validator = ROOT / relative_path
    if not validator.is_file():
        print(
            f"[KuuOS runtime root] missing validator: {relative_path}",
            file=sys.stderr,
            flush=True,
        )
        return 1
    return _run_command(relative_path, (sys.executable, str(validator)), env)


def _run_validators(paths: Sequence[str], env: dict[str, str]) -> int:
    for relative_path in paths:
        result = _run_validator(relative_path, env)
        if result != 0:
            return result
    return 0


def _run_frontier_steps(env: dict[str, str]) -> int:
    for validator_path, test_module in FRONTIER_STEPS_AFTER_V095:
        result = _run_validator(validator_path, env)
        if result != 0:
            return result
        result = _run_command(
            test_module,
            (sys.executable, "-m", "unittest", "-v", test_module),
            env,
        )
        if result != 0:
            return result
    return 0


def main() -> int:
    print(
        "[KuuOS runtime root] cumulative validation through "
        f"{CURRENT_RUNTIME_FRONTIER}",
        flush=True,
    )

    if run_v054_full_check() != 0:
        return 1
    if check_modular_evolution_mesh_v0_1() != 0:
        return 1
    if check_v055() != 0:
        return 1

    env = _runtime_environment()
    if _run_validators(VALIDATORS_AFTER_V055, env) != 0:
        return 1
    return _run_frontier_steps(env)


if __name__ == "__main__":
    raise SystemExit(main())
