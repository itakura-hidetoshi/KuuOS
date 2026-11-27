"""R37: append-only, evidence-bound exact contextual route memory.
A stored route is a proposal for fresh application, not proof or execution
authority. Different routes may share an underlying proof dependency.
No search miss is a mathematical refutation. No historical view is rewritten.
"""
from __future__ import annotations
import copy
from runtime import kuuos_codeai_olean_contextual_premise_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
DIRECT="57319e74efa75fa859a2cf0d8986b12f267aa2bc0832075e528b9dce0c362122"
MCP="3ebc4e00c1cf1c04426487ee340123ffb8f4ace6ec37a3de256b1332086be850"
COMPAT=prev.LEC+"nativeF55_twoChart_shadow_compatible"
GLOBAL=prev.LEC+"nativeF55_twoChart_shadow_global"
RULE=prev.LEC+"global_implies_compatible"
CASE="new_shadow_compat"
def project(view,d,mp,ind):
    if (view["key"]!=prev.VIEW or prev.portable.seal(view)["key"]!=prev.VIEW or
        old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R36_DIRECT_CONTEXTUAL_PREMISE" or mp["status"]!="R36_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R36_INDEPENDENT_CONTEXTUAL_PREMISE_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or ind["memory_bytes_equal"] is not True or
        d["context_view_key"]!=prev.VIEW or ind["context_view_key"]!=prev.VIEW or
        d["source_head"]!=prev.CURRENT or d["source_tree"]!=prev.CURRENT_TREE or d["scope_digest"]!=old.SCOPE or
        ind["source_head"]!=prev.CURRENT or ind["source_tree"]!=prev.CURRENT_TREE or ind["scope_digest"]!=old.SCOPE or
        ind["root_trials"]!=18 or ind["direct_routes"]!=1 or ind["premise_routes"]!=1 or
        ind["new_typed_applications"]!=10 or ind["mcp_audits"]!=25 or ind["proof_authority"] is not False):
        raise ValueError("R36 admission")
    obs=d["observations"][CASE];q=d["requests"][CASE];prev.root.validate(q)
    if (d["decisions"][CASE]["status"]!="HOLD_SEARCH_REQUIRED" or not obs["target_aligned"] or
        obs["target_matches"] or obs["context_matches"] or obs["goal_expr"]!=obs["context_goal_expr"] or
        q["target"]!=prev.cm.prev.context_target(q) or len(obs["context_exprs"])!=7):
        raise ValueError("context is not an aligned historical miss")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=len(ma) or len(hist)!=25 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD or
        prev.portable.hash_type(hist[n]["type_expr_repr"])!=hist[n]["type_expr_sha256"] for n in hist):
        raise ValueError("R36 proof audit binding")
    if COMPAT not in hist[GLOBAL]["proof_constants"]:
        raise ValueError("expected shared proof dependency missing")
    routes=d["discovery"]["routes"]
    if (d["discovery"]["status"]!="APPLICATION_REQUIRED" or len(routes)!=2 or
        {(r["kind"],r["rule"],r["polarity"]) for r in routes}!={("direct",COMPAT,"positive"),("one_premise",RULE,"positive")}):
        raise ValueError("R36 route inventory")
    entries=[]
    for r in routes:
        if hist[r["rule"]]["type_expr_repr"]!=r["source_type"]:raise ValueError("source type drift")
        refs=[r["rule"]]
        if r["kind"]=="direct":
            if r["premise"] is not None:raise ValueError("unexpected premise")
        else:
            p=r["premise"];rec=view["records"][p["context_key"]]
            if (rec["case"]!="new_shadow_global" or p["candidate"]["name"]!=GLOBAL or
                p["candidate"] not in [m["candidate"] for m in rec["matches"]] or
                p["candidate"]["polarity"]!="positive" or rec["context_args"]!=q["context_args"] or
                rec["request"]["context_modules"]!=q["context_modules"] or rec["request"]["mode"]!=q["mode"]):
                raise ValueError("premise provenance")
            refs.append(GLOBAL)
        ws=[(n,a) for n,a in d["applications"].items() if a["case"]==CASE and a["route"]==r]
        if len(ws)!=1:raise ValueError("route witness cardinality")
        n,a=ws[0];req=a["request"];typed.validate(req)
        z=a["application"]
        if (typed.names(req)[1]!=n or req["source"]!=r["rule"] or req["target"]!=q["target"] or
            req["module"]!=r["module"] or req["polarity"]!=r["polarity"] or req["arguments"] or
            a["current_binding"]!=old.digest({"context_view_key":prev.VIEW,"request":q,"route":r,"current_head":prev.CURRENT}) or
            z["exact_kernel_type_match"] is not True or z["target_expr_repr"]!=obs["goal_expr"] or
            z["witness_type_repr"]!=hist[n]["type_expr_repr"] or not set(refs)<=set(hist[n]["proof_constants"]) or
            not set(hist[n]["axioms"])<={a for p in refs for a in hist[p]["axioms"]}):
            raise ValueError("historical route binding")
        entries.append({"route":copy.deepcopy(r),"witness":n,"application_digest":old.digest(a),
                        "witness_observation":hist[n],"source_refs":refs})
    key=old.digest({"target_expr":obs["goal_expr"],"context_args":q["context_args"],
                    "context_modules":q["context_modules"],"mode":q["mode"]})
    if key in view["records"] or any(x["target_expr"]==obs["goal_expr"] for x in view["records"].values()):
        raise ValueError("non-append route context")
    return prev.portable.seal({"schema":"kuuos.codeai.contextual-route-memory-layer.v1",
        "parent_view_key":prev.VIEW,"source_head":prev.CURRENT,"source_tree":prev.CURRENT_TREE,
        "scope_digest":old.SCOPE,"lean":prev.portable.LEAN,"mathlib":prev.portable.MATHLIB,
        "r36_direct_digest":DIRECT,"r36_mcp_digest":MCP,"r36_independent_digest":old.digest(ind),
        "context_key":key,"request":q,"observation":obs,"routes":entries,
        "source_observations":{n:hist[n] for n in sorted({COMPAT,GLOBAL,RULE})},
        "observed_shared_dependency":{"from":GLOBAL,"to":COMPAT},
        "mathematical_independence_claimed":False,"semantic_search_complete":False,"proof_authority":False})

def recall(layer,trusted,view,q,obs,head):
    if layer.get("key")!=prev.portable.seal(layer)["key"]:
        return {"status":"HOLD_ROUTE_LAYER_INTEGRITY","routes":[]}
    if layer!=trusted:return {"status":"HOLD_UNADMITTED_ROUTE_LAYER","routes":[]}
    if (head!=prev.CURRENT or layer["source_head"]!=head or layer["source_tree"]!=prev.CURRENT_TREE or
        layer["scope_digest"]!=old.SCOPE or view["key"]!=prev.VIEW or prev.portable.seal(view)["key"]!=prev.VIEW or
        layer["parent_view_key"]!=view["key"]):
        return {"status":"HOLD_ROUTE_SCOPE","routes":[]}
    prev.root.validate(q);saved=layer["request"];prior=layer["observation"]
    if (not obs["target_aligned"] or obs["goal_expr"]!=obs["context_goal_expr"] or
        any(q[k]!=saved[k] for k in ("target","context_args","context_modules","mode")) or
        any(obs[k]!=prior[k] for k in ("goal_expr","context_goal_expr","context_exprs","target_aligned","target_matches","context_matches"))):
        return {"status":"HOLD_ROUTE_CONTEXT_MISMATCH","routes":[]}
    return {"status":"EXACT_CONTEXT_ROUTE_APPLICATION_REQUIRED","context_key":layer["context_key"],
            "routes":[x["route"] for x in layer["routes"]],"candidate_comparison_searches":0,
            "root_searches":0,"proof_authority":False}
