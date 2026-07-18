from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import GeneratedUnifiedDiffCandidate

VERSION = "kuuos_codeai_autonomous_structured_edit_synthesis_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Structured Edit Synthesis v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_PROPOSAL_ONLY = "proposal_only"
BOUNDARY_CANDIDATE = "CANDIDATE"
BOUNDARY_HOLD = "HOLD"
BOUNDARY_REPAIR = "REPAIR"
BOUNDARY_REJECT = "REJECT"
BOUNDARY_QUARANTINE = "QUARANTINE"
DISPOSITION_SYNTHESIZED = "autonomous_structured_edit_candidates_synthesized"
DISPOSITION_NO_CANDIDATE = "no_governed_structured_edit_candidate"
REQUEST_DIGEST_FIELD = "codeai_autonomous_structured_edit_synthesis_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_structured_edit_synthesis_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_structured_edit_synthesis_receipt_digest"

REQUEST_FIELDS = {
    "request_id", "request_revision", "intent_text", "candidate_count",
    "request_created_epoch", "requirement_trace_ids", "test_plan_ids",
    "risk_labels", "unresolved_candidate_questions", "prior_candidate_digests",
    "prior_producer_session_ids", REQUEST_DIGEST_FIELD,
}
POLICY_FIELDS = {
    "allowed_provider_ids", "maximum_provider_calls", "maximum_raw_output_bytes",
    "maximum_intent_bytes", "maximum_repository_snapshot_bytes",
    "maximum_proposals", "evaluation_epoch", "maximum_response_age",
    "maximum_request_age", "allowed_repository_path_prefixes",
    "forbidden_repository_path_prefixes", POLICY_DIGEST_FIELD,
}
RESPONSE_FIELDS = {
    "provider_response_id", "producer_session_id", "response_created_epoch",
    "raw_output", "claims_authority", "hides_uncertainty",
    "bypasses_governance", "evidence_missing",
}
RAW_PROPOSAL_FIELDS = {
    "proposal_id", "candidate_revision", "edits", "risk_labels",
    "unresolved_candidate_questions",
}


@dataclass(frozen=True)
class ProviderAdapter:
    adapter_id: str
    provider_id: str
    model_id: str
    generate: Callable[[Mapping[str, Any]], Any]


@dataclass(frozen=True)
class ProviderAttemptReceipt:
    adapter_id: str
    provider_id: str
    model_id: str
    prompt_digest: str
    response_digest: str = ""
    provider_response_id: str = ""
    producer_session_id: str = ""
    boundary_status: str = BOUNDARY_REJECT
    route_reason: str = ""
    raw_output_size_bytes: int = 0
    structured_proposal_id: str = ""
    raw_output_accepted: bool = False
    structured_proposal_produced: bool = False


@dataclass(frozen=True)
class CodeAIAutonomousStructuredEditSynthesisResult:
    status: str
    issues: tuple[str, ...]
    attempts: tuple[ProviderAttemptReceipt, ...]
    candidates: tuple[GeneratedUnifiedDiffCandidate, ...]
    receipt: dict[str, Any] | None


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def nat(value: Any, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value if not positive or value > 0 else None


def strings(value: Any, *, nonempty: bool = False) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    if len(value) != len(set(value)) or (nonempty and not value):
        return None
    return list(value)


def exact(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def digest_ok(value: Mapping[str, Any], field: str) -> bool:
    return value.get(field) == canonical_digest({k: v for k, v in value.items() if k != field})


def canonical_path(path: str) -> bool:
    parts = path.split("/")
    return (
        bool(path) and not path.startswith("/") and not path.endswith("/")
        and "\\" not in path and "\0" not in path and "\n" not in path
        and "\r" not in path and all(part not in ("", ".", "..") for part in parts)
    )


def canonical_text(value: Any) -> bool:
    return (
        isinstance(value, str) and "\0" not in value and "\r" not in value
        and (not value or value.endswith("\n"))
    )


def validate_repository(value: Any) -> tuple[Mapping[str, str] | None, list[str]]:
    repository = mapping(value)
    if repository is None:
        return None, ["repository_files_not_mapping"]
    issues: list[str] = []
    for path, content in repository.items():
        if not isinstance(path, str) or not canonical_path(path):
            issues.append("repository_file_path_invalid")
        if not canonical_text(content):
            issues.append("repository_file_content_invalid:" + str(path))
    return repository, issues


def validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = mapping(value)
    if request is None:
        return None, ["synthesis_request_not_mapping"]
    issues = exact(request, REQUEST_FIELDS, "synthesis_request")
    if issues:
        return request, issues
    for field in ("request_id", "request_revision", "intent_text"):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("synthesis_request_invalid_string:" + field)
    for field in (
        "requirement_trace_ids", "test_plan_ids", "risk_labels",
        "unresolved_candidate_questions", "prior_candidate_digests",
        "prior_producer_session_ids",
    ):
        if strings(request[field]) is None:
            issues.append("synthesis_request_invalid_string_list:" + field)
    if nat(request["candidate_count"], positive=True) is None:
        issues.append("synthesis_request_invalid_candidate_count")
    if nat(request["request_created_epoch"]) is None:
        issues.append("synthesis_request_invalid_created_epoch")
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("synthesis_request_digest_mismatch")
    return request, issues


def validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = mapping(value)
    if policy is None:
        return None, ["synthesis_policy_not_mapping"]
    issues = exact(policy, POLICY_FIELDS, "synthesis_policy")
    if issues:
        return policy, issues
    for field in (
        "maximum_provider_calls", "maximum_raw_output_bytes", "maximum_intent_bytes",
        "maximum_repository_snapshot_bytes", "maximum_proposals",
        "maximum_response_age", "maximum_request_age",
    ):
        if nat(policy[field], positive=True) is None:
            issues.append("synthesis_policy_invalid_positive_nat:" + field)
    if nat(policy["evaluation_epoch"]) is None:
        issues.append("synthesis_policy_invalid_evaluation_epoch")
    if strings(policy["allowed_provider_ids"], nonempty=True) is None:
        issues.append("synthesis_policy_invalid_allowed_provider_ids")
    for field in ("allowed_repository_path_prefixes", "forbidden_repository_path_prefixes"):
        if strings(policy[field], nonempty=(field == "allowed_repository_path_prefixes")) is None:
            issues.append("synthesis_policy_invalid_string_list:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("synthesis_policy_digest_mismatch")
    return policy, issues


def validate_adapters(value: Any) -> tuple[list[ProviderAdapter] | None, list[str]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
        return None, ["provider_adapters_not_nonempty_sequence"]
    issues: list[str] = []
    adapters: list[ProviderAdapter] = []
    ids: set[str] = set()
    for index, adapter in enumerate(value):
        prefix = f"provider_adapter[{index}]"
        if not isinstance(adapter, ProviderAdapter):
            issues.append(prefix + ":invalid_type")
            continue
        for field in ("adapter_id", "provider_id", "model_id"):
            if not isinstance(getattr(adapter, field), str) or not getattr(adapter, field):
                issues.append(prefix + ":invalid_string:" + field)
        if adapter.adapter_id in ids:
            issues.append(prefix + ":duplicate_adapter_id")
        ids.add(adapter.adapter_id)
        if not callable(adapter.generate):
            issues.append(prefix + ":generate_not_callable")
        adapters.append(adapter)
    return adapters, issues


def path_has_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/")
    return path == normalized or path.startswith(normalized + "/")


def repository_scope_issues(repository: Mapping[str, str], policy: Mapping[str, Any]) -> list[str]:
    allowed = policy["allowed_repository_path_prefixes"]
    forbidden = policy["forbidden_repository_path_prefixes"]
    issues: list[str] = []
    for path in repository:
        if not any(path_has_prefix(path, prefix) for prefix in allowed):
            issues.append("repository_path_not_allowed:" + path)
        if any(path_has_prefix(path, prefix) for prefix in forbidden):
            issues.append("repository_path_forbidden:" + path)
    return issues


def prompt_packet(request: Mapping[str, Any], repository: Mapping[str, str], adapter: ProviderAdapter, index: int) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_digest": request[REQUEST_DIGEST_FIELD],
        "request_id": request["request_id"],
        "request_revision": request["request_revision"],
        "intent_text": request["intent_text"],
        "repository_snapshot_digest": canonical_digest(repository),
        "repository_files": dict(sorted(repository.items())),
        "adapter_id": adapter.adapter_id,
        "provider_id": adapter.provider_id,
        "model_id": adapter.model_id,
        "attempt_index": index,
        "requested_candidate_count": request["candidate_count"],
        "output_contract": {
            "format": "json_object_only",
            "required_fields": sorted(RAW_PROPOSAL_FIELDS),
            "edit_operations": ["add", "modify", "delete"],
            "complete_new_content_required": True,
            "unified_diff_syntax_forbidden": True,
        },
        "provider_output_is_candidate_material_only": True,
        "selection_authority_granted": False,
        "execution_authority_granted": False,
    }
