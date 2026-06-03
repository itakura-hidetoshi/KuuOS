#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_cadence_observability_projection_v0_2.py"


def dump(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def finality() -> dict:
    return {
        "finality_packet_status": "QI_CADENCE_SUPERCHAIN_FINALITY_PACKET_READY",
        "finality_packet_id": "qi-cadence-finality-demo",
        "superchain_root_digest": "superchain-root-demo",
        "source_baseline_packet_id": "qi-cadence-baseline-demo",
        "chain_index_count": 12,
        "finality_confirmed": True,
        "canonical_chain_complete": True,
        "receipt_only_finality_packet": True,
        "no_authority_boundary_preserved": True,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    }


def context(extra: dict | None = None) -> dict:
    value = {
        "cadence_observability_enabled": True,
        "projection_only_required": True,
        "dashboard_projection_only_required": True,
    }
    if extra:
        value.update(extra)
    return value


def run(root: pathlib.Path, name: str, f: dict, c: dict) -> tuple[int, dict, str, dict]:
    fp = root / f"{name}_finality.json"
    cp = root / f"{name}_ctx.json"
    op = root / f"{name}_out.json"
    mp = root / f"{name}.prom"
    dp = root / f"{name}_dashboard.json"
    dump(fp, f)
    dump(cp, c)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--finality", str(fp),
        "--context", str(cp),
        "--write", str(op),
        "--write-prometheus", str(mp),
        "--write-dashboard", str(dp),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    prom = mp.read_text(encoding="utf-8") if mp.is_file() else ""
    dash = load(dp)
    return done.returncode, load(op), prom, dash


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        rc, out, prom, dash = run(root, "ready", finality(), context())
        if rc != 0 or out.get("observability_status") != "QI_CADENCE_OBSERVABILITY_PROJECTION_READY":
            errors.append("ready_failed")
        if out.get("projection_only") is not True or out.get("runtime_control_authority") is not False:
            errors.append("projection_boundary_failed")
        if out.get("finality_confirmed_gauge") != 1 or out.get("scheduler_bypass_gauge") != 0:
            errors.append("gauge_failed")
        if "kuuos_qi_cadence_finality_confirmed" not in prom:
            errors.append("prometheus_missing")
        if dash.get("projection_only") is not True or dash.get("runtime_control_authority") is not False:
            errors.append("dashboard_boundary_failed")

        rc, out, prom, dash = run(root, "control", finality(), context({"request_runtime_control": True}))
        if rc != 1 or out.get("observability_status") != "QI_CADENCE_OBSERVABILITY_PROJECTION_BLOCKED":
            errors.append("control_not_blocked")

        f = finality()
        f["finality_packet_status"] = "NOT_READY"
        rc, out, prom, dash = run(root, "bad_finality", f, context())
        if rc != 1 or out.get("observability_status") != "QI_CADENCE_OBSERVABILITY_PROJECTION_BLOCKED":
            errors.append("bad_finality_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi cadence observability projection check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
