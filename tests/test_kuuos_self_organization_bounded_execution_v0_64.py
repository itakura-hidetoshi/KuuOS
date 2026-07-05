import unittest

from runtime.kuuos_self_organization_bounded_execution_v0_64 import (
    ACTIVE_STATE_PATH,
    EXECUTION_SCOPE,
    SELF_ORGANIZATION_ACTIVE,
    STATE_PUBLICATION_APPLIED,
    active_state_tokens_present,
    failed_steps,
    verify_bounded_execution,
)


class KuuOSSelfOrganizationBoundedExecutionV064Test(unittest.TestCase):
    def test_bounded_execution_verifies(self):
        self.assertEqual((), failed_steps())
        self.assertTrue(verify_bounded_execution())

    def test_active_state_is_published(self):
        self.assertEqual("docs/kuuos_self_organization_active_state.md", ACTIVE_STATE_PATH)
        self.assertEqual("publish_active_self_organization_state", EXECUTION_SCOPE)
        self.assertTrue(SELF_ORGANIZATION_ACTIVE)
        self.assertTrue(STATE_PUBLICATION_APPLIED)
        self.assertTrue(active_state_tokens_present())


if __name__ == "__main__":
    unittest.main()
