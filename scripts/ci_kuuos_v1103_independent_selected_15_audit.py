#!/usr/bin/env python3
"""Independent v1.103 proof audit on a *different* GitHub runner.

This entrypoint never generates new proof candidates, edits formal source, calls
git/gh, promotes CodeAI memory, or merges PRs. It consumes the winning local
sandbox artifacts and checks exact Git object bytes and provenance, then writes
two Lean inputs for an independent kernel/audit pass. All data are fail-closed.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle
from scripts import ci_kuuos_v1103_second_five_trial_sandbox as trial

ROOT = Path(__file__).resolve().parents[1]
REPO = "itakura-hidetoshi/KuuOS"
SANDBOX_RUN = 45165964775
SANDBOX_HEAD = "66e1d236e9e03c01d4ff3a0806fb673891a88a26"
WINNING_BLOB = "dbec61c9798481709f2deda0028e84b7515f209e"
WINNING_SHA256 = "63ee3997ab664ede85a7b24176cbd1729e892128a9aa7b8a8de0b0f81df66094"
WINNING_FILE = "0001-F-calc-defeq-plain-simple-congr.lean"
SCRIPT_BLOB = "da0c43ffd3eb4bc8815d87b80fd8b76e0299f90f"
SELECTED = Path("/tmp/kuuos-v1103-independent-selected")
LOCAL = Path("/tmp/kuuos-v1103-independent-local")
OUT = Path("/tmp/kuuos-v1103-independent-proof")
STAGING = ROOT / "formal/KUOS/.v1103-independent-kernel"
NAMES = 15
STANDARD = {"propext", "Classical.choice", "Quot.sound"}

def require(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError("INDEPENDENT_HOLD: " + why)

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def one_file(p: Path, name: str) -> Path:
    found = list(p.rglob(name))
    require(len(found) == 1, "exactly one " + name + ", got " + str(len(found)))
    return found[0]

def github_get(endpoint: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN", "")
    require(bool(token), "GITHUB_TOKEN needed for read-only run authenticity")
    req = Request(
        "https://api.github.com/repos/" + REPO + endpoint,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KuuOS-v1103-Independent-Proof-Only",
        },
    )
    with urlopen(req, timeout=30) as response:
        return json.load(response)

def run_receipt() -> dict:
    upstream = github_get("/actions/runs/" + str(SANDBOX_RUN))
    require(upstream["head_sha"] == SANDBOX_HEAD and
            upstream["status"] == "completed" and upstream["conclusion"] == "success" and
            upstream["run_attempt"] == 1,
            "upstream run must be pinned and completed/success")
    jobs = github_get("/actions/runs/" + str(SANDBOX_RUN) + "/jobs?per_page=100")
    js = jobs.get("jobs", [])
    require(len(js) == 1 and
            js[0]["name"] == "pinned-isolated-five-candidate-local-lean" and
            js[0]["status"] == "completed" and js[0]["conclusion"] == "success",
            "upstream sandbox job must be unambiguously successful")
    return {"upstream_run": SANDBOX_RUN, "upstream_head": SANDBOX_HEAD,
            "sandbox_job": js[0]["id"], "status": "SANDBOX_COMPLETED_SUCCESS"}

def reconstruct(source: str) -> str:
    obj = trial.exact_once(
        source,
        "            natSimplex_triangle_face_comparison\n",
        "            NatNormalizedDuskinCocycle.natSimplex_triangle_face_comparison\n",
    )
    obj = trial.exact_once(
        obj,
        "    (natTypeAHighCocycle g hn f).TypeADistinguishedZero g.i := by",
        "    KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101.NatNormalizedDuskinCocycle.TypeADistinguishedZero\n"
        "      (natTypeAHighCocycle g hn f) g.i := by",
    )
    obj = trial.exact_once(obj, trial.ORIGINAL_HNAT, trial.HNAT_PROOFS["calc"])
    obj = trial.exact_once(obj, trial.ORIGINAL_MAP2, trial.MAP2_PROOFS["defeq"])
    obj = trial.exact_once(obj, trial.ORIGINAL_EXT, trial.EXT_PROOFS["plain"])
    obj = trial.exact_once(obj, trial.ORIGINAL_CONGR, trial.CONGR_PROOFS["simple-congr"])
    return obj

def source_receipt() -> dict:
    require(os.environ.get("GITHUB_ACTIONS") == "true",
            "must run on a fresh GitHub Actions runner")
    require(os.environ.get("GITHUB_REF_NAME") ==
            "research/v1103-codeai-second-local-five-20261123",
            "unexpected independent research branch")
    require(cycle.git_blob((ROOT / "scripts/ci_kuuos_v1103_second_five_trial_sandbox.py").read_bytes())
            == SCRIPT_BLOB, "CodeAI repair generator source changed")
    require(cycle.git_blob((ROOT / trial.SOURCE).read_bytes()) == trial.ORIGINAL_BLOB,
            "v1.103 original source changed")
    require(cycle.git_blob((ROOT / trial.IMPORT_V102).read_bytes()) == trial.IMPORT_V102_BLOB,
            "adopted v1.102 independent source changed")
    cycle.require_pins(ROOT, verify_binaries=False)

    candidate = (SELECTED / "selected.lean").read_bytes()
    selected = json.loads((SELECTED / "selected-source.json").read_text())
    require(cycle.git_blob(candidate) == WINNING_BLOB and
            sha256(candidate) == WINNING_SHA256,
            "candidate not byte-for-byte same as local certified blob and SHA256")
    require(selected["source_commit_sha"] == SANDBOX_HEAD and
            selected["original_blob"] == trial.ORIGINAL_BLOB and
            selected["v102_import_blob"] == trial.IMPORT_V102_BLOB and
            selected["selected_file"] == WINNING_FILE and
            selected["candidate_blob"] == WINNING_BLOB and
            selected["candidate_sha256"] == WINNING_SHA256 and
            selected["trials_executed"] == 1 and
            selected["direct_lean_success"] is True and
            selected["axiom_declarations_checked"] == 15 and
            selected["typed_lean_mcp_success"] is True and
            selected["independent_ci_success"] is False and
            selected["PR_source_adopted"] is False,
            "sandbox GREEN receipt inconsistent")

    source = (ROOT / trial.SOURCE).read_text()
    expected = reconstruct(source)
    require(candidate == expected.encode(), "selected bytes differ from exact CodeAI proof patch")
    contract = cycle.source_contract(source, expected, trial.REASONS, {})
    names = list(cycle.declarations(expected))
    require(names == contract["public_declarations"] and len(names) == NAMES and
            "toSimplexMap_mapComp" in names and
            set(contract["signature_changes"]) == set(trial.REASONS) and
            contract["import_additions"] == {},
            "15 original declarations, namespace or signature contract invalid")
    require(not STAGING.exists(), "stale independent proof staging path")
    STAGING.mkdir(parents=True, exist_ok=False)
    (STAGING / "Selected.lean").write_bytes(candidate)
    qualified = [
        "NatNormalizedDuskinCocycle.toSimplexMap_mapComp"
        if name == "toSimplexMap_mapComp" else name for name in names
    ]
    namespace = trial.NAMESPACE
    (STAGING / "AxiomAudit.lean").write_text(
        expected + "\n" +
        "\n".join("#print axioms " + namespace + "." + n for n in qualified) + "\n"
    )
    return {"candidate_blob": WINNING_BLOB, "candidate_sha256": WINNING_SHA256,
            "names": names, "qualified_names": qualified, "namespace": namespace,
            "contract": contract}

def local_receipt() -> dict:
    ledger = one_file(LOCAL, "ledger.jsonl")
    mcpfile = one_file(LOCAL, "real-mcp-receipt.json")
    rows = [json.loads(x) for x in ledger.read_text().splitlines()]
    require(len(rows) == 1, "expected first winner and no second trial")
    r = rows[0]
    mcp = json.loads(mcpfile.read_text())
    require(r["status"] == "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY" and
            r["candidate_file"] == WINNING_FILE and
            r["candidate_blob"] == WINNING_BLOB and
            r["candidate_sha256"] == WINNING_SHA256 and
            r["claimed_source_head"] == SANDBOX_HEAD and
            r["original_blob"] == trial.ORIGINAL_BLOB and
            r["import_v102_blob"] == trial.IMPORT_V102_BLOB and
            r["direct_lean"]["exit_code"] == 0 and
            r["direct_lean"]["error_count"] == 0 and
            r["axiom_run"]["exit_code"] == 0 and
            r["axioms"]["checked"] == NAMES and
            r["axioms"]["sorryAx"] is False and
            not set(r["axioms"]["allowed"]) - STANDARD,
            "local direct Lean and 15 axiom receipts not green")
    require(mcp["status"] == "MCP_TYPED_LOCAL_GREEN" and
            mcp["candidate_blob"] == WINNING_BLOB and
            mcp["selected_attempt"] == 1 and
            mcp["diagnostics_success"] is True and
            mcp["diagnostics_partial"] is False and
            mcp["error_count"] == 0 and
            not mcp["failed_dependencies"] and
            mcp["independent_ci_success"] is False,
            "typed real lean-lsp-mcp 0.30.0 not source-bound green")
    return {"local": r, "mcp": mcp,
            "local_ledger_sha256": sha256(ledger.read_bytes()),
            "real_mcp_sha256": sha256(mcpfile.read_bytes())}

def prepare():
    ci = run_receipt()
    src = source_receipt()
    local = local_receipt()
    OUT.mkdir(parents=True, exist_ok=False)
    data = {
        "schema": "kuuos-v1103-independent-selected-proof-v1",
        "source_commit_sha": os.environ.get("GITHUB_SHA"),
        "upstream": ci,
        "git_blob": WINNING_BLOB,
        "sha256": WINNING_SHA256,
        "original_blob": trial.ORIGINAL_BLOB,
        "v102_blob": trial.IMPORT_V102_BLOB,
        "public_declarations": src["names"],
        "qualified_declarations": src["qualified_names"],
        "local_ledger_sha256": local["local_ledger_sha256"],
        "real_mcp_sha256": local["real_mcp_sha256"],
        "local_axioms": local["local"]["axioms"],
        "independent_ci_success": False,
        "git_mutation": False,
        "merged": False,
    }
    (OUT / "prepared.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    print("KUUOS_V1103_INDEPENDENT_EXACT_GREEN_SOURCE_PREPARED",
          json.dumps({k:data[k] for k in ("git_blob", "sha256", "source_commit_sha",
                                          "independent_ci_success")}, sort_keys=True))

def complete():
    prepared = json.loads((OUT / "prepared.json").read_text())
    source = (STAGING / "Selected.lean").read_bytes()
    require(cycle.git_blob(source) == WINNING_BLOB,
            "source changed between independent preflight and kernel")
    reportfile = Path("/tmp/kuuos-v1103-independent-axioms.log")
    report = reportfile.read_text(encoding="utf-8")
    result = cycle.audit_axioms(
        report,
        prepared["qualified_declarations"],
        trial.NAMESPACE
    )
    require(result["checked"] == NAMES and result["sorryAx"] is False and
            not set(result["allowed"]) - STANDARD,
            "independent kernel 15-axiom result does not meet strict standard")
    require(Path("/tmp/kuuos-v1103-independent-selected.olean").is_file(),
            "compiled independent OLean artifact missing")
    receipt = {
        "schema": "kuuos-v1103-independent-selected-proof-v1",
        "source_commit_sha": prepared["source_commit_sha"],
        "upstream_sandbox_run": SANDBOX_RUN,
        "upstream_source_sha": SANDBOX_HEAD,
        "original_blob": trial.ORIGINAL_BLOB,
        "candidate_blob": WINNING_BLOB,
        "candidate_sha256": WINNING_SHA256,
        "v102_certified_import_blob": trial.IMPORT_V102_BLOB,
        "independent_public_declarations": result["checked"],
        "independent_axioms": result,
        "independent_axiom_log_sha256": sha256(reportfile.read_bytes()),
        "independent_kernel_olean_created": True,
        "local_real_mcp_sha256": prepared["real_mcp_sha256"],
        "independent_ci_success": True,
        "formal_source_adopted": False,
        "github_merge_authority": False,
        "four_family_codeai_usefulness": "NO_DATA",
        "git_mutation": False,
    }
    (OUT / "independent-receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    )
    print("KUUOS_V1103_INDEPENDENT_15_OF_15_FIXED_LEAN_AXIOMS_SUCCESS",
          json.dumps(receipt, sort_keys=True))

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"prepare", "complete"}:
        raise SystemExit("usage: ... {prepare|complete}")
    if sys.argv[1] == "prepare":
        prepare()
    else:
        complete()
