"""R45: materialize the independently admitted R44 joint proof as a capsule.
Use its three routes to infer local compatibility, preserving the old HOLD
observation and the original negative context. No new mathematical root.
"""
from __future__ import annotations
import copy
from runtime import kuuos_codeai_olean_contextual_joint_memory_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
DIRECT="69a0d4a8d60f6bcd5afd5a1ded5984843dd8d31faedb753c99252a3ec85cf334"
MCP="5480aa0857d8862b6d82af89dbd6a98fb36a787fb6d917cdfbef2d48e218e46d"
MODULE="KuuOSCodeAIR45JointCapsule"
NS="KuuOSR45Compatibility"
RAW_MARK="KUUOS_R45_RAW "
MARK="KUUOS_R45_TARGETS "
BACK=base.LEC+"global_implies_compatible"
GLUE=base.LEC+"compatible_iff_hasGlobal"
COVER=base.LEC+"nativeF55_twoChart_cover"
def material(d,mp,ind,index,extension,mem,obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R44_DIRECT_CONTEXTUAL_JOINT_MEMORY" or
        mp["status"]!="R44_REAL_MCP_GREEN" or mp["direct_digest"]!=DIRECT or
        ind["status"]!="R44_INDEPENDENT_CONTEXTUAL_JOINT_MEMORY_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        extension["key"]!=prev.LAYER or base.portable.seal(extension)["key"]!=prev.LAYER or
        index["key"]!=prev.prev.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        extension["parent_dispatch_layer"]!=index["key"] or index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["extension_key"]!=extension["key"] or
            x["dispatch_layer_key"]!=index["key"] or x["capsule_layer_key"]!=mem["key"] or
            x["capsule_manifest"]!=dispatch.prev.MANIFEST or x["root_trials"]!=0 or
            x["capsule_rebuilds"]!=0 or x["provider_calls"]!=0 or
            x["joint_witnesses"]!=3 or x["source_separation_witnesses"]!=3 or
            x["exact_kernel_type"] is not True or x["proof_authority"] is not False or
            x["semantic_search_complete"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["raw_type_and_proof_equal"] is not True or
        ind["mcp_audits"]!=23 or ind["unobserved_module_count"]!=695 or
        d["joint_refs"]!=ind["joint_refs"] or d["controls"]!=ind["controls"]):
        raise ValueError("R44 receipt binding")
    qs=d["requests"]
    if obs!=d["observations"]:raise ValueError("R44 live contexts")
    decisions={k:prev.prev.dispatch(index,extension,extension,q,obs[k],base.CURRENT) for k,q in sorted(qs.items())}
    if decisions!=d["decisions"] or prev.plan(qs,obs,decisions,{k:k for k in ("shadow","raw","alternate")})!=d["joint_plan"]:
        raise ValueError("R44 plan provenance")
    if decisions["unknown"]["status"]!="HOLD_UNREGISTERED_TARGET":
        raise ValueError("original HOLD changed")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=23 or len(ma)!=23 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R44 axiom binding")
    names=sorted(n for n in hist if n.startswith((prev.REPLAY+".",prev.NS+".")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    if len(names)!=15 or set(d["joint_refs"])!={prev.NS+"."+k+str(i) for k in ("joint","separate") for i in range(3)} or any(
        not set(rs)<=set(hist[n]["proof_constants"]) or
        not set(hist[n]["axioms"])<={a for r in rs for a in hist[r]["axioms"]}
        for n,rs in d["joint_refs"].items()):
        raise ValueError("R44 proof dependency")
    return d["fresh_application"]["mcp_source"],names,hist

def requests(qs):
    result={}
    for k in ("shadow","raw","alternate"):
        q=qs[k];t=copy.deepcopy(q["target"])
        t["apply"][0]={"const":base.LEC+"Compatible"}
        result[k]=base.root.make_request("r45_"+k,t,q["context_args"],q["context_modules"])
    if any(result["alternate"][k]!=qs["unknown"][k] for k in ("target","context_args","context_modules","mode")):
        raise ValueError("prior HOLD target drift")
    return result

def plan(qs,new,obs):
    expected=requests(qs)
    if new!=expected:raise ValueError("HOLD_COMPATIBILITY_CONTEXT")
    for k,q in new.items():
        base.root.validate(q)
        if (not obs[k]["aligned"] or q["target"]!=base.cm.prev.context_target(q) or
            q["context_args"]!=qs[k]["context_args"]):
            raise ValueError("HOLD_COMPATIBILITY_CONTEXT")
    return {"requests":new,"observations":obs,
            "polarity":{"shadow":"positive","raw":"negative","alternate":"positive"},
            "rule_sources":[BACK,GLUE,COVER],
            "joint_roots":[prev.NS+".joint"+str(i) for i in range(3)],
            "historical_hold":qs["unknown"],"root_trials":0,"proof_authority":False}

def consumer(p):
    qs=p["requests"]
    body="import "+MODULE+"\n\nnamespace "+NS+"\nset_option autoImplicit false\nset_option maxHeartbeats 4000000\n"
    refs={};targets={}
    for k,q in qs.items():
        body+="def "+k+"Target : Prop := "+typed.term(q["target"])+"\n"
    for i,j in enumerate(p["joint_roots"]):
        j=typed.name(j)
        for k,part in (("shadow","1"),("raw","2.1"),("alternate","2.2")):
            q=qs[k];u=typed.term(q["context_args"][4]);s=typed.term(q["context_args"][6]);w=k+str(i)
            if k=="raw":
                body+="theorem "+w+" : Not rawTarget := by\n  intro h\n  exact (@"+j+")."+part+" (("+GLUE+" "+u+" "+s+" "+COVER+").1 h)\n"
                rs=[j,GLUE,COVER]
            else:
                body+="theorem "+w+" : "+k+"Target := "+BACK+" "+u+" "+s+" (@"+j+")."+part+"\n"
                rs=[j,BACK]
            refs[NS+"."+w]=rs;targets[NS+"."+w]=(NS+"."+k+"Target",k=="raw")
    body+="end "+NS+"\n"
    tick=chr(96)*2
    check="open Lean\nrun_cmd do\n  let env ← getEnv\n"
    for k in qs:
        n=NS+"."+k+"Target"
        check+="  let some "+k+"Info := env.find? "+tick+n+' | throwError "missing compatibility target"\n'
        check+="  let some "+k+"Body := "+k+'Info.value? (allowOpaque := true) | throwError "missing compatibility body"\n'
    for i,(n,(t,neg)) in enumerate(sorted(targets.items())):
        x="w"+str(i);exp="mkConst "+tick+t
        if neg:exp="mkApp (mkConst "+tick+"Not) ("+exp+")"
        check+="  let some "+x+" := env.find? "+tick+n+' | throwError "missing compatibility witness"\n'
        check+="  unless "+x+".isTheorem && "+x+".type.equal ("+exp+') do throwError "compatibility type drift"\n'
    check+='  let payload := Json.mkObj ['+", ".join('("'+k+'", toJson (reprStr '+k+'Body))' for k in qs)+']\n'
    check+='  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)\n'
    return body,check,refs
