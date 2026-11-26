#!/usr/bin/env python3
"""Bounded olean structural feature reader.

Never expand reprStr of the entire Expr. A new row is a discovery record
for an exact compiled object and declaration, not a complete type digest.
Retain source and file hashes so the full original Expr is recoverable.
Use the fixed Lean getUsedConstants and binder/conclusion classifiers.
"""
from __future__ import annotations
from collections import Counter
import gzip
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

import check_codeai_kernel_obstruction_index_v1_r5 as r5
v=r5.v
ROOT=v.ROOT
MARK="KUUOS_OLEAN_FEATURE_EXPORT"
LIMIT_RSS=4*1024**2  # KiB; parent Python remains outside this child cap
LIMIT_RAW=64*1024**2
TIMEOUT=90
BATCH_SIZE=12
BATCH_BYTES=24*1024**2

ROW=r'''
def theoremRow (name : Name) (moduleName : String) (info : ConstantInfo) : Json :=
  let (domains, conclusion) := peel info.type
  Json.mkObj [
    ("name", toJson name.toString),
    ("module", toJson moduleName),
    ("kernel_expr_hash64_advisory", toJson (toString info.type.hash)),
    ("universe_parameters", toJson (info.levelParams.map Name.toString)),
    ("type_constants", toJson (info.type.getUsedConstants.map Name.toString)),
    ("binder_domains", toJson (domains.map binderRow)),
    ("conclusion_head", toJson (headName conclusion)),
    ("conclusion_negative_head", toJson (negativeHead conclusion)),
    ("conclusion_negative_marker", toJson (negativeMarker conclusion)),
    ("conclusion_constants", toJson (conclusion.getUsedConstants.map Name.toString)),
    ("unresolved_type", toJson (info.type.hasMVar || info.type.hasFVar || info.type.hasLooseBVars))]
'''

def batches(modules,artifacts):
    group=[];size=0
    for m in modules:
        weight=sum(f["bytes"] for f in artifacts[m]["files"])
        if group and (len(group)>=BATCH_SIZE or size+weight>BATCH_BYTES):
            yield group
            group=[];size=0
        group.append(m);size+=weight
    if group:yield group

def rss(pid):
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    except (OSError,ValueError,IndexError):
        pass
    return 0

def run_bounded(folder,probe,raw,env):
    log=folder/"export.log"
    start=time.monotonic();peak=0;reason=None
    with log.open("w",encoding="utf-8") as f:
        p=subprocess.Popen(["lean",str(probe.relative_to(ROOT))],cwd=ROOT,env=env,
                           stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
        try:
            while p.poll() is None:
                peak=max(peak,rss(p.pid))
                if peak>LIMIT_RSS: reason="RSS_LIMIT";break
                if raw.exists() and raw.stat().st_size>LIMIT_RAW:reason="RAW_BYTES_LIMIT";break
                if time.monotonic()-start>TIMEOUT:reason="TIME_LIMIT";break
                time.sleep(.05)
        finally:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGKILL)
                except ProcessLookupError:pass
            p.wait()
    v.save(folder/"resource.json",{"peak_rss_sample_kib":peak,"elapsed_seconds":round(time.monotonic()-start,3),
                                   "exit_code":p.returncode,"limit_reason":reason})
    if reason or p.returncode:
        print("KUUOS_OLEAN_FEATURE_LIMIT",folder.name,reason,p.returncode,peak,flush=True)
        raise ValueError("bounded reader failed:"+str(reason or p.returncode))
    v.need(raw.is_file() and raw.stat().st_size<=LIMIT_RAW,"missing or excessive raw output")
    msg=log.read_text(encoding="utf-8")
    v.need(not re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked)",msg),"Lean reader diagnostics")
    return msg

def read_rows(raw,meta,modules,sources,artifacts,folder):
    rows=[];seen=set()
    with raw.open(encoding="utf-8") as stream,gzip.open(folder/"kernel-types.jsonl.gz","wt",encoding="utf-8") as gz:
        for line in stream:
            x=json.loads(line);m=x["module"];name=x["name"]
            v.need(m in modules and (m,name) not in seen and x["unresolved_type"] is False,
                   "unresolved or duplicate declaration")
            seen.add((m,name))
            v.need(isinstance(x["kernel_expr_hash64_advisory"],str) and x["kernel_expr_hash64_advisory"].isdigit(),
                   "missing advisory kernel hash")
            ds=x["binder_domains"];head=x["conclusion_head"]
            neg=x["conclusion_negative_head"];nested=x["conclusion_negative_marker"]
            v.need(type(neg) is bool and type(nested) is bool and neg==(head in v.MARKER),"negative head inconsistent")
            nhead=sum(d["negative_head"] is True for d in ds)
            nmark=sum(d["negative_marker"] is True for d in ds)
            v.need(nhead<=nmark,"negative binder marker lost")
            shape=("FALSE_TAIL" if head=="False" else "NEGATIVE_HEAD" if neg else
                   "NESTED_NEGATIVE_MARKER" if nested else "NEGATIVE_BINDER_ONLY" if nmark else "OTHER_OR_UNFOLDED")
            if head in ("let","metadata","bound-variable","projection","other","lambda","forall"):
                shape="UNRESOLVED_CONCLUSION_SHAPE"
            row={k:x[k] for k in ("name","module","universe_parameters","binder_domains",
                                  "conclusion_head","conclusion_negative_head","conclusion_negative_marker")}
            row.update(type_expr_sha256=None,kernel_expr_hash64_advisory=x["kernel_expr_hash64_advisory"],
                       type_constants=sorted(set(x["type_constants"])),conclusion_constants=sorted(set(x["conclusion_constants"])),
                       binder_count=len(ds),negative_binder_heads=nhead,negative_binder_markers=nmark,shape=shape,
                       source_candidates=sources[m],source_mapping="UNIQUE_MODULE_PATH",
                       applicability_certified=False,axiom_audit="NOT_AUDITED_BY_FEATURE_INDEX",
                       full_type_materialized=False,observation_kind="OLEAN_TYPE_FEATURES",
                       artifact_binding_digest=v.digest(artifacts[m]))
            row["type_observation_sha256"]=v.digest(row)
            rows.append(row);gz.write(line)
    counts=Counter(x["module"] for x in rows)
    v.need(len(rows)==meta["selected_theorems"] and
           all(counts[m["module"]]==m["theorem_count"] for m in meta["modules"]),"feature inventory mismatch")
    return sorted(rows,key=lambda x:(x["module"],x["name"]))

def run_batch(folder,modules,sources,artifacts,env):
    folder.mkdir()
    wanted=folder/"modules.txt";meta_path=folder/"environment.json";raw=folder/"kernel-types.jsonl"
    wanted.write_text("".join(m+"\t"+"\t".join(f["path"] for f in artifacts[m]["files"])+"\n"
                              for m in modules),encoding="utf-8")
    old=v.TEMPLATE.read_text(encoding="utf-8")
    marker="def theoremRow "
    v.need(old.startswith("import KuuOSFormal\n") and old.count(marker)==1,"original type helpers changed")
    lean=old.split(marker,1)[0].replace("import KuuOSFormal\n","import Lean\n",1)+ROW+r5.TAIL.replace(r5.MARK,MARK)
    for key,path in (("__MODULE_FILE__",wanted),("__META_FILE__",meta_path),("__ROWS_FILE__",raw)):
        v.need(lean.count(key)==1,"unexpected placeholder")
        lean=lean.replace(key,path.relative_to(ROOT).as_posix())
    probe=folder/"OleanFeatures.lean";probe.write_text(lean,encoding="utf-8")
    msg=run_bounded(folder,probe,raw,env)
    meta=r5.load(meta_path)
    v.need([m["module"] for m in meta["modules"]]==modules
           and meta["selected_theorems"]==sum(m["theorem_count"] for m in meta["modules"])
           and f"{MARK} {meta['selected_theorems']}" in msg,"raw feature receipt incomplete")
    for m in meta["modules"]:
        expected="readModuleData" if len(artifacts[m["module"]]["files"])==1 else "readModuleDataParts"
        v.need(m["mode"]==expected,"unexpected reader mode")
    rows=read_rows(raw,meta,modules,sources,artifacts,folder)
    raw.unlink()
    for m in modules:
        for f in artifacts[m]["files"]:
            v.need(r5.filehash(ROOT/f["path"])==f["sha256"],"artifact changed")
    v.save(folder/"kernel-index.json",rows)
    result={"modules":meta["modules"],"artifact_bindings":[artifacts[m] for m in modules],
            "type_digest":v.digest(rows),"type_count":len(rows),"probe_sha256":v.sha(lean.encode()),
            "representation":"OLEAN_TYPE_FEATURES_NOT_FULL_EXPR"}
    v.save(folder/"receipt.json",result)
    print("KUUOS_OLEAN_FEATURE_BATCH",json.dumps({"modules":len(modules),"type_count":len(rows),
             "type_digest":result["type_digest"]},sort_keys=True),flush=True)
    return rows,result

def compare_features(new,old):
    keys=("module","name","universe_parameters","binder_domains","conclusion_head","conclusion_negative_head",
          "conclusion_negative_marker","type_constants","conclusion_constants","binder_count",
          "negative_binder_heads","negative_binder_markers","shape","source_candidates","source_mapping")
    return [{k:r[k] for k in keys} for r in new]==[{k:r[k] for k in keys} for r in old]

def reconcile(inv,rows):
    # R5 rows retain their original exact expression digests. R7 rows use
    # separate observation identifiers; never pass these as Expr digests.
    from collections import defaultdict
    by_module=defaultdict(lambda:defaultdict(list))
    for r in rows:
        pieces=r["name"].split(".")
        for i in range(len(pieces)):
            by_module[r["module"]][".".join(pieces[i:])].append(r)
    def hint(r):
        return {"name":r["name"],"type_expr_sha256":r["type_expr_sha256"],
                "type_observation_sha256":r.get("type_observation_sha256"),
                "shape":r["shape"],"full_type_materialized":r["type_expr_sha256"] is not None}
    joined=[];potential=set()
    for h in inv["hints"]:
        found=by_module[h["module"]].get(h["name_lexical"],[])
        potential.update((r["module"],r["name"]) for r in found)
        joined.append({"lexical_id":h["id"],"path":h["path"],"source_blob":h["source_blob"],
                       "name_lexical":h["name_lexical"],"candidates":[hint(r) for r in found],
                       "status":"POTENTIAL_KERNEL_MATCH" if len(found)==1 else "HOLD_AMBIGUOUS" if found else "HOLD_NO_KERNEL_MATCH",
                       "applicability_certified":False})
    v.need(len(joined)==inv["hint_count"],"lexical inventory lost")
    unmatched=[{"module":r["module"],**hint(r)} for r in rows
               if r["shape"] in ("NEGATIVE_HEAD","FALSE_TAIL","NESTED_NEGATIVE_MARKER","NEGATIVE_BINDER_ONLY")
               and (r["module"],r["name"]) not in potential]
    return joined,unmatched
