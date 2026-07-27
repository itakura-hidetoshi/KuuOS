from __future__ import annotations

import json
import unittest

from runtime import kuuos_github_mcp_issue_label_binding_canary_v0_7 as base
from runtime.kuuos_github_mcp_issue_label_binding_canary_v0_7_1 import (
    _decode_observed_issue_body_once,
    _issue_identity_blockers,
)

ISSUE_NUMBER = 1359
TITLE = "[KuuOS MCP Issue Label Binding Canary v0.7]"
VERSION = "kuuos_github_mcp_issue_label_binding_canary_request_v0_7"
CONFIRMATION = "RUN_KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY"
BASE_SHA = "dacf2c8a2fd3c247ffa289db51719e9e0d8406c5"
NONCE = "binding-v07-1c51f1af035a826d"
IMAGE = "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"


def _body() -> str:
    return json.dumps(
        {
            "version": VERSION,
            "confirmation": CONFIRMATION,
            "expected_main_sha": BASE_SHA,
            "transaction_nonce": NONCE,
            "server_image": IMAGE,
        },
        indent=2,
    )


def _observed(body: str) -> dict[str, object]:
    return {
        "number": ISSUE_NUMBER,
        "title": TITLE,
        "body": body,
        "state": "open",
    }


def _blockers(body: str) -> list[str]:
    return _issue_identity_blockers(
        observed=_observed(body),
        issue_number=ISSUE_NUMBER,
        expected_title=TITLE,
        expected_version=VERSION,
        expected_confirmation=CONFIRMATION,
        expected_base_sha=BASE_SHA,
        expected_nonce=NONCE,
    )


class IssueBodyCompatibilityTests(unittest.TestCase):
    def test_official_numeric_quote_entities_are_decoded(self) -> None:
        escaped = _body().replace('"', "&#34;")
        self.assertEqual(_blockers(escaped), [])

    def test_raw_json_remains_compatible(self) -> None:
        self.assertEqual(_blockers(_body()), [])

    def test_decode_occurs_exactly_once(self) -> None:
        original = '{"value":"literal &#34; marker"}'
        encoded_by_server = original.replace("&", "&amp;").replace('"', "&#34;")
        self.assertEqual(_decode_observed_issue_body_once(encoded_by_server), original)

    def test_malformed_body_remains_fail_closed(self) -> None:
        blockers = _blockers("{not-json")
        self.assertIn("observed_issue_body_not_strict_json", blockers)

    def test_base_runtime_uses_compatibility_validator(self) -> None:
        self.assertIs(base._issue_identity_blockers, _issue_identity_blockers)


if __name__ == "__main__":
    unittest.main()
