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

from runtime.kuuos_runtime_observability_invariant_carrier_v7_8 import (
    BLOCKED,
    FACTORIZED,
    FACTOR_HELD,
    FACTOR_OBSTRUCTED,
    LOCAL_IMAGE,
    OBSTRUCTED,
    PARTIAL,
    READY,
    build_observability_invariant_carrier,
)

PLAN = "observability_invariant_carrier_plan_v7_8.json"
SOURCE = "observability_presentation_invariance_packet_v7_7.json"
OUTPUT = "observability_invariant_carrier_packet_v7_8.json"


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
        "authority_status": "KUUOS_OBSERVABILITY_INVARIANT_CARRIER_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_invariance_packet_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_invariant_carrier_enabled": True,
        "apply_observability_invariant_carrier": True,
    }


def invariant_row(
    presentation_id: str,
    digest_char: str | None,
    *,
    state: str = "observed",
) -> dict[str, Any]:
    return {
        "presentation_id": presentation_id,
        "invariant_state": state,
        "invariant_digest": (digest_char * 64) if digest_char is not None else "",
    }


def sector(
    sector_id: str,
    members: list[str],
    *,
    status: str,
    common_digest_char: str | None = None,
) -> dict[str, Any]:
    return {
        "sector_id": sector_id,
        "presentation_ids": members,
        "presentation_count": len(members),
        "preinvariant_v7_4_status": "descended_contextual_presentation",
        "presentation_invariance_status": status,
        "presentation_invariant": status == "presentation_invariant",
        "runtime_descent_conclusion": (
            "presentation_independent_descent"
            if status == "presentation_invariant"
            else "descent_held_for_missing_invariant"
            if status == "presentation_invariance_held"
            else "descent_denied_by_invariant_variance"
            if status == "presentation_invariance_obstructed"
            else "local_invariant_presentation_only"
        ),
        "common_invariant_digest": (
            common_digest_char * 64 if common_digest_char is not None else ""
        ),
        "presentation_local_differences_ignored_by_invariant_projection": True,
        "compatibility_promoted_to_invariance": False,
        "formal_factorization_claimed": False,
    }


def source_packet(
    *,
    rows: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    projection_id: str = "kuuos-ci-semantic-v1",
    schema_digest: str = "f" * 64,
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_presentation_invariance_v7_7",
        "status": "KUUOS_OBSERVABILITY_PRESENTATION_INVARIANCE_READY",
        "source_descent_packet_digest": "a" * 64,
        "invariant_projection_id": projection_id,
        "invariant_schema_digest": schema_digest,
        "presentation_invariants": rows,
        "presentation_invariance_sectors": sectors,
        "quotient_invariant_witnesses": [],
        "obstruction_witnesses": [],
        "summary": {},
        "dependent_origination_boundary": {
            "presentation_invariance_required_for_descent": True,
            "invariant_match_erases_presentation_dependence": True,
            "presentation_local_equality_required": False,
            "provider_equality_required": False,
            "raw_observation_equality_required": False,
            "shared_context_is_not_invariance": True,
            "temporal_compatibility_is_not_invariance": True,
            "overlap_compatibility_is_not_invariance": True,
            "v7_4_descent_status_is_preinvariance_candidate_only": True,
            "runtime_descent_authorized_only_after_invariance": True,
            "invariant_projection_is_not_ultimate_truth": True,
            "invariant_projection_is_not_substance": True,
            "global_collapse_performed": False,
            "causal_inference_performed": False,
            "source_authority_transferred": False,
            "python_formal_theorem_authority": False,
            "formal_v4_49_factorization_theorem_replaced": False,
        },
    }


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_invariant_carrier_plan_v7_8",
        "source_invariance_packet_digest": sha(source),
        "invariant_projection_id": source["invariant_projection_id"],
        "invariant_schema_digest": source["invariant_schema_digest"],
        "read_only": True,
        "canonical_carrier_map_required": True,
        "carrier_identity_depends_only_on_invariant": True,
        "presentation_id_may_affect_carrier_identity": False,
        "sector_id_may_affect_carrier_identity": False,
        "provider_may_affect_carrier_identity": False,
        "source_authority_transfer_allowed": False,
        "python_is_formal_universality_authority": False,
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


def test_same_invariant_same_carrier_across_presentations_and_sectors() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet(
            rows=[
                invariant_row("github-a", "1"),
                invariant_row("vercel-b", "1"),
                invariant_row("supabase-c", "1"),
            ],
            sectors=[
                sector(
                    "sector-one",
                    ["github-a", "vercel-b"],
                    status="presentation_invariant",
                    common_digest_char="1",
                ),
                sector(
                    "sector-two",
                    ["supabase-c"],
                    status="local_presentation_only",
                    common_digest_char="1",
                ),
            ],
        )
        write_case(root, source)

        result = build_observability_invariant_carrier(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.presentation_count == 3
        assert result.carrier_element_count == 1
        assert result.canonical_image_count == 3
        assert result.factorized_sector_count == 1
        assert result.local_image_sector_count == 1

        out = json.loads((root / OUTPUT).read_text())
        ids = {
            record["carrier_element_id"]
            for record in out["canonical_presentation_map"]
            if record["canonical_image_defined"]
        }
        assert len(ids) == 1

        carrier = out["carrier_elements"][0]
        assert carrier["presentation_witness_count"] == 3
        assert carrier["presentation_witness_ids"] == [
            "github-a",
            "supabase-c",
            "vercel-b",
        ]
        assert carrier["carrier_identity_uses_presentation_id"] is False
        assert carrier["carrier_identity_uses_sector_id"] is False
        assert carrier["carrier_identity_uses_provider"] is False

        by_sector = {
            item["sector_id"]: item
            for item in out["sector_factorizations"]
        }
        assert by_sector["sector-one"]["carrier_factorization_status"] == FACTORIZED
        assert by_sector["sector-two"]["carrier_factorization_status"] == LOCAL_IMAGE
        assert (
            by_sector["sector-one"]["carrier_element_id"]
            == by_sector["sector-two"]["carrier_element_id"]
        )


def test_different_invariants_remain_distinct_carrier_elements() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet(
            rows=[
                invariant_row("a", "2"),
                invariant_row("b", "3"),
            ],
            sectors=[
                sector(
                    "sector-obstructed",
                    ["a", "b"],
                    status="presentation_invariance_obstructed",
                )
            ],
        )
        write_case(root, source)

        result = build_observability_invariant_carrier(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.carrier_element_count == 2
        assert result.obstructed_sector_count == 1

        out = json.loads((root / OUTPUT).read_text())
        factor = out["sector_factorizations"][0]
        assert factor["carrier_factorization_status"] == FACTOR_OBSTRUCTED
        assert len(factor["distinct_observed_carrier_element_ids"]) == 2


def test_held_invariant_gives_partial_canonical_map() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet(
            rows=[
                invariant_row("a", "4"),
                invariant_row("b", None, state="held"),
            ],
            sectors=[
                sector(
                    "sector-held",
                    ["a", "b"],
                    status="presentation_invariance_held",
                    common_digest_char="4",
                )
            ],
        )
        write_case(root, source)

        result = build_observability_invariant_carrier(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.carrier_element_count == 1
        assert result.canonical_image_count == 1
        assert result.held_image_count == 1
        assert result.held_sector_count == 1

        out = json.loads((root / OUTPUT).read_text())
        factor = out["sector_factorizations"][0]
        assert factor["carrier_factorization_status"] == FACTOR_HELD
        assert factor["missing_canonical_image_presentation_ids"] == ["b"]


def test_carrier_id_ignores_presentation_names() -> None:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        root1 = pathlib.Path(td1)
        root2 = pathlib.Path(td2)

        source1 = source_packet(
            rows=[
                invariant_row("presentation-left", "5"),
                invariant_row("presentation-right", "5"),
            ],
            sectors=[
                sector(
                    "sector-alpha",
                    ["presentation-left", "presentation-right"],
                    status="presentation_invariant",
                    common_digest_char="5",
                )
            ],
        )
        source2 = source_packet(
            rows=[
                invariant_row("totally-different-a", "5"),
                invariant_row("totally-different-b", "5"),
            ],
            sectors=[
                sector(
                    "sector-beta",
                    ["totally-different-a", "totally-different-b"],
                    status="presentation_invariant",
                    common_digest_char="5",
                )
            ],
        )

        write_case(root1, source1)
        write_case(root2, source2)

        r1 = build_observability_invariant_carrier(
            runtime_context=ctx(root1),
            authority_packet=authority(),
        )
        r2 = build_observability_invariant_carrier(
            runtime_context=ctx(root2),
            authority_packet=authority(),
        )
        assert r1.status == READY
        assert r2.status == READY

        out1 = json.loads((root1 / OUTPUT).read_text())
        out2 = json.loads((root2 / OUTPUT).read_text())
        assert (
            out1["carrier_elements"][0]["carrier_element_id"]
            == out2["carrier_elements"][0]["carrier_element_id"]
        )


def test_projection_identity_still_matters() -> None:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        root1 = pathlib.Path(td1)
        root2 = pathlib.Path(td2)

        source1 = source_packet(
            rows=[invariant_row("a", "6")],
            sectors=[
                sector(
                    "s1",
                    ["a"],
                    status="local_presentation_only",
                    common_digest_char="6",
                )
            ],
            projection_id="projection-one",
        )
        source2 = source_packet(
            rows=[invariant_row("a", "6")],
            sectors=[
                sector(
                    "s2",
                    ["a"],
                    status="local_presentation_only",
                    common_digest_char="6",
                )
            ],
            projection_id="projection-two",
        )

        write_case(root1, source1)
        write_case(root2, source2)

        r1 = build_observability_invariant_carrier(
            runtime_context=ctx(root1),
            authority_packet=authority(),
        )
        r2 = build_observability_invariant_carrier(
            runtime_context=ctx(root2),
            authority_packet=authority(),
        )
        assert r1.status == READY
        assert r2.status == READY

        out1 = json.loads((root1 / OUTPUT).read_text())
        out2 = json.loads((root2 / OUTPUT).read_text())
        assert (
            out1["carrier_elements"][0]["carrier_element_id"]
            != out2["carrier_elements"][0]["carrier_element_id"]
        )


def test_stale_source_digest_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet(
            rows=[invariant_row("a", "7")],
            sectors=[
                sector(
                    "s",
                    ["a"],
                    status="local_presentation_only",
                    common_digest_char="7",
                )
            ],
        )
        p = plan(source)
        p["source_invariance_packet_digest"] = "0" * 64
        write_case(root, source, override_plan=p)

        result = build_observability_invariant_carrier(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "source_invariance_packet_digest_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def main() -> int:
    test_same_invariant_same_carrier_across_presentations_and_sectors()
    test_different_invariants_remain_distinct_carrier_elements()
    test_held_invariant_gives_partial_canonical_map()
    test_carrier_id_ignores_presentation_names()
    test_projection_identity_still_matters()
    test_stale_source_digest_blocks()
    print("PASS: KuuOS Observability Invariant Carrier v7.8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
