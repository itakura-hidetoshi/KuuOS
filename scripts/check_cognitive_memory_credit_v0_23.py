from __future__ import annotations

import json

from runtime.kuuos_cognitive_memory_credit_scenarios_v0_23 import (
    run_cognitive_memory_credit_scenarios,
)


def main() -> None:
    print(
        json.dumps(
            run_cognitive_memory_credit_scenarios(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
