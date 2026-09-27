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

from runtime.kuuos_runtime_two_truths_noncollapse_v7_11 import (
    BLOCKED,
    PARTIAL,
    READY,
    SAME_PARAMARTHA_DISTINCT_SAMVRTI,
    SAME_PARAMARTHA_SAME_SAMVRTI,
    SAME_PARAMARTHA_SAMVRTI_UNRESOLVED,
    build_two_truths_noncollapse,
)

PLAN = "two_truths_noncollapse_plan_v7_11.json"
SOURCE = "invariant_projection_choice_independence_packet_v7_10.json"
SAMVRTI = "two_truths_samvrti_worlds_input_v7_11.json"
OUTPUT = "two_truths_noncollapse_packet_v7_11.json"


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
        "authority_status": "KUUOS_TWO_TRUTHS_NONCOLLAPSE_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_choice_packet_read_allowed": True,
        "samvrti_input_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "two_truths_noncollapse_enabled": True,
        "apply_two_truths_noncollapse": True,
    }


def source_packet() -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_invariant_projection_choice_independence_v7_10",
        "status": "KUUOS_INVARIANT_PROJECTION_CHOICE_INDEPENDENCE_READY",
        "normalized_observable_id": "kuuos-normalized-meaning-v1",
        "normalized_schema_digest": "a" * 64,
        "projection_presentations": [],
        "semantic_subjects": [
            {
                "semantic_subject_id": "subject-A",
                "projection_choice_status": "projection_choice_invariant",
                "projection_presentations": [],
                "projection_count": 2,
                "distinct_local_invariant_digest_count": 2,
                "local_invariants_may_differ": True,
                "normalized_observable_digest": "1" * 64,
                "choice_independent_carrier_element_id": "paramartha-shared",
                "projection_id_defines_semantic_identity": False,
                "local_invariant_equality_required": False,
                "normalized_observable_defines_choice_independent_meaning": True,
            },
            {
                "semantic_subject_id": "subject-B",
                "projection_choice_status": "projection_choice_invariant",
                "projection_presentations": [],
                "projection_count": 2,
                "distinct_local_invariant_digest_count": 2,
                "local_invariants_may_differ": True,
                "normalized_observable_digest": "1" * 64,
                "choice_independent_carrier_element_id": "paramartha-shared",
                "projection_id_defines_semantic_identity": False,
                "local_invariant_equality_required": False,
                "normalized_observable_defines_choice_independent_meaning": True,
            },
            {
                "semantic_subject_id": "subject-C",
                "projection_choice_status": "projection_choice_invariant",
                "projection_presentations": [],
                "projection_count": 2,
                "distinct_local_invariant_digest_count": 1,
                "local_invariants_may_differ": True,
                "normalized_observable_digest": "2" * 64,
                "choice_independent_carrier_element_id": "paramartha-other",
                "projection_id_defines_semantic_identity": False,
                "local_invariant_equality_required": False,
                "normalized_observable_defines_choice_independent_meaning": True,
            },
        ],
        "choice_independent_carrier_element_ids": [
            "paramartha-other",
            "paramartha-shared",
        ],
        "obstruction_witnesses": [],
        "summary": {},
        "dependent_origination_boundary": {
            "projection_choice_is_presentation": True,
            "projection_id_defines_semantic_identity": False,
            "local_invariant_equality_required": False,
            "different_local_invariants_may_share_normalized_meaning": True,
            "normalized_observable_defines_choice_independent_meaning": True,
            "choice_independent_carrier_identity_ignores_projection_id": True,
            "normalization_choice_is_substance": False,
            "normalized_observable_is_ultimate_truth": False,
            "formal_normalization_equivalence_claimed": False,
            "source_authority_transferred": False,
            "python_formal_theorem_authority": False,
            "formal_v1_28_normalization_choice_theorem_replaced": False,
        },
    }


def world(
    subject_id: str,
    world_id: str,
    conventional_value: Any = None,
    *,
    state: str = "observed",
    scope: Any = None,
    conditions: Any = None,
    governance_boundary: Any = None,
    action_constraints: Any = None,
    visible_residuals: Any = None,
    lineage_char: str = "b",
) -> dict[str, Any]:
    return {
        "semantic_subject_id": subject_id,
        "samvrti_world_id": world_id,
        "samvrti_state": state,
        "conventional_operational_value": (
            conventional_value if state == "observed" else None
        ),
        "scope": scope,
        "conditions": conditions,
        "governance_boundary": governance_boundary,
        "action_constraints": action_constraints,
        "visible_residuals": visible_residuals,
        "lineage_digest": lineage_char * 64 if state == "observed" else "",
    }


def samvrti_packet(
    source: dict[str, Any],
    worlds: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "version": "kuuos_two_truths_samvrti_worlds_input_v7_11",
        "source_choice_packet_digest": sha(source),
        "world_presentations": worlds,
    }


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_two_truths_noncollapse_plan_v7_11",
        "source_choice_packet_digest": sha(source),
        "read_only": True,
        "two_truths_noncollapse_required": True,
        "paramartha_equivalence_may_erase_samvrti_difference": False,
        "samvrti_difference_is_error": False,
        "conventional_substitution_requires_samvrti_equivalence": True,
        "paramartha_carrier_is_ultimate_substance": False,
        "source_authority_transfer_allowed": False,
        "max_samvrti_value_bytes": 16384,
    }


def write_case(
    root: pathlib.Path,
    source: dict[str, Any],
    samvrti: dict[str, Any],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / SOURCE).write_text(json.dumps(source), encoding="utf-8")
    (root / SAMVRTI).write_text(json.dumps(samvrti), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(source)),
        encoding="utf-8",
    )


def test_same_paramartha_distinct_samvrti_is_valid_noncollapse() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()

        worlds = samvrti_packet(
            source,
            [
                world(
                    "subject-A",
                    "clinical-world",
                    {"action": "treat"},
                    scope={"domain": "clinical"},
                    conditions=["patient-present"],
                    governance_boundary={"authority": "clinical"},
                    action_constraints=["consent-required"],
                    visible_residuals=["uncertainty"],
                    lineage_char="c",
                ),
                world(
                    "subject-B",
                    "research-world",
                    {"action": "analyze"},
                    scope={"domain": "research"},
                    conditions=["dataset-present"],
                    governance_boundary={"authority": "research"},
                    action_constraints=["no-direct-care"],
                    visible_residuals=["external-validity"],
                    lineage_char="d",
                ),
                world(
                    "subject-C",
                    "other-world",
                    {"action": "observe"},
                    scope={"domain": "other"},
                    conditions=["other"],
                    governance_boundary={"authority": "other"},
                    action_constraints=["other"],
                    visible_residuals=["other"],
                    lineage_char="e",
                ),
            ],
        )
        write_case(root, source, worlds)

        result = build_two_truths_noncollapse(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.same_paramartha_distinct_samvrti_count == 1

        out = json.loads((root / OUTPUT).read_text())
        pair = next(
            p
            for p in out["two_truths_relations"]
            if {
                p["left_semantic_subject_id"],
                p["right_semantic_subject_id"],
            }
            == {"subject-A", "subject-B"}
        )
        assert pair["two_truths_relation"] == SAME_PARAMARTHA_DISTINCT_SAMVRTI
        assert pair["same_paramartha_meaning"] is True
        assert pair["conventional_substitution_allowed"] is False
        assert pair["samvrti_distinction_required"] is True
        assert pair["samvrti_difference_is_error"] is False
        assert out["two_truths_boundary"]["same_paramartha_does_not_imply_conventional_substitutability"] is True


def test_same_paramartha_same_samvrti_allows_conventional_substitution() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        common = {
            "action": "observe",
            "state": "stable",
        }
        common_scope = {"domain": "shared"}
        common_conditions = ["same-condition"]
        common_governance = {"authority": "same"}
        common_constraints = ["same-constraint"]
        common_residuals = ["same-residual"]

        worlds = samvrti_packet(
            source,
            [
                world(
                    "subject-A",
                    "world-label-A",
                    common,
                    scope=common_scope,
                    conditions=common_conditions,
                    governance_boundary=common_governance,
                    action_constraints=common_constraints,
                    visible_residuals=common_residuals,
                    lineage_char="f",
                ),
                world(
                    "subject-B",
                    "world-label-B",
                    common,
                    scope=common_scope,
                    conditions=common_conditions,
                    governance_boundary=common_governance,
                    action_constraints=common_constraints,
                    visible_residuals=common_residuals,
                    lineage_char="f",
                ),
                world(
                    "subject-C",
                    "other-world",
                    {"action": "other"},
                    scope={"domain": "other"},
                    conditions=["other"],
                    governance_boundary={"authority": "other"},
                    action_constraints=["other"],
                    visible_residuals=["other"],
                    lineage_char="1",
                ),
            ],
        )
        write_case(root, source, worlds)

        result = build_two_truths_noncollapse(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.same_paramartha_same_samvrti_count == 1

        out = json.loads((root / OUTPUT).read_text())
        pair = next(
            p
            for p in out["two_truths_relations"]
            if {
                p["left_semantic_subject_id"],
                p["right_semantic_subject_id"],
            }
            == {"subject-A", "subject-B"}
        )
        assert pair["two_truths_relation"] == SAME_PARAMARTHA_SAME_SAMVRTI
        assert pair["conventional_substitution_allowed"] is True
        assert pair["samvrti_distinction_required"] is False


def test_same_paramartha_missing_samvrti_is_partial_not_collapse() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        worlds = samvrti_packet(
            source,
            [
                world(
                    "subject-A",
                    "world-A",
                    {"action": "observe"},
                    scope={"domain": "shared"},
                    conditions=["condition"],
                    governance_boundary={"authority": "shared"},
                    action_constraints=["constraint"],
                    visible_residuals=["residual"],
                    lineage_char="2",
                ),
                world(
                    "subject-B",
                    "world-B",
                    state="held",
                ),
                world(
                    "subject-C",
                    "world-C",
                    {"action": "other"},
                    scope={"domain": "other"},
                    conditions=["other"],
                    governance_boundary={"authority": "other"},
                    action_constraints=["other"],
                    visible_residuals=["other"],
                    lineage_char="3",
                ),
            ],
        )
        write_case(root, source, worlds)

        result = build_two_truths_noncollapse(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.unresolved_samvrti_pair_count == 1

        out = json.loads((root / OUTPUT).read_text())
        pair = next(
            p
            for p in out["two_truths_relations"]
            if {
                p["left_semantic_subject_id"],
                p["right_semantic_subject_id"],
            }
            == {"subject-A", "subject-B"}
        )
        assert pair["two_truths_relation"] == SAME_PARAMARTHA_SAMVRTI_UNRESOLVED
        assert pair["conventional_substitution_allowed"] is False


def test_world_label_alone_does_not_define_conventional_difference() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        common_kwargs = dict(
            conventional_value={"action": "same"},
            scope={"domain": "same"},
            conditions=["same"],
            governance_boundary={"authority": "same"},
            action_constraints=["same"],
            visible_residuals=["same"],
            lineage_char="4",
        )
        worlds = samvrti_packet(
            source,
            [
                world("subject-A", "label-one", **common_kwargs),
                world("subject-B", "label-two", **common_kwargs),
                world(
                    "subject-C",
                    "other",
                    {"action": "other"},
                    scope={"domain": "other"},
                    conditions=["other"],
                    governance_boundary={"authority": "other"},
                    action_constraints=["other"],
                    visible_residuals=["other"],
                    lineage_char="5",
                ),
            ],
        )
        write_case(root, source, worlds)

        result = build_two_truths_noncollapse(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY

        out = json.loads((root / OUTPUT).read_text())
        pair = next(
            p
            for p in out["two_truths_relations"]
            if {
                p["left_semantic_subject_id"],
                p["right_semantic_subject_id"],
            }
            == {"subject-A", "subject-B"}
        )
        assert pair["two_truths_relation"] == SAME_PARAMARTHA_SAME_SAMVRTI


def test_raw_conventional_values_not_persisted() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        marker = "RAW-CONVENTIONAL-MUST-NOT-PERSIST"
        worlds = samvrti_packet(
            source,
            [
                world(
                    "subject-A",
                    "world-A",
                    {"marker": marker},
                    scope={"domain": "A"},
                    conditions=["A"],
                    governance_boundary={"authority": "A"},
                    action_constraints=["A"],
                    visible_residuals=["A"],
                    lineage_char="6",
                ),
                world(
                    "subject-B",
                    "world-B",
                    {"marker": marker},
                    scope={"domain": "A"},
                    conditions=["A"],
                    governance_boundary={"authority": "A"},
                    action_constraints=["A"],
                    visible_residuals=["A"],
                    lineage_char="6",
                ),
                world(
                    "subject-C",
                    "world-C",
                    {"other": True},
                    scope={"domain": "C"},
                    conditions=["C"],
                    governance_boundary={"authority": "C"},
                    action_constraints=["C"],
                    visible_residuals=["C"],
                    lineage_char="7",
                ),
            ],
        )
        write_case(root, source, worlds)
        result = build_two_truths_noncollapse(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY
        assert marker not in (root / OUTPUT).read_text()


def test_stale_source_binding_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        worlds = samvrti_packet(source, [])
        worlds["source_choice_packet_digest"] = "0" * 64
        write_case(root, source, worlds)

        result = build_two_truths_noncollapse(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "samvrti_source_choice_packet_digest_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def main() -> int:
    test_same_paramartha_distinct_samvrti_is_valid_noncollapse()
    test_same_paramartha_same_samvrti_allows_conventional_substitution()
    test_same_paramartha_missing_samvrti_is_partial_not_collapse()
    test_world_label_alone_does_not_define_conventional_difference()
    test_raw_conventional_values_not_persisted()
    test_stale_source_binding_blocks()
    print("PASS: KuuOS Two Truths Non-collapse v7.11")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
