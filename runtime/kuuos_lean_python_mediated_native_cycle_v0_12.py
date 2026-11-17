"""Plural/Wa event gates around the original isolated native fixture route.

This explicit LOCAL TEST builder composes two mediator store gates with
v0.11's six core gates and selected Act pre-host check. The gates run before
event-result commit append/snapshot update and during event replay. Store
initialization is unchanged. The original v0.9 evidence record remains
write-once; a later read-only audit does not attest historical guard use.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager, ExitStack
from dataclasses import dataclass
from importlib import import_module
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterator

from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as core
from runtime import kuuos_lean_python_pre_host_native_cycle_v0_11 as prior
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    GOOD, IsolatedEvidenceAudit, ROOT,
)
from runtime.kuuos_lean_python_mediator_transition_v0_12 import (
    checked_apply_mediator_event,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json

VERSION = "kuuos_lean_python_mediated_native_cycle_v0_12"
SOURCE_MAIN = "dacc6fb5ae3cd85b9afee48d53348e6cc0a8dcc7"
SUCCESS = "MEDIATED_LOCAL_NATIVE_FIXTURE_CHECKED"
MEDIATOR_OS = ("DecisionOSPlural", "DecisionOSWa")
GUARDED_OS = (
    "DecisionOS", "DecisionOSPlural", "DecisionOSWa", "PlanOS", "ActOS",
    "ObserveOS", "VerifyOS", "LearnOS",
)
STORE_BINDINGS = (
    ("DecisionOSPlural", "runtime.kuuos_decision_os_plural_store_v0_2", "apply_plural_event"),
    ("DecisionOSWa", "runtime.kuuos_decision_os_wa_store_v0_3", "apply_wa_event"),
)
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "state_guard_calls", "pre_host_guard_calls",
    "native_record_sha256", "counts_include_recovery_replays",
    "act_invocation_inputs_checked_before_host", "all_effects_prevented_on_any_failure",
    "all_store_writes_guarded", "wa_real_number_refinement_proved",
))


@dataclass(frozen=True)
class MediatedNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    source_main: str = SOURCE_MAIN
    scope: str = "eight_native_event_result_gates_and_selected_Act_pre_host_inputs"
    counts_include_recovery_replays: bool = True
    guard_observation_mode: str = "local_child_stdout_unattested"
    act_invocation_inputs_checked_before_host: bool = True
    all_store_writes_guarded: bool = False
    wa_real_number_refinement_proved: bool = False
    all_effects_prevented_on_any_failure: bool = False
    host_rollback_guaranteed: bool = False
    state_commit_atomic_with_host: bool = False
    external_issuer_authenticated: bool = False
    historical_guard_execution_proved: bool = False
    lean_python_refinement_proved: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False


def audit_local_evidence(root: Any) -> IsolatedEvidenceAudit:
    """Read-only original evidence audit; no new guard is executed or attested."""
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_mediator_stores(counts: dict[str, int]) -> Iterator[None]:
    """Private single-child bindings; kernel functions and genesis stay intact.

    Count completed checks, including native rejection/replay and recovery.
    Each actual store retains its own native APPLIED/REPLAYED/REJECTED policy.
    """
    if (type(counts) is not dict or set(counts) != set(MEDIATOR_OS)
            or any(type(n) is not int or n != 0 for n in counts.values())):
        raise ValueError("fresh_mediator_guard_counters_required")
    with ExitStack() as stack:
        for os_name, module_name, function_name in STORE_BINDINGS:
            store_module = import_module(module_name)
            kernel_module = import_module(module_name.replace("_store_", "_kernel_"))
            if getattr(store_module, function_name) is not getattr(kernel_module, function_name):
                raise ValueError("original_mediator_store_binding_required:" + os_name)

            def guarded(state: Any, event: Any, *, _os_name: str = os_name) -> dict[str, Any]:
                result = checked_apply_mediator_event(_os_name, state, event)
                counts[_os_name] += 1
                return result

            stack.enter_context(core._replace_binding(store_module, function_name, guarded))
        yield


def _make_child_report(state_counts: dict[str, int], host_count: int,
                       audit: IsolatedEvidenceAudit) -> dict[str, Any]:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "state_guard_calls": dict(state_counts), "pre_host_guard_calls": host_count,
        "native_record_sha256": audit.record_sha256,
        "counts_include_recovery_replays": True,
        "act_invocation_inputs_checked_before_host": True,
        "all_effects_prevented_on_any_failure": False,
        "all_store_writes_guarded": False,
        "wa_real_number_refinement_proved": False,
    }


def _checked_report(value: Any, audit: IsolatedEvidenceAudit
                    ) -> tuple[tuple[tuple[str, int], ...], int]:
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
            or report["act_invocation_inputs_checked_before_host"] is not True
            or report["all_effects_prevented_on_any_failure"] is not False
            or report["all_store_writes_guarded"] is not False
            or report["wa_real_number_refinement_proved"] is not False):
        raise ValueError("child_report_scope_invalid")
    counts = report["state_guard_calls"]
    if (type(counts) is not dict or set(counts) != set(GUARDED_OS)
            or any(type(n) is not int or n <= 0 for n in counts.values())):
        raise ValueError("child_report_eight_os_coverage_missing")
    count = report["pre_host_guard_calls"]
    if type(count) is not int or count != 1:
        raise ValueError("child_report_one_native_act_invocation_required")
    return tuple((name, counts[name]) for name in GUARDED_OS), count


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_mediator_sources_v0_12 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("mediator_source_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = core._fresh_root(root)
    _source_preflight()
    counts = {name: 0 for name in MEDIATOR_OS}
    with _guard_mediator_stores(counts):
        old_report = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    state_counts, host_count = prior._checked_report(old_report, audit)
    combined = {**dict(state_counts), **counts}
    report = _make_child_report(combined, host_count, audit)
    _checked_report(report, audit)
    return report


def build_mediated_native_fixture(root: Path) -> MediatedNativeRun:
    """Build a bounded local fixture in a fresh interpreter, then reread it.

    Inputs require an empty trusted root. A failure never retries or removes
    partial output. Neither process isolation nor a passed guard establishes
    issuer authenticity, numerical refinement, rollback, or new authority.
    """
    root = core._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_mediated_native_cycle_v0_12",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("mediated_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > core.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    state_counts, host_count = _checked_report(report, audit)
    return MediatedNativeRun(
        status=SUCCESS, state_guard_calls=state_counts,
        pre_host_guard_calls=host_count, native_audit=audit,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("mediated_native_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "MEDIATOR_OS", "GUARDED_OS", "MediatedNativeRun",
    "build_mediated_native_fixture", "audit_local_evidence",
)
