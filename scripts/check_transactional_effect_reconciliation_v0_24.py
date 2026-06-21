from __future__ import annotations

import json

from runtime.kuuos_transactional_effect_scenarios_v0_24 import (
    run_transactional_effect_scenarios,
)


def main() -> None:
    print(
        json.dumps(
            run_transactional_effect_scenarios(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
