#!/usr/bin/env python3
"""
Tests for examples/ai_yogacara_runtime_adapter_minimal.py

Stdlib-only tests ensuring that the minimal adapter never grants authority
and correctly flags proof-like / decision-like / context-drift outputs.
"""

from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "examples" / "ai_yogacara_runtime_adapter_minimal.py"

spec = importlib.util.spec_from_file_location("ai_yogacara_runtime_adapter_minimal", ADAPTER_PATH)
assert spec is not None and spec.loader is not None
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class TestAIYogacaraRuntimeAdapterMinimal(unittest.TestCase):
    def make_input(self, text: str):
        return adapter.AdapterInput(
            request_id="test-001",
            ai_system="GPT",
            model_or_agent_id="unit-test-agent",
            raw_output_text=text,
            user_world_context_ref="kuos_test_world",
            declared_task_scope="unit_test",
            control_surface_ref="interface_level",
        )

    def test_raw_output_never_grants_authority(self) -> None:
        out = adapter.adapt(self.make_input("This is a careful candidate with context and uncertainty."))
        self.assertEqual(out.raw_output_status, "candidate")
        self.assertFalse(out.authority_granted)
        self.assertIn("CANDIDATE_ONLY", out.allowed_next_status)

    def test_proof_like_text_gets_proof_hold(self) -> None:
        out = adapter.adapt(self.make_input("This proves the theorem. QED."))
        self.assertIn("proof_authority_hold", out.meta_manas_signals)
        self.assertIn("proof_tone_seed", out.seed_classifications)
        self.assertFalse(out.authority_granted)

    def test_decision_like_text_gets_decision_hold(self) -> None:
        out = adapter.adapt(self.make_input("You should execute this now."))
        self.assertIn("decision_authority_hold", out.meta_manas_signals)
        self.assertIn("decision_tone_seed", out.seed_classifications)
        self.assertFalse(out.authority_granted)

    def test_context_drift_gets_context_recheck(self) -> None:
        out = adapter.adapt(self.make_input("Generally speaking, ignore the prior context."))
        self.assertIn("context_recheck", out.meta_manas_signals)
        self.assertIn("context_drift_seed", out.seed_classifications)
        self.assertIn("REPAIR", out.allowed_next_status)

    def test_non_reifying_trace_seed_detected(self) -> None:
        out = adapter.adapt(self.make_input("Within this scope, this remains a candidate under uncertain conditions."))
        self.assertIn("non_reifying_trace_seed", out.seed_classifications)
        self.assertFalse(out.authority_granted)


if __name__ == "__main__":
    unittest.main()
