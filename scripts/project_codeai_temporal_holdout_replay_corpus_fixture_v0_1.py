#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.build_codeai_temporal_holdout_replay_corpus_fixture_v0_1 import (
    build_fixture,
    project_fixture as _project_fixture,
)


def project_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    return _project_fixture(fixture)


def main() -> int:
    output = Path("examples/codeai_temporal_holdout_replay_corpus_v0_1.json")
    output.write_text(
        json.dumps(project_fixture(build_fixture()), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
