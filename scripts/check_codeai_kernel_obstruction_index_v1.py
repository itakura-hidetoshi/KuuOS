#!/usr/bin/env python3
"""Read actual theorem types in KuuOSFormal's imported Lean environment.

Retain all lexical obstruction hints and unresolved module/declaration
mappings. Syntactic negation is discovery evidence, never applicability.
Separate selected direct/MCP axiom observations from the all-type index.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path.cwd().resolve()
INSTALL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(INSTALL))
from runtime import kuuos_codeai_whole_library_obstruction_recall_v1 as lex
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from scripts.codeai_prior_proof_kernel_recall_v0_4 import canonical_direct_options,suffix,read_direct,sha,save
from scripts import ci_verified_lean_project_cache_v1 as cache
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient,PROTOCOL_VERSION,EXPECTED_SERVER_VERSION,DISABLED_DURING_PROBE,
    call_tool,tool_map,server_version)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured

MAIN="e1d754e8e0fc9382001a2e698751aa11d4272b84"
TREE="bdf2e81fc2cf702481b80e7079e59b1b47836013"
SCOPE="2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b"
LEX="07fd8c9c849a09d2f75fce0ac676d480e2c5b2a92ddebedfcb8a468561283619"
TEMPLATE=INSTALL/"scripts/lean_probes/codeai_kernel_obstruction_index_v1.lean"
F112="Kuu.F112.Physical."
LEC="Kuu.LivingEngi."
QI="KUOS.Architecture.WuxingPentagonUnified.FivefoldP77FiniteRefinement.PentagonAdjoinedSixCell."
# Existing typed witnesses across the observed families. A classification
# is only syntax of the actual Expr; a no-go application needs more.
SELECTED={
    F112+"northNativeF55P92_original_unit_naturality_no_filler":("Kuu.F112.PolygonNativeF55P92OriginalUnitNaturalityNoGo","Not"),
    F112+"nativeK5BPNonerasing_no_singleton_BG":("Kuu.F112.PolygonNativeC60PhysicalBinarySizeNonerasingNoGo","Not"),
    F112+"nativeK5BPNonerasing_no_all_BG":("Kuu.F112.PolygonNativeC60PhysicalBinarySizeNonerasingNoGo","Not"),
    F112+"nativeK5BKExchange_no_sixteen_cell":("Kuu.F112.PolygonNativeC60PhysicalParallelBoundaryNoGo","Not"),
    F112+"nativeK5BKParallelNaturality_has_comparison":("Kuu.F112.PolygonNativeC60PhysicalParallelBoundaryNoGo",None),
    QI+"selectedRawCongruentFiniteTower_notInjective":("KUOS.Architecture.QiWuxingGK5CHP77UniformFiniteAncestorTowerObstructionV5_63","Not"),
    QI+"selectedRawCongruentFiniteTower_noClassDecoder":("KUOS.Architecture.QiWuxingGK5CHP77UniformFiniteAncestorTowerObstructionV5_63","Not"),
    LEC+"nativeF55_twoChart_raw_no_global":("Kuu.LivingEngi.NativeF55CechSourceGluingObstruction","Not"),
    LEC+"nativeF55_twoChart_constant_raw_global":("Kuu.LivingEngi.NativeF55CechSourceGluingObstruction",LEC+"HasGlobal"),
    LEC+"no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal":("Kuu.LivingEngi.SourceAwareOverlapDescentCriterion","Iff"),
    LEC+"no_source_promotion_of_refuted_overlapFaithfulness":("Kuu.LivingEngi.SourceAwareOverlapDescentCriterion","Not"),
    LEC+"nativeF55_source_vs_alternative_overlap_faithfulness":("Kuu.LivingEngi.SourceAwareOverlapDescentCriterion","And"),
}
STANDARD={"Classical.choice","Quot.sound","propext"}
MARKER={"Not","Ne","IsEmpty","False"}

def need(ok,reason):
    if not ok:
        raise ValueError(reason)

def snapshot(head):
    need(head==MAIN,"pilot exact canonical head changed")
    obs=github_observation(head,"canonical_main")
    scope=cache.local_scope(ROOT,head)
    need(obs["source_tree"]==TREE and scope==cache.remote_scope(cache.api,head)
         and digest(scope)==SCOPE,"proof scope mismatch")
    cat=build_catalog(ROOT,obs)
    inv=lex.build_obstruction_inventory(ROOT,obs,cat)
    need(inv["inventory_digest"]==LEX and inv["hint_count"]==6380,"lexical inventory drift")
    return obs,cat,inv

def run_lean(path,source,timeout=600):
    path.write_text(source,encoding="utf-8")
    opts=canonical_direct_options((ROOT/"lakefile.toml").read_bytes())
    p=subprocess.run(["lake","env","lean",*opts,str(path.relative_to(ROOT))],
        cwd=ROOT,capture_output=True,text=True,timeout=timeout)
    log=p.stdout+"\n"+p.stderr
    path.with_suffix(".log").write_text(log,encoding="utf-8")
    if p.returncode or re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked)",log):
        print(log[-20000:],flush=True)
        raise ValueError("direct Lean observation failed")
    return log

def read_rows(path,meta,source_modules,out):
    rows=[]
    names=set()
    raw_path=out/"kernel-types.jsonl.gz"
    # The exact type expression representation is retained in the archive.
    # The sorted index below binds it with SHA256 (not a mere Lean hash).
    with path.open(encoding="utf-8") as stream,gzip.open(raw_path,"wt",encoding="utf-8") as compressed:
        for line in stream:
            row=json.loads(line)
            need(row["name"] not in names and row["module"] in source_modules,
                 "duplicate or nonproject kernel theorem")
            names.add(row["name"])
            need(isinstance(row["type_expr_repr"],str) and row["type_expr_repr"] and
                 row["unresolved_type"] is False,"open/unresolved kernel theorem type")
            need(row["module"] in meta["imported_modules"],"theorem origin not imported")
            domains=row["binder_domains"]
            head=row["conclusion_head"]
            neg=row["conclusion_negative_head"]
            nested=row["conclusion_negative_marker"]
            need(type(neg) is bool and type(nested) is bool and neg==(head in MARKER),
                 "negative syntactic head classifier inconsistent")
            nhead=sum(d["negative_head"] is True for d in domains)
            nmark=sum(d["negative_marker"] is True for d in domains)
            need(nhead<=nmark,"negative domain marker lost")
            # A trailing False may be a dependent implication, not
            # an unconditional refutation. All binders are retained.
            shape=("FALSE_TAIL" if head=="False" else
                   "NEGATIVE_HEAD" if neg else
                   "NESTED_NEGATIVE_MARKER" if nested else
                   "NEGATIVE_BINDER_ONLY" if nmark else
                   "OTHER_OR_UNFOLDED")
            if head in ("let","metadata","bound-variable","projection","other","lambda","forall"):
                shape="UNRESOLVED_CONCLUSION_SHAPE"
            sources=source_modules[row["module"]]
            result={k:row[k] for k in ("name","module","universe_parameters","binder_domains",
                "conclusion_head","conclusion_negative_head","conclusion_negative_marker")}
            result.update(type_expr_sha256=sha(row["type_expr_repr"].encode()),
                type_constants=sorted(set(row["type_constants"])),
                conclusion_constants=sorted(set(row["conclusion_constants"])),
                binder_count=len(domains),negative_binder_heads=nhead,
                negative_binder_markers=nmark,shape=shape,
                source_candidates=sources,source_mapping="UNIQUE_MODULE_PATH" if len(sources)==1 else "HOLD_AMBIGUOUS_MODULE",
                applicability_certified=False,axiom_audit="SELECTED_ONLY_NOT_THIS_INDEX")
            rows.append(result)
            compressed.write(line)
    need(len(rows)==meta["selected_theorems"] and rows,"kernel export inventory mismatch")
    rows.sort(key=lambda x:(x["module"],x["name"]))
    return rows

def reconcile(inv,rows):
    by_module=defaultdict(lambda:defaultdict(list))
    for row in rows:
        parts=row["name"].split(".")
        for i in range(len(parts)):
            by_module[row["module"]][".".join(parts[i:])].append(row)
    joined=[]
    potential=set()
    for hint in inv["hints"]:
        found=by_module[hint["module"]].get(hint["name_lexical"],[])
        # Suffix lookup is an explicit candidate mapping, not proof of
        # identical declaration names across namespaces.
        hit=[{"name":x["name"],"type_expr_sha256":x["type_expr_sha256"],
              "shape":x["shape"]} for x in found]
        potential.update((x["module"],x["name"]) for x in found)
        joined.append({"lexical_id":hint["id"],"path":hint["path"],
            "source_blob":hint["source_blob"],"name_lexical":hint["name_lexical"],
            "candidates":hit,"status":"POTENTIAL_KERNEL_MATCH" if len(hit)==1 else
            "HOLD_AMBIGUOUS" if hit else "HOLD_NO_KERNEL_MATCH",
            "applicability_certified":False})
    need(len(joined)==inv["hint_count"],"lexical hints dropped")
    unmatched=[{"module":r["module"],"name":r["name"],"type_expr_sha256":r["type_expr_sha256"],
        "shape":r["shape"]} for r in rows if r["shape"] in ("NEGATIVE_HEAD","FALSE_TAIL",
            "NESTED_NEGATIVE_MARKER","NEGATIVE_BINDER_ONLY") and (r["module"],r["name"]) not in potential]
    return joined,unmatched

def direct(head,out):
    obs,cat,inv=snapshot(head)
    source_modules=defaultdict(list)
    for f in cat["files"]:
        source_modules[f["module_path_lexical"]].append({"path":f["path"],"blob":f["blob"]})
    source_modules={k:sorted(v,key=lambda x:x["path"]) for k,v in sorted(source_modules.items())}
    modules=out/"modules.txt"; modules.write_text("\n".join(source_modules)+"\n",encoding="utf-8")
    meta_file=out/"environment.json"; rows_file=out/"kernel-types.jsonl"
    source=TEMPLATE.read_text(encoding="utf-8")
    for marker,p in (("__MODULE_FILE__",modules),("__META_FILE__",meta_file),("__ROWS_FILE__",rows_file)):
        need(source.count(marker)==1,"template path missing")
        source=source.replace(marker,p.relative_to(ROOT).as_posix())
    log=run_lean(out/"Export.lean",source,timeout=900)
    meta=json.loads(meta_file.read_text())
    need(f"KUUOS_KERNEL_OBSTRUCTION_EXPORT {meta['selected_theorems']}" in log,"export completion missing")
    rows=read_rows(rows_file,meta,source_modules,out)
    rows_file.unlink()
    present=set(meta["imported_modules"])&set(source_modules)
    absent=sorted(set(source_modules)-present)
    joined,unmatched=reconcile(inv,rows)
    by_name={r["name"]:r for r in rows}
    need(len(by_name)==len(rows),"duplicate full kernel names")
    # Independently inspect full types, direct proof constants and actual
    # axioms for twelve existing witnesses from their own imported modules.
    selected_imports=sorted({mod for mod,_ in SELECTED.values()})
    selected_source="\n".join("import "+mod for mod in selected_imports)+"\n"+suffix(list(SELECTED))
    selected_log=run_lean(out/"Selected.lean",selected_source)
    audited=read_direct(selected_log,[{"name":k,"expected_direct_refs":[]} for k in SELECTED])
    for audit in audited:
        name=audit["name"]
        row=by_name[name]; mod,head_expected=SELECTED[name]
        need(row["module"]==mod and row["type_expr_sha256"]==audit["type_expr_sha256"]
             and (head_expected is None or row["conclusion_head"]==head_expected),
             "selected actual type mismatch:"+name)
    need(by_name[LEC+"nativeF55_twoChart_raw_no_global"]["binder_count"]==0
         and by_name[F112+"nativeK5BPNonerasing_no_singleton_BG"]["binder_count"]>0
         and by_name[LEC+"no_source_promotion_of_refuted_overlapFaithfulness"]["negative_binder_heads"]>0
         and by_name[LEC+"no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal"]["conclusion_negative_marker"]
         and not by_name[LEC+"nativeF55_twoChart_constant_raw_global"]["conclusion_negative_head"],
         "conditional/positive/negative selected controls differ")
    save(out/"kernel-index.json",rows)
    save(out/"lexical-join.json",joined)
    save(out/"kernel-negative-without-lexical-match.json",unmatched)
    save(out/"unimported-source-modules.json",[{"module":m,"sources":source_modules[m]} for m in absent])
    # Retain the full prior lexical inventory, including 573 incomplete
    # signature previews and any source-only candidates.
    save(out/"lexical-inventory.json",inv)
    stable={"schema":"kuuos.codeai.kernel-obstruction-index.v1",
        "source_head":head,"source_tree":obs["source_tree"],"scope_digest":SCOPE,
        "lexical_inventory_digest":LEX,"lexical_hint_count":len(joined),
        "canonical_public_root":"KuuOSFormal","source_module_count":len(source_modules),
        "imported_project_module_count":len(present),"unimported_source_module_count":len(absent),
        "kernel_theorem_count":len(rows),"type_index_digest":digest(rows),
        "lexical_join_digest":digest(joined),"unmatched_kernel_hint_digest":digest(unmatched),
        "shape_counts":dict(sorted(Counter(r["shape"] for r in rows).items())),
        "lexical_join_counts":dict(sorted(Counter(r["status"] for r in joined).items())),
        "negative_kernel_without_lexical_match_count":len(unmatched),
        "unimported_module_digest":digest(absent),"selected_count":len(audited),
        "selected_observations":audited,"selected_axioms":sorted({a for r in audited for a in r["axioms"]}),
        "kernel_types_observed_not_reproved":True,"applicability_certified":False,
        "full_corpus_kernel_coverage_claimed":False,"all_axioms_audited":False,
        "semantic_search_complete":False,"proof_authority":False,"novelty_certified":False}
    save(out/"direct.json",stable)
    need(github_observation(head,"canonical_main")==obs,"canonical source changed")
    print("KUUOS_KERNEL_OBSTRUCTION_DIRECT_GREEN",json.dumps({**{k:v for k,v in stable.items()
        if k!="selected_observations"},"direct_digest":digest(stable)},sort_keys=True),flush=True)
    return stable

def mcp(head,out):
    d=json.loads((out/"direct.json").read_text())
    need(d["source_head"]==head and d["scope_digest"]==SCOPE
         and len(d["selected_observations"])==len(SELECTED),"unbound direct index")
    source="\n".join("import "+m for m in sorted({mod for mod,_ in SELECTED.values()}))
    source+="\n\nset_option pp.universes false\n"+"\n".join("#check @"+n for n in SELECTED)+"\n"
    file=out/"McpProbe.lean";file.write_text(source,encoding="utf-8")
    command=["uvx","--from",f"lean-lsp-mcp=={EXPECTED_SERVER_VERSION}","lean-lsp-mcp","--transport","stdio"]
    ver=server_version(command[:-2],ROOT)
    client=MCPClient(command,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    audited=[]
    try:
        client.request("initialize",{"protocolVersion":PROTOCOL_VERSION,"capabilities":{},
            "clientInfo":{"name":"KuuOS kernel obstruction index","version":"1"}})
        client.notify("notifications/initialized")
        need({"lean_verify","lean_diagnostic_messages"}.issubset(tool_map(client.request("tools/list"))),
             "real MCP tools unavailable")
        rel=str(file.relative_to(ROOT))
        raw=call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
        save(out/"mcp-diagnostics.json",raw)
        diag=structured(raw)
        need(diag.get("success") is True and diag.get("partial") is False and diag.get("timed_out") is False
             and diag.get("failed_dependencies")==[] and isinstance(diag.get("items"),list)
             and not any(x.get("severity") in ("error","warning") for x in diag["items"]),
             "MCP diagnostics incomplete")
        for i,r in enumerate(d["selected_observations"]):
            raw=call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":r["name"],"scan_source":False})
            save(out/f"mcp-verify-{i}.json",raw)
            result=structured(raw);ax=result.get("axioms")
            need(isinstance(ax,list) and len(set(ax))==len(ax) and set(ax)<=STANDARD
                 and sorted(ax)==r["axioms"] and result.get("warnings")==[],
                 "MCP axiom mismatch:"+r["name"])
            audited.append({"name":r["name"],"axioms":sorted(ax),"type_expr_sha256":r["type_expr_sha256"]})
    finally:
        client.close()
    receipt={"status":"REAL_LEAN_MCP_SELECTED_KERNEL_OBSTRUCTION_GREEN",
        "direct_digest":digest(d),"mcp_version":EXPECTED_SERVER_VERSION,
        "mcp_version_output":ver,"selected_observations":audited,
        "probe_sha256":sha(source.encode()),"all_types_mcp_verified":False}
    save(out/"mcp.json",receipt)
    print("KUUOS_KERNEL_OBSTRUCTION_REAL_MCP",json.dumps({"selected":len(audited),
        "direct_digest":digest(d),"mcp_digest":digest(receipt)},sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--head",required=True)
    p.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--first",type=Path)
    a=p.parse_args();out=a.out.resolve()
    need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    if a.phase=="mcp":
        mcp(a.head,out);return
    d=direct(a.head,out)
    if a.phase=="independent":
        need(a.first is not None,"first runner receipt required")
        first=json.loads((a.first/"direct.json").read_text())
        mp=json.loads((a.first/"mcp.json").read_text())
        need(first==d and mp["direct_digest"]==digest(d)
             and mp["status"]=="REAL_LEAN_MCP_SELECTED_KERNEL_OBSTRUCTION_GREEN"
             and len(mp["selected_observations"])==len(SELECTED),"independent type inventory differs")
        receipt={"status":"INDEPENDENT_KERNEL_OBSTRUCTION_INDEX_GREEN",
            "direct_digest":digest(d),"type_index_digest":d["type_index_digest"],
            "lexical_join_digest":d["lexical_join_digest"],"mcp_digest":digest(mp),
            "kernel_theorem_count":d["kernel_theorem_count"],"selected_count":len(SELECTED),
            "full_corpus_kernel_coverage_claimed":False,"proof_authority":False,"semantic_search_complete":False}
        save(out/"independent.json",receipt)
        print("KUUOS_KERNEL_OBSTRUCTION_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
