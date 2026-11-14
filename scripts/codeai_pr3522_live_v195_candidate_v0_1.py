#!/usr/bin/env python3
"""Real source-anchored CodeAI v0.1 observation and Candidate Patch for PR #3522.

The patch is an externally proposed one-lemma repair, not a kernel-generated
proof, Lean success, repository edit, or permission to merge. This route
invokes the repository's actual CodeAI Python kernels, not fixture simulation.
"""
from __future__ import annotations

from copy import deepcopy
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.request

from runtime import kuuos_codeai_intent_repository_observation_envelope_v0_1 as observation
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as candidate_patch

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "itakura-hidetoshi/KuuOS"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95.lean"
AUDIT = "tests/test_public_root_restoration.py"
BEFORE = "simpa only [Nat.succ_add, Nat.zero_add] using hinv"
AFTER = "simpa only [Nat.one_add] using hinv"
NEXT_AFTER = """calc
      Nat.succ (inv
        (show Quiver.Hom.{0} NatOneCell.star NatOneCell.star
          from (1 : Nat))) =
          Nat.add (inv
            (show Quiver.Hom.{0} NatOneCell.star NatOneCell.star
              from (1 : Nat))) 1 := (Nat.add_one _).symm
      _ = Nat.add 1 (inv
            (show Quiver.Hom.{0} NatOneCell.star NatOneCell.star
              from (1 : Nat))) := Nat.add_comm _ _
      _ = 0 := hinv"""
UNIT_BEFORE = """  map₂_leftUnitor := by
    intros
    simp [natTriangleMapComp]
  map₂_rightUnitor := by
    intros
    simp [natTriangleMapComp]"""
UNIT_AFTER = """  map₂_leftUnitor := by
    intros
    change (0 : Nat) = Nat.add (Nat.add 0 0) _
    simp [natTriangleMapComp]
  map₂_rightUnitor := by
    intros
    change (0 : Nat) = Nat.add (Nat.add 0 0) _
    simp [natTriangleMapComp]"""
ASSOC_BEFORE = """  map₂_associator := by
    intro a b c d f g h
    have hab : a.as ≤ b.as := f.as.le
    have hbc : b.as ≤ c.as := g.as.le
    have hcd : c.as ≤ d.as := h.as.le
    have ha := a.as.isLt
    have hb := b.as.isLt
    have hc := c.as.isLt
    have hd := d.as.isLt
    simp only [natTriangleMapComp]
    split_ifs <;> omega"""
ASSOC_AFTER = """  map₂_associator := by
    intro a b c d f g h
    have hab : a.as ≤ b.as := f.as.le
    have hbc : b.as ≤ c.as := g.as.le
    have hcd : c.as ≤ d.as := h.as.le
    rcases a with ⟨a⟩
    rcases b with ⟨b⟩
    rcases c with ⟨c⟩
    rcases d with ⟨d⟩
    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
      simp_all [natTriangleMapComp] <;> omega"""

def git_blob_sha(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\\0".decode("unicode_escape").encode("ascii") + content).hexdigest()


def load_example(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def read_true_head_tree(source_head: str) -> str:
    # Read-only public GitHub REST endpoint. No git/gh CLI or repository mutation.
    uri = "https://api.github.com/repos/" + REPOSITORY + "/git/commits/" + source_head
    request = urllib.request.Request(
        uri, headers={"Accept": "application/vnd.github+json", "User-Agent": "KuuOS-CodeAI-v195"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    if data.get("sha") != source_head:
        raise RuntimeError("CodeAI source HEAD mismatch")
    tree = data.get("tree", {}).get("sha")
    if not isinstance(tree, str) or re.fullmatch(r"[0-9a-f]{40}", tree) is None:
        raise RuntimeError("CodeAI true source Git tree unavailable")
    return tree


def run_if_parent_pr() -> None:
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return
    event_file = os.environ.get("GITHUB_EVENT_PATH")
    if not event_file:
        raise RuntimeError("CodeAI live PR event path absent")
    event = json.loads(Path(event_file).read_text(encoding="utf-8"))
    if event.get("number") != 3522:
        return
    if event.get("repository", {}).get("full_name") != REPOSITORY:
        raise RuntimeError("CodeAI repository identity mismatch")
    pr = event["pull_request"]
    head_sha = pr["head"]["sha"]
    branch = pr["head"]["ref"]
    if re.fullmatch(r"[0-9a-f]{40}", head_sha) is None:
        raise RuntimeError("Invalid CodeAI parent HEAD")
    if pr["head"]["repo"]["full_name"] != REPOSITORY:
        raise RuntimeError("CodeAI parent source repository mismatch")

    data = (ROOT / TARGET).read_bytes()
    source_text = data.decode("utf-8")
    old_blob = git_blob_sha(data)
    audit_text = (ROOT / AUDIT).read_text(encoding="utf-8")
    audit_entry = '"KUOS/DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95.lean": "' + old_blob + '"'
    if audit_text.count(audit_entry) != 1:
        raise RuntimeError("CodeAI exact-source blob not individually registered")
    if source_text.count(BEFORE) == 1:
        repair_before, repair_after = BEFORE, AFTER
        repair_stage = "round1-Nat-one-add"
    elif (old_blob == "c51cbc33e9897252f6893f4c00c352fdd6369e00"
          and source_text.count(AFTER) == 1):
        # The exact prior CodeAI candidate is materialized in the parent.
        # A fresh Strict Lean error identified the next source-bound repair.
        repair_before, repair_after = AFTER, NEXT_AFTER
        repair_stage = "round2-Nat-add-one-explicit-calc"
    elif (old_blob == "55f0fd1aff12e2450003b0355d983013fd4ed3a3"
          and source_text.count(UNIT_BEFORE) == 1):
        # Exact new Lean error (#43650529216): unitor equations need explicit
        # translation into the additive Nat hom category. This is only a
        # proposal; it must be validated by fresh strict Lean after application.
        repair_before, repair_after = UNIT_BEFORE, UNIT_AFTER
        repair_stage = "round3-left-right-unitors-nat-normalization"
    elif (old_blob == "f7dcf6d9cddf3820b78c91375f0ec460874a7734"
          and source_text.count(ASSOC_BEFORE) == 1):
        # Exact strict Lean run #43652242761: only the finite ordinal
        # associator proof blocks the core; directly enumerate all
        # finite endpoint values, retaining each monotonicity witness.
        repair_before, repair_after = ASSOC_BEFORE, ASSOC_AFTER
        repair_stage = "round4-Duskin-finite-associator-enumeration"
    elif old_blob == "ca05d2cad1994d94713be4d7b3feea9f315905c6":
        print("KUUOS_CODEAI_REAL_V195_APPLIED_RECEIPT " + json.dumps({
            "source_head": head_sha,
            "applied_blob": old_blob,
            "candidate_regenerated": False,
            "replay_excluded": True,
            "strict_lean_proof": "unverified",
        }, sort_keys=True))
        return
    else:
        raise RuntimeError("CodeAI v1.95 source drift or unsupported proof candidate")
    if any(token in repair_after for token in ("admit", "sorry", "axiom")):
        raise RuntimeError("CodeAI candidate forbidden proof marker")

    new_text = source_text.replace(repair_before, repair_after)
    new_blob = git_blob_sha(new_text.encode("utf-8"))
    unified = "".join(
        difflib.unified_diff(
            source_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile="a/" + TARGET,
            tofile="b/" + TARGET,
            n=3,
        )
    )
    artifact = (
        "diff --git a/" + TARGET + " b/" + TARGET + "\n"
        + "index " + old_blob[:7] + ".." + new_blob[:7] + " 100644\n"
        + unified
    )
    shape, parse_issues = candidate_patch.parse_unified_diff(artifact)
    if parse_issues or shape is None or shape.changed_paths != (TARGET,):
        raise RuntimeError("CodeAI candidate diff rejected: " + repr(parse_issues))

    t0 = int(time.time())
    true_tree_sha = read_true_head_tree(head_sha)
    observed_paths = [TARGET, AUDIT, "lean-toolchain", "lake-manifest.json"]
    if any(not (ROOT / x).is_file() for x in observed_paths):
        raise RuntimeError("CodeAI observed path missing")
    toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    if toolchain != "leanprover/lean4:v4.30.0-rc2":
        raise RuntimeError("CodeAI fixed Lean pin changed: " + toolchain)
    manifest_sha = hashlib.sha256((ROOT / "lake-manifest.json").read_bytes()).hexdigest()
    toolchain_id = "lean-4.30.0-rc2-python-3.12"

    sample = load_example("codeai_intent_repository_observation_envelope_v0_1.json")
    intent = deepcopy(sample["intent_packet"])
    intent.update({
        "intent_id": "kuuos-pr3522-v195-nat-one-add-" + head_sha[:12],
        "intent_revision": "r1",
        "source_actor_id": "codeai-assisted-research",
        "source_channel": "pull-request-exact-source-diagnostics",
        "requirements": ["Repair the exact v1.95 non-invertible Nat 2-cell proof without new axioms"],
        "assumptions": ["Candidate patch is a hypothesis until strict pinned Lean validates it"],
        "unresolved_questions": [],
        "preserved_invariants": ["exact parent source","no sorry/admit/axiom","independent Lean certification"],
        "forbidden_changes": ["no theorem weakening","no main merge","no branch rewrite"],
        "success_criteria": ["candidate is admitted only as an unverified CodeAI proposal"],
        "intent_created_epoch": t0,
        "prior_intent_digests": [],
        "intent_provenance_confirmed": True,
    })
    intent = observation.seal(intent, observation.INTENT_DIGEST_FIELD)

    repo_sample = deepcopy(sample["repository_observation"])
    repo_sample.update({
        "repository_full_name": REPOSITORY,
        "source_commit_sha": head_sha,
        "source_branch": branch,
        "tree_digest": true_tree_sha,
        "dependency_lock_digest": manifest_sha,
        "toolchain_digest": toolchain_id,
        "toolchain_supported": True,
        "observed_paths": observed_paths,
        "unavailable_paths": [],
        "declared_path_count": len(observed_paths),
        "baseline_check_digests": ["exact-v195-blob:" + old_blob, "pinned-manifest:" + manifest_sha],
        "baseline_checks_complete": True,
        "code_owner_scope_digest": "repo-owner:" + REPOSITORY,
        "crosses_unowned_boundary": False,
        "observation_started_epoch": t0,
        "observation_completed_epoch": int(time.time()),
        "session_id": "pr3522-" + head_sha[:16],
        "nonce_digest": hashlib.sha256((head_sha + ":codeai-v195").encode()).hexdigest(),
        "prior_session_ids": [],
        "prior_nonce_digests": [],
        "prior_observation_digests": [],
    })
    repo_sample = observation.seal(repo_sample, observation.REPOSITORY_OBSERVATION_DIGEST_FIELD)
    op = deepcopy(sample["observation_policy"])
    op.update({
        "expected_repository_full_name": REPOSITORY,
        "expected_source_commit_sha": head_sha,
        "allowed_source_branches": [branch],
        "supported_toolchain_digests": [toolchain_id],
        "require_complete_baseline": True,
        "require_code_owner_scope": True,
        "allow_partial_observation": False,
    })
    op = observation.seal(op, observation.POLICY_DIGEST_FIELD)
    result = observation.build_codeai_intent_repository_observation_envelope(
        intent_packet=intent, repository_observation=repo_sample, observation_policy=op
    )
    if result.status != observation.STATUS_READY or result.receipt is None:
        raise RuntimeError("CodeAI actual observation blocked: " + repr(result.issues))
    source_receipt = result.receipt
    if source_receipt["codeai_disposition"] != observation.DISPOSITION_SUPPORTED:
        raise RuntimeError("CodeAI actual observation not supported: " + source_receipt["codeai_disposition"])

    cand_sample = load_example("codeai_candidate_patch_envelope_v0_1.json")
    candidate = deepcopy(cand_sample["patch_candidate"])
    candidate.update({
        "candidate_id": "pr3522-v195-" + repair_stage + "-" + head_sha[:12],
        "candidate_revision": "r1",
        "producer_id": "external-research-candidate",
        "producer_session_id": "candidate-" + head_sha[:16],
        "source_observation_receipt_digest": source_receipt[observation.RECEIPT_DIGEST_FIELD],
        "intent_packet_digest": intent[observation.INTENT_DIGEST_FIELD],
        "repository_full_name": REPOSITORY,
        "source_commit_sha": head_sha,
        "patch_artifact_digest": candidate_patch.patch_artifact_digest(artifact),
        "patch_size_bytes": len(artifact.encode("utf-8")),
        "changed_paths": [TARGET],
        "added_paths": [],
        "modified_paths": [TARGET],
        "deleted_paths": [],
        "renamed_from_paths": [],
        "renamed_to_paths": [],
        "declared_change_count": 1,
        "requirement_trace_ids": ["pr3522:v195:noninvertible-Nat-proof"],
        "test_plan_ids": ["pinned-Lean4-Strict-v195-exact-source"],
        "risk_labels": ["formal-proof"],
        "unresolved_candidate_questions": [],
        "candidate_created_epoch": int(time.time()),
        "prior_candidate_digests": [],
        "prior_producer_session_ids": [],
        "candidate_provenance_confirmed": True,
    })
    candidate = candidate_patch.seal(candidate, candidate_patch.CANDIDATE_DIGEST_FIELD)
    cp = deepcopy(cand_sample["candidate_policy"])
    cp.update({
        "expected_source_observation_receipt_digest": source_receipt[observation.RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name": REPOSITORY,
        "expected_source_commit_sha": head_sha,
        "allowed_path_prefixes": ["formal/KUOS"],
        "forbidden_path_prefixes": ["legacy", "formal/KuuOSFormal"],
        "maximum_changed_paths": 1,
        "allow_deletions": False,
        "allow_renames": False,
        "allow_binary_patches": False,
        "allow_submodule_patches": False,
        "allow_mode_changes": False,
        "require_requirement_trace": True,
        "require_test_plan": True,
        "allow_evidence_degradation": False,
        "known_risk_labels": ["formal-proof"],
        "handover_risk_labels": [],
        "evaluation_epoch": int(time.time()) + 1,
        "maximum_candidate_age": 3600,
    })
    cp = candidate_patch.seal(cp, candidate_patch.POLICY_DIGEST_FIELD)
    cr = candidate_patch.build_codeai_candidate_patch_envelope(
        source_observation_receipt=source_receipt,
        patch_candidate=candidate,
        patch_artifact=artifact,
        candidate_policy=cp,
    )
    if cr.status != candidate_patch.STATUS_READY or cr.receipt is None:
        raise RuntimeError("CodeAI candidate execution blocked: " + repr(cr.issues))
    if cr.receipt["codeai_disposition"] != candidate_patch.DISPOSITION_SUPPORTED:
        raise RuntimeError("CodeAI candidate not admitted: " + cr.receipt["codeai_disposition"])
    if cr.receipt.get("repository_mutation_performed") or cr.receipt.get("candidate_selected"):
        raise RuntimeError("CodeAI candidate improperly escalated authority")
    # CodeAI's actual autonomous unified-diff, selection and isolated
    # application kernels run on the same exact v1.95 source snapshot.
    # None of these stages compiles Lean, modifies Git or authorizes merge.
    from runtime import kuuos_codeai_autonomous_unified_diff_candidates_v0_1 as unified
    from runtime import kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 as selection
    from runtime import kuuos_codeai_autonomous_isolated_candidate_application_v0_1 as isolated
    repository_files = {TARGET: source_text}
    original_snapshot = deepcopy(repository_files)
    proposal = {
        "proposal_id": "pr3522-v195-" + repair_stage + "-" + head_sha[:12],
        "candidate_revision": "r1",
        "producer_id": "external-research-candidate",
        "producer_session_id": "structured-proposal-" + head_sha[:16],
        "candidate_created_epoch": int(time.time()),
        "edits": [{"path": TARGET, "operation": "modify", "new_content": new_text}],
        "requirement_trace_ids": ["pr3522:v195:noninvertible-Nat-proof"],
        "test_plan_ids": ["pinned-Lean4-Strict-v195-exact-source"],
        "risk_labels": ["formal-proof"],
        "unresolved_candidate_questions": [],
        "prior_candidate_digests": [],
        "prior_producer_session_ids": [],
    }
    ur = unified.build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=source_receipt,
        repository_files=repository_files,
        proposals=[proposal],
        candidate_policy=cp,
    )
    if ur.status != unified.STATUS_READY or ur.receipt is None or len(ur.candidates) != 1:
        raise RuntimeError("CodeAI real autonomous candidate generation blocked: " + repr(ur.issues))
    if ur.receipt["codeai_disposition"] != unified.DISPOSITION_SYNTHESIZED:
        raise RuntimeError("CodeAI autonomous candidate not synthesized")

    select_example = load_example("codeai_autonomous_candidate_portfolio_selection_v0_1.json")
    req = deepcopy(select_example["selection_request"])
    req.update({
        "selection_request_id": "pr3522-v195-selection-" + head_sha[:12],
        "source_portfolio_receipt_digest": ur.receipt[unified.RECEIPT_DIGEST_FIELD],
        "requested_by_actor_id": "codeai-assisted-research",
        "request_created_epoch": int(time.time()),
    })
    req = candidate_patch.seal(req, selection.REQUEST_DIGEST_FIELD)
    sel_policy = deepcopy(select_example["selection_policy"])
    sel_policy.update({
        "expected_source_portfolio_receipt_digest": ur.receipt[unified.RECEIPT_DIGEST_FIELD],
        "maximum_candidate_count": 1,
        "maximum_changed_paths": 1,
        "allowed_risk_labels": ["formal-proof"],
        "forbidden_risk_labels": [],
        "allowed_path_prefixes": ["formal/KUOS"],
        "forbidden_path_prefixes": ["legacy"],
        "evaluation_epoch": int(time.time()) + 1,
        "maximum_request_age": 3600,
    })
    sel_policy = candidate_patch.seal(sel_policy, selection.POLICY_DIGEST_FIELD)
    selected = selection.build_codeai_autonomous_candidate_portfolio_selection(
        source_portfolio_receipt=ur.receipt,
        candidates=ur.candidates,
        selection_request=req,
        selection_policy=sel_policy,
    )
    if selected.status != selection.STATUS_READY or selected.receipt is None or selected.selected_candidate is None:
        raise RuntimeError("CodeAI real selection blocked: " + repr(selected.issues))

    app_example = load_example("codeai_autonomous_isolated_candidate_application_v0_1.json")
    request = deepcopy(app_example["application_request"])
    selected_candidate = selected.selected_candidate
    selected_digest = selected_candidate.patch_candidate[candidate_patch.CANDIDATE_DIGEST_FIELD]
    source_snapshot_digest = candidate_patch.canonical_digest(repository_files)
    request.update({
        "application_request_id": "pr3522-v195-isolated-" + head_sha[:12],
        "source_selection_receipt_digest": selected.receipt[selection.RECEIPT_DIGEST_FIELD],
        "selected_candidate_digest": selected_digest,
        "source_repository_snapshot_digest": source_snapshot_digest,
        "requested_by_actor_id": "codeai-assisted-research",
        "request_created_epoch": int(time.time()),
    })
    request = candidate_patch.seal(request, isolated.REQUEST_DIGEST_FIELD)
    app_policy = deepcopy(app_example["application_policy"])
    app_policy.update({
        "expected_source_selection_receipt_digest": selected.receipt[selection.RECEIPT_DIGEST_FIELD],
        "expected_selected_candidate_digest": selected_digest,
        "expected_patch_artifact_digest": selected_candidate.patch_candidate["patch_artifact_digest"],
        "expected_repository_full_name": REPOSITORY,
        "expected_source_commit_sha": head_sha,
        "expected_source_repository_snapshot_digest": source_snapshot_digest,
        "maximum_source_path_count": 1,
        "maximum_result_path_count": 1,
        "maximum_changed_paths": 1,
        "allowed_path_prefixes": ["formal/KUOS"],
        "forbidden_path_prefixes": ["legacy"],
        "allow_additions": False,
        "allow_modifications": True,
        "allow_deletions": False,
        "require_exact_changed_path_accounting": True,
        "evaluation_epoch": int(time.time()) + 1,
        "maximum_request_age": 3600,
    })
    app_policy = candidate_patch.seal(app_policy, isolated.POLICY_DIGEST_FIELD)
    applied = isolated.build_codeai_autonomous_isolated_candidate_application(
        source_selection_receipt=selected.receipt,
        selected_candidate=selected_candidate,
        repository_files=repository_files,
        application_request=request,
        application_policy=app_policy,
    )
    if applied.status != isolated.STATUS_READY or applied.receipt is None or applied.resulting_repository_files is None:
        raise RuntimeError("CodeAI real isolated application blocked: " + repr(applied.issues))
    if repository_files != original_snapshot or applied.resulting_repository_files.get(TARGET) != new_text:
        raise RuntimeError("CodeAI real isolated application content mismatch")
    if not applied.receipt["isolated_patch_applied"] or applied.receipt["repository_mutation_performed"]:
        raise RuntimeError("CodeAI isolated execution did not preserve no-Git boundary")

    output = ROOT / "artifacts" / "codeai-v195"
    output.mkdir(parents=True, exist_ok=True)
    record = {
        "repair_stage": repair_stage,
        "source_repo": REPOSITORY,
        "source_head": head_sha,
        "source_git_tree": true_tree_sha,
        "source_blob": old_blob,
        "candidate_blob": new_blob,
        "source_observation_receipt": source_receipt,
        "candidate_receipt": cr.receipt,
        "generated_candidate_receipt": ur.receipt,
        "selection_receipt": selected.receipt,
        "isolated_application_receipt": applied.receipt,
        "isolated_verification": "snapshot_materialized_not_Lean_compiled",
        "strict_lean_proof": "not_certified",
        "git_effect": False,
    }
    (output / "pr3522-codeai-v195-candidate.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "pr3522-v195-candidate.diff").write_text(artifact, encoding="utf-8")
    print("KUUOS_CODEAI_REAL_V195_CANDIDATE_RECEIPT " + json.dumps({
        "source_head": head_sha,
        "repair_stage": repair_stage,
        "source_blob": old_blob,
        "candidate_blob": new_blob,
        "observation_receipt": source_receipt[observation.RECEIPT_DIGEST_FIELD],
        "candidate_receipt": cr.receipt[candidate_patch.RECEIPT_DIGEST_FIELD],
        "candidate_disposition": cr.receipt["codeai_disposition"],
        "generated_candidate_receipt": ur.receipt[unified.RECEIPT_DIGEST_FIELD],
        "selection_receipt": selected.receipt[selection.RECEIPT_DIGEST_FIELD],
        "isolated_application_receipt": applied.receipt[isolated.RECEIPT_DIGEST_FIELD],
        "isolated_patch_applied": applied.receipt["isolated_patch_applied"],
        "strict_lean_proof": "unverified",
        "actual_kernel_calls": [
            "build_codeai_intent_repository_observation_envelope",
            "build_codeai_candidate_patch_envelope",
            "build_codeai_autonomous_unified_diff_candidates",
            "build_codeai_autonomous_candidate_portfolio_selection",
            "build_codeai_autonomous_isolated_candidate_application",
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    run_if_parent_pr()
