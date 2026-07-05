import json
import unittest

from runtime.kuuos_self_organization_status_v0_67 import (
    build_status,
    status_issues,
    status_json,
    verify_status,
)


class KuuOSSelfOrganizationStatusV067Test(unittest.TestCase):
    def test_status_verifies(self):
        self.assertEqual((), status_issues())
        self.assertTrue(verify_status())

    def test_status_payload_is_machine_readable(self):
        status = build_status()
        self.assertEqual("v0.67", status["status_schema_version"])
        self.assertEqual("kuuos_self_organization_status", status["status_command"])
        self.assertTrue(status["active"])
        self.assertEqual(
            "docs/kuuos_self_organization_active_state.md",
            status["active_state_path"],
        )
        self.assertEqual(
            "kuuos_self_organization_bounded_execution_v0_64",
            status["active_state_frontier"],
        )
        self.assertEqual("kuuos_current_root_sequence_v0_66", status["current_root_sequence"])
        self.assertTrue(status["bounded_execution_verified"])
        self.assertTrue(status["current_root_sequence_verified"])
        self.assertTrue(status["public_status_checked"])
        self.assertEqual("active_state_not_unbounded_authority", status["authority_boundary"])

    def test_status_json_round_trips(self):
        payload = json.loads(status_json())
        self.assertEqual(build_status(), payload)


if __name__ == "__main__":
    unittest.main()
