#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
import pathlib
import re
import selectors
import subprocess
import threading
import time
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "2025-06-18"
PLAYWRIGHT_VERSION = "0.0.82"
PLAYWRIGHT_UPSTREAM_SHA = "e87bb897e15a6f2af402afb0f10b45eced9e1f9b"
CHROME_DEVTOOLS_VERSION = "1.10.1"
CHROME_DEVTOOLS_UPSTREAM_SHA = "ae0aaef884c41445d83f86f099ef211f4584b791"

FIXTURE_MARKER = "KUUOS_BROWSER_MCP_FIXTURE_V7_21"
CONSOLE_MARKER = "KUUOS_BROWSER_FIXTURE_READY"

PLAYWRIGHT_REQUIRED = {"browser_navigate", "browser_snapshot"}
CHROME_REQUIRED = {
    "new_page",
    "list_pages",
    "take_snapshot",
    "list_console_messages",
}


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


class FixtureHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{FIXTURE_MARKER}</title>
</head>
<body>
  <main>
    <h1>{FIXTURE_MARKER}</h1>
    <p id="status">browser-mcp-ready</p>
    <button id="probe-button">Probe action</button>
  </main>
  <script>
    console.log("{CONSOLE_MARKER}");
  </script>
</body>
</html>
""".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


class MCPClient:
    def __init__(
        self,
        command: Sequence[str],
        *,
        cwd: pathlib.Path,
        env: Mapping[str, str] | None = None,
        timeout_seconds: float = 180.0,
    ) -> None:
        merged = os.environ.copy()
        if env:
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
                    raise TimeoutError(f"mcp_timeout:{method}")
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
                        "mcp_server_closed:"
                        + str(self.process.poll())
                        + ":"
                        + stderr[-2000:]
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
                            "mcp_rpc_error:"
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

    def initialize(self, name: str) -> dict[str, Any]:
        response = self.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": name, "version": "7.21"},
            },
        )
        self.notify("notifications/initialized")
        return response

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
            + json.dumps(result, ensure_ascii=False)[:2600]
        )
    return response


def textual_payload(response: Mapping[str, Any]) -> str:
    result = response.get("result", {})
    if not isinstance(result, Mapping):
        return ""
    parts: list[str] = []
    content = result.get("content", [])
    if isinstance(content, list):
        for item in content:
            if isinstance(item, Mapping) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
    structured = result.get("structuredContent")
    if structured is not None:
        parts.append(json.dumps(structured, ensure_ascii=False))
    return "\n".join(parts)


def _find_page_id(value: Any, fixture_url: str) -> int | None:
    if isinstance(value, Mapping):
        url = str(value.get("url", ""))
        for key in ("pageId", "id"):
            candidate = value.get(key)
            if fixture_url in url and isinstance(candidate, int):
                return candidate
        for child in value.values():
            found = _find_page_id(child, fixture_url)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find_page_id(child, fixture_url)
            if found is not None:
                return found
    return None


def extract_page_id(response: Mapping[str, Any], fixture_url: str) -> int | None:
    result = response.get("result", {})
    found = _find_page_id(result, fixture_url)
    if found is not None:
        return found
    text = textual_payload(response)
    escaped = re.escape(fixture_url)
    patterns = [
        rf"(?:pageId|page_id)\s*[:=]\s*(\d+).*?{escaped}",
        rf"(\d+)\s*:\s*{escaped}",
        rf"{escaped}.*?(?:pageId|page_id)\s*[:=]\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return int(match.group(1))
    return None


def probe_playwright(root: pathlib.Path, fixture_url: str) -> dict[str, Any]:
    origin = fixture_url.rsplit("/", 1)[0]
    command = [
        "npx",
        "-y",
        f"@playwright/mcp@{PLAYWRIGHT_VERSION}",
        "--browser",
        "chrome",
        "--headless",
        "--isolated",
        "--no-webmcp",
        "--block-service-workers",
        "--allowed-origins",
        origin,
    ]
    client = MCPClient(command, cwd=root)
    try:
        initialized = client.initialize("KuuOS Playwright MCP Compatibility Probe")
        listed = tool_map(client.request("tools/list"))
        missing = sorted(PLAYWRIGHT_REQUIRED.difference(listed))
        if missing:
            raise RuntimeError(
                "playwright_required_tools_missing:" + ",".join(missing)
            )

        navigation = call_tool(
            client,
            "browser_navigate",
            {"url": fixture_url},
        )
        snapshot = call_tool(client, "browser_snapshot", {})
        snapshot_text = textual_payload(snapshot)
        if FIXTURE_MARKER not in snapshot_text:
            raise RuntimeError("playwright_snapshot_marker_missing")

        init_result = initialized.get("result", {})
        return {
            "protocol_version": (
                str(init_result.get("protocolVersion", ""))
                if isinstance(init_result, Mapping)
                else ""
            ),
            "listed_tool_count": len(listed),
            "listed_tools_digest": digest(sorted(listed)),
            "required_tools_present": True,
            "navigation_result_digest": digest(navigation.get("result", {})),
            "snapshot_result_digest": digest(snapshot.get("result", {})),
            "fixture_marker_observed": True,
            "fixture_origin_digest": digest(origin),
            "headless": True,
            "isolated_profile": True,
            "external_navigation_performed": False,
        }
    finally:
        client.close()


def probe_chrome_devtools(
    root: pathlib.Path,
    fixture_url: str,
) -> dict[str, Any]:
    command = [
        "npx",
        "-y",
        f"chrome-devtools-mcp@{CHROME_DEVTOOLS_VERSION}",
        "--headless=true",
        "--isolated=true",
        "--usage-statistics=false",
        "--performance-crux=false",
    ]
    client = MCPClient(
        command,
        cwd=root,
        env={
            "CI": "true",
            "CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS": "1",
            "CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS": "1",
        },
    )
    try:
        initialized = client.initialize(
            "KuuOS Chrome DevTools MCP Compatibility Probe"
        )
        listed = tool_map(client.request("tools/list"))
        missing = sorted(CHROME_REQUIRED.difference(listed))
        if missing:
            raise RuntimeError(
                "chrome_required_tools_missing:" + ",".join(missing)
            )

        created = call_tool(
            client,
            "new_page",
            {"url": fixture_url, "timeout": 15000},
        )
        page_id = extract_page_id(created, fixture_url)
        pages = call_tool(client, "list_pages", {})
        if page_id is None:
            page_id = extract_page_id(pages, fixture_url)
        if page_id is None:
            raise RuntimeError("chrome_fixture_page_id_missing")

        snapshot = call_tool(
            client,
            "take_snapshot",
            {"pageId": page_id, "verbose": False},
        )
        snapshot_text = textual_payload(snapshot)
        if FIXTURE_MARKER not in snapshot_text:
            raise RuntimeError("chrome_snapshot_marker_missing")

        console = call_tool(
            client,
            "list_console_messages",
            {"pageId": page_id},
        )
        console_text = textual_payload(console)
        if CONSOLE_MARKER not in console_text:
            raise RuntimeError("chrome_console_marker_missing")

        init_result = initialized.get("result", {})
        return {
            "protocol_version": (
                str(init_result.get("protocolVersion", ""))
                if isinstance(init_result, Mapping)
                else ""
            ),
            "listed_tool_count": len(listed),
            "listed_tools_digest": digest(sorted(listed)),
            "required_tools_present": True,
            "new_page_result_digest": digest(created.get("result", {})),
            "list_pages_result_digest": digest(pages.get("result", {})),
            "snapshot_result_digest": digest(snapshot.get("result", {})),
            "console_result_digest": digest(console.get("result", {})),
            "fixture_marker_observed": True,
            "console_marker_observed": True,
            "page_id_digest": digest(page_id),
            "headless": True,
            "isolated_profile": True,
            "usage_statistics_disabled": True,
            "performance_crux_disabled": True,
            "external_navigation_performed": False,
        }
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument(
        "--receipt",
        default="browser_mcp_compatibility_receipt_v7_21.json",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.repository_root).resolve()
    if not (root / ".git").exists():
        raise RuntimeError("kuuos_repository_root_invalid")

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    fixture_url = f"http://127.0.0.1:{server.server_port}/fixture"

    try:
        playwright = probe_playwright(root, fixture_url)
        chrome = probe_chrome_devtools(root, fixture_url)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    receipt = {
        "version": "kuuos_browser_mcp_compatibility_receipt_v7_21",
        "status": "KUUOS_BROWSER_MCP_COMPATIBILITY_VERIFIED",
        "playwright": {
            "package_version": PLAYWRIGHT_VERSION,
            "upstream_main_sha": PLAYWRIGHT_UPSTREAM_SHA,
            "probe": playwright,
        },
        "chrome_devtools": {
            "package_version": CHROME_DEVTOOLS_VERSION,
            "upstream_main_sha": CHROME_DEVTOOLS_UPSTREAM_SHA,
            "probe": chrome,
        },
        "shared_fixture": {
            "host": "127.0.0.1",
            "path": "/fixture",
            "fixture_marker_digest": digest(FIXTURE_MARKER),
            "console_marker_digest": digest(CONSOLE_MARKER),
            "external_network_target": False,
        },
        "boundary": {
            "playwright_and_chrome_are_same_presentation": False,
            "playwright_role": "functional_browser_verification",
            "chrome_devtools_role": "console_network_performance_diagnostics",
            "compatibility_receipt_is_browser_effect_authority": False,
            "browser_effects_were_localhost_only": True,
            "persistent_browser_profile_used": False,
            "usage_statistics_enabled": False,
            "crux_lookup_enabled": False,
            "source_authority_transferred": False,
        },
    }

    receipt_path = pathlib.Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
