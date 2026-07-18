from __future__ import annotations
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import *

def build_receipt(*, generation, digest_field, source, request, policy,
                  candidate_policy, repository, adapters, seed, attempts,
                  regenerated, combined, rounds_executed, no_progress_rounds,
                  issues):
    target = int(request["target_unique_candidate_count"])
    value = {
        "schema_version": SCHEMA_VERSION, "profile_version": PROFILE_VERSION,
        "source_generation_profile_version": generation["profile_version"],
        "source_generation_receipt_digest": generation[digest_field],
        "source_observation_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "regeneration_request_digest": request[REQUEST_DIGEST_FIELD],
        "regeneration_policy_digest": policy[POLICY_DIGEST_FIELD],
        "candidate_policy_digest": candidate_policy[CANDIDATE_POLICY_DIGEST_FIELD],
        "repository_snapshot_digest": canonical_digest(repository),
        "provider_adapter_set_digest": canonical_digest([
            {"adapter_id": x.adapter_id, "provider_id": x.provider_id, "model_id": x.model_id}
            for x in adapters]),
        "seed_candidate_count": len(seed),
        "seed_candidate_ids": [x.proposal_id for x in seed],
        "seed_candidate_digests": [x.patch_candidate[CANDIDATE_DIGEST_FIELD] for x in seed],
        "seed_patch_artifact_digests": [x.patch_candidate["patch_artifact_digest"] for x in seed],
        "target_unique_candidate_count": target,
        "rounds_executed": rounds_executed, "no_progress_rounds": no_progress_rounds,
        "provider_call_count": len(attempts),
        "regeneration_attempt_receipts": [asdict(x) for x in attempts],
        "regenerated_candidate_count": len(regenerated),
        "regenerated_candidate_ids": [x.proposal_id for x in regenerated],
        "regenerated_candidate_digests": [x.patch_candidate[CANDIDATE_DIGEST_FIELD] for x in regenerated],
        "regenerated_patch_artifact_digests": [x.patch_candidate["patch_artifact_digest"] for x in regenerated],
        "combined_candidate_count": len(combined),
        "combined_candidate_ids": [x.proposal_id for x in combined],
        "combined_candidate_digests": [x.patch_candidate[CANDIDATE_DIGEST_FIELD] for x in combined],
        "combined_patch_artifact_digests": [x.patch_candidate["patch_artifact_digest"] for x in combined],
        "target_reached": len(combined) >= target, "issues": list(issues),
        "codeai_disposition": DISPOSITION_REGENERATED if regenerated else DISPOSITION_NO_NOVEL_CANDIDATE,
        "operating_mode": MODE_PROPOSAL_ONLY, "route_receipt_recorded": True,
        "provider_calls_performed_by_kernel": bool(attempts),
        "provider_output_boundary_evaluated": bool(attempts),
        "feedback_used_as_candidate_context_only": True,
        "semantic_patch_deduplication_performed": True,
        "repository_snapshot_read_only": True,
        "candidate_regeneration_performed": bool(regenerated),
        "candidate_selected": False, "verification_lease_issued": False,
        "execution_lease_issued": False, "patch_applied": False,
        "repository_mutation_performed": False, "git_ref_changed": False,
        "branch_created": False, "commit_created": False,
        "push_performed": False, "pull_request_created": False,
        "merge_performed": False, "deployment_performed": False,
        "secret_access_performed": False, "selection_authority_granted": False,
        "verification_authority_granted": False, "execution_authority_granted": False,
        "merge_authority_granted": False, "deployment_authority_granted": False,
        "secret_access_authority_granted": False, "feedback_treated_as_truth": False,
        "novelty_treated_as_correctness": False,
        "regenerated_candidate_treated_as_correct": False,
        "validation_treated_as_correctness_proof": False,
        "history_read_only": True, "future_only": True, "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)

__all__ = [name for name in globals() if not name.startswith("__")]
