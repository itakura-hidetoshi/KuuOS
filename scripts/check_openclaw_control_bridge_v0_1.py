#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_openclaw_control_bridge_v0_1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    require(not missing, f"{path}: missing tokens: {missing}")


def main() -> int:
    package = ROOT / "integrations/openclaw/package.json"
    plugin_manifest = ROOT / "integrations/openclaw/openclaw.plugin.json"
    plugin_entry = ROOT / "integrations/openclaw/index.mjs"
    skill = ROOT / "integrations/openclaw/skills/kuuos-control/SKILL.md"
    runtime = ROOT / "runtime/kuuos_openclaw_control_server_v0_1.py"
    docs = ROOT / "docs/KUUOS_OPENCLAW_CONTROL_BRIDGE_v0_1.md"
    manifest_path = ROOT / "manifests/kuuos_openclaw_control_bridge_v0_1.json"

    for path in (package, plugin_manifest, plugin_entry, skill, runtime, docs, manifest_path):
        require(path.is_file(), f"missing required file: {path}")

    package_data = json.loads(package.read_text(encoding="utf-8"))
    require(
        package_data.get("openclaw", {}).get("extensions") == ["./index.mjs"],
        "package.json must expose exactly ./index.mjs as the OpenClaw entry",
    )

    plugin_data = json.loads(plugin_manifest.read_text(encoding="utf-8"))
    require(plugin_data.get("id") == "kuuos-control", "unexpected OpenClaw plugin id")
    schema = plugin_data.get("configSchema", {})
    require(schema.get("additionalProperties") is False, "plugin config must reject unknown keys")
    require(plugin_data.get("activation", {}).get("onStartup") is True, "plugin must activate on startup")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("version") == VERSION, "bridge manifest version mismatch")
    invariants = manifest.get("invariants", {})
    for key in (
        "adapter_invocation_is_world_commit",
        "host_receipt_is_world_truth",
        "automatic_truth_promotion",
        "automatic_plan_completion",
        "automatic_rollback",
    ):
        require(invariants.get(key) is False, f"invariant must remain false: {key}")
    require(invariants.get("effect_recorded_requires_observation") is True, "observation debt missing")
    require(invariants.get("effect_recorded_requires_verification") is True, "verification debt missing")

    require_tokens(
        plugin_entry,
        (
            'api.pluginConfig',
            '"before_tool_call"',
            '"after_tool_call"',
            '"/v1/preflight"',
            '"/v1/post-effect"',
            '"allow-once"',
            '"allow-always"',
            'cfg.failClosed',
            'worldCommit: false',
            'automaticTruthPromotion: false',
        ),
    )

    runtime_text = runtime.read_text(encoding="utf-8")
    ast.parse(runtime_text, filename=str(runtime))
    require_tokens(
        runtime,
        (
            '"/v1/preflight"',
            '"/v1/approval-resolution"',
            '"/v1/post-effect"',
            '"openclaw_preflight"',
            '"openclaw_host_receipt"',
            '"worldCommit": False',
            '"hostReceiptIsWorldTruth": False',
            '"observationRequired": True',
            '"verificationRequired": True',
        ),
    )

    require_tokens(
        docs,
        (
            "DecisionOS / PlanOS",
            "ActOS",
            "before_tool_call",
            "after_tool_call",
            "adapter invocation != WORLD commit",
            "host receipt != WORLD truth",
            "nested effect",
        ),
    )
    require_tokens(
        skill,
        (
            "DecisionOS / PlanOS -> ActOS",
            "Do not bypass a KuuOS block.",
            "observation and verification debt",
        ),
    )

    print(f"{VERSION}: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
