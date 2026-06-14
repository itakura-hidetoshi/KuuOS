#!/usr/bin/env python3
from __future__ import annotations

import importlib
from typing import Any, Mapping

MODULE_NAME = "runtime.kuuos_runtime_daemon_qi_parent_cycle_reentry_v0_11"
ENTRYPOINT_NAME = "build_indra_qi_parent_cycle_assimilation_reentry_v0_11"


def make_request(
    *,
    runtime_root: str,
    loop_plan: Mapping[str, Any],
    loop_license: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "runtime_context": {
            "runtime_root": runtime_root,
            "indra_qi_parent_cycle_assimilation_reentry_v0_11_enabled": True,
            "apply_indra_qi_parent_cycle_assimilation_reentry_v0_11": True,
        },
        "loop_plan": dict(loop_plan),
        "loop_license": dict(loop_license),
    }


def build_link(request: Mapping[str, Any]) -> dict[str, Any]:
    module = importlib.import_module(MODULE_NAME)
    entrypoint = getattr(module, ENTRYPOINT_NAME)
    result = entrypoint(**dict(request))
    return result.to_dict()


compose = make_request
run = build_link
