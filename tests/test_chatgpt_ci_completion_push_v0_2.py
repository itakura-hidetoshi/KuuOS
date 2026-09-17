import unittest

from scripts.chatgpt_ci_completion_push_v0_2 import resolve_pr_numbers


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


if __name__ == "__main__":
    unittest.main()
