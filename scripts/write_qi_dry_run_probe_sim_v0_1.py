#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_dry_run_probe_simulator_v0_1 import build_qi_dry_run_probe_simulation


def read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Write Qi dry-run probe simulation v0.1")
    p.add_argument("--license", type=pathlib.Path, required=True)
    p.add_argument("--summary", type=pathlib.Path, required=True)
    p.add_argument("--plan", type=pathlib.Path, default=None)
    p.add_argument("--write", type=pathlib.Path, required=True)
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)
    sim = build_qi_dry_run_probe_simulation(
        license_candidate=read_json(args.license),
        trend_summary=read_json(args.summary),
        probe_plan=read_json(args.plan) if args.plan else None,
    )
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(sim.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(sim.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if sim.simulation_status == "QI_DRY_RUN_PROBE_SIMULATION_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
