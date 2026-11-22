#!/usr/bin/env python3
"""v1.102 GitHub-hosted isolated Sandbox: pinned direct Lean -> axioms -> real Lean MCP.

NO independent CI, original theorem edits, GitHub writes, merge, or authority grant.
R2 is never adopted from this process. All receipts are outside the worktree.
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
SOURCE = Path("formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean")
R2 = Path("formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersCodeAICandidateR2V1_102.lean")
ORIGINAL_BLOB = "7274ceba97bb4bf7b3aaffa9862952d79cf6f4c3"
R2_BLOB = "641800b1d4f2c1763a0bcb3cccc23b80d666a245"
BASE_PR_HEAD = "92608af59fa6eb4f3fc2b755e755d7b2a6cad2e3"
ORIGINAL_NS = "KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102"
R2_NS = "KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersCodeAICandidateR2V1_102"
RECEIPTS = Path("/tmp/kuuos-v1102-r2-sandbox-receipts")
INBOX = Path("/tmp/kuuos-v1102-r2-sandbox-inbox")
CANDIDATE = INBOX / "0001-R2-original-namespace.lean"
MCP_FILE = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersSandboxProbeV1_102.lean"
MCP_REL = str(MCP_FILE.relative_to(ROOT))
REASONS = {
    "natDuskin_mapId_eq_zero": "Clarify numeral as Nat.zero for a 2-cell; original target remains definitionally equivalent.",
    "natThreeCocycle_typeA_i1_zero": "Resolve the actual v1.101 predicate by its fully qualified constant, preserving its argument and property.",
    "natThreeCocycle_typeA_i2_zero": "Resolve the actual v1.101 predicate by its fully qualified constant, preserving its argument and property.",
    "natTypeAThreeI1Label012_eq_zero": "Fix elaboration of the zero comparison with Nat.zero, without changing the mathematical target.",
    "natTypeAThreeI2Label123_eq_zero": "Fix elaboration of the zero comparison with Nat.zero, without changing the mathematical target.",
}

def fail_closed(message: str) -> None:
    raise cycle.Hold(message)

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def prepare_candidate() -> tuple[bytes, bytes, list[str]]:
    original = (ROOT / SOURCE).read_bytes()
    raw = (ROOT / R2).read_bytes()
    if blob(original) != ORIGINAL_BLOB or blob(raw) != R2_BLOB:
        fail_closed("SOURCE_OBSTRUCTION: original/R2 exact Git blobs do not match")
    if (ROOT / SOURCE).is_symlink() or (ROOT / R2).is_symlink():
        fail_closed("SOURCE_OBSTRUCTION: symlink source")
    original_text = original.decode("utf-8")
    candidate_text = raw.decode("utf-8")
    for old, new in (("namespace " + R2_NS, "namespace " + ORIGINAL_NS),
                     ("end " + R2_NS, "end " + ORIGINAL_NS)):
        if candidate_text.count(old) != 1:
            fail_closed("SOURCE_OBSTRUCTION: named namespace normalization not unique")
        candidate_text = candidate_text.replace(old, new, 1)
    candidate = candidate_text.encode("utf-8")
    orig_signatures = cycle.declarations(original_text)
    revised_signatures = cycle.declarations(candidate_text)
    if list(orig_signatures) != list(revised_signatures) or len(orig_signatures) != 36:
        fail_closed("DECLARATION_OBSTRUCTION: 36 original public names/order not preserved")
    changed = [name for name in orig_signatures if orig_signatures[name] != revised_signatures[name]]
    if set(changed) != set(REASONS):
        fail_closed("SIGNATURE_OBSTRUCTION: unexpected original/R2 statement changes: " + str(changed))
    contract = cycle.source_contract(
        original_text, candidate_text, {name: REASONS[name] for name in changed}, {}
    )
    if len(contract["public_declarations"]) != 36 or contract["import_additions"]:
        fail_closed("SOURCE_OBSTRUCTION: candidate contract mismatch")
    return original, candidate, changed

def real_mcp(candidate: bytes) -> None:
    # The existing KuuOS MCP implementation is invoked only after direct
    # Lean and the 36-declaration axiom audit have returned LOCAL_GREEN.
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
        MCPClient, PROTOCOL_VERSION, call_tool, tool_map,
    )
    from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
    from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics
    disabled = ",".join([
        "lean_run_code", "lean_build", "lean_profile_proof",
        "lean_minimal_hypotheses", "lean_leansearch", "lean_loogle",
        "lean_leanfinder", "lean_state_search", "lean_hammer_premise",
    ])
    if MCP_FILE.exists():
        fail_closed("MCP sandbox probe path already exists")
    with MCP_FILE.open("xb") as handle:
        handle.write(candidate)
    receipt = {
        "schema": "kuuos-v1102-r2-github-sandbox-real-mcp-v1",
        "status": "MCP_NO_DATA",
        "mcp_version": "lean-lsp-mcp==0.30.0",
        "normalized_candidate_blob": blob(candidate),
        "R2_source_blob": R2_BLOB,
        "independent_ci_success": False,
        "git_write_performed": False,
        "authority": "LOCAL_ONLY",
    }
    client = None
    try:
        env = {
            "LEAN_PROJECT_PATH": str(ROOT),
            "LEAN_LOG_LEVEL": "NONE",
            "LEAN_MCP_SCRATCH_SLOTS": "1",
            "LEAN_MCP_DISABLED_TOOLS": disabled,
        }
        client = MCPClient(
            ["uvx", "--from", "lean-lsp-mcp==0.30.0",
             "lean-lsp-mcp", "--transport", "stdio"],
            cwd=ROOT, env=env, timeout_seconds=240,
        )
        initialized = client.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "KuuOS v1.102 isolated Sandbox", "version": "1"},
        })
        client.notify("notifications/initialized")
        tools = tool_map(client.request("tools/list"))
        if "lean_diagnostic_messages" not in tools:
            fail_closed("MCP_NO_DATA: lean_diagnostic_messages unavailable")
        if "lean_run_code" in tools or "lean_build" in tools:
            fail_closed("MCP_OBSTRUCTION: high-effect tools exposed")
        response = call_tool(
            client, "lean_diagnostic_messages",
            {"file_path": MCP_REL, "timeout_s": 120},
        )
        observed = require_semantics(structured(response), candidate)
        receipt.update({
            "status": "MCP_TYPED_LOCAL_GREEN" if observed.success and not observed.errors
                      else "MCP_SEMANTIC_FAILED",
            "mcp_protocol": initialized.get("result", {}).get("protocolVersion"),
            "diagnostics_success": observed.success,
            "diagnostics_partial": observed.partial,
            "diagnostics_count": len(observed.diagnostics),
            "failed_dependencies": observed.failed_dependencies,
            "error_count": len(observed.errors),
            "diagnostics": observed.diagnostics[:36],
        })
        if not observed.success or observed.errors:
            fail_closed("MCP_OBSTRUCTION: candidate has semantic diagnostic errors")
    finally:
        if client is not None:
            client.close()
        if MCP_FILE.exists():
            if MCP_FILE.read_bytes() != candidate:
                fail_closed("MCP_OBSTRUCTION: local probe unexpectedly mutated")
            MCP_FILE.unlink()
        RECEIPTS.mkdir(parents=True, exist_ok=True)
        (RECEIPTS / "real-mcp-receipt.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        )
    if receipt["status"] != "MCP_TYPED_LOCAL_GREEN":
        fail_closed("MCP_NO_DATA: typed green response not received")
    print("KUUOS_V1102_SANDBOX_DIRECT_LEAN_AXIOMS_REAL_MCP_LOCAL_GREEN_ONLY",
          json.dumps({k: receipt[k] for k in (
              "status", "normalized_candidate_blob", "diagnostics_count",
              "independent_ci_success", "authority")}))

def main() -> int:
    if os.getenv("GITHUB_ACTIONS") != "true":
        fail_closed("RUNTIME_OBSTRUCTION: isolated GitHub-hosted runner required")
    if os.getenv("GITHUB_REF_NAME") != "research/v1.102-codeai-r2-structure-20261123":
        fail_closed("SOURCE_OBSTRUCTION: unexpected research sandbox branch")
    if (ROOT / "lean-toolchain").read_text().strip() != cycle.LEAN_PIN:
        fail_closed("PIN_MISMATCH: lean toolchain")
    cycle.require_pins(ROOT, verify_binaries=True)
    original, candidate, changed = prepare_candidate()
    if INBOX.exists() or RECEIPTS.exists():
        fail_closed("SANDBOX_OBSTRUCTION: candidate inbox/receipt directory reused")
    INBOX.mkdir(parents=True)
    RECEIPTS.mkdir(parents=True)
    with CANDIDATE.open("xb") as output:
        output.write(candidate)
    admission = Path("/tmp/kuuos-v1102-r2-sandbox-admission.json")
    if admission.exists():
        fail_closed("SANDBOX_OBSTRUCTION: stale admission file")
    admission.write_text(json.dumps({
        "signature_changes": [
            {"name": name, "reason": REASONS[name]} for name in changed
        ],
        "import_additions": [],
    }, indent=2) + "\n")
    args = argparse.Namespace(
        project_root=str(ROOT), source=str(SOURCE),
        source_blob=ORIGINAL_BLOB, source_head=BASE_PR_HEAD,
        namespace=ORIGINAL_NS, candidates_dir=str(INBOX),
        receipt_dir=str(RECEIPTS), admission=str(admission),
        max_attempts=1, timeout_seconds=700, idle_seconds=0,
        poll_seconds=3,
    )
    rc = cycle.run(args)
    records = [json.loads(line) for line in (RECEIPTS / "ledger.jsonl").read_text().splitlines()]
    if len(records) != 1 or rc != 0:
        fail_closed("DIRECT_LEAN_FAILED: sandbox candidate not local green")
    result = records[0]
    if (result.get("status") != "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY"
        or result.get("candidate_blob") != blob(candidate)
        or result.get("axioms", {}).get("checked") != 36
        or result.get("independent_ci_success") is not False):
        fail_closed("AXIOM_OBSTRUCTION: exact 36-declaration local receipt missing")
    if (ROOT / SOURCE).read_bytes() != original:
        fail_closed("SOURCE_OBSTRUCTION: original source was modified")
    real_mcp(candidate)
    if (ROOT / SOURCE).read_bytes() != original:
        fail_closed("SOURCE_OBSTRUCTION: original source mutated after real MCP")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        RECEIPTS.mkdir(parents=True, exist_ok=True)
        with (RECEIPTS / "sandbox-obstruction.txt").open("w") as f:
            f.write(str(type(exc).__name__) + ": " + str(exc) + "\n")
        print("KUUOS_V1102_SANDBOX_HOLD", str(type(exc).__name__), str(exc), file=sys.stderr)
        sys.exit(2)
