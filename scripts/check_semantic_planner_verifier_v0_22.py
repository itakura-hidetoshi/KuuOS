from __future__ import annotations

import json

from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    run_semantic_planner_verifier_scenarios,
)


def main() -> None:
    print(
        json.dumps(
            run_semantic_planner_verifier_scenarios(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
