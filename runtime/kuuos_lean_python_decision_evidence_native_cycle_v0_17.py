"""Actual local Decision ledger -> Plural -> Wa -> original receipt v0.17 child.

One fresh, process-isolated native fixture; all original OS stores and return
receipts remain untouched. Postflight audit is read-only, unsigned and local.
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
from runtime import kuuos_lean_python_wa_profile_source_guard_v0_16 as profile
from runtime import kuuos_lean_python_wa_profile_source_native_cycle_v0_16 as prior
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_lean_python_decision_evidence_guard_v0_17 import (
    DecisionEvidenceBoundaryError, checked_apply_wa_decision_evidence_event,
    checked_local_decision_receipt_chain,
)
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_FILE, GOOD, IsolatedEvidenceAudit, MAX_EVIDENCE_BYTES, ROOT,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint

VERSION = "kuuos_lean_python_decision_evidence_native_cycle_v0_17"
SOURCE_MAIN = "9e1ce34bdf5f52faac28d741aa34dddda91bcba5"
SUCCESS = "LOCAL_DECISION_PLURAL_WA_NATIVE_RECEIPT_CHAIN_CHECKED"
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "profile_report", "decision_guard_calls",
    "decision_witness_digest", "native_receipt_digest", "belief_receipt_digest",
    "local_decision_ledger_recovered", "original_native_receipt_checked",
    "external_issuer_authenticated", "lean_python_refinement_proved",
))


@dataclass(frozen=True)
class DecisionEvidenceNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    wa_numeric_guard_calls: int
    wa_gate_guard_calls: int
    wa_evaluation_guard_calls: int
    wa_profile_source_guard_calls: int
    decision_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    plural_witness_digest: str
    decision_witness_digest: str
    native_receipt_digest: str
    belief_receipt_digest: str
    source_main: str = SOURCE_MAIN
    scope: str = "local_decision_plural_wa_and_native_receipt_recovered_chain"
    local_decision_ledger_recovered: bool = True
    original_native_receipt_checked: bool = True
    external_issuer_authenticated: bool = False
    historical_guard_execution_proved: bool = False
    lean_python_refinement_proved: bool = False
    all_store_writes_guarded: bool = False
    state_commit_atomic_with_host: bool = False
    host_rollback_guaranteed: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False
    guard_observation_mode: str = "local_child_stdout_unattested"
    counts_include_recovery_replays: bool = True


def audit_local_evidence(root: Any) -> IsolatedEvidenceAudit:
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_decision_source_boundary(
    root: Path, count: dict[str, int], identity: list[str],
) -> Iterator[None]:
    if (type(count) is not dict or set(count) != {"DecisionOSWa"}
            or type(count["DecisionOSWa"]) is not int or count["DecisionOSWa"] != 0
            or type(identity) is not list or identity != [""]):
        raise ValueError("fresh_decision_witness_counter_required")
    if prior.checked_apply_wa_profile_source_event is not profile.checked_apply_wa_profile_source_event:
        raise ValueError("original_profile_source_boundary_binding_required")
    cached: list[dict[str, Any]] = []

    def guarded(state: Any, event: Any, plural: Any) -> dict[str, Any]:
        if not cached:
            try:
                recovered = DecisionStore(root / "decision").recover(require_snapshot_match=True)
                captured = _finite_json(recovered)
            except Exception as exc:
                raise DecisionEvidenceBoundaryError(
                    "NO_DATA", ("local_decision_recovery_failed:" + type(exc).__name__,)
                ) from exc
            cached.append(captured)
            identity[0] = _fingerprint(captured)
        result = checked_apply_wa_decision_evidence_event(state, event, plural, cached[0])
        count["DecisionOSWa"] += 1
        return result

    with core._replace_binding(prior, "checked_apply_wa_profile_source_event", guarded):
        yield


def _evidence_record(root: Path) -> dict[str, Any]:
    path = root / EVIDENCE_FILE
    if path.is_symlink() or not path.is_file():
        raise ValueError("local_native_evidence_missing_or_nonregular")
    raw = path.read_bytes()
    if not raw or len(raw) > MAX_EVIDENCE_BYTES:
        raise ValueError("local_native_evidence_size_invalid")
    try:
        result = _finite_json(json.loads(raw))
    except Exception as exc:
        raise ValueError("local_native_evidence_json_invalid:" + type(exc).__name__) from exc
    if type(result) is not dict:
        raise ValueError("local_native_evidence_object_required")
    return result


def _postflight(root: Path, audit: IsolatedEvidenceAudit) -> dict[str, str]:
    if audit.status != GOOD:
        raise ValueError("original_native_evidence_audit_not_good")
    decision = DecisionStore(root / "decision").recover(require_snapshot_match=True)
    plural = PluralDecisionStore(root / "plural").recover(require_snapshot_match=True)
    return checked_local_decision_receipt_chain(decision, plural, _evidence_record(root))


def _make_child_report(profile_report: dict[str, Any], count: int,
                       identity: dict[str, str]) -> dict[str, Any]:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "profile_report": _finite_json(profile_report), "decision_guard_calls": count,
        "decision_witness_digest": identity["decision_witness_digest"],
        "native_receipt_digest": identity["native_receipt_digest"],
        "belief_receipt_digest": identity["belief_receipt_digest"],
        "local_decision_ledger_recovered": True,
        "original_native_receipt_checked": True,
        "external_issuer_authenticated": False, "lean_python_refinement_proved": False,
    }


def _checked_report(value: Any, audit: IsolatedEvidenceAudit) -> tuple[Any, ...]:
    report = _finite_json(value)
    if type(report) is not dict or set(report) != REPORT_KEYS:
        raise ValueError("child_report_inventory_invalid")
    if (report["version"] != VERSION or report["source_main"] != SOURCE_MAIN
            or report["status"] != SUCCESS
            or report["local_decision_ledger_recovered"] is not True
            or report["original_native_receipt_checked"] is not True
            or report["external_issuer_authenticated"] is not False
            or report["lean_python_refinement_proved"] is not False):
        raise ValueError("child_report_status_or_scope_invalid")
    old = prior._checked_report(report["profile_report"], audit)
    count = report["decision_guard_calls"]
    if type(count) is not int or count <= 0 or count != old[-2]:
        raise ValueError("child_report_decision_guard_count_invalid")
    for name in ("decision_witness_digest", "native_receipt_digest", "belief_receipt_digest"):
        digest = report[name]
        if (type(digest) is not str or len(digest) != 64
                or any(letter not in "0123456789abcdef" for letter in digest)):
            raise ValueError("child_report_digest_invalid:" + name)
    return (*old, count, report["decision_witness_digest"],
            report["native_receipt_digest"], report["belief_receipt_digest"])


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_decision_evidence_sources_v0_17 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("decision_evidence_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = core._fresh_root(root)
    _source_preflight()
    counters = {"DecisionOSWa": 0}
    witness = [""]
    with _guard_decision_source_boundary(root, counters, witness):
        original = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    identity = _postflight(root, audit)
    if witness[0] != identity["decision_witness_digest"]:
        raise ValueError("child_decision_guard_witness_differs_from_recovered_ledger")
    if original["source_witness_digest"] != identity["plural_witness_digest"]:
        raise ValueError("child_plural_guard_witness_differs_from_recovered_ledger")
    report = _make_child_report(original, counters["DecisionOSWa"], identity)
    _checked_report(report, audit)
    return report


def build_decision_evidence_native_fixture(root: Path) -> DecisionEvidenceNativeRun:
    """Run selected native fixture only in a fresh child; reobserve postflight."""
    root = core._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_decision_evidence_native_cycle_v0_17",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("decision_evidence_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > core.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        child = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    (states, host, numeric, gate, evaluation, profile_count, plural_digest,
     decision_count, decision_digest, receipt_digest, belief_digest) = _checked_report(child, audit)
    identity = _postflight(root, audit)
    expected = {"decision_witness_digest": decision_digest,
                "plural_witness_digest": plural_digest,
                "native_receipt_digest": receipt_digest,
                "belief_receipt_digest": belief_digest}
    if identity != expected:
        raise ValueError("parent_recovered_local_chain_differs_from_child_report")
    return DecisionEvidenceNativeRun(
        status=SUCCESS, state_guard_calls=states, pre_host_guard_calls=host,
        wa_numeric_guard_calls=numeric, wa_gate_guard_calls=gate,
        wa_evaluation_guard_calls=evaluation, wa_profile_source_guard_calls=profile_count,
        decision_guard_calls=decision_count, native_audit=audit,
        plural_witness_digest=plural_digest, decision_witness_digest=decision_digest,
        native_receipt_digest=receipt_digest, belief_receipt_digest=belief_digest,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("decision_evidence_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "DecisionEvidenceNativeRun",
    "build_decision_evidence_native_fixture", "audit_local_evidence",
)
