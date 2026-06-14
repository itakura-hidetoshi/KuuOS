#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_approved_action_core_v0_9 import (
    approval_digest,
    evidence_digest,
    execution_plan_digest,
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
from scripts.qi_action_v0_9_test_support import (
    build_execution_plan,
    execution_license,
    prepare_envelope,
    run_execution,
)


def latest(path: pathlib.Path) -> dict:
    values = records(path)
    return values[-1] if values else {}


def assert_parent_unchanged(root: pathlib.Path, digest: str) -> None:
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    assert world["indra_qi_world_state_digest"] == digest
    assert compute_indra_qi_world_state_digest(world) == digest


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "intervention"
        world, reentry, child, causal, source = prepare_envelope(
            root, "intervention", "bounded"
        )
        envelope = source["envelope"]
        activation = source["activation"]
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=envelope,
            activation=activation,
            kind="bounded_intervention_candidate",
            suffix="intervention",
        )
        variable_name = next(
            value["source_causal_variable"]
            for value in envelope["bounded_intervention_candidates"]
            if value["candidate_id"] == plan["selected_candidate_id"]
        )
        before_digest = causal["world_model_digest"]
        parent_digest = world["indra_qi_world_state_digest"]
        events_before = len(
            records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")
        )
        result = run_execution(root, plan, causal)
        assert result["status"] == "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_READY", result
        assert result["execution_status"] == "approved_action_applied_and_feedback_returned"
        assert result["selected_action_kind"] == "bounded_intervention_candidate"
        assert result["action_command_kind"] == "intervene"
        assert result["action_invoked"] is True
        assert result["action_ready"] is True
        assert result["state_mutated"] is True
        assert result["counterfactual_generated"] is False
        assert result["snapshot_verified"] is True
        assert result["undo_readiness_ready"] is True
        assert result["feedback_invoked"] is True
        assert result["feedback_ready"] is True
        assert result["feedback_candidate_count"] >= 2
        assert result["feedback_local_patch_candidate_count"] >= 1
        assert result["feedback_qi_flow_candidate_count"] == 1
        assert result["parent_world_state_unchanged"] is True
        assert result["child_indra_state_unchanged"] is True
        assert result["before_v14_world_model_digest"] == before_digest
        assert result["after_v14_world_model_digest"] != before_digest
        assert_parent_unchanged(root, parent_digest)

        child_state = read_json(child / "kuuos_causal_world_model_state_v14_0.json")
        assert valid_v14_digest(child_state, "world_model_digest")
        assert child_state["variables"][variable_name]["status"] == "intervened"
        assert child_state["variables"][variable_name]["value"] == plan[
            "approved_value"
        ]
        assert child_state["world_model_digest"] == result[
            "after_v14_world_model_digest"
        ]
        events = records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")
        assert len(events) == events_before + 1
        action_event = events[-1]
        assert valid_digest(action_event, "record_digest")
        assert action_event["command_kind"] == "intervene"
        assert action_event["record_digest"] == result["action_event_record_digest"]

        snapshot = read_json(
            child
            / "kuuos_causal_world_model_snapshots_v14_0"
            / f"{plan['action_transaction_id']}.json"
        )
        assert valid_v14_digest(snapshot, "world_model_digest")
        assert snapshot["world_model_digest"] == before_digest
        readiness = read_json(pathlib.Path(result["undo_readiness_path"]))
        assert valid_digest(readiness, "undo_readiness_digest")
        assert readiness["readiness_status"] == "undo_ready"
        assert readiness["source_undo_reserve_digest"]
        assert readiness["snapshot_world_model_digest"] == before_digest
        assert readiness["undo_command"]["payload"]["target_transaction_id"] == plan[
            "action_transaction_id"
        ]
        assert readiness["undo_license_packet"]["bound_command_digest"] == readiness[
            "undo_command"
        ]["command_digest"]
        assert readiness["boundary"]["undo_command_not_yet_executed"] is True

        feedback = read_json(
            child / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
        )
        handoff = read_json(
            child / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
        )
        feedback_ledger = latest(
            child / "indra_qi_causal_feedback_ledger_v0_3.jsonl"
        )
        assert valid_digest(feedback, "feedback_packet_digest")
        assert valid_digest(handoff, "approval_handoff_digest")
        assert valid_digest(feedback_ledger, "record_digest")
        assert feedback["source_causal_event_digest"] == action_event["record_digest"]
        assert feedback["source_causal_event_kind"] == "intervene"
        assert feedback["feedback_status"] == "feedback_candidates_ready"
        assert feedback["boundary"]["feedback_is_candidate_not_direct_mutation"] is True
        assert handoff["direct_application_allowed"] is False

        execution_record = read_json(
            root / "indra_qi_approved_recovery_action_execution_record_v0_9.json"
        )
        execution_ledger = latest(
            root / "indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl"
        )
        assert valid_digest(execution_record, "execution_record_digest")
        assert valid_digest(execution_ledger, "record_digest")
        assert execution_record["selected_candidate_digest"] == plan[
            "selected_candidate_digest"
        ]
        assert execution_record["feedback_packet_digest"] == feedback[
            "feedback_packet_digest"
        ]
        assert execution_ledger["source_execution_record_digest"] == execution_record[
            "execution_record_digest"
        ]

        execution_count = len(
            records(
                root / "indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl"
            )
        )
        event_count = len(events)
        replay = run_execution(root, plan, child_state)
        assert replay["status"].endswith("BLOCKED")
        assert "approved_action_execution_id_replay" in replay["blockers"]
        assert "approved_action_source_envelope_replay" in replay["blockers"]
        assert "approved_action_selected_candidate_replay" in replay["blockers"]
        assert replay["action_invoked"] is False
        assert len(
            records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")
        ) == event_count
        assert len(
            records(
                root / "indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl"
            )
        ) == execution_count

        root = base / "counterfactual"
        world, reentry, child, causal, source = prepare_envelope(
            root, "counterfactual", "counterfactual"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="counterfactual_candidate",
            suffix="counterfactual",
        )
        before_digest = causal["world_model_digest"]
        result = run_execution(root, plan, causal)
        assert result["status"].endswith("READY"), result
        assert result["action_command_kind"] == "counterfactual"
        assert result["state_mutated"] is False
        assert result["counterfactual_generated"] is True
        assert result["snapshot_verified"] is False
        assert result["undo_readiness_ready"] is False
        assert result["feedback_ready"] is True
        assert result["before_v14_world_model_digest"] == before_digest
        assert result["after_v14_world_model_digest"] == before_digest
        assert read_json(child / "kuuos_causal_world_model_state_v14_0.json")[
            "world_model_digest"
        ] == before_digest
        feedback = read_json(
            child / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
        )
        assert feedback["source_causal_event_kind"] == "counterfactual"
        assert feedback["boundary"]["causal_result_not_truth"] is True

        root = base / "observe"
        world, reentry, child, causal, source = prepare_envelope(
            root, "observe", "observe"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="observation_request",
            suffix="observe",
        )
        before_digest = causal["world_model_digest"]
        result = run_execution(root, plan, causal)
        assert result["status"].endswith("READY"), result
        assert result["action_command_kind"] == "observe"
        assert result["state_mutated"] is True
        assert result["counterfactual_generated"] is False
        assert result["snapshot_verified"] is True
        assert result["undo_readiness_ready"] is False
        assert result["feedback_ready"] is True
        assert result["after_v14_world_model_digest"] != before_digest
        feedback = read_json(
            child / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
        )
        assert feedback["source_causal_event_kind"] == "observe"

        root = base / "candidate-digest"
        world, reentry, child, causal, source = prepare_envelope(
            root, "candidate-digest", "bounded"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="candidate-digest",
        )
        plan["selected_candidate_digest"] = "mismatch"
        plan["approval"]["approved_candidate_digest"] = "mismatch"
        plan["approval"]["approval_digest"] = approval_digest(plan["approval"])
        plan["execution_plan_digest"] = execution_plan_digest(plan)
        event_count = len(
            records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")
        )
        blocked = run_execution(root, plan, causal)
        assert "approved_action_selected_candidate_digest_mismatch" in blocked[
            "blockers"
        ]
        assert blocked["action_invoked"] is False
        assert len(
            records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")
        ) == event_count

        root = base / "stale-evidence"
        world, reentry, child, causal, source = prepare_envelope(
            root, "stale-evidence", "bounded"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="stale-evidence",
        )
        plan["fresh_observation_evidence"]["observed_value"] = float(
            plan["fresh_observation_evidence"]["observed_value"]
        ) + 0.1
        plan["fresh_observation_evidence"]["evidence_digest"] = evidence_digest(
            plan["fresh_observation_evidence"]
        )
        plan["approval"]["source_evidence_digest"] = plan[
            "fresh_observation_evidence"
        ]["evidence_digest"]
        plan["approval"]["approval_digest"] = approval_digest(plan["approval"])
        plan["execution_plan_digest"] = execution_plan_digest(plan)
        blocked = run_execution(root, plan, causal)
        assert "approved_action_evidence_not_current_variable_value" in blocked[
            "blockers"
        ]
        assert blocked["action_invoked"] is False

        root = base / "approval-tamper"
        world, reentry, _, causal, source = prepare_envelope(
            root, "approval-tamper", "bounded"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="approval-tamper",
        )
        plan["approval"]["approval_id"] = "tampered"
        plan["execution_plan_digest"] = execution_plan_digest(plan)
        blocked = run_execution(root, plan, causal)
        assert "approved_action_approval_digest_invalid" in blocked["blockers"]
        assert blocked["action_invoked"] is False

        root = base / "delta"
        world, reentry, _, causal, source = prepare_envelope(root, "delta", "bounded")
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="delta",
        )
        candidate = next(
            value
            for value in source["envelope"]["bounded_intervention_candidates"]
            if value["candidate_id"] == plan["selected_candidate_id"]
        )
        plan["approved_value"] = float(candidate["candidate_payload"]["current_value"]) + float(
            candidate["candidate_payload"]["maximum_delta"]
        ) * 2.0
        plan["execution_plan_digest"] = execution_plan_digest(plan)
        blocked = run_execution(root, plan, causal)
        assert "approved_action_intervention_value_exceeds_maximum_delta" in blocked[
            "blockers"
        ]
        assert blocked["action_invoked"] is False

        root = base / "action-license"
        world, reentry, child, causal, source = prepare_envelope(
            root, "action-license", "bounded"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="action-license",
        )
        license_value = execution_license(plan, causal)
        license_value["v14_action_license_template"]["intervention_allowed"] = False
        count = len(records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"))
        blocked = run_execution(root, plan, causal, license_value)
        assert "approved_action_nested_v14_intervention_allowed_not_true" in blocked[
            "blockers"
        ]
        assert blocked["action_invoked"] is False
        assert len(records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")) == count

        root = base / "feedback-license"
        world, reentry, child, causal, source = prepare_envelope(
            root, "feedback-license", "bounded"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="feedback-license",
        )
        license_value = execution_license(plan, causal)
        license_value["v0_3_feedback_license_template"][
            "feedback_packet_write_allowed"
        ] = False
        count = len(records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"))
        blocked = run_execution(root, plan, causal, license_value)
        assert "approved_action_nested_feedback_feedback_packet_write_allowed_not_true" in blocked[
            "blockers"
        ]
        assert blocked["action_invoked"] is False
        assert len(records(child / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")) == count

        root = base / "envelope-tamper"
        world, reentry, _, causal, source = prepare_envelope(
            root, "envelope-tamper", "bounded"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="envelope-tamper",
        )
        source["envelope"]["bounded_intervention_candidates"][0][
            "candidate_priority"
        ] = 0.999
        write_json(
            root / "indra_qi_recoverability_action_envelope_v0_8.json",
            source["envelope"],
        )
        blocked = run_execution(root, plan, causal)
        assert "approved_action_source_envelope_digest_invalid" in blocked["blockers"]
        assert blocked["action_invoked"] is False

        root = base / "source-v14"
        world, reentry, _, causal, source = prepare_envelope(
            root, "source-v14", "bounded"
        )
        plan = build_execution_plan(
            world=world,
            reentry=reentry,
            causal=causal,
            envelope=source["envelope"],
            activation=source["activation"],
            kind="bounded_intervention_candidate",
            suffix="source-v14",
        )
        plan["source_v14_world_model_digest"] = "mismatch"
        plan["execution_plan_digest"] = execution_plan_digest(plan)
        blocked = run_execution(root, plan, causal)
        assert "approved_action_plan_source_v14_world_model_digest_mismatch" in blocked[
            "blockers"
        ]
        assert blocked["action_invoked"] is False

    print("qi_approved_action_execution_v0_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
