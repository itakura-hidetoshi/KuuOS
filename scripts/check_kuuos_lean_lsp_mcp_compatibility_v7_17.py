#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import selectors
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "2025-11-25"
EXPECTED_SERVER_VERSION = "0.30.0"
EXPECTED_UPSTREAM_SHA = "bb176c58a4f895061561685318e92b8db446f1b5"
EXPECTED_LEAN_TOOLCHAIN = "leanprover/lean4:v4.30.0-rc2"
EXPECTED_MATHLIB_SHA = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
PROBE_FILE = "formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean"

REQUIRED_TOOLS = {
    "lean_file_outline",
    "lean_diagnostic_messages",
    "lean_goal",
    "lean_hover_info",
    "lean_declaration_file",
    "lean_references",
    "lean_completions",
    "lean_code_actions",
    "lean_verify",
}

DISABLED_DURING_PROBE = ",".join(
    [
        "lean_run_code",
        "lean_build",
        "lean_profile_proof",
        "lean_minimal_hypotheses",
        "lean_multi_attempt",
        "lean_leansearch",
        "lean_loogle",
        "lean_leanfinder",
        "lean_state_search",
        "lean_hammer_premise",
    ]
)


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def read_json(path: pathlib.Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected_object:{path}")
    return value


def require_pins(root: pathlib.Path) -> dict[str, Any]:
    toolchain = (root / "lean-toolchain").read_text(encoding="utf-8").strip()
    if toolchain != EXPECTED_LEAN_TOOLCHAIN:
        raise RuntimeError(
            f"lean_toolchain_mismatch:{toolchain}:{EXPECTED_LEAN_TOOLCHAIN}"
        )

    manifest = read_json(root / "lake-manifest.json")
    mathlib = next(
        (
            item
            for item in manifest.get("packages", [])
            if isinstance(item, Mapping) and item.get("name") == "mathlib"
        ),
        None,
    )
    if not isinstance(mathlib, Mapping):
        raise RuntimeError("mathlib_manifest_entry_missing")
    mathlib_sha = str(mathlib.get("rev", ""))
    if mathlib_sha != EXPECTED_MATHLIB_SHA:
        raise RuntimeError(
            f"mathlib_sha_mismatch:{mathlib_sha}:{EXPECTED_MATHLIB_SHA}"
        )

    probe = root / PROBE_FILE
    if not probe.is_file():
        raise RuntimeError("probe_file_missing")
    text = probe.read_text(encoding="utf-8")
    if not text.startswith("import Mathlib"):
        raise RuntimeError("probe_file_not_mathlib_direct")

    return {
        "lean_toolchain": toolchain,
        "mathlib_sha": mathlib_sha,
        "probe_file": PROBE_FILE,
        "probe_file_digest": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


class MCPClient:
    def __init__(
        self,
        command: Sequence[str],
        *,
        cwd: pathlib.Path,
        env: Mapping[str, str],
        timeout_seconds: float = 120.0,
    ) -> None:
        merged = os.environ.copy()
        merged.update({str(k): str(v) for k, v in env.items()})
        self.process = subprocess.Popen(
            list(command),
            cwd=str(cwd),
            env=merged,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        if self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("mcp_stdio_unavailable")
        self.stdin = self.process.stdin
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.timeout = timeout_seconds
        self.next_id = 1
        self.stderr_tail: list[str] = []

    def _read_response(self, request_id: int) -> dict[str, Any]:
        selector = selectors.DefaultSelector()
        selector.register(self.stdout, selectors.EVENT_READ)
        deadline = time.monotonic() + self.timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"mcp_timeout:id={request_id}")
                events = selector.select(remaining)
                if not events:
                    continue
                line = self.stdout.readline()
                if line == "":
                    if self.stderr is not None:
                        try:
                            err = self.stderr.read()
                        except Exception:
                            err = ""
                        if err:
                            self.stderr_tail.extend(err.splitlines()[-20:])
                    raise RuntimeError(
                        "mcp_server_closed:"
                        + str(self.process.poll())
                        + ":"
                        + " | ".join(self.stderr_tail[-5:])
                    )
                line = line.strip()
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    self.stderr_tail.append("stdout_non_json:" + line[:240])
                    continue
                if isinstance(message, dict) and message.get("id") == request_id:
                    return message
        finally:
            selector.close()

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
        response = self._read_response(request_id)
        if "error" in response:
            raise RuntimeError(
                "mcp_rpc_error:"
                + method
                + ":"
                + json.dumps(response["error"], ensure_ascii=False)
            )
        return response

    def notify(
        self,
        method: str,
        params: Mapping[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "jsonrpc": "2.0",
            "method": method,
        }
        if params is not None:
            payload["params"] = dict(params)
        self.stdin.write(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            + "\n"
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
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)


def tool_map(list_response: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result = list_response.get("result", {})
    if not isinstance(result, Mapping):
        return {}
    raw = result.get("tools", [])
    if not isinstance(raw, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for item in raw:
        if isinstance(item, Mapping) and item.get("name"):
            out[str(item["name"])] = dict(item)
    return out


def call_tool(
    client: MCPClient,
    name: str,
    arguments: Mapping[str, Any],
) -> dict[str, Any]:
    response = client.request(
        "tools/call",
        {"name": name, "arguments": dict(arguments)},
    )
    result = response.get("result", {})
    if isinstance(result, Mapping) and result.get("isError") is True:
        raise RuntimeError(
            "mcp_tool_error:"
            + name
            + ":"
            + json.dumps(result, ensure_ascii=False)[:2000]
        )
    return response


def extract_text(response: Mapping[str, Any]) -> str:
    result = response.get("result", {})
    if not isinstance(result, Mapping):
        return ""
    content = result.get("content", [])
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if isinstance(item, Mapping) and item.get("type") == "text":
            parts.append(str(item.get("text", "")))
    return "\n".join(parts)


def server_version(command: Sequence[str], root: pathlib.Path) -> str:
    completed = subprocess.run(
        [*command, "--version"],
        cwd=str(root),
        env={**os.environ, "LEAN_LOG_LEVEL": "NONE"},
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = (completed.stdout + "\n" + completed.stderr).strip()
    if EXPECTED_SERVER_VERSION not in output:
        raise RuntimeError(
            "lean_lsp_mcp_version_mismatch:" + output[:500]
        )
    return output


def live_probe(
    root: pathlib.Path,
    *,
    command: Sequence[str],
) -> dict[str, Any]:
    env = {
        "LEAN_PROJECT_PATH": str(root),
        "LEAN_LOG_LEVEL": "NONE",
        "LEAN_MCP_DISABLED_TOOLS": DISABLED_DURING_PROBE,
        "LEAN_MCP_SCRATCH_SLOTS": "1",
    }
    client = MCPClient(command, cwd=root, env=env, timeout_seconds=180)
    try:
        initialized = client.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "KuuOS Lean-LSP MCP Compatibility Probe",
                    "version": "7.17",
                },
            },
        )
        client.notify("notifications/initialized")

        listed = client.request("tools/list")
        tools = tool_map(listed)
        missing = sorted(REQUIRED_TOOLS.difference(tools))
        if missing:
            raise RuntimeError(
                "required_lean_lsp_tools_missing:" + ",".join(missing)
            )

        forbidden_visible = sorted(
            set(DISABLED_DURING_PROBE.split(",")).intersection(tools)
        )
        if forbidden_visible:
            raise RuntimeError(
                "disabled_tools_still_visible:" + ",".join(forbidden_visible)
            )

        outline = call_tool(
            client,
            "lean_file_outline",
            {"file_path": PROBE_FILE},
        )
        outline_text = extract_text(outline)
        if "DependentOriginationFunctorialTransportV0_1" not in outline_text:
            # Some versions return structured output without the namespace text.
            # Require non-empty successful output in that case.
            result = outline.get("result", {})
            if not outline_text and not (
                isinstance(result, Mapping) and result.get("structuredContent")
            ):
                raise RuntimeError("lean_file_outline_empty")

        diagnostics = call_tool(
            client,
            "lean_diagnostic_messages",
            {"file_path": PROBE_FILE, "severity": "error"},
        )

        init_result = initialized.get("result", {})
        protocol = (
            str(init_result.get("protocolVersion", ""))
            if isinstance(init_result, Mapping)
            else ""
        )
        if not protocol:
            raise RuntimeError("initialize_protocol_version_missing")

        return {
            "initialize_protocol_version": protocol,
            "server_info_digest": sha(
                init_result.get("serverInfo", {})
                if isinstance(init_result, Mapping)
                else {}
            ),
            "listed_tool_count": len(tools),
            "listed_tool_names_digest": sha(sorted(tools)),
            "required_tools_present": True,
            "disabled_tools_absent": True,
            "outline_result_digest": sha(outline.get("result", {})),
            "outline_text_length": len(outline_text),
            "diagnostics_result_digest": sha(
                diagnostics.get("result", {})
            ),
            "diagnostics_call_succeeded": True,
        }
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repository-root",
        default=".",
        help="KuuOS repository root",
    )
    parser.add_argument(
        "--receipt",
        default="lean_lsp_mcp_compatibility_receipt_v7_17.json",
    )
    parser.add_argument(
        "--live-probe",
        action="store_true",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.repository_root).resolve()
    pins = require_pins(root)

    command = [
        "uvx",
        "--from",
        f"lean-lsp-mcp=={EXPECTED_SERVER_VERSION}",
        "lean-lsp-mcp",
        "--transport",
        "stdio",
    ]

    version_output = server_version(command[:-2], root)

    probe_result: dict[str, Any] = {}
    if args.live_probe:
        probe_result = live_probe(root, command=command)

    receipt = {
        "version": "kuuos_lean_lsp_mcp_compatibility_receipt_v7_17",
        "status": (
            "KUUOS_LEAN_LSP_MCP_COMPATIBILITY_VERIFIED"
            if args.live_probe
            else "KUUOS_LEAN_LSP_MCP_STATIC_COMPATIBILITY_READY"
        ),
        "kuuos_repository_head_expected_at_branch_base": (
            "e958491505e21d47b2f29d10b29f206ff1a84c8d"
        ),
        "lean_lsp_mcp": {
            "package_version": EXPECTED_SERVER_VERSION,
            "upstream_main_sha": EXPECTED_UPSTREAM_SHA,
            "version_output_digest": sha(version_output),
        },
        "kuuos_pins": pins,
        "probe": probe_result,
        "boundary": {
            "full_strict_lean_rerun_required": False,
            "representative_existing_module_only": True,
            "mcp_probe_write_tools_enabled": False,
            "external_lean_search_tools_enabled_during_probe": False,
            "registry_entry_is_authority": False,
            "compatibility_receipt_is_theorem_authority": False,
            "source_authority_transferred": False,
        },
    }

    receipt_path = pathlib.Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
