"""R49: audit the finite observed proof dependency graph of R48.

Recipe dependencies must be actual kernel-observed constants. A topological
schedule is scoped to audited declarations; outside references are retained
as an explicit frontier, not promoted to observed proofs. Candidate cycles,
missing dependencies, and altered recipes are rejected before application.
"""
from __future__ import annotations
from collections import Counter
from runtime import kuuos_codeai_olean_contextual_transport_memory_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
transport=prev.prev
derived=transport.prev
DIRECT="15846a03f1f8841cfcbb85b6c587d9c3fa4d8215102bd0d7bb09a2370d47ccef"
MCP="d8aec208c086cc2749479bf9a5b4655dfdca16da05655e203b387db0d595b2b6"
LAYER="43bbc56dbf1aebec9103ee1a095324f641e02cedfebd0cc1c7c3ef21770cad45"
MANIFEST=prev.MANIFEST

def admit(d,mp,ind,index,extension,layer,memory,mem):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R48_DIRECT_CONTEXTUAL_TRANSPORT_MEMORY" or mp["status"]!="R48_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R48_INDEPENDENT_CONTEXTUAL_TRANSPORT_MEMORY_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        memory["key"]!=LAYER or base.portable.seal(memory)["key"]!=LAYER or
        layer["key"]!=prev.PARENT or base.portable.seal(layer)["key"]!=layer["key"] or
        extension["key"]!=derived.PARENT or base.portable.seal(extension)["key"]!=extension["key"] or
        index["key"]!=derived.parent.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        memory["parent_derived_key"]!=layer["key"] or memory["parent_extension_key"]!=extension["key"] or
        memory["parent_dispatch_key"]!=index["key"] or layer["parent_extension_key"]!=extension["key"] or
        layer["parent_dispatch_key"]!=index["key"] or index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["transport_layer_key"]!=LAYER or
            x["derived_layer_key"]!=layer["key"] or x["extension_key"]!=extension["key"] or
            x["dispatch_layer_key"]!=index["key"] or x["capsule_layer_key"]!=mem["key"] or
            x["capsule_manifest"]!=dispatch.prev.MANIFEST or x["joint_capsule_manifest"]!=MANIFEST or
            x["new_contexts"]!=2 or x["recalled_routes"]!=6 or x["compatibility_witnesses"]!=3 or
            x["global_witnesses"]!=3 or x["historical_hold_retained"] is not True or
            x["raw_negative_retained"] is not True or x["exact_kernel_type"] is not True or
            x["root_trials"]!=0 or x["capsule_rebuilds"]!=0 or x["reapplied_compatibility_recipes"]!=9 or
            x["reapplied_transport_recipes"]!=6 or x["provider_calls"]!=0 or
            x["proof_authority"] is not False or x["semantic_search_complete"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["transport_layer_bytes_equal"] is not True or
        ind["raw_type_and_proof_equal"] is not True or ind["mcp_audits"]!=41 or
        ind["unobserved_module_count"]!=695 or d["controls"]!=ind["controls"]):
        raise ValueError("R48 receipt binding")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=41 or len(ma)!=41 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R48 audit binding")
    if memory["equality"]["observation"]!=hist[transport.EQUAL] or memory["equality"]["digest"]!=old.digest(hist[transport.EQUAL]):
        raise ValueError("equality receipt drift")
    return hist

def recipe_refs(memory,layer,decisions,result):
    # Recover the nine derived recipes and six transport recipes from admitted
    # records. Preserve every historical route; no merging by pretty type.
    refs={}
    for k,d in sorted(decisions.items()):
        if d["status"]!="EXACT_DERIVED_COMPATIBILITY_REQUIRED" or len(d["routes"])!=3:
            raise ValueError("HOLD_RECIPE_CONTEXT")
        for i,r in enumerate(d["routes"]):
            n=derived.NS+"."+k+str(i)
            refs[n]=[r["joint_root"]]+r["rule_sources"]
    for k,d in sorted(result.items()):
        if d["status"]!="EXACT_SHADOW_TRANSPORT_REQUIRED" or d["kind"]!=k or d["polarity"]!="positive" or len(d["routes"])!=3:
            raise ValueError("HOLD_RECIPE_CONTEXT")
        for i,r in enumerate(d["routes"]):
            if r["source_route"]!=decisions["shadow"]["routes"][i]:
                raise ValueError("HOLD_RECIPE_CONTEXT")
            n=r["historical_witness"].replace(transport.NS,prev.NS)
            refs[n]=[x.replace(transport.NS,prev.NS) for x in r["rule_sources"]]
    if len(refs)!=15:raise ValueError("HOLD_RECIPE_INVENTORY")
    return refs

def schedule(graph):
    """Dependencies precede consumers; never silently drop an unknown node."""
    state={};order=[];stack=[]
    def visit(n):
        if n not in graph:raise ValueError("HOLD_UNOBSERVED_DEPENDENCY")
        if state.get(n)==1:raise ValueError("HOLD_CYCLIC_DEPENDENCY")
        if state.get(n)==2:return
        state[n]=1;stack.append(n)
        for dep in sorted(graph[n]):visit(dep)
        stack.pop();state[n]=2;order.append(n)
    for n in sorted(graph):visit(n)
    return order

def verify_recipe_edges(rows,refs,expected):
    if refs!=expected:raise ValueError("HOLD_RECIPE_PROVENANCE")
    for n,rs in refs.items():
        if n not in rows or any(r not in rows for r in rs):raise ValueError("HOLD_UNOBSERVED_DEPENDENCY")
        if not set(rs)<=set(rows[n]["proof_constants"]):raise ValueError("HOLD_KERNEL_EDGE_MISMATCH")
        if not set(rows[n]["axioms"])<={a for r in rs for a in rows[r]["axioms"]}:
            raise ValueError("HOLD_RECIPE_AXIOM_DRIFT")

def audit_graph(rows,refs,expected):
    verify_recipe_edges(rows,refs,expected)
    nodes=set(rows)
    graph={n:sorted(set(x["proof_constants"])&nodes) for n,x in sorted(rows.items())}
    frontier={n:sorted(set(x["proof_constants"])-nodes) for n,x in sorted(rows.items())}
    order=schedule(graph)
    pos={n:i for i,n in enumerate(order)}
    if any(pos[r]>=pos[n] for n,rs in graph.items() for r in rs):raise ValueError("HOLD_CYCLIC_DEPENDENCY")
    roots=sorted(n for n in refs if n.startswith(prev.NS+".global"))
    if len(roots)!=3:raise ValueError("HOLD_RECIPE_INVENTORY")
    def closure(n):
        seen=set()
        def visit(x):
            if x in seen:return
            seen.add(x)
            for r in graph[x]:visit(r)
        visit(n);return seen
    closures={n:sorted(closure(n)) for n in roots}
    shared=sorted(n for n,c in Counter(x for xs in closures.values() for x in xs).items() if c>1)
    # Dependency frontier is deliberately not claimed to be an audited graph.
    return {"schema":"kuuos.codeai.observed-dependency-dag.v1","nodes":sorted(nodes),
        "observed_edges":graph,"unobserved_frontier":frontier,"topological_order":order,
        "recipe_edges":refs,"selected_roots":roots,"root_closures":closures,"shared_nodes":shared,
        "node_count":len(nodes),"observed_edge_count":sum(map(len,graph.values())),
        "recipe_edge_count":sum(map(len,refs.values())),
        "frontier_constant_count":len({x for rs in frontier.values() for x in rs}),
        "all_repository_dependencies_observed":False,"proof_authority":False}

def controls(rows,refs,graph):
    from copy import deepcopy
    out={}
    def reject(label,fn):
        try:fn()
        except ValueError as e:out[label]=str(e)
        else:raise ValueError("invalid graph accepted "+label)
    root=prev.NS+".global0";leaf=prev.NS+".compatible0"
    v=deepcopy(graph);v[root].append(root)
    reject("self_cycle",lambda:schedule(v))
    v=deepcopy(graph);v[leaf].append(root)
    reject("two_node_cycle",lambda:schedule(v))
    v=deepcopy(graph);v[root].append("KuuOSR49.Unobserved")
    reject("missing_dependency",lambda:schedule(v))
    bad=deepcopy(refs);bad[root]=[x for x in bad[root] if x!=leaf]
    reject("omitted_recipe_edge",lambda:verify_recipe_edges(rows,bad,refs))
    bad=deepcopy(refs);bad[root]=[derived.NS+".raw0" if x==leaf else x for x in bad[root]]
    reject("wrong_polarity_recipe",lambda:verify_recipe_edges(rows,bad,refs))
    # Even when the proposed recipe is internally consistent, the actual
    # kernel observation must contain its claimed dependency.
    bad=deepcopy(refs);bad[root].append(root)
    reject("invented_kernel_edge",lambda:verify_recipe_edges(rows,bad,bad))
    expected={"self_cycle":"HOLD_CYCLIC_DEPENDENCY","two_node_cycle":"HOLD_CYCLIC_DEPENDENCY",
        "missing_dependency":"HOLD_UNOBSERVED_DEPENDENCY","omitted_recipe_edge":"HOLD_RECIPE_PROVENANCE",
        "wrong_polarity_recipe":"HOLD_RECIPE_PROVENANCE","invented_kernel_edge":"HOLD_KERNEL_EDGE_MISMATCH"}
    if out!=expected:raise ValueError("graph control drift")
    return out
