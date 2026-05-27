import unittest

from runtime.kuuos_runtime_daemon_qi_counterfactual_probe_lattice_v0_1 import build_qi_counterfactual_probe_lattice


READY_SIM = {
    "simulation_status": "QI_DRY_RUN_PROBE_SIMULATION_READY",
    "simulated_probe_type": "observation_debt_probe",
    "simulated_target_time_slice": "recent_transition_window",
    "simulation_only": True,
    "dry_run_only": True,
    "state_mutation_performed": False,
    "control_packet_mutation_performed": False,
    "memory_write_performed": False,
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


class QiCounterfactualProbeLatticeTests(unittest.TestCase):
    def test_lattice_ranks_chosen_and_unchosen_without_mutation(self):
        lattice = build_qi_counterfactual_probe_lattice(
            dry_run_simulation=READY_SIM,
            trend_summary=READY_SUMMARY,
        )
        self.assertEqual(lattice.lattice_status, "QI_COUNTERFACTUAL_PROBE_LATTICE_READY")
        self.assertEqual(lattice.chosen_probe_type, "observation_debt_probe")
        self.assertGreaterEqual(lattice.candidate_count, 2)
        self.assertTrue(lattice.unchosen_probe_explanations)
        roles = {candidate["candidate_role"] for candidate in lattice.ranked_candidates}
        self.assertIn("chosen_probe", roles)
        self.assertIn("unchosen_counterfactual_probe", roles)
        self.assertTrue(lattice.counterfactual_only)
        self.assertTrue(lattice.simulation_only)
        self.assertTrue(lattice.dry_run_only)
        self.assertFalse(lattice.state_mutation_performed)
        self.assertFalse(lattice.control_packet_mutation_performed)
        self.assertFalse(lattice.memory_write_performed)
        self.assertFalse(lattice.grants_execution_authority)
        self.assertFalse(lattice.grants_probe_execution_authority)
        self.assertFalse(lattice.grants_dry_run_execution_authority)
        self.assertFalse(lattice.grants_next_tick_execution_authority)
        self.assertFalse(lattice.grants_control_packet_authority)
        self.assertFalse(lattice.grants_memory_overwrite_authority)
        self.assertFalse(lattice.grants_world_update_authority)

    def test_blocked_when_simulation_not_ready(self):
        sim = dict(READY_SIM)
        sim["simulation_status"] = "QI_DRY_RUN_PROBE_SIMULATION_BLOCKED"
        lattice = build_qi_counterfactual_probe_lattice(
            dry_run_simulation=sim,
            trend_summary=READY_SUMMARY,
        )
        self.assertEqual(lattice.lattice_status, "QI_COUNTERFACTUAL_PROBE_LATTICE_BLOCKED")
        self.assertIn("dry_run_simulation_not_ready", lattice.lattice_blockers)


if __name__ == "__main__":
    unittest.main()
