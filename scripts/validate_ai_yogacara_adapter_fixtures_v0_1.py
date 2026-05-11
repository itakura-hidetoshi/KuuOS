#!/usr/bin/env python3
"""
validate_ai_yogacara_adapter_fixtures_v0_1.py

Stdlib-only fixture validator for the minimal AI Yogacara Runtime Adapter.

No external dependencies and no external AI API calls.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "specs" / "ai_yogacara_adapter_fixtures_v0_1.json"
ADAPTER_PATH = ROOT / "examples" / "ai_yogacara_runtime_adapter_minimal.py"


def load_adapter() -> Any:
    module_name = "ai_yogacara_runtime_adapter_minimal"
    spec = importlib.util.spec_from_file_location(module_name, ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load adapter module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def require_subset(actual: list[str], required: list[str], label: str, fixture_id: str) -> list[str]:
    errors: list[str] = []
    actual_set = set(actual)
    for item in required:
        if item not in actual_set:
            errors.append(f"{fixture_id}: missing {label}: {item}")
    return errors


def validate_fixture(adapter: Any, fixture: dict[str, Any]) -> list[str]:
    fixture_id = fixture["id"]
    expected = fixture["expected"]
    inp = adapter.AdapterInput(
        request_id=fixture_id,
        ai_system="GPT",
        model_or_agent_id="fixture-test-agent",
        raw_output_text=fixture["raw_output_text"],
        user_world_context_ref="kuos_fixture_world",
        declared_task_scope="fixture_validation",
        control_surface_ref="interface_level",
    )
    out = adapter.adapt(inp)
    data = dataclasses.asdict(out)

    errors: list[str] = []
    if data.get("raw_output_status") != expected["raw_output_status"]:
        errors.append(f"{fixture_id}: raw_output_status expected {expected['raw_output_status']} got {data.get('raw_output_status')}")
    if data.get("authority_granted") != expected["authority_granted"]:
        errors.append(f"{fixture_id}: authority_granted expected {expected['authority_granted']} got {data.get('authority_granted')}")

    errors += require_subset(
        data.get("meta_manas_signals", []),
        expected.get("required_meta_manas_signals", []),
        "meta_manas_signal",
        fixture_id,
    )
    errors += require_subset(
        data.get("seed_classifications", []),
        expected.get("required_seed_classifications", []),
        "seed_classification",
        fixture_id,
    )
    errors += require_subset(
        data.get("allowed_next_status", []),
        expected.get("required_allowed_next_status", []),
        "allowed_next_status",
        fixture_id,
    )
    return errors


def main() -> int:
    if not FIXTURE_PATH.is_file():
        print(f"ERROR: missing fixture file: {FIXTURE_PATH.relative_to(ROOT)}")
        return 1
    fixture_data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    adapter = load_adapter()

    errors: list[str] = []
    for fixture in fixture_data.get("fixtures", []):
        errors += validate_fixture(adapter, fixture)

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print("PASS: AI Yogacara adapter fixtures validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
