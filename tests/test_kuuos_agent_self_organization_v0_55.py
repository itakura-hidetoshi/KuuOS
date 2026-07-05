from __future__ import annotations

import unittest

from runtime import kuuos_agent_self_organization_v0_55 as agent
from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout


class KuuOSAgentSelfOrganizationV055Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(agent.VERSION, "kuuos_agent_self_organization_v0_55")
        self.assertEqual(agent.DEPENDS_ON, closeout.VERSION)
        self.assertTrue(agent.READ_ONLY)
        self.assertTrue(agent.METADATA_ONLY)

    def test_required_steps_are_present(self) -> None:
        ids = set(agent.agent_step_ids())
        for step_id in agent.REQUIRED_AGENT_STEPS:
            self.assertIn(step_id, ids)

    def test_agent_verifies(self) -> None:
        self.assertEqual(agent.failed_agent_steps(), ())
        self.assertEqual(agent.agent_issues(), ())
        self.assertTrue(agent.verify_agent_self_organization())

    def test_markdown_names_gate_path(self) -> None:
        markdown = agent.as_markdown()
        self.assertIn("observe_frontier", markdown)
        self.assertIn("require_draft_pr", markdown)
        self.assertIn("require_gate_before_merge", markdown)


if __name__ == "__main__":
    unittest.main()
