"""R27: provenance-bound multi-candidate typed recall with local exact-goal memo.
The memo is a comparison cache inside one imported Lean environment, not a
proof cache or a semantic negative result. All matches retain their identities.
Only exact independently audited witnesses permit local route decisions."""
from __future__ import annotations
import hashlib
from runtime import kuuos_codeai_olean_recursive_capsule_recall_v1_r2 as prev
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime import kuuos_codeai_olean_general_application_v1 as typed
root=prev.root
lookup=prev.lookup
MARK=prev.MARK
PROBE="KUUOS_R27_RECALL "
LEC="Kuu.LivingEngi."
EXTRA=((LEC+"SourceAwareOverlapDescentCriterion",LEC+"nativeF55_constant_twoChart_refined_global","positive"),
       (LEC+"NativeF55CechSourceGluingObstruction",LEC+"nativeF55_twoChart_constant_raw_global","positive"),
       (LEC+"NativeF55CechSourceGluingObstruction",LEC+"nativeF55_twoChart_raw_no_global","negative"))

def inventory(base,observations,additional):
    if lookup.preflight(base,lookup.request("inventory_probe",{"const":"True"}),old.SCOPE)!="TYPE_COMPARISON_REQUIRED":
        raise ValueError("base registry")
    rows={r["name"]:r for r in observations}
    if len(rows)!=len(observations):raise ValueError("duplicate prior observations")
    raw=EXTRA[-1][1]
    if additional["name"]!=raw:raise ValueError("new material identity")
    rows[raw]=additional
    candidates=[dict(x) for x in base["candidates"]]+[{"module":m,"name":n,"polarity":p} for m,n,p in EXTRA]
    for c in candidates:
        typed.name(c["module"]);typed.name(c["name"])
        r=rows[c["name"]]
        if set(r["axioms"])-typed.STANDARD or r["type_expr_sha256"]!=hashlib.sha256(r["type_expr_repr"].encode()).hexdigest():
            raise ValueError("unadmitted full type")
        c["type_sha256"]=r["type_expr_sha256"]
        c["axioms"]=r["axioms"]
        c["observation_digest"]=old.digest(r)
    candidates.sort(key=lambda c:(c["module"],c["name"],c["polarity"]))
    if len({c["name"] for c in candidates})!=len(candidates):raise ValueError("duplicate candidate")
    x={"source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "parent_inventory_key":base["key"],"candidates":candidates,
       "semantic_search_complete":False,"proof_authority":False}
    return {**x,"key":old.digest(x)}

def valid(inv):
    if inv["key"]!=old.digest({k:v for k,v in inv.items() if k!="key"}):
        return "HOLD_INVENTORY_INTEGRITY"
    if inv["scope_digest"]!=old.SCOPE or inv["source_head"]!=old.HEAD or inv["source_tree"]!=old.TREE:
        return "HOLD_SCOPE"
    if not 1<=len(inv["candidates"])<=64 or len({c["name"] for c in inv["candidates"]})!=len(inv["candidates"]):
        return "HOLD_INVENTORY_INTEGRITY"
    if any(c["polarity"] not in ("positive","negative") for c in inv["candidates"]):
        return "HOLD_INVENTORY_INTEGRITY"
    return "TYPE_COMPARISON_REQUIRED"

# Cache keys are synthetic, inventory-bound names distinct from real rules.
# Reuse only exact structural goal keys, never a failed comparison.
HELPER=r'''
open Lean Meta KuuOSR16 KuuOSR17
namespace KuuOSR27
def trial (entries : Array KuuOSR17.CacheEntry) (key n : Name)
    (moduleName : String) (target : Expr) :
    MetaM (KuuOSR16.Trial × Array KuuOSR17.CacheEntry × Bool) := do
  for e in entries do
    if e.rule == key && e.goal.equal target then
      return (e.trial, entries, true)
  let t ← try
    withNewMCtxDepth do
      let env ← getEnv
      let info ← getConstInfo n
      let some idx := env.getModuleIdxFor? n |
        throwError "R27 missing origin"
      unless info.isTheorem && info.levelParams.isEmpty &&
          KuuOSR16.closed info.type && !info.type.hasLevelMVar &&
          env.allImportedModuleNames[idx]!.toString == moduleName do
        throwError "R27 inadmissible recall source"
      let same ← isDefEq info.type target
      pure ⟨if same then (if info.type.equal target then "MATCH_EXACT" else "MATCH_DEFEQ")
        else "HOLD_NOT_DEFEQ", 0, 0, 0, #[]⟩
    catch _ => pure ⟨"HOLD_COMPARISON_FAILURE", 0, 0, 0, #[]⟩
  if t.status == "HOLD_COMPARISON_FAILURE" then
    return (t, entries, false)
  return (t, entries.push ⟨target, key, t⟩, false)
end KuuOSR27
'''

def helpers(inv):
    if valid(inv)!="TYPE_COMPARISON_REQUIRED":raise ValueError("registry preflight")
    tick=chr(96)*2
    import json
    names=", ".join("("+tick+typed.name(c["name"])+", "+json.dumps(typed.name(c["module"]))+", "+
        ("true" if c["polarity"]=="negative" else "false")+")" for c in inv["candidates"])
    hook=r'''
  let mut recallCache := entries
  let mut recallHits := 0
  let mut yes : Array (Name × Bool) := #[]
  let mut no : Array Name := #[]
  let mut failed := false
  if KuuOSR16.closed goal && !goal.hasLevelMVar then
    let candidates : Array (Name × String × Bool) := #[CANDIDATES]
    for (n, m, neg) in candidates do
      let target := if neg then mkApp (mkConst NOTCONST) goal else goal
      let key := Name.str (Name.mkSimple "KuuOSR27Recall") ("REGISTRY:" ++ n.toString)
      let (t, next, hit) ← KuuOSR27.trial recallCache key n m target
      recallCache := next
      if hit then recallHits := recallHits + 1
      if t.status == "HOLD_COMPARISON_FAILURE" then failed := true
      if t.status == "MATCH_EXACT" || t.status == "MATCH_DEFEQ" then
        if neg then no := no.push n
        else yes := yes.push (n, t.status == "MATCH_EXACT")
    if failed || (!yes.isEmpty && !no.isEmpty) then
      return ⟨none, recallCache, #[KuuOSR17.holdRow "HOLD_RECALL_CONFLICT_OR_COMPARISON" goal], recallHits⟩
    if let some n := no[0]? then
      return ⟨none, recallCache, #[Json.mkObj [
        ("status", toJson "HOLD_ROUTE_EXACT_NEGATIVE"),
        ("goal_expr", toJson (reprStr goal)), ("rule", toJson n.toString),
        ("matches", toJson (no.map Name.toString)), ("recall_hits", toJson recallHits)]], recallHits⟩
    if let some (p, structural) := yes[0]? then
      return ⟨some [(p, 0)], recallCache, #[Json.mkObj [
        ("status", toJson "CAPSULE_EXACT_LEAF_CANDIDATE"),
        ("goal_expr", toJson (reprStr goal)), ("rule", toJson p.toString),
        ("matches", toJson (yes.map (fun x => x.1.toString))),
        ("recall_hits", toJson recallHits), ("structural_equal", toJson structural)]], recallHits⟩
  let entries := recallCache
'''.replace("CANDIDATES",names).replace("NOTCONST",tick+"Not").replace("REGISTRY",inv["key"])
    s=root.base.HELPER
    start="  if ancestors.any (fun e => e.equal goal) then"
    if s.count(start)!=1:raise ValueError("walk boundary")
    # Only modify walk, not negative or lookupBound. Carry exact recall
    # cache entries and hit accounting through fallback AND-OR search.
    prefix,walk=s.split("def walk ",1)
    walk=walk.replace(start,hook+start,1)
    walk=walk.replace("let mut hits := 0","let mut hits := recallHits",1)
    walk=walk.replace('#[KuuOSR17.holdRow "HOLD_DEPTH_BUDGET" goal], 0⟩',
                      '#[KuuOSR17.holdRow "HOLD_DEPTH_BUDGET" goal], recallHits⟩',1)
    marker="    let (neg, initial, negTrace, negHits) ← negative pools goal entries"
    if walk.count(marker)!=1:raise ValueError("fallback boundary")
    walk=walk.replace(marker,marker+"\n    let negHits := negHits + recallHits\n    let negTrace := (#[KuuOSR17.holdRow \"HOLD_NO_TYPED_MATCH_CONTINUE\" goal] : Array Json) ++ negTrace",1)
    return HELPER+"\n"+prefix+"def walk "+walk

def render(q,inv,capsules):
    s=root.render(q,inv);marker=root.base.HELPER
    if s.count(marker)!=1:raise ValueError("root helper boundary")
    mods={typed.name(x["module"]) for x in capsules["candidates"]}
    imports="".join("import "+m+"\n" for m in sorted(mods) if "import "+m+"\n" not in s)
    return imports+s.replace(marker,helpers(capsules),1)

def fixture(qs,base,inv):
    s=prev.fixture(qs,base)
    marker=prev.helpers(base)
    if s.count(marker)!=1:raise ValueError("fixture helper boundary")
    mods={typed.name(c["module"]) for c in inv["candidates"]}
    imports="".join("import "+m+"\n" for m in sorted(mods) if "import "+m+"\n" not in s)
    return imports+s.replace(marker,helpers(inv),1)

def targets(qs,r20):
    # Fresh requests: raw and refined contexts are distinct. No rewriting
    # of the original atlas is performed to make a proof applicable.
    c=lambda n:{"const":n}
    q=r20["requests"]
    a=q["local_refined_context"]["context_args"]
    b=q["wrong_source_context"]["context_args"]
    raw=lambda xs:{"apply":[c(LEC+"HasGlobal"),xs[0],xs[1],xs[2],xs[4],xs[6]]}
    return {"capsule_exact":qs["exact_new"]["target"],"capsule_defeq":qs["defeq_new"]["target"],
            "refined_global":q["global_identity_context"]["target"],
            "raw_global":raw(a),"raw_negative":raw(b),
            "refined_negative":qs["negative_defeq"]["target"],"unknown":qs["wrong_atlas"]["target"]}

def probe(targets,inv):
    mods=sorted({typed.name(c["module"]) for c in inv["candidates"]})
    out=["import "+m for m in mods]+["",root.poly.HELPER,root.base.prev.HELPER,helpers(inv),
         "namespace KuuOSR27Probe","set_option autoImplicit false","set_option maxHeartbeats 16000000"]
    for k,t in sorted(targets.items()):
        if not typed.CASE.fullmatch(k):raise ValueError("probe identity")
        out+=["def "+k+" : Prop := "+typed.term(t)]
    out+=["end KuuOSR27Probe","open Lean Meta","run_cmd do","  let env ← getEnv"]
    tick=chr(96)*2
    for i,k in enumerate(sorted(targets)):
        out+=["  let some c"+str(i)+" := env.find? "+tick+"KuuOSR27Probe."+k+' | throwError "missing target"',
              "  let some p"+str(i)+" := c"+str(i)+'.value? (allowOpaque := true) | throwError "missing target body"']
    out+=["  let payload ← Lean.Elab.Command.liftTermElabM do",
          "    let mut entries : Array KuuOSR17.CacheEntry := #[]","    let mut rows : Array Json := #[]"]
    for i,k in enumerate(sorted(targets)):
        out+=["    let first"+str(i)+" ← KuuOSR18.walk #[] #[] #[] 3 #[] p"+str(i)+" entries",
              "    let replay"+str(i)+" ← KuuOSR18.walk #[] #[] #[] 3 #[] p"+str(i)+" first"+str(i)+".entries",
              "    entries := replay"+str(i)+".entries",
              '    rows := rows.push (Json.mkObj [("case", toJson "'+k+'"), ("first", KuuOSR18.resultJson first'+str(i)+'), ("replay", KuuOSR18.resultJson replay'+str(i)+')])']
    out+=["    pure (toJson rows)",'  Lean.Elab.Command.liftIO <| IO.println ("'+PROBE+'" ++ payload.compress)',""]
    return "\n".join(out)
