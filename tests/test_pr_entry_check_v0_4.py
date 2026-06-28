#!/usr/bin/env python3
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_pr_entry_check_v0_4 import CHECK_IDS, build_commands

MIGRATED = {
    "memoryos-json": ".github/workflows/memoryos-json-governance.yml",
    "qi-process-review": ".github/workflows/qi-process-tensor-review.yml",
    "kustring-finality": ".github/workflows/kustring_runtime_finality_v0_2.yml",
}


class PrEntryCheckTests(unittest.TestCase):
    def test_registered_ids_have_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(len(CHECK_IDS), 5)
            for check_id in CHECK_IDS:
                commands = build_commands(check_id, root / check_id)
                self.assertTrue(commands)
                self.assertLessEqual(len(commands), 8)

    def test_migrated_workflows_have_no_direct_pr_trigger(self):
        for workflow in MIGRATED.values():
            text = (ROOT / workflow).read_text(encoding="utf-8")
            self.assertNotIn("pull_request:", text, workflow)
            self.assertIn("workflow_dispatch:", text, workflow)
            self.assertIn("push:", text, workflow)

    def test_migrated_checks_are_bound_in_registry(self):
        registry = json.loads(
            (ROOT / "ci/check_registry.yaml").read_text(encoding="utf-8")
        )
        checks = registry["checks"]
        for check_id, workflow in MIGRATED.items():
            self.assertIn(check_id, checks)
            self.assertIn(workflow, checks[check_id]["paths"])
            self.assertIn("scripts/run_pr_entry_check_v0_4.py", checks[check_id]["command"])

    def test_unknown_id_is_rejected(self):
        with self.assertRaises(ValueError):
            build_commands("unknown", pathlib.Path("artifacts/checks/unknown"))


if __name__ == "__main__":
    unittest.main()
