#!/usr/bin/env python3
"""Bounded v1.102 CodeAI variants in ONE isolated GitHub Actions Sandbox.

Prepare five immutable, source-bound *proof-body* variants (no theorem changes).
Sequentially call the canonical append-only KuuOS direct-Lean+axioms loop.
Only after its FIRST local-green receipt perform real lean-lsp-mcp==0.30.0.
Never call GitHub, git/gh, paid model APIs, independent CI, or merge.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle
from scripts.ci_kuuos_v1102_github_sandbox_r6 import (
    REASONS, R6_BLOB, ORIGINAL_BLOB, ORIGINAL_NS, R6_NS, SOURCE, R6,
)
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, call_tool, tool_map,
)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/v1.102-codeai-multitrial-sandbox-20261123"
INBOX = Path("/tmp/kuuos-v1102-multitrial-inbox")
RECEIPTS = Path("/tmp/kuuos-v1102-multitrial-receipts")
APPROVED = Path("/tmp/kuuos-v1102-multitrial-green")
ADMISSION = Path("/tmp/kuuos-v1102-multitrial-admission.json")
PROBE = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersMultiTrialProbeV1_102.lean"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}

R6_PROOF = """    -- The bicategory has a single one-cell; expose the pinned Hom reduction
    -- before invoking the explicitly provided subsingleton instance.
    change (sigma.map f : NatOneCell) = (tau.map f : NatOneCell)
    exact Subsingleton.elim _ _"""

REPAIRS = (
    ("explicit-inductive-unique", """    -- Explicitly prove equality of the unique NatOneCell constructor.
    have hUnique (x y : NatOneCell) : x = y := by
      cases x
      cases y
      rfl
    change (sigma.map f : NatOneCell) = (tau.map f : NatOneCell)
    exact hUnique _ _"""),
    ("direct-hom-ext", """    -- Instantiate both NatOneCell terms before touching type-class search.
    have hUnique : ∀ x y : NatOneCell, x = y := by
      intro x y
      cases x
      cases y
      rfl
    exact hUnique (sigma.map f : NatOneCell) (tau.map f : NatOneCell)"""),
    ("explicit-subsingleton-witness", """    -- Supply an explicit NatOneCell Subsingleton witness, not inferred Hom.
    have hsub : Subsingleton NatOneCell := by
      constructor
      intro x y
      cases x
      cases y
      rfl
    change (sigma.map f : NatOneCell) = (tau.map f : NatOneCell)
    exact hsub.elim _ _"""),
    ("explicit-cases-of-typed-terms", """    -- Case split on an *ascribed* NatOneCell, not a bundled Hom projection.
    change (sigma.map f : NatOneCell) = (tau.map f : NatOneCell)
    cases (sigma.map f : NatOneCell)
    cases (tau.map f : NatOneCell)
    rfl"""),
    ("local-hom-type-instance", """    -- Make the dependent Hom instance an explicit local object.
    haveI : Subsingleton (sigma.obj a ⟶ sigma.obj b) := by
      change Subsingleton NatOneCell
      exact ⟨by intro x y; cases x; cases y; rfl⟩
    exact Subsingleton.elim _ _"""),
)

def guard(condition: bool, message: str) -> None:
    if not condition:
        raise cycle.Hold(message)

def git_blob(source: bytes) -> str:
    return cycle.git_blob(source)

def materialize_variants() -> tuple[bytes, list[dict]]:
    raw = (ROOT / R6).read_bytes()
    original = (ROOT / SOURCE).read_bytes()
    guard(git_blob(raw) == R6_BLOB and git_blob(original) == ORIGINAL_BLOB,
          "SOURCE_OBSTRUCTION: R6 and original blobs differ")
    seed = raw.decode("utf-8")
    for old, new in (("namespace " + R6_NS, "namespace " + ORIGINAL_NS),
                     ("end " + R6_NS, "end " + ORIGINAL_NS)):
        guard(seed.count(old) == 1, "SOURCE_OBSTRUCTION: namespace normalization ambiguous")
        seed = seed.replace(old, new, 1)
    guard(seed.count(R6_PROOF) == 1, "SOURCE_OBSTRUCTION: R6 proof block changed")
    original_signatures = cycle.declarations(original.decode())
    guard(len(original_signatures) == 36, "DECLARATION_OBSTRUCTION: expected 36 original names")
    guard(not INBOX.exists() and not RECEIPTS.exists() and not APPROVED.exists()
          and not ADMISSION.exists(), "SANDBOX_OBSTRUCTION: temp evidence path reused")
    INBOX.mkdir(parents=True)
    RECEIPTS.mkdir(parents=True)
    declarations = list(original_signatures)
    manifest = []
    for i, (name, proof) in enumerate(REPAIRS, 1):
        candidate = seed.replace(R6_PROOF, proof, 1)
        contract = cycle.source_contract(original.decode("utf-8"), candidate,
                                         REASONS, {})
        guard(contract["public_declarations"] == declarations, "DECLARATION_OBSTRUCTION")
        guard(set(contract["signature_changes"]) == set(REASONS),
              "SIGNATURE_OBSTRUCTION: unexpected target statement edits")
        guard(not contract["import_additions"], "IMPORT_OBSTRUCTION")
        data = candidate.encode("utf-8")
        path = INBOX / f"{i:04d}-{name}.lean"
        with path.open("xb") as f:
            f.write(data)
        manifest.append({
            "sequence": i,
            "name": name,
            "file": path.name,
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": git_blob(data),
            "base_git_blob": R6_BLOB,
            "original_git_blob": ORIGINAL_BLOB,
            "named_declarations": len(declarations),
            "independent_ci_success": False,
            "proof_change_only": True,
            "memory_state": "TEST_REQUIRED",
        })
    ADMISSION.write_text(json.dumps({
        "signature_changes": [
            {"name": name, "reason": reason} for name, reason in REASONS.items()
        ],
        "import_additions": [],
    }, sort_keys=True, indent=2) + "\n")
    (RECEIPTS / "planned-candidates.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n"
    )
    return original, manifest

def real_mcp(candidate: bytes, selected: dict) -> None:
    disabled = ",".join([
        "lean_run_code", "lean_build", "lean_profile_proof",
        "lean_minimal_hypotheses", "lean_leansearch", "lean_loogle",
        "lean_leanfinder", "lean_state_search", "lean_hammer_premise",
    ])
    guard(not PROBE.exists(), "MCP_OBSTRUCTION: existing probe file")
    with PROBE.open("xb") as f:
        f.write(candidate)
    receipt = {
        "schema": "kuuos-v1102-multitrial-real-mcp-v1",
        "status": "MCP_NO_DATA",
        "candidate_blob": git_blob(candidate),
        "selected_attempt": selected["attempt"],
        "selected_name": selected["candidate_file"],
        "base_r6_blob": R6_BLOB,
        "independent_ci_success": False,
        "source_adopted": False,
        "git_write_performed": False,
    }
    client = None
    try:
        env = {
            "LEAN_PROJECT_PATH": str(ROOT), "LEAN_LOG_LEVEL": "NONE",
            "LEAN_MCP_SCRATCH_SLOTS": "1",
            "LEAN_MCP_DISABLED_TOOLS": disabled,
        }
        client = MCPClient(
            ["uvx", "--from", "lean-lsp-mcp==0.30.0",
             "lean-lsp-mcp", "--transport", "stdio"],
            cwd=ROOT, env=env, timeout_seconds=240
        )
        init = client.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "KuuOS v1.102 bounded multitrial", "version": "1"},
        })
        client.notify("notifications/initialized")
        tools = tool_map(client.request("tools/list"))
        guard("lean_diagnostic_messages" in tools and "lean_goal" in tools,
              "MCP_NO_DATA: semantic Lean MCP tools absent")
        guard("lean_build" not in tools and "lean_run_code" not in tools,
              "MCP_OBSTRUCTION: unsafe tools enabled")
        response = call_tool(client, "lean_diagnostic_messages",
                             {"file_path": str(PROBE.relative_to(ROOT)), "timeout_s": 120})
        observed = require_semantics(structured(response), candidate)
        receipt.update({
            "status": "MCP_TYPED_LOCAL_GREEN" if observed.success and not observed.errors
                      else "MCP_SEMANTIC_FAILED",
            "protocol": init.get("result", {}).get("protocolVersion"),
            "diagnostics_success": observed.success,
            "diagnostics_partial": observed.partial,
            "failed_dependencies": observed.failed_dependencies,
            "error_count": len(observed.errors),
            "diagnostic_count": len(observed.diagnostics),
            "diagnostic_preview": observed.diagnostics[:36],
        })
        guard(observed.success and not observed.errors,
              "MCP_OBSTRUCTION: semantic diagnostics not green")
    finally:
        if client is not None:
            client.close()
        if PROBE.exists():
            guard(PROBE.read_bytes() == candidate,
                  "MCP_OBSTRUCTION: temporary probe changed")
            PROBE.unlink()
        (RECEIPTS / "real-mcp-receipt.json").write_text(
            json.dumps(receipt, sort_keys=True, indent=2) + "\n"
        )
    guard(receipt["status"] == "MCP_TYPED_LOCAL_GREEN", "MCP_OBSTRUCTION")

def main() -> int:
    guard(os.getenv("GITHUB_ACTIONS") == "true", "RUNTIME_OBSTRUCTION: GitHub runner required")
    guard(os.getenv("GITHUB_REF_NAME") == BRANCH, "SOURCE_OBSTRUCTION: wrong branch")
    cycle.require_pins(ROOT)
    original, manifest = materialize_variants()
    args = argparse.Namespace(
        project_root=str(ROOT),
        source=str(SOURCE),
        source_blob=ORIGINAL_BLOB,
        source_head=os.environ.get("GITHUB_SHA"),
        namespace=ORIGINAL_NS,
        candidates_dir=str(INBOX),
        receipt_dir=str(RECEIPTS),
        admission=str(ADMISSION),
        max_attempts=len(manifest),
        timeout_seconds=500,
        idle_seconds=0, poll_seconds=2,
    )
    rc = cycle.run(args)
    ledger = RECEIPTS / "ledger.jsonl"
    records = [json.loads(x) for x in ledger.read_text().splitlines()] if ledger.exists() else []
    guard((ROOT / SOURCE).read_bytes() == original, "SOURCE_OBSTRUCTION: original file was mutated")
    green = [r for r in records if r.get("status") == "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY"]
    guard(rc == 0 and len(green) == 1 and len(records) <= len(manifest),
          "DIRECT_LEAN_NO_LOCAL_GREEN: all tested variants retained in append-only ledger")
    selected = green[0]
    chosen = INBOX / selected["candidate_file"]
    candidate = chosen.read_bytes()
    guard(git_blob(candidate) == selected["candidate_blob"], "SOURCE_OBSTRUCTION: accepted blob mismatch")
    guard(selected["axioms"]["checked"] == 36 and
          not set(selected["axioms"]["allowed"]) - STANDARD and
          selected["axioms"]["sorryAx"] is False and
          selected["direct_lean"]["exit_code"] == 0,
          "AXIOM_OBSTRUCTION: local Lean or full 36/36 axiom audit not green")
    real_mcp(candidate, selected)
    guard((ROOT / SOURCE).read_bytes() == original, "SOURCE_OBSTRUCTION: original source mutated")
    APPROVED.mkdir(parents=True, exist_ok=False)
    (APPROVED / "selected.lean").write_bytes(candidate)
    (APPROVED / "selected-source.json").write_text(json.dumps({
        "schema": "kuuos-v1102-local-green-source-selection-v1",
        "source_commit_sha": os.environ.get("GITHUB_SHA"),
        "original_blob": ORIGINAL_BLOB,
        "seed_r6_blob": R6_BLOB,
        "candidate_file": selected["candidate_file"],
        "candidate_blob": selected["candidate_blob"],
        "candidate_sha256": selected["candidate_sha256"],
        "attempts_executed": len(records),
        "direct_lean_success": True,
        "full_axiom_declarations_checked": 36,
        "real_mcp_local_green": True,
        "independent_ci_success": False,
        "source_adopted": False,
        "authorization": "LOCAL_ONLY",
    }, indent=2, sort_keys=True) + "\n")
    print("KUUOS_V1102_CODEAI_MULTI_TRIAL_LOCAL_GREEN_ONLY",
          json.dumps({"attempts": len(records), "selected": selected["candidate_file"],
                      "source_blob": selected["candidate_blob"],
                      "axiom_count": 36, "real_mcp": True,
                      "independent_ci_success": False}, sort_keys=True))
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        RECEIPTS.mkdir(parents=True, exist_ok=True)
        with (RECEIPTS / "sandbox-obstruction.txt").open("x") as f:
            f.write(type(e).__name__ + ": " + str(e) + "\n")
        print("KUUOS_V1102_CODEAI_MULTI_TRIAL_HOLD",
              type(e).__name__, str(e), file=sys.stderr)
        sys.exit(2)
