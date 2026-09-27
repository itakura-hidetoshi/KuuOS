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

from runtime.kuuos_runtime_observability_dependent_origination_overlap_v7_6 import (
    BLOCKED,
    OBSTRUCTED,
    OVERLAP_COMPATIBLE,
    OVERLAP_HELD,
    OVERLAP_MISMATCH,
    OVERLAP_TRIVIAL,
    PARTIAL,
    READY,
    SECTOR_OVERLAP_OBSTRUCTED,
    SECTOR_OVERLAP_HELD,
    SECTOR_PAIRWISE_NOT_GLOBAL,
    SECTOR_STABLE,
    build_observability_dependent_origination_overlap,
)

PLAN = "observability_dependent_origination_overlap_plan_v7_6.json"
DESCENT = "observability_dependent_origination_descent_packet_v7_4.json"
RESTRICTION = "observability_dependent_origination_restriction_packet_v7_5.json"
OUTPUT = "observability_dependent_origination_overlap_packet_v7_6.json"


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
        "authority_status": "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_OVERLAP_AUTHORITY_READY",
        "plan_read_allowed": True,
        "descent_packet_read_allowed": True,
        "restriction_packet_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_dependent_origination_overlap_enabled": True,
        "apply_observability_dependent_origination_overlap": True,
    }


def presentation(pid: str, digest_char: str) -> dict[str, Any]:
    return {
        "presentation_id": pid,
        "provider": f"provider-{pid}",
        "operation": "logs",
        "source_digest": digest_char * 64,
        "source_status": "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED",
        "availability": "observed",
        "window_start": "2026-09-27T11:00:00Z",
        "window_end": "2026-09-27T11:00:10Z",
        "condition_family_ids": [],
        "presentation_is_substance": False,
        "provider_is_ultimate_authority": False,
    }


def comparison(left: str, right: str, relation: str, compatible: bool) -> dict[str, Any]:
    return {
        "left_presentation_id": left,
        "right_presentation_id": right,
        "temporal_relation": relation,
        "temporally_compatible": compatible,
        "alignment_state": "temporal_only" if compatible else "no_alignment_evidence",
        "has_shared_exact_identifier": False,
    }


def descent_sector(
    *,
    sector_id: str,
    members: list[str],
    family_ids: list[str],
    descent_status: str,
    comparisons: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "sector_id": sector_id,
        "presentation_ids": members,
        "presentation_count": len(members),
        "condition_family_ids": family_ids,
        "condition_family_count": len(family_ids),
        "local_compatibility": "compatible",
        "descent_status": descent_status,
        "descended_presentation_id": (
            "descended-test" if descent_status == "descended_contextual_presentation" else ""
        ),
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
        "formal_factorization_claimed": False,
        "higher_coherence_claimed": False,
    }


def descent_packet(
    *,
    presentations: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_dependent_origination_descent_v7_4",
        "status": "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_READY",
        "source_temporal_packet_digest": "1" * 64,
        "source_alignment_packet_digest": "2" * 64,
        "presentations": presentations,
        "conditioning_families": [],
        "descent_sectors": sectors,
        "obstruction_witnesses": [],
        "summary": {},
        "dependent_origination_boundary": {
            "many_presentations_preserved": True,
            "conditioning_relation_is_not_substance": True,
            "descent_requires_local_compatibility": True,
            "obstruction_witnesses_preserved": True,
            "global_collapse_performed": False,
            "single_provider_privileged": False,
            "causal_inference_performed": False,
            "causal_direction_inferred": False,
            "source_authority_transferred": False,
            "runtime_descent_is_formal_theorem_proof": False,
            "formal_v4_49_factorization_theorem_replaced": False,
            "formal_v4_61_higher_coherence_replaced": False,
        },
    }


def local_cmp(left: str, right: str, relation: str, compatible: bool) -> dict[str, Any]:
    return {
        "left_presentation_id": left,
        "right_presentation_id": right,
        "temporal_relation": relation,
        "temporally_compatible": compatible,
    }


def family_restriction(
    family_id: str,
    members: list[str],
    *,
    status: str = "restriction_compatible",
    local_comparisons: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "condition_family_id": family_id,
        "condition_kind": "correlation_id",
        "condition_digest": sha({"family": family_id}),
        "presentation_ids": members,
        "presentation_count": len(members),
        "restriction_status": status,
        "local_comparison_count": len(local_comparisons or []),
        "local_comparisons": local_comparisons or [],
        "condition_is_substance": False,
    }


def restriction_sector(
    *,
    sector_id: str,
    source_diagnosis: str,
    families: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "sector_id": sector_id,
        "presentation_ids": sorted(
            {pid for family in families for pid in family["presentation_ids"]}
        ),
        "source_descent_status": "descended_contextual_presentation",
        "restriction_diagnosis": source_diagnosis,
        "conditioning_family_restrictions": families,
        "conditioning_family_restriction_count": len(families),
        "higher_gluing_witnesses": [],
        "higher_gluing_witness_count": 0,
        "restriction_preservation_is_formal_v4_61_theorem_claim": False,
        "higher_coherence_claimed": False,
    }


def restriction_packet(
    descent: dict[str, Any],
    sectors: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_dependent_origination_restriction_v7_5",
        "status": "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_RESTRICTION_READY",
        "source_descent_packet_digest": sha(descent),
        "restriction_sectors": sectors,
        "summary": {},
        "dependent_origination_boundary": {
            "restriction_preserves_local_presentation_context": True,
            "local_compatibility_checked_before_higher_gluing": True,
            "higher_gluing_obstruction_is_not_reduced_to_graph_connectivity": True,
            "global_collapse_performed": False,
            "causal_inference_performed": False,
            "causal_direction_inferred": False,
            "source_authority_transferred": False,
            "python_formal_theorem_authority": False,
            "formal_v4_61_restriction_whiskering_replaced": False,
        },
    }


def plan(descent: dict[str, Any], restriction: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_dependent_origination_overlap_plan_v7_6",
        "source_descent_packet_digest": sha(descent),
        "source_restriction_packet_digest": sha(restriction),
        "read_only": True,
        "global_collapse_allowed": False,
        "causal_inference_allowed": False,
        "pairwise_overlap_implies_global_descent": False,
        "higher_coherence_claim_allowed": False,
        "source_authority_transfer_allowed": False,
        "python_is_formal_theorem_authority": False,
        "max_overlap_pairs": 512,
    }


def write_case(
    root: pathlib.Path,
    descent: dict[str, Any],
    restriction: dict[str, Any],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / DESCENT).write_text(json.dumps(descent), encoding="utf-8")
    (root / RESTRICTION).write_text(json.dumps(restriction), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(descent, restriction)),
        encoding="utf-8",
    )


def test_singleton_overlap_supports_stable_descent_without_global_inference() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        comparisons = [
            comparison("a", "b", "overlap", True),
            comparison("b", "c", "within_tolerance", True),
            comparison("a", "c", "overlap", True),
        ]
        descent = descent_packet(
            presentations=[
                presentation("a", "a"),
                presentation("b", "b"),
                presentation("c", "c"),
            ],
            sectors=[
                descent_sector(
                    sector_id="s-abc",
                    members=["a", "b", "c"],
                    family_ids=["f-ab", "f-bc"],
                    descent_status="descended_contextual_presentation",
                    comparisons=comparisons,
                )
            ],
        )
        families = [
            family_restriction(
                "f-ab",
                ["a", "b"],
                local_comparisons=[local_cmp("a", "b", "overlap", True)],
            ),
            family_restriction(
                "f-bc",
                ["b", "c"],
                local_comparisons=[local_cmp("b", "c", "within_tolerance", True)],
            ),
        ]
        restriction = restriction_packet(
            descent,
            [
                restriction_sector(
                    sector_id="s-abc",
                    source_diagnosis="restriction_stable_descent",
                    families=families,
                )
            ],
        )
        write_case(root, descent, restriction)
        result = build_observability_dependent_origination_overlap(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.trivial_overlap_count == 1
        out = json.loads((root / OUTPUT).read_text())
        sector = out["overlap_sectors"][0]
        assert sector["overlap_diagnosis"] == SECTOR_STABLE
        record = sector["overlap_records"][0]
        assert record["overlap_status"] == OVERLAP_TRIVIAL
        assert record["overlap_presentation_ids"] == ["b"]
        assert record["common_restriction_witness_present"] is True
        assert record["global_descent_inferred_from_pairwise_overlap"] is False
        assert out["dependent_origination_boundary"]["pairwise_overlap_compatibility_sufficient_for_global_descent"] is False


def test_nontrivial_overlap_compatible() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        comparisons = [
            comparison("a", "b", "overlap", True),
            comparison("a", "c", "overlap", True),
            comparison("b", "c", "within_tolerance", True),
            comparison("b", "d", "overlap", True),
            comparison("c", "d", "within_tolerance", True),
            comparison("a", "d", "overlap", True),
        ]
        descent = descent_packet(
            presentations=[
                presentation("a", "a"),
                presentation("b", "b"),
                presentation("c", "c"),
                presentation("d", "d"),
            ],
            sectors=[
                descent_sector(
                    sector_id="s-abcd",
                    members=["a", "b", "c", "d"],
                    family_ids=["f-abc", "f-bcd"],
                    descent_status="descended_contextual_presentation",
                    comparisons=comparisons,
                )
            ],
        )
        shared_bc = local_cmp("b", "c", "within_tolerance", True)
        families = [
            family_restriction(
                "f-abc",
                ["a", "b", "c"],
                local_comparisons=[
                    local_cmp("a", "b", "overlap", True),
                    local_cmp("a", "c", "overlap", True),
                    shared_bc,
                ],
            ),
            family_restriction(
                "f-bcd",
                ["b", "c", "d"],
                local_comparisons=[
                    shared_bc,
                    local_cmp("b", "d", "overlap", True),
                    local_cmp("c", "d", "within_tolerance", True),
                ],
            ),
        ]
        restriction = restriction_packet(
            descent,
            [
                restriction_sector(
                    sector_id="s-abcd",
                    source_diagnosis="restriction_stable_descent",
                    families=families,
                )
            ],
        )
        write_case(root, descent, restriction)
        result = build_observability_dependent_origination_overlap(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.compatible_overlap_count == 1
        out = json.loads((root / OUTPUT).read_text())
        record = out["overlap_sectors"][0]["overlap_records"][0]
        assert record["overlap_status"] == OVERLAP_COMPATIBLE
        assert record["overlap_presentation_ids"] == ["b", "c"]
        assert record["projection_equal"] is True
        assert record["projection_validation_reasons"] == []


def test_pairwise_overlap_compatible_but_global_descent_obstructed() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        comparisons = [
            comparison("a", "b", "overlap", True),
            comparison("b", "c", "overlap", True),
            comparison("a", "c", "disjoint", False),
        ]
        descent = descent_packet(
            presentations=[
                presentation("a", "a"),
                presentation("b", "b"),
                presentation("c", "c"),
            ],
            sectors=[
                descent_sector(
                    sector_id="s-abc",
                    members=["a", "b", "c"],
                    family_ids=["f-ab", "f-bc"],
                    descent_status="descent_obstructed",
                    comparisons=comparisons,
                )
            ],
        )
        families = [
            family_restriction(
                "f-ab",
                ["a", "b"],
                local_comparisons=[local_cmp("a", "b", "overlap", True)],
            ),
            family_restriction(
                "f-bc",
                ["b", "c"],
                local_comparisons=[local_cmp("b", "c", "overlap", True)],
            ),
        ]
        restriction = restriction_packet(
            descent,
            [
                restriction_sector(
                    sector_id="s-abc",
                    source_diagnosis="higher_gluing_obstruction",
                    families=families,
                )
            ],
        )
        write_case(root, descent, restriction)
        result = build_observability_dependent_origination_overlap(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.pairwise_not_global_sector_count == 1
        out = json.loads((root / OUTPUT).read_text())
        sector = out["overlap_sectors"][0]
        assert sector["overlap_diagnosis"] == SECTOR_PAIRWISE_NOT_GLOBAL
        assert sector["overlap_records"][0]["overlap_status"] == OVERLAP_TRIVIAL
        assert sector["pairwise_overlap_compatibility_sufficient_for_global_descent"] is False


def test_overlap_projection_mismatch_is_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        comparisons = [
            comparison("a", "b", "overlap", True),
            comparison("a", "c", "overlap", True),
            comparison("b", "c", "overlap", True),
            comparison("b", "d", "overlap", True),
            comparison("c", "d", "overlap", True),
            comparison("a", "d", "overlap", True),
        ]
        descent = descent_packet(
            presentations=[
                presentation("a", "a"),
                presentation("b", "b"),
                presentation("c", "c"),
                presentation("d", "d"),
            ],
            sectors=[
                descent_sector(
                    sector_id="s-abcd",
                    members=["a", "b", "c", "d"],
                    family_ids=["f-abc", "f-bcd"],
                    descent_status="descended_contextual_presentation",
                    comparisons=comparisons,
                )
            ],
        )
        families = [
            family_restriction(
                "f-abc",
                ["a", "b", "c"],
                local_comparisons=[
                    local_cmp("a", "b", "overlap", True),
                    local_cmp("a", "c", "overlap", True),
                    local_cmp("b", "c", "overlap", True),
                ],
            ),
            family_restriction(
                "f-bcd",
                ["b", "c", "d"],
                local_comparisons=[
                    local_cmp("b", "c", "disjoint", False),
                    local_cmp("b", "d", "overlap", True),
                    local_cmp("c", "d", "overlap", True),
                ],
            ),
        ]
        restriction = restriction_packet(
            descent,
            [
                restriction_sector(
                    sector_id="s-abcd",
                    source_diagnosis="restriction_stable_descent",
                    families=families,
                )
            ],
        )
        write_case(root, descent, restriction)
        result = build_observability_dependent_origination_overlap(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.mismatch_overlap_count == 1
        out = json.loads((root / OUTPUT).read_text())
        sector = out["overlap_sectors"][0]
        assert sector["overlap_diagnosis"] == SECTOR_OVERLAP_OBSTRUCTED
        record = sector["overlap_records"][0]
        assert record["overlap_status"] == OVERLAP_MISMATCH
        assert record["projection_equal"] is False
        assert any(
            "temporal_relation_mismatch:b:c" in reason
            for reason in record["projection_validation_reasons"]
        )


def test_overlap_held_is_partial() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        comparisons = [
            comparison("a", "b", "overlap", True),
            comparison("b", "c", "source_obstruction", False),
            comparison("a", "c", "source_obstruction", False),
        ]
        descent = descent_packet(
            presentations=[
                presentation("a", "a"),
                presentation("b", "b"),
                presentation("c", "c"),
            ],
            sectors=[
                descent_sector(
                    sector_id="s-abc",
                    members=["a", "b", "c"],
                    family_ids=["f-ab", "f-bc"],
                    descent_status="descent_held",
                    comparisons=comparisons,
                )
            ],
        )
        families = [
            family_restriction(
                "f-ab",
                ["a", "b"],
                local_comparisons=[local_cmp("a", "b", "overlap", True)],
            ),
            family_restriction(
                "f-bc",
                ["b", "c"],
                status="restriction_held",
                local_comparisons=[local_cmp("b", "c", "source_obstruction", False)],
            ),
        ]
        restriction = restriction_packet(
            descent,
            [
                restriction_sector(
                    sector_id="s-abc",
                    source_diagnosis="higher_gluing_unresolved",
                    families=families,
                )
            ],
        )
        write_case(root, descent, restriction)
        result = build_observability_dependent_origination_overlap(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.held_overlap_count == 1
        out = json.loads((root / OUTPUT).read_text())
        sector = out["overlap_sectors"][0]
        assert sector["overlap_diagnosis"] == SECTOR_OVERLAP_HELD
        assert sector["overlap_records"][0]["overlap_status"] == OVERLAP_HELD


def test_stale_restriction_digest_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        descent = descent_packet(
            presentations=[presentation("a", "a")],
            sectors=[
                descent_sector(
                    sector_id="s-a",
                    members=["a"],
                    family_ids=[],
                    descent_status="local_presentation_only",
                    comparisons=[],
                )
            ],
        )
        restriction = restriction_packet(
            descent,
            [
                restriction_sector(
                    sector_id="s-a",
                    source_diagnosis="local_only_no_restriction",
                    families=[],
                )
            ],
        )
        stale_plan = plan(descent, restriction)
        stale_plan["source_restriction_packet_digest"] = "0" * 64
        write_case(root, descent, restriction, override_plan=stale_plan)
        result = build_observability_dependent_origination_overlap(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "source_restriction_packet_digest_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def main() -> int:
    test_singleton_overlap_supports_stable_descent_without_global_inference()
    test_nontrivial_overlap_compatible()
    test_pairwise_overlap_compatible_but_global_descent_obstructed()
    test_overlap_projection_mismatch_is_obstruction()
    test_overlap_held_is_partial()
    test_stale_restriction_digest_blocks()
    print("PASS: KuuOS Observability Dependent-Origination Overlap v7.6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
