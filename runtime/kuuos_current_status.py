#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_current_status_resolver_v0_71 import (
    resolved_status,
    resolved_status_json,
    resolver_issues,
    verify_resolver,
)


def main() -> int:
    issues = resolver_issues()
    if issues:
        print("\n".join(issues))
        return 1
    print(resolved_status_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
