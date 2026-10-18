"""Regression: focused CodeAI CI must not rebuild the entire KuuOS proof package.

The central Governance Gate retains strict aggregate Lean validation. All 49
registered CodeAI Lean roots still receive their own strict, standalone
feature check. The trusted-main and PR caches are restored read-only; only
the central gate can publish a PR-local build-prefix cache.
"""
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
SHARED_PIN_FILES = ("lean-toolchain", "lake-manifest.json", "lakefile.toml")
CACHE_CONDITION = "if: steps.trusted-lake-workspace.outputs.cache-matched-key == ''"
FOCUSED_ROOT_PATTERN = re.compile(r"(?m)^\s+build (KuuOSCodeAI[A-Za-z0-9_]+)\b")


def focused_codeai_workflows():
    for path in sorted(WORKFLOWS.glob("codeai-*.yml")):
        content = path.read_text(encoding="utf-8")
        if FOCUSED_ROOT_PATTERN.search(content):
            yield path, content


class CodeAIDeduplicatedLeanCITests(unittest.TestCase):
    def test_all_registered_codeai_roots_are_still_strictly_compiled(self):
        lake = tomllib.loads((ROOT / "lakefile.toml").read_text(encoding="utf-8"))
        self.assertEqual(lake["defaultTargets"], ["KuuOSFormal"])
        self.assertEqual(len(lake["lean_lib"]), 1)
        self.assertEqual(lake["lean_lib"][0]["name"], "KuuOSFormal")
        roots = set(lake["lean_lib"][0]["roots"])
        codeai_roots = {root for root in roots if root.startswith("KuuOSCodeAI")}
        workflows = list(focused_codeai_workflows())
        self.assertEqual(len(workflows), 49)
        targets = set()
        for path, content in workflows:
            with self.subTest(workflow=path.name):
                matches = FOCUSED_ROOT_PATTERN.findall(content)
                self.assertEqual(len(matches), 1)
                self.assertNotIn(matches[0], targets, "duplicate scoped target")
                targets.add(matches[0])
                self.assertIn(matches[0], roots, "feature root is not publicly registered")
                self.assertIn("-KleanArgs=-DwarningAsError=true", content)
                self.assertIn("-KleanArgs=-DsorryAsError=true", content)
                self.assertNotIn("build KuuOSFormal", content,
                                 "the aggregate must be compiled once in Governance")
                self.assertNotIn("Strictly compile repository formal baseline", content)
                self.assertIn("Verify committed dependency manifest is canonical", content)
                self.assertIn("Restore trusted main Lake workspace (read-only)", content)
                self.assertIn("Restore previously compiled PR Lean prefix (read-only)", content)
                self.assertIn("uses: actions/cache/restore@v5", content)
                self.assertNotIn("uses: actions/cache/save@", content)
                self.assertEqual(content.count(CACHE_CONDITION), 2)
                self.assertIn("github.event.pull_request.number", content)
                self.assertIn("  pull_request:\n    paths:\n", content)
                paths = content.split("  pull_request:\n    paths:\n", 1)[1].split(
                    "\n\n", 1)[0]
                self.assertIn(".github/workflows/" + path.name, paths)
                for shared_pin in SHARED_PIN_FILES:
                    self.assertNotIn('      - "' + shared_pin + '"', paths,
                                     "shared pin edits use the central strict gate")
        self.assertEqual(targets, codeai_roots,
                         "every public CodeAI Lean root needs a strict focused job")

    def test_single_canonical_pr_gate_keeps_strict_full_validation(self):
        gate = (WORKFLOWS / "pr-governance-gate.yml").read_text(encoding="utf-8")
        selector = (ROOT / "scripts" / "select_impacted_checks.py").read_text(
            encoding="utf-8")
        self.assertIn("on:\n  pull_request:\n", gate)
        self.assertIn("name: Strict Lean formal validation", gate)
        self.assertIn("if: needs.select.outputs.lean_required == 'true'", gate)
        self.assertIn('"lakefile.toml"', selector)
        self.assertIn('"lake-manifest.json"', selector)
        self.assertIn('"lean-toolchain"', selector)
        self.assertIn('FULL_LEAN_TARGET = "KuuOSFormal"', selector)
        self.assertIn("lake", gate)
        self.assertIn("-KleanArgs=-DwarningAsError=true", gate)
        self.assertIn("-KleanArgs=-DsorryAsError=true", gate)
        self.assertIn("tests.test_codeai_ci_focus_and_cache", gate)


if __name__ == "__main__":
    unittest.main()
