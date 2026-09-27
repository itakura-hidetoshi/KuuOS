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

from runtime.kuuos_runtime_observability_carrier_model_independence_v7_9 import (
    BLOCKED,
    MODEL_COMPLETE,
    MODEL_OBSTRUCTED,
    MODEL_PARTIAL,
    OBSTRUCTED,
    PAIR_EQUIVALENT,
    PAIR_HELD,
    PAIR_OBSTRUCTED,
    PARTIAL,
    READY,
    build_observability_carrier_model_independence,
)

PLAN = "observability_carrier_model_independence_plan_v7_9.json"
SOURCE = "observability_invariant_carrier_packet_v7_8.json"
MODELS = "observability_carrier_models_input_v7_9.json"
OUTPUT = "observability_carrier_model_independence_packet_v7_9.json"


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
        "authority_status": "KUUOS_OBSERVABILITY_CARRIER_MODEL_INDEPENDENCE_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_carrier_packet_read_allowed": True,
        "models_input_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "observability_carrier_model_independence_enabled": True,
        "apply_observability_carrier_model_independence": True,
    }


def source_packet() -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_observability_invariant_carrier_v7_8",
        "status": "KUUOS_OBSERVABILITY_INVARIANT_CARRIER_READY",
        "source_invariance_packet_digest": "a" * 64,
        "invariant_projection_id": "kuuos-release-invariant-v1",
        "invariant_schema_digest": "b" * 64,
        "carrier_elements": [
            {
                "carrier_element_id": "carrier-A",
                "invariant_digest": "1" * 64,
                "presentation_witness_ids": ["github-a", "vercel-a"],
                "presentation_witness_count": 2,
                "carrier_identity_uses_presentation_id": False,
                "carrier_identity_uses_sector_id": False,
                "carrier_identity_uses_provider": False,
                "carrier_element_is_substance": False,
            },
            {
                "carrier_element_id": "carrier-B",
                "invariant_digest": "2" * 64,
                "presentation_witness_ids": ["github-b"],
                "presentation_witness_count": 1,
                "carrier_identity_uses_presentation_id": False,
                "carrier_identity_uses_sector_id": False,
                "carrier_identity_uses_provider": False,
                "carrier_element_is_substance": False,
            },
        ],
        "canonical_presentation_map": [],
        "sector_factorizations": [],
        "summary": {
            "presentation_count": 3,
            "carrier_element_count": 2,
        },
        "dependent_origination_boundary": {
            "same_invariant_same_carrier_element": True,
            "carrier_identity_depends_only_on_invariant": True,
            "presentation_id_affects_carrier_identity": False,
            "sector_id_affects_carrier_identity": False,
            "provider_affects_carrier_identity": False,
            "presentation_local_differences_erased_after_invariance": True,
            "carrier_preserves_invariant_not_presentation": True,
            "carrier_element_is_substance": False,
            "canonical_map_is_runtime_construction_not_formal_universality_proof": True,
            "source_authority_transferred": False,
            "python_formal_universality_authority": False,
            "formal_v2_0_universal_property_replaced": False,
        },
    }


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_carrier_model_independence_plan_v7_9",
        "source_carrier_packet_digest": sha(source),
        "invariant_projection_id": source["invariant_projection_id"],
        "invariant_schema_digest": source["invariant_schema_digest"],
        "read_only": True,
        "carrier_model_independence_required": True,
        "model_token_equality_required": False,
        "presentation_data_may_affect_model_equivalence": False,
        "formal_category_equivalence_claim_allowed": False,
        "source_authority_transfer_allowed": False,
        "python_is_formal_universality_authority": False,
        "max_model_token_bytes": 8192,
    }


def models_packet(
    source: dict[str, Any],
    models: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "version": "kuuos_observability_carrier_models_input_v7_9",
        "source_carrier_packet_digest": sha(source),
        "models": models,
    }


def model(
    model_id: str,
    mapping: list[tuple[str, Any]],
) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "elements": [
            {
                "carrier_element_id": carrier_id,
                "model_element_value": value,
            }
            for carrier_id, value in mapping
        ],
    }


def write_case(
    root: pathlib.Path,
    source: dict[str, Any],
    models: dict[str, Any],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / SOURCE).write_text(json.dumps(source), encoding="utf-8")
    (root / MODELS).write_text(json.dumps(models), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(source)),
        encoding="utf-8",
    )


def test_two_different_model_presentations_same_meaning() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        models = models_packet(
            source,
            [
                model(
                    "model-json",
                    [
                        ("carrier-A", {"code": "alpha"}),
                        ("carrier-B", {"code": "beta"}),
                    ],
                ),
                model(
                    "model-integer",
                    [
                        ("carrier-A", 101),
                        ("carrier-B", 202),
                    ],
                ),
            ],
        )
        write_case(root, source, models)

        result = build_observability_carrier_model_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == READY, result.to_dict()
        assert result.complete_model_count == 2
        assert result.equivalent_model_pair_count == 1

        out = json.loads((root / OUTPUT).read_text())
        pair = out["carrier_model_pairs"][0]
        assert pair["pair_status"] == PAIR_EQUIVALENT
        assert pair["same_invariant_meaning"] is True
        assert pair["model_token_equality_required"] is False
        assert pair["presentation_data_used_for_equivalence"] is False
        assert pair["finite_runtime_bijection_witness"] is True
        assert len(pair["carrier_correspondences"]) == 2
        assert out["dependent_origination_boundary"]["same_invariant_meaning_independent_of_carrier_model_tokens"] is True


def test_model_token_rename_does_not_change_semantic_signature() -> None:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        root1 = pathlib.Path(td1)
        root2 = pathlib.Path(td2)
        source = source_packet()

        models1 = models_packet(
            source,
            [
                model("left", [("carrier-A", "x"), ("carrier-B", "y")]),
                model("right", [("carrier-A", "u"), ("carrier-B", "v")]),
            ],
        )
        models2 = models_packet(
            source,
            [
                model("renamed-1", [("carrier-A", "totally-new-a"), ("carrier-B", "totally-new-b")]),
                model("renamed-2", [("carrier-A", {"n": 1}), ("carrier-B", {"n": 2})]),
            ],
        )

        write_case(root1, source, models1)
        write_case(root2, source, models2)

        r1 = build_observability_carrier_model_independence(
            runtime_context=ctx(root1),
            authority_packet=authority(),
        )
        r2 = build_observability_carrier_model_independence(
            runtime_context=ctx(root2),
            authority_packet=authority(),
        )
        assert r1.status == READY
        assert r2.status == READY

        out1 = json.loads((root1 / OUTPUT).read_text())
        out2 = json.loads((root2 / OUTPUT).read_text())
        assert out1["semantic_carrier_signature"] == out2["semantic_carrier_signature"]
        assert out1["canonical_carrier_elements"] == out2["canonical_carrier_elements"]


def test_model_collapsing_distinct_invariants_is_obstructed() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        models = models_packet(
            source,
            [
                model(
                    "good-model",
                    [("carrier-A", "a"), ("carrier-B", "b")],
                ),
                model(
                    "bad-model",
                    [("carrier-A", "same"), ("carrier-B", "same")],
                ),
            ],
        )
        write_case(root, source, models)

        result = build_observability_carrier_model_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.obstructed_model_count == 1
        assert result.obstructed_model_pair_count == 1

        out = json.loads((root / OUTPUT).read_text())
        bad = next(
            item for item in out["carrier_models"]
            if item["model_id"] == "bad-model"
        )
        assert bad["model_status"] == MODEL_OBSTRUCTED
        assert bad["collision_witness_count"] == 1
        assert bad["collision_witnesses"][0]["obstruction_kind"] == "model_collapses_distinct_invariants"
        pair = out["carrier_model_pairs"][0]
        assert pair["pair_status"] == PAIR_OBSTRUCTED


def test_partial_model_holds_equivalence_open() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        models = models_packet(
            source,
            [
                model(
                    "complete-model",
                    [("carrier-A", "a"), ("carrier-B", "b")],
                ),
                model(
                    "partial-model",
                    [("carrier-A", "only-a")],
                ),
            ],
        )
        write_case(root, source, models)

        result = build_observability_carrier_model_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.partial_model_count == 1
        assert result.held_model_pair_count == 1

        out = json.loads((root / OUTPUT).read_text())
        partial = next(
            item for item in out["carrier_models"]
            if item["model_id"] == "partial-model"
        )
        assert partial["model_status"] == MODEL_PARTIAL
        assert partial["missing_carrier_element_ids"] == ["carrier-B"]
        pair = out["carrier_model_pairs"][0]
        assert pair["pair_status"] == PAIR_HELD


def test_presentation_witness_changes_do_not_change_semantic_signature() -> None:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        root1 = pathlib.Path(td1)
        root2 = pathlib.Path(td2)
        source1 = source_packet()
        source2 = source_packet()
        source2["carrier_elements"][0]["presentation_witness_ids"] = [
            "different-provider-x",
            "different-provider-y",
            "different-provider-z",
        ]
        source2["carrier_elements"][0]["presentation_witness_count"] = 3

        models1 = models_packet(
            source1,
            [
                model("m1", [("carrier-A", "a"), ("carrier-B", "b")]),
                model("m2", [("carrier-A", "c"), ("carrier-B", "d")]),
            ],
        )
        models2 = models_packet(
            source2,
            [
                model("m1", [("carrier-A", "a"), ("carrier-B", "b")]),
                model("m2", [("carrier-A", "c"), ("carrier-B", "d")]),
            ],
        )

        write_case(root1, source1, models1)
        write_case(root2, source2, models2)

        r1 = build_observability_carrier_model_independence(
            runtime_context=ctx(root1),
            authority_packet=authority(),
        )
        r2 = build_observability_carrier_model_independence(
            runtime_context=ctx(root2),
            authority_packet=authority(),
        )
        assert r1.status == READY
        assert r2.status == READY

        out1 = json.loads((root1 / OUTPUT).read_text())
        out2 = json.loads((root2 / OUTPUT).read_text())
        assert out1["semantic_carrier_signature"] == out2["semantic_carrier_signature"]


def test_stale_models_source_binding_blocks() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        models = models_packet(
            source,
            [
                model("m1", [("carrier-A", "a"), ("carrier-B", "b")]),
                model("m2", [("carrier-A", "c"), ("carrier-B", "d")]),
            ],
        )
        models["source_carrier_packet_digest"] = "0" * 64
        write_case(root, source, models)

        result = build_observability_carrier_model_independence(
            runtime_context=ctx(root),
            authority_packet=authority(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "models_source_carrier_packet_digest_mismatch" in result.blockers
        assert not (root / OUTPUT).exists()


def main() -> int:
    test_two_different_model_presentations_same_meaning()
    test_model_token_rename_does_not_change_semantic_signature()
    test_model_collapsing_distinct_invariants_is_obstructed()
    test_partial_model_holds_equivalence_open()
    test_presentation_witness_changes_do_not_change_semantic_signature()
    test_stale_models_source_binding_blocks()
    print("PASS: KuuOS Observability Carrier Model Independence v7.9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
