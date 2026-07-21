from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_temporal_holdout_replay_corpus_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Temporal Holdout Replay Corpus v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
DISPOSITION_SEALED = "temporal_holdout_replay_corpus_sealed"

SPLIT_DEVELOPMENT = "development"
SPLIT_HOLDOUT = "holdout"
SPLITS = (SPLIT_DEVELOPMENT, SPLIT_HOLDOUT)

SCENARIO_PASS = "verified_patch"
SCENARIO_TYPECHECK_FAILURE = "typecheck_failure"
SCENARIO_OVERCORRECTION = "overcorrection"
SCENARIO_TEST_OVERFIT = "test_overfit"
SCENARIO_ABSTENTION = "abstention"
SCENARIO_ENVIRONMENT_FAILURE = "environment_failure"
SCENARIO_CLASSES = (
    SCENARIO_PASS,
    SCENARIO_TYPECHECK_FAILURE,
    SCENARIO_OVERCORRECTION,
    SCENARIO_TEST_OVERFIT,
    SCENARIO_ABSTENTION,
    SCENARIO_ENVIRONMENT_FAILURE,
)

ENTRY_DIGEST_FIELD = "codeai_temporal_holdout_replay_entry_digest"
CORPUS_DIGEST_FIELD = "codeai_temporal_holdout_replay_corpus_digest"
REQUEST_DIGEST_FIELD = "codeai_temporal_holdout_replay_corpus_request_digest"
POLICY_DIGEST_FIELD = "codeai_temporal_holdout_replay_corpus_policy_digest"
EVIDENCE_DIGEST_FIELD = "codeai_temporal_holdout_replay_corpus_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_temporal_holdout_replay_corpus_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,127}$")

ENTRY_FIELDS = {
    "schema_version", "profile_version", "case_id", "repository_full_name",
    "issue_digest", "source_commit_sha", "observed_epoch", "split",
    "scenario_class", "replay_case_digest", "environment_digest",
    "provider_configuration_digest", "evaluation_protocol_digest",
    "labels_available_to_candidate_generation", "used_for_threshold_tuning",
    "used_for_memory_training", "used_for_prompt_selection",
    "used_for_model_selection", ENTRY_DIGEST_FIELD,
}

CORPUS_FIELDS = {
    "schema_version", "profile_version", "corpus_id", "repository_full_name",
    "cutoff_commit_sha", "cutoff_epoch", "development_window_start_epoch",
    "development_window_end_epoch", "holdout_window_start_epoch",
    "holdout_window_end_epoch", "entries", "entry_digests",
    "development_entry_digests", "holdout_entry_digests",
    "development_case_count", "holdout_case_count", "scenario_classes",
    "environment_digest", "provider_configuration_digest",
    "evaluation_protocol_digest", "content_addressed", "temporal_split_frozen",
    "holdout_hidden_from_candidate_generation",
    "holdout_excluded_from_threshold_tuning",
    "holdout_excluded_from_memory_training",
    "holdout_excluded_from_prompt_selection",
    "holdout_excluded_from_model_selection", CORPUS_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "schema_version", "profile_version", "corpus_id", "repository_full_name",
    "corpus_digest", "evaluator_id", "request_created_epoch",
    "seal_temporal_holdout_corpus", REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "schema_version", "profile_version", "expected_repository_full_name",
    "expected_corpus_digest", "authorized_evaluator_ids", "evaluation_epoch",
    "maximum_request_age", "minimum_development_cases", "minimum_holdout_cases",
    "required_scenario_classes", "require_temporal_order",
    "require_distinct_case_ids_across_splits",
    "require_distinct_issue_digests_across_splits",
    "require_distinct_replay_case_digests_across_splits",
    "require_uniform_environment_digest",
    "require_uniform_provider_configuration_digest",
    "require_uniform_evaluation_protocol_digest",
    "require_holdout_hidden_from_candidate_generation",
    "require_holdout_excluded_from_threshold_tuning",
    "require_holdout_excluded_from_memory_training",
    "require_holdout_excluded_from_prompt_selection",
    "require_holdout_excluded_from_model_selection",
    "allow_read_only_corpus_sealing", "allow_historical_code_reexecution",
    "allow_provider_invocation", "allow_verification_runner_invocation",
    "allow_repository_mutation", "allow_git_effect", "allow_network_access",
    "allow_secret_read", "allow_selection_authority", "allow_successor_authority",
    POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAITemporalHoldoutReplayCorpusResult:
    status: str
    issues: tuple[str, ...]
    evidence: dict[str, Any] | None
    receipt: dict[str, Any] | None


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result[field] = digest_without(result, field)
    return result


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def exact_fields(value: Mapping[str, Any], expected: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = expected - set(value)
    extra = set(value) - expected
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def digest_value(value: Any) -> bool:
    return isinstance(value, str) and SHA256.fullmatch(value) is not None


def identifier(value: Any) -> bool:
    return isinstance(value, str) and IDENTIFIER.fullmatch(value) is not None


def natural(value: Any, *, positive: bool = False) -> int | None:
    minimum = 1 if positive else 0
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        return None
    return value


def unique_strings(value: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    if not isinstance(value, list) or (nonempty and not value):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    result = tuple(value)
    return result if len(result) == len(set(result)) else None


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAITemporalHoldoutReplayCorpusResult", "canonical_json", "canonical_digest",
    "digest_without", "seal", "mapping", "exact_fields", "digest_value",
    "identifier", "natural", "unique_strings",
]
