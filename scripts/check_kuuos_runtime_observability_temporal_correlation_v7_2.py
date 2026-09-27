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

from runtime.kuuos_runtime_observability_temporal_correlation_v7_2 import (
    BLOCKED,
    PARTIAL,
    READY,
    build_observability_temporal_correlation,
)

PLAN = "observability_temporal_correlation_plan_v7_2.json"
INPUT = "observability_temporal_correlation_input_v7_2.json"
OUTPUT = "observability_temporal_correlation_packet_v7_2.json"


def authority() -> dict[str, Any]:
    return {
        "authority_status": "KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_AUTHORITY_READY",
        "plan_read_allowed": True,
        "input_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_temporal_correlation_enabled": True,
        "apply_observability_temporal_correlation": True,
    }


def plan(tolerance: int = 5) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_temporal_correlation_plan_v7_2",
        "read_only": True,
        "causal_inference_allowed": False,
        "source_authority_transfer_allowed": False,
        "temporal_tolerance_seconds": tolerance,
        "max_observations": 32,
    }


def packet(observations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_temporal_correlation_input_v7_2",
        "observations": observations,
    }


def obs(
    oid: str,
    provider: str,
    start: str | None,
    end: str | None,
    *,
    status: str = "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED",
    digest_char: str = "a",
) -> dict[str, Any]:
    shape: dict[str, Any] = {}
    if start is not None:
        shape["first_timestamp_hint"] = start
    if end is not None:
        shape["last_timestamp_hint"] = end
    return {
        "observation_id": oid,
        "provider": provider,
        "operation": "logs",
        "status": status,
        "observed_value_digest": digest_char * 64,
        "shape_summary": shape,
    }


def write_case(
    root: pathlib.Path,
    observations: list[dict[str, Any]],
    *,
    tolerance: int = 5,
) -> None:
    (root / PLAN).write_text(json.dumps(plan(tolerance)), encoding="utf-8")
    (root / INPUT).write_text(json.dumps(packet(observations)), encoding="utf-8")


def test_overlap_and_disjoint() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_case(
            root,
            [
                obs("gh", "github_actions", "2026-09-27T11:00:00Z", "2026-09-27T11:00:10Z", digest_char="a"),
                obs("vercel", "vercel", "2026-09-27T11:00:08Z", "2026-09-27T11:00:20Z", digest_char="b"),
                obs("neon", "neon", "2026-09-27T11:01:00Z", "2026-09-27T11:01:05Z", digest_char="c"),
            ],
            tolerance=5,
        )
        result = build_observability_temporal_correlation(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.observation_count == 3
        assert result.pair_count == 3
        out = json.loads((root / OUTPUT).read_text())
        by_ids = {
            (p["left_observation_id"], p["right_observation_id"]): p
            for p in out["pairs"]
        }
        assert by_ids[("gh", "vercel")]["relation"] == "overlap"
        assert by_ids[("gh", "vercel")]["temporally_compatible"] is True
        assert by_ids[("gh", "neon")]["relation"] == "disjoint"
        assert by_ids[("vercel", "neon")]["relation"] == "disjoint"
        assert all(p["causal_claim"] == "not_inferred" for p in out["pairs"])
        assert out["interpretation_boundary"]["causal_inference_performed"] is False


def test_within_tolerance() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_case(
            root,
            [
                obs("a", "github_actions", "2026-09-27T11:00:00Z", "2026-09-27T11:00:10Z", digest_char="d"),
                obs("b", "vercel", "2026-09-27T11:00:14Z", "2026-09-27T11:00:20Z", digest_char="e"),
            ],
            tolerance=5,
        )
        result = build_observability_temporal_correlation(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        pair = out["pairs"][0]
        assert pair["relation"] == "within_tolerance"
        assert pair["gap_seconds"] == 4.0
        assert pair["temporally_compatible"] is True


def test_missing_time_is_partial_not_false_negative() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_case(
            root,
            [
                obs("a", "github_actions", None, None, digest_char="f"),
                obs("b", "supabase", "2026-09-27T11:00:00Z", "2026-09-27T11:00:01Z", digest_char="1"),
            ],
        )
        result = build_observability_temporal_correlation(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.insufficient_pair_count == 1
        out = json.loads((root / OUTPUT).read_text())
        assert out["pairs"][0]["relation"] == "insufficient_time_metadata"
        assert out["pairs"][0]["temporally_compatible"] is False


def test_transient_source_is_partial() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_case(
            root,
            [
                obs(
                    "gh",
                    "github_actions",
                    "2026-09-27T11:00:00Z",
                    "2026-09-27T11:00:00Z",
                    status="KUUOS_OBSERVABILITY_MCP_TRANSIENT_OBSTRUCTION",
                    digest_char="2",
                ),
                obs("v", "vercel", "2026-09-27T11:00:00Z", "2026-09-27T11:00:01Z", digest_char="3"),
            ],
        )
        result = build_observability_temporal_correlation(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.transient_pair_count == 1
        out = json.loads((root / OUTPUT).read_text())
        assert out["pairs"][0]["relation"] == "source_obstruction"
        assert out["pairs"][0]["causal_claim_permitted"] is False


def test_reversed_window_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_case(
            root,
            [
                obs("a", "github_actions", "2026-09-27T11:00:10Z", "2026-09-27T11:00:00Z", digest_char="4"),
                obs("b", "vercel", "2026-09-27T11:00:00Z", "2026-09-27T11:00:01Z", digest_char="5"),
            ],
        )
        result = build_observability_temporal_correlation(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "observation_0_time_window_reversed" in result.blockers
        assert not (root / OUTPUT).exists()


def test_naive_timestamp_blocks_by_lack_of_metadata() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write_case(
            root,
            [
                obs("a", "github_actions", "2026-09-27T11:00:00", "2026-09-27T11:00:01", digest_char="6"),
                obs("b", "vercel", "2026-09-27T11:00:00Z", "2026-09-27T11:00:01Z", digest_char="7"),
            ],
        )
        result = build_observability_temporal_correlation(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.insufficient_pair_count == 1


def main() -> int:
    test_overlap_and_disjoint()
    test_within_tolerance()
    test_missing_time_is_partial_not_false_negative()
    test_transient_source_is_partial()
    test_reversed_window_blocks()
    test_naive_timestamp_blocks_by_lack_of_metadata()
    print("PASS: KuuOS Observability Temporal Correlation v7.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
