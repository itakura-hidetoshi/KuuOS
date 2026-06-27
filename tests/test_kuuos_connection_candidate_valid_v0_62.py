import unittest

from runtime.kuuos_connection_candidate_receipt_v0_62 import evaluate_connection_candidate
from runtime.kuuos_discrete_gauge_connection_v0_60 import KuuConnection
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import AssociatedField, SignedPermutation
from runtime.kuuos_os_curvature_holonomy_v0_61 import OSGaugeBundle
from runtime.kuuos_os_gauge_field_types_v0_61 import ChannelPreservingGaugeGroup, OSAssociatedGaugeField, os_field_values


class ValidConnectionCandidateV062(unittest.TestCase):
    def test_valid_candidate(self):
        group = ChannelPreservingGaugeGroup()
        identity = group.identity()
        swap = SignedPermutation((0,1,2,3,5,4,6,8,7,10,9,11), (1,) * 12)
        values = os_field_values(evidence_support=.9, uncertainty=.1, contradiction=.2, criterion_coverage=.8, verification_debt=0, history_depth=.6, residue_load=.2, predictive_uncertainty=.3)
        fields = {}
        for role in ("observe", "verify", "memory"):
            local = AssociatedField(role, role, values, role + "OS", "read_only", role + "-source")
            fields[role] = OSAssociatedGaugeField(role, role + "-version", role + "-source", role + "-boundary", local)
        source = KuuConnection(group, {("observe","verify"):swap, ("verify","memory"):swap, ("memory","observe"):identity})
        flat = KuuConnection(group, {("observe","verify"):identity, ("verify","memory"):identity, ("memory","observe"):identity})
        receipt = evaluate_connection_candidate(OSGaugeBundle(group, source, fields), flat)
        self.assertTrue(receipt.admissible)
        self.assertTrue(receipt.curvature_strictly_decreased)
        self.assertTrue(receipt.protected_holonomy_observables_preserved)
        self.assertFalse(receipt.state_write_performed)


if __name__ == "__main__":
    unittest.main()
