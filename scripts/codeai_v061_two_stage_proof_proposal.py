#!/usr/bin/env python3
"""CodeAI native provider-neutral candidate pipeline for Lean v0.61.

Run only against the exact original canonical main source snapshot. The
model-supplied candidate is TEXT committed in examples, not a live provider
inference performed by the CodeAI runtime; identify that provenance honestly.
Actual KuuOS CodeAI kernels create read-only observation receipt, accept a
provider-neutral structured proposal, admit its candidate-patch governance,
and generate one advisory unified diff with all non-authority flags false.

Only after CodeAI admits that proposal, this CI script materializes its exact
text into the EPHEMERAL runner checkout for independent pinned Lean testing.
CodeAI itself does not modify GitHub refs, commit, merge or grant authority.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import time

from runtime import kuuos_codeai_intent_repository_observation_envelope_v0_1 as observation
from runtime import kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 as synth
from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    seal,
)

ROOT = Path(__file__).resolve().parents[1]
MAIN_HEAD = "ac5f7db4425e7d377abce8cadee676b4e34341a4"
MAIN_TREE = "f043d43e953cd793122acdb64beaf83ab68e6585"
TOOLCHAIN = "leanprover/lean4:v4.30.0-rc2"
MATHLIB = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
PROPOSAL_SOURCE = "examples/codeai_v061_two_stage_private_append.lean.txt"
CANDIDATE_PATH = (
    "formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendV0_61.lean"
)
SOURCE_BLOBS = {
    "formal/KUOS/Architecture/LeanPythonTaggedPrivateAppendInvarianceV0_60.lean":
        "0fa7e765056bdb0fff7540165a741d2dcb191efb",
    "formal/KUOS/Architecture/LeanPythonTaggedSpanObservationGluingV0_59.lean":
        "a1c931c4382e7d150706fb19cacda9d697ed95b4",
    "formal/KUOS/Architecture/LeanPythonTaggedForkArchiveBoundaryV0_58.lean":
        "06e01b49e7d2119e37340351906ad587f0f440bb",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
}
AXIOM_NAMES = (
    "private_append_two_stage_assoc",
    "two_stage_overlap_compatibility_iff",
    "two_stage_obstruction_persists",
    "two_stage_tagged_gluing_iff",
    "two_stage_tagged_gluing_obstruction",
    "two_stage_old_left_private_observation",
    "two_stage_old_right_private_observation",
    "two_stage_proof_grants_no_original_execution",
)


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def _read_pinned_snapshot() -> dict[str, str]:
    if (base := os.getenv("CODEAI_EXACT_MAIN_SHA", MAIN_HEAD)) != MAIN_HEAD:
        raise ValueError("CODEAI_EXACT_MAIN_SHA_not_canonical:" + base)
    if (ROOT / "lean-toolchain").read_text().strip() != TOOLCHAIN:
        raise ValueError("pinned_Lean_toolchain_modified")
    manifest = json.loads((ROOT / "lake-manifest.json").read_text())
    mathlibs = [p for p in manifest["packages"] if p["name"] == "mathlib"]
    if len(mathlibs) != 1 or mathlibs[0]["rev"] != MATHLIB:
        raise ValueError("pinned_mathlib_revision_modified")
    sources: dict[str, str] = {}
    for name, expected in SOURCE_BLOBS.items():
        data = (ROOT / name).read_bytes()
        if _git_blob(data) != expected:
            raise ValueError("pinned_main_source_changed:" + name)
        sources[name] = data.decode("utf-8")
    if (ROOT / CANDIDATE_PATH).exists():
        raise ValueError("candidate_was_already_adopted_or_preexisting")
    return sources


def _fresh_observation(
    repository_files: dict[str, str], epoch: int,
) -> dict[str, object]:
    example = json.loads((
        ROOT / "examples/codeai_intent_repository_observation_envelope_v0_1.json"
    ).read_text(encoding="utf-8"))
    intent = deepcopy(example["intent_packet"])
    intent.update(
        intent_id="chatgpt-request-codeai-v061-two-stage-proof",
        source_actor_id="chatgpt-user-request",
        source_channel="chatgpt-github-mcp-controlled-research",
        intent_revision="v061-model-supplied-r1",
        requirements=[
            "Use KuuOS original CodeAI kernels on current pinned Lean sources",
            "Generate advisory complete-file Lean theorem patch candidate only",
            "Independently compile candidate in fixed Lean before adoption",
        ],
        assumptions=[
            "This model-supplied candidate is not a live CodeAI provider inference",
            "Source files were collected outside CodeAI using exact pinned Git SHA",
            "The source snapshot is limited to four imported formal modules",
        ],
        preserved_invariants=[
            "append-only and overwrite-forbidden original repository root",
            "external model proposal not repository truth",
            "candidate selection not independent verification or merge authority",
        ],
        forbidden_changes=[
            "do not modify canonical source modules",
            "no original PlanOS authority or host execution effects",
            "no Git reference write, commit, push or merge",
        ],
        success_criteria=[
            "admit one CodeAI governed proof candidate with precise source provenance",
            "obtain independent strict Lean and exact axiom audits",
        ],
        intent_created_epoch=epoch,
        prior_intent_digests=[],
        intent_provenance_confirmed=True,
    )
    intent = observation.seal(intent, observation.INTENT_DIGEST_FIELD)

    repository = deepcopy(example["repository_observation"])
    repository.update(
        source_commit_sha=MAIN_HEAD,
        source_branch="main",
        tree_digest=MAIN_TREE,
        dependency_lock_digest=hashlib.sha256(
            (ROOT / "lake-manifest.json").read_bytes()
        ).hexdigest(),
        toolchain_digest="lean-4.30.0-rc2-python-3.12",
        toolchain_supported=True,
        observed_paths=sorted(repository_files),
        unavailable_paths=[],
        declared_path_count=len(repository_files),
        baseline_check_digests=[
            "exact-main-git-tree:" + MAIN_TREE,
            "original-lean-blobs:" + canonical_digest(SOURCE_BLOBS),
        ],
        baseline_checks_complete=True,
        code_owner_scope_digest="user-supplied-intent:itakura-hidetoshi/KuuOS",
        crosses_unowned_boundary=False,
        observation_started_epoch=epoch,
        observation_completed_epoch=epoch,
        session_id="codeai-v061-source-" + MAIN_HEAD[:12],
        nonce_digest=hashlib.sha256(
            ("codeai-v061-source:" + MAIN_HEAD).encode()
        ).hexdigest(),
        prior_session_ids=[],
        prior_nonce_digests=[],
        prior_observation_digests=[],
        observation_collected_by_kernel=False,
    )
    repository = observation.seal(
        repository, observation.REPOSITORY_OBSERVATION_DIGEST_FIELD
    )

    policy = deepcopy(example["observation_policy"])
    policy.update(
        expected_source_commit_sha=MAIN_HEAD,
        allowed_source_branches=["main"],
        supported_toolchain_digests=["lean-4.30.0-rc2-python-3.12"],
    )
    policy = observation.seal(policy, observation.POLICY_DIGEST_FIELD)
    result = observation.build_codeai_intent_repository_observation_envelope(
        intent_packet=intent,
        repository_observation=repository,
        observation_policy=policy,
    )
    if result.status != observation.STATUS_READY or result.receipt is None:
        raise AssertionError("CodeAI_observation_preflight:" + repr(result))
    if result.receipt["codeai_disposition"] != observation.DISPOSITION_SUPPORTED:
        raise AssertionError("CodeAI_observation_NOT_SUPPORTED:" + repr(result))
    return result.receipt


def run_codeai_proposal(*, materialize_for_independent_ci: bool = False):
    repo = _read_pinned_snapshot()
    proof = (ROOT / PROPOSAL_SOURCE).read_text(encoding="utf-8")
    assert proof.startswith("import Mathlib\n"), "candidate imports not pinned"
    assert proof.endswith("\n")
    assert proof.count("#print axioms ") == len(AXIOM_NAMES)
    prefix = "KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61."
    for name in AXIOM_NAMES:
        assert "#print axioms " + prefix + name in proof, name
    # Run with freshly sealed epoch-bounded requests. Epoch is SELF-ASSERTED,
    # not a cryptographically authenticated historical event timestamp.
    now = int(time.time())
    source = _fresh_observation(repo, now)
    example = json.loads((
        ROOT / "examples/codeai_autonomous_structured_edit_synthesis_v0_1.json"
    ).read_text(encoding="utf-8"))
    patch_example = json.loads((
        ROOT / "examples/codeai_candidate_patch_envelope_v0_1.json"
    ).read_text(encoding="utf-8"))

    synthesis_request = deepcopy(example["synthesis_request"])
    synthesis_request.update(
        request_id="v061-two-stage-conditional-append-proposal",
        request_revision="r1",
        intent_text=(
            "Use the supplied canonical Lean sources to propose a separate "
            "v0.61 two-stage private-append theorem module. Preserve original "
            "v0.60 assumptions, prove gluing iff and persistent obstruction, "
            "and never assert external custody, history truth or host authority."
        ),
        candidate_count=2,
        request_created_epoch=now,
        requirement_trace_ids=["research:v061:two-stage-append-proof"],
        test_plan_ids=["ci:v061:strict-Lean-8-axioms"],
        risk_labels=["formal"],
        unresolved_candidate_questions=[],
        prior_candidate_digests=[],
        prior_producer_session_ids=[],
    )
    synthesis_request = seal(synthesis_request, synth.REQUEST_DIGEST_FIELD)

    synthesis_policy = deepcopy(example["synthesis_policy"])
    synthesis_policy.update(
        evaluation_epoch=now,
        allowed_provider_ids=["gpt", "local_model"],
        allowed_repository_path_prefixes=["formal/KUOS/Architecture", "formal/KUOS/PlanOS"],
        forbidden_repository_path_prefixes=["formal/KUOS/Architecture/private"],
        maximum_repository_snapshot_bytes=300000,
        maximum_intent_bytes=30000,
        maximum_raw_output_bytes=100000,
    )
    synthesis_policy = seal(synthesis_policy, synth.POLICY_DIGEST_FIELD)

    candidate_policy = deepcopy(patch_example["candidate_policy"])
    candidate_policy.update(
        expected_source_observation_receipt_digest=source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        expected_source_commit_sha=MAIN_HEAD,
        expected_repository_full_name="itakura-hidetoshi/KuuOS",
        allowed_path_prefixes=["formal/KUOS/Architecture"],
        forbidden_path_prefixes=["formal/KUOS/Architecture/private"],
        known_risk_labels=["formal", "documentation", "release", "security"],
        handover_risk_labels=["release", "security"],
        maximum_patch_bytes=200000,
        allow_deletions=False,
        allow_renames=False,
        evaluation_epoch=now,
        maximum_candidate_age=3600,
    )
    candidate_policy = seal(
        candidate_policy, "codeai_candidate_patch_policy_digest"
    )

    candidate_raw = {
        "proposal_id": "model-supplied-v061-two-stage-proof-r1",
        "candidate_revision": "r1",
        "edits": [{
            "path": CANDIDATE_PATH,
            "operation": "add",
            "new_content": proof,
        }],
        "risk_labels": ["formal"],
        "unresolved_candidate_questions": [],
    }
    accepted_response = {
        "provider_response_id": "chatgpt-model-supplied-v061-proof-r1",
        "producer_session_id": "model-supplied-not-live-provider-session-v061",
        "response_created_epoch": now,
        "raw_output": json.dumps(
            candidate_raw, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ),
        "claims_authority": False,
        "hides_uncertainty": False,
        "bypasses_governance": False,
        "evidence_missing": False,
    }
    rejected_response = dict(accepted_response)
    rejected_response.update(
        provider_response_id="synthetic-asserted-authority-v061",
        producer_session_id="synthetic-rejected-provider-session-v061",
        claims_authority=True,
    )
    adapters = [
        synth.ProviderAdapter(
            "a-chatgpt-model-supplied", "gpt", "gpt-6-model-supplied",
            lambda _prompt: accepted_response,
        ),
        synth.ProviderAdapter(
            "z-synthetic-authority-claim", "local_model",
            "adversarial-fixture-only", lambda _prompt: rejected_response,
        ),
    ]

    result = synth.build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=source,
        repository_files=repo,
        synthesis_request=synthesis_request,
        provider_adapters=adapters,
        synthesis_policy=synthesis_policy,
        candidate_policy=candidate_policy,
    )
    if result.status != synth.STATUS_READY or len(result.candidates) != 1:
        raise AssertionError(
            "CodeAI_unadmitted_proof_candidate:"
            + repr((result.status, result.issues, result.attempts))
        )
    assert tuple(a.boundary_status for a in result.attempts) == (
        synth.BOUNDARY_CANDIDATE,
        synth.BOUNDARY_REJECT,
    ), result.attempts
    candidate = result.candidates[0]
    patch_data = candidate.patch_candidate
    assert patch_data["changed_paths"] == [CANDIDATE_PATH], patch_data
    assert patch_data["added_paths"] == [CANDIDATE_PATH]
    assert patch_data["source_commit_sha"] == MAIN_HEAD
    assert patch_data["repository_full_name"] == "itakura-hidetoshi/KuuOS"
    assert "diff --git a/" + CANDIDATE_PATH in candidate.patch_artifact
    assert result.receipt is not None
    assert result.receipt["generated_candidate_count"] == 1
    assert result.receipt["provider_call_count"] == 2
    assert result.receipt["candidate_selected"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["execution_authority_granted"] is False
    assert result.receipt["merge_authority_granted"] is False
    assert result.receipt["provider_output_treated_as_correct"] is False

    evidence = {
        "source_commit_sha": MAIN_HEAD,
        "source_git_tree_sha": MAIN_TREE,
        "candidate_source_sha256": hashlib.sha256(
            proof.encode("utf-8")
        ).hexdigest(),
        "candidate_path": CANDIDATE_PATH,
        "model_input_provenance": "model-supplied-example-not-live-inference",
        "codeai_observation_receipt_digest":
            source[SOURCE_RECEIPT_DIGEST_FIELD],
        "codeai_synthesis_receipt_digest":
            result.receipt[synth.RECEIPT_DIGEST_FIELD],
        "codeai_candidate_digest": patch_data["codeai_candidate_patch_digest"],
        "admitted_provider_boundary_routes": [
            a.boundary_status for a in result.attempts
        ],
        "codeai_diff_candidate_generated": True,
        "codeai_candidate_selected": False,
        "codeai_candidate_verified_by_Lean": False,
        "codeai_candidate_applied_to_Git": False,
        "original_planos_host_authority": False,
        "independent_custody_authenticated": False,
        "lean_comparison_pending": True,
    }

    if materialize_for_independent_ci:
        if os.environ.get("CODEAI_ISOLATED_CI_PROOF_VERIFY") != "1":
            raise PermissionError("only_explicit_ephemeral_ci_materialization")
        path = ROOT / CANDIDATE_PATH
        # A separate, explicitly authorized CI verification action writes to
        # the ephemeral checkout AFTER the CodeAI proposal-only receipt.
        # CodeAI itself has not applied the patch or changed GitHub.
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8", newline="\n") as out:
            out.write(proof)
        assert path.read_bytes() == proof.encode("utf-8")
        evidence["ephemeral_ci_candidate_materialized"] = True

    evidence_dir = ROOT / "artifacts" / "codeai-v061-proof"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "receipt.json").write_text(
        json.dumps(evidence, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    (evidence_dir / "candidate.patch").write_text(
        candidate.patch_artifact, encoding="utf-8",
    )
    print("CODEAI_V061_ACTUAL_KERNEL_CANDIDATE_ADMITTED:", json.dumps(
        evidence, sort_keys=True
    ))
    return evidence


if __name__ == "__main__":
    run_codeai_proposal(materialize_for_independent_ci=True)
