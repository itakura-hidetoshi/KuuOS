"""R38: bounded context-aware composition of remembered positive routes and
a certified negative premise on the genuine native F55 two-chart atlas.
A composite request names propositions, not a theorem or authority.
Only the explicitly checked native atlas pair is admitted in this pilot.
The existing canonical conjunction is a type/control witness, not a new theorem.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_contextual_route_memory_v1 as memory
from runtime import kuuos_codeai_olean_contextual_premise_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
DIRECT="13d577db1af93340fa71b7b92c6c6e0c3455a1cc6532471d69928756f5b65180"
MCP="320f56acc9c2dac20e214c05f731c4653d692619d0b69f7a825d40516b562a47"
LAYER="f380a15fc7e0b31623a9b1a263adf04531fd2a08858a258c0174240e78f4433b"
NS="KuuOSR38Composite"
MODULE=prev.LEC+"NativeF55CechSourceGluingObstruction"
CANON=prev.LEC+"nativeF55_twoChart_shadow_glues_not_raw"
COVER=prev.LEC+"nativeF55_twoChart_cover"
GLUE=prev.LEC+"compatible_iff_hasGlobal"
BACK=prev.LEC+"global_implies_compatible"
RAW=prev.LEC+"nativeF55_twoChart_raw_incompatible"
def plan(view,layer,q,obs,recall,rawq,rawobs,rawdecision):
    c=prev.cm.prev.c;ap=prev.cm.prev.ap
    prev.root.validate(q);prev.root.validate(rawq)
    if (layer["key"]!=LAYER or layer["parent_view_key"]!=view["key"] or
        memory.recall(layer,layer,view,q,obs,prev.CURRENT)!=recall or
        recall["status"]!="EXACT_CONTEXT_ROUTE_APPLICATION_REQUIRED"):
        raise ValueError("unadmitted positive route layer")
    a=q["context_args"];b=rawq["context_args"]
    if (q["target"]!=prev.cm.prev.context_target(q) or rawq["target"]!=prev.cm.prev.context_target(rawq) or
        q["target"]["apply"][0]!=c(prev.LEC+"Compatible") or rawq["target"]["apply"][0]!=c(prev.LEC+"Compatible") or
        not obs["target_aligned"] or not rawobs["target_aligned"] or
        obs["goal_expr"]!=obs["context_goal_expr"] or rawobs["goal_expr"]!=rawobs["context_goal_expr"] or
        any(a[i]!=b[i] or obs["context_exprs"][i]!=rawobs["context_exprs"][i] for i in (0,1,4)) or
        a[4]!=c(prev.LEC+"northNativeF55TwoChartCover") or a[6]!=c(prev.LEC+"northNativeF55TwoChartShadow") or
        b[6]!=c(prev.LEC+"northNativeF55TwoChartRaw") or b[5]!=c(prev.LEC+"northNativeF55Observe") or
        a[2]!=b[3] or a[3]!=b[3] or a[6]==b[6] or q["context_modules"]!=rawq["context_modules"] or q["mode"]!=rawq["mode"]):
        raise ValueError("HOLD_COMPOSITE_CONTEXT")
    if rawdecision["status"]!="EXACT_CONTEXT_APPLICATION_REQUIRED":
        raise ValueError("HOLD_COMPOSITE_NEGATIVE_PREMISE")
    rk=rawdecision["context_key"];rec=view["records"][rk]
    if (rk not in rawobs["context_matches"] or rec["target_expr"]!=rawobs["goal_expr"] or
        rec["context_args"]!=b or rec["request"]["context_modules"]!=rawq["context_modules"] or
        rec["request"]["mode"]!=rawq["mode"] or rawdecision["matches"]!=[m["candidate"] for m in rec["matches"]] or
        [(x["name"],x["polarity"]) for x in rawdecision["matches"]]!=[(RAW,"negative")]):
        raise ValueError("HOLD_COMPOSITE_NEGATIVE_PREMISE")
    positive=ap(prev.LEC+"HasGlobal",a[0],a[1],a[2],a[4],a[6])
    negative=ap(prev.LEC+"HasGlobal",b[0],b[1],b[2],b[4],b[6])
    target=ap("And",positive,ap("Not",negative))
    typed.term(target)
    return {"target":target,"positive_context_key":layer["context_key"],"negative_context_key":rk,
            "positive_request":q,"negative_request":rawq,"positive_routes":recall["routes"],
            "negative_candidates":rawdecision["matches"],"shared_context_indices":[0,1,4],
            "route_layer_key":LAYER,"parent_view_key":view["key"],
            "root_trials":0,"semantic_search_complete":False,"proof_authority":False}

def declarations(p,positive_witnesses,negative_witness):
    if len(positive_witnesses)!=2 or len(set(positive_witnesses))!=2:
        raise ValueError("two distinct route witnesses required")
    a=p["positive_request"]["context_args"];b=p["negative_request"]["context_args"]
    u=typed.term(a[4]);s=typed.term(a[6]);r=typed.term(b[6])
    neg=typed.name(negative_witness)
    body="namespace "+NS+"\nset_option autoImplicit false\nset_option maxHeartbeats 4000000\n"
    body+="def target : Prop := "+typed.term(p["target"])+"\n"
    body+="theorem direct : target := @"+CANON+"\n"
    refs={NS+".direct":[CANON]}
    for i,n in enumerate(positive_witnesses):
        n=typed.name(n);label="via"+str(i)
        body+="theorem "+label+" : target := by\n"
        body+="  exact ⟨("+GLUE+" "+u+" "+s+" "+COVER+").1 (@"+n+"), "
        body+="fun h => (@"+neg+") ("+BACK+" "+u+" "+r+" h)⟩\n"
        refs[NS+"."+label]=[GLUE,COVER,n,neg,BACK]
    body+="end "+NS+"\n"
    tick=chr(96)*2
    check="open Lean\nrun_cmd do\n  let env ← getEnv\n"
    check+="  let some t := env.find? "+tick+NS+'.target | throwError "missing composite target"\n'
    check+='  let some b := t.value? (allowOpaque := true) | throwError "missing composite target body"\n'
    check+="  let some c := env.find? "+tick+CANON+' | throwError "missing canonical comparison"\n'
    check+='  unless b.equal c.type do throwError "composite target drift"\n'
    for label in ("direct","via0","via1"):
        check+="  let some w_"+label+" := env.find? "+tick+NS+"."+label+' | throwError "missing composite witness"\n'
        check+="  unless w_"+label+".isTheorem && w_"+label+".type.equal (mkConst "+tick+NS+'.target) do throwError "composite witness type drift"\n'
    check+='  Lean.Elab.Command.liftIO <| IO.println "KUUOS_R38_COMPOSITE_EXACT"\n'
    return body,check,refs
