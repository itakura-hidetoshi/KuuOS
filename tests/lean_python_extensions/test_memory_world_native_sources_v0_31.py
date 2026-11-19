"""v0.31 exact original MemoryOS/WORLD Lean and native source proof pins.

Source pins and theorem names alone do not make a machine-checked
new proof, universal Python refinement, or issuer authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import unittest

from scripts import check_kuuos_lean_python_memory_world_native_sources_v0_31 as checker


class NativeMemoryWorldNativeSourceTests(unittest.TestCase):
    def test_exact_twelve_original_memory_world_codeai_pins(self):
        self.assertEqual(len(checker.PINNED), 12)
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_original_prior_codeai_proof_pins_still_match(self):
        self.assertEqual(checker.prior.check_sources(checker.ROOT), ())

    def test_all_pinned_lean_python_blob_identities_match(self):
        for path, expected in checker.PINNED.items():
            with self.subTest(path=path):
                source, problem = checker.prior._read(checker.ROOT, path)
                self.assertIsNone(problem)
                self.assertEqual(checker.prior._blob(source), expected)

    def test_two_source_bound_entrypoints_in_separate_os_modules(self):
        self.assertEqual(len(checker.ENTRYPOINTS), 2)
        self.assertEqual(set(checker.inventory()), set(checker.TEST_CLASSES))
        self.assertEqual(checker.check_sources(), ())

    def test_original_memory_kernel_byte_drift_is_detected(self):
        path = "runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("original_pin_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_original_world_lean_theorem_drift_is_detected(self):
        path = "formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean"
        with patch.dict(checker.PINNED, {path: "0" * 40}):
            self.assertIn("original_pin_changed:" + path,
                          checker.check_sources(checker.ROOT))

    def test_missing_world_entrypoint_blocks_source_check(self):
        path = "runtime/kuuos_lean_python_world_native_binding_v0_31.py"
        prior = checker.prior._read

        def fake(root: Path, name: str):
            if name == path:
                return b"from __future__ import annotations\n", None
            return prior(root, name)

        with patch.object(checker.prior, "_read", side_effect=fake):
            self.assertIn("native_entrypoint_missing:" + path,
                          checker.check_sources(checker.ROOT))

    def test_untrusted_root_is_no_data(self):
        self.assertEqual(checker.check_sources(None),
                         ("root:trusted_path_required",))

    def test_old_world_true_flags_do_not_mean_new_host_authority(self):
        from runtime.kuuos_lean_python_memory_world_native_v0_31 import (
            NativeMemoryWorldAudit, PASS,
        )
        result = NativeMemoryWorldAudit(os_name="WORLD", status=PASS)
        for key in ("external_source_issuer_authenticated",
                    "nested_lean_proof_structures_constructed",
                    "new_world_commit_performed",
                    "complete_lean_python_semantic_refinement",
                    "execution_authority_granted",
                    "git_authority_granted"):
            self.assertFalse(getattr(result, key))


if __name__ == "__main__":
    unittest.main()
