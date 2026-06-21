#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "kuuos_operational_agent_controller_v1_1.json"


def main() -> int:
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert value["version"] == "kuuos_operational_agent_controller_v1_1"
    assert value["base"] == "kuuos_adaptive_agent_reference_architecture_v1_0"
    assert value["lineage_mode"] == "additive_only"
    assert value["same_root_required"] is True
    assert value["fail_closed"] is True
    assert value["controller_owns_ordering_only"] is True
    assert value["external_commit_supported"] is False
    for path in value["runtime_files"] + value["validation_files"]:
        assert (ROOT / path).is_file(), path
    print("PASS: Operational Agent Controller v1.1 manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
