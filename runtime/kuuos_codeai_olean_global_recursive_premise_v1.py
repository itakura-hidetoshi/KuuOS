"""R17: global indexed polymorphic single-residual search with exact-context memo.

All R7 rows are accounted for. A syntactic head is advisory; no match,
deferred head, budget, cycle or failure is a mathematical refutation.
Cache entries live in one fixed imported Lean environment and are not
certificates. Only final independently audited applications are admitted.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3
from runtime import kuuos_codeai_olean_polymorphic_premise_v1 as poly
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

MARK="KUUOS_R17_SEARCH "
LIMIT=24
FUEL=3
HELPER=r'''
open Lean Meta KuuOSR16
namespace KuuOSR17
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

structure CacheEntry where
  goal : Expr
  rule : Name
  trial : KuuOSR16.Trial

structure SearchResult where
  route : Option (List Name)
  entries : Array CacheEntry
  trace : Array Json
  hits : Nat

def lookupTrial (entries : Array CacheEntry) (n : Name) (goal : Expr) :
    MetaM (KuuOSR16.Trial × Array CacheEntry × Bool) := do
  for e in entries do
    if e.rule == n && e.goal.equal goal then
      return (e.trial, entries, true)
  let t ← KuuOSR16.safeSpecialize n goal
  return (t, entries.push ⟨goal, n, t⟩, false)

def holdRow (reason : String) (goal : Expr) : Json :=
  Json.mkObj [("status", toJson reason), ("goal_expr", toJson (reprStr goal))]

def walk (pools : Array (String × Array Name)) (fuel : Nat)
    (ancestors : Array Expr) (goal : Expr) (entries : Array CacheEntry) :
    MetaM SearchResult := do
  if ancestors.any (fun e => e.equal goal) then
    return ⟨none, entries, #[holdRow "HOLD_EXACT_CYCLE" goal], 0⟩
  match fuel with
  | 0 => return ⟨none, entries, #[holdRow "HOLD_DEPTH_BUDGET" goal], 0⟩
  | remaining + 1 =>
    let head := if goal.getAppFn.isConst then goal.getAppFn.constName!.toString else ""
    let some (_, rules) := pools.find? (fun p => p.1 == head) |
      return ⟨none, entries, #[holdRow "HOLD_UNRANKED_HEAD" goal], 0⟩
    let mut cacheNow := entries
    let mut traceNow : Array Json := #[]
    let mut hitsNow := 0
    for n in rules do
      let (trial, nextCache, hit) ← lookupTrial cacheNow n goal
      cacheNow := nextCache
      if hit then hitsNow := hitsNow + 1
      traceNow := traceNow.push (Json.mkObj [
        ("goal_expr", toJson (reprStr goal)),
        ("rule", toJson n.toString), ("trial", KuuOSR16.trialJson n trial),
        ("cache_hit", toJson hit)])
      if trial.status == "MATCH_COMPLETE" then
        return ⟨some [n], cacheNow, traceNow, hitsNow⟩
      if trial.status == "MATCH_RESIDUAL" && trial.residual.size == 1 then
        let child ← walk pools remaining (ancestors.push goal) trial.residual[0]! cacheNow
        cacheNow := child.entries
        traceNow := traceNow ++ child.trace
        hitsNow := hitsNow + child.hits
        if let some route := child.route then
          return ⟨some (n :: route), cacheNow, traceNow, hitsNow⟩
      else if trial.status == "MATCH_RESIDUAL" then
        traceNow := traceNow.push (holdRow "HOLD_MULTI_RESIDUAL" goal)
    return ⟨none, cacheNow, traceNow, hitsNow⟩
termination_by fuel

def resultJson (s : SearchResult) : Json :=
  Json.mkObj [("route", toJson (s.route.map (List.map Name.toString))),
    ("trace", toJson s.trace), ("cache_entries", toJson s.entries.size),
    ("cache_hits", toJson s.hits)]
end KuuOSR17
'''

def inventory(db,receipt,historical):
    db=Path(db)
    if (old.digest(receipt)!=old.R7 or receipt["source_head"]!=old.HEAD or
            receipt["scope_digest"]!=old.SCOPE or db.is_symlink() or not db.is_file()):
        raise ValueError("unadmitted index")
    with db.open("rb") as f:
        if hashlib.file_digest(f,"sha256").hexdigest()!=receipt["database_sha256"]:
            raise ValueError("index bytes changed")
    primary_heads=set();secondary_heads=set()
    for row in historical["specializations"].values():
        primary_heads.update(x for x in row["primary"]["heads"] if x)
        for b in row["branches"]:secondary_heads.update(x for x in b["secondary"]["heads"] if x)
    heads=sorted(primary_heads|secondary_heads)
    if not heads or len(heads)>8:raise ValueError("bounded head inventory")
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        rows=[json.loads(x[0]) for x in con.execute("SELECT row_json FROM theorem_types ORDER BY module,name")]
        modules={x[0]:json.loads(x[1]) for x in con.execute("SELECT module,row_json FROM modules ORDER BY module")}
    finally:con.close()
    if len(rows)!=47705 or len(modules)!=2815:raise ValueError("global index inventory")
    gaps=[x for x in modules.values() if x["state"].startswith("HOLD")]
    if len(gaps)!=695:raise ValueError("coverage drift")
    counts=Counter(x["name"] for x in rows);pools={h:[] for h in heads};excluded=Counter()
    for x in rows:
        h=x["conclusion_head"]
        if h not in pools:excluded["OTHER_HEAD_DEFERRED"]+=1;continue
        if x["binder_count"]>32:excluded["BINDER_BUDGET_DEFERRED"]+=1;continue
        if counts[x["name"]]!=1 or modules[x["module"]]["state"].startswith("HOLD"):
            excluded["AMBIGUOUS_OR_UNOBSERVED_ORIGIN"]+=1;continue
        try:typed.name(x["name"]);typed.name(x["module"])
        except ValueError:
            excluded["UNSUPPORTED_IDENTIFIER"]+=1;continue
        is_open=bool(x["binder_count"] or x["universe_parameters"])
        priority=int(is_open!=(h in primary_heads))
        pools[h].append({"module":x["module"],"name":x["name"],"row_digest":old.digest(x),
                         "binder_count":x["binder_count"],"universe_parameters":x["universe_parameters"],
                         "priority":priority})
    selected={};deferred={}
    for h,rs in pools.items():
        rs.sort(key=lambda x:(x["priority"],x["binder_count"],x["module"],x["name"]))
        selected[h]=rs[:LIMIT];deferred[h]=rs[LIMIT:]
    if sum(map(len,selected.values()))+sum(map(len,deferred.values()))+sum(excluded.values())!=len(rows):
        raise ValueError("index partition")
    return {"source_head":old.HEAD,"scope_digest":old.SCOPE,"index_rows":len(rows),
            "primary_heads":sorted(primary_heads),"secondary_heads":sorted(secondary_heads),
            "selected":selected,"deferred_matching":deferred,"other_deferred_counts":dict(sorted(excluded.items())),
            "unobserved_modules":gaps,"semantic_search_complete":False,"proof_authority":False}

def render(q,inv):
    poly.validate(q);req=q["request"];tick=chr(96)*2
    if inv["source_head"]!=old.HEAD or inv["scope_digest"]!=old.SCOPE:raise ValueError("inventory scope")
    flat=[p for ps in inv["selected"].values() for p in ps]
    mods=sorted(set([req["module"]]+q["context_modules"]+[p["module"] for p in flat]))
    for m in mods:typed.name(m)
    for p in flat:typed.name(p["name"])
    entries=", ".join('("'+p["module"]+'", '+tick+p["name"]+')' for p in flat)
    pools=", ".join('("'+h+'", #['+", ".join(tick+p["name"] for p in ps)+'])'
                    for h,ps in inv["selected"].items())
    for h in inv["selected"]:typed.name(h)
    ns="KuuOSR17."+req["case_id"];goal=typed.term(req["target"])
    if req["polarity"]=="negative":goal="Not ("+goal+")"
    out=["import "+m for m in mods]+["",poly.HELPER,HELPER,"namespace "+ns,
        "set_option autoImplicit false","set_option maxRecDepth 8192","set_option maxHeartbeats 8000000",
        "def goal : Prop := "+goal,"end "+ns,"open Lean Meta KuuOSR16 KuuOSR17",
        "run_cmd do","  let env ← getEnv",
        "  let some info := env.find? "+tick+ns+".goal"+' | throwError "missing goal"',
        '  let some goal := info.value? (allowOpaque := true) | throwError "missing goal body"',
        "  let candidates : Array (String × Name) := #["+entries+"]",
        "  for (moduleName, n) in candidates do",
        '    let some candidate := env.find? n | throwError "indexed theorem missing"',
        '    let some idx := env.getModuleIdxFor? n | throwError "indexed origin missing"',
        '    unless candidate.isTheorem && env.allImportedModuleNames[idx]!.toString == moduleName do',
        '      throwError "indexed theorem origin changed"',
        "  let pools : Array (String × Array Name) := #["+pools+"]",
        "  let payload ← Lean.Elab.Command.liftTermElabM do",
        "    let n := "+tick+req["source"],
        "    let primary ← KuuOSR16.safeSpecialize n goal",
        '    unless primary.status == "MATCH_RESIDUAL" && primary.residual.size == 1 do',
        '      throwError "primary did not yield one closed premise"',
        "    let residual := primary.residual[0]!",
        "    let first ← KuuOSR17.walk pools "+str(FUEL)+" #[goal] residual #[]",
        "    let replay ← KuuOSR17.walk pools "+str(FUEL)+" #[goal] residual first.entries",
        "    let cycle ← KuuOSR17.walk pools "+str(FUEL)+" #[residual] residual first.entries",
        "    let budget ← KuuOSR17.walk pools 0 #[] residual first.entries",
        '    pure (Json.mkObj [("goal_expr", toJson (reprStr goal)),',
        '      ("primary", KuuOSR16.trialJson n primary),',
        '      ("first", KuuOSR17.resultJson first), ("replay", KuuOSR17.resultJson replay),',
        '      ("cycle_fixture", KuuOSR17.resultJson cycle), ("budget_fixture", KuuOSR17.resultJson budget)])',
        '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    return "\n".join(out)

def application(q,route,case):
    poly.validate(q);r=q["request"]
    req=typed.make_request(case,r["module"],r["source"],r["target"],[],r["polarity"])
    if not 1<=len(route)<=FUEL:raise ValueError("route depth")
    for p in route:typed.name(p["module"]);typed.name(p["name"])
    mods=sorted(set([r["module"]]+q["context_modules"]+[p["module"] for p in route]))
    prefix="import "+r["module"]+"\n"
    ty="target" if r["polarity"]=="positive" else "Not target"
    marker="theorem witness : "+ty+" := @"+r["source"]
    change=typed.term(r["target"])
    if r["polarity"]=="negative":change="Not ("+change+")"
    replacement="theorem witness : "+ty+" := by\n  change "+change+"\n  apply @"+r["source"]
    replacement+="".join("\n  apply @"+p["name"] for p in route)
    def transform(s):
        if not s.startswith(prefix) or s.count(marker)!=1:raise ValueError("renderer boundary")
        return "".join("import "+m+"\n" for m in mods)+s[len(prefix):].replace(marker,replacement)
    return req,transform(typed.render(req)),transform(typed.declarations(req))
