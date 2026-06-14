#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_process_tensor_activation_core_v0_4 import (
    activation_plan_digest,
    protected_structure_digest,
    sha,
    valid_digest,
    without,
)
from runtime.kuuos_runtime_daemon_indra_qi_process_tensor_activation_v0_4 import (
    build_indra_qi_process_tensor_activation_v0_4,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_causal_feedback_bridge_v0_3 import (
    feedback_plan,
    initialize_projection,
    latest,
    read_json,
    records,
    run_feedback,
    run_v14,
    write_json,
)

EXAMPLE = ROOT / "examples" / "indra_qi_process_tensor_activation_plan_v0_4.json"


def prepare_feedback(
    root: pathlib.Path,
    *,
    suffix: str,
    event_kind: str = "observe",
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    source, projection = initialize_projection(root, f"activation-{suffix}")
    transaction_id = f"activation-{suffix}-{event_kind}-event"
    run_v14(root, projection, kind=event_kind, transaction_id=transaction_id)
    plan = feedback_plan(root, source, projection, transaction_id, f"activation-{suffix}")
    result = run_feedback(root, plan)
    assert result["status"] == "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_READY", result
    packet = read_json(root / "indra_qi_causal_feedback_candidate_packet_v0_3.json")
    handoff = read_json(root / "indra_qi_causal_feedback_approval_handoff_v0_3.json")
    assert valid_digest(packet, "feedback_packet_digest")
    assert valid_digest(handoff, "approval_handoff_digest")
    return source, projection, packet, handoff


def build_plan(
    source: dict[str, Any],
    packet: dict[str, Any],
    handoff: dict[str, Any],
    *,
    suffix: str,
    approve_count: int = 2,
) -> dict[str, Any]:
    plan = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    candidates = packet["feedback_candidates"]
    decisions: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        approved = index < approve_count
        decisions.append(
            {
                "candidate_id": candidate["candidate_id"],
                "decision": "approve" if approved else "reject",
                "reason": (
                    "explicitly approved after process-history review"
                    if approved
                    else "reviewed and retained without WORLD mutation"
                ),
            }
        )
    plan.update(
        {
            "activation_id": f"indra-qi-process-tensor-activation-{suffix}",
            "source_feedback_id": packet["feedback_id"],
            "source_feedback_packet_digest": packet["feedback_packet_digest"],
            "source_approval_handoff_digest": handoff["approval_handoff_digest"],
            "source_indra_qi_world_state_digest": source["indra_qi_world_state_digest"],
            "review_decisions": decisions,
        }
    )
    plan["activation_plan_digest"] = activation_plan_digest(plan)
    return plan


def activation_license(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_LICENSE_READY",
        "bound_activation_plan_digest": plan["activation_plan_digest"],
        "source_feedback_packet_read_allowed": True,
        "source_approval_handoff_read_allowed": True,
        "world_state_read_allowed": True,
        "activation_plan_validate_allowed": True,
        "process_tensor_review_write_allowed": True,
        "rollback_snapshot_write_allowed": True,
        "runtime_observation_overlay_write_allowed": True,
        "world_state_write_allowed": True,
        "post_write_verification_allowed": True,
        "activation_record_write_allowed": True,
        "mutation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "allowed_mutation_scopes": ["runtime_observation_overlays_only"],
        "allowed_feedback_kinds": [
            "local_patch_observation_candidate",
            "qi_flow_observable_candidate",
        ],
        "max_approved_candidates": 3,
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_process_tensor_activation_v0_4_enabled": True,
        "apply_indra_qi_process_tensor_activation_v0_4": True,
    }


def run_activation(
    root: pathlib.Path,
    plan: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_process_tensor_activation_v0_4(
        runtime_context=context(root),
        activation_plan=plan,
        activation_license=license_value or activation_license(plan),
    ).to_dict()


def assert_world_unchanged(root: pathlib.Path, before: dict[str, Any]) -> None:
    after = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    assert after["indra_qi_world_state_digest"] == before["indra_qi_world_state_digest"]
    assert compute_indra_qi_world_state_digest(after) == before["indra_qi_world_state_digest"]


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        source, _, packet, handoff = prepare_feedback(root, suffix="success")
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        before_protected = protected_structure_digest(before)
        plan = build_plan(source, packet, handoff, suffix="success", approve_count=2)
        result = run_activation(root, plan)
        assert result["status"] == "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_READY", result
        assert result["activation_status"] == "process_tensor_activation_completed"
        assert result["reviewed_candidate_count"] == 3
        assert result["approved_candidate_count"] == 2
        assert result["rejected_candidate_count"] == 1
        assert result["overlays_applied"] == 2
        assert result["world_state_mutated"] is True
        assert result["rollback_snapshot_written"] is True
        assert result["rollback_performed"] is False
        assert result["protected_structure_preserved"] is True
        assert result["before_world_state_digest"] != result["after_world_state_digest"]

        after = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        review = read_json(root / "indra_qi_process_tensor_review_v0_4.json")
        activation = read_json(root / "indra_qi_process_tensor_activation_record_v0_4.json")
        ledger = latest(root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl")
        snapshot = read_json(
            root / f"indra_qi_world_rollback_snapshot_v0_4_{plan['activation_id']}.json"
        )
        overlays = after["runtime_observation_overlays"]

        assert compute_indra_qi_world_state_digest(after) == after["indra_qi_world_state_digest"]
        assert after["world_mutation_revision"] == 1
        assert after["last_process_tensor_activation_id"] == plan["activation_id"]
        assert len(overlays) == 2
        assert protected_structure_digest(after) == before_protected
        for field in (
            "core_statement",
            "causal_world_model_bridge",
            "local_world_patches",
            "indra_connections",
            "qi_flow_channels",
            "holonomy_cycles",
            "ku_string_correspondences",
            "extended_m_brane_surfaces",
            "mandala_inclusion",
            "two_truths_boundary",
            "governance_boundary",
        ):
            assert after[field] == before[field]

        assert overlays[0]["previous_overlay_digest"] == "GENESIS"
        assert overlays[1]["previous_overlay_digest"] == overlays[0]["overlay_digest"]
        assert all(valid_digest(overlay, "overlay_digest") for overlay in overlays)
        assert {overlay["feedback_kind"] for overlay in overlays} == {
            "local_patch_observation_candidate",
            "qi_flow_observable_candidate",
        }
        assert all(overlay["boundary"]["runtime_observation_overlay_only"] is True for overlay in overlays)
        assert all(overlay["boundary"]["gauge_connection_unchanged"] is True for overlay in overlays)

        assert valid_digest(review, "process_tensor_review_digest")
        assert review["review_status"] == "admissible"
        assert len(review["assessments"]) == 3
        for assessment in review["assessments"]:
            receipt = assessment["qi_process_tensor_receipt"]
            assert receipt["process_tensor_visible"] is True
            assert receipt["transition_continuity_visible"] is True
            assert receipt["memory_continuity_visible"] is True
            assert receipt["nonmarkov_memory_visible"] is True
            assert receipt["grants_execution_authority"] is False
            assert receipt["grants_truth_authority"] is False
            assert assessment["history_depth"] >= 3
            assert assessment["nonmarkov_link_density"] >= 0.5
            assert assessment["recoverability_branching_capacity"] >= 0.75
            assert assessment["observation_debt_pressure"] <= 0.1

        assert valid_digest(snapshot, "rollback_snapshot_digest")
        assert snapshot["world_state"]["indra_qi_world_state_digest"] == before[
            "indra_qi_world_state_digest"
        ]
        assert snapshot["protected_structure_digest"] == before_protected
        assert valid_digest(activation, "activation_record_digest")
        assert activation["process_tensor_review_digest"] == review["process_tensor_review_digest"]
        assert activation["after_world_state_digest"] == after["indra_qi_world_state_digest"]
        assert valid_digest(ledger, "record_digest")
        assert ledger["source_activation_record_digest"] == activation["activation_record_digest"]
        assert ledger["overlays_applied"] == 2

        ledger_count = len(records(root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl"))
        replay = run_activation(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "process_tensor_activation_id_replay" in replay["blockers"]
        assert "source_feedback_activation_replay" in replay["blockers"]
        assert len(records(root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl")) == ledger_count
        after_replay = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        assert after_replay["indra_qi_world_state_digest"] == after["indra_qi_world_state_digest"]

        root = base / "counterfactual-low-weight"
        source, _, packet, handoff = prepare_feedback(
            root,
            suffix="low-weight",
            event_kind="counterfactual",
        )
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="low-weight", approve_count=3)
        result = run_activation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert any(blocker.endswith("weight_below_policy") for blocker in result["blockers"])
        assert result["world_state_mutated"] is False
        assert result["rollback_snapshot_written"] is False
        assert_world_unchanged(root, before)

        root = base / "nonmarkov-density"
        source, _, packet, handoff = prepare_feedback(root, suffix="nonmarkov")
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="nonmarkov", approve_count=1)
        plan["process_tensor_policy"]["min_nonmarkov_link_density"] = 1.0
        plan["activation_plan_digest"] = activation_plan_digest(plan)
        result = run_activation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert any("nonmarkov_link_density_outside_policy" in blocker for blocker in result["blockers"])
        assert_world_unchanged(root, before)

        root = base / "context-missing"
        source, _, packet, handoff = prepare_feedback(root, suffix="context")
        packet_path = root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
        handoff_path = root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
        packet["source_process_tensor_context"]["memory_kernel_digest"] = ""
        packet["feedback_packet_digest"] = sha(without(packet, "feedback_packet_digest"))
        write_json(packet_path, packet)
        handoff["source_feedback_packet_digest"] = packet["feedback_packet_digest"]
        handoff["approval_handoff_digest"] = sha(without(handoff, "approval_handoff_digest"))
        write_json(handoff_path, handoff)
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="context", approve_count=1)
        result = run_activation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "source_feedback_process_context_memory_kernel_digest_missing" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "decision-set"
        source, _, packet, handoff = prepare_feedback(root, suffix="decisions")
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="decisions", approve_count=1)
        plan["review_decisions"] = plan["review_decisions"][:-1]
        plan["activation_plan_digest"] = activation_plan_digest(plan)
        result = run_activation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_review_decision_set_mismatch" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "license-digest"
        source, _, packet, handoff = prepare_feedback(root, suffix="license-digest")
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="license-digest", approve_count=1)
        result = run_activation(
            root,
            plan,
            activation_license(plan, bound_activation_plan_digest="mismatch"),
        )
        assert result["status"].endswith("BLOCKED")
        assert "activation_license_plan_digest_mismatch" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "candidate-limit"
        source, _, packet, handoff = prepare_feedback(root, suffix="candidate-limit")
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="candidate-limit", approve_count=2)
        result = run_activation(
            root,
            plan,
            activation_license(plan, max_approved_candidates=1),
        )
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_activation_approved_candidate_limit_exceeded" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "all-rejected"
        source, _, packet, handoff = prepare_feedback(root, suffix="all-rejected")
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="all-rejected", approve_count=0)
        result = run_activation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_activation_no_admissible_candidates" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "scope"
        source, _, packet, handoff = prepare_feedback(root, suffix="scope")
        before = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        plan = build_plan(source, packet, handoff, suffix="scope", approve_count=1)
        plan["mutation_scope"] = "gauge_connection_update"
        plan["activation_plan_digest"] = activation_plan_digest(plan)
        result = run_activation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_activation_mutation_scope_invalid" in result["blockers"]
        assert_world_unchanged(root, before)

    print("indra_qi_process_tensor_activation_v0_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
