#!/usr/bin/env python3
"""R46: recall independently certified derived compatibility memory."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_joint_capsule_v1_r45_r2 as r45
from runtime import kuuos_codeai_olean_contextual_derived_compatibility_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r45.r29
r23=r45.r23
r39=r45.r39
v=r45.v
ROOT=r45.ROOT
load=r45.load
FILES=r45.FILES+(r45.NEW,)
NEW="derived-compatibility-layer-v1.json"
RUN=45956835763
HEAD="3461e76458b683691b3c8bbaf0c00206e299b5fe"
ARTS=((15179372102,"codeai-olean-r45-r2-local-45956835763-1","sha256:1bab6fa26d829f0d3f495ea82d2ee0c734d32ef3d506722235526ca40de61a2c"),
      (15179796261,"codeai-olean-r45-r2-independent-45956835763-1","sha256:2bb7021d806105bdb880b3d54ada4685325660a73b6fbbca56d501a2eb956056"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R45 R2 run")
    for jid,steps in ((140365157519,["Verify R45 R2 contextual joint capsule","Actual Lean MCP R45 R2 compatibility audit"]),
                      (140366795862,["Independently verify R45 R2 contextual joint capsule"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R45 R2 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R45 R2 artifact")
    d=load(a.r45_local/"direct.json");mp=load(a.r45_local/"mcp.json");ind=load(a.r45_independent/"independent.json")
    v.need(d==load(a.r45_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R45 R2 evidence")
    for name in FILES:
        raw=(a.r45_local/name).read_bytes()
        v.need(raw==(a.r45_independent/name).read_bytes(),"R45 R2 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r45_local/"capsule";other=a.r45_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR46",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR46Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    dispatch=gate.dispatch
    global_qs=dispatch.requests(mem)
    alt=global_qs["alternate"]
    t=copy.deepcopy(alt["target"]);t["apply"][0]={"const":gate.base.LEC+"Compatible"}
    global_qs["unknown"]=gate.base.root.make_request("r43_unknown",t,alt["context_args"],alt["context_modules"])
    global_obs=r29.parse(r23.run_lean([],out/"ObserveR46.lean",dispatch.observe(global_qs)),"KUUOS_R41_CONTEXT ")
    extension=load(out/r45.r44.r43.EXT)
    qs=gate.prev.requests(global_qs)
    # As in R45 R2, retain canonical controls in each bounded observation.
    def observe(label,q):
        controls={n:global_qs[n] for n in ("shadow","raw","alternate")}
        batch={**controls,label:q}
        row=r29.parse(r23.run_lean([],out/("ObserveR46_"+label+".lean"),dispatch.observe(batch)),"KUUOS_R41_CONTEXT ")
        v.need(set(row)==set(batch) and all(row[n]==global_obs[n] for n in controls),"canonical control drift")
        return row[label]
    obs={k:observe("compat_"+k,q) for k,q in sorted(qs.items())}
    layer=gate.project(prior,mp,ind,index,extension,mem,global_qs,global_obs,qs,obs)
    v.save(out/NEW,layer)
    # Reuse actual compiled bytes from both certified runners, never compile them here.
    joint=load(out/r45.NEW);a0=a.r45_local/"joint-capsule";b0=a.r45_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(prior["joint_raw"])
    raw=r45.raw_read(a0,out,"RawJointR46",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR46Independent",names)==prior["joint_raw"],"joint full raw identity")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    def recall(q,o):return gate.recall(index,extension,layer,layer,q,o,gate.base.CURRENT)
    decisions={k:recall(q,obs[k]) for k,q in sorted(qs.items())}
    v.need(all(d["status"]=="EXACT_DERIVED_COMPATIBILITY_REQUIRED" and len(d["routes"])==3 and
               d["polarity"]==prior["compatibility_plan"]["polarity"][k] for k,d in decisions.items()),"derived recall")
    earlier={k:recall(q,global_obs[k]) for k,q in sorted(global_qs.items()) if k!="unknown"}
    v.need(all(x==gate.parent.dispatch(index,extension,extension,global_qs[k],global_obs[k],gate.base.CURRENT)
               for k,x in earlier.items()),"earlier global decisions drift")
    promoted=recall(global_qs["unknown"],global_obs["unknown"])
    v.need(promoted==decisions["alternate"],"prior HOLD recall")
    # Genuine unregistered constant-shadow compatibility and wrong source.
    q=qs["shadow"];ctx=copy.deepcopy(q["context_args"]);ctx[6]={"const":gate.base.LEC+"northNativeF55TwoChartConstantShadow"}
    t=copy.deepcopy(q["target"]);t["apply"][-1]=ctx[6]
    miss=gate.base.root.make_request("r46_miss",t,ctx,q["context_modules"])
    mo=observe("miss",miss)
    q=qs["raw"]
    wrong=gate.base.root.make_request("r46_wrong",q["target"],qs["alternate"]["context_args"],q["context_modules"])
    wo=observe("wrong",wrong)
    bad=copy.deepcopy(layer);bad["records"]=[]
    def control(e,tr,q,o,h):return gate.recall(index,extension,e,tr,q,o,h)["status"]
    controls={"unregistered":recall(miss,mo)["status"],"wrong_source":recall(wrong,wo)["status"],
              "tampered":control(bad,layer,q,obs["raw"],gate.base.CURRENT),
              "resealed":control(gate.base.portable.seal(bad),layer,q,obs["raw"],gate.base.CURRENT),
              "old_head":control(layer,layer,q,obs["raw"],old.HEAD)}
    v.need(mo["aligned"] and not wo["aligned"] and controls=={
        "unregistered":"HOLD_UNREGISTERED_TARGET","wrong_source":"HOLD_CONTEXT_MISMATCH",
        "tampered":"HOLD_DERIVED_INTEGRITY","resealed":"HOLD_UNADMITTED_DERIVED_LAYER",
        "old_head":"HOLD_DERIVED_SCOPE"},"derived controls")
    body,check,refs=gate.consumer(qs,decisions)
    hist={x["name"]:x for x in prior["fresh_application"]["observations"]}
    retained={n:x for n,x in hist.items() if not n.startswith(gate.prev.NS+".")}
    expected={n:x["expected_direct_refs"] for n,x in retained.items()};expected.update(refs)
    log=r23.run_lean([],out/"ApplyR46.lean",body+check+v.suffix(sorted(expected)))
    v.need(r29.parse(log,gate.MARK)=={k:o["goal_expr"] for k,o in obs.items()},"recalled exact goal")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n,x in retained.items():
        v.need(all(by[n][f]==x[f] for f in ("type_expr_repr","type_expr_sha256","type_constants",
               "proof_constants","axioms","universe_parameters")),"retained proof drift "+n)
    for n,rs in refs.items():
        old_n=gate.prev.NS+"."+n.rsplit(".",1)[1]
        v.need(prior["compatibility_refs"][old_n]==rs and set(rs)<=set(by[n]["proof_constants"]) and
               by[n]["axioms"]==hist[old_n]["axioms"] and
               set(by[n]["axioms"])<={a for r in rs for a in by[r]["axioms"]},"recalled dependency "+n)
    v.need(len(audit)==35 and r29.observe_scope()==scope,"audit scope")
    d={"status":"R46_DIRECT_CONTEXTUAL_DERIVED_COMPATIBILITY","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r45_direct_digest":gate.DIRECT,
       "r45_mcp_digest":gate.MCP,"capsule_manifest":manifest,"joint_capsule_manifest":joint,
       "capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],"extension_key":extension["key"],
       "derived_layer_key":layer["key"],"new_contexts":len(layer["records"]),"recalled_routes":len(refs),
       "positive_witnesses":6,"negative_witnesses":3,"historical_hold_retained":True,"prior_hold_recalled":True,
       "controls":controls,"earlier_decisions":earlier,"requests":qs,"observations":obs,"decisions":decisions,
       "compatibility_refs":refs,"root_trials":0,"capsule_rebuilds":0,"consumer_proof_body_rebuilds":0,
       "provider_calls":0,"exact_kernel_type":True,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R46_DIRECT",json.dumps({"direct_digest":old.digest(d),"derived_layer_key":layer["key"],
          "new_contexts":len(layer["records"]),"recalled_routes":len(refs),"positive_witnesses":6,
          "negative_witnesses":3,"historical_hold_retained":True,"prior_hold_recalled":True,
          "root_trials":0,"capsule_rebuilds":0,"audits":len(audit),"controls":controls},sort_keys=True),flush=True)
    return d

def mcp(out):
    d=load(out/"direct.json");x=d["fresh_application"]
    p=out/"McpApplication.lean";p.write_text(x["mcp_source"],encoding="utf-8")
    rel=str(p.relative_to(ROOT))
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=v.server_version(cmd[:-2],ROOT)
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows=[]
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                                     "clientInfo":{"name":"KuuOS contextual derived compatibility","version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),"MCP tools")
        raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
        v.save(out/"mcp-diagnostics.json",raw);diag=v.structured(raw)
        v.need(raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
               and diag["timed_out"] is False and diag["failed_dependencies"]==[]
               and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnostics")
        for j,row in enumerate(x["observations"]):
            raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":row["name"],"scan_source":False})
            v.save(out/f"mcp-verify-{j}.json",raw);val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"MCP axiom audit")
            rows.append({"name":row["name"],"axioms":ax})
    finally:client.close()
    result={"status":"R46_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R46_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R46_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
           and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnosis")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[]
               and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"]
               and row["name"]==mp["audits"][j]["name"],"MCP evidence mismatch")
    for name in FILES+(NEW,):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    v.need(r45.capsule_files(out/"joint-capsule")==r45.capsule_files(first/"joint-capsule")==d["joint_capsule_manifest"]["files"],
           "joint capsule bytes")
    result={"status":"R46_INDEPENDENT_CONTEXTUAL_DERIVED_COMPATIBILITY_GREEN","source_head":d["source_head"],
            "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"capsule_layer_key":d["capsule_layer_key"],
            "dispatch_layer_key":d["dispatch_layer_key"],"extension_key":d["extension_key"],
            "derived_layer_key":d["derived_layer_key"],"capsule_manifest":d["capsule_manifest"],
            "joint_capsule_manifest":d["joint_capsule_manifest"],"new_contexts":d["new_contexts"],
            "recalled_routes":d["recalled_routes"],"positive_witnesses":6,"negative_witnesses":3,
            "historical_hold_retained":True,"prior_hold_recalled":True,"exact_kernel_type":True,
            "parent_bytes_preserved":True,"derived_layer_bytes_equal":True,"raw_type_and_proof_equal":True,
            "root_trials":0,"capsule_rebuilds":0,"consumer_proof_body_rebuilds":0,"provider_calls":0,
            "controls":d["controls"],"mcp_audits":len(rows),"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R46_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r45-local","r45-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
