"""Bound local Decision ledger witness -> Plural -> Wa and native receipt links.

The selected child supplies a real recovered Decision store state. Native receipt
cross-checks run only AFTER v0.9 has issued its original write-once local record.
This cannot authenticate an external issuer, a rewritten genesis or Lean/Python.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any, NoReturn

from runtime import kuuos_lean_python_wa_profile_source_guard_v0_16 as prior
from runtime.kuuos_decision_os_kernel_v0_1 import validate_decision_state
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    RECEIPT_VERSION as BELIEF_RECEIPT_VERSION, receipt_digest as belief_receipt_digest,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    full_cycle_receipt_digest, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    EVIDENCE_KEYS, evidence_digest,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint

VERSION = "kuuos_lean_python_decision_evidence_guard_v0_17"
SOURCE_MAIN = "9e1ce34bdf5f52faac28d741aa34dddda91bcba5"
BLOCKED, NO_DATA = "BLOCKED", "NO_DATA"
_DECISION_PLURAL_FIELDS = {
    "lineage_id": "lineage_id",
    "mission_contract_digest": "mission_contract_digest",
    "source_decision_state_digest": "decision_state_digest",
    "source_decision_basis_digest": "decision_basis_digest",
    "source_committed_decision_digest": "latest_committed_decision_digest",
    "source_route": "route",
    "source_selected_option_id": "selected_option_id",
    "source_option_ids": "admissible_option_ids",
}


class DecisionEvidenceBoundaryError(RuntimeError):
    def __init__(self, status: str, issues: tuple[str, ...]) -> None:
        self.status, self.issues = status, tuple(issues)
        super().__init__(status + ":" + ";".join(self.issues))


def _fail(issue: str, *, status: str = BLOCKED) -> NoReturn:
    raise DecisionEvidenceBoundaryError(status, (issue,))


def _obj(value: Any, label: str) -> dict[str, Any]:
    if value is None:
        _fail(label + ":missing", status=NO_DATA)
    try:
        data = _finite_json(value)
    except Exception as exc:
        _fail(label + ":nonfinite_json:" + type(exc).__name__)
    if type(data) is not dict:
        _fail(label + ":exact_object_required")
    return data


def _required(value: dict[str, Any], key: str, label: str) -> Any:
    if key not in value:
        _fail(label + ":" + key + ":missing", status=NO_DATA)
    return value[key]


def _same(a: Any, b: Any) -> bool:
    return _fingerprint(a) == _fingerprint(b)


def _check_decision_plural(decision: dict[str, Any], plural: dict[str, Any]) -> None:
    """Validate one fixed local committed Decision source and exact native projection.

    This is a content relationship; the native caller must separately recover
    each witness from its real local ledger, not caller-asserted hashes.
    """
    if _required(decision, "current_phase", "decision") != "commit":
        _fail("decision:not_committed")
    supplied = _required(decision, "decision_state_digest", "decision")
    if type(supplied) is not str or supplied != _fingerprint(
        {k: v for k, v in decision.items() if k != "decision_state_digest"}
    ):
        _fail("decision:state_digest_not_canonical")
    frozen = _fingerprint(decision)
    try:
        errors = validate_decision_state(decision)
    except Exception as exc:
        _fail("decision:validator_raised:" + type(exc).__name__)
    if _fingerprint(decision) != frozen or type(errors) is not list or errors:
        _fail("decision:original_validator_rejected_or_mutated")
    for dest, source in _DECISION_PLURAL_FIELDS.items():
        if not _same(_required(plural, dest, "plural"), _required(decision, source, "decision")):
            _fail("plural:" + dest + ":decision_ledger_projection_mismatch")
    ids = _required(decision, "admissible_option_ids", "decision")
    opts = _required(decision, "options", "decision")
    if type(ids) is not list or type(opts) is not list or any(type(x) is not str for x in ids):
        _fail("decision:option_inventory_type_invalid")
    if len(ids) != len(set(ids)):
        _fail("decision:duplicate_admissible_option_id")
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for option in opts:
        if type(option) is not dict:
            _fail("decision:option_object_required")
        option_id = _required(option, "option_id", "decision:option")
        if type(option_id) is not str or not option_id or option_id in seen:
            _fail("decision:option_identity_invalid_or_duplicate")
        seen.add(option_id)
        if option_id in ids:
            selected.append(option)
    if set(ids) != {option["option_id"] for option in selected}:
        _fail("decision:admissible_option_not_found")
    if not _same(_required(plural, "source_options", "plural"), selected):
        _fail("plural:source_options:decision_ledger_projection_mismatch")
    if not _same(_required(plural, "source_options_digest", "plural"), _fingerprint(selected)):
        _fail("plural:source_options_digest:decision_ledger_projection_mismatch")


def checked_apply_wa_decision_evidence_event(
    state: Any, event: Any, source_plural_state: Any, source_decision_state: Any,
) -> dict[str, Any]:
    """Exactly one unchanged v0.16 Wa adapter call after upstream checks."""
    original = _obj(state, "state")
    observed = _obj(event, "event")
    plural = _obj(source_plural_state, "plural")
    decision = _obj(source_decision_state, "decision")
    _check_decision_plural(decision, plural)
    before = _fingerprint([original, observed, plural, decision])
    try:
        outcome = prior.checked_apply_wa_profile_source_event(original, observed, plural)
    except prior.WaProfileSourceBoundaryError as exc:
        raise DecisionEvidenceBoundaryError(
            exc.status if exc.status in (BLOCKED, NO_DATA) else BLOCKED,
            tuple("profile_source:" + issue for issue in exc.issues),
        ) from exc
    except Exception as exc:
        _fail("profile_source_adapter_raised:" + type(exc).__name__)
    if _fingerprint([original, observed, plural, decision]) != before:
        _fail("profile_source_adapter_mutated_arguments")
    return _obj(outcome, "result")


def checked_local_decision_receipt_chain(
    source_decision_state: Any, source_plural_state: Any, evidence_record: Any,
) -> dict[str, str]:
    """Independent read-only postflight link to actual v0.9 native receipt copy.

    The evidence record is local and unsigned; this does not prove that it was
    issued by an external source or that its historical content is truthful.
    """
    decision = _obj(source_decision_state, "decision")
    plural = _obj(source_plural_state, "plural")
    record = _obj(evidence_record, "evidence")
    _check_decision_plural(decision, plural)
    if set(record) != EVIDENCE_KEYS:
        _fail("evidence:unexpected_or_missing_fields",
              status=NO_DATA if EVIDENCE_KEYS - set(record) else BLOCKED)
    if record["record_sha256"] != evidence_digest(record):
        _fail("evidence:local_record_digest_mismatch")
    receipt = _obj(_required(record, "native_cycle_receipt", "evidence"), "native_receipt")
    try:
        problems = validate_native_full_cycle_receipt(receipt)
    except Exception as exc:
        _fail("native_receipt:validator_raised:" + type(exc).__name__)
    if type(problems) is not list or problems:
        _fail("native_receipt:original_validator_rejected")
    digest = _required(receipt, "native_full_cycle_receipt_digest", "native_receipt")
    if (type(digest) is not str or digest != full_cycle_receipt_digest(receipt)
            or digest != record["native_cycle_digest"]):
        _fail("native_receipt:full_cycle_digest_binding_invalid")
    artifacts = _obj(_required(receipt, "native_artifacts", "native_receipt"), "artifacts")
    for name, source in (("DecisionOS", decision), ("DecisionOSPlural", plural)):
        if not _same(_required(artifacts, name, "artifacts"), source):
            _fail("artifacts:" + name + ":recovered_ledger_state_mismatch")
    belief = _obj(_required(artifacts, "BeliefOSReceipt", "artifacts"), "belief_receipt")
    belief_digest = _required(belief, "belief_gerbe_receipt_digest", "belief_receipt")
    if (belief.get("version") != BELIEF_RECEIPT_VERSION or type(belief_digest) is not str
            or belief_digest != belief_receipt_digest(belief)):
        _fail("belief_receipt:local_digest_or_schema_mismatch")
    if _required(decision, "source_belief_receipt_digest", "decision") != belief_digest:
        _fail("decision:source_belief_receipt_digest:receipt_mismatch")
    return {
        "decision_witness_digest": _fingerprint(decision),
        "plural_witness_digest": _fingerprint(plural),
        "native_receipt_digest": digest,
        "belief_receipt_digest": belief_digest,
    }


__all__ = (
    "VERSION", "SOURCE_MAIN", "BLOCKED", "NO_DATA", "DecisionEvidenceBoundaryError",
    "checked_apply_wa_decision_evidence_event", "checked_local_decision_receipt_chain",
)
