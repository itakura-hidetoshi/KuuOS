"""R30: append independently rechecked proof witnesses to a portable ledger.
Keep historical R28 records byte-identical. Distinct witnesses for one exact
goal coexist. A pending extension is not admitted proof authority; fresh
Lean application and independent certification are required."""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_portable_recursive_recall_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
portable=prev.portable
MODULE="KuuOSCodeAIR30Capsule"
ROOT_CASES=("local_refined_context","global_identity_context")
NEGATIVE="KuuOSR26Proof.blockedPair"
NEGATIVE_LEAF="KuuOSR26Proof.negativeLeaf"
RAW_MARK="KUUOS_R30_RAW "

def material(d,mem):
    src=d["fresh_application"]["mcp_source"]
    imports="".join(l+"\n" for l in src.splitlines() if l.startswith("import "))
    if not imports or not src.startswith(imports):raise ValueError("import boundary")
    blocks=[];items={}
    for k in ROOT_CASES:
        a=d["applications"][k];q=a["renderer_request"];typed.validate(q)
        ns=typed.NS+"."+q["case_id"]
        n=ns+".witness"
        if n!=a["witness"] or q["polarity"]!="positive" or a["application"]["exact_kernel_type_match"] is not True:
            raise ValueError("root witness binding")
        start="namespace "+ns+"\n";end="end "+ns+"\n"
        if src.count(start)!=1 or src.count(end)!=1:raise ValueError("root source boundary")
        blocks.append(start+src.split(start,1)[1].split(end,1)[0]+end)
        items[k]={"target":q["target"],"target_expr":a["expected_target_expr"],"name":n,"polarity":"positive",
                  "prior_application_digest":old.digest(a)}
    rows={x["case"]:x for x in mem["records"].values()}
    target={"apply":[{"const":"And"},rows["refined_negative"]["target"],rows["capsule_exact"]["target"]]}
    typed.term(target)
    start="namespace KuuOSR26Proof\n";end="end KuuOSR26Proof\n"
    if src.count(start)!=1 or src.count(end)!=1:raise ValueError("negative source boundary")
    body=src.split(start,1)[1].split(end,1)[0]
    lines=[l for l in body.splitlines() if l.startswith(("theorem negativeLeaf ","theorem blockedPair "))]
    if len(lines)!=2 or not lines[0].startswith("theorem negativeLeaf ") or not lines[1].startswith("theorem blockedPair "):
        raise ValueError("negative declaration boundary")
    blocks.append(start+"set_option autoImplicit false\n"+"\n".join(lines)+"\n"+end)
    items["blocked_pair"]={"target":target,"name":NEGATIVE,"polarity":"negative",
                           "prior_application_digest":old.digest(d["branch_control"])}
    return imports+"\n"+"\n".join(blocks),items

def candidates(mem,items,raw,obs):
    old_cs={r["candidate"]["name"]:r["candidate"] for r in mem["records"].values() if r["candidate"] is not None}
    if len(old_cs)!=5:raise ValueError("parent candidate inventory")
    cs=[dict(c) for _,c in sorted(old_cs.items())]
    for k,x in sorted(items.items()):
        n=x["name"];r=raw[n];o=obs[n]
        if portable.hash_type(r["type_expr"])!=o["type_expr_sha256"] or r["type_expr"]!=o["type_expr_repr"] or set(o["axioms"])-typed.STANDARD:
            raise ValueError("new capsule full type binding")
        cs.append({"module":MODULE,"name":n,"polarity":x["polarity"],"type_sha256":o["type_expr_sha256"],
                   "proof_sha256":portable.hash_type(r["proof_expr"]),"axioms":o["axioms"]})
    if len({c["name"] for c in cs})!=8:raise ValueError("duplicate candidate identity")
    return {"candidates":cs}

def journal(mem,bridge,items,obs,cs,manifest,r29digest):
    if mem["key"]!=prev.R28_MEMORY or portable.seal(mem)["key"]!=mem["key"]:
        raise ValueError("parent memory changed")
    by={c["name"]:c for c in cs["candidates"]}
    records={}
    for k,x in sorted(items.items()):
        expr=obs[k];key=portable.hash_type(expr)
        if x.get("target_expr",expr)!=expr:raise ValueError("historical exact target drift")
        row={"case":k,"target":x["target"],"target_expr":expr,"target_key":key,
             "candidate":by[x["name"]],"prior_application_digest":x["prior_application_digest"],
             "status":"EXACT_APPLICATION_REQUIRED","proof_authority":False}
        records.setdefault(key,[]).append(row)
    return portable.seal({"schema":"kuuos.codeai.portable-memory-extension.v1","parent_memory_key":mem["key"],
        "transport_key":bridge["key"],"source_head":prev.CURRENT,"source_tree":prev.CURRENT_TREE,
        "scope_digest":old.SCOPE,"lean":portable.LEAN,"mathlib":portable.MATHLIB,
        "r29_direct_digest":r29digest,"capsule_manifest":manifest,"additions":records,
        "semantic_search_complete":False,"proof_authority":False})

def lookup(mem,layer,trusted,bridge,expr,live,expected_live):
    if layer.get("key")!=portable.seal(layer)["key"]:return {"status":"HOLD_EXTENSION_INTEGRITY","matches":[]}
    if layer!=trusted:return {"status":"HOLD_UNADMITTED_EXTENSION","matches":[]}
    if (mem["key"]!=layer["parent_memory_key"] or mem["key"]!=portable.seal(mem)["key"] or
        bridge["key"]!=layer["transport_key"] or layer["source_head"]!=prev.CURRENT or
        layer["source_tree"]!=prev.CURRENT_TREE or layer["scope_digest"]!=old.SCOPE):
        return {"status":"HOLD_EXTENSION_SCOPE","matches":[]}
    if live!=expected_live:return {"status":"HOLD_SOURCE_TYPE_DRIFT","matches":[]}
    k=portable.hash_type(expr);base=mem["records"].get(k);added=layer["additions"].get(k,[])
    rows=([base] if base is not None else [])+added
    if any(x["target_expr"]!=expr for x in rows):return {"status":"HOLD_TARGET_COLLISION","matches":[]}
    matches=[x["candidate"] for x in rows if x["candidate"] is not None]
    if len({x["name"] for x in matches})!=len(matches):return {"status":"HOLD_DUPLICATE_WITNESS","matches":[]}
    if len({x["polarity"] for x in matches})>1:return {"status":"HOLD_CONFLICTING_WITNESSES","matches":matches}
    if matches:return {"status":"EXACT_APPLICATION_REQUIRED","matches":matches}
    return {"status":"HOLD_HISTORICAL_NO_MATCH" if base is not None else "HOLD_SEARCH_REQUIRED","matches":[]}
