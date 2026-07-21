from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_subtask_level_version_bound_memory_schema_v0_1 import *
from runtime.kuuos_codeai_subtask_level_version_bound_memory_schema_v0_1 import _validate_binding


def binding_mismatches(entry: Mapping[str, Any], query: Mapping[str, Any]) -> list[str]:
    return [field for field in VERSION_BINDING_FIELDS if entry.get(field) != query.get(field)]


def validate_entry(entry: Mapping[str, Any], index: int) -> list[str]:
    required = {
        "schema_version", "profile_version", "entry_id", "entry_revision",
        *VERSION_BINDING_FIELDS, "outcome", "evidence_created_epoch",
        "subtask_summary", "input_artifact_digest", "output_artifact_digest",
        "verification_evidence_digest", "derived_from_holdout",
        "superseded", "repository_mutation_performed", "candidate_selected",
        "repair_executed", "execution_authority_granted", "git_authority_granted",
        "correctness_claimed", "future_success_claimed", ENTRY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(entry)
    extra = set(entry).difference(required)
    prefix = f"entry:{index}:"
    if missing:
        issues.append(prefix + "missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if entry["schema_version"] != SCHEMA_VERSION or entry["profile_version"] != PROFILE_VERSION:
        issues.append(prefix + "profile_invalid")
    for field in ("entry_id", "entry_revision"):
        if not isinstance(entry[field], str) or IDENTIFIER.fullmatch(entry[field]) is None:
            issues.append(prefix + "identifier_invalid:" + field)
    issues.extend(prefix + item for item in _validate_binding(entry, "binding"))
    if entry["outcome"] not in OUTCOMES:
        issues.append(prefix + "outcome_invalid")
    if not nonnegative_int(entry["evidence_created_epoch"]):
        issues.append(prefix + "epoch_invalid")
    if not isinstance(entry["subtask_summary"], str) or not entry["subtask_summary"]:
        issues.append(prefix + "summary_invalid")
    for field in ("input_artifact_digest", "output_artifact_digest", "verification_evidence_digest"):
        if not isinstance(entry[field], str) or SHA256.fullmatch(entry[field]) is None:
            issues.append(prefix + "artifact_digest_invalid:" + field)
    for field in (
        "derived_from_holdout", "superseded", "repository_mutation_performed",
        "candidate_selected", "repair_executed", "execution_authority_granted",
        "git_authority_granted", "correctness_claimed", "future_success_claimed",
    ):
        if not isinstance(entry[field], bool):
            issues.append(prefix + "boolean_invalid:" + field)
    if not digest_ok(entry, ENTRY_DIGEST_FIELD):
        issues.append(prefix + "digest_mismatch")
    return sorted(set(issues))


def validate_corpus(corpus: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", "corpus_id", "corpus_revision",
        "repository_full_name", "temporal_corpus_digest", "context_pack_digest",
        "verifier_ensemble_digest", "entries", CORPUS_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(corpus)
    extra = set(corpus).difference(required)
    if missing:
        issues.append("corpus_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("corpus_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if corpus["schema_version"] != SCHEMA_VERSION or corpus["profile_version"] != PROFILE_VERSION:
        issues.append("corpus_profile_invalid")
    for field in ("corpus_id", "corpus_revision"):
        if not isinstance(corpus[field], str) or IDENTIFIER.fullmatch(corpus[field]) is None:
            issues.append("corpus_identifier_invalid:" + field)
    if not isinstance(corpus["repository_full_name"], str) or not corpus["repository_full_name"]:
        issues.append("corpus_repository_invalid")
    for field in ("temporal_corpus_digest", "context_pack_digest", "verifier_ensemble_digest"):
        if not isinstance(corpus[field], str) or SHA256.fullmatch(corpus[field]) is None:
            issues.append("corpus_digest_invalid:" + field)
    entries = corpus.get("entries")
    if not isinstance(entries, list):
        issues.append("corpus_entries_invalid")
    else:
        ids: list[str] = []
        digests: list[str] = []
        for index, item in enumerate(entries):
            if not isinstance(item, Mapping):
                issues.append(f"entry:{index}:not_mapping")
                continue
            issues.extend(validate_entry(item, index))
            ids.append(str(item.get("entry_id", "")))
            digests.append(str(item.get(ENTRY_DIGEST_FIELD, "")))
        if len(ids) != len(set(ids)):
            issues.append("corpus_entry_ids_not_unique")
        if len(digests) != len(set(digests)):
            issues.append("corpus_entry_digests_not_unique")
        kinds = {str(item.get("subtask_kind")) for item in entries if isinstance(item, Mapping)}
        if kinds != set(SUBTASK_KINDS):
            issues.append("corpus_subtask_coverage_incomplete")
    if not digest_ok(corpus, CORPUS_DIGEST_FIELD):
        issues.append("corpus_digest_mismatch")
    return sorted(set(issues))


__all__ = ["binding_mismatches", "validate_corpus", "validate_entry"]
