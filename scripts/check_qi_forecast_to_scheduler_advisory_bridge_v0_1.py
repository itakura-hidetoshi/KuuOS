#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_forecast_to_scheduler_advisory_bridge_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def forecast(bias: str, cadence: str, risk: str, confidence: float = 1.0) -> dict:
    return {
        "forecast_status": "QI_RHYTHM_TREND_FORECAST_READY",
        "forecast_packet_id": f"forecast-{bias}-{risk}",
        "ledger_root_digest": "ledger-root-demo",
        "source_last_entry_digest": "last-entry-demo",
        "forecast_window_bias": bias,
        "forecast_cadence_mode_hint": cadence,
        "forecast_risk_class": risk,
        "forecast_confidence": confidence,
        "projection_only": True,
        "replaces_ledger_root": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "probe_execution_performed": False,
    }


def ctx(extra: dict | None = None) -> dict:
    value = {
        "forecast_to_scheduler_bridge_enabled": True,
        "advisory_only_required": True,
        "projection_only_required": True,
        "base_min_window_ticks": 1,
        "base_max_window_ticks": 4,
        "absolute_max_window_ticks": 16,
    }
    if extra:
        value.update(extra)
    return value


def run_case(root: pathlib.Path, name: str, packet: dict, context: dict) -> tuple[int, dict]:
    forecast_path = root / f"{name}_forecast.json"
    ctx_path = root / f"{name}_ctx.json"
    out_path = root / f"{name}_out.json"
    dump(forecast_path, packet)
    dump(ctx_path, context)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--forecast", str(forecast_path),
        "--context", str(ctx_path),
        "--write", str(out_path),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(out_path)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, out = run_case(root, "low", forecast("expand_if_low_pressure", "wide_compressed_window", "low"), ctx())
        if rc != 0 or out.get("bridge_status") != "QI_FORECAST_TO_SCHEDULER_ADVISORY_BRIDGE_READY":
            errors.append("low_bridge_not_ready")
        if out.get("advisory_max_window_ticks_hint") != 4 or out.get("advisory_cadence_mode_hint") != "wide_compressed_window":
            errors.append("low_advisory_failed")
        if out.get("forecast_directly_sets_window") is not False or out.get("scheduler_context_patch_authoritative") is not False:
            errors.append("low_authority_boundary_failed")

        rc, out = run_case(root, "contract", forecast("contract_window", "single_tick_high_pressure", "moderate"), ctx())
        if rc != 0 or out.get("advisory_max_window_ticks_hint") > 2:
            errors.append("contract_hint_failed")

        rc, out = run_case(root, "observe", forecast("observe_first", "observe_first_single_tick", "high"), ctx())
        if rc != 0 or out.get("advisory_cadence_mode_hint") != "observe_first_single_tick" or out.get("advisory_max_window_ticks_hint") != 1:
            errors.append("observe_hint_failed")

        rc, out = run_case(root, "full", forecast("full_history_guarded", "full_history_single_tick", "high"), ctx())
        if rc != 0 or out.get("advisory_cadence_mode_hint") != "full_history_single_tick" or out.get("advisory_max_window_ticks_hint") != 1:
            errors.append("full_history_hint_failed")

        rc, out = run_case(root, "freeze", forecast("freeze_guarded", "single_tick_high_pressure", "critical"), ctx())
        if rc != 0 or out.get("advisory_reason") != "critical_or_freeze_forecast" or out.get("advisory_max_window_ticks_hint") != 1:
            errors.append("freeze_hint_failed")

        rc, out = run_case(root, "direct", forecast("expand_if_low_pressure", "wide_compressed_window", "low"), ctx({"request_direct_window_set": True}))
        if rc != 1 or out.get("bridge_status") != "QI_FORECAST_TO_SCHEDULER_ADVISORY_BRIDGE_BLOCKED":
            errors.append("direct_window_set_not_blocked")

        bad = forecast("expand_if_low_pressure", "wide_compressed_window", "low")
        bad["projection_only"] = False
        rc, out = run_case(root, "bad_forecast", bad, ctx())
        if rc != 1 or out.get("bridge_status") != "QI_FORECAST_TO_SCHEDULER_ADVISORY_BRIDGE_BLOCKED":
            errors.append("bad_forecast_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi forecast-to-scheduler advisory bridge check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
