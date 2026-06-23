#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    paths = (
        ROOT / "formal/KuuOSActOSV0_4.lean",
        ROOT / "formal/KUOS/ActOS/VacuumExpectationBoundedAdapterInvocationV0_4.lean",
        ROOT / "docs/KUUOS_ACTOS_BOUNDED_ADAPTER_INVOCATION_v0_4.md",
        ROOT / "manifests/kuuos_actos_bounded_adapter_invocation_v0_4.json",
        ROOT / ".github/workflows/actos-bounded-invocation-v0-4.yml",
    )
    for path in paths:
        require(path.is_file(), f"missing file: {path}")
    print("ActOS v0.4 registration files present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
