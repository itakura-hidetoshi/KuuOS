from __future__ import annotations
import unittest
from typing import Any,Mapping
from scripts.check_kuuos_github_mcp_sub_issue_chain_canary_v1_0 import *
from runtime.kuuos_github_mcp_sub_issue_chain_canary_v1_0 import BLOCKED,COMPENSATED,VERIFIED

class PreexistingRoot(MockTransport):
 def __init__(self):super().__init__();self.children[ROOT]=[{"id":1,"number":99,"title":"existing"}]
class WrongGrandParent(MockTransport):
 def call_tool(self,name:str,arguments:Mapping[str,Any]):
  if name=="issue_read" and arguments.get("method")=="get_parent" and arguments.get("issue_number")==GRAND and self.parents.get(GRAND) is not None:return response({"parent":{"number":ROOT,"title":REQUEST_TITLE,"state":"OPEN","url":f"https://github.com/itakura-hidetoshi/KuuOS/issues/{ROOT}","repository":"itakura-hidetoshi/KuuOS"}})
  return super().call_tool(name,arguments)
class ResidualParent(MockTransport):
 def call_tool(self,name:str,arguments:Mapping[str,Any]):
  if name=="sub_issue_write" and arguments.get("method")=="remove" and arguments.get("sub_issue_id")==GRAND_ID:return response({"status":"removed"})
  return super().call_tool(name,arguments)
class WrongAnnotation(MockTransport):
 def list_tools(self):
  value=super().list_tools();value["result"]["tools"][1]["annotations"]["readOnlyHint"]=False;return value
class ChainTests(unittest.TestCase):
 def test_complete_chain(self):
  r=run_case();self.assertEqual(r.status,VERIFIED);self.assertFalse(r.compensation_attempted)
 def test_preexisting_root_blocks_before_creation(self):
  t=PreexistingRoot();r=run_case(t);self.assertEqual(r.status,BLOCKED);self.assertFalse(t.issues)
 def test_wrong_grand_parent_compensates(self):
  r=run_case(WrongGrandParent());self.assertEqual(r.status,COMPENSATED);self.assertTrue(r.compensation_cleanup_verified)
 def test_residual_parent_never_verifies(self):
  r=run_case(ResidualParent());self.assertNotEqual(r.status,VERIFIED);self.assertTrue({"parent_not_absent","sub_issues_not_empty"}&set(r.blockers))
 def test_read_tool_must_be_read_only(self):
  r=run_case(WrongAnnotation());self.assertEqual(r.status,BLOCKED);self.assertIn("issue_read_not_classified_read_only",r.blockers)
 def test_unpinned_image_blocks(self):
  r=run_case(mutate=lambda p:p["server"].update({"image":"ghcr.io/github/github-mcp-server:latest"}));self.assertEqual(r.status,BLOCKED);self.assertIn("official_server_image_not_pinned",r.blockers)
 def test_bad_nonce_blocks(self):
  r=run_case(mutate=lambda p:p.update({"transaction_nonce":"bad"}));self.assertEqual(r.status,BLOCKED);self.assertIn("transaction_nonce_invalid",r.blockers)
if __name__=="__main__":unittest.main()
