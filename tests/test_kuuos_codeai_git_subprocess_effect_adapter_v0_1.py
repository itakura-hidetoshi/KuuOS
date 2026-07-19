from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from runtime.kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    GitEffectInvocation,
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_PUSH,
)
from runtime.kuuos_codeai_git_subprocess_effect_adapter_v0_1 import (
    CommandOutcome,
    build_subprocess_git_effect_adapter,
)

SHA_A = "a" * 40
SHA_B = "b" * 40


def invocation(phase: str, **overrides) -> GitEffectInvocation:
    values = dict(
        effect_phase=phase,
        repository_full_name="itakura-hidetoshi/KuuOS",
        source_commit_sha=SHA_A,
        base_branch="main",
        head_branch="codeai/effect-test",
        remote_name="origin",
        merge_method="merge",
        change_set_digest="1" * 64,
        commit_message="autonomous effect" if phase == PHASE_LOCAL_COMMIT else "",
        pull_request_title="Autonomous effect PR" if phase == PHASE_CREATE_PR else "",
        pull_request_body="Bounded effect." if phase == PHASE_CREATE_PR else "",
        pull_request_draft=phase == PHASE_CREATE_PR,
        pull_request_number=1303 if phase in {PHASE_MARK_PR_READY, PHASE_MERGE} else 0,
        expected_head_sha=SHA_A if phase == PHASE_LOCAL_COMMIT else SHA_B,
        maximum_command_count=6,
        maximum_output_bytes=32768,
        maximum_timeout_seconds=60,
        opaque_token_use_allowed=True,
        secret_material_read_allowed=False,
    )
    values.update(overrides)
    return GitEffectInvocation(**values)


class FakeRunner:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def __call__(self, command, cwd, environment, stdin, timeout_seconds):
        self.calls.append((list(command), cwd, stdin, timeout_seconds))
        if not self.outcomes:
            raise AssertionError("unexpected command")
        return self.outcomes.pop(0)


class SubprocessEffectAdapterTests(unittest.TestCase):
    def test_create_pr_uses_exact_draft_command_and_observes_result(self):
        runner = FakeRunner([
            CommandOutcome(0, "https://github.com/itakura-hidetoshi/KuuOS/pull/1303\n", ""),
            CommandOutcome(0, json.dumps({"number": 1303, "url": "https://github.com/itakura-hidetoshi/KuuOS/pull/1303", "isDraft": True, "headRefOid": SHA_B, "baseRefName": "main"}), ""),
        ])
        adapter = build_subprocess_git_effect_adapter(workdir=".", runner=runner, completed_epoch=100)
        result = adapter(invocation(PHASE_CREATE_PR))
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["pull_request_created"])
        self.assertTrue(result["pull_request_draft"])
        self.assertTrue(result["opaque_token_used"])
        create = runner.calls[0]
        self.assertEqual(create[0][:4], ["gh", "pr", "create", "--repo"])
        self.assertIn("--draft", create[0])
        self.assertEqual(create[2], "Bounded effect.")
        self.assertNotIn("GH_TOKEN", " ".join(create[0]))

    def test_mark_ready_uses_pr_number_and_reobserves_head(self):
        runner = FakeRunner([
            CommandOutcome(0, "ready\n", ""),
            CommandOutcome(0, json.dumps({"number": 1303, "isDraft": False, "headRefOid": SHA_B, "baseRefName": "main"}), ""),
        ])
        adapter = build_subprocess_git_effect_adapter(workdir=".", runner=runner)
        result = adapter(invocation(PHASE_MARK_PR_READY))
        self.assertTrue(result["pull_request_marked_ready"])
        self.assertEqual(runner.calls[0][0], ["gh", "pr", "ready", "1303", "--repo", "itakura-hidetoshi/KuuOS"])

    def test_merge_pins_head_and_never_uses_admin_or_delete(self):
        runner = FakeRunner([
            CommandOutcome(0, "", ""),
            CommandOutcome(0, json.dumps({"number": 1303, "headRefOid": SHA_B, "mergedAt": "2026-07-19T00:00:00Z", "mergeCommit": {"oid": "c" * 40}}), ""),
        ])
        adapter = build_subprocess_git_effect_adapter(workdir=".", runner=runner)
        result = adapter(invocation(PHASE_MERGE))
        self.assertTrue(result["merge_performed"])
        command = runner.calls[0][0]
        self.assertIn("--match-head-commit", command)
        self.assertIn(SHA_B, command)
        self.assertNotIn("--admin", command)
        self.assertNotIn("--delete-branch", command)

    def test_local_commit_executes_against_disposable_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", "-b", "codeai/effect-test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "KuuOS Test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
            (root / "README.md").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=root, check=True)
            source = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            (root / "README.md").write_text("base\nnext\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            adapter = build_subprocess_git_effect_adapter(workdir=root, completed_epoch=100)
            result = adapter(invocation(PHASE_LOCAL_COMMIT, source_commit_sha=source, expected_head_sha=source))
            self.assertEqual(result["status"], "completed", result["stderr"])
            self.assertTrue(result["local_commit_created"])
            self.assertEqual(result["local_commit_parent_sha"], source)
            self.assertNotEqual(result["local_commit_sha"], source)

    def test_push_is_non_force_to_exact_branch(self):
        runner = FakeRunner([CommandOutcome(0, SHA_B + "\n", ""), CommandOutcome(0, "To origin\n", "")])
        adapter = build_subprocess_git_effect_adapter(workdir=".", runner=runner)
        result = adapter(invocation(PHASE_PUSH))
        self.assertTrue(result["branch_pushed"])
        command = runner.calls[1][0]
        self.assertEqual(command, ["git", "push", "--porcelain", "origin", "HEAD:refs/heads/codeai/effect-test"])
        self.assertFalse(any(item in {"--force", "-f"} for item in command))

    def test_command_budget_failure_is_bounded(self):
        runner = FakeRunner([CommandOutcome(0, SHA_B + "\n", "")])
        adapter = build_subprocess_git_effect_adapter(workdir=".", runner=runner)
        result = adapter(invocation(PHASE_PUSH, maximum_command_count=1))
        self.assertEqual(result["status"], "failed")
        self.assertIn("command budget exhausted", result["stderr"])
        self.assertEqual(result["command_count"], 1)


if __name__ == "__main__":
    unittest.main()
