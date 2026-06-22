from __future__ import annotations

from copy import deepcopy
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_operational_agent_adapter_contract_v1_1 import (
    DeterministicStagedAdapter,
)
from runtime.kuuos_operational_agent_capability_registry_v1_1 import CapabilityRegistry
from runtime.kuuos_operational_agent_lease_ledger_v1_1 import (
    JsonlExecutionLeaseUsageLedger,
)
from runtime.kuuos_operational_agent_receipt_store_v1_1 import (
    JsonlAppendOnlyReceiptStore,
)
from runtime.kuuos_operational_agent_scenarios_v1_1 import (
    _run,
    build_fixture,
    run_external_commit_hold,
    run_nominal_scenario,
    run_replay_hold,
    run_stale_epoch_hold,
)
from runtime.kuuos_operational_agent_types_v1_1 import sha


class OperationalAgentControllerV11Tests(unittest.TestCase):
    def test_nominal_cycle_closes_without_external_commit(self) -> None:
        result = run_nominal_scenario()
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["state"]["task_stage"], "PLAN")
        self.assertFalse(result["state"]["execution_allowed"])
        self.assertFalse(result["external_commit_performed"])
        self.assertTrue(result["observation"]["independent_from_adapter"])
        self.assertTrue(result["learning"]["future_only"])

    def test_external_commit_stops_before_adapter(self) -> None:
        result = run_external_commit_hold()
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["recovery_decision"], "REQUEST_HUMAN")
        self.assertFalse(result["adapter_invoked"])
        self.assertFalse(result["external_commit_performed"])

    def test_stale_epoch_routes_to_rerotation(self) -> None:
        result = run_stale_epoch_hold()
        self.assertEqual(result["recovery_decision"], "REROTATE")
        self.assertEqual(result["state"]["control_mode"], "SUSPENDED")

    def test_replayed_intent_is_not_reexecuted(self) -> None:
        result = run_replay_hold()
        self.assertEqual(result["recovery_decision"], "REVALIDATE")
        self.assertFalse(result["adapter_invoked"])

    def test_capability_identifier_cannot_be_reused(self) -> None:
        fixture = build_fixture(label="cap-reuse")
        registry = CapabilityRegistry()
        registry.register(fixture["capability"])
        with self.assertRaisesRegex(ValueError, "capability_id_reuse_forbidden"):
            registry.register(fixture["capability"])

    def test_adapter_external_commit_claim_is_quarantined(self) -> None:
        fixture = build_fixture(label="malicious")

        class MaliciousAdapter(DeterministicStagedAdapter):
            def stage(self, intent):
                value = super().stage(intent)
                value["external_commit_performed"] = True
                value["adapter_result_digest"] = sha(
                    {
                        key: item
                        for key, item in value.items()
                        if key != "adapter_result_digest"
                    }
                )
                return value

        fixture["adapter"] = MaliciousAdapter()
        result = _run(fixture)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["recovery_decision"], "ABORT")
        self.assertTrue(result["adapter_invoked"])
        self.assertFalse(result["external_commit_performed"])
        self.assertEqual(result["state"]["control_mode"], "SUSPENDED")

    def test_jsonl_receipts_reload_and_detect_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipts.jsonl"
            store = JsonlAppendOnlyReceiptStore(
                same_root_id="kuuos-main-root", path=path
            )
            store.append(record_type="A", payload={"value": 1})
            store.append(record_type="B", payload={"value": 2})
            reloaded = JsonlAppendOnlyReceiptStore(
                same_root_id="kuuos-main-root", path=path
            )
            self.assertEqual(reloaded.validate(), [])
            lines = path.read_text(encoding="utf-8").splitlines()
            lines[0] = lines[0].replace('"value":1', '"value":9')
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "receipt_chain_invalid"):
                JsonlAppendOnlyReceiptStore(
                    same_root_id="kuuos-main-root", path=path
                )

    def test_jsonl_usage_reservation_survives_restart(self) -> None:
        fixture = build_fixture(label="restart", max_uses=2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "usage.jsonl"
            ledger = JsonlExecutionLeaseUsageLedger(path)
            ledger.reserve(
                lease=fixture["lease"],
                intent=fixture["intent"],
                session_digest=fixture["state"]["active_session_digest"],
            )
            restarted = JsonlExecutionLeaseUsageLedger(path)
            self.assertIn(
                "intent_replay_forbidden",
                restarted.can_consume(fixture["lease"], fixture["intent"]),
            )

    def test_invalid_adaptive_state_fails_closed_without_transition(self) -> None:
        fixture = build_fixture(label="invalid-state")
        fixture["state"] = deepcopy(fixture["state"])
        fixture["state"]["adaptive_control_state_digest"] = "tampered"
        result = _run(fixture)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["recovery_decision"], "ABORT")
        self.assertFalse(result["adapter_invoked"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
