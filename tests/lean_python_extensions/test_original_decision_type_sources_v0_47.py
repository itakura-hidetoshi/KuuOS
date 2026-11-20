"""v0.47 exact original imported-type and Lake registration source tests.

Static checks do not stand in for pinned Strict Lean elaboration.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import (
    check_kuuos_lean_python_original_decision_type_sources_v0_47 as checker,
)


class OriginalDecisionTypeSourceTests(unittest.TestCase):
    def test_prior_original_native_three_kernel_pins_are_unchanged(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())

    def test_exact_original_receipt_type_and_mapped_bridge_have_same_fields(self):
        first, error = checker._read(
            checker.ROOT,
            "formal/KUOS/DecisionOS/BoundedPlanSynthesisRequestHandoffV0_8.lean",
        )
        self.assertIsNone(error)
        second, error = checker._read(
            checker.ROOT,
            "formal/KUOS/Architecture/LeanPythonDecisionVerifyPlanNativeHandoffV0_46.lean",
        )
        self.assertIsNone(error)
        original = first.decode("utf-8")
        mapped = second.decode("utf-8")
        self.assertEqual(len(checker._original_fields(original)), 35)
        self.assertEqual(checker._original_fields(original),
                         checker._mapped_fields(mapped))
        self.assertEqual(len(checker._original_validity_fields(original)), 35)
        self.assertEqual(checker._original_validity_fields(original),
                         checker._mapped_validity_fields(mapped))

    def test_exact_ten_legacy_build_modules_only(self):
        self.assertEqual(len(checker.LEGACY_MODULES), 10)
        self.assertEqual(len(set(checker.LEGACY_MODULES)), 10)
        raw, error = checker._read(checker.ROOT, "lakefile.toml")
        self.assertIsNone(error)
        lake = raw.decode("utf-8")
        for module in checker.LEGACY_MODULES:
            self.assertEqual(lake.count('"' + module + '"'), 1, module)
        self.assertNotIn('"KuuOS.*"', lake)

    def test_existing_107_root_registration_is_byte_preserved(self):
        raw, error = checker._read(checker.ROOT, "lakefile.toml")
        self.assertIsNone(error)
        self.assertEqual(raw.count(checker.LAKE_INSERT.encode("utf-8")), 1)
        self.assertEqual(
            checker._blob(raw.replace(checker.LAKE_INSERT.encode("utf-8"), b"", 1)),
            checker.ORIGINAL_LAKE_BLOB,
        )

    def test_all_original_sources_and_additive_registration_pass(self):
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_original_import_and_seven_lean_declarations_are_present(self):
        raw, error = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(error)
        lines = tuple(x.strip() for x in raw.decode("utf-8").splitlines())
        self.assertEqual(len(checker.LEAN_IMPORTS), 3)
        self.assertEqual(len(checker.LEAN_DECLARATIONS), 7)
        for name in checker.LEAN_IMPORTS:
            self.assertIn(name, lines)
        for name in checker.LEAN_DECLARATIONS:
            self.assertTrue(any(
                l == name or l.startswith(name + " ") or l.startswith(name + ":")
                for l in lines
            ), name)

    def test_reverse_map_and_validity_iff_are_not_omitted(self):
        raw, error = checker._read(checker.ROOT, checker.NEW[0])
        self.assertIsNone(error)
        lean = raw.decode("utf-8")
        self.assertIn("left_inv := by", lean)
        self.assertIn("right_inv := by", lean)
        self.assertIn("BoundedPlanSynthesisRequestHandoffValid r ↔", lean)
        self.assertIn("SourceMappedDecisionHandoffValid (originalToMapped r)", lean)
        self.assertIn("WholeReceiptSeam Receipt decisionOutput verifySource", lean)

    def test_missing_prior_original_source_is_not_admitted(self):
        for name in checker.PINNED:
            with self.subTest(name=name), patch.dict(
                checker.PINNED, {name: "0" * 40},
            ):
                self.assertIn(
                    "v047_original_source_changed:" + name,
                    checker.check_sources(checker.ROOT),
                )

    def test_lakefile_inadvertent_extra_glob_is_blocked(self):
        original_read = checker._read
        def tampered_read(root, path):
            raw, error = original_read(root, path)
            if path == "lakefile.toml" and not error:
                raw += b'\n# unauthorized source or root expansion\n'
            return raw, error
        with patch.object(checker, "_read", side_effect=tampered_read):
            self.assertIn(
                "v047_canonical_lakefile_modified_outside_tight_addition",
                checker.check_sources(checker.ROOT),
            )

    def test_modified_or_missing_ten_module_registration_is_blocked(self):
        original_read = checker._read
        def tampered_read(root, path):
            raw, error = original_read(root, path)
            if path == "lakefile.toml" and not error:
                raw = raw.replace(
                    b'"KuuOS.PlanOSV102"', b'"KuuOS.PlanOSV103"', 1
                )
            return raw, error
        with patch.object(checker, "_read", side_effect=tampered_read):
            self.assertIn("v047_legacy_registration_incorrect",
                          checker.check_sources(checker.ROOT))

    def test_required_lean_file_missing_is_no_data_not_success(self):
        dummy = "formal/KUOS/Architecture/UnseenV047.lean"
        with patch.object(checker, "NEW", checker.NEW + (dummy,)):
            self.assertIn(
                "v047_new_file_missing:" + dummy,
                checker.check_sources(checker.ROOT),
            )

    def test_actual_unproved_lean_commands_are_rejected(self):
        for term in ("sorry", "admit", "axiom"):
            with self.subTest(term=term):
                self.assertTrue(
                    checker.prior.prior._contains_unproved_lean(
                        "theorem missing : True := by " + term
                    )
                )

    def test_identifier_prefix_and_comment_not_a_proof_hole(self):
        self.assertFalse(
            checker.prior.prior._contains_unproved_lean(
                'def admittedForStatus := true\n/- sorry axiom admit -/\n'
            )
        )

    def test_current_new_file_inventory_and_python_are_parseable(self):
        for path in checker.NEW:
            raw, error = checker._read(checker.ROOT, path)
            self.assertIsNone(error, path)
            self.assertTrue(raw, path)

    def test_untrusted_root_and_side_effectful_path_are_refused(self):
        class Hostile:
            def __fspath__(self):
                raise AssertionError("must not call path conversion")
        for root in (None, str(checker.ROOT), Hostile()):
            self.assertEqual(checker.check_sources(root),
                             ("root:trusted_path_required",))

    def test_path_traversal_and_symlink_alias_are_rejected(self):
        self.assertEqual(
            checker.check_sources(checker.ROOT / ".." / checker.ROOT.name),
            ("root:trusted_path_required",),
        )
        with TemporaryDirectory() as temp:
            alias = Path(temp) / "alias"
            alias.symlink_to(checker.ROOT, target_is_directory=True)
            self.assertEqual(
                checker.check_sources(alias),
                ("root:trusted_path_required",),
            )


if __name__ == "__main__":
    unittest.main()
