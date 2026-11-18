"""Local Belief gerbe ledger -> native receipt -> Decision -> Plural -> Wa.

A selected native child supplies a committed local Belief state before Wa and
a quiescent ledger replay after the original write-once native evidence exists.
This does not verify an outside issuer, historical guard use or Lean/Python.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any, NoReturn

from runtime import kuuos_lean_python_decision_evidence_guard_v0_17 as prior
from runtime.kuuos_belief_os_gerbe_store_v0_3 import (
    apply_gerbe_packet, validate_gerbe_state,
)
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    STORE_COMMIT_VERSION, receipt_digest, store_commit_digest,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)

VERSION = "kuuos_lean_python_belief_receipt_guard_v0_18"
SOURCE_MAIN = "157841103706f31b884bb8d3d691c7cb3d4899c0"
BLOCKED = "BLOCKED"
NO_DATA = "NO_DATA"
_COMMIT_FIELDS = frozenset((
    "version", "commit_index", "predecessor_commit_digest",
    "predecessor_gerbe_state_digest", "result_gerbe_state_digest",
    "belief_gerbe_packet_digest", "belief_gerbe_receipt_digest", "packet",
    "belief_gerbe_store_commit_digest",
))


class BeliefReceiptBoundaryError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise BeliefReceiptBoundaryError(status, (issue,))


def _json(value: Any, label: str, kind: type) -> Any:
    if value is None:
        _fail(label + ":missing", status=NO_DATA)
    try:
        copied = _finite_json(value)
    except Exception as exc:
        _fail(label + ":invalid_finite_json:" + type(exc).__name__)
    if type(copied) is not kind:
        _fail(label + ":exact_" + kind.__name__ + "_required")
    return copied


def _need(data: dict[str, Any], key: str, label: str) -> Any:
    if key not in data:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return data[key]


def _equal(a: Any, b: Any) -> bool:
    return _fingerprint(a) == _fingerprint(b)


def _checked_belief_source(belief: dict[str, Any], decision: dict[str, Any]) -> None:
    """Belief's real local recovered state is point-in-time only."""
    frozen = _fingerprint(belief)
    try:
        errors = validate_gerbe_state(belief)
    except Exception as exc:
        _fail("belief:validator_raised:" + type(exc).__name__)
    if type(errors) is not list or errors or _fingerprint(belief) != frozen:
        _fail("belief:original_validator_rejected_or_mutated")
    count = _need(belief, "event_count", "belief")
    history = _need(belief, "receipt_history", "belief")
    if (type(count) is not int or count < 1 or type(history) is not list
            or not history or len(history) != count):
        _fail("belief:committed_receipt_history_required")
    last = _json(history[-1], "belief:last_history", dict)
    latest = _need(belief, "latest_receipt_digest", "belief")
    if (type(latest) is not str or not latest
            or latest != _need(last, "belief_gerbe_receipt_digest", "belief:last_history")):
        _fail("belief:last_history_receipt_mismatch")
    if not _equal(_need(belief, "lineage_id", "belief"),
                  _need(decision, "lineage_id", "decision")):
        _fail("belief:decision_lineage_mismatch")
    if not _equal(latest, _need(decision, "source_belief_receipt_digest", "decision")):
        _fail("belief:decision_source_receipt_mismatch")


def checked_apply_wa_belief_receipt_event(
    state: Any, event: Any, plural: Any, decision: Any, belief: Any,
) -> dict[str, Any]:
    """Verify recovered Belief reference before exactly one unchanged v0.17 call.

    This check is at the selected Wa boundary, not before all prior host/OS
    effects. It does not reconstruct an external issuance certificate.
    """
    args = [
        _json(state, "state", dict), _json(event, "event", dict),
        _json(plural, "plural", dict), _json(decision, "decision", dict),
        _json(belief, "belief", dict),
    ]
    _checked_belief_source(args[4], args[3])
    frozen = _fingerprint(args)
    try:
        outcome = prior.checked_apply_wa_decision_evidence_event(*args[:4])
    except prior.DecisionEvidenceBoundaryError as exc:
        raise BeliefReceiptBoundaryError(
            exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED,
            tuple("decision_evidence:" + issue for issue in exc.issues),
        ) from exc
    except Exception as exc:
        _fail("decision_evidence_adapter_raised:" + type(exc).__name__)
    if _fingerprint(args) != frozen:
        _fail("decision_evidence_adapter_mutated_arguments")
    return _json(outcome, "result", dict)


def _replay_belief_ledger(
    genesis: dict[str, Any], commits: list[Any], recovered: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    """Replay actual local commits with the original Belief kernel, read-only."""
    try:
        errors = validate_gerbe_state(genesis)
    except Exception as exc:
        _fail("belief_genesis:validator_raised:" + type(exc).__name__)
    if type(errors) is not list or errors:
        _fail("belief_genesis:original_validator_rejected")
    if _need(genesis, "event_count", "belief_genesis") != 0:
        _fail("belief_genesis:nonzero_initial_event_count")
    if not commits:
        _fail("belief_ledger:missing_commits", status=NO_DATA)
    current = genesis
    preceding = ""
    last_receipt: dict[str, Any] | None = None
    for number, raw in enumerate(commits, 1):
        label = "belief_ledger:" + str(number)
        commit = _json(raw, label, dict)
        if set(commit) != _COMMIT_FIELDS:
            missing = _COMMIT_FIELDS - set(commit)
            _fail(label + ":missing_fields" if missing else label + ":extra_fields",
                  status=NO_DATA if missing else BLOCKED)
        if (commit["version"] != STORE_COMMIT_VERSION
                or type(commit["commit_index"]) is not int
                or commit["commit_index"] != number):
            _fail(label + ":commit_version_or_index_invalid")
        try:
            calculated_digest = store_commit_digest(commit)
        except Exception as exc:
            _fail(label + ":store_digest_raised:" + type(exc).__name__)
        if commit["belief_gerbe_store_commit_digest"] != calculated_digest:
            _fail(label + ":store_commit_digest_invalid")
        if (commit["predecessor_commit_digest"] != preceding
                or commit["predecessor_gerbe_state_digest"]
                != current["belief_gerbe_state_digest"]):
            _fail(label + ":predecessor_chain_broken")
        packet = _json(commit["packet"], label + ":packet", dict)
        if commit["belief_gerbe_packet_digest"] != _need(
                packet, "belief_gerbe_packet_digest", label + ":packet"):
            _fail(label + ":packet_digest_mismatch")
        before = _fingerprint([current, packet])
        try:
            original = apply_gerbe_packet(current, packet)
        except Exception as exc:
            _fail(label + ":original_apply_raised:" + type(exc).__name__)
        if _fingerprint([current, packet]) != before:
            _fail(label + ":original_kernel_mutated_inputs")
        result = _json(original, label + ":result", dict)
        if _need(result, "status", label + ":result") != "APPLIED":
            _fail(label + ":original_kernel_not_applied")
        receipt = _json(_need(result, "receipt", label + ":result"), label + ":receipt", dict)
        next_state = _json(_need(result, "state", label + ":result"), label + ":next_state", dict)
        try:
            digest = receipt_digest(receipt)
        except Exception as exc:
            _fail(label + ":receipt_digest_raised:" + type(exc).__name__)
        if (digest != _need(receipt, "belief_gerbe_receipt_digest", label + ":receipt")
                or digest != commit["belief_gerbe_receipt_digest"]):
            _fail(label + ":replayed_receipt_not_stored_receipt")
        if _need(next_state, "belief_gerbe_state_digest", label + ":next_state") != commit["result_gerbe_state_digest"]:
            _fail(label + ":result_state_digest_mismatch")
        current = next_state
        preceding = calculated_digest
        last_receipt = receipt
    if not _equal(current, recovered):
        _fail("belief_ledger:replayed_final_state_differs_from_recovered")
    if last_receipt is None:
        _fail("belief_ledger:receipt_missing", status=NO_DATA)
    return last_receipt, preceding


def checked_local_belief_receipt_chain(
    decision_state: Any, plural_state: Any, belief_genesis: Any,
    belief_commits: Any, belief_recovered: Any, evidence_record: Any,
) -> dict[str, Any]:
    """Independently bind real Belief genesis+ledger to the original native receipt.

    Record and ledger are both locally controlled; their consistency is
    not a signature, independent observer or authenticated issuer.
    """
    decision = _json(decision_state, "decision", dict)
    plural = _json(plural_state, "plural", dict)
    genesis = _json(belief_genesis, "belief_genesis", dict)
    commits = _json(belief_commits, "belief_commits", list)
    belief = _json(belief_recovered, "belief", dict)
    record = _json(evidence_record, "evidence", dict)
    _checked_belief_source(belief, decision)
    # Retain the exact v0.17 original receipt/Decision/Plural verification.
    try:
        identity = prior.checked_local_decision_receipt_chain(decision, plural, record)
    except prior.DecisionEvidenceBoundaryError as exc:
        raise BeliefReceiptBoundaryError(
            exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED,
            tuple("decision_evidence:" + issue for issue in exc.issues),
        ) from exc
    last_receipt, last_commit = _replay_belief_ledger(genesis, commits, belief)
    packet = _json(_need(record, "native_cycle_receipt", "evidence"), "native_receipt", dict)
    artifacts = _json(_need(packet, "native_artifacts", "native_receipt"), "artifacts", dict)
    if not _equal(_need(artifacts, "BeliefOSState", "artifacts"), belief):
        _fail("artifacts:BeliefOSState:recovered_ledger_state_mismatch")
    if not _equal(_need(artifacts, "BeliefOSReceipt", "artifacts"), last_receipt):
        _fail("artifacts:BeliefOSReceipt:replayed_ledger_receipt_mismatch")
    if not _equal(_need(belief, "latest_receipt_digest", "belief"),
                  _need(last_receipt, "belief_gerbe_receipt_digest", "last_receipt")):
        _fail("belief:latest_replayed_receipt_mismatch")
    return {
        **identity,
        "belief_state_witness_digest": _fingerprint(belief),
        "belief_last_commit_digest": last_commit,
        "belief_ledger_commit_count": len(commits),
    }


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "BeliefReceiptBoundaryError",
    "checked_apply_wa_belief_receipt_event", "checked_local_belief_receipt_chain",
)
