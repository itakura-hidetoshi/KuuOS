"""R12: bounded, data-driven closed Lean theorem applications.
Only explicit constant/numeral/application expressions are rendered. No
caller-supplied Lean commands, tactics, arbitrary code or provider lease.
A failed elaboration is HOLD, never a mathematical refutation.
"""
from __future__ import annotations
import re
import hashlib
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

NS="KuuOSOleanR12"
MARK="KUUOS_R12_APPLICATION "
STANDARD={"propext","Classical.choice","Quot.sound"}
IDENT=re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*\Z")
CASE=re.compile(r"[A-Za-z][A-Za-z0-9_]{0,39}\Z")
FORBIDDEN={"_","sorry","admit","by","let","fun","match","do","unsafe","axiom","opaque","run_cmd"}

def name(value):
    if (not isinstance(value,str) or len(value)>350 or not IDENT.fullmatch(value)
            or any(s in FORBIDDEN for s in value.split("."))):
        raise ValueError("invalid constant or module")
    return value

def term(node,depth=0,budget=None):
    if budget is None:budget=[256]
    budget[0]-=1
    if budget[0]<0 or depth>24 or not isinstance(node,dict) or len(node)!=1:
        raise ValueError("invalid or oversized term")
    if "const" in node:
        return "@"+name(node["const"])
    if "nat" in node and type(node["nat"]) is int and 0<=node["nat"]<=10**9:
        return "("+str(node["nat"])+" : Nat)"
    if "apply" in node:
        xs=node["apply"]
        if isinstance(xs,list) and 2<=len(xs)<=64:
            return "("+" ".join(term(x,depth+1,budget) for x in xs)+")"
    raise ValueError("unsupported term syntax")

def make_request(case_id,module,source,target,arguments,polarity):
    if not isinstance(case_id,str) or not CASE.fullmatch(case_id):
        raise ValueError("invalid case identity")
    name(module);name(source)
    if not isinstance(arguments,list) or len(arguments)>64 or polarity not in ("positive","negative"):
        raise ValueError("invalid application arguments or polarity")
    budget=[256]
    term(target,budget=budget)
    for arg in arguments:term(arg,budget=budget)
    result={"schema":"kuuos.codeai.closed-typed-application-request.v1",
            "case_id":case_id,"source_head":old.HEAD,"source_tree":old.TREE,
            "scope_digest":old.SCOPE,"module":module,"source":source,"target":target,
            "arguments":arguments,"polarity":polarity}
    return {**result,"request_digest":old.digest(result)}

def validate(request):
    if request!=make_request(request["case_id"],request["module"],request["source"],
                              request["target"],request["arguments"],request["polarity"]):
        raise ValueError("request binding changed")

def names(request):
    base=NS+"."+request["case_id"]
    return base+".target",base+".witness"

def declarations(request):
    validate(request)
    ns=NS+"."+request["case_id"]
    goal=term(request["target"])
    proof="@"+request["source"]
    if request["arguments"]:
        proof="("+proof+" "+" ".join(term(x) for x in request["arguments"])+")"
    ty="Not target" if request["polarity"]=="negative" else "target"
    return ("import "+request["module"]+"\n\nnamespace "+ns+"\n"
            "set_option autoImplicit false\nset_option maxHeartbeats 4000000\n"
            "def target : Prop := "+goal+"\n"
            "theorem witness : "+ty+" := "+proof+"\nend "+ns+"\n")

def render(request):
    target,witness=names(request)
    q=chr(96)*2
    expected="mkConst "+q+target
    if request["polarity"]=="negative":expected="mkApp (mkConst "+q+"Not) ("+expected+")"
    return declarations(request)+"\n".join([
        "open Lean","run_cmd do","  let env ← getEnv",
        "  let some t := env.find? "+q+target+' | throwError "missing target"',
        "  let some w := env.find? "+q+witness+' | throwError "missing witness"',
        '  let some body := t.value? (allowOpaque := true) | throwError "missing target body"',
        "  let expected := "+expected,
        '  unless w.isTheorem && w.type.equal expected do throwError "exact witness type mismatch"',
        '  if body.hasMVar || body.hasFVar || body.hasLooseBVars then throwError "open target"',
        '  let payload := Lean.Json.mkObj [',
        '    ("target_name", Lean.toJson "'+target+'"),',
        '    ("witness_name", Lean.toJson "'+witness+'"),',
        '    ("target_expr_repr", Lean.toJson (reprStr body)),',
        '    ("witness_type_repr", Lean.toJson (reprStr w.type)),',
        '    ("exact_kernel_type_match", Lean.toJson true)]',
        '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""])

def hold(reason,**kw):
    return old.hold(reason,**kw)

def project(direct,independent,mcp):
    """The host must independently admit the run/artifact provenance.
    The returned route is evidence for this exact request only.
    """
    try:
        if (direct!=independent or direct["status"]!="R12_DIRECT_APPLICATIONS"
                or mcp["status"]!="R12_REAL_MCP_GREEN" or mcp["direct_digest"]!=old.digest(direct)
                or direct["source_head"]!=old.HEAD or direct["source_tree"]!=old.TREE
                or direct["scope_digest"]!=old.SCOPE or direct["unobserved_module_count"]!=695
                or direct["proof_authority"] is not False):
            return hold("independent_application_evidence_missing")
        requests=direct["requests"]; results=direct["results"];audits=mcp["audits"]
        if set(requests)!=set(results) or set(audits)!={k for k,r in results.items()
                            if r["status"]=="EXACT_TYPED_APPLICATION"}:
            return hold("result_inventory_mismatch")
        routes={}
        for k,req in requests.items():
            validate(req)
            row=results[k]
            if req["case_id"]!=k or row["request_digest"]!=req["request_digest"]:
                return hold("request_identity_mismatch")
            if row["status"]=="HOLD_LEAN_APPLICATION":
                routes[k]=hold("application_not_proved",request_digest=req["request_digest"])
                continue
            if row["status"]!="EXACT_TYPED_APPLICATION":return hold("unknown_result_status")
            source=req["source"];target,witness=names(req)
            inventory={x["name"]:x for x in row["observations"]}
            mp={x["name"]:x["axioms"] for x in audits[k]}
            if set(inventory)!={source,witness} or len(row["observations"])!=2 or set(mp)!=set(inventory):
                return hold("audit_inventory_mismatch")
            s,w=inventory[source],inventory[witness];a=row["application"]
            material=direct["materialized_sources"][req["module"]+"::"+source]
            if (material["module"]!=req["module"] or material["name"]!=source
                    or material["type_expr_sha256"]!=s["type_expr_sha256"]
                    or a["target_name"]!=target or a["witness_name"]!=witness
                    or a["exact_kernel_type_match"] is not True
                    or a["witness_type_repr"]!=w["type_expr_repr"]
                    or not a["target_expr_repr"] or target not in w["type_constants"]
                    or (req["polarity"]=="negative")!=("Not" in w["type_constants"])
                    or source not in w["proof_constants"]
                    or any(set(x["axioms"])-STANDARD or x["axioms"]!=mp[n] or
                       hashlib.sha256(x["type_expr_repr"].encode()).hexdigest()!=x["type_expr_sha256"]
                       for n,x in inventory.items())):
                return hold("exact_type_or_axiom_mismatch")
            routes[k]={"status":"REFUTED_EXACT_TARGET" if req["polarity"]=="negative" else "REUSE_EXISTING",
                       "request_digest":req["request_digest"],"target_expr_digest":old.digest(a["target_expr_repr"]),
                       "source":source,"module":req["module"],"source_type_sha256":s["type_expr_sha256"],
                       "application_type_sha256":w["type_expr_sha256"],"axioms":w["axioms"],
                       "candidate_generation_allowed":False,"proof_authority":False}
        return {"status":"R12_INDEPENDENT_TYPED_ROUTES_OBSERVED","source_head":old.HEAD,
                "source_tree":old.TREE,"scope_digest":old.SCOPE,
                "direct_digest":old.digest(direct),"mcp_digest":old.digest(mcp),
                "routes":routes,"unobserved_module_count":695,
                "candidate_generation_allowed":False,"proof_authority":False,
                "execution_authority":False,"semantic_search_complete":False}
    except (KeyError,TypeError,ValueError,AttributeError):
        return hold("malformed_application_evidence")

def pre_provider(context,expected_context_digest,request):
    try:
        validate(request)
        if (context["status"]!="R12_INDEPENDENT_TYPED_ROUTES_OBSERVED"
                or old.digest(context)!=expected_context_digest
                or context["scope_digest"]!=old.SCOPE or context["source_head"]!=old.HEAD
                or context["proof_authority"] is not False):
            return hold("unadmitted_application_context")
        route=context["routes"][request["case_id"]]
        if route["request_digest"]!=request["request_digest"]:
            return hold("application_request_changed")
        return {**route,"synthesis":None,"provider_calls":0,"candidate_generation_allowed":False,
                "execution_authority":False,"semantic_search_complete":False}
    except (KeyError,TypeError,ValueError,AttributeError):
        return hold("unknown_or_invalid_application")
