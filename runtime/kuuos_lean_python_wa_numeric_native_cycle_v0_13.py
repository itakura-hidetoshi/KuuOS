"""Wa numeric checks composed with the original isolated eight-route fixture.

Only v0.12's imported pure mediator boundary is wrapped in the explicit local
test child. Its Wa calls use the additive numeric gate; its Plural calls keep
the original structural gate. Existing store, kernel, host, source-check and
write-once evidence paths remain intact. A later audit does not rerun these
numeric checks or prove their historical execution.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterator

from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as core
from runtime import kuuos_lean_python_mediator_transition_v0_12 as structural
from runtime import kuuos_lean_python_mediated_native_cycle_v0_12 as prior
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    IsolatedEvidenceAudit, ROOT,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_lean_python_wa_numeric_guard_v0_13 import checked_apply_wa_numeric_event

VERSION = "kuuos_lean_python_wa_numeric_native_cycle_v0_13"
SOURCE_MAIN = "a866f5841e8f324133928eed101cec405d67ac76"
SUCCESS = "WA_NUMERIC_LOCAL_NATIVE_FIXTURE_CHECKED"
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "mediated_report", "wa_numeric_guard_calls",
    "wa_numeric_interval_bounds_checked", "numeric_values_modified",
    "wa_real_number_refinement_proved",
))


@dataclass(frozen=True)
class WaNumericNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    wa_numeric_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    source_main: str = SOURCE_MAIN
    scope: str = "Wa_numeric_schema_on_eight_route_local_native_fixture"
    wa_numeric_interval_bounds_checked: bool = True
    numeric_values_modified: bool = False
    counts_include_recovery_replays: bool = True
    guard_observation_mode: str = "local_child_stdout_unattested"
    act_invocation_inputs_checked_before_host: bool = True
    all_store_writes_guarded: bool = False
    wa_real_number_refinement_proved: bool = False
    wa_evaluation_equivalence_proved: bool = False
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
    """Read the original v0.9 evidence; no historical numeric attestation."""
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_numeric_boundary(counts: dict[str, int]) -> Iterator[None]:
    """Child-local wrapper around v0.12's imported boundary, not its kernels."""
    if (type(counts) is not dict or set(counts) != {"DecisionOSWa"}
            or type(counts["DecisionOSWa"]) is not int or counts["DecisionOSWa"] != 0):
        raise ValueError("fresh_wa_numeric_counter_required")
    original = prior.checked_apply_mediator_event
    if original is not structural.checked_apply_mediator_event:
        raise ValueError("original_mediator_boundary_binding_required")

    def guarded(os_name: str, state: Any, event: Any) -> dict[str, Any]:
        if os_name == "DecisionOSWa":
            result = checked_apply_wa_numeric_event(state, event)
            counts["DecisionOSWa"] += 1
            return result
        return original(os_name, state, event)

    with core._replace_binding(prior, "checked_apply_mediator_event", guarded):
        yield


def _make_child_report(mediated_report: dict[str, Any], numeric_count: int) -> dict[str, Any]:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "mediated_report": _finite_json(mediated_report),
        "wa_numeric_guard_calls": numeric_count,
        "wa_numeric_interval_bounds_checked": True,
        "numeric_values_modified": False,
        "wa_real_number_refinement_proved": False,
    }


def _checked_report(value: Any, audit: IsolatedEvidenceAudit
                    ) -> tuple[tuple[tuple[str, int], ...], int, int]:
    report = _finite_json(value)
    if type(report) is not dict or set(report) != REPORT_KEYS:
        raise ValueError("child_report_inventory_invalid")
    if (report["version"] != VERSION or report["source_main"] != SOURCE_MAIN
            or report["status"] != SUCCESS):
        raise ValueError("child_report_source_or_status_invalid")
    if (report["wa_numeric_interval_bounds_checked"] is not True
            or report["numeric_values_modified"] is not False
            or report["wa_real_number_refinement_proved"] is not False):
        raise ValueError("child_report_numeric_scope_invalid")
    # Keep the actual older report and its validator intact; do not substitute
    # a report with rewritten source identity or a different native record.
    state_counts, host_count = prior._checked_report(report["mediated_report"], audit)
    numeric_count = report["wa_numeric_guard_calls"]
    if (type(numeric_count) is not int or numeric_count <= 0
            or numeric_count != dict(state_counts)["DecisionOSWa"]):
        raise ValueError("child_report_every_wa_call_requires_numeric_check")
    return state_counts, host_count, numeric_count


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_wa_numeric_sources_v0_13 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("wa_numeric_source_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = core._fresh_root(root)
    _source_preflight()
    counts = {"DecisionOSWa": 0}
    with _guard_numeric_boundary(counts):
        old_report = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    report = _make_child_report(old_report, counts["DecisionOSWa"])
    _checked_report(report, audit)
    return report


def build_wa_numeric_native_fixture(root: Path) -> WaNumericNativeRun:
    """Run the explicit local fixture once in a fresh Python interpreter.

    Preflight requires selected original source bytes and the new inventory.
    No numeric result is repaired or clamped. Failure retains partial output
    and is never retried. This is not a sandbox, a host rollback mechanism,
    an external signature, or a Lean/Python numerical refinement proof.
    """
    root = core._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_wa_numeric_native_cycle_v0_13",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("wa_numeric_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > core.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    state_counts, host_count, numeric_count = _checked_report(report, audit)
    return WaNumericNativeRun(
        status=SUCCESS, state_guard_calls=state_counts,
        pre_host_guard_calls=host_count, wa_numeric_guard_calls=numeric_count,
        native_audit=audit,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("wa_numeric_native_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "WaNumericNativeRun",
    "build_wa_numeric_native_fixture", "audit_local_evidence",
)
