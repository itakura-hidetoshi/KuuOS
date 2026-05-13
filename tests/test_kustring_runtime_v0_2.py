#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "kustring_runtime_v0_2.py"

spec = importlib.util.spec_from_file_location("kustring_runtime_v0_2", MODULE_PATH)
runtime = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(runtime)


class TestKuStringRuntimeV02(unittest.TestCase):
    def test_default_packet_is_candidate(self) -> None:
        out = runtime.evaluate(runtime.Packet())
        self.assertEqual(out["status"], "CANDIDATE")
        self.assertEqual(out["gap"], "33/20")
        self.assertFalse(out["execution_authority_granted"])

    def test_k_objectification_is_rejected(self) -> None:
        out = runtime.evaluate(runtime.Packet(k_object=True))
        self.assertEqual(out["status"], "REJECT")

    def test_gap_must_be_on_kperp(self) -> None:
        out = runtime.evaluate(runtime.Packet(gap_domain="K"))
        self.assertEqual(out["status"], "REJECT")

    def test_centered_observable_required(self) -> None:
        out = runtime.evaluate(runtime.Packet(observable_centered=False))
        self.assertEqual(out["status"], "HOLD")


if __name__ == "__main__":
    unittest.main()
