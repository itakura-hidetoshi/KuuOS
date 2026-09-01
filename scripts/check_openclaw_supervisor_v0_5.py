#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime" / "kuuos_openclaw_supervisor_v0_5.py"
TEST = ROOT / "tests" / "test_openclaw_supervisor_v0_5.py"
DOC = ROOT / "docs" / "KUUOS_OPENCLAW_SUPERVISOR_v0_5.md"
MANIFEST = ROOT / "manifests" / "kuuos_openclaw_supervisor_v0_5.json"
FORMAL = ROOT / "formal" / "KUOS" / "ObserveOS" / "OpenClawSupervisorV0_5.lean"
REGISTRY = ROOT / "ci" / "check_registry.d" / "openclaw_supervisor_v0_5.json"
PLUGIN_MANIFEST = ROOT / "integrations" / "openclaw" / "openclaw.plugin.json"
V01 = ROOT / "runtime" / "kuuos_openclaw_control_server_v0_1.py"
V03 = ROOT / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3.py"
V04 = ROOT / "integrations" / "openclaw" / "event-stream" / "subscriber.mjs"

REQUIRED = [RUNTIME, TEST, DOC, MANIFEST, FORMAL, REGISTRY, PLUGIN_MANIFEST, V01, V03, V04]


def fail(message: str) -> None:
    raise SystemExit(message)


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        fail(f"{label}: missing required tokens: {missing}")


for path in REQUIRED:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")

for path in (RUNTIME, TEST):
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as error:
        fail(f"python syntax error in {path.relative_to(ROOT)}: {error}")

try:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    plugin_manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
except json.JSONDecodeError as error:
    fail(f"JSON parse failure: {error}")

if manifest.get("version") != "kuuos_openclaw_supervisor_v0_5":
    fail("supervisor manifest version mismatch")
if manifest.get("required_layers") != ["v0.1-control", "v0.4-live-events", "v0.3-audit-reconciliation"]:
    fail("supervisor required layer order mismatch")
if manifest.get("supervisor_scope") != "local_gateway_only":
    fail("v0.5 must remain local-Gateway-only")

authority = manifest.get("authority", {})
for key in (
    "world_commit",
    "truth_promotion",
    "observe_commit",
    "verification_result",
    "plan_completion",
    "automatic_plan_completion",
    "rollback_proof",
    "automatic_rollback",
    "memory_overwrite",
):
    if authority.get(key) is not False:
        fail(f"supervisor authority must keep {key}=false")

activation = plugin_manifest.get("activation", {})
if "hook" not in activation.get("onCapabilities", []):
    fail("kuuos-control hook-only plugin must declare activation.onCapabilities hook")

checks = registry.get("checks")
if not isinstance(checks, dict) or "openclaw-supervisor-v05" not in checks:
    fail("CI registry check openclaw-supervisor-v05 missing")

runtime_text = RUNTIME.read_text(encoding="utf-8")
require_tokens(
    runtime_text,
    [
        'PLUGIN_ID = "kuuos-control"',
        '"plugins", "inspect", PLUGIN_ID, "--runtime", "--json"',
        '"before_tool_call"',
        '"after_tool_call"',
        '"gateway", "status", "--deep", "--require-rpc", "--json"',
        '"audit.activity.list"',
        '"plugins", "install"',
        '"--link"',
        '"--approve-install"',
        '"gateway", "restart", "--safe", "--json"',
        "openclaw_supervisor_closed_loop_ready",
        "openclaw_supervisor_required_component_failure",
        "openclaw_gateway_connection_sequence_gap",
        "openclaw_gateway_run_sequence_gap",
        '"worldCommitAuthority": False',
        '"truthPromotionAuthority": False',
        '"automaticPlanCompletion": False',
        '"automaticRollback": False',
        "v0.5 closed-loop supervisor is local-Gateway only",
        "KUUOS_OPENCLAW_TOKEN",
    ],
    "runtime",
)

doc_text = DOC.read_text(encoding="utf-8")
require_tokens(
    doc_text,
    [
        "control healthy + fresh Gateway hello + initial audit reconciliation",
        "closed-loop ready != WORLD truth",
        "required component failure -> supervisor stops policy service",
        "plugins inspect kuuos-control --runtime --json",
        "openclaw plugins install --link",
        "openclaw gateway restart --safe",
        "activation.onCapabilities = [\"hook\"]",
        "local-Gateway only",
        "actual machine installation is not performed by repository CI",
    ],
    "documentation",
)

formal_text = FORMAL.read_text(encoding="utf-8")
require_tokens(
    formal_text,
    [
        "OpenClawSupervisorReadinessBoundary",
        "OpenClawSupervisorAuthorityBoundary",
        "OpenClawSupervisorFailureBoundary",
        "OpenClawSupervisorInstallBoundary",
        "openclaw_supervisor_readiness_requires_all_layers",
        "openclaw_supervisor_ready_grants_no_new_authority",
        "openclaw_supervisor_component_failure_revokes_ready_claim",
        "openclaw_supervisor_install_requires_explicit_approval",
    ],
    "formal boundary",
)

completed = subprocess.run(
    [sys.executable, str(TEST)],
    cwd=ROOT,
    check=False,
    capture_output=True,
    text=True,
)
if completed.returncode != 0:
    sys.stderr.write(completed.stdout)
    sys.stderr.write(completed.stderr)
    fail("OpenClaw supervisor v0.5 unit tests failed")

print("kuuos_openclaw_supervisor_v0_5: OK")
