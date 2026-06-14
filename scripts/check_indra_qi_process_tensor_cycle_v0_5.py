#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
import pathlib
import shutil
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import (
    cycle_plan_digest,
    cycle_state_digest,
    valid_digest,
    without,
    sha,
)
from runtime.kuuos_runtime_daemon_indra_qi_process_tensor_cycle_v0_5 import (
    build_indra_qi_process_tensor_cycle_v0_5,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_process_tensor_activation_v0_4 import (
    build_plan as activation_plan,
    prepare_feedback,
    read_json,
    records,
    run_activation,
    write_json,
)

EXAMPLE = ROOT / "examples" / "indra_qi_process_tensor_cycle_plan_v0_5.json"


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def prepare_activation(
    root: pathlib.Path,
    suffix: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    source, _, packet, handoff = prepare_feedback(root, suffix=f"cycle-{suffix}")
    plan = activation_plan(source, packet, handoff, suffix=f"cycle-{suffix}", approve_count=2)
    result = run_activation(root, plan)
    assert result["status"] == "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_READY", result
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    activation = read_json(root / "indra_qi_process_tensor_activation_record_v0_4.json")
    review = read_json(root / "indra_qi_process_tensor_review_v0_4.json")
    assert valid_digest(activation, "activation_record_digest")
    assert valid_digest(review, "process_tensor_review_digest")
    return source, world, activation, review


def build_plan(
    world: dict[str, Any],
    activation: dict[str, Any],
    review: dict[str, Any],
    *,
    suffix: str,
    previous_digest: str = "GENESIS",
) -> dict[str, Any]:
    plan = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    plan.update(
        {
            "cycle_id": f"indra-qi-process-tensor-cycle-{suffix}",
            "source_activation_id": activation["activation_id"],
            "source_activation_record_digest": activation["activation_record_digest"],
            "source_process_tensor_review_digest": review["process_tensor_review_digest"],
            "source_world_state_digest": world["indra_qi_world_state_digest"],
            "expected_previous_cycle_state_digest": previous_digest,
        }
    )
    plan["cycle_plan_digest"] = cycle_plan_digest(plan)
    return plan


def cycle_license(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_LICENSE_READY",
        "bound_cycle_plan_digest": plan["cycle_plan_digest"],
        "world_state_read_allowed": True,
        "activation_record_read_allowed": True,
        "process_tensor_review_read_allowed": True,
        "feedback_packet_read_allowed": True,
        "mutation_ledger_read_allowed": True,
        "previous_cycle_state_read_allowed": True,
        "cycle_plan_validate_allowed": True,
        "cycle_state_write_allowed": True,
        "next_cycle_seed_write_allowed": True,
        "cycle_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_process_tensor_cycle_v0_5_enabled": True,
        "evolve_indra_qi_process_tensor_cycle_v0_5": True,
    }


def run_cycle(
    root: pathlib.Path,
    plan: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_process_tensor_cycle_v0_5(
        runtime_context=context(root),
        cycle_plan=plan,
        cycle_license=license_value or cycle_license(plan),
    ).to_dict()


def assert_world_unchanged(root: pathlib.Path, before_digest: str) -> None:
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    assert world["indra_qi_world_state_digest"] == before_digest
    assert compute_indra_qi_world_state_digest(world) == before_digest


def copy_cycle_history(source_root: pathlib.Path, target_root: pathlib.Path) -> None:
    shutil.copyfile(
        source_root / "indra_qi_process_tensor_cycle_state_v0_5.json",
        target_root / "indra_qi_process_tensor_cycle_state_v0_5.json",
    )
    shutil.copyfile(
        source_root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl",
        target_root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl",
    )


def refresh_activation_and_ledger(
    root: pathlib.Path,
    activation: dict[str, Any],
    world_digest: str,
) -> dict[str, Any]:
    activation["after_world_state_digest"] = world_digest
    activation["activation_record_digest"] = sha(without(activation, "activation_record_digest"))
    write_json(root / "indra_qi_process_tensor_activation_record_v0_4.json", activation)
    ledger_path = root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl"
    values = records(ledger_path)
    record = values[-1]
    record["source_activation_record_digest"] = activation["activation_record_digest"]
    record["after_world_state_digest"] = world_digest
    record["record_digest"] = sha(without(record, "record_digest"))
    ledger_path.write_text(
        "\n".join(json.dumps(value, ensure_ascii=False, sort_keys=True) for value in values[:-1] + [record])
        + "\n",
        encoding="utf-8",
    )
    return activation


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "cycle-one"
        _, world, activation, review = prepare_activation(root, "one")
        before_digest = world["indra_qi_world_state_digest"]
        plan = build_plan(world, activation, review, suffix="one")
        result = run_cycle(root, plan)
        assert result["status"] == "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_READY", result
        assert result["cycle_status"] == "process_tensor_cycle_evolved"
        assert result["cycle_index"] == 1
        assert result["channel_count"] == 2
        assert result["seed_entry_count"] == 2
        assert result["source_world_state_unchanged"] is True
        assert result["previous_cycle_state_digest"] == "GENESIS"
        assert_world_unchanged(root, before_digest)

        state = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
        seed = read_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json")
        ledger = latest(root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl")
        assert cycle_state_digest(state) == state["process_tensor_cycle_state_digest"]
        assert valid_digest(seed, "next_cycle_seed_packet_digest")
        assert valid_digest(ledger, "record_digest")
        assert state["cycle_index"] == 1
        assert state["reviewed_nonactivated_evidence_count"] == 1
        assert len(state["channels"]) == 2
        assert len(seed["seed_entries"]) == 2
        assert seed["source_process_tensor_cycle_state_digest"] == state[
            "process_tensor_cycle_state_digest"
        ]
        assert ledger["process_tensor_cycle_state_digest"] == state[
            "process_tensor_cycle_state_digest"
        ]
        assert ledger["next_cycle_seed_packet_digest"] == seed["next_cycle_seed_packet_digest"]
        assert all(valid_digest(channel, "channel_state_digest") for channel in state["channels"])
        assert all(valid_digest(entry, "seed_entry_digest") for entry in seed["seed_entries"])
        assert all(channel["memory_kernel_strength"] > 0 for channel in state["channels"])
        assert all(channel["nonmarkov_coupling"] > 0 for channel in state["channels"])
        assert all(channel["recoverability_reserve"] >= 0.25 for channel in state["channels"])
        assert all(channel["observation_debt"] <= 0.20 for channel in state["channels"])
        assert all(channel["previous_channel_state_digest"] == "GENESIS" for channel in state["channels"])
        assert seed["boundary"]["next_cycle_seed_not_fact"] is True
        assert seed["boundary"]["next_cycle_seed_requires_new_projection_license"] is True

        ledger_count = len(records(root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl"))
        replay = run_cycle(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "process_tensor_cycle_id_replay" in replay["blockers"]
        assert "source_activation_cycle_replay" in replay["blockers"]
        assert len(records(root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl")) == ledger_count
        assert_world_unchanged(root, before_digest)

        root_two = base / "cycle-two"
        _, world_two, activation_two, review_two = prepare_activation(root_two, "two")
        copy_cycle_history(root, root_two)
        previous_state = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
        previous_digest = previous_state["process_tensor_cycle_state_digest"]
        plan_two = build_plan(
            world_two,
            activation_two,
            review_two,
            suffix="two",
            previous_digest=previous_digest,
        )
        result_two = run_cycle(root_two, plan_two)
        assert result_two["status"] == "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_READY", result_two
        assert result_two["cycle_index"] == 2
        state_two = read_json(root_two / "indra_qi_process_tensor_cycle_state_v0_5.json")
        assert state_two["previous_cycle_state_digest"] == previous_digest
        previous_by_key = {channel["target_key"]: channel for channel in previous_state["channels"]}
        for channel in state_two["channels"]:
            prior = previous_by_key[channel["target_key"]]
            assert channel["previous_channel_state_digest"] == prior["channel_state_digest"]
            assert channel["memory_kernel_strength"] > prior["memory_kernel_strength"]
            assert channel["nonmarkov_coupling"] > prior["nonmarkov_coupling"]
            assert channel["recoverability_reserve"] > prior["recoverability_reserve"]

        root = base / "activation-digest"
        _, world, activation, review = prepare_activation(root, "activation-digest")
        before_digest = world["indra_qi_world_state_digest"]
        plan = build_plan(world, activation, review, suffix="activation-digest")
        activation["overlays_applied"] = 99
        write_json(root / "indra_qi_process_tensor_activation_record_v0_4.json", activation)
        result = run_cycle(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "source_v0_4_activation_record_digest_invalid" in result["blockers"]
        assert_world_unchanged(root, before_digest)

        root = base / "overlay-chain"
        _, world, activation, review = prepare_activation(root, "overlay-chain")
        overlays = world["runtime_observation_overlays"]
        overlays[0]["previous_overlay_digest"] = "BROKEN"
        overlays[0]["overlay_digest"] = sha(without(overlays[0], "overlay_digest"))
        world["indra_qi_world_state_digest"] = compute_indra_qi_world_state_digest(world)
        write_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
        activation = refresh_activation_and_ledger(root, activation, world["indra_qi_world_state_digest"])
        plan = build_plan(world, activation, review, suffix="overlay-chain")
        result = run_cycle(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "world_overlay_0_previous_digest_mismatch" in result["blockers"]
        assert "world_overlay_1_previous_digest_mismatch" in result["blockers"]
        assert_world_unchanged(root, world["indra_qi_world_state_digest"])

        root = base / "process-context"
        _, world, activation, review = prepare_activation(root, "process-context")
        feedback_path = root / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
        feedback = read_json(feedback_path)
        feedback["source_process_tensor_context"]["memory_kernel_digest"] = ""
        feedback["feedback_packet_digest"] = sha(without(feedback, "feedback_packet_digest"))
        write_json(feedback_path, feedback)
        activation["source_feedback_packet_digest"] = feedback["feedback_packet_digest"]
        activation["activation_record_digest"] = sha(without(activation, "activation_record_digest"))
        write_json(root / "indra_qi_process_tensor_activation_record_v0_4.json", activation)
        ledger_path = root / "indra_qi_world_observation_overlay_ledger_v0_4.jsonl"
        values = records(ledger_path)
        values[-1]["source_activation_record_digest"] = activation["activation_record_digest"]
        values[-1]["record_digest"] = sha(without(values[-1], "record_digest"))
        ledger_path.write_text(
            "\n".join(json.dumps(value, ensure_ascii=False, sort_keys=True) for value in values) + "\n",
            encoding="utf-8",
        )
        plan = build_plan(world, activation, review, suffix="process-context")
        result = run_cycle(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "source_v0_3_feedback_process_context_memory_kernel_digest_missing" in result[
            "blockers"
        ]
        assert_world_unchanged(root, world["indra_qi_world_state_digest"])

        root = base / "license-digest"
        _, world, activation, review = prepare_activation(root, "license-digest")
        plan = build_plan(world, activation, review, suffix="license-digest")
        result = run_cycle(
            root,
            plan,
            cycle_license(plan, bound_cycle_plan_digest="mismatch"),
        )
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_cycle_license_plan_digest_mismatch" in result["blockers"]
        assert_world_unchanged(root, world["indra_qi_world_state_digest"])

        root = base / "channel-limit"
        _, world, activation, review = prepare_activation(root, "channel-limit")
        plan = build_plan(world, activation, review, suffix="channel-limit")
        plan["evolution_policy"]["max_channels"] = 1
        plan["cycle_plan_digest"] = cycle_plan_digest(plan)
        result = run_cycle(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_cycle_channel_limit_exceeded" in result["blockers"]
        assert_world_unchanged(root, world["indra_qi_world_state_digest"])

        root = base / "no-seeds"
        _, world, activation, review = prepare_activation(root, "no-seeds")
        plan = build_plan(world, activation, review, suffix="no-seeds")
        plan["evolution_policy"]["min_next_cycle_prior_weight"] = 0.99
        plan["cycle_plan_digest"] = cycle_plan_digest(plan)
        result = run_cycle(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_cycle_no_admissible_next_cycle_seeds" in result["blockers"]
        assert_world_unchanged(root, world["indra_qi_world_state_digest"])

        root = base / "previous-state"
        _, world, activation, review = prepare_activation(root, "previous-state")
        copy_cycle_history(base / "cycle-one", root)
        previous = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
        expected_previous = previous["process_tensor_cycle_state_digest"]
        previous["global_metrics"]["mean_memory_kernel_strength"] = 0.999
        write_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json", previous)
        plan = build_plan(
            world,
            activation,
            review,
            suffix="previous-state",
            previous_digest=expected_previous,
        )
        result = run_cycle(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "previous_process_tensor_cycle_state_digest_invalid" in result["blockers"]
        assert_world_unchanged(root, world["indra_qi_world_state_digest"])

        root = base / "boundary"
        _, world, activation, review = prepare_activation(root, "boundary")
        plan = build_plan(world, activation, review, suffix="boundary")
        plan["boundary"]["non_markov_feedback_preserved"] = False
        plan["cycle_plan_digest"] = cycle_plan_digest(plan)
        result = run_cycle(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "process_tensor_cycle_boundary_non_markov_feedback_preserved_mismatch" in result[
            "blockers"
        ]
        assert_world_unchanged(root, world["indra_qi_world_state_digest"])

    print("indra_qi_process_tensor_cycle_v0_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
