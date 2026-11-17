"""Isolated native v0.15 score checks preserving all original v0.14 effects.

Only the v0.14 module's imported pure gate adapter is wrapped in a
fresh child. Local unsigned counters and read-only evidence do not attest
external provenance or historical guard execution.

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
from runtime import kuuos_lean_python_wa_gate_guard_v0_14 as gate
from runtime import kuuos_lean_python_wa_gate_native_cycle_v0_14 as prior
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import IsolatedEvidenceAudit, ROOT
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_lean_python_wa_evaluation_guard_v0_15 import checked_apply_wa_evaluation_event

VERSION = "kuuos_lean_python_wa_evaluation_native_cycle_v0_15"
SOURCE_MAIN = "69bd75f4ae14e912b45f520636ffd8a400067d36"
SUCCESS = "WA_FLOAT_DERIVATION_LOCAL_NATIVE_FIXTURE_CHECKED"
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "gate_report", "wa_evaluation_guard_calls",
    "wa_native_float_derivation_checked", "numeric_values_modified",
    "lean_python_refinement_proved",
))


@dataclass(frozen=True)
class WaEvaluationNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    wa_numeric_guard_calls: int
    wa_gate_guard_calls: int
    wa_evaluation_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    source_main: str = SOURCE_MAIN
    scope: str = "Wa_v03_float_derivation_on_eight_route_native_fixture"
    wa_native_float_derivation_checked: bool = True
    wa_gate_conditions_checked: bool = True
    numeric_values_modified: bool = False
    counts_include_recovery_replays: bool = True
    guard_observation_mode: str = "local_child_stdout_unattested"
    all_store_writes_guarded: bool = False
    wa_real_number_refinement_proved: bool = False
    external_issuer_authenticated: bool = False
    historical_guard_execution_proved: bool = False
    lean_python_refinement_proved: bool = False
    all_effects_prevented_on_any_failure: bool = False
    host_rollback_guaranteed: bool = False
    state_commit_atomic_with_host: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False


def audit_local_evidence(root: Any) -> IsolatedEvidenceAudit:
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_evaluation_boundary(counts: dict[str, int]) -> Iterator[None]:
    if (type(counts) is not dict or set(counts) != {"DecisionOSWa"}
            or type(counts["DecisionOSWa"]) is not int or counts["DecisionOSWa"] != 0):
        raise ValueError("fresh_wa_evaluation_counter_required")
    if prior.checked_apply_wa_gate_event is not gate.checked_apply_wa_gate_event:
        raise ValueError("original_gate_adapter_binding_required")
    def guarded(state: Any, event: Any) -> dict:
        result = checked_apply_wa_evaluation_event(state, event)
        counts["DecisionOSWa"] += 1
        return result
    with core._replace_binding(prior, "checked_apply_wa_gate_event", guarded):
        yield


def _make_child_report(gate_report: dict, count: int) -> dict:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "gate_report": _finite_json(gate_report), "wa_evaluation_guard_calls": count,
        "wa_native_float_derivation_checked": True,
        "numeric_values_modified": False, "lean_python_refinement_proved": False,
    }


def _checked_report(value: Any, audit: IsolatedEvidenceAudit
                    ) -> tuple[tuple[tuple[str, int], ...], int, int, int, int]:
    report = _finite_json(value)
    if type(report) is not dict or set(report) != REPORT_KEYS:
        raise ValueError("child_report_inventory_invalid")
    if (report["version"] != VERSION or report["source_main"] != SOURCE_MAIN
            or report["status"] != SUCCESS):
        raise ValueError("child_report_identity_invalid")
    if (report["wa_native_float_derivation_checked"] is not True
            or report["numeric_values_modified"] is not False
            or report["lean_python_refinement_proved"] is not False):
        raise ValueError("child_report_scope_invalid")
    state_counts, host_count, numeric_count, gate_count = prior._checked_report(
        report["gate_report"], audit,
    )
    count = report["wa_evaluation_guard_calls"]
    if type(count) is not int or count <= 0 or count != gate_count:
        raise ValueError("every_gate_call_must_have_evaluation_check")
    return state_counts, host_count, numeric_count, gate_count, count


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_wa_evaluation_sources_v0_15 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("wa_evaluation_source_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict:
    root = core._fresh_root(root)
    _source_preflight()
    counts = {"DecisionOSWa": 0}
    with _guard_evaluation_boundary(counts):
        gate_report = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    report = _make_child_report(gate_report, counts["DecisionOSWa"])
    _checked_report(report, audit)
    return report


def build_wa_evaluation_native_fixture(root: Path) -> WaEvaluationNativeRun:
    root = core._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_wa_evaluation_native_cycle_v0_15",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("wa_evaluation_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > core.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    state_counts, host_count, numeric_count, gate_count, count = _checked_report(report, audit)
    return WaEvaluationNativeRun(
        status=SUCCESS, state_guard_calls=state_counts,
        pre_host_guard_calls=host_count, wa_numeric_guard_calls=numeric_count,
        wa_gate_guard_calls=gate_count, wa_evaluation_guard_calls=count, native_audit=audit,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("wa_evaluation_native_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = ("VERSION", "SOURCE_MAIN", "SUCCESS", "WaEvaluationNativeRun",
           "build_wa_evaluation_native_fixture", "audit_local_evidence")
