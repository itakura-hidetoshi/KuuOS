"""R28: transport exact closed-target recall observations across runs.
Only independently admitted R27 receipts can seed the memory. A memory
hit selects a candidate for fresh Lean application, never proof authority.
Misses and historical no-match remain HOLD. No persisted metavariables."""
from __future__ import annotations
import hashlib
import json
from runtime import kuuos_codeai_olean_multi_typed_recall_v1_r2 as prior
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

MARK="KUUOS_R28_OBSERVATION "
LEAN="v4.30.0-rc2"
MATHLIB="5450b53e5ddc75d46418fabb605edbf36bd0beb6"

def hash_type(s):
    return hashlib.sha256(s.encode()).hexdigest()

def seal(x):
    return {**{k:v for k,v in x.items() if k!="key"},"key":old.digest({k:v for k,v in x.items() if k!="key"})}

def memory(d,mp,ind,targets):
    # Caller must first authenticate the upstream workflow, job and artifacts.
    reg=d["registry"]
    if (prior.valid(reg)!="TYPE_COMPARISON_REQUIRED" or d["inventory_key"]!=reg["key"] or
        old.digest(d)!=ind["direct_digest"] or old.digest(mp)!=ind["mcp_digest"] or
        mp["direct_digest"]!=ind["direct_digest"] or ind["inventory_key"]!=reg["key"]):
        raise ValueError("unadmitted registry receipt")
    if set(targets)!=set(d["multi_recall"]):raise ValueError("historical target inventory")
    obs={r["name"]:r for r in d["fresh_application"]["observations"]}
    audits={r["name"]:r["axioms"] for r in mp["audits"]}
    if len(obs)!=len(d["fresh_application"]["observations"]) or set(obs)!=set(audits):
        raise ValueError("source audit inventory")
    if any(r["axioms"]!=audits[n] or set(r["axioms"])-typed.STANDARD or
           hash_type(r["type_expr_repr"])!=r["type_expr_sha256"] for n,r in obs.items()):
        raise ValueError("source audit mismatch")
    candidates={x["name"]:x for x in reg["candidates"]}
    records={}
    for k,x in sorted(d["multi_recall"].items()):
        a,b=x["first"],x["replay"]
        if (a["route"]!=b["route"] or a["cache_entries"]!=b["cache_entries"] or
            b["cache_hits"]<len(candidates)):
            raise ValueError("historical replay mismatch")
        t=a["trace"][0];u=b["trace"][0]
        expr=t["goal_expr"];key=hash_type(expr)
        if key in records or u["goal_expr"]!=expr or u["status"]!=t["status"]:
            raise ValueError("historical goal binding")
        row={"case":k,"target":targets[k],"target_expr":expr,"target_key":key,
             "prior_observation_digest":old.digest(x),"proof_authority":False}
        if t["status"] in ("CAPSULE_EXACT_LEAF_CANDIDATE","HOLD_ROUTE_EXACT_NEGATIVE"):
            pol="positive" if t["status"]=="CAPSULE_EXACT_LEAF_CANDIDATE" else "negative"
            c=candidates[t["rule"]];w=obs[typed.NS+".r27_"+k+".witness"];s=obs[c["name"]]
            if (t["matches"]!=u["matches"] or c["name"] not in t["matches"] or c["polarity"]!=pol or
                s["type_expr_sha256"]!=c["type_sha256"] or s["axioms"]!=c["axioms"] or
                c["name"] not in w["proof_constants"] or not set(w["axioms"])<=set(s["axioms"])):
                raise ValueError("historical witness/source binding")
            if pol=="positive" and a["route"]!=[{"rule":c["name"],"arity":0}]:raise ValueError("positive route")
            if pol=="negative" and a["route"] is not None:raise ValueError("negative route")
            row.update(status="EXACT_APPLICATION_REQUIRED",candidate=c,matches=t["matches"],
                       prior_witness_digest=old.digest(w))
        elif t["status"]=="HOLD_NO_TYPED_MATCH_CONTINUE" and a["route"] is None:
            row.update(status="HOLD_HISTORICAL_NO_MATCH",candidate=None,matches=[])
        else:raise ValueError("unsupported historical outcome")
        records[key]=row
    return seal({"schema":"kuuos.codeai.portable-exact-recall.v1","source_head":old.HEAD,"source_tree":old.TREE,
                 "scope_digest":old.SCOPE,"lean":LEAN,"mathlib":MATHLIB,"inventory_key":reg["key"],
                 "direct_digest":ind["direct_digest"],"mcp_digest":ind["mcp_digest"],"records":records,
                 "semantic_search_complete":False,"proof_authority":False})

def validate(mem,trusted,registry):
    if mem.get("key")!=seal(mem)["key"]:return "HOLD_MEMORY_INTEGRITY"
    if (mem["source_head"],mem["source_tree"],mem["scope_digest"],mem["lean"],mem["mathlib"])!=(old.HEAD,old.TREE,old.SCOPE,LEAN,MATHLIB):
        return "HOLD_SCOPE"
    if prior.valid(registry)!="TYPE_COMPARISON_REQUIRED" or mem["inventory_key"]!=registry["key"]:
        return "HOLD_INVENTORY_INTEGRITY"
    # Self-consistent hashes alone do not authorize a changed memory.
    if mem!=trusted:return "HOLD_UNADMITTED_MEMORY"
    return "EXACT_OBSERVATION_REQUIRED"

def decide(mem,trusted,registry,expr,live_types):
    status=validate(mem,trusted,registry)
    if status!="EXACT_OBSERVATION_REQUIRED":return {"status":status,"proof_authority":False}
    if live_types!={c["name"]:c["type_sha256"] for c in registry["candidates"]}:
        return {"status":"HOLD_SOURCE_TYPE_DRIFT","proof_authority":False}
    row=mem["records"].get(hash_type(expr))
    if row is None or row["target_expr"]!=expr:
        return {"status":"HOLD_SEARCH_REQUIRED","proof_authority":False}
    return {"status":row["status"],"record_key":row["target_key"],"candidate":row["candidate"],
            "proof_authority":False}

def render(targets,registry):
    """Observe current elaborated expression and live source types only.
    No isDefEq candidate comparison, no recursive search, no proof selection."""
    mods=sorted({typed.name(c["module"]) for c in registry["candidates"]})
    out=["import "+m for m in mods]+["","namespace KuuOSR28Probe","set_option autoImplicit false"]
    for k,t in sorted(targets.items()):
        if not typed.CASE.fullmatch(k):raise ValueError("case identity")
        out+=["def "+k+" : Prop := "+typed.term(t)]
    out+=["end KuuOSR28Probe","open Lean","run_cmd do","  let env ← getEnv"]
    tick=chr(96)*2
    pairs=", ".join("("+json.dumps(c["module"])+", "+tick+typed.name(c["name"])+")" for c in registry["candidates"])
    out+=["  let candidates : Array (String × Name) := #["+pairs+"]",
          "  let mut types : Array Json := #[]",
          "  for (m,n) in candidates do",
          '    let some info := env.find? n | throwError "missing source"',
          '    let some idx := env.getModuleIdxFor? n | throwError "missing origin"',
          "    unless info.isTheorem && info.levelParams.isEmpty && env.allImportedModuleNames[idx]!.toString == m do",
          '      throwError "source origin changed"',
          '    if info.type.hasMVar || info.type.hasFVar || info.type.hasLooseBVars || info.type.hasLevelMVar then throwError "open source type"',
          '    types := types.push (Json.mkObj [("name", toJson n.toString), ("type_expr", toJson (reprStr info.type))])',
          "  let mut targets : Array Json := #[]"]
    for i,k in enumerate(sorted(targets)):
        out+=["  let some t"+str(i)+" := env.find? "+tick+"KuuOSR28Probe."+k+' | throwError "missing target"',
              "  let some e"+str(i)+" := t"+str(i)+'.value? (allowOpaque := true) | throwError "missing target body"',
              "  if e"+str(i)+".hasMVar || e"+str(i)+".hasFVar || e"+str(i)+'.hasLooseBVars || e'+str(i)+'.hasLevelMVar then throwError "open target"',
              '  targets := targets.push (Json.mkObj [("case", toJson "'+k+'"), ("expr", toJson (reprStr e'+str(i)+'))])']
    out+=['  let payload := Json.mkObj [("types", toJson types), ("targets", toJson targets)]',
          '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    return "\n".join(out)
