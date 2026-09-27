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

from runtime.kuuos_runtime_action_effect_lineage_binding_v7_13 import (
    AUTHORIZED_PREPARED,
    AWAITING_LOWER_AUTHORITY,
    BINDING_OBSTRUCTED,
    COMPENSATION_PROPOSED,
    EFFECT_CONFIRMED,
    OBSTRUCTED,
    PARTIAL,
    READY,
    REOBSERVATION_REQUIRED,
    build_action_effect_lineage_binding,
)
from runtime.kuuos_transactional_effect_scenarios_v0_24 import (
    _compensable,
    _confirmed,
    _prepared_transaction,
    _reobserve,
)

PLAN = "action_effect_lineage_binding_plan_v7_13.json"
SOURCE = "middle_way_action_lifting_packet_v7_12.json"
INPUT = "action_effect_lineage_bindings_input_v7_13.json"
OUTPUT = "action_effect_lineage_binding_packet_v7_13.json"


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
        "authority_status": "KUUOS_ACTION_EFFECT_LINEAGE_BINDING_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_action_packet_read_allowed": True,
        "lineage_bindings_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "action_effect_lineage_binding_enabled": True,
        "apply_action_effect_lineage_binding": True,
    }


def assessment(
    action_id: str,
    *,
    route: str,
    target_world: str = "world-A",
    world_relation: str = "exact_world",
    world_dependence: str = "contextual",
) -> dict[str, Any]:
    action_digest = sha(
        {
            "action_id": action_id,
            "semantic_subject_id": "subject-A",
            "route_seed": route,
            "target_world": target_world,
        }
    )
    return {
        "action_id": action_id,
        "action_digest": action_digest,
        "semantic_subject_id": "subject-A",
        "paramartha_basis_stable": True,
        "paramartha_carrier_element_id": "paramartha-shared",
        "source_samvrti_world_id": "world-A",
        "target_samvrti_world_id": target_world,
        "world_relation": world_relation,
        "world_usable_for_requested_action": route
        not in {"world_transfer_or_reconciliation_required"},
        "world_dependence": world_dependence,
        "action_invariant_across_samvrti": False,
        "transfer_mode": "none",
        "transfer_witness_present": False,
        "direct_execution_requested": True,
        "action_class": "fixture-effect",
        "effect_mode": "reversible_effect",
        "estimated_risk": 0.1,
        "reversibility": 0.95,
        "recoverability": 0.95,
        "impact_radius": 0.1,
        "evidence_complete": True,
        "requires_human_review": False,
        "authority_state": "valid"
        if route.startswith("licensed_execution_candidate")
        else "absent",
        "fresh_authority": route.startswith("licensed_execution_candidate"),
        "authority_action_covered": route.startswith(
            "licensed_execution_candidate"
        ),
        "authority_world_covered": route.startswith(
            "licensed_execution_candidate"
        ),
        "authority_valid_for_action_and_world": route.startswith(
            "licensed_execution_candidate"
        ),
        "probe_authorized": False,
        "execution_fit": True,
        "bounded_probe_fit": True,
        "action_route": route,
        "execution_candidate": route.startswith(
            "licensed_execution_candidate"
        ),
        "reasons": [],
        "direct_execution_request_was_not_used_as_block_reason": True,
        "world_mismatch_was_not_used_as_automatic_block_reason": True,
        "paramartha_only_was_not_used_as_automatic_block_reason": True,
        "assessment_executes_action": False,
    }


def source_packet(actions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_middle_way_action_lifting_v7_12",
        "status": "KUUOS_MIDDLE_WAY_ACTION_LIFTING_READY",
        "source_two_truths_packet_digest": "a" * 64,
        "action_assessments": actions,
        "summary": {},
        "middle_way_action_boundary": {
            "direct_execution_request_is_block_reason": False,
            "paramartha_only_action_is_automatically_blocked": False,
            "world_binding_mismatch_is_automatically_blocked": False,
            "fresh_external_authority_required_for_effect": True,
            "paramartha_meaning_does_not_grant_execution_authority": True,
            "world_transfer_witness_can_support_cross_world_lifting": True,
            "world_invariant_action_can_cross_samvrti_presentations": True,
            "bounded_reversible_probe_can_resolve_world_uncertainty": True,
            "direct_execution_request_can_become_licensed_candidate": True,
            "runtime_assessment_executes_action": False,
            "transactional_effect_reconciliation_still_required_after_effect": True,
            "execution_success_does_not_imply_mission_success": True,
        },
    }


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_action_effect_lineage_binding_plan_v7_13",
        "source_action_packet_digest": sha(source),
        "read_only": True,
        "semantic_route_is_execution_authority": False,
        "binding_layer_executes_effect": False,
        "lower_authority_can_resolve_prior_authority_pending": True,
        "new_world_witness_can_resolve_prior_world_pending": True,
        "transaction_outcome_may_refine_action_status": True,
        "execution_success_implies_mission_success": False,
        "source_authority_transfer_allowed": False,
    }


def binding_for_prepared(
    action: dict[str, Any],
    prepared_act: dict[str, Any],
    *,
    world_resolution: str = "",
) -> dict[str, Any]:
    return {
        "action_id": action["action_id"],
        "expected_action_digest": action["action_digest"],
        "mapped_operation_id": prepared_act["operation_id"],
        "mapped_operation_input_digest": prepared_act[
            "operation_input_digest"
        ],
        "intended_effect_digest": "",
        "world_binding_evidence_digest": "b" * 64
        if action["world_dependence"] != "none"
        else "",
        "world_transfer_resolution_digest": world_resolution,
        "explicit_reassessment_authorized": False,
        "prepared_act_state": prepared_act,
        "transaction_state": {},
    }


def binding_for_transaction(
    action: dict[str, Any],
    transaction: dict[str, Any],
) -> dict[str, Any]:
    intent = transaction["transaction_intent"]
    return {
        "action_id": action["action_id"],
        "expected_action_digest": action["action_digest"],
        "mapped_operation_id": intent["operation_id"],
        "mapped_operation_input_digest": intent["operation_input_digest"],
        "intended_effect_digest": intent["intended_effect_digest"],
        "world_binding_evidence_digest": "c" * 64
        if action["world_dependence"] != "none"
        else "",
        "world_transfer_resolution_digest": "",
        "explicit_reassessment_authorized": False,
        "prepared_act_state": {},
        "transaction_state": transaction,
    }


def write_case(
    root: pathlib.Path,
    source: dict[str, Any],
    bindings: list[dict[str, Any]],
) -> None:
    (root / SOURCE).write_text(json.dumps(source), encoding="utf-8")
    (root / PLAN).write_text(json.dumps(plan(source)), encoding="utf-8")
    (root / INPUT).write_text(
        json.dumps(
            {
                "version": "kuuos_action_effect_lineage_bindings_input_v7_13",
                "source_action_packet_digest": sha(source),
                "bindings": bindings,
            }
        ),
        encoding="utf-8",
    )


def record_by_id(out: dict[str, Any], action_id: str) -> dict[str, Any]:
    return next(
        item
        for item in out["action_effect_lineages"]
        if item["action_id"] == action_id
    )


def test_real_prepared_act_state_exact_binding() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture_root = pathlib.Path(td) / "fixture"
        (
            _policy,
            _bundle,
            _license,
            prepared_act,
            _act_store,
            _connector,
            _intent,
            _store,
        ) = _prepared_transaction(
            fixture_root,
            transaction_id="v713-prepared",
            compensation_mode="explicit_operation",
        )

        action = assessment(
            "action-prepared",
            route="licensed_execution_candidate_exact_world",
        )
        source = source_packet([action])

        runtime_root = pathlib.Path(td) / "runtime"
        runtime_root.mkdir()
        write_case(
            runtime_root,
            source,
            [binding_for_prepared(action, prepared_act)],
        )

        result = build_action_effect_lineage_binding(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.authorized_prepared_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        record = record_by_id(out, "action-prepared")
        assert record["action_effect_lineage_state"] == AUTHORIZED_PREPARED
        assert (
            record["step_authorization_digest"]
            == prepared_act["step_authorization_digest"]
        )
        assert (
            record["capability_lease_digest"]
            == prepared_act["host_license_digest"]
        )
        assert (
            record["host_projection_digest"]
            == prepared_act["host_projection_digest"]
        )
        assert record["semantic_route_grants_execution_authority"] is False
        assert record["binding_layer_executes_effect"] is False


def test_prior_authority_pending_can_advance_when_real_actos_authority_arrives() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture_root = pathlib.Path(td) / "fixture"
        (
            _policy,
            _bundle,
            _license,
            prepared_act,
            _act_store,
            _connector,
            _intent,
            _store,
        ) = _prepared_transaction(
            fixture_root,
            transaction_id="v713-authority-resolution",
            compensation_mode="explicit_operation",
        )

        action = assessment(
            "action-authority-pending",
            route="fresh_authority_required",
        )
        source = source_packet([action])

        runtime_root = pathlib.Path(td) / "runtime"
        runtime_root.mkdir()
        write_case(
            runtime_root,
            source,
            [binding_for_prepared(action, prepared_act)],
        )

        result = build_action_effect_lineage_binding(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()

        out = json.loads((runtime_root / OUTPUT).read_text())
        record = record_by_id(out, "action-authority-pending")
        assert record["action_effect_lineage_state"] == AUTHORIZED_PREPARED
        assert (
            "prior_authority_pending_resolved_by_valid_lower_artifact"
            in record["binding_reasons"]
        )


def test_authority_pending_without_lower_artifact_remains_partial_not_rejected() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        action = assessment(
            "action-awaiting",
            route="fresh_authority_required",
        )
        source = source_packet([action])
        binding = {
            "action_id": action["action_id"],
            "expected_action_digest": action["action_digest"],
            "mapped_operation_id": "fixture.success",
            "mapped_operation_input_digest": "d" * 64,
            "intended_effect_digest": "",
            "world_binding_evidence_digest": "e" * 64,
            "world_transfer_resolution_digest": "",
            "explicit_reassessment_authorized": False,
            "prepared_act_state": {},
            "transaction_state": {},
        }
        write_case(root, source, [binding])

        result = build_action_effect_lineage_binding(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == PARTIAL, result.to_dict()
        assert result.awaiting_count == 1

        out = json.loads((root / OUTPUT).read_text())
        record = record_by_id(out, "action-awaiting")
        assert (
            record["action_effect_lineage_state"]
            == AWAITING_LOWER_AUTHORITY
        )
        assert record["binding_errors"] == []


def test_real_confirmed_transaction_refines_to_effect_confirmed() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture_root = pathlib.Path(td) / "fixture"
        committed, _store, _event = _confirmed(fixture_root)

        action = assessment(
            "action-confirmed",
            route="licensed_execution_candidate_exact_world",
        )
        source = source_packet([action])

        runtime_root = pathlib.Path(td) / "runtime"
        runtime_root.mkdir()
        write_case(
            runtime_root,
            source,
            [binding_for_transaction(action, committed)],
        )

        result = build_action_effect_lineage_binding(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.effect_confirmed_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        record = record_by_id(out, "action-confirmed")
        assert record["action_effect_lineage_state"] == EFFECT_CONFIRMED
        assert record["transaction_final_receipt_digest"]
        assert out["dependent_origination_effect_boundary"][
            "effect_confirmation_requires_transaction_reconciliation_and_verification"
        ] is True
        assert out["dependent_origination_effect_boundary"][
            "execution_success_implies_mission_success"
        ] is False


def test_real_reobservation_and_compensation_routes_are_preserved() -> None:
    with tempfile.TemporaryDirectory() as td:
        root_path = pathlib.Path(td)
        reobserve_tx = _reobserve(root_path / "reobserve-fixture")
        compensation_tx = _compensable(root_path / "comp-fixture")

        a1 = assessment(
            "action-reobserve",
            route="licensed_execution_candidate_exact_world",
        )
        a2 = assessment(
            "action-compensate",
            route="licensed_execution_candidate_exact_world",
        )
        source = source_packet([a1, a2])

        runtime_root = root_path / "runtime"
        runtime_root.mkdir()
        write_case(
            runtime_root,
            source,
            [
                binding_for_transaction(a1, reobserve_tx),
                binding_for_transaction(a2, compensation_tx),
            ],
        )

        result = build_action_effect_lineage_binding(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.reobservation_required_count == 1
        assert result.compensation_proposed_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        assert (
            record_by_id(out, "action-reobserve")[
                "action_effect_lineage_state"
            ]
            == REOBSERVATION_REQUIRED
        )
        assert (
            record_by_id(out, "action-compensate")[
                "action_effect_lineage_state"
            ]
            == COMPENSATION_PROPOSED
        )


def test_exact_operation_binding_mismatch_is_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture_root = pathlib.Path(td) / "fixture"
        (
            _policy,
            _bundle,
            _license,
            prepared_act,
            _act_store,
            _connector,
            _intent,
            _store,
        ) = _prepared_transaction(
            fixture_root,
            transaction_id="v713-mismatch",
            compensation_mode="explicit_operation",
        )

        action = assessment(
            "action-mismatch",
            route="licensed_execution_candidate_exact_world",
        )
        source = source_packet([action])
        binding = binding_for_prepared(action, prepared_act)
        binding["mapped_operation_id"] = "different.operation"

        runtime_root = pathlib.Path(td) / "runtime"
        runtime_root.mkdir()
        write_case(runtime_root, source, [binding])

        result = build_action_effect_lineage_binding(
            runtime_context=ctx(runtime_root),
            authority_packet=authority_packet(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.obstructed_count == 1

        out = json.loads((runtime_root / OUTPUT).read_text())
        record = record_by_id(out, "action-mismatch")
        assert record["action_effect_lineage_state"] == BINDING_OBSTRUCTED
        assert "operation_id_mismatch" in record["binding_errors"]


def main() -> int:
    test_real_prepared_act_state_exact_binding()
    test_prior_authority_pending_can_advance_when_real_actos_authority_arrives()
    test_authority_pending_without_lower_artifact_remains_partial_not_rejected()
    test_real_confirmed_transaction_refines_to_effect_confirmed()
    test_real_reobservation_and_compensation_routes_are_preserved()
    test_exact_operation_binding_mismatch_is_obstruction()
    print("PASS: KuuOS Action-Effect Lineage Binding v7.13")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
