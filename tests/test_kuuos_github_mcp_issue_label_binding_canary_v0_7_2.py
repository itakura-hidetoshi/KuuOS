from __future__ import annotations

import unittest

from runtime import kuuos_github_mcp_issue_label_binding_canary_v0_7 as base
from runtime.kuuos_github_mcp_issue_label_binding_canary_v0_7_2 import (
    GITHUB_LABEL_NAME_MAX_LENGTH,
    LABEL_PREFIX,
    _validate_plan,
)

BASE_SHA = "0c4c93dd96b310b7f16f95a16eb5ab1c36609263"
IMAGE = "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"


def _plan(*, nonce: str, prefix: str = LABEL_PREFIX) -> dict[str, object]:
    return {
        "version": "kuuos_github_mcp_issue_label_binding_canary_plan_v0_7",
        "mode": "mock",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "base_branch": "main",
        "base_sha": BASE_SHA,
        "write_capable": True,
        "read_only": False,
        "lockdown_mode": True,
        "execute_external_actions": True,
        "confirmation": "RUN_KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY",
        "transaction_nonce": nonce,
        "request_issue_number": 1702,
        "request_issue_title": "[KuuOS MCP Issue Label Binding Canary v0.7]",
        "request_version_marker": "kuuos_github_mcp_issue_label_binding_canary_request_v0_7",
        "label_prefix": prefix,
        "label_color": "0e8a16",
        "label_description_marker": "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY v0.7",
        "server": {
            "kind": "official_github_mcp_server",
            "launcher": "docker",
            "image": IMAGE,
            "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
            "toolsets": ["issues", "labels"],
            "tools": ["issue_write", "issue_read", "label_write", "get_label"],
        },
    }


class LabelNameBoundTests(unittest.TestCase):
    def test_maximum_allowed_nonce_stays_below_github_limit(self) -> None:
        nonce = "a" * 32
        blockers: list[str] = []
        _validate_plan(_plan(nonce=nonce), blockers)
        self.assertEqual(blockers, [])
        self.assertEqual(len(LABEL_PREFIX + nonce), 47)
        self.assertLessEqual(len(LABEL_PREFIX + nonce), GITHUB_LABEL_NAME_MAX_LENGTH)

    def test_live_nonce_name_stays_below_github_limit(self) -> None:
        nonce = "binding-v07-887dc1eaafb2ec40"
        self.assertLessEqual(len(LABEL_PREFIX + nonce), GITHUB_LABEL_NAME_MAX_LENGTH)

    def test_legacy_unbounded_prefix_is_rejected(self) -> None:
        blockers: list[str] = []
        _validate_plan(
            _plan(nonce="binding-v07-test-002", prefix="kuuos-mcp-binding-canary-"),
            blockers,
        )
        self.assertIn("label_prefix_not_v0_7_2_bounded", blockers)

    def test_base_runtime_uses_bounded_validator(self) -> None:
        self.assertIs(base._validate_plan, _validate_plan)


if __name__ == "__main__":
    unittest.main()
