#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


KNOWN_EXECUTION_CLASSES = {
    "policy_hold",
    "policy_runner_completed",
    "policy_runner_blocked",
    "not_run",
}

POSITIVE_OUTCOMES = {
    "policy_hold": "held_by_policy",
    "policy_runner_completed": "runner_completed",
}

BLOCKED_OUTCOMES = {
    "policy_runner_blocked",
    "not_run",
}


@dataclass(frozen=True)
class QiGitHubActionsPolicyOutcomeLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    policy_hint: str
    runner_mode: str
    execution_class: str
    outcome_class: str
    outcome_ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    ledger_appended: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _read_last_digest(path: pathlib.Path) -> str:
    if not path.is_file():
        return "GENESIS"
    last = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            last = line
    if not last:
        return "GENESIS"
    try:
        payload = json.loads(last)
    except json.JSONDecodeError:
        return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(payload.get("record_digest", _sha(payload)))


def _classify(policy: Mapping[str, Any], runner: Mapping[str, Any]) -> str:
    execution_class = str(runner.get("execution_class", "not_run"))
    if execution_class in POSITIVE_OUTCOMES:
        return POSITIVE_OUTCOMES[execution_class]
    if execution_class in BLOCKED_OUTCOMES:
        return "blocked_or_not_run"
    if policy.get("hold_required") is True:
        return "hold_policy_not_respected"
    return "unknown_outcome"


def _outcome_record(policy: Mapping[str, Any], runner: Mapping[str, Any], previous_digest: str) -> dict[str, Any]:
    record = {
        "version": "qi_github_actions_policy_outcome_record_v7_3",
        "record_type": "policy_outcome",
        "policy_hint": str(policy.get("policy_hint", "unknown")),
        "runner_mode": str(policy.get("runner_mode", "unknown")),
        "hold_required": policy.get("hold_required") is True,
        "execution_class": str(runner.get("execution_class", "unknown")),
        "runner_status": str(runner.get("status", "unknown")),
        "integrated_runner_status": str(runner.get("integrated_runner_status", "unknown")),
        "integrated_runner_invoked": runner.get("integrated_runner_invoked") is True,
        "outcome_class": _classify(policy, runner),
        "policy_digest": _sha(dict(policy)),
        "runner_receipt_digest": _sha(dict(runner)),
        "prev_record_digest": previous_digest,
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha(record)
    return record


def _summary(record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        "version": "qi_github_actions_policy_outcome_summary_v7_3",
        "policy_hint": str(record.get("policy_hint", "unknown")),
        "runner_mode": str(record.get("runner_mode", "unknown")),
        "execution_class": str(record.get("execution_class", "unknown")),
        "outcome_class": str(record.get("outcome_class", "unknown")),
        "integrated_runner_invoked": record.get("integrated_runner_invoked") is True,
        "record_digest": str(record.get("record_digest", "")),
        "epoch": int(time.time()),
    }
    summary["summary_digest"] = _sha(summary)
    return summary


def build_qi_github_actions_policy_outcome_ledger(*, runtime_context: Mapping[str, Any], outcome_ledger_license: Mapping[str, Any]) -> QiGitHubActionsPolicyOutcomeLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(outcome_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    policy_path = root / "qi_github_actions_lifecycle_policy_packet.json"
    runner_receipt_path = root / "qi_github_actions_policy_aware_runner_receipt.json"
    ledger_path = root / "qi_github_actions_policy_outcome_ledger.jsonl"
    summary_path = root / "qi_github_actions_policy_outcome_summary.json"
    receipt_path = root / "qi_github_actions_policy_outcome_ledger_receipt.json"
    audit_path = root / "qi_github_actions_policy_outcome_ledger_audit.jsonl"

    if ctx.get("qi_github_actions_policy_outcome_ledger_enabled") is not True:
        blockers.append("qi_github_actions_policy_outcome_ledger_enabled_not_true")
    if ctx.get("apply_github_actions_policy_outcome_ledger") is not True:
        blockers.append("apply_github_actions_policy_outcome_ledger_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_OUTCOME_LEDGER_LICENSE_READY":
        blockers.append("github_actions_policy_outcome_ledger_license_not_ready")
    for name in ["policy_packet_read_allowed", "policy_aware_runner_receipt_read_allowed", "outcome_ledger_append_allowed", "summary_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    policy = _read_json(policy_path)
    runner = _read_json(runner_receipt_path)
    if not policy:
        blockers.append("lifecycle_policy_packet_missing_or_invalid")
    if not runner:
        blockers.append("policy_aware_runner_receipt_missing_or_invalid")
    policy_hint = str(policy.get("policy_hint", "unknown")) if policy else "unknown"
    runner_mode = str(policy.get("runner_mode", "unknown")) if policy else "unknown"
    execution_class = str(runner.get("execution_class", "unknown")) if runner else "unknown"
    if runner and str(runner.get("status", "unknown")) not in {"QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_READY", "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_BLOCKED"}:
        blockers.append("policy_aware_runner_receipt_status_invalid")
    if execution_class not in KNOWN_EXECUTION_CLASSES and runner:
        warnings.append("execution_class_not_known")
    if policy and runner and str(runner.get("runner_mode", runner_mode)) != runner_mode:
        blockers.append("runner_mode_mismatch")
    if policy and runner and str(runner.get("policy_hint", policy_hint)) != policy_hint:
        blockers.append("policy_hint_mismatch")

    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    outcome_class = "unknown"
    if not blockers:
        prev = _read_last_digest(ledger_path)
        record = _outcome_record(policy, runner, prev)
        outcome_class = str(record["outcome_class"])
        summary = _summary(record)
        _append_jsonl(ledger_path, record)
        _write_json(summary_path, summary)
        appended = True

    status = "QI_GITHUB_ACTIONS_POLICY_OUTCOME_LEDGER_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_OUTCOME_LEDGER_BLOCKED"
    packet_id = "qi-github-actions-policy-outcome-" + _sha({"policy": policy, "runner": runner, "record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_outcome_ledger_v7_3",
        "status": status,
        "packet_id": packet_id,
        "policy_hint": policy_hint,
        "runner_mode": runner_mode,
        "execution_class": execution_class,
        "outcome_class": outcome_class,
        "ledger_appended": appended,
        "outcome_record_digest": _sha(record),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsPolicyOutcomeLedgerResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_outcome_ledger_v7_3",
        status,
        packet_id,
        str(root),
        policy_hint,
        runner_mode,
        execution_class,
        outcome_class,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
