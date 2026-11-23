#!/usr/bin/env python3
"""v1.103 CodeAI: sequential isolated direct-Lean repair; NEVER external CI on red.

Exact original Lean source and public 15-name order are immutable.
Every unapproved candidate is a local append-only artifact with diagnostic logs.
The first candidate to pass pinned direct Lean and 15/15 #print axioms is
re-observed by REAL lean-lsp-mcp==0.30.0. This local verdict has NO authority
to merge, modify the PR, or grant future CodeAI memory usefulness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/v1103-codeai-local-five-trials-20261123"
SOURCE = Path("formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean")
ORIGINAL_BLOB = "04de7e72813e0e28c9d4e499b68876f081b3bdba"
IMPORT_V102 = Path("formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean")
IMPORT_V102_BLOB = "f8b492b210e5525990aa587fa2eb5c8648a5ff19"
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103"
INBOX = Path("/tmp/kuuos-v1103-five-trial-inbox")
RECEIPTS = Path("/tmp/kuuos-v1103-five-trial-receipts")
GREEN = Path("/tmp/kuuos-v1103-five-trial-green")
ADMISSION = Path("/tmp/kuuos-v1103-five-trial-admission.json")
MCP_PROBE = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersSandboxProbeV1_103.lean"
STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

REASONS = {
    "natTypeAHighCocycle_distinguished_zero": (
        "Replace invalid field projection with the exact v1.101 "
        "fully qualified TypeADistinguishedZero predicate on the same cocycle."
    )
}

ORIGINAL_HNAT = """          apply congrArg duskinComparison
          rw [← hsource]
          exact hnat.symm"""
HNAT_PROOFS = {
    "simp-only": """          simpa only [hsource] using
            (congrArg duskinComparison hnat.symm)""",
    "simp-full": """          simpa [hsource] using
            (congrArg duskinComparison hnat.symm)""",
    "calc": """          calc
            duskinComparison
                ((duskinNerve NatDoubleDelooping).map alpha.op
                  (f.map.app (op ⦋m⦌) x)) =
              duskinComparison
                (f.map.app (op ⦋2⦌)
                  ((Λ[g.n, g.i] : SSet).map alpha.op x)) := by
                    exact congrArg duskinComparison hnat.symm
            _ = _ := by rw [hsource]""",
}

ORIGINAL_MAP2 = """  rw [C.toDuskinSimplex_map₂]
  change _ + 0 = _
  rw [Nat.add_zero]
  rfl"""
MAP2_PROOFS = {
    "defeq": """  change _ + Nat.zero = _
  rw [Nat.add_zero]
  rfl""",
    "simp": """  simp only [C.toDuskinSimplex_map₂, Nat.add_zero]
  rfl""",
    "simp-rewrite": """  simp only [C.toDuskinSimplex_map₂]
  change _ + 0 = _
  rw [Nat.add_zero]
  rfl""",
}

ORIGINAL_EXT = """  ext Δ x
  rcases Δ with ⟨⟨m⟩⟩"""
EXT_PROOFS = {
    "plain": """  ext U x
  rcases U with ⟨⟨m⟩⟩""",
    "nattrans": """  apply NatTrans.ext
  funext U
  apply ConcreteCategory.hom_ext
  intro x
  rcases U with ⟨⟨m⟩⟩""",
}

SCHEDULE = (
    ("A-simp-only-defeq-plain", "simp-only", "defeq", "plain"),
    ("B-simp-full-defeq-plain", "simp-full", "defeq", "plain"),
    ("C-calc-defeq-plain", "calc", "defeq", "plain"),
    ("D-calc-simp-nattrans", "calc", "simp", "nattrans"),
    ("E-simp-only-simp-rewrite-nattrans", "simp-only", "simp-rewrite", "nattrans"),
)

def check(condition: bool, message: str) -> None:
    if not condition:
        raise cycle.Hold(message)

def exact_once(text: str, before: str, after: str) -> str:
    check(text.count(before) == 1, "SOURCE_OBSTRUCTION: expected one exact edit " + before[:90])
    return text.replace(before, after, 1)

def candidates() -> tuple[bytes, list[dict]]:
    original = (ROOT / SOURCE).read_bytes()
    check(cycle.git_blob(original) == ORIGINAL_BLOB, "SOURCE_OBSTRUCTION: v1.103 original Git blob changed")
    check(cycle.git_blob((ROOT / IMPORT_V102).read_bytes()) == IMPORT_V102_BLOB,
          "SOURCE_OBSTRUCTION: independently certified v1.102 changed")
    check(not any(p.exists() for p in (INBOX, RECEIPTS, GREEN, ADMISSION)),
          "SANDBOX_OBSTRUCTION: append-only directory reused")
    check((ROOT / "lean-toolchain").read_text().strip() == cycle.LEAN_PIN,
          "PIN_MISMATCH: Lean toolchain")
    seed = original.decode("utf-8")
    seed = exact_once(
        seed,
        "            natSimplex_triangle_face_comparison\n",
        "            NatNormalizedDuskinCocycle.natSimplex_triangle_face_comparison\n",
    )
    seed = exact_once(
        seed,
        "    (natTypeAHighCocycle g hn f).TypeADistinguishedZero g.i := by",
        "    KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101.NatNormalizedDuskinCocycle.TypeADistinguishedZero\n"
        "      (natTypeAHighCocycle g hn f) g.i := by",
    )
    assert len(cycle.declarations(original.decode("utf-8"))) == 15
    INBOX.mkdir(parents=True)
    RECEIPTS.mkdir(parents=True)
    manifest: list[dict] = []
    for i, (label, hnat, map2, ext) in enumerate(SCHEDULE, 1):
        text = exact_once(seed, ORIGINAL_HNAT, HNAT_PROOFS[hnat])
        text = exact_once(text, ORIGINAL_MAP2, MAP2_PROOFS[map2])
        text = exact_once(text, ORIGINAL_EXT, EXT_PROOFS[ext])
        contract = cycle.source_contract(original.decode(), text, REASONS, {})
        check(len(contract["public_declarations"]) == 15,
              "DECLARATION_OBSTRUCTION: 15 original names not preserved")
        check(set(contract["signature_changes"]) == set(REASONS) and
              not contract["import_additions"], "SOURCE_OBSTRUCTION: invalid theorem signature change")
        p = INBOX / f"{i:04d}-{label}.lean"
        b = text.encode()
        with p.open("xb") as stream:
            stream.write(b)
        manifest.append({
            "index": i, "name": label, "file": p.name,
            "sha256": cycle.sha256(b), "git_blob": cycle.git_blob(b),
            "original_blob": ORIGINAL_BLOB, "v102_blob": IMPORT_V102_BLOB,
            "public_declarations": 15, "reason": REASONS,
            "codeai_status": "TEST_REQUIRED", "independent_ci_success": False,
        })
    ADMISSION.write_text(json.dumps({
        "signature_changes": [
            {"name": k, "reason": v} for k, v in REASONS.items()
        ],
        "import_additions": [],
    }, sort_keys=True, indent=2) + "\n")
    (RECEIPTS / "candidate-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return original, manifest

def real_lean_mcp(candidate: bytes, selected: dict) -> None:
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
        MCPClient, PROTOCOL_VERSION, call_tool, tool_map,
    )
    from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
    from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics
    disabled = ",".join([
        "lean_run_code", "lean_build", "lean_profile_proof", "lean_minimal_hypotheses",
        "lean_leansearch", "lean_loogle", "lean_leanfinder", "lean_state_search",
        "lean_hammer_premise",
    ])
    check(not MCP_PROBE.exists(), "MCP_OBSTRUCTION: probe already exists")
    with MCP_PROBE.open("xb") as stream:
        stream.write(candidate)
    receipt = {
        "schema": "kuuos-v1103-real-lean-mcp-v1",
        "status": "MCP_NO_DATA",
        "candidate_blob": cycle.git_blob(candidate),
        "selected_attempt": selected["attempt"],
        "mcp_version": "lean-lsp-mcp==0.30.0",
        "independent_ci_success": False,
        "github_write_performed": False,
        "authority": "LOCAL_ONLY",
    }
    client = None
    try:
        client = MCPClient(
            ["uvx", "--from", "lean-lsp-mcp==0.30.0",
             "lean-lsp-mcp", "--transport", "stdio"],
            cwd=ROOT,
            env={
                "LEAN_PROJECT_PATH": str(ROOT), "LEAN_LOG_LEVEL": "NONE",
                "LEAN_MCP_SCRATCH_SLOTS": "1", "LEAN_MCP_DISABLED_TOOLS": disabled,
            },
            timeout_seconds=240,
        )
        initialized = client.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "KuuOS v1.103 isolated sandbox", "version": "1"},
        })
        client.notify("notifications/initialized")
        tools = tool_map(client.request("tools/list"))
        check("lean_diagnostic_messages" in tools and "lean_goal" in tools,
              "MCP_NO_DATA: typed Lean MCP tools missing")
        check("lean_build" not in tools and "lean_run_code" not in tools,
              "MCP_OBSTRUCTION: high-effect tool exposed")
        response = call_tool(
            client, "lean_diagnostic_messages",
            {"file_path": str(MCP_PROBE.relative_to(ROOT)), "timeout_s": 120}
        )
        diag = require_semantics(structured(response), candidate)
        receipt.update({
            "status": "MCP_TYPED_LOCAL_GREEN" if diag.success and not diag.errors
                      else "MCP_SEMANTIC_FAILED",
            "protocol": initialized.get("result", {}).get("protocolVersion"),
            "diagnostics_success": diag.success,
            "diagnostics_partial": diag.partial,
            "failed_dependencies": diag.failed_dependencies,
            "error_count": len(diag.errors),
            "diagnostics": diag.diagnostics[:30],
        })
        check(diag.success and not diag.errors and not diag.partial
              and not diag.failed_dependencies, "MCP_OBSTRUCTION: not full typed green")
    finally:
        if client is not None:
            client.close()
        if MCP_PROBE.exists():
            check(MCP_PROBE.read_bytes() == candidate, "MCP_OBSTRUCTION: probe mutation")
            MCP_PROBE.unlink()
        (RECEIPTS / "real-mcp-receipt.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    check(receipt["status"] == "MCP_TYPED_LOCAL_GREEN", "MCP_OBSTRUCTION")

def main() -> int:
    check(os.environ.get("GITHUB_ACTIONS") == "true",
          "RUNTIME_OBSTRUCTION: GitHub isolated runner required")
    check(os.environ.get("GITHUB_REF_NAME") == BRANCH,
          "SOURCE_OBSTRUCTION: wrong research branch")
    cycle.require_pins(ROOT)
    original, manifest = candidates()
    # The v1.103 module has one nested namespace declaration. The reusable
    # baseline runner's flat #print assumption does not apply here. Compile
    # through the exact canonical cycle.run_lean, but audit every ACTUAL kernel
    # name, including the nested toSimplexMap_mapComp name.
    named = list(cycle.declarations(original.decode("utf-8")))
    check(len(named) == 15 and "toSimplexMap_mapComp" in named,
          "DECLARATION_OBSTRUCTION: 15 public names or nested theorem changed")
    axiom_names = [
        "NatNormalizedDuskinCocycle.toSimplexMap_mapComp"
        if name == "toSimplexMap_mapComp" else name for name in named
    ]
    ledger = RECEIPTS / "ledger.jsonl"
    records: list[dict] = []
    for item in manifest:
        path = INBOX / item["file"]
        data = path.read_bytes()
        check(cycle.sha256(data) == item["sha256"] and
              cycle.git_blob(data) == item["git_blob"],
              "SOURCE_OBSTRUCTION: CodeAI candidate data changed")
        contract = cycle.source_contract(original.decode(), data.decode(), REASONS, {})
        check(contract["public_declarations"] == named and not contract["import_additions"],
              "DECLARATION_OBSTRUCTION: original 15 declarations changed")
        folder = RECEIPTS / ("attempt-%05d-%s" % (item["index"], item["sha256"][:12]))
        folder.mkdir(parents=True, exist_ok=False)
        direct = cycle.run_lean(ROOT, path, folder / "direct", seconds=500)
        record: dict = {
            "schema": "kuuos_v1103_multitrial_local_v1",
            "attempt": item["index"],
            "candidate_file": item["file"],
            "candidate_blob": item["git_blob"],
            "candidate_sha256": item["sha256"],
            "original_blob": ORIGINAL_BLOB,
            "import_v102_blob": IMPORT_V102_BLOB,
            "claimed_source_head": os.environ.get("GITHUB_SHA", ""),
            "direct_lean": direct,
            "contract": contract,
            "independent_ci_success": False,
            "github_write_performed": False,
            "authority": "LOCAL_ONLY",
            "status": "DIRECT_LEAN_FAILED",
        }
        if direct["direct_success"]:
            audit_source = (
                data.decode("utf-8") + "\n" +
                "\n".join("#print axioms " + NAMESPACE + "." + name
                          for name in axiom_names) + "\n"
            )
            audit_file = folder / "audit.lean"
            audit_file.write_text(audit_source)
            axiom_run = cycle.run_lean(ROOT, audit_file,
                                     folder / "axiom_audit", seconds=500)
            record["axiom_run"] = axiom_run
            if axiom_run["direct_success"]:
                report = (folder / "axiom_audit" / "stdout.log").read_text()
                record["axioms"] = cycle.audit_axioms(
                    report, axiom_names, NAMESPACE)
                record["status"] = "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY"
            else:
                record["status"] = "AXIOM_AUDIT_UNCERTIFIED"
        (folder / "receipt.json").write_text(
            json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
        cycle.append_receipt(ledger, record)
        records.append(record)
        print("KUUOS_V1103_SANDBOX_LOCAL_RECEIPT",
              json.dumps(record, sort_keys=True, ensure_ascii=False), flush=True)
        check((ROOT / SOURCE).read_bytes() == original,
              "SOURCE_OBSTRUCTION: authoritative Lean source changed")
        if record["status"] == "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY":
            break
    green = [r for r in records
             if r["status"] == "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY"]
    check(len(green) == 1 and 1 <= len(records) <= len(manifest),
          "DIRECT_LEAN_NO_LOCAL_GREEN: all attempted proof candidates retained; no independent CI")
    receipt = green[0]
    selected = INBOX / receipt["candidate_file"]
    candidate = selected.read_bytes()
    check(cycle.git_blob(candidate) == receipt["candidate_blob"],
          "SOURCE_OBSTRUCTION: successful candidate SHA mutated")
    check(receipt["direct_lean"]["exit_code"] == 0
          and receipt["direct_lean"]["error_count"] == 0
          and receipt["axioms"]["checked"] == 15
          and receipt["axioms"]["sorryAx"] is False
          and not set(receipt["axioms"]["allowed"]) - STD_AXIOMS,
          "AXIOM_OBSTRUCTION: incomplete local proof verification")
    real_lean_mcp(candidate, receipt)
    check((ROOT / SOURCE).read_bytes() == original, "SOURCE_OBSTRUCTION: original mutated")
    GREEN.mkdir(parents=True, exist_ok=False)
    (GREEN / "selected.lean").write_bytes(candidate)
    (GREEN / "selected-source.json").write_text(json.dumps({
        "schema": "kuuos-v1103-local-certified-candidate-v1",
        "source_commit_sha": os.environ.get("GITHUB_SHA"),
        "original_blob": ORIGINAL_BLOB,
        "v102_import_blob": IMPORT_V102_BLOB,
        "selected_file": receipt["candidate_file"],
        "candidate_blob": receipt["candidate_blob"],
        "candidate_sha256": receipt["candidate_sha256"],
        "trials_executed": len(records),
        "direct_lean_success": True,
        "axiom_declarations_checked": 15,
        "typed_lean_mcp_success": True,
        "independent_ci_success": False,
        "PR_source_adopted": False,
        "authority": "LOCAL_ONLY",
    }, indent=2, sort_keys=True) + "\n")
    print("KUUOS_V1103_LOCAL_15_AXIOMS_AND_REAL_MCP_GREEN",
          json.dumps({
              "source": receipt["candidate_blob"],
              "attempts": len(records),
              "name": receipt["candidate_file"],
              "axioms": 15,
              "independent_CI": False,
          }, sort_keys=True))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        RECEIPTS.mkdir(parents=True, exist_ok=True)
        (RECEIPTS / "sandbox-obstruction.txt").write_text(
            type(exc).__name__ + ": " + str(exc) + "\n"
        )
        print("KUUOS_V1103_LOCAL_HOLD", type(exc).__name__, str(exc), file=sys.stderr)
        raise SystemExit(2)
