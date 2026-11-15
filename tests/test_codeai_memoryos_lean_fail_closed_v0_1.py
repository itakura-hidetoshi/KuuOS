"""Regression: an opt-in CodeAI generator cannot skip Lean verification as success.

Source of truth: original wrapper with generator.main returning zero but never
invoking the pinned direct-Lean/MCP entrypoint. This is a deliberately synthetic
protocol test, not a Lean theorem proof.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import test_codeai_memoryos_lean_adapter_v0_1 as fixture
from scripts import kuuos_codeai_memoryos_lean_v0_1 as adapter


class FailClosedMissingVerificationTests(unittest.TestCase):
    def test_generator_zero_without_lean_cannot_claim_success(self):
        with tempfile.TemporaryDirectory() as dirname:
            root=Path(dirname)
            history=root/'history'
            history.mkdir()
            core,generator,modules,_=fixture.AdapterTests().fixture(root,green=True)
            original_main=core.main
            generator.main=lambda: 0  # Never invokes core.main / direct Lean.
            with patch.dict(sys.modules, modules), patch.dict(
                os.environ, {'GITHUB_RUN_ID':'123'}
            ):
                result=adapter.run(generator.__name__,history,root/'out')
            report=json.loads((root/'out/receipt.json').read_text())
            self.assertNotEqual(result,0,
                'A generator that bypasses the Lean runner must not return success')
            self.assertEqual(report['status'],'VERIFICATION_NOT_RUN')
            self.assertFalse(report['independent_ci_certified'])
            self.assertIs(core.main,original_main)
            self.assertFalse(core.OUT.exists())


if __name__=='__main__':
    unittest.main()
