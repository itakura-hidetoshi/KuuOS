import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_routed_daemon_cycle_runner_v0_1 import run_qi_routed_daemon_cycle

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "routed-001",
    "next_cycle_id": "routed-002",
    "generated_at_utc": "2026-05-21T00:00:00+00:00",
    "dispatched_at_utc": "2026-05-21T00:00:01+00:00",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "physical_process_visible": True,
    "thermodynamic_activity_visible": True,
    "process_history": PROCESS_HISTORY,
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}

EVIDENCE = {
    "boundary_review_evidence": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "identity_blocker": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
    "runtime_variation_visible": True,
    "policy_candidate_receipt": True,
    "value_witness_receipt": True,
    "barrier_witness_receipt": True,
    "candidate_only": True,
    "nonfinal_marker": True,
    "hold_review_evidence": True,
}


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class QiRoutedDaemonCycleRunnerTests(unittest.TestCase):
    def test_routed_daemon_cycle_writes_full_policy_candidate_feedback_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            write_json(raw_path, RAW)
            write_json(evidence_path, EVIDENCE)
            result = run_qi_routed_daemon_cycle(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=daemon_dir,
                dispatch_dir=dispatch_dir,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
            )
            self.assertIn(result.runner_status, {
                "QI_ROUTED_DAEMON_CYCLE_DISPATCHED",
                "QI_ROUTED_DAEMON_CYCLE_ROUTED_NON_EXECUTING",
            })
            self.assertEqual(result.daemon_ticks_run, 1)
            self.assertTrue(Path(result.daemon_result_path).is_file())
            self.assertTrue(Path(result.surface_path).is_file())
            self.assertTrue(Path(result.route_path).is_file())
            self.assertTrue(Path(result.dispatch_result_path).is_file())
            self.assertTrue(Path(result.feedback_path).is_file())
            self.assertTrue(Path(result.policy_feedback_surface_path).is_file())
            self.assertTrue(Path(result.policy_candidate_adapter_path).is_file())
            self.assertTrue(Path(result.policy_candidate_admission_path).is_file())
            self.assertTrue(Path(result.admitted_policy_candidate_handoff_path).is_file())
            self.assertTrue(Path(result.policy_flow_handoff_receiver_path).is_file())
            self.assertTrue(Path(result.policy_flow_candidate_inbox_path).is_file())
            self.assertTrue(Path(result.policy_flow_candidate_intake_view_path).is_file())
            self.assertTrue(Path(result.policy_flow_candidate_shadow_evaluator_path).is_file())
            self.assertTrue(Path(result.final_raw_state_path).is_file())
            self.assertTrue(Path(result.final_state_bundle_path).is_file())
            route = load(Path(result.route_path))
            dispatch = load(Path(result.dispatch_result_path))
            feedback = load(Path(result.feedback_path))
            policy_feedback = load(Path(result.policy_feedback_surface_path))
            candidate_adapter = load(Path(result.policy_candidate_adapter_path))
            admission = load(Path(result.policy_candidate_admission_path))
            handoff = load(Path(result.admitted_policy_candidate_handoff_path))
            receiver = load(Path(result.policy_flow_handoff_receiver_path))
            inbox = load(Path(result.policy_flow_candidate_inbox_path))
            intake_view = load(Path(result.policy_flow_candidate_intake_view_path))
            shadow_eval = load(Path(result.policy_flow_candidate_shadow_evaluator_path))
            self.assertEqual(route["next_outer_action"], result.next_outer_action)
            self.assertEqual(dispatch["dispatcher_status"], result.dispatcher_status)
            self.assertEqual(feedback["feedback_signal"], result.feedback_signal)
            self.assertEqual(feedback["policy_adjustment_hint"], result.policy_adjustment_hint)
            self.assertEqual(policy_feedback["policy_feedback_class"], result.policy_feedback_class)
            self.assertEqual(policy_feedback["policy_flow_candidate_signal"], result.policy_flow_candidate_signal)
            self.assertEqual(policy_feedback["active_inference_candidate_signal"], result.active_inference_candidate_signal)
            self.assertEqual(candidate_adapter["candidate_adjustment_class"], result.candidate_adjustment_class)
            self.assertEqual(candidate_adapter["recommended_candidate_action"], result.recommended_candidate_action)
            self.assertEqual(candidate_adapter["candidate_priority"], result.candidate_priority)
            self.assertEqual(admission["admission_decision"], result.admission_decision)
            self.assertEqual(admission["admission_reason"], result.admission_reason)
            self.assertEqual(admission["admitted_candidate_action"], result.admitted_candidate_action)
            self.assertEqual(handoff["handoff_decision"], result.handoff_decision)
            self.assertEqual(handoff["handoff_reason"], result.handoff_reason)
            self.assertEqual(handoff["handoff_decision"] == "QI_POLICY_CANDIDATE_HANDOFF_READY", result.policy_flow_handoff_ready)
            self.assertEqual(receiver["intake_decision"], result.policy_flow_intake_decision)
            self.assertEqual(receiver["policy_flow_candidate_available"], result.policy_flow_candidate_available)
            self.assertEqual(receiver["policy_flow_candidate_action"], result.policy_flow_candidate_action)
            self.assertEqual(inbox["inbox_decision"], result.policy_flow_inbox_decision)
            self.assertEqual(inbox["queued_candidate_available"], result.policy_flow_inbox_queued)
            self.assertEqual(inbox["queued_candidate_action"], result.policy_flow_inbox_action)
            self.assertEqual(intake_view["view_decision"], result.policy_flow_view_decision)
            self.assertEqual(intake_view["policy_flow_view_available"], result.policy_flow_view_available)
            self.assertEqual(intake_view["candidate_action"], result.policy_flow_view_action)
            self.assertEqual(shadow_eval["shadow_decision"], result.policy_flow_shadow_decision)
            self.assertEqual(shadow_eval["candidate_shadow_score"], result.policy_flow_shadow_score)
            self.assertEqual(shadow_eval["candidate_shadow_grade"], result.policy_flow_shadow_grade)
            self.assertIn("candidate_weight_hints", candidate_adapter)
            self.assertIn("policy_candidate_constraints", candidate_adapter)
            self.assertIn("policy_flow_handoff_payload", handoff)
            self.assertIn("normalized_policy_flow_intake", receiver)
            self.assertIn("inbox_packet", inbox)
            self.assertIn("policy_flow_candidate_view", intake_view)
            self.assertIn("boundary_markers", shadow_eval)
            self.assertTrue(shadow_eval["shadow_only"])
            self.assertTrue(shadow_eval["read_only"])
            self.assertFalse(result.grants_truth_authority)
            self.assertFalse(result.grants_memory_overwrite_authority)

    def test_routed_daemon_cycle_respects_reentry_cap_when_invoked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            write_json(raw_path, RAW)
            write_json(evidence_path, EVIDENCE)
            result = run_qi_routed_daemon_cycle(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=daemon_dir,
                dispatch_dir=dispatch_dir,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
            )
            self.assertLessEqual(result.reentry_cycles_run, 1)
            self.assertLessEqual(result.reentry_ticks_invoked, 1)


if __name__ == "__main__":
    unittest.main()
