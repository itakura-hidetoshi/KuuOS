#!/usr/bin/env python3
"""KuuOS -> OpenClaw Gateway active controller v0.2.

The controller starts, observes, waits for, and aborts OpenClaw Gateway agent
runs while preserving the KuuOS/ActOS authority boundary.  Effectful controller
operations are preflighted through the local KuuOS control service before the
OpenClaw Gateway RPC is issued.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

VERSION = "kuuos_openclaw_gateway_controller_v0_2"
BRIDGE_VERSION = "kuuos_openclaw_control_bridge_v0_1"
DEFAULT_POLICY_URL = "http://127.0.0.1:8765"
DEFAULT_RECEIPT_DIR = "~/.kuuos/openclaw"


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


class ControllerReceipts:
    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        self.path = data_dir / "gateway-controller-receipts.jsonl"

    def append(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        now_ns = time.time_ns()
        body: dict[str, Any] = {
            "version": VERSION,
            "kind": kind,
            "recordedAtUnixNs": now_ns,
            "payload": payload,
            "worldCommitAuthority": False,
            "truthPromotionAuthority": False,
            "automaticPlanCompletion": False,
            "automaticRollback": False,
        }
        body["receiptDigest"] = digest(body)
        body["receiptId"] = f"kuuos-oc-gw-{now_ns}-{body['receiptDigest'][:16]}"
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(body, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return body


def policy_post(policy_url: str, path: str, payload: dict[str, Any], token: str) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        policy_url.rstrip("/") + path,
        data=canonical_json(payload),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            value = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"KuuOS control service unavailable: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError("KuuOS control service returned a non-object response")
    return value


def preflight_effect(args: argparse.Namespace, action: str, params: dict[str, Any]) -> str:
    envelope = {
        "version": BRIDGE_VERSION,
        "boundary": "ActOS.bounded_adapter_invocation",
        "operation": "gateway-control-preflight",
        "tool": {
            "name": f"openclaw_gateway_{action}",
            "kind": "gateway-rpc",
            "inputKind": "controller",
            "params": params,
            "derivedPaths": [],
        },
        "correlation": {
            "runId": params.get("runId"),
            "toolCallId": None,
            "agentId": params.get("agentId"),
            "sessionKey": params.get("sessionKey") or params.get("key"),
            "sessionId": None,
        },
        "requester": {"surface": "kuuos-gateway-controller", "senderIsOwner": True},
        "invariants": {
            "projectedOnly": True,
            "worldCommit": False,
            "automaticTruthPromotion": False,
            "automaticPlanCompletion": False,
            "automaticRollback": False,
        },
    }
    result = policy_post(args.policy_url, "/v1/preflight", envelope, args.policy_token)
    decision = result.get("decision")
    receipt_id = result.get("receiptId")
    if decision == "deny":
        raise RuntimeError(str(result.get("reason") or "Denied by KuuOS policy"))
    if decision == "approval":
        if not args.approve:
            raise RuntimeError(
                "KuuOS requires explicit approval. Re-run this exact controller command with --approve."
            )
        policy_post(
            args.policy_url,
            "/v1/approval-resolution",
            {
                "version": BRIDGE_VERSION,
                "receiptId": receipt_id,
                "decision": "allow-once",
                "toolName": f"openclaw_gateway_{action}",
                "runId": params.get("runId"),
                "toolCallId": None,
            },
            args.policy_token,
        )
    elif decision != "allow":
        raise RuntimeError(f"Invalid KuuOS preflight decision: {decision!r}")
    return str(receipt_id or "")


def gateway_call(args: argparse.Namespace, method: str, params: dict[str, Any], timeout_ms: int) -> dict[str, Any]:
    command = [
        args.openclaw_bin,
        "gateway",
        "call",
        method,
        "--params",
        json.dumps(params, ensure_ascii=False, separators=(",", ":")),
        "--timeout",
        str(timeout_ms),
        "--json",
        "--no-color",
    ]
    if args.port is not None:
        command.extend(["--port", str(args.port)])
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=max(5.0, timeout_ms / 1000 + 10.0),
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"OpenClaw Gateway RPC {method} failed: {detail}")
    raw = completed.stdout.strip()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"OpenClaw Gateway RPC {method} returned non-JSON output: {raw[:500]}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"OpenClaw Gateway RPC {method} returned a non-object payload")
    return value


def command_start(args: argparse.Namespace, receipts: ControllerReceipts) -> dict[str, Any]:
    idempotency_key = args.idempotency_key or f"kuuos-{int(time.time() * 1000)}-{secrets.token_hex(8)}"
    params: dict[str, Any] = {
        "message": args.message,
        "idempotencyKey": idempotency_key,
    }
    if args.session_key:
        params["sessionKey"] = args.session_key
    if args.agent_id:
        params["agentId"] = args.agent_id
    if args.timeout_ms is not None:
        params["timeout"] = args.timeout_ms

    policy_receipt = preflight_effect(args, "agent_start", params)
    receipts.append(
        "gateway_agent_start_authorized",
        {
            "policyReceiptId": policy_receipt,
            "requestDigest": digest(params),
            "sessionKey": args.session_key,
            "agentId": args.agent_id,
            "idempotencyKey": idempotency_key,
        },
    )
    result = gateway_call(args, "agent", params, args.rpc_timeout_ms)
    run_id = result.get("runId")
    if not isinstance(run_id, str) or not run_id:
        raise RuntimeError(f"OpenClaw agent RPC did not return runId: {result}")
    receipt = receipts.append(
        "gateway_agent_start_receipt",
        {
            "runId": run_id,
            "acceptedAt": result.get("acceptedAt"),
            "sessionKey": result.get("sessionKey") or args.session_key,
            "idempotencyKey": idempotency_key,
            "gatewayPayloadDigest": digest(result),
            "observationRequired": True,
            "verificationRequired": True,
        },
    )
    output: dict[str, Any] = {"start": result, "receiptId": receipt["receiptId"]}
    if args.wait_ms is not None:
        wait_result = gateway_call(
            args,
            "agent.wait",
            {"runId": run_id, "timeoutMs": args.wait_ms},
            max(args.rpc_timeout_ms, args.wait_ms + 5000),
        )
        wait_receipt = receipts.append(
            "gateway_agent_wait_receipt",
            {
                "runId": run_id,
                "gatewayPayloadDigest": digest(wait_result),
                "status": wait_result.get("status"),
                "terminal": wait_result.get("status") in {"ok", "error"},
            },
        )
        output["wait"] = wait_result
        output["waitReceiptId"] = wait_receipt["receiptId"]
    return output


def command_wait(args: argparse.Namespace, receipts: ControllerReceipts) -> dict[str, Any]:
    params = {"runId": args.run_id, "timeoutMs": args.wait_ms}
    result = gateway_call(args, "agent.wait", params, max(args.rpc_timeout_ms, args.wait_ms + 5000))
    receipt = receipts.append(
        "gateway_agent_wait_receipt",
        {
            "runId": args.run_id,
            "gatewayPayloadDigest": digest(result),
            "status": result.get("status"),
            "terminal": result.get("status") in {"ok", "error"},
        },
    )
    return {"wait": result, "receiptId": receipt["receiptId"]}


def command_abort(args: argparse.Namespace, receipts: ControllerReceipts) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if args.session_key:
        params["key"] = args.session_key
    if args.run_id:
        params["runId"] = args.run_id
    if not params:
        raise RuntimeError("abort requires --run-id and/or --session-key")

    policy_receipt = preflight_effect(args, "run_abort", params)
    receipts.append(
        "gateway_abort_authorized",
        {"policyReceiptId": policy_receipt, "requestDigest": digest(params)},
    )
    result = gateway_call(args, "sessions.abort", params, args.rpc_timeout_ms)
    receipt = receipts.append(
        "gateway_abort_receipt",
        {
            "runId": args.run_id,
            "sessionKey": args.session_key,
            "gatewayPayloadDigest": digest(result),
            "gatewayResult": result,
            "observationRequired": True,
            "verificationRequired": True,
        },
    )
    return {"abort": result, "receiptId": receipt["receiptId"]}


def command_sessions(args: argparse.Namespace, receipts: ControllerReceipts) -> dict[str, Any]:
    params: dict[str, Any] = {"limit": args.limit}
    result = gateway_call(args, "sessions.list", params, args.rpc_timeout_ms)
    receipt = receipts.append(
        "gateway_sessions_observation",
        {"gatewayPayloadDigest": digest(result), "limit": args.limit},
    )
    return {"sessions": result, "receiptId": receipt["receiptId"]}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Control OpenClaw Gateway runs through KuuOS/ActOS.")
    root.add_argument("--openclaw-bin", default=os.environ.get("OPENCLAW_BIN", "openclaw"))
    root.add_argument("--port", type=int, default=None, help="Local Gateway port; omit to use OpenClaw config.")
    root.add_argument("--policy-url", default=os.environ.get("KUUOS_OPENCLAW_POLICY_URL", DEFAULT_POLICY_URL))
    root.add_argument("--policy-token", default=os.environ.get("KUUOS_OPENCLAW_TOKEN", ""))
    root.add_argument("--data-dir", default=os.environ.get("KUUOS_OPENCLAW_DATA_DIR", DEFAULT_RECEIPT_DIR))
    root.add_argument("--rpc-timeout-ms", type=int, default=30000)
    root.add_argument("--approve", action="store_true", help="Resolve one KuuOS controller preflight approval as allow-once.")

    sub = root.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Start an OpenClaw Gateway agent run.")
    start.add_argument("--message", required=True)
    start.add_argument("--session-key")
    start.add_argument("--agent-id")
    start.add_argument("--idempotency-key")
    start.add_argument("--timeout-ms", type=int)
    start.add_argument("--wait-ms", type=int)

    wait = sub.add_parser("wait", help="Wait for an existing run without cancelling it on observation timeout.")
    wait.add_argument("--run-id", required=True)
    wait.add_argument("--wait-ms", type=int, default=30000)

    abort = sub.add_parser("abort", help="Abort exact run/session work through sessions.abort.")
    abort.add_argument("--run-id")
    abort.add_argument("--session-key")

    sessions = sub.add_parser("sessions", help="Observe the Gateway session index.")
    sessions.add_argument("--limit", type=int, default=20)
    return root


def main() -> int:
    args = parser().parse_args()
    receipts = ControllerReceipts(Path(args.data_dir).expanduser())
    try:
        if args.command == "start":
            result = command_start(args, receipts)
        elif args.command == "wait":
            result = command_wait(args, receipts)
        elif args.command == "abort":
            result = command_abort(args, receipts)
        elif args.command == "sessions":
            result = command_sessions(args, receipts)
        else:
            raise RuntimeError(f"unknown command {args.command!r}")
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        receipts.append("gateway_controller_error", {"command": args.command, "error": str(error)[:2000]})
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
