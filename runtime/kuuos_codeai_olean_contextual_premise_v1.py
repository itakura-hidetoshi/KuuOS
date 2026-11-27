"""R36: one-step typed premise discovery from the current contextual ledger.
Only a genuine, aligned memory miss may enter the bounded selected index.
Both direct and one-residual routes are kept. A residual is matched against
a stored proposition AND all seven elaborated context arguments. A negative
witness cannot discharge a positive premise. No arbitrary new theorem or
provider call is authorized. The caller must authenticate R35 evidence.
"""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_contextual_extension_v2 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

cm=prev.cm
root=prev.root
portable=prev.portable
base=prev.base
ext=prev.ext
CURRENT=prev.CURRENT
CURRENT_TREE=prev.CURRENT_TREE
DIRECT="c7b068e1d2ce4be52c842c8bb710c1bd3ea2dbac7980b90771064899f000730b"
MCP="5882f402982c45ec939ea01fe46ac3cd9491e18251228557a4c45a53ae3ac566"
VIEW="fdc7a11922ad285f1e6dadd3897b643557ded2e7a54b16c4895bdb2d13dfa76c"
LAYER="a5ce2ed8cae5b9bfd6ecbf3c59a838d5aad99fce6ce0c08cd7de72d2cec7cf82"
MARK="KUUOS_R36_PREMISES "
LEC=cm.prev.LEC

def requests(d):
    return {k:root.make_request("r36_"+k,q["target"],q["context_args"],q["context_modules"])
            for k,q in sorted(d["requests"].items())}

def plan(q,view,inv):
    root.validate(q)
    if view["key"]!=VIEW or portable.seal(view)["key"]!=VIEW:
        raise ValueError("unadmitted view")
    if q["target"]!=cm.prev.context_target(q):raise ValueError("unaligned target")
    h=q["target"]["apply"][0]["const"]
    if h not in inv["selected"]:raise ValueError("unranked head")
    candidates={}
    # All 12 remembered sources remain eligible as theorem candidates.
    for c in view["registry"]["candidates"]:
        candidates[c["name"]]={**c,"origin":"context_registry"}
    for head,pol in ((h,"positive"),("Not","negative")):
        for c in inv["selected"][head]:
            if pol=="negative" and h not in c["negative_head_matches"]:continue
            n=c["name"]
            if n in candidates:
                if (candidates[n]["module"],candidates[n]["polarity"])!=(c["module"],pol):
                    raise ValueError("indexed origin/polarity drift")
                continue
            candidates[n]={"name":n,"module":c["module"],"polarity":pol,
                           "origin":"bounded_index","row_digest":c["row_digest"]}
    cs=sorted(candidates.values(),key=lambda c:(c["origin"],c["module"],c["name"]))
    for c in cs:typed.name(c["module"]);typed.name(c["name"])
    return {"context_view_key":VIEW,"selected_index_digest":old.digest(inv),
            "target_head":h,"candidates":cs,"depth":1,"unobserved_module_count":len(inv["unobserved_modules"]),
            "semantic_search_complete":False,"proof_authority":False}

def render(k,q,view,p):
    src=cm.render({k:q},view)
    mods=sorted({x["module"] for x in p["candidates"]})
    src="".join("import "+m+"\n" for m in mods if "import "+m+"\n" not in src)+src
    src+="\n"+root.poly.HELPER+"\nset_option maxHeartbeats 16000000\nset_option maxRecDepth 8192\n"
    tick=chr(96)*2
    cs=", ".join("("+tick+typed.name(c["name"])+", "+json.dumps(c["module"])+", "+
                  ("true" if c["polarity"]=="negative" else "false")+")" for c in p["candidates"])
    def args(a):return "#["+ ", ".join(tick+"KuuOSR33Context."+a+"_"+str(j) for j in range(7))+"]"
    rs=[]
    for i,(key,r) in enumerate(sorted(view["records"].items())):
        if r["request"]["context_modules"]!=q["context_modules"] or r["request"]["mode"]!=q["mode"]:continue
        rs.append("("+json.dumps(key)+", "+tick+"KuuOSR28Probe.r"+str(i)+", "+args("r"+str(i))+")")
    src+="\nopen Lean Meta\nrun_cmd do\n  let env ← getEnv\n"
    src+="  let some qi := env.find? "+tick+'KuuOSR28Probe.q0 | throwError "missing target"\n'
    src+='  let some goal := qi.value? (allowOpaque := true) | throwError "missing goal body"\n'
    src+="  let some ei := env.find? "+tick+'KuuOSR28Probe.e0 | throwError "missing context target"\n'
    src+='  let some eg := ei.value? (allowOpaque := true) | throwError "missing context body"\n'
    src+='  unless goal.equal eg do throwError "unaligned target"\n'
    src+="  let queryContext : Array Name := "+args("q0")+"\n"
    src+="  let memories : Array (String × Name × Array Name) := #["+ ", ".join(rs)+"]\n"
    src+="  let candidates : Array (Name × String × Bool) := #["+cs+"]\n"
    src+=r'''
  let mut eligible : Array (String × Expr) := #[]
  for (key, tn, ctx) in memories do
    let mut same := ctx.size == queryContext.size
    for i in [:ctx.size] do
      let some a := env.find? ctx[i]! | throwError "missing stored context"
      let some b := env.find? queryContext[i]! | throwError "missing live context"
      let some av := a.value? (allowOpaque := true) | throwError "missing stored context body"
      let some bv := b.value? (allowOpaque := true) | throwError "missing live context body"
      unless av.equal bv do
        same := false
    if same then
      let some t := env.find? tn | throwError "missing premise target"
      let some body := t.value? (allowOpaque := true) | throwError "missing premise body"
      unless KuuOSR16.closed body && !body.hasLevelMVar do throwError "open remembered premise"
      eligible := eligible.push (key, body)
  let payload ← Lean.Elab.Command.liftTermElabM do
    let mut trials : Array Json := #[]
    for (n,m,neg) in candidates do
      let some info := env.find? n | throwError "missing indexed source"
      let some idx := env.getModuleIdxFor? n | throwError "missing source origin"
      unless info.isTheorem && env.allImportedModuleNames[idx]!.toString == m do
        throwError "indexed source identity"
      let target := if neg then mkApp (mkConst NOTCONST) goal else goal
      let t ← KuuOSR16.safeSpecialize n target
      let mut matchedKeys : Array String := #[]
      if t.status == "MATCH_RESIDUAL" && t.residual.size == 1 then
        let p := t.residual[0]!
        if KuuOSR16.closed p && !p.hasLevelMVar then
          for (key, body) in eligible do
            if p.equal body then
              matchedKeys := matchedKeys.push key
      trials := trials.push (Json.mkObj [
        ("name", toJson n.toString), ("module", toJson m),
        ("polarity", toJson (if neg then "negative" else "positive")),
        ("type_expr", toJson (reprStr info.type)),
        ("trial", KuuOSR16.trialJson n t), ("premise_matches", toJson matchedKeys)])
    pure (Json.mkObj [("goal_expr", toJson (reprStr goal)),
      ("eligible_context_keys", toJson (eligible.map Prod.fst)), ("trials", toJson trials)])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R36_PREMISES " ++ payload.compress)
'''.replace("NOTCONST",tick+"Not")
    return src

def decide(p,obs,view,q,goal,live):
    if obs["goal_expr"]!=goal:raise ValueError("search goal drift")
    cs={c["name"]:c for c in p["candidates"]}
    ts=obs["trials"]
    if len(ts)!=len(cs) or {t["name"] for t in ts}!=set(cs):
        raise ValueError("search inventory")
    eligible=obs["eligible_context_keys"]
    if len(set(eligible))!=len(eligible) or not set(eligible)<=set(view["records"]):
        raise ValueError("context inventory")
    for k in eligible:
        r=view["records"][k]
        if r["request"]["context_modules"]!=q["context_modules"] or r["request"]["mode"]!=q["mode"]:
            raise ValueError("context scope")
    routes=[];holds=[]
    for t in ts:
        c=cs[t["name"]];trial=t["trial"];keys=t["premise_matches"]
        if (t["module"],t["polarity"],trial["name"])!=(c["module"],c["polarity"],c["name"]):
            raise ValueError("trial source drift")
        if c["origin"]=="context_registry" and (t["type_expr"]!=live[c["name"]] or portable.hash_type(t["type_expr"])!=c["type_sha256"]):
            raise ValueError("remembered source drift")
        if not set(keys)<=set(eligible) or len(keys)!=len(set(keys)):
            raise ValueError("premise context drift")
        s=trial["status"];pol=c["polarity"]
        if s=="MATCH_COMPLETE":
            if trial["residuals"] or keys:raise ValueError("complete proof residual")
            routes.append({"rule":c["name"],"module":c["module"],"polarity":pol,"kind":"direct",
                           "source_type":t["type_expr"],"premise":None})
        elif s=="MATCH_RESIDUAL" and len(trial["residuals"])==1 and len(keys)==1:
            key=keys[0];r=view["records"][key]
            if r["target_expr"]!=trial["residuals"][0]:raise ValueError("premise exact expression drift")
            matches=[m["candidate"] for m in r["matches"]]
            if {m["polarity"] for m in matches}=={"positive"}:
                for m in matches:
                    routes.append({"rule":c["name"],"module":c["module"],"polarity":pol,"kind":"one_premise",
                                   "source_type":t["type_expr"],"premise":{"context_key":key,"candidate":m}})
            else:holds.append({"rule":c["name"],"reason":"HOLD_REFUTED_EXACT_PREMISE","context_key":key})
        else:
            holds.append({"rule":c["name"],"reason":s if s!="MATCH_RESIDUAL" else "HOLD_UNRESOLVED_OR_DEPTH"})
    if len({r["polarity"] for r in routes})>1:return {"status":"HOLD_CONFLICT","routes":[],"holds":holds}
    if any(t["trial"]["status"]=="HOLD_COMPARISON_FAILURE" for t in ts):
        return {"status":"HOLD_COMPARISON_FAILURE","routes":[],"holds":holds}
    return {"status":"APPLICATION_REQUIRED" if routes else "HOLD_RECURSIVE_SEARCH_REQUIRED",
            "routes":routes,"holds":holds,"candidate_trials":len(ts),"proof_authority":False}

def application(q,route,case):
    req=typed.make_request(case,route["module"],route["rule"],q["target"],[],route["polarity"])
    decl=typed.declarations(req);rendered=typed.render(req)
    ty="Not target" if route["polarity"]=="negative" else "target"
    marker="theorem witness : "+ty+" := @"+route["rule"]
    goal=typed.term(q["target"])
    if route["polarity"]=="negative":goal="Not ("+goal+")"
    proof="theorem witness : "+ty+" := by\n  change "+goal+"\n  apply @"+typed.name(route["rule"])
    if route["premise"] is not None:
        proof+="\n  exact @"+typed.name(route["premise"]["candidate"]["name"])
    if decl.count(marker)!=1 or rendered.count(marker)!=1:raise ValueError("application boundary")
    return req,rendered.replace(marker,proof,1),decl.replace(marker,proof,1)
