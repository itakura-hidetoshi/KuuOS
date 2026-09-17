import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECEIVER = ROOT / ".github/workflows/chatgpt-ci-completion-dispatch-v0-1.yml"
PRIMARY = ROOT / ".github/workflows/chatgpt-ci-completion-push-v0-1.yml"
VALIDATION = ROOT / ".github/workflows/chatgpt-ci-completion-dispatch-validation-v0-1.yml"
KUUOS_GATE = ROOT / ".github/workflows/pr-governance-gate.yml"


class WorkflowWiringTests(unittest.TestCase):
    def test_receiver_uses_repository_dispatch_and_trusted_main(self):
        text = RECEIVER.read_text(encoding="utf-8")
        self.assertIn("repository_dispatch:", text)
        self.assertIn("types: [chatgpt_ci_completion_dispatch_v0_1]", text)
        self.assertIn("actions: read", text)
        self.assertIn("contents: read", text)
        self.assertIn("issues: write", text)
        self.assertIn("pull-requests: write", text)
        self.assertIn("ref: main", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn(
            "python3 -m unittest -v tests.test_chatgpt_ci_completion_dispatch_v0_1",
            text,
        )
        self.assertIn("scripts/chatgpt_ci_completion_dispatch_v0_1.py", text)

    def test_primary_wakeup_can_write_pr_comment(self):
        text = PRIMARY.read_text(encoding="utf-8")
        self.assertIn("issues: write", text)
        self.assertIn("pull-requests: write", text)

    def test_validation_watches_primary_wakeup_workflow(self):
        text = VALIDATION.read_text(encoding="utf-8")
        self.assertIn(
            '- ".github/workflows/chatgpt-ci-completion-push-v0-1.yml"',
            text,
        )

    def test_kuuos_source_gate_dispatches_exact_identity_nonfatally(self):
        text = KUUOS_GATE.read_text(encoding="utf-8")
        self.assertIn("chatgpt-completion-dispatch:", text)
        self.assertIn("needs: governance-gate", text)
        self.assertIn("github.event_name == 'pull_request'", text)
        self.assertIn("contents: write", text)
        self.assertIn("chatgpt_ci_completion_dispatch_v0_1", text)
        self.assertIn("${{ github.event.pull_request.number }}", text)
        self.assertIn("${{ github.run_id }}", text)
        self.assertIn("${{ github.run_attempt }}", text)
        self.assertIn("${{ github.event.pull_request.head.sha }}", text)
        self.assertIn("${{ github.event.pull_request.head.ref }}", text)
        self.assertIn("KuuOS PR Governance Gate", text)
        self.assertIn('if [ "${http_code}" != "204" ]; then', text)
        finalizer = text.split("chatgpt-completion-dispatch:", 1)[1]
        self.assertNotIn("exit 1", finalizer)


if __name__ == "__main__":
    unittest.main()
