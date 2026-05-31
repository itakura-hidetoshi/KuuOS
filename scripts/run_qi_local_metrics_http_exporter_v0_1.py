#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_local_metrics_http_exporter_v0_1 import (
    build_qi_local_metrics_http_exporter_snapshot,
    render_metrics_http_response,
)


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Qi local metrics HTTP exporter snapshot v0.1")
    parser.add_argument("--metrics-file", type=pathlib.Path, required=True)
    parser.add_argument("--health-report", type=pathlib.Path, default=None)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--write-response", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    snapshot = build_qi_local_metrics_http_exporter_snapshot(
        metrics_file_path=args.metrics_file,
        health_report_path=args.health_report,
        exporter_context=read_json(args.context),
    )
    payload = snapshot.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_response is not None:
        args.write_response.parent.mkdir(parents=True, exist_ok=True)
        response = render_metrics_http_response(snapshot)
        args.write_response.write_text(json.dumps(response, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if snapshot.exporter_status == "QI_LOCAL_METRICS_HTTP_EXPORTER_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
