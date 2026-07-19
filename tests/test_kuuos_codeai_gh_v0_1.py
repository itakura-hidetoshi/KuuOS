from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "kuuos_codeai_gh_v0_1.sh"


class GitHubCliWrapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        temp = Path(self.tempdir.name)
        self.log = temp / "gh-args.jsonl"
        self.fake_gh = temp / "fake-gh"
        self.fake_gh.write_text(
            """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ[\"KUUOS_GH_TEST_LOG\"]).open(\"a\", encoding=\"utf-8\").write(
    json.dumps(sys.argv[1:]) + \"\\n\"
)
if sys.argv[1:] == [\"--version\"]:
    print(\"gh version test\")
elif sys.argv[1:3] == [\"auth\", \"status\"]:
    print(\"authenticated\", file=sys.stderr)
else:
    print(json.dumps({\"ok\": True, \"args\": sys.argv[1:]}))
""",
            encoding="utf-8",
        )
        self.fake_gh.chmod(0o755)
        self.env = {
            **os.environ,
            "GH_TOKEN": "never-log-this-token",
            "GH_REPO": "itakura-hidetoshi/KuuOS",
            "KUUOS_GH_BIN": str(self.fake_gh),
            "KUUOS_GH_TEST_LOG": str(self.log),
        }

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_wrapper(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(WRAPPER), *args],
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    def logged_calls(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_probe_binds_repository_and_never_passes_token(self) -> None:
        result = self.run_wrapper("probe")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = self.logged_calls()
        self.assertEqual(calls[0], ["--version"])
        self.assertEqual(calls[1], ["auth", "status", "--active", "--hostname", "github.com"])
        self.assertEqual(
            calls[2],
            [
                "repo",
                "view",
                "itakura-hidetoshi/KuuOS",
                "--json",
                "nameWithOwner,defaultBranchRef,isPrivate,url",
            ],
        )
        self.assertNotIn("never-log-this-token", json.dumps(calls))

    def test_pr_checks_is_exact_and_read_only(self) -> None:
        result = self.run_wrapper("pr-checks", "1299")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.logged_calls(),
            [[
                "pr",
                "checks",
                "1299",
                "--repo",
                "itakura-hidetoshi/KuuOS",
                "--json",
                "name,state,bucket,link",
            ]],
        )

    def test_invalid_identifier_fails_before_invocation(self) -> None:
        result = self.run_wrapper("pr-view", "1;echo-bad")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.logged_calls(), [])

    def test_unsupported_operation_fails_closed(self) -> None:
        result = self.run_wrapper("pr-merge", "1299")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported read-only operation", result.stderr)
        self.assertEqual(self.logged_calls(), [])

    def test_missing_token_fails_closed(self) -> None:
        self.env.pop("GH_TOKEN")
        result = self.run_wrapper("repo-view")
        self.assertEqual(result.returncode, 2)
        self.assertIn("GH_TOKEN is required", result.stderr)
        self.assertEqual(self.logged_calls(), [])

    def test_repository_must_be_owner_name(self) -> None:
        self.env["GH_REPO"] = "https://github.com/itakura-hidetoshi/KuuOS"
        result = self.run_wrapper("repo-view")
        self.assertEqual(result.returncode, 2)
        self.assertIn("owner/repository", result.stderr)
        self.assertEqual(self.logged_calls(), [])


if __name__ == "__main__":
    unittest.main()
