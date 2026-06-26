from __future__ import annotations

from runtime.kuuos_capabilityos_qi_world_kernel_v0_60 import STATUS_OK
from runtime.kuuos_capabilityos_qi_world_scenarios_v0_60 import (
    run_capabilityos_qi_world_scenarios,
)


def main() -> int:
    result = run_capabilityos_qi_world_scenarios()
    assert result["ready_route"] == "READY_FOR_PLANOS"
    assert result["plural_route"] == "READY_WITH_WORLD_PLURALITY"
    assert result["saturation_route"] == "CONTAIN_YANG_SATURATION"
    assert result["verifier_route"] == "HOLD_NO_VERIFIER"
    assert result["guard_route"] == "QUARANTINE_GUARD_EVIDENCE"
    assert result["process_route"] == "REOBSERVE_PROCESS"
    assert result["world_route"] == "REOBSERVE_WORLD_PRECONDITION"
    assert result["path_ready"] is False
    assert result["path_support"] == 0
    assert result["world_plurality_preserved"] is True
    assert result["authority_extended"] is False
    print(STATUS_OK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
