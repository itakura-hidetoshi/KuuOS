#!/usr/bin/env python3
"""R48: recall independently certified shadow transport memory."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_shadow_transport_v1_r47 as r47
from runtime import kuuos_codeai_olean_contextual_transport_memory_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r46=r47.r46
r45=r47.r45
r29=r47.r29
r23=r47.r23
r39=r47.r39
v=r47.v
ROOT=r47.ROOT
load=r47.load
FILES=r47.FILES
NEW="shadow-transport-layer-v1.json"
RUN=45960380678
HEAD="0f9b1e23d77a93e1bf0922ea24da6de026b193a8"
ARTS=((15181121586,"codeai-olean-r47-local-45960380678-1","sha256:3ffeb7f6a9a9edfb9ba48ca81098c823c63e307cea19e4be06d0b70a18802c43"),
      (15180552937,"codeai-olean-r47-independent-45960380678-1","sha256:4ff4262dddbe8367aa4ae7299baa7a9ca96e0940e4d992896959d3d247870ca6"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R47 run")
    for jid,steps in ((140376545894,["Verify R47 contextual shadow transport","Actual Lean MCP R47 transport audit"]),
                      (140378084328,["Independently verify R47 contextual shadow transport"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R47 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R47 artifact")
    d=load(a.r47_local/"direct.json");mp=load(a.r47_local/"mcp.json");ind=load(a.r47_independent/"independent.json")
    v.need(d==load(a.r47_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R47 evidence")
    for name in FILES:
        raw=(a.r47_local/name).read_bytes()
        v.need(raw==(a.r47_independent/name).read_bytes(),"R47 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r47_local/"capsule";other=a.r47_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR48",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR48Independent",names) and
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
    global_obs=r29.parse(r23.run_lean([],out/"ObserveR48.lean",dispatch.observe(global_qs)),"KUUOS_R41_CONTEXT ")
    extension=load(out/r45.r44.r43.EXT);layer=load(out/r46.NEW)
    qs=gate.prev.prev.prev.requests(global_qs)
    def observe(label,q):
        controls={n:global_qs[n] for n in ("shadow","raw","alternate")}
        batch={**controls,label:q}
        row=r29.parse(r23.run_lean([],out/("ObserveR48_"+label+".lean"),dispatch.observe(batch)),"KUUOS_R41_CONTEXT ")
        v.need(set(row)==set(batch) and all(row[n]==global_obs[n] for n in controls),"canonical control drift")
        return row[label]
    obs={k:observe("compat_"+k,q) for k,q in sorted(qs.items())}
    hist={x["name"]:x for x in prior["fresh_application"]["observations"]}
    decisions={k:gate.prev.prev.recall(index,extension,layer,layer,q,obs[k],gate.base.CURRENT) for k,q in sorted(qs.items())}
    joint=load(out/r45.NEW);a0=a.r47_local/"joint-capsule";b0=a.r47_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.prev.prev.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR48",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR48Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    targets=gate.prev.requests(qs["shadow"])
    observations={k:observe("transport_"+k,q) for k,q in sorted(targets.items())}
    transport=gate.project(prior,mp,ind,index,extension,layer,mem,qs,obs,targets,observations)
    v.save(out/NEW,transport)
    def recall(q,o):return gate.recall(index,extension,layer,transport,transport,q,o,gate.base.CURRENT)
    # A fresh case identifier does not erase or merge the original context.
    requests={k:gate.base.root.make_request("r48_recall_"+k,q["target"],q["context_args"],q["context_modules"])
              for k,q in targets.items()}
    result={k:recall(q,observations[k]) for k,q in sorted(requests.items())}
    v.need(all(x["status"]=="EXACT_SHADOW_TRANSPORT_REQUIRED" and x["polarity"]=="positive" and
               x["kind"]==k and len(x["routes"])==3 and x==recall(targets[k],observations[k])
               for k,x in result.items()),"transport recall")
    for k,q in qs.items():
        v.need(recall(q,obs[k])==decisions[k],"parent compatibility drift")
    earlier={k:recall(q,global_obs[k]) for k,q in sorted(global_qs.items())}
    v.need(all(x==gate.prev.prev.recall(index,extension,layer,layer,global_qs[k],global_obs[k],gate.base.CURRENT)
               for k,x in earlier.items()),"parent global decision drift")
    v.need(decisions["raw"]["polarity"]=="negative" and earlier["raw"]["polarity"]=="negative","raw obstruction lost")
    # A real Lean-observed wrong-context request, not merely a fabricated hash.
    q=targets["compat"]
    wrong=gate.base.root.make_request("r48_wrong_source",q["target"],qs["raw"]["context_args"],q["context_modules"])
    wo=observe("wrong",wrong)
    bad=copy.deepcopy(transport);bad["equality"]["name"]=gate.prev.GLUE
    def control(e,tr,q,o,h):return gate.recall(index,extension,layer,e,tr,q,o,h)["status"]
    controls={"wrong_source":recall(wrong,wo)["status"],
              "tampered":control(bad,transport,q,observations["compat"],gate.base.CURRENT),
              "resealed":control(gate.base.portable.seal(bad),transport,q,observations["compat"],gate.base.CURRENT),
              "old_head":control(transport,transport,q,observations["compat"],old.HEAD)}
    v.need(not wo["aligned"] and controls=={"wrong_source":"HOLD_CONTEXT_MISMATCH",
              "tampered":"HOLD_TRANSPORT_INTEGRITY","resealed":"HOLD_UNADMITTED_TRANSPORT",
              "old_head":"HOLD_TRANSPORT_SCOPE"},"transport memory controls")
    body0,check0,refs0=gate.prev.prev.consumer(qs,decisions)
    body,check,refs=gate.consumer(transport,requests,observations,result)
    retained={n:x for n,x in hist.items() if not n.startswith(gate.prev.NS+".")}
    expected={n:x["expected_direct_refs"] for n,x in retained.items()};expected.update(refs)
    log=r23.run_lean([],out/"ApplyR48.lean",body0+body+check0+check+v.suffix(sorted(expected)))
    v.need(r29.parse(log,gate.prev.prev.MARK)=={k:o["goal_expr"] for k,o in obs.items()} and
           r29.parse(log,gate.MARK)=={k:o["goal_expr"] for k,o in observations.items()},"transport recalled exact goal")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n,x in retained.items():
        v.need(all(by[n][f]==x[f] for f in ("type_expr_repr","type_expr_sha256","type_constants",
               "proof_constants","axioms","universe_parameters")),"retained proof drift "+n)
    for n,rs in refs.items():
        old_n=n.replace(gate.NS,gate.prev.NS)
        v.need(prior["transport_refs"][old_n]==[r.replace(gate.NS,gate.prev.NS) for r in rs] and
               set(rs)<=set(by[n]["proof_constants"]) and by[n]["axioms"]==hist[old_n]["axioms"] and
               set(by[n]["axioms"])<={a for r in rs for a in by[r]["axioms"]},"transport dependency "+n)
    v.need(len(audit)==41 and all(set(x["axioms"])<=typed.STANDARD for x in audit) and
           r29.observe_scope()==scope,"audit scope")
    d={"status":"R48_DIRECT_CONTEXTUAL_TRANSPORT_MEMORY","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r47_direct_digest":gate.DIRECT,
       "r47_mcp_digest":gate.MCP,"capsule_manifest":manifest,"joint_capsule_manifest":joint,
       "capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],"extension_key":extension["key"],
       "derived_layer_key":layer["key"],"transport_layer_key":transport["key"],"new_contexts":2,
       "recalled_routes":6,"compatibility_witnesses":3,"global_witnesses":3,"historical_hold_retained":True,
       "raw_negative_retained":True,"controls":controls,"earlier_decisions":earlier,"requests":requests,
       "observations":observations,"decisions":result,"transport_refs":refs,"root_trials":0,"capsule_rebuilds":0,
       "reapplied_compatibility_recipes":9,"reapplied_transport_recipes":6,"provider_calls":0,
       "exact_kernel_type":True,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":body0+body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R48_DIRECT",json.dumps({"direct_digest":old.digest(d),"transport_layer_key":transport["key"],
          "new_contexts":2,"recalled_routes":6,"compatibility_witnesses":3,"global_witnesses":3,
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
                                     "clientInfo":{"name":"KuuOS contextual transport memory","version":"1"}})
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
    result={"status":"R48_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R48_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R48_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R48_INDEPENDENT_CONTEXTUAL_TRANSPORT_MEMORY_GREEN","source_head":d["source_head"],
            "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"capsule_layer_key":d["capsule_layer_key"],
            "dispatch_layer_key":d["dispatch_layer_key"],"extension_key":d["extension_key"],
            "derived_layer_key":d["derived_layer_key"],"transport_layer_key":d["transport_layer_key"],
            "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
            "new_contexts":2,"recalled_routes":6,"compatibility_witnesses":3,"global_witnesses":3,
            "historical_hold_retained":True,"raw_negative_retained":True,"exact_kernel_type":True,
            "parent_bytes_preserved":True,"transport_layer_bytes_equal":True,"raw_type_and_proof_equal":True,
            "root_trials":0,"capsule_rebuilds":0,"reapplied_compatibility_recipes":9,
            "reapplied_transport_recipes":6,"provider_calls":0,"controls":d["controls"],
            "mcp_audits":len(rows),"unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R48_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r47-local","r47-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
