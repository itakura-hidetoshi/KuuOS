#!/usr/bin/env python3
"""Actual canonical-source duplicate/reuse gate and isolated Lean consumer.
No external provider, new public proof, or change to canonical source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT))
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import recall_kernel_memory
from runtime.kuuos_codeai_prior_proof_kernel_research_gate_v0_5 import (
    kernel_context_text, build_kernel_memory_research_synthesis)
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, scan
from scripts.codeai_prior_proof_kernel_recall_v0_4 import canonical_direct_options
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, EXPECTED_SERVER_VERSION, DISABLED_DURING_PROBE,
    call_tool, tool_map)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured

NAME = "Kuu.LivingEngi.sourceGlobal_implies_overlapFaithful"
SHORT = NAME.rsplit(".", 1)[-1]
SOURCE = "formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean"
PROBE_NAME = "KuuOSCanonicalCacheReuseProbe.reuseExisting"
PROBE = """import Kuu.LivingEngi.SourceAwareOverlapDescentCriterion

namespace KuuOSCanonicalCacheReuseProbe
open Kuu.LivingEngi
set_option autoImplicit false
universe u v w z

theorem reuseExisting {X : Type u} {I : Type v}
    {Raw : Type w} {Obs : Type z}
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (h : HasGlobal U s) :
    OverlapFiberFaithful U q s :=
  sourceGlobal_implies_overlapFaithful U q s h

#print axioms reuseExisting
end KuuOSCanonicalCacheReuseProbe
"""
STANDARD = {"propext", "Classical.choice", "Quot.sound"}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n")

def actual_observation(head):
    local = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    need(local == head, "checkout is not the expected canonical commit")
    return github_observation(head, "canonical_main")

def actual_gate(head, out):
    obs = actual_observation(head)
    recall = recall_kernel_memory(ROOT, obs, SHORT, terms=[SHORT], limit=500)
    need(recall["status"] == "REVIEW_REQUIRED", "kernel recall incomplete")
    known = recall["matched_observations"]
    need(len(known) == 1 and known[0]["observation"]["name"] == NAME,
         "exact target recall is ambiguous; review before proceeding")
    row = known[0]
    need(row["observation"]["path"] == SOURCE, "source path mismatch")
    need(row["observation"]["axioms"] == [], "unexpected historical axiom inventory")
    hit = row["lexical_id"]
    intent = {"intent_text": "Reuse the exact existing declaration " + NAME + "\n"
              + kernel_context_text(recall)}
    # The target is the exact recalled declaration, not a new proposition.
    # Unobserved hits remain explicit; no positive novelty review is supplied.
    review = {
        "request": "new",
        "kernel_receipt_digest": recall["receipt_digest"],
        "library_receipt_digest": recall["lexical_receipt"]["receipt_digest"],
        "library_comparisons": [{"id": hit, "relation": "equivalent"}],
        "kernel_comparisons": [{
            "id": hit, "relation": "equivalent",
            "observation_digest": digest(row),
            "type_expr_sha256": row["observation"]["type_expr_sha256"],
            "type_assumptions_comparison": "The target is this exact existing declaration, with unchanged quantified arguments.",
            "type_conclusion_comparison": "The target is the same named declaration and exact historical type.",
            "proof_reference_review": "Reuse the original declaration; do not regenerate its proof."
        }],
        "unobserved_kernel_hit_ids": recall["without_kernel_observation"],
        "synthesis_request_binding": digest(intent),
    }
    legacy = scan(ROOT, head, [SHORT, "OverlapFiberFaithful"])
    calls = []
    def forbidden_provider(*args, **kwargs):
        calls.append(1)
        raise AssertionError("duplicate/reuse must not call provider")
    kwargs = dict(root=ROOT, observation=obs, kernel_receipt=recall,
                  recall_receipt=legacy, synthesis_request=intent,
                  repository_files={SOURCE: (ROOT / SOURCE).read_bytes().decode("utf-8")},
                  provider_adapters=[forbidden_provider])
    new = build_kernel_memory_research_synthesis(mathematical_review=review, **kwargs)
    reuse = build_kernel_memory_research_synthesis(
        mathematical_review=dict(review, request="reuse"), **kwargs)
    need(new["kernel_review"]["status"] == "HOLD_DUPLICATE_REUSE_REQUIRED", str(new))
    need(reuse["kernel_review"]["status"] == "REUSE_EXISTING", str(reuse))
    need(new["synthesis"] is None and reuse["synthesis"] is None and not calls,
         "unexpected candidate generation")
    result = {"canonical_head": head, "canonical_tree": obs["source_tree"],
              "scope": obs["scope"], "target": NAME,
              "type_expr_sha256": row["observation"]["type_expr_sha256"],
              "recall_digest": recall["receipt_digest"],
              "new_status": new["kernel_review"]["status"],
              "reuse_status": reuse["kernel_review"]["status"],
              "unobserved_hits": recall["without_kernel_observation"],
              "provider_calls": 0, "novelty_certified": False,
              "proof_authority": False}
    save(out / "gate.json", result)
    print("KUUOS_CANONICAL_REUSE_GATE", json.dumps(result, sort_keys=True), flush=True)
    return result

def direct(head, out):
    before = actual_observation(head)
    gate = actual_gate(head, out)
    probe = out / "Probe.lean"
    probe.write_text(PROBE, encoding="utf-8")
    opts = canonical_direct_options((ROOT / "lakefile.toml").read_bytes())
    p = subprocess.run(["lake", "env", "lean", *opts, str(probe.relative_to(ROOT))],
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    log = p.stdout + "\n" + p.stderr
    (out / "direct.log").write_text(log)
    print(log, flush=True)
    need(p.returncode == 0, "direct Lean failed")
    need(not re.search(r"\b(?:warning|error):", log), "unexpected Lean diagnostics")
    need("sorryAx" not in log, "sorryAx in audit")
    need("does not depend on any axioms" in log, "expected axiom-free reuse")
    need(actual_observation(head) == before, "canonical observation changed")
    result = {"schema": "kuuos.codeai.canonical-cache-reuse-probe.v1",
              "gate": gate, "probe_sha256": hashlib.sha256(probe.read_bytes()).hexdigest(),
              "direct_options": opts, "axioms": [], "direct_exit": 0,
              "proof_authority": False, "novelty_certified": False}
    save(out / "direct.json", result)
    print("KUUOS_CANONICAL_REUSE_DIRECT", digest(result), flush=True)

def mcp(head, out):
    actual_observation(head)
    d = json.loads((out / "direct.json").read_text())
    need(d["gate"]["canonical_head"] == head, "unbound direct receipt")
    command = ["uvx", "--from", f"lean-lsp-mcp=={EXPECTED_SERVER_VERSION}",
               "lean-lsp-mcp", "--transport", "stdio"]
    client = MCPClient(command, cwd=ROOT, env={"LEAN_PROJECT_PATH": str(ROOT),
        "LEAN_LOG_LEVEL": "NONE", "LEAN_MCP_DISABLED_TOOLS": DISABLED_DURING_PROBE,
        "LEAN_MCP_SCRATCH_SLOTS": "1"}, timeout_seconds=240)
    try:
        client.request("initialize", {"protocolVersion": PROTOCOL_VERSION,
            "capabilities": {}, "clientInfo": {"name": "KuuOS canonical reuse", "version": "1"}})
        client.notify("notifications/initialized")
        tools = tool_map(client.request("tools/list"))
        need({"lean_diagnostic_messages", "lean_verify"}.issubset(tools), "missing real MCP tools")
        rel = str((out / "Probe.lean").relative_to(ROOT))
        raw = call_tool(client, "lean_diagnostic_messages", {"file_path": rel, "timeout_s": 180})
        save(out / "mcp-diagnostics.json", raw)
        diag = structured(raw)
        need(diag.get("success") is True and diag.get("partial") is False
             and diag.get("timed_out") is False and diag.get("failed_dependencies") == []
             and isinstance(diag.get("items"), list)
             and not any(x.get("severity") in ("error", "warning") for x in diag["items"]),
             "MCP diagnostics incomplete")
        raw = call_tool(client, "lean_verify", {"file_path": rel, "theorem_name": PROBE_NAME,
                                             "scan_source": False})
        save(out / "mcp-verify.json", raw)
        verify = structured(raw)
        need(verify.get("axioms") == [] and verify.get("warnings") == [],
             "MCP verification mismatch")
    finally:
        client.close()
    result = {"status": "REAL_LEAN_MCP_REUSE_GREEN",
              "direct_digest": digest(d), "axioms": [], "mcp_version": EXPECTED_SERVER_VERSION}
    save(out / "mcp.json", result)
    print("KUUOS_CANONICAL_REUSE_REAL_MCP", json.dumps(result, sort_keys=True), flush=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--head", required=True)
    p.add_argument("--phase", choices=("direct", "mcp", "independent"), required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--first", type=Path)
    a = p.parse_args()
    out = a.out.resolve()
    need(out.is_relative_to(ROOT / "artifacts"), "output must be isolated")
    out.mkdir(parents=True, exist_ok=True)
    if a.phase == "mcp":
        mcp(a.head, out)
        return
    direct(a.head, out)
    if a.phase == "independent":
        need(a.first is not None, "first runner receipt required")
        old = json.loads((a.first / "direct.json").read_text())
        new = json.loads((out / "direct.json").read_text())
        first_mcp = json.loads((a.first / "mcp.json").read_text())
        need(old == new and first_mcp["status"] == "REAL_LEAN_MCP_REUSE_GREEN"
             and first_mcp["direct_digest"] == digest(old), "independent receipt mismatch")
        result = {"status": "INDEPENDENT_CANONICAL_REUSE_GREEN",
                  "canonical_head": a.head, "direct_digest": digest(new),
                  "first_mcp_digest": digest(first_mcp),
                  "proof_authority": False, "novelty_certified": False}
        save(out / "independent.json", result)
        print("KUUOS_CANONICAL_REUSE_INDEPENDENT", json.dumps(result, sort_keys=True), flush=True)

if __name__ == "__main__":
    main()
