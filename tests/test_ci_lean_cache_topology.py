"""Verify the trusted-main Lake cache and focused CodeAI PR CI topology."""
from __future__ import annotations

from pathlib import Path
import re
from scripts.ci_codeai_lean_scope import workflow_pr_paths, needs_targeted_lean
from scripts.ci_subsystem_lean_scope import needs_subsystem_lean
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
                self.assertIn("PYTHONPATH=. python3 scripts/ci_subsystem_lean_scope.py", text)
                self.assertIn("'scripts/ci_subsystem_lean_scope.py'", text)
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
                self.assertFalse(needs_subsystem_lean(
                    ["formal/KuuOSFormal.lean"], patterns, delegated))
                self.assertFalse(needs_subsystem_lean(
                    ["formal/KUOS.lean", "lakefile.toml"], patterns, delegated))
                self.assertFalse(needs_subsystem_lean(
                    [doc_path], patterns, delegated))
                self.assertTrue(needs_subsystem_lean(
                    [".github/workflows/" + name], patterns, delegated))
                self.assertTrue(needs_subsystem_lean(
                    [], patterns, delegated))  # unknown diff fails closed

    def test_qi_three_stages_and_capability_are_scoped_and_cache_read_only(self):
        """Aggregate-only F112 PRs must not start four redundant Lean builds.

        The canonical PR Governance job still owns the strict public-root build.
        Dedicated workflows retain static public-root/import assertions and,
        for CapabilityOS, all runtime/unit regressions on every matching PR.
        """
        specs = {
            "qi-wuxing-cyclic-group-paths-v3-1-validation.yml": (
                "formal/KUOS/Architecture/QiWuxingCyclicGroupPathsV3_1.lean",
                ["formal/KuuOSFormal.lean",
                 "docs/KUUOS_QI_WUXING_CYCLIC_GROUP_PATHS_v3_1.md"],
            ),
            "qi-wuxing-path-observation-v3-2-validation.yml": (
                "formal/KUOS/Architecture/QiWuxingPathObservationCongruenceV3_2.lean",
                ["formal/KuuOSFormal.lean",
                 "docs/KUUOS_QI_WUXING_PATH_OBSERVATION_CONGRUENCE_v3_2.md"],
            ),
            "qi-wuxing-reachable-observation-v3-3-validation.yml": (
                "formal/KUOS/Architecture/QiWuxingReachableObservationCategoryV3_3.lean",
                ["formal/KuuOSFormal.lean",
                 "docs/KUUOS_QI_WUXING_REACHABLE_OBSERVATION_CATEGORY_v3_3.md"],
            ),
            "capabilityos-qi-world-v0-60-validation.yml": (
                "formal/KUOS/CapabilityOS/QiWorldCapabilityKernelV0_60.lean",
                ["formal/KuuOSFormal.lean", "formal/KUOS.lean",
                 "docs/KUUOS_CAPABILITYOS_QI_WORLD_KERNEL_v0_60.md"],
            ),
        }
        for name, (owned_source, delegated) in specs.items():
            with self.subTest(workflow=name):
                text = (WORKFLOWS / name).read_text(encoding="utf-8")
                patterns = workflow_pr_paths(text)
                self.assertIn("Select ", text)
                self.assertIn("scope (fail closed)", text)
                self.assertIn("PYTHONPATH=. python3 scripts/ci_subsystem_lean_scope.py", text)
                self.assertIn("--head HEAD", text)
                self.assertIn("if: steps.lean-scope.outputs.needed == 'true'", text)
                self.assertIn("scripts/ci_subsystem_lean_scope.py", patterns)
                self.assertIn("scripts/ci_codeai_lean_scope.py", patterns)
                self.assertIn("Restore trusted main Lake workspace (read-only)", text)
                self.assertIn("uses: actions/cache/restore@v5", text)
                self.assertIn("path: .lake\n", text)
                self.assertIn("key: kuuos-lake-${{ runner.os }}-${{ runner.arch }}-", text)
                self.assertNotIn("uses: actions/cache/save@v5", text)
                self.assertIn("scripts/check_public_proof_roots.py", text)
                self.assertIn("-DwarningAsError=true", text)
                self.assertIn("-DsorryAsError=true", text)
                self.assertIn("git diff --exit-code -- lake-manifest.json lean-toolchain", text)
                self.assertTrue(needs_subsystem_lean([owned_source], patterns, delegated))
                self.assertTrue(needs_subsystem_lean([".github/workflows/" + name], patterns, delegated))
                self.assertTrue(needs_subsystem_lean(["scripts/ci_subsystem_lean_scope.py"], patterns, delegated))
                self.assertTrue(needs_subsystem_lean([], patterns, delegated))
                self.assertFalse(needs_subsystem_lean(["formal/KuuOSFormal.lean"], patterns, delegated))
                self.assertFalse(needs_subsystem_lean(["formal/KuuOSFormal.lean", "lakefile.toml"], patterns, delegated))
                self.assertFalse(needs_subsystem_lean([delegated[-1]], patterns, delegated))

        cap = (WORKFLOWS / "capabilityos-qi-world-v0-60-validation.yml").read_text(encoding="utf-8")
        self.assertIn("Run CapabilityOS v0.60 unit tests", cap)
        self.assertIn("Run MemoryOS v0.37 regression", cap)
        self.assertIn("grep -Fq 'import KUOS.CapabilityOS.QiWorldCapabilityKernelV0_60'", cap)
        self.assertIn("- name: Strictly compile formal root\n"
                      "        if: github.event_name == 'workflow_dispatch'", cap)
        self.assertIn("runs-on: ubuntu-24.04", cap)

    def test_canonical_main_saves_a_warm_lake_cache(self):
        text = (WORKFLOWS / "lean-formal-validation.yml").read_text(encoding="utf-8")
        self.assertIn("id: lake-workspace", text)
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
        # The additive F112 `:olean` fast path must not inherit the
        # unrelated 30-minute wall-time cap: typed coherence elaboration
        # can exceed it even with all dependencies already compiled.
        self.assertIn("lean_f112_heavy: ${{ steps.fastpath.outputs.lean_f112_heavy }}", gate)
        self.assertIn('p.startswith("formal/Kuu/F112/") and p.endswith(".lean")', gate)
        self.assertIn('f.write(f"lean_f112_heavy=', gate)
        self.assertIn("needs.select.outputs.lean_f112_heavy == 'true'", gate)
        self.assertIn("timeout --signal=TERM --kill-after=30s 75m", gate)
        self.assertIn("if: always() && !cancelled()", gate)

    def test_known_lean_library_suggestions_panic_is_not_kernel_bypass(self):
        wrapper = (ROOT / "scripts" / "build_lean4.sh").read_text(encoding="utf-8")
        self.assertIn("env -u LEAN_ABORT_ON_PANIC lake", wrapper)
        self.assertIn("build_status=${PIPESTATUS[0]}", wrapper)
        self.assertIn("-KleanArgs=-DwarningAsError=true", wrapper)
        self.assertIn("-KleanArgs=-DsorryAsError=true", wrapper)
        self.assertIn("grep -F 'PANIC at '", wrapper)
        self.assertIn("SymbolFrequency|SineQuaNon", wrapper)

        main = (WORKFLOWS / "lean-formal-validation.yml").read_text(encoding="utf-8")
        self.assertIn(
            'bash scripts/build_lean4.sh --no-update --no-cache --target "$target"',
            main,
        )
        self.assertIn('--target "${f112_targets[0]}"', main)


    def test_governance_rerun_recovers_only_same_run_exact_head_receipts(self):
        import json
        import tempfile

        from scripts.build_audit_summary import collect_receipts

        gate = (WORKFLOWS / "pr-governance-gate.yml").read_text(encoding="utf-8")
        self.assertEqual(gate.count("pattern: audit-selection-${{ github.run_id }}-*"), 3)
        self.assertIn("pattern: audit-check-*-${{ github.run_id }}-*", gate)
        self.assertIn("--run-id '${{ github.run_id }}'", gate)
        self.assertIn("--git-sha '${{ github.sha }}'", gate)

        with tempfile.TemporaryDirectory() as root_name:
            root = Path(root_name)
            def write(attempt, check, status, *, sha="merge-sha", run="7"):
                folder = root / f"audit-check-{check}-7-{attempt}" / check
                folder.mkdir(parents=True, exist_ok=True)
                (folder / "receipt.json").write_text(json.dumps({
                    "check_id": check, "run_id": run, "git_sha": sha,
                    "selection_digest": "selection-sha",
                    "run_attempt": str(attempt), "status": status,
                }), encoding="utf-8")

            write(1, "lean-formal", "failed")
            write(2, "lean-formal", "passed")
            write(1, "python", "passed")
            kwargs = dict(run_id="7", git_sha="merge-sha",
                          selection_digest="selection-sha")
            receipts = collect_receipts(root, **kwargs)
            self.assertEqual(receipts["lean-formal"]["status"], "passed")
            self.assertEqual(receipts["python"]["run_attempt"], "1")
            write(3, "lean-formal", "failed")
            self.assertEqual(
                collect_receipts(root, **kwargs)["lean-formal"]["status"], "failed"
            )
            write(4, "lean-formal", "passed", sha="another-sha")
            with self.assertRaisesRegex(ValueError, "mismatched git_sha"):
                collect_receipts(root, **kwargs)


if __name__ == "__main__":
    unittest.main()
