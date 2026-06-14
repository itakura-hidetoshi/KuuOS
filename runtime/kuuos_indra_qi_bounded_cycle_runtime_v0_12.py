#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
import shutil
import time
from typing import Any, Mapping

from runtime.kuuos_indra_qi_bounded_cycle_child_stage_v0_12 import run_child_stages
from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import (
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    mapping,
    runner_state_digest,
    sha,
    validate_plan,
)
from runtime.kuuos_indra_qi_bounded_cycle_plans_v0_12 import convergence_reached
from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import (
    append_jsonl,
    read_json,
    restore_root_files,
    restore_tree,
    safe_id,
    snapshot_root_files,
    snapshot_tree,
    validate_license_templates,
    validate_runner_state,
    validate_source_v0_11,
    write_json,
)
from runtime.kuuos_indra_qi_bounded_cycle_tail_v0_12 import build_tail
from runtime.kuuos_indra_qi_bounded_cycle_v0_10_stage_v0_12 import run_v0_10_stage

VERSION = "indra_qi_bounded_generational_cycle_v0_12"
READY = "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_READY"
BLOCKED = "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_BLOCKED"
LICENSE_READY = "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_LICENSE_READY"


@dataclass(frozen=True)
class IndraQiBoundedCycleV0_12Result:
    version: str
    status: str
    packet_id: str
    runner_id: str
    generation_index: int
    completed_generations: int
    runner_status: str
    stop_reason: str
    transaction_committed: bool
    transaction_rolled_back: bool
    runner_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
