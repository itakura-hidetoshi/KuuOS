"""R33: append context-bound recall records from independently admitted R32.
Preserve the R28/R30/R31 ledger; only admit observed closed theorem sources.
A context hit selects candidates for fresh Lean application, never authority.
The exact goal AND seven elaborated context arguments must match. A miss
does not refute a goal and must not suppress future indexed search."""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_contextual_root_recall_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
root=prev.root
ext=prev.ext
portable=prev.portable
VIEW=prev.VIEW
CURRENT=base.prev.CURRENT
CURRENT_TREE=base.prev.CURRENT_TREE
DIRECT="4d128b5e4ef1d31923e154bf812afe88fee1b7cd1a5a00d6676c1864189797c7"
MCP="e118db3743d2c78af4db5cc276f34fc54e0883db2cf81df5e0710aa20d96757a"
MARK="KUUOS_R33_CONTEXT "
POSITIVE={"EXACT_ROOT_POSITIVE_CANDIDATES","INDEXED_POSITIVE_CANDIDATE"}
NEGATIVE={"EXACT_ROOT_NEGATIVE_CANDIDATE","INDEXED_NEGATIVE_CANDIDATE"}

def projection(d,mp,ind,reg,rows,bridge):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        d["source_head"]!=CURRENT or d["source_tree"]!=CURRENT_TREE or d["scope_digest"]!=old.SCOPE or
        d["ledger_view_digest"]!=VIEW or old.digest(rows)!=VIEW or d["transport_key"]!=bridge["key"]):
        raise ValueError("R32 source/receipt")
    hist={r["name"]:r for r in d["fresh_application"]["observations"]}
    audits={r["name"]:r["axioms"] for r in mp["audits"]}
    if len(hist)!=17 or len(audits)!=17 or set(hist)!=set(audits) or any(
        hist[n]["axioms"]!=audits[n] or set(audits[n])-typed.STANDARD or
        portable.hash_type(hist[n]["type_expr_repr"])!=hist[n]["type_expr_sha256"] for n in hist):
        raise ValueError("R32 complete audit")
    cs={c["name"]:dict(c) for c in reg["candidates"]}
    if len(cs)!=8:raise ValueError("prior registry")
    for n,c in cs.items():
        if hist[n]["type_expr_sha256"]!=c["type_sha256"] or hist[n]["axioms"]!=c["axioms"]:
            raise ValueError("prior source drift")
    records={};held={};used=set();new=[]
    for k,z in sorted(d["requests"].items()):
        q=z["request"];ctx=z["admitted_context"];root.validate(q)
        obs=d["results"][k];decision=d["decisions"][k]
        binding=old.digest({"request":q,"admitted_context":ctx,"current_head":CURRENT,
                            "transport_key":bridge["key"],"ledger_view":VIEW})
        if d["request_bindings"][k]!=binding:raise ValueError("R32 request binding")
        apps=[(n,a) for n,a in d["applications"].items() if a["case"]==k]
        if decision["status"]=="HOLD_CONTEXT_MISMATCH":
            if obs["search_executed"] or obs["result"] is not None or apps or decision["routes"]:
                raise ValueError("invalid context HOLD")
            held[k]={"request":q,"historical_binding":binding,"observation_digest":old.digest(obs),
                     "status":"HOLD_CONTEXT_MISMATCH","proof_authority":False}
            continue
        pol="positive" if decision["status"] in POSITIVE else "negative" if decision["status"] in NEGATIVE else None
        if (pol is None or not obs["search_executed"] or not obs["target_aligned"] or not obs["context_aligned"] or
            obs["goal_expr"]!=obs["context_goal_expr"] or q["context_args"]!=ctx or
            q["target"]!=prev.context_target(q)):
            raise ValueError("unbound admitted context")
        matches=[]
        for route in decision["routes"]:
            if len(route)!=1 or route[0]["arity"]!=0:raise ValueError("nonclosed root")
            n=route[0]["rule"];ls=[(w,a) for w,a in apps if a["request"]["source"]==n]
            if len(ls)!=1:raise ValueError("missing historical witness")
            w,a=ls[0];req=a["request"];typed.validate(req)
            _,wn=typed.names(req)
            if (w!=wn or req["polarity"]!=pol or req["target"]!=q["target"] or req["arguments"] or
                a["current_binding"]!=binding or a["expected_target_expr"]!=obs["goal_expr"] or
                a["application"]["exact_kernel_type_match"] is not True or
                a["application"]["target_expr_repr"]!=obs["goal_expr"] or
                a["application"]["witness_type_repr"]!=hist[w]["type_expr_repr"] or
                n not in hist[w]["proof_constants"] or not set(hist[w]["axioms"])<=set(hist[n]["axioms"])):
                raise ValueError("historical proof binding")
            if n not in cs:
                cs[n]={"module":req["module"],"name":n,"polarity":pol,
                       "type_sha256":hist[n]["type_expr_sha256"],"axioms":hist[n]["axioms"],
                       "observation_digest":old.digest(hist[n])}
                new.append(n)
            c=cs[n]
            if c["module"]!=req["module"] or c["polarity"]!=pol:raise ValueError("source identity")
            matches.append({"candidate":c,"historical_witness":w,"witness_digest":old.digest(hist[w]),
                            "application_digest":old.digest(a)})
            used.add(w)
        if len(matches)!=len(apps) or not matches:raise ValueError("application inventory")
        key=old.digest({"target_expr":obs["goal_expr"],"context_args":ctx,
                        "context_modules":q["context_modules"],"mode":q["mode"]})
        if key in records:raise ValueError("duplicate context")
        records[key]={"case":k,"request":q,"target_expr":obs["goal_expr"],"context_args":ctx,
                      "context_key":key,"historical_binding":binding,"matches":matches,"proof_authority":False}
    if (len(records)!=5 or len(held)!=2 or len(used)!=6 or used!=set(d["applications"]) or
        len(cs)!=10 or len(new)!=2 or set(new)!={prev.LEC+"nativeF55_constant_twoChart_overlapFiberFaithful",
                                               prev.LEC+"nativeF55_twoChart_not_overlapFiberFaithful"}):
        raise ValueError("context extension inventory")
    registry={"candidates":[cs[n] for n in sorted(cs)]}
    return portable.seal({"schema":"kuuos.codeai.contextual-memory-extension.v1",
        "source_head":CURRENT,"source_tree":CURRENT_TREE,"scope_digest":old.SCOPE,
        "lean":portable.LEAN,"mathlib":portable.MATHLIB,"parent_ledger_view":VIEW,
        "transport_key":bridge["key"],"r32_direct_digest":DIRECT,"r32_mcp_digest":MCP,
        "records":records,"historical_holds":held,"new_candidate_names":sorted(new),
        "registry":registry,"semantic_search_complete":False,"proof_authority":False})

def requests(d):
    qs={}
    for k,z in sorted(d["requests"].items()):
        q=z["request"]
        qs[k]=root.make_request("r33_"+k,q["target"],q["context_args"],q["context_modules"])
    a=qs["faithful_original"]["context_args"]
    target=prev.ap(prev.LEC+"Compatible",a[0],a[1],a[2],a[4],a[6])
    qs["new_original_compat"]=root.make_request("r33_new_original_compat",target,a,qs["faithful_original"]["context_modules"])
    return qs

def render(qs,memory):
    # Re-elaborate both stored and fresh expressions in ONE imported Lean
    # environment, not by decoding untrusted serialized Expr or text.
    tick=chr(96)*2
    records=sorted(memory["records"].items())
    fresh=sorted(qs.items())
    targets={"q"+str(i):q["target"] for i,(_,q) in enumerate(fresh)}
    targets.update({"r"+str(i):r["request"]["target"] for i,(_,r) in enumerate(records)})
    targets.update({"e"+str(i):prev.context_target(q) for i,(_,q) in enumerate(fresh)})
    src=portable.render(targets,memory["registry"])
    mods=sorted({m for _,q in fresh for m in q["context_modules"]}|
                {m for _,r in records for m in r["request"]["context_modules"]})
    src="".join("import "+typed.name(m)+"\n" for m in mods if "import "+m+"\n" not in src)+src
    src+="\nnamespace KuuOSR33Context\nset_option autoImplicit false\n"
    for prefix,seq in (("q",[(k,q["context_args"]) for k,q in fresh]),
                       ("r",[(k,r["context_args"]) for k,r in records])):
        for i,(_,args) in enumerate(seq):
            for j,a in enumerate(args):
                src+="noncomputable def "+prefix+str(i)+"_"+str(j)+" := "+typed.term(a)+"\n"
    src+="end KuuOSR33Context\nopen Lean\nrun_cmd do\n  let env ← getEnv\n"
    def goal(alias):return tick+"KuuOSR28Probe."+alias
    def args(alias):return "#["+ ", ".join(tick+"KuuOSR33Context."+alias+"_"+str(j) for j in range(7))+"]"
    fresh_entries=", ".join("("+json.dumps(k)+", "+goal("q"+str(i))+", "+goal("e"+str(i))+", "+args("q"+str(i))+")" for i,(k,q) in enumerate(fresh))
    record_entries=", ".join("("+json.dumps(k)+", "+goal("r"+str(i))+", "+args("r"+str(i))+")" for i,(k,r) in enumerate(records))
    src+="  let queries : Array (String × Name × Name × Array Name) := #["+fresh_entries+"]\n"
    src+="  let records : Array (String × Name × Array Name) := #["+record_entries+"]\n"
    src+=r'''
  let mut result : Array Json := #[]
  for (label, qn, en, qa) in queries do
    let some qi := env.find? qn | throwError "missing fresh target"
    let some q := qi.value? (allowOpaque := true) | throwError "missing fresh body"
    let some ei := env.find? en | throwError "missing reconstructed target"
    let some e := ei.value? (allowOpaque := true) | throwError "missing reconstructed body"
    let mut qvals : Array Expr := #[]
    for n in qa do
      let some ci := env.find? n | throwError "missing query context"
      let some val := ci.value? (allowOpaque := true) | throwError "missing context body"
      if val.hasMVar || val.hasFVar || val.hasLooseBVars || val.hasLevelMVar then
        throwError "open query context"
      qvals := qvals.push val
    let mut targetMatches : Array String := #[]
    let mut contextMatches : Array String := #[]
    for (key, rn, ra) in records do
      let some ri := env.find? rn | throwError "missing record target"
      let some r := ri.value? (allowOpaque := true) | throwError "missing record body"
      let mut same := qa.size == ra.size
      for j in [:ra.size] do
        let some ai := env.find? ra[j]! | throwError "missing record context"
        let some av := ai.value? (allowOpaque := true) | throwError "missing record context body"
        if av.hasMVar || av.hasFVar || av.hasLooseBVars || av.hasLevelMVar then
          throwError "open record context"
        unless qvals[j]!.equal av do
          same := false
      if q.equal r then
        targetMatches := targetMatches.push key
        if same then
          contextMatches := contextMatches.push key
    result := result.push (Json.mkObj [
      ("case", toJson label), ("goal_expr", toJson (reprStr q)),
      ("context_goal_expr", toJson (reprStr e)), ("target_aligned", toJson (q.equal e)),
      ("target_matches", toJson targetMatches), ("context_matches", toJson contextMatches),
      ("context_exprs", toJson (qvals.map reprStr))])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R33_CONTEXT " ++ (toJson result).compress)
'''
    return src

def decide(mem,trusted,q,obs,live,expected,head):
    if mem.get("key")!=portable.seal(mem)["key"]:return {"status":"HOLD_MEMORY_INTEGRITY","matches":[]}
    if mem!=trusted:return {"status":"HOLD_UNADMITTED_MEMORY","matches":[]}
    if head!=CURRENT or mem["source_head"]!=head or mem["source_tree"]!=CURRENT_TREE or mem["scope_digest"]!=old.SCOPE:
        return {"status":"HOLD_CURRENT_SCOPE","matches":[]}
    if live!=expected:return {"status":"HOLD_SOURCE_TYPE_DRIFT","matches":[]}
    root.validate(q)
    ts=sorted(k for k,r in mem["records"].items() if r["target_expr"]==obs["goal_expr"])
    if sorted(obs["target_matches"])!=ts or len(obs["context_exprs"])!=7:
        raise ValueError("target observation drift")
    if not obs["target_aligned"] or obs["goal_expr"]!=obs["context_goal_expr"]:
        return {"status":"HOLD_CONTEXT_MISMATCH","matches":[]}
    matches=[]
    for k in obs["context_matches"]:
        r=mem["records"][k]
        if k not in ts:raise ValueError("context matched wrong target")
        if r["request"]["context_modules"]==q["context_modules"] and r["request"]["mode"]==q["mode"]:
            matches.append(k)
    if len(matches)>1:return {"status":"HOLD_AMBIGUOUS_CONTEXT","matches":[]}
    if not matches:return {"status":"HOLD_CONTEXT_MISMATCH" if ts else "HOLD_SEARCH_REQUIRED","matches":[]}
    k=matches[0]
    return {"status":"EXACT_CONTEXT_APPLICATION_REQUIRED","context_key":k,
            "matches":[x["candidate"] for x in mem["records"][k]["matches"]],"candidate_comparison_searches":0,
            "proof_authority":False}
