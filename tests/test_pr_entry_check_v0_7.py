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

from run_pr_entry_check_v0_7 import CHECK_IDS, build_commands
from select_impacted_checks import load_registry, select

MIGRATED = {
    "core-autonomy-v01": ".github/workflows/kuuos_core_autonomy_validation.yml",
    "belief-os-v01": ".github/workflows/belief-os-v0-1-validation.yml",
    "review-seal-v01": ".github/workflows/kuuos_review_seal_validation.yml",
}
REGISTRY = load_registry(ROOT / "ci/check_registry.yaml")


def selected_ids(result: dict[str, object]) -> set[str]:
    checks = result["selected_checks"]
    assert isinstance(checks, list)
    return {str(item["id"]) for item in checks}


class PrEntryCheckV07Tests(unittest.TestCase):
    def test_registered_check_ids_match_migrated_workflows(self) -> None:
        self.assertEqual(CHECK_IDS, set(MIGRATED))
        for check_id in MIGRATED:
            self.assertIn(check_id, REGISTRY["checks"])

    def test_each_check_has_finite_commands(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for check_id in sorted(CHECK_IDS):
                commands = build_commands(check_id, root / check_id)
                self.assertGreater(len(commands), 0, check_id)
                self.assertLessEqual(len(commands), 4, check_id)

    def test_core_autonomy_logs_are_bound_to_check_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = pathlib.Path(directory) / "core-autonomy-v01"
            commands = build_commands("core-autonomy-v01", output)
            self.assertIn(str(output / "contract-check.jsonl"), commands[1])
            self.assertIn(str(output / "once-self-test.jsonl"), commands[2])

    def test_migrated_workflows_have_no_direct_pr_trigger(self) -> None:
        for check_id, workflow in MIGRATED.items():
            text = (ROOT / workflow).read_text(encoding="utf-8")
            self.assertNotIn("pull_request:", text, workflow)
            self.assertIn("workflow_dispatch:", text, workflow)
            self.assertIn("scripts/run_pr_entry_check_v0_7.py", text, workflow)
            if check_id != "review-seal-v01":
                self.assertIn("branches: [main]", text, workflow)
            else:
                self.assertNotIn("push:", text, workflow)

    def test_core_autonomy_change_selects_focused_check(self) -> None:
        result = select(
            REGISTRY,
            ["scripts/validate_kuuos_core_autonomy_contract_v0_1.py"],
            None,
        )
        self.assertFalse(result["full_audit_required"])
        self.assertIn("core-autonomy-v01", selected_ids(result))

    def test_belief_runtime_change_selects_focused_and_runtime_checks(self) -> None:
        result = select(
            REGISTRY,
            ["runtime/kuuos_belief_os_kernel_v0_1.py"],
            None,
        )
        self.assertFalse(result["full_audit_required"])
        ids = selected_ids(result)
        self.assertIn("belief-os-v01", ids)
        self.assertIn("runtime-full", ids)

    def test_review_seal_change_selects_focused_check(self) -> None:
        result = select(
            REGISTRY,
            ["scripts/validate_kuuos_review_seal_os_bridge_v0_1_min.py"],
            None,
        )
        self.assertFalse(result["full_audit_required"])
        self.assertIn("review-seal-v01", selected_ids(result))

    def test_unknown_check_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                build_commands("unknown", pathlib.Path(directory))


if __name__ == "__main__":
    unittest.main()
