import unittest

from scripts.chatgpt_ci_completion_commit_wakeup_v0_1 import (
    build_receipt,
    receipt_path,
    should_skip_source,
)


class CommitWakeupTests(unittest.TestCase):
    def test_receipt_path_binds_exact_identity(self):
        self.assertEqual(
            receipt_path(
                pull_request=1662,
                run_id=35299820821,
                run_attempt=1,
                head_sha="f40105cb6ded280cb854222580642e9047c5b1b5",
            ),
            "ci-events/1662-35299820821-1-f40105cb6ded.json",
        )

    def test_receipt_is_non_authoritative_and_exact(self):
        packet = build_receipt(
            repository="itakura-hidetoshi/KuuOS",
            pull_request=1662,
            workflow="KuuOS PR Governance Gate",
            run_id=35299820821,
            run_attempt=1,
            status="completed",
            conclusion="success",
            head_sha="f40105cb6ded280cb854222580642e9047c5b1b5",
            head_branch="feature/x",
            run_url="https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35299820821",
            updated_at="2026-09-18T02:34:14Z",
        )
        self.assertEqual(packet["version"], "chatgpt_ci_commit_wakeup_v0_1")
        self.assertEqual(packet["run_id"], 35299820821)
        self.assertEqual(packet["run_attempt"], 1)
        self.assertEqual(
            packet["head_sha"], "f40105cb6ded280cb854222580642e9047c5b1b5"
        )
        self.assertTrue(packet["event_is_wakeup_signal_only"])
        self.assertTrue(packet["fresh_mcp_reobservation_required"])
        self.assertFalse(packet["merge_authority_granted"])
        self.assertFalse(packet["write_authority_granted"])

    def test_inbox_branch_never_reemits_itself(self):
        self.assertTrue(
            should_skip_source(
                pull_request=1663,
                head_branch="infra/chatgpt-ci-inbox-events-v0-1",
                inbox_pull_request=1663,
                inbox_branch="infra/chatgpt-ci-inbox-events-v0-1",
            )
        )
        self.assertTrue(
            should_skip_source(
                pull_request=1664,
                head_branch="infra/chatgpt-ci-inbox-events-v0-1",
                inbox_pull_request=1663,
                inbox_branch="infra/chatgpt-ci-inbox-events-v0-1",
            )
        )
        self.assertFalse(
            should_skip_source(
                pull_request=1662,
                head_branch="feature/x",
                inbox_pull_request=1663,
                inbox_branch="infra/chatgpt-ci-inbox-events-v0-1",
            )
        )


if __name__ == "__main__":
    unittest.main()
