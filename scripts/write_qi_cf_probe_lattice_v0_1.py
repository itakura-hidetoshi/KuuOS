#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_counterfactual_probe_lattice_v0_1 import build_qi_counterfactual_probe_lattice


def read_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi CF probe lattice v0.1")
    parser.add_argument("--simulation", type=pathlib.Path, required=True)
    parser.add_argument("--summary", type=pathlib.Path, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    lattice = build_qi_counterfactual_probe_lattice(
        dry_run_simulation=read_json(args.simulation),
        trend_summary=read_json(args.summary),
    )
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(lattice.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(lattice.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if lattice.lattice_status == "QI_COUNTERFACTUAL_PROBE_LATTICE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
