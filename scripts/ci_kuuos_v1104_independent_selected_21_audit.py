#!/usr/bin/env python3
"""KuuOS v1.104: independently recompile exactly the locally GREEN R3-A proof.
This only consumes completed sandbox receipts. It does not synthesize proofs,
modify the original formal source, promote CodeAI memory, or merge anything.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

REPO = "itakura-hidetoshi/KuuOS"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_BRANCH = "research/v1104-codeai-r3-independent-20261124"
SANDBOX_RUN = 45277456165
SANDBOX_HEAD = "35e78ab04f993f531065ccc414346d1bff0e3a10"
SANDBOX_JOB = 138052828576
WINNER_BLOB = "5c911aaeb9a21baff57f6af8c8655309af47d027"
WINNER_SHA256 = "e1b8e67f9744012d120e6d7ea67ba4f8ead0c9440161b3ca280ba9a82bccbf02"
PREDECESSOR_BLOB = "dbec61c9798481709f2deda0028e84b7515f209e"
LOW_BLOB = "f8b492b210e5525990aa587fa2eb5c8648a5ff19"
ORIGINAL_BLOB = "dc75c6d91c317bc8d350c7c45d4268dce38bf06c"
ENGINE_BLOB = "5383253dbe9cda9cab90a410c2fd66ee6b9d6f41"

ORIGINAL = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
HIGH = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
LOW = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean"
RESEARCH = ROOT / "research/codeai/v1104/r3/A-revert.lean"
SELECTED = Path("/tmp/kuuos-v1104-independent-selected")
LOCAL = Path("/tmp/kuuos-v1104-independent-local")
OUT = Path("/tmp/kuuos-v1104-independent-proof")
STAGING = ROOT / "formal/KUOS/.v1104-independent-kernel"
AXIOM_LOG = Path("/tmp/kuuos-v1104-independent-axioms.log")
OLEAN = Path("/tmp/kuuos-v1104-independent-selected.olean")
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}

def require(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError("KUUOS_V1104_INDEPENDENT_HOLD: " + why)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_blob(path: Path, blob: str) -> None:
    require(path.exists() and path.is_file() and not path.is_symlink() and
            cycle.git_blob(path.read_bytes()) == blob,
            "SOURCE_BLOB_MISMATCH: " + str(path))

def exactly_one(root: Path, name: str) -> Path:
    require(root.exists() and root.is_dir(), "MISSING_ARTIFACT_DIRECTORY: " + str(root))
    files = [p for p in root.rglob(name) if p.is_file() and not p.is_symlink()]
    require(len(files) == 1, "EXPECTED_SINGLE_ARTIFACT_FILE " + name)
    return files[0]

def api_get(path: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN", "")
    require(bool(token), "NO_GITHUB_TOKEN")
    req = Request(
        "https://api.github.com/repos/" + REPO + path,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KuuOS-v1104-independent-kernel-source-bound",
        })
    with urlopen(req, timeout=40) as response:
        return json.load(response)

def exact_upstream() -> dict:
    run = api_get("/actions/runs/" + str(SANDBOX_RUN))
    require(
        run.get("head_sha") == SANDBOX_HEAD and run.get("status") == "completed" and
        run.get("conclusion") == "success" and run.get("run_attempt") == 1 and
        run.get("head_branch") == "research/v1104-codeai-r3-multitrial-20261124",
        "SOURCE_SANDBOX_NOT_EXACT_COMPLETED_SUCCESS")
    jobs = api_get("/actions/runs/" + str(SANDBOX_RUN) + "/jobs?per_page=100").get("jobs", [])
    require(len(jobs) == 1, "SOURCE_SANDBOX_JOB_COUNT_MISMATCH")
    job = jobs[0]
    require(
        job.get("id") == SANDBOX_JOB and
        job.get("name") == "v1104-codeai-r3-serial-real-lean-mcp-local" and
        job.get("status") == "completed" and job.get("conclusion") == "success",
        "SOURCE_SANDBOX_JOB_NOT_GREEN")
    expected_steps = [
        "Pin original, certified imports, CodeAI 3-candidate source and Python scripts",
        "Build certified exact v1.103 dependency only, no full parent Governance",
        "CodeAI R3 direct Lean serial candidates with 21 axioms then real Lean MCP",
        "Export selected exact local GREEN bytes for later independent Lean runner",
    ]
    completed = {s.get("name") for s in job.get("steps", [])
                 if s.get("status") == "completed" and s.get("conclusion") == "success"}
    require(set(expected_steps) <= completed, "SOURCE_SANDBOX_REQUIRED_STEPS_MISSING")
    artifacts = api_get("/actions/runs/" + str(SANDBOX_RUN) + "/artifacts?per_page=100").get("artifacts", [])
    expected = {
        "kuuos-v1104-r3-multitrial-direct-lean-21-axioms-mcp-receipts": 14868128032,
        "kuuos-v1104-r3-local-green-selected-source": 14866879267,
    }
    for name, id_ in expected.items():
        matching = [a for a in artifacts if a.get("name") == name and not a.get("expired")]
        require(len(matching) == 1 and matching[0].get("id") == id_,
                "SOURCE_ARTIFACT_ID_NOT_EXACT: " + name)
    return {"run": SANDBOX_RUN, "head": SANDBOX_HEAD, "job": SANDBOX_JOB,
            "status": "COMPLETED_SUCCESS"}

def contract(original: str, candidate: str) -> dict:
    left, right = cycle.declarations(original), cycle.declarations(candidate)
    require(len(left) == 21 and list(left) == list(right) and
            list(left)[-1] == "natDoubleDelooping_standardTypeA_rlp",
            "PUBLIC_DECLARATIONS_NOT_21_OR_REORDERED")
    reasons = {}
    for name in left:
        if left[name] == right[name]:
            continue
        if name == "natTypeAHornLabel_tetrahedron_of_hornSimplex":
            expect = left[name].replace("(Λ[g.n, g.i] : SSet)", "(Λ[g.n, g.i] : SSet.{0})")
            reason = "Explicit Type0 universe of original horn carrier"
        elif name == "natTypeAFourCocycle_distinguished_zero":
            expect = left[name].replace(
                "(natTypeAFourCocycle i h0 h4 f).TypeADistinguishedZero i",
                "KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101."
                "NatNormalizedDuskinCocycle.TypeADistinguishedZero "
                "(natTypeAFourCocycle i h0 h4 f) i")
            reason = "Resolve certified v1.101 predicate instead of invalid field projection"
        else:
            raise RuntimeError("UNAUTHORIZED_SIGNATURE_CHANGE " + name)
        require(right[name] == expect, "UNREVIEWED_INTERFACE_CHANGE: " + name)
        reasons[name] = reason
    require(set(reasons) == {
        "natTypeAHornLabel_tetrahedron_of_hornSimplex",
        "natTypeAFourCocycle_distinguished_zero",
    }, "REQUIRED_INTERFACE_CORRECTIONS_MISSING")
    result = cycle.source_contract(original, candidate, reasons, {})
    require(cycle.imports(candidate) == [
        "KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103"
    ], "IMPORT_OBSTRUCTION")
    require(result["import_additions"] == {}, "UNEXPECTED_IMPORT")
    return result

def local_green_receipts(data: bytes) -> dict:
    selected = json.loads(exactly_one(SELECTED, "selected-source.json").read_text())
    require(
        selected["candidate"] == "A-revert" and selected["git_blob"] == WINNER_BLOB and
        selected["source_sha"] == SANDBOX_HEAD and
        selected["original_blob"] == ORIGINAL_BLOB and
        selected["v102_blob"] == LOW_BLOB and
        selected["v103_blob"] == PREDECESSOR_BLOB and
        selected["public_decl_count"] == 21 and
        selected["local_direct_lean"] is True and
        selected["local_axiom_21"] is True and
        selected["real_lean_mcp"] is True and
        selected["independent_ci_started"] is False and
        selected["PR_3555_modified"] is False,
        "SELECTED_LOCAL_GREEN_MANIFEST_MISMATCH")
    receipt = json.loads(exactly_one(LOCAL, "receipt.json").read_text())
    require(
        receipt["candidate"] == "A-revert" and receipt["blob"] == WINNER_BLOB and
        receipt["source_sha"] == SANDBOX_HEAD and
        receipt["status"] == "LOCAL_DIRECT_AND_21_AXIOMS_GREEN" and
        receipt["original_blob"] == ORIGINAL_BLOB and
        receipt["dependency_blob"] == PREDECESSOR_BLOB and
        receipt["direct"]["direct_success"] is True and
        receipt["direct"]["exit_code"] == 0 and
        receipt["direct"]["error_count"] == 0 and
        receipt["audit_direct"]["direct_success"] is True and
        receipt["audit_direct"]["exit_code"] == 0 and
        receipt["audit_direct"]["error_count"] == 0 and
        receipt["axioms"]["checked"] == 21 and
        receipt["axioms"]["sorryAx"] is False and
        receipt["axioms"]["nonstandard"] == [] and
        not set(receipt["axioms"]["allowed"]) - STANDARD and
        receipt["independent_ci_started"] is False and
        receipt["PR_3555_modified"] is False,
        "LOCAL_DIRECT_AXIOM_21_RECEIPT_NOT_GREEN")
    mcp = json.loads(exactly_one(LOCAL, "real-lean-mcp-receipt.json").read_text())
    require(
        mcp["candidate_blob"] == WINNER_BLOB and mcp["status"] == "MCP_TYPED_LOCAL_GREEN" and
        mcp["version"] == "lean-lsp-mcp==0.30.0" and
        mcp["diagnostics_success"] is True and mcp["partial"] is False and
        mcp["error_count"] == 0 and mcp["failed_dependencies"] == [] and
        mcp["independent_ci_success"] is False,
        "REAL_TYPED_LEAN_MCP_NOT_GREEN")
    summary = json.loads(exactly_one(LOCAL, "summary.json").read_text())
    require(
        summary["source_sha"] == SANDBOX_HEAD and summary["selected"] == "A-revert" and
        summary["status"] == "LOCAL_LEAN_21_AXIOMS_AND_REAL_MCP_GREEN" and
        summary["original_blob"] == ORIGINAL_BLOB and
        summary["v102_blob"] == LOW_BLOB and summary["v103_blob"] == PREDECESSOR_BLOB and
        summary["independent_ci_started"] is False and
        summary["PR_3555_modified"] is False and
        len(summary["trials"]) == 1 and
        summary["trials"][0]["blob"] == WINNER_BLOB,
        "LOCAL_SUMMARY_MISMATCH")
    require(cycle.git_blob(data) == selected["git_blob"], "SELECTED_BYTES_NOT_FROM_GREEN")
    return {
        "summary_sha256": sha256(exactly_one(LOCAL, "summary.json").read_bytes()),
        "mcp_sha256": sha256(exactly_one(LOCAL, "real-lean-mcp-receipt.json").read_bytes()),
        "local_axioms": receipt["axioms"],
        "candidate": "A-revert"
    }

def prepare() -> None:
    require(os.environ.get("GITHUB_ACTIONS") == "true" and
            os.environ.get("GITHUB_REF_NAME") == SOURCE_BRANCH,
            "WRONG_INDEPENDENT_RUNNER_OR_BRANCH")
    upstream = exact_upstream()
    require(cycle.git_blob((ROOT / "scripts/kuuos_sandbox_lean_cycle_v1.py").read_bytes())
            == ENGINE_BLOB, "CODEAI_ENGINE_PIN_CHANGED")
    for path, blob in ((ORIGINAL, ORIGINAL_BLOB), (HIGH, PREDECESSOR_BLOB),
                       (LOW, LOW_BLOB), (RESEARCH, WINNER_BLOB)):
        verify_blob(path, blob)
    require(cycle.imports(ORIGINAL.read_text()) == [
        "KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103"
    ], "ORIGINAL_IMPORT_DIFFERENT")
    require(cycle.require_pins(ROOT, verify_binaries=False) == {
        "lean_toolchain": "leanprover/lean4:v4.30.0-rc2",
        "mathlib_sha": "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
    }, "FIXED_ENVIRONMENT_MISMATCH")
    selected_bytes = exactly_one(SELECTED, "selected.lean").read_bytes()
    require(cycle.git_blob(selected_bytes) == WINNER_BLOB and
            sha256(selected_bytes) == WINNER_SHA256 and
            selected_bytes == RESEARCH.read_bytes(), "SELECTED_BYTES_BLOB_SHA256_OR_REPO_MISMATCH")
    contract_result = contract(ORIGINAL.read_text(), selected_bytes.decode("utf-8"))
    local = local_green_receipts(selected_bytes)
    require(not STAGING.exists() and not OUT.exists() and not OLEAN.exists(),
            "INDEPENDENT_OUTPUT_PATH_ALREADY_EXISTS")
    STAGING.mkdir(parents=True)
    (STAGING / "Selected.lean").write_bytes(selected_bytes)
    names = contract_result["public_declarations"]
    (STAGING / "AxiomAudit.lean").write_text(
        selected_bytes.decode("utf-8") + "\n" +
        "\n".join("#print axioms " + NAMESPACE + "." + name for name in names) + "\n",
        encoding="utf-8",
    )
    OUT.mkdir()
    data = {
        "schema": "kuuos-v1104-independent-selected-21-axioms-v1",
        "independent_head": os.environ["GITHUB_SHA"],
        "upstream": upstream,
        "winner_blob": WINNER_BLOB,
        "winner_sha256": WINNER_SHA256,
        "original_blob": ORIGINAL_BLOB,
        "predecessor_blob": PREDECESSOR_BLOB,
        "low_blob": LOW_BLOB,
        "contract": contract_result,
        "local": local,
        "independent_ci_success": False,
        "formal_PR_3555_mutated": False,
        "merged": False,
    }
    (OUT / "prepared.json").write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")
    print("KUUOS_V1104_INDEPENDENT_EXACT_SOURCE_PREPARED", json.dumps({
        "winner_blob": WINNER_BLOB, "winner_sha256": WINNER_SHA256,
        "public_declarations": len(names), "independent_ci_success": False,
    }, sort_keys=True), flush=True)

def complete() -> None:
    prepared = json.loads((OUT / "prepared.json").read_text())
    source = (STAGING / "Selected.lean").read_bytes()
    require(cycle.git_blob(source) == WINNER_BLOB and sha256(source) == WINNER_SHA256,
            "SOURCE_CHANGED_DURING_INDEPENDENT_LEAN")
    require(OLEAN.is_file() and OLEAN.stat().st_size > 0,
            "INDEPENDENT_LEAN_OLEAN_NOT_CREATED")
    require(AXIOM_LOG.is_file(), "INDEPENDENT_AX_YEARS_NO_DATA")
    axioms = cycle.audit_axioms(AXIOM_LOG.read_text(encoding="utf-8"), 
                               prepared["contract"]["public_declarations"], NAMESPACE)
    require(axioms["checked"] == 21 and axioms["sorryAx"] is False and
            axioms["nonstandard"] == [] and not set(axioms["allowed"]) - STANDARD,
            "INDEPENDENT_21_AXIOMS_NOT_ALLOWED")
    for path, blob in ((ORIGINAL, ORIGINAL_BLOB), (HIGH, PREDECESSOR_BLOB),
                       (LOW, LOW_BLOB), (RESEARCH, WINNER_BLOB)):
        verify_blob(path, blob)
    receipt = {
        "schema": "kuuos-v1104-independent-selected-21-axioms-v1",
        "independent_head": os.environ["GITHUB_SHA"],
        "upstream_sandbox_run": SANDBOX_RUN,
        "upstream_sandbox_head": SANDBOX_HEAD,
        "candidate_git_blob": WINNER_BLOB,
        "candidate_sha256": WINNER_SHA256,
        "local_axiom_count": prepared["local"]["local_axioms"]["checked"],
        "independent_axioms": axioms,
        "independent_compilation": "SUCCESS",
        "sorryAx": False,
        "warnings": 0,
        "errors": 0,
        "independent_ci_success": True,
        "PR_3555_source_modified": False,
        "merged": False,
        "authority": "EXACT_SOURCE_INDEPENDENT_KERNEL_ONLY",
        "limit": "Does not certify PR Governance, all standard type-A RLP beyond candidate source scope, or global fibrancy"
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2) + "\n")
    print("KUUOS_V1104_INDEPENDENT_21_AXIOMS_GREEN",json.dumps({
        "candidate": WINNER_BLOB, "decl": 21,
        "axioms": axioms, "independent_ci_success": True,
    },sort_keys=True),flush=True)

if __name__ == "__main__":
    try:
        require(len(sys.argv) == 2 and sys.argv[1] in ("prepare", "complete"),
                "EXPECTED_PREPARE_OR_COMPLETE")
        (prepare if sys.argv[1] == "prepare" else complete)()
    except Exception as exc:
        OUT.mkdir(exist_ok=True)
        (OUT / "obstruction.txt").write_text(type(exc).__name__ + ": " + str(exc) + "\n")
        print("KUUOS_V1104_INDEPENDENT_HOLD", type(exc).__name__, str(exc), file=sys.stderr)
        raise SystemExit(2)
