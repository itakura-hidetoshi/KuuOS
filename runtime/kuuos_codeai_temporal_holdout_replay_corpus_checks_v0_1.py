from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_temporal_holdout_replay_corpus_schema_v0_1 import *


def validate_entry(entry: Mapping[str, Any], *, index: int) -> list[str]:
    prefix = f"entry:{index}"
    issues = exact_fields(entry, ENTRY_FIELDS, prefix)
    if issues:
        return issues
    if entry.get("schema_version") != SCHEMA_VERSION:
        issues.append(prefix + "_schema_unsupported")
    if entry.get("profile_version") != PROFILE_VERSION:
        issues.append(prefix + "_profile_unsupported")
    if not identifier(entry.get("case_id")):
        issues.append(prefix + "_case_id_invalid")
    repository = entry.get("repository_full_name")
    if not isinstance(repository, str) or REPOSITORY.fullmatch(repository) is None:
        issues.append(prefix + "_repository_invalid")
    if not digest_value(entry.get("issue_digest")):
        issues.append(prefix + "_issue_digest_invalid")
    if not isinstance(entry.get("source_commit_sha"), str) or SHA40.fullmatch(
        entry["source_commit_sha"]
    ) is None:
        issues.append(prefix + "_source_commit_invalid")
    if natural(entry.get("observed_epoch")) is None:
        issues.append(prefix + "_observed_epoch_invalid")
    if entry.get("split") not in SPLITS:
        issues.append(prefix + "_split_invalid")
    if entry.get("scenario_class") not in SCENARIO_CLASSES:
        issues.append(prefix + "_scenario_class_invalid")
    for field in (
        "replay_case_digest", "environment_digest",
        "provider_configuration_digest", "evaluation_protocol_digest",
    ):
        if not digest_value(entry.get(field)):
            issues.append(prefix + "_digest_invalid:" + field)
    for field in (
        "labels_available_to_candidate_generation", "used_for_threshold_tuning",
        "used_for_memory_training", "used_for_prompt_selection",
        "used_for_model_selection",
    ):
        if not isinstance(entry.get(field), bool):
            issues.append(prefix + "_boolean_invalid:" + field)
    if entry.get(ENTRY_DIGEST_FIELD) != digest_without(entry, ENTRY_DIGEST_FIELD):
        issues.append(prefix + "_digest_mismatch")
    return issues


def validate_corpus(corpus: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(corpus, CORPUS_FIELDS, "corpus")
    if issues:
        return issues
    if corpus.get("schema_version") != SCHEMA_VERSION:
        issues.append("corpus_schema_unsupported")
    if corpus.get("profile_version") != PROFILE_VERSION:
        issues.append("corpus_profile_unsupported")
    if not identifier(corpus.get("corpus_id")):
        issues.append("corpus_id_invalid")
    repository = corpus.get("repository_full_name")
    if not isinstance(repository, str) or REPOSITORY.fullmatch(repository) is None:
        issues.append("corpus_repository_invalid")
    if not isinstance(corpus.get("cutoff_commit_sha"), str) or SHA40.fullmatch(
        corpus["cutoff_commit_sha"]
    ) is None:
        issues.append("corpus_cutoff_commit_invalid")
    for field in (
        "cutoff_epoch", "development_window_start_epoch",
        "development_window_end_epoch", "holdout_window_start_epoch",
        "holdout_window_end_epoch", "development_case_count", "holdout_case_count",
    ):
        if natural(corpus.get(field), positive=field.endswith("_case_count")) is None:
            issues.append("corpus_nat_invalid:" + field)
    for field in (
        "environment_digest", "provider_configuration_digest",
        "evaluation_protocol_digest",
    ):
        if not digest_value(corpus.get(field)):
            issues.append("corpus_digest_invalid:" + field)
    for field in (
        "content_addressed", "temporal_split_frozen",
        "holdout_hidden_from_candidate_generation",
        "holdout_excluded_from_threshold_tuning",
        "holdout_excluded_from_memory_training",
        "holdout_excluded_from_prompt_selection",
        "holdout_excluded_from_model_selection",
    ):
        if not isinstance(corpus.get(field), bool):
            issues.append("corpus_boolean_invalid:" + field)
    scenario_classes = unique_strings(corpus.get("scenario_classes"), nonempty=True)
    if scenario_classes is None or any(
        scenario not in SCENARIO_CLASSES for scenario in (scenario_classes or ())
    ):
        issues.append("corpus_scenario_classes_invalid")

    entries_raw = corpus.get("entries")
    if not isinstance(entries_raw, list) or not entries_raw:
        issues.append("corpus_entries_invalid")
        entries: list[Mapping[str, Any]] = []
    else:
        entries = []
        for index, raw in enumerate(entries_raw):
            mapped = mapping(raw)
            if mapped is None:
                issues.append(f"entry:{index}_not_mapping")
            else:
                entries.append(mapped)
                issues.extend(validate_entry(mapped, index=index))

    entry_digests = unique_strings(corpus.get("entry_digests"), nonempty=True)
    development_digests = unique_strings(
        corpus.get("development_entry_digests"), nonempty=True
    )
    holdout_digests = unique_strings(corpus.get("holdout_entry_digests"), nonempty=True)
    for name, values in (
        ("entry_digests", entry_digests),
        ("development_entry_digests", development_digests),
        ("holdout_entry_digests", holdout_digests),
    ):
        if values is None or any(not digest_value(item) for item in (values or ())):
            issues.append("corpus_" + name + "_invalid")

    if entries and not issues:
        actual_all = tuple(entry[ENTRY_DIGEST_FIELD] for entry in entries)
        actual_development = tuple(
            entry[ENTRY_DIGEST_FIELD]
            for entry in entries
            if entry["split"] == SPLIT_DEVELOPMENT
        )
        actual_holdout = tuple(
            entry[ENTRY_DIGEST_FIELD]
            for entry in entries
            if entry["split"] == SPLIT_HOLDOUT
        )
        if entry_digests != actual_all:
            issues.append("corpus_entry_digest_order_mismatch")
        if development_digests != actual_development:
            issues.append("corpus_development_digest_order_mismatch")
        if holdout_digests != actual_holdout:
            issues.append("corpus_holdout_digest_order_mismatch")
        if corpus["development_case_count"] != len(actual_development):
            issues.append("corpus_development_case_count_mismatch")
        if corpus["holdout_case_count"] != len(actual_holdout):
            issues.append("corpus_holdout_case_count_mismatch")
        if corpus["scenario_classes"] != sorted(
            {entry["scenario_class"] for entry in entries}
        ):
            issues.append("corpus_scenario_class_projection_mismatch")
        for entry in entries:
            if entry["repository_full_name"] != corpus["repository_full_name"]:
                issues.append("corpus_entry_repository_mismatch:" + entry["case_id"])
            for field in (
                "environment_digest", "provider_configuration_digest",
                "evaluation_protocol_digest",
            ):
                if entry[field] != corpus[field]:
                    issues.append("corpus_entry_uniform_binding_mismatch:" + field)
    if corpus.get(CORPUS_DIGEST_FIELD) != digest_without(corpus, CORPUS_DIGEST_FIELD):
        issues.append("corpus_digest_mismatch")
    return issues


def validate_request(request: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(request, REQUEST_FIELDS, "request")
    if issues:
        return issues
    if request.get("schema_version") != SCHEMA_VERSION:
        issues.append("request_schema_unsupported")
    if request.get("profile_version") != PROFILE_VERSION:
        issues.append("request_profile_unsupported")
    for field in ("corpus_id", "evaluator_id"):
        if not identifier(request.get(field)):
            issues.append("request_identifier_invalid:" + field)
    repository = request.get("repository_full_name")
    if not isinstance(repository, str) or REPOSITORY.fullmatch(repository) is None:
        issues.append("request_repository_invalid")
    if not digest_value(request.get("corpus_digest")):
        issues.append("request_corpus_digest_invalid")
    if natural(request.get("request_created_epoch")) is None:
        issues.append("request_epoch_invalid")
    if request.get("seal_temporal_holdout_corpus") is not True:
        issues.append("request_sealing_not_requested")
    if request.get(REQUEST_DIGEST_FIELD) != digest_without(request, REQUEST_DIGEST_FIELD):
        issues.append("request_digest_mismatch")
    return issues


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(policy, POLICY_FIELDS, "policy")
    if issues:
        return issues
    if policy.get("schema_version") != SCHEMA_VERSION:
        issues.append("policy_schema_unsupported")
    if policy.get("profile_version") != PROFILE_VERSION:
        issues.append("policy_profile_unsupported")
    repository = policy.get("expected_repository_full_name")
    if not isinstance(repository, str) or REPOSITORY.fullmatch(repository) is None:
        issues.append("policy_repository_invalid")
    if not digest_value(policy.get("expected_corpus_digest")):
        issues.append("policy_corpus_digest_invalid")
    evaluators = unique_strings(policy.get("authorized_evaluator_ids"), nonempty=True)
    if evaluators is None or any(not identifier(item) for item in (evaluators or ())):
        issues.append("policy_authorized_evaluators_invalid")
    for field in (
        "evaluation_epoch", "maximum_request_age",
        "minimum_development_cases", "minimum_holdout_cases",
    ):
        if natural(policy.get(field), positive=True) is None:
            issues.append("policy_positive_integer_invalid:" + field)
    scenarios = unique_strings(policy.get("required_scenario_classes"), nonempty=True)
    if scenarios is None or any(
        scenario not in SCENARIO_CLASSES for scenario in (scenarios or ())
    ):
        issues.append("policy_required_scenario_classes_invalid")
    for field in (
        "require_temporal_order", "require_distinct_case_ids_across_splits",
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
        "allow_read_only_corpus_sealing",
    ):
        if policy.get(field) is not True:
            issues.append("policy_required_true:" + field)
    for field in (
        "allow_historical_code_reexecution", "allow_provider_invocation",
        "allow_verification_runner_invocation", "allow_repository_mutation",
        "allow_git_effect", "allow_network_access", "allow_secret_read",
        "allow_selection_authority", "allow_successor_authority",
    ):
        if policy.get(field) is not False:
            issues.append("policy_required_false:" + field)
    if policy.get(POLICY_DIGEST_FIELD) != digest_without(policy, POLICY_DIGEST_FIELD):
        issues.append("policy_digest_mismatch")
    return issues


__all__ = ["validate_entry", "validate_corpus", "validate_request", "validate_policy"]
