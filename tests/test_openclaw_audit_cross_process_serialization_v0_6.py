#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3.py"
SPEC = importlib.util.spec_from_file_location("kuuos_openclaw_audit_observation_ingest_v0_3", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class OpenClawAuditCrossProcessSerializationTests(unittest.TestCase):
    def test_public_v03_api_is_retained(self) -> None:
        self.assertEqual(mod.VERSION, "kuuos_openclaw_audit_observation_ingest_v0_3")
        self.assertEqual(mod.SERIALIZATION_VERSION, "kuuos_openclaw_audit_cross_process_serialization_v0_6")
        self.assertIs(mod._IMPL.sync, mod.sync)
        self.assertIs(mod._IMPL.status, mod.status)
        self.assertTrue(callable(mod.project_event))
        self.assertTrue(callable(mod.query_digest))

    def test_same_data_dir_is_exclusive_across_processes_and_crash_released(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_dir = Path(directory)
            ready = data_dir / "holder-ready"
            child_code = r'''
import importlib.util
import sys
import time
from pathlib import Path
module_path = Path(sys.argv[1])
data_dir = Path(sys.argv[2])
ready = Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("kuuos_openclaw_audit_child", module_path)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
with module.AuditStateLock(data_dir, timeout_ms=5000):
    ready.write_text("locked\n", encoding="utf-8")
    time.sleep(30)
'''
            process = subprocess.Popen(
                [sys.executable, "-c", child_code, str(MODULE_PATH), str(data_dir), str(ready)],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                deadline = time.monotonic() + 5.0
                while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.05)
                if not ready.exists():
                    stdout, stderr = process.communicate(timeout=2)
                    self.fail(f"lock holder failed to start: stdout={stdout!r} stderr={stderr!r}")

                with self.assertRaises(RuntimeError):
                    with mod.AuditStateLock(data_dir, timeout_ms=150):
                        pass
            finally:
                if process.poll() is None:
                    process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)

            # Kernel advisory ownership must disappear with the holder process;
            # the persistent lock file itself is not a stale-lock authority.
            with mod.AuditStateLock(data_dir, timeout_ms=1000):
                self.assertTrue((data_dir / mod.LOCK_FILENAME).is_file())

    def test_different_data_dirs_do_not_block_each_other(self) -> None:
        with tempfile.TemporaryDirectory() as left, tempfile.TemporaryDirectory() as right:
            with mod.AuditStateLock(Path(left), timeout_ms=1000):
                with mod.AuditStateLock(Path(right), timeout_ms=1000):
                    pass

    @unittest.skipIf(os.name == "nt", "POSIX permission bits are not authoritative on Windows")
    def test_lock_file_is_private_on_posix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock = mod.AuditStateLock(Path(directory), timeout_ms=1000)
            with lock:
                mode = stat.S_IMODE(lock.path.stat().st_mode)
                self.assertEqual(mode & 0o077, 0)


if __name__ == "__main__":
    unittest.main()
