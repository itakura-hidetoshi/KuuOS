"""Git-fact-checked conservative F112 public-import-only Lean routing tests."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.select_lean_import_only_route import choose_lean_targets


class AdditiveF112RootRouteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "CI test")
        self.git("config", "user.email", "ci@example.invalid")
        (self.root / "formal").mkdir()
        self.root_file = self.root / "formal/KuuOSFormal.lean"
        self.root_file.write_text("import Kuu.Presentation\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "base root")
        self.base = self.git("rev-parse", "HEAD")
        self.git("checkout", "-qb", "feature")
        self.add_source("NewF112Proof")
        self.head_commit()
        self.selection = self.receipt(["NewF112Proof"])

    def git(self, *args):
        p = subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, text=True,
            check=True,
        )
        return p.stdout.strip()

    def add_source(self, name: str):
        path = self.root / f"formal/Kuu/F112/{name}.lean"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("namespace Kuu.F112\ntheorem safe : True := trivial\nend Kuu.F112\n", encoding="utf-8")
        with self.root_file.open("a", encoding="utf-8") as f:
            f.write(f"import Kuu.F112.{name}\n")

    def head_commit(self):
        self.git("add", ".")
        self.git("commit", "--allow-empty", "-qm", "proof and imports")
        self.head = self.git("rev-parse", "HEAD")

    def receipt(self, names):
        return {
            "lean_required": True,
            "full_audit_required": False,
            "comparison_mode": "full-pr",
            "validated_lean_incremental": False,
            "unknown_paths": [],
            "unmapped_paths": [],
            "full_audit_trigger_paths": [],
            "comparison_base": self.base,
            "comparison_head": self.head,
            "changed_paths": sorted(
                ["formal/KuuOSFormal.lean"]
                + [f"formal/Kuu/F112/{n}.lean" for n in names]
            ),
            "lean_targets": ["KuuOSFormal"] + [
                f"+Kuu.F112.{n}" for n in sorted(names)
            ],
        }

    def choose(self):
        return choose_lean_targets(self.selection, self.root)

    def test_exact_additive_new_f112_import_and_source_uses_olean(self):
        targets, route = self.choose()
        self.assertEqual(
            targets, ["+KuuOSFormal:olean", "+Kuu.F112.NewF112Proof:olean"]
        )
        self.assertEqual(route, "verified-additive-f112-root-olean")

    def test_two_added_modules_with_matching_imports(self):
        self.add_source("SecondProof")
        self.head_commit()
        self.selection = self.receipt(["NewF112Proof", "SecondProof"])
        self.assertEqual(self.choose()[0], [
            "+KuuOSFormal:olean",
            "+Kuu.F112.NewF112Proof:olean",
            "+Kuu.F112.SecondProof:olean",
        ])

    def test_root_comment_edit_falls_back(self):
        self.root_file.write_text(
            "import Kuu.Presentation\n-- unrelated edit\n"
            "import Kuu.F112.NewF112Proof\n", encoding="utf-8"
        )
        self.head_commit()
        self.selection = self.receipt(["NewF112Proof"])
        self.assertEqual(self.choose()[0], self.selection["lean_targets"])

    def test_root_import_deletion_falls_back(self):
        self.root_file.write_text("import Kuu.F112.NewF112Proof\n", encoding="utf-8")
        self.head_commit()
        self.selection = self.receipt(["NewF112Proof"])
        self.assertEqual(self.choose()[0], self.selection["lean_targets"])

    def test_source_modification_not_new_falls_back(self):
        # The initial new source was committed; change it on another commit
        # and compare from that validated parent where its status is M.
        parent = self.head
        path = self.root / "formal/Kuu/F112/NewF112Proof.lean"
        path.write_text(path.read_text(encoding="utf-8") + "-- update\n")
        self.head_commit()
        self.selection = self.receipt(["NewF112Proof"])
        self.selection["comparison_base"] = parent
        self.selection["changed_paths"] = ["formal/Kuu/F112/NewF112Proof.lean"]
        self.assertEqual(self.choose()[0], self.selection["lean_targets"])

    def test_extra_document_change_falls_back(self):
        doc = self.root / "docs/example.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("more text\n")
        self.head_commit()
        self.selection = self.receipt(["NewF112Proof"])
        self.selection["changed_paths"].append("docs/example.md")
        self.assertEqual(self.choose()[0], self.selection["lean_targets"])

    def test_hidden_deletion_falls_back(self):
        # The full name-status diff catches D even if the upper selector
        # only included AC/MR paths.
        self.git("checkout", "main", "--", "formal/KuuOSFormal.lean")
        self.root_file.write_text("import Kuu.F112.NewF112Proof\n")
        other = self.root / "formal/Unrelated.lean"
        other.write_text("def stale := 0\n")
        self.head_commit()
        previous = self.head
        other.unlink()
        self.head_commit()
        self.selection["comparison_head"] = self.head
        self.assertNotEqual(previous, self.head)
        self.assertEqual(self.choose()[0], self.selection["lean_targets"])

    def test_unknown_diff_or_full_audit_falls_back(self):
        for field, value in [
            ("comparison_mode", "validated-lean-incremental"),
            ("full_audit_required", True),
            ("unknown_paths", ["unknown.file"]),
            ("comparison_head", "not-a-sha"),
            ("lean_required", False),
        ]:
            with self.subTest(field=field):
                current = self.selection[field]
                self.selection[field] = value
                self.assertEqual(self.choose()[0], self.selection["lean_targets"])
                self.selection[field] = current

    def test_mismatched_targets_or_imports_fall_back(self):
        self.selection["lean_targets"] = ["KuuOSFormal"]
        self.assertEqual(self.choose()[0], ["KuuOSFormal"])
        self.selection["lean_targets"] = ["KuuOSFormal", "+Kuu.F112.NewF112Proof"]
        self.root_file.write_text("import Kuu.Presentation\nimport Kuu.F112.Different\n")
        self.head_commit()
        self.selection["comparison_head"] = self.head
        self.assertEqual(self.choose()[0], self.selection["lean_targets"])


if __name__ == "__main__":
    unittest.main()
