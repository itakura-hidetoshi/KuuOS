"""Selected native v0.18 Belief ledger and receipt evidence boundary.

One original eight-route child and original write-once evidence. The new
Belief->Decision check runs before selected Wa commits. Full local ledger
reconstruction and receipt equality run as child and parent postflight.
Not external issuer authentication, historical attestation or Lean refinement.

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
from runtime import kuuos_lean_python_decision_evidence_native_cycle_v0_17 as prior
from runtime import kuuos_lean_python_decision_evidence_guard_v0_17 as prior_guard
from runtime.kuuos_belief_os_gerbe_store_v0_3 import BeliefGerbeStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_lean_python_belief_receipt_guard_v0_18 import (
    BeliefReceiptBoundaryError, checked_apply_wa_belief_receipt_event,
    checked_local_belief_receipt_chain,
)
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    GOOD, IsolatedEvidenceAudit, ROOT,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint

VERSION = "kuuos_lean_python_belief_receipt_native_cycle_v0_18"
SOURCE_MAIN = "157841103706f31b884bb8d3d691c7cb3d4899c0"
SUCCESS = "LOCAL_BELIEF_GERBE_LEDGER_RECEIPT_DECISION_CHAIN_CHECKED"
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "decision_report", "belief_guard_calls",
    "belief_state_witness_digest", "belief_last_commit_digest",
    "belief_ledger_commit_count", "local_belief_ledger_recovered",
    "local_belief_receipt_replayed", "external_issuer_authenticated",
    "lean_python_refinement_proved",
))


@dataclass(frozen=True)
class BeliefReceiptNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    wa_numeric_guard_calls: int
    wa_gate_guard_calls: int
    wa_evaluation_guard_calls: int
    wa_profile_source_guard_calls: int
    decision_guard_calls: int
    belief_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    plural_witness_digest: str
    decision_witness_digest: str
    native_receipt_digest: str
    belief_receipt_digest: str
    belief_state_witness_digest: str
    belief_last_commit_digest: str
    belief_ledger_commit_count: int
    source_main: str = SOURCE_MAIN
    scope: str = "local_belief_ledger_receipt_replay_and_decision_plural_wa_chain"
    local_belief_ledger_recovered: bool = True
    local_belief_receipt_replayed: bool = True
    historical_guard_execution_proved: bool = False
    external_issuer_authenticated: bool = False
    lean_python_refinement_proved: bool = False
    all_store_writes_guarded: bool = False
    host_rollback_guaranteed: bool = False
    state_commit_atomic_with_host: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False
    guard_observation_mode: str = "local_child_stdout_unattested"


def audit_local_evidence(root: Any) -> IsolatedEvidenceAudit:
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_belief_source_boundary(
    root: Path, counters: dict[str, int], witness_identity: list[str],
) -> Iterator[None]:
    if (type(counters) is not dict or set(counters) != {"DecisionOSWa"}
            or type(counters["DecisionOSWa"]) is not int or counters["DecisionOSWa"] != 0
            or type(witness_identity) is not list or witness_identity != [""]):
        raise ValueError("fresh_belief_source_counter_required")
    if prior.checked_apply_wa_decision_evidence_event is not prior_guard.checked_apply_wa_decision_evidence_event:
        raise ValueError("original_decision_evidence_boundary_binding_required")
    cached: list[dict[str, Any]] = []

    def guarded(state: Any, event: Any, plural: Any, decision: Any) -> dict[str, Any]:
        if not cached:
            try:
                recovered = BeliefGerbeStore(root / "belief").recover(
                    require_snapshot_match=True
                )
                copied = _finite_json(recovered)
            except Exception as exc:
                raise BeliefReceiptBoundaryError(
                    "NO_DATA", ("local_belief_recovery_failed:" + type(exc).__name__,)
                ) from exc
            cached.append(copied)
            witness_identity[0] = _fingerprint(copied)
        result = checked_apply_wa_belief_receipt_event(
            state, event, plural, decision, cached[0],
        )
        counters["DecisionOSWa"] += 1
        return result

    with core._replace_binding(prior, "checked_apply_wa_decision_evidence_event", guarded):
        yield


def _postflight(root: Path, audit: IsolatedEvidenceAudit) -> dict[str, Any]:
    if audit.status != GOOD:
        raise ValueError("original_native_evidence_audit_not_good")
    store = BeliefGerbeStore(root / "belief")
    recovered = store.recover(require_snapshot_match=True)
    genesis = store._read_json(store.genesis_path)
    commits = store._read_ledger()
    decision = DecisionStore(root / "decision").recover(require_snapshot_match=True)
    plural = PluralDecisionStore(root / "plural").recover(require_snapshot_match=True)
    record = prior._evidence_record(root)
    # The v0.17 original postflight and its source/receipt checks are not bypassed.
    preceding = prior._postflight(root, audit)
    identity = checked_local_belief_receipt_chain(
        decision, plural, genesis, commits, recovered, record,
    )
    if any(identity.get(k) != v for k, v in preceding.items()):
        raise ValueError("original_decision_receipt_postflight_mismatch")
    return identity


def _make_child_report(decision_report: dict[str, Any],
                       count: int, identity: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "decision_report": _finite_json(decision_report),
        "belief_guard_calls": count,
        "belief_state_witness_digest": identity["belief_state_witness_digest"],
        "belief_last_commit_digest": identity["belief_last_commit_digest"],
        "belief_ledger_commit_count": identity["belief_ledger_commit_count"],
        "local_belief_ledger_recovered": True,
        "local_belief_receipt_replayed": True,
        "external_issuer_authenticated": False,
        "lean_python_refinement_proved": False,
    }


def _checked_report(value: Any, audit: IsolatedEvidenceAudit) -> tuple[Any, ...]:
    report = _finite_json(value)
    if type(report) is not dict or set(report) != REPORT_KEYS:
        raise ValueError("child_report_inventory_invalid")
    if (report["version"] != VERSION or report["source_main"] != SOURCE_MAIN
            or report["status"] != SUCCESS
            or report["local_belief_ledger_recovered"] is not True
            or report["local_belief_receipt_replayed"] is not True
            or report["external_issuer_authenticated"] is not False
            or report["lean_python_refinement_proved"] is not False):
        raise ValueError("child_report_scope_invalid")
    old = prior._checked_report(report["decision_report"], audit)
    count = report["belief_guard_calls"]
    if type(count) is not int or count <= 0 or count != old[7]:
        raise ValueError("child_report_belief_guard_count_invalid")
    for name in ("belief_state_witness_digest", "belief_last_commit_digest"):
        value = report[name]
        if (type(value) is not str or len(value) != 64
                or any(ch not in "0123456789abcdef" for ch in value)):
            raise ValueError("child_report_digest_invalid:" + name)
    commits = report["belief_ledger_commit_count"]
    if type(commits) is not int or commits <= 0:
        raise ValueError("child_report_belief_commits_invalid")
    return (*old, count, report["belief_state_witness_digest"],
            report["belief_last_commit_digest"], commits)


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_belief_receipt_sources_v0_18 import check_sources
    problems = check_sources(ROOT)
    if problems:
        raise ValueError("belief_receipt_preflight_failed:" + ";".join(problems))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = core._fresh_root(root)
    _source_preflight()
    counters, witness = {"DecisionOSWa": 0}, [""]
    with _guard_belief_source_boundary(root, counters, witness):
        old_report = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    identity = _postflight(root, audit)
    if witness[0] != identity["belief_state_witness_digest"]:
        raise ValueError("child_belief_guard_witness_differs_from_recovered_ledger")
    if old_report["decision_witness_digest"] != identity["decision_witness_digest"]:
        raise ValueError("child_decision_guard_witness_differs_from_recovered_ledger")
    report = _make_child_report(old_report, counters["DecisionOSWa"], identity)
    _checked_report(report, audit)
    return report


def build_belief_receipt_native_fixture(root: Path) -> BeliefReceiptNativeRun:
    root = core._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_belief_receipt_native_cycle_v0_18",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError("belief_receipt_native_child_failed:" + str(completed.returncode) + ":" + detail)
    if len(completed.stdout.encode("utf-8")) > core.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        report = json.loads(completed.stdout)
    except (TypeError, ValueError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    (states, host, numeric, gate, evaluation, profile_count, plural_digest,
     decision_count, decision_digest, native_receipt_digest, belief_receipt_digest,
     belief_count, belief_digest, last_commit, ledger_count) = _checked_report(report, audit)
    identity = _postflight(root, audit)
    expected = {
        "plural_witness_digest": plural_digest,
        "decision_witness_digest": decision_digest,
        "native_receipt_digest": native_receipt_digest,
        "belief_receipt_digest": belief_receipt_digest,
        "belief_state_witness_digest": belief_digest,
        "belief_last_commit_digest": last_commit,
        "belief_ledger_commit_count": ledger_count,
    }
    if identity != expected:
        raise ValueError("parent_recovered_local_belief_chain_differs_from_child")
    return BeliefReceiptNativeRun(
        status=SUCCESS, state_guard_calls=states, pre_host_guard_calls=host,
        wa_numeric_guard_calls=numeric, wa_gate_guard_calls=gate,
        wa_evaluation_guard_calls=evaluation, wa_profile_source_guard_calls=profile_count,
        decision_guard_calls=decision_count, belief_guard_calls=belief_count,
        native_audit=audit, plural_witness_digest=plural_digest,
        decision_witness_digest=decision_digest,
        native_receipt_digest=native_receipt_digest,
        belief_receipt_digest=belief_receipt_digest,
        belief_state_witness_digest=belief_digest,
        belief_last_commit_digest=last_commit,
        belief_ledger_commit_count=ledger_count,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("belief_receipt_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "BeliefReceiptNativeRun",
    "build_belief_receipt_native_fixture", "audit_local_evidence",
)
