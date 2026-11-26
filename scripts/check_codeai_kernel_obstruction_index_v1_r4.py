#!/usr/bin/env python3
"""R4: verified-artifact-only Lean .olean reader, without importing project modules.

Use readModuleData for ordinary files and readModuleDataParts for the complete
exported/server/private prefix. Select the private ModuleData, not a union of
overlapping levels. Keep all types, origins and unresolved coverage. Raw
discovery cannot admit a proof, refute a goal or replace Lean applicability.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

import check_codeai_kernel_obstruction_index_v1_r2 as r2
v = r2.v
ROOT = v.ROOT
R2_HEAD = "07aad79f93f7ec14a02c2a0ba830ab127fb68516"
R2_RUN = 45752056242
R2_DIRECT = "778616a511407b854dd105c1613f436196020831b16be54579f95559aa3fc60c"
R2_TYPES = "25a1497c8b2a2e8418e34718e153be1660d2593a1fe2628b22f23230ded716ff"
R2_MCP = "0321687c37f70efb5475d209a9b3c3ffaf94a28e5e64c9a551f3aa648760458c"
R2_ARTIFACTS = (
    (15085633941, "codeai-kernel-obstruction-r2-local-45752056242-1",
     "sha256:b51c54f794b1d4fad63ea822241ff36606fc9f31eec4c472aab12e3078a46660"),
    (15086730463, "codeai-kernel-obstruction-r2-independent-45752056242-1",
     "sha256:48906a525088210fd94340cc23bdbb4affebaceb6dfa9a8c3bba5e508d57d12b"),
)
SCHEMA = "kuuos.codeai.kernel-obstruction-index.verified-olean.v1-r4"
BATCH = 16
MAX_BATCH_BYTES = 96 * 1024**2
MARK = "KUUOS_OLEAN_R4_EXPORT"
TAIL = r'''
set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
run_cmd do
  Lean.Elab.Command.liftIO do
    let manifest ← IO.FS.readFile "__MODULE_FILE__"
    let (modules, count) ←
      IO.FS.withFile "__ROWS_FILE__" .write fun handle => do
        let mut modules : Array Json := #[]
        let mut count : Nat := 0
        for entry in manifest.splitOn "\n" do
          unless entry.isEmpty do
            let (moduleName, data, mode) ←
              match entry.splitOn "\t" with
              | [moduleName, path] => do
                let (data, _region) ← Lean.readModuleData (System.FilePath.mk path)
                if data.isModule then
                  throw <| IO.userError s!"missing complete module parts: {moduleName}"
                pure (moduleName, data, "readModuleData")
              | [moduleName, exported, server, priv] => do
                let parts ← Lean.readModuleDataParts #[
                  System.FilePath.mk exported, System.FilePath.mk server, System.FilePath.mk priv]
                if parts.size != 3 then
                  throw <| IO.userError s!"incomplete module parts: {moduleName}"
                let data := parts[2]!.1
                unless data.isModule && parts[0]!.1.isModule && parts[1]!.1.isModule do
                  throw <| IO.userError s!"invalid module part levels: {moduleName}"
                pure (moduleName, data, "readModuleDataParts")
              | _ => throw <| IO.userError "malformed artifact manifest"
            unless data.constNames == data.constants.map (·.name) do
              throw <| IO.userError s!"constant name inventory mismatch: {moduleName}"
            let mut localCount : Nat := 0
            for info in data.constants do
              if info.isTheorem then
                handle.putStr ((theoremRow info.name moduleName info).compress ++ "\n")
                localCount := localCount + 1
            count := count + localCount
            modules := modules.push (Json.mkObj [
              ("module", toJson moduleName), ("mode", toJson mode),
              ("theorem_count", toJson localCount),
              ("constant_count", toJson data.constants.size)])
        return (modules, count)
    IO.FS.writeFile "__META_FILE__" ((Json.mkObj [
      ("modules", toJson modules), ("selected_theorems", toJson count)]).compress ++ "\n")
    IO.println s!"KUUOS_OLEAN_R4_EXPORT {count}"
end KuuOSKernelObstructionIndexProbe
'''

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def filehash(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def fixed_lean():
    env = dict(os.environ)
    env.pop("LEAN_PATH", None)
    version = subprocess.check_output(["lean", "--version"], cwd=ROOT, env=env, text=True)
    v.need(re.search(r"\bversion 4\.30\.0-rc2(?:,|\s)", version) is not None,
           "wrong Lean executable")
    return env

def lean_run(folder, argv, label, env, cwd=ROOT, timeout=300):
    log = folder / (label + ".log")
    timing = folder / (label + ".timing")
    if Path("/usr/bin/time").is_file():
        argv = ["/usr/bin/time", "-v", "-o", str(timing), *argv]
    start = time.monotonic()
    with log.open("w", encoding="utf-8") as f:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
    msg = log.read_text(encoding="utf-8")
    if proc.returncode or re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked)", msg):
        print(msg[-20000:], flush=True)
        raise ValueError("Lean raw reader failed: " + label)
    resource = next((x.strip() for x in timing.read_text().splitlines()
                     if "Maximum resident set size" in x), "NO_DATA") if timing.is_file() else "NO_DATA"
    print("KUUOS_OLEAN_R4_RESOURCE", label, round(time.monotonic() - start, 3), resource, flush=True)
    return msg

def r2_reference(local, independent, head):
    run = v.cache.api("actions/runs/" + str(R2_RUN))
    v.need(run["head_sha"] == R2_HEAD and run["status"] == "completed"
           and run["conclusion"] == "success" and run["run_attempt"] == 1, "R2 run not certified")
    for artifact_id, name, digest in R2_ARTIFACTS:
        a = v.cache.api("actions/artifacts/" + str(artifact_id))
        v.need(a["id"] == artifact_id and a["name"] == name and a["digest"] == digest
               and not a["expired"] and a["workflow_run"]["id"] == R2_RUN
               and a["workflow_run"]["head_sha"] == R2_HEAD, "R2 artifact identity mismatch")
    first, second = load(local/"direct.json"), load(independent/"direct.json")
    mcp, receipt = load(local/"mcp.json"), load(independent/"independent.json")
    a, b = load(local/"kernel-index.json"), load(independent/"kernel-index.json")
    v.need(first == second and v.digest(first) == R2_DIRECT and first["source_head"] == head
           and first["scope_digest"] == v.SCOPE and a == b and v.digest(a) == R2_TYPES
           and len(a) == 124 and v.digest(mcp) == R2_MCP and mcp["direct_digest"] == R2_DIRECT
           and len(mcp["selected_observations"]) == 12
           and receipt["status"] == "INDEPENDENT_KERNEL_OBSTRUCTION_INDEX_R2_GREEN"
           and receipt["direct_digest"] == R2_DIRECT and receipt["type_index_digest"] == R2_TYPES
           and receipt["mcp_digest"] == R2_MCP, "R2 calibration artifacts differ")
    return a

def bind_files(module, base, source):
    paths = [base, Path(str(base)+".server"), Path(str(base)+".private")]
    exists = [p.is_file() for p in paths]
    if not exists[0]:
        return None, "HOLD_MISSING_OLEAN"
    if exists[1] != exists[2]:
        return None, "HOLD_INCOMPLETE_MODULE_PARTS"
    paths = paths if all(exists) else paths[:1]
    v.need(all(p.resolve().is_relative_to(ROOT) and not p.is_symlink() for p in paths),
           "nonlocal olean artifact")
    return {"module": module, "source": source,
            "files": [{"path": p.relative_to(ROOT).as_posix(), "sha256": filehash(p),
                       "bytes": p.stat().st_size} for p in paths]}, None

def run_batch(folder, modules, sources, artifacts, env):
    folder.mkdir()
    wanted, meta_path, raw = folder/"modules.txt", folder/"environment.json", folder/"kernel-types.jsonl"
    wanted.write_text("".join(m+"\t"+"\t".join(f["path"] for f in artifacts[m]["files"])+"\n"
                             for m in modules), encoding="utf-8")
    old = v.TEMPLATE.read_text(encoding="utf-8")
    marker = "set_option maxRecDepth 8192 in\n"
    v.need(old.startswith("import KuuOSFormal\n") and old.count(marker)==1, "serializer changed")
    lean = old.split(marker, 1)[0].replace("import KuuOSFormal\n", "import Lean\n", 1)+TAIL
    for key, path in (("__MODULE_FILE__",wanted),("__META_FILE__",meta_path),("__ROWS_FILE__",raw)):
        v.need(lean.count(key)==1, "unexpected serializer placeholder")
        lean=lean.replace(key,path.relative_to(ROOT).as_posix())
    probe = folder/"OleanExport.lean"
    probe.write_text(lean,encoding="utf-8")
    log = lean_run(folder,["lean",str(probe.relative_to(ROOT))],"export",env)
    meta = load(meta_path)
    v.need([m["module"] for m in meta["modules"]]==modules
           and meta["selected_theorems"]==sum(m["theorem_count"] for m in meta["modules"])
           and f"{MARK} {meta['selected_theorems']}" in log, "incomplete raw inventory")
    for m in meta["modules"]:
        expected = "readModuleData" if len(artifacts[m["module"]]["files"])==1 else "readModuleDataParts"
        v.need(m["mode"]==expected, "reader path mismatch")
    if meta["selected_theorems"]:
        # Only a serializer adapter: this is NOT an import-environment receipt.
        rows = v.read_rows(raw,{"imported_modules":modules,"selected_theorems":meta["selected_theorems"]},
                           {m:sources[m] for m in modules},folder)
    else:
        v.need(not raw.read_text(encoding="utf-8").strip(), "unexpected rows")
        rows=[]
    raw.unlink()
    counts=Counter(x["module"] for x in rows)
    for m in meta["modules"]:
        v.need(counts[m["module"]]==m["theorem_count"], "module type count mismatch")
    for m in modules:
        for f in artifacts[m]["files"]:
            v.need(filehash(ROOT/f["path"])==f["sha256"], "artifact changed")
    v.save(folder/"kernel-index.json",rows)
    receipt={"modules":meta["modules"],"artifact_bindings":[artifacts[m] for m in modules],
             "type_digest":v.digest(rows),"type_count":len(rows),"probe_sha256":v.sha(lean.encode())}
    v.save(folder/"receipt.json",receipt)
    print("KUUOS_OLEAN_R4_BATCH",json.dumps({k:z for k,z in receipt.items() if k!="artifact_bindings"},sort_keys=True),flush=True)
    return rows,receipt

def fixtures(work, env):
    # Actual compiler-generated olean forms, not manufactured JSON data.
    d=work/"fixtures"
    d.mkdir()
    texts={
      "Single":"import Lean\nnamespace KuuOSOleanFixture\ntheorem singleWitness : True := True.intro\nend KuuOSOleanFixture\n",
      "Multipart":"module\npublic import Lean\npublic section\nnamespace KuuOSOleanFixture\nprivate theorem multipartHidden : True := True.intro\ntheorem multipartVisible : True := multipartHidden\nend KuuOSOleanFixture\n",
    }
    artifacts={}
    sources={}
    for name, source in texts.items():
        path=d/(name+".lean")
        path.write_text(source,encoding="utf-8")
        lean_run(d,["lean","-o",name+".olean",name+".lean"],name,env,cwd=d)
        src={"path":path.relative_to(ROOT).as_posix(),"blob":v.sha(source.encode())}
        sources[name]=[src]
        artifact,hold=bind_files(name,d/(name+".olean"),src)
        v.need(hold is None and len(artifact["files"])==(1 if name=="Single" else 3),
               "compiler fixture did not produce expected format")
        artifacts[name]=artifact
    rows,receipt=run_batch(d/"reader",list(texts),sources,artifacts,env)
    names=[x["name"] for x in rows]
    v.need("KuuOSOleanFixture.singleWitness" in names and "KuuOSOleanFixture.multipartVisible" in names
           and any(n.endswith(".multipartHidden") for n in names),"single/multipart private witness missing")
    # Artifact byte hashes of compiler-generated fixtures need not be portable.
    # Only the observed names/modes and structural result are compared.
    stable={"single":True,"multipart":True,"private_theorem_retained":True,
            "modes":[m["mode"] for m in receipt["modules"]]}
    v.save(d/"fixture-result.json",stable)
    print("KUUOS_OLEAN_R4_FIXTURE_GREEN",json.dumps(stable,sort_keys=True),flush=True)
    return stable

def batches(modules, artifacts):
    group=[];size=0
    for m in modules:
        weight=sum(f["bytes"] for f in artifacts[m]["files"])
        if group and (len(group)>=BATCH or size+weight>MAX_BATCH_BYTES):
            yield group
            group=[];size=0
        group.append(m);size+=weight
    if group:
        yield group

def direct(head,out,reference,extra):
    obs,cat,inv=v.snapshot(head)
    sources=r2.module_sources(cat)
    counts=Counter(x["module"] for x in inv["hints"])
    ordered=sorted((m for m in sources if m not in r2.MODULES),key=lambda m:(-counts[m],m))
    requested=list(r2.MODULES)+(ordered if extra==0 else ordered[:extra])
    env=fixed_lean()
    work=out
    work.mkdir(parents=True,exist_ok=False)
    fixture=fixtures(work,env)
    v.save(work/"lexical-inventory.json",inv)
    states={};artifacts={}
    for m in requested:
        if len(sources[m])!=1:
            states[m]="HOLD_AMBIGUOUS_SOURCE";continue
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*",m):
            states[m]="HOLD_UNSUPPORTED_MODULE_PATH";continue
        base=ROOT/".lake/build/lib/lean"/(m.replace(".","/")+".olean")
        artifact,hold=bind_files(m,base,sources[m][0])
        if hold is not None:
            states[m]=hold;continue
        artifacts[m]=artifact
    v.need(set(r2.MODULES)<=set(artifacts),"mandatory calibration artifacts absent")
    v.save(work/"plan.json",{"requested":requested,"preflight_holds":states,"artifacts":artifacts})
    rows=[];receipts=[]
    for i,group in enumerate(batches([m for m in requested if m in artifacts],artifacts)):
        local,receipt=run_batch(work/f"batch-{i+1:03}",group,sources,artifacts,env)
        rows.extend(local);receipts.append(receipt)
        for m in receipt["modules"]:
            states[m["module"]]="RAW_OLEAN_TYPE_OBSERVED_"+m["mode"]
    rows.sort(key=lambda x:(x["module"],x["name"]))
    v.need(len({(x["module"],x["name"]) for x in rows})==len(rows),"duplicate module-local types")
    calibrated=[x for x in rows if x["module"] in r2.MODULES]
    if calibrated!=reference:
        v.save(work/"calibration-mismatch.json",{"reference":reference,"raw":calibrated})
        raise ValueError("raw olean types do not match independent R2 kernel observation")
    for m in r2.MODULES:
        states[m]="R2_IMPORTED_TYPE_EQUAL"
    joined,unmatched=v.reconcile(inv,rows)
    v.need(len(joined)==6380,"lexical inventory lost")
    names=Counter(x["name"] for x in rows)
    ambiguous=sorted(k for k,z in names.items() if z>1)
    n=Counter(x["module"] for x in rows)
    coverage=[{"module":m,"sources":sources[m],"state":states.get(m,"HOLD_NOT_REQUESTED"),
               "type_count":n[m],"lexical_hint_count":counts[m]} for m in sorted(sources)]
    v.save(work/"kernel-index.json",rows)
    v.save(work/"lexical-join.json",joined)
    v.save(work/"unmatched-negative-types.json",unmatched)
    v.save(work/"ambiguous-global-names.json",ambiguous)
    v.save(work/"module-coverage.json",coverage)
    v.need(v.github_observation(head,"canonical_main")==obs,"canonical source changed")
    stable={"schema":SCHEMA,"source_head":head,"source_tree":obs["source_tree"],"scope_digest":v.SCOPE,
            "r2_direct_digest":R2_DIRECT,"r2_type_digest":R2_TYPES,"r2_mcp_digest":R2_MCP,
            "fixture":fixture,"calibrated_theorems":len(calibrated),"requested_modules":len(requested),
            "source_module_count":len(sources),"raw_type_count":len(rows),
            "additional_raw_type_count":len(rows)-len(calibrated),
            "reader_mode_counts":dict(sorted(Counter(m["mode"] for z in receipts for m in z["modules"]).items())),
            "state_counts":dict(sorted(Counter(x["state"] for x in coverage).items())),
            "coverage_digest":v.digest(coverage),"raw_type_digest":v.digest(rows),
            "lexical_hint_count":len(joined),"lexical_join_digest":v.digest(joined),
            "unmatched_negative_digest":v.digest(unmatched),"ambiguous_names_digest":v.digest(ambiguous),
            "batch_receipt_digests":[v.digest(z) for z in receipts],
            "project_module_imports":False,"all_axioms_audited":False,
            "fresh_mcp_executed":False,"proof_authority":False,"applicability_certified":False,
            "semantic_search_complete":False,"full_corpus_kernel_coverage_claimed":False}
    v.save(work/"direct.json",stable)
    print("KUUOS_OLEAN_R4_DIRECT_GREEN",json.dumps({**stable,"digest":v.digest(stable)},sort_keys=True),flush=True)
    return stable

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--r2-local",type=Path,required=True)
    p.add_argument("--r2-independent",type=Path,required=True)
    p.add_argument("--extra",type=int,default=64,help="0 = request full inventory")
    p.add_argument("--first",type=Path)
    a=p.parse_args()
    v.need(a.extra>=0,"invalid module limit")
    out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    ref=r2_reference(a.r2_local,a.r2_independent,a.head)
    receipt=direct(a.head,out,ref,a.extra)
    if a.first is not None:
        v.need(receipt==load(a.first/"direct.json"),"independent raw index differs")
        result={"status":"INDEPENDENT_OLEAN_R4_GREEN","direct_digest":v.digest(receipt),
                "r2_direct_digest":R2_DIRECT,"r2_mcp_digest":R2_MCP,
                "raw_type_count":receipt["raw_type_count"],"reader_mode_counts":receipt["reader_mode_counts"],
                "state_counts":receipt["state_counts"],"proof_authority":False,"applicability_certified":False}
        v.save(out/"independent.json",result)
        print("KUUOS_OLEAN_R4_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
