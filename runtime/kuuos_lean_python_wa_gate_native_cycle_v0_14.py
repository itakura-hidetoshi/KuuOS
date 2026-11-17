"""Wa classification/plurality/gate checks on the isolated native fixture.

Only the v0.13 native module's imported numeric adapter is wrapped in the
explicit local child. The pure numeric adapter, original kernels/stores, and
the existing v0.9 evidence format remain intact. The unchanged nested report
is validated by v0.13, whose numeric count must equal the new gate count.
A later read-only audit does not attest past gate execution.

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
from runtime import kuuos_lean_python_wa_numeric_guard_v0_13 as numeric
from runtime import kuuos_lean_python_wa_numeric_native_cycle_v0_13 as prior
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    IsolatedEvidenceAudit, ROOT,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_lean_python_wa_gate_guard_v0_14 import checked_apply_wa_gate_event

VERSION = "kuuos_lean_python_wa_gate_native_cycle_v0_14"
SOURCE_MAIN = "05693ef17179ebddb974f23021be2e7d352b4fbb"
SUCCESS = "WA_GATE_LOCAL_NATIVE_FIXTURE_CHECKED"
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "numeric_report", "wa_gate_guard_calls",
    "wa_gate_conditions_checked", "numeric_values_modified",
    "wa_evaluation_equivalence_proved",
))


@dataclass(frozen=True)
class WaGateNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    wa_numeric_guard_calls: int
    wa_gate_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    source_main: str = SOURCE_MAIN
    scope: str = "Wa_local_classification_plurality_gate_on_eight_route_native_fixture"
    wa_gate_conditions_checked: bool = True
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
    """Read the original v0.9 evidence without rerunning gate checks."""
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_gate_boundary(counts: dict[str, int]) -> Iterator[None]:
    """Wrap v0.13's imported numeric adapter only inside the fixture context."""
    if (type(counts) is not dict or set(counts) != {"DecisionOSWa"}
            or type(counts["DecisionOSWa"]) is not int or counts["DecisionOSWa"] != 0):
        raise ValueError("fresh_wa_gate_counter_required")
    original = prior.checked_apply_wa_numeric_event
    if original is not numeric.checked_apply_wa_numeric_event:
        raise ValueError("original_numeric_boundary_binding_required")

    def guarded(state: Any, event: Any) -> dict[str, Any]:
        result = checked_apply_wa_gate_event(state, event)
        counts["DecisionOSWa"] += 1
        return result

    with core._replace_binding(prior, "checked_apply_wa_numeric_event", guarded):
        yield


def _make_child_report(numeric_report: dict[str, Any], gate_count: int) -> dict[str, Any]:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "numeric_report": _finite_json(numeric_report),
        "wa_gate_guard_calls": gate_count,
        "wa_gate_conditions_checked": True,
        "numeric_values_modified": False,
        "wa_evaluation_equivalence_proved": False,
    }


def _checked_report(value: Any, audit: IsolatedEvidenceAudit
                    ) -> tuple[tuple[tuple[str, int], ...], int, int, int]:
    report = _finite_json(value)
    if type(report) is not dict or set(report) != REPORT_KEYS:
        raise ValueError("child_report_inventory_invalid")
    if (report["version"] != VERSION or report["source_main"] != SOURCE_MAIN
            or report["status"] != SUCCESS):
        raise ValueError("child_report_source_or_status_invalid")
    if (report["wa_gate_conditions_checked"] is not True
            or report["numeric_values_modified"] is not False
            or report["wa_evaluation_equivalence_proved"] is not False):
        raise ValueError("child_report_gate_scope_invalid")
    # Preserve and validate the actual older report, including its source,
    # evidence identity, all eight state counters and selected pre-host check.
    state_counts, host_count, numeric_count = prior._checked_report(
        report["numeric_report"], audit,
    )
    gate_count = report["wa_gate_guard_calls"]
    if (type(gate_count) is not int or gate_count <= 0 or gate_count != numeric_count):
        raise ValueError("child_report_every_wa_numeric_call_requires_gate_check")
    return state_counts, host_count, numeric_count, gate_count


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_wa_gate_sources_v0_14 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("wa_gate_source_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = core._fresh_root(root)
    _source_preflight()
    counts = {"DecisionOSWa": 0}
    with _guard_gate_boundary(counts):
        old_report = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    report = _make_child_report(old_report, counts["DecisionOSWa"])
    _checked_report(report, audit)
    return report


def build_wa_gate_native_fixture(root: Path) -> WaGateNativeRun:
    """Run the selected local native fixture once in a fresh Python process.

    Failure leaves partial evidence and is not retried. The gate does not
    modify scores or recompute the scoring algorithm. This is not a sandbox,
    external attestation, host rollback, or Python/Lean refinement proof.
    """
    root = core._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_wa_gate_native_cycle_v0_14",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("wa_gate_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > core.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    state_counts, host_count, numeric_count, gate_count = _checked_report(report, audit)
    return WaGateNativeRun(
        status=SUCCESS, state_guard_calls=state_counts,
        pre_host_guard_calls=host_count, wa_numeric_guard_calls=numeric_count,
        wa_gate_guard_calls=gate_count, native_audit=audit,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("wa_gate_native_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "WaGateNativeRun",
    "build_wa_gate_native_fixture", "audit_local_evidence",
)

