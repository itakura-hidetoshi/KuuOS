#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import tempfile
from typing import Any,Mapping
from runtime.kuuos_github_mcp_sub_issue_chain_canary_v1_0 import *
BASE_SHA="8102cfc7c5de1cf7801ab987e83f97f678d71856";NONCE="chain-v10-check-001";ROOT=2001;CHILD=2002;GRAND=2003;CHILD_ID=92002;GRAND_ID=92003
IMAGE="ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"
def response(payload:Any,error:bool=False):
 text=payload if isinstance(payload,str) else json.dumps(payload);return {"jsonrpc":"2.0","id":1,"result":{"isError":error,"content":[{"type":"text","text":text}]}}
class MockTransport:
 def __init__(self):self.issues={};self.children={ROOT:[],CHILD:[]};self.parents={CHILD:None,GRAND:None}
 def list_tools(self):return {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"issue_write","annotations":{"readOnlyHint":False}},{"name":"issue_read","annotations":{"readOnlyHint":True}},{"name":"sub_issue_write","annotations":{"readOnlyHint":False}}]}}
 def root(self):return {"number":ROOT,"title":REQUEST_TITLE,"state":"open","body":json.dumps({"version":REQUEST_VERSION,"confirmation":CONFIRMATION,"expected_main_sha":BASE_SHA,"transaction_nonce":NONCE,"server_image":IMAGE})}
 def call_tool(self,name:str,arguments:Mapping[str,Any]):
  a=dict(arguments);method=a.get("method")
  if name=="issue_read" and method=="get":return response(self.root() if a["issue_number"]==ROOT else self.issues[a["issue_number"]])
  if name=="issue_read" and method=="get_sub_issues":return response(self.children.get(a["issue_number"],[]))
  if name=="issue_read" and method=="get_parent":
   n=a["issue_number"];pn=self.parents.get(n)
   if pn is None:return response({"parent":None})
   parent=self.root() if pn==ROOT else self.issues[pn]
   return response({"parent":{"number":pn,"title":parent["title"],"state":"OPEN","url":f"https://github.com/itakura-hidetoshi/KuuOS/issues/{pn}","repository":"itakura-hidetoshi/KuuOS"}})
  if name=="issue_write" and method=="create":
   n=CHILD if CHILD not in self.issues else GRAND;db=CHILD_ID if n==CHILD else GRAND_ID;self.issues[n]={"number":n,"title":a["title"],"state":"open","body":a["body"]};return response({"id":str(db),"url":f"https://github.com/itakura-hidetoshi/KuuOS/issues/{n}"})
  if name=="issue_write" and method=="update":self.issues[a["issue_number"]]["state"]="closed";return response({"ok":True})
  if name=="sub_issue_write" and method=="add":
   parent=a["issue_number"];node=CHILD if a["sub_issue_id"]==CHILD_ID else GRAND;self.parents[node]=parent;issue=self.issues[node];self.children.setdefault(parent,[])[:]=[{"id":a["sub_issue_id"],"number":node,"title":issue["title"],"state":"open"}];return response({"status":"added"})
  if name=="sub_issue_write" and method=="remove":
   parent=a["issue_number"];node=CHILD if a["sub_issue_id"]==CHILD_ID else GRAND;self.parents[node]=None;self.children.setdefault(parent,[])[:]=[];return response({"status":"removed"})
  return response("unexpected",True)
 def close(self):pass
def plan():return {"version":PLAN_VERSION,"mode":"mock","repository_full_name":"itakura-hidetoshi/KuuOS","base_branch":"main","base_sha":BASE_SHA,"write_capable":True,"read_only":False,"lockdown_mode":True,"execute_external_actions":True,"confirmation":CONFIRMATION,"transaction_nonce":NONCE,"root_issue_number":ROOT,"request_issue_title":REQUEST_TITLE,"request_version_marker":REQUEST_VERSION,"server":{"kind":"official_github_mcp_server","launcher":"docker","image":IMAGE,"token_env":"GITHUB_PERSONAL_ACCESS_TOKEN","toolsets":["issues"],"tools":["issue_write","issue_read","sub_issue_write"]}}
def authority():return {"authority_status":AUTHORITY_READY,"plan_read_allowed":True,"tool_discovery_allowed":True,"external_action_allowed":True,"mcp_write_tool_call_allowed":True,"post_write_reobservation_allowed":True,"upward_parent_reobservation_allowed":True,"compensating_chain_remove_allowed":True,"compensating_issue_close_allowed":True,"receipt_write_allowed":True,"audit_append_allowed":True}
def run_case(t=None,mutate=None):
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);pl=plan();mutate and mutate(pl);(root/"github_mcp_sub_issue_chain_canary_plan_v1_0.json").write_text(json.dumps(pl));(root/"github_mcp_sub_issue_chain_canary_authority_v1_0.json").write_text(json.dumps(authority()));return build_github_mcp_sub_issue_chain_canary(runtime_context={"runtime_root":str(root),"github_mcp_sub_issue_chain_canary_enabled":True,"apply_github_mcp_sub_issue_chain_canary":True,"execute_external_actions":True,"confirmation":CONFIRMATION,"repository_full_name":"itakura-hidetoshi/KuuOS","base_sha":BASE_SHA,"transaction_nonce":NONCE,"root_issue_number":ROOT,"mode":"mock"},authority_packet=authority(),transport=t or MockTransport())
def main():
 r=run_case();assert r.status==VERIFIED,r.to_dict();assert r.child_root_parent_verified and r.grandchild_child_parent_verified;assert r.child_parent_removed_verified and r.grandchild_parent_removed_verified;assert r.child_closed_verified and r.grandchild_closed_verified;assert not r.compensation_attempted;print(json.dumps(r.to_dict(),ensure_ascii=False,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
