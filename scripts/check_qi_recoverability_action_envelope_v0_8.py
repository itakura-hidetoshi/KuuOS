#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_recovery_action_core_v0_8 import (
    action_plan_digest,
    valid_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    read_json,
    records,
    write_json,
)
from scripts.qi_recovery_action_v0_8_test_support import (
    action_license,
    build_plan,
    latest,
    prepare_reentry,
    run_action,
)


def assert_states_unchanged(
    root: pathlib.Path,
    child: pathlib.Path,
    parent_digest: str,
    child_digest: str,
) -> None:
    parent = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    causal = read_json(child / "kuuos_causal_world_model_state_v14_0.json")
    assert parent["indra_qi_world_state_digest"] == parent_digest
    assert compute_indra_qi_world_state_digest(parent) == parent_digest
    assert causal["world_model_digest"] == child_digest
    assert valid_v14_digest(causal, "world_model_digest")


def force_bounded(plan: dict) -> None:
    policy = plan["gate_policy"]
    policy["observe_only_risk_threshold"] = 1.0
    policy["counterfactual_first_risk_threshold"] = 1.0
    policy["minimum_intervention_recoverability"] = 0.0
    policy["maximum_intervention_debt"] = 1.0
    policy["minimum_intervention_corridor_openness"] = 0.0
    plan["action_plan_digest"] = action_plan_digest(plan)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        world, _, reentry, child, generated, causal = prepare_reentry(root, "success")
        parent_digest = world["indra_qi_world_state_digest"]
        child_digest = causal["world_model_digest"]
        plan = build_plan(world, reentry, suffix="success")
        force_bounded(plan)
        result = run_action(root, plan)
        assert result["status"] == "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_READY", result
        assert result["envelope_status"] == "recoverability_gated_action_candidates_ready"
        assert result["variable_gate_count"] == 2
        assert result["observation_request_count"] == 2
        assert result["counterfactual_candidate_count"] == 1
        assert result["bounded_intervention_candidate_count"] == 1
        assert result["undo_reserve_count"] == 1
        assert result["action_executed"] is False
        assert result["v14_command_invoked"] is False
        assert result["parent_world_state_unchanged"] is True
        assert result["child_causal_world_unchanged"] is True
        assert_states_unchanged(root, child, parent_digest, child_digest)

        envelope = read_json(root / "indra_qi_recoverability_action_envelope_v0_8.json")
        activation = read_json(
            root / "indra_qi_recoverability_action_envelope_record_v0_8.json"
        )
        ledger = latest(
            root / "indra_qi_recoverability_action_envelope_ledger_v0_8.jsonl"
        )
        assert valid_digest(envelope, "action_envelope_digest")
        assert valid_digest(activation, "activation_record_digest")
        assert valid_digest(ledger, "record_digest")
        assert activation["source_action_envelope_digest"] == envelope[
            "action_envelope_digest"
        ]
        assert ledger["source_activation_record_digest"] == activation[
            "activation_record_digest"
        ]
        assert envelope["source_reentry_record_digest"] == reentry[
            "reentry_record_digest"
        ]
        assert envelope["source_world_state_digest"] == parent_digest
        assert envelope["source_v14_world_model_digest"] == child_digest
        assert envelope["boundary"]["no_v14_command_invoked"] is True
        assert envelope["boundary"]["envelope_contains_candidates_only"] is True

        gates = {gate["binding_kind"]: gate for gate in envelope["variable_gates"]}
        assert gates["qi_flow_observable_projection"]["gate_mode"] == "observe_only"
        assert gates["local_patch_observable"]["gate_mode"] == "bounded_intervention_candidate"
        flow_name = gates["qi_flow_observable_projection"]["variable_name"]
        local_name = gates["local_patch_observable"]["variable_name"]
        assert all(
            candidate["source_causal_variable"] != flow_name
            for candidate in envelope["counterfactual_candidates"]
            + envelope["bounded_intervention_candidates"]
            + envelope["undo_reserves"]
        )
        assert envelope["bounded_intervention_candidates"][0][
            "source_causal_variable"
        ] == local_name
        assert envelope["undo_reserves"][0]["source_causal_variable"] == local_name
        assert envelope["bounded_intervention_candidates"][0]["candidate_payload"][
            "snapshot_required"
        ] is True
        assert envelope["undo_reserves"][0]["candidate_payload"][
            "undo_license_required"
        ] is True
        for collection in (
            "observation_requests",
            "counterfactual_candidates",
            "bounded_intervention_candidates",
            "undo_reserves",
        ):
            for candidate in envelope[collection]:
                assert valid_digest(candidate, "action_candidate_digest")
                assert candidate["boundary"]["candidate_only"] is True
                assert candidate["boundary"]["not_direct_execution"] is True
                assert candidate["boundary"]["fresh_license_required"] is True
        assert len(generated["variables"]) == 3

        ledger_count = len(
            records(root / "indra_qi_recoverability_action_envelope_ledger_v0_8.jsonl")
        )
        replay = run_action(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "recovery_action_envelope_id_replay" in replay["blockers"]
        assert "recovery_action_source_reentry_replay" in replay["blockers"]
        assert replay["action_executed"] is False
        assert len(
            records(root / "indra_qi_recoverability_action_envelope_ledger_v0_8.jsonl")
        ) == ledger_count
        assert_states_unchanged(root, child, parent_digest, child_digest)

        root = base / "counterfactual"
        world, _, reentry, child, _, causal = prepare_reentry(root, "counterfactual")
        plan = build_plan(world, reentry, suffix="counterfactual")
        policy = plan["gate_policy"]
        policy["observe_only_risk_threshold"] = 1.0
        policy["counterfactual_first_risk_threshold"] = 0.0
        policy["minimum_intervention_recoverability"] = 0.0
        policy["maximum_intervention_debt"] = 1.0
        policy["minimum_intervention_corridor_openness"] = 0.0
        plan["action_plan_digest"] = action_plan_digest(plan)
        result = run_action(root, plan)
        assert result["status"].endswith("READY")
        assert result["observation_request_count"] == 2
        assert result["counterfactual_candidate_count"] == 1
        assert result["bounded_intervention_candidate_count"] == 0
        assert result["undo_reserve_count"] == 0
        assert_states_unchanged(
            root,
            child,
            world["indra_qi_world_state_digest"],
            causal["world_model_digest"],
        )

        root = base / "observe-only"
        world, _, reentry, child, _, causal = prepare_reentry(root, "observe-only")
        plan = build_plan(world, reentry, suffix="observe-only")
        plan["gate_policy"]["observe_only_risk_threshold"] = 0.0
        plan["gate_policy"]["counterfactual_first_risk_threshold"] = 0.0
        plan["action_plan_digest"] = action_plan_digest(plan)
        result = run_action(root, plan)
        assert result["status"].endswith("READY")
        assert result["observation_request_count"] == 2
        assert result["counterfactual_candidate_count"] == 0
        assert result["bounded_intervention_candidate_count"] == 0
        assert result["undo_reserve_count"] == 0
        assert_states_unchanged(
            root,
            child,
            world["indra_qi_world_state_digest"],
            causal["world_model_digest"],
        )

        root = base / "budget"
        world, _, reentry, _, _, _ = prepare_reentry(root, "budget")
        plan = build_plan(world, reentry, suffix="budget")
        force_bounded(plan)
        plan["gate_policy"]["max_observation_requests"] = 1
        plan["gate_policy"]["max_counterfactual_candidates"] = 0
        plan["gate_policy"]["max_intervention_candidates"] = 0
        plan["action_plan_digest"] = action_plan_digest(plan)
        result = run_action(root, plan)
        assert result["status"].endswith("READY")
        assert result["observation_request_count"] == 1
        assert result["counterfactual_candidate_count"] == 0
        assert result["bounded_intervention_candidate_count"] == 0
        assert result["undo_reserve_count"] == 0

        root = base / "world-tamper"
        world, _, reentry, _, _, _ = prepare_reentry(root, "world-tamper")
        plan = build_plan(world, reentry, suffix="world-tamper")
        world["local_patch_dynamic_states"][0]["observation_debt"] = 0.999
        write_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json", world)
        result = run_action(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_source_world_state_digest_invalid" in result[
            "blockers"
        ]
        assert "recovery_action_source_dynamic_world_state_digest_invalid" in result[
            "blockers"
        ]

        root = base / "projection-tamper"
        world, _, reentry, child, generated, _ = prepare_reentry(root, "projection-tamper")
        plan = build_plan(world, reentry, suffix="projection-tamper")
        first = next(iter(generated["variables"]))
        generated["variables"][first]["value"] = 0.999
        write_json(child / "indra_qi_generated_causal_projection_plan_v0_7.json", generated)
        result = run_action(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_generated_projection_plan_digest_mismatch" in result[
            "blockers"
        ]

        root = base / "v14-tamper"
        world, _, reentry, child, _, causal = prepare_reentry(root, "v14-tamper")
        plan = build_plan(world, reentry, suffix="v14-tamper")
        first = next(iter(causal["variables"]))
        causal["variables"][first]["value"] = 0.999
        write_json(child / "kuuos_causal_world_model_state_v14_0.json", causal)
        result = run_action(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_v14_world_model_digest_invalid" in result["blockers"]
        assert "recovery_action_child_causal_world_changed" in result["blockers"]

        root = base / "reentry-tamper"
        world, _, reentry, _, _, _ = prepare_reentry(root, "reentry-tamper")
        plan = build_plan(world, reentry, suffix="reentry-tamper")
        reentry["causal_world_id"] = "tampered-world"
        write_json(
            root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json",
            reentry,
        )
        result = run_action(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_source_reentry_digest_invalid" in result["blockers"]

        root = base / "license-kinds"
        world, _, reentry, _, _, _ = prepare_reentry(root, "license-kinds")
        plan = build_plan(world, reentry, suffix="license-kinds")
        license_value = action_license(plan)
        license_value["allowed_action_kinds"] = ["observation_request"]
        result = run_action(root, plan, license_value)
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_license_allowed_action_kinds_not_exact" in result[
            "blockers"
        ]

        root = base / "license-digest"
        world, _, reentry, _, _, _ = prepare_reentry(root, "license-digest")
        plan = build_plan(world, reentry, suffix="license-digest")
        result = run_action(
            root,
            plan,
            action_license(plan, bound_action_plan_digest="mismatch"),
        )
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_license_plan_digest_mismatch" in result[
            "blockers"
        ]

        root = base / "boundary"
        world, _, reentry, _, _, _ = prepare_reentry(root, "boundary")
        plan = build_plan(world, reentry, suffix="boundary")
        plan["boundary"]["qi_flow_observation_only"] = False
        plan["action_plan_digest"] = action_plan_digest(plan)
        result = run_action(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_boundary_qi_flow_observation_only_mismatch" in result[
            "blockers"
        ]

        root = base / "source-mismatch"
        world, _, reentry, _, _, _ = prepare_reentry(root, "source-mismatch")
        plan = build_plan(world, reentry, suffix="source-mismatch")
        plan["source_v14_world_model_digest"] = "mismatch"
        plan["action_plan_digest"] = action_plan_digest(plan)
        result = run_action(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "recovery_action_plan_source_v14_world_model_digest_mismatch" in result[
            "blockers"
        ]

    print("qi_recoverability_action_envelope_v0_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
