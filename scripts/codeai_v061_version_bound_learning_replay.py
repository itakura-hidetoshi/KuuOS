#!/usr/bin/env python3
"""Read-only KuuOS CodeAI v0.61 subtask-memory replay from independent Lean evidence.

A SEPARATE GitHub CI job must have completed its candidate verification job
successfully and transferred the immutable evidence artifact. This step
constructs a source-bound, append-only learning/recall receipt, NOT a model
weight update or an independent externally curated memory database.

All four subtasks, including VERIFY, remain inconclusive until independently
issued four-family CodeAI verifier evidence is established. Formal Lean success
is preserved separately and never becomes a verified-useful learning hint.
Failed candidate C is NOT given a repair-memory success hint or silently
translated into static errors.

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


def check_actual_v02_ensemble_hold(evidence: dict, now: int) -> dict:
    """Run the ORIGINAL KuuOS v0.2 ensemble kernel on actual v0.61 formal evidence.

    This is NOT a four-family certificate. Only ONE candidate-bound type/formal
    result exists. The separately compiled Lean result is real, but external
    issuer attestation, reviewer organization separation, independent prompts,
    and three complementary verification families are NO_DATA. We intentionally
    set each unproven independence claim to False and demand fail-closed.
    The packet's timestamp is the local replay time, NOT a GitHub-issued
    verification timestamp. That is another reason this is not an admissible
    external verifier certificate.
    """
    from runtime.kuuos_codeai_independent_verifier_ensemble_v0_2 import (
        evaluate_independent_verifier_ensemble,
    )
    from runtime.kuuos_codeai_independent_verifier_ensemble_checks_v0_2 import seal
    from runtime.kuuos_codeai_independent_verifier_ensemble_schema_v0_2 import (
        EVIDENCE_DIGEST_FIELD, POLICY_DIGEST_FIELD, REQUEST_DIGEST_FIELD,
        STATUS_BLOCKED,
    )
    from scripts.build_codeai_independent_verifier_ensemble_fixture_v0_2 import build_fixture

    template = build_fixture()  # Schema/policy shape ONLY; never reuse its fake 4 packets.
    a = evidence["results"][0]
    assert a["status"] == "INDEPENDENT_FIXED_LEAN_AND_AXIOM_PASSED"
    assert a["axiom_declarations_checked"] == 8
    assert a["strict_lean_exit_code"] == 0
    assert not a["sorryAx"]
    digest = a["source_sha256"]
    source_context_digest = stable({
        "source_commit": source.MAIN_HEAD,
        "source_tree_sha1": source.MAIN_TREE,
        "source_git_blobs": source.SOURCE_BLOBS,
        "candidate_sha256": digest,
        "independent_fixed_Lean_evidence_digest": evidence["evidence_digest"],
    })
    request = dict(template["request"])
    request.update(
        request_id="v061-real-formal-only-nonadmitted",
        request_revision="r1",
        repository_full_name="itakura-hidetoshi/KuuOS",
        source_commit_sha=source.MAIN_HEAD,
        candidate_digest=digest,
        context_pack_digest=source_context_digest,
        request_created_epoch=now,
    )
    request = seal(request, REQUEST_DIGEST_FIELD)
    policy = dict(template["policy"])
    policy.update(
        expected_repository_full_name=request["repository_full_name"],
        expected_source_commit_sha=request["source_commit_sha"],
        expected_candidate_digest=digest,
        expected_context_pack_digest=source_context_digest,
        allowed_verifier_ids=["github-ci-formal-one-runner"],
        allowed_reviewer_ids=["no-attested-external-reviewer"],
        allowed_runner_ids=["github-actions-one-verifier"],
        evaluation_epoch=now,
    )
    policy = seal(policy, POLICY_DIGEST_FIELD)

    # This is a DECLARED, content-bound formal observation, not an independently
    # signed reviewer packet. The other three families are deliberately absent.
    formal = dict(template["evidence_packets"][0])
    checks = ["candidate-A-eight-axiom-audit", "candidate-A-pinned-Lean-compile"]
    formal.update(
        evidence_id="v061-formal-only-"+digest[:16],
        verifier_id="github-ci-formal-one-runner",
        reviewer_id="no-attested-external-reviewer",
        runner_id="github-actions-one-verifier",
        organization_id="single-github-origin-unattested",
        verification_session_id="v061-formal-replay-"+digest[:12],
        nonce="read-only-replay-"+digest[:12],
        repository_full_name=request["repository_full_name"],
        source_commit_sha=source.MAIN_HEAD,
        candidate_digest=digest,
        context_pack_digest=source_context_digest,
        check_family="type_and_formal",
        verification_method_digest=stable({"method":"pinned-lean-8-axioms"}),
        environment_digest=stable({"source":"github-ci-formal-artifact","attested":False}),
        toolchain_digest=stable({"lean":source.TOOLCHAIN,"mathlib":source.MATHLIB}),
        protocol_digest=stable({"version":"v0.61","independence":"NO_DATA"}),
        check_ids=checks,
        passed_check_ids=checks,
        failed_check_ids=[],
        skipped_check_ids=[],
        finding_labels=[],
        highest_severity="none",
        declared_outcome="passed",
        falsification_executed=False,
        falsification_passed=False,
        acceptance_criteria_satisfied=True,
        independent_from_candidate_producer=False,
        independent_from_other_verifiers=False,
        prompt_lineage_independent=False,
        repair_memory_independent=False,
        test_generation_independent=False,
        isolated_execution_reported=False,
        evidence_artifact_digest=evidence["evidence_digest"],
        verification_started_epoch=now,
        verification_completed_epoch=now,
        kernel_executed_verification=False,
        repository_mutation_performed=False,
        candidate_selection_performed=False,
        execution_authority_granted=False,
        git_authority_granted=False,
        correctness_proof_claimed=False,
    )
    formal = seal(formal, EVIDENCE_DIGEST_FIELD)
    outcome = evaluate_independent_verifier_ensemble(
        request=request, policy=policy, evidence_packets=[formal],
    )
    required = {
        "ensemble_insufficient_verifier_count",
        "ensemble_insufficient_organization_count",
        "ensemble_insufficient_method_count",
        "ensemble_required_family_missing",
        "evidence[0]:independence_requirement_failed:independent_from_candidate_producer",
        "evidence[0]:independence_requirement_failed:independent_from_other_verifiers",
        "evidence[0]:independence_requirement_failed:prompt_lineage_independent",
        "evidence[0]:independence_requirement_failed:repair_memory_independent",
        "evidence[0]:independence_requirement_failed:test_generation_independent",
    }
    assert outcome.status == STATUS_BLOCKED, (outcome.status, outcome.issues)
    assert required.issubset(set(outcome.issues)), (required, outcome.issues)
    assert outcome.receipt is None and outcome.ensemble is None
    return {
        "schema":"kuuos.codeai.v061.actual-ensemble-v02-formal-only-hold.v1",
        "source_main_sha":source.MAIN_HEAD,
        "candidate_source_sha256":digest,
        "independent_formal_evidence_sha256":evidence["evidence_digest"],
        "actual_original_ensemble_v02_invoked":True,
        "actual_original_ensemble_v02_status":outcome.status,
        "ensemble_v02_issues":list(outcome.issues),
        "observed_family":["type_and_formal"],
        "unobserved_families":[
            "adversarial_and_falsification","behavioral_and_regression",
            "maintainability_and_static",
        ],
        "independent_organizations_attested":0,
        "external_verifier_issuer_authentication":"NO_DATA",
        "verification_epoch_is_git_signed":False,
        "reusable_memory_hint":False,
        "verified_useful":False,
        "execution_or_merge_authority":False,
    }


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
        # This is only a VERSION BINDING for the currently incomplete
        # verification slice, NOT a certified 4-family v0.2 ensemble receipt.
        "verifier_ensemble_digest":stable({
            "independent_verifier_ensemble_v0_2": "NO_DATA",
            "type_and_formal": evidence["results"][0]["log_sha256"],
            "behavioral_and_regression": "NO_DATA",
            "adversarial_and_falsification": "NO_DATA",
            "maintainability_and_static": "NO_DATA",
            "organizations_and_sessions_independent": "NO_DATA",
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
        # The fixed Lean kernel may have certified the eight declarations,
        # but the current candidate has no independently admitted *four-
        # family* CodeAI Verifier Ensemble v0.2 evidence. No subtask record
        # can yet claim independently verified usefulness for a future task.
        "outcome":memory.OUTCOME_INCONCLUSIVE,
        "evidence_created_epoch":now,
        "subtask_summary":(
            "v0.61 fixed-Lean source-bound verification observed; missing "
            "four-family CodeAI Independent Verifier Ensemble v0.2, so "
            "future-usefulness NOT certified" if kind=="verify" else
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


def check_candidate_c_compiler_lint_boundary(
    evidence: dict, lean_log: str, original_source: str,
) -> dict:
    """Bind actual rejected C lint diagnostics to their exact Lean/compiler bytes.

    A Lean elaborator/linter error is NOT a KuuOS static-preflight finding.
    No TypedErrorClassification v0.1 certificate, regeneration receipt, or
    verified-useful repair memory may be synthesized from this observation.
    The compiler log and candidate bytes are consumed from separate CI
    artifacts; the artifact transport is not an external issuer signature.
    """
    import re

    from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
        FINDING_TAXONOMY,
    )
    from scripts.codeai_v061_independent_candidate_verification import (
        EXPECTED_SHA256,
    )

    assert len(evidence["results"]) == 3
    assert evidence["source_candidate_portfolio"] == \
        "model_supplied_proposals_governed_by_actual_codeai"
    c = evidence["results"][2]
    assert c["label"] == "model-c"
    assert c["status"] == "DIRECT_LEAN_REJECTED_TYPED_LINT_PENDING"
    assert c["source_sha256"] == EXPECTED_SHA256["model-c"]
    assert hashlib.sha256(original_source.encode("utf-8")).hexdigest() == \
        c["source_sha256"], "C_SOURCE_BYTES_CHANGED"
    assert c["diagnostic_digest"] == hashlib.sha256(
        lean_log.encode("utf-8")).hexdigest(), "C_LEAN_LOG_DIGEST_CHANGED"
    assert c["strict_lean_exit_code"] != 0
    assert c["proven_lean_declarations"] == 0
    assert c["error_count"] == 2
    assert c["original_source_unchanged"] is True
    assert c["independent_repair_evidence_admitted"] is False
    assert c["reusable_repair_memory_admitted"] is False
    assert evidence["typed_error_classification_c_admitted"] is False

    matches = re.findall(
        r"(?m)^.*?\.lean:(\d+):(\d+): error: ([^\r\n]*)$",
        lean_log,
    )
    assert len(matches) == 2, "C_COMPILER_DIAGNOSTIC_COUNT_MISMATCH"
    assert [int(row[0]) for row in matches] == [140, 159], \
        "C_COMPILER_LINE_MISMATCH"
    messages = [row[2].strip() for row in matches]
    assert messages == c["diagnostics"], "C_COMPILER_MESSAGE_MISMATCH"
    assert all("try 'simp' instead of 'simpa'" in m for m in messages), \
        "C_COMPILER_DIAGNOSTIC_KIND_MISMATCH"

    lines = original_source.splitlines()
    assert len(lines) >= 159
    assert lines[139].strip() == "simpa only [hL] using"
    assert lines[158].strip() == "simpa only [hR] using"

    # The current original KuuOS taxonomy covers *static preflight* findings.
    # It contains no Lean kernel/elaborator/linter diagnostic code. A matching
    # English word must not be treated as a certified native taxonomy entry.
    assert "lean_simp_simpa_lint" not in FINDING_TAXONOMY
    assert "lean_elaborator_lint" not in FINDING_TAXONOMY

    report = {
        "schema": "kuuos.codeai.v061.compiler-lint-boundary.v1",
        "source_main_sha": source.MAIN_HEAD,
        "candidate": "model-c",
        "candidate_source_sha256": c["source_sha256"],
        "compiler_log_sha256": c["diagnostic_digest"],
        "source_evidence_digest": evidence["evidence_digest"],
        "observed_diagnostics": [
            {"line": int(line), "column": int(col), "message": msg}
            for (line, col, _), msg in zip(matches, messages)
        ],
        "observed_stage": "independent_pinned_lean_elaboration_and_lint",
        "native_codeai_static_preflight_taxonomy_applicable": False,
        "native_typed_error_classification_certified": False,
        "structural_repair_cause_proved": False,
        "repair_hypothesis": "replace redundant simpa with simp at the two observed lines; test required",
        "verification_guided_regeneration_receipt": "NO_DATA",
        "independently_issued_repair_receipt": "NO_DATA",
        "candidate_formally_adopted": False,
        "candidate_repair_executed": False,
        "candidate_selection_authority": False,
        "verified_useful_memory_admitted": False,
        "reusable_memory_hint": False,
        "global_four_family_ensemble": "NO_DATA",
        "source_log_external_signature": "NO_DATA",
        "host_execution_or_git_authority": False,
    }
    report["observation_digest"] = stable(report)
    return report


def main(path: Path) -> int:
    # The Memory kernel itself is a read-only lookup. The V0.61 evidence
    # promoter must be called only AFTER the separate independent verifier
    # job succeeded, as expressed by this exact GitHub Actions needs chain.
    # Environment checks are NOT cryptographic identity proof; the GitHub
    # workflow/receipt lineage is still necessary.
    if (
        os.getenv("GITHUB_ACTIONS")!="true"
        or os.getenv("GITHUB_REPOSITORY")!="itakura-hidetoshi/KuuOS"
        or os.getenv("GITHUB_JOB")!="read-only-exact-subtask-memory-replay"
        or os.getenv("GITHUB_WORKFLOW")!=
          "KuuOS CodeAI v0.61 exact-source learning, Lean MCP and independent verification"
        or not os.getenv("GITHUB_RUN_ID","").isdigit()
        or Path(path).resolve()!=DEFAULT_EVIDENCE.resolve()
    ):
        raise RuntimeError("HOLD_NO_ACTUAL_INDEPENDENT_CI_PREDECESSOR_CONTEXT")
    evidence=load_exact_evidence(path)
    now=int(time.time())
    # Independently replay C's actual negative compiler log, not an invented
    # static-preflight/typed-classifier receipt or a successful repair.
    c_log = (DEFAULT_EVIDENCE.parent / "model-c/lean.log").read_text(
        encoding="utf-8")
    c_source = (ROOT / "examples/codeai_v061_two_stage_private_append_variant_c.lean.txt").read_text(
        encoding="utf-8")
    c_boundary = check_candidate_c_compiler_lint_boundary(
        evidence, c_log, c_source)
    ensemble_hold=check_actual_v02_ensemble_hold(evidence,now)
    entries=[build_entry(kind,evidence,now)
             for kind in memory.SUBTASK_KINDS]
    req,pol,corp=build_request_policy(evidence,entries,now)
    output=memory.build_codeai_subtask_level_version_bound_memory(
        request=req,policy=pol,corpus=corp,
    )
    assert output.status==memory.STATUS_READY,(output.status,output.issues)
    pack=output.memory_pack
    assert pack is not None and output.receipt is not None
    assert pack["matched_entry_count"]==0,pack
    assert pack["excluded_entry_count"]==4,pack
    assert pack["matched_entries"]==[],pack
    assert pack["recommendation"]==memory.RECOMMENDATION_NONE
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
            "exact-GitHub-needs-success-bound verification receipt; runner context not external signature",
        "github_workflow_run_id":os.environ["GITHUB_RUN_ID"],
        "github_workflow_job":os.environ["GITHUB_JOB"],
        "learning_mode":"read_only_source_bound_hold_until_actual_v02_ensemble",
        "verified_useful_memory_admitted":False,
        "actual_four_family_independent_verifier_ensemble_v02":"NO_DATA",
        "actual_v02_ensemble_kernel_invoked":ensemble_hold["actual_original_ensemble_v02_invoked"],
        "actual_v02_ensemble_status":ensemble_hold["actual_original_ensemble_v02_status"],
        "actual_v02_ensemble_unmet_issues":ensemble_hold["ensemble_v02_issues"],
        "model_c_compiler_lint_boundary_digest":c_boundary["observation_digest"],
        "model_c_native_typed_classifier_admitted":False,
        "next_candidate_memory_hint_available":False,
        "memory_weights_updated":False,
        "persistent_external_memory_curated":False,
        "live_repository_mutated":False,
        "patch_selected":False,
        "actual_Lean_to_CPython_refinement_proved":False,
        "global_CI_run_complete":False,
        "host_action_authorized":False,
    }
    (OUTPUT/"compiler-lint-boundary.json").write_text(
        json.dumps(c_boundary,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    (OUTPUT/"independent-v02-held.json").write_text(
        json.dumps(ensemble_hold,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
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
