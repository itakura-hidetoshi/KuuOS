#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME = ROOT / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3.py"
TEST = ROOT / "tests" / "test_openclaw_audit_observation_ingest_v0_3.py"
DOC = ROOT / "docs" / "KUUOS_OPENCLAW_AUDIT_OBSERVATION_INGEST_v0_3.md"
MANIFEST = ROOT / "manifests" / "kuuos_openclaw_audit_observation_ingest_v0_3.json"
FORMAL = ROOT / "formal" / "KUOS" / "ObserveOS" / "OpenClawAuditObservationIntakeV0_3.lean"
REGISTRY = ROOT / "ci" / "check_registry.d" / "openclaw_audit_observation_v0_3.json"
V02 = ROOT / "runtime" / "kuuos_openclaw_gateway_controller_v0_2.py"
V01 = ROOT / "runtime" / "kuuos_openclaw_control_server_v0_1.py"
OBSERVE_V02 = ROOT / "formal" / "KUOS" / "ObserveOS" / "ReplanLineageObservationEnvelopeV0_2.lean"

REQUIRED = [RUNTIME, TEST, DOC, MANIFEST, FORMAL, REGISTRY, V02, V01, OBSERVE_V02]


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
except json.JSONDecodeError as error:
    fail(f"JSON parse failure: {error}")

if manifest.get("version") != "kuuos_openclaw_audit_observation_ingest_v0_3":
    fail("manifest version mismatch")
if manifest.get("openclaw_rpc") != ["audit.activity.list"]:
    fail("manifest must bind exactly to audit.activity.list")
authority = manifest.get("authority")
if not isinstance(authority, dict):
    fail("manifest authority object missing")
for key in (
    "observe_commit",
    "verification_result",
    "world_commit",
    "truth_promotion",
    "plan_completion",
    "automatic_plan_completion",
    "rollback_proof",
    "automatic_rollback",
    "memory_overwrite",
):
    if authority.get(key) is not False:
        fail(f"manifest authority must keep {key}=false")

checks = registry.get("checks")
if not isinstance(checks, dict) or "openclaw-audit-observation-v03" not in checks:
    fail("CI registry check openclaw-audit-observation-v03 missing")
if checks["openclaw-audit-observation-v03"].get("command") != (
    "python3 scripts/check_openclaw_audit_observation_ingest_v0_3.py"
):
    fail("CI registry command mismatch")

runtime_text = RUNTIME.read_text(encoding="utf-8")
require_tokens(
    runtime_text,
    [
        "audit.activity.list",
        "metadata_only",
        "sourceEventDigest",
        "actorDigest",
        "sessionKeyDigest",
        "audit-observation-candidates.jsonl",
        "audit-ingest-checkpoints.json",
        "resumeCursor",
        "catchupHighWaterSequence",
        '"observeCommitPerformed": False',
        '"verificationRequired": True',
        '"verificationCreated": False',
        '"worldCommitAuthority": False',
        '"truthPromotionAuthority": False',
        '"automaticPlanCompletion": False',
        '"automaticRollback": False',
        '"absenceProvesNonOccurrence": False',
        '"memoryOverwriteAuthority": False',
    ],
    "runtime",
)

doc_text = DOC.read_text(encoding="utf-8")
require_tokens(
    doc_text,
    [
        "OpenClaw audit row != ObserveOS commit",
        "OpenClaw status succeeded != PlanOS completion",
        "OpenClaw audit absence != non-occurrence proof",
        "bestEffortSource = true",
        "observeCommitPerformed = false",
        "verificationCreated = false",
        "worldCommitAuthority = false",
        "automaticPlanCompletion = false",
        "automaticRollback = false",
        "memoryOverwriteAuthority = false",
        "persistent WebSocket event subscription",
    ],
    "documentation",
)

formal_text = FORMAL.read_text(encoding="utf-8")
require_tokens(
    formal_text,
    [
        "OpenClawAuditSourceBoundary",
        "OpenClawAuditIntakeBoundary",
        "OpenClawHostStatusAuthorityBoundary",
        "openclaw_audit_candidate_is_not_observe_commit",
        "openclaw_host_status_grants_no_observe_authority",
        "openclaw_host_status_does_not_complete_plan_or_prove_rollback",
        "partial_openclaw_audit_window_preserves_old_checkpoint",
        "observe_lineage_envelope_grants_no_new_authority",
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
    fail("OpenClaw audit observation v0.3 unit tests failed")

print("kuuos_openclaw_audit_observation_ingest_v0_3: OK")
