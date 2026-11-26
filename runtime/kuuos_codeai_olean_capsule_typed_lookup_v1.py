"""R25: fresh closed target requests, typed capsule/No-Go lookup.
A registry key or structural ranking is never proof. Exact Lean type
comparison is followed by a new kernel-checked application and independent
audit. R24's historical request-bound registry remains unchanged.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime import kuuos_codeai_olean_general_application_v1 as typed

MARK="KUUOS_R25_TYPE_LOOKUP "

def request(case,target):
    if not isinstance(case,str) or not typed.CASE.fullmatch(case):
        raise ValueError("fresh case identity")
    typed.term(target)
    q={"schema":"kuuos.codeai.closed-proof-lookup.v1","case_id":case,
       "target":target,"source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"mode":"CLOSED_TARGET"}
    return {**q,"request_digest":old.digest(q)}

def validate(q):
    if q!=request(q["case_id"],q["target"]):
        raise ValueError("fresh request binding changed")

def inventory(e,neg):
    # The host must admit R24/R23 evidence before constructing this inventory.
    if e["key"]!=old.digest({k:v for k,v in e.items() if k!="key"}):
        raise ValueError("registry integrity")
    if (e["source_head"]!=old.HEAD or e["source_tree"]!=old.TREE or e["scope_digest"]!=old.SCOPE or
        e["lean"]!="v4.30.0-rc2" or e["mathlib"]!="5450b53e5ddc75d46418fabb605edbf36bd0beb6"):
        raise ValueError("registry scope")
    nq=neg["request"];typed.validate(nq)
    if (nq["polarity"]!="negative" or nq["arguments"]!=[] or
        neg["application"]["exact_kernel_type_match"] is not True or
        neg["target_expr_repr"]!=neg["application"]["target_expr_repr"] or
        nq["source"] not in neg["source_refs"]):
        raise ValueError("negative witness lineage")
    p={"module":typed.name(e["module"]),"name":typed.name(e["name"]),"polarity":"positive",
       "registry_key":e["key"]}
    n={"module":typed.name(nq["module"]),"name":typed.name(nq["source"]),"polarity":"negative",
       "prior_evidence_digest":old.digest(neg)}
    x={"source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "candidates":[p,n],"semantic_search_complete":False,"proof_authority":False}
    return {**x,"key":old.digest(x)}

def preflight(inv,q,scope):
    validate(q)
    if inv["key"]!=old.digest({k:v for k,v in inv.items() if k!="key"}):
        return "HOLD_INVENTORY_INTEGRITY"
    if scope!=old.SCOPE or inv["scope_digest"]!=scope or q["scope_digest"]!=scope:
        return "HOLD_SCOPE"
    if inv["source_head"]!=old.HEAD or inv["source_tree"]!=old.TREE:
        return "HOLD_SOURCE"
    return "TYPE_COMPARISON_REQUIRED"

def render(inv,qs):
    if len(inv["candidates"])!=2:raise ValueError("bounded registry fixture")
    p,n=inv["candidates"]
    if p["polarity"]!="positive" or n["polarity"]!="negative":raise ValueError("polarity")
    mods=sorted({typed.name(x["module"]) for x in inv["candidates"]})
    out=["import "+m for m in mods]+["","open Lean Meta","namespace KuuOSR25",
         "set_option autoImplicit false","set_option maxHeartbeats 12000000"]
    for k,q in sorted(qs.items()):
        if k!=q["case_id"] or preflight(inv,q,old.SCOPE)!="TYPE_COMPARISON_REQUIRED":
            raise ValueError("request preflight")
        out+=["def "+k+" : Prop := "+typed.term(q["target"])]
    out+=["end KuuOSR25","open Lean Meta","run_cmd do","  let env ← getEnv"]
    tick=chr(96)*2
    for key,c in (("p",p),("n",n)):
        out+=["  let some "+key+" := env.find? "+tick+c["name"]+' | throwError "missing admitted theorem"',
              "  let some "+key+"Idx := env.getModuleIdxFor? "+tick+c["name"]+' | throwError "missing theorem origin"',
              "  unless "+key+".isTheorem && "+key+".levelParams.isEmpty && env.allImportedModuleNames["+key+"Idx]!.toString == "+'"'+c["module"]+'" do',
              '    throwError "candidate origin/type shape changed"']
    for k in sorted(qs):
        out+=["  let some g"+k+" := env.find? "+tick+"KuuOSR25."+k+' | throwError "missing request"',
              "  let some t"+k+" := g"+k+'.value? (allowOpaque := true) | throwError "missing request body"',
              "  if t"+k+".hasMVar || t"+k+".hasFVar || t"+k+".hasLooseBVars || t"+k+".hasLevelMVar then throwError \"open target\"",
              "  let (pEq"+k+", nEq"+k+") ← Lean.Elab.Command.liftTermElabM do",
              "    let a ← withNewMCtxDepth <| isDefEq p.type t"+k,
              "    let b ← withNewMCtxDepth <| isDefEq n.type (mkApp (mkConst "+tick+"Not) t"+k+")",
              "    pure (a,b)",
              "  let result"+k+" := Json.mkObj [",
              '    ("case", toJson "'+k+'"), ("target_expr", toJson (reprStr t'+k+')),',
              '    ("positive_type", toJson (reprStr p.type)), ("negative_type", toJson (reprStr n.type)),',
              '    ("positive_structural_equal", toJson (p.type.equal t'+k+')),',
              '    ("positive_defeq", toJson pEq'+k+'), ("negative_defeq", toJson nEq'+k+')]',
              '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ result'+k+'.compress)']
    return "\n".join(out)+"\n"

def decide(inv,q,row):
    if preflight(inv,q,old.SCOPE)!="TYPE_COMPARISON_REQUIRED" or row["case"]!=q["case_id"]:
        return {"status":"HOLD_REQUEST_BINDING"}
    p,n=row["positive_defeq"],row["negative_defeq"]
    if type(p) is not bool or type(n) is not bool:
        raise ValueError("invalid Lean comparison result")
    if p and n:return {"status":"HOLD_CONFLICTING_CANDIDATES"}
    if not p and not n:return {"status":"HOLD_NO_TYPED_MATCH"}
    c=inv["candidates"][0 if p else 1]
    return {"status":"EXACT_APPLICATION_REQUIRED","candidate":c,"lookup_request_digest":q["request_digest"],
            "proof_authority":False}

def application(inv,q,row):
    result=decide(inv,q,row)
    if result["status"]!="EXACT_APPLICATION_REQUIRED":raise ValueError("unmatched target")
    c=result["candidate"]
    req=typed.make_request("r25_"+q["case_id"],c["module"],c["name"],q["target"],[],c["polarity"])
    return req,typed.render(req),typed.declarations(req)
