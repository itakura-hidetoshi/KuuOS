#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_openclaw_gateway_controller_v0_2"

CONTROLLER = ROOT / "runtime/kuuos_openclaw_gateway_controller_v0_2.py"
DOC = ROOT / "docs/KUUOS_OPENCLAW_GATEWAY_CONTROLLER_v0_2.md"
MANIFEST = ROOT / "manifests/kuuos_openclaw_gateway_controller_v0_2.json"
BRIDGE = ROOT / "runtime/kuuos_openclaw_control_server_v0_1.py"
PLUGIN = ROOT / "integrations/openclaw/index.mjs"


def require(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        raise SystemExit(f"{path}: missing required tokens: {missing}")


def main() -> int:
    for path in (CONTROLLER, DOC, MANIFEST, BRIDGE, PLUGIN):
        if not path.is_file():
            raise SystemExit(f"missing required file: {path}")

    ast.parse(CONTROLLER.read_text(encoding="utf-8"), filename=str(CONTROLLER))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        raise SystemExit("manifest version mismatch")

    require(
        CONTROLLER,
        (
            '"agent"',
            '"agent.wait"',
            '"sessions.abort"',
            '"sessions.list"',
            '"/v1/preflight"',
            '"/v1/approval-resolution"',
            '"allow-once"',
            '"worldCommitAuthority": False',
            '"truthPromotionAuthority": False',
            "gateway-controller-receipts.jsonl",
        ),
    )
    require(
        DOC,
        (
            "KuuOS OpenClaw Gateway Controller v0.2",
            "agent.wait timeout != run failure",
            "Gateway run terminal ok != WORLD truth",
            "KuuOS -> OpenClaw",
            "OpenClaw -> KuuOS",
        ),
    )
    require(
        BRIDGE,
        (
            '"/v1/preflight"',
            '"/v1/approval-resolution"',
            '"worldCommitAuthority": False',
            '"truthPromotionAuthority": False',
        ),
    )
    require(
        PLUGIN,
        (
            '"before_tool_call"',
            '"after_tool_call"',
            'worldCommit: false',
            'automaticTruthPromotion: false',
        ),
    )

    print(f"{VERSION}: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
