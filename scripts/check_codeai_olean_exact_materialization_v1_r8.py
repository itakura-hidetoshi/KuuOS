#!/usr/bin/env python3
"""R8: on-demand complete Expr retrieval from the exact certified R7 index.

No project imports, no fresh proof assertion, no provider execution.
Use original verified olean bytes and the exact declaration, not a hash64
match or a source preview. Independently compare selected full expressions.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import re
import sqlite3

import check_codeai_kernel_obstruction_index_v1_r5 as r5
import codeai_olean_bounded_features_v1 as features
v=r5.v
ROOT=v.ROOT
from runtime.kuuos_codeai_olean_exact_materialization_preflight_v1 import exact_lookup,prepare

R7_RUN=45774874136
R7_HEAD="eb5728205f4518503708924d2bf8a42cc5555061"
R7_JOB=139761540302
R7_ARTIFACT=15095689716
R7_ZIP="sha256:391a32db3622608c97579276682e71a493c87c7bf9fd587eb3e8f6fdcff79d65"
R7_RECEIPT="b47968f3f9983c2c938b6d268d0ee718679936c20748bc21b83c665f8121af54"
R7_DB="5ba2628195addbd6d27e0cfff2060a45fd3206b973444f0423894ef7f42e2b07"
MARK="KUUOS_OLEAN_R8_EXACT_EXPORT"

def admit(index,head):
    run=v.cache.api("actions/runs/"+str(R7_RUN))
    job=v.cache.api("actions/jobs/"+str(R7_JOB))
    art=v.cache.api("actions/artifacts/"+str(R7_ARTIFACT))
    v.need(run["head_sha"]==R7_HEAD and run["status"]=="completed" and run["conclusion"]=="success"
           and run["run_attempt"]==1 and job["run_id"]==R7_RUN and job["status"]=="completed"
           and job["conclusion"]=="success"
           and any(s["name"]=="Assemble indexed SQLite catalog and test read-only candidate recall"
                   and s["status"]=="completed" and s["conclusion"]=="success" for s in job["steps"])
           and art["id"]==R7_ARTIFACT and art["digest"]==R7_ZIP and not art["expired"]
           and art["workflow_run"]["id"]==R7_RUN and art["workflow_run"]["head_sha"]==R7_HEAD,
           "R7 independent aggregate provenance not admitted")
    receipt=r5.load(index/"aggregate.json")
    db=index/"kernel-recall.sqlite"
    v.need(v.digest(receipt)==R7_RECEIPT and receipt["source_head"]==head
           and receipt["scope_digest"]==v.SCOPE and receipt["database_sha256"]==R7_DB
           and r5.filehash(db)==R7_DB and receipt["raw_type_count"]==47705
           and receipt["source_module_count"]==2815 and receipt["lexical_hint_count"]==6380
           and receipt["state_counts"]["HOLD_MISSING_OLEAN"]==695,
           "R7 index contents changed")
    return receipt,db

def materialize(folder,request,sources,env):
    folder.mkdir()
    m,n=request["module"],request["name"]
    v.need(request["status"]=="EXACT_OLEAN_MATERIALIZATION_REQUIRED"
           and request["request_digest"]==v.digest({k:z for k,z in request.items() if k!="request_digest"}),
           "unbound exact materialization request")
    v.need(m in sources and len(sources[m])==1 and sources[m]==request["coverage"]["sources"]
           and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*",m),
           "source module identity changed")
    v.need("\n" not in n and "\r" not in n and "\t" not in n,"invalid exact name")
    base=ROOT/".lake/build/lib/lean"/(m.replace(".","/")+".olean")
    artifact,hold=r5.bind_files(m,base,sources[m][0])
    v.need(hold is None and artifact==request["binding"],"verified olean binding changed")
    v.save(folder/"request.json",request)
    wanted=folder/"modules.txt"; names=folder/"selected.txt"
    meta=folder/"environment.json";raw=folder/"kernel-types.jsonl"
    wanted.write_text(m+"\t"+"\t".join(f["path"] for f in artifact["files"])+"\n",encoding="utf-8")
    names.write_text(n+"\n",encoding="utf-8")
    template=v.TEMPLATE.read_text(encoding="utf-8")
    marker="set_option maxRecDepth 8192 in\n"
    v.need(template.startswith("import KuuOSFormal\n") and template.count(marker)==1,
           "serializer boundary changed")
    prefix=template.split(marker,1)[0].replace("import KuuOSFormal\n","import Lean\n",1)
    old='("type_expr_repr", toJson (reprStr info.type)),'
    v.need(prefix.count(old)==1,"exact type serializer changed")
    prefix=prefix.replace(old,old+'\n    ("kernel_expr_hash64_advisory", toJson (toString info.type.hash)),')
    tail=r5.TAIL.replace(r5.MARK,MARK)
    old='    let manifest ← IO.FS.readFile "__MODULE_FILE__"'
    v.need(tail.count(old)==1 and tail.count("if info.isTheorem then")==1,"reader boundary changed")
    tail=tail.replace(old,old+'\n    let selected ← IO.FS.readFile "__NAMES_FILE__"\n'
                      '    let wantedNames : Std.HashSet String := (selected.splitOn "\\n").foldl\n'
                      '      (fun acc name => acc.insert name) {}')
    tail=tail.replace("if info.isTheorem then","if info.isTheorem && wantedNames.contains info.name.toString then")
    lean=prefix+tail
    for key,path in (("__MODULE_FILE__",wanted),("__NAMES_FILE__",names),("__META_FILE__",meta),("__ROWS_FILE__",raw)):
        v.need(lean.count(key)==1,"missing exact probe placeholder")
        lean=lean.replace(key,path.relative_to(ROOT).as_posix())
    probe=folder/"ExactType.lean";probe.write_text(lean,encoding="utf-8")
    msg=features.run_bounded(folder,probe,raw,env)
    data=r5.load(meta)
    v.need(data["selected_theorems"]==1 and len(data["modules"])==1
           and data["modules"][0]["module"]==m and data["modules"][0]["theorem_count"]==1
           and f"{MARK} 1" in msg,"exact declaration not uniquely exported")
    text_rows=raw.read_text(encoding="utf-8").splitlines()
    v.need(len(text_rows)==1,"multiple raw selected declarations")
    raw_row=json.loads(text_rows[0])
    v.need(raw_row["module"]==m and raw_row["name"]==n,"wrong selected theorem")
    rows=v.read_rows(raw,{"imported_modules":[m],"selected_theorems":1},{m:sources[m]},folder)
    row=rows[0];prior=request["row"]
    v.need(features.compare_features([row],[prior]),"complete type features disagree with R7")
    if prior["type_expr_sha256"] is not None:
        v.need(row==prior,"previous complete type digest changed")
    else:
        v.need(prior["kernel_expr_hash64_advisory"]==raw_row["kernel_expr_hash64_advisory"],
               "advisory kernel hash changed")
    for f in artifact["files"]:
        v.need(r5.filehash(ROOT/f["path"])==f["sha256"],"artifact changed during exact read")
    full=raw_row["type_expr_repr"]
    v.need(isinstance(full,str) and full and v.sha(full.encode())==row["type_expr_sha256"],
           "exact expression digest mismatch")
    # The complete Expr representation and raw row are archived separately.
    # Neither the Expr repr nor its digest is an applicability certificate.
    receipt={"status":"EXACT_OLEAN_TYPE_OBSERVED","source_head":request["source_head"],
             "aggregate_receipt_digest":R7_RECEIPT,"request_digest":request["request_digest"],
             "module":m,"name":n,"artifact_binding_digest":v.digest(artifact),
             "type_expr_sha256":row["type_expr_sha256"],"full_type_repr_bytes":len(full.encode()),
             "row":row,"old_full_type_digest_matched":prior["type_expr_sha256"] is not None,
             "feature_match":True,"kernel_expr_hash64_advisory":raw_row["kernel_expr_hash64_advisory"],
             "probe_sha256":v.sha(lean.encode()),"proof_authority":False,
             "applicability_certified":False,"candidate_generation_allowed":False,"axiom_audit":"NOT_AUDITED"}
    v.save(folder/"receipt.json",receipt)
    raw.unlink()
    print("KUUOS_OLEAN_R8_EXACT",json.dumps({k:z for k,z in receipt.items() if k!="row"},sort_keys=True),flush=True)
    return receipt

def controls(db,receipt,head):
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        old=[
            (v.SELECTED[v.F112+"nativeK5BPNonerasing_no_singleton_BG"][0],
             v.F112+"nativeK5BPNonerasing_no_singleton_BG"),
            (v.SELECTED[v.LEC+"nativeF55_twoChart_constant_raw_global"][0],
             v.LEC+"nativeF55_twoChart_constant_raw_global"),
        ]
        # Choose bounded deterministic controls from actual new R7 rows,
        # not from a synthetic theorem or a generated source preview.
        newer=[]
        for shape in ("NEGATIVE_HEAD","OTHER_OR_UNFOLDED"):
            found=None
            for (text,) in con.execute("SELECT row_json FROM theorem_types WHERE type_sha IS NULL AND shape=? "
                                       "ORDER BY length(row_json),module,name",(shape,)):
                row=json.loads(text)
                if (row["type_constants"] and row["binder_count"]<=4
                        and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*",row["name"])
                        and not row["name"].startswith("_private.")):
                    found=(row["module"],row["name"]);break
            v.need(found is not None,"no actual feature-only control")
            newer.append(found)
        missing=con.execute("SELECT module FROM modules WHERE state='HOLD_MISSING_OLEAN' ORDER BY module LIMIT 1").fetchone()[0]
        duplicates=con.execute("SELECT name FROM theorem_types GROUP BY name HAVING COUNT(*)>1 ORDER BY name").fetchall()
        gaps=[json.loads(x[0]) for x in con.execute("SELECT row_json FROM modules WHERE state LIKE 'HOLD%' ORDER BY module")]
    finally:
        con.close()
    v.need(len(gaps)==695 and len(duplicates)==1,"R7 gap or ambiguity inventory changed")
    selection=[{"module":m,"name":n} for m,n in old+newer]
    terms=[s["name"] for s in selection]
    plan=prepare(db,receipt,R7_RECEIPT,head,terms,"R8 selected prior proof and obstruction inspection",selection)
    v.need(plan["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" and len(plan["requests"])==4
           and len(plan["search"]["unobserved_modules"])==695
           and plan["search"]["omitted_matches"]==0 and not plan["candidate_generation_allowed"],
           "exact search-to-materialization boundary failed")
    v.need(sum(x["complete_type_already_indexed"] for x in plan["requests"])==2,
           "old/new control distinction lost")
    wrong=copy.deepcopy(receipt);wrong["raw_type_count"]+=1
    checks={
      "tampered_receipt":exact_lookup(db,wrong,R7_RECEIPT,head,*old[0]),
      "missing_module":exact_lookup(db,receipt,R7_RECEIPT,head,missing,"unknown"),
      "unknown_declaration":exact_lookup(db,receipt,R7_RECEIPT,head,old[0][0],"unknown"),
      "ambiguous_without_module":exact_lookup(db,receipt,R7_RECEIPT,head,"",duplicates[0][0]),
      "suffix_not_exact":exact_lookup(db,receipt,R7_RECEIPT,head,old[0][0],old[0][1].rsplit(".",1)[-1]),
      "selection_outside_search":prepare(db,receipt,R7_RECEIPT,head,[old[0][1]],"negative only",
                                         [{"module":old[1][0],"name":old[1][1]}]),
    }
    expected={"tampered_receipt":"HOLD_INVALID_INDEX","missing_module":"HOLD_MISSING_OLEAN",
              "unknown_declaration":"HOLD_EXACT_DECLARATION_NOT_FOUND",
              "ambiguous_without_module":"HOLD_EXACT_MODULE_AND_NAME_REQUIRED",
              "suffix_not_exact":"HOLD_EXACT_DECLARATION_NOT_FOUND",
              "selection_outside_search":"HOLD_SELECTION_OUTSIDE_SEARCH_OR_DUPLICATE"}
    v.need(all(checks[k]["status"]==z and not checks[k]["candidate_generation_allowed"]
               for k,z in expected.items()),"adversarial exact lookup control failed")
    # This is a descriptive coverage split, not a claim that missing modules
    # are outside the library or cannot build.
    missing_paths=Counter(path["path"].split("/",1)[0] for x in gaps for path in x["sources"])
    return plan,checks,dict(sorted(missing_paths.items()))

def direct(head,index,out,module=None,name=None):
    receipt,db=admit(index,head)
    obs,cat,inv=v.snapshot(head)
    sources=r5.r2.module_sources(cat)
    out.mkdir(parents=True,exist_ok=False)
    if module is not None or name is not None:
        request=exact_lookup(db,receipt,R7_RECEIPT,head,module,name)
        v.save(out/"selection.json",request)
        if request["status"]!="EXACT_OLEAN_MATERIALIZATION_REQUIRED":
            print("KUUOS_OLEAN_R8_HOLD",request["status"],flush=True)
            return None
        requests=[request];checks={};missing_paths={}
    else:
        plan,checks,missing_paths=controls(db,receipt,head)
        v.save(out/"search-plan.json",plan)
        v.save(out/"adversarial-controls.json",checks)
        requests=plan["requests"]
    env=r5.fixed_lean()
    results=[]
    for i,request in enumerate(requests):
        folder=out/f"exact-{i+1:02}"
        try:
            result=materialize(folder,request,sources,env)
        except (OSError,ValueError,RuntimeError) as exc:
            v.save(folder/"hold.json",{"status":"HOLD_EXACT_TYPE_READ_FAILURE","reason":str(exc),
                                       "module":request["module"],"name":request["name"],
                                       "proof_authority":False,"candidate_generation_allowed":False})
            raise
        results.append(result)
    v.need(v.github_observation(head,"canonical_main")==obs,"source changed")
    stable={"schema":"kuuos.codeai.olean-exact-materialization.v1-r8",
            "status":"EXACT_TYPE_MATERIALIZATION_OBSERVED","source_head":head,"source_tree":obs["source_tree"],
            "scope_digest":v.SCOPE,"r7_receipt_digest":R7_RECEIPT,"r7_database_sha256":R7_DB,
            "selected_count":len(results),"old_full_type_matches":sum(r["old_full_type_digest_matched"] for r in results),
            "new_full_type_count":sum(not r["old_full_type_digest_matched"] for r in results),
            "selections":[{k:z for k,z in r.items() if k!="row"} for r in results],
            "adversarial_controls":{k:z["status"] for k,z in checks.items()},
            "missing_olean_modules":695,"missing_olean_source_prefix_counts":missing_paths,
            "proof_authority":False,"applicability_certified":False,"candidate_generation_allowed":False,
            "fresh_axiom_audit":False,"fresh_mcp_executed":False}
    v.save(out/"direct.json",stable)
    print("KUUOS_OLEAN_R8_DIRECT_GREEN",json.dumps({**stable,"digest":v.digest(stable)},sort_keys=True),flush=True)
    return stable

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True);p.add_argument("--index",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--first",type=Path)
    p.add_argument("--module");p.add_argument("--name")
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    d=direct(a.head,a.index,out,a.module,a.name)
    if a.first is not None:
        v.need(d is not None and d==r5.load(a.first/"direct.json"),"independent exact type receipt differs")
        result={"status":"INDEPENDENT_OLEAN_R8_GREEN","direct_digest":v.digest(d),
                "selected_count":d["selected_count"],"new_full_type_count":d["new_full_type_count"],
                "proof_authority":False,"applicability_certified":False,"candidate_generation_allowed":False}
        v.save(out/"independent.json",result)
        print("KUUOS_OLEAN_R8_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
