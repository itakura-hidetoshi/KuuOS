#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_process_tensor_aware_scheduler_state_v0_2 import step_qi_process_tensor_aware_scheduler_state_v0_2


def read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi process tensor aware scheduler state v0.2")
    parser.add_argument("--scheduler-state", type=pathlib.Path, required=True)
    parser.add_argument("--scheduler-proposal", type=pathlib.Path, required=True)
    parser.add_argument("--process-tensor-metrics", type=pathlib.Path, required=True)
    parser.add_argument("--proposal-reuse", type=pathlib.Path, default=None)
    parser.add_argument("--current-tick", type=int, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = step_qi_process_tensor_aware_scheduler_state_v0_2(
        scheduler_state=read_json(args.scheduler_state),
        scheduler_proposal=read_json(args.scheduler_proposal),
        process_tensor_metrics=read_json(args.process_tensor_metrics),
        current_tick=args.current_tick,
        proposal_reuse=read_json(args.proposal_reuse),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.adjustment_status == "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
