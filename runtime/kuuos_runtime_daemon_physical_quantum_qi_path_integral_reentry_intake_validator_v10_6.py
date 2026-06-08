#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


OS_NAMES = ("MemoryOS", "PlanOS", "RunGovernance")
REENTRY_MODES = {"reinforce_path_weight", "open_probe_potential", "add_barrier_potential"}


@dataclass(frozen=True)
class PhysicalQuantumQiPathIntegralReentryIntakeValidatorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    reentry_intake_decision: str
    ready_count: int
    probe_count: int
    barrier_count: int
    reentry_intake_packet_path: str
    receipt_path: str
    audit_path: str
    reentry_intake_packet_written: bool
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


def _os_reentry(packet: Mapping[str, Any], os_name: str) -> Mapping[str, Any]:
    return _m(_m(packet.get("os_reentry")).get(os_name))


def _decision_from_counts(ready: int, probe: int, barrier: int, warnings: list[str]) -> str:
    if barrier > 0:
        return "block"
    if probe > 0 or warnings:
        return "hold"
    return "accept"


def _validate_os(packet: Mapping[str, Any], os_name: str) -> tuple[list[str], list[str], str]:
    blockers: list[str] = []
    warnings: list[str] = []
    item = _os_reentry(packet, os_name)
    if not item:
        blockers.append(f"{os_name.lower()}_reentry_missing")
        return blockers, warnings, "add_barrier_potential"
    mode = str(item.get("reentry_mode", ""))
    if mode not in REENTRY_MODES:
        blockers.append(f"{os_name.lower()}_reentry_mode_invalid")
        mode = "add_barrier_potential"
    boundary = _m(item.get("boundary"))
    effect = _m(item.get("path_integral_effect"))
    if boundary.get("reentry_only") is not True:
        blockers.append(f"{os_name.lower()}_reentry_only_boundary_missing")
    if boundary.get("does_not_execute_path") is not True:
        blockers.append(f"{os_name.lower()}_execute_path_boundary_missing")
    if boundary.get("does_not_authorize_execution") is not True:
        blockers.append(f"{os_name.lower()}_execution_boundary_missing")
    if boundary.get("path_integral_candidate_weighting_only") is not True:
        blockers.append(f"{os_name.lower()}_candidate_weighting_boundary_missing")
    if mode == "reinforce_path_weight" and int(effect.get("path_weight_delta", 0) or 0) <= 0:
        warnings.append(f"{os_name.lower()}_reinforce_weight_nonpositive")
    if mode == "open_probe_potential" and effect.get("probe_potential_required") is not True:
        warnings.append(f"{os_name.lower()}_probe_potential_not_visible")
    if mode == "add_barrier_potential":
        if effect.get("barrier_potential_required") is not True:
            blockers.append(f"{os_name.lower()}_barrier_potential_not_visible")
        if boundary.get("barrier_blocks_ready_weight") is not True:
            blockers.append(f"{os_name.lower()}_barrier_blocks_ready_boundary_missing")
    return blockers, warnings, mode


def _packet(reentry: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    modes: dict[str, str] = {}
    os_decisions: dict[str, dict[str, Any]] = {}
    for os_name in OS_NAMES:
        os_blockers, os_warnings, mode = _validate_os(reentry, os_name)
        modes[os_name] = mode
        blockers.extend(os_blockers)
        warnings.extend(os_warnings)
        os_decisions[os_name] = {
            "decision": "block" if os_blockers or mode == "add_barrier_potential" else ("hold" if os_warnings or mode == "open_probe_potential" else "accept"),
            "reentry_mode": mode,
            "blockers": os_blockers,
            "warnings": os_warnings,
        }
    ready = sum(1 for m in modes.values() if m == "reinforce_path_weight")
    probe = sum(1 for m in modes.values() if m == "open_probe_potential")
    barrier = sum(1 for m in modes.values() if m == "add_barrier_potential")
    decision = "block" if blockers else _decision_from_counts(ready, probe, barrier, warnings)
    return {
        "version": "physical_quantum_qi_path_integral_reentry_intake_decision_packet_v10_6",
        "physical_quantum_qi_path_integral_reentry_intake_considered": True,
        "reentry_intake_decision": decision,
        "os_decisions": os_decisions,
        "counts": {
            "reinforce_path_weight": ready,
            "open_probe_potential": probe,
            "add_barrier_potential": barrier,
        },
        "blockers": blockers,
        "warnings": warnings,
        "source_digests": {"physical_quantum_qi_path_integral_reentry": _sha(dict(reentry))},
        "boundary": {
            "reentry_intake_validation_only": True,
            "does_not_execute_path": True,
            "does_not_run_runner": True,
            "does_not_commit_plan": True,
            "does_not_consume_memory": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
            "barrier_potential_can_only_block_or_probe": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }


def build_physical_quantum_qi_path_integral_reentry_intake_validator(*, runtime_context: Mapping[str, Any], reentry_intake_license: Mapping[str, Any]) -> PhysicalQuantumQiPathIntegralReentryIntakeValidatorResult:
    ctx = _m(runtime_context)
    lic = _m(reentry_intake_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    reentry_path = root / "physical_quantum_qi_path_integral_reentry_packet.json"
    packet_path = root / "physical_quantum_qi_path_integral_reentry_intake_decision_packet.json"
    receipt_path = root / "physical_quantum_qi_path_integral_reentry_intake_validator_receipt.json"
    audit_path = root / "physical_quantum_qi_path_integral_reentry_intake_validator_audit.jsonl"

    if ctx.get("physical_quantum_qi_path_integral_reentry_intake_validator_enabled") is not True:
        blockers.append("physical_quantum_qi_path_integral_reentry_intake_validator_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_path_integral_reentry_intake_validator") is not True:
        blockers.append("apply_physical_quantum_qi_path_integral_reentry_intake_validator_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_VALIDATOR_LICENSE_READY":
        blockers.append("physical_quantum_qi_path_integral_reentry_intake_validator_license_not_ready")
    for name in ["reentry_packet_read_allowed", "reentry_intake_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    reentry = _read_json(reentry_path)
    if not reentry:
        blockers.append("physical_quantum_qi_path_integral_reentry_packet_missing_or_invalid")
    elif reentry.get("physical_quantum_qi_path_integral_reentry_considered") is not True:
        blockers.append("physical_quantum_qi_path_integral_reentry_considered_not_true")
    if reentry and reentry.get("boundary", {}).get("reentry_only") is not True:
        blockers.append("reentry_only_boundary_invalid")
    if reentry and reentry.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("reentry_execution_boundary_invalid")
    if reentry and reentry.get("boundary", {}).get("barrier_potential_can_only_block_or_probe") is not True:
        blockers.append("barrier_potential_boundary_invalid")

    packet: dict[str, Any] = {}
    written = False
    decision = "block"
    ready = probe = barrier = 0
    if not blockers:
        packet = _packet(reentry)
        decision = str(packet["reentry_intake_decision"])
        ready = int(packet["counts"]["reinforce_path_weight"])
        probe = int(packet["counts"]["open_probe_potential"])
        barrier = int(packet["counts"]["add_barrier_potential"])
        _write_json(packet_path, packet)
        written = True

    status = "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_VALIDATOR_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_VALIDATOR_BLOCKED"
    packet_id = "physical-quantum-qi-path-integral-reentry-intake-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_path_integral_reentry_intake_validator_v10_6",
        "status": status,
        "packet_id": packet_id,
        "reentry_intake_decision": decision,
        "ready_count": ready,
        "probe_count": probe,
        "barrier_count": barrier,
        "reentry_intake_packet_written": written,
        "reentry_intake_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return PhysicalQuantumQiPathIntegralReentryIntakeValidatorResult(
        "kuuos_runtime_daemon_physical_quantum_qi_path_integral_reentry_intake_validator_v10_6",
        status,
        packet_id,
        str(root),
        decision,
        ready,
        probe,
        barrier,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
