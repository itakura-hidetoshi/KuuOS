from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_integrated_long_duration_operation_kernel_v0_27 import (
    build_cycle_receipt,
    build_initial_state,
    build_integrated_operation_contract,
    validate_contract,
    validate_state,
)
from runtime.kuuos_integrated_long_duration_operation_scenarios_v0_27 import (
    run_integrated_long_duration_operation_scenarios,
)
from runtime.kuuos_integrated_long_duration_operation_types_v0_27 import (
    LOWER_COMPONENTS,
)


def lower_digests(label: str) -> dict[str, str]:
    return {component: sha(f"{label}:{component}") for component in LOWER_COMPONENTS}


class IntegratedLongDurationOperationV027Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_integrated_long_duration_operation_scenarios()
        self.assertEqual(
            "KUUOS_INTEGRATED_LONG_DURATION_OPERATION_V0_27_OK",
            result["status"],
        )
        self.assertEqual(7, result["completed_cycles"])
        self.assertEqual(1, result["lease_sequence"])
        self.assertEqual(1, result["process_epoch"])
        self.assertEqual(1, result["host_epoch"])
        self.assertEqual("RENEWAL_REQUIRED", result["repeatable_route"])
        self.assertEqual("TERMINATED", result["terminate_route"])
        self.assertEqual("HANDED_OVER", result["handover_route"])
        self.assertEqual("REPLAYED", result["replay_status"])
        self.assertEqual("REJECTED", result["stale_status"])
        self.assertTrue(result["foreground_control_available"])
        self.assertFalse(result["automatic_renewal"])
        self.assertFalse(result["automatic_resume"])
        self.assertFalse(result["authority_extended"])

    def test_contract_binds_all_lower_components(self) -> None:
        contract = build_integrated_operation_contract(
            contract_id="contract",
            mission_id="mission",
            lineage_id="lineage",
            lower_contract_digests=lower_digests("contract"),
            initial_host_license_digest=sha("host-license"),
            max_cycle_cost=10,
            max_cycle_steps=10,
            max_cycle_duration_ms=1_000,
            max_lease_cycles=3,
            max_lease_cost=30,
            initial_lease_id="lease-0",
            initial_lease_cycles=3,
            initial_lease_cost=30,
            initial_lease_expires_at_ms=10_000,
            user_control_policy_digest=sha("control"),
            recovery_policy_digest=sha("recovery"),
            audit_policy_digest=sha("audit"),
            created_at_ms=1,
        )
        self.assertEqual([], validate_contract(contract))
        self.assertEqual(set(LOWER_COMPONENTS), set(contract["lower_contract_digests"]))
        self.assertFalse(contract["automatic_renewal"])
        self.assertTrue(contract["finite_cycle_contract"])
        self.assertTrue(contract["finite_lease_contract"])

    def test_cycle_requires_exact_host_license(self) -> None:
        contract = build_integrated_operation_contract(
            contract_id="contract-host",
            mission_id="mission-host",
            lineage_id="lineage-host",
            lower_contract_digests=lower_digests("contract-host"),
            initial_host_license_digest=sha("host-license-canonical"),
            max_cycle_cost=10,
            max_cycle_steps=10,
            max_cycle_duration_ms=1_000,
            max_lease_cycles=2,
            max_lease_cost=20,
            initial_lease_id="lease-host",
            initial_lease_cycles=2,
            initial_lease_cost=20,
            initial_lease_expires_at_ms=10_000,
            user_control_policy_digest=sha("control-host"),
            recovery_policy_digest=sha("recovery-host"),
            audit_policy_digest=sha("audit-host"),
            created_at_ms=1,
        )
        state = build_initial_state(contract=contract, initialized_at_ms=2)
        with self.assertRaisesRegex(ValueError, "cycle_host_license_mismatch"):
            build_cycle_receipt(
                state=state,
                cycle_id="cycle-host",
                lower_cycle_receipt_digests=lower_digests("cycle-host"),
                cycle_authorization_digest=sha("cycle-authority"),
                host_license_digest=sha("substituted-host-license"),
                cycle_cost=5,
                cycle_steps=5,
                started_at_ms=3,
                completed_at_ms=100,
                route="CONTINUE",
                checkpoint_digest=sha("checkpoint"),
            )

    def test_state_rejects_authority_expansion(self) -> None:
        contract = build_integrated_operation_contract(
            contract_id="contract-tamper",
            mission_id="mission-tamper",
            lineage_id="lineage-tamper",
            lower_contract_digests=lower_digests("contract-tamper"),
            initial_host_license_digest=sha("host-license"),
            max_cycle_cost=10,
            max_cycle_steps=10,
            max_cycle_duration_ms=1_000,
            max_lease_cycles=2,
            max_lease_cost=20,
            initial_lease_id="lease-tamper",
            initial_lease_cycles=2,
            initial_lease_cost=20,
            initial_lease_expires_at_ms=10_000,
            user_control_policy_digest=sha("control"),
            recovery_policy_digest=sha("recovery"),
            audit_policy_digest=sha("audit"),
            created_at_ms=1,
        )
        state = build_initial_state(contract=contract, initialized_at_ms=2)
        tampered = deepcopy(state)
        tampered["non_authority"]["extends_existing_authority"] = True
        self.assertIn("integrated_state_authority_expansion", validate_state(tampered))

    def test_initial_lease_must_be_finite(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "initial_lease_cycles_above_contract_cap"
        ):
            build_integrated_operation_contract(
                contract_id="contract-invalid",
                mission_id="mission-invalid",
                lineage_id="lineage-invalid",
                lower_contract_digests=lower_digests("contract-invalid"),
                initial_host_license_digest=sha("host-license"),
                max_cycle_cost=10,
                max_cycle_steps=10,
                max_cycle_duration_ms=1_000,
                max_lease_cycles=2,
                max_lease_cost=20,
                initial_lease_id="lease-invalid",
                initial_lease_cycles=3,
                initial_lease_cost=20,
                initial_lease_expires_at_ms=10_000,
                user_control_policy_digest=sha("control"),
                recovery_policy_digest=sha("recovery"),
                audit_policy_digest=sha("audit"),
                created_at_ms=1,
            )


if __name__ == "__main__":
    unittest.main()
