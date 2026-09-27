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

from runtime.kuuos_runtime_observability_dependent_origination_restriction_v7_5 import (
    BLOCKED,
    GENERATOR_LOCAL_OBSTRUCTION,
    HIGHER_GLUING_OBSTRUCTION,
    HIGHER_GLUING_UNRESOLVED,
    LOCAL_ONLY_NO_RESTRICTION,
    LOCAL_RESTRICTION_UNRESOLVED,
    OBSTRUCTED,
    PARTIAL,
    READY,
    RESTRICTION_COMPATIBLE,
    RESTRICTION_HELD,
    RESTRICTION_OBSTRUCTED,
    STABLE_DESCENT,
    build_observability_dependent_origination_restriction,
)

PLAN = "observability_dependent_origination_restriction_plan_v7_5.json"
SOURCE = "observability_dependent_origination_descent_packet_v7_4.json"
OUTPUT = "observability_dependent_origination_restriction_packet_v7_5.json"


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
        "authority_status": "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_RESTRICTION_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_descent_packet_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_dependent_origination_restriction_enabled": True,
        "apply_observability_dependent_origination_restriction": True,
    }


def comparison(
    left: str,
    right: str,
    relation: str,
    compatible: bool,
) -> dict[str, Any]:
    return {
        "left_presentation_id": left,
        "right_presentation_id": right,
        "temporal_relation": relation,
        "temporally_compatible": compatible,
        "alignment_state": (
            "temporal_only"
            if compatible
            else "source_obstruction"
            if relation == "source_obstruction"
            else "no_alignment_evidence"
        ),
        "has_shared_exact_identifier": False,
    }


def family(
    family_id: str,
    members: list[str],
    *,
    kind: str = "correlation_id",
    digest_char: str = "a",
) -> dict[str, Any]:
    return {
        "condition_family_id": family_id,
        "condition_kind": kind,
        "condition_digest": digest_char * 64,
        "presentation_ids": members,
        "presentation_count": len(members),
        "witness_pair_count": 1,
        "non_reified": True,
    }


def sector(
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
        "local_compatibility": (
            "compatible"
            if descent_status == "descended_contextual_presentation"
            else "obstructed"
            if descent_status == "descent_obstructed"
            else "unresolved"
            if descent_status == "descent_held"
            else "not_applicable_singleton"
        ),
        "descent_status": descent_status,
        "descended_presentation_id": (
            "descended-test"
            if descent_status == "descended_contextual_presentation"
            else ""
        ),
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
        "formal_factorization_claimed": False,
        "higher_coherence_claimed": False,
    }


def source_packet(
    *,
    families: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    obstructions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_dependent_origination_descent_v7_4",
        "status": "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_READY",
        "source_temporal_packet_digest": "1" * 64,
        "source_alignment_packet_digest": "2" * 64,
        "presentations": [],
        "conditioning_families": families,
        "descent_sectors": sectors,
        "obstruction_witnesses": obstructions or [],
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


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_dependent_origination_restriction_plan_v7_5",
        "source_descent_packet_digest": sha(source),
        "read_only": True,
        "global_collapse_allowed": False,
        "causal_inference_allowed": False,
        "higher_coherence_claim_allowed": False,
        "source_authority_transfer_allowed": False,
        "python_is_formal_theorem_authority": False,
        "max_conditioning_families": 128,
    }


def write_case(
    root: pathlib.Path,
    source: dict[str, Any],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / SOURCE).write_text(json.dumps(source), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(source)),
        encoding="utf-8",
    )


def test_stable_descent_restricts_compatibly() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        families = [
            family("f-ab", ["a", "b"], digest_char="a"),
            family("f-bc", ["b", "c"], digest_char="b"),
        ]
        comparisons = [
            comparison("a", "b", "overlap", True),
            comparison("b", "c", "within_tolerance", True),
            comparison("a", "c", "overlap", True),
        ]
        source = source_packet(
            families=families,
            sectors=[
                sector(
                    "s-abc",
                    ["a", "b", "c"],
                    ["f-ab", "f-bc"],
                    "descended_contextual_presentation",
                    comparisons,
                )
            ],
        )
        write_case(root, source)
        result = build_observability_dependent_origination_restriction(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.stable_descent_count == 1
        out = json.loads((root / OUTPUT).read_text())
        s = out["restriction_sectors"][0]
        assert s["restriction_diagnosis"] == STABLE_DESCENT
        assert {
            r["restriction_status"] for r in s["conditioning_family_restrictions"]
        } == {RESTRICTION_COMPATIBLE}
        assert out["dependent_origination_boundary"]["formal_v4_61_restriction_whiskering_replaced"] is False


def test_generator_local_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        families = [family("f-ab", ["a", "b"], digest_char="c")]
        source = source_packet(
            families=families,
            sectors=[
                sector(
                    "s-ab",
                    ["a", "b"],
                    ["f-ab"],
                    "descent_obstructed",
                    [comparison("a", "b", "disjoint", False)],
                )
            ],
            obstructions=[
                {
                    "obstruction_kind": "related_presentations_temporally_disjoint",
                    "left_presentation_id": "a",
                    "right_presentation_id": "b",
                }
            ],
        )
        write_case(root, source)
        result = build_observability_dependent_origination_restriction(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.generator_local_obstruction_count == 1
        out = json.loads((root / OUTPUT).read_text())
        s = out["restriction_sectors"][0]
        assert s["restriction_diagnosis"] == GENERATOR_LOCAL_OBSTRUCTION
        assert s["conditioning_family_restrictions"][0]["restriction_status"] == RESTRICTION_OBSTRUCTED


def test_higher_gluing_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        families = [
            family("f-ab", ["a", "b"], digest_char="d"),
            family("f-bc", ["b", "c"], digest_char="e"),
        ]
        source = source_packet(
            families=families,
            sectors=[
                sector(
                    "s-abc",
                    ["a", "b", "c"],
                    ["f-ab", "f-bc"],
                    "descent_obstructed",
                    [
                        comparison("a", "b", "overlap", True),
                        comparison("b", "c", "overlap", True),
                        comparison("a", "c", "disjoint", False),
                    ],
                )
            ],
            obstructions=[
                {
                    "obstruction_kind": "related_presentations_temporally_disjoint",
                    "left_presentation_id": "a",
                    "right_presentation_id": "c",
                }
            ],
        )
        write_case(root, source)
        result = build_observability_dependent_origination_restriction(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.higher_gluing_obstruction_count == 1
        assert result.generator_local_obstruction_count == 0

        out = json.loads((root / OUTPUT).read_text())
        s = out["restriction_sectors"][0]
        assert s["restriction_diagnosis"] == HIGHER_GLUING_OBSTRUCTION
        assert {
            r["restriction_status"] for r in s["conditioning_family_restrictions"]
        } == {RESTRICTION_COMPATIBLE}
        assert s["higher_gluing_witness_count"] == 1
        assert s["higher_gluing_witnesses"][0]["scope"] == "across_conditioning_families"


def test_higher_gluing_unresolved() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        families = [
            family("f-ab", ["a", "b"], digest_char="f"),
            family("f-bc", ["b", "c"], digest_char="1"),
        ]
        source = source_packet(
            families=families,
            sectors=[
                sector(
                    "s-abc",
                    ["a", "b", "c"],
                    ["f-ab", "f-bc"],
                    "descent_held",
                    [
                        comparison("a", "b", "overlap", True),
                        comparison("b", "c", "overlap", True),
                        comparison("a", "c", "source_obstruction", False),
                    ],
                )
            ],
        )
        write_case(root, source)
        result = build_observability_dependent_origination_restriction(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.unresolved_count == 1
        out = json.loads((root / OUTPUT).read_text())
        assert out["restriction_sectors"][0]["restriction_diagnosis"] == HIGHER_GLUING_UNRESOLVED


def test_local_restriction_unresolved() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        families = [family("f-ab", ["a", "b"], digest_char="2")]
        source = source_packet(
            families=families,
            sectors=[
                sector(
                    "s-ab",
                    ["a", "b"],
                    ["f-ab"],
                    "descent_held",
                    [comparison("a", "b", "source_obstruction", False)],
                )
            ],
        )
        write_case(root, source)
        result = build_observability_dependent_origination_restriction(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        s = out["restriction_sectors"][0]
        assert s["restriction_diagnosis"] == LOCAL_RESTRICTION_UNRESOLVED
        assert s["conditioning_family_restrictions"][0]["restriction_status"] == RESTRICTION_HELD


def test_local_only_remains_local() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet(
            families=[],
            sectors=[
                sector(
                    "s-a",
                    ["a"],
                    [],
                    "local_presentation_only",
                    [],
                )
            ],
        )
        write_case(root, source)
        result = build_observability_dependent_origination_restriction(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.local_only_count == 1
        out = json.loads((root / OUTPUT).read_text())
        assert out["restriction_sectors"][0]["restriction_diagnosis"] == LOCAL_ONLY_NO_RESTRICTION


def test_stale_source_digest_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet(families=[], sectors=[])
        stale_plan = plan(source)
        stale_plan["source_descent_packet_digest"] = "0" * 64
        write_case(root, source, override_plan=stale_plan)
        result = build_observability_dependent_origination_restriction(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "source_descent_packet_digest_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def main() -> int:
    test_stable_descent_restricts_compatibly()
    test_generator_local_obstruction()
    test_higher_gluing_obstruction()
    test_higher_gluing_unresolved()
    test_local_restriction_unresolved()
    test_local_only_remains_local()
    test_stale_source_digest_blocks()
    print("PASS: KuuOS Observability Dependent-Origination Restriction v7.5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
