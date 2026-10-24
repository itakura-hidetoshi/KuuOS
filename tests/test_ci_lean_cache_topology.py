"""Verify the trusted-main Lake cache and focused CodeAI PR CI topology."""
from __future__ import annotations

from pathlib import Path
import re
from scripts.ci_codeai_lean_scope import workflow_pr_paths, needs_targeted_lean
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
                self.assertEqual(text.count("id: lean-scope"), 1)
                self.assertIn("python3 scripts/ci_codeai_lean_scope.py", text)
                self.assertIn("if: steps.lean-scope.outputs.needed == 'true'", text)
                self.assertIn("uses: actions/cache/restore@v5", text)
                self.assertIn("path: .lake\n", text)
                self.assertIn("path: .lake/build\n", text)
                self.assertIn("key: kuuos-lake-${{ runner.os }}-${{ runner.arch }}-", text)
                self.assertIn("key: kuuos-pr-build-${{ runner.os }}-${{ runner.arch }}-", text)
                self.assertIn("hashFiles('lake-manifest.json')", text)
                self.assertIn("hashFiles('lean-toolchain')", text)
                self.assertLess(text.index("id: trusted-lake-cache"),
                                text.index("uses: leanprover/lean-action@v1"))
                self.assertIn("steps.trusted-lake-cache.outputs.cache-matched-key == ''\n"
                              "        run: lake update", text)
                self.assertIn("steps.trusted-lake-cache.outputs.cache-matched-key == ''\n"
                              "        run: lake exe cache get", text)
                self.assertRegex(text,
                    r"- name: Strictly compile repository formal baseline\n"
                    r"        if: github\.event_name == 'workflow_dispatch'\n")
                self.assertIn("build KuuOSFormal", text)
                self.assertIn("-DwarningAsError=true", text)
                self.assertIn("-DsorryAsError=true", text)

    def test_codeai_lean_scope_retains_domain_changes(self):
        codeai = (WORKFLOWS / "codeai-autonomous-trajectory-synthesis-envelope-v0-1.yml")
        patterns = workflow_pr_paths(codeai.read_text(encoding="utf-8"))
        self.assertIn("lakefile.toml", patterns)
        self.assertTrue(needs_targeted_lean(["runtime/kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1.py"], patterns))
        self.assertTrue(needs_targeted_lean([codeai.relative_to(ROOT).as_posix()], patterns))
        self.assertFalse(needs_targeted_lean(["lakefile.toml", "lean-toolchain"], patterns))
        self.assertTrue(needs_targeted_lean([], patterns))  # unknown diff is fail-closed
        self.assertTrue(needs_targeted_lean(["lakefile.toml"], []))

    def test_three_long_running_subsystems_scope_and_cache(self):
        """Dedicated checks must not redo a cold full aggregate on root-only PRs."""
        subsystems = {
            "kuuos-gauge-field-self-organization-v0-60.yml":
                ("Build v0.60 formal root", "docs/KUUOS_GAUGE_FIELD_SELF_ORGANIZATION_v0_60.md"),
            "kuuos-os-associated-gauge-fields-v0-61.yml":
                ("Build v0.61 formal root", "docs/KUUOS_OS_ASSOCIATED_GAUGE_FIELDS_v0_61.md"),
            "modular-evolution-mesh-v0-1.yml":
                ("Strictly compile modular formal root", "docs/KUUOS_MODULAR_EVOLUTION_MESH_v0_1.md"),
        }
        for name, (target_step, doc_path) in subsystems.items():
            with self.subTest(workflow=name):
                text = (WORKFLOWS / name).read_text(encoding="utf-8")
                self.assertIn("Select subsystem Lean scope (fail closed)", text)
                self.assertIn("python3 scripts/ci_codeai_lean_scope.py", text)
                self.assertIn("--delegated-path formal/KuuOSFormal.lean", text)
                self.assertIn("--delegated-path formal/KUOS.lean", text)
                self.assertIn("Restore trusted main Lake workspace (read-only)", text)
                self.assertIn("uses: actions/cache/restore@v5", text)
                self.assertIn("path: .lake\n", text)
                self.assertIn("key: kuuos-lake-${{ runner.os }}-${{ runner.arch }}-", text)
                self.assertIn("hashFiles('lean-toolchain')", text)
                self.assertIn("hashFiles('lake-manifest.json')", text)
                self.assertLess(text.index("Select subsystem Lean scope"),
                                text.index("Restore trusted main Lake workspace"))
                self.assertLess(text.index("Restore trusted main Lake workspace"),
                                text.index("uses: leanprover/lean-action@v1"))
                self.assertNotIn("uses: actions/cache/save@v5", text)
                self.assertIn("if: steps.lean-scope.outputs.needed == 'true'", text)
                self.assertIn("- name: " + target_step + "\n"
                              "        if: steps.lean-scope.outputs.needed == 'true'", text)
                aggregate_step = ("Strictly compile aggregate formal root"
                                  if "modular" in name else "Build aggregate formal root")
                self.assertIn("- name: " + aggregate_step + "\n"
                              "        if: github.event_name == 'workflow_dispatch'", text)
                self.assertIn("-DwarningAsError=true", text)
                self.assertIn("-DsorryAsError=true", text)
                self.assertIn("git diff --exit-code -- lake-manifest.json lean-toolchain", text)
                self.assertIn("if [[ ! -d .lake/packages/mathlib ]]; then", text)

                patterns = workflow_pr_paths(text)
                delegated = ["formal/KuuOSFormal.lean", "formal/KUOS.lean", doc_path]
                self.assertFalse(needs_targeted_lean(
                    ["formal/KuuOSFormal.lean"], patterns, delegated))
                self.assertFalse(needs_targeted_lean(
                    ["formal/KUOS.lean", "lakefile.toml"], patterns, delegated))
                self.assertFalse(needs_targeted_lean(
                    [doc_path], patterns, delegated))
                self.assertTrue(needs_targeted_lean(
                    [".github/workflows/" + name], patterns, delegated))
                self.assertTrue(needs_targeted_lean(
                    [], patterns, delegated))  # unknown diff fails closed

    def test_canonical_main_saves_a_warm_lake_cache(self):
        text = (WORKFLOWS / "lean-formal-validation.yml").read_text(encoding="utf-8")
        self.assertIn("id: lake-workspace-cache", text)
        self.assertIn("uses: actions/cache/restore@v5", text)
        self.assertIn("uses: actions/cache/save@v5", text)
        self.assertIn("path: .lake\n", text)
        self.assertIn("MATCHED_LAKE_KEY: ${{ steps.lake-workspace.outputs.cache-matched-key }}", text)
        self.assertIn("scripts/build_lean4.sh --no-update --no-cache", text)
        self.assertIn("scripts/build_lean4.sh --no-update --no-cache --target", text)
        self.assertIn("git diff --exit-code -- lake-manifest.json lean-toolchain", text)

    def test_pr_governance_retains_the_single_canonical_full_build(self):
        gate = (WORKFLOWS / "pr-governance-gate.yml").read_text(encoding="utf-8")
        selector = (ROOT / "scripts" / "select_impacted_checks.py").read_text(encoding="utf-8")
        self.assertIn("name: Strict Lean formal validation", gate)
        self.assertIn("Restore validated parent/main Lake workspace cache", gate)
        self.assertIn("Restore PR-local Lean build overlay", gate)
        self.assertIn("Save PR-local Lean build overlay", gate)
        self.assertIn('FULL_LEAN_TARGET = "KuuOSFormal"', selector)
        self.assertIn('"lakefile.toml",', selector)


if __name__ == "__main__":
    unittest.main()
