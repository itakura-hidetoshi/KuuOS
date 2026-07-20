#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Callable, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import RESUME_INPUT_DIGEST_FIELD
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1 import (
    DISPOSITION_CONSUMED as SOURCE_DISPOSITION_CONSUMED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    EXECUTION_INPUT_DIGEST_FIELD,
    EXECUTION_INPUT_PROFILE_VERSION,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as SOURCE_REGISTRY_DIGEST_FIELD,
    _validate_registry as _validate_source_registry,
    _validate_resume_input,
    canonical_digest,
    digest_without,
)
from runtime.kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    EVIDENCE_DIGEST_FIELD as INNER_EVIDENCE_DIGEST_FIELD,
    LIFECYCLE_RECEIPT_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as INNER_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as INNER_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as INNER_REQUEST_DIGEST_FIELD,
    STATUS_READY as INNER_STATUS_READY,
    build_codeai_bounded_autonomous_git_lifecycle_loop_orchestration,
)

VERSION = "kuuos_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Durable Git Lifecycle Loop Resumption Execution v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
DISPOSITION_EXECUTED = "durable_git_lifecycle_loop_resumption_executed"
REQUEST_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_execution_request_digest"
POLICY_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_execution_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_execution_registry_digest"
EVIDENCE_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_execution_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_execution_receipt_digest"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.:/-]+$")

EXECUTION_INPUT_FIELDS = {
    "schema_version", "profile_version", "execution_input_id",
    "source_resumption_receipt_digest", "source_resumption_evidence_digest",
    "source_resumption_registry_digest", "source_resume_input_digest", "checkpoint_id",
    "checkpoint_envelope_digest", "loop_id", "lifecycle_id", "repository_full_name",
    "prior_loop_disposition", "prior_effect_count", "prior_maximum_effect_count",
    "resume_effect_budget", "resume_execution_command_budget", "resume_execution_output_bytes",
    "issued_epoch", "one_shot", "reusable", "active_now", "loop_execution_authorized",
    "direct_git_effect_authorized", "automatic_execution_authorized",
    "network_access_authorized", "secret_material_read_authorized",
    "general_git_authority_granted", "general_successor_stage_authority_granted",
    EXECUTION_INPUT_DIGEST_FIELD,
}
REQUEST_FIELDS = {
    "execution_session_id", "invocation_nonce_digest", "source_consumption_receipt_digest",
    "source_consumption_evidence_digest", "source_consumption_registry_digest",
    "source_execution_input_digest", "source_resume_input_digest", "loop_id", "lifecycle_id",
    "repository_full_name", "executor_id", "request_created_epoch", "consume_execution_input",
    "invoke_bounded_loop", "source_correspondence_confirmed", REQUEST_DIGEST_FIELD,
}
POLICY_FIELDS = {
    "expected_source_consumption_receipt_digest", "expected_source_consumption_evidence_digest",
    "expected_source_consumption_registry_digest", "expected_source_execution_input_digest",
    "expected_source_resume_input_digest", "expected_repository_full_name",
    "authorized_executor_ids", "maximum_request_age", "maximum_registry_entries",
    "maximum_effect_count", "maximum_total_command_count", "maximum_total_output_bytes",
    "evaluation_epoch", "allow_execution_input_consumption", "allow_bounded_loop_invocation",
    "require_one_shot", "require_active_input", "require_existing_lifecycle_effect_chain",
    "allow_direct_git_effect", "allow_automatic_execution", "allow_unbounded_execution",
    "allow_network_access_outside_orchestrator", "allow_secret_material_read",
    "allow_general_successor_authority", POLICY_DIGEST_FIELD,
}
REGISTRY_FIELDS = {
    "registry_id", "registry_revision", "consumed_invocation_nonce_digests",
    "consumed_execution_input_digests", "emitted_loop_receipt_digests",
    "successful_execution_count", "last_execution_epoch", REGISTRY_DIGEST_FIELD,
}

@dataclass(frozen=True)
class CodeAIDurableGitLifecycleLoopResumptionExecutionResult:
    status: str
    issues: tuple[str, ...]
    loop_result: Any | None
    evidence: dict[str, Any] | None
    next_registry: dict[str, Any] | None
    receipt: dict[str, Any] | None

BoundedLoopOrchestrator = Callable[..., Any]

def _mapping(v: Any) -> Mapping[str, Any] | None:
    return v if isinstance(v, Mapping) else None

def _nat(v: Any, *, positive: bool = False) -> int | None:
    return v if isinstance(v, int) and not isinstance(v, bool) and v >= (1 if positive else 0) else None

def _strings(v: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    if not isinstance(v, list) or not all(isinstance(x, str) and x for x in v):
        return None
    out = tuple(v)
    return out if len(out) == len(set(out)) and (out or not nonempty) else None

def _exact(v: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    missing, extra = fields - set(v), set(v) - fields
    return ([prefix + "_missing_fields:" + ",".join(sorted(missing))] if missing else []) + ([prefix + "_extra_fields:" + ",".join(sorted(extra))] if extra else [])

def _digest_ok(v: Mapping[str, Any], field: str) -> bool:
    return v.get(field) == digest_without(v, field)

def _validate_source_receipt(v: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not _digest_ok(v, SOURCE_RECEIPT_DIGEST_FIELD): issues.append("source_consumption_receipt_digest_mismatch")
    if v.get("profile_version") != SOURCE_PROFILE_VERSION: issues.append("source_consumption_receipt_profile_unsupported")
    if v.get("codeai_disposition") != SOURCE_DISPOSITION_CONSUMED: issues.append("source_consumption_receipt_disposition_invalid")
    for f in ("route_receipt_recorded", "source_resumption_bundle_verified", "source_resume_input_verified", "consumption_nonce_consumed", "consumption_registry_advanced_once", "resume_input_consumed", "execution_input_issued", "execution_input_one_shot", "execution_input_active", "loop_execution_authorized_for_successor"):
        if v.get(f) is not True: issues.append("source_consumption_receipt_required_true:" + f)
    for f in ("execution_input_reusable", "direct_git_effect_authorized", "automatic_execution_authorized", "loop_execution_performed", "git_effect_performed", "automatic_resumption_performed", "network_accessed", "secret_material_read", "general_git_authority_granted", "general_successor_stage_authority_granted"):
        if v.get(f) is not False: issues.append("source_consumption_receipt_required_false:" + f)
    return issues

def _validate_source_evidence(v: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not _digest_ok(v, SOURCE_EVIDENCE_DIGEST_FIELD): issues.append("source_consumption_evidence_digest_mismatch")
    for f in ("source_correspondence_verified", "resume_input_consumed", "execution_input_issued", "execution_input_active"):
        if v.get(f) is not True: issues.append("source_consumption_evidence_required_true:" + f)
    for f in ("loop_execution_performed", "git_effect_performed", "automatic_resumption_performed", "network_accessed", "secret_material_read"):
        if v.get(f) is not False: issues.append("source_consumption_evidence_required_false:" + f)
    return issues

def _validate_execution_input(v: Mapping[str, Any]) -> list[str]:
    issues = _exact(v, EXECUTION_INPUT_FIELDS, "execution_input")
    if issues: return issues
    if not _digest_ok(v, EXECUTION_INPUT_DIGEST_FIELD): issues.append("execution_input_digest_mismatch")
    if v.get("profile_version") != EXECUTION_INPUT_PROFILE_VERSION: issues.append("execution_input_profile_unsupported")
    for f in ("execution_input_id", "checkpoint_id", "loop_id", "lifecycle_id"):
        if not isinstance(v.get(f), str) or not _IDENTIFIER.fullmatch(v[f]): issues.append("execution_input_invalid_identifier:" + f)
    if not isinstance(v.get("repository_full_name"), str) or not _REPOSITORY.fullmatch(v["repository_full_name"]): issues.append("execution_input_invalid_repository")
    for f in ("source_resumption_receipt_digest", "source_resumption_evidence_digest", "source_resumption_registry_digest", "source_resume_input_digest", "checkpoint_envelope_digest"):
        if not isinstance(v.get(f), str) or not _SHA256.fullmatch(v[f]): issues.append("execution_input_invalid_digest:" + f)
    for f in ("prior_effect_count", "prior_maximum_effect_count", "resume_effect_budget", "resume_execution_command_budget", "resume_execution_output_bytes", "issued_epoch"):
        if _nat(v.get(f), positive=f in {"resume_effect_budget", "resume_execution_command_budget", "resume_execution_output_bytes"}) is None: issues.append("execution_input_invalid_nat:" + f)
    required = ("one_shot", "active_now", "loop_execution_authorized")
    forbidden = ("reusable", "direct_git_effect_authorized", "automatic_execution_authorized", "network_access_authorized", "secret_material_read_authorized", "general_git_authority_granted", "general_successor_stage_authority_granted")
    for f in required:
        if v.get(f) is not True: issues.append("execution_input_required_true:" + f)
    for f in forbidden:
        if v.get(f) is not False: issues.append("execution_input_required_false:" + f)
    return issues

def _validate_request(v: Mapping[str, Any]) -> list[str]:
    issues = _exact(v, REQUEST_FIELDS, "resumption_execution_request")
    if issues: return issues
    for f in REQUEST_FIELDS - {"request_created_epoch", "consume_execution_input", "invoke_bounded_loop", "source_correspondence_confirmed", REQUEST_DIGEST_FIELD}:
        if not isinstance(v.get(f), str) or not v[f]: issues.append("resumption_execution_request_invalid_string:" + f)
    for f in ("invocation_nonce_digest", "source_consumption_receipt_digest", "source_consumption_evidence_digest", "source_consumption_registry_digest", "source_execution_input_digest", "source_resume_input_digest"):
        if not _SHA256.fullmatch(v[f]): issues.append("resumption_execution_request_invalid_digest:" + f)
    if _nat(v.get("request_created_epoch")) is None: issues.append("resumption_execution_request_invalid_epoch")
    if not _digest_ok(v, REQUEST_DIGEST_FIELD): issues.append("resumption_execution_request_digest_mismatch")
    return issues

def _validate_policy(v: Mapping[str, Any]) -> list[str]:
    issues = _exact(v, POLICY_FIELDS, "resumption_execution_policy")
    if issues: return issues
    for f in ("expected_source_consumption_receipt_digest", "expected_source_consumption_evidence_digest", "expected_source_consumption_registry_digest", "expected_source_execution_input_digest", "expected_source_resume_input_digest"):
        if not isinstance(v.get(f), str) or not _SHA256.fullmatch(v[f]): issues.append("resumption_execution_policy_invalid_digest:" + f)
    if not isinstance(v.get("expected_repository_full_name"), str) or not _REPOSITORY.fullmatch(v["expected_repository_full_name"]): issues.append("resumption_execution_policy_invalid_repository")
    executors = _strings(v.get("authorized_executor_ids"), nonempty=True)
    if executors is None: issues.append("resumption_execution_policy_invalid_executors")
    for f in ("maximum_request_age", "maximum_registry_entries", "maximum_effect_count", "maximum_total_command_count", "maximum_total_output_bytes", "evaluation_epoch"):
        if _nat(v.get(f), positive=f != "evaluation_epoch") is None: issues.append("resumption_execution_policy_invalid_nat:" + f)
    if not _digest_ok(v, POLICY_DIGEST_FIELD): issues.append("resumption_execution_policy_digest_mismatch")
    return issues

def _validate_registry(v: Mapping[str, Any]) -> list[str]:
    issues = _exact(v, REGISTRY_FIELDS, "resumption_execution_registry")
    if issues: return issues
    for f in ("registry_revision", "successful_execution_count", "last_execution_epoch"):
        if _nat(v.get(f)) is None: issues.append("resumption_execution_registry_invalid_nat:" + f)
    histories = [_strings(v.get(f)) for f in ("consumed_invocation_nonce_digests", "consumed_execution_input_digests", "emitted_loop_receipt_digests")]
    if any(h is None for h in histories): issues.append("resumption_execution_registry_invalid_history")
    elif len({len(h or ()) for h in histories}) != 1: issues.append("resumption_execution_registry_parallel_history_mismatch")
    elif v["registry_revision"] != len(histories[0] or ()) or v["successful_execution_count"] != len(histories[0] or ()): issues.append("resumption_execution_registry_count_mismatch")
    if not _digest_ok(v, REGISTRY_DIGEST_FIELD): issues.append("resumption_execution_registry_digest_mismatch")
    return issues

def _source_correspondence(*, source_receipt: Mapping[str, Any], source_evidence: Mapping[str, Any], source_registry: Mapping[str, Any], resume_input: Mapping[str, Any], execution_input: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any], initial_lifecycle_receipt: Mapping[str, Any], loop_request: Mapping[str, Any], loop_policy: Mapping[str, Any]) -> bool:
    return (
        source_receipt["consumption_evidence_digest"] == source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
        and source_receipt["next_consumption_registry_digest"] == source_registry[SOURCE_REGISTRY_DIGEST_FIELD]
        and source_receipt["source_resume_input_digest"] == resume_input[RESUME_INPUT_DIGEST_FIELD]
        and source_receipt["execution_input_digest"] == execution_input[EXECUTION_INPUT_DIGEST_FIELD]
        and source_evidence["source_resume_input_digest"] == resume_input[RESUME_INPUT_DIGEST_FIELD]
        and source_evidence["next_consumption_registry_digest"] == source_registry[SOURCE_REGISTRY_DIGEST_FIELD]
        and source_evidence["execution_input_digest"] == execution_input[EXECUTION_INPUT_DIGEST_FIELD]
        and execution_input[EXECUTION_INPUT_DIGEST_FIELD] in source_registry["issued_execution_input_digests"]
        and resume_input[RESUME_INPUT_DIGEST_FIELD] in source_registry["consumed_resume_input_digests"]
        and execution_input["source_resume_input_digest"] == resume_input[RESUME_INPUT_DIGEST_FIELD]
        and request["source_consumption_receipt_digest"] == source_receipt[SOURCE_RECEIPT_DIGEST_FIELD]
        and request["source_consumption_evidence_digest"] == source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
        and request["source_consumption_registry_digest"] == source_registry[SOURCE_REGISTRY_DIGEST_FIELD]
        and request["source_execution_input_digest"] == execution_input[EXECUTION_INPUT_DIGEST_FIELD]
        and request["source_resume_input_digest"] == resume_input[RESUME_INPUT_DIGEST_FIELD]
        and request["loop_id"] == execution_input["loop_id"] == resume_input["loop_id"] == loop_request["loop_id"]
        and request["lifecycle_id"] == execution_input["lifecycle_id"] == resume_input["lifecycle_id"] == loop_request["lifecycle_id"]
        and request["repository_full_name"] == execution_input["repository_full_name"] == resume_input["repository_full_name"] == loop_request["repository_full_name"]
        and policy["expected_source_consumption_receipt_digest"] == source_receipt[SOURCE_RECEIPT_DIGEST_FIELD]
        and policy["expected_source_consumption_evidence_digest"] == source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
        and policy["expected_source_consumption_registry_digest"] == source_registry[SOURCE_REGISTRY_DIGEST_FIELD]
        and policy["expected_source_execution_input_digest"] == execution_input[EXECUTION_INPUT_DIGEST_FIELD]
        and policy["expected_source_resume_input_digest"] == resume_input[RESUME_INPUT_DIGEST_FIELD]
        and policy["expected_repository_full_name"] == execution_input["repository_full_name"]
        and request["executor_id"] in policy["authorized_executor_ids"]
        and initial_lifecycle_receipt.get(LIFECYCLE_RECEIPT_DIGEST_FIELD) == resume_input["final_lifecycle_receipt_digest"]
        and _digest_ok(loop_request, INNER_REQUEST_DIGEST_FIELD)
        and _digest_ok(loop_policy, INNER_POLICY_DIGEST_FIELD)
    )

def _policy_safe(request: Mapping[str, Any], policy: Mapping[str, Any], active: Mapping[str, Any], inner_request: Mapping[str, Any], inner_policy: Mapping[str, Any]) -> bool:
    required = (policy["allow_execution_input_consumption"], policy["allow_bounded_loop_invocation"], policy["require_one_shot"], policy["require_active_input"], policy["require_existing_lifecycle_effect_chain"])
    forbidden = (policy["allow_direct_git_effect"], policy["allow_automatic_execution"], policy["allow_unbounded_execution"], policy["allow_network_access_outside_orchestrator"], policy["allow_secret_material_read"], policy["allow_general_successor_authority"])
    command_total = inner_policy.get("maximum_total_execution_command_count", 0) + inner_policy.get("maximum_total_reobservation_command_count", 0)
    output_total = inner_policy.get("maximum_total_execution_output_bytes", 0) + inner_policy.get("maximum_total_reobservation_output_bytes", 0)
    effects = inner_request.get("requested_max_effect_count", 0)
    return (
        all(required) and not any(forbidden)
        and request["consume_execution_input"] is True and request["invoke_bounded_loop"] is True and request["source_correspondence_confirmed"] is True
        and active["one_shot"] is True and active["reusable"] is False and active["active_now"] is True and active["loop_execution_authorized"] is True
        and active["direct_git_effect_authorized"] is False and active["automatic_execution_authorized"] is False and active["general_git_authority_granted"] is False
        and _nat(effects, positive=True) is not None and effects <= active["resume_effect_budget"] and effects <= policy["maximum_effect_count"]
        and _nat(command_total, positive=True) is not None and command_total <= active["resume_execution_command_budget"] and command_total <= policy["maximum_total_command_count"]
        and _nat(output_total, positive=True) is not None and output_total <= active["resume_execution_output_bytes"] and output_total <= policy["maximum_total_output_bytes"]
    )

def _fresh_and_replay_closed(request: Mapping[str, Any], policy: Mapping[str, Any], registry: Mapping[str, Any]) -> bool:
    age = policy["evaluation_epoch"] - request["request_created_epoch"]
    return 0 <= age <= policy["maximum_request_age"] and request["invocation_nonce_digest"] not in registry["consumed_invocation_nonce_digests"] and request["source_execution_input_digest"] not in registry["consumed_execution_input_digests"] and len(registry["consumed_invocation_nonce_digests"]) < policy["maximum_registry_entries"]

def _next_registry(registry: Mapping[str, Any], *, request: Mapping[str, Any], loop_receipt_digest: str, epoch: int) -> dict[str, Any]:
    out = dict(registry)
    out["registry_revision"] += 1
    out["consumed_invocation_nonce_digests"] = [*out["consumed_invocation_nonce_digests"], request["invocation_nonce_digest"]]
    out["consumed_execution_input_digests"] = [*out["consumed_execution_input_digests"], request["source_execution_input_digest"]]
    out["emitted_loop_receipt_digests"] = [*out["emitted_loop_receipt_digests"], loop_receipt_digest]
    out["successful_execution_count"] += 1
    out["last_execution_epoch"] = epoch
    out.pop(REGISTRY_DIGEST_FIELD, None)
    out[REGISTRY_DIGEST_FIELD] = canonical_digest(out)
    return out

def build_codeai_durable_git_lifecycle_loop_resumption_execution(*, consumption_receipt: Any, consumption_evidence: Any, consumption_registry: Any, source_resume_input: Any, execution_input: Any, execution_request: Any, execution_policy: Any, execution_registry: Any, source_trajectory_receipt: Any, initial_lifecycle_receipt: Any, loop_request: Any, loop_policy: Any, loop_registry: Any, inner_execution_registry: Any, reobservation_registry: Any, continuation_registry: Any, execution_adapter: Any, reobservation_adapter: Any, orchestrator: BoundedLoopOrchestrator = build_codeai_bounded_autonomous_git_lifecycle_loop_orchestration) -> CodeAIDurableGitLifecycleLoopResumptionExecutionResult:
    source_receipt, source_evidence, source_registry = map(_mapping, (consumption_receipt, consumption_evidence, consumption_registry))
    resume_input, active, request, policy, registry = map(_mapping, (source_resume_input, execution_input, execution_request, execution_policy, execution_registry))
    lifecycle, inner_request, inner_policy = map(_mapping, (initial_lifecycle_receipt, loop_request, loop_policy))
    issues: list[str] = []
    named = ((source_receipt,"consumption_receipt"),(source_evidence,"consumption_evidence"),(source_registry,"consumption_registry"),(resume_input,"source_resume_input"),(active,"execution_input"),(request,"execution_request"),(policy,"execution_policy"),(registry,"execution_registry"),(lifecycle,"initial_lifecycle_receipt"),(inner_request,"loop_request"),(inner_policy,"loop_policy"))
    issues += [name + "_not_mapping" for value, name in named if value is None]
    if source_receipt is not None: issues += _validate_source_receipt(source_receipt)
    if source_evidence is not None: issues += _validate_source_evidence(source_evidence)
    if source_registry is not None: issues += _validate_source_registry(source_registry)
    if resume_input is not None: issues += _validate_resume_input(resume_input)
    if active is not None: issues += _validate_execution_input(active)
    if request is not None: issues += _validate_request(request)
    if policy is not None: issues += _validate_policy(policy)
    if registry is not None: issues += _validate_registry(registry)
    if issues or any(v is None for v, _ in named): return CodeAIDurableGitLifecycleLoopResumptionExecutionResult(STATUS_BLOCKED, tuple(issues), None, None, None, None)
    assert source_receipt is not None and source_evidence is not None and source_registry is not None and resume_input is not None and active is not None and request is not None and policy is not None and registry is not None and lifecycle is not None and inner_request is not None and inner_policy is not None
    if not _source_correspondence(source_receipt=source_receipt, source_evidence=source_evidence, source_registry=source_registry, resume_input=resume_input, execution_input=active, request=request, policy=policy, initial_lifecycle_receipt=lifecycle, loop_request=inner_request, loop_policy=inner_policy): issues.append("resumption_execution_source_correspondence_mismatch")
    if not _policy_safe(request, policy, active, inner_request, inner_policy): issues.append("resumption_execution_policy_not_safe")
    if not _fresh_and_replay_closed(request, policy, registry): issues.append("resumption_execution_freshness_capacity_or_replay_violation")
    if issues: return CodeAIDurableGitLifecycleLoopResumptionExecutionResult(STATUS_BLOCKED, tuple(issues), None, None, None, None)
    loop_result = orchestrator(source_trajectory_receipt=source_trajectory_receipt, initial_lifecycle_receipt=initial_lifecycle_receipt, loop_request=loop_request, loop_policy=loop_policy, loop_registry=loop_registry, execution_registry=inner_execution_registry, reobservation_registry=reobservation_registry, continuation_registry=continuation_registry, execution_adapter=execution_adapter, reobservation_adapter=reobservation_adapter)
    if getattr(loop_result, "status", None) != INNER_STATUS_READY or getattr(loop_result, "receipt", None) is None or getattr(loop_result, "evidence", None) is None:
        inner_issues = tuple("bounded_loop:" + str(x) for x in getattr(loop_result, "issues", ())) or ("bounded_loop:not_ready_or_missing_receipt",)
        return CodeAIDurableGitLifecycleLoopResumptionExecutionResult(STATUS_BLOCKED, inner_issues, loop_result, None, None, None)
    loop_receipt, loop_evidence = loop_result.receipt, loop_result.evidence
    loop_digest = loop_receipt[INNER_RECEIPT_DIGEST_FIELD]
    next_registry = _next_registry(registry, request=request, loop_receipt_digest=loop_digest, epoch=policy["evaluation_epoch"])
    effects = loop_receipt.get("effect_count", loop_receipt.get("total_effect_count", 0))
    effects = effects if isinstance(effects, int) and effects >= 0 else 0
    common = {
        "source_consumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_consumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_consumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
        "source_resume_input_digest": resume_input[RESUME_INPUT_DIGEST_FIELD],
        "source_execution_input_digest": active[EXECUTION_INPUT_DIGEST_FIELD],
        "execution_request_digest": request[REQUEST_DIGEST_FIELD], "execution_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_execution_registry_digest": registry[REGISTRY_DIGEST_FIELD], "next_execution_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
    }
    evidence = {"schema_version": SCHEMA_VERSION, "profile_version": PROFILE_VERSION, **common,
        "bounded_loop_request_digest": inner_request[INNER_REQUEST_DIGEST_FIELD], "bounded_loop_policy_digest": inner_policy[INNER_POLICY_DIGEST_FIELD],
        "bounded_loop_evidence_digest": loop_evidence[INNER_EVIDENCE_DIGEST_FIELD], "bounded_loop_receipt_digest": loop_digest,
        "source_correspondence_verified": True, "execution_input_consumed": True, "invocation_nonce_consumed": True,
        "bounded_loop_invoked_once": True, "existing_lifecycle_effect_chain_enforced": True, "direct_git_effect_performed": False,
        "delegated_git_effect_count": effects, "automatic_execution_performed": False, "network_accessed_outside_orchestrator": False, "secret_material_read": False}
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)
    receipt = {"schema_version": SCHEMA_VERSION, "profile_version": PROFILE_VERSION, **common, "execution_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "bounded_loop_receipt_digest": loop_digest, "bounded_loop_disposition": loop_receipt.get("codeai_disposition", "unknown"),
        "checkpoint_id": active["checkpoint_id"], "checkpoint_envelope_digest": active["checkpoint_envelope_digest"], "loop_id": active["loop_id"], "lifecycle_id": active["lifecycle_id"], "repository_full_name": active["repository_full_name"],
        "codeai_disposition": DISPOSITION_EXECUTED, "operating_mode": "durable_git_lifecycle_loop_resumption_execution", "route_receipt_recorded": True,
        "source_consumption_bundle_verified": True, "source_resume_input_verified": True, "active_execution_input_verified": True,
        "execution_input_consumed": True, "invocation_nonce_consumed": True, "execution_registry_advanced_once": True,
        "bounded_loop_invoked_once": True, "loop_execution_performed": True, "existing_lifecycle_effect_chain_enforced": True,
        "direct_git_effect_performed": False, "delegated_git_effect_count": effects, "automatic_execution_performed": False,
        "network_accessed_outside_orchestrator": False, "secret_material_read": False, "general_git_authority_granted": False, "general_successor_stage_authority_granted": False}
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIDurableGitLifecycleLoopResumptionExecutionResult(STATUS_READY, (), loop_result, evidence, next_registry, receipt)

__all__ = ["VERSION", "SCHEMA_VERSION", "PROFILE_VERSION", "STATUS_READY", "STATUS_BLOCKED", "DISPOSITION_EXECUTED", "REQUEST_DIGEST_FIELD", "POLICY_DIGEST_FIELD", "REGISTRY_DIGEST_FIELD", "EVIDENCE_DIGEST_FIELD", "RECEIPT_DIGEST_FIELD", "CodeAIDurableGitLifecycleLoopResumptionExecutionResult", "build_codeai_durable_git_lifecycle_loop_resumption_execution"]
