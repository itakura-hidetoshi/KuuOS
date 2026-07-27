#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
from runtime.kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_2 import CONFIRMATION,VERIFIED,build_github_mcp_sub_issue_chain_canary

def main():
 p=argparse.ArgumentParser(description="Run the reversible KuuOS GitHub MCP three-level sub-issue chain canary v1.0 with bounded parent reobservation v1.0.2.")
 p.add_argument("runtime_root",type=Path);p.add_argument("--confirmation",required=True);p.add_argument("--repository",required=True);p.add_argument("--base-sha",required=True);p.add_argument("--transaction-nonce",required=True);p.add_argument("--root-issue-number",type=int,required=True);p.add_argument("--resolved-image-digest",default="");p.add_argument("--execute-external-actions",action="store_true")
 a=p.parse_args();root=a.runtime_root.expanduser().resolve();ap=root/"github_mcp_sub_issue_chain_canary_authority_v1_0.json"
 if not ap.is_file():print(json.dumps({"status":"authority_packet_missing"},sort_keys=True));return 2
 result=build_github_mcp_sub_issue_chain_canary(runtime_context={"runtime_root":str(root),"github_mcp_sub_issue_chain_canary_enabled":True,"apply_github_mcp_sub_issue_chain_canary":True,"execute_external_actions":a.execute_external_actions,"confirmation":a.confirmation,"repository_full_name":a.repository,"base_sha":a.base_sha,"transaction_nonce":a.transaction_nonce,"root_issue_number":a.root_issue_number,"resolved_image_digest":a.resolved_image_digest,"mode":"stdio" if os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN") else "mock"},authority_packet=json.loads(ap.read_text(encoding="utf-8")))
 print(json.dumps(result.to_dict(),ensure_ascii=False,indent=2,sort_keys=True));return 0 if a.confirmation==CONFIRMATION and result.status==VERIFIED else 1
if __name__=="__main__":sys.exit(main())
