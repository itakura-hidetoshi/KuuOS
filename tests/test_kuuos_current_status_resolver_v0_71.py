import json
import unittest

from runtime.kuuos_current_status_resolver_v0_71 import (
    resolved_status,
    resolved_status_json,
    resolver_issues,
    verify_resolver,
)


class KuuOSCurrentStatusResolverV071Test(unittest.TestCase):
    def test_resolver_verifies(self):
        self.assertEqual((), resolver_issues())
        self.assertTrue(verify_resolver())

    def test_resolved_status_has_expected_layers(self):
        status = resolved_status()
        self.assertEqual("v0.71", status["resolver_schema_version"])
        self.assertEqual("kuuos_current_status_resolver_v0_71", status["resolver_frontier"])
        self.assertEqual("runtime/kuuos_current_status.py", status["stable_entrypoint"])
        self.assertTrue(status["pointer_verified"])
        self.assertTrue(status["status_index_verified"])
        self.assertTrue(status["snapshot_verified"])
        self.assertEqual("resolver_not_authority_grant", status["authority_boundary"])

    def test_resolved_status_follows_pointer_to_snapshot(self):
        status = resolved_status()
        self.assertEqual(
            "status/kuuos_status_index_v0_69.json",
            status["current_pointer"]["current_status_index"],
        )
        self.assertEqual(
            "status/kuuos_self_organization_status_v0_68.json",
            status["current_status_index"]["latest_self_organization_snapshot"],
        )
        self.assertTrue(status["current_status_snapshot"]["active"])

    def test_resolved_status_json_round_trips(self):
        self.assertEqual(resolved_status(), json.loads(resolved_status_json()))


if __name__ == "__main__":
    unittest.main()
