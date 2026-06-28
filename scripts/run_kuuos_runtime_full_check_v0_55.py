#!/usr/bin/env python3
from __future__ import annotations

"""Cumulative KuuOS runtime validation root.

The filename is retained for compatibility with existing workflows and external
callers.  The actual validation frontier follows the integrated `main` branch
through KuuOS Self-Organizing Improvement Loop v0.78.

This runner executes validators in dependency order and stops at the first
failure.  A successful run is an integrity receipt for the checked repository
surfaces; it is not truth, external theorem acceptance, institutional approval,
or unrestricted execution authority.
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


CURRENT_RUNTIME_FRONTIER = "v0.78"

VALIDATORS_AFTER_V055: tuple[str, ...] = (
    # WORLD continuation with runtime-facing static validators.
    "scripts/check_world_kuu_vacuum_araki_hessian_physical_realization_v0_56.py",
    "scripts/check_world_four_great_phase_dynamics_v0_59.py",
    # Gauge-field self-organization and governed evidence review.
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
    # Module-bundle and MemoryOS production chain.
    "scripts/check_kuuos_module_bundle_v070.py",
    "scripts/check_kuuos_noncommutative_leibniz_v071.py",
    "scripts/check_kuuos_nonmarkov_memory_v072.py",
    "scripts/check_kuuos_memory_evaluation_v073.py",
    "scripts/check_kuuos_memory_review_v074.py",
    "scripts/check_kuuos_memory_application_v075.py",
    "scripts/check_kuuos_memory_rollback_v076.py",
    # Primary no-external-approval self-organization loop.
    "scripts/check_kuuos_self_organization_v078.py",
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


def _run_validator(relative_path: str, env: dict[str, str]) -> int:
    validator = ROOT / relative_path
    if not validator.is_file():
        print(
            f"[KuuOS runtime root] missing validator: {relative_path}",
            file=sys.stderr,
            flush=True,
        )
        return 1

    print(
        f"[KuuOS runtime root] running {relative_path}",
        flush=True,
    )
    completed = subprocess.run(
        [sys.executable, str(validator)],
        cwd=ROOT,
        env=env,
        check=False,
    )
    if completed.returncode != 0:
        print(
            "[KuuOS runtime root] failed "
            f"{relative_path} with exit code {completed.returncode}",
            file=sys.stderr,
            flush=True,
        )
        return completed.returncode or 1
    return 0


def _run_validators(paths: Sequence[str]) -> int:
    env = _runtime_environment()
    for relative_path in paths:
        result = _run_validator(relative_path, env)
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

    return _run_validators(VALIDATORS_AFTER_V055)


if __name__ == "__main__":
    raise SystemExit(main())
