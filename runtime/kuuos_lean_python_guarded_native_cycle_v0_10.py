"""Six native store routes consume checked transitions in an isolated fixture.

This is an explicit local TEST builder. A checked state transition precedes
the original store commit, not every prior host effect. The existing Act
fixture issues its bounded host tick before store.apply. Neither a successful
run nor a later read-only audit grants authority or Lean/Python refinement.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager, ExitStack
from dataclasses import dataclass
from importlib import import_module
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Iterator

from runtime.kuuos_lean_python_checked_transition_v0_10 import checked_apply_event
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    GOOD, IsolatedEvidenceAudit, ROOT, _child_fixture_entry as _original_child,
    audit_isolated_evidence,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json

VERSION = "kuuos_lean_python_guarded_native_cycle_v0_10"
SOURCE_MAIN = "8b855cf1f1c2296dbe0d8d3057cd391729d572d1"
SUCCESS = "GUARDED_LOCAL_NATIVE_FIXTURE_CHECKED"
GUARDED_OS = ("DecisionOS", "PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS")
STORE_BINDINGS = tuple(
    (name, "runtime.kuuos_" + stem + "_os_store_v0_1", "apply_" + stem + "_event")
    for name, stem in zip(GUARDED_OS, ("decision", "plan", "act", "observe", "verify", "learn"))
)
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "guard_calls", "native_record_sha256",
    "counts_include_recovery_replays", "pre_host_effect_guarded",
))
MAX_LOCAL_ENTRIES = 10_000
MAX_CHILD_OUTPUT_BYTES = 16_384


@dataclass(frozen=True)
class GuardedNativeRun:
    status: str
    guard_calls: tuple[tuple[str, int], ...]
    native_audit: IsolatedEvidenceAudit
    source_main: str = SOURCE_MAIN
    scope: str = "six_core_state_transitions_before_local_store_commit"
    counts_include_recovery_replays: bool = True
    guard_observation_mode: str = "local_child_stdout_unattested"
    pre_host_effect_guarded: bool = False
    external_issuer_authenticated: bool = False
    historical_guard_execution_proved: bool = False
    lean_python_refinement_proved: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False


def _local_path_issues(root: Any) -> tuple[str, ...]:
    """Check a quiescent trusted fixture, without following linked children."""
    if not isinstance(root, Path) or root.is_symlink() or not root.is_dir():
        return ("fixture:trusted_existing_nonlinked_directory_required",)
    def fail_on_walk_error(error: OSError) -> None:
        raise error
    try:
        count = 0
        for parent, directories, files in os.walk(root, followlinks=False,
                                                   onerror=fail_on_walk_error):
            for name in directories + files:
                count += 1
                if count > MAX_LOCAL_ENTRIES:
                    return ("fixture:path_budget_exceeded",)
                path = Path(parent) / name
                mode = path.lstat().st_mode
                if stat.S_ISLNK(mode):
                    return ("fixture:symlink_not_allowed:" + str(path.relative_to(root)),)
                if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                    return ("fixture:not_regular_file_or_directory",)
    except (OSError, ValueError):
        return ("fixture:local_path_read_failed",)
    return ()


def audit_local_evidence(root: Any) -> IsolatedEvidenceAudit:
    """Read-only v0.9 evidence audit with an additional local path precheck.

    This audit cannot establish historical execution of the v0.10 guards.
    No process is launched, no state is applied, and no record is written.
    """
    issues = _local_path_issues(root)
    if issues:
        return IsolatedEvidenceAudit(status="BLOCKED", violations=issues)
    try:
        return audit_isolated_evidence(root)
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        return IsolatedEvidenceAudit(
            status="BLOCKED", violations=("fixture:audit_failed:" + type(exc).__name__,),
        )


@contextmanager
def _replace_binding(module: Any, name: str, replacement: Any) -> Iterator[None]:
    original = getattr(module, name)
    setattr(module, name, replacement)
    try:
        yield
    finally:
        setattr(module, name, original)


@contextmanager
def _guard_native_stores(counts: dict[str, int]) -> Iterator[None]:
    """Private child-local instrumentation; original kernel globals stay intact.

    Calls include ledger recovery replays. Count only fully checked results;
    native REJECTED remains a rejection, not an APPLIED transition.
    """
    if set(counts) != set(GUARDED_OS) or any(type(n) is not int or n != 0 for n in counts.values()):
        raise ValueError("fresh_guard_counters_required")
    with ExitStack() as stack:
        for os_name, module_name, function_name in STORE_BINDINGS:
            store_module = import_module(module_name)
            kernel_module = import_module(module_name.replace("_store_", "_kernel_"))
            if getattr(store_module, function_name) is not getattr(kernel_module, function_name):
                raise ValueError("original_store_binding_required:" + os_name)

            def guarded(state: Any, event: Any, *, _os_name: str = os_name) -> dict[str, Any]:
                result = checked_apply_event(_os_name, state, event)
                counts[_os_name] += 1
                return result

            stack.enter_context(_replace_binding(store_module, function_name, guarded))
        yield


def _make_child_report(counts: dict[str, int], audit: IsolatedEvidenceAudit) -> dict[str, Any]:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "guard_calls": dict(counts), "native_record_sha256": audit.record_sha256,
        "counts_include_recovery_replays": True, "pre_host_effect_guarded": False,
    }


def _checked_report_counts(value: Any, audit: IsolatedEvidenceAudit) -> tuple[tuple[str, int], ...]:
    report = _finite_json(value)
    if type(report) is not dict or set(report) != REPORT_KEYS:
        raise ValueError("child_report_inventory_invalid")
    if (report["version"] != VERSION or report["source_main"] != SOURCE_MAIN
            or report["status"] != SUCCESS):
        raise ValueError("child_report_source_or_status_invalid")
    if (audit.status != GOOD or type(audit.record_sha256) is not str
            or report["native_record_sha256"] != audit.record_sha256):
        raise ValueError("child_report_evidence_binding_invalid")
    if (report["counts_include_recovery_replays"] is not True
            or report["pre_host_effect_guarded"] is not False):
        raise ValueError("child_report_scope_invalid")
    counts = report["guard_calls"]
    if (type(counts) is not dict or set(counts) != set(GUARDED_OS)
            or any(type(n) is not int or n <= 0 for n in counts.values())):
        raise ValueError("child_report_six_os_coverage_missing")
    return tuple((name, counts[name]) for name in GUARDED_OS)


def _fresh_root(root: Any) -> Path:
    if not isinstance(root, Path) or root.is_symlink() or not root.is_dir():
        raise ValueError("fresh_existing_nonlinked_fixture_root_required")
    if any(root.iterdir()):
        raise ValueError("fixture_root_not_empty_no_overwrite")
    return root.resolve(strict=True)


def _source_preflight() -> None:
    # Imported here to keep the checker independent of runtime imports.
    from scripts.check_kuuos_lean_python_checked_transition_sources_v0_10 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("source_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = _fresh_root(root)
    _source_preflight()
    counts = {name: 0 for name in GUARDED_OS}
    with _guard_native_stores(counts):
        # Original v0.9 construction calls original v0.8/v1.3 and preserves
        # the v0.9 write-once record. Only store module bindings are wrapped.
        _original_child(root)
    audit = audit_local_evidence(root)
    report = _make_child_report(counts, audit)
    _checked_report_counts(report, audit)
    return report


def build_guarded_native_fixture(root: Path) -> GuardedNativeRun:
    """Explicit bounded LOCAL test effects, with six checked state routes.

    The child emits a scoped, unsigned count report; parent independently
    re-reads v0.9 evidence. Counts are not durable historical attestation.
    Host tick creation remains in the original earlier fixture route.
    """
    root = _fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_guarded_native_cycle_v0_10",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("guarded_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    counts = _checked_report_counts(report, audit)
    return GuardedNativeRun(status=SUCCESS, guard_calls=counts, native_audit=audit)


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("guarded_native_fixture_failed:" + type(exc).__name__ + ":" + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "GUARDED_OS", "STORE_BINDINGS",
    "GuardedNativeRun", "build_guarded_native_fixture", "audit_local_evidence",
)
