"""Additive MemoryOS v0.2: multiple immutable GitHub source-run observations.

All prior v0.1 observations remain untouched. A directory of independently
named, append-only evidence packets is combined without mutating entries.
"""
from __future__ import annotations
from pathlib import Path

from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed

PATTERN="kuuos_codeai_lean_observations*_v1.json"

def read_observation_directory(directory: str | Path) -> list[dict]:
    root=Path(directory)
    if not root.is_dir():
        raise ValueError("MemoryOS evidence directory unavailable")
    paths=sorted(root.glob(PATTERN))
    if not paths:
        raise ValueError("MemoryOS no immutable evidence observation packets")
    result,seen=[],set()
    for file in paths:
        if file.is_symlink() or not file.is_file():
            raise ValueError("MemoryOS untrusted evidence path")
        records=read_observation_seed(file)
        for case in records:
            if case["id"] in seen:
                raise ValueError("MemoryOS duplicate cross-packet immutable case id")
            seen.add(case["id"])
            result.append(case)
    return result
