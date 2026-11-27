"""R46: append and recall R45 compatibility routes without rebuilding capsules.
A memory match admits only a fresh typed application, never authority.
The historical aligned miss is preserved as an observation, not a refutation.
"""
from __future__ import annotations
import copy
from runtime import kuuos_codeai_olean_contextual_joint_capsule_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
parent=prev.prev.prev
DIRECT="c427d64259cff620621d8d367c44ebf69d0a2135cc86a57e1e31f6133093d0ee"
MCP="5fcb91fd9fb87f7842eef54b7bd2ec80b8d40a295f15dab65252fc06a756b11e"
PARENT=prev.prev.LAYER
NS="KuuOSR46Compatibility"
MARK="KUUOS_R46_TARGETS "
MANIFEST={"module":prev.MODULE,"source_sha256":"8bab7934bf64170edfdc93ed3df4e4e3641366db246740684df93559731b13d0",
          "files":[{"name":prev.MODULE+".olean","bytes":20992,"sha256":"7f5ade9ca8d7a2cef76d6420e0f4dc5e9ba6aef2dff1727782526118755c4a74"}]}
def project(d,mp,ind,index,extension,mem,global_qs,global_obs,qs,obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R45_DIRECT_CONTEXTUAL_JOINT_CAPSULE" or mp["status"]!="R45_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R45_INDEPENDENT_CONTEXTUAL_JOINT_CAPSULE_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        extension["key"]!=PARENT or base.portable.seal(extension)["key"]!=PARENT or
        index["key"]!=parent.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        extension["parent_dispatch_layer"]!=index["key"] or index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["extension_key"]!=PARENT or x["dispatch_layer_key"]!=index["key"] or
            x["capsule_layer_key"]!=mem["key"] or x["capsule_manifest"]!=dispatch.prev.MANIFEST or
            x["joint_capsule_manifest"]!=MANIFEST or x["joint_capsule_theorems"]!=15 or
            x["compatibility_witnesses"]!=9 or x["positive_witnesses"]!=6 or x["negative_witnesses"]!=3 or
            x["historical_hold_retained"] is not True or x["exact_kernel_type"] is not True or
            x["root_trials"]!=0 or x["parent_capsule_rebuilds"]!=0 or x["new_capsule_builds"]!=1 or
            x["consumer_proof_body_rebuilds"]!=0 or x["provider_calls"]!=0 or
            x["proof_authority"] is not False or x["semantic_search_complete"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["raw_type_and_proof_equal"] is not True or
        ind["imported_sandbox_joint_capsule"] is not True or ind["mcp_audits"]!=35 or
        ind["unobserved_module_count"]!=695 or d["compatibility_refs"]!=ind["compatibility_refs"] or
        len(d["joint_raw"])!=15):
        raise ValueError("R45 receipt binding")
    p=prev.plan(global_qs,qs,obs)
    if p!=d["compatibility_plan"]:raise ValueError("R45 compatibility plan drift")
    historical=parent.dispatch(index,extension,extension,global_qs["unknown"],global_obs["unknown"],base.CURRENT)
    if historical["status"]!="HOLD_UNREGISTERED_TARGET" or obs["alternate"]!=global_obs["unknown"]:
        raise ValueError("historical HOLD provenance")
    for k in qs:
        if obs[k]["context_exprs"]!=global_obs[k]["context_exprs"]:raise ValueError("context transport drift")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=35 or len(ma)!=35 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R45 axiom binding")
    records=[]
    for k,q in sorted(qs.items()):
        o=obs[k];pol=p["polarity"][k];routes=[]
        for i,j in enumerate(p["joint_roots"]):
            n=prev.NS+"."+k+str(i)
            refs=[j,prev.GLUE,prev.COVER] if pol=="negative" else [j,prev.BACK]
            if (d["compatibility_refs"][n]!=refs or j not in d["joint_raw"] or
                not set(refs)<=set(hist[n]["proof_constants"]) or
                not set(hist[n]["axioms"])<={a for r in refs for a in hist[r]["axioms"]}):
                raise ValueError("derived proof dependency")
            routes.append({"joint_root":j,"projection":{"shadow":"1","raw":"2.1","alternate":"2.2"}[k],
                           "rule_sources":refs[1:],"historical_witness":n,
                           "historical_observation":hist[n],"historical_digest":old.digest(hist[n]),
                           "joint_raw_digest":old.digest(d["joint_raw"][j])})
        records.append({"request":q,"goal_expr":o["goal_expr"],"context_exprs":o["context_exprs"],
                        "polarity":pol,"routes":routes})
    return base.portable.seal({"schema":"kuuos.codeai.contextual-derived-compatibility-layer.v1",
        "source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_extension_key":PARENT,"parent_dispatch_key":index["key"],"r45_direct_digest":DIRECT,
        "r45_mcp_digest":MCP,"joint_capsule_manifest":MANIFEST,"records":records,
        "historical_hold":{"request":global_qs["unknown"],"observation":global_obs["unknown"],
                           "decision":historical,"parent_extension_key":PARENT},
        "semantic_search_complete":False,"proof_authority":False})

def recall(index,extension,layer,trusted,q,obs,head):
    def hold(s):return {"status":s,"routes":[],"proof_authority":False}
    if layer.get("key")!=base.portable.seal(layer)["key"]:return hold("HOLD_DERIVED_INTEGRITY")
    if layer!=trusted:return hold("HOLD_UNADMITTED_DERIVED_LAYER")
    if (head!=base.CURRENT or layer["source_head"]!=head or layer["source_tree"]!=base.CURRENT_TREE or
        layer["scope_digest"]!=old.SCOPE or layer["parent_extension_key"]!=PARENT or
        extension.get("key")!=PARENT or base.portable.seal(extension)["key"]!=PARENT or
        index.get("key")!=parent.PARENT or base.portable.seal(index)["key"]!=parent.PARENT or
        layer["parent_dispatch_key"]!=index["key"]):
        return hold("HOLD_DERIVED_SCOPE")
    base.root.validate(q)
    if not obs["aligned"]:return hold("HOLD_CONTEXT_MISMATCH")
    earlier=parent.dispatch(index,extension,extension,q,obs,head)
    if earlier["status"]!="HOLD_UNREGISTERED_TARGET":return earlier
    matches=[r for r in layer["records"] if r["goal_expr"]==obs["goal_expr"] and
             r["context_exprs"]==obs["context_exprs"] and all(q[k]==r["request"][k] for k in
             ("target","context_args","context_modules","mode"))]
    if len(matches)>1:return hold("HOLD_CONFLICT")
    if not matches:
        return hold("HOLD_CONTEXT_MISMATCH" if any(r["goal_expr"]==obs["goal_expr"] for r in layer["records"])
                    else "HOLD_UNREGISTERED_TARGET")
    r=matches[0]
    return {"status":"EXACT_DERIVED_COMPATIBILITY_REQUIRED","polarity":r["polarity"],
            "routes":r["routes"],"root_trials":0,"proof_authority":False}

def consumer(qs,decisions):
    body="import "+prev.MODULE+"\n\nnamespace "+NS+"\nset_option autoImplicit false\nset_option maxHeartbeats 4000000\n"
    refs={};targets={}
    for k,q in sorted(qs.items()):
        d=decisions[k];base.root.validate(q)
        if d["status"]!="EXACT_DERIVED_COMPATIBILITY_REQUIRED" or len(d["routes"])!=3:
            raise ValueError("unadmitted compatibility request")
        pol=d["polarity"];u=typed.term(q["context_args"][4]);s=typed.term(q["context_args"][6])
        body+="def "+k+"Target : Prop := "+typed.term(q["target"])+"\n"
        for i,r in enumerate(d["routes"]):
            j=typed.name(r["joint_root"]);part=r["projection"];w=k+str(i)
            if pol=="negative" and part=="2.1" and r["rule_sources"]==[prev.GLUE,prev.COVER]:
                body+="theorem "+w+" : Not "+k+"Target := by\n  intro h\n  exact (@"+j+")."+part+" (("+prev.GLUE+" "+u+" "+s+" "+prev.COVER+").1 h)\n"
            elif pol=="positive" and part in ("1","2.2") and r["rule_sources"]==[prev.BACK]:
                body+="theorem "+w+" : "+k+"Target := "+prev.BACK+" "+u+" "+s+" (@"+j+")."+part+"\n"
            else:raise ValueError("unadmitted rule recipe")
            refs[NS+"."+w]=[j]+r["rule_sources"];targets[NS+"."+w]=(NS+"."+k+"Target",pol=="negative")
    body+="end "+NS+"\n"
    # Reuse the certified R45 exact type-observation construction, with fresh names.
    tick=chr(96)*2
    check="open Lean\nrun_cmd do\n  let env ← getEnv\n"
    for k in sorted(qs):
        n=NS+"."+k+"Target"
        check+="  let some "+k+"Info := env.find? "+tick+n+' | throwError "missing recall target"\n'
        check+="  let some "+k+"Body := "+k+'Info.value? (allowOpaque := true) | throwError "missing recall body"\n'
    for i,(n,(t,neg)) in enumerate(sorted(targets.items())):
        x="w"+str(i);exp="mkConst "+tick+t
        if neg:exp="mkApp (mkConst "+tick+"Not) ("+exp+")"
        check+="  let some "+x+" := env.find? "+tick+n+' | throwError "missing recall witness"\n'
        check+="  unless "+x+".isTheorem && "+x+".type.equal ("+exp+') do throwError "recall type drift"\n'
    check+='  let payload := Json.mkObj ['+", ".join('("'+k+'", toJson (reprStr '+k+'Body))' for k in sorted(qs))+']\n'
    check+='  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)\n'
    return body,check,refs
