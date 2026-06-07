#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


EFFECT_TO_QI = {
    "prefer_stable_continue": "smooth_circulation",
    "prefer_observe_more": "observation_deficiency",
    "prefer_retry_heavy": "retry_stagnation",
    "reduce_autonomy_and_observe": "mixed_turbulence",
    "respect_hold_boundary": "review_constraint",
    "collect_more_outcomes": "observation_deficiency",
}

POLICY_TO_QI = {
    "stable_continue": "smooth_circulation",
    "observe_more": "observation_deficiency",
    "retry_heavy": "retry_stagnation",
    "hold_for_review": "review_constraint",
}


@dataclass(frozen=True)
class QiProcessTensorPolicyCouplerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    qi_state: str
    process_memory_depth: int
    next_policy_bias: str
    coupling_packet_path: str
    receipt_path: str
    audit_path: str
    coupling_packet_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _window(rows: list[dict[str, Any]], depth: int) -> list[dict[str, Any]]:
    return rows[-depth:] if depth > 0 else []


def _votes(effectiveness: Mapping[str, Any], trend: Mapping[str, Any], lifecycle: list[dict[str, Any]], outcomes: list[dict[str, Any]]) -> list[str]:
    votes: list[str] = []
    eff = str(effectiveness.get("effectiveness_hint", ""))
    if eff in EFFECT_TO_QI:
        votes.append(EFFECT_TO_QI[eff])
    pol = str(trend.get("policy_hint", ""))
    if pol in POLICY_TO_QI:
        votes.append(POLICY_TO_QI[pol])
    for row in lifecycle:
        stop = str(row.get("stop_reason", ""))
        ext = str(row.get("external_selected_stage", ""))
        if "blocked" in stop:
            votes.append("review_constraint")
        elif "observation" in stop or ext == "await_external_call":
            votes.append("observation_deficiency")
        elif ext == "await_dispatch_result" or "connector" in stop:
            votes.append("retry_stagnation")
    for row in outcomes:
        outcome = str(row.get("outcome_class", ""))
        hint = str(row.get("policy_hint", ""))
        if outcome == "blocked_or_not_run":
            votes.append("mixed_turbulence")
        elif outcome == "held_by_policy":
            votes.append("review_constraint")
        elif outcome == "runner_completed" and hint == "stable_continue":
            votes.append("smooth_circulation")
    return votes


def _choose(votes: list[str]) -> str:
    if not votes:
        return "observation_deficiency"
    order = ["review_constraint", "mixed_turbulence", "retry_stagnation", "observation_deficiency", "smooth_circulation"]
    counts = {v: votes.count(v) for v in set(votes)}
    return sorted(counts, key=lambda v: (-counts[v], order.index(v) if v in order else 99))[0]


def _bias(state: str) -> str:
    return {
        "smooth_circulation": "stable_continue",
        "observation_deficiency": "observe_more",
        "retry_stagnation": "retry_heavy",
        "review_constraint": "hold_for_review",
        "mixed_turbulence": "observe_more",
    }.get(state, "observe_more")


def _strength(state: str) -> str:
    return {
        "smooth_circulation": "light",
        "observation_deficiency": "moderate_observe",
        "retry_stagnation": "moderate_retry",
        "review_constraint": "hold",
        "mixed_turbulence": "rebalance",
    }.get(state, "moderate_observe")


def _make_packet(effectiveness: Mapping[str, Any], trend: Mapping[str, Any], lifecycle: list[dict[str, Any]], outcomes: list[dict[str, Any]], depth: int) -> dict[str, Any]:
    lw = _window(lifecycle, depth)
    ow = _window(outcomes, depth)
    votes = _votes(effectiveness, trend, lw, ow)
    state = _choose(votes)
    return {
        "version": "qi_process_tensor_policy_coupling_packet_v7_5",
        "qi_process_tensor_considered": True,
        "process_memory_depth": depth,
        "qi_state": state,
        "next_policy_bias": _bias(state),
        "coupling_strength": _strength(state),
        "state_votes": votes,
        "history_digests": {
            "policy_effectiveness": _sha(dict(effectiveness)),
            "lifecycle_trend": _sha(dict(trend)),
            "lifecycle_window": _sha(lw),
            "policy_outcome_window": _sha(ow),
        },
        "boundary": {
            "coupling_only": True,
            "non_markov_history_visible": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_process_tensor_policy_coupler(*, runtime_context: Mapping[str, Any], qi_process_tensor_policy_coupler_license: Mapping[str, Any]) -> QiProcessTensorPolicyCouplerResult:
    ctx = _m(runtime_context)
    lic = _m(qi_process_tensor_policy_coupler_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    effectiveness_path = root / "qi_github_actions_policy_effectiveness_packet.json"
    trend_path = root / "qi_github_actions_lifecycle_trend_packet.json"
    lifecycle_path = root / "qi_github_actions_bridge_lifecycle_ledger.jsonl"
    outcome_path = root / "qi_github_actions_policy_outcome_ledger.jsonl"
    coupling_path = root / "qi_process_tensor_policy_coupling_packet.json"
    receipt_path = root / "qi_process_tensor_policy_coupler_receipt.json"
    audit_path = root / "qi_process_tensor_policy_coupler_audit.jsonl"

    if ctx.get("qi_process_tensor_policy_coupler_enabled") is not True:
        blockers.append("qi_process_tensor_policy_coupler_enabled_not_true")
    if ctx.get("apply_qi_process_tensor_policy_coupler") is not True:
        blockers.append("apply_qi_process_tensor_policy_coupler_not_true")
    if lic.get("license_status") != "QI_PROCESS_TENSOR_POLICY_COUPLER_LICENSE_READY":
        blockers.append("qi_process_tensor_policy_coupler_license_not_ready")
    for name in ["policy_effectiveness_read_allowed", "lifecycle_trend_read_allowed", "lifecycle_ledger_read_allowed", "policy_outcome_ledger_read_allowed", "coupling_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    depth = _i(ctx.get("process_memory_depth", 5), 5)
    if depth < 1:
        blockers.append("process_memory_depth_invalid")
        depth = 0
    if depth > 50:
        warnings.append("process_memory_depth_capped_to_50")
        depth = 50

    effectiveness = _read_json(effectiveness_path)
    trend = _read_json(trend_path)
    lifecycle = _read_jsonl(lifecycle_path)
    outcomes = _read_jsonl(outcome_path)
    if not effectiveness:
        blockers.append("policy_effectiveness_packet_missing_or_invalid")
    if not trend:
        blockers.append("lifecycle_trend_packet_missing_or_invalid")
    if not lifecycle:
        warnings.append("lifecycle_ledger_empty_or_missing")
    if not outcomes:
        warnings.append("policy_outcome_ledger_empty_or_missing")

    packet: dict[str, Any] = {}
    written = False
    state = "unknown"
    bias = "unknown"
    if not blockers:
        packet = _make_packet(effectiveness, trend, lifecycle, outcomes, depth)
        state = str(packet["qi_state"])
        bias = str(packet["next_policy_bias"])
        _write_json(coupling_path, packet)
        written = True

    status = "QI_PROCESS_TENSOR_POLICY_COUPLER_READY" if not blockers else "QI_PROCESS_TENSOR_POLICY_COUPLER_BLOCKED"
    packet_id = "qi-process-tensor-policy-coupler-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_process_tensor_policy_coupler_v7_5",
        "status": status,
        "packet_id": packet_id,
        "qi_state": state,
        "next_policy_bias": bias,
        "process_memory_depth": depth,
        "coupling_packet_written": written,
        "coupling_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiProcessTensorPolicyCouplerResult(
        "kuuos_runtime_daemon_qi_process_tensor_policy_coupler_v7_5",
        status,
        packet_id,
        str(root),
        state,
        depth,
        bias,
        str(coupling_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
