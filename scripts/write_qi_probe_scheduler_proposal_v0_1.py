#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_probe_scheduler_proposal_v0_1 import build_qi_probe_scheduler_proposal


def read_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi probe scheduler proposal v0.1")
    parser.add_argument("--lattice", type=pathlib.Path, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    proposal = build_qi_probe_scheduler_proposal(counterfactual_lattice=read_json(args.lattice))
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(proposal.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(proposal.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if proposal.scheduler_status == "QI_PROBE_SCHEDULER_PROPOSAL_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
