#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "runtime" / "kuuos_openclaw_supervisor_v0_5.py"
SPEC = importlib.util.spec_from_file_location("kuuos_openclaw_supervisor_v0_5_serialization_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class OpenClawSupervisorSerializationTests(unittest.TestCase):
    def test_audit_reconciliation_is_single_writer_inside_supervisor(self) -> None:
        state_lock = threading.Lock()
        active = 0
        peak = 0
        original = mod._BASE_RUN_AUDIT_ONCE

        def fake_run(_args, _paths):
            nonlocal active, peak
            with state_lock:
                active += 1
                peak = max(peak, active)
            time.sleep(0.05)
            with state_lock:
                active -= 1
            return {"completedWindow": True}

        mod._BASE_RUN_AUDIT_ONCE = fake_run
        try:
            threads = [
                threading.Thread(target=mod._serialized_run_audit_once, args=(None, None))
                for _ in range(4)
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=2.0)
            self.assertTrue(all(not thread.is_alive() for thread in threads))
            self.assertEqual(peak, 1)
        finally:
            mod._BASE_RUN_AUDIT_ONCE = original

    def test_partial_jsonl_tail_is_deferred_until_newline_arrives(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "gateway-event-hints.jsonl"
            first = {"recordType": "complete"}
            second = {"recordType": "openclaw_gateway_connection_sequence_gap"}
            first_line = json.dumps(first) + "\n"
            second_line = json.dumps(second)
            path.write_text(first_line + second_line[:12], encoding="utf-8")

            offset, records = mod.read_new_jsonl(path, 0)
            self.assertEqual(records, [first])
            self.assertEqual(offset, len(first_line.encode("utf-8")))

            with path.open("a", encoding="utf-8") as handle:
                handle.write(second_line[12:] + "\n")

            new_offset, new_records = mod.read_new_jsonl(path, offset)
            self.assertGreater(new_offset, offset)
            self.assertEqual(new_records, [second])


if __name__ == "__main__":
    unittest.main()
