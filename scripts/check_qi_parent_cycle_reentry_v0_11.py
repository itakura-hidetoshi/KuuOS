#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_parent_cycle_reentry_core_v0_11 import (
    loop_plan_digest,
    valid_digest,
)
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    dynamic_world_state_digest,
    overlay_history_digest,
    protected_constitution_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    read_json,
    records,
    write_json,
)
from scripts.qi_parent_cycle_reentry_v0_11_test_support import (
    build_plan,
    latest,
    loop_license,
    prepare_v0_10_cycle,
    reentry_template,
    run_loop,
    v14_template,
    projection_template,
)


def snapshot(paths: list[pathlib.Path]) -> dict[pathlib.Path, bytes | None]:
    return {path: path.read_bytes() if path.is_file() else None for path in paths}


def assert_snapshot(value: dict[pathlib.Path, bytes | None]) -> None:
    for path, expected in value.items():
        actual = path.read_bytes() if path.is_file() else None
        assert actual == expected, path


def transaction_paths(root: pathlib.Path, assimilation_id: str) -> list[pathlib.Path]:
    return [
        root / "ku_indra_qi_noncommutative_mandala_world_state.json",
        root
        / f"indra_qi_world_assimilation_rollback_snapshot_v0_6_{assimilation_id}.json",
        root / "indra_qi_post_assimilation_projection_seed_v0_6.json",
        root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json",
        root / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl",
        root / "indra_qi_process_tensor_world_assimilation_receipt_v0_6.json",
        root / "indra_qi_process_tensor_world_assimilation_audit_v0_6.jsonl",
        root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json",
        root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl",
        root / "indra_qi_post_assimilation_causal_reentry_receipt_v0_7.json",
        root / "indra_qi_post_assimilation_causal_reentry_audit_v0_7.jsonl",
    ]


def make_plan(
    root: pathlib.Path,
    suffix: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    world, handoff, record, ledger, cycle, seed = prepare_v0_10_cycle(root, suffix)
    plan = build_plan(
        world=world,
        handoff=handoff,
        bridge_record=record,
        bridge_ledger=ledger,
        cycle=cycle,
        seed=seed,
        suffix=suffix,
    )
    return world, plan


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        before_world, plan = make_plan(root, "success")
        before_digest = before_world["indra_qi_world_state_digest"]
        before_dynamic_digest = before_world["process_tensor_dynamic_world_state_digest"]
        before_dynamic_revision = before_world["world_dynamic_revision"]
        before_constitution = protected_constitution_digest(before_world)
        before_overlays = overlay_history_digest(before_world)
        source_cycle = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
        source_seed = read_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json")
        source_snapshot = snapshot(
            [
                root / "indra_qi_child_feedback_parent_cycle_handoff_v0_10.json",
                root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json",
                root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl",
                root / "indra_qi_process_tensor_cycle_state_v0_5.json",
                root / "indra_qi_next_cycle_projection_seed_v0_5.json",
                root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl",
            ]
        )

        result = run_loop(root, plan)
        assert result["status"] == "INDRA_QI_PARENT_CYCLE_ASSIMILATION_REENTRY_V0_11_READY", result
        assert result["loop_status"] == "parent_cycle_assimilated_and_causal_reentry_initialized"
        assert result["v0_6_assimilation_invoked"] is True
        assert result["v0_6_assimilation_ready"] is True
        assert result["v0_7_reentry_invoked"] is True
        assert result["v0_7_reentry_ready"] is True
        assert result["transaction_committed"] is True
        assert result["transaction_rolled_back"] is False
        assert result["rollback_reason"] == ""
        assert result["before_parent_world_state_digest"] == before_digest
        assert result["after_assimilation_world_state_digest"] != before_digest
        assert result["previous_dynamic_world_state_digest"] == before_dynamic_digest
        assert result["dynamic_world_state_digest"] != before_dynamic_digest
        assert result["dynamic_revision"] == before_dynamic_revision + 1
        assert result["post_assimilation_seed_packet_digest"]
        assert result["projection_packet_digest"]
        assert result["projection_activation_digest"]
        assert result["v14_world_model_digest"]
        assert result["loop_handoff_packet_digest"]
        assert_snapshot(source_snapshot)

        after_world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        assert compute_indra_qi_world_state_digest(after_world) == after_world[
            "indra_qi_world_state_digest"
        ]
        assert dynamic_world_state_digest(after_world) == after_world[
            "process_tensor_dynamic_world_state_digest"
        ]
        assert after_world["indra_qi_world_state_digest"] == result[
            "after_assimilation_world_state_digest"
        ]
        assert after_world["process_tensor_dynamic_world_state_digest"] == result[
            "dynamic_world_state_digest"
        ]
        assert protected_constitution_digest(after_world) == before_constitution
        assert overlay_history_digest(after_world) == before_overlays

        assimilation = read_json(
            root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json"
        )
        assimilation_seed = read_json(
            root / "indra_qi_post_assimilation_projection_seed_v0_6.json"
        )
        assimilation_ledger = latest(
            root / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
        )
        assert valid_digest(assimilation, "assimilation_record_digest")
        assert assimilation["assimilation_status"] == "dynamic_world_state_assimilated"
        assert assimilation["source_cycle_state_digest"] == source_cycle[
            "process_tensor_cycle_state_digest"
        ]
        assert assimilation["source_seed_packet_digest"] == source_seed[
            "next_cycle_seed_packet_digest"
        ]
        assert assimilation["after_world_state_digest"] == after_world[
            "indra_qi_world_state_digest"
        ]
        assert valid_digest(assimilation_seed, "post_assimilation_seed_packet_digest")
        assert assimilation_seed["source_world_state_digest"] == after_world[
            "indra_qi_world_state_digest"
        ]
        assert valid_digest(assimilation_ledger, "record_digest")
        assert assimilation_ledger["source_assimilation_record_digest"] == assimilation[
            "assimilation_record_digest"
        ]

        child = pathlib.Path(result["child_runtime_root"])
        assert child.is_dir()
        child_world = read_json(child / "ku_indra_qi_noncommutative_mandala_world_state.json")
        generated = read_json(child / "indra_qi_generated_causal_projection_plan_v0_7.json")
        projection_packet = read_json(child / "indra_qi_causal_projection_packet_v0_2.json")
        projection_activation = read_json(
            child / "indra_qi_causal_projection_activation_record_v0_2.json"
        )
        v14_state = read_json(child / "kuuos_causal_world_model_state_v14_0.json")
        reentry = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
        reentry_ledger = latest(
            root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl"
        )
        assert child_world["indra_qi_world_state_digest"] == after_world[
            "indra_qi_world_state_digest"
        ]
        assert generated["source_indra_qi_world_state_digest"] == after_world[
            "indra_qi_world_state_digest"
        ]
        assert valid_digest(projection_packet, "projection_packet_digest")
        assert valid_digest(projection_activation, "activation_record_digest")
        assert valid_v14_digest(v14_state, "world_model_digest")
        assert v14_state["world_id"] == plan["causal_world_id"]
        assert valid_digest(reentry, "reentry_record_digest")
        assert reentry["source_assimilation_record_digest"] == assimilation[
            "assimilation_record_digest"
        ]
        assert reentry["projection_packet_digest"] == projection_packet[
            "projection_packet_digest"
        ]
        assert valid_digest(reentry_ledger, "record_digest")
        assert reentry_ledger["source_reentry_record_digest"] == reentry[
            "reentry_record_digest"
        ]

        handoff = read_json(
            root / "indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json"
        )
        loop_record = read_json(
            root / "indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json"
        )
        loop_ledger = latest(
            root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl"
        )
        assert valid_digest(handoff, "loop_handoff_packet_digest")
        assert valid_digest(loop_record, "loop_record_digest")
        assert valid_digest(loop_ledger, "record_digest")
        assert handoff["source_v0_10_handoff_packet_digest"] == plan[
            "source_v0_10_handoff_packet_digest"
        ]
        assert handoff["assimilation_record_digest"] == assimilation[
            "assimilation_record_digest"
        ]
        assert handoff["reentry_record_digest"] == reentry["reentry_record_digest"]
        assert handoff["v14_world_model_digest"] == v14_state["world_model_digest"]
        assert handoff["boundary"]["transaction_committed"] is True
        assert loop_ledger["source_loop_record_digest"] == loop_record[
            "loop_record_digest"
        ]

        loop_count = len(
            records(root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl")
        )
        success_parent_snapshot = snapshot(transaction_paths(root, plan["assimilation_id"]))
        success_child_snapshot = snapshot(
            [
                child / "ku_indra_qi_noncommutative_mandala_world_state.json",
                child / "indra_qi_generated_causal_projection_plan_v0_7.json",
                child / "indra_qi_causal_projection_packet_v0_2.json",
                child / "indra_qi_causal_projection_activation_record_v0_2.json",
                child / "kuuos_causal_world_model_state_v14_0.json",
            ]
        )
        replay = run_loop(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_loop_id_replay" in replay["blockers"]
        assert "parent_cycle_reentry_source_v0_10_handoff_replay" in replay["blockers"]
        assert replay["v0_6_assimilation_invoked"] is False
        assert len(
            records(root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl")
        ) == loop_count
        assert_snapshot(success_parent_snapshot)
        assert_snapshot(success_child_snapshot)

        root = base / "v0-7-failure"
        before_world, plan = make_plan(root, "v0-7-failure")
        plan["projection_policy"]["minimum_seed_count"] = 99
        plan["loop_plan_digest"] = loop_plan_digest(plan)
        before = snapshot(transaction_paths(root, plan["assimilation_id"]))
        child = root / "indra_qi_causal_reentry_cycles_v0_7" / plan["reentry_id"]
        result = run_loop(root, plan)
        assert result["status"].endswith("BLOCKED"), result
        assert result["v0_6_assimilation_invoked"] is True
        assert result["v0_6_assimilation_ready"] is True
        assert result["v0_7_reentry_invoked"] is True
        assert result["v0_7_reentry_ready"] is False
        assert result["transaction_committed"] is False
        assert result["transaction_rolled_back"] is True
        assert any(value.startswith("nested_v0_7:") for value in result["blockers"])
        assert_snapshot(before)
        assert not child.exists()
        restored = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        assert restored["indra_qi_world_state_digest"] == before_world[
            "indra_qi_world_state_digest"
        ]
        assert restored["process_tensor_dynamic_world_state_digest"] == before_world[
            "process_tensor_dynamic_world_state_digest"
        ]
        assert not (
            root / "indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json"
        ).exists()

        root = base / "handoff-tamper"
        _, plan = make_plan(root, "handoff-tamper")
        handoff_path = root / "indra_qi_child_feedback_parent_cycle_handoff_v0_10.json"
        handoff_value = read_json(handoff_path)
        handoff_value["cycle_index"] = 999
        write_json(handoff_path, handoff_value)
        result = run_loop(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_source_v0_10_handoff_digest_invalid" in result[
            "blockers"
        ]
        assert result["v0_6_assimilation_invoked"] is False

        root = base / "seed-tamper"
        _, plan = make_plan(root, "seed-tamper")
        seed_path = root / "indra_qi_next_cycle_projection_seed_v0_5.json"
        seed_value = read_json(seed_path)
        seed_value["seed_entries"][0]["prior_weight"] = 0.999
        write_json(seed_path, seed_value)
        result = run_loop(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_source_cycle_seed_digest_invalid" in result[
            "blockers"
        ]
        assert result["v0_6_assimilation_invoked"] is False

        root = base / "dynamic-digest"
        _, plan = make_plan(root, "dynamic-digest")
        plan["expected_previous_dynamic_world_state_digest"] = "mismatch"
        plan["loop_plan_digest"] = loop_plan_digest(plan)
        result = run_loop(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_expected_previous_dynamic_digest_mismatch" in result[
            "blockers"
        ]
        assert result["v0_6_assimilation_invoked"] is False

        root = base / "nested-v0-6-license"
        _, plan = make_plan(root, "nested-v0-6-license")
        license_value = loop_license(plan)
        license_value["v0_6_assimilation_license_template"][
            "world_state_write_allowed"
        ] = False
        result = run_loop(root, plan, license_value)
        assert result["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_nested_v0_6_world_state_write_allowed_not_true" in result[
            "blockers"
        ]
        assert result["v0_6_assimilation_invoked"] is False

        root = base / "nested-v0-7-license"
        _, plan = make_plan(root, "nested-v0-7-license")
        nested_projection = projection_template(
            v14_initialize_license_template=v14_template(state_write_allowed=False)
        )
        nested_reentry = reentry_template(
            v0_2_projection_license_template=nested_projection
        )
        result = run_loop(
            root,
            plan,
            loop_license(plan, v0_7_reentry_license_template=nested_reentry),
        )
        assert result["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_nested_v14_state_write_allowed_not_true" in result[
            "blockers"
        ]
        assert result["v0_6_assimilation_invoked"] is False

        root = base / "child-exists"
        _, plan = make_plan(root, "child-exists")
        child = root / "indra_qi_causal_reentry_cycles_v0_7" / plan["reentry_id"]
        child.mkdir(parents=True)
        result = run_loop(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_child_runtime_already_exists" in result[
            "blockers"
        ]
        assert result["v0_6_assimilation_invoked"] is False

        root = base / "boundary"
        _, plan = make_plan(root, "boundary")
        plan["boundary"]["v0_6_and_v0_7_transaction_compensated"] = False
        plan["loop_plan_digest"] = loop_plan_digest(plan)
        result = run_loop(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "parent_cycle_reentry_boundary_v0_6_and_v0_7_transaction_compensated_mismatch" in result[
            "blockers"
        ]
        assert result["v0_6_assimilation_invoked"] is False

    print("qi_parent_cycle_reentry_v0_11 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
