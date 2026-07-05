#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_current_surface_entrypoint_v0_77 import (
    current_surface,
    current_surface_index,
    current_surface_json,
    entrypoint_issues,
    verify_entrypoint,
)


def main() -> int:
    issues = entrypoint_issues()
    if issues:
        print("\n".join(issues))
        return 1
    print(current_surface_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
