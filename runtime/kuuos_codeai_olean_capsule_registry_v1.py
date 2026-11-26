"""R24: version-fixed capsule selection. A registry hit is only a candidate.
Admit the artifact externally, read the actual .olean, and check both
applications in Lean. A miss or changed context is HOLD, not refutation.
"""
from __future__ import annotations
import copy
import hashlib
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_root_discovery_v1_r2 as roots
from runtime import kuuos_codeai_olean_shared_specialized_subproof_v1 as sub

def sha(s):return hashlib.sha256(s.encode()).hexdigest()

def entry(d,manifest,provenance,plan):
    if (d["source_head"]!=old.HEAD or d["source_tree"]!=old.TREE or d["scope_digest"]!=old.SCOPE or
        d["capsule_source_sha256"]!=manifest["source_sha256"] or
        d["raw"]["name"]!="KuuOSR23.shared" or d["consumer"]["origin"]!=manifest["module"] or
        d["consumer"]["type_expr"]!=d["raw"]["type_expr"] or d["consumer"]["proof_expr"]!=d["raw"]["proof_expr"] or
        d["consumer"]["wrong_type_defeq"] is not False):
        raise ValueError("capsule provenance")
    x={"source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
       "module":manifest["module"],"name":d["raw"]["name"],
       "type_sha256":sha(d["raw"]["type_expr"]),"proof_sha256":sha(d["raw"]["proof_expr"]),
       "manifest":manifest,"provenance":provenance,"request_digests":plan["request_digests"],
       "shared_tree":plan["shared_tree"],"proof_authority":False}
    return {**x,"key":old.digest(x)}

def lookup(e,request,case,type_sha,scope):
    roots.validate(request)
    payload={k:v for k,v in e.items() if k!="key"}
    if e["key"]!=old.digest(payload):
        return {"status":"HOLD_REGISTRY_INTEGRITY"}
    if scope!=e["scope_digest"] or request["scope_digest"]!=scope:
        return {"status":"HOLD_SCOPE"}
    if request["case_id"]!=case or e["request_digests"].get(case)!=request["request_digest"]:
        return {"status":"HOLD_CONTEXT"}
    if type_sha!=e["type_sha256"]:
        return {"status":"HOLD_TYPE"}
    return {"status":"CAPSULE_CANDIDATE","key":e["key"],"name":e["name"],"module":e["module"],"proof_authority":False}

def application(e,q,route,inv,case):
    if lookup(e,q,case,e["type_sha256"],old.SCOPE)["status"]!="CAPSULE_CANDIDATE":
        raise ValueError("registry request")
    req,src,mcp=roots.application(q,inv,route,"r24_"+case)
    selected={p["name"]:p for ps in inv["selected"].values() for p in ps}
    shared=sub.tree([{"rule":e["shared_tree"][0],"arity":1},
                     {"rule":e["shared_tree"][1][0][0],"arity":0}])
    t=sub.tree(route)
    if sub.nodes(t).count(shared)!=1 or t==shared:
        raise ValueError("shared subtree occurrence")
    replaced=0
    def render(node,indent,depth):
        nonlocal replaced
        if node==shared:
            replaced+=1
            return ["exact @"+typed.name(e["name"])]
        n,children=node
        term=roots.base.bound_term(n,q["context_args"]) if depth==0 or n in roots.base.BOUND_RULES else "@"+n
        lines=["apply "+term]
        for child in children:
            rows=render(child,indent+2,depth+1)
            lines+=[" "*indent+"· "+rows[0]]+rows[1:]
        return lines
    lines=render(t,2,0)
    if replaced!=1:raise ValueError("subtree replacement count")
    start="theorem witness : target := by\n"
    end="\nend "+typed.NS+"."+req["case_id"]
    body="  change "+typed.term(req["target"])+"\n  "+lines[0]+"\n"+"\n".join(lines[1:])
    def transform(s):
        if s.count(start)!=1:raise ValueError("witness boundary")
        pre,tail=s.split(start,1)
        if tail.count(end)!=1:raise ValueError("witness end")
        _,post=tail.split(end,1)
        return pre+start+body+end+post
    return req,transform(src),transform(mcp)
