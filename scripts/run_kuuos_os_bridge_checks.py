#!/usr/bin/env python3
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = os.environ.copy()
ENV["PYTHONPATH"] = os.pathsep.join(
    part for part in (str(ROOT), ENV.get("PYTHONPATH", "")) if part
)

CHECKS = [
    "scripts/validate_kuuos_two_truths_os_bridge_v0_1.py",
    "scripts/validate_kuuos_dependent_origination_os_bridge_v0_1.py",
    "scripts/validate_kuuos_indranet_os_dependency_bridge_v0_1.py",
    "scripts/validate_kuuos_gauge_os_transport_bridge_v0_1.py",
    "scripts/validate_kuuos_sheaf_os_gluing_bridge_v0_1.py",
    "scripts/validate_kuuos_cech_obstruction_os_bridge_v0_1.py",
    "scripts/validate_kuuos_descent_os_bridge_v0_1.py",
    "scripts/validate_kuuos_hyperdescent_os_bridge_v0_1.py",
    "scripts/validate_kuuos_infinity_topos_os_bridge_v0_1_min.py",
    "scripts/validate_kuuos_cohesive_os_bridge_v0_1_min.py",
    "scripts/validate_kuuos_differential_cohesive_os_bridge_v0_1_min.py",
    "scripts/validate_kuuos_jet_stability_os_bridge_v0_1_min.py",
    "scripts/validate_kuuos_variational_stability_os_bridge_v0_1_min.py",
    "scripts/validate_kuuos_policy_barrier_os_bridge_v0_1_min.py",
    "scripts/validate_kuuos_selector_boundary_os_bridge_v0_1_min.py",
]


def main() -> int:
    failures: list[str] = []

    for relative in CHECKS:
        path = ROOT / relative
        if not path.is_file():
            print(f"FAIL: missing validator: {relative}")
            failures.append(relative)
            continue

        print(f"\n>>> {relative}", flush=True)
        result = subprocess.run(
            [sys.executable, relative],
            cwd=ROOT,
            env=ENV,
        )
        if result.returncode != 0:
            failures.append(relative)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("\nPASS: KuuOS foundational and geometric OS bridge checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
