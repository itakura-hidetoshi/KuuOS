"""Source preservation and ordinary unittest extension discovery for v0.12.

The fixtures exercise the loader in separate Python processes; the production
helper returns suites and never executes tests inside another test case.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from contextlib import contextmanager
from importlib import import_module
from importlib.util import find_spec
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
CHECKER_MODULE = "scripts.check_kuuos_lean_python_mediator_sources_v0_12"
LOADER_MODULE = "tests.lean_python_extensions"
NATIVE_MODULE = "tests.test_kuuos_lean_python_plan_act_native_v0_4"
REGISTRATION_PATH = "tests/test_kuuos_lean_python_plan_act_native_v0_4.py"
LOADER_PATH = "tests/lean_python_extensions/__init__.py"
SOURCE_PATH = "runtime/original.py"
SOURCE_BLOB = "ce013625030ba8dba906f756967f9e9ca394464a"
REQUIRED_PATH = "docs/new-contract.md"
PRIOR_BYTES = (
    b'# original registry\nimport unittest\n\n'
    b'if __name__ == "__main__":\n    unittest.main()\n'
)
PRIOR_BLOB = "81a369ebb4266a93cf3c35ece56cbdb38c95e28d"
REGISTRATION_BLOCK = '''# v0.12 adds ordinary discovery for additive Lean/Python extension tests.
def load_tests(loader, tests, pattern):
    from tests.lean_python_extensions import load_extension_tests

    tests.addTests(load_extension_tests(loader))
    return tests


'''
REQUIRED_TEST_FILES = (
    "test_mediator_transition_v0_12.py",
    "test_mediated_native_cycle_v0_12.py",
    "test_mediator_sources_v0_12.py",
)
NEW_PIN_PATHS = (
    "runtime/kuuos_lean_python_pre_host_guard_v0_11.py",
    "runtime/kuuos_lean_python_pre_host_native_cycle_v0_11.py",
    "scripts/check_kuuos_lean_python_pre_host_sources_v0_11.py",
    "tests/test_kuuos_lean_python_os_registry_v0_5.py",
    "runtime/kuuos_decision_os_plural_kernel_v0_2.py",
    "runtime/kuuos_decision_os_plural_types_v0_2.py",
    "runtime/kuuos_decision_os_plural_store_v0_2.py",
    "runtime/kuuos_decision_os_wa_kernel_v0_3.py",
    "runtime/kuuos_decision_os_wa_types_v0_3.py",
    "runtime/kuuos_decision_os_wa_store_v0_3.py",
    "runtime/kuuos_decision_os_wa_state_v0_3.py",
    "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean",
    "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean",
    "runtime/v02_decision_os_plural_harmony_appeal.py",
    "runtime/v03_decision_os_wa_relational_harmony.py",
)


def registered_bytes(block=REGISTRATION_BLOCK):
    anchor = b'if __name__ == "__main__":'
    return PRIOR_BYTES.replace(anchor, block.encode("utf-8") + anchor, 1)


def case_ids(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from case_ids(item)
        else:
            yield item.id()


class MediatorSourceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(find_spec(CHECKER_MODULE), "v0.12 source checker required")
        self.checker = import_module(CHECKER_MODULE)

    @contextmanager
    def source_fixture(self, registration=None):
        with TemporaryDirectory(prefix="kuuos-v012-source-") as folder:
            root = Path(folder)
            source = root / SOURCE_PATH
            source.parent.mkdir(parents=True)
            source.write_bytes(b"hello\n")
            required = root / REQUIRED_PATH
            required.parent.mkdir(parents=True)
            required.write_text("required inventory\n", encoding="utf-8")
            helper = root / LOADER_PATH
            helper.parent.mkdir(parents=True)
            helper.write_bytes(b"hello\n")
            registered = root / REGISTRATION_PATH
            registered.write_bytes(
                registered_bytes() if registration is None else registration
            )
            with patch.object(self.checker, "SOURCE_BLOBS", {SOURCE_PATH: SOURCE_BLOB}), \
                 patch.object(self.checker, "REQUIRED_PATHS", (REQUIRED_PATH,)), \
                 patch.object(self.checker, "PRIOR_REGISTRATION_BLOB", PRIOR_BLOB), \
                 patch.object(self.checker, "LOADER_BLOB", SOURCE_BLOB):
                yield root, source, required, helper, registered

    @contextmanager
    def helper_fixture(self, source_issues=()):
        with TemporaryDirectory(prefix="kuuos-v012-loader-") as folder:
            root = Path(folder)
            package = root / "tests/lean_python_extensions"
            package.mkdir(parents=True)
            (package / "__init__.py").write_bytes((ROOT / LOADER_PATH).read_bytes())
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "__init__.py").write_text("", encoding="utf-8")
            (scripts / "check_kuuos_lean_python_mediator_sources_v0_12.py").write_text(
                "def check_sources(root):\n    return " + repr(tuple(source_issues)) + "\n",
                encoding="utf-8",
            )
            for name in REQUIRED_TEST_FILES:
                (package / name).write_text(
                    "import unittest\n"
                    "class FixtureTests(unittest.TestCase):\n"
                    "    def test_case(self):\n        pass\n",
                    encoding="utf-8",
                )
            self.assertFalse((root / "tests/__init__.py").exists())
            yield root, package

    def helper_process(self, root, *, run=False, foreign=False):
        program = '''import io, json, pathlib, sys, types, unittest
sys.path.insert(0, sys.argv[1])
if sys.argv[3] == "foreign":
    name = "tests.lean_python_extensions.test_mediator_transition_v0_12"
    module = types.ModuleType(name)
    module.__file__ = str(pathlib.Path(sys.argv[1]) / "other/test_mediator_transition_v0_12.py")
    sys.modules[name] = module
from tests.lean_python_extensions import load_extension_tests
loader = unittest.TestLoader()
def ids(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from ids(item)
        else:
            yield item.id()
try:
    suite = load_extension_tests(loader)
    result = {"ids": list(ids(suite)), "count": suite.countTestCases(),
              "loader_errors": list(loader.errors)}
    if sys.argv[2] == "run":
        stream = io.StringIO()
        outcome = unittest.TextTestRunner(stream=stream).run(suite)
        result.update(tests_run=outcome.testsRun, failures=len(outcome.failures),
                      errors=len(outcome.errors), skipped=len(outcome.skipped),
                      output=stream.getvalue())
        print(json.dumps(result))
        raise SystemExit(0 if outcome.wasSuccessful() else 1)
    print(json.dumps(result))
except Exception as exc:
    print(json.dumps({"error": type(exc).__name__ + ":" + str(exc),
                      "loader_errors": list(loader.errors)}))
    raise SystemExit(2)
'''
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", program, str(root),
             "run" if run else "load", "foreign" if foreign else "local"],
            capture_output=True, text=True, timeout=20, check=False,
        )
        self.assertTrue(result.stdout.strip(), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_actual_sources_and_registration(self):
        self.assertEqual(self.checker.check_sources(ROOT), ())

    def test_existing_v010_and_v011_checks_remain_unchanged_and_pass(self):
        for name in (
            "scripts.check_kuuos_lean_python_checked_transition_sources_v0_10",
            "scripts.check_kuuos_lean_python_pre_host_sources_v0_11",
        ):
            with self.subTest(checker=name):
                self.assertEqual(import_module(name).check_sources(ROOT), ())

    def test_expected_mediator_sources_and_frozen_v05_registry_are_pinned(self):
        self.assertTrue(set(NEW_PIN_PATHS).issubset(self.checker.SOURCE_BLOBS))

    def test_every_prior_pin_is_retained_and_still_detects_drift(self):
        old_path = ROOT / "scripts/check_kuuos_lean_python_pre_host_sources_v0_11.py"
        old_body = ast.parse(old_path.read_text(encoding="utf-8")).body
        old_pins = next(
            ast.literal_eval(node.value) for node in old_body
            if isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "SOURCE_BLOBS" for t in node.targets)
        )
        self.assertEqual({p: self.checker.SOURCE_BLOBS.get(p) for p in old_pins}, old_pins)
        with TemporaryDirectory(prefix="kuuos-v012-prior-") as folder:
            root = Path(folder)
            for path in self.checker.SOURCE_BLOBS:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / path).read_bytes())
            helper = root / LOADER_PATH
            helper.parent.mkdir(parents=True, exist_ok=True)
            helper.write_bytes((ROOT / LOADER_PATH).read_bytes())
            with patch.object(self.checker, "REQUIRED_PATHS", ()):
                self.assertEqual(self.checker.check_sources(root, False), ())
                for path in old_pins:
                    with self.subTest(path=path):
                        target = root / path
                        raw = target.read_bytes()
                        try:
                            target.write_bytes(raw + b"changed\n")
                            issues = self.checker.check_sources(root, False)
                        finally:
                            target.write_bytes(raw)
                        self.assertIn("source_byte_drift:" + path, issues)

    def test_exact_original_bytes_and_expected_hook_are_accepted(self):
        with self.source_fixture() as fixture:
            self.assertEqual(self.checker.check_sources(fixture[0]), ())

    def test_source_drift_missing_or_nonregular_file_blocks(self):
        for kind in ("drift", "missing", "directory"):
            with self.subTest(kind=kind), self.source_fixture() as (root, source, *_):
                if kind == "drift":
                    source.write_bytes(b"changed\n")
                else:
                    source.unlink()
                    if kind == "directory":
                        source.mkdir()
                issues = self.checker.check_sources(root)
                expected = {"drift": "byte_drift", "missing": "missing",
                            "directory": "not_regular_file"}[kind]
                self.assertIn("source_" + expected + ":" + SOURCE_PATH, issues)

    def test_source_and_parent_symlinks_block_even_when_bytes_match(self):
        for parent in (False, True):
            with self.subTest(parent=parent), self.source_fixture() as (root, source, *_):
                if parent:
                    saved = root / "saved-runtime"
                    source.parent.rename(saved)
                    (root / "runtime").symlink_to(saved, target_is_directory=True)
                else:
                    saved = root / "saved-original.py"
                    source.rename(saved)
                    source.symlink_to(saved)
                issues = self.checker.check_sources(root)
                self.assertIn("source_symlink_not_allowed:" + SOURCE_PATH, issues)

    def test_unreadable_source_is_reported(self):
        with self.source_fixture() as (root, source, *_):
            original = Path.read_bytes
            def read(candidate):
                if candidate == source:
                    raise PermissionError("controlled source denial")
                return original(candidate)
            with patch.object(Path, "read_bytes", read):
                issues = self.checker.check_sources(root)
            self.assertIn("source_unreadable:" + SOURCE_PATH, issues)

    def test_required_inventory_missing_or_symlink_blocks(self):
        for symlink in (False, True):
            with self.subTest(symlink=symlink), self.source_fixture() as (root, source, required, *_):
                required.unlink()
                if symlink:
                    required.symlink_to(source)
                issues = self.checker.check_sources(root)
                issue = "symlink_not_allowed" if symlink else "missing"
                self.assertIn("required_v012_file_" + issue + ":" + REQUIRED_PATH, issues)

    def test_loader_bytes_missing_drift_and_symlink_block(self):
        for kind in ("missing", "drift", "symlink"):
            with self.subTest(kind=kind), self.source_fixture() as (root, source, required, helper, registered):
                if kind == "drift":
                    helper.write_bytes(b"def load_extension_tests(loader): return []\n")
                else:
                    helper.unlink()
                    if kind == "symlink":
                        helper.symlink_to(source)
                issues = self.checker.check_sources(root)
                expected = {"missing": "missing", "drift": "byte_drift",
                            "symlink": "symlink_not_allowed"}[kind]
                self.assertIn("extension_loader_" + expected, issues)

    def test_missing_or_symlink_registry_blocks(self):
        for symlink in (False, True):
            with self.subTest(symlink=symlink), self.source_fixture() as (root, source, required, helper, registered):
                registered.unlink()
                if symlink:
                    registered.symlink_to(source)
                issues = self.checker.check_sources(root)
                expected = "symlink_not_allowed" if symlink else "missing"
                self.assertIn("native_test_module_" + expected, issues)

    def test_original_native_comment_or_import_change_blocks(self):
        variants = (
            registered_bytes().replace(b"# original registry", b"# changed registry"),
            b"import os\n" + registered_bytes(),
        )
        for raw in variants:
            with self.subTest(raw=raw), self.source_fixture(raw) as fixture:
                self.assertIn("prior_native_test_bytes_not_preserved", self.checker.check_sources(fixture[0]))

    def test_missing_or_duplicate_hook_blocks(self):
        for raw in (PRIOR_BYTES, registered_bytes(REGISTRATION_BLOCK * 2)):
            with self.subTest(raw=raw), self.source_fixture(raw) as fixture:
                self.assertIn("v012_registration_block_missing_or_nonunique", self.checker.check_sources(fixture[0]))

    def test_comment_string_conditional_or_aliased_hook_cannot_register(self):
        variants = (
            "\n".join("# " + line for line in REGISTRATION_BLOCK.splitlines()) + "\n",
            "'''\n" + REGISTRATION_BLOCK + "'''\n",
            "if True:\n" + "\n".join("    " + line for line in REGISTRATION_BLOCK.splitlines()) + "\n",
            REGISTRATION_BLOCK.replace("import load_extension_tests\n", "import load_extension_tests as hidden\n"),
        )
        for block in variants:
            with self.subTest(block=block), self.source_fixture(registered_bytes(block)) as fixture:
                self.assertIn("v012_load_tests_ast_invalid", self.checker.check_sources(fixture[0]))

    def test_replacing_or_executing_existing_suite_blocks(self):
        variants = (
            REGISTRATION_BLOCK.replace("    return tests\n", "    return unittest.TestSuite()\n"),
            REGISTRATION_BLOCK.replace("    tests.addTests", "    tests = unittest.TestSuite()\n    tests.addTests", 1),
            REGISTRATION_BLOCK.replace("    return tests\n", "    tests.run(unittest.TestResult())\n    return tests\n"),
        )
        for block in variants:
            with self.subTest(block=block), self.source_fixture(registered_bytes(block)) as fixture:
                self.assertIn("v012_load_tests_ast_invalid", self.checker.check_sources(fixture[0]))

    def test_hook_after_main_or_second_definition_blocks(self):
        variants = (
            (PRIOR_BYTES + REGISTRATION_BLOCK.encode(), "v012_load_tests_after_main"),
            (registered_bytes() + b"\ndef load_tests(loader, tests, pattern):\n    return tests\n", "v012_load_tests_ast_invalid"),
        )
        for raw, issue in variants:
            with self.subTest(issue=issue), self.source_fixture(raw) as fixture:
                self.assertIn(issue, self.checker.check_sources(fixture[0]))

    def test_invalid_native_syntax_or_encoding_blocks(self):
        for raw in (b"def broken(:\n", b"\xff\xfe"):
            with self.subTest(raw=raw), self.source_fixture(raw) as fixture:
                self.assertIn("native_test_registration_invalid", self.checker.check_sources(fixture[0]))

    def test_disabling_registration_keeps_pins_inventory_and_loader_check(self):
        with self.source_fixture() as (root, source, required, helper, registered):
            registered.unlink()
            self.assertEqual(self.checker.check_sources(root, False), ())
            source.write_bytes(b"drift\n")
            required.unlink()
            helper.write_bytes(b"drift\n")
            issues = self.checker.check_sources(root, False)
            self.assertIn("source_byte_drift:" + SOURCE_PATH, issues)
            self.assertIn("required_v012_file_missing:" + REQUIRED_PATH, issues)
            self.assertIn("extension_loader_byte_drift", issues)

    def test_checker_import_has_no_runtime_import(self):
        code = '''import importlib, sys
sys.path.insert(0, sys.argv[1])
class NoRuntime:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "runtime" or fullname.startswith("runtime."):
            raise AssertionError("source checker imported runtime")
        return None
sys.meta_path.insert(0, NoRuntime())
importlib.import_module(sys.argv[2])
print("static_source_checker_only")
'''
        result = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(ROOT), CHECKER_MODULE],
                                capture_output=True, text=True, timeout=20, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "static_source_checker_only")

    def test_namespace_parent_and_absolute_discovery_preserve_normal_ids(self):
        with self.helper_fixture() as (root, package):
            status, result = self.helper_process(root, run=True)
        self.assertEqual(status, 0, result)
        self.assertEqual(result["tests_run"], 3)
        self.assertEqual(result["loader_errors"], [])
        self.assertTrue(all(name.startswith(LOADER_MODULE + ".test_") for name in result["ids"]))

    def test_new_extension_module_is_discovered_without_editing_loader(self):
        with self.helper_fixture() as (root, package):
            (package / "test_future_v0_13.py").write_text(
                "import unittest\nclass FutureTests(unittest.TestCase):\n    def test_future(self): pass\n",
                encoding="utf-8",
            )
            (package / "not_a_test.py").write_text("raise RuntimeError('not selected')\n", encoding="utf-8")
            status, result = self.helper_process(root, run=True)
        self.assertEqual(status, 0, result)
        self.assertEqual(result["tests_run"], 4)
        self.assertTrue(any("test_future_v0_13.FutureTests.test_future" in name for name in result["ids"]))

    def test_source_preflight_runs_before_importing_extension_test_modules(self):
        with self.helper_fixture(("controlled_source_drift",)) as (root, package):
            marker = root / "module_was_imported"
            (package / REQUIRED_TEST_FILES[0]).write_text(
                "from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('imported')\n",
                encoding="utf-8",
            )
            status, result = self.helper_process(root)
            self.assertFalse(marker.exists())
        self.assertNotEqual(status, 0)
        self.assertIn("controlled_source_drift", result["error"])

    def test_empty_missing_or_skipped_required_module_does_not_turn_green(self):
        for kind in ("empty", "missing", "skip"):
            with self.subTest(kind=kind), self.helper_fixture() as (root, package):
                module = package / REQUIRED_TEST_FILES[0]
                if kind == "missing":
                    module.unlink()
                else:
                    module.write_text("" if kind == "empty" else "import unittest\nraise unittest.SkipTest('must not hide required tests')\n", encoding="utf-8")
                status, result = self.helper_process(root, run=True)
                self.assertNotEqual(status, 0, result)
                self.assertIn("required_extension_tests_not_discovered", result["error"])

    def test_syntax_error_stays_a_standard_unittest_failure(self):
        with self.helper_fixture() as (root, package):
            (package / "test_added_broken.py").write_text("def broken(:\n", encoding="utf-8")
            status, result = self.helper_process(root, run=True)
        self.assertEqual(status, 1, result)
        self.assertEqual(result["errors"], 1)
        self.assertTrue(result["loader_errors"])
        self.assertIn("SyntaxError", result["output"])

    def test_failing_extension_case_is_not_run_or_hidden_by_loader(self):
        with self.helper_fixture() as (root, package):
            (package / REQUIRED_TEST_FILES[0]).write_text(
                "import unittest\nclass FixtureTests(unittest.TestCase):\n"
                "    def test_case(self): self.fail('visible failure')\n",
                encoding="utf-8",
            )
            loaded, _ = self.helper_process(root)
            status, result = self.helper_process(root, run=True)
        self.assertEqual(loaded, 0)
        self.assertEqual(status, 1, result)
        self.assertEqual(result["failures"], 1)
        self.assertIn("visible failure", result["output"])

    def test_duplicate_imported_case_ids_fail_closed(self):
        with self.helper_fixture() as (root, package):
            (package / "test_duplicate.py").write_text(
                "from .test_mediator_transition_v0_12 import FixtureTests\n", encoding="utf-8"
            )
            status, result = self.helper_process(root)
        self.assertNotEqual(status, 0, result)
        self.assertIn("duplicate_extension_test_id", result["error"])

    def test_foreign_cached_test_module_is_rejected_by_standard_discovery(self):
        with self.helper_fixture() as (root, package):
            status, result = self.helper_process(root, foreign=True)
        self.assertNotEqual(status, 0, result)
        self.assertIn("incorrectly imported", result["error"])

    def test_actual_native_entry_retains_seven_cases_and_normal_extension_ids_once(self):
        package = import_module(LOADER_MODULE)
        self.assertFalse(hasattr(package, "load_tests"))
        with patch.object(unittest.TestSuite, "run", side_effect=AssertionError("discovery must not execute tests")):
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromName(NATIVE_MODULE)
        ids = list(case_ids(suite))
        self.assertEqual(loader.errors, [])
        self.assertEqual(sum(name.startswith(NATIVE_MODULE + ".NativePlanActTests.") for name in ids), 7)
        for file in REQUIRED_TEST_FILES:
            prefix = LOADER_MODULE + "." + file.removesuffix(".py") + "."
            self.assertTrue(any(name.startswith(prefix) for name in ids), prefix)
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
