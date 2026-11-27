"""R39: retain an admitted R38 composite proof DAG as a portable capsule.
The exact six selected theorem bodies are compiled once in the sandbox.
The independent runner reconstructs, compares full raw Exprs, and imports
the sandbox capsule. A consumer only uses the compiled proof constants.
No new canonical theorem or general proof-search authority is claimed.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_contextual_composite_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
DIRECT="32129c486ecc2a9a0e4445be855ffe4481a22d67e20c01aa5369cf898d78a028"
MCP="c3330ec02baf4de56483f1bb87bf6c5d2c6e5dcf11c896d755b6d7306b02578d"
MODULE="KuuOSCodeAIR39CompositeCapsule"
RAW_MARK="KUUOS_R39_RAW "
NS="KuuOSR39Consumer"
COMPOSITES=tuple(prev.NS+"."+x for x in ("direct","via0","via1"))
def material(d,mp,ind,view,layer):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R38_DIRECT_CONTEXTUAL_COMPOSITE" or mp["status"]!="R38_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R38_INDEPENDENT_CONTEXTUAL_COMPOSITE_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        d["source_head"]!=prev.prev.CURRENT or d["source_tree"]!=prev.prev.CURRENT_TREE or d["scope_digest"]!=old.SCOPE or
        ind["source_head"]!=d["source_head"] or ind["source_tree"]!=d["source_tree"] or ind["scope_digest"]!=old.SCOPE or
        view["key"]!=prev.prev.VIEW or prev.prev.portable.seal(view)["key"]!=view["key"] or
        layer["key"]!=prev.LAYER or prev.prev.portable.seal(layer)["key"]!=layer["key"] or
        d["context_view_key"]!=view["key"] or ind["context_view_key"]!=view["key"] or
        d["route_layer_key"]!=layer["key"] or ind["route_layer_key"]!=layer["key"] or
        ind["parent_bytes_preserved"] is not True or ind["route_layer_bytes_equal"] is not True or
        ind["composite_exact_kernel_type"] is not True or d["composite_exact_kernel_type"] is not True or
        ind["fresh_leaf_applications"]!=10 or ind["composite_witnesses"]!=3 or ind["mcp_audits"]!=31 or
        ind["root_trials"]!=0 or ind["proof_authority"] is not False):
        raise ValueError("R38 admission")
    p=d["composite_plan"]
    k="new_shadow_compat";r="new_original_compat";q=d["requests"]
    recall=prev.memory.recall(layer,layer,view,q[k],d["observations"][k],prev.prev.CURRENT)
    if recall!=d["recall"] or prev.plan(view,layer,q[k],d["observations"][k],recall,q[r],d["observations"][r],d["decisions"][r])!=p:
        raise ValueError("composite plan binding")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=31 or len(ma)!=31 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD or
        prev.prev.portable.hash_type(hist[n]["type_expr_repr"])!=hist[n]["type_expr_sha256"] for n in hist):
        raise ValueError("R38 audit binding")
    refs=d["composite_refs"]
    if refs!=ind["composite_refs"] or set(refs)!=set(COMPOSITES) or refs[COMPOSITES[0]]!=[prev.CANON]:
        raise ValueError("composite inventory")
    positive=[n for n,a in d["applications"].items() if a["case"]==k]
    negative=[n for n,a in d["applications"].items() if a["case"]==r]
    if len(positive)!=2 or len(negative)!=1:raise ValueError("leaf inventory")
    positive.sort()
    for i,n in enumerate(positive):
        if refs[COMPOSITES[i+1]]!=[prev.GLUE,prev.COVER,n,negative[0],prev.BACK]:
            raise ValueError("route DAG drift")
    src=d["fresh_application"]["mcp_source"];blocks=[];imports={prev.MODULE}
    for n in positive+negative:
        a=d["applications"][n];req=a["request"];typed.validate(req)
        if typed.names(req)[1]!=n or a["application"]["exact_kernel_type_match"] is not True or req["polarity"]!=("positive" if n in positive else "negative"):
            raise ValueError("leaf proof binding")
        imports.add(req["module"]);imports.update(q[a["case"]]["context_modules"])
        ns=n.rsplit(".",1)[0];start="namespace "+ns+"\n";end="end "+ns+"\n"
        if src.count(start)!=1 or src.count(end)!=1:raise ValueError("leaf source boundary")
        blocks.append(start+src.split(start,1)[1].split(end,1)[0]+end)
    start="namespace "+prev.NS+"\n";end="end "+prev.NS+"\n"
    if src.count(start)!=1 or src.count(end)!=1:raise ValueError("composite source boundary")
    blocks.append(start+src.split(start,1)[1].split(end,1)[0]+end)
    for m in imports:typed.name(m)
    if any(not m.startswith("Kuu.") for m in imports):raise ValueError("noncanonical capsule dependency")
    names=sorted(positive+negative+list(COMPOSITES))
    source="".join("import "+m+"\n" for m in sorted(imports))+"\n"+"\n".join(blocks)
    return source,names,{n:hist[n] for n in names},p

def consumer(p):
    body="import "+MODULE+"\n\nnamespace "+NS+"\nset_option autoImplicit false\n"
    body+="def target : Prop := "+typed.term(p["target"])+"\n"
    refs={}
    for i,n in enumerate(COMPOSITES):
        label="replay"+str(i)
        body+="theorem "+label+" : target := @"+n+"\n"
        refs[NS+"."+label]=[n]
    body+="end "+NS+"\n"
    tick=chr(96)*2
    check="open Lean\nrun_cmd do\n  let env ← getEnv\n"
    check+="  let some t := env.find? "+tick+NS+'.target | throwError "missing target"\n'
    check+='  let some b := t.value? (allowOpaque := true) | throwError "missing target body"\n'
    check+="  let some c := env.find? "+tick+prev.CANON+' | throwError "missing canonical target"\n'
    check+='  unless b.equal c.type do throwError "target drift"\n'
    for i in range(3):
        name="w"+str(i)
        check+="  let some "+name+" := env.find? "+tick+NS+".replay"+str(i)+' | throwError "missing replay"\n'
        check+="  unless "+name+".isTheorem && "+name+".type.equal (mkConst "+tick+NS+'.target) do throwError "replay type drift"\n'
    check+='  Lean.Elab.Command.liftIO <| IO.println "KUUOS_R39_EXACT_REPLAY"\n'
    return body,check,refs
