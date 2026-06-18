from __future__ import annotations

from typing import Any

import runtime.kuuos_plan_os_closed_loop_fixture_v0_4 as source_fixture
from runtime.kuuos_plan_os_closed_loop_stage_fixture_v0_4 import (
    committed_learn_after_verify,
    committed_observe_after_effect,
    committed_verify_after_observe,
)


def install_monotone_stage_fixtures() -> None:
    def prepare_observe(*, root: Any, observe_id: str, act_state: dict, **_: Any):
        return None, committed_observe_after_effect(
            root,
            observe_id=observe_id,
            act_state=act_state,
        )

    def prepare_verify(*, root: Any, verify_id: str, observe_state: dict, **_: Any):
        return None, committed_verify_after_observe(
            root,
            verify_id=verify_id,
            observe_state=observe_state,
        )

    def prepare_learn(*, root: Any, learn_id: str, verify_state: dict, **_: Any):
        return None, committed_learn_after_verify(
            root,
            learn_id=learn_id,
            verify_state=verify_state,
        )

    def already_committed(*, state: dict, **_: Any):
        return state, {}

    source_fixture.prepared_assessed_state = prepare_observe
    source_fixture.finish_observe = already_committed
    source_fixture.prepared_corroborated_state = prepare_verify
    source_fixture.finish_verify = already_committed
    source_fixture.prepared_gated_state = prepare_learn
    source_fixture.finish_learn = already_committed
