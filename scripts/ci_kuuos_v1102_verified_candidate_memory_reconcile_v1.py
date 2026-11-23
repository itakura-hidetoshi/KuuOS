#!/usr/bin/env python3
"""Read-only real-evidence CodeAI v1.102 version-bound memory reconciliation.

Only after the two independently successful GitHub Actions jobs on an immutable
SHA. This does not infer four-family CodeAI usefulness, mutate model weights,
adopt a Lean source, grant GitHub authority, or trigger fresh Lean CI.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import os
import time
from urllib.request import Request, urlopen

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle
from scripts import ci_kuuos_v1102_multi_candidate_sandbox_v1 as sandbox
from runtime import kuuos_codeai_subtask_level_version_bound_memory_v0_1 as memory

REPO = "itakura-hidetoshi/KuuOS"
SOURCE_HEAD = "1a7f98191c72b513d680a7788ca3410129dc70b9"
UPSTREAM_RUN = 45128298012
SELECTED_GIT_BLOB = "f8b492b210e5525990aa587fa2eb5c8648a5ff19"
SELECTED_SHA256 = "81a2245cd3e659d10e33ef6ce6d5ebd3b1778f9f5b6ca928ef025024a8e70a02"
SELECTED_PATH = Path("/tmp/kuuos-v1102-memory-selected")
SANDBOX_RECEIPTS = Path("/tmp/kuuos-v1102-memory-sandbox")
INDEPENDENT_RECEIPTS = Path("/tmp/kuuos-v1102-memory-independent")
OUTPUT = Path("/tmp/kuuos-v1102-codeai-verified-memory")
STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

def check(value: bool, message: str):
    if not value:
        raise RuntimeError("MEMORY_NO_DATA_OR_OBSTRUCTION: " + message)

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def onefile(where: Path, pat: str) -> Path:
    matches = list(where.rglob(pat))
    check(len(matches) == 1, f"{pat} must have exactly one match: {len(matches)}")
    return matches[0]

def github_api(path: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN", "")
    check(bool(token), "GitHub Actions read token absent")
    req = Request(
        "https://api.github.com/repos/" + REPO + path,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KuuOS-CodeAI-SourceBound-Memory",
        },
    )
    with urlopen(req, timeout=30) as result:
        return json.load(result)

def confirmed_independent_ci() -> dict:
    r = github_api("/actions/runs/" + str(UPSTREAM_RUN))
    check(r["head_sha"] == SOURCE_HEAD and r["status"] == "completed"
          and r["conclusion"] == "success" and r["run_attempt"] == 1,
          "upstream workflow not exact-head completed/SUCCESS")
    jobs = github_api("/actions/runs/" + str(UPSTREAM_RUN) + "/jobs?per_page=100")
    required = {
        "isolated-sandbox-direct-lean-real-mcp",
        "independent-candidate-strict-lean-36-axiom",
    }
    joblist = jobs.get("jobs", [])
    actual = {
        j.get("name") for j in joblist
        if j.get("status") == "completed" and j.get("conclusion") == "success"
    }
    check(required <= actual and len(joblist) == 2, "both exact independent CI jobs not green")
    return {
        "run": UPSTREAM_RUN, "run_sha": SOURCE_HEAD,
        "jobs": {j["name"]: {"id": j["id"], "conclusion": j["conclusion"]}
                 for j in joblist},
    }

def verified_sources() -> dict:
    root = sandbox.ROOT
    candidate = (SELECTED_PATH / "selected.lean").read_bytes()
    selected = json.loads((SELECTED_PATH / "selected-source.json").read_text())
    original = (root / sandbox.SOURCE).read_bytes()
    r6 = (root / sandbox.R6).read_bytes()
    check(cycle.git_blob(original) == sandbox.ORIGINAL_BLOB, "original Lean blob")
    check(cycle.git_blob(r6) == sandbox.R6_BLOB, "R6 seed Lean blob")
    check(cycle.git_blob(candidate) == SELECTED_GIT_BLOB, "selected candidate git blob")
    check(sha256(candidate) == SELECTED_SHA256, "selected candidate sha256")
    check(selected["candidate_blob"] == SELECTED_GIT_BLOB
          and selected["candidate_sha256"] == SELECTED_SHA256
          and selected["source_commit_sha"] == SOURCE_HEAD
          and selected["candidate_file"] == "0001-explicit-inductive-unique.lean"
          and selected["attempts_executed"] == 1
          and selected["direct_lean_success"] is True
          and selected["real_mcp_local_green"] is True
          and selected["independent_ci_success"] is False,
          "sandbox local selected-source receipt inconsistent")
    seed = r6.decode("utf-8")
    for left, right in (
        ("namespace " + sandbox.R6_NS, "namespace " + sandbox.ORIGINAL_NS),
        ("end " + sandbox.R6_NS, "end " + sandbox.ORIGINAL_NS)
    ):
        check(seed.count(left) == 1, "R6 namespace ambiguity")
        seed = seed.replace(left, right, 1)
    check(seed.count(sandbox.R6_PROOF) == 1, "R6 seed proof ambiguity")
    name, tactic = sandbox.REPAIRS[0]
    check(name == "explicit-inductive-unique", "first proof must be pinned")
    reconstructed = seed.replace(sandbox.R6_PROOF, tactic, 1).encode("utf-8")
    check(candidate == reconstructed, "exact selected proof not matching CodeAI generator")
    source_contract = cycle.source_contract(
        original.decode("utf-8"), candidate.decode("utf-8"),
        sandbox.REASONS, {},
    )
    check(len(source_contract["public_declarations"]) == 36
          and source_contract["import_additions"] == {}
          and set(source_contract["signature_changes"]) == set(sandbox.REASONS),
          "36 declaration statements, order, or import contract invalid")
    if (root / "lean-toolchain").read_text().strip() != cycle.LEAN_PIN:
        raise RuntimeError("PIN_MISMATCH: Lean toolchain")
    manifest = json.loads((root / "lake-manifest.json").read_text())
    check([p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"]
          == [cycle.MATHLIB_PIN], "pinned mathlib changed")
    return {
        "candidate": candidate, "original": original,
        "public_declarations": source_contract["public_declarations"],
    }

def evidence(candidate: bytes, names: list[str]) -> dict:
    ledger = onefile(SANDBOX_RECEIPTS, "ledger.jsonl")
    mcp_file = onefile(SANDBOX_RECEIPTS, "real-mcp-receipt.json")
    records = [json.loads(s) for s in ledger.read_text().splitlines()]
    check(len(records) == 1, "one successful sandbox trial expected")
    local = records[0]
    mcp = json.loads(mcp_file.read_text())
    check(local["status"] == "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY"
          and local["claimed_source_head"] == SOURCE_HEAD
          and local["candidate_blob"] == SELECTED_GIT_BLOB
          and local["candidate_sha256"] == SELECTED_SHA256
          and local["direct_lean"]["exit_code"] == 0
          and local["direct_lean"]["error_count"] == 0
          and local["axioms"]["checked"] == 36
          and local["axioms"]["sorryAx"] is False
          and set(local["axioms"]["allowed"]) <= STD_AXIOMS,
          "local direct Lean or local 36 axioms not certified")
    check(mcp["status"] == "MCP_TYPED_LOCAL_GREEN"
          and mcp["candidate_blob"] == SELECTED_GIT_BLOB
          and mcp["diagnostics_success"] is True
          and mcp["diagnostics_partial"] is False
          and mcp["error_count"] == 0 and not mcp["failed_dependencies"],
          "real lean-lsp-mcp typed diagnostics not green")
    audit_file = onefile(INDEPENDENT_RECEIPTS, "*independent-axioms.log")
    audit_bytes = audit_file.read_bytes()
    audit = cycle.audit_axioms(
        audit_bytes.decode("utf-8"), names, sandbox.ORIGINAL_NS)
    check(audit["checked"] == 36 and audit["sorryAx"] is False
          and set(audit["allowed"]) <= STD_AXIOMS,
          "independent 36-declaration Lean axiom log not valid")
    return {
        "sandbox": local, "mcp": mcp, "independent_axioms": audit,
        "independent_axioms_sha256": sha256(audit_bytes),
        "sandbox_mcp_receipt_sha256": sha256(mcp_file.read_bytes()),
    }

def memory_audit(ci: dict, source: dict, evidence: dict) -> dict:
    def digest(v: object) -> str:
        return memory.canonical_digest(v)
    now = int(time.time())
    # This is a binding, not a claim that four external verifier families passed.
    binding = {
        "repository_full_name": REPO,
        "source_commit_sha": SOURCE_HEAD,
        "source_tree_digest": digest({
            "source_commit": SOURCE_HEAD,
            "tree_status": "not-certified-by-memory-stage"
        }),
        "temporal_corpus_digest": digest({
            "session": UPSTREAM_RUN, "schema": memory.SCHEMA_VERSION
        }),
        "context_pack_digest": digest({
            "original_git_blob": sandbox.ORIGINAL_BLOB,
            "source_git_blob": SELECTED_GIT_BLOB,
            "selected_sha256": SELECTED_SHA256,
            "names": source["public_declarations"],
        }),
        "verifier_ensemble_digest": digest({
            "type_formal_proof": evidence["independent_axioms_sha256"],
            "real_mcp": evidence["sandbox_mcp_receipt_sha256"],
            "behavioral_regression": "NO_DATA",
            "adversarial_falsification": "NO_DATA",
            "maintainability_static": "NO_DATA",
            "organizational_independence": "NO_DATA"
        }),
        "subtask_kind": "verify",
        "subtask_contract_digest": digest({
            "subtask": "verify", "project": "KuuOS", "v": "v1.102",
            "only_verified_usefulness_reusable": True
        }),
        "predecessor_output_digest": digest({
            "selected_git_blob": SELECTED_GIT_BLOB,
            "independent_36_axiom_sha256": evidence["independent_axioms_sha256"]
        }),
        "dependency_slice_digest": digest({
            "import_git_blob": "c1eff27a2e2b1abaf869e1b2e7f59869e33c3558",
            "original_git_blob": sandbox.ORIGINAL_BLOB,
            "candidate_git_blob": SELECTED_GIT_BLOB
        }),
        "toolchain_digest": digest({"lean": cycle.LEAN_PIN, "mathlib": cycle.MATHLIB_PIN}),
        "environment_digest": digest({
            "runner": "ubuntu-22.04", "source_run": UPSTREAM_RUN,
            "jobs": ci["jobs"]
        }),
        "memory_policy_digest": digest({
            "policy": "CodeAI Subtask-Level Version-Bound Memory v0.1",
            "requires_four_family_independence": True,
            "no_git_authority": True
        }),
    }
    def mk_entry(kind: str, ident: str, rev_sha: str, message: str) -> dict:
        x = dict(binding)
        x["subtask_kind"] = kind
        x["source_commit_sha"] = rev_sha
        x["source_tree_digest"] = digest({
            "source_commit": rev_sha, "tree_status": "not-certified-by-memory-stage"
        })
        x["subtask_contract_digest"] = digest({
            "subtask": kind, "project": "KuuOS", "v": "v1.102",
            "only_verified_usefulness_reusable": True
        })
        item = {
            "schema_version": memory.SCHEMA_VERSION,
            "profile_version": memory.PROFILE_VERSION,
            "entry_id": ident,
            "entry_revision": "r1",
            **x,
            "outcome": memory.OUTCOME_INCONCLUSIVE,
            "evidence_created_epoch": now,
            "subtask_summary": message,
            "input_artifact_digest": digest({"entry": ident, "input": rev_sha}),
            "output_artifact_digest": digest({"entry": ident, "output": message}),
            "verification_evidence_digest": digest({"entry": ident, "evidence": ci}),
            "derived_from_holdout": False,
            "superseded": False,
            "repository_mutation_performed": False,
            "candidate_selected": False,
            "repair_executed": False,
            "execution_authority_granted": False,
            "git_authority_granted": False,
            "correctness_claimed": False,
            "future_success_claimed": False,
        }
        return memory.seal(item, memory.ENTRY_DIGEST_FIELD)
    entries = [
        mk_entry("localize", "v1102-original-25-errors",
                 "058d14384d619289703f566be5a4d49f88dbb6c0",
                 "Original v1.102 direct Lean failed 25 errors; source-bound failure only"),
        mk_entry("diagnose", "v1102-R1-15-errors",
                 "24849d33a140c625bffb6dd6c149ad669db687d1",
                 "R1 direct Lean failed 15 errors; no verified reuse"),
        mk_entry("edit", "v1102-R6-one-error",
                 "3db8d16d4fb01b89f4c25360bbc3e9d453392d21",
                 "R6 direct Lean failed one Hom Subsingleton goal"),
        mk_entry("verify", "v1102-selected-formal-certified",
                 SOURCE_HEAD,
                 "First CodeAI trial independently verified 36 Lean declarations; CodeAI four-family usefulness not certified"),
    ]
    request = memory.seal({
        "schema_version": memory.SCHEMA_VERSION,
        "profile_version": memory.PROFILE_VERSION,
        "request_id": "v1102-exact-formal-memory-recall",
        "request_revision": "r1",
        **binding,
        "request_created_epoch": now,
        "unresolved_questions": [],
        "claims_selection_authority": False,
        "claims_repair_authority": False,
        "claims_execution_authority": False,
        "claims_git_authority": False,
    }, memory.REQUEST_DIGEST_FIELD)
    policy = memory.seal({
        "schema_version": memory.SCHEMA_VERSION,
        "profile_version": memory.PROFILE_VERSION,
        **{"expected_" + x: request[x] for x in memory.VERSION_BINDING_FIELDS},
        "evaluation_epoch": now,
        "maximum_request_age": 3600,
        "maximum_entry_age": 3600,
        "maximum_corpus_entries": 16,
        "maximum_matched_entries": 4,
        "allowed_outcomes": [memory.OUTCOME_VERIFIED_USEFUL],
        "required_subtask_kinds": list(memory.SUBTASK_KINDS),
        "require_exact_version_binding": True,
        "require_subtask_alignment": True,
        "require_dependency_alignment": True,
        "require_verifier_grounding": True,
        "require_holdout_protection": True,
        "require_not_superseded": True,
        "allow_memory_hint": True,
        "allow_repository_mutation": False,
        "allow_candidate_selection": False,
        "allow_repair_execution": False,
        "allow_execution_authority": False,
        "allow_git_authority": False,
    }, memory.POLICY_DIGEST_FIELD)
    corpus = memory.seal({
        "schema_version": memory.SCHEMA_VERSION,
        "profile_version": memory.PROFILE_VERSION,
        "corpus_id": "v1102-formal-36-run-45128298012",
        "corpus_revision": "r1",
        "repository_full_name": REPO,
        "temporal_corpus_digest": request["temporal_corpus_digest"],
        "context_pack_digest": request["context_pack_digest"],
        "verifier_ensemble_digest": request["verifier_ensemble_digest"],
        "entries": entries,
    }, memory.CORPUS_DIGEST_FIELD)
    result = memory.build_codeai_subtask_level_version_bound_memory(
        request=request, policy=policy, corpus=corpus
    )
    check(result.status == memory.STATUS_READY and result.memory_pack is not None,
          "real version-bound MemoryOS kernel did not return ready")
    pack = result.memory_pack
    check(pack["matched_entry_count"] == 0
          and pack["excluded_entry_count"] == len(entries)
          and pack["recommendation"] == memory.RECOMMENDATION_NONE,
          "unverified evidence incorrectly admitted to reusable CodeAI memory")
    check(any("binding_mismatch:source_commit_sha" in e["reasons"]
              for e in pack["excluded_entries"]),
          "wrong-version entries were not excluded")
    check(any("outcome_not_allowed" in e["reasons"]
              for e in pack["excluded_entries"]),
          "inconclusive candidate incorrectly accepted")
    receipt = {
        "schema": "kuuos-v1102-exact-ci-codeai-memory-v1",
        "source_run": UPSTREAM_RUN,
        "source_commit_sha": SOURCE_HEAD,
        "source_candidate_git_blob": SELECTED_GIT_BLOB,
        "source_candidate_sha256": SELECTED_SHA256,
        "independent_Lean_axiom_audit": "36_of_36_standard_only_SUCCESS",
        "actual_CodeAI_MemoryOS": memory.VERSION,
        "memory_status": result.status,
        "matched_verified_useful": 0,
        "excluded_records": pack["excluded_entry_count"],
        "exclusion_counts": pack["exclusion_counts"],
        "four_family_verifier_ensemble": "NO_DATA",
        "source_candidate_formal_certified": True,
        "CodeAI_future_usefulness_certified": False,
        "model_weights_updated": False,
        "git_write_performed": False,
        "source_adopted": False,
        "merge_authorized": False,
        "memory_pack_digest": pack[memory.PACK_DIGEST_FIELD],
        "memory_receipt_digest": result.receipt[memory.RECEIPT_DIGEST_FIELD],
    }
    return {"receipt": receipt, "pack": pack}

def main():
    check(os.environ.get("GITHUB_ACTIONS") == "true",
          "GitHub Actions read-only runtime required")
    check(os.environ.get("GITHUB_REF_NAME") ==
          "validation/v1102-codeai-version-bound-after-independent-20261123",
          "unexpected memory research branch")
    ci = confirmed_independent_ci()
    src = verified_sources()
    ev = evidence(src["candidate"], src["public_declarations"])
    reconciliation = memory_audit(ci, src, ev)
    OUTPUT.mkdir(parents=True, exist_ok=False)
    for label, value in reconciliation.items():
        (OUTPUT / (label + ".json")).write_text(
            json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        )
    print("KUUOS_V1102_REAL_VERSION_BOUND_MEMORY_EXCLUDES_UNCERTIFIED",
          json.dumps(reconciliation["receipt"], sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
