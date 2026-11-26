"""Advisory exact-scope olean preflight. No semantic or proof authority.

Only a caller with a separately admitted aggregate receipt can bind the
database. A digest proves equality to that receipt, not authenticity by
itself. This API never permits provider generation or returns REFUTED.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sqlite3
import unicodedata

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKC",s).casefold() if c.isalnum())

def hold(reason):
    return {"status":"HOLD_INVALID_INDEX","issues":[reason],
            "candidate_generation_allowed":False,"proof_authority":False,
            "applicability_certified":False,"semantic_search_complete":False}

def recall(db,receipt,expected_receipt_digest,head,terms,target):
    """Return ALL literal matches, not a top-k. Negative binder-only and
    positive controls remain distinct. Missing coverage remains explicit.
    The caller must independently admit the receipt and check applicability.
    """
    try:
        if (digest(receipt)!=expected_receipt_digest or receipt["source_head"]!=head
                or receipt["status"]!="INDEPENDENT_PARTITIONED_INDEX_ACCOUNTED"
                or receipt["proof_authority"] is not False or receipt["applicability_certified"] is not False):
            return hold("unbound_aggregate_receipt")
        if not isinstance(target,str) or not target.strip() or not isinstance(terms,list):
            return hold("invalid_target_or_terms")
        keys=sorted(set(norm(t) for t in terms if isinstance(t,str) and len(norm(t))>=3))
        if not keys or len(keys)>256:
            return hold("invalid_search_terms")
        db=Path(db)
        if db.is_symlink() or not db.is_file():
            return hold("missing_database")
        with db.open("rb") as f:
            if hashlib.file_digest(f,"sha256").hexdigest()!=receipt["database_sha256"]:
                return hold("database_digest_mismatch")
        con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
        try:
            where=" OR ".join("instr(search_text,?)>0" for _ in keys)
            types=[json.loads(r[0]) for r in con.execute(
                "SELECT row_json FROM theorem_types WHERE "+where+" ORDER BY module,name",keys)]
            lexical=[json.loads(r[0]) for r in con.execute(
                "SELECT row_json FROM hints WHERE "+where+" ORDER BY module,id",keys)]
            gaps=[json.loads(r[0]) for r in con.execute(
                "SELECT row_json FROM modules WHERE state LIKE 'HOLD%' ORDER BY module")]
        finally:
            con.close()
        out={"status":"HOLD_OBSTRUCTION_REVIEW" if types or lexical else "HOLD_NO_DATA",
             "source_head":head,"aggregate_receipt_digest":expected_receipt_digest,"target":target,
             "terms":keys,"type_matches":types,"lexical_matches":lexical,"unobserved_modules":gaps,
             "parse_gaps":receipt["parse_gaps"],"type_match_count":len(types),"lexical_match_count":len(lexical),
             "global_lexical_hint_count":receipt["lexical_hint_count"],"omitted_matches":0,
             "candidate_generation_allowed":False,"proof_authority":False,
             "applicability_certified":False,"semantic_search_complete":False}
        out["receipt_digest"]=digest(out)
        return out
    except (OSError,KeyError,TypeError,ValueError,sqlite3.Error) as exc:
        return hold(type(exc).__name__)
