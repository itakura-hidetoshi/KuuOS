#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
from typing import Any

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from runtime.kuuos_runtime_observability_event_alignment_v7_3 import (
    BLOCKED,
    PARTIAL,
    READY,
    build_observability_event_alignment,
)

PLAN = "observability_event_alignment_plan_v7_3.json"
INPUT = "observability_event_alignment_input_v7_3.json"
TEMPORAL = "observability_temporal_correlation_packet_v7_2.json"
OUTPUT = "observability_event_alignment_packet_v7_3.json"


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def authority() -> dict[str, Any]:
    return {
        "authority_status": "KUUOS_OBSERVABILITY_EVENT_ALIGNMENT_AUTHORITY_READY",
        "plan_read_allowed": True,
        "input_read_allowed": True,
        "temporal_packet_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_event_alignment_enabled": True,
        "apply_observability_event_alignment": True,
    }


def plan() -> dict[str, Any]:
    return {
        "version": "kuuos_observability_event_alignment_plan_v7_3",
        "read_only": True,
        "causal_inference_allowed": False,
        "source_authority_transfer_allowed": False,
        "max_identity_bindings": 128,
    }


def temporal_packet(
    *,
    relation: str = "overlap",
    compatible: bool = True,
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_temporal_correlation_v7_2",
        "status": "KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_READY",
        "observations": [
            {
                "observation_id": "gh",
                "provider": "github_actions",
                "operation": "ci_logs",
                "source_digest": "a" * 64,
                "source_status": "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED",
                "availability": "observed",
                "window_start": "2026-09-27T11:00:00Z",
                "window_end": "2026-09-27T11:00:10Z",
            },
            {
                "observation_id": "deploy",
                "provider": "vercel",
                "operation": "runtime_logs",
                "source_digest": "b" * 64,
                "source_status": "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED",
                "availability": "observed",
                "window_start": "2026-09-27T11:00:05Z",
                "window_end": "2026-09-27T11:00:15Z",
            },
        ],
        "pairs": [
            {
                "left_observation_id": "gh",
                "right_observation_id": "deploy",
                "left_provider": "github_actions",
                "right_provider": "vercel",
                "relation": relation,
                "temporally_compatible": compatible,
                "gap_seconds": 0.0 if compatible else 50.0,
                "tolerance_seconds": 5,
                "reason": "test",
                "causal_claim": "not_inferred",
                "causal_claim_permitted": False,
            }
        ],
        "summary": {
            "observation_count": 2,
            "pair_count": 1,
        },
        "interpretation_boundary": {
            "temporal_compatibility_is_not_causation": True,
            "causal_inference_performed": False,
            "causal_claim_permitted": False,
            "source_authority_transferred": False,
            "raw_provider_payloads_present": False,
        },
    }


def alignment_input(
    temporal: dict[str, Any],
    *,
    gh_ids: dict[str, str],
    deploy_ids: dict[str, str],
) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_event_alignment_input_v7_3",
        "source_temporal_packet_digest": sha(temporal),
        "identity_bindings": [
            {"observation_id": "gh", "identifiers": gh_ids},
            {"observation_id": "deploy", "identifiers": deploy_ids},
        ],
    }


def write_case(
    root: pathlib.Path,
    temporal: dict[str, Any],
    alignment: dict[str, Any],
) -> None:
    (root / PLAN).write_text(json.dumps(plan()), encoding="utf-8")
    (root / TEMPORAL).write_text(json.dumps(temporal), encoding="utf-8")
    (root / INPUT).write_text(json.dumps(alignment), encoding="utf-8")


def test_shared_commit_temporally_compatible() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet()
        commit = "1" * 40
        alignment = alignment_input(
            temporal,
            gh_ids={"commit_sha": commit, "workflow_run_id": "123"},
            deploy_ids={"commit_sha": commit, "deployment_id": "dpl_example"},
        )
        write_case(root, temporal, alignment)
        result = build_observability_event_alignment(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.exact_context_compatible_count == 1
        out_text = (root / OUTPUT).read_text()
        assert commit not in out_text
        out = json.loads(out_text)
        pair = out["pairs"][0]
        assert pair["alignment_state"] == "exact_context_temporally_compatible"
        assert pair["has_shared_exact_identifier"] is True
        assert pair["shared_identifier_evidence"][0]["identifier_type"] == "commit_sha"
        assert pair["identity_values_exposed"] is False
        assert pair["causal_claim"] == "not_inferred"
        assert pair["causal_direction"] == "not_inferred"


def test_shared_request_but_temporally_disjoint_is_partial() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet(relation="disjoint", compatible=False)
        request_id = "req-sensitive-value"
        alignment = alignment_input(
            temporal,
            gh_ids={"request_id": request_id},
            deploy_ids={"request_id": request_id},
        )
        write_case(root, temporal, alignment)
        result = build_observability_event_alignment(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.exact_context_disjoint_count == 1
        out_text = (root / OUTPUT).read_text()
        assert request_id not in out_text
        pair = json.loads(out_text)["pairs"][0]
        assert pair["alignment_state"] == "exact_context_temporally_disjoint"
        assert pair["causal_claim_permitted"] is False


def test_temporal_only() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet()
        alignment = alignment_input(
            temporal,
            gh_ids={"workflow_run_id": "123"},
            deploy_ids={"deployment_id": "dpl_other"},
        )
        write_case(root, temporal, alignment)
        result = build_observability_event_alignment(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.temporal_only_count == 1
        out = json.loads((root / OUTPUT).read_text())
        assert out["pairs"][0]["alignment_state"] == "temporal_only"


def test_same_type_distinct_values_are_not_false_match() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet()
        alignment = alignment_input(
            temporal,
            gh_ids={"correlation_id": "corr-a"},
            deploy_ids={"correlation_id": "corr-b"},
        )
        write_case(root, temporal, alignment)
        result = build_observability_event_alignment(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        pair = out["pairs"][0]
        assert pair["has_shared_exact_identifier"] is False
        assert pair["same_type_distinct_value_identifiers"] == ["correlation_id"]
        assert pair["alignment_state"] == "temporal_only"


def test_stale_temporal_digest_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet()
        alignment = alignment_input(
            temporal,
            gh_ids={"workflow_run_id": "123"},
            deploy_ids={"deployment_id": "dpl"},
        )
        alignment["source_temporal_packet_digest"] = "0" * 64
        write_case(root, temporal, alignment)
        result = build_observability_event_alignment(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "source_temporal_packet_digest_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def test_invalid_commit_sha_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet()
        alignment = alignment_input(
            temporal,
            gh_ids={"commit_sha": "not-a-sha"},
            deploy_ids={"commit_sha": "not-a-sha"},
        )
        write_case(root, temporal, alignment)
        result = build_observability_event_alignment(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert any("commit_sha_invalid" in b for b in result.blockers)


def main() -> int:
    test_shared_commit_temporally_compatible()
    test_shared_request_but_temporally_disjoint_is_partial()
    test_temporal_only()
    test_same_type_distinct_values_are_not_false_match()
    test_stale_temporal_digest_blocks()
    test_invalid_commit_sha_blocks()
    print("PASS: KuuOS Observability Event Alignment v7.3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
