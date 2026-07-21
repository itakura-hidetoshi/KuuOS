#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import PurePosixPath
from typing import Any, Mapping

from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_schema_v0_2 import (
    ALLOWED_ROLES,
    HYPOTHESIS_DIGEST_FIELD,
    HYPOTHESIS_FIELDS,
    POLICY_DIGEST_FIELD,
    POLICY_FIELDS,
    REQUEST_DIGEST_FIELD,
    REQUEST_FIELDS,
    SOURCE_RECEIPT_DIGEST_FIELD,
)

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    result[field] = canonical_digest(result)
    return result


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


def strings(value: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    parsed = tuple(value)
    if len(parsed) != len(set(parsed)) or (nonempty and not parsed):
        return None
    return parsed


def exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def canonical_path(path: Any) -> bool:
    if not isinstance(path, str) or not path or path.startswith("/") or path.endswith("/"):
        return False
    if any(char in path for char in ("\\", "\0", "\n", "\r")):
        return False
    return all(part not in ("", ".", "..") for part in path.split("/"))


def canonical_text(value: Any) -> bool:
    return isinstance(value, str) and "\0" not in value and "\r" not in value and (
        not value or value.endswith("\n")
    )


def path_has_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/")
    return path == normalized or path.startswith(normalized + "/")


def validate_source_receipt(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    required = (
        SOURCE_RECEIPT_DIGEST_FIELD,
        "codeai_disposition",
        "operating_mode",
        "repository_observation_read_only",
        "repository_mutation_performed",
        "repository_full_name",
        "source_commit_sha",
        "tree_digest",
    )
    for field in required:
        if field not in value:
            issues.append("source_observation_receipt_missing_field:" + field)
    if issues:
        return issues
    digest = value[SOURCE_RECEIPT_DIGEST_FIELD]
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        issues.append("source_observation_receipt_digest_invalid")
    elif digest != digest_without(value, SOURCE_RECEIPT_DIGEST_FIELD):
        issues.append("source_observation_receipt_digest_mismatch")
    if value["codeai_disposition"] != "intent_repository_observation_supported":
        issues.append("source_observation_receipt_not_supported")
    if value["operating_mode"] != "read_only" or value["repository_observation_read_only"] is not True:
        issues.append("source_observation_receipt_not_read_only")
    if value["repository_mutation_performed"] is not False:
        issues.append("source_observation_receipt_reports_mutation")
    if not isinstance(value["repository_full_name"], str) or not value["repository_full_name"]:
        issues.append("source_observation_receipt_repository_invalid")
    if not isinstance(value["source_commit_sha"], str) or not _SHA40.fullmatch(value["source_commit_sha"]):
        issues.append("source_observation_receipt_commit_invalid")
    if not isinstance(value["tree_digest"], str) or not _SHA256.fullmatch(value["tree_digest"]):
        issues.append("source_observation_receipt_tree_digest_invalid")
    return issues


def validate_hypothesis(value: Mapping[str, Any], index: int) -> list[str]:
    prefix = f"context_hypothesis_{index}"
    issues = exact_fields(value, HYPOTHESIS_FIELDS, prefix)
    if issues:
        return issues
    for field in ("hypothesis_id", "statement"):
        if not isinstance(value[field], str) or not value[field]:
            issues.append(prefix + "_invalid_string:" + field)
    for field in ("query_terms", "expected_symbols"):
        if strings(value[field], nonempty=(field == "query_terms")) is None:
            issues.append(prefix + "_invalid_string_list:" + field)
    digest = value[HYPOTHESIS_DIGEST_FIELD]
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        issues.append(prefix + "_digest_invalid")
    elif digest != digest_without(value, HYPOTHESIS_DIGEST_FIELD):
        issues.append(prefix + "_digest_mismatch")
    return issues


def validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(value, REQUEST_FIELDS, "context_request")
    if issues:
        return issues
    for field in ("request_id", "request_revision", "intent_text"):
        if not isinstance(value[field], str) or not value[field]:
            issues.append("context_request_invalid_string:" + field)
    for field in ("initial_query_terms", "target_path_prefixes", "target_symbols", "required_roles"):
        if strings(value[field], nonempty=(field == "initial_query_terms")) is None:
            issues.append("context_request_invalid_string_list:" + field)
    hypotheses = value["candidate_hypotheses"]
    if not isinstance(hypotheses, list) or not hypotheses:
        issues.append("context_request_invalid_hypotheses")
    else:
        hypothesis_ids: list[str] = []
        for index, item in enumerate(hypotheses):
            parsed = mapping(item)
            if parsed is None:
                issues.append(f"context_hypothesis_{index}_not_object")
                continue
            issues.extend(validate_hypothesis(parsed, index))
            if isinstance(parsed.get("hypothesis_id"), str):
                hypothesis_ids.append(parsed["hypothesis_id"])
        if len(hypothesis_ids) != len(set(hypothesis_ids)):
            issues.append("context_request_duplicate_hypothesis_id")
    if nat(value["request_created_epoch"]) is None:
        issues.append("context_request_invalid_created_epoch")
    for field in ("repository_snapshot_digest", "expected_source_observation_receipt_digest"):
        item = value[field]
        if not isinstance(item, str) or not _SHA256.fullmatch(item):
            issues.append("context_request_invalid_digest:" + field)
    if any(role not in ALLOWED_ROLES for role in value["required_roles"]):
        issues.append("context_request_invalid_required_role")
    if any(not canonical_path(prefix.rstrip("/")) for prefix in value["target_path_prefixes"]):
        issues.append("context_request_invalid_target_path_prefix")
    digest = value[REQUEST_DIGEST_FIELD]
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        issues.append("context_request_digest_invalid")
    elif digest != digest_without(value, REQUEST_DIGEST_FIELD):
        issues.append("context_request_digest_mismatch")
    return issues


def validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = exact_fields(value, POLICY_FIELDS, "context_policy")
    if issues:
        return issues
    for field in ("expected_repository_full_name", "expected_source_commit_sha"):
        if not isinstance(value[field], str) or not value[field]:
            issues.append("context_policy_invalid_string:" + field)
    if not _SHA40.fullmatch(value["expected_source_commit_sha"]):
        issues.append("context_policy_invalid_source_commit")
    for field in (
        "allowed_repository_path_prefixes",
        "forbidden_repository_path_prefixes",
        "supported_file_suffixes",
    ):
        if strings(value[field], nonempty=(field != "forbidden_repository_path_prefixes")) is None:
            issues.append("context_policy_invalid_string_list:" + field)
    for field in (
        "maximum_repository_snapshot_bytes",
        "maximum_candidate_files",
        "maximum_selected_files",
        "maximum_file_bytes",
        "maximum_excerpt_bytes",
        "maximum_total_context_bytes",
        "maximum_query_terms",
        "maximum_hypotheses",
        "maximum_dependency_depth",
        "minimum_intent_evidence_score",
        "maximum_request_age",
    ):
        if nat(value[field], positive=True) is None:
            issues.append("context_policy_invalid_positive_nat:" + field)
    if nat(value["evaluation_epoch"]) is None:
        issues.append("context_policy_invalid_evaluation_epoch")
    for field in (
        "allow_text_fallback",
        "require_dependency_path",
        "require_symbol_digest",
        "allow_repository_mutation",
        "allow_network_access",
        "allow_secret_access",
        "allow_candidate_selection_authority",
        "allow_execution_authority",
    ):
        if not isinstance(value[field], bool):
            issues.append("context_policy_invalid_bool:" + field)
    if any(not suffix.startswith(".") for suffix in value["supported_file_suffixes"]):
        issues.append("context_policy_invalid_supported_suffix")
    if any(not canonical_path(prefix.rstrip("/")) for prefix in value["allowed_repository_path_prefixes"]):
        issues.append("context_policy_invalid_allowed_prefix")
    if any(not canonical_path(prefix.rstrip("/")) for prefix in value["forbidden_repository_path_prefixes"]):
        issues.append("context_policy_invalid_forbidden_prefix")
    digest = value[POLICY_DIGEST_FIELD]
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        issues.append("context_policy_digest_invalid")
    elif digest != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("context_policy_digest_mismatch")
    return issues


def validate_repository(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    for path, content in value.items():
        if not canonical_path(path):
            issues.append("repository_file_path_invalid:" + str(path))
        if not canonical_text(content):
            issues.append("repository_file_content_invalid:" + str(path))
    return issues


def role_for_path(path: str) -> str:
    pure = PurePosixPath(path)
    suffix = pure.suffix.lower()
    parts = pure.parts
    name = pure.name.lower()
    if path.startswith(".github/workflows/"):
        return "workflow"
    if "tests" in parts or name.startswith("test_") or name.endswith("_test.py"):
        return "test"
    if "formal" in parts or suffix == ".lean":
        return "formal"
    if suffix in {".json", ".toml", ".yaml", ".yml"}:
        return "config"
    if suffix in {".md", ".rst", ".txt"}:
        return "documentation"
    return "source"


def language_for_path(path: str) -> str:
    return {
        ".py": "python",
        ".lean": "lean",
        ".json": "json",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".rst": "restructuredtext",
        ".txt": "text",
    }.get(PurePosixPath(path).suffix.lower(), "text")
