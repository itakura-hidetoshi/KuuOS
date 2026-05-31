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

from runtime.kuuos_runtime_daemon_qi_incident_handoff_packet_v0_1 import build_qi_incident_handoff_packet


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Qi incident handoff packet v0.1")
    parser.add_argument("--alertmanager-payload", type=pathlib.Path, required=True)
    parser.add_argument("--exporter-snapshot", type=pathlib.Path, default=None)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    packet = build_qi_incident_handoff_packet(
        alertmanager_payload=read_json(args.alertmanager_payload),
        exporter_snapshot=read_json(args.exporter_snapshot),
        handoff_context=read_json(args.context),
    )
    payload = packet.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if packet.handoff_status == "QI_INCIDENT_HANDOFF_PACKET_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
