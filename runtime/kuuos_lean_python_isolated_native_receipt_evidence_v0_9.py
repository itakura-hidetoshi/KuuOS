"""Process-isolated, write-once native receipt capture evidence v0.9.

Explicit local bounded fixture construction happens ONLY in a child Python
process. The separate audit reads the resulting evidence record and the
original ActOS ledger without modifying either. The child invokes v0.8's
genuine-return instrumentation on the original native v1.3 fixture.

A local digest chain and root binding do NOT authenticate a signature,
external issuer, past historical observation, Lean/Python refinement,
real-world execution permission, or mathematical descent/gluing.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_lean_python_native_cycle_receipt_capture_v0_8 import (
    SUCCESS as CAPTURE_PASS,
    ReturnCaptureAudit,
    audit_captured_native_receipts,
    build_captured_native_test_fixture,
)

VERSION = "kuuos_lean_python_isolated_native_receipt_evidence_v0_9"
SOURCE_MAIN = "afcb9cd7d84ba6beee45b2fcfc704473f593df25"
MODE = "local_child_process_original_return_capture_write_once"
EVIDENCE_FILE = "kuuos-lean-python-native-return-evidence-v0-9.json"
GOOD = "ISOLATED_LOCAL_FIXTURE_EVIDENCE_REPLAYED"
NO_DATA = "NO_DATA"
BLOCKED = "BLOCKED"
ROOT = Path(__file__).resolve().parents[1]
MAX_EVIDENCE_BYTES = 8_000_000
EVIDENCE_KEYS = frozenset((
    "version", "source_main", "mode", "root_binding_sha256",
    "native_cycle_receipt", "return_capture", "native_cycle_digest",
    "return_capture_sha256", "record_sha256",
))


@dataclass(frozen=True)
class IsolatedEvidenceAudit:
    status: str
    violations: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    record_sha256: str | None = None
    native_cycle_digest: str | None = None
    return_capture_sha256: str | None = None
    local_audit: ReturnCaptureAudit | None = None
    source_main: str = SOURCE_MAIN
    observation_mode: str = MODE
    process_isolation_scope: str = "explicit_local_fixture_child_only"
    local_record_checked: bool = False
    external_issuer_authenticated: bool = False
    historical_issuance_proved: bool = False
    lean_python_refinement_proved: bool = False
    formal_descent_certified: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def root_binding(root: Path) -> str:
    """Local directory-name checksum only, NOT an authenticated filesystem ID."""
    return hashlib.sha256(str(root.resolve(strict=True)).encode("utf-8")).hexdigest()


def evidence_digest(record: dict[str, Any]) -> str:
    return _sha({k: v for k, v in record.items() if k != "record_sha256"})


def _make_record(
    root: Path, original: dict[str, Any], captured: dict[str, Any],
) -> dict[str, Any]:
    record = {
        "version": VERSION,
        "source_main": SOURCE_MAIN,
        "mode": MODE,
        "root_binding_sha256": root_binding(root),
        "native_cycle_receipt": _finite_json(original),
        "return_capture": _finite_json(captured),
        "native_cycle_digest": original["native_full_cycle_receipt_digest"],
        "return_capture_sha256": captured["capture_sha256"],
        "record_sha256": "",
    }
    record["record_sha256"] = evidence_digest(record)
    return record


def _write_once(root: Path, record: dict[str, Any]) -> None:
    """Stage & atomically hard-link with no-replace semantics (local Linux FS).

    If an evidence record already exists, os.link fails with FileExistsError;
    no original record is ever overwritten. A preflight in the builder also
    rejects nonempty fixture roots before any original OS builder effects.
    """
    content = _canonical(_finite_json(record)) + b"\n"
    if len(content) > MAX_EVIDENCE_BYTES:
        raise ValueError("evidence_too_large")
    target = root / EVIDENCE_FILE
    fd, temp = tempfile.mkstemp(prefix=".kuuos-native-evidence-", dir=root)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        # Atomic no-replace: never use os.replace or a writable target.
        os.link(temp, target, follow_symlinks=False)
        if hasattr(os, "O_DIRECTORY"):
            dfd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def _child_fixture_entry(root: Path) -> None:
    """Only called under explicit '--fixture-child'; writes local test files."""
    if not isinstance(root, Path) or not root.is_dir() or root.is_symlink():
        raise ValueError("trusted_existing_fixture_root_required")
    if any(root.iterdir()):
        raise ValueError("fixture_root_not_empty_no_overwrite")
    original, capture = build_captured_native_test_fixture(root)
    check = audit_captured_native_receipts(root, original, capture)
    if check.status != CAPTURE_PASS:
        raise ValueError("captured_native_fixture_not_valid:" + check.status)
    _write_once(root, _make_record(root, original, capture))


def build_isolated_fixture_evidence(root: Path) -> IsolatedEvidenceAudit:
    """Explicit effectful LOCAL test builder, not a read-only verifier.

    Forks a separate Python interpreter; temporary global receipt observation
    wrappers from v0.8 live only in that child interpreter. No shell is used.
    Original native v1.3 bounded local fixture effects and test journals are
    generated in this fresh root. No existing root may be reused or overwritten.
    """
    if not isinstance(root, Path) or not root.is_dir() or root.is_symlink():
        raise ValueError("trusted_existing_fixture_root_required")
    if any(root.iterdir()):
        raise ValueError("fixture_root_not_empty_no_overwrite")
    root = root.resolve(strict=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join((
        str(ROOT),
        env["PYTHONPATH"] if env.get("PYTHONPATH") else "",
    ))
    command = [
        sys.executable, "-m",
        "runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9",
        "--fixture-child", str(root),
    ]
    completed = subprocess.run(
        command, cwd=ROOT, env=env,
        capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        # Short, explicit diagnostic from trusted native fixture code only.
        detail = (completed.stderr or completed.stdout)[-700:]
        raise RuntimeError(
            f"isolated_native_fixture_child_failed:{completed.returncode}:{detail}"
        )
    result = audit_isolated_evidence(root)
    if result.status != GOOD:
        raise RuntimeError(
            "isolated_native_fixture_postverification_failed:" + result.status
            + ":" + repr(result.violations) + ":" + repr(result.missing)
        )
    return result


def _finish(errors: list[str], missing: list[str],
            record: dict[str, Any] | None = None,
            native_audit: ReturnCaptureAudit | None = None) -> IsolatedEvidenceAudit:
    status = BLOCKED if errors else NO_DATA if missing else GOOD
    return IsolatedEvidenceAudit(
        status=status,
        violations=tuple(dict.fromkeys(errors)),
        missing=tuple(dict.fromkeys(missing)),
        record_sha256=(record.get("record_sha256") if record else None),
        native_cycle_digest=(record.get("native_cycle_digest") if record else None),
        return_capture_sha256=(record.get("return_capture_sha256") if record else None),
        local_audit=native_audit,
        local_record_checked=(status == GOOD),
    )


def audit_isolated_evidence(root: Any) -> IsolatedEvidenceAudit:
    """Read-only exact local evidence check. No subprocess or host invocation.

    The file checksum/root binding are forgeable by a local writer; only the
    original native builder's specific scoped runtime constraints are checked.
    Inspect quiescent fixture roots only (no concurrent OS ledger writes).
    """
    errors: list[str] = []
    missing: list[str] = []
    if not isinstance(root, Path) or not root.is_dir() or root.is_symlink():
        return _finish(["root:trusted_existing_path_required"], missing)
    target = root / EVIDENCE_FILE
    if target.is_symlink():
        return _finish(["record:symlink_not_allowed"], missing)
    if not target.exists():
        return _finish(errors, ["record:missing"])
    if not target.is_file():
        return _finish(["record:not_regular_file"], missing)
    try:
        if target.stat().st_size > MAX_EVIDENCE_BYTES:
            return _finish(["record:oversize"], missing)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(target, flags)
        with os.fdopen(fd, "rb") as handle:
            raw = handle.read(MAX_EVIDENCE_BYTES + 1)
        if len(raw) > MAX_EVIDENCE_BYTES:
            return _finish(["record:oversize"], missing)
        record = _finite_json(json.loads(raw.decode("utf-8")))
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        return _finish(["record:invalid_json_or_read_failed"], missing)
    if type(record) is not dict:
        return _finish(["record:plain_dict_required"], missing)
    if set(record) != EVIDENCE_KEYS:
        return _finish(["record:field_inventory_mismatch"], missing, record)
    if record["version"] != VERSION or record["source_main"] != SOURCE_MAIN:
        errors.append("record:source_version_mismatch")
    if record["mode"] != MODE:
        errors.append("record:observation_mode_mismatch")
    if (type(record["record_sha256"]) is not str
            or record["record_sha256"] != evidence_digest(record)):
        errors.append("record:checksum_mismatch")
    if record["root_binding_sha256"] != root_binding(root):
        errors.append("record:root_binding_mismatch")
    if type(record["native_cycle_receipt"]) is not dict:
        errors.append("record:native_cycle_receipt_type_invalid")
    if type(record["return_capture"]) is not dict:
        errors.append("record:return_capture_type_invalid")
    if errors:
        return _finish(errors, missing, record)
    original = record["native_cycle_receipt"]
    captured = record["return_capture"]
    if record["native_cycle_digest"] != original.get("native_full_cycle_receipt_digest"):
        errors.append("record:native_cycle_reference_mismatch")
    if record["return_capture_sha256"] != captured.get("capture_sha256"):
        errors.append("record:return_capture_reference_mismatch")

    # A read-only check of all actual original native snapshots, raw receipt
    # return contents and the ActOS ledger inherited from v0.7/v0.8.
    try:
        check = audit_captured_native_receipts(root, original, captured)
    except Exception as exc:
        errors.append("audit:unexpected_exception:" + type(exc).__name__)
        return _finish(errors, missing, record)
    if check.status == BLOCKED:
        errors.extend("original_native:" + issue
                      for issue in (check.violations or ("blocked",)))
        missing.extend("original_native:" + issue for issue in check.missing)
    elif check.status == NO_DATA:
        missing.extend("original_native:" + issue
                       for issue in (check.missing or ("no_data",)))
    elif check.status != CAPTURE_PASS:
        errors.append("original_native:unsupported_status")
    return _finish(errors, missing, record, check)


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("local_native_fixture_child_failed:" + type(exc).__name__
              + ":" + str(exc), file=sys.stderr)
        return 1
    print("local_native_fixture_evidence_written_once")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "MODE", "EVIDENCE_FILE", "GOOD", "NO_DATA",
    "BLOCKED", "ROOT", "MAX_EVIDENCE_BYTES", "EVIDENCE_KEYS",
    "IsolatedEvidenceAudit", "root_binding", "evidence_digest",
    "build_isolated_fixture_evidence", "audit_isolated_evidence",
)
