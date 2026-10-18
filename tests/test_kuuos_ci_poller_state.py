from __future__ import annotations

import base64
import hashlib
import http.client
import io
import json
import traceback
import unittest
import urllib.error
from unittest.mock import patch

from runtime.kuuos_ci_poller_state import GitHubStateStore


REPO = "itakura-hidetoshi/KuuOS"
BRANCH = "state/kuuos-mgap-ci-poller-v1-2"
PATH = "kuuos_mgap_ci_completion_poller_v1_2.json"
TOKEN = "unit-test-token-never-send"
STATE = {"version": "test", "last_processed_run_id": 100}


def state_bytes(state):
    return (json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def contents(state=STATE, **overrides):
    raw = state_bytes(state)
    payload = {
        "type": "file", "path": PATH, "encoding": "base64",
        "sha": blob_sha(raw), "size": len(raw),
        "content": base64.encodebytes(raw).decode(),
    }
    payload.update(overrides)
    return payload


def saved(state):
    return {"content": {"type": "file", "path": PATH, "sha": blob_sha(state_bytes(state))}}


class Response:
    def __init__(self, payload=None, *, raw=None, status=200):
        self.status = status
        self.stream = io.BytesIO(raw if raw is not None else json.dumps(payload).encode())

    def read(self, amount=-1):
        return self.stream.read(amount)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakeHTTP:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append(request)
        if not self.responses:
            raise AssertionError("Unexpected HTTP request")
        result = self.responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


class GitHubStateStoreTests(unittest.TestCase):
    def use_http(self, *responses):
        fake = FakeHTTP(*responses)
        mock = patch("runtime.kuuos_ci_poller_state.urllib.request.build_opener", return_value=fake)
        self.addCleanup(mock.stop)
        mock.start()
        return fake

    def test_load_reads_only_named_branch_and_returns_checkpoint(self):
        http = self.use_http(Response(contents()))
        self.assertEqual(GitHubStateStore(REPO, TOKEN).load(), STATE)
        req = http.requests[0]
        self.assertEqual(req.method, "GET")
        self.assertEqual(req.full_url, f"https://api.github.com/repos/{REPO}/contents/{PATH}?ref=state%2Fkuuos-mgap-ci-poller-v1-2")
        self.assertEqual(req.get_header("Authorization"), f"Bearer {TOKEN}")

    def test_save_uses_loaded_sha_and_advances_cas_after_each_success(self):
        next_state = {**STATE, "last_processed_run_id": 101}
        final_state = {**STATE, "last_processed_run_id": 102}
        http = self.use_http(Response(contents()), Response(saved(next_state)), Response(saved(final_state)))
        store = GitHubStateStore(REPO, TOKEN)
        store.load()
        store.save(next_state)
        store.save(final_state)
        first = json.loads(http.requests[1].data)
        second = json.loads(http.requests[2].data)
        self.assertEqual(http.requests[1].method, "PUT")
        self.assertEqual(http.requests[1].full_url, f"https://api.github.com/repos/{REPO}/contents/{PATH}")
        self.assertEqual(first["branch"], BRANCH)
        self.assertEqual(first["sha"], contents()["sha"])
        self.assertEqual(second["sha"], saved(next_state)["content"]["sha"])
        self.assertEqual(json.loads(base64.b64decode(first["content"])), next_state)

    def test_save_before_load_never_creates_state(self):
        http = self.use_http()
        with self.assertRaisesRegex(RuntimeError, "state_store_not_loaded"):
            GitHubStateStore(REPO, TOKEN).save(STATE)
        self.assertEqual(http.requests, [])

    def test_missing_state_fails_closed_without_initialization(self):
        error = urllib.error.HTTPError("https://api.github.com", 404, "secret body", {}, io.BytesIO(b"secret body"))
        http = self.use_http(error)
        store = GitHubStateStore(REPO, TOKEN)
        with self.assertRaisesRegex(RuntimeError, "state_store_missing"):
            store.load()
        with self.assertRaisesRegex(RuntimeError, "state_store_not_loaded"):
            store.save(STATE)
        self.assertEqual(len(http.requests), 1)

    def test_corrupt_contents_fail_closed(self):
        cases = [
            [], contents(type="dir"), contents(path="other.json"),
            contents(encoding="none"), contents(sha="invalid"),
            contents(content="%%%"), contents(content=base64.b64encode(b"not json").decode()),
            contents(state=[]), contents(state=None),
            contents(sha="0" * 40), contents(size=0),
        ]
        for payload in cases:
            with self.subTest(payload=payload):
                http = self.use_http(Response(payload))
                store = GitHubStateStore(REPO, TOKEN)
                with self.assertRaisesRegex(RuntimeError, "state_store_invalid"):
                    store.load()
                with self.assertRaisesRegex(RuntimeError, "state_store_not_loaded"):
                    store.save(STATE)
                self.assertEqual(len(http.requests), 1)

    def test_non_json_response_has_sanitized_error(self):
        self.use_http(Response(raw=("secret " + TOKEN).encode()))
        with self.assertRaisesRegex(RuntimeError, "state_store_invalid_response") as caught:
            GitHubStateStore(REPO, TOKEN).load()
        self.assertNotIn(TOKEN, str(caught.exception))

    def test_stale_cas_conflict_does_not_retry_or_reinitialize(self):
        error = urllib.error.HTTPError("https://api.github.com", 409, TOKEN, {}, io.BytesIO(TOKEN.encode()))
        http = self.use_http(Response(contents()), error)
        store = GitHubStateStore(REPO, TOKEN)
        store.load()
        with self.assertRaisesRegex(RuntimeError, "state_store_conflict") as caught:
            store.save({**STATE, "last_processed_run_id": 101})
        self.assertNotIn(TOKEN, str(caught.exception))
        with self.assertRaisesRegex(RuntimeError, "state_store_not_loaded"):
            store.save(STATE)
        self.assertEqual(len(http.requests), 2)

    def test_http_and_transport_errors_do_not_leak_body_token_or_traceback(self):
        errors = [
            urllib.error.HTTPError("https://example.invalid/" + TOKEN, 403, TOKEN, {}, io.BytesIO(TOKEN.encode())),
            urllib.error.URLError(TOKEN), TimeoutError(TOKEN), OSError(TOKEN),
            http.client.IncompleteRead(TOKEN.encode()),
        ]
        for error in errors:
            with self.subTest(error_type=type(error).__name__):
                self.use_http(error)
                try:
                    GitHubStateStore(REPO, TOKEN).load()
                except RuntimeError:
                    self.assertNotIn(TOKEN, traceback.format_exc())
                else:
                    self.fail("Expected sanitized failure")

    def test_failed_reload_invalidates_previous_loaded_sha(self):
        self.use_http(Response(contents()), Response(raw=b"broken"))
        store = GitHubStateStore(REPO, TOKEN)
        store.load()
        with self.assertRaises(RuntimeError):
            store.load()
        with self.assertRaisesRegex(RuntimeError, "state_store_not_loaded"):
            store.save(STATE)

    def test_ambiguous_save_response_requires_fresh_load(self):
        for response in [Response({}), Response(saved(STATE), status=201), Response(saved({"wrong": True}))]:
            with self.subTest(response=response):
                http = self.use_http(Response(contents()), response)
                store = GitHubStateStore(REPO, TOKEN)
                store.load()
                with self.assertRaisesRegex(RuntimeError, "state_store_invalid|state_store_unexpected"):
                    store.save({**STATE, "last_processed_run_id": 101})
                with self.assertRaisesRegex(RuntimeError, "state_store_not_loaded"):
                    store.save(STATE)
                self.assertEqual(len(http.requests), 2)

    def test_non_json_and_oversize_state_rejected_before_network(self):
        for state in [[], {"value": object()}, {"value": float("nan")}, {"data": "x" * 1048576}]:
            with self.subTest(state_type=type(state).__name__):
                http = self.use_http(Response(contents()))
                store = GitHubStateStore(REPO, TOKEN)
                store.load()
                with self.assertRaisesRegex(RuntimeError, "state_store_invalid|state_store_too_large"):
                    store.save(state)
                self.assertEqual(len(http.requests), 1)

    def test_oversize_response_rejected(self):
        self.use_http(Response(raw=b" " * 2097153))
        with self.assertRaisesRegex(RuntimeError, "state_store_response_too_large"):
            GitHubStateStore(REPO, TOKEN).load()

    def test_invalid_destination_or_missing_token_rejected_before_network(self):
        http = self.use_http()
        for repo, token, branch, path in [
            ("https://evil.invalid/repo", TOKEN, BRANCH, PATH),
            ("owner/../repo", TOKEN, BRANCH, PATH),
            (REPO, "", BRANCH, PATH),
            (REPO, TOKEN, "main", PATH),
            (REPO, TOKEN, BRANCH, ".github/workflows/kuuos-mgap-ci-reentry-poller-v1-2.yml"),
        ]:
            with self.subTest(repo=repo, branch=branch, path=path):
                with self.assertRaisesRegex(RuntimeError, "state_store_invalid|state_store_token_missing"):
                    GitHubStateStore(repo, token, branch=branch, path=path)
        self.assertEqual(http.requests, [])

    def test_redirect_handler_refuses_cross_host_token_forwarding(self):
        with patch("runtime.kuuos_ci_poller_state.urllib.request.build_opener") as build:
            GitHubStateStore(REPO, TOKEN)
        handler = build.call_args.args[0]
        self.assertIsNone(handler.redirect_request(None, None, 302, "redirect", {}, "https://evil.invalid"))


if __name__ == "__main__":
    unittest.main()
