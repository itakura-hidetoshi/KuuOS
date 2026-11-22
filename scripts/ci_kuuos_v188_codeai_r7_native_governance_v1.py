#!/usr/bin/env python3
"""Run REAL repository CodeAI observation / synthesis / candidate governance on v1.88 R6.

The full Lean candidate was model supplied in an earlier research commit,
not inferred by a live provider inside this test. CodeAI only checks its exact
source-bound proposal and rejection boundary; it does NOT certify any Lean
proof, select a candidate, promote MemoryOS, or grant merge authority.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import time

from runtime import kuuos_codeai_intent_repository_observation_envelope_v0_1 as observation
from runtime import kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 as synth
from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    SOURCE_RECEIPT_DIGEST_FIELD, seal, canonical_digest,
)
from scripts.ci_kuuos_v176_exact_source_audit_v1 import verify_inputs, blob

ROOT = Path(__file__).resolve().parents[1]
REPO = "itakura-hidetoshi/KuuOS"
BASELINE_HEAD = "4dfdb8190f406a92a21fe02fc0ed4af62f002487"
BASELINE_TREE = "8768196a4a5761561aa544a8c6cebb5825aac873"
BASELINE_BRANCH = "validation/kuuos-v188-codeai-r6-component-gluing-20261122"
PARENT_SOURCE = "formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
R1_PATH = "formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR6V1_88.lean"
R2_PATH = "formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR7V1_88.lean"
PINNED_BLOBS = {
 PARENT_SOURCE:"ba6190c2b2f9dac0febfb6357e908e81601c79a1",
 R1_PATH:"a5622716d4d5c7d180f122b67602459fad144af4",
}
R7_BLOB = "e6801f096bc85b0b0111774c726c081341be81b2"
OUT = ROOT / "artifacts/codeai-v188-r7-native-governance"

def baseline_files():
    verify_inputs()
    source={}
    for path,sha in PINNED_BLOBS.items():
        data=(ROOT/path).read_bytes()
        if blob(data)!=sha: raise AssertionError("CODEAI_SOURCE_BLOB_DRIFT:"+path)
        source[path]=data.decode("utf8")
    if blob((ROOT/R2_PATH).read_bytes())!=R7_BLOB:
        raise AssertionError("CODEAI_R2_CANDIDATE_DRIFT")
    return source

def fresh_observation(source,now):
    fixture=json.loads((ROOT/"examples/codeai_intent_repository_observation_envelope_v0_1.json").read_text())
    intent=deepcopy(fixture["intent_packet"])
    intent.update(
      intent_id="codeai-v188-r7-typed-repair",
      source_actor_id="chatgpt-user-intent",
      source_channel="github-mcp-isolated-lean-research",
      intent_revision="v188-r7-source-bound",
      requirements=[
       "Retain immutable frozen original, rejected R2 and pinned v1.88 source blobs",
       "Propose the fixed endpoint and retract proof R3, without weakening statements",
       "Require separate fixed Lean kernel and independent 22-axiom audit",
      ],
      assumptions=[
       "Candidate source was model-supplied and already committed, not live provider-generated",
       "CodeAI observation relies only on the exact supplied baseline files",
       "Independent Lean success and future MemoryOS admissibility remain separate",
      ],
      unresolved_questions=[],
      preserved_invariants=[
       "append-only original and failed candidate source",
       "Lean v4.30.0-rc2 and pinned mathlib",
       "no unproved equality, endpoint RLP or external authority",
      ],
      forbidden_changes=[
       "no original module or legacy tree edits",
       "no trust bypass, no sorry, no new axioms",
       "no CodeAI repository mutation, candidate promotion or merge",
      ],
      success_criteria=[
       "actual native CodeAI admits the exact model-supplied R7 patch as proposal only",
       "synthetic provider falsely claiming authority is explicitly rejected",
      ],
      prior_intent_digests=[],
      intent_created_epoch=now,
      intent_provenance_confirmed=True,
    )
    intent=observation.seal(intent,observation.INTENT_DIGEST_FIELD)
    repo=deepcopy(fixture["repository_observation"])
    repo.update(
      repository_full_name=REPO,
      source_commit_sha=BASELINE_HEAD,
      source_branch=BASELINE_BRANCH,
      tree_digest=BASELINE_TREE,
      dependency_lock_digest=hashlib.sha256((ROOT/"lake-manifest.json").read_bytes()).hexdigest(),
      toolchain_digest="lean-4.30.0-rc2-python-3.12",
      toolchain_supported=True,
      observed_paths=sorted(source),
      unavailable_paths=[],
      declared_path_count=len(source),
      baseline_check_digests=[
         "baseline-git-tree:"+BASELINE_TREE,
         "source-blobs:"+canonical_digest(PINNED_BLOBS),
      ],
      baseline_checks_complete=True,
      code_owner_scope_digest="user-intent:itakura-hidetoshi/KuuOS",
      crosses_unowned_boundary=False,
      observation_started_epoch=now,
      observation_completed_epoch=now,
      session_id="codeai-v188-r7-source-"+BASELINE_HEAD[:12],
      nonce_digest=hashlib.sha256(("v188-r7:"+BASELINE_HEAD).encode()).hexdigest(),
      prior_session_ids=[],
      prior_nonce_digests=[],
      prior_observation_digests=[],
      observation_collected_by_kernel=False,
    )
    repo=observation.seal(repo,observation.REPOSITORY_OBSERVATION_DIGEST_FIELD)
    pol=deepcopy(fixture["observation_policy"])
    pol.update(
      expected_source_commit_sha=BASELINE_HEAD,
      allowed_source_branches=[BASELINE_BRANCH],
      supported_toolchain_digests=["lean-4.30.0-rc2-python-3.12"],
    )
    pol=observation.seal(pol,observation.POLICY_DIGEST_FIELD)
    result=observation.build_codeai_intent_repository_observation_envelope(
      intent_packet=intent,repository_observation=repo,observation_policy=pol)
    if result.status!=observation.STATUS_READY or result.receipt is None:
        raise AssertionError("CODEAI_OBSERVATION_BLOCKED:"+repr(result))
    if result.receipt["codeai_disposition"]!=observation.DISPOSITION_SUPPORTED:
        raise AssertionError("CODEAI_OBSERVATION_NOT_SUPPORTED")
    return result.receipt

def verify_codeai():
    source=baseline_files()
    source_r2=(ROOT/R2_PATH).read_text(encoding="utf8")
    now=int(time.time())
    observation_receipt=fresh_observation(source,now)
    synth_fixture=json.loads((ROOT/"examples/codeai_autonomous_structured_edit_synthesis_v0_1.json").read_text())
    patch_fixture=json.loads((ROOT/"examples/codeai_candidate_patch_envelope_v0_1.json").read_text())
    req=deepcopy(synth_fixture["synthesis_request"])
    req.update(
      request_id="v188-r7-source-bound-model-candidate",
      request_revision="r2",
      intent_text="Propose source-bound 22-declaration Lean candidate R7 for v1.88 with explicit endpoint/first-projection retract witnesses and pinned universes, without changing original or proof obligations.",
      candidate_count=2,
      request_created_epoch=now,
      requirement_trace_ids=["research:v188:canonical-attachment-scaling-retract:typed-repair"],
      test_plan_ids=["pinned-strict-Lean-22-axioms", "exact-source-check", "independent-runner"],
      risk_labels=["formal"],
      unresolved_candidate_questions=[],
      prior_candidate_digests=[],
      prior_producer_session_ids=[],
    )
    req=seal(req,synth.REQUEST_DIGEST_FIELD)
    policy=deepcopy(synth_fixture["synthesis_policy"])
    policy.update(
      evaluation_epoch=now,
      allowed_provider_ids=["gpt","local_model"],
      maximum_provider_calls=2,
      maximum_proposals=2,
      maximum_raw_output_bytes=100000,
      maximum_intent_bytes=30000,
      maximum_repository_snapshot_bytes=250000,
      allowed_repository_path_prefixes=["formal/KUOS"],
      forbidden_repository_path_prefixes=["formal/KUOS/private"],
    )
    policy=seal(policy,synth.POLICY_DIGEST_FIELD)
    candidate_policy=deepcopy(patch_fixture["candidate_policy"])
    candidate_policy.update(
      expected_source_observation_receipt_digest=observation_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
      expected_source_commit_sha=BASELINE_HEAD,
      expected_repository_full_name=REPO,
      allowed_path_prefixes=["formal/KUOS"],
      forbidden_path_prefixes=["formal/KUOS/private"],
      maximum_patch_bytes=200000,
      known_risk_labels=["formal","documentation","release","security"],
      handover_risk_labels=["release","security"],
      allow_deletions=False,
      allow_renames=False,
      evaluation_epoch=now,
      maximum_candidate_age=3600,
    )
    candidate_policy=seal(candidate_policy,"codeai_candidate_patch_policy_digest")
    proposal={
      "proposal_id":"v188-r7-model-supplied-source-bound",
      "candidate_revision":"r2",
      "edits":[{"path":R2_PATH,"operation":"add","new_content":source_r2}],
      "risk_labels":["formal"],"unresolved_candidate_questions":[]
    }
    response={
      "provider_response_id":"v188-model-supplied-r2",
      "producer_session_id":"v188-existing-proposal-not-live-model-inference",
      "response_created_epoch":now,
      "raw_output":json.dumps(proposal,ensure_ascii=False,sort_keys=True,separators=(",",":")),
      "claims_authority":False,
      "hides_uncertainty":False,
      "bypasses_governance":False,
      "evidence_missing":False,
    }
    rejected=dict(response)
    rejected.update(
      provider_response_id="v188-synthetic-untrusted-claim",
      producer_session_id="v188-synthetic-untrusted-session",
      claims_authority=True,
    )
    adapters=[
      synth.ProviderAdapter("a-source-bound-model","gpt","model-supplied-v188-r7",lambda _prompt:response),
      synth.ProviderAdapter("z-unsafe-authority","local_model","synthetic-rejected-claim",lambda _prompt:rejected),
    ]
    result=synth.build_codeai_autonomous_structured_edit_synthesis(
      source_observation_receipt=observation_receipt,
      repository_files=source,
      synthesis_request=req,
      provider_adapters=adapters,
      synthesis_policy=policy,
      candidate_policy=candidate_policy,
    )
    if result.status!=synth.STATUS_READY or len(result.candidates)!=1:
        raise AssertionError("CODEAI_V188_R7_REJECTED:"+repr((result.status,result.issues,result.attempts)))
    if [x.boundary_status for x in result.attempts]!=[synth.BOUNDARY_CANDIDATE,synth.BOUNDARY_REJECT]:
        raise AssertionError("CODEAI_V188_R7_PROVIDER_BOUNDARY")
    c=result.candidates[0]
    patch=c.patch_candidate
    if patch["source_commit_sha"]!=BASELINE_HEAD or patch["changed_paths"]!=[R2_PATH]:
        raise AssertionError("CODEAI_V188_R7_SOURCE_OR_PATH_MISMATCH")
    if patch["added_paths"]!=[R2_PATH]:
        raise AssertionError("CODEAI_V188_R7_NOT_NEW_CANDIDATE_ONLY")
    if result.receipt is None:
        raise AssertionError("CODEAI_V188_R7_RECEIPT_NO_DATA")
    for key in ("candidate_selected","repository_mutation_performed","verification_authority_granted","merge_authority_granted"):
        if result.receipt[key]:
            raise AssertionError("CODEAI_R2_FORBIDDEN_AUTHORITY:"+key)
    if not re.fullmatch(r"[0-9a-f]{40}",os.environ.get("SOURCE_HEAD","")):
        raise AssertionError("CODEAI_R2_EXECUTING_HEAD_NOT_PINNED")
    OUT.mkdir(parents=True,exist_ok=True)
    if list(OUT.iterdir()):
        raise AssertionError("CODEAI_R2_APPEND_ONLY_OUTPUT_VIOLATION")
    receipt={
      "kind":"KUUOS_V188_R7_REAL_CODEAI_NATIVE_GOVERNANCE",
      "codeai_source_parent_head":BASELINE_HEAD,
      "execution_head":os.environ["SOURCE_HEAD"],
      "candidate_source_blob":R7_BLOB,
      "candidate_source_sha256":hashlib.sha256(source_r2.encode()).hexdigest(),
      "candidate_patch_digest":patch["codeai_candidate_patch_digest"],
      "codeai_synthesis_receipt_digest":result.receipt[synth.RECEIPT_DIGEST_FIELD],
      "codeai_observation_receipt_digest":observation_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
      "boundary_statuses":[x.boundary_status for x in result.attempts],
      "model_supplied_not_live_provider_inference":True,
      "r7_candidate_advisory_only":True,
      "proof_certified_by_codeai":False,
      "independent_lean_job_outside_this_receipt":True,
      "memory_admission":False,
      "global_presentation_equality_claimed":False,
      "git_or_merge_authority":False,
    }
    (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V188_R7_REAL_CODEAI_GOVERNANCE_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)

if __name__=="__main__":
    verify_codeai()
