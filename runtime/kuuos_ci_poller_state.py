"""Fail-closed, compare-and-swap storage for the public CI poller checkpoint.

The state-only branch and file must already exist. This module never creates a
branch, initializes a cursor, falls back to a cache, or retries an uncertain
write. Callers validate the checkpoint's schema and source identity before use.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import http.client
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Mapping


STATE_BRANCH = "state/kuuos-mgap-ci-poller-v1-2"
STATE_PATH = "kuuos_mgap_ci_completion_poller_v1_2.json"
MAX_STATE_BYTES = 1024 * 1024
MAX_RESPONSE_BYTES = 2 * MAX_STATE_BYTES
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # In particular, never forward the repository token to another host.
        return None


def _reject_non_json_constant(value: str) -> None:
    raise ValueError("non_json_constant")


def _blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


class GitHubStateStore:
    """Update only a pre-provisioned state file using its last observed blob SHA."""

    def __init__(
        self,
        repo: str,
        token: str,
        branch: str = STATE_BRANCH,
        path: str = STATE_PATH,
    ) -> None:
        if (
            not isinstance(repo, str)
            or _REPO.fullmatch(repo) is None
            or any(part in {".", ".."} for part in repo.split("/"))
            or branch != STATE_BRANCH
            or path != STATE_PATH
        ):
            raise RuntimeError("state_store_invalid_destination")
        if not isinstance(token, str) or not token.strip() or "\n" in token or "\r" in token:
            raise RuntimeError("state_store_token_missing")
        self._url = f"https://api.github.com/repos/{repo}/contents/{path}"
        self._branch = branch
        self._path = path
        self._token = token
        self._sha: str | None = None
        self._opener = urllib.request.build_opener(_NoRedirect())

    def _request(self, method: str, payload: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
        url = self._url
        if method == "GET":
            url += "?ref=" + urllib.parse.quote(self._branch, safe="")
        request = urllib.request.Request(
            url,
            data=None if payload is None else json.dumps(dict(payload)).encode("utf-8"),
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "KuuOS-public-ci-poller-state-v1.2",
            },
        )
        try:
            with self._opener.open(request, timeout=20) as response:
                if response.status != 200:
                    raise RuntimeError("state_store_unexpected_response_status")
                raw = response.read(MAX_RESPONSE_BYTES + 1)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise RuntimeError("state_store_missing") from None
            if exc.code == 409:
                raise RuntimeError("state_store_conflict") from None
            raise RuntimeError(f"state_store_http_{exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise RuntimeError("state_store_transport_failed") from None
        if len(raw) > MAX_RESPONSE_BYTES:
            raise RuntimeError("state_store_response_too_large")
        try:
            result = json.loads(raw.decode("utf-8"), parse_constant=_reject_non_json_constant)
        except (ValueError, UnicodeError, RecursionError):
            raise RuntimeError("state_store_invalid_response") from None
        if not isinstance(result, dict):
            raise RuntimeError("state_store_invalid_response")
        return result

    def load(self) -> Mapping[str, Any]:
        self._sha = None
        payload = self._request("GET")
        sha = payload.get("sha")
        content = payload.get("content")
        size = payload.get("size")
        if (
            payload.get("type") != "file"
            or payload.get("path") != self._path
            or payload.get("encoding") != "base64"
            or not isinstance(sha, str)
            or _SHA40.fullmatch(sha) is None
            or not isinstance(content, str)
            or type(size) is not int
            or not 0 <= size <= MAX_STATE_BYTES
        ):
            raise RuntimeError("state_store_invalid_contents")
        try:
            raw = base64.b64decode("".join(content.split()), validate=True)
            if len(raw) != size or _blob_sha(raw) != sha:
                raise ValueError("contents_integrity_mismatch")
            state = json.loads(raw.decode("utf-8"), parse_constant=_reject_non_json_constant)
        except (ValueError, binascii.Error, UnicodeError, RecursionError):
            raise RuntimeError("state_store_invalid_checkpoint") from None
        if not isinstance(state, dict):
            raise RuntimeError("state_store_invalid_checkpoint")
        self._sha = sha
        return state

    def save(self, state: Mapping[str, Any]) -> None:
        if self._sha is None:
            raise RuntimeError("state_store_not_loaded")
        if not isinstance(state, Mapping):
            raise RuntimeError("state_store_invalid_checkpoint")
        try:
            raw = (
                json.dumps(dict(state), ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
                + "\n"
            ).encode("utf-8")
        except (TypeError, ValueError, UnicodeError, RecursionError):
            raise RuntimeError("state_store_invalid_checkpoint") from None
        if len(raw) > MAX_STATE_BYTES:
            raise RuntimeError("state_store_too_large")
        expected_sha = self._sha
        # Any ambiguous response invalidates this instance until a fresh load.
        self._sha = None
        result = self._request(
            "PUT",
            {
                "message": "chore: checkpoint public CI poller [skip ci]",
                "content": base64.b64encode(raw).decode("ascii"),
                "branch": self._branch,
                "sha": expected_sha,
            },
        )
        content = result.get("content")
        if (
            not isinstance(content, dict)
            or content.get("type") != "file"
            or content.get("path") != self._path
            or content.get("sha") != _blob_sha(raw)
        ):
            raise RuntimeError("state_store_invalid_save_response")
        self._sha = content["sha"]
