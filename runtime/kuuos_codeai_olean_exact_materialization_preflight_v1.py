"""Bind a search hit to an exact module/declaration before materializing it.

This is a read-only candidate preflight, not an admission or applicability
certificate. The caller must independently admit the aggregate receipt.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sqlite3

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from runtime.kuuos_codeai_olean_obstruction_preflight_v1 import recall

def hold(status, **context):
    return {"status":status, **context, "candidate_generation_allowed":False,
            "proof_authority":False,"applicability_certified":False,
            "semantic_search_complete":False}

def exact_lookup(db, receipt, expected_digest, head, module, name):
    """No suffix selection; an explicit module is mandatory even for unique names."""
    try:
        if (digest(receipt)!=expected_digest or receipt["source_head"]!=head
                or receipt["status"]!="INDEPENDENT_PARTITIONED_INDEX_ACCOUNTED"
                or receipt["proof_authority"] is not False
                or receipt["applicability_certified"] is not False):
            return hold("HOLD_INVALID_INDEX")
        if not isinstance(module,str) or not module or not isinstance(name,str) or not name:
            return hold("HOLD_EXACT_MODULE_AND_NAME_REQUIRED")
        db=Path(db)
        if db.is_symlink() or not db.is_file():
            return hold("HOLD_INVALID_INDEX")
        with db.open("rb") as f:
            if hashlib.file_digest(f,"sha256").hexdigest()!=receipt["database_sha256"]:
                return hold("HOLD_INVALID_INDEX")
        con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
        try:
            m=con.execute("SELECT row_json FROM modules WHERE module=?",(module,)).fetchone()
            if m is None:
                return hold("HOLD_UNKNOWN_MODULE",module=module,name=name)
            coverage=json.loads(m[0])
            if coverage["state"].startswith("HOLD"):
                return hold(coverage["state"],module=module,name=name,coverage=coverage)
            rows=con.execute("SELECT row_json FROM theorem_types WHERE module=? AND name=?",
                             (module,name)).fetchall()
            aliases=con.execute("SELECT module FROM theorem_types WHERE name=? ORDER BY module",(name,)).fetchall()
        finally:
            con.close()
        if len(rows)!=1:
            return hold("HOLD_EXACT_DECLARATION_NOT_FOUND",module=module,name=name)
        row=json.loads(rows[0][0]);origin=coverage.get("origin") or {}
        binding=origin.get("binding")
        if (row["module"]!=module or row["name"]!=name or not isinstance(binding,dict)
                or binding["module"]!=module or row["source_candidates"]!=coverage["sources"]
                or coverage["sources"]!=[binding["source"]]):
            return hold("HOLD_UNBOUND_DECLARATION")
        if row["type_expr_sha256"] is None:
            if (row["artifact_binding_digest"]!=digest(binding)
                    or row["type_observation_sha256"]!=digest({k:v for k,v in row.items()
                                                              if k!="type_observation_sha256"})):
                return hold("HOLD_UNBOUND_DECLARATION")
        result=hold("EXACT_OLEAN_MATERIALIZATION_REQUIRED",source_head=head,
                    aggregate_receipt_digest=expected_digest,module=module,name=name,
                    row=row,coverage=coverage,binding=binding,
                    same_name_modules=[x[0] for x in aliases],
                    complete_type_already_indexed=row["type_expr_sha256"] is not None)
        result["request_digest"]=digest(result)
        return result
    except (OSError,KeyError,TypeError,ValueError,sqlite3.Error):
        return hold("HOLD_INVALID_INDEX")

def prepare(db,receipt,expected_digest,head,terms,target,selections):
    """Carry all lexical/type hits, all gaps, and explicit requested full types."""
    search=recall(db,receipt,expected_digest,head,terms,target)
    if search["status"]!="HOLD_OBSTRUCTION_REVIEW":
        return hold(search["status"],search=search,requests=[])
    if not isinstance(selections,list):
        return hold("HOLD_INVALID_SELECTION",search=search,requests=[])
    hits={(x["module"],x["name"]) for x in search["type_matches"]}
    requested=[];seen=set()
    for x in selections:
        if not isinstance(x,dict) or not isinstance(x.get("module"),str) or not isinstance(x.get("name"),str):
            return hold("HOLD_INVALID_SELECTION",search=search,requests=requested)
        key=(x["module"],x["name"])
        if key not in hits or key in seen:
            return hold("HOLD_SELECTION_OUTSIDE_SEARCH_OR_DUPLICATE",search=search,requests=requested)
        seen.add(key)
        request=exact_lookup(db,receipt,expected_digest,head,*key)
        if request["status"]!="EXACT_OLEAN_MATERIALIZATION_REQUIRED":
            return hold(request["status"],search=search,requests=requested,obstruction=request)
        requested.append(request)
    out=hold("HOLD_TYPED_APPLICABILITY_REVIEW",search=search,requests=requested,
             omitted_search_matches=0,unselected_type_match_count=len(hits)-len(requested))
    out["preflight_digest"]=digest(out)
    return out
