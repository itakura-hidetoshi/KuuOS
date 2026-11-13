#!/usr/bin/env python3
"""Offline bounded repair loop contract: fake MCP and fake provider, no paid API."""
import importlib.util
import json
import pathlib
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

# Allow isolated execution of pure logic tests without downloading Mathlib or MCP SDK.
if "scripts" not in sys.modules:
    p = types.ModuleType("scripts")
    p.__path__ = []
    sys.modules["scripts"] = p
compat = types.ModuleType("scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17")
compat.MCPClient = object
compat.PROTOCOL_VERSION = "2025-11-25"
compat.call_tool = None
compat.require_pins = lambda root: {"synthetic": True}
compat.tool_map = lambda v: {t["name"]: t for t in v.get("result", {}).get("tools", [])}
sys.modules[compat.__name__] = compat
probe = types.ModuleType("scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1")
probe.structured = lambda r: r.get("result", {}).get("structuredContent", {}).get("result", {})
sys.modules[probe.__name__] = probe
spec = importlib.util.spec_from_file_location(
    "loop_test_module", pathlib.Path(__file__).resolve().parents[1] / "scripts" / "kuuos_lean_mcp_repair_loop_v1.py"
)
loop = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = loop
spec.loader.exec_module(loop)


class FakeMCP:
    def __init__(self, *args, **kwargs):
        self.closed = False

    def request(self, method, params=None):
        if method == "initialize":
            return {"result": {"protocolVersion": "2025-11-25"}}
        if method == "tools/list":
            return {"result": {"tools": [{"name": s} for s in (
                "lean_diagnostic_messages", "lean_goal", "lean_multi_attempt")]}}
        raise ValueError(method)

    def notify(self, *args):
        return None

    def close(self):
        self.closed = True


def fake_tools(root):
    def invoke(_client, name, params):
        if name == "lean_goal":
            return {"result": {"status": "goals"}}
        if name == "lean_multi_attempt":
            return {"result": {"items": [{"snippet": "norm_num"}]}}
        if name == "lean_diagnostic_messages":
            text = (root / params["file_path"]).read_text()
            has_skip = "  skip\n" in text
            return {"result": {"structuredContent": {"result": {
                "success": not has_skip,
                "partial": False, "timed_out": False,
                "items": ([{"severity": "error", "message": "unsolved goals", "line": 5, "column": 3}]
                          if has_skip else []),
                "failed_dependencies": [],
            }}}}
        raise ValueError(name)
    return invoke


class Contract(unittest.TestCase):
    def make_project(self, home):
        project = home / "project"
        target = project / "tests/mcp_repair_fixture/Repair.lean"
        target.parent.mkdir(parents=True)
        target.write_text("import Mathlib\nnamespace Smoke\ntheorem smoke : (2 : Nat) + 2 = 4 := by\n  skip\nend Smoke\n")
        return project, target

    def test_exact_unambiguous_and_no_trust_bypass(self):
        source = "import Mathlib\ntheorem t : True := by\n  skip\n"
        good = {"expected_sha256": loop.digest(source), "old_text": "  skip\n",
                "new_text": "  trivial\n", "reason": "repair"}
        self.assertIn("  trivial\n", loop.patch_source(source, good))
        with self.assertRaisesRegex(loop.Obstruction, "source"):
            loop.patch_source(source, dict(good, expected_sha256="0" * 64))
        with self.assertRaisesRegex(loop.Obstruction, "trust"):
            loop.patch_source(source, dict(good, new_text="  sorry\n"))
        with self.assertRaisesRegex(loop.Obstruction, "proof body"):
            loop.patch_source(source, {**good, "old_text": "theorem t : True := by\n  skip\n",
                                       "new_text": "theorem t : False := by\n  trivial\n"})

    def test_no_data_partial_and_false_success_rejected(self):
        src = b"hello\n"
        with self.assertRaisesRegex(loop.Obstruction, "NO_DATA"):
            loop.require_semantics({"items": []}, src)
        with self.assertRaisesRegex(loop.Obstruction, "partial"):
            loop.require_semantics({"success": False, "partial": True,
                                    "items": [], "failed_dependencies": []}, src)
        with self.assertRaisesRegex(loop.Obstruction, "contradiction"):
            loop.require_semantics({"success": True, "partial": False,
                                    "items": [{"severity": "error"}], "failed_dependencies": []}, src)

    def test_two_round_loop_produces_candidate_and_restores_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            root, target = self.make_project(home)
            before = target.read_bytes()
            gate = lambda root, rel_file, timeout: {"exit_code": 0 if "norm_num" in (root / rel_file).read_text() else 1}
            with patch.object(loop, "call_tool", fake_tools(root)):
                receipt = loop.run_loop(
                    root=root, rel_file="tests/mcp_repair_fixture/Repair.lean",
                    output_dir=home / "export", expected_sha256=loop.digest(before),
                    provider=loop.fixture_provider, mcp_factory=FakeMCP, direct_gate=gate,
                )
            self.assertEqual(receipt["status"], "LOCAL_LEAN_GREEN_CANDIDATE_ONLY")
            self.assertEqual(len(receipt["rounds"]), 2)
            self.assertEqual(receipt["provider_calls"], 1)
            self.assertTrue(receipt["source_restored"])
            self.assertEqual(target.read_bytes(), before)
            self.assertIn("norm_num", (home / "export/candidate.lean").read_text())
            self.assertFalse(receipt["independent_ci_success"])
            self.assertFalse(receipt["git_write_performed"])

    def test_failure_does_not_export_or_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            root, target = self.make_project(home)
            before = target.read_bytes()
            def malicious_provider(src, obs):
                return {"expected_sha256": loop.digest(src), "old_text": "  skip\n",
                        "new_text": "  sorry\n", "reason": "not allowed"}
            with patch.object(loop, "call_tool", fake_tools(root)):
                receipt = loop.run_loop(
                    root=root, rel_file="tests/mcp_repair_fixture/Repair.lean",
                    output_dir=home / "export", expected_sha256=loop.digest(before),
                    provider=malicious_provider, mcp_factory=FakeMCP,
                    direct_gate=lambda *args, **kwargs: {"exit_code": 0},
                )
            self.assertEqual(receipt["status"], "CANDIDATE_OBSTRUCTION")
            self.assertTrue(receipt["source_restored"])
            self.assertEqual(target.read_bytes(), before)
            self.assertFalse((home / "export/candidate.lean").exists())

    def test_existing_sorry_cannot_be_promoted_to_green(self):
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            root, target = self.make_project(home)
            before = b"import Mathlib\nnamespace Smoke\ntheorem t : True := by\n  sorry\nend Smoke\n"
            target.write_bytes(before)
            with patch.object(loop, "call_tool", fake_tools(root)):
                receipt = loop.run_loop(
                    root=root, rel_file="tests/mcp_repair_fixture/Repair.lean",
                    output_dir=home / "export", expected_sha256=loop.digest(before),
                    provider=loop.fixture_provider, mcp_factory=FakeMCP,
                    direct_gate=lambda *args, **kwargs: {"exit_code": 0},
                )
            self.assertEqual(receipt["status"], "DIRECT_LEAN_GATE_OBSTRUCTION")
            self.assertFalse((home / "export/candidate.lean").exists())
            self.assertTrue(receipt["source_restored"])
            self.assertEqual(target.read_bytes(), before)

    def test_wrong_sha_and_export_inside_project_block(self):
        with tempfile.TemporaryDirectory() as td:
            home = pathlib.Path(td)
            root, target = self.make_project(home)
            with self.assertRaisesRegex(loop.Obstruction, "exact-source"):
                loop.run_loop(root=root, rel_file="tests/mcp_repair_fixture/Repair.lean",
                              output_dir=home / "export", expected_sha256="0" * 64,
                              provider=loop.fixture_provider)
            with self.assertRaisesRegex(loop.Obstruction, "outside"):
                loop.run_loop(root=root, rel_file="tests/mcp_repair_fixture/Repair.lean",
                              output_dir=root / "oops", expected_sha256=loop.digest(target.read_bytes()),
                              provider=loop.fixture_provider)


if __name__ == "__main__":
    unittest.main(verbosity=2)