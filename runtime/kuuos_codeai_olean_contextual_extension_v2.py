"""R35: append independently admitted R34 context evidence, without rewriting
the R33 parent or earlier ledgers. Derive a read-only merged view; reject
conflicting/duplicate context identities. Re-elaborate the full target and
seven context arguments in Lean before selection. No search miss is a No-Go.
"""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_contextual_fallback_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
cm=prev.prev
root=prev.root
portable=prev.portable
base=prev.base
ext=prev.ext
CURRENT=prev.CURRENT
CURRENT_TREE=prev.CURRENT_TREE
VIEW=prev.VIEW
KEY=prev.KEY
DIRECT="7e48831bd8f62bd8d10f1dba8cff8e30f924642597b773bf5c58436e56604572"
MCP="7d1e97a709f8823fcc4c9cb6a7ef826193fc676b8fc7646ab89444e1aa067c83"
NEW_CASES={"new_original_compat":("negative",prev.LEC+"nativeF55_twoChart_raw_incompatible"),
           "new_shadow_global":("positive",prev.LEC+"nativeF55_twoChart_shadow_global")}

def projection(parent,d,mp,ind):
    if (parent["key"]!=KEY or portable.seal(parent)["key"]!=KEY or
        old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        d["context_memory_key"]!=KEY or d["parent_ledger_view"]!=VIEW or
        d["source_head"]!=CURRENT or d["source_tree"]!=CURRENT_TREE or d["scope_digest"]!=old.SCOPE or
        d["transport_key"]!=parent["transport_key"] or d["fallback_requests"]!=2 or d["fallback_comparisons"]!=25):
        raise ValueError("parent scope or R34 receipt")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    audits={x["name"]:x["axioms"] for x in mp["audits"]}
    if (len(hist)!=21 or len(audits)!=21 or set(hist)!=set(audits) or
        any(hist[n]["axioms"]!=audits[n] or set(audits[n])-typed.STANDARD or
            portable.hash_type(hist[n]["type_expr_repr"])!=hist[n]["type_expr_sha256"] for n in hist)):
        raise ValueError("R34 complete audit")
    old_cs={x["name"]:x for x in parent["registry"]["candidates"]}
    if len(old_cs)!=10 or any(hist[n]["type_expr_sha256"]!=c["type_sha256"] or
                            hist[n]["axioms"]!=c["axioms"] for n,c in old_cs.items()):
        raise ValueError("old registry drift")
    if set(d["fallback_decisions"])!=set(d["plans"]) or set(d["plans"])!=set(d["fallback_traces"]) or set(d["plans"])!=set(NEW_CASES):
        raise ValueError("fallback inventory")
    records={};candidates=[];used=set()
    for k,(pol,n) in sorted(NEW_CASES.items()):
        q=d["requests"][k];root.validate(q);obs=d["observations"][k]
        if (d["decisions"][k]["status"]!="HOLD_SEARCH_REQUIRED" or not obs["target_aligned"] or
            obs["goal_expr"]!=obs["context_goal_expr"] or obs["target_matches"] or obs["context_matches"] or
            q["target"]!=cm.prev.context_target(q)):
            raise ValueError("unaligned new context")
        plan=d["plans"][k];trace=d["fallback_traces"][k];dec=d["fallback_decisions"][k]
        live={n:hist[n]["type_expr_repr"] for n in old_cs}
        if plan["context_memory_key"]!=KEY or prev.decide(plan,trace,obs["goal_expr"],live)!=dec or dec["status"]!="INDEXED_APPLICATION_REQUIRED":
            raise ValueError("fallback trace drift")
        ms=dec["matches"]
        if len(ms)!=1 or ms[0]["name"]!=n or ms[0]["polarity"]!=pol or ms[0]["origin"]!="bounded_index" or n in old_cs:
            raise ValueError("new source identity")
        s=ms[0]
        ws=[(w,a) for w,a in d["applications"].items() if a["case"]==k]
        if len(ws)!=1:raise ValueError("fallback witness inventory")
        w,a=ws[0];req=a["request"];typed.validate(req);_,wn=typed.names(req)
        expected=old.digest({"context_memory_key":KEY,"request":q,"decision":dec,"current_head":CURRENT})
        if (wn!=w or a["route_kind"]!="indexed" or a["current_binding"]!=expected or
            req["source"]!=n or req["module"]!=s["module"] or req["polarity"]!=pol or req["target"]!=q["target"] or req["arguments"] or
            a["application"]["exact_kernel_type_match"] is not True or a["application"]["target_expr_repr"]!=obs["goal_expr"] or
            a["application"]["witness_type_repr"]!=hist[w]["type_expr_repr"] or
            n not in hist[w]["proof_constants"] or not set(hist[w]["axioms"])<=set(hist[n]["axioms"]) or
            s["type_expr"]!=hist[n]["type_expr_repr"]):
            raise ValueError("indexed proof binding")
        c={"module":req["module"],"name":n,"polarity":pol,"type_sha256":hist[n]["type_expr_sha256"],
           "axioms":hist[n]["axioms"],"observation_digest":old.digest(hist[n])}
        key=old.digest({"target_expr":obs["goal_expr"],"context_args":q["context_args"],
                        "context_modules":q["context_modules"],"mode":q["mode"]})
        if key in parent["records"] or key in records or any(r["target_expr"]==obs["goal_expr"] for r in parent["records"].values()):
            raise ValueError("nonappend context record")
        records[key]={"case":k,"request":q,"target_expr":obs["goal_expr"],"context_args":q["context_args"],
                      "context_key":key,"historical_binding":expected,
                      "matches":[{"candidate":c,"historical_witness":w,"witness_digest":old.digest(hist[w]),
                                  "application_digest":old.digest(a)}],
                      "proof_authority":False}
        candidates.append(c);used.add(w)
    if len(records)!=2 or len(used)!=2 or len(candidates)!=2:
        raise ValueError("extension inventory")
    return portable.seal({"schema":"kuuos.codeai.contextual-memory-layer.v2",
        "parent_memory_key":KEY,"parent_ledger_view":VIEW,"source_head":CURRENT,"source_tree":CURRENT_TREE,
        "scope_digest":old.SCOPE,"lean":portable.LEAN,"mathlib":portable.MATHLIB,
        "transport_key":parent["transport_key"],"r34_direct_digest":DIRECT,"r34_mcp_digest":MCP,
        "additions":records,"new_candidates":sorted(candidates,key=lambda c:c["name"]),
        "semantic_search_complete":False,"proof_authority":False})

def merged(parent,layer,trusted_parent,trusted_layer):
    if parent.get("key")!=portable.seal(parent)["key"] or layer.get("key")!=portable.seal(layer)["key"]:
        raise ValueError("HOLD_LAYER_INTEGRITY")
    if parent!=trusted_parent or layer!=trusted_layer:
        raise ValueError("HOLD_UNADMITTED_LAYER")
    if (parent["key"]!=KEY or layer["parent_memory_key"]!=KEY or layer["parent_ledger_view"]!=VIEW or
        layer["transport_key"]!=parent["transport_key"] or layer["source_head"]!=CURRENT or
        layer["source_tree"]!=CURRENT_TREE or layer["scope_digest"]!=old.SCOPE or
        layer["lean"]!=portable.LEAN or layer["mathlib"]!=portable.MATHLIB):
        raise ValueError("HOLD_LAYER_SCOPE")
    if set(parent["records"])&set(layer["additions"]):
        raise ValueError("HOLD_DUPLICATE_CONTEXT")
    cs=parent["registry"]["candidates"]+layer["new_candidates"]
    if len(cs)!=12 or len({c["name"] for c in cs})!=12:
        raise ValueError("HOLD_DUPLICATE_SOURCE")
    records={**parent["records"],**layer["additions"]}
    if len(records)!=7 or len({r["target_expr"] for r in records.values()})!=7:
        raise ValueError("HOLD_CONTEXT_COLLISION")
    by={c["name"]:c for c in cs}
    for key,r in records.items():
        if r["context_key"]!=key or any(by[m["candidate"]["name"]]!=m["candidate"] for m in r["matches"]):
            raise ValueError("HOLD_WITNESS_BINDING")
        if not r["matches"] or len({m["candidate"]["polarity"] for m in r["matches"]})!=1:
            raise ValueError("HOLD_CONFLICTING_WITNESSES")
    return portable.seal({**{k:v for k,v in parent.items() if k not in ("key","schema","registry","records","new_candidate_names")},
        "schema":"kuuos.codeai.contextual-memory-view.v2","parent_memory_key":KEY,"extension_key":layer["key"],
        "records":records,"registry":{"candidates":sorted(cs,key=lambda c:c["name"])},
        "new_candidate_names":sorted(c["name"] for c in layer["new_candidates"])})

def requests(d):
    qs={k:root.make_request("r35_"+k,q["target"],q["context_args"],q["context_modules"])
        for k,q in sorted(d["requests"].items())}
    shadow=qs["new_shadow_global"];raw=qs["new_original_compat"];orig=qs["raw_negative"]
    c=cm.prev.c
    compat={ "apply":[c(prev.LEC+"Compatible"),*shadow["target"]["apply"][1:]]}
    qs["new_shadow_compat"]=root.make_request("r35_new_shadow_compat",compat,shadow["context_args"],shadow["context_modules"])
    qs["wrong_shadow_as_raw"]=root.make_request("r35_wrong_shadow_as_raw",shadow["target"],raw["context_args"],shadow["context_modules"])
    qs["wrong_raw_observer"]=root.make_request("r35_wrong_raw_observer",raw["target"],orig["context_args"],raw["context_modules"])
    return qs
