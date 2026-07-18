from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import *
from runtime.kuuos_codeai_autonomous_candidate_regeneration_portfolio_v0_1 import *

@dataclass(frozen=True)
class PreparedRegeneration:
    generation: Mapping[str, Any]
    source: Mapping[str, Any]
    repository: Mapping[str, str]
    seed: tuple[GeneratedUnifiedDiffCandidate, ...]
    request: Mapping[str, Any]
    policy: Mapping[str, Any]
    candidate_policy: Mapping[str, Any]
    adapters: tuple[ProviderAdapter, ...]
    source_digest_field: str
    target: int
    diversity_axes: tuple[str, ...]

def blocked(*issues: str):
    return CodeAIAutonomousCandidateRegenerationResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), (), (), (), None)

def prepare(*, source_generation_receipt: Any, source_observation_receipt: Any,
            repository_files: Any, seed_candidates: Any,
            regeneration_request: Any, provider_adapters: Any,
            regeneration_policy: Any, candidate_policy: Any):
    generation = mapping(source_generation_receipt)
    source = mapping(source_observation_receipt)
    candidate_policy_map = mapping(candidate_policy)
    repository, repository_issues = validate_repository(repository_files)
    request, request_issues = validate_request(regeneration_request)
    policy, policy_issues = validate_policy(regeneration_policy)
    adapters, adapter_issues = validate_adapters(provider_adapters)
    issues = repository_issues + request_issues + policy_issues + adapter_issues
    if generation is None:
        issues.append("source_generation_receipt_not_mapping")
    if source is None:
        issues.append("source_observation_receipt_not_mapping")
    elif not isinstance(source.get(SOURCE_RECEIPT_DIGEST_FIELD), str):
        issues.append("source_observation_receipt_digest_missing")
    elif not digest_ok(source, SOURCE_RECEIPT_DIGEST_FIELD):
        issues.append("source_observation_receipt_digest_mismatch")
    if candidate_policy_map is None:
        issues.append("candidate_policy_not_mapping")
    elif not isinstance(candidate_policy_map.get(CANDIDATE_POLICY_DIGEST_FIELD), str):
        issues.append("candidate_policy_digest_missing")
    elif not digest_ok(candidate_policy_map, CANDIDATE_POLICY_DIGEST_FIELD):
        issues.append("candidate_policy_digest_mismatch")
    digest_field = source_digest_field(generation.get("profile_version") if generation else None)
    if generation is not None:
        if digest_field is None:
            issues.append("source_generation_profile_unsupported")
        elif not isinstance(generation.get(digest_field), str) or not digest_ok(generation, digest_field):
            issues.append("source_generation_receipt_digest_mismatch")
        else:
            issues.extend(source_route_issues(generation, str(generation.get("profile_version"))))
    values = (generation, source, candidate_policy_map, repository, request, policy, adapters)
    if issues or None in values or digest_field is None:
        return None, blocked(*issues)
    assert generation is not None and source is not None and repository is not None
    assert request is not None and policy is not None and adapters is not None
    assert candidate_policy_map is not None
    checks = (
        ("source_generation_observation_mismatch", generation.get("source_observation_receipt_digest"), source.get(SOURCE_RECEIPT_DIGEST_FIELD)),
        ("source_generation_candidate_policy_mismatch", generation.get("candidate_policy_digest"), candidate_policy_map.get(CANDIDATE_POLICY_DIGEST_FIELD)),
        ("source_generation_repository_snapshot_mismatch", generation.get("repository_snapshot_digest"), canonical_digest(repository)),
        ("candidate_policy_source_receipt_mismatch", candidate_policy_map.get("expected_source_observation_receipt_digest"), source.get(SOURCE_RECEIPT_DIGEST_FIELD)),
        ("candidate_policy_repository_mismatch", candidate_policy_map.get("expected_repository_full_name"), source.get("repository_full_name")),
        ("candidate_policy_source_commit_mismatch", candidate_policy_map.get("expected_source_commit_sha"), source.get("source_commit_sha")),
    )
    for issue, expected, observed in checks:
        if expected != observed:
            return None, blocked(issue)
    seed, seed_issues = validate_seed_candidates(seed_candidates, generation, source)
    if seed_issues or seed is None:
        return None, blocked(*seed_issues)
    if len(seed) > int(policy["maximum_existing_candidates"]):
        return None, blocked("seed_candidate_budget_exceeded")
    evaluation = int(policy["evaluation_epoch"]); created = int(request["request_created_epoch"])
    if not evaluation - int(policy["maximum_request_age"]) <= created <= evaluation:
        return None, blocked("regeneration_request_window_invalid")
    if len(request["intent_text"].encode("utf-8")) > int(policy["maximum_intent_bytes"]):
        return None, blocked("intent_budget_exceeded")
    if len(request["feedback_reasons"]) > int(policy["maximum_feedback_items"]):
        return None, blocked("feedback_item_budget_exceeded")
    snapshot_bytes = len(json.dumps(repository, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8"))
    if snapshot_bytes > int(policy["maximum_repository_snapshot_bytes"]):
        return None, blocked("repository_snapshot_budget_exceeded")
    scope_issues = repository_scope_issues(repository, policy)
    if scope_issues:
        return None, blocked(*scope_issues)
    if int(request["maximum_rounds_requested"]) > int(policy["maximum_rounds"]):
        return None, blocked("requested_round_count_exceeds_policy")
    target = int(request["target_unique_candidate_count"])
    if target <= len(seed):
        return None, blocked("target_must_exceed_seed_candidate_count")
    if target > int(policy["maximum_unique_candidates"]):
        return None, blocked("target_unique_candidate_count_exceeds_policy")
    axes = tuple(request["diversity_axes"])
    disallowed_axes = sorted(set(axes).difference(policy["allowed_diversity_axes"]))
    if disallowed_axes:
        return None, blocked(*(f"diversity_axis_not_allowed:{x}" for x in disallowed_axes))
    ordered = tuple(sorted(adapters, key=lambda item: item.adapter_id))
    disallowed_providers = sorted({x.provider_id for x in ordered}.difference(policy["allowed_provider_ids"]))
    if disallowed_providers:
        return None, blocked(*(f"provider_not_allowed:{x}" for x in disallowed_providers))
    return PreparedRegeneration(
        generation, source, repository, tuple(seed), request, policy,
        candidate_policy_map, ordered, digest_field, target, axes,
    ), None

__all__ = [name for name in globals() if not name.startswith("__")]
