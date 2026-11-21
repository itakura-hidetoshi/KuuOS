#!/usr/bin/env python3
"""Read-only KuuOS CodeAI v0.61 subtask-memory replay from independent Lean evidence.

A SEPARATE GitHub CI job must have completed its candidate verification job
successfully and transferred the immutable evidence artifact. This step
constructs a source-bound, append-only learning/recall receipt, NOT a model
weight update or an independent externally curated memory database.

Only the source-bound VERIFY procedure with real Lean/axiom evidence is marked
verified_useful. The localize/diagnose/edit traces remain inconclusive pending
separate independent usefulness adjudication. Failed candidate C is NOT given
a repair-memory success hint or silently translated into static errors.

Actual KuuOS SubtaskLevelVersionBoundMemory runtime is invoked. Exact source
mismatch, different subtask or holdout-derived data cannot transfer hints.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import os
import time

from runtime import kuuos_codeai_subtask_level_version_bound_memory_v0_1 as memory
from scripts import codeai_v061_two_stage_proof_proposal as source

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE=ROOT/"artifacts/codeai-v061-independent-verification/verified-candidates.json"
OUTPUT=ROOT/"artifacts/codeai-v061-learning-replay"

def stable(data) -> str:
    return memory.canonical_digest(data)

def load_exact_evidence(file: Path) -> dict:
    data=json.loads(file.read_text(encoding="utf-8"))
    digest=data.pop("evidence_digest")
    assert digest==stable(data), "independent_evidence_digest_mismatch"
    data["evidence_digest"]=digest
    assert data["schema"]=="kuuos.codeai.v061.independent-fixed-lean-evidence.v1"
    assert data["canonical_parent_main"]==source.MAIN_HEAD
    assert data["canonical_parent_tree_sha1"]==source.MAIN_TREE
    assert data["toolchain"]==source.TOOLCHAIN
    assert data["mathlib_commit"]==source.MATHLIB
    assert data["attempts"]==["CANDIDATE"]*3+["REJECT"]
    assert len(data["results"])==3
    a,b,c=data["results"]
    for record in (a,b):
        assert record["status"]=="INDEPENDENT_FIXED_LEAN_AND_AXIOM_PASSED"
        assert record["axiom_declarations_checked"]==8
        assert record["strict_lean_exit_code"]==0
        assert not record["sorryAx"]
        assert set(record["axioms_used"]) <= {"propext","Classical.choice","Quot.sound"}
    assert c["status"]=="DIRECT_LEAN_REJECTED_TYPED_LINT_PENDING"
    assert c["error_count"]==2
    assert not c["reusable_repair_memory_admitted"]
    assert not data["typed_error_classification_c_admitted"]
    assert not data["subtask_memory_update_performed"]
    assert not data["all_proposals_adopted"]
    return data

def bindings(kind: str, evidence: dict) -> dict:
    # All predicates are version-scoped to the original EXACT pinned main.
    # Here the tree SHA-1 remains separately recorded in the receipt; the
    # schema's 64-character digest is a SHA-256 content-addressed binding.
    return {
        "repository_full_name":"itakura-hidetoshi/KuuOS",
        "source_commit_sha":source.MAIN_HEAD,
        "source_tree_digest":stable({"git_tree_sha1":source.MAIN_TREE}),
        "temporal_corpus_digest":stable({
            "replay_scope":"v061-development-only",
            "holdout_label_exposure":False,
            "gold_patch_exposure":False,
            "source_main":source.MAIN_HEAD,
        }),
        "context_pack_digest":stable({
            "exact_imported_source_git_blobs":source.SOURCE_BLOBS,
            "candidate_source_sha256":evidence["results"][0]["source_sha256"],
        }),
        "verifier_ensemble_digest":stable({
            "independent_fixed_lean_log":evidence["results"][0]["log_sha256"],
            "second_passing_candidate_log":evidence["results"][1]["log_sha256"],
            "failed_candidate_diagnostic_digest":
                evidence["results"][2]["diagnostic_digest"],
            "actual_real_lean_mcp_local_separately_observed":True,
            "full_GitHub_CI_run_not_part_of_the_memory_claim":True,
        }),
        "subtask_kind":kind,
        "subtask_contract_digest":stable({
            "contract_kind":kind,"scope":"v061-two-stage-append",
            "no_host_authority":True,
        }),
        "predecessor_output_digest":stable({
            "kind":kind,"source_portfolio_digest":evidence["portfolio_digest"],
            "actual_previous_step_evidence":evidence["evidence_digest"],
        }),
        "dependency_slice_digest":stable({
            "kind":kind,"pinned_imported_git_blobs":source.SOURCE_BLOBS,
        }),
        "toolchain_digest":stable({
            "lean_toolchain":source.TOOLCHAIN,"mathlib_sha":source.MATHLIB,
        }),
        "environment_digest":stable({
            "execution_context":"separate-GitHub-Actions-candidate-verifier",
            "source_sha":source.MAIN_HEAD,
            "no_network_or_original_host_action_in_memory_kernel":True,
        }),
        "memory_policy_digest":stable({
            "policy":"exact-development-only-verified-utility-v061",
            "holdout_excluded":True,"no_git_or_execution_authority":True,
        }),
    }

def build_entry(kind: str, result: dict, now: int) -> dict:
    a,b,c=result["results"]
    evidence_by_kind={
        "localize":(result["evidence_digest"],result["portfolio_digest"],
                    result["results"][0]["source_sha256"]),
        "diagnose":(c["source_sha256"],c["diagnostic_digest"],
                    c["diagnostic_digest"]),
        "edit":(result["portfolio_digest"],a["source_sha256"],
                b["log_sha256"]),
        "verify":(a["source_sha256"],a["log_sha256"],
                  a["log_sha256"]),
    }
    inp,out,check=evidence_by_kind[kind]
    entry={
        "schema_version":memory.SCHEMA_VERSION,
        "profile_version":memory.PROFILE_VERSION,
        "entry_id":"v061-"+kind+"-observed",
        "entry_revision":"r1",
        **bindings(kind,result),
        "outcome":(
            memory.OUTCOME_VERIFIED_USEFUL if kind=="verify"
            else memory.OUTCOME_INCONCLUSIVE
        ),
        "evidence_created_epoch":now,
        "subtask_summary":(
            "v0.61 verified exact fixed-Lean direct 8/8 axiom-check "
            "procedure on model A; no main adoption or external proof authority"
            if kind=="verify" else
            "v0.61 evidence-bound observed "+kind+
            " stage; usefulness still inconclusive, no transferable hint"
        ),
        "input_artifact_digest":inp,
        "output_artifact_digest":out,
        "verification_evidence_digest":check,
        "derived_from_holdout":False,
        "superseded":False,
        "repository_mutation_performed":False,
        "candidate_selected":False,
        "repair_executed":False,
        "execution_authority_granted":False,
        "git_authority_granted":False,
        "correctness_claimed":False,
        "future_success_claimed":False,
    }
    return memory.seal(entry,memory.ENTRY_DIGEST_FIELD)

def build_request_policy(evidence: dict, entries: list[dict], now: int):
    binding=bindings("verify",evidence)
    req=memory.seal({
        "schema_version":memory.SCHEMA_VERSION,
        "profile_version":memory.PROFILE_VERSION,
        "request_id":"v061-exact-verify-recall",
        "request_revision":"r1",
        **binding,
        "request_created_epoch":now,
        "unresolved_questions":[],
        "claims_selection_authority":False,
        "claims_repair_authority":False,
        "claims_execution_authority":False,
        "claims_git_authority":False,
    },memory.REQUEST_DIGEST_FIELD)
    policy=memory.seal({
        "schema_version":memory.SCHEMA_VERSION,
        "profile_version":memory.PROFILE_VERSION,
        **{"expected_"+key:req[key] for key in memory.VERSION_BINDING_FIELDS},
        "evaluation_epoch":now,
        "maximum_request_age":3600,
        "maximum_entry_age":7200,
        "maximum_corpus_entries":16,
        "maximum_matched_entries":4,
        "allowed_outcomes":[memory.OUTCOME_VERIFIED_USEFUL],
        "required_subtask_kinds":list(memory.SUBTASK_KINDS),
        "require_exact_version_binding":True,
        "require_subtask_alignment":True,
        "require_dependency_alignment":True,
        "require_verifier_grounding":True,
        "require_holdout_protection":True,
        "require_not_superseded":True,
        "allow_memory_hint":True,
        "allow_repository_mutation":False,
        "allow_candidate_selection":False,
        "allow_repair_execution":False,
        "allow_execution_authority":False,
        "allow_git_authority":False,
    },memory.POLICY_DIGEST_FIELD)
    corpus=memory.seal({
        "schema_version":memory.SCHEMA_VERSION,
        "profile_version":memory.PROFILE_VERSION,
        "corpus_id":"v061-CI-run-development-only",
        "corpus_revision":"r1",
        "repository_full_name":"itakura-hidetoshi/KuuOS",
        "temporal_corpus_digest":req["temporal_corpus_digest"],
        "context_pack_digest":req["context_pack_digest"],
        "verifier_ensemble_digest":req["verifier_ensemble_digest"],
        "entries":entries,
    },memory.CORPUS_DIGEST_FIELD)
    return req,policy,corpus

def main(path: Path) -> int:
    evidence=load_exact_evidence(path)
    now=int(time.time())
    entries=[build_entry(kind,evidence,now)
             for kind in memory.SUBTASK_KINDS]
    req,pol,corp=build_request_policy(evidence,entries,now)
    output=memory.build_codeai_subtask_level_version_bound_memory(
        request=req,policy=pol,corpus=corp,
    )
    assert output.status==memory.STATUS_READY,(output.status,output.issues)
    pack=output.memory_pack
    assert pack is not None and output.receipt is not None
    assert pack["matched_entry_count"]==1,pack
    assert pack["excluded_entry_count"]==3,pack
    assert pack["matched_entries"][0]["entry_id"]=="v061-verify-observed"
    assert pack["recommendation"]==memory.RECOMMENDATION_AVAILABLE
    assert not pack["repair_executed"]
    assert not pack["git_authority_granted"]
    assert not pack["future_success_claimed"]
    # A different real Git source cannot inherit the hint by similarity.
    stale_req=dict(req,source_commit_sha="0"*40)
    stale_req=memory.seal(stale_req,memory.REQUEST_DIGEST_FIELD)
    stale_pol=dict(pol,expected_source_commit_sha="0"*40)
    stale_pol=memory.seal(stale_pol,memory.POLICY_DIGEST_FIELD)
    stale=memory.build_codeai_subtask_level_version_bound_memory(
        request=stale_req,policy=stale_pol,corpus=corp)
    assert stale.status==memory.STATUS_READY
    assert stale.memory_pack["matched_entry_count"]==0
    # C's actual failed Lean lint cannot become a reusable repair hint.
    diagnose_req=memory.seal(dict(req,**bindings("diagnose",evidence),
                                  request_id="v061-diagnose-negative-lookup"),
                             memory.REQUEST_DIGEST_FIELD)
    diagnose_pol=memory.seal(dict(pol,**{
        "expected_"+key:diagnose_req[key]
        for key in memory.VERSION_BINDING_FIELDS}),
                             memory.POLICY_DIGEST_FIELD)
    diagnose=memory.build_codeai_subtask_level_version_bound_memory(
        request=diagnose_req,policy=diagnose_pol,corpus=corp)
    assert diagnose.status==memory.STATUS_READY
    assert diagnose.memory_pack["matched_entry_count"]==0
    # A test-only holdout-derived copy must be excluded and must never be
    # emitted into the actual learning corpus below.
    tampered=deepcopy(corp)
    tampered["entries"][-1]["derived_from_holdout"]=True
    tampered["entries"][-1]=memory.seal(
        tampered["entries"][-1],memory.ENTRY_DIGEST_FIELD)
    tampered=memory.seal(tampered,memory.CORPUS_DIGEST_FIELD)
    check=memory.build_codeai_subtask_level_version_bound_memory(
        request=req,policy=pol,corpus=tampered)
    assert check.status==memory.STATUS_READY
    assert check.memory_pack["matched_entry_count"]==0

    OUTPUT.mkdir(parents=True,exist_ok=True)
    values={
        "schema":"kuuos.codeai.v061.source-bound-read-only-learning-replay.v1",
        "exact_main_source_commit":source.MAIN_HEAD,
        "exact_main_source_tree_git_sha1":source.MAIN_TREE,
        "separate_verifier_output_sha256":evidence["evidence_digest"],
        "subtask_memory_pack_digest":pack[memory.PACK_DIGEST_FIELD],
        "subtask_memory_receipt_digest":
            output.receipt[memory.RECEIPT_DIGEST_FIELD],
        "subtask_corpus_digest":corp[memory.CORPUS_DIGEST_FIELD],
        "observed_subtasks":list(memory.SUBTASK_KINDS),
        "corpus_entry_count":len(entries),
        "matched_verify_count":pack["matched_entry_count"],
        "excluded_verify_count":pack["excluded_entry_count"],
        "stale_version_matched_count":stale.memory_pack["matched_entry_count"],
        "unclassified_failed_candidate_matched_count":
            diagnose.memory_pack["matched_entry_count"],
        "holdout_test_only_matched_count":check.memory_pack["matched_entry_count"],
        "source_covered_by_real_GitHub_CI":
            "independent verification predecessor job completed/SUCCESS",
        "learning_mode":"read_only_source_bound_verified_utility_lookup",
        "memory_weights_updated":False,
        "persistent_external_memory_curated":False,
        "live_repository_mutated":False,
        "patch_selected":False,
        "actual_Lean_to_CPython_refinement_proved":False,
        "global_CI_run_complete":False,
        "host_action_authorized":False,
    }
    (OUTPUT/"receipt.json").write_text(
        json.dumps(values,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    (OUTPUT/"memory-pack.json").write_text(
        json.dumps(pack,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    (OUTPUT/"corpus.json").write_text(
        json.dumps(corp,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    print("CODEAI_V061_VERSION_BOUND_MEMORY_REPLAY",json.dumps(values,sort_keys=True))
    return 0

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--evidence",type=Path,default=DEFAULT_EVIDENCE)
    args=parser.parse_args()
    raise SystemExit(main(args.evidence))
