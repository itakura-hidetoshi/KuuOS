#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_plan_trend_summary_v0_1 import build_qi_process_tensor_probe_plan_trend_summary


def read_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_text(summary) -> str:
    lines = [
        "Qi Process Tensor Probe Plan Trend Summary v0.1",
        f"summary_status: {summary.summary_status}",
        f"dominant_probe_type: {summary.dominant_probe_type or 'UNKNOWN'}",
        f"latest_recommended_probe_type: {summary.latest_recommended_probe_type or 'UNKNOWN'}",
        f"latest_probe_target_time_slice: {summary.latest_probe_target_time_slice or 'UNKNOWN'}",
        f"repeated_probe_types: {', '.join(summary.repeated_probe_types) if summary.repeated_probe_types else 'none'}",
        f"qi_process_tensor_characterization: {summary.qi_process_tensor_characterization}",
        f"trend_interpretation: {summary.trend_interpretation}",
        f"recommended_operator_focus: {summary.recommended_operator_focus}",
        "authority: none",
        "scope: trend-summary-read-only",
    ]
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write KuuOS Qi process tensor trend summary v0.1")
    parser.add_argument("--index", type=pathlib.Path, required=True)
    parser.add_argument("--write-json", type=pathlib.Path, required=True)
    parser.add_argument("--write-text", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = build_qi_process_tensor_probe_plan_trend_summary(artifact_index=read_json(args.index))
    write_json(args.write_json, summary.to_dict())
    text = build_text(summary)
    if args.write_text:
        args.write_text.parent.mkdir(parents=True, exist_ok=True)
        args.write_text.write_text(text, encoding="utf-8")
    if not args.quiet:
        print(text, end="")
    return 0 if summary.summary_status == "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
