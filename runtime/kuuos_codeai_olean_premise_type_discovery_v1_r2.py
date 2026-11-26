"""R14: extract actual closed premise domains and compare indexed theorem types.

No theorem-name vocabulary. The explicit module boundary, excluded rows,
and every attempted comparison remain visible. Dependent/open slots,
polymorphic candidates, resource failures and nonmatches remain HOLD.
Type matching alone is not an application certificate or generation lease.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sqlite3
from itertools import product
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

MARK="KUUOS_R14_PREMISE "
def make_query(case_id,module,source,target,fixed,polarity,context_modules,slot_modules):
    if (not isinstance(slot_modules,list) or not 1<=len(slot_modules)<=4
            or not isinstance(context_modules,list) or len(context_modules)>8):
        raise ValueError("invalid module scope")
    typed.make_request(case_id,module,source,target,fixed,polarity)
    for ms in [context_modules]+slot_modules:
        if not isinstance(ms,list) or len(ms)>8 or len(ms)!=len(set(ms)):
            raise ValueError("invalid module list")
        for m in ms:typed.name(m)
    if any(not ms for ms in slot_modules):raise ValueError("empty slot scope")
    q={"schema":"kuuos.codeai.closed-premise-type-discovery.v1","case_id":case_id,
       "module":module,"source":source,"target":target,"fixed":fixed,"polarity":polarity,
       "context_modules":context_modules,"slot_modules":slot_modules,
       "source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE}
    return {**q,"query_digest":old.digest(q)}

def validate(q):
    if q!=make_query(q["case_id"],q["module"],q["source"],q["target"],q["fixed"],
                     q["polarity"],q["context_modules"],q["slot_modules"]):
        raise ValueError("query changed")

def inventory(db,receipt,q):
    validate(q)
    db=Path(db)
    if (old.digest(receipt)!=old.R7 or receipt["source_head"]!=old.HEAD
            or receipt["scope_digest"]!=old.SCOPE or db.is_symlink() or not db.is_file()):
        raise ValueError("index lineage mismatch")
    with db.open("rb") as f:
        if hashlib.file_digest(f,"sha256").hexdigest()!=receipt["database_sha256"]:
            raise ValueError("database digest mismatch")
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        gaps=[json.loads(x[0]) for x in con.execute("SELECT row_json FROM modules WHERE state LIKE 'HOLD%' ORDER BY module")]
        scopes=[];pools=[]
        for modules in q["slot_modules"]:
            rows=[];coverage=[]
            for m in sorted(modules):
                rs=con.execute("SELECT row_json FROM modules WHERE module=?",(m,)).fetchall()
                if len(rs)!=1:raise ValueError("unknown candidate module")
                coverage.append(json.loads(rs[0][0]))
                rows.extend(json.loads(x[0]) for x in con.execute(
                    "SELECT row_json FROM theorem_types WHERE module=? ORDER BY name",(m,)))
            eligible=[];excluded=[]
            for x in rows:
                item={"module":x["module"],"name":x["name"],"row_digest":old.digest(x)}
                if x["binder_count"]!=0 or x["universe_parameters"]:
                    excluded.append({**item,"reason":"OPEN_OR_POLYMORPHIC_TYPE"});continue
                try:typed.name(x["name"])
                except ValueError:
                    excluded.append({**item,"reason":"UNSUPPORTED_IDENTIFIER"});continue
                eligible.append(item)
            if len(eligible)>96:raise ValueError("candidate scope exceeds bounded comparison budget")
            scopes.append({"modules":sorted(modules),"coverage":coverage,"indexed_count":len(rows),
                           "excluded":excluded,"eligible":eligible})
            pools.append(eligible)
    finally:con.close()
    if len(gaps)!=695:raise ValueError("unobserved inventory changed")
    return {"query_digest":q["query_digest"],"scopes":scopes,"pools":pools,"unobserved_modules":gaps,
            "semantic_search_complete":False,"candidate_generation_allowed":False,"proof_authority":False}

def render(q,inv):
    validate(q)
    if inv["query_digest"]!=q["query_digest"] or len(inv["pools"])!=len(q["slot_modules"]):
        raise ValueError("inventory binding")
    mods=sorted(set([q["module"]]+q["context_modules"]+
                    [m for ms in q["slot_modules"] for m in ms]))
    ns="KuuOSR14."+q["case_id"]
    qname=chr(96)*2
    app="@"+q["source"]
    if q["fixed"]:app="("+app+" "+" ".join(typed.term(a) for a in q["fixed"])+")"
    out=["import "+m for m in mods]+["","open Lean","namespace "+ns,
        "set_option autoImplicit false","set_option maxRecDepth 8192","set_option maxHeartbeats 4000000",
        "noncomputable def partialApp := "+app,"end "+ns,"",
        "run_cmd do","  let env ← getEnv",
        "  let some info := env.find? "+qname+ns+".partialApp"+' | throwError "missing partial application"',
        '  unless info.levelParams.isEmpty do throwError "open universe parameters"',
        "  let mut rest := info.type","  let mut domains : Array Expr := #[]",
        "  for _ in [:"+str(len(inv["pools"]))+"] do",
        '    let .forallE _ domain body _ := rest | throwError "missing premise binder"',
        '    if domain.hasLooseBVars || domain.hasMVar || domain.hasFVar then throwError "dependent or open premise"',
        "    let isProp ← Lean.Elab.Command.liftTermElabM (Lean.Meta.isProp domain)",
        '    unless isProp do throwError "premise slot is not a proposition"',
        "    domains := domains.push domain","    rest := body"]
    for j,pool in enumerate(inv["pools"]):
        accumulator="comparisonsSlot"+str(j)
        entries=", ".join('("'+p["module"]+'", '+qname+p["name"]+')' for p in pool)
        out+=["  do","    let domain := domains["+str(j)+"]!",
              "    let candidates : Array (String × Name) := #["+entries+"]",
              "    let mut "+accumulator+" : Array Json := #[]",
              "    for (moduleName, n) in candidates do",
              '      let some candidate := env.find? n | throwError "indexed theorem not imported"',
              '      let some idx := env.getModuleIdxFor? n | throwError "unknown theorem origin"',
              '      unless env.allImportedModuleNames[idx]!.toString == moduleName do throwError "theorem module mismatch"',
              '      unless candidate.isTheorem && candidate.levelParams.isEmpty do throwError "not a closed theorem"',
              "      let status ← Lean.Elab.Command.liftTermElabM do",
              "        try",
              "          let matched ← Lean.Meta.withNewMCtxDepth (Lean.Meta.isDefEq candidate.type domain)",
              '          pure (if matched then "MATCH" else "HOLD_NOT_DEFEQ")',
              '        catch _ => pure "HOLD_COMPARISON_FAILURE"',
              "      "+accumulator+" := "+accumulator+".push (Json.mkObj [",
              '        ("module", toJson moduleName), ("name", toJson n.toString),',
              '        ("status", toJson status),',
              '        ("matched_type_repr", toJson (if status == "MATCH" then reprStr candidate.type else ""))])',
              "    let payload := Json.mkObj [",
              '      ("slot", toJson ('+str(j)+' : Nat)), ("domain_expr_repr", toJson (reprStr domain)),',
              '      ("comparisons", toJson '+accumulator+')]',
              '    Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)']
    return "\n".join(out)+"\n"

def match_plan(q,inv,observations):
    validate(q)
    if inv["query_digest"]!=q["query_digest"] or len(observations)!=len(inv["pools"]):
        raise ValueError("premise observation inventory")
    pools=[]
    for j,(p,row) in enumerate(zip(inv["pools"],observations)):
        if row["slot"]!=j or not row["domain_expr_repr"]:raise ValueError("missing domain")
        cs=row["comparisons"]
        if [(x["module"],x["name"]) for x in cs]!=[(x["module"],x["name"]) for x in p]:
            raise ValueError("candidate comparison inventory mismatch")
        wins=[]
        for x in cs:
            if x["status"] not in ("MATCH","HOLD_NOT_DEFEQ","HOLD_COMPARISON_FAILURE"):
                raise ValueError("unknown comparison")
            if x["status"]=="MATCH":
                if not x["matched_type_repr"]:raise ValueError("missing exact matched type")
                wins.append({"module":x["module"],"name":x["name"],
                             "type_expr_sha256":hashlib.sha256(x["matched_type_repr"].encode()).hexdigest()})
            elif x["matched_type_repr"]:raise ValueError("unexpected match expression")
        pools.append(wins)
    count=1
    for p in pools:count*=len(p)
    if count>32:return old.hold("matched_combinations_exceed_budget",pools=pools,combination_count=count)
    combos=[list(x) for x in product(*pools)]
    return {"status":"MATCHED_CANDIDATES_REQUIRE_APPLICATION" if combos else "HOLD_NO_MATCHED_PREMISE",
            "query_digest":q["query_digest"],"pools":pools,"combinations":combos,"combination_count":count,
            "observations_digest":old.digest(observations),"unobserved_module_count":695,
            "candidate_generation_allowed":False,"proof_authority":False,"semantic_search_complete":False}

def application_request(q,combo,case):
    return typed.make_request(case,q["module"],q["source"],q["target"],
                              q["fixed"]+[{"const":x["name"]} for x in combo],q["polarity"])

def same_application(a,b):
    return {k:v for k,v in a.items() if k not in ("case_id","request_digest")}=={
            k:v for k,v in b.items() if k not in ("case_id","request_digest")}
