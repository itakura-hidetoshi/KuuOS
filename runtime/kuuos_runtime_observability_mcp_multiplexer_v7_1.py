#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_observability_mcp_multiplexer_v7_1"
PLAN_VERSION = "kuuos_observability_mcp_multiplexer_plan_v7_1"
AUTHORITY_READY = "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_AUTHORITY_READY"
PREPARED = "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_PREPARED"
INGESTED = "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED"
UNAVAILABLE = "KUUOS_OBSERVABILITY_MCP_PROVIDER_UNAVAILABLE"
BLOCKED = "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_BLOCKED"

READ_ONLY_SQL_START = re.compile(r"^\s*(select|with)\b", re.IGNORECASE)
FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy|attach|detach|system|optimize)\b",
    re.IGNORECASE,
)

PROVIDER_OPERATIONS: dict[str, dict[str, dict[str, Any]]] = {
    "github_actions": {
        "workflow_job_logs": {
            "connector_action": "GitHub.fetch_workflow_job_logs",
            "required": ("repo_full_name", "job_id"),
            "polling_policy": "bounded_polling_allowed",
            "data_class": "ci_logs",
        },
    },
    "vercel": {
        "runtime_logs": {
            "connector_action": "Vercel.get_runtime_logs",
            "required": ("projectId", "teamId"),
            "polling_policy": "bounded_polling_allowed",
            "data_class": "runtime_logs",
        },
        "runtime_errors": {
            "connector_action": "Vercel.get_runtime_errors",
            "required": ("projectId", "teamId"),
            "polling_policy": "one_shot_preferred",
            "data_class": "error_clusters",
        },
        "deployment_build_logs": {
            "connector_action": "Vercel.get_deployment_build_logs",
            "required": ("idOrUrl", "teamId"),
            "polling_policy": "bounded_polling_allowed",
            "data_class": "build_logs",
        },
    },
    "supabase": {
        "query_logs": {
            "connector_action": "Supabase.query_logs",
            "required": ("project_id", "sql"),
            "polling_policy": "one_shot_only",
            "data_class": "unified_logs",
        },
    },
    "neon": {
        "query_logs": {
            "connector_action": "Neon.query_logs",
            "required": ("branch_id",),
            "polling_policy": "bounded_polling_allowed",
            "data_class": "branch_logs",
        },
    },
}

OPTIONAL_UNROUTED_PROVIDERS = {
    "datadog": {
        "reason": "optional_provider_requires_runtime_connection_and_region_compatibility",
        "authority_inferred": False,
    },
}


@dataclass(frozen=True)
class ObservabilityMCPMultiplexerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    stage: str
    provider: str
    operation: str
    connector_action: str
    request_path: str
    raw_result_path: str
    normalized_observation_path: str
    receipt_path: str
    audit_path: str
    request_emitted: bool
    normalized_observation_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _provider_spec(provider: str, operation: str) -> Mapping[str, Any]:
    return _m(_m(PROVIDER_OPERATIONS.get(provider)).get(operation))


def _validate_common_plan(plan: Mapping[str, Any], blockers: list[str]) -> tuple[str, str]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("persist_raw_result") is not False:
        blockers.append("persist_raw_result_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    provider = str(plan.get("provider", "")).strip()
    operation = str(plan.get("operation", "")).strip()
    if not provider:
        blockers.append("provider_missing")
    if not operation:
        blockers.append("operation_missing")
    return provider, operation


def _require_payload_fields(
    payload: Mapping[str, Any],
    required: tuple[str, ...],
    blockers: list[str],
) -> None:
    for field in required:
        value = payload.get(field)
        if value is None or value == "":
            blockers.append(f"connector_payload_{field}_missing")


def _validate_github_payload(payload: Mapping[str, Any], blockers: list[str]) -> None:
    repo = str(payload.get("repo_full_name", ""))
    if repo.count("/") != 1:
        blockers.append("github_repo_full_name_invalid")
    if _i(payload.get("job_id"), 0) <= 0:
        blockers.append("github_job_id_invalid")


def _validate_vercel_payload(
    operation: str,
    payload: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if operation in {"runtime_logs", "deployment_build_logs"}:
        limit = _i(payload.get("limit"), 50 if operation == "runtime_logs" else 100)
        if limit < 1 or limit > 100:
            blockers.append("vercel_limit_out_of_bounds")
    if operation == "runtime_logs":
        level = payload.get("level")
        if level is not None and (
            not isinstance(level, list)
            or any(str(x) not in {"error", "warning", "info", "fatal"} for x in level)
        ):
            blockers.append("vercel_level_invalid")
    if operation == "deployment_build_logs":
        direction = payload.get("direction")
        if direction is not None and direction not in {"tail", "head"}:
            blockers.append("vercel_direction_invalid")


def _validate_supabase_payload(payload: Mapping[str, Any], blockers: list[str]) -> None:
    sql = str(payload.get("sql", ""))
    if not READ_ONLY_SQL_START.search(sql):
        blockers.append("supabase_sql_not_read_only_query")
    if FORBIDDEN_SQL.search(sql):
        blockers.append("supabase_sql_forbidden_keyword")
    stripped = sql.strip().rstrip(";")
    if ";" in stripped:
        blockers.append("supabase_sql_multiple_statements_forbidden")


def _validate_neon_payload(payload: Mapping[str, Any], blockers: list[str]) -> None:
    limit = _i(payload.get("limit"), 100)
    if limit < 1 or limit > 1000:
        blockers.append("neon_limit_out_of_bounds")
    if payload.get("since") and payload.get("start_time"):
        blockers.append("neon_since_and_start_time_mutually_exclusive")
    structured_filters = {
        "source",
        "service_name",
        "scope_name",
        "minimum_severity",
        "severity_text",
        "body_contains",
        "trace_id",
    }
    if payload.get("logql") and any(payload.get(k) not in (None, "") for k in structured_filters):
        blockers.append("neon_logql_and_structured_filters_mutually_exclusive")


def _validate_payload(
    provider: str,
    operation: str,
    payload: Mapping[str, Any],
    blockers: list[str],
) -> None:
    spec = _provider_spec(provider, operation)
    required = tuple(str(x) for x in spec.get("required", ()))
    _require_payload_fields(payload, required, blockers)
    if provider == "github_actions":
        _validate_github_payload(payload, blockers)
    elif provider == "vercel":
        _validate_vercel_payload(operation, payload, blockers)
    elif provider == "supabase":
        _validate_supabase_payload(payload, blockers)
    elif provider == "neon":
        _validate_neon_payload(payload, blockers)


def _known_item_list(value: Any) -> list[Any] | None:
    if isinstance(value, list):
        return value
    if not isinstance(value, Mapping):
        return None
    for key in (
        "logs",
        "errors",
        "events",
        "results",
        "rows",
        "items",
        "data",
        "records",
    ):
        candidate = value.get(key)
        if isinstance(candidate, list):
            return candidate
    result = value.get("result")
    if isinstance(result, list):
        return result
    if isinstance(result, Mapping):
        nested = _known_item_list(result)
        if nested is not None:
            return nested
    return None


def _string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _signal_count(value: Any) -> int:
    count = 0
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in {"error", "fatal"} and child not in (None, False, "", 0, [], {}):
                count += 1
            if lowered in {"level", "severity", "severity_text", "status", "conclusion"}:
                text = str(child).lower()
                if text in {
                    "error",
                    "fatal",
                    "failure",
                    "failed",
                    "cancelled",
                    "timed_out",
                    "action_required",
                }:
                    count += 1
            count += _signal_count(child)
    elif isinstance(value, list):
        for child in value:
            count += _signal_count(child)
    return count


def _timestamp_hints(value: Any) -> tuple[str, str]:
    found: list[str] = []
    keys = {
        "timestamp",
        "time",
        "datetime",
        "created_at",
        "updated_at",
        "first_seen",
        "last_seen",
        "started_at",
        "finished_at",
    }

    def walk(node: Any, depth: int = 0) -> None:
        if depth > 4 or len(found) >= 64:
            return
        if isinstance(node, Mapping):
            for key, child in node.items():
                if str(key).lower() in keys and isinstance(child, str) and child:
                    found.append(child)
                walk(child, depth + 1)
        elif isinstance(node, list):
            for child in node[:64]:
                walk(child, depth + 1)

    walk(value)
    if not found:
        return "", ""
    return min(found), max(found)


def _shape_summary(value: Any, max_fields: int) -> dict[str, Any]:
    if isinstance(value, Mapping):
        keys = sorted(str(k) for k in value.keys())
        kind = "object"
    elif isinstance(value, list):
        keys = []
        kind = "array"
    elif isinstance(value, str):
        keys = []
        kind = "string"
    else:
        keys = []
        kind = type(value).__name__

    items = _known_item_list(value)
    first_ts, last_ts = _timestamp_hints(value)
    return {
        "result_kind": kind,
        "top_level_keys": keys[:max_fields],
        "top_level_key_count": len(keys),
        "item_count": len(items) if items is not None else None,
        "error_signal_count": _signal_count(value),
        "first_timestamp_hint": first_ts,
        "last_timestamp_hint": last_ts,
    }


def _prepare_request(
    plan: Mapping[str, Any],
    provider: str,
    operation: str,
) -> dict[str, Any]:
    spec = _provider_spec(provider, operation)
    payload = dict(_m(plan.get("connector_payload")))
    return {
        "version": "kuuos_observability_mcp_connector_request_v7_1",
        "provider": provider,
        "operation": operation,
        "connector_action": str(spec.get("connector_action", "")),
        "connector_payload": payload,
        "polling_policy": str(spec.get("polling_policy", "unknown")),
        "data_class": str(spec.get("data_class", "unknown")),
        "source_plan_digest": _sha(dict(plan)),
        "result_expected_file": "observability_mcp_raw_result_v7_1.json",
        "boundary": {
            "read_only": True,
            "dispatch_packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "source_authority_transferred": False,
            "raw_result_persistence_requested": False,
        },
        "epoch": int(time.time()),
    }


def _connector_error_classification(
    raw: Mapping[str, Any],
    provider: str,
) -> tuple[str, str, bool]:
    error = _m(raw.get("connector_error"))
    if not error:
        return "", "", False

    status_code = _i(error.get("status_code"), _i(error.get("status"), 0))
    code = str(error.get("code", "")).lower()
    reason = str(error.get("reason", "")).lower()
    message = str(error.get("message", "")).lower()
    combined = " ".join((code, reason, message))

    if provider == "neon" and "telemetry_not_enabled" in combined:
        return "neon_telemetry_not_enabled", UNAVAILABLE, False
    if status_code == 404 and (
        "blobnotfound" in combined
        or "blob not found" in combined
        or "log blob" in combined
    ):
        return "log_not_yet_materialized", TRANSIENT, True
    if status_code == 429:
        return "provider_rate_limited", TRANSIENT, True
    if status_code >= 500:
        return "provider_server_unavailable", TRANSIENT, True
    return "connector_error_unclassified", BLOCKED, False


def _normalize_result(
    request: Mapping[str, Any],
    raw: Mapping[str, Any],
    *,
    max_fields: int,
) -> dict[str, Any]:
    result = raw.get("connector_result")
    if result is None:
        result = raw.get("result")
    if result is None:
        result = {}
    return {
        "version": "kuuos_observability_mcp_normalized_observation_v7_1",
        "observation_result_allowed": True,
        "provider": str(request.get("provider", "")),
        "operation": str(request.get("operation", "")),
        "connector_action": str(request.get("connector_action", "")),
        "polling_policy": str(request.get("polling_policy", "")),
        "data_class": str(request.get("data_class", "")),
        "source_request_digest": _sha(dict(request)),
        "source_raw_result_digest": _sha(dict(raw)),
        "observed_value_digest": _sha(result),
        "shape_summary": _shape_summary(result, max_fields),
        "raw_result_persisted": False,
        "source_authority_transferred": False,
        "epoch": int(time.time()),
    }


def build_observability_mcp_multiplexer(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityMCPMultiplexerResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_mcp_multiplexer_plan_v7_1.json"
    request_path = root / "observability_mcp_connector_request_v7_1.json"
    raw_result_path = root / "observability_mcp_raw_result_v7_1.json"
    normalized_path = root / "observability_mcp_normalized_observation_v7_1.json"
    receipt_path = root / "observability_mcp_multiplexer_receipt_v7_1.json"
    audit_path = root / "observability_mcp_multiplexer_audit_v7_1.jsonl"

    if ctx.get("observability_mcp_multiplexer_enabled") is not True:
        blockers.append("observability_mcp_multiplexer_enabled_not_true")
    if ctx.get("apply_observability_mcp_multiplexer") is not True:
        blockers.append("apply_observability_mcp_multiplexer_not_true")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("observability_mcp_multiplexer_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "request_write_allowed",
        "raw_result_read_allowed",
        "normalized_observation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    stage = str(ctx.get("stage", "prepare"))
    if stage not in {"prepare", "ingest"}:
        blockers.append("stage_invalid")

    plan = _read_json(plan_path)
    if not plan:
        blockers.append("observability_plan_missing_or_invalid")
        provider = ""
        operation = ""
    else:
        provider, operation = _validate_common_plan(plan, blockers)

    connector_action = ""
    request_emitted = False
    normalized_written = False
    request: dict[str, Any] = {}
    normalized: dict[str, Any] = {}
    connector_obstruction = ""
    connector_retryable = False

    if provider in OPTIONAL_UNROUTED_PROVIDERS:
        warnings.append(str(OPTIONAL_UNROUTED_PROVIDERS[provider]["reason"]))
        status = UNAVAILABLE
    else:
        if provider and provider not in PROVIDER_OPERATIONS:
            blockers.append("provider_not_allowlisted")
        if provider in PROVIDER_OPERATIONS and operation not in PROVIDER_OPERATIONS[provider]:
            blockers.append("operation_not_allowlisted_for_provider")

        spec = _provider_spec(provider, operation)
        connector_action = str(spec.get("connector_action", ""))
        payload = _m(plan.get("connector_payload")) if plan else {}
        if spec:
            _validate_payload(provider, operation, payload, blockers)

        max_fields = _i(plan.get("max_summary_fields"), 24) if plan else 24
        if max_fields < 1 or max_fields > 64:
            blockers.append("max_summary_fields_out_of_bounds")

        if not blockers and stage == "prepare":
            request = _prepare_request(plan, provider, operation)
            _write_json(request_path, request)
            request_emitted = True
            status = PREPARED
        elif not blockers and stage == "ingest":
            request = _read_json(request_path)
            raw = _read_json(raw_result_path)
            if not request:
                blockers.append("observability_connector_request_missing_or_invalid")
            if not raw:
                blockers.append("observability_raw_result_missing_or_invalid")
            if request:
                if str(request.get("provider", "")) != provider:
                    blockers.append("request_provider_mismatch")
                if str(request.get("operation", "")) != operation:
                    blockers.append("request_operation_mismatch")
                if str(request.get("connector_action", "")) != connector_action:
                    blockers.append("request_connector_action_mismatch")
            if raw and request:
                expected_digest = _sha(dict(request))
                source_digest = str(raw.get("source_request_digest", ""))
                if source_digest != expected_digest:
                    blockers.append("raw_result_source_request_digest_mismatch")
                if str(raw.get("provider", "")) != provider:
                    blockers.append("raw_result_provider_mismatch")
                if str(raw.get("operation", "")) != operation:
                    blockers.append("raw_result_operation_mismatch")
            if not blockers:
                (
                    connector_obstruction,
                    connector_error_status,
                    connector_retryable,
                ) = _connector_error_classification(raw, provider)
                if connector_obstruction:
                    if connector_error_status == BLOCKED:
                        blockers.append(connector_obstruction)
                        status = BLOCKED
                    else:
                        warnings.append(connector_obstruction)
                        status = connector_error_status
                else:
                    normalized = _normalize_result(
                        request,
                        raw,
                        max_fields=max_fields,
                    )
                    _write_json(normalized_path, normalized)
                    normalized_written = True
                    status = INGESTED
            else:
                status = BLOCKED
        else:
            status = BLOCKED

    packet_id = "kuuos-observability-mcp-" + _sha(
        {
            "stage": stage,
            "plan": plan,
            "request": request,
            "normalized": normalized,
            "blockers": sorted(set(blockers)),
            "warnings": warnings,
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "stage": stage,
        "provider": provider,
        "operation": operation,
        "connector_action": connector_action,
        "request_emitted": request_emitted,
        "request_digest": _sha(request),
        "normalized_observation_written": normalized_written,
        "normalized_observation_digest": _sha(normalized),
        "connector_obstruction": connector_obstruction,
        "connector_retryable": connector_retryable,
        "raw_result_persisted_by_multiplexer": False,
        "source_authority_transferred": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return ObservabilityMCPMultiplexerResult(
        VERSION,
        status,
        packet_id,
        str(root),
        stage,
        provider,
        operation,
        connector_action,
        str(request_path),
        str(raw_result_path),
        str(normalized_path),
        str(receipt_path),
        str(audit_path),
        request_emitted,
        normalized_written,
        sorted(set(blockers)),
        warnings,
    )
