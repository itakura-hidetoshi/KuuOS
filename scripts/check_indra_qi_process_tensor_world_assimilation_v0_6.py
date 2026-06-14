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

from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import cycle_state_digest
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    DYNAMIC_WORLD_FIELDS,
    assimilation_plan_digest,
    dynamic_world_state_digest,
    overlay_history_digest,
    protected_constitution_digest,
    sha,
    valid_digest,
    without,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_assimilation_v0_6 import (
    build_indra_qi_process_tensor_world_assimilation_v0_6,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_process_tensor_cycle_v0_5 import (
    build_plan as cycle_plan,
    latest,
    prepare_activation,
    read_json,
    records,
    run_cycle,
    write_json,
)

EXAMPLE = ROOT / "examples" / "indra_qi_process_tensor_world_assimilation_plan_v0_6.json"


def prepare_cycle(
    root: pathlib.Path,
    suffix: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _, world, activation, review = prepare_activation(root, f"assimilation-{suffix}")
    plan = cycle_plan(world, activation, review, suffix=f"assimilation-{suffix}")
    result = run_cycle(root, plan)
    assert result["status"] == "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_READY", result
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    cycle = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
    seed = read_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json")
    assert cycle_state_digest(cycle) == cycle["process_tensor_cycle_state_digest"]
    assert valid_digest(seed, "next_cycle_seed_packet_digest")
    return world, cycle, seed


def build_plan(
    world: dict[str, Any],
    cycle: dict[str, Any],
    seed: dict[str, Any],
    *,
    suffix: str,
    previous_dynamic_digest: str = "GENESIS",
) -> dict[str, Any]:
    plan = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    plan.update(
        {
            "assimilation_id": f"indra-qi-world-assimilation-{suffix}",
            "source_cycle_id": cycle["cycle_id"],
            "source_cycle_state_digest": cycle["process_tensor_cycle_state_digest"],
            "source_seed_packet_digest": seed["next_cycle_seed_packet_digest"],
            "source_world_state_digest": world["indra_qi_world_state_digest"],
            "expected_previous_dynamic_world_state_digest": previous_dynamic_digest,
        }
    )
    plan["assimilation_plan_digest"] = assimilation_plan_digest(plan)
    return plan


def assimilation_license(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_LICENSE_READY",
        "bound_assimilation_plan_digest": plan["assimilation_plan_digest"],
        "world_state_read_allowed": True,
        "cycle_state_read_allowed": True,
        "source_seed_read_allowed": True,
        "cycle_ledger_read_allowed": True,
        "assimilation_plan_validate_allowed": True,
        "rollback_snapshot_write_allowed": True,
        "dynamic_world_state_write_allowed": True,
        "world_state_write_allowed": True,
        "post_write_verification_allowed": True,
        "post_assimilation_seed_write_allowed": True,
        "assimilation_record_write_allowed": True,
        "assimilation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "allowed_mutation_scopes": ["process_tensor_dynamic_world_state_only"],
        "allowed_dynamic_world_fields": [
            *DYNAMIC_WORLD_FIELDS,
            "process_tensor_world_state",
        ],
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_process_tensor_world_assimilation_v0_6_enabled": True,
        "apply_indra_qi_process_tensor_world_assimilation_v0_6": True,
    }


def run_assimilation(
    root: pathlib.Path,
    plan: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_process_tensor_world_assimilation_v0_6(
        runtime_context=context(root),
        assimilation_plan=plan,
        assimilation_license=license_value or assimilation_license(plan),
    ).to_dict()


def assert_world_unchanged(root: pathlib.Path, before: dict[str, Any]) -> None:
    after = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    assert after["indra_qi_world_state_digest"] == before["indra_qi_world_state_digest"]
    assert compute_indra_qi_world_state_digest(after) == before["indra_qi_world_state_digest"]


def rewrite_cycle_chain(
    root: pathlib.Path,
    cycle: dict[str, Any],
    seed: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    cycle["process_tensor_cycle_state_digest"] = cycle_state_digest(cycle)
    write_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json", cycle)

    seed["source_process_tensor_cycle_state_digest"] = cycle[
        "process_tensor_cycle_state_digest"
    ]
    seed["next_cycle_seed_packet_digest"] = sha(
        without(seed, "next_cycle_seed_packet_digest")
    )
    write_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json", seed)

    ledger_path = root / "indra_qi_process_tensor_cycle_ledger_v0_5.jsonl"
    ledger_values = records(ledger_path)
    ledger = ledger_values[-1]
    ledger["process_tensor_cycle_state_digest"] = cycle[
        "process_tensor_cycle_state_digest"
    ]
    ledger["next_cycle_seed_packet_digest"] = seed[
        "next_cycle_seed_packet_digest"
    ]
    ledger["record_digest"] = sha(without(ledger, "record_digest"))
    ledger_path.write_text(
        "\n".join(
            json.dumps(value, ensure_ascii=False, sort_keys=True)
            for value in ledger_values[:-1] + [ledger]
        )
        + "\n",
        encoding="utf-8",
    )
    return cycle, seed


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        before, cycle, source_seed = prepare_cycle(root, "success")
        constitution_before = protected_constitution_digest(before)
        overlays_before = overlay_history_digest(before)
        base_connections = deepcopy(before["indra_connections"])
        base_holonomy = deepcopy(before["holonomy_cycles"])
        plan = build_plan(before, cycle, source_seed, suffix="success")
        result = run_assimilation(root, plan)
        assert result["status"] == "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_READY", result
        assert result["assimilation_status"] == "dynamic_world_state_assimilated"
        assert result["dynamic_revision"] == 1
        assert result["local_patch_state_count"] == 1
        assert result["qi_flow_state_count"] == 1
        assert result["debt_ledger_entries_added"] == 2
        assert result["corridor_count"] == 2
        assert result["effective_holonomy_state_count"] == 1
        assert result["post_assimilation_seed_count"] == 2
        assert result["world_state_mutated"] is True
        assert result["rollback_snapshot_written"] is True
        assert result["rollback_performed"] is False
        assert result["protected_constitution_preserved"] is True
        assert result["overlay_history_preserved"] is True
        assert result["before_world_state_digest"] != result["after_world_state_digest"]

        after = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        snapshot = read_json(
            root
            / f"indra_qi_world_assimilation_rollback_snapshot_v0_6_{plan['assimilation_id']}.json"
        )
        record = read_json(
            root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json"
        )
        ledger = latest(
            root / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
        )
        seed = read_json(root / "indra_qi_post_assimilation_projection_seed_v0_6.json")

        assert compute_indra_qi_world_state_digest(after) == after[
            "indra_qi_world_state_digest"
        ]
        assert dynamic_world_state_digest(after) == after[
            "process_tensor_dynamic_world_state_digest"
        ]
        assert protected_constitution_digest(after) == constitution_before
        assert overlay_history_digest(after) == overlays_before
        assert after["indra_connections"] == base_connections
        assert after["holonomy_cycles"] == base_holonomy
        assert after["world_dynamic_revision"] == 1
        assert after["last_world_assimilation_id"] == plan["assimilation_id"]

        patch_state = after["local_patch_dynamic_states"][0]
        flow_state = after["qi_flow_effective_states"][0]
        assert valid_digest(patch_state, "dynamic_state_entry_digest")
        assert valid_digest(flow_state, "dynamic_state_entry_digest")
        assert patch_state["observation_debt"] > 0
        assert patch_state["recoverability_reserve"] < 1
        assert patch_state["effective_response_capacity"] < 1
        assert patch_state["relational_tension"] > 0
        assert flow_state["observation_debt"] > 0
        assert flow_state["recoverability_reserve"] < 1
        assert flow_state["effective_transport_resistance"] > 0
        assert flow_state["effective_transport_coefficient"] < 1
        assert flow_state["effective_holonomy_residue_pressure"] >= 0
        assert flow_state["qi_substance_claim"] is False

        debt_entries = after["observation_debt_ledger"]
        assert len(debt_entries) == 2
        assert all(valid_digest(entry, "debt_entry_digest") for entry in debt_entries)
        assert all(entry["current_observation_debt"] > 0 for entry in debt_entries)
        assert all(entry["boundary"]["debt_is_world_state"] is True for entry in debt_entries)
        assert all(entry["boundary"]["debt_not_moral_blame"] is True for entry in debt_entries)

        corridors = after["recoverability_corridors"]
        assert len(corridors) == 2
        assert all(valid_digest(entry, "corridor_digest") for entry in corridors)
        assert all(entry["branch_capacity"] > 0 for entry in corridors)
        assert all(entry["status"] in {"open", "constrained", "critical"} for entry in corridors)
        assert all(entry["boundary"]["corridor_not_execution_permission"] is True for entry in corridors)

        holonomy_states = after["effective_holonomy_states"]
        assert len(holonomy_states) == 1
        assert valid_digest(
            holonomy_states[0], "effective_holonomy_state_digest"
        )
        assert holonomy_states[0]["base_holonomy_digest"] == base_holonomy[0][
            "holonomy_digest"
        ]
        assert holonomy_states[0]["boundary"][
            "effective_holonomy_not_base_holonomy_replacement"
        ] is True
        assert holonomy_states[0]["boundary"]["base_holonomy_preserved"] is True

        summary = after["process_tensor_world_state"]
        assert summary["assimilation_status"] == "dynamic_world_state_assimilated"
        assert summary["dynamic_revision"] == 1
        assert summary["boundary"]["debt_changes_world_state"] is True
        assert summary["boundary"]["recoverability_changes_world_state"] is True
        assert summary["boundary"]["base_constitution_preserved"] is True

        assert valid_digest(snapshot, "rollback_snapshot_digest")
        assert snapshot["world_state"]["indra_qi_world_state_digest"] == before[
            "indra_qi_world_state_digest"
        ]
        assert snapshot["protected_constitution_digest"] == constitution_before
        assert snapshot["overlay_history_digest"] == overlays_before
        assert valid_digest(record, "assimilation_record_digest")
        assert record["after_world_state_digest"] == after[
            "indra_qi_world_state_digest"
        ]
        assert record["dynamic_world_state_digest"] == after[
            "process_tensor_dynamic_world_state_digest"
        ]
        assert valid_digest(ledger, "record_digest")
        assert ledger["source_assimilation_record_digest"] == record[
            "assimilation_record_digest"
        ]
        assert valid_digest(seed, "post_assimilation_seed_packet_digest")
        assert seed["source_world_state_digest"] == after[
            "indra_qi_world_state_digest"
        ]
        assert seed["source_dynamic_world_state_digest"] == after[
            "process_tensor_dynamic_world_state_digest"
        ]
        assert len(seed["seed_entries"]) == 2
        assert all(valid_digest(entry, "seed_entry_digest") for entry in seed["seed_entries"])
        assert all(
            entry["boundary"]["debt_and_recoverability_world_conditioned"] is True
            for entry in seed["seed_entries"]
        )

        ledger_count = len(
            records(
                root
                / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
            )
        )
        replay = run_assimilation(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "world_assimilation_id_replay" in replay["blockers"]
        assert "source_cycle_world_assimilation_replay" in replay["blockers"]
        assert len(
            records(
                root
                / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
            )
        ) == ledger_count
        after_replay = read_json(
            root / "ku_indra_qi_noncommutative_mandala_world_state.json"
        )
        assert after_replay["indra_qi_world_state_digest"] == after[
            "indra_qi_world_state_digest"
        ]

        root = base / "cycle-tamper"
        before, cycle, source_seed = prepare_cycle(root, "cycle-tamper")
        plan = build_plan(before, cycle, source_seed, suffix="cycle-tamper")
        cycle["channels"][0]["memory_kernel_strength"] = 0.999
        write_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json", cycle)
        result = run_assimilation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "source_v0_5_cycle_state_digest_invalid" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "seed-tamper"
        before, cycle, source_seed = prepare_cycle(root, "seed-tamper")
        plan = build_plan(before, cycle, source_seed, suffix="seed-tamper")
        source_seed["seed_entries"][0]["prior_weight"] = 0.999
        write_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json", source_seed)
        result = run_assimilation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "source_v0_5_seed_packet_digest_invalid" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "boundary"
        before, cycle, source_seed = prepare_cycle(root, "boundary")
        cycle["boundary"]["uses_process_tensor_feedback"] = False
        cycle, source_seed = rewrite_cycle_chain(root, cycle, source_seed)
        plan = build_plan(before, cycle, source_seed, suffix="boundary")
        result = run_assimilation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "source_v0_5_cycle_boundary_uses_process_tensor_feedback_not_true" in result[
            "blockers"
        ]
        assert_world_unchanged(root, before)

        root = base / "license-digest"
        before, cycle, source_seed = prepare_cycle(root, "license-digest")
        plan = build_plan(before, cycle, source_seed, suffix="license-digest")
        result = run_assimilation(
            root,
            plan,
            assimilation_license(plan, bound_assimilation_plan_digest="mismatch"),
        )
        assert result["status"].endswith("BLOCKED")
        assert "world_assimilation_license_plan_digest_mismatch" in result[
            "blockers"
        ]
        assert_world_unchanged(root, before)

        root = base / "scope"
        before, cycle, source_seed = prepare_cycle(root, "scope")
        plan = build_plan(before, cycle, source_seed, suffix="scope")
        plan["mutation_scope"] = "base_gauge_connection_update"
        plan["assimilation_plan_digest"] = assimilation_plan_digest(plan)
        result = run_assimilation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "world_assimilation_mutation_scope_invalid" in result["blockers"]
        assert_world_unchanged(root, before)

        root = base / "license-fields"
        before, cycle, source_seed = prepare_cycle(root, "license-fields")
        plan = build_plan(before, cycle, source_seed, suffix="license-fields")
        result = run_assimilation(
            root,
            plan,
            assimilation_license(
                plan,
                allowed_dynamic_world_fields=["process_tensor_world_state"],
            ),
        )
        assert result["status"].endswith("BLOCKED")
        assert "world_assimilation_license_dynamic_fields_not_exact" in result[
            "blockers"
        ]
        assert_world_unchanged(root, before)

        root = base / "previous-digest"
        before, cycle, source_seed = prepare_cycle(root, "previous-digest")
        plan = build_plan(
            before,
            cycle,
            source_seed,
            suffix="previous-digest",
            previous_dynamic_digest="not-genesis",
        )
        result = run_assimilation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "world_assimilation_expected_previous_dynamic_digest_mismatch" in result[
            "blockers"
        ]
        assert_world_unchanged(root, before)

        root = base / "plan-boundary"
        before, cycle, source_seed = prepare_cycle(root, "plan-boundary")
        plan = build_plan(before, cycle, source_seed, suffix="plan-boundary")
        plan["boundary"]["debt_changes_world_state"] = False
        plan["assimilation_plan_digest"] = assimilation_plan_digest(plan)
        result = run_assimilation(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "world_assimilation_boundary_debt_changes_world_state_mismatch" in result[
            "blockers"
        ]
        assert_world_unchanged(root, before)

        root = base / "no-post-seed"
        before, cycle, source_seed = prepare_cycle(root, "no-post-seed")
        plan = build_plan(before, cycle, source_seed, suffix="no-post-seed")
        plan["assimilation_policy"]["min_post_assimilation_seed_weight"] = 0.99
        plan["assimilation_plan_digest"] = assimilation_plan_digest(plan)
        result = run_assimilation(root, plan)
        assert result["status"] == "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_READY", result
        assert result["post_assimilation_seed_count"] == 0
        changed = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        assert changed["indra_qi_world_state_digest"] != before[
            "indra_qi_world_state_digest"
        ]
        empty_seed = read_json(
            root / "indra_qi_post_assimilation_projection_seed_v0_6.json"
        )
        assert empty_seed["seed_entries"] == []
        assert empty_seed["seed_status"] == "post_assimilation_projection_seed_ready"

    print("indra_qi_process_tensor_world_assimilation_v0_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
