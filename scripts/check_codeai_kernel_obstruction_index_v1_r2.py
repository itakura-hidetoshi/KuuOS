#!/usr/bin/env python3
"""R2: bounded module-local theorem type exports.

R1 was terminated by the runner before producing an export receipt. Do
not infer a Lean error or OOM. Never import the entire aggregate in one
probe. Keep every original lexical hint, including not-yet-indexed modules.
The six selected module shards are a bounded frontier, not all-library
kernel coverage. No original theorem, public root, pin or assumption changes.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess

import check_codeai_kernel_obstruction_index_v1 as v

ROOT=v.ROOT
MODULES=tuple(sorted({module for module,_ in v.SELECTED.values()}))
MARK="KUUOS_KERNEL_OBSTRUCTION_EXPORT"
R2_SCHEMA="kuuos.codeai.kernel-obstruction-index.module-shards.v1-r2"

def run_lean(path,source,timeout=600):
    """Keep diagnostics on disk even on failure; report shard boundaries."""
    path.write_text(source,encoding="utf-8")
    opts=v.canonical_direct_options((ROOT/"lakefile.toml").read_bytes())
    argv=["lake","env","lean",*opts,str(path.relative_to(ROOT))]
    timing=path.with_suffix(".timing")
    if Path("/usr/bin/time").is_file():
        argv=["/usr/bin/time","-v","-o",str(timing),*argv]
    log_path=path.with_suffix(".log")
    print("KUUOS_KERNEL_SHARD_START",str(path.relative_to(ROOT)),flush=True)
    with log_path.open("w",encoding="utf-8") as log:
        proc=subprocess.run(argv,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=timeout)
    log=log_path.read_text(encoding="utf-8")
    if proc.returncode or re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked)",log):
        print(log[-20000:],flush=True)
        if timing.is_file(): print(timing.read_text(),flush=True)
        raise ValueError("module-local direct Lean failed: "+str(path))
    if timing.is_file():
        print("KUUOS_KERNEL_SHARD_RESOURCE",str(path.relative_to(ROOT)),
              next((x.strip() for x in timing.read_text().splitlines()
                    if "Maximum resident set size" in x),"NO_DATA"),flush=True)
    return log

def module_sources(cat):
    sources=defaultdict(list)
    for f in cat["files"]:
        sources[f["module_path_lexical"]].append({"path":f["path"],"blob":f["blob"]})
    return {k:sorted(rows,key=lambda x:x["path"]) for k,rows in sorted(sources.items())}

def shard_direct(module,out,sources):
    v.need(module in sources and len(sources[module])==1,
           "missing or ambiguous observed module source")
    shard=out/("shard-"+str(MODULES.index(module)+1).zfill(2))
    shard.mkdir()
    names=[name for name,(mod,_) in v.SELECTED.items() if mod==module]
    wanted=shard/"modules.txt"
    wanted.write_text(module+"\n",encoding="utf-8")
    meta_file=shard/"environment.json"
    rows_file=shard/"kernel-types.jsonl"
    template=v.TEMPLATE.read_text(encoding="utf-8")
    v.need(template.startswith("import KuuOSFormal\n"),"unexpected original export template")
    source=template.replace("import KuuOSFormal\n","import "+module+"\n",1)
    for marker,path in (("__MODULE_FILE__",wanted),("__META_FILE__",meta_file),("__ROWS_FILE__",rows_file)):
        v.need(source.count(marker)==1,"template path missing")
        source=source.replace(marker,path.relative_to(ROOT).as_posix())
    source+="\n"+v.suffix(names)
    log=run_lean(shard/"Export.lean",source)
    meta=json.loads(meta_file.read_text())
    v.need(module in meta["imported_modules"] and f"{MARK} {meta['selected_theorems']}" in log,
           "module import or export completion missing")
    rows=v.read_rows(rows_file,meta,{module:sources[module]},shard)
    rows_file.unlink()
    audited=v.read_direct(log,[{"name":name,"expected_direct_refs":[]} for name in names])
    by_name={row["name"]:row for row in rows}
    for audit in audited:
        name=audit["name"]; row=by_name[name]; expected_mod,expected_head=v.SELECTED[name]
        v.need(row["module"]==expected_mod and row["type_expr_sha256"]==audit["type_expr_sha256"]
               and (expected_head is None or row["conclusion_head"]==expected_head),
               "selected actual type mismatch:"+name)
    receipt={"module":module,"source":sources[module][0],"theorem_count":len(rows),
             "type_index_digest":v.digest(rows),"selected_observations":audited,
             "probe_sha256":v.sha(source.encode()),
             "imported_project_modules":sorted(set(meta["imported_modules"])&set(sources)),
             "proof_authority":False,"applicability_certified":False}
    v.save(shard/"kernel-index.json",rows)
    v.save(shard/"receipt.json",receipt)
    print("KUUOS_KERNEL_SHARD_GREEN",json.dumps({k:z for k,z in receipt.items()
        if k not in ("selected_observations","imported_project_modules")},sort_keys=True),flush=True)
    return rows,receipt

def direct(head,out):
    obs,cat,inv=v.snapshot(head)
    sources=module_sources(cat)
    v.need(len(MODULES)==6 and len(v.SELECTED)==12,"selected frontier changed")
    # Preserve unobserved lexical results BEFORE any potentially long import.
    v.save(out/"lexical-inventory.json",inv)
    print("KUUOS_KERNEL_SHARD_PLAN",json.dumps({"modules":MODULES,
        "all_source_modules":len(sources),"lexical_hints":inv["hint_count"]},sort_keys=True),flush=True)
    rows=[]; shards=[]
    for module in MODULES:
        local,receipt=shard_direct(module,out,sources)
        rows.extend(local);shards.append(receipt)
    rows.sort(key=lambda r:(r["module"],r["name"]))
    by_name={r["name"]:r for r in rows}
    v.need(len(by_name)==len(rows),"duplicate kernel declaration across modules")
    audited=sorted([a for shard in shards for a in shard["selected_observations"]],key=lambda a:a["name"])
    v.need({a["name"] for a in audited}==set(v.SELECTED) and len(audited)==12,
           "selected audit inventory mismatch")
    v.need(by_name[v.LEC+"nativeF55_twoChart_raw_no_global"]["binder_count"]==0
           and by_name[v.F112+"nativeK5BPNonerasing_no_singleton_BG"]["binder_count"]>0
           and by_name[v.LEC+"no_source_promotion_of_refuted_overlapFaithfulness"]["negative_binder_heads"]>0
           and by_name[v.LEC+"no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal"]["conclusion_negative_marker"]
           and not by_name[v.LEC+"nativeF55_twoChart_constant_raw_global"]["conclusion_negative_head"],
           "conditional/positive/negative selected controls differ")
    joined,unmatched=v.reconcile(inv,rows)
    unobserved=[{"module":m,"sources":sources[m],"status":"HOLD_KERNEL_TYPE_NOT_OBSERVED"}
                for m in sorted(set(sources)-set(MODULES))]
    observed_imports=sorted({m for shard in shards for m in shard["imported_project_modules"]})
    v.need(len(joined)==6380 and len(unobserved)+len(MODULES)==len(sources),
           "source inventory lost")
    v.save(out/"kernel-index.json",rows)
    v.save(out/"lexical-join.json",joined)
    v.save(out/"kernel-negative-without-lexical-match.json",unmatched)
    v.save(out/"unobserved-source-modules.json",unobserved)
    stable={"schema":R2_SCHEMA,"source_head":head,"source_tree":obs["source_tree"],"scope_digest":v.SCOPE,
        "lexical_inventory_digest":v.LEX,"lexical_hint_count":len(joined),
        "indexed_modules":list(MODULES),"indexed_module_count":len(MODULES),
        "source_module_count":len(sources),"unobserved_module_count":len(unobserved),
        "unobserved_module_digest":v.digest(unobserved),
        "observed_import_union_count":len(observed_imports),
        "observed_import_union_digest":v.digest(observed_imports),
        "kernel_theorem_count":len(rows),"type_index_digest":v.digest(rows),
        "lexical_join_digest":v.digest(joined),"unmatched_kernel_hint_digest":v.digest(unmatched),
        "shape_counts":dict(sorted(Counter(r["shape"] for r in rows).items())),
        "lexical_join_counts":dict(sorted(Counter(r["status"] for r in joined).items())),
        "negative_kernel_without_lexical_match_count":len(unmatched),
        "selected_count":len(audited),"selected_observations":audited,
        "selected_axioms":sorted({a for r in audited for a in r["axioms"]}),
        "shard_receipt_digests":[v.digest(x) for x in shards],
        "kernel_types_observed_not_reproved":True,"applicability_certified":False,
        "full_corpus_kernel_coverage_claimed":False,"all_axioms_audited":False,
        "semantic_search_complete":False,"proof_authority":False,"novelty_certified":False}
    v.save(out/"direct.json",stable)
    v.need(v.github_observation(head,"canonical_main")==obs,"canonical source changed")
    print("KUUOS_KERNEL_OBSTRUCTION_R2_DIRECT_GREEN",json.dumps({**{k:z for k,z in stable.items()
        if k!="selected_observations"},"direct_digest":v.digest(stable)},sort_keys=True),flush=True)
    return stable

def mcp(head,out):
    d=json.loads((out/"direct.json").read_text())
    v.need(d["schema"]==R2_SCHEMA and d["source_head"]==head and d["scope_digest"]==v.SCOPE
           and len(d["selected_observations"])==12,"unbound direct index")
    command=["uvx","--from",f"lean-lsp-mcp=={v.EXPECTED_SERVER_VERSION}","lean-lsp-mcp","--transport","stdio"]
    ver=v.server_version(command[:-2],ROOT)
    audited=[]
    for j,module in enumerate(MODULES):
        shard=out/("shard-"+str(j+1).zfill(2))
        names=[a for a in d["selected_observations"] if v.SELECTED[a["name"]][0]==module]
        source="import "+module+"\n\nset_option pp.universes false\n"+"\n".join(
            "#check @"+a["name"] for a in names)+"\n"
        file=shard/"McpProbe.lean";file.write_text(source,encoding="utf-8")
        client=v.MCPClient(command,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
            "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},
            timeout_seconds=240)
        try:
            client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                "clientInfo":{"name":"KuuOS module-local kernel obstruction index","version":"1.2"}})
            client.notify("notifications/initialized")
            v.need({"lean_verify","lean_diagnostic_messages"}.issubset(v.tool_map(client.request("tools/list"))),
                "real MCP tools unavailable")
            rel=str(file.relative_to(ROOT))
            raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
            v.save(shard/"mcp-diagnostics.json",raw); diag=v.structured(raw)
            v.need(diag.get("success") is True and diag.get("partial") is False and diag.get("timed_out") is False
                 and diag.get("failed_dependencies")==[] and isinstance(diag.get("items"),list)
                 and not any(x.get("severity") in ("error","warning") for x in diag["items"]),
                 "MCP diagnostics incomplete:"+module)
            for i,r in enumerate(names):
                raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":r["name"],"scan_source":False})
                v.save(shard/f"mcp-verify-{i}.json",raw)
                result=v.structured(raw);ax=result.get("axioms")
                print("KUUOS_KERNEL_SHARD_MCP_AXIOMS",json.dumps({"name":r["name"],"expected":r["axioms"],
                    "actual":ax,"warnings":result.get("warnings")},sort_keys=True),flush=True)
                v.need(isinstance(ax,list) and len(set(ax))==len(ax) and set(ax)<=v.STANDARD
                    and sorted(ax)==r["axioms"] and result.get("warnings")==[],
                    "MCP axiom mismatch:"+r["name"])
                audited.append({"name":r["name"],"module":module,"axioms":sorted(ax),
                    "type_expr_sha256":r["type_expr_sha256"],"probe_sha256":v.sha(source.encode())})
        finally:
            client.close()
        print("KUUOS_KERNEL_SHARD_MCP_GREEN",module,len(names),flush=True)
    audited.sort(key=lambda a:a["name"])
    v.need({a["name"] for a in audited}==set(v.SELECTED) and len(audited)==12,"incomplete MCP audit")
    receipt={"status":"REAL_LEAN_MCP_SELECTED_KERNEL_OBSTRUCTION_R2_GREEN",
        "direct_digest":v.digest(d),"mcp_version":v.EXPECTED_SERVER_VERSION,
        "mcp_version_output":ver,"selected_observations":audited,
        "all_types_mcp_verified":False}
    v.save(out/"mcp.json",receipt)
    print("KUUOS_KERNEL_OBSTRUCTION_R2_REAL_MCP",json.dumps({"selected":len(audited),
        "direct_digest":v.digest(d),"mcp_digest":v.digest(receipt)},sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--head",required=True)
    p.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--first",type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    if a.phase=="mcp":
        mcp(a.head,out);return
    d=direct(a.head,out)
    if a.phase=="independent":
        v.need(a.first is not None,"first runner receipt required")
        first=json.loads((a.first/"direct.json").read_text())
        mp=json.loads((a.first/"mcp.json").read_text())
        v.need(first==d and mp["direct_digest"]==v.digest(d)
             and mp["status"]=="REAL_LEAN_MCP_SELECTED_KERNEL_OBSTRUCTION_R2_GREEN"
             and len(mp["selected_observations"])==12,"independent type inventory differs")
        receipt={"status":"INDEPENDENT_KERNEL_OBSTRUCTION_INDEX_R2_GREEN",
            "direct_digest":v.digest(d),"type_index_digest":d["type_index_digest"],
            "lexical_join_digest":d["lexical_join_digest"],"mcp_digest":v.digest(mp),
            "kernel_theorem_count":d["kernel_theorem_count"],"indexed_module_count":len(MODULES),
            "unobserved_module_count":d["unobserved_module_count"],"selected_count":12,
            "full_corpus_kernel_coverage_claimed":False,"proof_authority":False,"semantic_search_complete":False}
        v.save(out/"independent.json",receipt)
        print("KUUOS_KERNEL_OBSTRUCTION_R2_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
