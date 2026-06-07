#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


READY_STATUS = "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY"
BLOCKED_STATUS = "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_BLOCKED"

ALLOWED_STOP_REASONS = {
    "await_dispatch_result",
    "await_external_call",
    "max_bridge_cycles_reached",
    "max_steps_reached",
    "waiting_for_external_observation",
    "waiting_for_connector_operation",
    "internal_loop_blocked",
    "external_bridge_blocked",
    "external_stage_result_unknown",
}

EXTERNAL_TERMINALS = {"await_dispatch_result", "await_external_call"}
LOCAL_EXTERNAL_COMPLETION = "local_external_stage_completed"


@dataclass(frozen=True)
class QiGitHubActionsProofInvariantsResult:
    version: str
    status: str
    packet_id: str
    proof_class: str
    passed_invariants: list[str]
    failed_invariants: list[str]
    receipt_path: str
    audit_path: str
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


def _records(receipt: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = receipt.get("cycle_records", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _ok(name: str, condition: bool, passed: list[str], failed: list[str]) -> None:
    if condition:
        passed.append(name)
    else:
        failed.append(name)


def prove_integrated_bridge_runner_invariants(receipt: Mapping[str, Any]) -> tuple[list[str], list[str], str]:
    passed: list[str] = []
    failed: list[str] = []
    status = str(receipt.get("status", ""))
    stop = str(receipt.get("stop_reason", ""))
    records = _records(receipt)
    blockers = receipt.get("blockers", [])
    blockers_list = blockers if isinstance(blockers, list) else []

    _ok("status_is_known", status in {READY_STATUS, BLOCKED_STATUS}, passed, failed)
    _ok("stop_reason_is_known", stop in ALLOWED_STOP_REASONS, passed, failed)
    _ok("ready_has_no_blockers", status != READY_STATUS or not blockers_list, passed, failed)
    _ok("blocked_has_blocker", status != BLOCKED_STATUS or bool(blockers_list), passed, failed)
    _ok("cycles_equal_records", int(receipt.get("cycles_run", -1)) == len(records), passed, failed)
    _ok("cycles_nonnegative", int(receipt.get("cycles_run", -1)) >= 0, passed, failed)

    indexed = all(int(record.get("index", 0)) == idx for idx, record in enumerate(records, start=1))
    _ok("cycle_indices_are_contiguous", indexed, passed, failed)

    digest_ok = all(bool(record.get("internal_digest")) for record in records)
    _ok("internal_digest_present_per_cycle", digest_ok, passed, failed)

    terminal_consistent = True
    if stop in EXTERNAL_TERMINALS:
        terminal_consistent = bool(records) and str(records[-1].get("external_selected_stage")) == stop
    _ok("external_terminal_matches_last_record", terminal_consistent, passed, failed)

    local_external_ok = True
    for record in records:
        stage = str(record.get("external_selected_stage", "not_run"))
        cls = str(record.get("external_stage_result_class", "not_run"))
        if stage not in {"not_run", "await_dispatch_result", "await_external_call"} and cls != LOCAL_EXTERNAL_COMPLETION:
            local_external_ok = False
            break
    _ok("nonterminal_external_stage_completed", local_external_ok, passed, failed)

    waiting_boundary_ok = True
    for record in records:
        ext = str(record.get("external_selected_stage", "not_run"))
        if ext in EXTERNAL_TERMINALS and str(record.get("external_status")) != "QI_GITHUB_ACTIONS_EXTERNAL_BRIDGE_EXECUTOR_READY":
            waiting_boundary_ok = False
            break
    _ok("external_wait_boundary_ready", waiting_boundary_ok, passed, failed)

    if failed:
        proof_class = "github_actions_integrated_bridge_proof_failed"
    elif stop in EXTERNAL_TERMINALS:
        proof_class = "github_actions_integrated_bridge_wait_boundary_proved"
    else:
        proof_class = "github_actions_integrated_bridge_local_invariants_proved"
    return passed, failed, proof_class


def build_qi_github_actions_proof_invariants(*, runtime_context: Mapping[str, Any], proof_invariant_license: Mapping[str, Any]) -> QiGitHubActionsProofInvariantsResult:
    ctx = _m(runtime_context)
    lic = _m(proof_invariant_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    runner_receipt_path = root / "qi_github_actions_integrated_bridge_runner_receipt.json"
    receipt_path = root / "qi_github_actions_proof_invariants_receipt.json"
    audit_path = root / "qi_github_actions_proof_invariants_audit.jsonl"

    if ctx.get("qi_github_actions_proof_invariants_enabled") is not True:
        blockers.append("qi_github_actions_proof_invariants_enabled_not_true")
    if ctx.get("apply_github_actions_proof_invariants") is not True:
        blockers.append("apply_github_actions_proof_invariants_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PROOF_INVARIANTS_LICENSE_READY":
        blockers.append("github_actions_proof_invariants_license_not_ready")
    for name in ["runner_receipt_read_allowed", "proof_receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    runner_receipt = _read_json(runner_receipt_path)
    if not runner_receipt:
        blockers.append("integrated_bridge_runner_receipt_missing_or_invalid")
    passed: list[str] = []
    failed: list[str] = []
    proof_class = "not_proved"
    if not blockers:
        passed, failed, proof_class = prove_integrated_bridge_runner_invariants(runner_receipt)
        if failed:
            blockers.append("proof_invariants_failed")

    status = "QI_GITHUB_ACTIONS_PROOF_INVARIANTS_READY" if not blockers else "QI_GITHUB_ACTIONS_PROOF_INVARIANTS_BLOCKED"
    packet_id = "qi-github-actions-proof-invariants-" + _sha({"receipt": runner_receipt, "failed": failed, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_proof_invariants_v6_9",
        "status": status,
        "packet_id": packet_id,
        "proof_class": proof_class,
        "passed_invariants": passed,
        "failed_invariants": failed,
        "source_runner_receipt_digest": _sha(runner_receipt),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("proof_receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsProofInvariantsResult(
        "kuuos_runtime_daemon_qi_github_actions_proof_invariants_v6_9",
        status,
        packet_id,
        proof_class,
        passed,
        failed,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
