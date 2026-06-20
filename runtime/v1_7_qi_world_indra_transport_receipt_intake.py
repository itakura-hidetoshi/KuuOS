from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_qi_world_indra_transport_receipt_intake_scenarios_v1_7 import (
    run_indra_transport_receipt_intake_scenarios,
)


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-indra-intake-entry-") as temporary:
        result = run_indra_transport_receipt_intake_scenarios()
        result["runtime_root"] = str(Path(temporary))
        return result


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
