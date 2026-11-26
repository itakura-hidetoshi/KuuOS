"""R29: admit R28's historical evidence across an observed identical proof
scope, without changing the historical receipts. Recall exact closed Exprs
inside the existing R27/R20 recursive search; only live Lean proofs certify.
An admitted no-match skips the old five-candidate comparison, NOT other
indexed rules. No external generation, merge or execution authority."""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_portable_exact_recall_v1 as portable
from runtime import kuuos_codeai_olean_multi_typed_recall_v1_r2 as multi
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
root=multi.root
CURRENT="a316e66f8a3a3f8dca2ae5177e4f04e7cc1dd063"
CURRENT_TREE="c6686a052dd0b26728e1d784520db5d07f965784"
R28_DIRECT="8a7a2b551642cf22050defb202e4928e4716a8d61d194066a46478d9fe5a466e"
R28_MCP="6a30a84ee4316548c972ed0aa18887c0791b179b9de55bb563e22649766c9bfc"
R28_MEMORY="bff98533e4163be2961bede75782204d3822e3e2275f049bdd953e150f28c339"
POS="PORTABLE_EXACT_LEAF_CANDIDATE"
NEG="HOLD_PORTABLE_EXACT_NEGATIVE"
MISS="HOLD_PORTABLE_NO_MATCH_CONTINUE"

def transport(scope,mem,reg):
    # The host must observe both complete scopes and canonical ancestry
    # with the unmodified canonical verifier before constructing scope.
    if (scope["historical_head"],scope["historical_tree"],scope["current_head"],
        scope["current_tree"],scope["scope_digest"])!=(old.HEAD,old.TREE,CURRENT,CURRENT_TREE,old.SCOPE):
        raise ValueError("scope transport mismatch")
    if scope["historical_scope"]!=scope["current_scope"] or old.digest(scope["current_scope"])!=old.SCOPE:
        raise ValueError("proof inputs changed")
    if mem["key"]!=R28_MEMORY or portable.validate(mem,mem,reg)!="EXACT_OBSERVATION_REQUIRED":
        raise ValueError("historical memory mismatch")
    return portable.seal({"schema":"kuuos.codeai.portable-recursive-transport.v1",
        "scope":scope,"historical_memory_key":mem["key"],"registry_key":reg["key"],
        "r28_direct_digest":R28_DIRECT,"r28_mcp_digest":R28_MCP,
        "proof_authority":False,"semantic_search_complete":False})

def preflight(bridge,trusted_bridge,mem,trusted_mem,reg,head):
    if bridge.get("key")!=portable.seal(bridge)["key"]:return "HOLD_TRANSPORT_INTEGRITY"
    if head!=CURRENT or bridge["scope"]["current_head"]!=head:return "HOLD_CURRENT_HEAD"
    if bridge!=trusted_bridge:return "HOLD_UNADMITTED_TRANSPORT"
    if bridge["historical_memory_key"]!=mem["key"] or bridge["registry_key"]!=reg["key"]:
        return "HOLD_TRANSPORT_BINDING"
    return portable.validate(mem,trusted_mem,reg)

def targets(mem):
    return {r["case"]:r["target"] for r in mem["records"].values()}

def base_fixture(mem):
    rows={x["case"]:x for x in mem["records"].values()}
    qs={a:{"target":rows[b]["target"]} for a,b in
        (("exact_new","capsule_exact"),("defeq_new","capsule_defeq"),
         ("negative_defeq","refined_negative"),("wrong_atlas","unknown"))}
    return qs,{"candidates":[rows["capsule_exact"]["candidate"],rows["refined_negative"]["candidate"]]}

def helpers(mem,reg):
    # Each named target below is re-elaborated by portable.render in this
    # SAME file. The host checks its complete Expr and all live source types
    # against the admitted historical receipt before admitting any route.
    # Matching is Lean Expr.equal, not a hash or a pretty-printer comparison.
    s=multi.helpers(reg);tick=chr(96)*2;xs=[]
    for key,row in sorted(mem["records"].items()):
        if not typed.CASE.fullmatch(row["case"]) or key!=row["target_key"]:
            raise ValueError("memory case identity")
        n=tick+"KuuOSR28Probe."+row["case"]
        if row["status"]=="EXACT_APPLICATION_REQUIRED":
            c=row["candidate"];rule=tick+typed.name(c["name"]);pol=c["polarity"]
        elif row["status"]=="HOLD_HISTORICAL_NO_MATCH":
            rule="Name.anonymous";pol="miss"
        else:raise ValueError("unknown memory status")
        xs.append("("+n+", "+rule+", "+json.dumps(pol)+", "+json.dumps(key)+")")
    hook=r'''
  let mut portableMiss := false
  let mut portableMissKey := ""
  if KuuOSR16.closed goal && !goal.hasLevelMVar then
    let memoryRows : Array (Name × Name × String × String) := #[MEMORY_ROWS]
    for (targetName, ruleName, polarity, recordKey) in memoryRows do
      let info ← getConstInfo targetName
      let some body := info.value? (allowOpaque := true) |
        throwError "missing portable goal"
      if body.equal goal then
        if polarity == "miss" then
          portableMiss := true
          portableMissKey := recordKey
        else
          let event := Json.mkObj [
            ("status", toJson (if polarity == "positive" then "PORTABLE_EXACT_LEAF_CANDIDATE" else "HOLD_PORTABLE_EXACT_NEGATIVE")),
            ("goal_expr", toJson (reprStr goal)), ("rule", toJson ruleName.toString),
            ("record_key", toJson recordKey), ("candidate_comparison_searches", toJson (0 : Nat))]
          if polarity == "positive" then
            return ⟨some [(ruleName, 0)], entries, #[event], 0⟩
          if polarity == "negative" then
            return ⟨none, entries, #[event], 0⟩
          throwError "invalid portable polarity"
'''.replace("MEMORY_ROWS",", ".join(xs))
    marker="  let mut recallCache := entries"
    guard="  if KuuOSR16.closed goal && !goal.hasLevelMVar then"
    trace='    let negTrace := (#[KuuOSR17.holdRow "HOLD_NO_TYPED_MATCH_CONTINUE" goal] : Array Json) ++ negTrace'
    if s.count(marker)!=1 or s.count(guard)!=1 or s.count(trace)!=1:
        raise ValueError("R27 helper boundary")
    s=s.replace(guard,"  if !portableMiss && KuuOSR16.closed goal && !goal.hasLevelMVar then",1)
    s=s.replace(marker,hook+marker,1)
    s=s.replace(trace,r'''    let recallTrace := if portableMiss then
      Json.mkObj [("status", toJson "HOLD_PORTABLE_NO_MATCH_CONTINUE"),
        ("goal_expr", toJson (reprStr goal)), ("record_key", toJson portableMissKey),
        ("candidate_comparison_searches", toJson (0 : Nat))]
      else KuuOSR17.holdRow "HOLD_NO_TYPED_MATCH_CONTINUE" goal
    let negTrace := (#[recallTrace] : Array Json) ++ negTrace''',1)
    return s

def extend(src,mem,reg):
    marker=multi.helpers(reg)
    if src.count(marker)!=1:raise ValueError("search helper boundary")
    src=src.replace(marker,helpers(mem,reg),1)
    pre=portable.render(targets(mem),reg)
    # Keep every import at the start; the portable goals are defined before
    # the recursive helper, not decoded from arbitrary serialized Exprs.
    texts=[pre,src]
    imports=sorted({l for text in texts for l in text.splitlines() if l.startswith("import ")})
    bodies=["\n".join(l for l in text.splitlines() if not l.startswith("import ")) for text in texts]
    return "\n".join(imports)+"\n\n"+"\n\n".join(bodies)+"\n"

def render(q,inv,mem,reg):
    return extend(multi.render(q,inv,reg),mem,reg)

def probe(mem,reg):
    ts=targets(mem)
    ts["new_target"]={"const":"True"}
    return extend(multi.probe(ts,reg),mem,reg)

def fixture(mem,reg):
    qs,base=base_fixture(mem)
    return extend(multi.fixture(qs,base,reg),mem,reg)

def check_live(log,mem,reg,historical_types):
    rows=[json.loads(l[len(portable.MARK):]) for l in log.splitlines() if l.startswith(portable.MARK)]
    if len(rows)!=1:raise ValueError("live exact observation")
    x=rows[0]
    types={r["name"]:r["type_expr"] for r in x["types"]}
    goals={r["case"]:r["expr"] for r in x["targets"]}
    if (len(x["types"])!=len(types) or types!=historical_types or
        {k:portable.hash_type(v) for k,v in types.items()}!={c["name"]:c["type_sha256"] for c in reg["candidates"]} or
        len(x["targets"])!=len(goals) or goals!={r["case"]:r["target_expr"] for r in mem["records"].values()}):
        raise ValueError("live source type or portable goal drift")
    return x

def trace_memory(trace,mem):
    hits=[]
    for t in trace:
        status=t.get("status")
        if status not in (POS,NEG,MISS):continue
        row=mem["records"][t["record_key"]]
        c=row["candidate"]
        if (t["goal_expr"]!=row["target_expr"] or t["candidate_comparison_searches"]!=0 or
            (status==MISS and c is not None) or
            (status!=MISS and (c is None or c["name"]!=t["rule"] or
                              c["polarity"]!=("positive" if status==POS else "negative")))):
            raise ValueError("portable trace lineage")
        hits.append(t)
    return hits
