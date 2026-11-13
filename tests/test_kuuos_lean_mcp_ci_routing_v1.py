#!/usr/bin/env python3
"""Exact, fail-closed CI registry classification for pinned Lean MCP tooling.

No proof, root or strict validator is changed. A changed formal Lean source
must still trigger the original Strict Lean job.
"""
from pathlib import Path
import unittest

from scripts.select_impacted_checks import load_registry, select

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = "ci/check_registry.d/lean_mcp_pinned_validation_v0_1.json"
CHECK_ID = "lean-mcp-bounded-closed-loop-v1"
REGISTRY_PATH = ROOT / "ci/check_registry.yaml"
EXPECTED_PINS = (
    "leanprover/lean4:v4.30.0-rc2",
    "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
)


class PinnedLeanMCPRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_registry(REGISTRY_PATH)
        cls.check = cls.registry["checks"][CHECK_ID]
        cls.exact_changes = list(cls.check["paths"])

    def test_registry_is_exact_and_all_paths_exist(self):
        paths = self.exact_changes
        self.assertEqual(len(paths), 28)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn(FRAGMENT, paths)
        self.assertIn("tests/test_kuuos_lean_mcp_ci_routing_v1.py", paths)
        for name in paths:
            with self.subTest(path=name):
                self.assertFalse(name.startswith("formal/"))
                self.assertFalse("*" in name or "?" in name or ".." in name)
                self.assertTrue((ROOT / name).is_file())
        self.assertEqual(
            self.registry.get("known_paths", []).count(".devcontainer/lean-mcp/devcontainer.json"), 1
        )
        self.assertNotIn(FRAGMENT, self.registry["full_audit_paths"])
        self.assertTrue(self.check["pr_required"])
        self.assertTrue(self.check["full_audit_member"])
        self.assertEqual(
            self.check["depends_on"], ["workflow-integrity", "ci-audit-tests"]
        )

    def test_exact_nonlean_changes_select_all_required_checks(self):
        result = select(self.registry, self.exact_changes, None)
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(result["unmapped_paths"], [])
        self.assertEqual(result["full_audit_trigger_paths"], [])
        self.assertFalse(result["full_audit_required"])
        self.assertFalse(result["lean_required"])
        self.assertEqual(result["lean_targets"], [])
        selected = {x["id"] for x in result["selected_checks"]}
        self.assertTrue(
            {"lean-mcp-bounded-closed-loop-v1", "workflow-integrity",
             "ci-audit-tests", "runtime-full"} <= selected,
            selected,
        )

    def test_genuine_formal_source_change_retains_strict_lean(self):
        # Existing formal file: proof changes are NOT included in the non-Lean exception.
        formal = "formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean"
        self.assertTrue((ROOT / formal).is_file())
        changed = [*self.exact_changes, formal]
        result = select(self.registry, changed, None)
        selected = {x["id"] for x in result["selected_checks"]}
        self.assertTrue(result["lean_required"], result)
        self.assertIn("lean-formal", selected)
        self.assertNotEqual(result["lean_targets"], [])

    def test_unrecognized_and_control_files_still_trigger_full_audit(self):
        unknown = select(self.registry, [*self.exact_changes, "unregistered/private.py"], None)
        self.assertTrue(unknown["full_audit_required"])
        self.assertTrue(unknown["lean_required"])
        self.assertIn("unregistered/private.py", unknown["unknown_paths"])
        altered_control = select(self.registry, [*self.exact_changes, "ci/check_registry.yaml"], None)
        self.assertTrue(altered_control["full_audit_required"])
        self.assertTrue(altered_control["lean_required"])
        self.assertIn("ci/check_registry.yaml", altered_control["full_audit_trigger_paths"])

    def test_pinned_lean_and_mathlib_preserved(self):
        import json
        self.assertEqual((ROOT / "lean-toolchain").read_text().strip(), EXPECTED_PINS[0])
        manifest = json.loads((ROOT / "lake-manifest.json").read_text())
        matches = [x["rev"] for x in manifest["packages"] if x.get("name") == "mathlib"]
        self.assertEqual(matches, [EXPECTED_PINS[1]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
