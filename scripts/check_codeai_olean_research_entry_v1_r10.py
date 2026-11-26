#!/usr/bin/env python3
"""Replay R7/R8/R9 historical evidence through the versioned research entry.
No new Lean propositions or elaboration; R9's actual Lean/MCP audit is reused.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_typed_applicability_v1_r9 as r9
from runtime import kuuos_codeai_olean_research_synthesis_v1 as gate
from runtime import kuuos_codeai_olean_typed_route_preflight_v1 as typed
from runtime.kuuos_codeai_research_structured_edit_synthesis_v0_1 import build_olean_bound_research_synthesis

v=r9.v
load=r9.r5.load
RUN=45779068886
COMMIT="72168e3fc05d33e2de1f3dd99dff93bb67a2b27f"
ARTIFACTS=(
    (15097697171,"codeai-olean-r9-local-45779068886-1","sha256:9e223b54af6511d49e2b646ec0178ebbf4f897ab90144a0c74de4870ab2b99ee"),
    (15098220801,"codeai-olean-r9-independent-45779068886-1","sha256:a4b3c639fd2d6f9e07f15c2f7662042fa303575de976170c1de627ba1bcb0634"),
)
JOBS={
    139769806493:("Verify exact indexed source types and closed target applications",
                  "Actual Lean MCP exact theorem and application audit"),
    139771234144:("Independently reconstruct exact typed applications and project closed target routes",),
}

def admit_r9():
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==COMMIT and run["run_attempt"]==1
           and run["status"]=="completed" and run["conclusion"]=="success","R9 run lineage")
    for jid,names in JOBS.items():
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==name and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for name in names),"R9 job or Lean/MCP step")
    for aid,name,sha in ARTIFACTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==name and a["digest"]==sha and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==COMMIT,
               "R9 artifact lineage")

def observe():
    ref=v.cache.api("git/ref/heads/main")
    v.need(ref["object"]["sha"]==gate.HEAD,"main moved; reobservation required")
    c=v.cache.api("git/commits/"+gate.HEAD)
    v.need(c["tree"]["sha"]==gate.TREE,"canonical tree changed")
    return {"repository":"itakura-hidetoshi/KuuOS","scope":"canonical_main",
            "source_head":gate.HEAD,"source_tree":gate.TREE}

def main():
    p=argparse.ArgumentParser()
    for x in ("index","r8-local","r8-independent","r9-local","r9-independent","out"):
        p.add_argument("--"+x,type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args()
    obs=observe()
    receipt,db=r9.r8.admit(a.index,gate.HEAD)
    old,req=r9.historical_r8(a.r8_local,a.r8_independent,gate.HEAD)
    admit_r9()
    d=load(a.r9_local/"direct.json")
    i=load(a.r9_independent/"direct.json")
    m=load(a.r9_local/"mcp.json")
    ctx=load(a.r9_independent/"routes.json")
    replay=load(a.r9_independent/"independent.json")
    v.need(any(x["name"]==old["name"] and x["type_expr_sha256"]==old["type_expr_sha256"]
               and x["request_digest"]==req["request_digest"] and x["reused_r8"] is True
               for x in d["materialized_sources"]),"R8 full type not reused")
    # An actual production entry symbol is imported above; the sentinel is
    # supplied as an adapter and any attempted generation fails the test.
    class ForbiddenProvider:
        adapter_id="r10-sentinel"
        provider_id="r10-sentinel"
        model_id="r10-sentinel"
        def generate(self, prompt):
            calls.append(prompt)
            raise AssertionError("provider must not be called")
    calls=[]
    base=dict(db=db,index_receipt=receipt,direct=d,independent=i,mcp=m,
              routes=ctx,replay=replay,observation=obs,
              provider_adapters=[ForbiddenProvider()])
    def invoke(key, **changes):
        args=dict(base,target=ctx["routes"][key]["target"],
                  target_request=typed.make_request(ctx,key))
        args.update(changes)
        return build_olean_bound_research_synthesis(**args)
    outputs={k:invoke(k) for k in typed.CASES}
    expected={"forward":"REUSE_EXISTING","reverse":"REFUTED_EXACT_TARGET",
              "reflexive":"REFUTED_EXACT_TARGET"}
    v.need({k:x["status"] for k,x in outputs.items()}==expected,"typed entry route mismatch")
    for x in outputs.values():
        v.need(len(x["search_plan"]["search"]["unobserved_modules"])==695
               and len(x["materialized_sources"])==3
               and x["candidate_generation_allowed"] is False
               and x["proof_authority"] is False and x["provider_calls"]==0,"missing evidence")
    request=typed.make_request(ctx,"reverse")
    controls={
      "missing_premise":invoke("reverse",target_request=dict(request,premise_witnesses=[])),
      "wrong_target":invoke("reverse",target=ctx["routes"]["forward"]["target"]),
      "wrong_scope":invoke("reverse",observation=dict(obs,source_head="0"*40)),
      "wrong_tree":invoke("reverse",observation=dict(obs,source_tree="0"*40)),
      "changed_context":invoke("reverse",routes=dict(ctx,unobserved_module_count=0)),
      "changed_index":invoke("reverse",index_receipt=dict(receipt,raw_type_count=1)),
      "missing_mcp":invoke("reverse",mcp={}),
      "changed_independent":invoke("reverse",independent=dict(i,provider_calls=1)),
      "unknown_id":invoke("reverse",target_request=dict(request,target_id="unknown")),
      "forged_authority":invoke("reverse",target_request=None,terms=["opposite_strict_steps_are_impossible"],
                                candidate_generation_allowed=True,execution_authority=True),
      "no_hit":invoke("reverse",target_request=None,target="unreviewed new goal",
                      terms=["r10zzzznohitzzzz"]),
      "no_terms":invoke("reverse",target_request=None,terms=[]),
    }
    v.need(all(x["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW"
               and x["candidate_generation_allowed"] is False and x["provider_calls"]==0
               for x in controls.values()) and not calls,"unsafe provider boundary")
    miss=controls["no_hit"]["search_plan"]["search"]
    v.need(miss["status"]=="HOLD_NO_DATA" and len(miss["unobserved_modules"])==695
           and miss["omitted_matches"]==0,"no hit lost missing coverage")
    v.need(observe()==obs,"canonical scope changed during replay")
    result={"status":"R10_VERSIONED_RESEARCH_ENTRY_GREEN","source_head":gate.HEAD,
            "source_tree":gate.TREE,"r9_context_digest":gate.R9_CONTEXT,
            "routes":expected,"hold_controls":sorted(controls),
            "route_digests":{k:gate.digest(x) for k,x in outputs.items()},
            "control_digests":{k:gate.digest(x) for k,x in controls.items()},
            "unobserved_modules":695,"provider_calls":len(calls),
            "fresh_lean_or_mcp_executed":False,"historical_lean_and_mcp_reused":True,
            "global_entry_replaced":False,"residual_generation_authorized":False,
            "proof_authority":False,"semantic_search_complete":False}
    a.out.mkdir(parents=True,exist_ok=False)
    v.save(a.out/"receipt.json",result)
    if a.first is not None:
        v.need(result==load(a.first/"receipt.json"),"independent R10 replay differs")
    print("KUUOS_R10_ENTRY",json.dumps(result,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
