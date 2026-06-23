#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def require_tokens(path: pathlib.Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_52.lean"
    require_tokens(formal, ("WorldVacuumExpectationOSReceiptCompositionBridge",))
    print("obsolete diagnostic branch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
