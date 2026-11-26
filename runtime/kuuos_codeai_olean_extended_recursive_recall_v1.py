"""R31: consume the independently admitted R30 append-only ledger within
recursive AND-OR search. Keep every exact matching proof identity. Prefer the
new capsule only as a deterministic search policy, not as stronger truth.
Historical no-match may skip the historical five candidates, never new ones.
All selected routes still require fresh kernel proof and independent audit."""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_memory_extension_v1 as ext
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
prev=ext.prev
portable=ext.portable
multi=prev.multi
root=prev.root
KEY="02666ac7224ba2d57163424df252d6158ff7273c33d11586fcbf7b36188bd912"
DIRECT="8b41b6576cc695b8ebe6d04b01e7588a64f1e39e44169cdb1c69dccbe1c532ac"
MCP="4f8be45415d97d98b39468cf696885c3c61b861fef5c1b678f95708a070dcdee"
MARK="KUUOS_R31_BRANCHES "
POS="R31_EXACT_POSITIVE_CANDIDATE"
NEG="R31_EXACT_NEGATIVE_PREMISE"
MISS="R31_HISTORY_MISS_NEW_CANDIDATES_CHECKED"
FRESH="R31_NEW_GOAL_CANDIDATES_CHECKED"

def ledger(mem,layer,bridge,reg):
    if (mem["key"]!=prev.R28_MEMORY or mem["key"]!=portable.seal(mem)["key"] or
        layer["key"]!=KEY or layer["key"]!=portable.seal(layer)["key"] or
        layer["parent_memory_key"]!=mem["key"] or layer["transport_key"]!=bridge["key"] or
        layer["source_head"]!=prev.CURRENT or layer["source_tree"]!=prev.CURRENT_TREE or
        layer["scope_digest"]!=old.SCOPE or layer["lean"]!=portable.LEAN or layer["mathlib"]!=portable.MATHLIB):
        raise ValueError("ledger provenance")
    cs={c["name"]:c for c in reg["candidates"]}
    if len(cs)!=len(reg["candidates"]) or len(cs)!=8:raise ValueError("candidate inventory")
    rows={};seen=set()
    for i,k in enumerate(sorted(set(mem["records"])|set(layer["additions"]))):
        h=mem["records"].get(k);new=layer["additions"].get(k,[])
        material=([h] if h is not None else [])+new
        x=material[0];expr=x["target_expr"]
        if portable.hash_type(expr)!=k or any(r["target_key"]!=k or r["target_expr"]!=expr for r in material):
            raise ValueError("target identity")
        for r in material:typed.term(r["target"])
        matches=[r["candidate"] for r in new+([h] if h is not None else []) if r["candidate"] is not None]
        if any(cs[c["name"]]!=c for c in matches) or len({c["name"] for c in matches})!=len(matches):
            raise ValueError("witness identity")
        if len({c["polarity"] for c in matches})>1:raise ValueError("conflicting exact evidence")
        seen.update(c["name"] for c in matches)
        if not matches and (h is None or h["status"]!="HOLD_HISTORICAL_NO_MATCH"):
            raise ValueError("unadmitted miss")
        rows[k]={"alias":"g"+str(i),"target":x["target"],"target_expr":expr,
                 "cases":[r["case"] for r in material],"matches":matches}
    if seen!=set(cs) or len(rows)!=9 or sum(len(r["matches"]) for r in rows.values())!=9:
        raise ValueError("ledger cardinality")
    return rows

def case(rows,k):
    xs=[(key,r) for key,r in rows.items() if k in r["cases"]]
    if len(xs)!=1:raise ValueError("case identity")
    return xs[0]

def helpers(rows,reg):
    tick=chr(96)*2
    entries=[]
    for k,r in sorted(rows.items()):
        cs=r["matches"];pol=cs[0]["polarity"] if cs else "miss"
        entries.append("("+tick+"KuuOSR28Probe."+r["alias"]+", "+json.dumps(pol)+", #["+
                       ", ".join(tick+typed.name(c["name"]) for c in cs)+"], "+json.dumps(k)+")")
    cand=", ".join("("+tick+typed.name(c["name"])+", "+json.dumps(typed.name(c["module"]))+", "+
                   ("true" if c["polarity"]=="negative" else "false")+")" for c in reg["candidates"])
    hook=r'''
  let mut memoOldMiss := false
  let mut memoKey := ""
  if KuuOSR16.closed goal && !goal.hasLevelMVar then
    let memoryRows : Array (Name × String × Array Name × String) := #[MEMROWS]
    for (targetName, polarity, witnesses, recordKey) in memoryRows do
      let info ← getConstInfo targetName
      let some body := info.value? (allowOpaque := true) | throwError "missing ledger goal"
      if body.equal goal then
        if polarity == "miss" then
          memoOldMiss := true
          memoKey := recordKey
        else
          let some chosen := witnesses[0]? | throwError "missing admitted witness"
          let event := Json.mkObj [
            ("status", toJson (if polarity == "positive" then "R31_EXACT_POSITIVE_CANDIDATE" else "R31_EXACT_NEGATIVE_PREMISE")),
            ("goal_expr", toJson (reprStr goal)), ("rule", toJson chosen.toString),
            ("matches", toJson (witnesses.map Name.toString)), ("record_key", toJson recordKey),
            ("candidate_comparison_searches", toJson (0 : Nat))]
          if polarity == "positive" then
            return ⟨some [(chosen, 0)], entries, #[event], 0⟩
          if polarity == "negative" then
            return ⟨none, entries, #[event], 0⟩
          throwError "invalid ledger polarity"
  let mut memoCache := entries
  let mut memoHits := 0
  let mut memoComparisons := 0
  let mut memoPositive : Array Name := #[]
  let mut memoNegative : Array Name := #[]
  let mut memoFailed := false
  if KuuOSR16.closed goal && !goal.hasLevelMVar then
    let candidates : Array (Name × String × Bool) := #[CANDIDATES]
    for (n, m, neg) in candidates do
      if memoOldMiss && m != "KuuOSCodeAIR30Capsule" then
        continue
      let target := if neg then mkApp (mkConst NOTCONST) goal else goal
      let key := Name.str (Name.mkSimple "KuuOSR31Recall") ("REGISTRY:" ++ n.toString)
      let (t, next, hit) ← KuuOSR27.trial memoCache key n m target
      memoCache := next
      if hit then memoHits := memoHits + 1
      else memoComparisons := memoComparisons + 1
      if t.status == "HOLD_COMPARISON_FAILURE" then memoFailed := true
      if t.status == "MATCH_EXACT" || t.status == "MATCH_DEFEQ" then
        if neg then memoNegative := memoNegative.push n
        else memoPositive := memoPositive.push n
    if memoFailed || (!memoPositive.isEmpty && !memoNegative.isEmpty) then
      return ⟨none, memoCache, #[KuuOSR17.holdRow "HOLD_RECALL_CONFLICT_OR_COMPARISON" goal], memoHits⟩
    if let some n := memoNegative[0]? then
      return ⟨none, memoCache, #[Json.mkObj [
        ("status", toJson "HOLD_ROUTE_EXACT_NEGATIVE"),
        ("goal_expr", toJson (reprStr goal)), ("rule", toJson n.toString),
        ("matches", toJson (memoNegative.map Name.toString)),
        ("candidate_comparison_searches", toJson memoComparisons)]], memoHits⟩
    if let some n := memoPositive[0]? then
      return ⟨some [(n, 0)], memoCache, #[Json.mkObj [
        ("status", toJson "CAPSULE_EXACT_LEAF_CANDIDATE"),
        ("goal_expr", toJson (reprStr goal)), ("rule", toJson n.toString),
        ("matches", toJson (memoPositive.map Name.toString)),
        ("candidate_comparison_searches", toJson memoComparisons)]], memoHits⟩
  let entries := memoCache
'''.replace("MEMROWS",", ".join(entries)).replace("CANDIDATES",cand).replace("NOTCONST",tick+"Not").replace("REGISTRY",KEY)
    s=root.base.HELPER
    marker="  if ancestors.any (fun e => e.equal goal) then"
    fallback="    let (neg, initial, negTrace, negHits) ← negative pools goal entries"
    if s.count(marker)!=1 or s.count(fallback)!=1:raise ValueError("walk boundary")
    s=s.replace(marker,hook+marker,1)
    s=s.replace(fallback,fallback+r'''
    let memoTrace := Json.mkObj [
      ("status", toJson (if memoOldMiss then "R31_HISTORY_MISS_NEW_CANDIDATES_CHECKED" else "R31_NEW_GOAL_CANDIDATES_CHECKED")),
      ("goal_expr", toJson (reprStr goal)), ("record_key", toJson memoKey),
      ("candidate_comparison_searches", toJson memoComparisons)]
    let negTrace := (#[memoTrace] : Array Json) ++ negTrace
    let negHits := negHits + memoHits''',1)
    return multi.HELPER+"\n"+s

def extend(src,rows,reg):
    mark=root.base.HELPER
    if src.count(mark)!=1:raise ValueError("R18 helper boundary")
    src=src.replace(mark,helpers(rows,reg),1)
    pre=portable.render({r["alias"]:r["target"] for r in rows.values()},reg)
    chunks=[pre,src]
    imports=sorted({l for s in chunks for l in s.splitlines() if l.startswith("import ")})
    bodies=["\n".join(l for l in s.splitlines() if not l.startswith("import ")) for s in chunks]
    return "\n".join(imports)+"\n\n"+"\n\n".join(bodies)+"\n"

def render(q,inv,rows,reg):
    return extend(root.render(q,inv),rows,reg)

RULES=r'''
namespace KuuOSR31Fixture
set_option autoImplicit false
theorem leftRule (a b c d : Prop) (ha : a) (hb : b) : (a ∧ b) ∨ (c ∧ d) := Or.inl ⟨ha,hb⟩
theorem rightRule (a b c d : Prop) (hc : c) (hd : d) : (a ∧ b) ∨ (c ∧ d) := Or.inr ⟨hc,hd⟩
theorem truth : True := True.intro
end KuuOSR31Fixture
'''

def fixture_terms(rows):
    return [case(rows,k)[1]["target"] for k in ("blocked_pair","capsule_exact","local_refined_context","global_identity_context")]

def fixture(rows,reg):
    imports="".join("import "+m+"\n" for m in sorted({c["module"] for c in reg["candidates"]}))
    a,b,c,d=map(typed.term,fixture_terms(rows))
    src=imports+"\n"+root.poly.HELPER+"\n"+root.base.prev.HELPER+"\n"+root.base.HELPER+"\n"+RULES
    src+="\nnamespace KuuOSR31Fixture\nset_option autoImplicit false\nset_option maxHeartbeats 16000000\n"
    src+="def goal : Prop := ("+a+" ∧ "+b+") ∨ ("+c+" ∧ "+d+")\n"
    src+="def unknown : Prop := "+typed.term(case(rows,"unknown")[1]["target"])+"\nend KuuOSR31Fixture\n"
    tick=chr(96)*2
    src+=r'''
open Lean Meta
run_cmd do
  let env ← getEnv
  let some g := env.find? TICKKuuOSR31Fixture.goal | throwError "missing goal"
  let some goal := g.value? (allowOpaque := true) | throwError "missing goal body"
  let some u := env.find? TICKKuuOSR31Fixture.unknown | throwError "missing unknown"
  let some unknown := u.value? (allowOpaque := true) | throwError "missing unknown body"
  let payload ← Lean.Elab.Command.liftTermElabM do
    let left := TICKKuuOSR31Fixture.leftRule
    let right := TICKKuuOSR31Fixture.rightRule
    let l ← KuuOSR16.safeSpecialize left goal
    let r ← KuuOSR16.safeSpecialize right goal
    unless l.status == "MATCH_RESIDUAL" && r.status == "MATCH_RESIDUAL" &&
        l.residual.size == 2 && r.residual.size == 2 do
      throwError "unexpected OR residuals"
    let a ← KuuOSR18.glueRoot #[] #[] #[] 3 left goal l #[]
    let b ← KuuOSR18.glueRoot #[] #[] #[] 3 right goal r a.entries
    let h ← KuuOSR18.walk #[] #[] #[] 3 #[] unknown #[]
    let p : Array (String × Array Name) := #[("True", #[TICKKuuOSR31Fixture.truth])]
    let f ← KuuOSR18.walk p #[] #[] 3 #[] (mkConst TICKTrue) #[]
    pure (Json.mkObj [
      ("left", KuuOSR18.resultJson a), ("right", KuuOSR18.resultJson b),
      ("unknown", KuuOSR18.resultJson h), ("fresh", KuuOSR18.resultJson f)])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R31_BRANCHES " ++ payload.compress)
'''.replace("TICK",tick)
    return extend(src,rows,reg)

def check_live(log,rows,reg,types):
    xs=[json.loads(l[len(portable.MARK):]) for l in log.splitlines() if l.startswith(portable.MARK)]
    if len(xs)!=1:raise ValueError("live observation")
    x=xs[0];ts={r["name"]:r["type_expr"] for r in x["types"]};goals={r["case"]:r["expr"] for r in x["targets"]}
    if (len(ts)!=len(x["types"]) or ts!=types or
        {k:portable.hash_type(v) for k,v in ts.items()}!={c["name"]:c["type_sha256"] for c in reg["candidates"]} or
        len(goals)!=len(x["targets"]) or goals!={r["alias"]:r["target_expr"] for r in rows.values()}):
        raise ValueError("live target/source drift")

def hits(trace,rows):
    result=[]
    for t in trace:
        if t.get("status") not in (POS,NEG):continue
        r=rows[t["record_key"]];cs=r["matches"]
        if (t["goal_expr"]!=r["target_expr"] or t["candidate_comparison_searches"]!=0 or not cs or
            t["matches"]!=[c["name"] for c in cs] or t["rule"]!=cs[0]["name"] or
            cs[0]["polarity"]!=("positive" if t["status"]==POS else "negative")):
            raise ValueError("exact recall provenance")
        result.append(t)
    return result

def fixture_proofs(rows,branch):
    a,b,c,d=map(typed.term,fixture_terms(rows))
    l=case(rows,"local_refined_context")[1]["matches"]
    g=case(rows,"global_identity_context")[1]["matches"]
    n=case(rows,"blocked_pair")[1]["matches"]
    if len(l)!=1 or len(g)!=2 or len(n)!=1:raise ValueError("fixture witness set")
    p=l[0]["name"];neg=n[0]["name"]
    expected=[{"rule":"KuuOSR31Fixture.rightRule","arity":2},{"rule":p,"arity":0},{"rule":g[0]["name"],"arity":0}]
    if branch["right"]["route"]!=expected:raise ValueError("selected fixture route")
    body=RULES+"\nnamespace KuuOSR31Proof\nset_option autoImplicit false\n"
    refs={"KuuOSR31Fixture.rightRule":["Or.inr"],"KuuOSR31Fixture.truth":["True.intro"]}
    for i,x in enumerate(g):
        q=x["name"];name="alternate"+str(i)
        body+="theorem "+name+" : ("+a+" ∧ "+b+") ∨ ("+c+" ∧ "+d+") := @KuuOSR31Fixture.rightRule ("+a+") ("+b+") ("+c+") ("+d+") (@"+p+") (@"+q+")\n"
        refs["KuuOSR31Proof."+name]=["KuuOSR31Fixture.rightRule",p,q]
    body+="theorem blockedBranch : Not ("+a+" ∧ "+b+") := fun h => (@"+neg+") h.1\n"
    refs["KuuOSR31Proof.blockedBranch"]=[neg]
    body+="theorem freshProof : True := KuuOSR31Fixture.truth\nend KuuOSR31Proof\n"
    refs["KuuOSR31Proof.freshProof"]=["KuuOSR31Fixture.truth"]
    return body,refs
