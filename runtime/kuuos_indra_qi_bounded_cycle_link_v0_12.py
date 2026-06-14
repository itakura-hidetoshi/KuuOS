#!/usr/bin/env python3
from __future__ import annotations

import importlib
from typing import Any, Mapping

MODULE_NAME = "runtime.kuuos_runtime_daemon_qi_parent_cycle_reentry_v0_11"


def build_link(request: Mapping[str, Any]) -> dict[str, Any]:
    module = importlib.import_module(MODULE_NAME)
    return {"module_loaded": module is not None}
