"""Act pre-host input checks on the original isolated native fixture route.

This explicit LOCAL TEST builder adds a caller-side gate to v0.10's six
store gates. Only the original fixture's imported invocation builder is
temporarily replaced, in the child. Original kernels, host functions and
persisted v0.9 record format stay intact. The unsigned child report does not
prove historical execution or make host effects atomic with a store commit.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from importlib import import_module
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterator

from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as prior
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    GOOD, IsolatedEvidenceAudit, ROOT,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_lean_python_pre_host_guard_v0_11 import (
    checked_build_authorized_invoke_event,
)

VERSION = "kuuos_lean_python_pre_host_native_cycle_v0_11"
SOURCE_MAIN = "3da68503b6be1f6ef02d6100b730fa5ab9b92498"
SUCCESS = "PRE_HOST_GUARDED_LOCAL_NATIVE_FIXTURE_CHECKED"
CALLER_MODULE = "runtime.v01_act_os_authority_bound_invocation"
BUILDER_BINDING = "build_authorized_invoke_event"
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "state_guard_calls", "pre_host_guard_calls",
    "native_record_sha256", "counts_include_recovery_replays",
    "act_invocation_inputs_checked_before_host", "all_effects_prevented_on_any_failure",
))


@dataclass(frozen=True)
class PreHostNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    source_main: str = SOURCE_MAIN
    scope: str = "selected_native_Act_invocation_inputs_before_original_host_call"
    counts_include_recovery_replays: bool = True
    guard_observation_mode: str = "local_child_stdout_unattested"
    act_invocation_inputs_checked_before_host: bool = True
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
    """Read-only original evidence audit; not a past pre-host execution proof."""
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_native_invocation(counts: dict[str, int]) -> Iterator[None]:
    """Private single-child instrumentation of the actual native caller."""
    if (type(counts) is not dict or set(counts) != {"ActOS"}
            or type(counts["ActOS"]) is not int or counts["ActOS"] != 0):
        raise ValueError("fresh_pre_host_counter_required")
    caller = import_module(CALLER_MODULE)
    kernel = import_module("runtime.kuuos_act_os_kernel_v0_1")
    if getattr(caller, BUILDER_BINDING) is not getattr(kernel, BUILDER_BINDING):
        raise ValueError("original_native_invocation_binding_required")

    def guarded(**kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        result = checked_build_authorized_invoke_event(**kwargs)
        counts["ActOS"] += 1
        return result

    with prior._replace_binding(caller, BUILDER_BINDING, guarded):
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
            or report["all_effects_prevented_on_any_failure"] is not False):
        raise ValueError("child_report_scope_invalid")
    counts = report["state_guard_calls"]
    if (type(counts) is not dict or set(counts) != set(prior.GUARDED_OS)
            or any(type(n) is not int or n <= 0 for n in counts.values())):
        raise ValueError("child_report_six_os_coverage_missing")
    count = report["pre_host_guard_calls"]
    if type(count) is not int or count != 1:
        raise ValueError("child_report_one_native_act_invocation_required")
    return tuple((name, counts[name]) for name in prior.GUARDED_OS), count


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_pre_host_sources_v0_11 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("pre_host_source_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = prior._fresh_root(root)
    _source_preflight()
    host_counts = {"ActOS": 0}
    with _guard_native_invocation(host_counts):
        old_report = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    state_counts = prior._checked_report_counts(old_report, audit)
    report = _make_child_report(dict(state_counts), host_counts["ActOS"], audit)
    _checked_report(report, audit)
    return report


def build_pre_host_guarded_native_fixture(root: Path) -> PreHostNativeRun:
    """Run a bounded local test in a fresh interpreter, then independently read.

    Passing input checks does not authenticate the authorization issuer or
    executor, promise whole-run exactly-once effects, or grant permissions.
    A post-host failure may already have effects; this builder never retries
    or removes partial output and never overwrites an existing fixture root.
    """
    root = prior._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_pre_host_native_cycle_v0_11",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("pre_host_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > prior.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    state_counts, host_count = _checked_report(report, audit)
    return PreHostNativeRun(
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
        print("pre_host_native_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "PreHostNativeRun",
    "build_pre_host_guarded_native_fixture", "audit_local_evidence",
)
