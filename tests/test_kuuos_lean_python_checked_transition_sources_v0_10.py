"""Source bytes and executable cumulative discovery for v0.10.

These checks do not execute Lean, authenticate issuers or prove refinement.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


CHECKER_MODULE = "scripts.check_kuuos_lean_python_checked_transition_sources_v0_10"
REPOSITORY = Path(__file__).resolve().parents[1]
REGISTRATION_PATH = "tests/test_kuuos_lean_python_os_registry_v0_5.py"
SOURCE_PATH = "runtime/original.py"
# The Git blob for the literal bytes b"hello\n", independently fixed here.
SOURCE_BLOB = "ce013625030ba8dba906f756967f9e9ca394464a"
REQUIRED_PATH = "docs/new-contract.md"

PRIOR_IMPORT_TEXT = '''from __future__ import annotations
from dataclasses import FrozenInstanceError
from importlib.util import find_spec
import unittest
from runtime import kuuos_lean_python_os_registry_v0_5 as registry
from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    ADDITIONAL_PROOF_LINKS, CORE_CONTRACTS,
)
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import HANDOFF_CONTRACTS
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import EDGE_SPECS
from tests.test_kuuos_lean_python_os_path_composition_v0_6 import (
    CompositionContractTests, NativeCompositionTests,
)
from tests.test_kuuos_lean_python_native_cycle_ledger_replay_v0_7 import (
    SourcePinTests, NativeCycleLedgerReplayTests,
)
from tests.test_kuuos_lean_python_native_cycle_receipt_capture_v0_8 import (
    NativeCaptureV08Tests, CaptureSourceV08Tests,
)
from tests.test_kuuos_lean_python_isolated_native_evidence_v0_9 import (
    IsolatedNativeEvidenceTests, EvidenceSourcePinTests,
)
'''
NEW_IMPORT_LINES = (
    "from tests.test_kuuos_lean_python_checked_transition_v0_10 "
    "import CheckedTransitionTests",
    "from tests.test_kuuos_lean_python_guarded_native_cycle_v0_10 "
    "import GuardedNativeCycleTests",
    "from tests.test_kuuos_lean_python_checked_transition_sources_v0_10 "
    "import CheckedTransitionSourceTests",
)
NEW_MODULES = (
    "tests.test_kuuos_lean_python_checked_transition_v0_10",
    "tests.test_kuuos_lean_python_guarded_native_cycle_v0_10",
    "tests.test_kuuos_lean_python_checked_transition_sources_v0_10",
)


class CheckedTransitionSourceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(
            find_spec(CHECKER_MODULE),
            "the v0.10 source guard must be available before it can check sources",
        )
        self.checker = import_module(CHECKER_MODULE)

    @contextmanager
    def source_fixture(self, registration=None):
        with TemporaryDirectory(prefix="kuuos-v010-source-") as folder:
            root = Path(folder)
            source = root / SOURCE_PATH
            source.parent.mkdir(parents=True)
            source.write_bytes(b"hello\n")
            required = root / REQUIRED_PATH
            required.parent.mkdir(parents=True)
            required.write_text("required inventory\n", encoding="utf-8")
            registered = root / REGISTRATION_PATH
            registered.parent.mkdir(parents=True)
            registered.write_text(
                PRIOR_IMPORT_TEXT + "\n".join(NEW_IMPORT_LINES) + "\n"
                if registration is None else registration,
                encoding="utf-8",
            )
            with patch.object(self.checker, "SOURCE_BLOBS", {SOURCE_PATH: SOURCE_BLOB}), \
                 patch.object(self.checker, "REQUIRED_PATHS", (REQUIRED_PATH,)):
                yield root, source, required, registered

    def test_repository_sources_and_all_cumulative_tests_are_registered(self):
        self.assertEqual(self.checker.check_sources(REPOSITORY), ())

    def test_exact_source_bytes_and_original_import_alias_are_accepted(self):
        with self.source_fixture() as (root, source, required, registered):
            self.assertEqual(self.checker.check_sources(root), ())

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

    def test_matching_symlinked_source_bytes_are_not_accepted(self):
        with self.source_fixture() as (root, source, required, registered):
            target = root / "original-copy.py"
            target.write_bytes(source.read_bytes())
            source.unlink()
            source.symlink_to(target)
            errors = self.checker.check_sources(root)
        self.assertIn("source_symlink_not_allowed:" + SOURCE_PATH, errors)

    def test_symlinked_source_parent_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            original_parent = root / "saved-runtime"
            source.parent.rename(original_parent)
            (root / "runtime").symlink_to(original_parent, target_is_directory=True)
            errors = self.checker.check_sources(root)
        self.assertIn("source_symlink_not_allowed:" + SOURCE_PATH, errors)

    def test_unreadable_original_is_reported_without_raising(self):
        with self.source_fixture() as (root, source, required, registered):
            read_bytes = Path.read_bytes

            def unreadable(candidate):
                if candidate == source:
                    raise PermissionError("controlled unreadable source")
                return read_bytes(candidate)

            # chmod cannot make a file unreadable to a privileged CI user.
            # Only the targeted filesystem read is replaced; parsing and pins run.
            with patch.object(Path, "read_bytes", unreadable):
                errors = self.checker.check_sources(root)
        self.assertIn("source_unreadable:" + SOURCE_PATH, errors)

    def test_directory_cannot_replace_a_pinned_source_file(self):
        with self.source_fixture() as (root, source, required, registered):
            source.unlink()
            source.mkdir()
            errors = self.checker.check_sources(root)
        self.assertIn("source_not_regular_file:" + SOURCE_PATH, errors)

    def test_missing_required_new_file_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            required.unlink()
            errors = self.checker.check_sources(root)
        self.assertIn("required_v010_file_missing:" + REQUIRED_PATH, errors)

    def test_required_new_file_cannot_be_a_symlink(self):
        with self.source_fixture() as (root, source, required, registered):
            required.unlink()
            required.symlink_to(source)
            errors = self.checker.check_sources(root)
        self.assertIn("required_v010_file_symlink_not_allowed:" + REQUIRED_PATH, errors)

    def test_missing_registration_file_is_blocked(self):
        with self.source_fixture() as (root, source, required, registered):
            registered.unlink()
            errors = self.checker.check_sources(root)
        self.assertIn("cumulative_test_module_missing", errors)

    def test_registration_can_be_disabled_without_disabling_source_checks(self):
        with self.source_fixture() as (root, source, required, registered):
            registered.unlink()
            self.assertEqual(self.checker.check_sources(root, check_registration=False), ())
            source.write_bytes(b"drift\n")
            errors = self.checker.check_sources(root, check_registration=False)
        self.assertIn("source_byte_drift:" + SOURCE_PATH, errors)

    def test_comments_and_string_literals_do_not_register_test_classes(self):
        for transform in (lambda line: "# " + line, repr):
            text = PRIOR_IMPORT_TEXT + "\n".join(map(transform, NEW_IMPORT_LINES))
            with self.subTest(transform=transform), self.source_fixture(text) as fixture:
                errors = self.checker.check_sources(fixture[0])
            for module in NEW_MODULES:
                self.assertIn("v010_tests_not_registered:" + module, errors)

    def test_each_new_test_class_must_be_imported(self):
        for omitted in range(len(NEW_IMPORT_LINES)):
            text = PRIOR_IMPORT_TEXT + "\n".join(
                line for index, line in enumerate(NEW_IMPORT_LINES) if index != omitted
            )
            with self.subTest(module=NEW_MODULES[omitted]), self.source_fixture(text) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v010_tests_not_registered:" + NEW_MODULES[omitted], errors)

    def test_aliased_new_classes_do_not_satisfy_registration(self):
        for alias in ("HiddenTests", "CheckedTransitionTests"):
            lines = list(NEW_IMPORT_LINES)
            lines[0] += " as " + alias
            text = PRIOR_IMPORT_TEXT + "\n".join(lines)
            with self.subTest(alias=alias), self.source_fixture(text) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v010_tests_not_registered:" + NEW_MODULES[0], errors)

    def test_conditional_or_nested_imports_do_not_satisfy_registration(self):
        for header in ("if True:", "if False:", "def delayed_registration():"):
            text = PRIOR_IMPORT_TEXT + header + "\n" + "\n".join(
                "    " + line for line in NEW_IMPORT_LINES
            ) + "\n"
            with self.subTest(header=header), self.source_fixture(text) as fixture:
                errors = self.checker.check_sources(fixture[0])
            for module in NEW_MODULES:
                self.assertIn("v010_tests_not_registered:" + module, errors)

    def test_duplicate_or_expanded_new_import_is_blocked(self):
        variants = (
            NEW_IMPORT_LINES + (NEW_IMPORT_LINES[0],),
            (NEW_IMPORT_LINES[0] + ", InventedTests",) + NEW_IMPORT_LINES[1:],
        )
        for lines in variants:
            text = PRIOR_IMPORT_TEXT + "\n".join(lines)
            with self.subTest(lines=lines), self.source_fixture(text) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("v010_tests_not_registered:" + NEW_MODULES[0], errors)

    def test_missing_or_aliased_prior_classes_are_blocked(self):
        for replacement in ("CaptureSourceV08Tests,", "NativeCaptureV08Tests as HiddenTests, CaptureSourceV08Tests,"):
            prior = PRIOR_IMPORT_TEXT.replace(
                "NativeCaptureV08Tests, CaptureSourceV08Tests,", replacement
            )
            text = prior + "\n".join(NEW_IMPORT_LINES)
            with self.subTest(replacement=replacement), self.source_fixture(text) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("prior_imports_not_preserved", errors)

    def test_prior_import_and_class_order_are_preserved(self):
        first = "from dataclasses import FrozenInstanceError\n"
        second = "from importlib.util import find_spec\n"
        variants = (
            PRIOR_IMPORT_TEXT.replace(first + second, second + first),
            PRIOR_IMPORT_TEXT.replace(
                "SourcePinTests, NativeCycleLedgerReplayTests,",
                "NativeCycleLedgerReplayTests, SourcePinTests,",
            ),
        )
        for prior in variants:
            text = prior + "\n".join(NEW_IMPORT_LINES)
            with self.subTest(prior=prior), self.source_fixture(text) as fixture:
                errors = self.checker.check_sources(fixture[0])
            self.assertIn("prior_imports_not_preserved", errors)

    def test_invalid_registration_syntax_is_blocked(self):
        with self.source_fixture("from broken import (\n") as fixture:
            errors = self.checker.check_sources(fixture[0])
        self.assertIn("cumulative_test_registration_invalid", errors)

    def test_checker_import_does_not_import_runtime(self):
        script = '''import importlib, sys
sys.path.insert(0, sys.argv[1])
class NoRuntime:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "runtime" or fullname.startswith("runtime."):
            raise AssertionError("source guard must not import runtime")
        return None
sys.meta_path.insert(0, NoRuntime())
importlib.import_module(sys.argv[2])
print("source_guard_loaded_without_runtime")
'''
        completed = subprocess.run(
            [sys.executable, "-I", "-c", script, str(REPOSITORY), CHECKER_MODULE],
            capture_output=True, text=True, timeout=20, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "source_guard_loaded_without_runtime")


if __name__ == "__main__":
    unittest.main()
