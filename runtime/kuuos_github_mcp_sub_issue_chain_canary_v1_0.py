#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,html,json,os,re,time
from pathlib import Path
from typing import Any,Mapping,Protocol

PLAN_VERSION="kuuos_github_mcp_sub_issue_chain_canary_plan_v1_0"
REQUEST_VERSION="kuuos_github_mcp_sub_issue_chain_canary_request_v1_0"
CHILD_VERSION="kuuos_github_mcp_sub_issue_chain_canary_child_v1_0"
GRANDCHILD_VERSION="kuuos_github_mcp_sub_issue_chain_canary_grandchild_v1_0"
AUTHORITY_READY="KUUOS_GITHUB_MCP_SUB_ISSUE_CHAIN_CANARY_AUTHORITY_READY"
CONFIRMATION="RUN_KUUOS_GITHUB_MCP_SUB_ISSUE_CHAIN_CANARY"
VERIFIED="KUUOS_GITHUB_MCP_SUB_ISSUE_CHAIN_CANARY_VERIFIED"
COMPENSATED="KUUOS_GITHUB_MCP_SUB_ISSUE_CHAIN_CANARY_COMPENSATED"
BLOCKED="KUUOS_GITHUB_MCP_SUB_ISSUE_CHAIN_CANARY_BLOCKED"
REQUEST_TITLE="[KuuOS MCP Sub-Issue Chain Canary v1.0]"
CHILD_TITLE_PREFIX="[KuuOS MCP Sub-Issue Chain Child v1.0] "
GRANDCHILD_TITLE_PREFIX="[KuuOS MCP Sub-Issue Chain Grandchild v1.0] "
NONCE=re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{7,31}")
SHA=re.compile(r"[0-9a-fA-F]{40}")
IMAGE=re.compile(r"ghcr\.io/github/github-mcp-server@sha256:[0-9a-fA-F]{64}")

class MCPTransport(Protocol):
 def list_tools(self)->dict[str,Any]:...
 def call_tool(self,name:str,arguments:Mapping[str,Any])->dict[str,Any]:...
 def close(self)->None:...

@dataclass(frozen=True)
class GitHubMCPSubIssueChainCanaryResult:
 version:str;status:str;packet_id:str;repository_full_name:str;base_branch:str;base_sha:str
 server_image:str;resolved_image_digest:str;transaction_nonce:str;root_issue_number:int
 child_issue_number:int;child_issue_id:int;grandchild_issue_number:int;grandchild_issue_id:int
 root_identity_verified:bool;root_preflight_empty:bool;child_created_verified:bool
 grandchild_created_verified:bool;child_parent_preflight_absent:bool
 grandchild_parent_preflight_absent:bool;root_child_added_verified:bool
 child_root_parent_verified:bool;child_grandchild_added_verified:bool
 grandchild_child_parent_verified:bool;child_grandchild_removed_verified:bool
 grandchild_parent_removed_verified:bool;root_child_removed_verified:bool
 child_parent_removed_verified:bool;grandchild_closed_verified:bool;child_closed_verified:bool
 compensation_attempted:bool;compensation_cleanup_verified:bool
 records:list[dict[str,Any]];blockers:list[str];warnings:list[str]
 def to_dict(self):return asdict(self)

def m(v):return dict(v) if isinstance(v,Mapping) else {}
def h(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
def norm(r):
 if "error" in r or m(r.get("result")).get("isError") is True:return {}
 c=m(r.get("result")).get("content")
 if not isinstance(c,list):return m(r.get("result"))
 s="\n".join(str(x.get("text","")) for x in c if isinstance(x,Mapping) and x.get("type")=="text")
 try:return json.loads(s)
 except json.JSONDecodeError:return s
def call(t,phase,tool,args):
 try:r=t.call_tool(tool,args)
 except Exception as e:return {"error":f"{type(e).__name__}:{e}"},{},[phase+"_tool_exception"]
 return dict(r),norm(r),([phase+"_tool_returned_error"] if "error" in r or m(r.get("result")).get("isError") is True else [])
def rec(phase,tool,args,r,o,status,b):
 x={"phase":phase,"tool":tool,"arguments_digest":h(args),"response":r,"observed":o,"observed_digest":h(o),"status":status,"blockers":sorted(set(b)),"epoch":int(time.time())};x["record_digest"]=h(x);return x
def strict(v):return json.loads(html.unescape(str(v)))
def issuechk(o,n,title,body,state):
 x=m(o);b=[]
 if int(x.get("number",0) or 0)!=n:b+=["issue_number_mismatch"]
 if x.get("title")!=title:b+=["issue_title_mismatch"]
 if str(x.get("state","")).lower()!=state:b+=[f"issue_state_not_{state}"]
 try:p=strict(x.get("body",""))
 except Exception:return b+["issue_body_not_strict_json"]
 if p!=body:b+=["issue_body_mismatch"]
 return b
def subchk(o,n=None,title=None):
 if not isinstance(o,list):return ["sub_issues_not_list"]
 if n is None:return [] if not o else ["sub_issues_not_empty"]
 if len(o)!=1:return ["sub_issue_count_not_one"]
 x=m(o[0]);b=[]
 if int(x.get("number",0) or 0)!=n:b+=["sub_issue_number_mismatch"]
 if x.get("title")!=title:b+=["sub_issue_title_mismatch"]
 return b
def parentchk(o,n=None,title=None,repo=""):
 p=m(o).get("parent")
 if n is None:return [] if p is None else ["parent_not_absent"]
 x=m(p);b=[]
 if int(x.get("number",0) or 0)!=n:b+=["parent_number_mismatch"]
 if x.get("title")!=title:b+=["parent_title_mismatch"]
 if str(x.get("state","")).upper()!="OPEN":b+=["parent_state_not_open"]
 if x.get("repository")!=repo:b+=["parent_repository_mismatch"]
 if x.get("url")!=f"https://github.com/{repo}/issues/{n}":b+=["parent_url_mismatch"]
 return b
def created(o):
 x=m(o);b=[]
 try:i=int(str(x.get("id","0")))
 except:i=0
 try:n=int(str(x.get("url","")).rstrip("/").rsplit("/",1)[-1])
 except:n=0
 if i<=0:b+=["created_issue_id_invalid"]
 if n<=0:b+=["created_issue_number_invalid"]
 return i,n,b
def nodebody(v,root,sha,nonce):return {"version":v,"root_issue_number":root,"base_sha":sha,"transaction_nonce":nonce}
def open_stdio(server,plan):
 from runtime.kuuos_github_mcp_server_bridge_v0_1 import OfficialGitHubMCPStdioClient,_stdio_command
 c,e=_stdio_command(server,plan);return OfficialGitHubMCPStdioClient(c,e)

def build_github_mcp_sub_issue_chain_canary(*,runtime_context,authority_packet,transport=None):
 ctx,auth=m(runtime_context),m(authority_packet);root=Path(str(ctx.get("runtime_root","."))).resolve()
 pp=root/"github_mcp_sub_issue_chain_canary_plan_v1_0.json";rp=root/"github_mcp_sub_issue_chain_canary_receipt_v1_0.json";ap=root/"github_mcp_sub_issue_chain_canary_audit_v1_0.jsonl"
 b=[];w=[];records=[]
 try:plan=json.loads(pp.read_text())
 except Exception as e:plan={};b+=[f"plan_read_failed:{type(e).__name__}"]
 repo=str(plan.get("repository_full_name",""));owner,name=(repo.split("/",1)+[""])[:2];sha=str(plan.get("base_sha",""));nonce=str(plan.get("transaction_nonce",""));rootn=int(plan.get("root_issue_number",0) or 0);server=m(plan.get("server"));image=str(server.get("image",""));digest=str(ctx.get("resolved_image_digest",""))
 tests=[(plan.get("version")==PLAN_VERSION,"plan_version_invalid"),(plan.get("base_branch")=="main","base_branch_not_main"),(SHA.fullmatch(sha) is not None,"base_sha_invalid"),(plan.get("write_capable") is True and plan.get("read_only") is False,"write_profile_invalid"),(plan.get("lockdown_mode") is True and plan.get("execute_external_actions") is True,"execution_boundary_invalid"),(plan.get("confirmation")==CONFIRMATION,"plan_confirmation_invalid"),(NONCE.fullmatch(nonce) is not None,"transaction_nonce_invalid"),(rootn>0,"root_issue_number_invalid"),(plan.get("request_issue_title")==REQUEST_TITLE and plan.get("request_version_marker")==REQUEST_VERSION,"request_contract_invalid"),(server.get("kind")=="official_github_mcp_server","server_kind_invalid"),(IMAGE.fullmatch(image) is not None,"official_server_image_not_pinned"),(set(server.get("toolsets",[]))=={"issues"},"toolsets_invalid"),(set(server.get("tools",[]))=={"issue_write","issue_read","sub_issue_write"},"tool_allowlist_invalid"),(ctx.get("github_mcp_sub_issue_chain_canary_enabled") is True,"chain_canary_enabled_not_true"),(ctx.get("apply_github_mcp_sub_issue_chain_canary") is True,"apply_chain_canary_not_true"),(ctx.get("execute_external_actions") is True,"runtime_execute_external_actions_not_true"),(ctx.get("confirmation")==CONFIRMATION,"runtime_confirmation_invalid"),(ctx.get("repository_full_name",repo)==repo,"runtime_repository_mismatch"),(ctx.get("base_sha",sha)==sha,"runtime_base_sha_mismatch"),(ctx.get("transaction_nonce",nonce)==nonce,"runtime_nonce_mismatch"),(int(ctx.get("root_issue_number",rootn) or 0)==rootn,"runtime_root_issue_mismatch"),(auth.get("authority_status")==AUTHORITY_READY,"authority_not_ready")]
 b += [e for ok,e in tests if not ok]
 for f in ("plan_read_allowed","tool_discovery_allowed","external_action_allowed","mcp_write_tool_call_allowed","post_write_reobservation_allowed","upward_parent_reobservation_allowed","compensating_chain_remove_allowed","compensating_issue_close_allowed","receipt_write_allowed","audit_append_allowed"):
  if auth.get(f) is not True:b+=[f.replace("_allowed","_not_allowed")]
 if str(plan.get("mode",ctx.get("mode","mock")))=="stdio" and not digest.startswith("sha256:"):b+=["resolved_image_digest_missing"]
 flags={k:False for k in ("root_identity_verified","root_preflight_empty","child_created_verified","grandchild_created_verified","child_parent_preflight_absent","grandchild_parent_preflight_absent","root_child_added_verified","child_root_parent_verified","child_grandchild_added_verified","grandchild_child_parent_verified","child_grandchild_removed_verified","grandchild_parent_removed_verified","root_child_removed_verified","child_parent_removed_verified","grandchild_closed_verified","child_closed_verified")}
 ci=cn=gi=gn=0;comp=False;cleanup=False;t=transport;owns=False
 if not b and t is None:
  if not os.environ.get(str(server.get("token_env","GITHUB_PERSONAL_ACCESS_TOKEN"))):b+=["github_personal_access_token_missing"]
  else:
   try:t=open_stdio(server,plan);owns=True
   except Exception as e:b+=[f"stdio_transport_build_failed:{type(e).__name__}"]
 if not b and t:
  try:
   tm={x["name"]:x for x in m(t.list_tools().get("result")).get("tools",[])}
   for q in ("issue_write","issue_read","sub_issue_write"):
    if q not in tm:b+=[f"required_tool_not_discovered:{q}"]
   if m(tm.get("issue_read",{}).get("annotations")).get("readOnlyHint") is not True:b+=["issue_read_not_classified_read_only"]
   for q in ("issue_write","sub_issue_write"):
    if m(tm.get(q,{}).get("annotations")).get("readOnlyHint") is True:b+=[f"{q}_not_classified_write"]
  except Exception as e:b+=[f"tool_discovery_failed:{type(e).__name__}"]
 def obs(key,phase,args,chk):
  nonlocal b
  r,o,l=call(t,phase,"issue_read",args)
  if not l:l+=chk(o)
  records.append(rec(phase,"issue_read",args,r,o,"verified" if not l else "blocked",l));b+=l;flags[key]=not l
 def mut(phase,tool,args):
  nonlocal b
  r,o,l=call(t,phase,tool,args);records.append(rec(phase,tool,args,r,o,"applied" if not l else "blocked",l));b+=l;return o
 rg={"method":"get","owner":owner,"repo":name,"issue_number":rootn};rc={"method":"get_sub_issues","owner":owner,"repo":name,"issue_number":rootn,"perPage":100,"page":1}
 ctitle=CHILD_TITLE_PREFIX+nonce;gtitle=GRANDCHILD_TITLE_PREFIX+nonce;cb=nodebody(CHILD_VERSION,rootn,sha,nonce);gb=nodebody(GRANDCHILD_VERSION,rootn,sha,nonce)
 if not b and t:
  expected={"version":REQUEST_VERSION,"confirmation":CONFIRMATION,"expected_main_sha":sha,"transaction_nonce":nonce,"server_image":image}
  obs("root_identity_verified","verify_root_issue",rg,lambda o:issuechk(o,rootn,REQUEST_TITLE,expected,"open"))
 if flags["root_identity_verified"] and not b:obs("root_preflight_empty","preflight_root_sub_issues",rc,lambda o:subchk(o))
 if flags["root_preflight_empty"] and not b:
  o=mut("create_child_issue","issue_write",{"method":"create","owner":owner,"repo":name,"title":ctitle,"body":json.dumps(cb,sort_keys=True)});ci,cn,l=created(o);b+=l
 cg={"method":"get","owner":owner,"repo":name,"issue_number":cn};cp={"method":"get_parent","owner":owner,"repo":name,"issue_number":cn};cc={"method":"get_sub_issues","owner":owner,"repo":name,"issue_number":cn,"perPage":100,"page":1}
 if cn and not b:obs("child_created_verified","verify_child_created",cg,lambda o:issuechk(o,cn,ctitle,cb,"open"))
 if flags["child_created_verified"] and not b:obs("child_parent_preflight_absent","preflight_child_parent",cp,lambda o:parentchk(o,repo=repo))
 if flags["child_parent_preflight_absent"] and not b:
  o=mut("create_grandchild_issue","issue_write",{"method":"create","owner":owner,"repo":name,"title":gtitle,"body":json.dumps(gb,sort_keys=True)});gi,gn,l=created(o);b+=l
 gg={"method":"get","owner":owner,"repo":name,"issue_number":gn};gp={"method":"get_parent","owner":owner,"repo":name,"issue_number":gn}
 if gn and not b:obs("grandchild_created_verified","verify_grandchild_created",gg,lambda o:issuechk(o,gn,gtitle,gb,"open"))
 if flags["grandchild_created_verified"] and not b:obs("grandchild_parent_preflight_absent","preflight_grandchild_parent",gp,lambda o:parentchk(o,repo=repo))
 if flags["grandchild_parent_preflight_absent"] and not b:mut("add_root_child_binding","sub_issue_write",{"method":"add","owner":owner,"repo":name,"issue_number":rootn,"sub_issue_id":ci})
 if not b:obs("root_child_added_verified","verify_root_child_added",rc,lambda o:subchk(o,cn,ctitle))
 if flags["root_child_added_verified"] and not b:obs("child_root_parent_verified","verify_child_root_parent",cp,lambda o:parentchk(o,rootn,REQUEST_TITLE,repo))
 if flags["child_root_parent_verified"] and not b:mut("add_child_grandchild_binding","sub_issue_write",{"method":"add","owner":owner,"repo":name,"issue_number":cn,"sub_issue_id":gi})
 if not b:obs("child_grandchild_added_verified","verify_child_grandchild_added",cc,lambda o:subchk(o,gn,gtitle))
 if flags["child_grandchild_added_verified"] and not b:obs("grandchild_child_parent_verified","verify_grandchild_child_parent",gp,lambda o:parentchk(o,cn,ctitle,repo))
 if flags["grandchild_child_parent_verified"] and not b:mut("remove_child_grandchild_binding","sub_issue_write",{"method":"remove","owner":owner,"repo":name,"issue_number":cn,"sub_issue_id":gi})
 if not b:obs("child_grandchild_removed_verified","verify_child_grandchild_removed",cc,lambda o:subchk(o))
 if flags["child_grandchild_removed_verified"] and not b:obs("grandchild_parent_removed_verified","verify_grandchild_parent_removed",gp,lambda o:parentchk(o,repo=repo))
 if flags["grandchild_parent_removed_verified"] and not b:mut("remove_root_child_binding","sub_issue_write",{"method":"remove","owner":owner,"repo":name,"issue_number":rootn,"sub_issue_id":ci})
 if not b:obs("root_child_removed_verified","verify_root_child_removed",rc,lambda o:subchk(o))
 if flags["root_child_removed_verified"] and not b:obs("child_parent_removed_verified","verify_child_parent_removed",cp,lambda o:parentchk(o,repo=repo))
 if flags["child_parent_removed_verified"] and not b:mut("close_grandchild_issue","issue_write",{"method":"update","owner":owner,"repo":name,"issue_number":gn,"state":"closed","state_reason":"completed"})
 if not b:obs("grandchild_closed_verified","verify_grandchild_closed",gg,lambda o:issuechk(o,gn,gtitle,gb,"closed"))
 if flags["grandchild_closed_verified"] and not b:mut("close_child_issue","issue_write",{"method":"update","owner":owner,"repo":name,"issue_number":cn,"state":"closed","state_reason":"completed"})
 if not b:obs("child_closed_verified","verify_child_closed",cg,lambda o:issuechk(o,cn,ctitle,cb,"closed"))
 primary=all(flags.values()) and not b
 if not primary and t and (cn or gn):
  comp=True
  for phase,pid,nid in (("compensate_remove_grandchild",cn,gi),("compensate_remove_child",rootn,ci)):
   if pid and nid:mut(phase,"sub_issue_write",{"method":"remove","owner":owner,"repo":name,"issue_number":pid,"sub_issue_id":nid})
  for phase,n in (("compensate_close_grandchild",gn),("compensate_close_child",cn)):
   if n:mut(phase,"issue_write",{"method":"update","owner":owner,"repo":name,"issue_number":n,"state":"closed","state_reason":"not_planned"})
  checks=[]
  if cn:
   _,o,l=call(t,"compensate_verify_child_parent","issue_read",cp);checks+=[not l and not parentchk(o,repo=repo)]
  if gn:
   _,o,l=call(t,"compensate_verify_grandchild_parent","issue_read",gp);checks+=[not l and not parentchk(o,repo=repo)]
  cleanup=bool(checks) and all(checks)
 if owns and t:
  try:t.close()
  except Exception as e:w+=[f"transport_close_failed:{type(e).__name__}"]
 status=VERIFIED if primary else (COMPENSATED if comp and cleanup else BLOCKED)
 result=GitHubMCPSubIssueChainCanaryResult(version=PLAN_VERSION,status=status,packet_id="kuuos-github-mcp-sub-issue-chain-"+h([repo,sha,nonce,rootn])[:16],repository_full_name=repo,base_branch=str(plan.get("base_branch","")),base_sha=sha,server_image=image,resolved_image_digest=digest,transaction_nonce=nonce,root_issue_number=rootn,child_issue_number=cn,child_issue_id=ci,grandchild_issue_number=gn,grandchild_issue_id=gi,compensation_attempted=comp,compensation_cleanup_verified=cleanup,records=records,blockers=sorted(set(b)),warnings=sorted(set(w)),**flags)
 if auth.get("receipt_write_allowed") is True:rp.write_text(json.dumps(result.to_dict(),ensure_ascii=False,indent=2,sort_keys=True)+"\n")
 if auth.get("audit_append_allowed") is True:ap.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in records))
 return result
