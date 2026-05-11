#!/usr/bin/env python3
"""
validate_paramita_repair_router_fixtures_v0_1.py

Stdlib-only fixture validator for the minimal Paramita Repair Router.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "specs" / "paramita_repair_router_fixtures_v0_1.json"
ROUTER_PATH = ROOT / "examples" / "paramita_repair_router_minimal.py"


def load_router() -> Any:
    module_name = "paramita_repair_router_minimal"
    spec = importlib.util.spec_from_file_location(module_name, ROUTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load router module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def validate_fixture(router: Any, fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    fixture_id = fixture["id"]
    inp = router.ParamitaRouterInput(**fixture["input"])
    out = router.route(inp)
    data = dataclasses.asdict(out)
    expected = fixture["expected"]

    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{fixture_id}: {key} expected {value!r}, got {data.get(key)!r}")

    if data.get("execution_authority_granted") is not False:
        errors.append(f"{fixture_id}: execution_authority_granted must be false")
    return errors


def main() -> int:
    if not FIXTURE_PATH.is_file():
        print(f"ERROR: missing fixture file: {FIXTURE_PATH.relative_to(ROOT)}")
        return 1

    router = load_router()
    fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    for fixture in fixture_data.get("fixtures", []):
        errors.extend(validate_fixture(router, fixture))

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Paramita Repair Router fixtures validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
