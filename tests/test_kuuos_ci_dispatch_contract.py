"""Synthetic sender/receiver contract tests; never contact GitHub or run Lean."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime import kuuos_github_ci_completion_reentry_v1_1 as receiver
from runtime import kuuos_github_public_ci_completion_poller_v1_2 as sender


class DispatchPayloadContractTests(unittest.TestCase):
    def setUp(self):
        self.run = {
            "id": 42,
            "name": sender.SOURCE_WORKFLOW_NAME,
            "head_sha": "a" * 40,
            "head_branch": "synthetic-ci-contract",
            "status": "completed",
            "conclusion": "success",
            "event": "pull_request",
            "pull_requests": [{"number": 7}],
        }
        self.completion = {
            "repository": sender.SOURCE_REPO,
            "run_id": 42,
            "workflow_name": sender.SOURCE_WORKFLOW_NAME,
            "head_sha": "a" * 40,
            "head_branch": "synthetic-ci-contract",
            "status": "completed",
            "conclusion": "success",
            "run_event": "pull_request",
            "required_job_names": [sender.REQUIRED_JOB],
            "required_step_names": [sender.REQUIRED_STEP],
            "source_pr_number": 7,
            "source_base_ref": sender.CANONICAL_BASE,
            "wakeup_is_success_evidence": False,
            "fresh_mcp_reobservation_required": True,
            "source_transport": "public_github_rest_poll_then_kuuos_self_dispatch",
        }
        self.envelope = {"schema_version": 2, "completion": self.completion}
        self.observed_run = {"repository": sender.SOURCE_REPO, **self.run}
        self.jobs = [{
            "name": sender.REQUIRED_JOB,
            "status": "completed",
            "conclusion": "success",
            "steps": [{
                "name": sender.REQUIRED_STEP,
                "status": "completed",
                "conclusion": "success",
            }],
        }]

    def compile(self, payload):
        return receiver.compile_completion_event(
            {"client_payload": payload},
            event_name="repository_dispatch",
            repository_allowlist=[sender.SOURCE_REPO],
            workflow_allowlist=[sender.SOURCE_WORKFLOW_NAME],
        )

    def assert_wakeup_only(self, compiled):
        packet = compiled["event_packet"]
        self.assertIs(packet["signal_is_success_evidence"], False)
        self.assertIs(packet["fresh_mcp_reobservation_required"], True)
        self.assertEqual(packet["boundary"], {
            "github_event_is_wakeup_signal_only": True,
            "github_event_does_not_prove_ci_success": True,
            "mcp_fresh_observation_required_before_reentry": True,
            "reentry_does_not_grant_merge_or_write_authority": True,
        })

    def test_sender_uses_two_key_v2_envelope_without_dropping_legacy_fields(self):
        payload = sender.make_dispatch_payload(self.run)
        self.assertEqual(payload, self.envelope)
        self.assertLessEqual(len(payload), 10)
        self.assertLess(len(json.dumps(payload).encode("utf-8")), 65536)
        self.assertEqual(len(payload["completion"]), 15)

    def test_real_sender_payload_compiles_to_exact_bounded_reobservation(self):
        compiled = self.compile(sender.make_dispatch_payload(self.run))
        self.assertEqual(compiled["event_packet"]["status"], receiver.READY)
        self.assert_wakeup_only(compiled)
        request = compiled["reobserve_request"]
        self.assertEqual(request["repo_full_name"], sender.SOURCE_REPO)
        self.assertEqual(request["run_id"], 42)
        self.assertEqual(request["expected_head_sha"], "a" * 40)
        self.assertEqual(request["expected_workflow_name"], sender.SOURCE_WORKFLOW_NAME)
        self.assertEqual(request["required_job_names"], [sender.REQUIRED_JOB])
        self.assertEqual(request["required_step_names"], [sender.REQUIRED_STEP])
        self.assertIs(request["fresh_mcp_reobservation_required"], True)

    def test_v2_and_legacy_flat_payloads_normalize_to_the_same_event(self):
        legacy = self.compile(self.completion)
        nested = self.compile(self.envelope)
        self.assertEqual(legacy["event_packet"]["status"], receiver.READY)
        self.assertEqual(nested["event_packet"]["status"], receiver.READY)
        self.assertEqual(nested["event_packet"]["event"], legacy["event_packet"]["event"])
        self.assertNotEqual(nested["event_packet"]["event_digest"], legacy["event_packet"]["event_digest"])
        for compiled in (legacy, nested):
            self.assert_wakeup_only(compiled)

    def test_unsupported_or_malformed_versions_cannot_fall_back_to_flat_fields(self):
        for version in (None, False, True, "2", 2.0, 1, 3, [], {}):
            for payload in ({"schema_version": version, "completion": self.completion},
                            {**self.completion, "schema_version": version}):
                with self.subTest(version=version, payload=payload):
                    compiled = self.compile(payload)
                    self.assertEqual(compiled["event_packet"]["status"], receiver.BLOCKED)
                    self.assertEqual(compiled["reobserve_request"], {})
                    self.assert_wakeup_only(compiled)

    def test_malformed_envelopes_cannot_fall_back_to_valid_flat_fields(self):
        payloads = [
            {"completion": self.completion},
            {**self.completion, "completion": self.completion},
            {"schema_version": 2},
            {**self.completion, **self.envelope},
            {**self.envelope, "unexpected": "value"},
        ]
        for completion in (None, False, 7, "{}", [], {}):
            payloads.append({"schema_version": 2, "completion": completion})
        for payload in payloads:
            with self.subTest(payload=payload):
                compiled = self.compile(payload)
                self.assertEqual(compiled["event_packet"]["status"], receiver.BLOCKED)
                self.assertEqual(compiled["reobserve_request"], {})
                self.assert_wakeup_only(compiled)

    def test_non_object_payloads_fail_closed(self):
        for payload in (None, False, 7, "{}", []):
            with self.subTest(payload=payload):
                compiled = self.compile(payload)
                self.assertEqual(compiled["event_packet"]["status"], receiver.BLOCKED)
                self.assertEqual(compiled["reobserve_request"], {})

    def test_v2_inner_fields_still_require_exact_identity_and_terminal_state(self):
        invalid = (
            ("repository", "other/repository", "repository_not_allowlisted"),
            ("workflow_name", "Other workflow", "workflow_not_allowlisted"),
            ("run_id", 0, "run_id_invalid"),
            ("head_sha", "bad-sha", "head_sha_invalid"),
            ("status", "in_progress", "workflow_run_not_completed"),
            ("conclusion", None, "workflow_conclusion_not_terminal"),
        )
        for field, value, blocker in invalid:
            with self.subTest(field=field):
                payload = copy.deepcopy(self.envelope)
                payload["completion"][field] = value
                compiled = self.compile(payload)
                self.assertEqual(compiled["event_packet"]["status"], receiver.BLOCKED)
                self.assertIn(blocker, compiled["event_packet"]["blockers"])
                self.assertEqual(compiled["reobserve_request"], {})

    def test_v2_verification_preserves_exact_run_and_required_names(self):
        packet = self.compile(self.envelope)["event_packet"]
        for field, value, blocker in (
            ("repository", "other/repository", "observed_repository_mismatch"),
            ("id", 43, "observed_run_id_mismatch"),
            ("name", "Other workflow", "observed_workflow_name_mismatch"),
            ("head_sha", "b" * 40, "observed_head_sha_mismatch"),
        ):
            with self.subTest(field=field):
                observed_run = {**self.observed_run, field: value}
                result = receiver.verify_fresh_reobservation(
                    packet, observed_run=observed_run, observed_jobs=self.jobs)
                self.assertEqual(result["status"], receiver.VERIFY_BLOCKED)
                self.assertIn(blocker, result["blockers"])
        for kind, blocker in (
            ("job", "required_job_missing:" + sender.REQUIRED_JOB),
            ("step", "required_step_missing:" + sender.REQUIRED_STEP),
        ):
            with self.subTest(kind=kind):
                jobs = copy.deepcopy(self.jobs)
                target = jobs[0] if kind == "job" else jobs[0]["steps"][0]
                target["name"] += " near-match"
                result = receiver.verify_fresh_reobservation(
                    packet, observed_run=self.observed_run, observed_jobs=jobs)
                self.assertEqual(result["status"], receiver.VERIFY_BLOCKED)
                self.assertIn(blocker, result["blockers"])

    def test_terminal_success_and_non_success_still_need_fresh_observation(self):
        for conclusion in ("success", "failure", "cancelled", "skipped"):
            with self.subTest(conclusion=conclusion):
                payload = copy.deepcopy(self.envelope)
                payload["completion"]["conclusion"] = conclusion
                compiled = self.compile(payload)
                self.assertEqual(compiled["event_packet"]["status"], receiver.READY)
                self.assert_wakeup_only(compiled)
                result = receiver.verify_fresh_reobservation(
                    compiled["event_packet"],
                    observed_run={**self.observed_run, "conclusion": conclusion},
                    observed_jobs=self.jobs,
                )
                self.assertEqual(result["status"], receiver.VERIFIED)
                self.assertEqual(result["route"], "verified_success" if conclusion == "success" else "verified_non_success")
                self.assertIs(result["merge_authority_granted"], False)
                self.assertIs(result["write_authority_granted"], False)
                blocked = receiver.verify_fresh_reobservation(
                    compiled["event_packet"], observed_run=self.observed_run, observed_jobs=[])
                self.assertEqual(blocked["status"], receiver.VERIFY_BLOCKED)
                self.assertIn("fresh_jobs_missing", blocked["blockers"])

    def verify_jobs(self, jobs, payload=None):
        packet = self.compile(self.envelope if payload is None else payload)["event_packet"]
        return receiver.verify_fresh_reobservation(
            packet, observed_run=self.observed_run, observed_jobs=jobs)

    def assert_verification_blocked(self, result, blocker):
        self.assertEqual(result["status"], receiver.VERIFY_BLOCKED)
        self.assertEqual(result["route"], "blocked")
        self.assertIn(blocker, result["blockers"])
        self.assertIs(result["merge_authority_granted"], False)
        self.assertIs(result["write_authority_granted"], False)

    def test_duplicate_required_jobs_are_ambiguous_not_verified(self):
        jobs = self.jobs + copy.deepcopy(self.jobs)
        self.assert_verification_blocked(
            self.verify_jobs(jobs), "required_job_cardinality:" + sender.REQUIRED_JOB + ":2")

    def test_required_step_in_an_unrequired_job_cannot_satisfy_the_gate(self):
        jobs = copy.deepcopy(self.jobs)
        unrelated = copy.deepcopy(jobs[0])
        unrelated["name"] = "Unrequired job"
        jobs[0]["steps"] = []
        jobs.append(unrelated)
        self.assert_verification_blocked(
            self.verify_jobs(jobs), "required_step_missing:" + sender.REQUIRED_STEP)

    def test_unrequired_job_steps_do_not_create_required_step_ambiguity(self):
        jobs = copy.deepcopy(self.jobs)
        unrelated = copy.deepcopy(jobs[0])
        unrelated["name"] = "Unrequired job"
        jobs.append(unrelated)
        self.assertEqual(self.verify_jobs(jobs)["status"], receiver.VERIFIED)

    def test_duplicate_required_steps_are_rejected_within_selected_jobs(self):
        for across_jobs in (False, True):
            with self.subTest(across_jobs=across_jobs):
                jobs = copy.deepcopy(self.jobs)
                payload = copy.deepcopy(self.envelope)
                if across_jobs:
                    other = copy.deepcopy(jobs[0])
                    other["name"] = "Another required job"
                    jobs.append(other)
                    payload["completion"]["required_job_names"].append(other["name"])
                else:
                    jobs[0]["steps"].append(copy.deepcopy(jobs[0]["steps"][0]))
                self.assert_verification_blocked(
                    self.verify_jobs(jobs, payload),
                    "required_step_cardinality:" + sender.REQUIRED_STEP + ":2")

    def test_selected_job_conclusion_must_be_terminal(self):
        for conclusion in (None, "", "in_progress", [], {}):
            with self.subTest(conclusion=conclusion):
                jobs = copy.deepcopy(self.jobs)
                jobs[0]["conclusion"] = conclusion
                self.assert_verification_blocked(
                    self.verify_jobs(jobs), "required_job_conclusion_not_terminal:" + sender.REQUIRED_JOB)

    def test_required_step_conclusion_must_be_terminal(self):
        for conclusion in (None, "", "in_progress", [], {}):
            with self.subTest(conclusion=conclusion):
                jobs = copy.deepcopy(self.jobs)
                jobs[0]["steps"][0]["conclusion"] = conclusion
                reason = "required_step_conclusion_missing:" if conclusion is None else "required_step_conclusion_not_terminal:"
                self.assert_verification_blocked(self.verify_jobs(jobs), reason + sender.REQUIRED_STEP)

    def test_selected_job_and_step_accept_all_terminal_conclusions(self):
        for conclusion in ("success", "failure", "cancelled", "timed_out", "neutral",
                           "skipped", "stale", "action_required", "startup_failure"):
            with self.subTest(conclusion=conclusion):
                jobs = copy.deepcopy(self.jobs)
                jobs[0]["conclusion"] = conclusion
                jobs[0]["steps"][0]["conclusion"] = conclusion
                result = self.verify_jobs(jobs)
                self.assertEqual(result["status"], receiver.VERIFIED)
                self.assertIs(result["merge_authority_granted"], False)
                self.assertIs(result["write_authority_granted"], False)

    def test_workflow_run_without_required_names_retains_existing_behavior(self):
        raw = {"action": "completed", "repository": {"full_name": sender.SOURCE_REPO},
               "workflow_run": self.run}
        packet = receiver.compile_completion_event(raw, event_name="workflow_run")["event_packet"]
        jobs = copy.deepcopy(self.jobs)
        jobs[0]["conclusion"] = None
        jobs[0]["steps"] = []
        jobs += copy.deepcopy(jobs)
        result = receiver.verify_fresh_reobservation(
            packet, observed_run=self.observed_run, observed_jobs=jobs)
        self.assertEqual(result["status"], receiver.VERIFIED)
        self.assertIs(result["merge_authority_granted"], False)
        self.assertIs(result["write_authority_granted"], False)


if __name__ == "__main__":
    unittest.main()
