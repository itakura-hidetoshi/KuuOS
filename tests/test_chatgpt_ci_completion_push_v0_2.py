import pathlib
import unittest

from scripts.chatgpt_ci_completion_push_v0_2 import resolve_pr_numbers

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/chatgpt-ci-completion-push-v0-1.yml"


class ResolvePrNumbersTests(unittest.TestCase):
    def test_uses_workflow_run_pull_requests_when_present(self):
        event_pull_requests = [{"number": 1651}]
        associated_pull_requests = []

        self.assertEqual(
            resolve_pr_numbers(
                event_pull_requests,
                associated_pull_requests,
                head_sha="abc123",
                repository="itakura-hidetoshi/KuuOS",
            ),
            [1651],
        )

    def test_falls_back_to_exact_commit_association_when_event_array_is_empty(self):
        associated_pull_requests = [
            {
                "number": 1651,
                "head": {
                    "sha": "abc123",
                    "repo": {"full_name": "itakura-hidetoshi/KuuOS"},
                },
            }
        ]

        self.assertEqual(
            resolve_pr_numbers(
                [],
                associated_pull_requests,
                head_sha="abc123",
                repository="itakura-hidetoshi/KuuOS",
            ),
            [1651],
        )

    def test_fallback_rejects_wrong_head_or_repository_and_deduplicates(self):
        associated_pull_requests = [
            {
                "number": 1651,
                "head": {
                    "sha": "abc123",
                    "repo": {"full_name": "itakura-hidetoshi/KuuOS"},
                },
            },
            {
                "number": 1651,
                "head": {
                    "sha": "abc123",
                    "repo": {"full_name": "itakura-hidetoshi/KuuOS"},
                },
            },
            {
                "number": 1652,
                "head": {
                    "sha": "wrong",
                    "repo": {"full_name": "itakura-hidetoshi/KuuOS"},
                },
            },
            {
                "number": 1653,
                "head": {
                    "sha": "abc123",
                    "repo": {"full_name": "other/repo"},
                },
            },
        ]

        self.assertEqual(
            resolve_pr_numbers(
                [],
                associated_pull_requests,
                head_sha="abc123",
                repository="itakura-hidetoshi/KuuOS",
            ),
            [1651],
        )

    def test_workflow_can_write_pull_request_comments(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("issues: write", text)
        self.assertIn("pull-requests: write", text)


if __name__ == "__main__":
    unittest.main()
