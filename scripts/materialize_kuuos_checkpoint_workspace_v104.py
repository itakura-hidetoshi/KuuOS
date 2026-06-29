#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime.v104_workspace_export import (
    materialize_repository_checkpoint_evolution_workspace,
)
from runtime.v104_workspace_serialization import (
    repository_checkpoint_evolution_workspace_from_dict,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_json")
    parser.add_argument("destination")
    args = parser.parse_args()
    payload = json.loads(Path(args.workspace_json).read_text(encoding="utf-8"))
    workspace = repository_checkpoint_evolution_workspace_from_dict(payload)
    written = materialize_repository_checkpoint_evolution_workspace(
        workspace,
        args.destination,
    )
    print(
        json.dumps(
            {
                "workspace_digest": workspace.workspace_digest,
                "tree_digest": workspace.tree_digest,
                "destination": str(Path(args.destination)),
                "written_paths": list(written),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
