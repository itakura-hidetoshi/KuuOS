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

from runtime.kuuos_runtime_observability_presentation_invariance_v7_7 import (
    BLOCKED,
    DESCENT_AUTHORIZED,
    DESCENT_DENIED,
    DESCENT_HELD,
    INVARIANT,
    INVARIANCE_HELD,
    INVARIANCE_OBSTRUCTED,
    OBSTRUCTED,
    PARTIAL,
    READY,
    build_observability_presentation_invariance,
)

PLAN = "observability_presentation_invariance_plan_v7_7.json"
DESCENT = "observability_dependent_origination_descent_packet_v7_4.json"
INVARIANTS = "observability_presentation_invariant_input_v7_7.json"
OUTPUT = "observability_presentation_invariance_packet_v7_7.json"


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
        "authority_status": "KUUOS_OBSERVABILITY_PRESENTATION_INVARIANCE_AUTHORITY_READY",
        "plan_read_allowed": True,
        "descent_packet_read_allowed": True,
        "invariant_input_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_presentation_invariance_enabled": True,
        "apply_observability_presentation_invariance": True,
    }


def presentation(
    pid: str,
    provider: str,
    source_digest: str,
    start: str,
    end: str,
) -> dict[str, Any]:
    return {
        "presentation_id": pid,
        "provider": provider,
        "operation": "logs",
        "source_digest": source_digest,
        "source_status": "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED",
        "availability": "observed",
        "window_start": start,
        "window_end": end,
        "condition_family_ids": ["c-shared"],
        "presentation_is_substance": False,
        "provider_is_ultimate_authority": False,
    }


def descent_packet(
    *,
    presentations: list[dict[str, Any]],
    members: list[str],
    preinvariant_status: str = "descended_contextual_presentation",
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_dependent_origination_descent_v7_4",
        "status": "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_READY",
        "source_temporal_packet_digest": "1" * 64,
        "source_alignment_packet_digest": "2" * 64,
        "presentations": presentations,
        "conditioning_families": [
            {
                "condition_family_id": "c-shared",
                "condition_kind": "commit_sha",
                "condition_digest": "3" * 64,
                "presentation_ids": members,
                "presentation_count": len(members),
                "witness_pair_count": 1,
                "non_reified": True,
            }
        ],
        "descent_sectors": [
            {
                "sector_id": "s-shared",
                "presentation_ids": members,
                "presentation_count": len(members),
                "condition_family_ids": ["c-shared"],
                "condition_family_count": 1,
                "local_compatibility": "compatible",
                "descent_status": preinvariant_status,
                "descended_presentation_id": "preinvariant-candidate",
                "comparison_count": 0,
                "comparisons": [],
                "formal_factorization_claimed": False,
                "higher_coherence_claimed": False,
            }
        ],
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


def invariant_input(
    descent: dict[str, Any],
    rows: list[dict[str, Any]],
    *,
    projection_id: str = "kuuos-ci-terminal-outcome-v1",
    schema_digest: str = "4" * 64,
) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_presentation_invariant_input_v7_7",
        "source_descent_packet_digest": sha(descent),
        "invariant_projection_id": projection_id,
        "invariant_schema_digest": schema_digest,
        "presentation_invariants": rows,
    }


def invariant_row(
    pid: str,
    value: Any = None,
    *,
    state: str = "observed",
) -> dict[str, Any]:
    row = {
        "presentation_id": pid,
        "invariant_state": state,
    }
    if state == "observed":
        row["invariant_value"] = value
    else:
        row["invariant_value"] = None
    return row


def plan(
    descent: dict[str, Any],
    invariants: dict[str, Any],
) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_presentation_invariance_plan_v7_7",
        "source_descent_packet_digest": sha(descent),
        "invariant_projection_id": invariants["invariant_projection_id"],
        "invariant_schema_digest": invariants["invariant_schema_digest"],
        "read_only": True,
        "presentation_invariance_required_for_descent": True,
        "invariant_match_erases_presentation_dependence": True,
        "presentation_local_equality_required": False,
        "compatibility_may_substitute_for_invariance": False,
        "global_collapse_allowed": False,
        "causal_inference_allowed": False,
        "source_authority_transfer_allowed": False,
        "python_is_formal_theorem_authority": False,
        "max_presentations": 128,
        "max_invariant_value_bytes": 8192,
    }


def write_case(
    root: pathlib.Path,
    descent: dict[str, Any],
    invariants: dict[str, Any],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / DESCENT).write_text(json.dumps(descent), encoding="utf-8")
    (root / INVARIANTS).write_text(json.dumps(invariants), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(descent, invariants)),
        encoding="utf-8",
    )


def test_different_presentations_same_invariant_descend() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        descent = descent_packet(
            presentations=[
                presentation(
                    "github",
                    "github_actions",
                    "a" * 64,
                    "2026-09-27T12:00:00Z",
                    "2026-09-27T12:00:10Z",
                ),
                presentation(
                    "vercel",
                    "vercel",
                    "b" * 64,
                    "2026-09-27T12:00:03Z",
                    "2026-09-27T12:00:12Z",
                ),
            ],
            members=["github", "vercel"],
        )
        invariant_value = {
            "terminal_class": "success",
            "artifact_semantic": "same-release",
        }
        invariants = invariant_input(
            descent,
            [
                invariant_row("github", invariant_value),
                invariant_row("vercel", invariant_value),
            ],
        )
        write_case(root, descent, invariants)
        result = build_observability_presentation_invariance(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.invariant_sector_count == 1
        assert result.quotient_invariant_witness_count == 1

        out = json.loads((root / OUTPUT).read_text())
        sector = out["presentation_invariance_sectors"][0]
        assert sector["presentation_invariance_status"] == INVARIANT
        assert sector["presentation_invariant"] is True
        assert sector["runtime_descent_conclusion"] == DESCENT_AUTHORIZED
        assert sector["presentation_local_differences_ignored_by_invariant_projection"] is True
        assert out["dependent_origination_boundary"]["provider_equality_required"] is False
        assert out["dependent_origination_boundary"]["raw_observation_equality_required"] is False
        assert out["dependent_origination_boundary"]["invariant_match_erases_presentation_dependence"] is True


def test_same_relation_different_invariant_obstructs() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        descent = descent_packet(
            presentations=[
                presentation(
                    "github",
                    "github_actions",
                    "a" * 64,
                    "2026-09-27T12:00:00Z",
                    "2026-09-27T12:00:10Z",
                ),
                presentation(
                    "vercel",
                    "vercel",
                    "b" * 64,
                    "2026-09-27T12:00:01Z",
                    "2026-09-27T12:00:11Z",
                ),
            ],
            members=["github", "vercel"],
        )
        invariants = invariant_input(
            descent,
            [
                invariant_row("github", {"terminal_class": "success"}),
                invariant_row("vercel", {"terminal_class": "failure"}),
            ],
        )
        write_case(root, descent, invariants)
        result = build_observability_presentation_invariance(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.obstructed_sector_count == 1
        assert result.obstruction_witness_count == 1

        out = json.loads((root / OUTPUT).read_text())
        sector = out["presentation_invariance_sectors"][0]
        assert sector["presentation_invariance_status"] == INVARIANCE_OBSTRUCTED
        assert sector["runtime_descent_conclusion"] == DESCENT_DENIED
        witness = out["obstruction_witnesses"][0]
        assert witness["obstruction_kind"] == "related_presentations_have_unequal_invariants"


def test_missing_invariant_holds_without_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        descent = descent_packet(
            presentations=[
                presentation(
                    "github",
                    "github_actions",
                    "a" * 64,
                    "2026-09-27T12:00:00Z",
                    "2026-09-27T12:00:10Z",
                ),
                presentation(
                    "vercel",
                    "vercel",
                    "b" * 64,
                    "2026-09-27T12:00:03Z",
                    "2026-09-27T12:00:12Z",
                ),
            ],
            members=["github", "vercel"],
        )
        invariants = invariant_input(
            descent,
            [
                invariant_row("github", {"terminal_class": "success"}),
                invariant_row("vercel", state="held"),
            ],
        )
        write_case(root, descent, invariants)
        result = build_observability_presentation_invariance(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.held_sector_count == 1
        assert result.obstruction_witness_count == 0

        out = json.loads((root / OUTPUT).read_text())
        sector = out["presentation_invariance_sectors"][0]
        assert sector["presentation_invariance_status"] == INVARIANCE_HELD
        assert sector["runtime_descent_conclusion"] == DESCENT_HELD


def test_preinvariant_v7_4_success_does_not_bypass_invariance() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        descent = descent_packet(
            presentations=[
                presentation("a", "github_actions", "a" * 64, "2026-09-27T12:00:00Z", "2026-09-27T12:00:05Z"),
                presentation("b", "vercel", "b" * 64, "2026-09-27T12:00:00Z", "2026-09-27T12:00:05Z"),
            ],
            members=["a", "b"],
            preinvariant_status="descended_contextual_presentation",
        )
        invariants = invariant_input(
            descent,
            [
                invariant_row("a", {"stable": 1}),
                invariant_row("b", {"stable": 2}),
            ],
        )
        write_case(root, descent, invariants)
        result = build_observability_presentation_invariance(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        sector = out["presentation_invariance_sectors"][0]
        assert sector["preinvariant_v7_4_status"] == "descended_contextual_presentation"
        assert sector["runtime_descent_conclusion"] == DESCENT_DENIED
        assert out["dependent_origination_boundary"]["v7_4_descent_status_is_preinvariance_candidate_only"] is True


def test_invariant_projection_must_be_uniform() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        descent = descent_packet(
            presentations=[
                presentation("a", "github_actions", "a" * 64, "2026-09-27T12:00:00Z", "2026-09-27T12:00:05Z"),
                presentation("b", "vercel", "b" * 64, "2026-09-27T12:00:00Z", "2026-09-27T12:00:05Z"),
            ],
            members=["a", "b"],
        )
        invariants = invariant_input(
            descent,
            [
                invariant_row("a", {"stable": True}),
                invariant_row("b", {"stable": True}),
            ],
            projection_id="projection-a",
        )
        p = plan(descent, invariants)
        p["invariant_projection_id"] = "projection-b"
        write_case(root, descent, invariants, override_plan=p)
        result = build_observability_presentation_invariance(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "invariant_projection_id_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def test_raw_invariant_values_not_persisted() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        descent = descent_packet(
            presentations=[
                presentation("a", "github_actions", "a" * 64, "2026-09-27T12:00:00Z", "2026-09-27T12:00:05Z"),
                presentation("b", "vercel", "b" * 64, "2026-09-27T12:00:00Z", "2026-09-27T12:00:05Z"),
            ],
            members=["a", "b"],
        )
        marker = "RAW-INVARIANT-MUST-NOT-PERSIST"
        invariants = invariant_input(
            descent,
            [
                invariant_row("a", {"value": marker}),
                invariant_row("b", {"value": marker}),
            ],
        )
        write_case(root, descent, invariants)
        result = build_observability_presentation_invariance(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY
        output_text = (root / OUTPUT).read_text()
        assert marker not in output_text


def main() -> int:
    test_different_presentations_same_invariant_descend()
    test_same_relation_different_invariant_obstructs()
    test_missing_invariant_holds_without_obstruction()
    test_preinvariant_v7_4_success_does_not_bypass_invariance()
    test_invariant_projection_must_be_uniform()
    test_raw_invariant_values_not_persisted()
    print("PASS: KuuOS Observability Presentation Invariance v7.7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
