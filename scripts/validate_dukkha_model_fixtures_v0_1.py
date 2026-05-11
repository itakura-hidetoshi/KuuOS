#!/usr/bin/env python3
"""
validate_dukkha_model_fixtures_v0_1.py

Stdlib-only fixture validator for the minimal KuuOS Dukkha Mathematical Model evaluator.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "specs" / "dukkha_model_fixtures_v0_1.json"
EVALUATOR_PATH = ROOT / "examples" / "dukkha_model_minimal.py"


def load_evaluator() -> Any:
    spec = importlib.util.spec_from_file_location("dukkha_model_minimal", EVALUATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load dukkha evaluator module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_fixture(evaluator: Any, fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    fixture_id = fixture["id"]
    inp = evaluator.DukkhaInput(**fixture["input"])
    out = evaluator.evaluate_dukkha(inp)
    data = dataclasses.asdict(out)
    expected = fixture["expected"]

    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{fixture_id}: {key} expected {value!r}, got {data.get(key)!r}")

    if data.get("dukkha_visible") is not True:
        errors.append(f"{fixture_id}: dukkha_visible must be true")
    if data.get("execution_authority_granted") is not False:
        errors.append(f"{fixture_id}: execution_authority_granted must be false")
    return errors


def main() -> int:
    if not FIXTURE_PATH.is_file():
        print(f"ERROR: missing fixture file: {FIXTURE_PATH.relative_to(ROOT)}")
        return 1

    evaluator = load_evaluator()
    fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    for fixture in fixture_data.get("fixtures", []):
        errors.extend(validate_fixture(evaluator, fixture))

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Dukkha model fixtures validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
