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

from runtime.kuuos_runtime_observability_dependent_origination_descent_v7_4 import (
    BLOCKED,
    DESCENDED,
    DESCENT_OBSTRUCTED,
    HELD,
    LOCAL_ONLY,
    OBSTRUCTED,
    PARTIAL,
    READY,
    build_observability_dependent_origination_descent,
)

PLAN = "observability_dependent_origination_descent_plan_v7_4.json"
TEMPORAL = "observability_temporal_correlation_packet_v7_2.json"
ALIGNMENT = "observability_event_alignment_packet_v7_3.json"
OUTPUT = "observability_dependent_origination_descent_packet_v7_4.json"


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
        "authority_status": "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_AUTHORITY_READY",
        "plan_read_allowed": True,
        "temporal_packet_read_allowed": True,
        "alignment_packet_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_dependent_origination_descent_enabled": True,
        "apply_observability_dependent_origination_descent": True,
    }


def temporal_packet(ids: list[str]) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_temporal_correlation_v7_2",
        "status": "KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_READY",
        "observations": [
            {
                "observation_id": oid,
                "provider": {
                    "a": "github_actions",
                    "b": "vercel",
                    "c": "supabase",
                    "d": "neon",
                }.get(oid, "provider-" + oid),
                "operation": "logs",
                "source_digest": (str(index + 1)[-1]) * 64,
                "source_status": "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED",
                "availability": "observed",
                "window_start": f"2026-09-27T11:00:0{index}Z",
                "window_end": f"2026-09-27T11:00:1{index}Z",
            }
            for index, oid in enumerate(ids)
        ],
        "pairs": [],
        "summary": {
            "observation_count": len(ids),
            "pair_count": len(ids) * (len(ids) - 1) // 2,
        },
        "interpretation_boundary": {
            "temporal_compatibility_is_not_causation": True,
            "causal_inference_performed": False,
            "source_authority_transferred": False,
        },
    }


def pair(
    left: str,
    right: str,
    *,
    relation: str,
    compatible: bool,
    shared: list[tuple[str, str]] | None = None,
    state: str | None = None,
) -> dict[str, Any]:
    shared = shared or []
    if state is None:
        if shared and relation in {"overlap", "within_tolerance"} and compatible:
            state = "exact_context_temporally_compatible"
        elif shared and relation == "disjoint":
            state = "exact_context_temporally_disjoint"
        elif shared:
            state = "exact_context_time_unresolved"
        elif compatible:
            state = "temporal_only"
        elif relation == "source_obstruction":
            state = "source_obstruction"
        else:
            state = "no_alignment_evidence"
    return {
        "left_observation_id": left,
        "right_observation_id": right,
        "left_provider": "",
        "right_provider": "",
        "temporal_relation": relation,
        "temporally_compatible": compatible,
        "alignment_state": state,
        "has_shared_exact_identifier": bool(shared),
        "shared_identifier_evidence": [
            {
                "identifier_type": identifier_type,
                "value_digest": value_digest,
            }
            for identifier_type, value_digest in shared
        ],
        "same_type_distinct_value_identifiers": [],
        "identity_values_exposed": False,
        "causal_claim": "not_inferred",
        "causal_direction": "not_inferred",
        "causal_claim_permitted": False,
    }


def alignment_packet(
    temporal: dict[str, Any],
    pairs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_event_alignment_v7_3",
        "status": "KUUOS_OBSERVABILITY_EVENT_ALIGNMENT_READY",
        "source_temporal_packet_digest": sha(temporal),
        "source_identity_input_digest": "f" * 64,
        "observation_count": len(temporal["observations"]),
        "pair_count": len(pairs),
        "pairs": pairs,
        "summary": {},
        "interpretation_boundary": {
            "shared_identifier_is_context_evidence_not_causation": True,
            "temporal_compatibility_is_not_causation": True,
            "causal_inference_performed": False,
            "causal_direction_inferred": False,
            "causal_claim_permitted": False,
            "identifier_values_exposed": False,
            "source_authority_transferred": False,
        },
    }


def plan(temporal: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_dependent_origination_descent_plan_v7_4",
        "source_temporal_packet_digest": sha(temporal),
        "source_alignment_packet_digest": sha(alignment),
        "read_only": True,
        "global_collapse_allowed": False,
        "substance_reification_allowed": False,
        "causal_inference_allowed": False,
        "source_authority_transfer_allowed": False,
        "python_is_formal_theorem_authority": False,
        "max_presentations": 64,
    }


def write_case(
    root: pathlib.Path,
    temporal: dict[str, Any],
    alignment: dict[str, Any],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / TEMPORAL).write_text(json.dumps(temporal), encoding="utf-8")
    (root / ALIGNMENT).write_text(json.dumps(alignment), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(temporal, alignment)),
        encoding="utf-8",
    )


def test_transitive_condition_relation_descends() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet(["a", "b", "c"])
        commit_digest = "a" * 64
        request_digest = "b" * 64
        alignment = alignment_packet(
            temporal,
            [
                pair(
                    "a",
                    "b",
                    relation="overlap",
                    compatible=True,
                    shared=[("commit_sha", commit_digest)],
                ),
                pair(
                    "b",
                    "c",
                    relation="within_tolerance",
                    compatible=True,
                    shared=[("request_id", request_digest)],
                ),
                pair(
                    "a",
                    "c",
                    relation="overlap",
                    compatible=True,
                ),
            ],
        )
        write_case(root, temporal, alignment)
        result = build_observability_dependent_origination_descent(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.presentation_count == 3
        assert result.conditioning_family_count == 2
        assert result.descent_sector_count == 1
        assert result.descended_sector_count == 1
        assert result.obstructed_sector_count == 0

        out_text = (root / OUTPUT).read_text()
        out = json.loads(out_text)
        sector = out["descent_sectors"][0]
        assert sector["presentation_ids"] == ["a", "b", "c"]
        assert sector["descent_status"] == DESCENDED
        assert sector["descended_presentation_id"]
        assert out["dependent_origination_boundary"]["many_presentations_preserved"] is True
        assert out["dependent_origination_boundary"]["global_collapse_performed"] is False
        assert out["dependent_origination_boundary"]["runtime_descent_is_formal_theorem_proof"] is False
        assert '"nodes"' not in out_text
        assert '"edges"' not in out_text
        assert '"graph"' not in out_text


def test_transitive_relation_with_local_incompatibility_obstructs_descent() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet(["a", "b", "c"])
        alignment = alignment_packet(
            temporal,
            [
                pair(
                    "a",
                    "b",
                    relation="overlap",
                    compatible=True,
                    shared=[("commit_sha", "c" * 64)],
                ),
                pair(
                    "b",
                    "c",
                    relation="overlap",
                    compatible=True,
                    shared=[("request_id", "d" * 64)],
                ),
                pair(
                    "a",
                    "c",
                    relation="disjoint",
                    compatible=False,
                ),
            ],
        )
        write_case(root, temporal, alignment)
        result = build_observability_dependent_origination_descent(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.obstructed_sector_count == 1
        assert result.obstruction_witness_count == 1
        out = json.loads((root / OUTPUT).read_text())
        sector = out["descent_sectors"][0]
        assert sector["descent_status"] == DESCENT_OBSTRUCTED
        assert sector["descended_presentation_id"] == ""
        witness = out["obstruction_witnesses"][0]
        assert witness["obstruction_kind"] == "related_presentations_temporally_disjoint"
        assert {witness["left_presentation_id"], witness["right_presentation_id"]} == {"a", "c"}


def test_unresolved_relation_holds_descent() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet(["a", "b"])
        alignment = alignment_packet(
            temporal,
            [
                pair(
                    "a",
                    "b",
                    relation="source_obstruction",
                    compatible=False,
                    shared=[("trace_id", "e" * 64)],
                    state="source_obstruction",
                )
            ],
        )
        write_case(root, temporal, alignment)
        result = build_observability_dependent_origination_descent(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.held_sector_count == 1
        out = json.loads((root / OUTPUT).read_text())
        assert out["descent_sectors"][0]["descent_status"] == HELD
        assert out["descent_sectors"][0]["local_compatibility"] == "unresolved"


def test_isolated_presentation_remains_local_without_global_failure() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet(["a", "b", "c"])
        alignment = alignment_packet(
            temporal,
            [
                pair(
                    "a",
                    "b",
                    relation="overlap",
                    compatible=True,
                    shared=[("workflow_run_id", "f" * 64)],
                ),
                pair("a", "c", relation="disjoint", compatible=False),
                pair("b", "c", relation="disjoint", compatible=False),
            ],
        )
        write_case(root, temporal, alignment)
        result = build_observability_dependent_origination_descent(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.descended_sector_count == 1
        assert result.local_only_sector_count == 1
        out = json.loads((root / OUTPUT).read_text())
        statuses = {sector["descent_status"] for sector in out["descent_sectors"]}
        assert statuses == {DESCENDED, LOCAL_ONLY}


def test_stale_alignment_digest_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet(["a", "b"])
        alignment = alignment_packet(
            temporal,
            [
                pair(
                    "a",
                    "b",
                    relation="overlap",
                    compatible=True,
                    shared=[("commit_sha", "1" * 64)],
                )
            ],
        )
        stale_plan = plan(temporal, alignment)
        stale_plan["source_alignment_packet_digest"] = "0" * 64
        write_case(root, temporal, alignment, override_plan=stale_plan)
        result = build_observability_dependent_origination_descent(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "plan_source_alignment_packet_digest_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def test_alignment_temporal_binding_mismatch_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        temporal = temporal_packet(["a", "b"])
        alignment = alignment_packet(
            temporal,
            [
                pair(
                    "a",
                    "b",
                    relation="overlap",
                    compatible=True,
                    shared=[("commit_sha", "2" * 64)],
                )
            ],
        )
        alignment["source_temporal_packet_digest"] = "0" * 64
        write_case(root, temporal, alignment)
        result = build_observability_dependent_origination_descent(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "alignment_source_temporal_packet_digest_mismatch" in result.blockers


def main() -> int:
    test_transitive_condition_relation_descends()
    test_transitive_relation_with_local_incompatibility_obstructs_descent()
    test_unresolved_relation_holds_descent()
    test_isolated_presentation_remains_local_without_global_failure()
    test_stale_alignment_digest_blocks()
    test_alignment_temporal_binding_mismatch_blocks()
    print("PASS: KuuOS Observability Dependent-Origination Descent v7.4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
