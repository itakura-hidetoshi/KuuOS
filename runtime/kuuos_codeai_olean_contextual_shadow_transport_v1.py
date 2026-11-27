"""R47: equality-licensed shadow transport and local-to-global composition.
A distinct presentation remains distinct in memory; only a checked equality
of the actual shadow atlases permits transporting the selected proposition.
No raw transport, overwrite, or external action authority is inferred.
"""
from __future__ import annotations
import copy
from runtime import kuuos_codeai_olean_contextual_derived_compatibility_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
DIRECT="e42a2eb74c81d6d4885e4d6ba42f19cbe43360ac0a97a521d32548bb680068a6"
MCP="2ecefb8438ae08350b29c32e46f204c967264854c942630b916f6035a0cd6aea"
LAYER="ad2dc7da544cbcf84de9d4d21c3fd60ac43d7c52e34f8754405a6f5dc451ebd3"
MANIFEST=prev.MANIFEST
EQUAL=dispatch.EQUAL
GLUE=prev.prev.GLUE
COVER=prev.prev.COVER
NS="KuuOSR47ShadowTransport"
MARK="KUUOS_R47_TARGETS "
SHADOW=base.LEC+"northNativeF55TwoChartShadow"
ALTERNATE=base.LEC+"northNativeF55TwoChartConstantShadow"
def admit(d,mp,ind,index,extension,layer,mem,qs,obs,global_qs,global_obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R46_DIRECT_CONTEXTUAL_DERIVED_COMPATIBILITY" or
        mp["status"]!="R46_REAL_MCP_GREEN" or mp["direct_digest"]!=DIRECT or
        ind["status"]!="R46_INDEPENDENT_CONTEXTUAL_DERIVED_COMPATIBILITY_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        layer["key"]!=LAYER or base.portable.seal(layer)["key"]!=LAYER or
        extension["key"]!=prev.PARENT or base.portable.seal(extension)["key"]!=prev.PARENT or
        index["key"]!=prev.parent.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        layer["parent_extension_key"]!=extension["key"] or layer["parent_dispatch_key"]!=index["key"] or
        index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["derived_layer_key"]!=LAYER or
            x["extension_key"]!=extension["key"] or x["dispatch_layer_key"]!=index["key"] or
            x["capsule_layer_key"]!=mem["key"] or x["capsule_manifest"]!=dispatch.prev.MANIFEST or
            x["joint_capsule_manifest"]!=MANIFEST or x["new_contexts"]!=3 or x["recalled_routes"]!=9 or
            x["positive_witnesses"]!=6 or x["negative_witnesses"]!=3 or
            x["historical_hold_retained"] is not True or x["prior_hold_recalled"] is not True or
            x["exact_kernel_type"] is not True or x["root_trials"]!=0 or x["capsule_rebuilds"]!=0 or
            x["consumer_proof_body_rebuilds"]!=0 or x["provider_calls"]!=0 or
            x["proof_authority"] is not False or x["semantic_search_complete"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["raw_type_and_proof_equal"] is not True or
        ind["derived_layer_bytes_equal"] is not True or ind["mcp_audits"]!=35 or
        ind["unobserved_module_count"]!=695 or d["controls"]!=ind["controls"] or
        d["requests"]!=qs or d["observations"]!=obs):
        raise ValueError("R46 receipt binding")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=35 or len(ma)!=35 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R46 audit binding")
    def recall(q,o):return prev.recall(index,extension,layer,layer,q,o,base.CURRENT)
    ds={k:recall(q,obs[k]) for k,q in sorted(qs.items())}
    earlier={k:recall(q,global_obs[k]) for k,q in sorted(global_qs.items()) if k!="unknown"}
    if ds!=d["decisions"] or earlier!=d["earlier_decisions"] or recall(global_qs["unknown"],global_obs["unknown"])!=ds["alternate"]:
        raise ValueError("R46 recall drift")
    return ds,hist

def requests(q):
    base.root.validate(q)
    if q["context_args"][6]!={"const":SHADOW} or q["target"]["apply"][0]!={"const":base.LEC+"Compatible"}:
        raise ValueError("HOLD_SHADOW_TRANSPORT_SOURCE")
    ctx=copy.deepcopy(q["context_args"]);ctx[6]={"const":ALTERNATE}
    t=copy.deepcopy(q["target"]);t["apply"][-1]=ctx[6]
    compat=base.root.make_request("r47_const_shadow_compat",t,ctx,q["context_modules"])
    g=copy.deepcopy(t);g["apply"][0]={"const":base.LEC+"HasGlobal"}
    glob=base.root.make_request("r47_const_shadow_global",g,ctx,q["context_modules"])
    return {"compat":compat,"global":glob}

def plan(index,extension,layer,q,o,targets,observations):
    expected=requests(q)
    if targets!=expected or not o["aligned"] or q["target"]!=base.cm.prev.context_target(q):
        raise ValueError("HOLD_SHADOW_TRANSPORT_CONTEXT")
    ds=prev.recall(index,extension,layer,layer,q,o,base.CURRENT)
    if ds["status"]!="EXACT_DERIVED_COMPATIBILITY_REQUIRED" or ds["polarity"]!="positive" or len(ds["routes"])!=3:
        raise ValueError("HOLD_SHADOW_TRANSPORT_PREMISE")
    for k,t in targets.items():
        ob=observations[k]
        if (not ob["aligned"] or t["target"]!=base.cm.prev.context_target(t) or
            any(t["context_args"][i]!=q["context_args"][i] or ob["context_exprs"][i]!=o["context_exprs"][i] for i in range(6)) or
            ob["context_exprs"][6]==o["context_exprs"][6] or ob["goal_expr"]==o["goal_expr"]):
            raise ValueError("HOLD_SHADOW_TRANSPORT_CONTEXT")
        if prev.recall(index,extension,layer,layer,t,ob,base.CURRENT)["status"]!="HOLD_UNREGISTERED_TARGET":
            raise ValueError("HOLD_SHADOW_TRANSPORT_ALREADY_REGISTERED")
    return {"source_request":q,"source_observation":o,"source_routes":ds["routes"],
            "targets":targets,"observations":observations,"equality_source":EQUAL,
            "rule_sources":[GLUE,COVER],"shared_context_indices":list(range(6)),
            "changed_context_index":6,"parent_derived_layer":LAYER,
            "root_trials":0,"proof_authority":False,"semantic_search_complete":False}

def consumer(p):
    cq=p["targets"]["compat"];gq=p["targets"]["global"]
    u=typed.term(cq["context_args"][4]);s=typed.term(cq["context_args"][6])
    body="namespace "+NS+"\nset_option autoImplicit false\nset_option maxHeartbeats 4000000\n"
    body+="def compatTarget : Prop := "+typed.term(cq["target"])+"\n"
    body+="def globalTarget : Prop := "+typed.term(gq["target"])+"\n"
    body+="def equalityTarget : Prop := (@"+ALTERNATE+") = (@"+SHADOW+")\n"
    refs={};targets={}
    for i,r in enumerate(p["source_routes"]):
        leaf=prev.NS+".shadow"+str(i)
        if r["projection"]!="1" or r["rule_sources"]!=[prev.prev.BACK]:
            raise ValueError("HOLD_SHADOW_TRANSPORT_RECIPE")
        c="compatible"+str(i);g="global"+str(i)
        body+="theorem "+c+" : compatTarget := by\n  change "+typed.term(cq["target"])+"\n"
        body+="  rw ["+EQUAL+"]\n  exact @"+leaf+"\n"
        body+="theorem "+g+" : globalTarget := ("+GLUE+" "+u+" "+s+" "+COVER+").1 (@"+NS+"."+c+")\n"
        refs[NS+"."+c]=[EQUAL,leaf];refs[NS+"."+g]=[GLUE,COVER,NS+"."+c]
        targets[NS+"."+c]=NS+".compatTarget";targets[NS+"."+g]=NS+".globalTarget"
    body+="end "+NS+"\n"
    tick=chr(96)*2
    check="open Lean\nrun_cmd do\n  let env ← getEnv\n"
    for k in ("compat","global","equality"):
        check+="  let some "+k+"Info := env.find? "+tick+NS+"."+k+'Target | throwError "missing transport target"\n'
        check+="  let some "+k+"Body := "+k+'Info.value? (allowOpaque := true) | throwError "missing transport body"\n'
    check+="  let some eqProof := env.find? "+tick+EQUAL+' | throwError "missing equality source"\n'
    check+='  unless eqProof.isTheorem && eqProof.type.equal equalityBody do throwError "transport equality type drift"\n'
    for i,(n,t) in enumerate(sorted(targets.items())):
        x="w"+str(i)
        check+="  let some "+x+" := env.find? "+tick+n+' | throwError "missing transport witness"\n'
        check+="  unless "+x+".isTheorem && "+x+".type.equal (mkConst "+tick+t+') do throwError "transport witness type drift"\n'
    check+='  let payload := Json.mkObj [("compat",toJson (reprStr compatBody)),("global",toJson (reprStr globalBody))]\n'
    check+='  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)\n'
    return body,check,refs
