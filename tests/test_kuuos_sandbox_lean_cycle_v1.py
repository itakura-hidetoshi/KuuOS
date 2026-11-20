#!/usr/bin/env python3
"""Offline tests for the fail-closed KuuOS Sandbox Lean replay loop."""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sandbox_cycle_test_module", ROOT / "scripts/kuuos_sandbox_lean_cycle_v1.py")
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


ORIGINAL = "namespace Proof\n theorem eqn : (1 : Nat) = 1 := by\n  skip\nend Proof\n"
GREEN = ORIGINAL.replace("  skip", "  rfl")
OTHER = ORIGINAL.replace("  skip", "  trivial")


class FakeCompiler:
    def __init__(self, *, fail_on_audit=False):
        self.calls = []
        self.fail_on_audit = fail_on_audit

    def __call__(self, cmd, *, cwd, timeout, check=False, capture_output=False,
                 text=False, stdout=None, stderr=None):
        self.calls.append(list(cmd))
        if cmd[:2] == ["lean", "--version"]:
            return type("P", (), {"returncode":0, "stdout":"Lean (version 4.30.0-rc2)",
                                  "stderr":""})()
        if cmd[:2] == ["lake", "--version"]:
            return type("P", (), {"returncode":0,
                                  "stdout":"Lake version 5.0.0 (Lean version 4.30.0-rc2)",
                                  "stderr":""})()
        assert cmd[:3] == ["lake", "env", "lean"]
        assert "-DwarningAsError=true" in cmd
        assert "-Dweak.sorryAsError=true" in cmd
        lean = Path(cmd[-1]).read_text()
        if "skip" in lean or "  trivial\n" in lean:
            stdout.write(b"candidate.lean:2:3: error: unsolved goals\n")
            return type("P", (), {"returncode":1})()
        if "#print axioms Proof.eqn" in lean:
            if self.fail_on_audit:
                stdout.write(b"'Proof.eqn' depends on axioms: [sorryAx]\n")
            else:
                stdout.write(b"'Proof.eqn' depends on axioms: [propext, Classical.choice, Quot.sound]\n")
        Path(cmd[cmd.index("-o")+1]).write_bytes(b"olean")
        return type("P", (), {"returncode":0})()


class Contracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.root = self.home / "repo"
        self.root.mkdir()
        (self.root/"lean-toolchain").write_text(mod.LEAN_PIN+"\n")
        (self.root/"lake-manifest.json").write_text(json.dumps({
            "packages":[{"name":"mathlib","rev":mod.MATHLIB_PIN}]}))
        self.source = self.root/"formal/Proof.lean"
        self.source.parent.mkdir()
        self.source.write_text(ORIGINAL)
        self.inbox = self.home/"inbox"
        self.inbox.mkdir()
        self.out = self.home/"receipts"

    def args(self):
        return argparse.Namespace(
            project_root=str(self.root), source="formal/Proof.lean",
            source_blob=mod.git_blob(ORIGINAL.encode()), source_head="a"*40,
            namespace="Proof", candidates_dir=str(self.inbox),
            receipt_dir=str(self.out), admission=None, max_attempts=9,
            timeout_seconds=30, idle_seconds=0, poll_seconds=1)

    def test_comment_mask_and_no_trust_escape(self):
        text="namespace Proof\n/- outer /- sorry -/ admit -/\n" \
             'theorem eqn : True := by\n  exact True.intro\n' \
             'def str := "sorry axiom unsafe"\n'
        cleaned=mod.without_comments_strings(text)
        self.assertNotIn("sorry",cleaned)
        self.assertNotIn("admit",cleaned)
        self.assertEqual(list(mod.declarations(text)),["eqn","str"])
        with self.assertRaises(mod.Hold):
            mod.without_comments_strings("/- unterminated")
        with self.assertRaises(mod.Hold):
            mod.source_contract(ORIGINAL, GREEN.replace("rfl","sorry"),{},{})
        with self.assertRaises(mod.Hold):
            mod.source_contract(ORIGINAL,GREEN.replace("rfl","native_decide"),{},{})

    def test_signature_changes_admitted_only_with_reason(self):
        c="namespace Proof\n theorem eqn : True := by\n  trivial\nend Proof\n"
        with self.assertRaisesRegex(mod.Hold,"SIGNATURE_OBSTRUCTION"):
            mod.source_contract(ORIGINAL,c,{}, {})
        contract=mod.source_contract(ORIGINAL,c,
            {"eqn":"deliberately changed proposition; requires authority review"}, {})
        self.assertFalse(contract["declaration_statement_text_unchanged"])
        with self.assertRaises(mod.Hold):
            mod.source_contract(ORIGINAL,c,{"missing":"unrelated stale permission"}, {})

    def test_import_removed_and_added(self):
        o="import Mathlib\n"+ORIGINAL
        c="import Mathlib\nimport Mathlib.Data.Nat.Bits\n"+GREEN
        with self.assertRaisesRegex(mod.Hold,"IMPORT_OBSTRUCTION"):
            mod.source_contract(o,c,{}, {})
        good=mod.source_contract(o,c,{},
             {"Mathlib.Data.Nat.Bits":"pinned mathlib bit decomposition theorem"})
        self.assertEqual(list(good["import_additions"]),["Mathlib.Data.Nat.Bits"])
        with self.assertRaisesRegex(mod.Hold,"IMPORT_OBSTRUCTION"):
            mod.source_contract(o, GREEN, {}, {})

    def test_public_declaration_inventory(self):
        with self.assertRaisesRegex(mod.Hold,"DECLARATION_OBSTRUCTION"):
            mod.source_contract(ORIGINAL,GREEN.replace("eqn","changed"),{}, {})

    def test_git_blob_and_pin_mismatch(self):
        self.assertEqual(mod.git_blob(b""), "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
        self.assertEqual(mod.require_pins(self.root,verify_binaries=False)["mathlib_sha"],
                         mod.MATHLIB_PIN)
        (self.root/"lean-toolchain").write_text("leanprover/lean4:v4.31.0\n")
        with self.assertRaisesRegex(mod.Hold,"PIN_MISMATCH"):
            mod.require_pins(self.root,verify_binaries=False)

    def test_block_unknown_axions(self):
        with self.assertRaisesRegex(mod.Hold,"AXIOM_OBSTRUCTION"):
            mod.audit_axioms("'Proof.eqn' depends on axioms: [sorryAx]",
                             ["eqn"],"Proof")
        with self.assertRaisesRegex(mod.Hold,"AXIOM_NO_DATA"):
            mod.audit_axioms("unrelated text",["eqn"],"Proof")

    def test_fail_then_green_append_only_and_resume(self):
        (self.inbox/"01-fail.lean").write_text(OTHER)
        (self.inbox/"02-green.lean").write_text(GREEN)
        compiler=FakeCompiler()
        with patch.object(mod.subprocess,"run",side_effect=compiler):
            self.assertEqual(mod.run(self.args()),0)
            ledger=[json.loads(s) for s in (self.out/"ledger.jsonl").read_text().splitlines()]
            self.assertEqual(len(ledger),2)
            self.assertEqual(ledger[0]["status"],"DIRECT_LEAN_FAILED")
            self.assertEqual(ledger[1]["status"],"LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY")
            self.assertEqual(ledger[1]["axioms"]["checked"],1)
            self.assertFalse(ledger[1]["independent_ci_success"])
            self.assertFalse(ledger[1]["git_write_performed"])
            self.assertEqual(self.source.read_text(),ORIGINAL)
            self.assertTrue((self.out/("attempt-00002-"+mod.sha256(GREEN.encode())[:12])/
                              "receipt.json").exists())
            # No candidate is repeated merely because the process/sandbox resumes.
            self.assertEqual(mod.run(self.args()),2)
            self.assertEqual(len((self.out/"ledger.jsonl").read_text().splitlines()),2)

    def test_axiom_failure_holds_and_preserves_source(self):
        (self.inbox/"candidate.lean").write_text(GREEN)
        with patch.object(mod.subprocess,"run",side_effect=FakeCompiler(fail_on_audit=True)):
            self.assertEqual(mod.run(self.args()),2)
        receipts=[json.loads(s) for s in (self.out/"ledger.jsonl").read_text().splitlines()]
        self.assertEqual(receipts[0]["status"],"BLOCKED")
        self.assertIn("AXIOM_OBSTRUCTION",receipts[0]["obstruction"])
        self.assertEqual(self.source.read_text(),ORIGINAL)

    def test_interrupted_attempt_is_retained_and_retried(self):
        (self.inbox/"new.lean").write_text(GREEN)
        self.out.mkdir()
        old=self.out/("attempt-00001-"+mod.sha256(GREEN.encode())[:12])
        old.mkdir()
        (old/"candidate.lean").write_text(GREEN)  # orphaned on VM stop
        with patch.object(mod.subprocess,"run",side_effect=FakeCompiler()):
            self.assertEqual(mod.run(self.args()),0)
        receipts=[json.loads(s) for s in (self.out/"ledger.jsonl").read_text().splitlines()]
        self.assertEqual(receipts[0]["attempt"],2)
        self.assertEqual(receipts[0]["orphaned_prior_attempt_dirs"],[old.name])
        self.assertTrue(old.is_dir())
        self.assertFalse((old/"receipt.json").exists())
        self.assertEqual(self.source.read_text(),ORIGINAL)

    def test_source_blob_refuses_stale(self):
        (self.inbox/"candidate.lean").write_text(GREEN)
        args=self.args()
        args.source_blob="0"*40
        with patch.object(mod.subprocess,"run",side_effect=FakeCompiler()):
            with self.assertRaisesRegex(mod.Hold,"SOURCE_OBSTRUCTION"):
                mod.run(args)
        self.assertFalse(self.out.exists())

    def test_symlink_and_isolation(self):
        (self.inbox/"symbolic.lean").symlink_to(self.source)
        with patch.object(mod.subprocess,"run",side_effect=FakeCompiler()):
            with self.assertRaisesRegex(mod.Hold,"symlink"):
                mod.run(self.args())
        args=self.args()
        args.receipt_dir=str(self.root/"inside-repo")
        with patch.object(mod.subprocess,"run",side_effect=FakeCompiler()):
            with self.assertRaisesRegex(mod.Hold,"isolation"):
                mod.run(args)


class ScopedGovernanceRouting(unittest.TestCase):
    """Future non-Lean changes are focused; registry changes still get full audit."""

    def test_sandbox_paths_use_focused_nonlean_checks(self):
        from scripts.select_impacted_checks import load_registry, select
        registry = load_registry(ROOT / "ci/check_registry.yaml")
        expected = [
            "scripts/kuuos_sandbox_lean_cycle_v1.py",
            "scripts/kuuos_sandbox_prepare_v1.sh",
            "tests/test_kuuos_sandbox_lean_cycle_v1.py",
            "docs/KUUOS_SANDBOX_LEAN_CYCLE_v1.md",
            ".github/workflows/kuuos-sandbox-lean-cycle-v1.yml",
        ]
        for paths in [expected, *([p] for p in expected)]:
            with self.subTest(paths=paths):
                result = select(registry, paths, None)
                self.assertFalse(result["full_audit_required"])
                self.assertFalse(result["lean_required"])
                self.assertEqual(result["unknown_paths"], [])
                self.assertEqual(result["unmapped_paths"], [])
                ids = {item["id"] for item in result["selected_checks"]}
                self.assertIn("kuuos-sandbox-lean-local-cycle", ids)
                self.assertIn("workflow-integrity", ids)

    def test_registry_control_change_remains_full_governance(self):
        from scripts.select_impacted_checks import load_registry, select
        registry = load_registry(ROOT / "ci/check_registry.yaml")
        path = "ci/check_registry.d/kuuos_sandbox_lean_cycle_v1.json"
        result = select(registry, [path], None)
        self.assertTrue(result["full_audit_required"])
        self.assertTrue(result["lean_required"])
        self.assertIn(path, result["full_audit_trigger_paths"])
        self.assertIn("lean-formal", {c["id"] for c in result["selected_checks"]})


if __name__ == "__main__":
    unittest.main()
