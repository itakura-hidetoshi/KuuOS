"""R48: append the independently certified R47 transport as exact contextual memory.
Retain original and destination observations, typed equality and every route.
An admitted match requests fresh Lean application, not external authority.
"""
from __future__ import annotations
import copy
from runtime import kuuos_codeai_olean_contextual_shadow_transport_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
DIRECT="4601f49e7a9ba604ee63a6446db28a37ec85118e582e4a14f655688448c33e4c"
MCP="51dc0498fc09026e0e4662d8c037372706c6fb50fa27332fade30196662e0202"
PARENT=prev.LAYER
MANIFEST=prev.MANIFEST
NS="KuuOSR48TransportRecall"
MARK="KUUOS_R48_TARGETS "
def project(d,mp,ind,index,extension,layer,mem,qs,obs,targets,observations):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R47_DIRECT_CONTEXTUAL_SHADOW_TRANSPORT" or mp["status"]!="R47_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R47_INDEPENDENT_CONTEXTUAL_SHADOW_TRANSPORT_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        layer["key"]!=PARENT or base.portable.seal(layer)["key"]!=PARENT or
        extension["key"]!=prev.prev.PARENT or base.portable.seal(extension)["key"]!=extension["key"] or
        index["key"]!=prev.prev.parent.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        layer["parent_extension_key"]!=extension["key"] or layer["parent_dispatch_key"]!=index["key"] or
        index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["derived_layer_key"]!=PARENT or
            x["extension_key"]!=extension["key"] or x["dispatch_layer_key"]!=index["key"] or
            x["capsule_layer_key"]!=mem["key"] or x["capsule_manifest"]!=dispatch.prev.MANIFEST or
            x["joint_capsule_manifest"]!=MANIFEST or x["new_targets"]!=2 or
            x["compatibility_witnesses"]!=3 or x["global_witnesses"]!=3 or
            x["historical_hold_retained"] is not True or x["raw_negative_retained"] is not True or
            x["exact_kernel_type"] is not True or x["root_trials"]!=0 or x["capsule_rebuilds"]!=0 or
            x["reapplied_compatibility_recipes"]!=9 or x["provider_calls"]!=0 or
            x["proof_authority"] is not False or x["semantic_search_complete"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["raw_type_and_proof_equal"] is not True or
        ind["mcp_audits"]!=41 or ind["unobserved_module_count"]!=695 or
        d["transport_refs"]!=ind["transport_refs"] or d["controls"]!=ind["controls"]):
        raise ValueError("R47 receipt binding")
    p=prev.plan(index,extension,layer,qs["shadow"],obs["shadow"],targets,observations)
    if p!=d["transport_plan"]:raise ValueError("R47 transport plan drift")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=41 or len(ma)!=41 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R47 audit binding")
    records=[]
    for k,q in sorted(targets.items()):
        o=observations[k];routes=[]
        earlier=prev.prev.recall(index,extension,layer,layer,q,o,base.CURRENT)
        if earlier["status"]!="HOLD_UNREGISTERED_TARGET":raise ValueError("R47 historical miss drift")
        for i,s in enumerate(p["source_routes"]):
            leaf=prev.prev.NS+".shadow"+str(i);c=prev.NS+".compatible"+str(i)
            n=c if k=="compat" else prev.NS+".global"+str(i)
            refs=[prev.EQUAL,leaf] if k=="compat" else [prev.GLUE,prev.COVER,c]
            if (d["transport_refs"][n]!=refs or
                not set(refs)<=set(hist[n]["proof_constants"]) or
                not set(hist[n]["axioms"])<={a for r in refs for a in hist[r]["axioms"]}):
                raise ValueError("R47 transport proof dependency")
            routes.append({"source_route":s,"source_witness":leaf,"source_observation":hist[leaf],
                "compatibility_witness":c,"compatibility_observation":hist[c],
                "historical_witness":n,"historical_observation":hist[n],"historical_digest":old.digest(hist[n]),
                "rule_sources":refs})
        records.append({"kind":k,"request":q,"goal_expr":o["goal_expr"],"context_exprs":o["context_exprs"],
             "polarity":"positive","routes":routes,"historical_decision":earlier})
    return base.portable.seal({"schema":"kuuos.codeai.contextual-shadow-transport-layer.v1",
        "source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_derived_key":PARENT,"parent_extension_key":extension["key"],"parent_dispatch_key":index["key"],
        "r47_direct_digest":DIRECT,"r47_mcp_digest":MCP,"joint_capsule_manifest":MANIFEST,
        "source_request":p["source_request"],"source_observation":p["source_observation"],
        "equality":{"name":prev.EQUAL,"observation":hist[prev.EQUAL],"digest":old.digest(hist[prev.EQUAL])},
        "rule_sources":p["rule_sources"],"shared_context_indices":p["shared_context_indices"],
        "changed_context_index":p["changed_context_index"],"records":records,
        "semantic_search_complete":False,"proof_authority":False})

def recall(index,extension,layer,transport,trusted,q,o,head):
    def hold(s):return {"status":s,"routes":[],"proof_authority":False}
    if transport.get("key")!=base.portable.seal(transport)["key"]:return hold("HOLD_TRANSPORT_INTEGRITY")
    if transport!=trusted:return hold("HOLD_UNADMITTED_TRANSPORT")
    if (head!=base.CURRENT or transport["source_head"]!=head or transport["source_tree"]!=base.CURRENT_TREE or
        transport["scope_digest"]!=old.SCOPE or layer.get("key")!=PARENT or base.portable.seal(layer)["key"]!=PARENT or
        transport["parent_derived_key"]!=PARENT or transport["parent_extension_key"]!=extension.get("key") or
        transport["parent_dispatch_key"]!=index.get("key")):
        return hold("HOLD_TRANSPORT_SCOPE")
    base.root.validate(q)
    if not o["aligned"]:return hold("HOLD_CONTEXT_MISMATCH")
    earlier=prev.prev.recall(index,extension,layer,layer,q,o,head)
    if earlier["status"]!="HOLD_UNREGISTERED_TARGET":return earlier
    matches=[r for r in transport["records"] if r["goal_expr"]==o["goal_expr"] and
         r["context_exprs"]==o["context_exprs"] and all(q[k]==r["request"][k] for k in
         ("target","context_args","context_modules","mode"))]
    if len(matches)>1:return hold("HOLD_CONFLICT")
    if not matches:
        return hold("HOLD_CONTEXT_MISMATCH" if any(r["goal_expr"]==o["goal_expr"] for r in transport["records"])
                    else "HOLD_UNREGISTERED_TARGET")
    r=matches[0]
    return {"status":"EXACT_SHADOW_TRANSPORT_REQUIRED","kind":r["kind"],"polarity":r["polarity"],
         "routes":r["routes"],"equality":transport["equality"],"source_request":transport["source_request"],
         "source_observation":transport["source_observation"],"root_trials":0,"proof_authority":False}

def consumer(transport,targets,observations,decisions):
    if set(targets)!={"compat","global"} or set(decisions)!=set(targets):raise ValueError("transport inventory")
    c=decisions["compat"];g=decisions["global"]
    if any(d["status"]!="EXACT_SHADOW_TRANSPORT_REQUIRED" or d["kind"]!=k or d["polarity"]!="positive" or
           len(d["routes"])!=3 or d["equality"]!=transport["equality"] or
           d["source_request"]!=transport["source_request"] or d["source_observation"]!=transport["source_observation"]
           for k,d in decisions.items()):raise ValueError("unadmitted transport")
    if any(a["source_route"]!=b["source_route"] or a["historical_witness"]!=b["compatibility_witness"]
           for a,b in zip(c["routes"],g["routes"])):raise ValueError("transport path mismatch")
    p={"source_request":transport["source_request"],"source_observation":transport["source_observation"],
       "source_routes":[r["source_route"] for r in c["routes"]],"targets":targets,"observations":observations,
       "equality_source":transport["equality"]["name"],"rule_sources":transport["rule_sources"],
       "shared_context_indices":transport["shared_context_indices"],"changed_context_index":transport["changed_context_index"],
       "parent_derived_layer":PARENT,"root_trials":0,"proof_authority":False,"semantic_search_complete":False}
    body,check,refs=prev.consumer(p)
    expected={r["historical_witness"]:r["rule_sources"] for d in decisions.values() for r in d["routes"]}
    if refs!=expected:raise ValueError("remembered recipe drift")
    return body.replace(prev.NS,NS),check.replace(prev.NS,NS).replace(prev.MARK,MARK),{
        n.replace(prev.NS,NS):[x.replace(prev.NS,NS) for x in rs] for n,rs in refs.items()}
