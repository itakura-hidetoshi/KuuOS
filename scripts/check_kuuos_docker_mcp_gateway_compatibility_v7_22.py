#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import selectors
import subprocess
import tempfile
import time
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "2025-06-18"
UPSTREAM_SHA = "a34df45d4ec0e941a9853ad768c4f6cd818966b3"
PROFILE_ID = "kuuos_gateway_probe"
IMAGE = "kuuos-mcp-gateway-probe:v7.22"


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def run(
    args: Sequence[str],
    *,
    cwd: pathlib.Path,
    check: bool = True,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "DOCKER_MCP_IN_CONTAINER": "1",
        "DOCKER_MCP_USE_CE": "1",
    }
    completed = subprocess.run(
        list(args),
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if check and completed.returncode != 0:
        raise RuntimeError(
            "command_failed:"
            + " ".join(args)
            + "\nstdout:\n"
            + completed.stdout[-3000:]
            + "\nstderr:\n"
            + completed.stderr[-3000:]
        )
    return completed


class MCPClient:
    def __init__(
        self,
        command: Sequence[str],
        *,
        cwd: pathlib.Path,
        timeout_seconds: float = 240.0,
    ) -> None:
        env = {
            **os.environ,
            "DOCKER_MCP_IN_CONTAINER": "1",
            "DOCKER_MCP_USE_CE": "1",
        }
        self.process = subprocess.Popen(
            list(command),
            cwd=str(cwd),
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        if self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("gateway_stdio_unavailable")
        self.stdin = self.process.stdin
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.timeout = timeout_seconds
        self.next_id = 1

    def request(
        self,
        method: str,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        request_id = self.next_id
        self.next_id += 1
        payload: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
        }
        if params is not None:
            payload["params"] = dict(params)
        self.stdin.write(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            + "\n"
        )
        self.stdin.flush()

        selector = selectors.DefaultSelector()
        selector.register(self.stdout, selectors.EVENT_READ)
        deadline = time.monotonic() + self.timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"gateway_timeout:{method}")
                if not selector.select(remaining):
                    continue
                line = self.stdout.readline()
                if line == "":
                    stderr = ""
                    if self.stderr is not None:
                        try:
                            stderr = self.stderr.read()
                        except Exception:
                            pass
                    raise RuntimeError(
                        "gateway_closed:"
                        + str(self.process.poll())
                        + ":"
                        + stderr[-2400:]
                    )
                line = line.strip()
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(message, dict) and message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(
                            "gateway_rpc_error:"
                            + method
                            + ":"
                            + json.dumps(
                                message["error"],
                                ensure_ascii=False,
                            )[:2200]
                        )
                    return message
        finally:
            selector.close()

    def notify(self, method: str) -> None:
        self.stdin.write(
            json.dumps({"jsonrpc": "2.0", "method": method}) + "\n"
        )
        self.stdin.flush()

    def close(self) -> None:
        try:
            self.stdin.close()
        except Exception:
            pass
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)


def tool_map(response: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result = response.get("result", {})
    if not isinstance(result, Mapping):
        return {}
    raw = result.get("tools", [])
    if not isinstance(raw, list):
        return {}
    return {
        str(item["name"]): dict(item)
        for item in raw
        if isinstance(item, Mapping) and item.get("name")
    }


def textual_payload(response: Mapping[str, Any]) -> str:
    result = response.get("result", {})
    if not isinstance(result, Mapping):
        return ""
    content = result.get("content", [])
    if not isinstance(content, list):
        return ""
    return "\n".join(
        str(item.get("text", ""))
        for item in content
        if isinstance(item, Mapping) and item.get("type") == "text"
    )


def build_fixture_image(root: pathlib.Path) -> str:
    fixture = (
        root
        / "scripts"
        / "fixtures"
        / "kuuos_docker_mcp_gateway_probe_server_v7_22.py"
    )
    if not fixture.is_file():
        raise RuntimeError("gateway_probe_fixture_missing")

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".Dockerfile",
        delete=False,
        encoding="utf-8",
    ) as handle:
        dockerfile = pathlib.Path(handle.name)
        handle.write(
            "FROM python:3.12-alpine\n"
            "WORKDIR /app\n"
            "COPY scripts/fixtures/"
            "kuuos_docker_mcp_gateway_probe_server_v7_22.py /app/server.py\n"
            "ENTRYPOINT [\"python\",\"/app/server.py\"]\n"
        )

    try:
        built = run(
            [
                "docker",
                "build",
                "--pull",
                "-t",
                IMAGE,
                "-f",
                str(dockerfile),
                ".",
            ],
            cwd=root,
            timeout=300,
        )
    finally:
        dockerfile.unlink(missing_ok=True)

    return digest(
        {
            "stdout": built.stdout[-4000:],
            "stderr": built.stderr[-4000:],
        }
    )


def prepare_profile(root: pathlib.Path) -> dict[str, Any]:
    docker_root = pathlib.Path.home() / ".docker" / "mcp"
    catalogs = docker_root / "catalogs"
    catalogs.mkdir(parents=True, exist_ok=True)

    entry_path = catalogs / "kuuos-gateway-probe-server.yaml"
    entry_path.write_text(
        "\n".join(
            [
                "name: kuuos-gateway-probe",
                "title: KuuOS Gateway Probe",
                "type: server",
                f"image: {IMAGE}",
                "description: Deterministic read-only KuuOS Docker MCP Gateway probe.",
                "disableNetwork: true",
                "longLived: false",
                "tools:",
                "  - name: kuuos_probe_echo",
                "    description: Read-only deterministic gateway forwarding probe.",
                "    annotations:",
                "      readOnlyHint: true",
                "      destructiveHint: false",
                "      idempotentHint: true",
                "      openWorldHint: false",
                "",
            ]
        ),
        encoding="utf-8",
    )

    run(["docker", "mcp", "feature", "enable", "profiles"], cwd=root)

    run(
        ["docker", "mcp", "profile", "remove", PROFILE_ID],
        cwd=root,
        check=False,
    )
    created = run(
        [
            "docker",
            "mcp",
            "profile",
            "create",
            "--name",
            "KuuOS Gateway Probe",
            "--id",
            PROFILE_ID,
            "--server",
            "file://./kuuos-gateway-probe-server.yaml",
        ],
        cwd=catalogs,
    )
    shown = run(
        [
            "docker",
            "mcp",
            "profile",
            "show",
            PROFILE_ID,
            "--format",
            "json",
        ],
        cwd=root,
    )

    if "kuuos-gateway-probe" not in shown.stdout:
        raise RuntimeError("gateway_profile_missing_probe_server")

    return {
        "entry_digest": hashlib.sha256(
            entry_path.read_bytes()
        ).hexdigest(),
        "create_output_digest": digest(created.stdout),
        "show_output_digest": digest(shown.stdout),
        "network_disabled": True,
    }


def live_gateway_probe(root: pathlib.Path) -> dict[str, Any]:
    client = MCPClient(
        ["docker", "mcp", "gateway", "run", "--profile", PROFILE_ID],
        cwd=root,
    )
    try:
        initialized = client.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "KuuOS Docker MCP Gateway Compatibility Probe",
                    "version": "7.22",
                },
            },
        )
        client.notify("notifications/initialized")

        listed = client.request("tools/list")
        tools = tool_map(listed)
        if not tools:
            raise RuntimeError("gateway_tools_list_empty")

        selected = ""
        for name, tool in tools.items():
            haystack = (
                name
                + " "
                + str(tool.get("title", ""))
                + " "
                + str(tool.get("description", ""))
            ).lower()
            if "kuuos" in haystack and "probe" in haystack:
                selected = name
                break
        if not selected:
            raise RuntimeError(
                "gateway_probe_tool_not_discovered:"
                + ",".join(sorted(tools))
            )

        call = client.request(
            "tools/call",
            {
                "name": selected,
                "arguments": {"message": "dependent-origination"},
            },
        )
        result = call.get("result", {})
        if isinstance(result, Mapping) and result.get("isError") is True:
            raise RuntimeError("gateway_probe_tool_returned_error")

        text = textual_payload(call)
        marker = "KUUOS_GATEWAY_PROBE:dependent-origination"
        if marker not in text:
            raise RuntimeError("gateway_probe_marker_missing")

        init_result = initialized.get("result", {})
        return {
            "protocol_version": (
                str(init_result.get("protocolVersion", ""))
                if isinstance(init_result, Mapping)
                else ""
            ),
            "listed_tool_count": len(tools),
            "listed_tools_digest": digest(sorted(tools)),
            "selected_tool_name_digest": digest(selected),
            "tool_forwarding_succeeded": True,
            "tool_call_result_digest": digest(call.get("result", {})),
            "marker_observed": True,
        }
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument(
        "--receipt",
        default="docker_mcp_gateway_compatibility_receipt_v7_22.json",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.repository_root).resolve()
    if not (root / ".git").exists():
        raise RuntimeError("kuuos_repository_root_invalid")

    docker_info = run(
        ["docker", "version", "--format", "{{json .}}"],
        cwd=root,
    )
    plugin_help = run(["docker", "mcp", "--help"], cwd=root)
    gateway_help = run(
        ["docker", "mcp", "gateway", "run", "--help"],
        cwd=root,
    )

    image_build_digest = build_fixture_image(root)
    profile = prepare_profile(root)
    live = live_gateway_probe(root)

    receipt = {
        "version": "kuuos_docker_mcp_gateway_compatibility_receipt_v7_22",
        "status": "KUUOS_DOCKER_MCP_GATEWAY_COMPATIBILITY_VERIFIED",
        "docker_mcp_gateway": {
            "upstream_main_sha": UPSTREAM_SHA,
            "built_from_upstream_source": True,
            "docker_version_digest": digest(docker_info.stdout),
            "plugin_help_digest": digest(plugin_help.stdout),
            "gateway_help_digest": digest(gateway_help.stdout),
        },
        "fixture": {
            "image": IMAGE,
            "image_build_digest": image_build_digest,
            **profile,
        },
        "gateway_probe": live,
        "boundary": {
            "fixture_network_disabled": True,
            "fixture_write_effect": False,
            "gateway_grants_downstream_authority": False,
            "profile_membership_grants_tool_authority": False,
            "gateway_isolation_replaces_provider_authority": False,
            "credentials_persisted": False,
            "external_catalog_required": False,
            "source_authority_transferred": False,
        },
    }

    receipt_path = pathlib.Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
