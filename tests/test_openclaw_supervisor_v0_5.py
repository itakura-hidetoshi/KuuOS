#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "runtime" / "kuuos_openclaw_supervisor_v0_5.py"
SPEC = importlib.util.spec_from_file_location("kuuos_openclaw_supervisor_v0_5", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class OpenClawSupervisorV05Tests(unittest.TestCase):
    def test_authority_semantics_are_all_non_authoritative(self) -> None:
        semantics = mod.authority_semantics()
        self.assertTrue(semantics)
        self.assertTrue(all(value is False for value in semantics.values()))

    def test_gateway_supervisor_is_loopback_only(self) -> None:
        self.assertEqual(mod.ensure_loopback_gateway_url("ws://127.0.0.1:18789"), "ws://127.0.0.1:18789")
        self.assertEqual(mod.ensure_loopback_gateway_url("ws://localhost:18789"), "ws://localhost:18789")
        with self.assertRaises(RuntimeError):
            mod.ensure_loopback_gateway_url("wss://gateway.example")
        with self.assertRaises(RuntimeError):
            mod.ensure_loopback_gateway_url("ws://user:secret@127.0.0.1:18789")

    def test_plugin_inventory_detection_is_explicit(self) -> None:
        self.assertTrue(mod.plugin_inventory_contains({"plugins": [{"id": "kuuos-control"}]}, "kuuos-control"))
        self.assertFalse(mod.plugin_inventory_contains({"plugins": [{"id": "other"}]}, "kuuos-control"))
        self.assertFalse(mod.plugin_inventory_contains({}, "kuuos-control"))

    def test_commands_are_fixed_argv_not_shell_strings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data"
            paths = mod.Paths(
                repo_root=root,
                data_dir=data,
                control_server=root / "control.py",
                audit_ingest=root / "audit.py",
                event_subscriber=root / "subscriber.mjs",
                event_package=root / "package.json",
                plugin_dir=root / "plugin",
                live_ledger=data / "gateway-event-hints.jsonl",
            )
            args = argparse.Namespace(
                python_bin="python3",
                node_bin="node",
                openclaw_bin="openclaw",
                control_port=8765,
                policy_mode="approval",
                gateway_url="ws://127.0.0.1:18789",
                session_limit=60,
                session_key=["agent:main:main"],
                rpc_timeout_ms=30000,
                audit_limit=500,
                audit_max_pages=20,
            )
            control = mod.control_command(args, paths)
            event = mod.event_command(args, paths)
            audit = mod.audit_command(args, paths)
            self.assertIsInstance(control, list)
            self.assertIsInstance(event, list)
            self.assertIsInstance(audit, list)
            self.assertNotIn("shell=True", " ".join(control + event + audit))
            self.assertIn("--session-key", event)
            self.assertIn("audit.py", " ".join(audit))

    def test_jsonl_reader_only_reads_from_given_offset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            first = {"recordType": "old"}
            path.write_text(json.dumps(first) + "\n", encoding="utf-8")
            offset = path.stat().st_size
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"recordType": "openclaw_gateway_connection_hello"}) + "\n")
            new_offset, records = mod.read_new_jsonl(path, offset)
            self.assertGreater(new_offset, offset)
            self.assertEqual([record["recordType"] for record in records], ["openclaw_gateway_connection_hello"])

    def test_supervisor_receipt_never_acquires_world_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = mod.SupervisorLedger(Path(directory))
            record = ledger.append("test", {"closedLoopReady": True})
            self.assertFalse(record["semantics"]["worldCommitAuthority"])
            self.assertFalse(record["semantics"]["truthPromotionAuthority"])
            self.assertFalse(record["semantics"]["automaticPlanCompletion"])
            self.assertFalse(record["semantics"]["automaticRollback"])


if __name__ == "__main__":
    unittest.main()
