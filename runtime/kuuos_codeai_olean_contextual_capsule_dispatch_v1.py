"""R41: target-driven dispatch of positive and negative capsule projections.
The request names a proposition and a seven-argument context, not a theorem.
Two certified capsule records are indexed; other goals remain HOLD, not false.
The actual alternate raw atlas has the same shadow but admits a global section.
"""
from __future__ import annotations
import copy
import json
from runtime import kuuos_codeai_olean_contextual_capsule_recall_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
DIRECT="5d832efaa4093f23f61968e2c497bb728f53a85cd91ccf4799f9e52adc763fee"
MCP="1a8cdbf8a66c126693c093e6035a48f1a399fdecf2952cd1db384ac5eb29cb1b"
LAYER="7f4f39621cc4af4e323c0eac777337d882384d695a1ae4ed15ad60b639b09568"
MODULE=prev.MODULE
NS="KuuOSR41Dispatch"
ALT=base.LEC+"nativeF55_twoChart_constant_raw_global"
EQUAL=base.LEC+"nativeF55_twoChart_constant_shadow_equal"

def requests(mem):
    p=mem["request"];q=p["positive_request"];r=p["negative_request"]
    t=p["target"]["apply"]
    def req(case,target,ctx):
        return base.root.make_request("r41_"+case,target,ctx,q["context_modules"])
    a=copy.deepcopy(r["context_args"]);a[6]={"const":base.LEC+"northNativeF55TwoChartConstantRaw"}
    alt=copy.deepcopy(t[2]["apply"][1]);alt["apply"][-1]=a[6]
    return {"shadow":req("shadow",t[1],q["context_args"]),
            "raw":req("raw",t[2]["apply"][1],r["context_args"]),
            "wrong_source":req("wrong_source",t[1],r["context_args"]),
            "alternate":req("alternate",alt,a)}

def observe(qs):
    src="import "+MODULE+"\n\nnamespace KuuOSR41Observe\nset_option autoImplicit false\n"
    for k,q in sorted(qs.items()):
        base.root.validate(q)
        src+="def "+k+"Goal : Prop := "+typed.term(q["target"])+"\n"
        src+="def "+k+"Expected : Prop := "+typed.term(base.cm.prev.context_target(q))+"\n"
        for i,t in enumerate(q["context_args"]):
            src+="noncomputable def "+k+"Ctx"+str(i)+" := "+typed.term(t)+"\n"
    src+="end KuuOSR41Observe\nopen Lean\nrun_cmd do\n  let env ← getEnv\n"
    tick=chr(96)*2
    for k in sorted(qs):
        for x in ["Goal","Expected"]+["Ctx"+str(i) for i in range(7)]:
            n=k+x
            src+="  let some "+n+"Info := env.find? "+tick+"KuuOSR41Observe."+n+' | throwError "missing context expression"\n'
            src+="  let some "+n+"Val := "+n+'Info.value? (allowOpaque := true) | throwError "missing context body"\n'
        src+="  let "+k+"Args : Array String := #["+ ", ".join("reprStr "+k+"Ctx"+str(i)+"Val" for i in range(7))+"]\n"
    src+='  let some p := env.find? '+tick+prev.SHADOW+' | throwError "missing shadow theorem"\n'
    src+='  let some n := env.find? '+tick+prev.RAW+' | throwError "missing raw theorem"\n'
    src+='  let some a := env.find? '+tick+ALT+' | throwError "missing alternate theorem"\n'
    src+='  unless p.type.equal shadowGoalVal && n.type.equal (mkApp (mkConst '+tick+'Not) rawGoalVal) && a.type.equal alternateGoalVal do throwError "canonical target drift"\n'
    rows=[]
    for k in sorted(qs):
        rows.append('('+json.dumps(k)+', Json.mkObj [("goal_expr", toJson (reprStr '+k+'GoalVal)), ("context_exprs", toJson '+k+'Args), ("aligned", toJson ('+k+'GoalVal.equal '+k+'ExpectedVal))])')
    src+='  let payload := Json.mkObj ['+", ".join(rows)+']\n'
    src+='  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R41_CONTEXT " ++ payload.compress)\n'
    return src

def project(d,mp,ind,mem,view,layer,qs,obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R40_DIRECT_CONTEXTUAL_CAPSULE_RECALL" or mp["status"]!="R40_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R40_INDEPENDENT_CONTEXTUAL_CAPSULE_RECALL_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        d["source_head"]!=base.CURRENT or d["source_tree"]!=base.CURRENT_TREE or d["scope_digest"]!=old.SCOPE or
        ind["source_head"]!=base.CURRENT or ind["source_tree"]!=base.CURRENT_TREE or ind["scope_digest"]!=old.SCOPE or
        mem["key"]!=LAYER or base.portable.seal(mem)["key"]!=LAYER or
        d["capsule_layer_key"]!=LAYER or ind["capsule_layer_key"]!=LAYER or
        d["capsule_manifest"]!=prev.MANIFEST or ind["capsule_manifest"]!=prev.MANIFEST or
        ind["capsule_layer_bytes_equal"] is not True or ind["raw_type_and_proof_equal"] is not True or
        ind["imported_certified_capsule"] is not True or ind["parent_bytes_preserved"] is not True or
        ind["mcp_audits"]!=16 or ind["capsule_rebuilds"]!=0 or ind["root_trials"]!=0 or
        any(ind[x]!=3 for x in ("positive_witnesses","negative_witnesses","no_promotion_witnesses"))):
        raise ValueError("R40 admission")
    if prev.recall(mem,mem,view,layer,d["request"],d["observations"],base.CURRENT)!=d["recall"]:
        raise ValueError("R40 capsule provenance")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=16 or len(ma)!=16 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R40 audit binding")
    if qs!=requests(mem):raise ValueError("record request drift")
    records=[]
    for k,role in (("shadow","positive"),("raw","negative")):
        q=qs[k];o=obs[k]
        if not o["aligned"] or o["context_exprs"]!=mem["observations"][role]["context_exprs"]:
            raise ValueError("live context drift")
        routes=[]
        for i,n in enumerate(mem["routes"]):
            w=prev.NS+"."+role+str(i)
            if d["projection_refs"][w]!=[n] or n not in hist[w]["proof_constants"] or not set(hist[w]["axioms"])<=set(hist[n]["axioms"]):
                raise ValueError("projection proof provenance")
            routes.append({"capsule_theorem":n,"projection":role,"historical_witness":w,
                           "historical_witness_digest":old.digest(hist[w])})
        records.append({"request":q,"goal_expr":o["goal_expr"],"context_exprs":o["context_exprs"],
                        "polarity":role,"routes":routes})
    return base.portable.seal({"schema":"kuuos.codeai.contextual-capsule-dispatch-layer.v1",
            "parent_capsule_layer":LAYER,"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,
            "scope_digest":old.SCOPE,"r40_direct_digest":DIRECT,"r40_mcp_digest":MCP,
            "records":records,"semantic_search_complete":False,"proof_authority":False})

def dispatch(index,trusted,q,obs,head):
    def hold(status):return {"status":status,"routes":[],"proof_authority":False}
    if index.get("key")!=base.portable.seal(index)["key"]:return hold("HOLD_DISPATCH_INTEGRITY")
    if index!=trusted:return hold("HOLD_UNADMITTED_DISPATCH")
    if head!=base.CURRENT or index["source_head"]!=head or index["source_tree"]!=base.CURRENT_TREE or index["scope_digest"]!=old.SCOPE:
        return hold("HOLD_DISPATCH_SCOPE")
    base.root.validate(q)
    if not obs["aligned"]:return hold("HOLD_CONTEXT_MISMATCH")
    exact=[r for r in index["records"] if r["goal_expr"]==obs["goal_expr"] and
           r["context_exprs"]==obs["context_exprs"] and all(q[k]==r["request"][k] for k in
           ("target","context_args","context_modules","mode"))]
    if not exact:
        return hold("HOLD_CONTEXT_MISMATCH" if any(r["goal_expr"]==obs["goal_expr"] for r in index["records"]) else "HOLD_CAPSULE_MISS")
    if len(exact)!=1:return hold("HOLD_CONFLICT")
    r=exact[0]
    return {"status":"EXACT_CAPSULE_PROJECTION_REQUIRED","polarity":r["polarity"],"routes":r["routes"],
            "root_trials":0,"proof_authority":False}

def consumer(qs,decisions):
    body="import "+MODULE+"\n\nnamespace "+NS+"\nset_option autoImplicit false\n"
    refs={}
    for k in ("shadow","raw"):
        d=decisions[k]
        if d["status"]!="EXACT_CAPSULE_PROJECTION_REQUIRED":raise ValueError("unadmitted projection")
        t=typed.term(qs[k]["target"])
        if d["polarity"]=="negative":t="Not ("+t+")"
        for i,r in enumerate(d["routes"]):
            w=k+str(i);n=typed.name(r["capsule_theorem"]);part="1" if d["polarity"]=="positive" else "2"
            body+="theorem "+w+" : "+t+" := (@"+n+")."+part+"\n"
            refs[NS+"."+w]=[n]
    # Independent positive control, NOT an answer obtained from a capsule miss.
    body+="theorem alternateControl : "+typed.term(qs["alternate"]["target"])+" := @"+ALT+"\n"
    body+="theorem sameShadowControl : "+base.LEC+"northNativeF55TwoChartConstantShadow = "+base.LEC+"northNativeF55TwoChartShadow := @"+EQUAL+"\n"
    refs[NS+".alternateControl"]=[ALT];refs[NS+".sameShadowControl"]=[EQUAL]
    body+="end "+NS+"\n"
    return body,refs
