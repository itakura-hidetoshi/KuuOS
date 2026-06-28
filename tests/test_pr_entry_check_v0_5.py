#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from run_pr_entry_check_v0_5 import CHECK_IDS, REQUIRED_MARKERS, build_commands
from select_impacted_checks import load_registry, select

REGISTRY = load_registry(ROOT / "ci/check_registry.yaml")
MIGRATED = {
    "world-v053-v059": ".github/workflows/world-v053-v059-main-validation.yml",
    "memoryos-world-observe-v039": ".github/workflows/memoryos-world-observe-intake-v0-39.yml",
}


def selected_ids(result: dict[str, object]) -> set[str]:
    checks = result["selected_checks"]
    assert isinstance(checks, list)
    return {str(item["id"]) for item in checks}


class PrEntryCheckV05Tests(unittest.TestCase):
    def test_fragments_are_loaded(self) -> None:
        self.assertIn("ci/check_registry.d/world_v053_v059_v0_5.json", REGISTRY["registry_fragments"])
        self.assertIn("ci/check_registry.d/memoryos_world_observe_v0_5.json", REGISTRY["registry_fragments"])
        self.assertEqual(CHECK_IDS, set(MIGRATED))
        for check_id in MIGRATED:
            self.assertIn(check_id, REGISTRY["checks"])

    def test_world_formal_change_selects_focused_and_global_formal_checks(self) -> None:
        result = select(
            REGISTRY,
            ["formal/KUOS/WORLD/FourGreatPhaseDynamicsCoreBridgeV0_59.lean"],
            None,
        )
        self.assertFalse(result["full_audit_required"])
        self.assertEqual(
            selected_ids(result),
            {"workflow-integrity", "world-v053-v059", "lean-formal"},
        )

    def test_memory_runtime_change_selects_focused_and_global_runtime_checks(self) -> None:
        result = select(
            REGISTRY,
            ["runtime/kuuos_memoryos_world_observe_intake_v0_39.py"],
            None,
        )
        self.assertFalse(result["full_audit_required"])
        ids = selected_ids(result)
        self.assertIn("workflow-integrity", ids)
        self.assertIn("memoryos-world-observe-v039", ids)
        self.assertIn("runtime-full", ids)

    def test_migrated_workflows_have_no_direct_pr_trigger(self) -> None:
        for workflow in MIGRATED.values():
            text = (ROOT / workflow).read_text(encoding="utf-8")
            self.assertNotIn("pull_request:", text, workflow)
            self.assertIn("workflow_dispatch:", text, workflow)
            self.assertIn("branches: [main]", text, workflow)
            self.assertIn("scripts/run_pr_entry_check_v0_5.py", text, workflow)

    def test_focused_command_sets_are_finite(self) -> None:
        for check_id in sorted(CHECK_IDS):
            commands = build_commands(check_id)
            self.assertGreater(len(commands), 0, check_id)
            self.assertLessEqual(len(commands), 8, check_id)
            self.assertTrue(REQUIRED_MARKERS[check_id])

    def test_duplicate_fragment_check_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            base = root / "check_registry.yaml"
            base.write_text(
                '{"schema_version":"0.2","known_paths":[],"full_audit_paths":[],"checks":{"x":{"paths":[]}}}',
                encoding="utf-8",
            )
            fragments = root / "check_registry.d"
            fragments.mkdir()
            (fragments / "duplicate.json").write_text(
                '{"schema_version":"0.2","checks":{"x":{"paths":[]}}}',
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_registry(base)


if __name__ == "__main__":
    unittest.main()
