"""Static source and declared-test inventory checks for the Wa numeric gate.

These tests check the v0.13 checker when it is invoked. The immutable v0.12
loader does not require every future version's tests to exist or to run.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from contextlib import contextmanager
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
CHECKER_MODULE = "scripts.check_kuuos_lean_python_wa_numeric_sources_v0_13"
SOURCE_PATH = "runtime/original.py"
SOURCE_BLOB = "ce013625030ba8dba906f756967f9e9ca394464a"  # b"hello\n"
DOC_PATH = "docs/required-v013.md"
TEST_PATH = "tests/lean_python_extensions/test_required_v0_13.py"
TEST_CLASS = "RequiredTests"
TEST_NAME = "tests.lean_python_extensions.test_required_v0_13.RequiredTests"
TEST_BYTES = (
    b"import unittest\n"
    b"class RequiredTests(unittest.TestCase):\n"
    b"    def test_one(self):\n        pass\n"
)
V012_PRESERVED_PATHS = (
    "docs/KUUOS_LEAN_PYTHON_MEDIATOR_TRANSITIONS_v0_12.md",
    "runtime/kuuos_lean_python_mediated_native_cycle_v0_12.py",
    "runtime/kuuos_lean_python_mediator_transition_v0_12.py",
    "scripts/check_kuuos_lean_python_mediator_sources_v0_12.py",
    "tests/lean_python_extensions/__init__.py",
    "tests/lean_python_extensions/test_mediated_native_cycle_v0_12.py",
    "tests/lean_python_extensions/test_mediator_sources_v0_12.py",
    "tests/lean_python_extensions/test_mediator_transition_v0_12.py",
    "tests/test_kuuos_lean_python_plan_act_native_v0_4.py",
    "runtime/kuuos_belief_os_types_v0_1.py",
)


class WaNumericSourceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(find_spec(CHECKER_MODULE), "v0.13 source checker required")
        self.checker = import_module(CHECKER_MODULE)

    @contextmanager
    def source_fixture(self, test_bytes=TEST_BYTES):
        with TemporaryDirectory(prefix="kuuos-v013-source-") as directory:
            root = Path(directory)
            source = root / SOURCE_PATH
            source.parent.mkdir(parents=True)
            source.write_bytes(b"hello\n")
            doc = root / DOC_PATH
            doc.parent.mkdir(parents=True)
            doc.write_text("mandatory inventory\n", encoding="utf-8")
            tests = root / TEST_PATH
            tests.parent.mkdir(parents=True)
            tests.write_bytes(test_bytes)
            with patch.object(self.checker, "SOURCE_BLOBS", {SOURCE_PATH: SOURCE_BLOB}), \
                 patch.object(self.checker, "REQUIRED_PATHS", (DOC_PATH, TEST_PATH)), \
                 patch.object(self.checker, "TEST_CLASSES", {TEST_PATH: TEST_CLASS}):
                yield root, source, doc, tests

    def test_actual_sources_and_inventory(self):
        self.assertEqual(self.checker.check_sources(ROOT), ())

    def test_actual_declared_inventory_names_and_source_count(self):
        inventory = self.checker.declared_test_inventory(ROOT)
        expected = {
            "tests.lean_python_extensions.test_wa_numeric_guard_v0_13.WaNumericGuardTests",
            "tests.lean_python_extensions.test_wa_numeric_native_cycle_v0_13.WaNumericNativeCycleTests",
            "tests.lean_python_extensions.test_wa_numeric_sources_v0_13.WaNumericSourceTests",
        }
        self.assertEqual(set(inventory), expected)
        self.assertTrue(all(methods for methods in inventory.values()))
        own = "tests.lean_python_extensions.test_wa_numeric_sources_v0_13.WaNumericSourceTests"
        self.assertEqual(
            len(inventory[own]), unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases()
        )

    def test_prior_checks_and_fixed_extension_registration_remain_valid(self):
        for module in (
            "scripts.check_kuuos_lean_python_checked_transition_sources_v0_10",
            "scripts.check_kuuos_lean_python_pre_host_sources_v0_11",
            "scripts.check_kuuos_lean_python_mediator_sources_v0_12",
        ):
            with self.subTest(module=module):
                self.assertEqual(import_module(module).check_sources(ROOT), ())

    def test_prior_manifest_is_retained_and_every_preservation_pin_detects_drift(self):
        path = ROOT / "scripts/check_kuuos_lean_python_mediator_sources_v0_12.py"
        body = ast.parse(path.read_text(encoding="utf-8")).body
        prior = next(
            ast.literal_eval(node.value) for node in body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "SOURCE_BLOBS" for target in node.targets)
        )
        self.assertEqual({path: self.checker.SOURCE_BLOBS.get(path) for path in prior}, prior)
        self.assertTrue(set(V012_PRESERVED_PATHS).issubset(self.checker.SOURCE_BLOBS))
        with TemporaryDirectory(prefix="kuuos-v013-pins-") as directory:
            root = Path(directory)
            for path in self.checker.SOURCE_BLOBS:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / path).read_bytes())
            with patch.object(self.checker, "REQUIRED_PATHS", ()), \
                 patch.object(self.checker, "TEST_CLASSES", {}):
                self.assertEqual(self.checker.check_sources(root), ())
                for path in set(prior) | set(V012_PRESERVED_PATHS):
                    with self.subTest(path=path):
                        target = root / path
                        before = target.read_bytes()
                        try:
                            target.write_bytes(before + b"changed original\n")
                            errors = self.checker.check_sources(root)
                        finally:
                            target.write_bytes(before)
                        self.assertIn("source_byte_drift:" + path, errors)

    def test_exact_fixture_and_ordinary_method_inventory_pass(self):
        with self.source_fixture() as (root, *_):
            self.assertEqual(self.checker.check_sources(root), ())
            self.assertEqual(self.checker.declared_test_inventory(root), {TEST_NAME: ("test_one",)})

    def test_original_byte_drift_missing_and_nonregular_file_block(self):
        for kind in ("drift", "missing", "directory"):
            with self.subTest(kind=kind), self.source_fixture() as (root, source, *_):
                if kind == "drift":
                    source.write_bytes(b"altered original\n")
                else:
                    source.unlink()
                    if kind == "directory":
                        source.mkdir()
                errors = self.checker.check_sources(root)
                code = {"drift": "byte_drift", "missing": "missing", "directory": "not_regular_file"}[kind]
                self.assertIn("source_" + code + ":" + SOURCE_PATH, errors)

    def test_original_file_and_parent_symlinks_block_even_with_matching_bytes(self):
        for parent in (False, True):
            with self.subTest(parent=parent), self.source_fixture() as (root, source, *_):
                if parent:
                    saved = root / "saved-runtime"
                    source.parent.rename(saved)
                    (root / "runtime").symlink_to(saved, target_is_directory=True)
                else:
                    saved = root / "saved.py"
                    source.rename(saved)
                    source.symlink_to(saved)
                self.assertIn("source_symlink_not_allowed:" + SOURCE_PATH, self.checker.check_sources(root))

    def test_unreadable_original_is_reported_without_raising(self):
        with self.source_fixture() as (root, source, *_):
            read_bytes = Path.read_bytes
            def read(candidate):
                if candidate == source:
                    raise PermissionError("controlled denial")
                return read_bytes(candidate)
            with patch.object(Path, "read_bytes", read):
                errors = self.checker.check_sources(root)
            self.assertIn("source_unreadable:" + SOURCE_PATH, errors)

    def test_missing_nonregular_and_symlink_new_inventory_block(self):
        for kind in ("missing", "directory", "symlink"):
            with self.subTest(kind=kind), self.source_fixture() as (root, source, doc, tests):
                doc.unlink()
                if kind == "directory":
                    doc.mkdir()
                elif kind == "symlink":
                    doc.symlink_to(source)
                errors = self.checker.check_sources(root)
                code = {"missing": "missing", "directory": "not_regular_file", "symlink": "symlink_not_allowed"}[kind]
                self.assertIn("required_v013_file_" + code + ":" + DOC_PATH, errors)

    def test_missing_new_test_is_blocked_when_checker_is_invoked(self):
        with self.source_fixture() as (root, source, doc, tests):
            tests.unlink()
            errors = self.checker.check_sources(root)
            self.assertIn("required_v013_file_missing:" + TEST_PATH, errors)
            self.assertIn("test_source_missing:" + TEST_PATH, errors)
            self.assertEqual(self.checker.declared_test_inventory(root), {})

    def test_unreadable_nonregular_and_symlink_test_module_block(self):
        for kind in ("unreadable", "directory", "symlink"):
            with self.subTest(kind=kind), self.source_fixture() as (root, source, doc, tests):
                read_bytes = Path.read_bytes
                def read(candidate):
                    if candidate == tests and kind == "unreadable":
                        raise PermissionError("controlled test denial")
                    return read_bytes(candidate)
                if kind != "unreadable":
                    tests.unlink()
                    if kind == "directory":
                        tests.mkdir()
                    else:
                        tests.symlink_to(source)
                with patch.object(Path, "read_bytes", read):
                    errors = self.checker.check_sources(root)
                code = {"unreadable": "unreadable", "directory": "not_regular_file", "symlink": "symlink_not_allowed"}[kind]
                self.assertIn("test_source_" + code + ":" + TEST_PATH, errors)

    def test_missing_comment_string_conditional_or_imported_class_is_not_a_declaration(self):
        variants = (
            b"", b"# class RequiredTests: pass\n", b"'class RequiredTests: pass'\n",
            b"class DifferentTests:\n    def test_one(self): pass\n",
            b"if True:\n    class RequiredTests:\n        def test_one(self): pass\n",
            b"from somewhere import RequiredTests\n",
        )
        for raw in variants:
            with self.subTest(raw=raw), self.source_fixture(raw) as (root, *_):
                self.assertIn("required_test_class_missing_or_nonunique:" + TEST_PATH + ":" + TEST_CLASS,
                              self.checker.check_sources(root))

    def test_duplicate_class_declarations_do_not_inflate_inventory(self):
        with self.source_fixture(TEST_BYTES + TEST_BYTES) as (root, *_):
            self.assertIn("required_test_class_missing_or_nonunique:" + TEST_PATH + ":" + TEST_CLASS,
                          self.checker.check_sources(root))

    def test_empty_or_async_only_class_has_no_ordinary_test_methods(self):
        for raw in (b"class RequiredTests:\n    pass\n",
                    b"class RequiredTests:\n    async def test_async(self): pass\n"):
            with self.subTest(raw=raw), self.source_fixture(raw) as (root, *_):
                self.assertIn("required_test_methods_missing:" + TEST_PATH + ":" + TEST_CLASS,
                              self.checker.check_sources(root))

    def test_duplicate_method_declarations_are_not_counted_as_two_tests(self):
        raw = TEST_BYTES + b"    def test_one(self):\n        pass\n"
        with self.source_fixture(raw) as (root, *_):
            self.assertIn("duplicate_test_method_name:" + TEST_PATH + ":" + TEST_CLASS,
                          self.checker.check_sources(root))

    def test_invalid_syntax_or_encoding_stays_an_error(self):
        for raw in (b"def invalid(:\n", b"\xff\xfe"):
            with self.subTest(raw=raw), self.source_fixture(raw) as (root, *_):
                self.assertIn("test_source_invalid:" + TEST_PATH, self.checker.check_sources(root))

    def test_arbitrary_module_imports_and_bodies_are_not_executed(self):
        raw = (b"raise AssertionError('do not execute module bodies')\n"
               b"import nonexistent_kuuos_test_dependency\n" + TEST_BYTES)
        with self.source_fixture(raw) as (root, *_):
            self.assertEqual(self.checker.check_sources(root), ())
            self.assertEqual(self.checker.declared_test_inventory(root), {TEST_NAME: ("test_one",)})

    def test_declared_inventory_is_sorted_and_excludes_nested_helpers_and_comments(self):
        raw = (
            b"class RequiredTests:\n"
            b"    def test_z(self): pass\n"
            b"    def helper(self):\n        def test_nested(): pass\n"
            b"    # def test_comment(self): pass\n"
            b"    def test_a(self): pass\n"
        )
        with self.source_fixture(raw) as (root, *_):
            self.assertEqual(self.checker.declared_test_inventory(root), {TEST_NAME: ("test_a", "test_z")})

    def test_checker_import_is_static_and_does_not_import_runtime_or_tests(self):
        program = '''import importlib, sys
sys.path.insert(0, sys.argv[1])
class StaticImportsOnly:
    def find_spec(self, fullname, path=None, target=None):
        if (fullname == "runtime" or fullname.startswith("runtime.")
                or fullname == "tests" or fullname.startswith("tests.")):
            raise AssertionError("checker imported runtime or test code")
        return None
sys.meta_path.insert(0, StaticImportsOnly())
importlib.import_module(sys.argv[2])
print("static_checker_only")
'''
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", program, str(ROOT), CHECKER_MODULE],
            capture_output=True, text=True, timeout=20, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "static_checker_only")


if __name__ == "__main__":
    unittest.main()
