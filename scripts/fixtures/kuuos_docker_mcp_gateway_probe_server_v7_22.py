#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from typing import Any


SERVER_INFO = {
    "name": "kuuos-docker-mcp-gateway-probe",
    "version": "7.22",
}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.write(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
    )
    sys.stdout.flush()


def response(request_id: Any, result: Any) -> None:
    emit({"jsonrpc": "2.0", "id": request_id, "result": result})


def error(request_id: Any, code: int, message: str) -> None:
    emit(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }
    )


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(message, dict):
            continue

        method = str(message.get("method", ""))
        request_id = message.get("id")

        if request_id is None:
            continue

        if method == "initialize":
            params = message.get("params", {})
            protocol_version = (
                str(params.get("protocolVersion", "2025-06-18"))
                if isinstance(params, dict)
                else "2025-06-18"
            )
            response(
                request_id,
                {
                    "protocolVersion": protocol_version,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": SERVER_INFO,
                },
            )
        elif method == "ping":
            response(request_id, {})
        elif method == "tools/list":
            response(
                request_id,
                {
                    "tools": [
                        {
                            "name": "kuuos_probe_echo",
                            "title": "KuuOS Gateway Probe Echo",
                            "description": (
                                "Read-only deterministic echo used only to verify "
                                "Docker MCP Gateway discovery and tool forwarding."
                            ),
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"}
                                },
                                "required": ["message"],
                                "additionalProperties": False,
                            },
                            "annotations": {
                                "readOnlyHint": True,
                                "destructiveHint": False,
                                "idempotentHint": True,
                                "openWorldHint": False,
                            },
                        }
                    ]
                },
            )
        elif method == "tools/call":
            params = message.get("params", {})
            if not isinstance(params, dict):
                error(request_id, -32602, "invalid params")
                continue
            name = str(params.get("name", ""))
            arguments = params.get("arguments", {})
            if name != "kuuos_probe_echo":
                error(request_id, -32601, "unknown tool")
                continue
            if not isinstance(arguments, dict):
                error(request_id, -32602, "invalid arguments")
                continue
            message_text = str(arguments.get("message", ""))
            marker = "KUUOS_GATEWAY_PROBE:" + message_text
            response(
                request_id,
                {
                    "content": [{"type": "text", "text": marker}],
                    "structuredContent": {
                        "marker": marker,
                        "network_required": False,
                        "write_effect": False,
                    },
                    "isError": False,
                },
            )
        else:
            error(request_id, -32601, "method not found")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
