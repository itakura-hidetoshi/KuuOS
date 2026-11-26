"""R19: global structural inventory for R18's bounded AND-OR engine.
Index ranking is advisory, never a proof. Prior independently verified
complete types may nominate terminal candidates; exact specialization and
final direct/MCP/independent audits remain mandatory.
"""
from __future__ import annotations
from collections import Counter
import json
import sqlite3
from runtime import kuuos_codeai_olean_multi_premise_gluing_v1_r2 as base
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime import kuuos_codeai_olean_general_application_v1 as typed

poly=base.poly
LEC=base.LEC
MARK="KUUOS_R19_SEARCH "
LIMIT=24

def inventory(db, historical, prior):
    if old.digest(historical)!=prior["inventory_digest"]:
        raise ValueError("R18 inventory changed")
    if prior["source_head"]!=old.HEAD or prior["source_tree"]!=old.TREE or prior["scope_digest"]!=old.SCOPE:
        raise ValueError("R18 proof scope changed")
    observed={x["name"]:x for x in prior["fresh_application"]["observations"]}
    admitted={}
    for k,m in prior["materials"].items():
        n=m["name"]
        if k!=m["module"]+"::"+n or n not in observed:
            raise ValueError("R18 source inventory")
        x=observed[n]
        if x["type_expr_sha256"]!=m["type_expr_sha256"] or set(x["axioms"])-typed.STANDARD:
            raise ValueError("R18 material audit mismatch")
        admitted[n]=m
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        rows=[json.loads(x[0]) for x in con.execute("SELECT row_json FROM theorem_types ORDER BY module,name")]
        modules={x[0]:json.loads(x[1]) for x in con.execute("SELECT module,row_json FROM modules ORDER BY module")}
    finally:con.close()
    gaps=[x for x in modules.values() if x["state"].startswith("HOLD")]
    if len(rows)!=47705 or len(modules)!=2815 or len(gaps)!=695:
        raise ValueError("R7 inventory drift")
    names=Counter(x["name"] for x in rows)
    heads=set(base.HEADS)
    pools={h:[] for h in sorted(heads|{"Not"})}
    deferred=Counter()
    for x in rows:
        h=x["conclusion_head"]
        relevant_negative=(h=="Not" and x["conclusion_negative_head"] and
                           bool(heads.intersection(x["conclusion_constants"])))
        if h not in heads and not relevant_negative:
            deferred["OTHER_STRUCTURE_DEFERRED"]+=1;continue
        if x["binder_count"]>32:
            deferred["BINDER_BUDGET_DEFERRED"]+=1;continue
        if names[x["name"]]!=1 or modules[x["module"]]["state"].startswith("HOLD"):
            deferred["ORIGIN_DEFERRED"]+=1;continue
        try:typed.name(x["module"]);typed.name(x["name"])
        except ValueError:
            deferred["IDENTIFIER_DEFERRED"]+=1;continue
        pools[h].append({"module":x["module"],"name":x["name"],"row_digest":old.digest(x),
            "binder_count":x["binder_count"],"universe_parameters":x["universe_parameters"],
            "prior_audited":x["name"] in admitted,
            "negative_head_matches":sorted(heads.intersection(x["conclusion_constants"])) if h=="Not" else []})
    selected={};capped={}
    for h,ps in pools.items():
        ps.sort(key=lambda x:(x["binder_count"],not x["prior_audited"],x["module"],x["name"]))
        selected[h]=ps[:LIMIT];capped[h]=ps[LIMIT:]
    if sum(map(len,selected.values()))+sum(map(len,capped.values()))+sum(deferred.values())!=len(rows):
        raise ValueError("index partition not complete")
    # No theorem-name whitelist: only selected positive closed declarations
    # whose exact source type appeared in the admitted R18 audited material.
    recall=sorted(p["name"] for h,ps in selected.items() if h!="Not" for p in ps
                  if p["binder_count"]==0 and p["prior_audited"] and
                  admitted[p["name"]]["module"]==p["module"])
    return {"source_head":old.HEAD,"scope_digest":old.SCOPE,"selected":selected,
        "capped":capped,"deferred_counts":dict(sorted(deferred.items())),
        "index_rows":len(rows),"unobserved_modules":gaps,"closed_recall":recall,
        "r18_inventory_digest":old.digest(historical),"semantic_search_complete":False,"proof_authority":False}

def render(q,args,inv):
    return base.render(q,args,inv).replace(base.MARK,MARK)

def application(q,args,route,case):
    return base.application(q,args,route,case)
