"""Regression: every published CodeAI Lean root retains a focused strict CI path.

The current canonical main dynamically selects affected CodeAI targets for
pull requests, while only manual dispatch repeats the public aggregate
KuuOSFormal build. The independent PR Governance gate remains required.
"""
from pathlib import Path
import re
import tomllib
import unittest

from scripts import ci_codeai_lean_scope as scope

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
FOCUSED_ROOT = re.compile(r"(?m)^\s+build (KuuOSCodeAI[A-Za-z0-9_]+)\b")
GLOBAL_INPUTS = ("lakefile.toml", "lake-manifest.json", "lean-toolchain")


def focused_codeai_workflows():
    for path in sorted(WORKFLOWS.glob("codeai-*.yml")):
        source = path.read_text(encoding="utf-8")
        if FOCUSED_ROOT.search(source):
            yield path, source


class CodeAIDeduplicatedLeanCITests(unittest.TestCase):
    def test_each_public_codeai_root_stays_selected_and_strict(self):
        config = tomllib.loads((ROOT / "lakefile.toml").read_text(encoding="utf-8"))
        self.assertEqual(config["defaultTargets"], ["KuuOSFormal"])
        self.assertEqual(len(config["lean_lib"]), 1)
        roots = set(config["lean_lib"][0]["roots"])
        published = {name for name in roots if name.startswith("KuuOSCodeAI")}
        observed = set()
        workflows = list(focused_codeai_workflows())
        self.assertEqual(len(workflows), 49)
        for path, source in workflows:
            with self.subTest(workflow=path.name):
                targets = FOCUSED_ROOT.findall(source)
                self.assertEqual(len(targets), 1)
                target = targets[0]
                self.assertNotIn(target, observed)
                self.assertIn(target, published)
                observed.add(target)
                self.assertIn("-KleanArgs=-DwarningAsError=true", source)
                self.assertIn("-KleanArgs=-DsorryAsError=true", source)
                self.assertIn("Compile Python surfaces", source)
                self.assertIn("Determine whether this CodeAI Lean target is impacted", source)
                self.assertIn("scripts/ci_codeai_lean_scope.py", source)
                self.assertIn("if: steps.lean-scope.outputs.needed == 'true'", source)
                self.assertIn("Restore trusted main Lake workspace (read-only)", source)
                self.assertIn("Restore PR-local Lean build overlay (read-only)", source)
                self.assertIn("uses: actions/cache/restore@v5", source)
                self.assertNotIn("uses: actions/cache/save@", source)
                self.assertIn("Strictly compile repository formal baseline", source)
                self.assertRegex(
                    source,
                    r"(?m)^      - name: Strictly compile repository formal baseline\n"
                    r"        if: github.event_name == 'workflow_dispatch'\n",
                )
                self.assertIn("  pull_request:\n    paths:\n", source)
                patterns = scope.workflow_pr_paths(source)
                for pin in GLOBAL_INPUTS:
                    self.assertIn(pin, patterns)
                    self.assertFalse(scope.needs_targeted_lean([pin], patterns))
                self.assertTrue(scope.needs_targeted_lean(
                    [".github/workflows/" + path.name], patterns))
        self.assertEqual(observed, published)

    def test_fail_closed_missing_scope_and_central_governance(self):
        self.assertTrue(scope.needs_targeted_lean([], ["example.py"]))
        self.assertTrue(scope.needs_targeted_lean(["example.py"], []))
        gate = (WORKFLOWS / "pr-governance-gate.yml").read_text(encoding="utf-8")
        self.assertIn("name: Strict Lean formal validation", gate)
        self.assertIn("if: needs.select.outputs.lean_required == 'true'", gate)
        self.assertIn("-KleanArgs=-DwarningAsError=true", gate)
        self.assertIn("tests.test_codeai_ci_focus_and_cache", gate)


if __name__ == "__main__":
    unittest.main()
