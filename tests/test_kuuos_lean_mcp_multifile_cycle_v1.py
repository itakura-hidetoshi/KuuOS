#!/usr/bin/env python3
"""Offline multi-file MCP orchestration: order, exact digests, rollback, fail closed."""
import hashlib
import pathlib
import tempfile
import unittest
from unittest.mock import patch

# Import shared stable one-file repair implementation (no real Lean until CI job).
from scripts import kuuos_lean_mcp_multifile_cycle_v1 as multi


class MultiFileContracts(unittest.TestCase):
    def setup_fixture(self, base):
        root = pathlib.Path(base) / "isolated"
        root.mkdir()
        (root / "lake-manifest.json").write_text("{}")
        a = "tests/mcp_repair_fixture/RepairMulti/Alpha.lean"
        b = "tests/mcp_repair_fixture/RepairMulti/Beta.lean"
        original = {
            a: "import Mathlib\nnamespace RepairMulti\ntheorem alpha : True := by\n  skip\nend RepairMulti\n",
            b: "import RepairMulti.Alpha\nnamespace RepairMulti\ntheorem beta : True := by\n  skip\nend RepairMulti\n",
        }
        for rel, contents in original.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents)
        plan = {
            "version": multi.VERSION, "source_head": "a" * 40,
            "targets": [
                {"path": a, "module": "RepairMulti.Alpha",
                 "sha256": multi.digest(original[a]), "depends_on": []},
                {"path": b, "module": "RepairMulti.Beta",
                 "sha256": multi.digest(original[b]), "depends_on": ["RepairMulti.Alpha"]},
            ],
        }
        return root, plan, original

    def fake_single(self, *, root, rel_file, output_dir, **_):
        if rel_file.endswith("Beta.lean"):
            alpha = root / "tests/mcp_repair_fixture/RepairMulti/Alpha.lean"
            self.assertIn("  simp\n", alpha.read_text())
            self.assertTrue(multi._olean_path(root, "RepairMulti.Alpha").exists())
        s = (root / rel_file).read_text()
        amended = s.replace("  skip\n", "  simp\n")
        self.assertNotEqual(s, amended)
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
        (pathlib.Path(output_dir) / "candidate.lean").write_text(amended)
        return {"status": "LOCAL_LEAN_GREEN_CANDIDATE_ONLY",
                "source_restored": True, "rounds": [{"errors": 1}, {"errors": 0}]}

    def fake_compile(self, root, rel_file, olean):
        source = (root / rel_file).read_text()
        self.assertIn("  simp\n", source)
        olean.parent.mkdir(parents=True, exist_ok=True)
        olean.write_bytes(b"olean candidate " + source.encode())
        return {"exit_code": 0}

    def test_green_two_file_candidate_and_full_rollback(self):
        with tempfile.TemporaryDirectory() as td:
            root, plan, originals = self.setup_fixture(td)
            previous_olean = multi._olean_path(root, "RepairMulti.Alpha")
            previous_olean.parent.mkdir(parents=True, exist_ok=True)
            previous_olean.write_bytes(b"original olean")
            out = pathlib.Path(td) / "output"
            with patch.object(multi, "require_pins", lambda p: {"pinned": True}):
                r = multi.run_multifile(
                    root=root, manifest=plan, output_dir=out,
                    single_loop=self.fake_single, compile_gate=self.fake_compile,
                )
            self.assertEqual(r["status"], "LOCAL_MULTIFILE_LEAN_GREEN_CANDIDATES_ONLY")
            self.assertTrue(r["source_and_olean_restored"])
            self.assertFalse(r["github_write_performed"])
            self.assertFalse(r["independent_ci_success"])
            self.assertEqual(len(r["validated_candidates"]), 2)
            for path, before in originals.items():
                self.assertEqual((root / path).read_text(), before)
                self.assertIn("  simp\n", (out / "candidates" / path).read_text())
            self.assertEqual(previous_olean.read_bytes(), b"original olean")
            self.assertFalse(multi._olean_path(root, "RepairMulti.Beta").exists())

    def test_fail_closed_on_wrong_sha_or_unordered_import(self):
        with tempfile.TemporaryDirectory() as td:
            root, plan, _ = self.setup_fixture(td)
            with patch.object(multi, "require_pins", lambda p: {"pinned": True}):
                plan["targets"][1]["sha256"] = "f" * 64
                with self.assertRaisesRegex(multi.Obstruction, "SHA256"):
                    multi.run_multifile(root=root, manifest=plan,
                                        output_dir=pathlib.Path(td) / "out")
                plan["targets"][1]["sha256"] = multi.digest((root / plan["targets"][1]["path"]).read_bytes())
                plan["targets"].reverse()
                with self.assertRaisesRegex(multi.Obstruction, "not topologically ordered"):
                    multi.run_multifile(root=root, manifest=plan,
                                        output_dir=pathlib.Path(td) / "out")

    def test_compile_failure_restores_and_never_exports(self):
        with tempfile.TemporaryDirectory() as td:
            root, plan, originals = self.setup_fixture(td)
            out = pathlib.Path(td) / "out"
            seen = []
            def fail_on_beta(root, rel_file, olean):
                seen.append(rel_file)
                if rel_file.endswith("Beta.lean"):
                    return {"exit_code": 1, "stderr_tail": "simulated failure"}
                return self.fake_compile(root, rel_file, olean)
            with patch.object(multi, "require_pins", lambda p: {"pinned": True}):
                r = multi.run_multifile(root=root, manifest=plan, output_dir=out,
                                        single_loop=self.fake_single,
                                        compile_gate=fail_on_beta)
            self.assertEqual(r["status"], "MULTIFILE_OBSTRUCTION")
            self.assertTrue(r["source_and_olean_restored"])
            self.assertFalse(r["validated_candidates"])
            for rel, contents in originals.items():
                self.assertEqual((root / rel).read_text(), contents)
                self.assertFalse((out / "candidates" / rel).exists())
            self.assertFalse(multi._olean_path(root, "RepairMulti.Alpha").exists())

    def test_reject_output_inside_repo_and_invalid_module(self):
        with tempfile.TemporaryDirectory() as td:
            root, plan, _ = self.setup_fixture(td)
            with patch.object(multi, "require_pins", lambda p: {"pinned": True}):
                with self.assertRaisesRegex(multi.Obstruction, "outside"):
                    multi.run_multifile(root=root, manifest=plan, output_dir=root / "out")
                plan["targets"][0]["module"] = "KuuOSFormal"
                with self.assertRaisesRegex(multi.Obstruction, "module"):
                    multi.run_multifile(root=root, manifest=plan,
                                        output_dir=pathlib.Path(td) / "out")


if __name__ == "__main__":
    unittest.main(verbosity=2)
