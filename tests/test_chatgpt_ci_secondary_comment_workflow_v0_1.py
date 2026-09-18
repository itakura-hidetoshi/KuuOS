import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".github/workflows/pr-governance-gate.yml"
REENTRY = ROOT / ".github/workflows/kuuos-github-ci-completion-reentry-v1-1.yml"


class SecondaryCommentWorkflowTests(unittest.TestCase):
    def test_source_gate_emits_nonfatal_exact_dispatch(self):
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn("chatgpt-completion-dispatch:", text)
        self.assertIn("needs: governance-gate", text)
        self.assertIn("contents: write", text)
        self.assertIn('"event_type": "kuuos_ci_completion_v1_1"', text)
        self.assertIn('"repository": os.environ["REPOSITORY"]', text)
        self.assertIn('"pull_request": int(os.environ["PR_NUMBER"])', text)
        self.assertIn('"run_id": int(os.environ["SOURCE_RUN_ID"])', text)
        self.assertIn('"run_attempt": int(os.environ["SOURCE_RUN_ATTEMPT"])', text)
        self.assertIn('"head_sha": os.environ["SOURCE_HEAD_SHA"]', text)
        self.assertIn('"workflow": os.environ["SOURCE_WORKFLOW"]', text)
        finalizer = text.split("chatgpt-completion-dispatch:", 1)[1]
        self.assertNotIn("exit 1", finalizer)

    def test_existing_reentry_emits_secondary_comment_for_same_repo_dispatch(self):
        text = REENTRY.read_text(encoding="utf-8")
        self.assertIn("repository_dispatch:", text)
        self.assertIn("types: [kuuos_ci_completion_v1_1]", text)
        self.assertIn("actions: read", text)
        self.assertIn("issues: write", text)
        self.assertIn("pull-requests: write", text)
        self.assertIn(
            "python3 scripts/chatgpt_ci_secondary_comment_v0_1.py",
            text,
        )
        self.assertIn("python3 -m unittest -v", text)
        self.assertIn("tests.test_chatgpt_ci_secondary_comment_v0_1", text)
        self.assertIn("tests.test_chatgpt_ci_secondary_comment_workflow_v0_1", text)


if __name__ == "__main__":
    unittest.main()
