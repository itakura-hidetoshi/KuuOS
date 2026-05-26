import unittest

from runtime.kuuos_runtime_daemon_qi_dry_run_probe_simulator_v0_1 import build_qi_dry_run_probe_simulation


READY_LICENSE = {
    "gate_status": "QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY",
    "candidate_license_kind": "dry_run_probe_simulation_candidate",
    "license_candidate_only": True,
    "dry_run_candidate_only": True,
    "authority": "none",
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
}

READY_SUMMARY = {
    "summary_status": "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY",
    "summary_only": True,
    "read_only": True,
    "latest_recommended_probe_type": "observation_debt_probe",
    "latest_probe_target_time_slice": "recent_transition_window",
    "authority": "none",
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
}


class QiDryRunProbeSimulatorTests(unittest.TestCase):
    def test_ready_simulation_is_non_mutating(self):
        sim = build_qi_dry_run_probe_simulation(
            license_candidate=READY_LICENSE,
            trend_summary=READY_SUMMARY,
        )
        self.assertEqual(sim.simulation_status, "QI_DRY_RUN_PROBE_SIMULATION_READY")
        self.assertEqual(sim.simulated_probe_type, "observation_debt_probe")
        self.assertTrue(sim.simulation_only)
        self.assertTrue(sim.dry_run_only)
        self.assertFalse(sim.state_mutation_performed)
        self.assertFalse(sim.control_packet_mutation_performed)
        self.assertFalse(sim.memory_write_performed)
        self.assertFalse(sim.grants_execution_authority)
        self.assertFalse(sim.grants_probe_execution_authority)
        self.assertFalse(sim.grants_dry_run_execution_authority)
        self.assertFalse(sim.grants_next_tick_execution_authority)
        self.assertFalse(sim.grants_control_packet_authority)
        self.assertFalse(sim.grants_memory_overwrite_authority)
        self.assertFalse(sim.grants_world_update_authority)

    def test_missing_license_blocks_simulation(self):
        sim = build_qi_dry_run_probe_simulation(
            license_candidate={},
            trend_summary=READY_SUMMARY,
        )
        self.assertEqual(sim.simulation_status, "QI_DRY_RUN_PROBE_SIMULATION_BLOCKED")
        self.assertIn("license_candidate_not_ready", sim.simulation_blockers)


if __name__ == "__main__":
    unittest.main()
