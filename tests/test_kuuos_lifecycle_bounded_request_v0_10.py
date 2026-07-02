from __future__ import annotations

import unittest

from runtime.kuuos_lifecycle_request_audit_conflict_v0_10 import (
    conflict_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_determinism_v0_10 import (
    determinism_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_governance_v0_10 import (
    governance_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_identity_v0_10 import (
    identity_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_integrity_v0_10 import (
    integrity_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_policy_scope_v0_10 import (
    policy_scope_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_roles_v0_10 import (
    role_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_safety_v0_10 import (
    safety_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_source_status_v0_10 import (
    source_status_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_temporal_v0_10 import (
    temporal_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_valid_v0_10 import (
    valid_audit_matrix,
)
from runtime.kuuos_lifecycle_request_audit_verification_v0_10 import (
    verification_audit_matrix,
)


class LifecycleBoundedRequestV010Tests(unittest.TestCase):
    def test_complete_audit_matrix(self) -> None:
        checks = {
            **valid_audit_matrix(),
            **source_status_audit_matrix(),
            **integrity_audit_matrix(),
            **identity_audit_matrix(),
            **role_audit_matrix(),
            **policy_scope_audit_matrix(),
            **governance_audit_matrix(),
            **conflict_audit_matrix(),
            **safety_audit_matrix(),
            **temporal_audit_matrix(),
            **verification_audit_matrix(),
            **determinism_audit_matrix(),
        }
        failures = sorted(name for name, passed in checks.items() if not passed)
        self.assertFalse(failures, f"failed lifecycle request checks: {failures}")
        self.assertEqual(len(checks), 20)


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=2).result
    raise SystemExit(0 if result.wasSuccessful() else 1)
