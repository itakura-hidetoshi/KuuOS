#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_rhythm_trend_forecast_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def write_ledger(path: pathlib.Path, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in entries), encoding="utf-8")


def entry(idx: int, pressure: float, stability: float, recommended: int, completed: int, stop: str, cadence: str = "wide_compressed_window") -> dict:
    digest = f"demo-{idx}"
    prior = f"demo-{idx-1}" if idx > 1 else None
    payload = {
        "entry_digest": digest,
        "ledger_version": "kuuos_runtime_daemon_qi_append_only_rhythm_receipt_ledger_v0_1",
        "rhythm_stability_score": stability,
        "source_candidate": {
            "cadence_mode": cadence,
            "delegated_completed_tick_count": completed,
            "delegated_stop_reason": stop,
            "process_tensor_pressure_score": pressure,
            "recommended_window_ticks": recommended,
            "rhythm_bias": "expand_if_low_pressure",
            "rhythm_mode": "stable_expansion",
        },
    }
    if prior:
        payload["prev_entry_digest"] = prior
    return payload


def ctx(extra: dict | None = None) -> dict:
    value = {
        "rhythm_trend_forecast_enabled": True,
        "read_only_forecast": True,
        "projection_only_required": True,
        "trend_window_size": 4,
    }
    if extra:
        value.update(extra)
    return value


def run_case(root: pathlib.Path, name: str, entries: list[dict], context: dict) -> tuple[int, dict]:
    ledger = root / f"{name}_ledger.jsonl"
    out = root / f"{name}_out.json"
    cpath = root / f"{name}_ctx.json"
    write_ledger(ledger, entries)
    dump(cpath, context)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--ledger", str(ledger),
        "--context", str(cpath),
        "--write", str(out),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(out)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        stable = [entry(1, 0.10, 0.85, 4, 4, "window_completed"), entry(2, 0.12, 0.90, 4, 4, "window_completed"), entry(3, 0.14, 0.92, 4, 4, "window_completed")]
        rc, out = run_case(root, "stable", stable, ctx())
        if rc != 0 or out.get("forecast_status") != "QI_RHYTHM_TREND_FORECAST_READY":
            errors.append("stable_forecast_not_ready")
        if out.get("forecast_window_bias") != "expand_if_low_pressure" or out.get("forecast_cadence_mode_hint") != "wide_compressed_window":
            errors.append("stable_forecast_failed")
        if out.get("projection_only") is not True or out.get("replaces_ledger_root") is not False:
            errors.append("stable_projection_boundary_failed")

        rising = [entry(1, 0.25, 0.70, 4, 4, "window_completed"), entry(2, 0.50, 0.65, 4, 3, "window_completed"), entry(3, 0.80, 0.55, 4, 2, "window_completed")]
        rc, out = run_case(root, "rising", rising, ctx())
        if rc != 0 or out.get("pressure_trend") != "pressure_rising" or out.get("forecast_window_bias") != "contract_window":
            errors.append("rising_pressure_contract_failed")

        observe = [entry(1, 0.30, 0.60, 2, 0, "process_tensor_observe_required", "observe_first_single_tick"), entry(2, 0.35, 0.55, 2, 0, "process_tensor_observe_required", "observe_first_single_tick"), entry(3, 0.25, 0.70, 2, 1, "window_completed")]
        rc, out = run_case(root, "observe", observe, ctx())
        if rc != 0 or out.get("forecast_window_bias") != "observe_first" or out.get("forecast_cadence_mode_hint") != "observe_first_single_tick":
            errors.append("observe_forecast_failed")

        full = [entry(1, 0.55, 0.50, 1, 0, "process_tensor_full_history_required", "full_history_single_tick"), entry(2, 0.60, 0.48, 1, 0, "process_tensor_full_history_required", "full_history_single_tick"), entry(3, 0.45, 0.60, 1, 1, "window_completed")]
        rc, out = run_case(root, "full", full, ctx())
        if rc != 0 or out.get("forecast_window_bias") != "full_history_guarded" or out.get("forecast_cadence_mode_hint") != "full_history_single_tick":
            errors.append("full_history_forecast_failed")

        freeze = [entry(1, 0.90, 0.20, 1, 0, "freeze_required", "single_tick_high_pressure"), entry(2, 0.85, 0.25, 1, 0, "freeze_required", "single_tick_high_pressure"), entry(3, 0.40, 0.60, 1, 1, "window_completed")]
        rc, out = run_case(root, "freeze", freeze, ctx())
        if rc != 0 or out.get("forecast_window_bias") != "freeze_guarded" or out.get("forecast_risk_class") != "critical":
            errors.append("freeze_forecast_failed")

        rc, out = run_case(root, "empty", [], ctx())
        if rc != 1 or out.get("forecast_status") != "QI_RHYTHM_TREND_FORECAST_BLOCKED":
            errors.append("empty_ledger_not_blocked")

        rc, out = run_case(root, "replace_root", stable, ctx({"replace_ledger_root": True}))
        if rc != 1 or out.get("forecast_status") != "QI_RHYTHM_TREND_FORECAST_BLOCKED":
            errors.append("replace_root_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi rhythm trend forecast check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
