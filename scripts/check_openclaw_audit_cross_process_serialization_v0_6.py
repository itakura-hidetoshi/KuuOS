#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3.py"
IMPLEMENTATION = ROOT / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3_impl.py"
TEST = ROOT / "tests" / "test_openclaw_audit_cross_process_serialization_v0_6.py"
LEGACY_CHECK = ROOT / "scripts" / "check_openclaw_audit_observation_ingest_v0_3.py"
DOC = ROOT / "docs" / "KUUOS_OPENCLAW_AUDIT_CROSS_PROCESS_SERIALIZATION_v0_6.md"
MANIFEST = ROOT / "manifests" / "kuuos_openclaw_audit_cross_process_serialization_v0_6.json"
FORMAL = ROOT / "formal" / "KUOS" / "ObserveOS" / "OpenClawAuditCrossProcessSerializationV0_6.lean"
REGISTRY = ROOT / "ci" / "check_registry.d" / "openclaw_audit_cross_process_serialization_v0_6.json"
SUPERVISOR = ROOT / "runtime" / "kuuos_openclaw_supervisor_v0_5_impl.py"

REQUIRED = [RUNTIME, IMPLEMENTATION, TEST, LEGACY_CHECK, DOC, MANIFEST, FORMAL, REGISTRY, SUPERVISOR]


def fail(message: str) -> None:
    raise SystemExit(message)


def require_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        fail(f"{label}: missing required tokens: {missing}")


for path in REQUIRED:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")

for path in (RUNTIME, IMPLEMENTATION, TEST):
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as error:
        fail(f"python syntax error in {path.relative_to(ROOT)}: {error}")

try:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
except json.JSONDecodeError as error:
    fail(f"JSON parse failure: {error}")

if manifest.get("version") != "kuuos_openclaw_audit_cross_process_serialization_v0_6":
    fail("v0.6 manifest version mismatch")
lock = manifest.get("lock")
if not isinstance(lock, dict):
    fail("v0.6 lock manifest missing")
for key in ("exclusive", "timeout_fail_closed", "kernel_owned", "persistent_file_is_not_lock_ownership", "process_exit_releases_ownership"):
    if lock.get(key) is not True:
        fail(f"v0.6 lock manifest must keep {key}=true")
if lock.get("scope") != "data_dir":
    fail("v0.6 lock must be data-dir scoped")
if lock.get("posix_backend") != "fcntl.flock" or lock.get("windows_backend") != "msvcrt.locking":
    fail("v0.6 lock backend contract mismatch")

authority = manifest.get("authority")
if not isinstance(authority, dict):
    fail("v0.6 authority object missing")
for key in (
    "observe_commit",
    "verification_result",
    "effect_permission",
    "world_commit",
    "truth_promotion",
    "plan_completion",
    "automatic_plan_completion",
    "rollback_proof",
    "automatic_rollback",
    "memory_overwrite",
):
    if authority.get(key) is not False:
        fail(f"v0.6 authority must keep {key}=false")

checks = registry.get("checks")
if not isinstance(checks, dict) or "openclaw-audit-cross-process-lock-v06" not in checks:
    fail("CI registry check openclaw-audit-cross-process-lock-v06 missing")
if checks["openclaw-audit-cross-process-lock-v06"].get("command") != (
    "python3 scripts/check_openclaw_audit_cross_process_serialization_v0_6.py"
):
    fail("v0.6 CI registry command mismatch")

runtime_text = RUNTIME.read_text(encoding="utf-8")
require_tokens(
    runtime_text,
    [
        'SERIALIZATION_VERSION = "kuuos_openclaw_audit_cross_process_serialization_v0_6"',
        'LOCK_FILENAME = "audit-ingest-state.lock"',
        'LOCK_TIMEOUT_ENV = "KUUOS_OPENCLAW_AUDIT_LOCK_TIMEOUT_MS"',
        "class AuditStateLock",
        "os.O_RDWR | os.O_CREAT",
        "0o600",
        "fcntl.flock",
        "msvcrt.locking",
        "LOCK_EX | fcntl.LOCK_NB",
        "msvcrt.LK_NBLCK",
        "timed out acquiring KuuOS audit state lock",
        "with AuditStateLock(checkpoints.data_dir)",
        "_IMPL.sync = sync",
        "_IMPL.status = status",
    ],
    "v0.6 runtime wrapper",
)

implementation_text = IMPLEMENTATION.read_text(encoding="utf-8")
require_tokens(
    implementation_text,
    [
        'VERSION = "kuuos_openclaw_audit_observation_ingest_v0_3"',
        'SOURCE = "openclaw.gateway.audit.activity"',
        '"audit.activity.list"',
        "class ObservationLedger",
        "class CheckpointStore",
        "def sync(",
        "def status(",
    ],
    "retained v0.3 implementation",
)

supervisor_text = SUPERVISOR.read_text(encoding="utf-8")
require_tokens(
    supervisor_text,
    ["kuuos_openclaw_audit_observation_ingest_v0_3.py"],
    "v0.5 inherited public audit path",
)

doc_text = DOC.read_text(encoding="utf-8")
require_tokens(
    doc_text,
    [
        "data-dir OS lock",
        "fcntl.flock(LOCK_EX | LOCK_NB)",
        "msvcrt.locking(LK_NBLCK, 1)",
        "lock ownership is not encoded by file existence",
        "lock unavailable != permission to bypass serialization",
        "cooperating-process guarantee",
        "exclusive lock != WORLD truth",
    ],
    "v0.6 documentation",
)

formal_text = FORMAL.read_text(encoding="utf-8")
require_tokens(
    formal_text,
    [
        "OpenClawAuditCrossProcessSerializationBoundary",
        "openclaw_audit_public_entrypoints_share_cross_process_lock",
        "OpenClawAuditLockAuthorityBoundary",
        "openclaw_audit_cross_process_lock_grants_no_new_authority",
        "openclaw_audit_cross_process_lock_does_not_complete_plan_or_prove_rollback",
    ],
    "v0.6 formal boundary",
)

for command, label in (
    ([sys.executable, str(LEGACY_CHECK)], "legacy v0.3 validation"),
    ([sys.executable, str(TEST)], "v0.6 cross-process serialization tests"),
):
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=30)
    if completed.returncode != 0:
        sys.stderr.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        fail(f"{label} failed")

print("kuuos_openclaw_audit_cross_process_serialization_v0_6: OK")
