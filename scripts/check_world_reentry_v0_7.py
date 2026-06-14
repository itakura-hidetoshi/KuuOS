#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_post_assimilation_reentry_core_v0_7 import (
    reentry_plan_digest,
    valid_digest,
)
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    protected_constitution_digest,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    read_json,
    records,
    write_json,
)
from scripts.world_reentry_v0_7_test_support import (
    assert_parent_unchanged,
    build_plan,
    latest,
    prepare_assimilated,
    projection_template,
    reentry_license,
    rewrite_seed_chain,
    run_reentry,
    v14_template,
)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        world, assimilation, seed = prepare_assimilated(root, "success")
        parent_digest = world["indra_qi_world_state_digest"]
        parent_constitution = protected_constitution_digest(world)
        plan = build_plan(world, assimilation, seed, suffix="success")
        result = run_reentry(root, plan)
        assert result["status"] == "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_READY", result
        assert result["reentry_status"] == "post_assimilation_causal_world_initialized"
        assert result["projected_variable_count"] == 3
        assert result["observed_variable_count"] == 2
        assert result["qi_flow_variable_count"] == 1
        assert result["v0_2_projection_invoked"] is True
        assert result["v0_2_projection_ready"] is True
        assert result["v14_state_initialized"] is True
        assert result["parent_world_state_unchanged"] is True
        assert_parent_unchanged(root, parent_digest)

        child = pathlib.Path(result["child_runtime_root"])
        child_world = read_json(child / "ku_indra_qi_noncommutative_mandala_world_state.json")
        generated = read_json(child / "indra_qi_generated_causal_projection_plan_v0_7.json")
        packet = read_json(child / "indra_qi_causal_projection_packet_v0_2.json")
        activation = read_json(child / "indra_qi_causal_projection_activation_record_v0_2.json")
        causal_state = read_json(child / "kuuos_causal_world_model_state_v14_0.json")
        record = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
        ledger = latest(root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl")

        assert child_world["indra_qi_world_state_digest"] == parent_digest
        assert protected_constitution_digest(child_world) == parent_constitution
        assert generated["source_indra_qi_world_state_digest"] == parent_digest
        assert len(generated["variables"]) == 3
        observed = {
            name: value
            for name, value in generated["variables"].items()
            if value["status"] == "observed"
        }
        assert len(observed) == 2
        for variable in observed.values():
            conditioning = variable["world_conditioning"]
            assert conditioning["observation_debt"] > 0
            assert conditioning["recoverability_reserve"] < 1
            assert conditioning["intervention_residue"] > 0
            assert variable["uncertainty"] > 0
        flow_variables = [
            value
            for value in observed.values()
            if value["source_binding"]["binding_kind"]
            == "qi_flow_observable_projection"
        ]
        assert len(flow_variables) == 1
        assert flow_variables[0]["source_binding"]["qi_itself"] is False
        assert flow_variables[0]["source_binding"]["projection_not_flow_identity"] is True

        assert valid_digest(packet, "projection_packet_digest")
        assert valid_digest(activation, "activation_record_digest")
        assert valid_v14_digest(causal_state, "world_model_digest")
        assert causal_state["world_id"] == plan["causal_world_id"]
        assert set(causal_state["variables"]) == set(generated["variables"])
        for name, variable in observed.items():
            assert causal_state["variables"][name]["value"] == variable["value"]
            assert causal_state["variables"][name]["uncertainty"] == variable[
                "uncertainty"
            ]
        assert causal_state["variables"]["world_adaptive_response"]["value"] > 0
        assert packet["boundary"]["causal_edge_not_gauge_connection"] is True
        assert packet["boundary"]["source_indra_state_not_mutated"] is True

        assert valid_digest(record, "reentry_record_digest")
        assert record["source_world_state_digest"] == parent_digest
        assert record["projection_packet_digest"] == packet[
            "projection_packet_digest"
        ]
        assert record["projection_activation_digest"] == activation[
            "activation_record_digest"
        ]
        assert record["v14_world_model_digest"] == causal_state[
            "world_model_digest"
        ]
        assert valid_digest(ledger, "record_digest")
        assert ledger["source_reentry_record_digest"] == record[
            "reentry_record_digest"
        ]

        count = len(
            records(root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl")
        )
        replay = run_reentry(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "post_assimilation_reentry_id_replay" in replay["blockers"]
        assert "source_assimilation_reentry_replay" in replay["blockers"]
        assert "post_assimilation_reentry_child_runtime_already_exists" in replay[
            "blockers"
        ]
        assert replay["v0_2_projection_invoked"] is False
        assert len(
            records(root / "indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl")
        ) == count

        root = base / "seed-tamper"
        world, assimilation, seed = prepare_assimilated(root, "seed-tamper")
        plan = build_plan(world, assimilation, seed, suffix="seed-tamper")
        seed["seed_entries"][0]["assimilated_prior_weight"] = 0.999
        write_json(root / "indra_qi_post_assimilation_projection_seed_v0_6.json", seed)
        blocked = run_reentry(root, plan)
        assert "source_v0_6_seed_packet_digest_invalid" in blocked["blockers"]
        assert blocked["v0_2_projection_invoked"] is False

        root = base / "world-tamper"
        world, assimilation, seed = prepare_assimilated(root, "world-tamper")
        plan = build_plan(world, assimilation, seed, suffix="world-tamper")
        world["local_patch_dynamic_states"][0]["observation_debt"] = 0.999
        write_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
        blocked = run_reentry(root, plan)
        assert "source_assimilated_world_state_digest_invalid" in blocked[
            "blockers"
        ]
        assert "source_dynamic_world_state_digest_invalid" in blocked["blockers"]

        root = base / "old-digest"
        world, assimilation, seed = prepare_assimilated(root, "old-digest")
        plan = build_plan(world, assimilation, seed, suffix="old-digest")
        plan["source_world_state_digest"] = assimilation["before_world_state_digest"]
        plan["reentry_plan_digest"] = reentry_plan_digest(plan)
        blocked = run_reentry(root, plan)
        assert "post_assimilation_reentry_plan_source_world_state_digest_mismatch" in blocked[
            "blockers"
        ]
        assert blocked["v0_2_projection_invoked"] is False

        root = base / "empty-seed"
        world, assimilation, seed = prepare_assimilated(root, "empty-seed")
        seed["seed_entries"] = []
        seed["seed_entry_order"] = []
        seed, assimilation = rewrite_seed_chain(root, seed, assimilation)
        plan = build_plan(world, assimilation, seed, suffix="empty-seed")
        blocked = run_reentry(root, plan)
        assert "post_assimilation_reentry_seed_count_below_minimum" in blocked[
            "blockers"
        ]
        assert "post_assimilation_reentry_qi_flow_seed_missing" in blocked[
            "blockers"
        ]

        root = base / "no-flow"
        world, assimilation, seed = prepare_assimilated(root, "no-flow")
        seed["seed_entries"] = [
            entry for entry in seed["seed_entries"] if entry["target"].get("patch_id")
        ]
        seed["seed_entry_order"] = [entry["seed_id"] for entry in seed["seed_entries"]]
        seed, assimilation = rewrite_seed_chain(root, seed, assimilation)
        plan = build_plan(world, assimilation, seed, suffix="no-flow")
        plan["projection_policy"]["minimum_seed_count"] = 1
        plan["reentry_plan_digest"] = reentry_plan_digest(plan)
        blocked = run_reentry(root, plan)
        assert "post_assimilation_reentry_qi_flow_seed_missing" in blocked[
            "blockers"
        ]

        root = base / "license-digest"
        world, assimilation, seed = prepare_assimilated(root, "license-digest")
        plan = build_plan(world, assimilation, seed, suffix="license-digest")
        blocked = run_reentry(
            root,
            plan,
            reentry_license(plan, bound_reentry_plan_digest="mismatch"),
        )
        assert "post_assimilation_reentry_license_plan_digest_mismatch" in blocked[
            "blockers"
        ]

        root = base / "top-license"
        world, assimilation, seed = prepare_assimilated(root, "top-license")
        plan = build_plan(world, assimilation, seed, suffix="top-license")
        blocked = run_reentry(
            root,
            plan,
            reentry_license(plan, v0_2_projection_invoke_allowed=False),
        )
        assert "v0_2_projection_invoke_not_allowed" in blocked["blockers"]
        assert blocked["v0_2_projection_invoked"] is False
        assert not pathlib.Path(blocked["child_runtime_root"]).exists()

        root = base / "nested-license"
        world, assimilation, seed = prepare_assimilated(root, "nested-license")
        plan = build_plan(world, assimilation, seed, suffix="nested-license")
        nested = projection_template(
            v14_initialize_license_template=v14_template(state_write_allowed=False)
        )
        blocked = run_reentry(
            root,
            plan,
            reentry_license(plan, v0_2_projection_license_template=nested),
        )
        assert "post_assimilation_reentry_v0_2_projection_not_ready" in blocked[
            "blockers"
        ]
        assert blocked["v0_2_projection_invoked"] is True
        assert blocked["v0_2_projection_ready"] is False

        root = base / "derived-patch"
        world, assimilation, seed = prepare_assimilated(root, "derived-patch")
        plan = build_plan(world, assimilation, seed, suffix="derived-patch")
        plan["derived_response_patch_id"] = "missing-patch"
        plan["reentry_plan_digest"] = reentry_plan_digest(plan)
        blocked = run_reentry(root, plan)
        assert "post_assimilation_reentry_derived_patch_unknown" in blocked[
            "blockers"
        ]
        assert blocked["v0_2_projection_invoked"] is False

        root = base / "child-exists"
        world, assimilation, seed = prepare_assimilated(root, "child-exists")
        plan = build_plan(world, assimilation, seed, suffix="child-exists")
        child = root / "indra_qi_causal_reentry_cycles_v0_7" / plan["reentry_id"]
        child.mkdir(parents=True)
        blocked = run_reentry(root, plan)
        assert "post_assimilation_reentry_child_runtime_already_exists" in blocked[
            "blockers"
        ]

        root = base / "boundary"
        world, assimilation, seed = prepare_assimilated(root, "boundary")
        plan = build_plan(world, assimilation, seed, suffix="boundary")
        plan["boundary"]["debt_conditions_causal_projection"] = False
        plan["reentry_plan_digest"] = reentry_plan_digest(plan)
        blocked = run_reentry(root, plan)
        assert "post_assimilation_reentry_boundary_debt_conditions_causal_projection_mismatch" in blocked[
            "blockers"
        ]

    print("world_reentry_v0_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
