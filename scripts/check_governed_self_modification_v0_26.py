from __future__ import annotations

import json

from runtime.kuuos_governed_self_modification_scenarios_v0_26 import (
    run_governed_self_modification_scenarios,
)


def main() -> None:
    print(
        json.dumps(
            run_governed_self_modification_scenarios(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
