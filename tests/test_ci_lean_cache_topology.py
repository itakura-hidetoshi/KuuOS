"""Verify the trusted-main Lake cache and focused CodeAI PR CI topology."""
from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class LakeCacheRoutingTests(unittest.TestCase):
    def codeai_with_full_baseline(self):
        return [
            path for path in sorted(WORKFLOWS.glob("codeai-*.yml"))
            if "- name: Strictly compile repository formal baseline" in path.read_text(encoding="utf-8")
        ]

    def test_codeai_focused_pr_builds_restore_trusted_and_pr_caches(self):
        workflows = self.codeai_with_full_baseline()
        self.assertEqual(len(workflows), 49, "unexpected number of CodeAI Lean workflows")
        for path in workflows:
            with self.subTest(workflow=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(text.count("id: trusted-lake-cache"), 1)
                self.assertIn("uses: actions/cache/restore@v5", text)
                self.assertIn("path: .lake\n", text)
                self.assertIn("path: .lake/build\n", text)
                self.assertIn("key: kuuos-lake-${{ runner.os }}-${{ runner.arch }}-", text)
                self.assertIn("key: kuuos-pr-build-${{ runner.os }}-${{ runner.arch }}-", text)
                self.assertIn("hashFiles('lake-manifest.json')", text)
                self.assertIn("hashFiles('lean-toolchain')", text)
                self.assertLess(text.index("id: trusted-lake-cache"),
                                text.index("uses: leanprover/lean-action@v1"))
                self.assertIn("if: steps.trusted-lake-cache.outputs.cache-matched-key == ''\n"
                              "        run: lake update", text)
                self.assertIn("if: steps.trusted-lake-cache.outputs.cache-matched-key == ''\n"
                              "        run: lake exe cache get", text)
                self.assertRegex(text,
                    r"- name: Strictly compile repository formal baseline\n"
                    r"        if: github\.event_name == 'workflow_dispatch'\n")
                self.assertIn("build KuuOSFormal", text)
                self.assertIn("-DwarningAsError=true", text)
                self.assertIn("-DsorryAsError=true", text)

    def test_canonical_main_saves_a_warm_lake_cache(self):
        text = (WORKFLOWS / "lean-formal-validation.yml").read_text(encoding="utf-8")
        self.assertIn("id: lake-workspace-cache", text)
        self.assertIn("uses: actions/cache@v5", text)
        self.assertIn("path: .lake\n", text)
        self.assertIn("LAKE_CACHE_MATCHED_KEY: ${{ steps.lake-workspace-cache.outputs.cache-matched-key }}", text)
        self.assertIn("scripts/build_lean4.sh --no-update --no-cache", text)
        self.assertIn("scripts/build_lean4.sh --target", text)
        self.assertIn("git diff --exit-code -- lean-toolchain lake-manifest.json", text)

    def test_pr_governance_retains_the_single_canonical_full_build(self):
        gate = (WORKFLOWS / "pr-governance-gate.yml").read_text(encoding="utf-8")
        selector = (ROOT / "scripts" / "select_impacted_checks.py").read_text(encoding="utf-8")
        self.assertIn("name: Strict Lean formal validation", gate)
        self.assertIn("Restore trusted main Lake workspace cache", gate)
        self.assertIn("Restore PR-local Lean build overlay", gate)
        self.assertIn("Save PR-local Lean build overlay", gate)
        self.assertIn('FULL_LEAN_TARGET = "KuuOSFormal"', selector)
        self.assertIn('"lakefile.toml",', selector)


if __name__ == "__main__":
    unittest.main()
