from __future__ import annotations
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import *
from runtime.kuuos_codeai_autonomous_candidate_regeneration_portfolio_v0_1 import *
from runtime.kuuos_codeai_autonomous_candidate_regeneration_preflight_v0_1 import PreparedRegeneration
from runtime.kuuos_codeai_autonomous_candidate_regeneration_receipt_v0_1 import build_receipt

def run_prepared(context: PreparedRegeneration):
    generation = context.generation; source = context.source
    repository = context.repository; seed = list(context.seed)
    request = context.request; policy = context.policy
    candidate_policy = context.candidate_policy; adapters = context.adapters
    combined = list(seed); regenerated = []
    attempts: list[CandidateRegenerationAttemptReceipt] = []
    route_issues: list[str] = []
    seen_ids = {x.proposal_id for x in seed}
    seen_digests = {x.patch_candidate[CANDIDATE_DIGEST_FIELD] for x in seed}
    seen_artifacts = {x.patch_candidate["patch_artifact_digest"] for x in seed}
    seen_response_ids: set[str] = set()
    seen_sessions = set(request["prior_producer_session_ids"])
    seen_sessions.update(str(x.patch_candidate.get("producer_session_id", "")) for x in seed
                         if x.patch_candidate.get("producer_session_id"))
    feedback = list(request["feedback_reasons"])
    rounds_executed = 0; no_progress_rounds = 0
    total_limit = int(policy["maximum_total_provider_calls"])
    per_round = int(policy["maximum_provider_calls_per_round"])
    round_limit = int(request["maximum_rounds_requested"])
    for round_index in range(1, round_limit + 1):
        if len(combined) >= context.target or len(attempts) >= total_limit:
            break
        rounds_executed = round_index; progress = False; round_feedback: list[str] = []
        axis = context.diversity_axes[(round_index - 1) % len(context.diversity_axes)]
        for adapter in adapters[:per_round]:
            if len(combined) >= context.target or len(attempts) >= total_limit:
                break
            attempt_index = len(attempts) + 1
            prompt = prompt_packet(
                request=request, repository=repository, adapter=adapter,
                round_index=round_index, attempt_index=attempt_index,
                diversity_axis=axis, feedback=feedback, candidates=rerank(combined))
            prompt_digest = canonical_digest(prompt)
            try:
                raw_response = adapter.generate(prompt)
            except Exception as exc:
                provider_attempt = attempt(
                    adapter, prompt_digest, boundary_status=BOUNDARY_REJECT,
                    route_reason="provider_exception:" + type(exc).__name__)
                issue = adapter.adapter_id + ":provider_exception:" + type(exc).__name__
                attempts.append(CandidateRegenerationAttemptReceipt(
                    round_index, attempt_index, axis, provider_attempt,
                    novelty_rejection_reason=issue))
                route_issues.append(issue); round_feedback.append(issue); continue
            parse_request = {
                "requirement_trace_ids": list(request["requirement_trace_ids"]),
                "test_plan_ids": list(request["test_plan_ids"]),
                "risk_labels": list(request["risk_labels"]),
                "unresolved_candidate_questions": list(request["unresolved_candidate_questions"]),
                "prior_candidate_digests": sorted(set(request["prior_candidate_digests"]) | seen_digests),
                "prior_producer_session_ids": sorted(set(request["prior_producer_session_ids"]) | seen_sessions),
            }
            parse_policy = {
                "evaluation_epoch": policy["evaluation_epoch"],
                "maximum_response_age": policy["maximum_response_age"],
                "maximum_raw_output_bytes": policy["maximum_raw_output_bytes"],
            }
            proposal, provider_attempt, parse_issues = parse_provider_response(
                adapter, prompt_digest, raw_response, parse_request, parse_policy)
            route_issues.extend(parse_issues); round_feedback.extend(parse_issues)
            duplicate = ""
            if provider_attempt.provider_response_id and provider_attempt.provider_response_id in seen_response_ids:
                duplicate = "duplicate_provider_response_id"
            elif provider_attempt.producer_session_id and provider_attempt.producer_session_id in seen_sessions:
                duplicate = "duplicate_producer_session_id"
            if provider_attempt.provider_response_id:
                seen_response_ids.add(provider_attempt.provider_response_id)
            if provider_attempt.producer_session_id:
                seen_sessions.add(provider_attempt.producer_session_id)
            if duplicate:
                issue = adapter.adapter_id + ":" + duplicate
                route_issues.append(issue); round_feedback.append(issue)
                attempts.append(CandidateRegenerationAttemptReceipt(
                    round_index, attempt_index, axis, provider_attempt,
                    novelty_rejection_reason=duplicate)); continue
            if proposal is None:
                attempts.append(CandidateRegenerationAttemptReceipt(
                    round_index, attempt_index, axis, provider_attempt,
                    novelty_rejection_reason=provider_attempt.route_reason)); continue
            downstream = build_codeai_autonomous_unified_diff_candidates(
                source_observation_receipt=source, repository_files=repository,
                proposals=[proposal], candidate_policy=candidate_policy)
            downstream_digest = (downstream.receipt.get(UNIFIED_DIFF_RECEIPT_DIGEST_FIELD, "")
                                 if downstream.receipt else "")
            if downstream.status != UNIFIED_DIFF_STATUS_READY or not downstream.candidates:
                issue = adapter.adapter_id + ":downstream_candidate_rejected"
                route_issues.append(issue); route_issues.extend(downstream.issues)
                round_feedback.append(issue)
                attempts.append(CandidateRegenerationAttemptReceipt(
                    round_index, attempt_index, axis, provider_attempt,
                    downstream_unified_diff_receipt_digest=downstream_digest,
                    novelty_rejection_reason="downstream_candidate_rejected")); continue
            generated = downstream.candidates[0]; candidate = generated.patch_candidate
            candidate_id = candidate["candidate_id"]
            candidate_digest = candidate[CANDIDATE_DIGEST_FIELD]
            artifact_digest = candidate["patch_artifact_digest"]
            if candidate_id in seen_ids:
                duplicate = "duplicate_candidate_id"
            elif candidate_digest in seen_digests:
                duplicate = "duplicate_candidate_digest"
            elif artifact_digest in seen_artifacts:
                duplicate = "semantic_duplicate_patch_artifact"
            if duplicate:
                issue = adapter.adapter_id + ":" + duplicate
                route_issues.append(issue); round_feedback.append(issue)
                attempts.append(CandidateRegenerationAttemptReceipt(
                    round_index, attempt_index, axis, provider_attempt,
                    downstream_unified_diff_receipt_digest=downstream_digest,
                    candidate_id=candidate_id, candidate_digest=candidate_digest,
                    patch_artifact_digest=artifact_digest,
                    novelty_rejection_reason=duplicate)); continue
            seen_ids.add(candidate_id); seen_digests.add(candidate_digest)
            seen_artifacts.add(artifact_digest); combined.append(generated)
            regenerated.append(generated); progress = True
            attempts.append(CandidateRegenerationAttemptReceipt(
                round_index, attempt_index, axis, provider_attempt,
                downstream_unified_diff_receipt_digest=downstream_digest,
                candidate_id=candidate_id, candidate_digest=candidate_digest,
                patch_artifact_digest=artifact_digest, accepted_novel_candidate=True))
        if not progress:
            no_progress_rounds += 1
        feedback = sorted(set(feedback + round_feedback))[-int(policy["maximum_feedback_items"]):]
    regenerated_ranked = rerank(regenerated); combined_ranked = rerank(combined)
    receipt = build_receipt(
        generation=generation, digest_field=context.source_digest_field,
        source=source, request=request, policy=policy,
        candidate_policy=candidate_policy, repository=repository,
        adapters=adapters, seed=rerank(seed), attempts=attempts,
        regenerated=regenerated_ranked, combined=combined_ranked,
        rounds_executed=rounds_executed, no_progress_rounds=no_progress_rounds,
        issues=route_issues)
    return CodeAIAutonomousCandidateRegenerationResult(
        STATUS_READY if regenerated else STATUS_BLOCKED,
        tuple(route_issues), tuple(attempts), regenerated_ranked,
        combined_ranked, receipt)

__all__ = [name for name in globals() if not name.startswith("__")]
