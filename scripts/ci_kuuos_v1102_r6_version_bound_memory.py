#!/usr/bin/env python3
"""v1.102: real CI evidence -> KuuOS Subtask-Level Version-Bound Memory.

This is an exact-head, READ-ONLY CodeAI memory admission check, not retraining,
a new independent proof, or a GitHub merge permit. The only output is a
version-bound, append-only CI artifact stored outside the repository.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import time

from runtime import kuuos_codeai_subtask_level_version_bound_memory_v0_1 as memory
from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean"
R6 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersCodeAICandidateR6V1_102.lean"
CANDIDATE = Path("/tmp/kuuos-v1102-r6-memory-candidate/0001-R6-original-namespace.lean")
SANDBOX = Path("/tmp/kuuos-v1102-r6-memory-sandbox")
INDEPENDENT = Path("/tmp/kuuos-v1102-r6-memory-independent")
OUTPUT = Path("/tmp/kuuos-v1102-r6-version-bound-memory")
ORIGINAL_BLOB = "7274ceba97bb4bf7b3aaffa9862952d79cf6f4c3"
R6_BLOB = "f0a5b31572c90d235f6207849f91d7f0d5ebbad4"
PREDECESSOR_BLOB = "c1eff27a2e2b1abaf869e1b2e7f59869e33c3558"
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102"
R6_NS = "KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersCodeAICandidateR6V1_102"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}
R1_RUN_HEAD = "24849d33a140c625bffb6dd6c149ad669db687d1"
ORIGINAL_RUN_HEAD = "058d14384d619289703f566be5a4d49f88dbb6c0"
R2_RUN_HEAD = "a7141b7bd06af8da8b4e8c1313ab28c1b86e5c2f"

def digest(value: object) -> str:
    return memory.canonical_digest(value)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def unique_file(folder: Path, glob: str) -> Path:
    found = list(folder.rglob(glob))
    if len(found) != 1:
        raise RuntimeError(f"NO_DATA: expected exactly one {glob} in {folder}; got {len(found)}")
    return found[0]

def entry(kind: str, entry_id: str, version: str, codeai_outcome: str,
          summary: str, binding_base: dict, input_digest: str,
          output_digest: str, evidence_digest: str, epoch: int,
          source_head: str) -> dict:
    bind = dict(binding_base)
    bind["subtask_kind"] = kind
    bind["subtask_contract_digest"] = digest({
        "scope": "v1.102-B2Nat-horn-fillers",
        "subtask_kind": kind,
        "verifier_ensemble_required": True,
        "query": "verified_useful_repair_memory_only"
    })
    bind["source_commit_sha"] = source_head
    # Do not reuse the current HEAD tree-slice digest for a different HEAD.
    bind["source_tree_digest"] = digest({
        "source_commit_sha": source_head, "source_slice": "v1.102",
        "tree_integration_status": "NOT_CERTIFIED_BY_THIS_MEMORY_STAGE"
    })
    obj = {
        "schema_version": memory.SCHEMA_VERSION,
        "profile_version": memory.PROFILE_VERSION,
        "entry_id": entry_id,
        "entry_revision": "r1",
        **bind,
        "outcome": codeai_outcome,
        "evidence_created_epoch": epoch,
        "subtask_summary": summary,
        "input_artifact_digest": input_digest,
        "output_artifact_digest": output_digest,
        "verification_evidence_digest": evidence_digest,
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
    return memory.seal(obj, memory.ENTRY_DIGEST_FIELD)

def main() -> int:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("RUNTIME_OBSTRUCTION: GitHub Actions runner required")
    head = os.environ.get("GITHUB_SHA", "")
    if len(head) != 40 or any(c not in "0123456789abcdef" for c in head):
        raise RuntimeError("NO_DATA: exact GitHub checkout SHA missing")
    if os.environ.get("GITHUB_REF_NAME") != "research/v1.102-codeai-r6-hom-instance-20261123":
        raise RuntimeError("SOURCE_OBSTRUCTION: mismatched version-bound research branch")

    original = SOURCE.read_bytes()
    r6 = R6.read_bytes()
    candidate = CANDIDATE.read_bytes()
    if cycle.git_blob(original) != ORIGINAL_BLOB or cycle.git_blob(r6) != R6_BLOB:
        raise RuntimeError("SOURCE_OBSTRUCTION: frozen original and R6 blobs differ")
    r6str = r6.decode("utf-8")
    expected = r6str.replace("namespace " + R6_NS, "namespace " + NAMESPACE).replace(
        "end " + R6_NS, "end " + NAMESPACE
    ).encode("utf-8")
    if candidate != expected:
        raise RuntimeError("SOURCE_OBSTRUCTION: independent candidate artifact differs from R6")
    pred = (ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101.lean").read_bytes()
    if cycle.git_blob(pred) != PREDECESSOR_BLOB:
        raise RuntimeError("SOURCE_OBSTRUCTION: predecessor import changed")
    if list(cycle.declarations(candidate.decode())) != list(cycle.declarations(original.decode())):
        raise RuntimeError("DECLARATION_OBSTRUCTION: public declaration names/order differ")
    if len(cycle.declarations(candidate.decode())) != 36:
        raise RuntimeError("DECLARATION_OBSTRUCTION: expected 36 public declarations")
    if (ROOT / "lean-toolchain").read_text().strip() != cycle.LEAN_PIN:
        raise RuntimeError("PIN_MISMATCH: Lean toolchain")
    manifest = json.loads((ROOT / "lake-manifest.json").read_text())
    if [m["rev"] for m in manifest["packages"] if m["name"] == "mathlib"] != [cycle.MATHLIB_PIN]:
        raise RuntimeError("PIN_MISMATCH: mathlib")

    ledger = unique_file(SANDBOX, "ledger.jsonl")
    mcpfile = unique_file(SANDBOX, "real-mcp-receipt.json")
    entries = [json.loads(s) for s in ledger.read_text().splitlines()]
    if len(entries) != 1:
        raise RuntimeError("SANDBOX_NO_DATA: multiple or no direct candidate attempts")
    local, mcp = entries[0], json.loads(mcpfile.read_text())
    if not (local["status"] == "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY"
            and local["candidate_blob"] == cycle.git_blob(candidate)
            and local["claimed_source_head"] == head
            and local["axioms"]["checked"] == 36
            and set(local["axioms"]["allowed"]) <= STANDARD
            and local["axioms"]["sorryAx"] is False
            and local["direct_lean"]["exit_code"] == 0
            and local["independent_ci_success"] is False):
        raise RuntimeError("SANDBOX_OBSTRUCTION: direct Lean and axioms local receipt not coherent")
    if not (mcp["status"] == "MCP_TYPED_LOCAL_GREEN"
            and mcp["R6_source_blob"] == R6_BLOB
            and mcp["normalized_candidate_blob"] == cycle.git_blob(candidate)
            and mcp["diagnostics_success"] is True
            and mcp["diagnostics_partial"] is False
            and mcp["error_count"] == 0
            and not mcp["failed_dependencies"]):
        raise RuntimeError("MCP_OBSTRUCTION: real MCP receipt incomplete")

    audit_log = unique_file(INDEPENDENT, "*independent-axioms.log")
    audit_bytes = audit_log.read_bytes()
    audit = cycle.audit_axioms(audit_bytes.decode("utf-8"), list(cycle.declarations(
        candidate.decode("utf-8"))), NAMESPACE)
    if audit["checked"] != 36 or audit["sorryAx"] or set(audit["allowed"]) - STANDARD:
        raise RuntimeError("INDEPENDENT_LEAN_OBSTRUCTION: 36 public axioms not fully audited")

    # The actual four-family Verifier Ensemble v0.2 has not independently
    # established cross-domain usefulness. Even a real 36/36 Lean certificate
    # cannot, by itself, promote a CodeAI memory hint to VERIFIED_USEFUL.
    now = int(time.time())
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if not run_id.isdigit():
        raise RuntimeError("NO_DATA: GitHub Actions run identifier missing")
    formal_digest = digest({
        "run_id": run_id, "source_blob": R6_BLOB, "actual_candidate_blob": cycle.git_blob(candidate),
        "independent_Lean_axioms_sha256": sha256_bytes(audit_bytes), "checked": 36
    })
    current = {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": head,
        "source_tree_digest": digest({
            "source_commit_sha": head, "source_slice": "v1.102",
            "tree_integration_status": "NOT_CERTIFIED_BY_THIS_MEMORY_STAGE"
        }),
        "temporal_corpus_digest": digest({"project": "KuuOS", "run_id": run_id,
                                         "candidate_blob": R6_BLOB, "memory_epoch": now}),
        "context_pack_digest": digest({"original_blob": ORIGINAL_BLOB,
                                       "candidate_blob": R6_BLOB,
                                       "predecessor_blob": PREDECESSOR_BLOB}),
        "verifier_ensemble_digest": digest({
            "actual_formal_evidence": formal_digest,
            "sandbox_mcp_receipt_sha256": sha256_bytes(mcpfile.read_bytes()),
            "behavioral_regression": "NO_DATA",
            "adversarial_falsification": "NO_DATA",
            "maintainability_static": "NO_DATA",
            "verifier_organization_independence": "NO_DATA",
        }),
        "subtask_kind": "verify",
        "subtask_contract_digest": digest({
            "scope": "v1.102-B2Nat-horn-fillers",
            "subtask_kind": "verify",
            "verifier_ensemble_required": True,
            "query": "verified_useful_repair_memory_only"
        }),
        "predecessor_output_digest": digest({"sandbox_candidate_blob": cycle.git_blob(candidate),
                                             "sandbox_log_sha256": local["direct_lean"]["log_sha256"]}),
        "dependency_slice_digest": digest({"v1101_blob": PREDECESSOR_BLOB,
                                            "R6_blob": R6_BLOB, "source_namespace": NAMESPACE}),
        "toolchain_digest": digest({"lean": cycle.LEAN_PIN, "mathlib": cycle.MATHLIB_PIN}),
        "environment_digest": digest({"kind": "independent-github-actions-memory-runner",
                                       "run_id": run_id, "source_commit": head}),
        "memory_policy_digest": digest({"profile": memory.PROFILE_VERSION,
                                        "allowed_outcomes": ["verified_useful"],
                                        "source_version_exact": True,
                                        "no_execution_or_git_authority": True}),
    }

    # Source-bound observations, not fabricated successes. Earlier observations
    # are correctly marked INCONCLUSIVE and intentionally stale.
    observed = [
        entry("localize", "v1102-original-localize", "original",
              memory.OUTCOME_INCONCLUSIVE, "Original exact Lean source failed with 25 diagnostics in run 45075201711",
              current, digest({"original_git_blob": ORIGINAL_BLOB}),
              digest({"diagnostics": 25, "run_id": 45075201711}),
              digest({"run": 45075201711, "conclusion": "failure"}),
              now, ORIGINAL_RUN_HEAD),
        entry("diagnose", "v1102-r1-diagnose", "r1",
              memory.OUTCOME_INCONCLUSIVE, "R1 run 45079187212 failed 15 exact-source Lean diagnostics",
              current, digest({"R1": "f66e7fb9c00de6c29072e9ce53894b6d6da32c2f"}),
              digest({"diagnostics": 15}), digest({"run": 45079187212, "conclusion": "failure"}),
              now, R1_RUN_HEAD),
        entry("edit", "v1102-r2-pending", "r2",
              memory.OUTCOME_INCONCLUSIVE, "R2 candidate had no complete independent Lean verification at candidate selection",
              current, digest({"R2": "641800b1d4f2c1763a0bcb3cccc23b80d666a245"}),
              digest({"R2": "candidate_only"}), digest({"run": 45080145560, "observed": "queued"}),
              now, R2_RUN_HEAD),
        entry("edit", "v1102-r6-current-edit", "r6",
              memory.OUTCOME_INCONCLUSIVE, "R6 syntax and proof candidate observed; verified usefulness NOT certified by four-family ensemble",
              current, digest({"R6": R6_BLOB}), digest({"candidate": sha256_bytes(candidate)}),
              digest({"local_direct_Lean": local["direct_lean"]["log_sha256"]}),
              now, head),
        entry("verify", "v1102-r6-current-verification", "r6",
              memory.OUTCOME_INCONCLUSIVE, "R6 independently compiled with 36/36 standard axiom audit; four-family CodeAI usefulness NO_DATA",
              current, digest({"candidate": sha256_bytes(candidate)}),
              formal_digest, digest({"independent_formal": formal_digest, "mcp": sha256_bytes(mcpfile.read_bytes())}),
              now, head),
    ]
    req = memory.seal({
        "schema_version": memory.SCHEMA_VERSION,
        "profile_version": memory.PROFILE_VERSION,
        "request_id": "v1102-r6-exact-verify-recall",
        "request_revision": "r1",
        **current,
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
        **{"expected_" + k: req[k] for k in memory.VERSION_BINDING_FIELDS},
        "evaluation_epoch": now, "maximum_request_age": 3600,
        "maximum_entry_age": 7200, "maximum_corpus_entries": 16,
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
        "corpus_id": "v1102-r6-real-github-ci-evidence-corpus",
        "corpus_revision": "r1",
        "repository_full_name": req["repository_full_name"],
        "temporal_corpus_digest": req["temporal_corpus_digest"],
        "context_pack_digest": req["context_pack_digest"],
        "verifier_ensemble_digest": req["verifier_ensemble_digest"],
        "entries": observed,
    }, memory.CORPUS_DIGEST_FIELD)
    result = memory.build_codeai_subtask_level_version_bound_memory(
        request=req, policy=policy, corpus=corpus
    )
    if result.status != memory.STATUS_READY or result.memory_pack is None or result.receipt is None:
        raise RuntimeError("MEMORY_OBSTRUCTION: " + str(result.issues))
    pack = result.memory_pack
    if pack["matched_entry_count"] != 0 or pack["excluded_entry_count"] != len(observed):
        raise RuntimeError("MEMORY_OBSTRUCTION: unverified candidate incorrectly promoted")
    if pack["recommendation"] != memory.RECOMMENDATION_NONE:
        raise RuntimeError("MEMORY_OBSTRUCTION: output granted reuse without ensemble")
    if not any("binding_mismatch:source_commit_sha" in x["reasons"]
               for x in pack["excluded_entries"]):
        raise RuntimeError("MEMORY_OBSTRUCTION: version mismatch not excluded")
    if not all(not x["derived_from_holdout"] for x in observed):
        raise RuntimeError("MEMORY_OBSTRUCTION: holdout source cannot enter memory")

    receipt = {
        "schema": "kuuos-codeai-v1102-r6-real-version-bound-recall-v1",
        "source_commit_sha": head,
        "source_candidate_blob": R6_BLOB,
        "independent_formal_36_axiom_audit": "SUCCESS_BOUND_TO_THIS_JOB_ONLY",
        "formal_evidence_digest": formal_digest,
        "memory_evaluator": memory.VERSION,
        "memory_status": result.status,
        "matched_verified_useful": pack["matched_entry_count"],
        "excluded_records": pack["excluded_entry_count"],
        "exclusion_counts": pack["exclusion_counts"],
        "four_family_verifier_ensemble": "NO_DATA",
        "formal_certification_does_not_imply_codeai_usefulness": True,
        "reusable_memory_hint": False,
        "memory_weights_updated": False,
        "execution_or_merge_authority": False,
        "git_write_performed": False,
        "memory_pack_digest": pack[memory.PACK_DIGEST_FIELD],
        "memory_receipt_digest": result.receipt[memory.RECEIPT_DIGEST_FIELD],
    }
    OUTPUT.mkdir(parents=True, exist_ok=False)
    for name, value in (("request", req), ("policy", policy), ("corpus", corpus),
                        ("memory_pack", pack), ("receipt", receipt)):
        (OUTPUT / (name + ".json")).write_text(
            json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        )
    print("KUUOS_V1102_R6_CODEAI_VERSION_BOUND_MEMORY_EXCLUDED_UNCERTIFIED",
          json.dumps(receipt, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
