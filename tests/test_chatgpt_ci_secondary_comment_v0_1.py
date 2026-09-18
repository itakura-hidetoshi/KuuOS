import json
import unittest

from scripts.chatgpt_ci_secondary_comment_v0_1 import (
    build_comment,
    process_event,
    producer_marker,
    validate_dispatch_payload,
)

REPO = "itakura-hidetoshi/KuuOS"
SHA = "a" * 40


def event(**overrides):
    payload = {
        "repository": REPO,
        "pull_request": 1662,
        "run_id": 123,
        "run_attempt": 1,
        "head_sha": SHA,
        "head_branch": "feature/x",
        "workflow": "KuuOS PR Governance Gate",
        "workflow_name": "KuuOS PR Governance Gate",
        "status": "completed",
        "conclusion": "success",
        "run_event": "pull_request",
    }
    payload.update(overrides)
    return {"action": "kuuos_ci_completion_v1_1", "client_payload": payload}


def run(status="completed", conclusion="success", **overrides):
    value = {
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
    value.update(overrides)
    return value


class FakeGitHub:
    def __init__(self, runs, comments=None, pr=None):
        self.runs = list(runs)
        self.comments = list(comments or [])
        self.pr = pr or {
            "number": 1662,
            "head": {"sha": SHA, "repo": {"full_name": REPO}},
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


class SecondaryCommentTests(unittest.TestCase):
    def test_validates_exact_dispatch_identity(self):
        ident = validate_dispatch_payload(event(), REPO)
        self.assertIsNotNone(ident)
        self.assertEqual(ident.pull_request, 1662)
        self.assertEqual(ident.workflow, "KuuOS PR Governance Gate")

    def test_rejects_wrong_event_or_repository(self):
        wrong = event()
        wrong["action"] = "other"
        self.assertIsNone(validate_dispatch_payload(wrong, REPO))
        self.assertIsNone(
            validate_dispatch_payload(
                event(repository="itakura-hidetoshi/4d-mass-gap"), REPO
            )
        )

    def test_secondary_marker_is_distinct_from_primary(self):
        ident = validate_dispatch_payload(event(), REPO)
        marker = producer_marker(ident)
        self.assertIn("CHATGPT_CI_COMPLETION_PUSH_V0_1", marker)
        self.assertIn("producer=repository_dispatch_v0_1", marker)
        primary = (
            "<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 "
            "run_id=123 attempt=1 pr=1662 -->"
        )
        self.assertNotEqual(marker, primary)

    def test_primary_comment_does_not_suppress_secondary(self):
        primary = (
            "<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 "
            "run_id=123 attempt=1 pr=1662 -->"
        )
        gh = FakeGitHub([run()], comments=[{"body": primary}])
        result = process_event(
            event(),
            gh,
            repository=REPO,
            sleep_fn=lambda _: None,
            delays=(0.0,),
        )
        self.assertEqual(result["outcome"], "comment_created")
        self.assertEqual(len(gh.created), 1)

    def test_secondary_replay_deduplicates(self):
        ident = validate_dispatch_payload(event(), REPO)
        gh = FakeGitHub([run()], comments=[{"body": producer_marker(ident)}])
        result = process_event(
            event(),
            gh,
            repository=REPO,
            sleep_fn=lambda _: None,
            delays=(0.0,),
        )
        self.assertEqual(result["outcome"], "deduplicated")
        self.assertEqual(gh.created, [])

    def test_bounded_polling_same_exact_run_then_comments(self):
        gh = FakeGitHub(
            [run(status="in_progress", conclusion=None), run()]
        )
        sleeps = []
        result = process_event(
            event(),
            gh,
            repository=REPO,
            sleep_fn=sleeps.append,
            delays=(0.0, 0.1),
        )
        self.assertEqual(result["outcome"], "comment_created")
        self.assertTrue(result["polling_used"])
        self.assertEqual(gh.run_reads, 2)
        self.assertEqual(sleeps, [0.1])

    def test_stale_current_pr_head_is_rejected(self):
        gh = FakeGitHub(
            [run()],
            pr={
                "number": 1662,
                "head": {
                    "sha": "b" * 40,
                    "repo": {"full_name": REPO},
                },
            },
        )
        result = process_event(
            event(),
            gh,
            repository=REPO,
            sleep_fn=lambda _: None,
            delays=(0.0,),
        )
        self.assertEqual(result["outcome"], "stale_pr_head")
        self.assertEqual(gh.created, [])

    def test_comment_packet_is_wakeup_only(self):
        ident = validate_dispatch_payload(event(), REPO)
        body = build_comment(ident, run(), polling_used=False)
        packet = json.loads(body.split("```json\n", 1)[1].split("\n```", 1)[0])
        self.assertEqual(packet["producer"], "repository_dispatch_v0_1")
        self.assertTrue(packet["event_is_wakeup_signal_only"])
        self.assertTrue(packet["fresh_mcp_reobservation_required"])


if __name__ == "__main__":
    unittest.main()
