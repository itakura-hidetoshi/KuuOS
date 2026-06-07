#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


TREND_TO_POLICY_HINT = {
    "stable_continue": "stable_continue",
    "observe_more": "observe_more",
    "retry_heavy": "retry_heavy",
    "hold_for_review": "hold_for_review",
}

EFFECTIVENESS_TO_POLICY_HINT = {
    "prefer_stable_continue": "stable_continue",
    "prefer_observe_more": "observe_more",
    "prefer_retry_heavy": "retry_heavy",
    "respect_hold_boundary": "hold_for_review",
    "reduce_autonomy_and_observe": "observe_more",
    "collect_more_outcomes": "observe_more",
}

ALLOWED_POLICY_HINTS = {
    "stable_continue",
    "observe_more",
    "retry_heavy",
    "hold_for_review",
}


@dataclass(frozen=True)
class QiGitHubActionsEffectivenessGuidedPolicyTunerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    trend_policy_hint: str
    effectiveness_hint: str
    tuned_policy_hint: str
    tuning_reason: str
    tuning_packet_path: str
    receipt_path: str
    audit_path: str
    tuning_packet_written: bool
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


def _effectiveness_policy(effectiveness_hint: str) -> str:
    return EFFECTIVENESS_TO_POLICY_HINT.get(effectiveness_hint, "observe_more")


def _trend_policy(trend_hint: str) -> str:
    return TREND_TO_POLICY_HINT.get(trend_hint, "observe_more")


def _tune(trend_packet: Mapping[str, Any], effectiveness_packet: Mapping[str, Any]) -> tuple[str, str]:
    trend_hint = str(trend_packet.get("policy_hint", "observe_more"))
    trend_policy = _trend_policy(trend_hint)
    eff_hint = str(effectiveness_packet.get("effectiveness_hint", "collect_more_outcomes"))
    eff_policy = _effectiveness_policy(eff_hint)
    records_used = int(effectiveness_packet.get("records_used", 0) or 0)
    if eff_hint == "respect_hold_boundary":
        return "hold_for_review", "effectiveness_hold_boundary_dominates"
    if eff_hint == "reduce_autonomy_and_observe":
        return "observe_more", "effectiveness_reduce_autonomy_dominates"
    if records_used < 2:
        return trend_policy, "trend_used_due_to_low_effectiveness_support"
    if trend_policy == eff_policy:
        return trend_policy, "trend_and_effectiveness_agree"
    if eff_hint in {"prefer_stable_continue", "prefer_observe_more", "prefer_retry_heavy"} and records_used >= 3:
        return eff_policy, "effectiveness_supported_override"
    return trend_policy, "trend_preserved_under_weak_effectiveness"


def _packet(trend: Mapping[str, Any], effectiveness: Mapping[str, Any], tuned: str, reason: str) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_effectiveness_guided_policy_tuning_packet_v7_5",
        "trend_policy_hint": str(trend.get("policy_hint", "observe_more")),
        "effectiveness_hint": str(effectiveness.get("effectiveness_hint", "collect_more_outcomes")),
        "tuned_policy_hint": tuned,
        "tuning_reason": reason,
        "effectiveness_records_used": int(effectiveness.get("records_used", 0) or 0),
        "trend_records_used": int(trend.get("records_used", 0) or 0),
        "source_trend_digest": _sha(dict(trend)),
        "source_effectiveness_digest": _sha(dict(effectiveness)),
        "boundary": {
            "advisory_tuning_only": True,
            "does_not_run_policy_applier": True,
            "does_not_run_github_connector": True,
            "hold_boundary_may_tighten": tuned == "hold_for_review",
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_effectiveness_guided_policy_tuner(*, runtime_context: Mapping[str, Any], policy_tuner_license: Mapping[str, Any]) -> QiGitHubActionsEffectivenessGuidedPolicyTunerResult:
    ctx = _m(runtime_context)
    lic = _m(policy_tuner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    trend_path = root / "qi_github_actions_lifecycle_trend_packet.json"
    effectiveness_path = root / "qi_github_actions_policy_effectiveness_packet.json"
    tuning_path = root / "qi_github_actions_effectiveness_guided_policy_tuning_packet.json"
    receipt_path = root / "qi_github_actions_effectiveness_guided_policy_tuner_receipt.json"
    audit_path = root / "qi_github_actions_effectiveness_guided_policy_tuner_audit.jsonl"

    if ctx.get("qi_github_actions_effectiveness_guided_policy_tuner_enabled") is not True:
        blockers.append("qi_github_actions_effectiveness_guided_policy_tuner_enabled_not_true")
    if ctx.get("apply_github_actions_effectiveness_guided_policy_tuner") is not True:
        blockers.append("apply_github_actions_effectiveness_guided_policy_tuner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_EFFECTIVENESS_GUIDED_POLICY_TUNER_LICENSE_READY":
        blockers.append("github_actions_effectiveness_guided_policy_tuner_license_not_ready")
    for name in ["trend_packet_read_allowed", "effectiveness_packet_read_allowed", "tuning_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    trend = _read_json(trend_path)
    effectiveness = _read_json(effectiveness_path)
    if not trend:
        blockers.append("lifecycle_trend_packet_missing_or_invalid")
    if not effectiveness:
        blockers.append("policy_effectiveness_packet_missing_or_invalid")
    trend_hint = str(trend.get("policy_hint", "unknown")) if trend else "unknown"
    effectiveness_hint = str(effectiveness.get("effectiveness_hint", "unknown")) if effectiveness else "unknown"
    if trend and _trend_policy(trend_hint) not in ALLOWED_POLICY_HINTS:
        blockers.append("trend_policy_hint_not_tunable")
    if effectiveness and _effectiveness_policy(effectiveness_hint) not in ALLOWED_POLICY_HINTS:
        blockers.append("effectiveness_hint_not_tunable")

    packet: dict[str, Any] = {}
    tuned = "unknown"
    reason = "not_run"
    written = False
    if not blockers:
        tuned, reason = _tune(trend, effectiveness)
        packet = _packet(trend, effectiveness, tuned, reason)
        _write_json(tuning_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_EFFECTIVENESS_GUIDED_POLICY_TUNER_READY" if not blockers else "QI_GITHUB_ACTIONS_EFFECTIVENESS_GUIDED_POLICY_TUNER_BLOCKED"
    packet_id = "qi-github-actions-policy-tuner-" + _sha({"trend": trend, "effectiveness": effectiveness, "packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_effectiveness_guided_policy_tuner_v7_5",
        "status": status,
        "packet_id": packet_id,
        "trend_policy_hint": trend_hint,
        "effectiveness_hint": effectiveness_hint,
        "tuned_policy_hint": tuned,
        "tuning_reason": reason,
        "tuning_packet_written": written,
        "tuning_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsEffectivenessGuidedPolicyTunerResult(
        "kuuos_runtime_daemon_qi_github_actions_effectiveness_guided_policy_tuner_v7_5",
        status,
        packet_id,
        str(root),
        trend_hint,
        effectiveness_hint,
        tuned,
        reason,
        str(tuning_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
