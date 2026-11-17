"""Offline lexical guard contracts, not Lean or MCP proof certificates."""
import importlib.util
import pathlib
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


def load_loop():
    saved = {n: sys.modules.get(n) for n in (
        'scripts', 'scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17',
        'scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1')}
    pkg = types.ModuleType('scripts')
    pkg.__path__ = []
    compat = types.ModuleType('scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17')
    compat.MCPClient = object
    compat.PROTOCOL_VERSION = '2025-11-25'
    compat.call_tool = None
    compat.require_pins = lambda root: {'synthetic': True}
    compat.tool_map = lambda v: {t['name']: t for t in v.get('result', {}).get('tools', [])}
    probe = types.ModuleType('scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1')
    probe.structured = lambda r: r['result']['structuredContent']['result']
    try:
        for m in (pkg, compat, probe):
            sys.modules[m.__name__] = m
        spec = importlib.util.spec_from_file_location('comment_guard_loop_test',
            pathlib.Path(__file__).resolve().parents[1] / 'scripts/kuuos_lean_mcp_repair_loop_v1.py')
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        for n, previous in saved.items():
            if previous is None:
                sys.modules.pop(n, None)
            else:
                sys.modules[n] = previous


loop = load_loop()


class FakeMCP:
    def __init__(self, *args, **kwargs):
        pass

    def request(self, method, params=None):
        if method == 'initialize':
            return {'result': {}}
        if method == 'tools/list':
            return {'result': {'tools': [{'name': n} for n in
                ('lean_diagnostic_messages', 'lean_goal', 'lean_multi_attempt')]}}
        raise AssertionError(method)

    def notify(self, *args):
        pass

    def close(self):
        pass


def fake_success(*args):
    return {'result': {'structuredContent': {'result': {
        'success': True, 'partial': False, 'timed_out': False,
        'items': [], 'failed_dependencies': []}}}}


class CommentGuard(unittest.TestCase):
    def gate(self, source):
        with tempfile.TemporaryDirectory() as td:
            base = pathlib.Path(td)
            root = base / 'project'
            root.mkdir()
            target = root / 'T.lean'
            original = source.encode()
            target.write_bytes(original)
            with patch.object(loop, 'call_tool', fake_success):
                r = loop.run_loop(root=root, rel_file='T.lean', output_dir=base / 'export',
                    expected_sha256=loop.digest(original), provider=loop.fixture_provider,
                    mcp_factory=FakeMCP, direct_gate=lambda *a, **k: {'exit_code': 0})
            self.assertEqual(target.read_bytes(), original)
            self.assertTrue(r['source_restored'])
            self.assertFalse(r['independent_ci_success'])
            self.assertFalse(r['git_write_performed'])
            return r

    def test_documentary_axiom_is_not_executable(self):
        r = self.gate('/- No model-structure axiom is inserted. -/\ntheorem t : True := by trivial\n')
        self.assertEqual(r['status'], 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY')
        self.assertEqual(r['rounds'][0]['forbidden_final_count'], 0)

    def test_nested_and_line_comments_are_not_executable(self):
        r = self.gate('/- outer /- sorry -/ axiom -/\n-- admit\ntheorem t : True := by trivial\n')
        self.assertEqual(r['status'], 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY')

    def test_actual_trust_bypasses_stay_blocked(self):
        for token in ('sorry', 'admit', 'axiom', 'unsafe', 'native_decide',
                      'debug.skipKernelTC', 'set_option kernel.typeAscription'):
            with self.subTest(token=token):
                r = self.gate('/- harmless commentary -/\n' + token + '\n')
                self.assertEqual(r['status'], 'DIRECT_LEAN_GATE_OBSTRUCTION')
                self.assertGreater(r['rounds'][0]['forbidden_final_count'], 0)

    def test_comment_end_does_not_hide_following_code(self):
        r = self.gate('/- /- nested -/ done -/ axiom bad : False\n')
        self.assertEqual(r['status'], 'DIRECT_LEAN_GATE_OBSTRUCTION')

    def test_comment_markers_in_normal_strings_do_not_hide_code(self):
        for text in ('def s := "/-"\naxiom bad : False\n',
                     'def s := "--"\naxiom bad : False\n',
                     'def s := "escaped \\" /-"\naxiom bad : False\n'):
            with self.subTest(text=text):
                self.assertNotEqual(self.gate(text)['status'], 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY')

    def test_comment_markers_in_raw_strings_do_not_hide_code(self):
        r = self.gate('def s := r###" /- " -- "###\naxiom bad : False\n')
        self.assertEqual(r['status'], 'DIRECT_LEAN_GATE_OBSTRUCTION')

    def test_unclosed_block_comment_fails_closed(self):
        r = self.gate('/- unclosed\ntheorem t : True := by trivial\n')
        self.assertEqual(r['status'], 'EXECUTION_OBSTRUCTION')

    def test_comment_only_proof_edit_not_false_rejected(self):
        src = 'theorem t : True := by\n  trivial\n'
        proposal = {'expected_sha256': loop.digest(src), 'old_text': '  trivial\n',
                    'new_text': '  trivial -- no axiom added\n', 'reason': 'documentation'}
        self.assertIn('no axiom', loop.patch_source(src, proposal))
        with self.assertRaises(loop.Obstruction):
            loop.patch_source(src, dict(proposal, new_text='  sorry\n'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
