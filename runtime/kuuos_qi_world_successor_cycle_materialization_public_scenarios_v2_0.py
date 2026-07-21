from __future__ import annotations

# Import the public facade first so the v2.0 core uses the dual-basis
# successor requirement/intake during every scenario build and validation.
from runtime import kuuos_qi_world_successor_cycle_materialization_public_v2_0 as _public
from runtime.kuuos_qi_world_successor_cycle_materialization_scenarios_v2_0 import (
    run_successor_cycle_materialization_scenarios,
)

__all__ = ["run_successor_cycle_materialization_scenarios"]
