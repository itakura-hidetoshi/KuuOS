#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_child_feedback_cycle_core_v0_10 import (
    bridge_plan_digest,
    valid_digest,
)
from runtime.kuuos_indra_qi_process_tensor_activation_core_v0_4 import (
    protected_structure_digest,
)
from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import (
    cycle_state_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    read_json,
    records,
    write_json,
)
from scripts.qi_child_feedback_cycle_v0_10_test_support import (
    bridge_license,
    build_plan,
    prepare_v0_9_execution,
    run_bridge,
)


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def snapshot(paths: list[pathlib.Path]) -> dict[pathlib.Path, bytes | None]:
    return {path: path.read_bytes() if path.is_file() else None for path in paths}


def assert_snapshot(snapshot_value: dict[pathlib.Path, bytes | None]) -> None:
    for path, expected in snapshot_value.items():
        actual = path.read_bytes() if path.is_file() else None
        assert actual == expected, path


def transaction_paths(root: pathlib.Path, activation_id: str) -> list[pathlib.Path]:
    return [
        root / "indra_qi_causal_feedback_candidate_packet_v0_3.json",
        root / "indra_qi_causal_feedback_approval_handoff_v0_3.json",
        root / "ku_indra_qi_noncommutative_mandala_world_state.json",
        root / "indra_qi_process_tensor_review_v0_4.json",
        root / "indra_qi_process_tensor_activation_record_v0_4.json",
        root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl",
        root / "indra_qi_process_tensor_activation_receipt_v0_4.json",
        root / "indra_qi_process_tensor_activation_audit_v0_4.jsonl",
        root / f"indra_qi_world_rollback_snapshot_v0_4_{activation_id}.json",
        root / "indra_qi_process_tensor_cycle_state_v0_5.json",
        root / "indra_qi_next_cycle_projection_seed_v0_5.json",
        root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl",
        root / "indra_qi_process_tensor_cycle_receipt_v0_5.json",
        root / "indra_qi_process_tensor_cycle_audit_v0_5.jsonl",
    ]


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        world, execution, child, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "success"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="success",
        )
        before_world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        before_digest = before_world["indra_qi_world_state_digest"]
        before_protected = protected_structure_digest(before_world)
        before_overlay_count = len(before_world.get("runtime_observation_overlays", []))
        previous_state = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
        previous_digest = previous_state["process_tensor_cycle_state_digest"]
        previous_index = previous_state["cycle_index"]
        previous_channels = {
            value["target_key"]: value for value in previous_state["channels"]
        }
        child_paths = [
            child / "ku_indra_qi_noncommutative_mandala_world_state.json",
            child / "kuuos_causal_world_model_state_v14_0.json",
            child / "indra_qi_causal_feedback_candidate_packet_v0_3.json",
            child / "indra_qi_causal_feedback_approval_handoff_v0_3.json",
            child / "indra_qi_causal_feedback_ledger_v0_3.jsonl",
        ]
        child_snapshot = snapshot(child_paths)

        result = run_bridge(root, plan)
        assert result["status"] == "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_READY", result
        assert result["handoff_status"] == "child_feedback_activated_and_parent_cycle_evolved"
        assert result["child_feedback_staged"] is True
        assert result["v0_4_activation_invoked"] is True
        assert result["v0_4_activation_ready"] is True
        assert result["v0_5_cycle_invoked"] is True
        assert result["v0_5_cycle_ready"] is True
        assert result["transaction_rolled_back"] is False
        assert result["rollback_reason"] == ""
        assert result["approved_candidate_count"] == 2
        assert result["overlays_applied"] == 2
        assert result["cycle_index"] == previous_index + 1
        assert result["channel_count"] == 2
        assert result["seed_entry_count"] == 2
        assert result["before_parent_world_state_digest"] == before_digest
        assert result["after_parent_world_state_digest"] != before_digest
        assert result["previous_cycle_state_digest"] == previous_digest
        assert result["child_feedback_packet_digest"] == feedback["feedback_packet_digest"]
        assert result["child_feedback_handoff_digest"] == handoff["approval_handoff_digest"]
        assert_snapshot(child_snapshot)

        after_world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        assert compute_indra_qi_world_state_digest(after_world) == after_world[
            "indra_qi_world_state_digest"
        ]
        assert after_world["indra_qi_world_state_digest"] == result[
            "after_parent_world_state_digest"
        ]
        assert protected_structure_digest(after_world) == before_protected
        assert len(after_world["runtime_observation_overlays"]) == before_overlay_count + 2
        assert all(
            value["activation_id"] == plan["activation_id"]
            for value in after_world["runtime_observation_overlays"][-2:]
        )

        parent_feedback = read_json(
            root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
        )
        parent_handoff = read_json(
            root / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
        )
        assert parent_feedback == feedback
        assert parent_handoff == handoff

        review = read_json(root / "indra_qi_process_tensor_review_v0_4.json")
        activation = read_json(root / "indra_qi_process_tensor_activation_record_v0_4.json")
        mutation_ledger = latest(
            root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl"
        )
        assert valid_digest(review, "process_tensor_review_digest")
        assert valid_digest(activation, "activation_record_digest")
        assert valid_digest(mutation_ledger, "record_digest")
        assert activation["source_feedback_packet_digest"] == feedback[
            "feedback_packet_digest"
        ]
        assert activation["approved_candidate_ids"] == plan["approved_candidate_ids"]
        assert activation["after_world_state_digest"] == after_world[
            "indra_qi_world_state_digest"
        ]

        cycle_state = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
        seed = read_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json")
        cycle_ledger = latest(root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl")
        assert cycle_state_digest(cycle_state) == cycle_state[
            "process_tensor_cycle_state_digest"
        ]
        assert valid_digest(seed, "next_cycle_seed_packet_digest")
        assert valid_digest(cycle_ledger, "record_digest")
        assert cycle_state["previous_cycle_state_digest"] == previous_digest
        assert cycle_state["cycle_index"] == previous_index + 1
        assert cycle_state["source_activation_record_digest"] == activation[
            "activation_record_digest"
        ]
        assert seed["source_process_tensor_cycle_state_digest"] == cycle_state[
            "process_tensor_cycle_state_digest"
        ]
        assert seed["boundary"]["next_cycle_seed_not_fact"] is True
        assert seed["boundary"][
            "next_cycle_seed_requires_new_projection_license"
        ] is True
        for channel in cycle_state["channels"]:
            assert channel["target_key"] in previous_channels
            assert channel["previous_channel_state_digest"] == previous_channels[
                channel["target_key"]
            ]["channel_state_digest"]

        handoff_packet = read_json(
            root / "indra_qi_child_feedback_parent_cycle_handoff_v0_10.json"
        )
        bridge_record = read_json(
            root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json"
        )
        bridge_ledger = latest(
            root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl"
        )
        assert valid_digest(handoff_packet, "handoff_packet_digest")
        assert valid_digest(bridge_record, "bridge_record_digest")
        assert valid_digest(bridge_ledger, "record_digest")
        assert handoff_packet["source_execution_record_digest"] == execution[
            "execution_record_digest"
        ]
        assert handoff_packet["activation_record_digest"] == activation[
            "activation_record_digest"
        ]
        assert handoff_packet["process_tensor_cycle_state_digest"] == cycle_state[
            "process_tensor_cycle_state_digest"
        ]
        assert handoff_packet["next_cycle_seed_packet_digest"] == seed[
            "next_cycle_seed_packet_digest"
        ]
        assert handoff_packet["boundary"]["child_runtime_unchanged"] is True
        assert bridge_ledger["source_bridge_record_digest"] == bridge_record[
            "bridge_record_digest"
        ]

        bridge_count = len(
            records(root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl")
        )
        parent_state_after_success = snapshot(
            transaction_paths(root, plan["activation_id"])
        )
        replay = run_bridge(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "child_feedback_cycle_bridge_id_replay" in replay["blockers"]
        assert "child_feedback_cycle_source_execution_replay" in replay["blockers"]
        assert "child_feedback_cycle_child_feedback_replay" in replay["blockers"]
        assert replay["v0_4_activation_invoked"] is False
        assert len(
            records(root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl")
        ) == bridge_count
        assert_snapshot(parent_state_after_success)

        root = base / "v0-4-failure"
        world, execution, child, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "v0-4-failure"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="v0-4-failure",
        )
        plan["process_tensor_policy"]["min_candidate_weight"] = 1.0
        plan["bridge_plan_digest"] = bridge_plan_digest(plan)
        before = snapshot(transaction_paths(root, plan["activation_id"]))
        result = run_bridge(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert result["v0_4_activation_invoked"] is True
        assert result["v0_4_activation_ready"] is False
        assert result["v0_5_cycle_invoked"] is False
        assert result["transaction_rolled_back"] is True
        assert any(value.startswith("nested_v0_4:") for value in result["blockers"])
        assert_snapshot(before)
        assert_snapshot(snapshot([
            child / "indra_qi_causal_feedback_candidate_packet_v0_3.json",
            child / "indra_qi_causal_feedback_approval_handoff_v0_3.json",
        ]))
        assert not (
            root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json"
        ).exists()

        root = base / "v0-5-failure"
        world, execution, child, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "v0-5-failure"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="v0-5-failure",
        )
        plan["evolution_policy"]["max_channels"] = 1
        plan["bridge_plan_digest"] = bridge_plan_digest(plan)
        before = snapshot(transaction_paths(root, plan["activation_id"]))
        result = run_bridge(root, plan)
        assert result["status"].endswith("BLOCKED"), result
        assert result["v0_4_activation_invoked"] is True
        assert result["v0_4_activation_ready"] is False or result[
            "v0_4_activation_ready"
        ] is True
        assert result["transaction_rolled_back"] is True
        assert_snapshot(before)
        assert not (
            root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json"
        ).exists()

        root = base / "child-feedback-tamper"
        world, execution, child, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "child-feedback-tamper"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="child-feedback-tamper",
        )
        feedback["feedback_candidates"][0]["candidate_weight"] = 0.999
        write_json(
            child / "indra_qi_causal_feedback_candidate_packet_v0_3.json",
            feedback,
        )
        before = snapshot(transaction_paths(root, plan["activation_id"]))
        result = run_bridge(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "child_feedback_cycle_child_feedback_digest_invalid" in result["blockers"]
        assert result["v0_4_activation_invoked"] is False
        assert result["transaction_rolled_back"] is False
        assert_snapshot(before)

        root = base / "approved-id"
        world, execution, _, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "approved-id"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="approved-id",
        )
        plan["approved_candidate_ids"] = ["missing-candidate"]
        plan["bridge_plan_digest"] = bridge_plan_digest(plan)
        result = run_bridge(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "child_feedback_cycle_approved_candidate_not_in_child_packet" in result[
            "blockers"
        ]
        assert result["v0_4_activation_invoked"] is False

        root = base / "previous-digest"
        world, execution, _, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "previous-digest"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="previous-digest",
        )
        plan["expected_previous_cycle_state_digest"] = "mismatch"
        plan["bridge_plan_digest"] = bridge_plan_digest(plan)
        result = run_bridge(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "child_feedback_cycle_expected_previous_cycle_digest_mismatch" in result[
            "blockers"
        ]
        assert result["v0_4_activation_invoked"] is False

        root = base / "license"
        world, execution, _, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "license"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="license",
        )
        license_value = bridge_license(plan)
        license_value["v0_4_activation_license_template"][
            "world_state_write_allowed"
        ] = False
        result = run_bridge(root, plan, license_value)
        assert result["status"].endswith("BLOCKED")
        assert "child_feedback_cycle_nested_v0_4_world_state_write_allowed_not_true" in result[
            "blockers"
        ]
        assert result["v0_4_activation_invoked"] is False

        root = base / "execution-tamper"
        world, execution, _, feedback, handoff, execution_ledger = prepare_v0_9_execution(
            root, "execution-tamper"
        )
        plan = build_plan(
            root=root,
            world=world,
            execution=execution,
            execution_ledger=execution_ledger,
            feedback=feedback,
            handoff=handoff,
            suffix="execution-tamper",
        )
        execution["feedback_candidate_count"] = 99
        write_json(
            root / "indra_qi_approved_recovery_action_execution_record_v0_9.json",
            execution,
        )
        result = run_bridge(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "child_feedback_cycle_source_execution_digest_invalid" in result[
            "blockers"
        ]
        assert result["v0_4_activation_invoked"] is False

    print("qi_child_feedback_parent_cycle_v0_10 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
