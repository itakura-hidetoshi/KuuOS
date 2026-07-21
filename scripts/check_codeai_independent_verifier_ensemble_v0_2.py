from __future__ import annotations

import json
from pathlib import Path

from scripts.project_codeai_independent_verifier_ensemble_fixture_v0_2 import project

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_independent_verifier_ensemble_v0_2.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_independent_verifier_ensemble_v0_2.json"


def main() -> None:
    expected = project()
    actual = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    if actual != expected:
        raise SystemExit("compact projection mismatch")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    required = {
        "profile": "CodeAI Independent Verifier Ensemble v0.2",
        "source_commit_sha": expected["source_commit_sha"],
        "reference_ensemble_digest": expected["ensemble_digest"],
        "reference_receipt_digest": expected["receipt_digest"],
        "reference_verifier_count": 4,
        "reference_pass_quorum": 3,
        "critical_failure_overrides_quorum": True,
        "conflict_requires_hold": True,
    }
    for key, value in required.items():
        if manifest.get(key) != value:
            raise SystemExit(f"manifest mismatch: {key}")
    print("independent verifier ensemble v0.2: ok")


if __name__ == "__main__":
    main()
