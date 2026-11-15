"""MemoryOS must never borrow a green real-Lean-MCP receipt from another blob.

This test uses a synthetic adapter protocol, not a kernel certification.
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


class LeanMCPLineageTests(unittest.TestCase):
    def test_mcp_selected_blob_mismatch_cannot_certify_candidate(self):
        with tempfile.TemporaryDirectory() as dirname:
            root=Path(dirname)
            history=root/'history'
            history.mkdir()
            core,generator,modules,_=fixture.AdapterTests().fixture(root,green=True)
            original_raw_main=core.main
            def mismatched_verification_receipt():
                code=original_raw_main()
                path=core.MCP_OUT/'receipt.json'
                data=json.loads(path.read_text())
                data.update({
                    'selected':'fixture',
                    'selected_blob':'f'*40,  # A different source blob.
                    'direct_lean_green':['fixture'],
                })
                path.write_text(json.dumps(data))
                return code
            core.main=mismatched_verification_receipt
            with patch.dict(sys.modules,modules),patch.dict(
                os.environ,{'GITHUB_RUN_ID':'123'}
            ):
                result=adapter.run(generator.__name__,history,root/'out')
            report=json.loads((root/'out/receipt.json').read_text())
            self.assertNotEqual(result,0,
                'Green MCP for another blob cannot verify this Lean candidate')
            self.assertEqual(report['status'],'LOCAL_UNCERTIFIED')
            self.assertFalse(report['independent_ci_certified'])


if __name__=='__main__':
    unittest.main()
