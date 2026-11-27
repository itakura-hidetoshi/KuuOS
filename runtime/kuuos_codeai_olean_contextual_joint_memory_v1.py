"""R44: compose admitted R43 routes, derive source separation from opposite
gluing outcomes, and retain the distinct contexts. This is a bounded native
F55 experiment, not a new canonical mathematical result or proof authority.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_contextual_fallback_extension_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.prev.prev
DIRECT="f5ff6e71e3941338d00035d948ddfc27f893922a2eadb3885c52e3c36411df66"
MCP="fdfdfeab7fe45c6884a6bbfc6c231ee6730c5ce00a08bc5c077455d1e9e2631e"
LAYER="8f49df648740cf7324a8ebf3842ad3cbfe802e772d752fd0a0154b39781e83aa"
REPLAY="KuuOSR44Replay"
NS="KuuOSR44Joint"
MARK="KUUOS_R44_EXACT_JOINT"
def admit(d,mp,ind,index,extension,mem,qs,obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R43_DIRECT_CONTEXTUAL_FALLBACK_EXTENSION" or
        mp["status"]!="R43_REAL_MCP_GREEN" or mp["direct_digest"]!=DIRECT or
        ind["status"]!="R43_INDEPENDENT_CONTEXTUAL_FALLBACK_EXTENSION_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        extension["key"]!=LAYER or base.portable.seal(extension)["key"]!=LAYER or
        index["key"]!=prev.PARENT or base.portable.seal(index)["key"]!=prev.PARENT or
        extension["parent_dispatch_layer"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["extension_key"]!=LAYER or
            x["dispatch_layer_key"]!=index["key"] or x["capsule_layer_key"]!=mem["key"] or
            x["capsule_manifest"]!=dispatch.prev.MANIFEST or x["new_contexts"]!=1 or
            x["root_trials"]!=0 or x["capsule_rebuilds"]!=0 or x["provider_calls"]!=0 or
            x["proof_authority"] is not False or x["semantic_search_complete"] is not False
            for x in (d,ind)) or
        ind["extension_bytes_equal"] is not True or ind["parent_bytes_preserved"] is not True or
        ind["raw_type_and_proof_equal"] is not True or ind["mcp_audits"]!=17 or
        ind["shadow_routes"]!=3 or ind["raw_negative_routes"]!=3 or ind["alternate_positive_routes"]!=1 or
        ind["unobserved_module_count"]!=695 or d["requests"]!=qs or d["observations"]!=obs):
        raise ValueError("R43 receipt binding")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=17 or len(ma)!=17 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R43 axiom binding")
    decisions={k:prev.dispatch(index,extension,extension,q,obs[k],base.CURRENT) for k,q in sorted(qs.items())}
    if decisions!=d["decisions"] or {k:x["status"] for k,x in decisions.items()}!=ind["decisions"]:
        raise ValueError("R43 dispatch drift")
    return decisions

def plan(qs,obs,decisions,roles):
    # Compose three exact proposition records, not interchangeable shadows.
    if set(roles)!={"shadow","raw","alternate"} or len(set(roles.values()))!=3:
        raise ValueError("HOLD_COMPOSITE_CONTEXT")
    a,b,c=[qs[roles[k]] for k in ("shadow","raw","alternate")]
    ao,bo,co=[obs[roles[k]] for k in ("shadow","raw","alternate")]
    ad,bd,cd=[decisions[roles[k]] for k in ("shadow","raw","alternate")]
    for q in (a,b,c):base.root.validate(q)
    if (ad["status"]!="EXACT_CAPSULE_PROJECTION_REQUIRED" or ad.get("polarity")!="positive" or
        bd["status"]!="EXACT_CAPSULE_PROJECTION_REQUIRED" or bd.get("polarity")!="negative" or
        cd["status"]!="EXACT_FALLBACK_MEMORY_APPLICATION_REQUIRED" or cd.get("polarity")!="positive"):
        raise ValueError("HOLD_COMPOSITE_POLARITY")
    if any(not o["aligned"] or q["target"]!=base.cm.prev.context_target(q) or
           q["target"]["apply"][0]!={"const":base.LEC+"HasGlobal"}
           for q,o in ((a,ao),(b,bo),(c,co))):
        raise ValueError("HOLD_COMPOSITE_CONTEXT")
    aa,bb,cc=[q["context_args"] for q in (a,b,c)]
    if (any(aa[i]!=bb[i] or ao["context_exprs"][i]!=bo["context_exprs"][i] for i in (0,1,4)) or
        any(bb[i]!=cc[i] or bo["context_exprs"][i]!=co["context_exprs"][i] for i in range(6)) or
        aa[2]!=bb[3] or aa[3]!=bb[3] or aa[6]==bb[6] or bb[6]==cc[6] or
        bo["context_exprs"][6]==co["context_exprs"][6] or bo["goal_expr"]==co["goal_expr"] or
        any(a[k]!=b[k] or b[k]!=c[k] for k in ("context_modules","mode"))):
        raise ValueError("HOLD_COMPOSITE_CONTEXT")
    ar={r["capsule_theorem"]:r for r in ad["routes"]};br={r["capsule_theorem"]:r for r in bd["routes"]}
    if len(ar)!=len(br) or len(ar)!=3 or set(ar)!=set(br) or len(cd["routes"])!=1 or any(
        ar[n]["projection"]!="positive" or br[n]["projection"]!="negative" for n in ar):
        raise ValueError("HOLD_COMPOSITE_ROUTE")
    target={"apply":[{"const":"And"},a["target"],{"apply":[{"const":"And"},
            {"apply":[{"const":"Not"},b["target"]]},c["target"]]}]}
    typed.term(target)
    return {"target":target,"roles":roles,"requests":{k:qs[v] for k,v in roles.items()},
            "observations":{k:obs[v] for k,v in roles.items()},
            "paired_capsule_routes":[{"capsule_theorem":n,"shadow":r,"raw":br[n]}
                for r in ad["routes"] for n in [r["capsule_theorem"]]],
            "alternate_route":cd["routes"][0],"shared_shadow_raw_indices":[0,1,4],
            "shared_raw_alternate_indices":[0,1,2,3,4,5],"distinct_source_index":6,
            "parent_extension_key":LAYER,"root_trials":0,"proof_authority":False,
            "semantic_search_complete":False}

def declarations(p,witness):
    alt=typed.name(witness)
    rq=p["requests"]["raw"];aq=p["requests"]["alternate"]
    raw=typed.term(rq["context_args"][6]);other=typed.term(aq["context_args"][6])
    body="namespace "+NS+"\nset_option autoImplicit false\nset_option maxHeartbeats 4000000\n"
    body+="def jointTarget : Prop := "+typed.term(p["target"])+"\n"
    body+="def separationTarget : Prop := "+other+" ≠ "+raw+"\n"
    refs={};targets={}
    for i,r in enumerate(p["paired_capsule_routes"]):
        s=REPLAY+".shadow"+str(i);n=REPLAY+".raw"+str(i)
        j="joint"+str(i);k="separate"+str(i)
        body+="theorem "+j+" : jointTarget := ⟨@"+s+", ⟨@"+n+", @"+alt+"⟩⟩\n"
        body+="theorem "+k+" : separationTarget := by\n  intro h\n"
        body+="  have ha : "+typed.term(aq["target"])+" := @"+alt+"\n"
        body+="  rw [h] at ha\n  exact @"+n+" ha\n"
        refs[NS+"."+j]=[s,n,alt];refs[NS+"."+k]=[n,alt]
        targets[NS+"."+j]=NS+".jointTarget";targets[NS+"."+k]=NS+".separationTarget"
    body+="end "+NS+"\n"
    tick=chr(96)*2
    check="open Lean\nrun_cmd do\n  let env ← getEnv\n"
    for i,(n,t) in enumerate(sorted(targets.items())):
        x="w"+str(i)
        check+="  let some "+x+" := env.find? "+tick+n+' | throwError "missing joint witness"\n'
        check+="  unless "+x+".isTheorem && "+x+".type.equal (mkConst "+tick+t+') do throwError "joint witness type drift"\n'
    check+='  Lean.Elab.Command.liftIO <| IO.println "'+MARK+'"\n'
    return body,check,refs
