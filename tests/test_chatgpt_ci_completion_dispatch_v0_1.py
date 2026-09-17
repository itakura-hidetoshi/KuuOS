import json
import unittest

from scripts.chatgpt_ci_completion_dispatch_v0_1 import (
    build_comment,
    process_event,
    producer_marker,
    validate_dispatch_payload,
    verify_run,
)

KUUOS = "itakura-hidetoshi/KuuOS"
MGAP = "itakura-hidetoshi/4d-mass-gap"
SHA = "a" * 40


def payload(repo=KUUOS, workflow="KuuOS PR Governance Gate", **overrides):
    p = {
        "repository": repo,
        "pull_request": 77,
        "run_id": 123,
        "run_attempt": 1,
        "head_sha": SHA,
        "head_branch": "feature/x",
        "workflow": workflow,
    }
    p.update(overrides)
    return {"action": "chatgpt_ci_completion_dispatch_v0_1", "client_payload": p}


def run(status="completed", conclusion="success", **overrides):
    r = {
        "id": 123,
        "run_attempt": 1,
        "name": "KuuOS PR Governance Gate",
        "event": "pull_request",
        "head_sha": SHA,
        "head_branch": "feature/x",
        "status": status,
        "conclusion": conclusion,
        "html_url": "https://github.com/itakura-hidetoshi/KuuOS/actions/runs/123",
        "updated_at": "2026-09-18T00:00:00Z",
    }
    r.update(overrides)
    return r


class FakeGitHub:
    def __init__(self, runs, comments=None, pr=None):
        self.runs = list(runs)
        self.comments = list(comments or [])
        self.pr = pr or {
            "number": 77,
            "head": {"sha": SHA, "repo": {"full_name": KUUOS}},
        }
        self.created = []
        self.run_reads = 0

    def get_workflow_run(self, repository, run_id):
        self.run_reads += 1
        if len(self.runs) > 1:
            return self.runs.pop(0)
        return self.runs[0]

    def get_pull_request(self, repository, pr_number):
        return self.pr

    def list_issue_comments(self, repository, pr_number):
        return self.comments

    def create_issue_comment(self, repository, pr_number, body):
        self.created.append((repository, pr_number, body))
        return {"id": 999}


class DispatchValidationTests(unittest.TestCase):
    def test_accepts_kuuos_payload(self):
        ident = validate_dispatch_payload(payload(), KUUOS)
        self.assertIsNotNone(ident)
        self.assertEqual(ident.repository, KUUOS)
        self.assertEqual(ident.workflow, "KuuOS PR Governance Gate")

    def test_accepts_mgap_payload(self):
        ident = validate_dispatch_payload(payload(MGAP, "PR Lean Fast Check"), MGAP)
        self.assertIsNotNone(ident)
        self.assertEqual(ident.repository, MGAP)

    def test_rejects_wrong_repository(self):
        self.assertIsNone(validate_dispatch_payload(payload("someone/else"), KUUOS))

    def test_rejects_wrong_workflow(self):
        self.assertIsNone(validate_dispatch_payload(payload(workflow="Other"), KUUOS))

    def test_rejects_wrong_action(self):
        event = payload()
        event["action"] = "other"
        self.assertIsNone(validate_dispatch_payload(event, KUUOS))

    def test_rejects_invalid_run_attempt_or_sha(self):
        self.assertIsNone(validate_dispatch_payload(payload(run_id=0), KUUOS))
        self.assertIsNone(validate_dispatch_payload(payload(run_attempt=0), KUUOS))
        self.assertIsNone(validate_dispatch_payload(payload(head_sha="bad"), KUUOS))


class ExactRunTests(unittest.TestCase):
    def setUp(self):
        self.ident = validate_dispatch_payload(payload(), KUUOS)

    def test_verifies_exact_completed_pull_request_run(self):
        self.assertTrue(verify_run(self.ident, run()))

    def test_rejects_identity_mismatch(self):
        for bad in [
            run(id=124),
            run(run_attempt=2),
            run(name="Other"),
            run(event="push"),
            run(head_sha="b" * 40),
        ]:
            self.assertFalse(verify_run(self.ident, bad))

    def test_nonterminal_run_is_not_verified(self):
        self.assertFalse(
            verify_run(self.ident, run(status="in_progress", conclusion=None))
        )


class MarkerTests(unittest.TestCase):
    def setUp(self):
        self.ident = validate_dispatch_payload(payload(), KUUOS)

    def test_producer_marker_is_distinct_and_keeps_trigger_substring(self):
        marker = producer_marker(self.ident)
        self.assertIn("CHATGPT_CI_COMPLETION_PUSH_V0_1", marker)
        self.assertIn("producer=repository_dispatch_v0_1", marker)
        self.assertIn("run_id=123", marker)
        self.assertIn("attempt=1", marker)
        self.assertIn("pr=77", marker)

    def test_comment_packet_identifies_secondary_producer(self):
        body = build_comment(self.ident, run(), polling_used=True)
        self.assertIn(producer_marker(self.ident), body)
        packet = json.loads(body.split("```json\n", 1)[1].split("\n```", 1)[0])
        self.assertEqual(packet["version"], "chatgpt_ci_completion_push_v0_3")
        self.assertEqual(packet["producer"], "repository_dispatch_v0_1")
        self.assertTrue(packet["polling_used"])
        self.assertTrue(packet["event_is_wakeup_signal_only"])
        self.assertTrue(packet["fresh_mcp_reobservation_required"])


class ProcessTests(unittest.TestCase):
    def test_in_progress_then_completed_uses_bounded_polling(self):
        gh = FakeGitHub([run(status="in_progress", conclusion=None), run()])
        sleeps = []
        result = process_event(
            payload(),
            gh,
            repository=KUUOS,
            sleep_fn=sleeps.append,
            delays=(0.0, 0.1),
        )
        self.assertEqual(result["outcome"], "comment_created")
        self.assertTrue(result["polling_used"])
        self.assertEqual(gh.run_reads, 2)
        self.assertEqual(sleeps, [0.1])
        self.assertEqual(len(gh.created), 1)

    def test_exhausted_poll_makes_no_comment(self):
        gh = FakeGitHub([run(status="in_progress", conclusion=None)])
        result = process_event(
            payload(),
            gh,
            repository=KUUOS,
            sleep_fn=lambda _: None,
            delays=(0.0, 0.0, 0.0),
        )
        self.assertEqual(result["outcome"], "nonterminal_exhausted")
        self.assertEqual(gh.run_reads, 3)
        self.assertEqual(gh.created, [])

    def test_fresh_run_identity_mismatch_makes_no_comment(self):
        gh = FakeGitHub([run(head_sha="b" * 40)])
        result = process_event(
            payload(), gh, repository=KUUOS, sleep_fn=lambda _: None, delays=(0.0,)
        )
        self.assertEqual(result["outcome"], "identity_mismatch")
        self.assertEqual(gh.created, [])

    def test_current_pr_head_mismatch_makes_no_comment(self):
        gh = FakeGitHub(
            [run()],
            pr={
                "number": 77,
                "head": {"sha": "b" * 40, "repo": {"full_name": KUUOS}},
            },
        )
        result = process_event(
            payload(), gh, repository=KUUOS, sleep_fn=lambda _: None, delays=(0.0,)
        )
        self.assertEqual(result["outcome"], "stale_pr_head")
        self.assertEqual(gh.created, [])

    def test_own_marker_deduplicates(self):
        ident = validate_dispatch_payload(payload(), KUUOS)
        gh = FakeGitHub([run()], comments=[{"body": producer_marker(ident)}])
        result = process_event(
            payload(), gh, repository=KUUOS, sleep_fn=lambda _: None, delays=(0.0,)
        )
        self.assertEqual(result["outcome"], "deduplicated")
        self.assertEqual(gh.created, [])

    def test_primary_producer_marker_does_not_suppress_secondary(self):
        primary = (
            "<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 "
            "run_id=123 attempt=1 pr=77 -->"
        )
        gh = FakeGitHub([run()], comments=[{"body": primary}])
        result = process_event(
            payload(), gh, repository=KUUOS, sleep_fn=lambda _: None, delays=(0.0,)
        )
        self.assertEqual(result["outcome"], "comment_created")
        self.assertEqual(len(gh.created), 1)

    def test_mgap_run_contract(self):
        event = payload(MGAP, "PR Lean Fast Check")
        mgap_run = run(
            name="PR Lean Fast Check",
            html_url="https://github.com/itakura-hidetoshi/4d-mass-gap/actions/runs/123",
        )
        gh = FakeGitHub(
            [mgap_run],
            pr={"number": 77, "head": {"sha": SHA, "repo": {"full_name": MGAP}}},
        )
        result = process_event(
            event, gh, repository=MGAP, sleep_fn=lambda _: None, delays=(0.0,)
        )
        self.assertEqual(result["outcome"], "comment_created")


if __name__ == "__main__":
    unittest.main()
