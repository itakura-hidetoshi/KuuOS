from __future__ import annotations

import json
from pathlib import Path

from scripts.build_codeai_environment_capsule_livelock_efficiency_gate_fixture_v0_1 import build_reference_fixture
from scripts.project_codeai_environment_capsule_livelock_efficiency_gate_fixture_v0_1 import project_fixture

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_environment_capsule_livelock_efficiency_gate_v0_1.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_environment_capsule_livelock_efficiency_gate_v0_1.json"


def main() -> int:
    fixture = build_reference_fixture()
    projection = project_fixture(fixture)
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if example != projection:
        raise SystemExit("example projection mismatch")
    if manifest != projection:
        raise SystemExit("manifest projection mismatch")
    print(json.dumps(projection, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
