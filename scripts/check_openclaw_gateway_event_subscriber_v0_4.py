#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "integrations" / "openclaw" / "event-stream"
PACKAGE = BASE / "package.json"
PROJECTION = BASE / "projection.mjs"
SUBSCRIBER = BASE / "subscriber.mjs"
TEST = BASE / "test_projection.mjs"
DOC = ROOT / "docs" / "KUUOS_OPENCLAW_GATEWAY_EVENT_SUBSCRIBER_v0_4.md"
MANIFEST = ROOT / "manifests" / "kuuos_openclaw_gateway_event_subscriber_v0_4.json"
FORMAL = ROOT / "formal" / "KUOS" / "ObserveOS" / "OpenClawGatewayEventHintV0_4.lean"
REGISTRY = ROOT / "ci" / "check_registry.d" / "openclaw_gateway_event_v0_4.json"
AUDIT = ROOT / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3.py"

REQUIRED = [PACKAGE, PROJECTION, SUBSCRIBER, TEST, DOC, MANIFEST, FORMAL, REGISTRY, AUDIT]


def fail(message: str) -> None:
    raise SystemExit(message)


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        fail(f"{label}: missing required tokens: {missing}")


for path in REQUIRED:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")

try:
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
except json.JSONDecodeError as error:
    fail(f"JSON parse failure: {error}")

expected_packages = {
    "@openclaw/gateway-client": "2026.8.1",
    "@openclaw/gateway-protocol": "2026.8.1",
}
if package.get("dependencies") != expected_packages:
    fail("OpenClaw Gateway package dependencies must be exact-pinned to 2026.8.1")
if package.get("engines", {}).get("node") != ">=22.19.0":
    fail("Node engine floor mismatch")
if manifest.get("version") != "kuuos_openclaw_gateway_event_subscriber_v0_4":
    fail("manifest version mismatch")
if manifest.get("openclaw_packages", {}).get("wire_protocol") != 4:
    fail("manifest wire protocol must be 4")
if manifest.get("gateway_scopes") != ["operator.read"]:
    fail("v0.4 must remain operator.read only")

authority = manifest.get("authority", {})
for key in (
    "durable_history",
    "observe_commit",
    "verification_result",
    "world_commit",
    "truth_promotion",
    "plan_completion",
    "automatic_plan_completion",
    "rollback_proof",
    "automatic_rollback",
    "memory_overwrite",
    "silence_proves_non_occurrence",
):
    if authority.get(key) is not False:
        fail(f"manifest authority must keep {key}=false")

checks = registry.get("checks")
if not isinstance(checks, dict) or "openclaw-gateway-event-v04" not in checks:
    fail("CI registry check openclaw-gateway-event-v04 missing")

subscriber_text = SUBSCRIBER.read_text(encoding="utf-8")
require_tokens(
    subscriber_text,
    [
        "GatewayClient",
        "GATEWAY_CLIENT_CAPS.SESSION_SCOPED_EVENTS",
        "GATEWAY_CLIENT_CAPS.TOOL_EVENTS",
        'scopes: ["operator.read"]',
        "minProtocol: PROTOCOL_VERSION",
        "maxProtocol: PROTOCOL_VERSION",
        'client.request("sessions.subscribe"',
        'client.request("sessions.messages.subscribe", { key })',
        "OPENCLAW_GATEWAY_BOOTSTRAP_TOKEN",
        "OPENCLAW_GATEWAY_PASSWORD",
        "remote Gateway requires wss://",
        "gateway-event-device-identity.json",
        "gateway-event-device-token.json",
        "gateway-event-hints.jsonl",
        "openclaw_gateway_connection_sequence_gap",
        "openclaw_gateway_run_sequence_gap",
        "rawSnapshotPersisted: false",
        "credentialsPersistedInHintLedger: false",
    ],
    "subscriber",
)

projection_text = PROJECTION.read_text(encoding="utf-8")
require_tokens(
    projection_text,
    [
        '"sessions.changed"',
        '"session.message"',
        '"session.operation"',
        '"session.tool"',
        '"agent"',
        "rawPayloadPersisted: false",
        "redactedContentFieldsPresent",
        "auditReconciliationRequired: true",
        "durableHistoryAuthority: false",
        "observeCommitPerformed: false",
        "verificationCreated: false",
        "worldCommitAuthority: false",
        "truthPromotionAuthority: false",
        "automaticPlanCompletion: false",
        "automaticRollback: false",
        "memoryOverwriteAuthority: false",
    ],
    "projection",
)

doc_text = DOC.read_text(encoding="utf-8")
require_tokens(
    doc_text,
    [
        "live event != durable history",
        "WebSocket silence != non-occurrence proof",
        "auditReconciliationRequired = true",
        "sessions.subscribe",
        "sessions.messages.subscribe { key }",
        "outer event frame",
        "agent per-run seq",
        "v0.3 audit.activity.list = bounded reconciliation source",
    ],
    "documentation",
)

formal_text = FORMAL.read_text(encoding="utf-8")
require_tokens(
    formal_text,
    [
        "OpenClawLiveHintBoundary",
        "OpenClawLiveAuthorityBoundary",
        "OpenClawSequenceGapBoundary",
        "OpenClawReconnectBoundary",
        "OpenClawSilenceBoundary",
        "openclaw_live_event_is_hint_not_durable_observation",
        "openclaw_live_hint_grants_no_observe_authority",
        "openclaw_sequence_gap_requires_audit_reconciliation",
        "openclaw_reconnect_reestablishes_subscriptions_without_cross_epoch_seq",
        "openclaw_websocket_silence_is_not_nonoccurrence_proof",
    ],
    "formal boundary",
)

for path in (PROJECTION, SUBSCRIBER, TEST):
    completed = subprocess.run(
        ["node", "--check", str(path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        fail(f"Node syntax check failed: {path.relative_to(ROOT)}")

completed = subprocess.run(
    ["node", str(TEST)],
    cwd=ROOT,
    check=False,
    capture_output=True,
    text=True,
)
if completed.returncode != 0:
    sys.stderr.write(completed.stdout)
    sys.stderr.write(completed.stderr)
    fail("OpenClaw Gateway event projection tests failed")

print("kuuos_openclaw_gateway_event_subscriber_v0_4: OK")
