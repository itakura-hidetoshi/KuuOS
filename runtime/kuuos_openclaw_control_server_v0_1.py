#!/usr/bin/env python3
"""KuuOS -> OpenClaw bounded policy and host-receipt bridge v0.1.

This service is deliberately small and loopback-first.  It is an ActOS host
adapter boundary, not WORLD commit authority and not a truth-promotion service.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import threading
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

VERSION = "kuuos_openclaw_control_bridge_v0_1"
STATUS = "bounded_openclaw_host_control"

READ_ONLY_TOOLS = frozenset(
    {
        "read",
        "web_fetch",
        "web_search",
        "memory_get",
        "memory_search",
        "session_status",
        "sessions_list",
        "sessions_history",
        "agents_list",
    }
)

CRITICAL_TOOLS = frozenset(
    {
        "exec",
        "apply_patch",
        "write",
        "edit",
        "browser",
        "nodes",
        "cron",
        "message",
        "spawn_agent",
    }
)

SECRET_KEY = re.compile(
    r"(authorization|cookie|token|secret|password|passwd|api[-_]?key|credential)",
    re.IGNORECASE,
)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def sanitize(value: Any, depth: int = 0) -> Any:
    if depth > 6:
        return "[depth-limit]"
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value[:4096] + ("…" if len(value) > 4096 else "")
    if isinstance(value, list):
        return [sanitize(item, depth + 1) for item in value[:128]]
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in list(value.items())[:256]:
            key_text = str(key)
            out[key_text] = "[redacted]" if SECRET_KEY.search(key_text) else sanitize(item, depth + 1)
        return out
    return str(value)


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    data_dir: Path
    bearer_token: str
    policy_mode: str

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "Settings":
        token = os.environ.get("KUUOS_OPENCLAW_TOKEN", "")
        return cls(
            host=args.host,
            port=args.port,
            data_dir=Path(args.data_dir).expanduser(),
            bearer_token=token,
            policy_mode=args.policy_mode,
        )


class ReceiptStore:
    def __init__(self, data_dir: Path) -> None:
        self._path = data_dir / "receipts.jsonl"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    @property
    def path(self) -> Path:
        return self._path

    def append(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        now_ns = time.time_ns()
        body = {
            "version": VERSION,
            "status": STATUS,
            "kind": kind,
            "recordedAtUnixNs": now_ns,
            "payload": sanitize(payload),
        }
        body["receiptDigest"] = digest(body)
        body["receiptId"] = f"kuuos-oc-{now_ns}-{body['receiptDigest'][:16]}"
        line = json.dumps(body, ensure_ascii=False, sort_keys=True)
        with self._lock:
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        return body


def tool_name(payload: dict[str, Any]) -> str:
    tool = payload.get("tool")
    if not isinstance(tool, dict):
        return ""
    name = tool.get("name")
    return name if isinstance(name, str) else ""


def requester_is_owner(payload: dict[str, Any]) -> bool | None:
    requester = payload.get("requester")
    if not isinstance(requester, dict):
        return None
    owner = requester.get("senderIsOwner")
    return owner if isinstance(owner, bool) else None


def decide_preflight(settings: Settings, payload: dict[str, Any]) -> dict[str, Any]:
    name = tool_name(payload)
    owner = requester_is_owner(payload)

    if settings.policy_mode == "observe":
        return {
            "decision": "allow",
            "reason": "observe mode: decision recorded without an execution veto",
        }

    if name in READ_ONLY_TOOLS:
        return {
            "decision": "allow",
            "reason": f"{name or 'tool'} is in the KuuOS bounded read-only set",
        }

    if settings.policy_mode == "owner-strict" and owner is False:
        return {
            "decision": "deny",
            "reason": "KuuOS owner-strict policy denies effectful tools for a proven non-owner requester.",
        }

    severity = "critical" if name in CRITICAL_TOOLS else "warning"
    return {
        "decision": "approval",
        "title": f"KuuOS ActOS approval: {name or 'unknown tool'}",
        "description": (
            "This OpenClaw call is an external-effect candidate. "
            "KuuOS keeps WORLD commit and truth promotion separate; approve only this bounded invocation."
        ),
        "severity": severity,
        "reason": "Effectful or unclassified tools require explicit ActOS-bounded approval.",
    }


class KuuOSHandler(BaseHTTPRequestHandler):
    server_version = "KuuOSOpenClaw/0.1"

    @property
    def settings(self) -> Settings:
        return self.server.settings  # type: ignore[attr-defined]

    @property
    def store(self) -> ReceiptStore:
        return self.server.store  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[KuuOS/OpenClaw] {self.address_string()} - {fmt % args}")

    def _authorized(self) -> bool:
        expected = self.settings.bearer_token
        if not expected:
            return True
        actual = self.headers.get("Authorization", "")
        return secrets.compare_digest(actual, f"Bearer {expected}")

    def _json_body(self) -> dict[str, Any] | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return None
        if length <= 0 or length > 1_048_576:
            return None
        try:
            value = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _send(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/health":
            self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        self._send(
            HTTPStatus.OK,
            {
                "version": VERSION,
                "status": "ok",
                "policyMode": self.settings.policy_mode,
                "receiptPath": str(self.store.path),
                "worldCommitAuthority": False,
                "truthPromotionAuthority": False,
            },
        )

    def do_POST(self) -> None:  # noqa: N802
        if not self._authorized():
            self._send(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
            return

        payload = self._json_body()
        if payload is None:
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_json"})
            return

        if self.path == "/v1/preflight":
            if payload.get("boundary") != "ActOS.bounded_adapter_invocation":
                self._send(
                    HTTPStatus.BAD_REQUEST,
                    {"error": "invalid_boundary", "decision": "deny"},
                )
                return
            decision = decide_preflight(self.settings, payload)
            receipt = self.store.append(
                "openclaw_preflight",
                {
                    "requestDigest": digest(sanitize(payload)),
                    "toolName": tool_name(payload),
                    "requesterIsOwner": requester_is_owner(payload),
                    "decision": decision["decision"],
                    "reason": decision.get("reason"),
                    "projectedOnly": True,
                    "worldCommit": False,
                    "automaticTruthPromotion": False,
                    "automaticPlanCompletion": False,
                    "automaticRollback": False,
                },
            )
            result = dict(decision)
            result["receiptId"] = receipt["receiptId"]
            self._send(HTTPStatus.OK, result)
            return

        if self.path == "/v1/approval-resolution":
            receipt = self.store.append(
                "openclaw_approval_resolution",
                {
                    "receiptId": payload.get("receiptId"),
                    "decision": payload.get("decision"),
                    "toolName": payload.get("toolName"),
                    "runId": payload.get("runId"),
                    "toolCallId": payload.get("toolCallId"),
                    "worldCommit": False,
                    "truthPromotion": False,
                },
            )
            self._send(HTTPStatus.OK, {"ok": True, "receiptId": receipt["receiptId"]})
            return

        if self.path == "/v1/post-effect":
            if payload.get("boundary") != "ActOS.canonical_host_receipt":
                self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_boundary"})
                return
            receipt = self.store.append(
                "openclaw_host_receipt",
                {
                    "hostPayloadDigest": digest(sanitize(payload)),
                    "toolName": payload.get("toolName"),
                    "runId": payload.get("runId"),
                    "toolCallId": payload.get("toolCallId"),
                    "hasError": payload.get("error") is not None,
                    "hostReceiptIsWorldCommit": False,
                    "hostReceiptIsWorldTruth": False,
                    "observationRequired": True,
                    "verificationRequired": True,
                    "automaticPlanCompletion": False,
                    "automaticRollback": False,
                },
            )
            self._send(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "receiptId": receipt["receiptId"],
                    "observationDebtOpen": True,
                    "verificationDebtOpen": True,
                },
            )
            return

        self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})


class KuuOSServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, settings: Settings, store: ReceiptStore) -> None:
        super().__init__((settings.host, settings.port), KuuOSHandler)
        self.settings = settings
        self.store = store


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the KuuOS bounded OpenClaw control service.",
    )
    parser.add_argument("--host", default=os.environ.get("KUUOS_OPENCLAW_HOST", "127.0.0.1"))
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("KUUOS_OPENCLAW_PORT", "8765")),
    )
    parser.add_argument(
        "--data-dir",
        default=os.environ.get("KUUOS_OPENCLAW_DATA_DIR", "~/.kuuos/openclaw"),
    )
    parser.add_argument(
        "--policy-mode",
        choices=("approval", "owner-strict", "observe"),
        default=os.environ.get("KUUOS_OPENCLAW_POLICY_MODE", "approval"),
    )
    return parser.parse_args()


def main() -> int:
    settings = Settings.from_args(parse_args())
    if settings.host not in {"127.0.0.1", "::1", "localhost"}:
        raise SystemExit(
            "Refusing a non-loopback bind in v0.1. Put an authenticated reverse proxy in front "
            "or extend the bridge deliberately."
        )

    store = ReceiptStore(settings.data_dir)
    server = KuuOSServer(settings, store)
    print(
        f"KuuOS OpenClaw control service {VERSION} listening on "
        f"http://{settings.host}:{settings.port}"
    )
    print(f"policy={settings.policy_mode} receipts={store.path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
