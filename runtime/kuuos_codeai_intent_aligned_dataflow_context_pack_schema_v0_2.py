#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SCHEMA_VERSION = "v0.2"
PROFILE_VERSION = "CodeAI Intent-Aligned Dataflow Context Pack v0.2"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_CONTEXT_ONLY = "context_only"
DISPOSITION_BUILT = "intent_aligned_dataflow_context_pack_built"

SOURCE_RECEIPT_DIGEST_FIELD = "codeai_intent_repository_observation_receipt_digest"
REQUEST_DIGEST_FIELD = "codeai_intent_aligned_dataflow_context_request_digest"
HYPOTHESIS_DIGEST_FIELD = "hypothesis_digest"
POLICY_DIGEST_FIELD = "codeai_intent_aligned_dataflow_context_policy_digest"
PACK_DIGEST_FIELD = "codeai_intent_aligned_dataflow_context_pack_digest"
RECEIPT_DIGEST_FIELD = "codeai_intent_aligned_dataflow_context_receipt_digest"
QUERY_NODE_DIGEST_FIELD = "query_node_digest"
SELECTED_FILE_DIGEST_FIELD = "selected_file_evidence_digest"

HYPOTHESIS_FIELDS = {
    "hypothesis_id",
    "statement",
    "query_terms",
    "expected_symbols",
    HYPOTHESIS_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "request_id",
    "request_revision",
    "intent_text",
    "initial_query_terms",
    "candidate_hypotheses",
    "target_path_prefixes",
    "target_symbols",
    "required_roles",
    "request_created_epoch",
    "repository_snapshot_digest",
    "expected_source_observation_receipt_digest",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "allowed_repository_path_prefixes",
    "forbidden_repository_path_prefixes",
    "supported_file_suffixes",
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
    "evaluation_epoch",
    "allow_text_fallback",
    "require_dependency_path",
    "require_symbol_digest",
    "allow_repository_mutation",
    "allow_network_access",
    "allow_secret_access",
    "allow_candidate_selection_authority",
    "allow_execution_authority",
    POLICY_DIGEST_FIELD,
}

ALLOWED_ROLES = {"source", "test", "formal", "config", "workflow", "documentation"}
QUERY_STAGES = ("intent", "hypothesis", "symbol", "dependency", "dataflow")


@dataclass(frozen=True)
class CodeAIIntentAlignedDataflowContextResult:
    status: str
    issues: tuple[str, ...]
    context_pack: dict[str, Any] | None
    receipt: dict[str, Any] | None
