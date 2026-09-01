#!/usr/bin/env python3
"""Fail-closed operational supervisor for the KuuOS ↔ OpenClaw control loop v0.5.

The supervisor composes existing repository layers without granting any new
WORLD, truth, verification, PlanOS completion, rollback, or memory authority:

* v0.1 KuuOS loopback policy service,
* v0.4 low-latency Gateway event subscriber,
* v0.3 bounded audit.activity.list reconciliation.

A closed-loop-ready receipt is emitted only after the policy service is healthy,
a *fresh* v0.4 hello record is observed, and an initial v0.3 audit sync succeeds.
If a required runtime component later fails, the supervisor stops the policy
service as well.  With the native plugin's default failClosed=true behavior,
policy unavailability therefore blocks subsequently observed OpenClaw tool calls
instead of silently continuing under a false KuuOS-ready claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

VERSION = "kuuos_openclaw_supervisor_v0_5"
PLUGIN_ID = "kuuos-control"
EXPECTED_OPENCLAW_GATEWAY_PACKAGES = {
    "@openclaw/gateway-client": "2026.8.1",
    "@openclaw/gateway-protocol": "2026.8.1",
}
RECONCILE_TRIGGER_TYPES = {
    "openclaw_gateway_connection_sequence_gap",
    "openclaw_gateway_run_sequence_gap",
    "openclaw_gateway_connection_closed",
    "openclaw_gateway_connect_error",
    "openclaw_gateway_reconnect_paused",
    "openclaw_gateway_subscription_error",
    "openclaw_gateway_event_projection_error",
}


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def authority_semantics() -> dict[str, bool]:
    return {
        "worldCommitAuthority": False,
        "truthPromotionAuthority": False,
        "observeCommitAuthority": False,
        "verificationAuthority": False,
        "planCompletionAuthority": False,
        "automaticPlanCompletion": False,
        "rollbackProofAuthority": False,
        "automaticRollback": False,
        "memoryOverwriteAuthority": False,
    }


def is_loopback_host(host: str | None) -> bool:
    return host in {"127.0.0.1", "localhost", "::1"}


def ensure_loopback_gateway_url(raw: str) -> str:
    parsed = urlparse(raw)
    if parsed.scheme not in {"ws", "wss"}:
        raise RuntimeError("v0.5 Gateway URL must use ws:// or wss://")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise RuntimeError("v0.5 Gateway URL must not contain credentials, query parameters, or fragments")
    if not is_loopback_host(parsed.hostname):
        raise RuntimeError(
            "v0.5 closed-loop supervisor is local-Gateway only; remote Gateway supervision remains a separate frontier"
        )
    return raw


def recursive_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from recursive_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from recursive_strings(item)


class SupervisorLedger:
    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        self.path = data_dir / "supervisor-receipts.jsonl"
        self._lock = threading.Lock()

    def append(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        now_ns = time.time_ns()
        record: dict[str, Any] = {
            "version": VERSION,
            "recordType": kind,
            "recordedAtUnixNs": now_ns,
            "payload": payload,
            "semantics": authority_semantics(),
        }
        record["recordDigest"] = digest(record)
        record["recordId"] = f"kuuos-oc-supervisor-{now_ns}-{record['recordDigest'][:16]}"
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        return record


@dataclass(frozen=True)
class Paths:
    repo_root: Path
    data_dir: Path
    control_server: Path
    audit_ingest: Path
    event_subscriber: Path
    event_package: Path
    plugin_dir: Path
    live_ledger: Path

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "Paths":
        repo_root = Path(args.repo_root).expanduser().resolve()
        data_dir = Path(args.data_dir).expanduser().resolve()
        return cls(
            repo_root=repo_root,
            data_dir=data_dir,
            control_server=repo_root / "runtime" / "kuuos_openclaw_control_server_v0_1.py",
            audit_ingest=repo_root / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3.py",
            event_subscriber=repo_root / "integrations" / "openclaw" / "event-stream" / "subscriber.mjs",
            event_package=repo_root / "integrations" / "openclaw" / "event-stream" / "package.json",
            plugin_dir=repo_root / "integrations" / "openclaw",
            live_ledger=data_dir / "gateway-event-hints.jsonl",
        )

    def require_repository_files(self) -> None:
        required = [
            self.control_server,
            self.audit_ingest,
            self.event_subscriber,
            self.event_package,
            self.plugin_dir / "openclaw.plugin.json",
            self.plugin_dir / "index.mjs",
        ]
        missing = [str(path) for path in required if not path.is_file()]
        if missing:
            raise RuntimeError(f"KuuOS OpenClaw repository files missing: {missing}")


@dataclass(frozen=True)
class CommandResult:
    command_name: str
    returncode: int
    stdout: str
    stderr: str


def run_command(argv: list[str], *, cwd: Path, timeout: float, name: str) -> CommandResult:
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f"{name} failed to execute: {error}") from error
    return CommandResult(name, completed.returncode, completed.stdout, completed.stderr)


def require_success(result: CommandResult) -> CommandResult:
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"{result.command_name} failed with exit {result.returncode}: {detail[:1200]}")
    return result


def parse_json_stdout(result: CommandResult) -> Any:
    require_success(result)
    raw = result.stdout.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{result.command_name} returned non-JSON output: {raw[:1200]}") from error


def inspect_event_dependencies(paths: Paths) -> dict[str, Any]:
    package = json.loads(paths.event_package.read_text(encoding="utf-8"))
    declared = package.get("dependencies")
    if declared != EXPECTED_OPENCLAW_GATEWAY_PACKAGES:
        raise RuntimeError(
            "v0.4 event-stream package dependencies do not match the v0.5 exact OpenClaw package contract"
        )

    installed: dict[str, str] = {}
    missing: list[str] = []
    for package_name, expected_version in EXPECTED_OPENCLAW_GATEWAY_PACKAGES.items():
        package_path = paths.event_subscriber.parent / "node_modules" / package_name / "package.json"
        if not package_path.is_file():
            missing.append(package_name)
            continue
        value = json.loads(package_path.read_text(encoding="utf-8"))
        version = value.get("version")
        if version != expected_version:
            raise RuntimeError(
                f"installed {package_name} version {version!r} != required {expected_version!r}"
            )
        installed[package_name] = str(version)
    return {"declared": declared, "installed": installed, "missing": missing}


def openclaw_json(
    args: argparse.Namespace,
    paths: Paths,
    suffix: list[str],
    *,
    timeout: float = 30.0,
    name: str,
) -> Any:
    result = run_command([args.openclaw_bin, *suffix], cwd=paths.repo_root, timeout=timeout, name=name)
    return parse_json_stdout(result)


def plugin_inventory_contains(value: Any, plugin_id: str) -> bool:
    if not isinstance(value, dict):
        return False
    candidates = value.get("plugins")
    if not isinstance(candidates, list):
        candidates = value.get("entries")
    if not isinstance(candidates, list):
        return False
    for candidate in candidates:
        if isinstance(candidate, dict) and candidate.get("id") == plugin_id:
            return True
    return False


def doctor(args: argparse.Namespace, paths: Paths, ledger: SupervisorLedger) -> dict[str, Any]:
    paths.require_repository_files()
    ensure_loopback_gateway_url(args.gateway_url)

    version = require_success(
        run_command([args.openclaw_bin, "--version"], cwd=paths.repo_root, timeout=15.0, name="openclaw --version")
    ).stdout.strip()

    inventory = openclaw_json(
        args,
        paths,
        ["plugins", "list", "--json"],
        name="openclaw plugins list --json",
    )
    if not plugin_inventory_contains(inventory, PLUGIN_ID):
        raise RuntimeError(
            "kuuos-control is not in the OpenClaw plugin inventory; run v0.5 install-plugin with explicit approval"
        )

    runtime_inspect = openclaw_json(
        args,
        paths,
        ["plugins", "inspect", PLUGIN_ID, "--runtime", "--json"],
        name="openclaw plugins inspect kuuos-control --runtime --json",
    )
    runtime_strings = set(recursive_strings(runtime_inspect))
    for hook_name in ("before_tool_call", "after_tool_call"):
        if hook_name not in runtime_strings:
            raise RuntimeError(f"OpenClaw runtime inspection does not show required hook {hook_name!r}")

    _gateway_status = openclaw_json(
        args,
        paths,
        ["gateway", "status", "--deep", "--require-rpc", "--json"],
        timeout=45.0,
        name="openclaw gateway status --deep --require-rpc --json",
    )

    audit_probe = openclaw_json(
        args,
        paths,
        [
            "gateway",
            "call",
            "audit.activity.list",
            "--params",
            '{"limit":1}',
            "--timeout",
            str(args.rpc_timeout_ms),
            "--json",
            "--no-color",
        ],
        timeout=max(30.0, args.rpc_timeout_ms / 1000 + 10.0),
        name="OpenClaw audit.activity.list doctor probe",
    )
    if not isinstance(audit_probe, dict) or not isinstance(audit_probe.get("events"), list):
        raise RuntimeError("OpenClaw audit.activity.list doctor probe returned an unexpected payload")

    dependencies = inspect_event_dependencies(paths)
    if dependencies["missing"]:
        raise RuntimeError(
            "OpenClaw event-stream dependencies are not installed: "
            + ", ".join(dependencies["missing"])
            + "; run npm install in integrations/openclaw/event-stream"
        )

    receipt = ledger.append(
        "openclaw_supervisor_doctor_success",
        {
            "openclawVersion": version,
            "pluginId": PLUGIN_ID,
            "requiredHooks": ["before_tool_call", "after_tool_call"],
            "gatewayRpcHealthy": True,
            "auditActivityReadable": True,
            "eventDependencies": dependencies["installed"],
            "pluginRuntimeInspectionIsWorldTruth": False,
            "gatewayHealthIsPlanCompletion": False,
        },
    )
    return {
        "ok": True,
        "version": VERSION,
        "openclawVersion": version,
        "pluginId": PLUGIN_ID,
        "eventDependencies": dependencies["installed"],
        "receiptId": receipt["recordId"],
        **authority_semantics(),
    }


def install_plugin(args: argparse.Namespace, paths: Paths, ledger: SupervisorLedger) -> dict[str, Any]:
    if not args.approve_install:
        raise RuntimeError("install-plugin mutates OpenClaw plugin/config state and requires --approve-install")
    paths.require_repository_files()

    manifest = json.loads((paths.plugin_dir / "openclaw.plugin.json").read_text(encoding="utf-8"))
    activation = manifest.get("activation")
    if not isinstance(activation, dict) or "hook" not in activation.get("onCapabilities", []):
        raise RuntimeError("kuuos-control manifest lacks activation.onCapabilities hook startup intent")

    require_success(
        run_command(
            [args.openclaw_bin, "plugins", "validate", "--entry", str(paths.plugin_dir), "--json"],
            cwd=paths.repo_root,
            timeout=60.0,
            name="openclaw plugins validate kuuos-control",
        )
    )
    require_success(
        run_command(
            [
                args.openclaw_bin,
                "plugins",
                "install",
                "--link",
                str(paths.plugin_dir),
                "--force",
            ],
            cwd=paths.repo_root,
            timeout=120.0,
            name="openclaw plugins install --link kuuos-control",
        )
    )
    require_success(
        run_command(
            [args.openclaw_bin, "plugins", "enable", PLUGIN_ID],
            cwd=paths.repo_root,
            timeout=60.0,
            name="openclaw plugins enable kuuos-control",
        )
    )

    restart_performed = False
    if args.approve_restart:
        require_success(
            run_command(
                [args.openclaw_bin, "gateway", "restart", "--safe", "--json"],
                cwd=paths.repo_root,
                timeout=330.0,
                name="openclaw gateway restart --safe",
            )
        )
        restart_performed = True

    receipt = ledger.append(
        "openclaw_supervisor_plugin_install",
        {
            "pluginId": PLUGIN_ID,
            "linkedSourceDigest": digest(str(paths.plugin_dir)),
            "explicitInstallApproval": True,
            "explicitRestartApproval": bool(args.approve_restart),
            "restartPerformed": restart_performed,
            "openclawConfigMutation": True,
            "worldCommit": False,
            "truthPromotion": False,
        },
    )
    return {
        "ok": True,
        "version": VERSION,
        "pluginId": PLUGIN_ID,
        "restartPerformed": restart_performed,
        "next": (
            "Run supervisor doctor. If restartPerformed=false and the live Gateway did not auto-reload, "
            "restart the serving Gateway before relying on the hooks."
        ),
        "receiptId": receipt["recordId"],
        **authority_semantics(),
    }


def control_command(args: argparse.Namespace, paths: Paths) -> list[str]:
    return [
        args.python_bin,
        str(paths.control_server),
        "--host",
        "127.0.0.1",
        "--port",
        str(args.control_port),
        "--data-dir",
        str(paths.data_dir),
        "--policy-mode",
        args.policy_mode,
    ]


def event_command(args: argparse.Namespace, paths: Paths) -> list[str]:
    command = [
        args.node_bin,
        str(paths.event_subscriber),
        "--gateway-url",
        ensure_loopback_gateway_url(args.gateway_url),
        "--data-dir",
        str(paths.data_dir),
        "--session-limit",
        str(args.session_limit),
    ]
    for key in args.session_key:
        command.extend(["--session-key", key])
    return command


def audit_command(args: argparse.Namespace, paths: Paths) -> list[str]:
    return [
        args.python_bin,
        str(paths.audit_ingest),
        "--openclaw-bin",
        args.openclaw_bin,
        "--data-dir",
        str(paths.data_dir),
        "--rpc-timeout-ms",
        str(args.rpc_timeout_ms),
        "sync",
        "--limit",
        str(args.audit_limit),
        "--max-pages",
        str(args.audit_max_pages),
    ]


def wait_control_health(args: argparse.Namespace, process: subprocess.Popen[str], timeout: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    url = f"http://127.0.0.1:{args.control_port}/health"
    last_error = "not attempted"
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"KuuOS control server exited before health readiness: {process.returncode}")
        try:
            with urllib.request.urlopen(url, timeout=1.5) as response:
                value = json.loads(response.read().decode("utf-8"))
            if isinstance(value, dict) and value.get("status") == "ok":
                return value
            last_error = f"unexpected health payload: {value!r}"
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as error:
            last_error = str(error)
        time.sleep(0.25)
    raise RuntimeError(f"KuuOS control server health readiness timeout: {last_error}")


def read_new_jsonl(path: Path, start_offset: int) -> tuple[int, list[dict[str, Any]]]:
    if not path.exists():
        return start_offset, []
    with path.open("r", encoding="utf-8") as handle:
        handle.seek(start_offset)
        records: list[dict[str, Any]] = []
        while True:
            line = handle.readline()
            if not line:
                break
            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeError(f"corrupt v0.4 live hint ledger: {error}") from error
            if not isinstance(value, dict):
                raise RuntimeError("invalid non-object v0.4 live hint ledger record")
            records.append(value)
        return handle.tell(), records


def wait_fresh_live_hello(
    paths: Paths,
    process: subprocess.Popen[str],
    start_offset: int,
    timeout: float,
) -> tuple[int, dict[str, Any]]:
    deadline = time.monotonic() + timeout
    offset = start_offset
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"OpenClaw v0.4 event subscriber exited before hello readiness: {process.returncode}")
        offset, records = read_new_jsonl(paths.live_ledger, offset)
        for record in records:
            if record.get("recordType") == "openclaw_gateway_connection_hello":
                return offset, record
        time.sleep(0.25)
    raise RuntimeError(
        "OpenClaw v0.4 event subscriber did not produce a fresh hello; device pairing or Gateway auth may be required"
    )


def run_audit_once(args: argparse.Namespace, paths: Paths) -> dict[str, Any]:
    result = run_command(
        audit_command(args, paths),
        cwd=paths.repo_root,
        timeout=max(60.0, args.rpc_timeout_ms / 1000 + 30.0),
        name="KuuOS OpenClaw v0.3 audit reconciliation",
    )
    value = parse_json_stdout(result)
    if not isinstance(value, dict):
        raise RuntimeError("v0.3 audit reconciliation returned a non-object payload")
    if value.get("resumeRequired") is True:
        raise RuntimeError(
            "initial/periodic v0.3 audit reconciliation exhausted its page budget; rerun or raise --audit-max-pages"
        )
    return value


def terminate_process(process: subprocess.Popen[str] | None, *, timeout: float = 8.0) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5.0)


def run_supervisor(args: argparse.Namespace, paths: Paths, ledger: SupervisorLedger) -> int:
    paths.require_repository_files()
    ensure_loopback_gateway_url(args.gateway_url)
    if os.environ.get("KUUOS_OPENCLAW_TOKEN"):
        raise RuntimeError(
            "v0.5 run refuses KUUOS_OPENCLAW_TOKEN because the supervisor cannot prove the installed plugin has the matching secret; "
            "use loopback without a token or configure a matched secret deliberately outside this supervisor"
        )

    doctor(args, paths, ledger)
    paths.data_dir.mkdir(parents=True, exist_ok=True)
    live_start_offset = paths.live_ledger.stat().st_size if paths.live_ledger.exists() else 0

    control: subprocess.Popen[str] | None = None
    live: subprocess.Popen[str] | None = None
    stopping = False
    stop_event = threading.Event()
    reconcile_trigger = threading.Event()
    live_watch_offset = live_start_offset
    thread_errors: list[BaseException] = []
    thread_error_lock = threading.Lock()

    def record_thread_error(error: BaseException) -> None:
        with thread_error_lock:
            if not thread_errors:
                thread_errors.append(error)
        stop_event.set()

    def audit_loop() -> None:
        try:
            while not stop_event.wait(args.audit_interval_seconds):
                reconcile_trigger.clear()
                result = run_audit_once(args, paths)
                ledger.append(
                    "openclaw_supervisor_periodic_audit_reconciled",
                    {
                        "queryDigest": result.get("queryDigest"),
                        "inserted": result.get("inserted"),
                        "fetched": result.get("fetched"),
                        "completedWindow": result.get("completedWindow"),
                        "triggeredByGapOrLifecycleHint": False,
                        "worldCommit": False,
                    },
                )
        except BaseException as error:  # fail-closed supervision boundary
            record_thread_error(error)

    def live_ledger_watch() -> None:
        nonlocal live_watch_offset
        try:
            while not stop_event.wait(0.5):
                live_watch_offset, records = read_new_jsonl(paths.live_ledger, live_watch_offset)
                if any(record.get("recordType") in RECONCILE_TRIGGER_TYPES for record in records):
                    reconcile_trigger.set()
        except BaseException as error:
            record_thread_error(error)

    def triggered_reconcile_loop() -> None:
        last_run = 0.0
        try:
            while not stop_event.is_set():
                if not reconcile_trigger.wait(0.5):
                    continue
                reconcile_trigger.clear()
                delay = args.audit_min_trigger_interval_seconds - (time.monotonic() - last_run)
                if delay > 0 and stop_event.wait(delay):
                    return
                result = run_audit_once(args, paths)
                last_run = time.monotonic()
                ledger.append(
                    "openclaw_supervisor_triggered_audit_reconciled",
                    {
                        "queryDigest": result.get("queryDigest"),
                        "inserted": result.get("inserted"),
                        "fetched": result.get("fetched"),
                        "completedWindow": result.get("completedWindow"),
                        "triggeredByGapOrLifecycleHint": True,
                        "worldCommit": False,
                    },
                )
        except BaseException as error:
            record_thread_error(error)

    def request_stop(_signum: int, _frame: Any) -> None:
        stop_event.set()

    previous_sigint = signal.signal(signal.SIGINT, request_stop)
    previous_sigterm = signal.signal(signal.SIGTERM, request_stop)
    try:
        ledger.append(
            "openclaw_supervisor_starting",
            {
                "policyMode": args.policy_mode,
                "controlPort": args.control_port,
                "gatewayOriginDigest": digest(urlparse(args.gateway_url).netloc),
                "auditIntervalSeconds": args.audit_interval_seconds,
                "requiredComponents": ["v0.1-control", "v0.4-live-events", "v0.3-audit-reconciliation"],
                "closedLoopReady": False,
            },
        )

        control = subprocess.Popen(
            control_command(args, paths),
            cwd=paths.repo_root,
            text=True,
        )
        health = wait_control_health(args, control, args.ready_timeout_seconds)
        ledger.append(
            "openclaw_supervisor_control_ready",
            {
                "policyMode": health.get("policyMode"),
                "receiptPathDigest": digest(health.get("receiptPath")),
                "closedLoopReady": False,
            },
        )

        live = subprocess.Popen(
            event_command(args, paths),
            cwd=paths.repo_root,
            text=True,
        )
        live_watch_offset, hello = wait_fresh_live_hello(
            paths,
            live,
            live_start_offset,
            args.live_ready_timeout_seconds,
        )
        ledger.append(
            "openclaw_supervisor_live_ready",
            {
                "freshHelloRecordId": hello.get("recordId"),
                "closedLoopReady": False,
                "auditReconciliationRequired": True,
            },
        )

        initial_audit = run_audit_once(args, paths)
        ledger.append(
            "openclaw_supervisor_initial_audit_reconciled",
            {
                "queryDigest": initial_audit.get("queryDigest"),
                "inserted": initial_audit.get("inserted"),
                "fetched": initial_audit.get("fetched"),
                "completedWindow": initial_audit.get("completedWindow"),
                "closedLoopReady": False,
            },
        )

        ready = ledger.append(
            "openclaw_supervisor_closed_loop_ready",
            {
                "pluginRuntimeHooksInspected": True,
                "controlServiceHealthy": True,
                "freshGatewayHelloObserved": True,
                "initialAuditReconciliationComplete": True,
                "closedLoopReady": True,
                "closedLoopReadyIsWorldTruth": False,
                "closedLoopReadyIsPlanCompletion": False,
            },
        )
        print(json.dumps({
            "status": "ready",
            "version": VERSION,
            "receiptId": ready["recordId"],
            "controlUrl": f"http://127.0.0.1:{args.control_port}",
            **authority_semantics(),
        }, ensure_ascii=False, sort_keys=True))

        threads = [
            threading.Thread(target=audit_loop, name="kuuos-openclaw-audit-periodic", daemon=True),
            threading.Thread(target=live_ledger_watch, name="kuuos-openclaw-live-watch", daemon=True),
            threading.Thread(target=triggered_reconcile_loop, name="kuuos-openclaw-audit-triggered", daemon=True),
        ]
        for thread in threads:
            thread.start()

        while not stop_event.wait(0.5):
            if control.poll() is not None:
                raise RuntimeError(f"required v0.1 control service exited: {control.returncode}")
            if live.poll() is not None:
                raise RuntimeError(f"required v0.4 live event subscriber exited: {live.returncode}")
            with thread_error_lock:
                if thread_errors:
                    raise RuntimeError(f"required observation/reconciliation worker failed: {thread_errors[0]}")

        with thread_error_lock:
            if thread_errors:
                raise RuntimeError(f"required observation/reconciliation worker failed: {thread_errors[0]}")
        stopping = True
        return 0
    except BaseException as error:
        ledger.append(
            "openclaw_supervisor_required_component_failure",
            {
                "errorClass": type(error).__name__,
                "errorDigest": digest(str(error)),
                "closedLoopReady": False,
                "policyServiceWillBeStopped": True,
                "futureObservedToolCallsShouldFailClosedWhenPluginDefaultIsPreserved": True,
                "failureIsRollbackProof": False,
            },
        )
        if isinstance(error, KeyboardInterrupt):
            return 130
        raise
    finally:
        stop_event.set()
        terminate_process(live)
        terminate_process(control)
        ledger.append(
            "openclaw_supervisor_stopped",
            {
                "gracefulStopRequested": stopping,
                "closedLoopReady": False,
                "policyServiceStopped": True,
                "stopIsRollbackProof": False,
            },
        )
        signal.signal(signal.SIGINT, previous_sigint)
        signal.signal(signal.SIGTERM, previous_sigterm)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Operate the KuuOS ↔ OpenClaw closed-loop control plane v0.5.")
    default_repo = Path(__file__).resolve().parents[1]
    root.add_argument("--repo-root", default=str(default_repo))
    root.add_argument("--data-dir", default=os.environ.get("KUUOS_OPENCLAW_DATA_DIR", "~/.kuuos/openclaw"))
    root.add_argument("--openclaw-bin", default=os.environ.get("OPENCLAW_BIN", "openclaw"))
    root.add_argument("--python-bin", default=sys.executable)
    root.add_argument("--node-bin", default=os.environ.get("NODE_BIN", "node"))
    root.add_argument("--gateway-url", default=os.environ.get("OPENCLAW_GATEWAY_URL", "ws://127.0.0.1:18789"))
    root.add_argument("--rpc-timeout-ms", type=int, default=30000)

    sub = root.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Read-only proof checks for plugin runtime hooks, Gateway RPC, audit access, and exact JS deps.")

    install = sub.add_parser("install-plugin", help="Explicitly link and enable the local KuuOS plugin in OpenClaw.")
    install.add_argument("--approve-install", action="store_true")
    install.add_argument("--approve-restart", action="store_true")

    run = sub.add_parser("run", help="Run the required v0.1 + v0.4 + v0.3 closed loop under fail-closed supervision.")
    run.add_argument("--policy-mode", choices=("approval", "owner-strict", "observe"), default="approval")
    run.add_argument("--control-port", type=int, default=8765)
    run.add_argument("--session-key", action="append", default=[])
    run.add_argument("--session-limit", type=int, default=60)
    run.add_argument("--audit-limit", type=int, default=500)
    run.add_argument("--audit-max-pages", type=int, default=20)
    run.add_argument("--audit-interval-seconds", type=float, default=60.0)
    run.add_argument("--audit-min-trigger-interval-seconds", type=float, default=10.0)
    run.add_argument("--ready-timeout-seconds", type=float, default=15.0)
    run.add_argument("--live-ready-timeout-seconds", type=float, default=30.0)
    return root


def validate_args(args: argparse.Namespace) -> None:
    if args.rpc_timeout_ms <= 0:
        raise RuntimeError("--rpc-timeout-ms must be positive")
    if args.command == "run":
        if not 1 <= args.control_port <= 65535:
            raise RuntimeError("--control-port must be 1..65535")
        if not 1 <= args.session_limit <= 200:
            raise RuntimeError("--session-limit must be 1..200")
        if not 1 <= args.audit_limit <= 500:
            raise RuntimeError("--audit-limit must be 1..500")
        if not 1 <= args.audit_max_pages <= 200:
            raise RuntimeError("--audit-max-pages must be 1..200")
        for name in (
            "audit_interval_seconds",
            "audit_min_trigger_interval_seconds",
            "ready_timeout_seconds",
            "live_ready_timeout_seconds",
        ):
            if getattr(args, name) <= 0:
                raise RuntimeError(f"--{name.replace('_', '-')} must be positive")


def main() -> int:
    args = parser().parse_args()
    try:
        validate_args(args)
        paths = Paths.from_args(args)
        ledger = SupervisorLedger(paths.data_dir)
        if args.command == "doctor":
            result = doctor(args, paths, ledger)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
            return 0
        if args.command == "install-plugin":
            result = install_plugin(args, paths, ledger)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
            return 0
        if args.command == "run":
            return run_supervisor(args, paths, ledger)
        raise RuntimeError(f"unknown command {args.command!r}")
    except (RuntimeError, OSError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
