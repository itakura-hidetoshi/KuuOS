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

from runtime.kuuos_runtime_samvrti_world_effect_update_v7_14 import (
    OBSTRUCTED,
    PARTIAL,
    READY,
    WORLD_COMPENSATION_OPEN,
    WORLD_HANDOVER_OPEN,
    WORLD_NO_EFFECT,
    WORLD_REOBSERVATION_OPEN,
    WORLD_TRANSITION_CONFIRMED,
    WORLD_UPDATE_OBSTRUCTED,
    build_samvrti_world_effect_update,
)
from runtime.kuuos_transactional_effect_scenarios_v0_24 import (
    _blocked_no_effect,
    _compensable,
    _confirmed,
    _handover,
    _reobserve,
)

PLAN = "samvrti_world_effect_update_plan_v7_14.json"
SOURCE = "action_effect_lineage_binding_packet_v7_13.json"
INPUT = "samvrti_world_effect_updates_input_v7_14.json"
OUTPUT = "samvrti_world_effect_update_packet_v7_14.json"


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def authority_packet() -> dict[str, Any]:
    return {
        "authority_status": "KUUOS_SAMVRTI_WORLD_EFFECT_UPDATE_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_lineage_packet_read_allowed": True,
        "world_update_input_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "samvrti_world_effect_update_enabled": True,
        "apply_samvrti_world_effect_update": True,
    }


def lineage_from_transaction(
    *,
    action_id: str,
    state_name: str,
    transaction: dict[str, Any],
    paramartha: str = "paramartha-shared",
    world_id: str = "world-A",
) -> dict[str, Any]:
    return {
        "action_id": action_id,
        "action_digest": sha({"action_id": action_id}),
        "source_action_route": "licensed_execution_candidate_exact_world",
        "semantic_subject_id": "subject-A",
        "paramartha_carrier_element_id": paramartha,
        "target_samvrti_world_id": world_id,
        "world_relation": "exact_world",
        "action_effect_lineage_state": state_name,
        "semantic_effect_binding_digest": sha(
            {"action_id": action_id, "binding": "fixture"}
        ),
        "act_id": str(transaction["transaction_intent"]["source_act_id"]),
        "prepared_act_state_digest": str(
            transaction["transaction_intent"]["source_prepared_act_state_digest"]
        ),
        "step_authorization_digest": str(
            transaction["transaction_intent"]["step_authorization_digest"]
        ),
        "capability_lease_digest": str(
            transaction["transaction_intent"]["capability_lease_digest"]
        ),
        "host_projection_digest": str(
            transaction["transaction_intent"]["host_projection_digest"]
        ),
        "transaction_intent_digest": str(
            transaction["transaction_intent_digest"]
        ),
        "transaction_state_digest": str(transaction["transaction_state_digest"]),
        "transaction_final_receipt_digest": str(
            transaction["transaction_final_receipt_digest"]
        ),
        "world_binding_evidence_digest": "a" * 64,
        "world_transfer_resolution_digest": "",
        "binding_errors": [],
        "binding_reasons": [],
        "semantic_route_grants_execution_authority": False,
        "binding_layer_executes_effect": False,
        "lower_receipts_remain_canonical": True,
    }


def source_packet(lineages: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_action_effect_lineage_binding_v7_13",
        "status": "KUUOS_ACTION_EFFECT_LINEAGE_BINDING_READY",
        "source_action_packet_digest": "b" * 64,
        "action_effect_lineages": lineages,
        "summary": {},
        "dependent_origination_effect_boundary": {
            "semantic_route_is_execution_authority": False,
            "binding_layer_executes_effect": False,
            "lower_actos_authorization_is_independently_validated": True,
            "capability_lease_is_independently_validated": True,
            "host_projection_is_independently_validated": True,
            "semantic_world_to_host_projection_binding_is_explicit": True,
            "prior_authority_pending_can_be_resolved_by_fresh_lower_authority": True,
            "prior_world_pending_can_be_resolved_by_new_world_witness": True,
            "transaction_outcome_refines_action_status_without_rewriting_source_semantics": True,
            "effect_confirmation_requires_transaction_reconciliation_and_verification": True,
            "compensation_proposal_requires_new_authorized_transaction": True,
            "lower_receipts_remain_canonical": True,
            "execution_success_implies_mission_success": False,
            "source_authority_transferred": False,
        },
    }


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_samvrti_world_effect_update_plan_v7_14",
        "source_lineage_packet_digest": sha(source),
        "read_only": True,
        "effect_confirmed_may_update_samvrti_world": True,
        "nonconfirmed_effect_may_fabricate_world_update": False,
        "world_update_may_change_paramartha_class": False,
        "effect_confirmed_implies_mission_success": False,
        "reconciliation_is_truth": False,
        "world_update_overwrites_history": False,
        "source_authority_transfer_allowed": False,
    }


def write_case(
    root: pathlib.Path,
    source: dict[str, Any],
    updates: list[dict[str, Any]],
) -> None:
    (root / SOURCE).write_text(json.dumps(source), encoding="utf-8")
    (root / PLAN).write_text(json.dumps(plan(source)), encoding="utf-8")
    (root / INPUT).write_text(
        json.dumps(
            {
                "version": "kuuos_samvrti_world_effect_updates_input_v7_14",
                "source_lineage_packet_digest": sha(source),
                "updates": updates,
            }
        ),
        encoding="utf-8",
    )


def update_for(
    lineage: dict[str, Any],
    transaction: dict[str, Any] | None,
    *,
    expected_paramartha: str | None = None,
) -> dict[str, Any]:
    return {
        "action_id": lineage["action_id"],
        "expected_paramartha_carrier_element_id": (
            expected_paramartha
            if expected_paramartha is not None
            else lineage["paramartha_carrier_element_id"]
        ),
        "transaction_state": transaction or {},
    }


def record_by_id(out: dict[str, Any], action_id: str) -> dict[str, Any]:
    return next(
        item
        for item in out["samvrti_world_effect_records"]
        if item["action_id"] == action_id
    )


def test_confirmed_effect_materializes_append_only_samvrti_world_version() -> None:
    with tempfile.TemporaryDirectory() as td:
        root_path = pathlib.Path(td)
        tx, _store, _event = _confirmed(root_path / "fixture")

        lineage = lineage_from_transaction(
            action_id="confirmed-action",
            state_name="effect_confirmed",
            transaction=tx,
        )
        source = source_packet([lineage])

        runtime_root = root_path / "runtime"
        runtime_root.mkdir()
        write_case(runtime_root, source, [update_for(lineage, tx)])

        result = build_samvrti_world_effect_update(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.confirmed_transition_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        assert len(out["materialized_samvrti_world_versions"]) == 1
        record = record_by_id(out, "confirmed-action")
        assert (
            record["samvrti_world_effect_state"]
            == WORLD_TRANSITION_CONFIRMED
        )
        transition = record["samvrti_world_transition"]
        receipt = tx["reconciliation_receipt"]
        assert (
            transition["prior_world_state_digest"]
            == receipt["prior_world_state_digest"]
        )
        assert (
            transition["observed_world_state_digest"]
            == receipt["observed_world_state_digest"]
        )
        assert (
            transition["observed_effect_digest"]
            == receipt["observed_effect_digest"]
        )
        assert (
            transition["paramartha_carrier_element_id_before"]
            == transition["paramartha_carrier_element_id_after"]
            == "paramartha-shared"
        )
        assert transition["paramartha_class_changed"] is False
        assert transition["mission_success"] == "undetermined"
        assert transition["mission_success_implied"] is False
        assert transition["world_transition_is_ultimate_truth"] is False
        assert out["two_truths_effect_return_boundary"][
            "samvrti_world_versions_are_append_only"
        ] is True


def test_reobservation_preserves_residue_without_world_version() -> None:
    with tempfile.TemporaryDirectory() as td:
        root_path = pathlib.Path(td)
        tx = _reobserve(root_path / "fixture")
        lineage = lineage_from_transaction(
            action_id="reobserve-action",
            state_name="reobservation_required",
            transaction=tx,
        )
        source = source_packet([lineage])
        runtime_root = root_path / "runtime"
        runtime_root.mkdir()
        write_case(runtime_root, source, [update_for(lineage, tx)])

        result = build_samvrti_world_effect_update(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.reobservation_open_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        assert out["materialized_samvrti_world_versions"] == []
        record = record_by_id(out, "reobserve-action")
        assert record["samvrti_world_effect_state"] == WORLD_REOBSERVATION_OPEN
        assert record["samvrti_world_transition"] == {}
        assert record["world_transition_residue_digest"]


def test_compensation_and_handover_do_not_fake_world_rollback() -> None:
    with tempfile.TemporaryDirectory() as td:
        root_path = pathlib.Path(td)
        compensation_tx = _compensable(root_path / "comp")
        handover_tx = _handover(root_path / "handover")

        comp = lineage_from_transaction(
            action_id="comp-action",
            state_name="compensation_proposed",
            transaction=compensation_tx,
        )
        hand = lineage_from_transaction(
            action_id="handover-action",
            state_name="handover_required",
            transaction=handover_tx,
        )
        source = source_packet([comp, hand])

        runtime_root = root_path / "runtime"
        runtime_root.mkdir()
        write_case(
            runtime_root,
            source,
            [
                update_for(comp, compensation_tx),
                update_for(hand, handover_tx),
            ],
        )

        result = build_samvrti_world_effect_update(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.compensation_open_count == 1
        assert result.handover_open_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        assert out["materialized_samvrti_world_versions"] == []
        assert (
            record_by_id(out, "comp-action")["samvrti_world_effect_state"]
            == WORLD_COMPENSATION_OPEN
        )
        assert (
            record_by_id(out, "handover-action")["samvrti_world_effect_state"]
            == WORLD_HANDOVER_OPEN
        )
        assert out["two_truths_effect_return_boundary"][
            "compensation_proposal_is_not_world_rollback"
        ] is True


def test_no_effect_recorded_produces_no_world_transition() -> None:
    with tempfile.TemporaryDirectory() as td:
        root_path = pathlib.Path(td)
        tx = _blocked_no_effect(root_path / "fixture")
        lineage = lineage_from_transaction(
            action_id="no-effect-action",
            state_name="no_effect_recorded",
            transaction=tx,
        )
        source = source_packet([lineage])

        runtime_root = root_path / "runtime"
        runtime_root.mkdir()
        write_case(runtime_root, source, [update_for(lineage, tx)])

        result = build_samvrti_world_effect_update(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.no_effect_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        assert out["materialized_samvrti_world_versions"] == []
        record = record_by_id(out, "no-effect-action")
        assert record["samvrti_world_effect_state"] == WORLD_NO_EFFECT
        assert record["samvrti_world_transition"] == {}


def test_paramartha_class_cannot_be_changed_by_world_update() -> None:
    with tempfile.TemporaryDirectory() as td:
        root_path = pathlib.Path(td)
        tx, _store, _event = _confirmed(root_path / "fixture")
        lineage = lineage_from_transaction(
            action_id="paramartha-change",
            state_name="effect_confirmed",
            transaction=tx,
        )
        source = source_packet([lineage])

        runtime_root = root_path / "runtime"
        runtime_root.mkdir()
        write_case(
            runtime_root,
            source,
            [
                update_for(
                    lineage,
                    tx,
                    expected_paramartha="different-paramartha",
                )
            ],
        )

        result = build_samvrti_world_effect_update(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.obstructed_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        record = record_by_id(out, "paramartha-change")
        assert record["samvrti_world_effect_state"] == WORLD_UPDATE_OBSTRUCTED
        assert "expected_paramartha_carrier_mismatch" in record["world_update_errors"]


def test_transaction_digest_mismatch_is_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root_path = pathlib.Path(td)
        tx, _store, _event = _confirmed(root_path / "fixture")
        lineage = lineage_from_transaction(
            action_id="digest-mismatch",
            state_name="effect_confirmed",
            transaction=tx,
        )
        lineage["transaction_state_digest"] = "0" * 64
        source = source_packet([lineage])

        runtime_root = root_path / "runtime"
        runtime_root.mkdir()
        write_case(runtime_root, source, [update_for(lineage, tx)])

        result = build_samvrti_world_effect_update(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()

        out = json.loads((runtime_root / OUTPUT).read_text())
        record = record_by_id(out, "digest-mismatch")
        assert record["samvrti_world_effect_state"] == WORLD_UPDATE_OBSTRUCTED
        assert "transaction_state_digest_mismatch" in record["world_update_errors"]


def main() -> int:
    test_confirmed_effect_materializes_append_only_samvrti_world_version()
    test_reobservation_preserves_residue_without_world_version()
    test_compensation_and_handover_do_not_fake_world_rollback()
    test_no_effect_recorded_produces_no_world_transition()
    test_paramartha_class_cannot_be_changed_by_world_update()
    test_transaction_digest_mismatch_is_obstruction()
    print("PASS: KuuOS Samvrti World Effect Update v7.14")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
