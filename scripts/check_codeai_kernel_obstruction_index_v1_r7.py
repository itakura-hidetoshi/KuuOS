#!/usr/bin/env python3
"""R7: full canonical source inventory, partitioned raw olean discovery.

Reuse the independently observed R5 rows ONLY after exact scope, receipt,
source and olean bytes agree. Read remaining compiled files, never import
project modules. Isolate failed batches; preserve missing/unreadable modules
and every lexical hint. Independent runners replay only the new observations.
Aggregate a searchable SQLite catalog without proof or admission authority.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess

import check_codeai_kernel_obstruction_index_v1_r5 as r5
import codeai_olean_bounded_features_v1 as features
v = r5.v
ROOT = v.ROOT
LOAD = r5.load
R5_HEAD = "6d2260fb9ffb18ee715b766327339b627ca9742e"
R5_RUN = 45762151506
R5_DIRECT = "f631971c54dfac73eb2669ef1459003d1293aa9df5dd7108a360ec5e5904b2d3"
R5_TYPES = "80e538ecfa4574b09d67c5896febf97bc9df36211124bf589cc8ac5078c1d1bd"
R5_ARTIFACTS = (
    (15091050061, "codeai-olean-r5-local-45762151506-1",
     "sha256:2cc0c8d1a54153e4b9c062d053dc4b7b6fdf5954d5a17c37b22f58999f89f917"),
    (15090471930, "codeai-olean-r5-independent-45762151506-1",
     "sha256:4c72515f7e1c98c1fa9933124c5f769ffa1ad0b150d6c3f0001bac7f18291e19"),
)
PARTITIONS = 4
SCHEMA = "kuuos.codeai.kernel-obstruction-index.partitioned.v1-r7"
READ = ("R2_IMPORTED_TYPE_EQUAL", "RAW_OLEAN_TYPE_OBSERVED_readModuleData",
        "RAW_OLEAN_TYPE_OBSERVED_readModuleDataParts")

def reference(local, independent, head):
    run = v.cache.api("actions/runs/" + str(R5_RUN))
    v.need(run["head_sha"] == R5_HEAD and run["status"] == "completed"
           and run["conclusion"] == "success" and run["run_attempt"] == 1, "R5 run not certified")
    for aid, name, digest in R5_ARTIFACTS:
        a = v.cache.api("actions/artifacts/" + str(aid))
        v.need(a["id"] == aid and a["name"] == name and a["digest"] == digest and not a["expired"]
               and a["workflow_run"]["id"] == R5_RUN and a["workflow_run"]["head_sha"] == R5_HEAD,
               "R5 artifact identity mismatch")
    first, second = LOAD(local/"direct.json"), LOAD(independent/"direct.json")
    replay = LOAD(independent/"independent.json")
    rows, rows2 = LOAD(local/"kernel-index.json"), LOAD(independent/"kernel-index.json")
    coverage, coverage2 = LOAD(local/"module-coverage.json"), LOAD(independent/"module-coverage.json")
    v.need(first == second and v.digest(first) == R5_DIRECT and first["source_head"] == head
           and first["scope_digest"] == v.SCOPE and first["r2_direct_digest"] == r5.R2_DIRECT
           and first["r2_mcp_digest"] == r5.R2_MCP and rows == rows2 and len(rows) == 2390
           and v.digest(rows) == R5_TYPES and coverage == coverage2
           and v.digest(coverage) == first["coverage_digest"]
           and replay["status"] == "INDEPENDENT_OLEAN_R5_GREEN"
           and replay["direct_digest"] == R5_DIRECT, "R5 reference receipt mismatch")
    batches = sorted(local.glob("batch-*/receipt.json"))
    receipts = [LOAD(p) for p in batches]
    v.need([v.digest(z) for z in receipts] == first["batch_receipt_digests"], "R5 batch receipt drift")
    bindings = {}
    for path, rec in zip(batches, receipts):
        for artifact in rec["artifact_bindings"]:
            m = artifact["module"]
            v.need(m not in bindings, "duplicate R5 module binding")
            bindings[m] = (artifact, path.parent.name)
    old = {x["module"]:x for x in coverage if x["state"] in READ}
    v.need(len(old) == 67 and set(old) == set(bindings), "R5 observed coverage differs")
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["module"]].append(row)
    v.need(set(grouped) <= set(old) and all(len(grouped[m]) == x["type_count"] for m,x in old.items()),
           "R5 module row count differs")
    return old, bindings, grouped

def partition_of(module):
    # Sorted hash partition is stable across machines and independent of
    # lexical hint ranking, with no module left out of the manifest.
    return int(v.sha(module.encode())[:8], 16) % PARTITIONS

def bind(module, sources):
    if len(sources[module]) != 1:
        return None, "HOLD_AMBIGUOUS_SOURCE"
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", module):
        return None, "HOLD_UNSUPPORTED_MODULE_PATH"
    base = ROOT/".lake/build/lib/lean"/(module.replace(".","/")+".olean")
    return r5.bind_files(module, base, sources[module][0])

def read_partition(head, out, part, local, independent):
    obs, cat, inv = v.snapshot(head)
    sources = r5.r2.module_sources(cat)
    old, bindings, grouped = reference(local, independent, head)
    modules = [m for m in sorted(sources) if partition_of(m) == part]
    v.need(modules and len(sources) == 2815, "canonical module inventory changed")
    hints = [h for h in inv["hints"] if partition_of(h["module"]) == part]
    counts = Counter(h["module"] for h in hints)
    v.need(all(h["module"] in sources for h in hints), "lexical hint without source module")
    out.mkdir(parents=True, exist_ok=False)
    v.save(out/"partition-plan.json", {"partition":part,"modules":modules,"lexical_ids":[h["id"] for h in hints]})
    env = r5.fixed_lean()
    rows=[]; states={}; origins={}; artifacts={}; failures=[]; receipts=[]
    for m in modules:
        artifact,hold = bind(m,sources)
        if m in old:
            expected, batch = bindings[m]
            v.need(hold is None and artifact == expected and sources[m] == old[m]["sources"],
                   "R5 reused artifact or source changed:"+m)
            rows.extend(grouped[m])
            states[m] = "REUSED_R5_TYPE_OBSERVATION"
            origins[m] = {"kind":"R5", "artifact_id":R5_ARTIFACTS[0][0],
                          "batch":batch,"binding":artifact}
        elif hold is not None:
            states[m]=hold
        else:
            artifacts[m]=artifact
    # Reobserve a small previously certified frontier using the compact
    # feature path. Preserve the exact R5 rows; compare every feature.
    calibration=[]
    for m in r5.r2.MODULES:
        if m in modules:
            bound=bindings[m][0]
            observed,rec=features.run_batch(out/("calibration-"+str(len(calibration)+1)),
                                            [m],sources,{m:bound},env)
            v.need(features.compare_features(observed,grouped[m]),"R5 feature calibration differs:"+m)
            calibration.append({"module":m,"types":len(observed),"receipt_digest":v.digest(rec)})
    v.save(out/"calibration.json",calibration)
    serial=0
    def visit(group):
        nonlocal serial
        serial += 1
        path=out/f"batch-{serial:04}"
        try:
            new,rec=features.run_batch(path,group,sources,artifacts,env)
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            # Keep full generated source/logs and parent failure. Bisect
            # failed batches, never infer an OOM or a no-go from failure.
            diagnostic={"batch":path.name,"modules":group,"error_class":type(exc).__name__}
            failures.append(diagnostic)
            v.save(path/"failure.json",diagnostic)
            if len(group)>1:
                mid=len(group)//2
                visit(group[:mid]);visit(group[mid:])
            else:
                states[group[0]]="HOLD_OLEAN_READ_FAILURE"
                origins[group[0]]={"kind":"failed","batch":path.name}
            return
        rows.extend(new);receipts.append({"batch":path.name,"receipt_digest":v.digest(rec)})
        for m in rec["modules"]:
            name=m["module"]
            states[name]="RAW_OLEAN_FEATURES_OBSERVED_"+m["mode"]
            origins[name]={"kind":"R7","batch":path.name,"binding":artifacts[name]}
    for group in features.batches([m for m in modules if m in artifacts],artifacts):
        visit(group)
    rows.sort(key=lambda x:(x["module"],x["name"]))
    v.need(len({(x["module"],x["name"]) for x in rows})==len(rows)
           and set(states)==set(modules),"partition accounting incomplete")
    n=Counter(x["module"] for x in rows)
    coverage=[{"module":m,"sources":sources[m],"state":states[m],
               "type_count":n[m],"lexical_hint_count":counts[m],"origin":origins.get(m)}
              for m in modules]
    joined,unmatched=features.reconcile({"hints":hints,"hint_count":len(hints)},rows)
    v.need(len(joined)==len(hints),"partition lexical inventory lost")
    v.save(out/"kernel-index.json",rows)
    v.save(out/"module-coverage.json",coverage)
    v.save(out/"lexical-join.json",joined)
    v.save(out/"unmatched-negative-types.json",unmatched)
    v.save(out/"failures.json",failures)
    v.need(v.github_observation(head,"canonical_main")==obs,"source changed")
    stable={"schema":SCHEMA,"partition":part,"partition_count":PARTITIONS,
            "source_head":head,"source_tree":obs["source_tree"],"scope_digest":v.SCOPE,
            "r5_direct_digest":R5_DIRECT,"r5_type_digest":R5_TYPES,
            "source_module_count":len(sources),"partition_modules":len(modules),
            "module_inventory_digest":v.digest(modules),
            "state_counts":dict(sorted(Counter(x["state"] for x in coverage).items())),
            "raw_type_count":len(rows),"raw_type_digest":v.digest(rows),
            "reused_type_count":sum(n[m] for m in modules if m in old),
            "coverage_digest":v.digest(coverage),"lexical_hint_count":len(joined),
            "lexical_join_digest":v.digest(joined),"unmatched_negative_digest":v.digest(unmatched),
            "batch_receipts":receipts,"failures_digest":v.digest(failures),
            "calibration":calibration,"full_type_rows":sum(r["type_expr_sha256"] is not None for r in rows),
            "feature_only_rows":sum(r["type_expr_sha256"] is None for r in rows),
            "read_failure_count":sum(x["state"]=="HOLD_OLEAN_READ_FAILURE" for x in coverage),
            "project_imports":False,"proof_authority":False,"applicability_certified":False,
            "semantic_search_complete":False}
    v.save(out/"direct.json",stable)
    print("KUUOS_OLEAN_R7_PARTITION_GREEN",json.dumps({**stable,"digest":v.digest(stable)},sort_keys=True),flush=True)
    return stable

def compact(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def aggregate(head,out,local,independent,run,attempt):
    obs,cat,inv=v.snapshot(head)
    sources=r5.r2.module_sources(cat)
    out.mkdir(parents=True,exist_ok=False)
    db=out/"kernel-recall.sqlite"
    con=sqlite3.connect(db)
    con.executescript("""
      CREATE TABLE modules(module TEXT PRIMARY KEY, state TEXT NOT NULL, row_json TEXT NOT NULL);
      CREATE TABLE theorem_types(module TEXT NOT NULL, name TEXT NOT NULL, type_sha TEXT,
        shape TEXT NOT NULL, search_text TEXT NOT NULL, row_json TEXT NOT NULL, PRIMARY KEY(module,name));
      CREATE TABLE hints(id TEXT PRIMARY KEY, module TEXT NOT NULL, search_text TEXT NOT NULL, row_json TEXT NOT NULL);
      CREATE INDEX theorem_name_idx ON theorem_types(name);
      CREATE INDEX theorem_shape_idx ON theorem_types(shape);
      CREATE INDEX hint_module_idx ON hints(module);
    """)
    hints={h["id"]:h for h in inv["hints"]}
    seen=set(); seen_hints=set(); totals=Counter(); parts=[]; raw_count=0; reused=0; feature_count=0; calibration_count=0
    for i in range(PARTITIONS):
        a=local/f"codeai-olean-r7-local-{i}-{run}-{attempt}"
        b=independent/f"codeai-olean-r7-independent-{i}-{run}-{attempt}"
        direct=LOAD(a/"direct.json")
        replay=LOAD(b/"independent.json")
        v.need(LOAD(b/"direct.json")==direct and direct["partition"]==i
               and direct["schema"]==SCHEMA and direct["source_head"]==head
               and direct["source_tree"]==obs["source_tree"] and direct["scope_digest"]==v.SCOPE
               and direct["r5_direct_digest"]==R5_DIRECT and replay["status"]=="INDEPENDENT_OLEAN_R7_PARTITION_GREEN"
               and replay["direct_digest"]==v.digest(direct),"independent partition mismatch")
        rows=LOAD(a/"kernel-index.json");coverage=LOAD(a/"module-coverage.json");joined=LOAD(a/"lexical-join.json")
        unmatched=LOAD(a/"unmatched-negative-types.json")
        v.need(v.digest(rows)==direct["raw_type_digest"] and len(rows)==direct["raw_type_count"]
               and v.digest(coverage)==direct["coverage_digest"]
               and v.digest(joined)==direct["lexical_join_digest"]
               and v.digest(unmatched)==direct["unmatched_negative_digest"],"partition artifact digest mismatch")
        expected=[m for m in sorted(sources) if partition_of(m)==i]
        v.need([x["module"] for x in coverage]==expected and len(coverage)==direct["partition_modules"]
               and v.digest(expected)==direct["module_inventory_digest"],"partition coverage mismatch")
        n=Counter(x["module"] for x in rows)
        for m in coverage:
            k=m["module"]
            v.need(k not in seen and m["sources"]==sources[k] and m["type_count"]==n[k],
                   "module provenance mismatch")
            seen.add(k);totals[m["state"]]+=1
            con.execute("INSERT INTO modules VALUES(?,?,?)",(k,m["state"],compact(m)))
        v.need(set(n)<=set(expected),"row outside partition")
        for row in rows:
            module,name=row["module"],row["name"]
            hay=v.lex.norm(" ".join([module,name,row["conclusion_head"],*row["type_constants"]]))
            con.execute("INSERT INTO theorem_types VALUES(?,?,?,?,?,?)",
                        (module,name,row["type_expr_sha256"],row["shape"],hay,compact(row)))
        for j in joined:
            k=j["lexical_id"];h=hints[k]
            v.need(k not in seen_hints and h["module"] in expected and j["source_blob"]==h["source_blob"],
                   "lexical provenance mismatch")
            seen_hints.add(k)
            hay=v.lex.norm(" ".join([h["name_lexical"],h["signature_preview"],h["path"]]))
            con.execute("INSERT INTO hints VALUES(?,?,?,?)",(k,h["module"],hay,compact({"hint":h,"join":j})))
        con.commit()
        raw_count+=len(rows);reused+=direct["reused_type_count"]
        feature_count+=direct["feature_only_rows"];calibration_count+=sum(x["types"] for x in direct["calibration"])
        v.need(direct["full_type_rows"]+direct["feature_only_rows"]==len(rows),"representation count mismatch")
        parts.append({"partition":i,"direct_digest":v.digest(direct),"raw_type_digest":direct["raw_type_digest"],
                      "coverage_digest":direct["coverage_digest"],"lexical_join_digest":direct["lexical_join_digest"],
                      "local_artifact":a.name,"independent_artifact":b.name})
    v.need(seen==set(sources) and seen_hints==set(hints) and len(seen)==2815 and len(seen_hints)==6380
           and reused==2390 and calibration_count==124 and feature_count==raw_count-reused,"whole-source accounting incomplete")
    duplicate_names=con.execute("SELECT name,COUNT(*) FROM theorem_types GROUP BY name HAVING COUNT(*)>1 ORDER BY name").fetchall()
    negative_count=con.execute("SELECT COUNT(*) FROM theorem_types WHERE shape IN ('FALSE_TAIL','NEGATIVE_HEAD','NESTED_NEGATIVE_MARKER','NEGATIVE_BINDER_ONLY')").fetchone()[0]
    v.need(con.execute("PRAGMA integrity_check").fetchone()[0]=="ok","SQLite integrity check failed")
    con.close()
    v.save(out/"ambiguous-global-names.json",duplicate_names)
    receipt={"schema":SCHEMA,"status":"INDEPENDENT_PARTITIONED_INDEX_ACCOUNTED",
             "source_head":head,"source_tree":obs["source_tree"],"scope_digest":v.SCOPE,
             "run_id":int(run),"run_attempt":int(attempt),"r5_direct_digest":R5_DIRECT,
             "partitions":parts,"partition_digest":v.digest(parts),"source_module_count":len(seen),
             "state_counts":dict(sorted(totals.items())),"raw_type_count":raw_count,"reused_r5_types":reused,
             "new_type_count":raw_count-reused,"new_feature_only_count":feature_count,"r5_full_type_count":reused,
             "calibration_types":calibration_count,"negative_syntax_count":negative_count,
             "lexical_hint_count":len(seen_hints),"ambiguous_global_name_count":len(duplicate_names),
             "parse_gaps":inv["parse_gaps"],"database_sha256":r5.filehash(db),
             "proof_authority":False,"applicability_certified":False,
             "all_axioms_audited":False,"semantic_search_complete":False,
             "all_module_types_observed":False,
             "all_module_features_observed":not any(k.startswith("HOLD") and n for k,n in totals.items())}
    v.save(out/"aggregate.json",receipt)
    # Exercise the exact runtime preflight used by the next candidate search.
    from runtime.kuuos_codeai_olean_obstruction_preflight_v1 import recall
    expected=v.digest(receipt)
    controls={}
    for key,terms in {"negative":["nativeK5BPNonerasing_no_singleton_BG"],
                      "positive":["nativeF55_twoChart_constant_raw_global"],
                      "miss":["kuuosunmatchedcontrol9f3b7d"]}.items():
        result=recall(db,receipt,expected,head,terms,target="R7 control "+key)
        v.need(result["candidate_generation_allowed"] is False and not result["proof_authority"],
               "preflight promoted discovery")
        controls[key]=result
    v.need(any(x["name"].endswith("nativeK5BPNonerasing_no_singleton_BG")
               and x["shape"]=="NEGATIVE_HEAD" for x in controls["negative"]["type_matches"]),
           "negative control not found")
    v.need(any(x["name"].endswith("nativeF55_twoChart_constant_raw_global")
               and x["shape"]=="OTHER_OR_UNFOLDED" for x in controls["positive"]["type_matches"]),
           "positive control not retained")
    v.need(controls["miss"]["status"]=="HOLD_NO_DATA","miss was promoted")
    v.need(all(x.get("candidate_generation_allowed") is False for x in controls.values()),"discovery authority leak")
    v.save(out/"recall-controls.json",controls)
    print("KUUOS_OLEAN_R7_AGGREGATE",json.dumps({**receipt,"receipt_digest":expected},sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--part",type=int)
    p.add_argument("--r5-local",type=Path)
    p.add_argument("--r5-independent",type=Path)
    p.add_argument("--first",type=Path)
    p.add_argument("--aggregate",action="store_true")
    p.add_argument("--local",type=Path)
    p.add_argument("--independent",type=Path)
    p.add_argument("--run")
    p.add_argument("--attempt")
    a=p.parse_args()
    out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    if a.aggregate:
        aggregate(a.head,out,a.local,a.independent,a.run,a.attempt)
        return
    v.need(a.part is not None and 0<=a.part<PARTITIONS,"invalid partition")
    d=read_partition(a.head,out,a.part,a.r5_local,a.r5_independent)
    if a.first is not None:
        v.need(d==LOAD(a.first/"direct.json"),"independent partition differs")
        receipt={"status":"INDEPENDENT_OLEAN_R7_PARTITION_GREEN","partition":a.part,
                 "direct_digest":v.digest(d),"raw_type_digest":d["raw_type_digest"],
                 "state_counts":d["state_counts"],"proof_authority":False,"applicability_certified":False}
        v.save(out/"independent.json",receipt)
        print("KUUOS_OLEAN_R7_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
