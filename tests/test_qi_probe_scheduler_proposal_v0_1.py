import unittest

from runtime.kuuos_runtime_daemon_qi_probe_scheduler_proposal_v0_1 import build_qi_probe_scheduler_proposal


READY_LATTICE = {
    "lattice_status": "QI_COUNTERFACTUAL_PROBE_LATTICE_READY",
    "recommended_probe_type": "observation_debt_probe",
    "chosen_probe_type": "observation_debt_probe",
    "counterfactual_only": True,
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


class QiProbeSchedulerProposalTests(unittest.TestCase):
    def test_ready_proposal_is_non_mutating(self):
        proposal = build_qi_probe_scheduler_proposal(counterfactual_lattice=READY_LATTICE)
        self.assertEqual(proposal.scheduler_status, "QI_PROBE_SCHEDULER_PROPOSAL_READY")
        self.assertEqual(proposal.recommended_schedule_mode, "near_term_revisit")
        self.assertEqual(proposal.recommended_revisit_after_ticks, 1)
        self.assertTrue(proposal.schedule_proposal_only)
        self.assertTrue(proposal.counterfactual_only)
        self.assertTrue(proposal.simulation_only)
        self.assertTrue(proposal.dry_run_only)
        self.assertFalse(proposal.scheduler_mutation_performed)
        self.assertFalse(proposal.control_packet_mutation_performed)
        self.assertFalse(proposal.memory_write_performed)
        self.assertEqual(proposal.authority, "none")
        self.assertFalse(proposal.grants_execution_authority)
        self.assertFalse(proposal.grants_probe_execution_authority)
        self.assertFalse(proposal.grants_dry_run_execution_authority)
        self.assertFalse(proposal.grants_next_tick_execution_authority)
        self.assertFalse(proposal.grants_scheduler_authority)
        self.assertFalse(proposal.grants_control_packet_authority)
        self.assertFalse(proposal.grants_memory_overwrite_authority)
        self.assertFalse(proposal.grants_world_update_authority)

    def test_blocked_when_lattice_not_ready(self):
        lattice = dict(READY_LATTICE)
        lattice["lattice_status"] = "QI_COUNTERFACTUAL_PROBE_LATTICE_BLOCKED"
        proposal = build_qi_probe_scheduler_proposal(counterfactual_lattice=lattice)
        self.assertEqual(proposal.scheduler_status, "QI_PROBE_SCHEDULER_PROPOSAL_BLOCKED")
        self.assertIn("counterfactual_lattice_not_ready", proposal.scheduler_blockers)
        self.assertIsNone(proposal.recommended_schedule_mode)


if __name__ == "__main__":
    unittest.main()
