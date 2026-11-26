"""R15: global advisory premise ranking; exact, bounded Lean comparisons.

No search-module or candidate theorem-name whitelist. All indexed rows
are accounted for. Ranking, exclusion, exhaustion and comparison failure
never certify absence. Only separately audited applications may be reused.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3
from runtime import kuuos_codeai_olean_premise_type_discovery_v1_r2 as local
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

LIMIT=6

def make_query(case_id,module,source,target,fixed,polarity,context_modules,slot_count):
    if type(slot_count) is not int or not 1<=slot_count<=4:
        raise ValueError("invalid closed premise count")
    q=local.make_query(case_id,module,source,target,fixed,polarity,context_modules,[[module]]*slot_count)
    q={k:v for k,v in q.items() if k not in ("slot_modules","query_digest","schema")}
    q.update(schema="kuuos.codeai.global-closed-premise-search.v1",slot_count=slot_count)
    return {**q,"query_digest":old.digest(q)}

def validate(q):
    if q!=make_query(q["case_id"],q["module"],q["source"],q["target"],q["fixed"],
                     q["polarity"],q["context_modules"],q["slot_count"]):
        raise ValueError("global query changed")

def catalog(db,receipt):
    db=Path(db)
    if (old.digest(receipt)!=old.R7 or receipt["source_head"]!=old.HEAD
            or receipt["scope_digest"]!=old.SCOPE or db.is_symlink() or not db.is_file()):
        raise ValueError("unadmitted index")
    with db.open("rb") as f:
        if hashlib.file_digest(f,"sha256").hexdigest()!=receipt["database_sha256"]:
            raise ValueError("index bytes changed")
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        rows=[json.loads(x[0]) for x in con.execute("SELECT row_json FROM theorem_types ORDER BY module,name")]
        modules={x[0]:json.loads(x[1]) for x in con.execute("SELECT module,row_json FROM modules ORDER BY module")}
    finally:con.close()
    if len(rows)!=47705 or len(modules)!=2815:raise ValueError("global index count changed")
    gaps=[x for x in modules.values() if x["state"].startswith("HOLD")]
    if len(gaps)!=695:raise ValueError("missing coverage changed")
    names=Counter(x["name"] for x in rows)
    eligible=[];excluded=Counter()
    for x in rows:
        if x["binder_count"]!=0 or x["universe_parameters"]:
            excluded["OPEN_OR_POLYMORPHIC_TYPE"]+=1;continue
        if names[x["name"]]!=1 or modules[x["module"]]["state"].startswith("HOLD"):
            excluded["AMBIGUOUS_OR_UNOBSERVED_ORIGIN"]+=1;continue
        try:typed.name(x["name"]);typed.name(x["module"])
        except ValueError:
            excluded["UNSUPPORTED_IDENTIFIER"]+=1;continue
        eligible.append(x)
    if len(eligible)+sum(excluded.values())!=len(rows):raise ValueError("index partition")
    df=Counter(n for x in eligible for n in set(x["type_constants"]))
    return eligible,df,{"index_rows":len(rows),"eligible":len(eligible),"excluded":dict(sorted(excluded.items())),
                         "eligible_inventory_digest":old.digest([(x["module"],x["name"],old.digest(x)) for x in eligible]),
                         "unobserved_modules":gaps,"semantic_search_complete":False}

def local_query(q,pools):
    validate(q)
    if len(pools)!=q["slot_count"]:raise ValueError("slot count")
    modules=[sorted({p["module"] for p in pool}) or [q["module"]] for pool in pools]
    b=local.make_query(q["case_id"],q["module"],q["source"],q["target"],q["fixed"],q["polarity"],
                       q["context_modules"],modules)
    return b,{"query_digest":b["query_digest"],"pools":pools}

def render(q,pools):
    b,inv=local_query(q,pools)
    src=local.render(b,inv)
    key='("comparisons", toJson '
    if src.count(key)!=q["slot_count"]:raise ValueError("renderer boundary changed")
    src=src.replace(key,'("domain_head", toJson (if domain.getAppFn.isConst then domain.getAppFn.constName!.toString else "")),\n'
                       '      ("domain_constants", toJson (domain.getUsedConstants.map Name.toString)),\n      '+key)
    return src

def rank(eligible,df,domain,limit=LIMIT):
    if type(limit) is not int or not 1<=limit<=8:raise ValueError("invalid comparison budget")
    constants=set(domain["domain_constants"]);head=domain["domain_head"]
    sha=hashlib.sha256(domain["domain_expr_repr"].encode()).hexdigest()
    if not constants or not head:raise ValueError("unresolved premise shape")
    scored=[]
    for x in eligible:
        other=set(x["type_constants"]);shared=constants&other
        exact=x["type_expr_sha256"]==sha
        # Deterministic advisory rank only; no structural mismatch is a no-go.
        score=[int(exact),int(constants==other),int(x["conclusion_head"]==head),
               sum(1000000//max(1,df[n]) for n in shared),-len(constants^other)]
        scored.append({"module":x["module"],"name":x["name"],"row_digest":old.digest(x),"score":score})
    scored.sort(key=lambda x:(tuple(-v for v in x["score"]),x["module"],x["name"]))
    return {"domain_sha256":sha,"ranked_count":len(scored),"selected":scored[:limit],
            "deferred_count":max(0,len(scored)-limit),"ranking_digest":old.digest(scored),
            "ranked":scored,"candidate_generation_allowed":False,"semantic_search_complete":False}

def plan(q,selected,rows):
    b,inv=local_query(q,selected)
    obs=[{k:v for k,v in x.items() if k not in ("domain_head","domain_constants")} for x in rows]
    return local.match_plan(b,inv,obs)

def application(q,combo,case):
    validate(q)
    return typed.make_request(case,q["module"],q["source"],q["target"],
                              q["fixed"]+[{"const":x["name"]} for x in combo],q["polarity"])
