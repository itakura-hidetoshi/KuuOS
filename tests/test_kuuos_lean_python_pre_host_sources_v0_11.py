"""Local static source and cumulative discovery checks for the pre-host guard.

No runtime import, Lean execution, external authenticity or refinement is
inferred from the source guard's result.
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


CHECKER_MODULE = "scripts.check_kuuos_lean_python_pre_host_sources_v0_11"
REPOSITORY = Path(__file__).resolve().parents[1]
REGISTRATION_PATH = "tests/test_kuuos_lean_python_os_registry_v0_5.py"
SOURCE_PATH = "runtime/original.py"
SOURCE_BLOB = "ce013625030ba8dba906f756967f9e9ca394464a"  # b"hello\n"
REQUIRED_PATH = "docs/new-contract.md"
PRIOR_BYTES = (
    b'# original registry\nimport unittest\n\n'
    b'if __name__ == "__main__":\n    unittest.main()\n'
)
PRIOR_BLOB = "81a369ebb4266a93cf3c35ece56cbdb38c95e28d"
REGISTRATION_BLOCK = '''# v0.11 adds pre-host tests while retaining the complete existing suite.
def load_tests(loader, tests, pattern):
    from tests.test_kuuos_lean_python_pre_host_guard_v0_11 import PreHostGuardTests
    from tests.test_kuuos_lean_python_pre_host_native_cycle_v0_11 import PreHostNativeCycleTests
    from tests.test_kuuos_lean_python_pre_host_sources_v0_11 import PreHostSourceTests

    tests.addTests(loader.loadTestsFromTestCase(PreHostGuardTests))
    tests.addTests(loader.loadTestsFromTestCase(PreHostNativeCycleTests))
    tests.addTests(loader.loadTestsFromTestCase(PreHostSourceTests))
    return tests


'''


def registered_bytes(block=REGISTRATION_BLOCK):
    anchor = b'if __name__ == "__main__":'
    return PRIOR_BYTES.replace(anchor, block.encode("utf-8") + anchor, 1)


class PreHostSourceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(
            find_spec(CHECKER_MODULE), "the pre-host source checker is required"
        )
        self.checker = import_module(CHECKER_MODULE)

    @contextmanager
    def source_fixture(self, registration=None):
        with TemporaryDirectory(prefix="kuuos-v011-source-") as folder:
            root = Path(folder)
            source = root / SOURCE_PATH
            source.parent.mkdir(parents=True)
            source.write_bytes(b"hello\n")
            required = root / REQUIRED_PATH
            required.parent.mkdir(parents=True)
            required.write_text("required inventory\n", encoding="utf-8")
            registered = root / REGISTRATION_PATH
            registered.parent.mkdir(parents=True)
            registered.write_bytes(
                registered_bytes() if registration is None else registration
            )
            with patch.object(self.checker, "SOURCE_BLOBS", {SOURCE_PATH: SOURCE_BLOB}), \
                 patch.object(self.checker, "REQUIRED_PATHS", (REQUIRED_PATH,)), \
                 patch.object(self.checker, "PRIOR_REGISTRATION_BLOB", PRIOR_BLOB):
                yield root, source, required, registered

    def test_actual_repository_sources_inventory_and_registration(self):
        self.assertEqual(self.checker.check_sources(REPOSITORY), ())

    def test_previous_v010_checker_still_accepts_original_top_level_imports(self):
        previous = import_module(
            "scripts.check_kuuos_lean_python_checked_transition_sources_v0_10"
        )
        self.assertEqual(previous.check_sources(REPOSITORY), ())

    def test_exact_original_bytes_with_additive_hook_are_accepted(self):
        with self.source_fixture() as (root, source, required, registered):
            self.assertEqual(self.checker.check_sources(root), ())

    def test_every_preceding_source_pin_still_detects_changed_bytes(self):
        prior_script = REPOSITORY / "scripts/check_kuuos_lean_python_checked_transition_sources_v0_10.py"
        body = ast.parse(prior_script.read_text(encoding="utf-8")).body
        prior_pins = next(
            ast.literal_eval(node.value) for node in body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "SOURCE_BLOBS"
                    for target in node.targets)
        )
        with TemporaryDirectory(prefix="kuuos-v011-prior-pins-") as folder:
            root = Path(folder)
            for relative in set(prior_pins) | set(self.checker.SOURCE_BLOBS):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((REPOSITORY / relative).read_bytes())
            with patch.object(self.checker, "REQUIRED_PATHS", ()):
                self.assertEqual(self.checker.check_sources(root, False), ())
                for relative in prior_pins:
                    with self.subTest(source=relative):
                        target = root / relative
                        original = target.read_bytes()
                        try:
                            target.write_bytes(original + b"\nchanged\n")
                            errors = self.checker.check_sources(root, False)
                        finally:
                            target.write_bytes(original)
                        self.assertIn("source_byte_drift:" + relative, errors)

    def test_source_byte_drift_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            source.write_bytes(b"changed original\n")
            errors = self.checker.check_sources(root)
        self.assertIn("source_byte_drift:" + SOURCE_PATH, errors)

    def test_missing_original_source_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            source.unlink()
            errors = self.checker.check_sources(root)
        self.assertIn("source_missing:" + SOURCE_PATH, errors)

    def test_matching_source_symlink_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            copy = root / "original-copy.py"
            copy.write_bytes(source.read_bytes())
            source.unlink()
            source.symlink_to(copy)
            errors = self.checker.check_sources(root)
        self.assertIn("source_symlink_not_allowed:" + SOURCE_PATH, errors)

    def test_source_parent_symlink_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            saved = root / "saved-runtime"
            source.parent.rename(saved)
            (root / "runtime").symlink_to(saved, target_is_directory=True)
            errors = self.checker.check_sources(root)
        self.assertIn("source_symlink_not_allowed:" + SOURCE_PATH, errors)

    def test_nonregular_source_is_blocked_without_reading_it(self):
        with self.source_fixture() as (root, source, required, registered):
            source.unlink()
            source.mkdir()
            errors = self.checker.check_sources(root)
        self.assertIn("source_not_regular_file:" + SOURCE_PATH, errors)

    def test_unreadable_source_is_reported_without_raising(self):
        with self.source_fixture() as (root, source, required, registered):
            read_bytes = Path.read_bytes

            def unreadable(candidate):
                if candidate == source:
                    raise PermissionError("controlled unreadable source")
                return read_bytes(candidate)

            # Privileged CI users can bypass chmod; replace only this read.
            with patch.object(Path, "read_bytes", unreadable):
                errors = self.checker.check_sources(root)
        self.assertIn("source_unreadable:" + SOURCE_PATH, errors)

    def test_missing_required_new_file_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            required.unlink()
            errors = self.checker.check_sources(root)
        self.assertIn("required_v011_file_missing:" + REQUIRED_PATH, errors)

    def test_required_file_symlink_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            required.unlink()
            required.symlink_to(source)
            errors = self.checker.check_sources(root)
        self.assertIn("required_v011_file_symlink_not_allowed:" + REQUIRED_PATH, errors)

    def test_missing_registry_file_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            registered.unlink()
            errors = self.checker.check_sources(root)
        self.assertIn("cumulative_test_module_missing", errors)

    def test_registry_file_symlink_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            saved = root / "saved-registry.py"
            registered.rename(saved)
            registered.symlink_to(saved)
            errors = self.checker.check_sources(root)
        self.assertIn("cumulative_test_module_symlink_not_allowed", errors)

    def test_disabled_registration_keeps_source_and_inventory_checks(self):
        with self.source_fixture() as (root, source, required, registered):
            registered.unlink()
            self.assertEqual(self.checker.check_sources(root, False), ())
            source.write_bytes(b"drift\n")
            required.unlink()
            errors = self.checker.check_sources(root, False)
        self.assertIn("source_byte_drift:" + SOURCE_PATH, errors)
        self.assertIn("required_v011_file_missing:" + REQUIRED_PATH, errors)

    def test_missing_or_duplicate_hook_block_is_blocked(self):
        variants = (PRIOR_BYTES, registered_bytes(REGISTRATION_BLOCK * 2))
        for raw in variants:
            with self.subTest(raw=raw), self.source_fixture(raw) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v011_registration_block_missing_or_nonunique", errors)

    def test_comments_or_string_literal_cannot_register_load_tests(self):
        commented = "\n".join("# " + line for line in REGISTRATION_BLOCK.splitlines()) + "\n"
        quoted = "'''\n" + REGISTRATION_BLOCK + "'''\n"
        for block in (commented, quoted):
            with self.subTest(block=block), self.source_fixture(registered_bytes(block)) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v011_load_tests_ast_invalid", errors)

    def test_conditional_or_nested_load_tests_is_blocked(self):
        for header in ("if True:\n", "def delayed_registration():\n"):
            block = header + "\n".join("    " + line for line in REGISTRATION_BLOCK.splitlines()) + "\n"
            with self.subTest(header=header), self.source_fixture(registered_bytes(block)) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v011_load_tests_ast_invalid", errors)

    def test_aliased_or_wrong_test_class_is_blocked(self):
        variants = (
            REGISTRATION_BLOCK.replace("import PreHostGuardTests\n", "import PreHostGuardTests as HiddenTests\n"),
            REGISTRATION_BLOCK.replace("import PreHostGuardTests\n", "import InventedTests\n"),
        )
        for block in variants:
            with self.subTest(block=block), self.source_fixture(registered_bytes(block)) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v011_load_tests_ast_invalid", errors)

    def test_each_new_class_must_be_added_to_the_existing_suite(self):
        for name in ("PreHostGuardTests", "PreHostNativeCycleTests", "PreHostSourceTests"):
            block = REGISTRATION_BLOCK.replace(
                "    tests.addTests(loader.loadTestsFromTestCase(" + name + "))\n", ""
            )
            with self.subTest(name=name), self.source_fixture(registered_bytes(block)) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v011_load_tests_ast_invalid", errors)

    def test_replacing_existing_suite_or_returning_new_suite_is_blocked(self):
        variants = (
            REGISTRATION_BLOCK.replace("    return tests\n", "    return unittest.TestSuite()\n"),
            REGISTRATION_BLOCK.replace("    tests.addTests", "    tests = unittest.TestSuite()\n    tests.addTests", 1),
        )
        for block in variants:
            with self.subTest(block=block), self.source_fixture(registered_bytes(block)) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v011_load_tests_ast_invalid", errors)

    def test_even_comment_drift_in_prior_registry_bytes_is_blocked(self):
        raw = registered_bytes().replace(b"# original registry", b"# changed registry")
        with self.source_fixture(raw) as fixture:
            errors = self.checker.check_sources(fixture[0])
        self.assertIn("prior_registry_bytes_not_preserved", errors)

    def test_new_top_level_import_cannot_replace_function_local_registration(self):
        raw = b"from tests.test_kuuos_lean_python_pre_host_guard_v0_11 import PreHostGuardTests\n" + registered_bytes()
        with self.source_fixture(raw) as fixture:
            errors = self.checker.check_sources(fixture[0])
        self.assertIn("prior_registry_bytes_not_preserved", errors)

    def test_hook_after_main_entrypoint_is_blocked(self):
        raw = PRIOR_BYTES + REGISTRATION_BLOCK.encode("utf-8")
        with self.source_fixture(raw) as fixture:
            errors = self.checker.check_sources(fixture[0])
        self.assertIn("v011_load_tests_after_main", errors)

    def test_second_load_tests_definition_is_blocked(self):
        raw = registered_bytes() + b"\ndef load_tests(loader, tests, pattern):\n    return tests\n"
        with self.source_fixture(raw) as fixture:
            errors = self.checker.check_sources(fixture[0])
        self.assertIn("v011_load_tests_ast_invalid", errors)

    def test_invalid_registry_syntax_or_encoding_is_blocked(self):
        for raw in (b"def broken(:\n", b"\xff\xfe"):
            with self.subTest(raw=raw), self.source_fixture(raw) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("cumulative_test_registration_invalid", errors)

    def test_checker_import_does_not_import_runtime(self):
        script = '''import importlib, sys
sys.path.insert(0, sys.argv[1])
class NoRuntime:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "runtime" or fullname.startswith("runtime."):
            raise AssertionError("source checker must not import runtime")
        return None
sys.meta_path.insert(0, NoRuntime())
importlib.import_module(sys.argv[2])
print("pre_host_source_checker_loaded_without_runtime")
'''
        completed = subprocess.run(
            [sys.executable, "-I", "-c", script, str(REPOSITORY), CHECKER_MODULE],
            capture_output=True, text=True, timeout=20, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "pre_host_source_checker_loaded_without_runtime")


if __name__ == "__main__":
    unittest.main()
