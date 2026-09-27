#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from runtime.kuuos_runtime_observability_mcp_multiplexer_v7_1 import (
    AUTHORITY_READY,
    BLOCKED,
    INGESTED,
    PREPARED,
    UNAVAILABLE,
    build_observability_mcp_multiplexer,
)

PLAN = "observability_mcp_multiplexer_plan_v7_1.json"
REQUEST = "observability_mcp_connector_request_v7_1.json"
RAW = "observability_mcp_raw_result_v7_1.json"
NORMALIZED = "observability_mcp_normalized_observation_v7_1.json"
RECEIPT = "observability_mcp_multiplexer_receipt_v7_1.json"


def sha(value: Any) -> str:
    import hashlib

    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def auth() -> dict[str, Any]:
    return {
        "authority_status": AUTHORITY_READY,
        "plan_read_allowed": True,
        "request_write_allowed": True,
        "raw_result_read_allowed": True,
        "normalized_observation_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path, stage: str) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "stage": stage,
        "observability_mcp_multiplexer_enabled": True,
        "apply_observability_mcp_multiplexer": True,
    }


def base_plan(provider: str, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_mcp_multiplexer_plan_v7_1",
        "provider": provider,
        "operation": operation,
        "connector_payload": payload,
        "read_only": True,
        "persist_raw_result": False,
        "source_authority_transfer_allowed": False,
        "max_summary_fields": 24,
    }


def write_plan(root: pathlib.Path, value: dict[str, Any]) -> None:
    (root / PLAN).write_text(json.dumps(value), encoding="utf-8")


def test_github_prepare() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_plan(
            root,
            base_plan(
                "github_actions",
                "workflow_job_logs",
                {"repo_full_name": "itakura-hidetoshi/KuuOS", "job_id": 123},
            ),
        )
        result = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "prepare"),
            authority_packet=auth(),
        )
        assert result.status == PREPARED, result.to_dict()
        assert result.request_emitted is True
        request = json.loads((root / REQUEST).read_text())
        assert request["connector_action"] == "GitHub.fetch_workflow_job_logs"
        assert request["boundary"]["read_only"] is True
        assert request["boundary"]["does_not_call_connector_inside_runtime"] is True


def test_vercel_prepare_and_ingest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_plan(
            root,
            base_plan(
                "vercel",
                "runtime_logs",
                {
                    "projectId": "prj_test",
                    "teamId": "team_test",
                    "environment": "production",
                    "level": ["error"],
                    "limit": 50,
                },
            ),
        )
        prepared = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "prepare"),
            authority_packet=auth(),
        )
        assert prepared.status == PREPARED, prepared.to_dict()
        request = json.loads((root / REQUEST).read_text())
        assert request["connector_action"] == "Vercel.get_runtime_logs"

        secret_marker = "DO_NOT_PERSIST_RAW_LOG_PAYLOAD"
        raw = {
            "version": "host_connector_result_v0",
            "provider": "vercel",
            "operation": "runtime_logs",
            "source_request_digest": sha(request),
            "connector_result": {
                "logs": [
                    {
                        "timestamp": "2026-09-27T11:00:00Z",
                        "level": "error",
                        "message": secret_marker,
                    },
                    {
                        "timestamp": "2026-09-27T11:01:00Z",
                        "level": "info",
                        "message": "recovered",
                    },
                ]
            },
        }
        (root / RAW).write_text(json.dumps(raw), encoding="utf-8")

        ingested = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "ingest"),
            authority_packet=auth(),
        )
        assert ingested.status == INGESTED, ingested.to_dict()
        normalized_text = (root / NORMALIZED).read_text()
        assert secret_marker not in normalized_text
        normalized = json.loads(normalized_text)
        assert normalized["provider"] == "vercel"
        assert normalized["shape_summary"]["item_count"] == 2
        assert normalized["shape_summary"]["error_signal_count"] >= 1
        assert normalized["raw_result_persisted"] is False
        receipt_text = (root / RECEIPT).read_text()
        assert secret_marker not in receipt_text


def test_supabase_read_only_sql() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_plan(
            root,
            base_plan(
                "supabase",
                "query_logs",
                {
                    "project_id": "project",
                    "sql": "DELETE FROM logs",
                },
            ),
        )
        result = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "prepare"),
            authority_packet=auth(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "supabase_sql_not_read_only_query" in result.blockers
        assert "supabase_sql_forbidden_keyword" in result.blockers
        assert not (root / REQUEST).exists()


def test_neon_query_shape() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_plan(
            root,
            base_plan(
                "neon",
                "query_logs",
                {
                    "branch_id": "br-test",
                    "logql": "{service_name=\"api\"}",
                    "minimum_severity": "error",
                },
            ),
        )
        result = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "prepare"),
            authority_packet=auth(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "neon_logql_and_structured_filters_mutually_exclusive" in result.blockers


def test_datadog_optional_unavailable() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_plan(
            root,
            base_plan("datadog", "logs", {"query": "service:kuuos"}),
        )
        result = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "prepare"),
            authority_packet=auth(),
        )
        assert result.status == UNAVAILABLE, result.to_dict()
        assert result.request_emitted is False
        assert result.blockers == []
        assert "optional_provider_requires_runtime_connection_and_region_compatibility" in result.warnings


def test_stale_result_rejected() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_plan(
            root,
            base_plan(
                "github_actions",
                "workflow_job_logs",
                {"repo_full_name": "itakura-hidetoshi/KuuOS", "job_id": 123},
            ),
        )
        prepared = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "prepare"),
            authority_packet=auth(),
        )
        assert prepared.status == PREPARED
        raw = {
            "provider": "github_actions",
            "operation": "workflow_job_logs",
            "source_request_digest": "0" * 64,
            "connector_result": {"content": "stale"},
        }
        (root / RAW).write_text(json.dumps(raw), encoding="utf-8")
        result = build_observability_mcp_multiplexer(
            runtime_context=ctx(root, "ingest"),
            authority_packet=auth(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "raw_result_source_request_digest_mismatch" in result.blockers
        assert not (root / NORMALIZED).exists()


def main() -> int:
    test_github_prepare()
    test_vercel_prepare_and_ingest()
    test_supabase_read_only_sql()
    test_neon_query_shape()
    test_datadog_optional_unavailable()
    test_stale_result_rejected()
    print("PASS: KuuOS Observability MCP Multiplexer v7.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
