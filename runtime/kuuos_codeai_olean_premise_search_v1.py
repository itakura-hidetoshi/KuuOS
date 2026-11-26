"""R13: bounded premise discovery and exact application planning.

Search is advisory. A caller supplies an explicit source, target, fixed
arguments and a bounded candidate vocabulary for the missing proof slots.
All discovered combinations are retained; only verified applications may
be projected. Exhaustion is HOLD, never REFUTED or a provider lease.
"""
from __future__ import annotations
from itertools import product
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_olean_obstruction_preflight_v1 import recall

def make_query(case_id,module,source,target,arguments,polarity,context_modules,slots):
    if not isinstance(arguments,list) or not isinstance(slots,list) or len(slots)>4:
        raise ValueError("invalid premise slots")
    if not isinstance(context_modules,list) or len(context_modules)>8:
        raise ValueError("invalid context modules")
    for m in context_modules:typed.name(m)
    if len(set(context_modules))!=len(context_modules):raise ValueError("duplicate context")
    seen=[]
    fixed=[]
    for a in arguments:
        if isinstance(a,dict) and set(a)=={"slot"}:
            if type(a["slot"]) is not int:raise ValueError("bad slot")
            seen.append(a["slot"])
        else:fixed.append(a)
    if sorted(seen)!=list(range(len(slots))):raise ValueError("slot inventory mismatch")
    typed.make_request(case_id,module,source,target,fixed,polarity)
    for s in slots:
        if (not isinstance(s,dict) or set(s)!={"modules","names"}
                or not isinstance(s["modules"],list) or not isinstance(s["names"],list)
                or not 1<=len(s["modules"])<=8 or not 1<=len(s["names"])<=16
                or len(set(s["modules"]))!=len(s["modules"]) or len(set(s["names"]))!=len(s["names"])):
            raise ValueError("invalid candidate vocabulary")
        for m in s["modules"]:typed.name(m)
        for n in s["names"]:
            typed.name(n)
            if "." in n:raise ValueError("use exact unqualified candidate vocabulary")
    q={"schema":"kuuos.codeai.bounded-premise-search.v1","case_id":case_id,
       "module":module,"source":source,"target":target,"arguments":arguments,
       "polarity":polarity,"context_modules":context_modules,"slots":slots,
       "source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE}
    return {**q,"query_digest":old.digest(q)}

def validate(q):
    if q!=make_query(q["case_id"],q["module"],q["source"],q["target"],q["arguments"],
                     q["polarity"],q["context_modules"],q["slots"]):
        raise ValueError("premise search request changed")

def discover(db,receipt,q,limit=16):
    validate(q)
    if type(limit) is not int or not 1<=limit<=32:raise ValueError("bad trial bound")
    evidence=[];pools=[]
    for s in q["slots"]:
        found=recall(db,receipt,old.R7,old.HEAD,s["names"],typed.term(q["target"]))
        if found["status"] not in ("HOLD_OBSTRUCTION_REVIEW","HOLD_NO_DATA"):
            return old.hold("index_search_failed",search_evidence=evidence+[found],trials=[])
        rows=found["type_matches"]
        pool=sorted({(x["module"],x["name"]) for x in rows
                     if x["module"] in s["modules"] and x["name"].rsplit(".",1)[-1] in s["names"]
                     and x["binder_count"]==0})
        pools.append([{"module":m,"name":n} for m,n in pool])
        evidence.append(found)
    count=1
    for p in pools:count*=len(p)
    if count>limit:
        return old.hold("bounded_premise_search_exceeds_budget",search_evidence=evidence,
                        pools=pools,combination_count=count,trials=[])
    trials=[]
    for j,combo in enumerate(product(*pools)):
        args=[{"const":combo[x["slot"]]["name"]} if isinstance(x,dict) and "slot" in x else x
              for x in q["arguments"]]
        req=typed.make_request(q["case_id"]+"_"+str(j).zfill(2),q["module"],q["source"],
                               q["target"],args,q["polarity"])
        trials.append({"request":req,"premises":list(combo)})
    return {"status":"BOUNDED_PREMISE_PLAN","query_digest":q["query_digest"],
            "pools":pools,"search_evidence":evidence,"trials":trials,
            "combination_count":count,"unobserved_module_count":695,
            "semantic_search_complete":False,"candidate_generation_allowed":False,
            "proof_authority":False}

def imports(q,trial):
    validate(q)
    ms=sorted(set([q["module"]]+q["context_modules"]+[x["module"] for x in trial["premises"]]))
    return "".join("import "+typed.name(m)+"\n" for m in ms)

def render(q,trial,with_checks=True):
    req=trial["request"]
    src=typed.render(req) if with_checks else typed.declarations(req)
    prefix="import "+req["module"]+"\n"
    if not src.startswith(prefix):raise ValueError("renderer boundary changed")
    return imports(q,trial)+src[len(prefix):]

def project(direct,independent,mcp):
    """Caller must separately admit the exact completed run and artifacts."""
    try:
        if (direct!=independent or direct["status"]!="R13_DIRECT_PREMISE_TRIALS"
                or mcp["status"]!="R13_REAL_MCP_GREEN" or mcp["direct_digest"]!=old.digest(direct)
                or direct["source_head"]!=old.HEAD or direct["scope_digest"]!=old.SCOPE
                or direct["source_tree"]!=old.TREE or direct["unobserved_module_count"]!=695):
            return old.hold("unadmitted_independent_premise_evidence")
        routes={};success_ids=set()
        for k,q in direct["queries"].items():
            validate(q)
            plan=direct["plans"][k];rows=direct["results"][k]
            if (q["case_id"]!=k or plan["query_digest"]!=q["query_digest"]
                    or plan["status"]!="BOUNDED_PREMISE_PLAN"
                    or len(plan["trials"])!=len(rows) or plan["combination_count"]!=len(rows)):
                return old.hold("premise_trial_inventory_mismatch")
            wins=[]
            for trial,row in zip(plan["trials"],rows):
                req=trial["request"];typed.validate(req)
                if row["request_digest"]!=req["request_digest"]:
                    return old.hold("trial_identity_mismatch")
                if row["status"]=="HOLD_LEAN_APPLICATION":continue
                if row["status"]!="EXACT_TYPED_APPLICATION":return old.hold("invalid_trial_result")
                t,w=typed.names(req)
                expected={req["source"],w}|{p["name"] for p in trial["premises"]}
                inv={x["name"]:x for x in row["observations"]}
                audits={x["name"]:x["axioms"] for x in mcp["audits"][req["case_id"]]}
                app=row["application"]
                if (set(inv)!=expected or set(audits)!=expected
                        or len(inv)!=len(row["observations"])
                        or app["target_name"]!=t or app["witness_name"]!=w
                        or app["exact_kernel_type_match"] is not True
                        or app["witness_type_repr"]!=inv[w]["type_expr_repr"]
                        or t not in inv[w]["type_constants"]
                        or (req["polarity"]=="negative")!=("Not" in inv[w]["type_constants"])
                        or not (expected-{w})<=set(inv[w]["proof_constants"])
                        or any(set(x["axioms"])-typed.STANDARD or x["axioms"]!=audits[n]
                               for n,x in inv.items())):
                    return old.hold("trial_type_or_mcp_audit_mismatch")
                for p in [{"module":req["module"],"name":req["source"]}]+trial["premises"]:
                    material=direct["materials"][p["module"]+"::"+p["name"]]
                    if material["type_expr_sha256"]!=inv[p["name"]]["type_expr_sha256"]:
                        return old.hold("premise_full_type_mismatch")
                success_ids.add(req["case_id"])
                wins.append({"request_digest":req["request_digest"],"case_id":req["case_id"],
                             "premises":trial["premises"],"target_expr_digest":old.digest(app["target_expr_repr"]),
                             "witness_type_sha256":inv[w]["type_expr_sha256"],"axioms":inv[w]["axioms"]})
            routes[k]={"status":("REFUTED_EXACT_TARGET" if q["polarity"]=="negative" else "REUSE_EXISTING")
                          if wins else "HOLD_TYPED_APPLICABILITY_REVIEW",
                       "query_digest":q["query_digest"],"successful_routes":wins,
                       "attempted_combinations":len(rows),"candidate_generation_allowed":False,
                       "proof_authority":False,"semantic_search_complete":False}
        if success_ids!=set(mcp["audits"]):return old.hold("extra_mcp_evidence")
        return {"status":"R13_INDEPENDENT_PREMISE_ROUTES_OBSERVED","routes":routes,
                "direct_digest":old.digest(direct),"mcp_digest":old.digest(mcp),
                "scope_digest":old.SCOPE,"source_head":old.HEAD,"unobserved_module_count":695,
                "proof_authority":False,"semantic_search_complete":False,
                "candidate_generation_allowed":False,"execution_authority":False}
    except (KeyError,TypeError,ValueError,AttributeError):
        return old.hold("malformed_premise_evidence")

def pre_provider(context,expected_digest,query):
    try:
        validate(query)
        if (context["status"]!="R13_INDEPENDENT_PREMISE_ROUTES_OBSERVED"
                or old.digest(context)!=expected_digest or context["scope_digest"]!=old.SCOPE
                or context["source_head"]!=old.HEAD or context["proof_authority"] is not False):
            return old.hold("unadmitted_premise_context")
        row=context["routes"][query["case_id"]]
        if row["query_digest"]!=query["query_digest"]:return old.hold("premise_query_changed")
        return {**row,"provider_calls":0,"synthesis":None,"execution_authority":False}
    except (KeyError,TypeError,ValueError,AttributeError):
        return old.hold("unknown_premise_query")
