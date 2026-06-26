from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_capabilityos_qi_world_kernel_v0_60 import (
    build_capability_path_candidate,
    validate_capability_candidate,
    validate_capability_path_candidate,
)
from runtime.kuuos_capabilityos_qi_world_scenarios_v0_60 import (
    fixture_candidate,
    fixture_definition,
    fixture_qi,
    fixture_world,
    fixture_yin_yang,
    run_capabilityos_qi_world_scenarios,
)


class CapabilityOSV060Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_capabilityos_qi_world_scenarios()
        self.assertEqual("READY_FOR_PLANOS", result["ready_route"])
        self.assertEqual("READY_WITH_WORLD_PLURALITY", result["plural_route"])
        self.assertEqual("CONTAIN_YANG_SATURATION", result["saturation_route"])
        self.assertEqual("QUARANTINE_GUARD_EVIDENCE", result["guard_route"])
        self.assertFalse(result["path_ready"])
        self.assertFalse(result["authority_extended"])

    def test_ready_candidate(self) -> None:
        packet = fixture_candidate()
        self.assertEqual("READY_FOR_PLANOS", packet["disposition"])
        self.assertEqual(3, packet["qi_surface"]["effective_capability_support"])
        self.assertEqual(
            [],
            validate_capability_candidate(
                definition=fixture_definition(), candidate=packet
            ),
        )

    def test_world_plurality_is_preserved(self) -> None:
        packet = fixture_candidate(world_context=fixture_world(plural=True))
        self.assertEqual("READY_WITH_WORLD_PLURALITY", packet["disposition"])
        self.assertTrue(packet["world_context"]["world_disagreement_visible"])
        self.assertEqual(2, packet["world_context"]["applicable_world_count"])

    def test_saturation_generates_containment(self) -> None:
        packet = fixture_candidate(
            yin_yang_receipt=fixture_yin_yang(intensity=7, capacity=5)
        )
        self.assertEqual("CONTAIN_YANG_SATURATION", packet["disposition"])
        self.assertEqual(0, packet["qi_surface"]["effective_capability_support"])

    def test_guard_loss_fails_closed(self) -> None:
        packet = fixture_candidate(
            yin_yang_receipt=fixture_yin_yang(boundary=False)
        )
        self.assertEqual("QUARANTINE_GUARD_EVIDENCE", packet["disposition"])
        self.assertFalse(packet["ready_for_planos_candidate"])

    def test_process_gap_requires_reobservation(self) -> None:
        packet = fixture_candidate(qi_receipt=fixture_qi(ready=False))
        self.assertEqual("REOBSERVE_PROCESS", packet["disposition"])

    def test_missing_verifier_holds(self) -> None:
        packet = fixture_candidate(available_verifiers=[])
        self.assertEqual("HOLD_NO_VERIFIER", packet["disposition"])

    def test_missing_world_precondition_reobserves(self) -> None:
        packet = fixture_candidate(world_context=fixture_world(applicable=False))
        self.assertEqual("REOBSERVE_WORLD_PRECONDITION", packet["disposition"])

    def test_candidate_tamper_is_detected(self) -> None:
        packet = fixture_candidate()
        tampered = deepcopy(packet)
        tampered["non_authority"]["grants_execution_authority"] = True
        errors = validate_capability_candidate(
            definition=fixture_definition(), candidate=tampered
        )
        self.assertIn("candidate_authority_expansion", errors)
        self.assertIn("candidate_digest_invalid", errors)

    def test_path_uses_guard_meet_and_impediment_join(self) -> None:
        ready = fixture_candidate()
        held = fixture_candidate(available_verifiers=[])
        path = build_capability_path_candidate(
            path_id="path", candidates=[ready, held]
        )
        self.assertFalse(path["path_ready_for_planos_candidate"])
        self.assertEqual(0, path["effective_path_support"])
        self.assertEqual([], validate_capability_path_candidate(path))


if __name__ == "__main__":
    unittest.main()
