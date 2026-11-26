"""R32: context-bound exact root recall, then real indexed fallback.
The proposition and its seven-argument request context are checked separately.
An exact theorem for a different requested atlas/observer is not authority
to answer that request. No synthetic True fallback in this experiment."""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_extended_recursive_recall_v1 as base
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
root=base.root
prev=base.prev
ext=base.ext
portable=base.portable
ledger=base.ledger
MARK="KUUOS_R32_ROOT "
LEC="Kuu.LivingEngi."
DIRECT="891b5aa7c59677f801e8332bcd7749fa4861e7754abd209c58142f1cd19376bc"
MCP="9a5a7bcc9f25130f974a2b0135247c64aab174f3a837e8f93756047b3dc67744"
VIEW="d8891acb12f4ab688dbb8bc75e6c3663edd2ff4f70954cd871269fc636b0d845"

def c(n):return {"const":n}
def ap(n,*args):return {"apply":[c(n),*args]}

def context_target(q):
    root.validate(q)
    a=q["context_args"]
    h=q["target"]["apply"][0]["const"]
    if h in (LEC+"Compatible",LEC+"HasGlobal"):
        return ap(h,a[0],a[1],a[2],a[4],a[6])
    if h==LEC+"OverlapFiberFaithful":
        return ap(h,*a)
    raise ValueError("unsupported contextual head")

def requests(qs,rows):
    local=qs["local_refined_context"];glob=qs["global_identity_context"]
    wrong=qs["wrong_source_context"]
    a=local["context_args"];orig=wrong["context_args"]
    # The same original F55 values/abstract cover, not a substitute atlas.
    observe=c(LEC+"northNativeF55Observe");shadow=c(LEC+"NorthNativeF55Shadow")
    goodfaith=[a[0],a[1],a[2],shadow,a[4],observe,a[6]]
    badfaith=goodfaith[:-1]+[orig[6]]
    mods=local["context_modules"]
    def req(k,t,args):return root.make_request(k,t,args,mods)
    negative=base.case(rows,"raw_negative")[1]["target"]
    return {
      "local":(local,a),
      "global":(glob,glob["context_args"]),
      "wrong_source":(wrong,a),
      "wrong_observer":(req("wrong_observer",local["target"],goodfaith),a),
      "raw_negative":(req("raw_negative",negative,orig),orig),
      "faithful_constant":(req("faithful_constant",ap(LEC+"OverlapFiberFaithful",*goodfaith),goodfaith),goodfaith),
      "faithful_original":(req("faithful_original",ap(LEC+"OverlapFiberFaithful",*badfaith),badfaith),badfaith)
    }

def render(q,admitted_args,inv,rows,reg):
    if len(admitted_args)!=7:raise ValueError("admitted context arity")
    src=root.render(q,inv);ns="KuuOSR20."+q["case_id"];tick=chr(96)*2
    end="end "+ns+"\n"
    if src.count(end)!=1:raise ValueError("context definition boundary")
    defs="def expectedGoal : Prop := "+typed.term(context_target(q))+"\n"
    defs+="".join("noncomputable def admittedCtx"+str(i)+" := "+typed.term(x)+"\n" for i,x in enumerate(admitted_args))
    src=src.replace(end,defs+end,1)
    marker="  let payload ← Lean.Elab.Command.liftTermElabM do\n"
    if src.count(marker)!=1:raise ValueError("root payload boundary")
    src=src.split(marker)[0]
    src+="  let some eGoal := env.find? "+tick+ns+'.expectedGoal | throwError "missing context goal"\n'
    src+='  let some expectedGoal := eGoal.value? (allowOpaque := true) | throwError "missing context goal body"\n'
    for i in range(7):
        src+="  let some ac"+str(i)+" := env.find? "+tick+ns+".admittedCtx"+str(i)+' | throwError "missing admitted context"\n'
        src+="  let some av"+str(i)+" := ac"+str(i)+'.value? (allowOpaque := true) | throwError "missing admitted context body"\n'
    src+="  let admittedArgs : Array Expr := #["+ ", ".join("av"+str(i) for i in range(7))+"]\n"
    src+=r'''
  let payload ← Lean.Elab.Command.liftTermElabM do
    let targetAligned := goal.equal expectedGoal
    let mut contextAligned := ctxArgs.size == admittedArgs.size
    for i in [:ctxArgs.size] do
      unless ctxArgs[i]!.equal admittedArgs[i]! do
        contextAligned := false
    if !targetAligned || !contextAligned then
      return Json.mkObj [
        ("goal_expr", toJson (reprStr goal)), ("context_goal_expr", toJson (reprStr expectedGoal)),
        ("target_aligned", toJson targetAligned), ("context_aligned", toJson contextAligned),
        ("search_executed", toJson false), ("result", Json.null)]
    let r ← KuuOSR18.walk pools bound closedRecall 3 #[] goal #[]
    pure (Json.mkObj [
      ("goal_expr", toJson (reprStr goal)), ("context_goal_expr", toJson (reprStr expectedGoal)),
      ("target_aligned", toJson targetAligned), ("context_aligned", toJson contextAligned),
      ("search_executed", toJson true), ("result", KuuOSR18.resultJson r)])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R32_ROOT " ++ payload.compress)
'''
    return base.extend(src,rows,reg)

def application(q,inv,reg,route,case,negative=False):
    if not route:raise ValueError("empty route")
    n=route[0]["rule"]
    materials={c["name"]:c for pool in inv["selected"].values() for c in pool}
    materials.update({c["name"]:c for c in reg["candidates"]})
    p=materials[n]
    if route[0]["arity"]==0:
        if len(route)!=1:raise ValueError("closed route has children")
        req=typed.make_request(case,p["module"],n,q["target"],[],"negative" if negative else "positive")
        return req,typed.render(req),typed.declarations(req)
    if negative:raise ValueError("negative proof route not closed")
    fixed=root.poly.make_query(q["case_id"],p["module"],n,q["target"],"positive",q["context_modules"],[])
    return root.base.application(fixed,q["context_args"],route,case)

def decision(row,rows):
    if not row["search_executed"]:
        if row["target_aligned"] and row["context_aligned"]:raise ValueError("unexplained context HOLD")
        return {"status":"HOLD_CONTEXT_MISMATCH","routes":[]}
    if not row["target_aligned"] or not row["context_aligned"] or row["goal_expr"]!=row["context_goal_expr"]:
        raise ValueError("unbound search")
    r=row["result"];tr=r["trace"];goal=row["goal_expr"]
    hits=base.hits(tr,rows)
    if hits and hits[0]["goal_expr"]==goal and tr[0]==hits[0]:
        h=hits[0];pol=h["status"]==base.NEG
        if r["cache_entries"]!=0 or r["cache_hits"]!=0 or h["candidate_comparison_searches"]!=0:
            raise ValueError("exact root performed comparison")
        if (pol and r["route"] is not None) or (not pol and r["route"]!=[{"rule":h["rule"],"arity":0}]):
            raise ValueError("exact root decision")
        return {"status":"EXACT_ROOT_NEGATIVE_CANDIDATE" if pol else "EXACT_ROOT_POSITIVE_CANDIDATES",
                "routes":[[{"rule":n,"arity":0}] for n in h["matches"]],"comparisons":0}
    if not tr or tr[0].get("status")!=base.FRESH or tr[0].get("candidate_comparison_searches")!=8:
        raise ValueError("new root did not compare complete admitted candidate set")
    if r["route"] is not None:
        return {"status":"INDEXED_POSITIVE_CANDIDATE","routes":[r["route"]],"comparisons":8}
    neg=[t["rule"] for t in tr if t.get("status")=="HOLD_PENDING_EXACT_NEGATIVE_AUDIT" and t["goal_expr"]==goal]
    if len(neg)==1:
        return {"status":"INDEXED_NEGATIVE_CANDIDATE","routes":[[{"rule":neg[0],"arity":0}]],"comparisons":8}
    return {"status":"HOLD_SEARCH_REQUIRED","routes":[],"comparisons":8}
