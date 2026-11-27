"""R40: context-bound, import-only recall of an independently admitted capsule.
Retain both original contexts and every composite proof route. A context hit
is a candidate for new kernel checks, not execution or promotion authority.
The concrete native F55 no-promotion consequence already exists in main.
"""
from __future__ import annotations
import copy
import json
from runtime import kuuos_codeai_olean_contextual_composite_capsule_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.prev.prev
DIRECT="003fc5c88ab59a474f14d8c1a186b35c9db3165aa9c066d2b422c731946562ec"
MCP="f139e110470c60c1a0b443015bc31f85feaef3af2ca7f4c1ea94f7c0dacd3224"
MODULE=prev.MODULE
NS="KuuOSR40Recall"
SHADOW=base.LEC+"nativeF55_twoChart_shadow_global"
RAW=base.LEC+"nativeF55_twoChart_raw_no_global"
DENY=base.LEC+"nativeF55_twoChart_raw_global_not_admissible"
SOUND=base.LEC+"admitted_sound"
MANIFEST={"module":MODULE,"source_sha256":"069c5063aa095a2a5531d0c56585bc1a0c38d6b83d3b397441c6e600234cf544",
          "files":[{"name":MODULE+".olean","bytes":13592,"sha256":"5fd80af83f69a2dd58bff8dde58ba553e5c2aeade9a4296d9bdf1edd2cb1fcae"}]}
def project(d,mp,ind,prior,view,layer):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or old.digest(prior)!=prev.DIRECT or
        d["status"]!="R39_DIRECT_COMPOSITE_CAPSULE" or mp["status"]!="R39_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R39_INDEPENDENT_COMPOSITE_CAPSULE_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        d["r38_direct_digest"]!=prev.DIRECT or d["r38_mcp_digest"]!=prev.MCP or
        d["source_head"]!=base.CURRENT or d["source_tree"]!=base.CURRENT_TREE or d["scope_digest"]!=old.SCOPE or
        ind["source_head"]!=d["source_head"] or ind["source_tree"]!=d["source_tree"] or ind["scope_digest"]!=old.SCOPE or
        view["key"]!=base.VIEW or base.portable.seal(view)["key"]!=view["key"] or
        layer["key"]!=prev.prev.LAYER or base.portable.seal(layer)["key"]!=layer["key"] or
        d["context_view_key"]!=view["key"] or ind["context_view_key"]!=view["key"] or
        d["route_layer_key"]!=layer["key"] or ind["route_layer_key"]!=layer["key"] or
        d["capsule_manifest"]!=MANIFEST or ind["capsule_manifest"]!=MANIFEST or
        ind["raw_type_and_proof_equal"] is not True or ind["imported_sandbox_capsule"] is not True or
        ind["parent_bytes_preserved"] is not True or ind["capsule_theorems"]!=6 or ind["replay_witnesses"]!=3 or
        ind["mcp_audits"]!=9 or ind["root_trials"]!=0 or ind["consumer_proof_body_rebuilds"]!=0 or
        ind["proof_authority"] is not False):
        raise ValueError("R39 admission")
    p=d["composite_plan"]
    if p!=prior["composite_plan"] or d["composite_refs"]!=prior["composite_refs"]:
        raise ValueError("composite plan drift")
    q=p["positive_request"];r=p["negative_request"]
    a=prior["observations"]["new_shadow_compat"];b=prior["observations"]["new_original_compat"]
    recall=prev.prev.memory.recall(layer,layer,view,q,a,base.CURRENT)
    if prev.prev.plan(view,layer,q,a,recall,r,b,prior["decisions"]["new_original_compat"])!=p:
        raise ValueError("context pair provenance")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    raw=d["raw"]
    if (len(hist)!=9 or len(ma)!=9 or set(hist)!=set(ma) or len(raw)!=6 or
        set(hist)!=set(raw)|set(d["replay_refs"]) or not set(prev.COMPOSITES)<=set(raw) or
        any(hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist) or
        any(raw[n]["type_expr"]!=hist[n]["type_expr_repr"] or
            base.portable.hash_type(raw[n]["type_expr"])!=hist[n]["type_expr_sha256"] for n in raw)):
        raise ValueError("capsule proof audit")
    request={"target":p["target"],"positive_request":q,"negative_request":r}
    return base.portable.seal({"schema":"kuuos.codeai.contextual-composite-capsule-layer.v1",
        "parent_view_key":view["key"],"parent_route_key":layer["key"],"source_head":base.CURRENT,
        "source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,"lean":base.portable.LEAN,"mathlib":base.portable.MATHLIB,
        "r39_direct_digest":DIRECT,"r39_mcp_digest":MCP,"manifest":MANIFEST,
        "request":request,"observations":{"positive":{"goal_expr":a["goal_expr"],"context_exprs":a["context_exprs"]},
                                           "negative":{"goal_expr":b["goal_expr"],"context_exprs":b["context_exprs"]}},
        "context_keys":[p["positive_context_key"],p["negative_context_key"]],
        "shared_context_indices":p["shared_context_indices"],"routes":list(prev.COMPOSITES),
        "composite_refs":d["composite_refs"],"source_observations":{n:hist[n] for n in sorted(raw)},
        "raw_digests":{n:old.digest(raw[n]) for n in sorted(raw)},
        "semantic_search_complete":False,"proof_authority":False})

def recall(memory,trusted,view,layer,request,observations,head):
    def hold(s):return {"status":s,"routes":[]}
    if memory.get("key")!=base.portable.seal(memory)["key"]:return hold("HOLD_CAPSULE_LAYER_INTEGRITY")
    if memory!=trusted:return hold("HOLD_UNADMITTED_CAPSULE_LAYER")
    if (head!=base.CURRENT or memory["source_head"]!=head or memory["source_tree"]!=base.CURRENT_TREE or
        memory["scope_digest"]!=old.SCOPE or memory["parent_view_key"]!=view["key"] or
        memory["parent_route_key"]!=layer["key"] or view["key"]!=base.VIEW or layer["key"]!=prev.prev.LAYER or
        base.portable.seal(view)["key"]!=view["key"] or base.portable.seal(layer)["key"]!=layer["key"]):
        return hold("HOLD_CAPSULE_SCOPE")
    if request!=memory["request"] or observations!=memory["observations"]:
        return hold("HOLD_CAPSULE_CONTEXT_MISMATCH")
    return {"status":"EXACT_COMPOSITE_CAPSULE_APPLICATION_REQUIRED","routes":memory["routes"],
            "capsule_layer_key":memory["key"],"root_trials":0,"proof_authority":False}

def observe(request):
    src="import "+MODULE+"\n\nnamespace KuuOSR40Observe\nset_option autoImplicit false\n"
    for key in ("positive","negative"):
        q=request[key+"_request"];base.root.validate(q)
        src+="def "+key+"Goal : Prop := "+typed.term(q["target"])+"\n"
        for i,t in enumerate(q["context_args"]):
            src+="noncomputable def "+key+"Ctx"+str(i)+" := "+typed.term(t)+"\n"
    src+="end KuuOSR40Observe\nopen Lean\nrun_cmd do\n  let env ← getEnv\n"
    tick=chr(96)*2
    for key in ("positive","negative"):
        src+="  let some "+key+"Info := env.find? "+tick+"KuuOSR40Observe."+key+'Goal | throwError "missing context goal"\n'
        src+="  let some "+key+"Goal := "+key+'Info.value? (allowOpaque := true) | throwError "missing goal body"\n'
        src+="  let mut "+key+"Args : Array String := #[]\n"
        for i in range(7):
            n=key+"Arg"+str(i)
            src+="  let some "+n+" := env.find? "+tick+"KuuOSR40Observe."+key+"Ctx"+str(i)+' | throwError "missing context arg"\n'
            src+="  let some "+n+"Val := "+n+'.value? (allowOpaque := true) | throwError "missing context body"\n'
            src+="  "+key+"Args := "+key+"Args.push (reprStr "+n+"Val)\n"
    src+='  let payload := Json.mkObj [("positive", Json.mkObj [("goal_expr", toJson (reprStr positiveGoal)), ("context_exprs", toJson positiveArgs)]),\n'
    src+='    ("negative", Json.mkObj [("goal_expr", toJson (reprStr negativeGoal)), ("context_exprs", toJson negativeArgs)])]\n'
    src+='  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R40_CONTEXT " ++ payload.compress)\n'
    return src

def consumer(request,routes):
    if routes!=list(prev.COMPOSITES):raise ValueError("capsule route inventory")
    t=request["target"]["apply"];neg=t[2]["apply"][1]
    if t[0]!={"const":"And"} or t[2]["apply"][0]!={"const":"Not"}:raise ValueError("composite shape")
    body="import "+MODULE+"\n\nnamespace "+NS+"\nset_option autoImplicit false\n"
    body+="def positiveTarget : Prop := "+typed.term(t[1])+"\n"
    body+="def negativeTarget : Prop := "+typed.term(t[2])+"\n"
    body+="def deniedTarget : Prop := ∀ ev : "+base.LEC+"PromotionEvidence ("+typed.term(neg)+"), ¬ "+base.LEC+"Admissible ev\n"
    refs={};targets={}
    for i,n in enumerate(routes):
        for label,target,proof in (("positive","positiveTarget","(@"+n+").1"),
                                   ("negative","negativeTarget","(@"+n+").2"),
                                   ("denied","deniedTarget","by\n  intro ev he\n  exact (@"+n+").2 ("+SOUND+" ev he)")):
            w=label+str(i)
            body+="theorem "+w+" : "+target+" := "+proof+"\n"
            refs[NS+"."+w]=[n]+([SOUND] if label=="denied" else [])
            targets[NS+"."+w]=NS+"."+target
    body+="end "+NS+"\n"
    tick=chr(96)*2
    check="open Lean\nrun_cmd do\n  let env ← getEnv\n"
    for label,canon in (("positive",SHADOW),("negative",RAW),("denied",DENY)):
        check+="  let some "+label+"Info := env.find? "+tick+NS+"."+label+'Target | throwError "missing projection target"\n'
        check+="  let some "+label+"Body := "+label+'Info.value? (allowOpaque := true) | throwError "missing projection body"\n'
        check+="  let some "+label+"Canon := env.find? "+tick+canon+' | throwError "missing canonical comparison"\n'
        check+="  unless "+label+"Body.equal "+label+'Canon.type do throwError "projection target drift"\n'
    for i,(n,t) in enumerate(sorted(targets.items())):
        x="w"+str(i)
        check+="  let some "+x+" := env.find? "+tick+n+' | throwError "missing projection witness"\n'
        check+="  unless "+x+".isTheorem && "+x+".type.equal (mkConst "+tick+t+') do throwError "projection witness type drift"\n'
    check+='  Lean.Elab.Command.liftIO <| IO.println "KUUOS_R40_EXACT_PROJECTIONS"\n'
    return body,check,refs
