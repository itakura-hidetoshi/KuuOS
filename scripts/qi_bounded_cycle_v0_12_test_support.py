#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_bounded_cycle_runtime_v0_12 import build_cycle
from scripts.qi_bounded_cycle_license_v0_12_test_support import cycle_license
from scripts.qi_bounded_cycle_plan_v0_12_test_support import build_plan, prepare_source


def run_cycle(
    root: pathlib.Path,
    plan: dict[str, Any],
    source: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_cycle(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_bounded_generational_cycle_v0_12_enabled": True,
            "apply_indra_qi_bounded_generation_v0_12": True,
        },
        cycle_plan=plan,
        cycle_license=license_value or cycle_license(plan, source),
    ).to_dict()


__all__ = ["build_plan", "cycle_license", "prepare_source", "run_cycle"]
