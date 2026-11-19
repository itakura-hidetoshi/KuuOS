"""Source-pinned Lean declaration and Python per-OS audit inventories, v0.27.

Static declarations and blob identity are not proof elaboration or
native runtime semantic correspondence. Copyright Hidetoshi Itakura.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_per_os_contracts_v0_27 as checker
from runtime.kuuos_lean_python_os_registry_v0_5 import OS_BINDINGS


class PerOSProofContractSourcesTests(unittest.TestCase):
    def test_all_twelve_actual_lean_sources_and_modules_match(self):
        self.assertEqual(set(checker.PROOF_SOURCES), set(OS_BINDINGS))
        self.assertEqual(set(checker.MODULES), set(OS_BINDINGS))
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_exact_original_lean_blob_pins_have_not_changed(self):
        for os_name, (path, expected) in checker.PROOF_SOURCES.items():
            with self.subTest(os=os_name):
                raw, issue = checker._read(checker.ROOT, path)
                self.assertIsNone(issue)
                self.assertEqual(checker._blob(raw), expected)

    def test_core_existing_python_registries_are_immutable(self):
        for path, sha in checker.BASE_BLOBS.items():
            with self.subTest(path=path):
                raw, issue = checker._read(checker.ROOT, path)
                self.assertIsNone(issue)
                self.assertEqual(checker._blob(raw), sha)

    def test_original_lean_pin_mutation_is_detected(self):
        original = checker.PROOF_SOURCES["PlanOS"]
        with patch.dict(checker.PROOF_SOURCES,
                        {"PlanOS": (original[0], "0" * 40)}):
            self.assertIn("lean_blob_changed:PlanOS",
                          checker.check_sources(checker.ROOT))

    def test_original_python_registry_pin_mutation_is_detected(self):
        path = "runtime/kuuos_lean_python_os_registry_v0_5.py"
        with patch.dict(checker.BASE_BLOBS, {path: "0" * 40}):
            self.assertIn("original_source_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_missing_python_os_module_is_detected(self):
        with patch.dict(checker.MODULES,
                        {"MemoryOS": "runtime/does_not_exist_v0_27.py"}):
            issues = checker.check_sources(checker.ROOT)
            self.assertTrue(any(
                issue.startswith("python_missing:MemoryOS")
                for issue in issues
            ))

    def test_missing_lean_theorem_name_is_not_silently_accepted(self):
        path = checker.PROOF_SOURCES["CodeAI"][0]
        original_read = checker._read

        def replaced(root: Path, item: str):
            if item == path:
                return b"theorem unrelated : True := by trivial\n", None
            return original_read(root, item)

        with patch.object(checker, "_read", side_effect=replaced):
            issues = checker.check_sources(checker.ROOT)
            self.assertIn("lean_blob_changed:CodeAI", issues)
            self.assertTrue(any(
                x.startswith("lean_declaration_not_found:CodeAI:")
                for x in issues
            ))

    def test_untrusted_root_is_no_data(self):
        self.assertEqual(checker.check_sources(None),
                         ("root:trusted_path_required",))

    def test_all_new_python_sources_are_present_and_parsed_statically(self):
        self.assertEqual(checker.check_sources(checker.ROOT), ())
        self.assertEqual(len(checker.MODULES), 12)
        self.assertEqual(len(checker.ADDITIVE), 4)

    def test_source_marker_check_never_grants_execution_authority(self):
        from runtime.kuuos_lean_python_per_os_contracts_v0_27 import (
            Verifier, LOCAL,
        )
        v = Verifier({"effectful": True}, fields=("effectful",))
        v.flag("effectful", True)
        audit = v.finish("PlanOS", checker.PROOF_SOURCES["PlanOS"][0],
                         ("effectfulStep_has_checkpoint",))
        self.assertEqual(audit.status, LOCAL)
        self.assertFalse(audit.lean_proof_term_constructed)
        self.assertFalse(audit.lean_python_refinement_proved)
        self.assertFalse(audit.execution_authority_granted)


if __name__ == "__main__":
    unittest.main()
