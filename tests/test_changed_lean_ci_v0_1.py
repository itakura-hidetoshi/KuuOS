#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from scripts.check_changed_lean import (
    EXPECTED_LEAN_TOOLCHAIN,
    EXPECTED_MATHLIB_REV,
    EXPECTED_MATHLIB_TAG,
    build_plan,
    pin_evidence,
)
from scripts.check_workflow_consolidation_integrity import all_repository_files

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ChangedLeanCiV01Tests(unittest.TestCase):
    def test_repository_pins_remain_lean_and_mathlib_431(self) -> None:
        evidence = pin_evidence()
        self.assertEqual(evidence["lean_toolchain"], EXPECTED_LEAN_TOOLCHAIN)
        self.assertEqual(evidence["mathlib_tag"], EXPECTED_MATHLIB_TAG)
        self.assertEqual(evidence["mathlib_manifest_rev"], EXPECTED_MATHLIB_REV)

    def test_changed_refinement_builds_direct_dependent_frontier(self) -> None:
        plan = build_plan(
            ["formal/KUOS/DependentOriginationRefinementTransitivityV1_2.lean"],
            dependent_depth=1,
        )
        self.assertEqual(
            plan["direct_targets"],
            ["KUOS.DependentOriginationRefinementTransitivityV1_2"],
        )
        self.assertIn(
            "KUOS.DependentOriginationDirectedCofinalSemanticsV1_3",
            plan["dependent_targets"],
        )
        self.assertIn(
            "KUOS.DependentOriginationCoreSpineV1_2",
            plan["dependent_targets"],
        )
        self.assertNotIn("KuuOSFormal", plan["build_targets"])

    def test_unregistered_orphan_dependents_remain_outside_validator_boundary(self) -> None:
        plan = build_plan(
            ["formal/KUOS/DependentOriginationFiniteTransferWordV0_4.lean"],
            dependent_depth=1,
        )
        orphan = "KUOS.DependentOriginationTransportSpineV0_4"
        self.assertIn(orphan, plan["skipped_unregistered_dependents"])
        self.assertNotIn(orphan, plan["build_targets"])

    def test_lake_input_change_degrades_to_full_required_mode(self) -> None:
        plan = build_plan(["lean-toolchain"], dependent_depth=1)
        self.assertEqual(plan["mode"], "full-required")
        self.assertEqual(plan["build_targets"], ["KuuOSFormal"])

    def test_workflow_runs_fast_before_merge_full_with_strict_flags(self) -> None:
        workflow = (ROOT / ".github/workflows/pr-governance-gate.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("scripts/check_changed_lean.py", workflow)
        self.assertIn("ready_for_review", workflow)
        self.assertIn("github.event.pull_request.draft == false", workflow)
        self.assertIn("full_lean", workflow)
        self.assertIn("needs:\n      - select\n      - lean-formal", workflow)
        self.assertGreaterEqual(workflow.count("-DwarningAsError=true"), 1)
        self.assertGreaterEqual(workflow.count("-DsorryAsError=true"), 1)
        self.assertIn("--lean-full-result", workflow)

    def test_workflow_scan_excludes_generated_dependency_and_receipt_trees(self) -> None:
        relative_paths = {
            path.relative_to(ROOT).as_posix() for path in all_repository_files()
        }
        self.assertFalse(any(path.startswith(".lake/") for path in relative_paths))
        self.assertFalse(any(path.startswith("artifacts/") for path in relative_paths))

    def test_audit_summary_requires_full_receipt_only_when_full_job_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            selection = root / "selection.json"
            selection.write_text(
                json.dumps(
                    {
                        "selected_checks": [],
                        "full_audit_required": False,
                        "changed_paths": [],
                    }
                ),
                encoding="utf-8",
            )
            common = [
                sys.executable,
                "scripts/build_audit_summary.py",
                "--selection",
                str(selection),
                "--receipts-root",
                str(root / "receipts"),
                "--output-dir",
                str(root / "summary"),
                "--python-result",
                "skipped",
                "--lean-result",
                "skipped",
            ]
            skipped = subprocess.run(
                [*common, "--lean-full-result", "skipped"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            self.assertEqual(skipped.returncode, 0, skipped.stdout)

            required = subprocess.run(
                [*common, "--lean-full-result", "success"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            self.assertEqual(required.returncode, 1, required.stdout)
            summary = json.loads(
                (root / "summary" / "audit-summary.json").read_text(encoding="utf-8")
            )
            self.assertIn("lean-formal-full", summary["missing_receipts"])


if __name__ == "__main__":
    unittest.main()
