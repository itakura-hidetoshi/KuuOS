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

from runtime.kuuos_runtime_invariant_projection_choice_independence_v7_10 import (
    BLOCKED,
    CHOICE_HELD,
    CHOICE_INVARIANT,
    CHOICE_OBSTRUCTED,
    OBSTRUCTED,
    PARTIAL,
    READY,
    build_invariant_projection_choice_independence,
)

PLAN = "invariant_projection_choice_independence_plan_v7_10.json"
INPUT = "invariant_projection_family_input_v7_10.json"
OUTPUT = "invariant_projection_choice_independence_packet_v7_10.json"


def authority() -> dict[str, Any]:
    return {
        "authority_status": "KUUOS_INVARIANT_PROJECTION_CHOICE_INDEPENDENCE_AUTHORITY_READY",
        "plan_read_allowed": True,
        "projection_family_input_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "invariant_projection_choice_independence_enabled": True,
        "apply_invariant_projection_choice_independence": True,
    }


def projection(
    projection_id: str,
    subjects: list[dict[str, Any]],
    *,
    schema_char: str,
    certificate_char: str,
) -> dict[str, Any]:
    return {
        "projection_id": projection_id,
        "projection_schema_digest": schema_char * 64,
        "comparison_certificate_digest": certificate_char * 64,
        "subjects": subjects,
    }


def subject(
    subject_id: str,
    local_value: Any = None,
    normalized_value: Any = None,
    *,
    state: str = "observed",
) -> dict[str, Any]:
    return {
        "semantic_subject_id": subject_id,
        "invariant_state": state,
        "local_invariant_value": local_value if state == "observed" else None,
        "normalized_observable_value": (
            normalized_value if state == "observed" else None
        ),
    }


def packet(projections: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "kuuos_invariant_projection_family_input_v7_10",
        "normalized_observable_id": "kuuos-release-semantic-v1",
        "normalized_schema_digest": "f" * 64,
        "projections": projections,
    }


def plan(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_invariant_projection_choice_independence_plan_v7_10",
        "normalized_observable_id": value["normalized_observable_id"],
        "normalized_schema_digest": value["normalized_schema_digest"],
        "read_only": True,
        "projection_choice_independence_required": True,
        "local_invariant_equality_required": False,
        "projection_id_may_define_semantic_identity": False,
        "normalized_observable_defines_choice_independent_meaning": True,
        "formal_normalization_equivalence_claim_allowed": False,
        "source_authority_transfer_allowed": False,
        "python_is_formal_theorem_authority": False,
        "max_projections": 16,
        "max_value_bytes": 8192,
    }


def write_case(
    root: pathlib.Path,
    value: dict[str, Any],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / INPUT).write_text(json.dumps(value), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(value)),
        encoding="utf-8",
    )


def test_different_local_invariants_same_normalized_meaning() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        marker_a = "LOCAL-PRESENTATION-A"
        marker_b = "LOCAL-PRESENTATION-B"
        normalized = {"release": "same", "terminal": "success"}
        value = packet(
            [
                projection(
                    "projection-structured",
                    [
                        subject(
                            "deployment-1",
                            {"status": "success", "marker": marker_a},
                            normalized,
                        )
                    ],
                    schema_char="a",
                    certificate_char="1",
                ),
                projection(
                    "projection-numeric",
                    [
                        subject(
                            "deployment-1",
                            {"exit_code": 0, "marker": marker_b},
                            normalized,
                        )
                    ],
                    schema_char="b",
                    certificate_char="2",
                ),
            ]
        )
        write_case(root, value)

        result = build_invariant_projection_choice_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.choice_invariant_subject_count == 1
        assert result.normalized_carrier_element_count == 1

        output_text = (root / OUTPUT).read_text()
        assert marker_a not in output_text
        assert marker_b not in output_text
        out = json.loads(output_text)
        s = out["semantic_subjects"][0]
        assert s["projection_choice_status"] == CHOICE_INVARIANT
        assert s["distinct_local_invariant_digest_count"] == 2
        assert s["local_invariant_equality_required"] is False
        assert s["normalized_observable_defines_choice_independent_meaning"] is True
        assert s["choice_independent_carrier_element_id"]


def test_projection_rename_does_not_change_choice_independent_carrier() -> None:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        root1 = pathlib.Path(td1)
        root2 = pathlib.Path(td2)
        normalized = {"meaning": "M"}

        value1 = packet(
            [
                projection(
                    "projection-A",
                    [subject("subject", {"a": 1}, normalized)],
                    schema_char="c",
                    certificate_char="3",
                ),
                projection(
                    "projection-B",
                    [subject("subject", {"b": 2}, normalized)],
                    schema_char="d",
                    certificate_char="4",
                ),
            ]
        )
        value2 = packet(
            [
                projection(
                    "completely-renamed-X",
                    [subject("subject", {"x": 99}, normalized)],
                    schema_char="e",
                    certificate_char="5",
                ),
                projection(
                    "completely-renamed-Y",
                    [subject("subject", {"y": 100}, normalized)],
                    schema_char="6",
                    certificate_char="6",
                ),
            ]
        )
        write_case(root1, value1)
        write_case(root2, value2)

        r1 = build_invariant_projection_choice_independence(
            runtime_context=ctx(root1),
            authority_packet=authority(),
        )
        r2 = build_invariant_projection_choice_independence(
            runtime_context=ctx(root2),
            authority_packet=authority(),
        )
        assert r1.status == READY
        assert r2.status == READY

        out1 = json.loads((root1 / OUTPUT).read_text())
        out2 = json.loads((root2 / OUTPUT).read_text())
        assert (
            out1["semantic_subjects"][0]["choice_independent_carrier_element_id"]
            == out2["semantic_subjects"][0]["choice_independent_carrier_element_id"]
        )


def test_normalized_disagreement_is_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        value = packet(
            [
                projection(
                    "projection-A",
                    [
                        subject(
                            "subject",
                            {"status": "success"},
                            {"meaning": "success"},
                        )
                    ],
                    schema_char="7",
                    certificate_char="7",
                ),
                projection(
                    "projection-B",
                    [
                        subject(
                            "subject",
                            {"exit": 1},
                            {"meaning": "failure"},
                        )
                    ],
                    schema_char="8",
                    certificate_char="8",
                ),
            ]
        )
        write_case(root, value)

        result = build_invariant_projection_choice_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.obstructed_subject_count == 1

        out = json.loads((root / OUTPUT).read_text())
        s = out["semantic_subjects"][0]
        assert s["projection_choice_status"] == CHOICE_OBSTRUCTED
        witness = out["obstruction_witnesses"][0]
        assert (
            witness["obstruction_kind"]
            == "projection_choices_disagree_after_common_normalization"
        )


def test_missing_projection_value_holds_choice_open() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        normalized = {"meaning": "same"}
        value = packet(
            [
                projection(
                    "projection-A",
                    [subject("subject", {"a": 1}, normalized)],
                    schema_char="9",
                    certificate_char="9",
                ),
                projection(
                    "projection-B",
                    [subject("subject", state="held")],
                    schema_char="a",
                    certificate_char="a",
                ),
            ]
        )
        write_case(root, value)

        result = build_invariant_projection_choice_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.held_subject_count == 1

        out = json.loads((root / OUTPUT).read_text())
        assert out["semantic_subjects"][0]["projection_choice_status"] == CHOICE_HELD


def test_subject_missing_from_one_projection_holds_not_obstructs() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        value = packet(
            [
                projection(
                    "projection-A",
                    [
                        subject(
                            "subject",
                            {"a": 1},
                            {"meaning": "same"},
                        )
                    ],
                    schema_char="b",
                    certificate_char="b",
                ),
                projection(
                    "projection-B",
                    [],
                    schema_char="c",
                    certificate_char="c",
                ),
            ]
        )
        write_case(root, value)

        result = build_invariant_projection_choice_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.held_subject_count == 1
        assert result.obstructed_subject_count == 0


def test_normalized_observable_identity_must_match_plan() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        normalized = {"meaning": "same"}
        value = packet(
            [
                projection(
                    "A",
                    [subject("subject", {"a": 1}, normalized)],
                    schema_char="d",
                    certificate_char="d",
                ),
                projection(
                    "B",
                    [subject("subject", {"b": 2}, normalized)],
                    schema_char="e",
                    certificate_char="e",
                ),
            ]
        )
        p = plan(value)
        p["normalized_observable_id"] = "different-normalized-observable"
        write_case(root, value, override_plan=p)

        result = build_invariant_projection_choice_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "normalized_observable_id_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def main() -> int:
    test_different_local_invariants_same_normalized_meaning()
    test_projection_rename_does_not_change_choice_independent_carrier()
    test_normalized_disagreement_is_obstruction()
    test_missing_projection_value_holds_choice_open()
    test_subject_missing_from_one_projection_holds_not_obstructs()
    test_normalized_observable_identity_must_match_plan()
    print("PASS: KuuOS Invariant Projection Choice Independence v7.10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
