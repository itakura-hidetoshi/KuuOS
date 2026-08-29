from __future__ import annotations

import json
import re
import threading
import time
import urllib.request
from copy import deepcopy
from typing import Any, Mapping

from .state_store import validate_loaded_state


DEFAULT_GITHUB_ISSUE_API_URL = (
    "https://api.github.com/repos/itakura-hidetoshi/KuuOS/issues/1548"
)
_JSON_FENCE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


def parse_canonical_issue_state(body: str) -> dict[str, Any]:
    """Extract and normalize the canonical JSON state embedded in the issue body."""
    match = _JSON_FENCE.search(body)
    if match is None:
        raise ValueError("canonical GitHub issue does not contain a fenced JSON state")

    state = json.loads(match.group(1))
    validate_loaded_state(state)

    normalized = deepcopy(state)
    if "mathematical_frontier" not in normalized and "frontier" in normalized:
        normalized["mathematical_frontier"] = normalized["frontier"]
    normalized.setdefault("next_actions", [])
    normalized.setdefault("continuation", {})
    normalized.setdefault("updated_at", None)
    normalized.setdefault("updated_by", "github-issue")
    return normalized


class GitHubIssueStateStore:
    """Read-only durable state backed by one public GitHub issue."""

    def __init__(
        self,
        api_url: str = DEFAULT_GITHUB_ISSUE_API_URL,
        *,
        timeout_seconds: float = 10.0,
        cache_ttl_seconds: float = 15.0,
    ):
        if not api_url.startswith("https://api.github.com/"):
            raise ValueError("GitHub issue backend requires an api.github.com HTTPS URL")
        self.api_url = api_url
        self.timeout_seconds = timeout_seconds
        self.cache_ttl_seconds = cache_ttl_seconds
        self._cache: dict[str, Any] | None = None
        self._cache_at = 0.0
        self._lock = threading.RLock()

    def read(self) -> dict[str, Any]:
        with self._lock:
            now = time.monotonic()
            if self._cache is not None and now - self._cache_at < self.cache_ttl_seconds:
                return deepcopy(self._cache)

            request = urllib.request.Request(
                self.api_url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "KuuOS-MCP-State-Bridge/0.3",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            )
            try:
                with urllib.request.urlopen(
                    request,
                    timeout=self.timeout_seconds,
                ) as response:
                    issue = json.load(response)
                body = issue.get("body")
                if not isinstance(body, str):
                    raise ValueError("canonical GitHub issue has no text body")
                state = parse_canonical_issue_state(body)
            except Exception:
                if self._cache is not None:
                    return deepcopy(self._cache)
                raise

            self._cache = deepcopy(state)
            self._cache_at = now
            return deepcopy(state)

    def update(
        self,
        patch: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]:
        raise RuntimeError("GitHub issue state backend is read-only")

    def replace(
        self,
        state: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]:
        raise RuntimeError("GitHub issue state backend is read-only")
