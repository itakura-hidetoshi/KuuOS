#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_26_reentry_weighting_activation import build_physical_quantum_qi_v13_26_reentry_weighting_activation

def load(path: pathlib.Path):
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", type=pathlib.Path, required=True)
    parser.add_argument("--license", type=pathlib.Path, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    args = parser.parse_args()
    result = build_physical_quantum_qi_v13_26_reentry_weighting_activation(runtime_context=load(args.context), v13_26_reentry_weighting_activation_license=load(args.license))
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result.status.endswith("READY") else 1

if __name__ == "__main__":
    raise SystemExit(main())
