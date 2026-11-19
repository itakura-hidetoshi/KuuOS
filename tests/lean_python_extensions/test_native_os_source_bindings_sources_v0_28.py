"""v0.28 native original-state binding source pins and regression inventory.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_native_os_source_bindings_v0_28 as chk


class NativeOSSourceBindingSourceTests(unittest.TestCase):
    def test_original_native_and_lean_sources_match_all_fifteen_pins(self):
        self.assertEqual(len(chk.PINNED), 15)
        for path, expected in chk.PINNED.items():
            with self.subTest(path=path):
                content, problem = chk.prior._read(chk.ROOT, path)
                self.assertIsNone(problem)
                self.assertEqual(chk.prior._blob(content), expected)

    def test_real_prior_os_source_checker_still_succeeds(self):
        self.assertEqual(chk.prior.check_sources(chk.ROOT), ())

    def test_all_new_source_and_entrypoints_present(self):
        self.assertEqual(len(chk.NEW), 10)
        self.assertEqual(len(chk.EXPECTED_BINDING_FUNCTIONS), 5)
        self.assertEqual(chk.check_sources(chk.ROOT), ())

    def test_original_source_pin_drift_is_blocked(self):
        first = next(iter(chk.PINNED))
        with patch.dict(chk.PINNED, {first: "0" * 40}):
            self.assertIn("original_source_drift:" + first,
                          chk.check_sources(chk.ROOT))

    def test_missing_new_file_is_not_ignored(self):
        nonexistent = "runtime/not_the_native_v028.py"
        with patch.object(chk, "NEW", chk.NEW + (nonexistent,)):
            issues = chk.check_sources(chk.ROOT)
            self.assertTrue(any(x.startswith("required_new_file_missing:" + nonexistent)
                                for x in issues))

    def test_missing_function_is_blocked_even_when_file_exists(self):
        path = "runtime/kuuos_lean_python_plan_native_binding_v0_28.py"
        original = chk.prior._read

        def absent(root: Path, selected: str):
            if selected == path:
                return b"from __future__ import annotations\n", None
            return original(root, selected)

        with patch.object(chk.prior, "_read", side_effect=absent):
            self.assertIn("native_binding_entrypoint_missing:" + path,
                          chk.check_sources(chk.ROOT))

    def test_invalid_python_syntax_is_blocked(self):
        path = "runtime/kuuos_lean_python_verify_native_binding_v0_28.py"
        original = chk.prior._read

        def invalid(root: Path, selected: str):
            if selected == path:
                return b"def invalid(:\n", None
            return original(root, selected)

        with patch.object(chk.prior, "_read", side_effect=invalid):
            self.assertIn("new_python_syntax_error:" + path,
                          chk.check_sources(chk.ROOT))

    def test_two_test_classes_uniquely_registered(self):
        inventory = chk._test_inventory(chk.ROOT)
        self.assertEqual(set(inventory), set(chk.TEST_CLASSES))
        self.assertTrue(all(len(v) >= 5 for v in inventory.values()))

    def test_untrusted_root_retains_no_data(self):
        self.assertEqual(chk.check_sources(None), ("root:trusted_path_required",))

    def test_static_pins_do_not_assert_refinement_or_authority(self):
        from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
            fail, NO_DATA,
        )
        result = fail("ActOS", "numeric_witness_unavailable")
        self.assertEqual(result.status, NO_DATA)
        self.assertFalse(result.formal_lean_python_refinement_proved)
        self.assertFalse(result.execution_authority_granted)


if __name__ == "__main__":
    unittest.main()
